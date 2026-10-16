// Pieces of the capture engine shared by Chromium (offscreen document + service worker)
// and Firefox (content script + background page).
"use strict";

var Engine = globalThis.Engine || {};
globalThis.Engine = Engine;

Engine.ACTIVE = ["connecting", "loading", "listening", "live", "stalled", "noresponse"];

// No subtitles for this long while there IS sound = the server is stuck (see check()).
Engine.SILENCE_MS = 20000;
Engine.SILENCE_TRANSLATING_MS = 30000;   // translated lines only come when a sentence closes
Engine.LOAD_TIMEOUT_MS = 90000;

// ---------------------------------------------------------------------------- run state
// Stored in storage.local so the popup can follow it (and it survives the background
// being unloaded). The toolbar badge mirrors it:
//   ...  amber = connecting / loading the model / waiting for speech
//   REC  red   = subtitles arriving
//   !    red   = audio stopped or error
const BADGE = {
  connecting: ["…", "#c58b00"], loading: ["…", "#c58b00"], listening: ["…", "#c58b00"],
  live: ["REC", "#e0245e"], stalled: ["!", "#d13b3b"], noresponse: ["!", "#c58b00"], error: ["!", "#d13b3b"], idle: ["", "#6d4aff"],
};

Engine.setRun = async function (patch) {
  const { runState } = await ext.storage.local.get("runState");
  const next = Object.assign({ state: "idle" }, runState || {}, patch);
  if (next.state === "idle") { next.error = null; next.detail = null; next.detectedLang = null; }
  await ext.storage.local.set({ runState: next });
  const action = ext.action || ext.browserAction;
  const [text, color] = BADGE[next.state] || BADGE.idle;
  try {
    await action.setBadgeText({ text });
    await action.setBadgeBackgroundColor({ color });
    if (action.setBadgeTextColor) await action.setBadgeTextColor({ color: "#ffffff" });
  } catch (e) { /* no badge support */ }
  return next;
};

// --------------------------------------------------------------------- request options

// Whisper's own "translate" task only writes English, but it beats a separate translator
// when English is what you want. Turbo/distilled models were not trained for it.
Engine.useWhisperTranslate = function (s) {
  return s.targetLang === "en" && s.sourceLang !== "en" && !/turbo|distil/i.test(s.model || "");
};

Engine.isTranslating = function (s) {
  return !!s.targetLang && !Engine.useWhisperTranslate(s);
};

Engine.wsOptions = function (s) {
  const translating = Engine.isTranslating(s);
  return {
    language: s.sourceLang || null,
    task: Engine.useWhisperTranslate(s) ? "translate" : "transcribe",
    // A plain WhisperLive server needs a size name; ours resolves ids and names.
    model: s.model || "small",
    use_vad: !!s.useVad,
    enable_translation: translating,
    target_language: translating ? s.targetLang : "en",
    // How many identical passes close a segment. Only closed segments get translated,
    // so this drives the delay: 2 is the lowest that still reads well.
    same_output_threshold: 2,
    // Without this, music or noise that never closes a segment makes the buffer (and
    // the delay) grow forever.
    clip_audio: true,
    // Stream Transcription server options (a plain WhisperLive ignores them)
    st_precision: s.precision || "auto",
    st_translator_device: s.translatorDevice || "auto",
  };
};

Engine.overlayStatus = function (msg) {
  switch (msg.state) {
    case "connecting": return ST.t("status_connecting");
    case "loading": return ST.t("status_loading");
    case "listening": return ST.t("status_listening");
    case "live": return "";
    case "stalled": return ST.t("error_reload");
    case "noresponse": return ST.t(msg.error === "slow_load" ? "warn_slow_load" : "warn_no_response");
    case "error":
      switch (msg.error) {
        case "server_full": return ST.t("error_server_full", msg.detail || "?");
        case "disconnected": return ST.t("error_disconnected");
        case "unreachable": return ST.t("server_unreachable");
        case "no_media": return ST.t("error_no_media");
        case "model_load": return ST.t("error_model_load");
        default: return ST.t("status_error");
      }
  }
  return undefined;
};

