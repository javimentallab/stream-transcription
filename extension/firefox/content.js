// Firefox capture engine. Firefox has no tabCapture, so the audio is taken from the
// page's <video>/<audio> elements with createMediaElementSource.
//
// Caveat that shapes this file: an element accepts ONE MediaElementSource in its whole
// life (spec). Building a second AudioContext on the same <video> throws and leaves it
// muted for good, so the graph is built once per page and reused by later sessions; if
// the context stops rendering, it can only be resumed, not rebuilt.
"use strict";

(function () {
  if (window.__stEngine) return;
  window.__stEngine = true;

  const WORKLET_URL = browser.runtime.getURL("audiopreprocessor.js");
  const AUDIO_STALL_MS = 4000;

  let audioContext = null;
  let workletNode = null;
  const hooked = new WeakSet();
  let session = null;
  let lastAudioAt = 0;
  let watchdog = null;
  let stalled = false;
  let observer = null;

  function emit(msg) {
    browser.runtime.sendMessage(Object.assign({ from: "engine" }, msg)).catch(() => {});
  }

  function mediaElements() {
    return Array.from(document.querySelectorAll("video, audio"));
  }

  function anyPlaying() {
    return mediaElements().some((el) => !el.paused && !el.ended && el.readyState > 2);
  }

  function hook(el) {
    if (hooked.has(el) || !audioContext) return;
    let src;
    try {
      src = audioContext.createMediaElementSource(el);
    } catch (e) {
      // Already owned by an earlier engine (the extension was reloaded with the page
      // open). Only a page reload frees it.
      console.warn("[stream-transcription] can't capture this element:", e);
      return;
    }
    hooked.add(el);
    src.connect(workletNode);
    src.connect(audioContext.destination);   // what you hear
  }

  async function ensureGraph() {
    if (audioContext) {
      if (audioContext.state !== "running") await audioContext.resume().catch(() => {});
      return;
    }
    audioContext = new AudioContext();
    audioContext.onstatechange = () => {
      if (audioContext && (audioContext.state === "suspended" || audioContext.state === "interrupted")) {
        audioContext.resume().catch(() => {});
      }
    };
    await audioContext.audioWorklet.addModule(WORKLET_URL);
    workletNode = new AudioWorkletNode(audioContext, "audiopreprocessor");
    // The source already goes straight to the speakers; the worklet's own output (a
    // copy of its input) goes through a muted gain so the audio isn't played twice.
    const sink = audioContext.createGain();
    sink.gain.value = 0;
    workletNode.connect(sink);
    sink.connect(audioContext.destination);
    workletNode.port.onmessage = (ev) => {
      lastAudioAt = Date.now();
      if (stalled) {
        stalled = false;
        session && session.setState(session.hasText ? "live" : (session.ready ? "listening" : "loading"));
      }
      if (session && anyPlaying()) session.sendAudio(ev.data);
    };
  }

  function checkAudio() {
    if (!session || session.closed || !audioContext) return;
    if (!anyPlaying()) { lastAudioAt = Date.now(); return; }   // paused: nothing to send
    if (Date.now() - lastAudioAt < AUDIO_STALL_MS) return;
    if (audioContext.state !== "running") {
      audioContext.resume().then(() => { lastAudioAt = Date.now(); }).catch(() => {});
      return;
    }
    if (!stalled) {
      stalled = true;
      session.setState("stalled");
    }
  }

  async function start(msg) {
    stop();
    const els = mediaElements();
    if (!els.length) {
      emit({ evt: "state", state: "error", error: "no_media" });
      return;
    }
    try {
      await ensureGraph();
      els.forEach(hook);
    } catch (e) {
      console.error("[stream-transcription] audio setup failed", e);
      emit({ evt: "state", state: "error", error: "capture" });
      return;
    }
    // Players that swap their <video> element (ads, quality changes) get hooked too.
    observer = new MutationObserver(() => mediaElements().forEach(hook));
    observer.observe(document.documentElement, { childList: true, subtree: true });

    session = new Engine.Session({
      serverUrl: msg.serverUrl, options: msg.options, translating: msg.translating, emit,
    });
    session.connect();
    lastAudioAt = Date.now();
    watchdog = setInterval(checkAudio, 2000);
    navigator.mediaDevices && navigator.mediaDevices.addEventListener("devicechange", onDeviceChange);
  }

  function onDeviceChange() {
    if (audioContext && audioContext.state !== "running") audioContext.resume().catch(() => {});
    setTimeout(checkAudio, 1000);
    setTimeout(checkAudio, 2500);
  }

  function stop() {
    if (watchdog) clearInterval(watchdog);
    watchdog = null;
    if (observer) observer.disconnect();
    observer = null;
    navigator.mediaDevices && navigator.mediaDevices.removeEventListener("devicechange", onDeviceChange);
    if (session) session.close();
    session = null;
    stalled = false;
    // The audio graph stays: see the caveat at the top.
  }

  browser.runtime.onMessage.addListener((msg) => {
    if (!msg || msg.st !== "engine") return;
    if (msg.cmd === "ping") return Promise.resolve({ alive: true, capturing: !!(session && !session.closed) });
    if (msg.cmd === "start") start(msg);
    if (msg.cmd === "stop") stop();
  });

  emit({ evt: "hello" });
})();
