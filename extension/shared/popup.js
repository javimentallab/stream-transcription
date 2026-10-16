"use strict";

const $ = (id) => document.getElementById(id);
const t = (...a) => ST.t(...a);

let settings;
let runState = { state: "idle" };
let serverInfo = null;      // last list_models answer, or {ok:false, error}

const ACTIVE = ["connecting", "loading", "listening", "live", "stalled", "noresponse"];
const LOCKED_IDS = ["model", "modelFree", "sourceLang", "targetLang", "useVad", "precision", "translatorDevice"];

document.addEventListener("DOMContentLoaded", init);

async function init() {
  await ST.i18n.init();
  ST.i18n.apply();
  settings = await ST.getSettings();

  fillLanguages();
  bindControls();
  applySettingsToForm();

  const { runState: rs } = await ext.storage.local.get("runState");
  if (rs) runState = rs;
  renderState();
  // The stored state can be stale if a capture died badly: the background checks it.
  ext.runtime.sendMessage({ cmd: "verify" }).catch(() => {});

  ext.storage.onChanged.addListener((changes, area) => {
    if (area !== "local") return;
    if (changes.runState) {
      runState = changes.runState.newValue || { state: "idle" };
      renderState();
    }
  });

  if (!settings.serverUrl) {
    showSetup(true);
  } else {
    checkServer();
  }
}

// ---------------------------------------------------------------------------------- form

function fillLanguages() {
  const ui = ST.i18n.lang;
  const src = $("sourceLang");
  src.append(new Option(t("auto_detect"), ""));
  ST.sortedLanguages(ST.WHISPER_LANGS, ui).forEach((l) => src.append(new Option(l.name, l.code)));

  const dst = $("targetLang");
  dst.append(new Option(t("original_lang"), ""));
  // Put the interface language and English first: they are the usual picks.
  const first = [...new Set([ui, "en"])];
  first.forEach((c) => dst.append(new Option(ST.languageName(c, ui), c)));
  const sep = new Option("──────────", "");
  sep.disabled = true;
  dst.append(sep);
  ST.sortedLanguages(ST.TRANSLATION_LANGS.filter((c) => !first.includes(c)), ui)
    .forEach((l) => dst.append(new Option(l.name, l.code)));

  const dl = $("stockModels");
  ST.STOCK_MODELS.forEach((m) => dl.append(new Option(m)));
}

function applySettingsToForm() {
  $("sourceLang").value = settings.sourceLang;
  $("targetLang").value = settings.targetLang;
  $("fontSize").value = settings.fontSize;
  $("saveSrt").checked = settings.saveSrt;
  $("useVad").checked = settings.useVad;
  $("precision").value = settings.precision;
  $("translatorDevice").value = settings.translatorDevice;
  $("modelFree").value = settings.model;
  renderLines();
  renderFooter();
}

function renderLines() {
  document.querySelectorAll("#lines button").forEach((b) => {
    b.classList.toggle("on", Number(b.dataset.v) === Number(settings.captionLines));
  });
}

function bindControls() {
  const save = (patch) => ST.setSettings(patch).then((s) => { settings = s; });

  $("sourceLang").addEventListener("change", (e) => save({ sourceLang: e.target.value }));
  $("targetLang").addEventListener("change", (e) => save({ targetLang: e.target.value }));
  $("model").addEventListener("change", (e) => save({ model: e.target.value }));
  $("modelFree").addEventListener("change", (e) => save({ model: e.target.value.trim() }));
  $("saveSrt").addEventListener("change", (e) => save({ saveSrt: e.target.checked }));
  $("useVad").addEventListener("change", (e) => save({ useVad: e.target.checked }));
  $("precision").addEventListener("change", (e) => save({ precision: e.target.value }));
  $("translatorDevice").addEventListener("change", (e) => save({ translatorDevice: e.target.value }));

  // Lines and size apply live, even while the subtitles are on.
  $("lines").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    settings.captionLines = Number(b.dataset.v);
    renderLines();
    save({ captionLines: settings.captionLines }).then(pushStyle);
  });
  $("fontSize").addEventListener("input", (e) => {
    settings.fontSize = Number(e.target.value);
    pushStyle();
  });
  $("fontSize").addEventListener("change", (e) => save({ fontSize: Number(e.target.value) }));

  $("toggleBtn").addEventListener("click", onToggle);
  $("openSettings").addEventListener("click", () => openSettings());
  $("manageModels").addEventListener("click", (e) => { e.preventDefault(); openSettings("models"); });
  $("srvChange").addEventListener("click", (e) => { e.preventDefault(); showSetup(true); });
  $("serverHelp").addEventListener("click", (e) => { e.preventDefault(); openSettings("server"); });

  $("setupConnect").addEventListener("click", onSetupConnect);
  $("setupUrl").addEventListener("keydown", (e) => { if (e.key === "Enter") onSetupConnect(); });
}