// ---------------------------------------------------------------------------- session
// One WebSocket transcription session. `emit` receives {evt:"state"|"segments"|"language"}.
Engine.Session = class {
  constructor({ serverUrl, options, translating, emit }) {
    this.url = serverUrl;
    this.options = options;
    this.translating = translating;
    this.emit = emit;
    this.uid = (crypto.randomUUID && crypto.randomUUID()) || String(Date.now()) + Math.random();
    this.ready = false;
    this.closed = false;
    this.hasText = false;
    this.language = options.language;
    this.state = null;
    this.startedAt = Date.now();
    this.readyAt = 0;
    this.lastPaintAt = 0;     // last message of the stream we show on screen
    this.lastLoudAt = 0;      // last chunk with actual sound in it
    this.warned = false;
  }

  setState(state, extra) {
    if (state === this.state && !extra) return;
    this.state = state;
    this.emit(Object.assign({ evt: "state", state }, extra || {}));
  }

  // Watchdog for a server that stops answering without saying why. The usual cause is a
  // model that does not fit in the graphics card's memory: the server either takes
  // forever loading it or keeps failing on every chunk, and the subtitles just freeze.
  // Only counts time with actual sound going out, so a quiet stream never trips it.
  check() {
    if (this.closed) return;
    const now = Date.now();
    let stuck = false;
    if (!this.ready) {
      stuck = this.state === "loading" && now - this.startedAt > Engine.LOAD_TIMEOUT_MS;
    } else {
      const since = Math.max(this.lastPaintAt, this.readyAt);
      const limit = this.translating ? Engine.SILENCE_TRANSLATING_MS : Engine.SILENCE_MS;
      stuck = now - this.lastLoudAt < 3000 && now - since > limit;
    }
    if (stuck && !this.warned) {
      this.warned = true;
      this.setState("noresponse", { error: this.ready ? "no_response" : "slow_load" });
    }
  }

  recovered() {
    if (!this.warned) return;
    this.warned = false;
    this.setState(this.hasText ? "live" : "listening");
  }

  connect() {
    this.watchdog = setInterval(() => this.check(), 2000);
    this.setState("connecting");
    let opened = false;
    try {
      this.ws = new WebSocket(this.url);
    } catch (e) {
      this.setState("error", { error: "unreachable" });
      return;
    }
    this.ws.binaryType = "arraybuffer";
    this.ws.onopen = () => {
      opened = true;
      this.setState("loading");
      this.ws.send(JSON.stringify(Object.assign({ uid: this.uid }, this.options)));
    };
    this.ws.onmessage = (ev) => this.onMessage(ev);
    this.ws.onerror = () => { /* onclose follows */ };
    this.ws.onclose = () => {
      if (this.closed) return;
      this.closed = true;
      this.setState("error", { error: opened ? "disconnected" : "unreachable" });
    };
  }

  onMessage(ev) {
    let data;
    try { data = JSON.parse(ev.data); } catch (e) { return; }
    if (data.uid && data.uid !== this.uid) return;

    if (data.status === "WAIT") {
      this.setState("error", { error: "server_full", detail: Math.round(Number(data.message) || 0) });
      this.close();
      return;
    }
    if (data.status === "ERROR") {
      console.error("[stream-transcription] server error:", data.message);
      // The usual one: the model doesn't fit in the GPU. Say so instead of a bare
      // "connection closed" a moment later.
      if (/load model|out of memory/i.test(String(data.message))) {
        this.closed = true;
        this.setState("error", { error: "model_load" });
        this.close();
      }
      return;
    }
    if (data.message === "SERVER_READY") {
      this.ready = true;
      this.readyAt = Date.now();
      this.warned = false;
      this.setState("listening");
      return;
    }
    if (data.message === "DISCONNECT") {
      this.closed = true;
      this.setState("error", { error: "disconnected" });
      return;
    }
    if (data.language && !this.language) {
      this.language = data.language;
      this.emit({ evt: "language", lang: data.language });
    }
    // With the translator on, the server sends two streams: "segments" (original
    // language, partial ones included) and "translated_segments" (closed ones only).
    // Showing both would make the subtitles jump between languages.
    const segments = this.translating ? data.translated_segments : data.segments;
    if (!Array.isArray(segments)) return;
    this.lastPaintAt = Date.now();
    this.recovered();
    if (segments.some((s) => s && typeof s.text === "string" && s.text.trim())) {
      this.hasText = true;
      this.setState("live");
    }
    this.emit({ evt: "segments", segments });
  }

  sendAudio(f32) {
    if (!this.ready || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    let sum = 0;
    for (let i = 0; i < f32.length; i += 4) sum += f32[i] * f32[i];
    if (Math.sqrt(sum / Math.max(1, f32.length / 4)) > 0.01) this.lastLoudAt = Date.now();
    this.ws.send(f32);
  }

  close() {
    this.closed = true;
    clearInterval(this.watchdog);
    try { this.ws && this.ws.close(); } catch (e) { /* ignore */ }
  }
};
