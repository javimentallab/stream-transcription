// Chromium capture engine, running in an offscreen document: gets the tab audio from
// tabCapture, plays it back (capturing mutes the tab), downsamples it to 16 kHz in an
// AudioWorklet and streams it to the server.
"use strict";

const WORKLET_URL = chrome.runtime.getURL("audiopreprocessor.js");
const AUDIO_STALL_MS = 4000;
const WATCHDOG_EVERY_MS = 2000;

let stream = null;
let audioContext = null;
let workletNode = null;
let session = null;
let lastAudioAt = 0;
let watchdog = null;
let rebuilding = false;
let stalled = false;

function emit(msg) {
  chrome.runtime.sendMessage(Object.assign({ from: "engine" }, msg)).catch(() => {});
}

async function buildGraph() {
  audioContext = new AudioContext();
  if (audioContext.state === "suspended") await audioContext.resume();
  // An output device change (e.g. moving the window to a screen with HDMI audio) can
  // leave the context suspended: wake it up.
  audioContext.onstatechange = () => {
    if (audioContext && (audioContext.state === "suspended" || audioContext.state === "interrupted")) {
      audioContext.resume().catch(() => {});
    }
  };
  await audioContext.audioWorklet.addModule(WORKLET_URL);
  workletNode = new AudioWorkletNode(audioContext, "audiopreprocessor");
  audioContext.createMediaStreamSource(stream).connect(workletNode);
  // The worklet copies its input to its output: this connection is what keeps the tab
  // audible, and it is also what makes the worklet run at all.
  workletNode.connect(audioContext.destination);
  workletNode.port.onmessage = (ev) => {
    lastAudioAt = Date.now();
    if (stalled) {
      stalled = false;
      session && session.setState(session.hasText ? "live" : (session.ready ? "listening" : "loading"));
    }
    session && session.sendAudio(ev.data);
  };
}

async function teardownGraph() {
  if (workletNode) {
    workletNode.port.onmessage = null;
    try { workletNode.disconnect(); } catch (e) { /* ignore */ }
    workletNode = null;
  }
  if (audioContext) {
    audioContext.onstatechange = null;
    try { await audioContext.close(); } catch (e) { /* ignore */ }
    audioContext = null;
  }
}

// The worklet only runs while the sound card clock drives the graph. When Windows
// reconfigures audio endpoints the context can stop rendering without any error and the
// subtitles freeze. Detect it and resume, or rebuild the graph on the same stream.
async function checkAudio() {
  if (rebuilding || !audioContext || !session || session.closed) return;
  const silent = Date.now() - lastAudioAt;
  if (silent < AUDIO_STALL_MS) return;
  if (audioContext.state !== "running") {
    audioContext.resume().then(() => { lastAudioAt = Date.now(); }).catch(() => rebuild());
    return;
  }
  rebuild();
}

async function rebuild() {
  if (rebuilding || !stream) return;
  if (!stream.getAudioTracks().some((t) => t.readyState === "live")) {
    stalled = true;
    session && session.setState("stalled");
    return;
  }
  rebuilding = true;
  try {
    await teardownGraph();
    await buildGraph();
    lastAudioAt = Date.now();
  } catch (e) {
    console.error("[stream-transcription] could not rebuild the audio graph", e);
    stalled = true;
    session && session.setState("stalled");
  } finally {
    rebuilding = false;
  }
}

function onDeviceChange() {
  setTimeout(checkAudio, 1000);
  setTimeout(checkAudio, 2500);
}

async function start(msg) {
  await stop();
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      audio: { mandatory: { chromeMediaSource: "tab", chromeMediaSourceId: msg.streamId } },
      video: false,
    });
  } catch (e) {
    console.error("[stream-transcription] tab capture failed", e);
    emit({ evt: "state", state: "error", error: "capture" });
    return;
  }
  stream.getAudioTracks().forEach((t) => {
    t.onended = () => { if (session && !session.closed) session.setState("error", { error: "capture" }); };
  });

  session = new Engine.Session({
    serverUrl: msg.serverUrl, options: msg.options, translating: msg.translating, emit,
  });
  try {
    await buildGraph();
  } catch (e) {
    console.error("[stream-transcription] audio setup failed", e);
    emit({ evt: "state", state: "error", error: "capture" });
    return;
  }
  session.connect();
  lastAudioAt = Date.now();
  watchdog = setInterval(checkAudio, WATCHDOG_EVERY_MS);
  navigator.mediaDevices.addEventListener("devicechange", onDeviceChange);
}

async function stop() {
  if (watchdog) clearInterval(watchdog);
  watchdog = null;
  navigator.mediaDevices.removeEventListener("devicechange", onDeviceChange);
  if (session) session.close();
  session = null;
  await teardownGraph();
  if (stream) stream.getTracks().forEach((t) => t.stop());
  stream = null;
  stalled = false;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg || msg.target !== "offscreen") return;
  if (msg.cmd === "start") start(msg);
  else if (msg.cmd === "stop") stop();
  sendResponse({});
});