function pushStyle() {
  ext.runtime.sendMessage({
    cmd: "style", captionLines: settings.captionLines, fontSize: settings.fontSize,
  }).catch(() => {});
}

function openSettings(section) {
  const url = ext.runtime.getURL("settings.html") + (section ? "#" + section : "");
  ext.tabs.create({ url });
  window.close();
}

// -------------------------------------------------------------------------------- server

function showSetup(show) {
  $("setupCard").hidden = !show;
  if (show) {
    $("setupUrl").value = settings.serverUrl ? ST.prettyServer(settings.serverUrl) : "";
    $("setupUrl").focus();
  }
  $("mainUi").hidden = show && !settings.serverUrl;
  $("foot").hidden = !settings.serverUrl;
}

async function onSetupConnect() {
  const url = ST.normalizeServerUrl($("setupUrl").value);
  const msg = $("setupMsg");
  if (!url) {
    setMsg(msg, t("server_bad_url"), "bad");
    return;
  }
  setMsg(msg, t("server_checking"), "");
  $("setupConnect").disabled = true;
  const res = await ST.serverRequest(url, { st_action: "list_models" }, 20000);
  $("setupConnect").disabled = false;
  if (!res.ok && res.error !== "unsupported") {
    setMsg(msg, t(res.error === "timeout" ? "server_timeout" : "server_unreachable"), "bad");
    return;
  }
  settings = await ST.setSettings({ serverUrl: url });
  setMsg(msg, "", "");
  showSetup(false);
  applyServerInfo(res);
}

async function checkServer() {
  renderFooter("checking");
  // A server started on demand can take a few seconds to wake up.
  const res = await ST.serverRequest(settings.serverUrl, { st_action: "list_models" }, 20000);
  applyServerInfo(res);
}

function applyServerInfo(res) {
  serverInfo = res;
  const sel = $("model");
  const free = $("modelFree");

  if (res.ok) {
    sel.hidden = false;
    free.hidden = true;
    sel.textContent = "";
    res.models.forEach((m) => {
      const { name } = ST.splitModelId(m.id);
      const label = (m.default ? t("model_default_tag", name) : name) + "  (" + ST.formatBytes(m.size) + ")";
      sel.append(new Option(label, m.id));
    });
    const ids = res.models.map((m) => m.id);
    let pick = settings.model;
    if (!ids.includes(pick)) {
      // Saved model was deleted (or never chosen): fall back to the server default.
      pick = res.default || ids[0] || "";
      if (pick !== settings.model) ST.setSettings({ model: pick }).then((s) => { settings = s; });
    }
    if (!ids.length) sel.append(new Option(t("model_server_default"), ""));
    sel.value = pick;
    renderFooter("ok", res.models.length);
  } else if (res.error === "unsupported") {
    // Plain WhisperLive: no list, the user types a size name.
    sel.hidden = true;
    free.hidden = false;
    free.placeholder = "small";
    renderFooter("plain");
  } else {
    sel.hidden = true;
    free.hidden = false;
    renderFooter("bad", res.error);
  }
  renderState();
}

