// Shared helpers for every extension page (popup, settings, background, engines).
// Works in Chromium (chrome.*) and Firefox (browser.*).
"use strict";

var ext = globalThis.browser || globalThis.chrome;

var ST = globalThis.ST || {};
globalThis.ST = ST;

ST.DEFAULTS = {
  serverUrl: "",          // e.g. ws://192.168.1.10:9090  (empty = not configured yet)
  model: "",              // model id from the server ("" = server default)
  sourceLang: "",         // "" = auto-detect
  targetLang: "",         // "" = keep the original language
  captionLines: 2,
  fontSize: 22,
  saveSrt: false,
  useVad: true,
  precision: "auto",      // auto | int8 (half the GPU memory, same output)
  translatorDevice: "auto", // auto | cpu
  uiLang: "auto",         // auto | en | es
};

ST.getSettings = async function () {
  const { settings } = await ext.storage.local.get("settings");
  return Object.assign({}, ST.DEFAULTS, settings || {});
};

ST.setSettings = async function (patch) {
  const cur = await ST.getSettings();
  const next = Object.assign(cur, patch);
  await ext.storage.local.set({ settings: next });
  return next;
};

// "192.168.1.10:9090", "http://host:9090", "wss://host/ws" ... -> a WebSocket URL.
ST.normalizeServerUrl = function (raw) {
  let s = String(raw || "").trim();
  if (!s) return "";
  if (/^https?:\/\//i.test(s)) s = s.replace(/^http/i, "ws");
  if (!/^wss?:\/\//i.test(s)) s = "ws://" + s;
  try {
    const u = new URL(s);
    if (!u.hostname) return "";
    if (!u.port && u.protocol === "ws:" && u.pathname === "/") u.port = "9090";
    return u.toString();
  } catch (e) {
    return "";
  }
};

ST.prettyServer = function (url) {
  try {
    const u = new URL(url);
    return u.host + (u.pathname !== "/" ? u.pathname : "");
  } catch (e) {
    return url || "";
  }
};

// One-shot request to the Stream Transcription extension of the server.
// Resolves {ok:true, ...} / {ok:false, error}. A plain WhisperLive server does not know
// the protocol and just closes the socket: that comes back as error "unsupported".
ST.serverRequest = function (url, payload, timeoutMs = 8000) {
  return new Promise((resolve) => {
    let done = false;
    let ws;
    const finish = (res) => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      try { ws && ws.close(); } catch (e) { /* ignore */ }
      resolve(res);
    };
    const timer = setTimeout(() => finish({ ok: false, error: "timeout" }), timeoutMs);
    let opened = false;
    try {
      ws = new WebSocket(url);
    } catch (e) {
      finish({ ok: false, error: "bad_url" });
      return;
    }
    ws.onopen = () => {
      opened = true;
      ws.send(JSON.stringify(payload));
    };
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data && data.st) finish(data);
        else finish({ ok: false, error: "unsupported" });
      } catch (e) {
        finish({ ok: false, error: "unsupported" });
      }
    };
    ws.onerror = () => finish({ ok: false, error: opened ? "unsupported" : "unreachable" });
    ws.onclose = () => finish({ ok: false, error: opened ? "unsupported" : "unreachable" });
  });
};

ST.connectedText = function (n) {
  return n === 1 ? ST.t("server_ok_one_model") : ST.t("server_ok_models", n);
};

ST.formatBytes = function (n) {
  if (!n) return "0 MB";
  if (n >= 1e9) return (n / 1e9).toFixed(1).replace(/\.0$/, "") + " GB";
  return Math.max(1, Math.round(n / 1e6)) + " MB";
};

// "Systran/faster-whisper-large-v3" -> {name: "faster-whisper-large-v3", org: "Systran"}
ST.splitModelId = function (id) {
  if (!id) return { name: "", org: "" };
  if (id.startsWith("url:")) return { name: id.slice(4), org: "" };
  const i = id.indexOf("/");
  return i < 0 ? { name: id, org: "" } : { name: id.slice(i + 1), org: id.slice(0, i) };
};

// Size names a plain WhisperLive server understands (no model management).
ST.STOCK_MODELS = ["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"];

// Suggestions on the "add model" form. All tested with faster-whisper.
ST.SUGGESTED_MODELS = [
  "Systran/faster-whisper-small",
  "Systran/faster-whisper-medium",
  "Systran/faster-whisper-large-v3",
  "deepdml/faster-whisper-large-v3-turbo-ct2",
];

// Languages Whisper can recognise (ISO 639-1, plus haw/jw/yue). Names come from
// Intl.DisplayNames in the interface language, so they never need translating.
ST.WHISPER_LANGS = [
  "af", "am", "ar", "as", "az", "ba", "be", "bg", "bn", "bo", "br", "bs", "ca", "cs",
  "cy", "da", "de", "el", "en", "es", "et", "eu", "fa", "fi", "fo", "fr", "gl", "gu",
  "ha", "haw", "he", "hi", "hr", "ht", "hu", "hy", "id", "is", "it", "ja", "jw", "ka",
  "kk", "km", "kn", "ko", "la", "lb", "ln", "lo", "lt", "lv", "mg", "mi", "mk", "ml",
  "mn", "mr", "ms", "mt", "my", "ne", "nl", "nn", "no", "oc", "pa", "pl", "ps", "pt",
  "ro", "ru", "sa", "sd", "si", "sk", "sl", "sn", "so", "sq", "sr", "su", "sv", "sw",
  "ta", "te", "tg", "th", "tk", "tl", "tr", "tt", "uk", "ur", "uz", "vi", "yi", "yo",
  "yue", "zh",
];

// Languages the server's translator (SMALL100 / M2M100) can write.
ST.TRANSLATION_LANGS = [
  "af", "am", "ar", "az", "ba", "be", "bg", "bn", "br", "bs", "ca", "cs", "cy", "da",
  "de", "el", "en", "es", "et", "fa", "fi", "fr", "ga", "gl", "gu", "ha", "he", "hi",
  "hr", "ht", "hu", "hy", "id", "ig", "is", "it", "ja", "jv", "ka", "kk", "km", "kn",
  "ko", "lb", "lg", "ln", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "my",
  "ne", "nl", "no", "ns", "oc", "or", "pa", "pl", "ps", "pt", "ro", "ru", "sd", "si",
  "sk", "sl", "so", "sq", "sr", "ss", "su", "sv", "sw", "ta", "th", "tl", "tn", "tr",
  "uk", "ur", "uz", "vi", "wo", "xh", "yi", "yo", "zh", "zu",
];

ST.languageName = function (code, uiLang) {
  const alias = { jw: "jv", haw: "haw", yue: "yue", ns: "nso" };
  try {
    const dn = new Intl.DisplayNames([uiLang || "en"], { type: "language" });
    const name = dn.of(alias[code] || code);
    if (name && name !== code) return name.charAt(0).toLocaleUpperCase(uiLang) + name.slice(1);
  } catch (e) { /* ignore */ }
  return code;
};

ST.sortedLanguages = function (codes, uiLang) {
  return codes
    .map((c) => ({ code: c, name: ST.languageName(c, uiLang) }))
    .sort((a, b) => a.name.localeCompare(b.name, uiLang));
};