function renderFooter(kind, extra) {
  const dot = $("srvDot");
  const text = $("srvText");
  const host = ST.prettyServer(settings.serverUrl);
  dot.className = "srv-dot";
  if (kind === "checking") {
    text.textContent = host + " · " + t("server_checking");
  } else if (kind === "ok") {
    dot.classList.add("ok");
    text.textContent = host + " · " + ST.connectedText(extra);
  } else if (kind === "plain") {
    dot.classList.add("warn");
    text.textContent = host + " · " + t("server_plain");
  } else if (kind === "bad") {
    dot.classList.add("bad");
    text.textContent = host + " · " + t(extra === "timeout" ? "server_timeout" : "server_unreachable");
    text.title = text.textContent;
  } else {
    text.textContent = host;
  }
}

// --------------------------------------------------------------------------------- state

function renderState() {
  const st = runState.state || "idle";
  // An error keeps its message on screen until the user stops: the button stays "Stop".
  const active = ACTIVE.includes(st) || (st === "error" && typeof runState.tabId === "number");

  $("statusPill").dataset.state = st;
  $("statusText").textContent = t("status_" + (st === "error" ? "error" : st));

  const btn = $("toggleBtn");
  btn.classList.toggle("running", active);
  $("toggleLabel").textContent = t(active ? "stop" : "start");
  btn.disabled = !active && !settings.serverUrl;

  $("fields").classList.toggle("locked", active);
  LOCKED_IDS.forEach((id) => { $(id).disabled = active; });

  const msg = $("mainMsg");
  if (st === "error" && runState.error) {
    setMsg(msg, errorText(runState), "bad");
  } else if (st === "stalled") {
    setMsg(msg, t("error_reload"), "warn");
  } else if (st === "noresponse") {
    setMsg(msg, t(runState.error === "slow_load" ? "warn_slow_load" : "warn_no_response"), "warn");
  } else if (st === "loading" || st === "connecting") {
    setMsg(msg, t("first_load_hint"), "");
  } else {
    setMsg(msg, "", "");
  }

  const det = $("detectedLang");
  if (runState.detectedLang && !settings.sourceLang) {
    det.textContent = t("detected", ST.languageName(runState.detectedLang, ST.i18n.lang));
  } else {
    det.textContent = "";
  }
}

function errorText(rs) {
  switch (rs.error) {
    case "capture": return t("error_capture");
    case "no_media": return t("error_no_media");
    case "model_load": return t("error_model_load");
    case "server_full": return t("error_server_full", rs.detail || "?");
    case "disconnected": return t("error_disconnected");
    case "unreachable": return t("server_unreachable");
    case "no_server": return t("error_no_server");
    default: return t("err_unknown", rs.error);
  }
}

async function onToggle() {
  const active = ACTIVE.includes(runState.state) ||
    (runState.state === "error" && typeof runState.tabId === "number");
  if (active) {
    await ext.runtime.sendMessage({ cmd: "stop" }).catch(() => {});
    return;
  }
  const [tab] = await ext.tabs.query({ active: true, currentWindow: true });
  if (!tab) return;
  // Chromium: the tab capture has to be requested here, while the user's click is still
  // "fresh"; the background and the offscreen document only receive the stream id.
  let streamId = null;
  if (ext.tabCapture && ext.tabCapture.getMediaStreamId) {
    try {
      streamId = await ext.tabCapture.getMediaStreamId({ targetTabId: tab.id });
    } catch (e) {
      runState = { state: "error", error: "capture" };
      renderState();
      return;
    }
  }
  // Optimistic: the background confirms (or corrects) through runState.
  runState = { state: "connecting" };
  renderState();
  await ext.runtime.sendMessage({ cmd: "start", tabId: tab.id, streamId }).catch(() => {});
}

function setMsg(el, text, kind) {
  el.textContent = text;
  el.className = el.className.replace(/\b(ok|bad|warn)\b/g, "").trim() + (kind ? " " + kind : "");
}
