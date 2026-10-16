"use strict";

const $ = (id) => document.getElementById(id);
const t = (...a) => ST.t(...a);

let settings;
let info = null;            // last list_models answer
let pollTimer = null;
const knownJobState = {};   // id -> last seen state, to notice when a job finishes

document.addEventListener("DOMContentLoaded", init);

async function init() {
  await ST.i18n.init();
  ST.i18n.apply();
  document.title = t("settings_title");
  settings = await ST.getSettings();
  $("version").textContent = "Stream Transcription " + ext.runtime.getManifest().version;

  initServer();
  initModels();
  initSubtitles();
  initPerformance();
  initInterface();
  initToc();

  if (settings.serverUrl) refreshModels();
  else showModelsMsg(t("error_no_server"), "warn");

  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && settings.serverUrl) refreshModels();
  });
}

function setMsg(el, text, kind) {
  el.textContent = text || "";
  el.className = "msg" + (kind ? " " + kind : "");
}

function errText(code, detail) {
  const key = "err_" + code;
  const s = t(key);
  return s === key ? t("err_unknown", detail || code) : s;
}

// -------------------------------------------------------------------------------- server

function initServer() {
  $("serverUrl").value = settings.serverUrl ? ST.prettyServer(settings.serverUrl) : "";
  const go = async () => {
    const url = ST.normalizeServerUrl($("serverUrl").value);
    if (!url) return setMsg($("serverMsg"), t("server_bad_url"), "bad");
    setMsg($("serverMsg"), t("server_checking"));
    $("serverSave").disabled = true;
    const res = await ST.serverRequest(url, { st_action: "list_models" }, 20000);
    $("serverSave").disabled = false;
    if (!res.ok && res.error !== "unsupported") {
      return setMsg($("serverMsg"), t(res.error === "timeout" ? "server_timeout" : "server_unreachable"), "bad");
    }
    settings = await ST.setSettings({ serverUrl: url });
    $("serverUrl").value = ST.prettyServer(url);
    setMsg($("serverMsg"), res.ok ? ST.connectedText(res.models.length) : t("server_plain"), res.ok ? "ok" : "warn");
    applyModels(res);
  };
  $("serverSave").addEventListener("click", go);
  $("serverUrl").addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
}

// -------------------------------------------------------------------------------- models

function initModels() {
  ST.STOCK_MODELS.forEach((m) => $("stockModels").append(new Option(m)));
  $("plainModel").value = settings.model;
  $("plainSave").addEventListener("click", async () => {
    settings = await ST.setSettings({ model: $("plainModel").value.trim() });
    showModelsMsg(t("saved"), "ok");
  });

  $("addBtn").addEventListener("click", () => startDownload($("addSource").value));
  $("addSource").addEventListener("keydown", (e) => { if (e.key === "Enter") startDownload($("addSource").value); });
}

function showModelsMsg(text, kind) {
  setMsg($("modelsMsg"), text, kind);
}

async function refreshModels() {
  const res = await ST.serverRequest(settings.serverUrl, { st_action: "list_models" }, 20000);
  applyModels(res);
}

function applyModels(res) {
  info = res;
  const managed = res.ok;
  $("modelsManaged").hidden = !managed;
  $("modelsPlain").hidden = managed || !(res.error === "unsupported");
  if (!res.ok && res.error !== "unsupported") {
    showModelsMsg(t(res.error === "timeout" ? "server_timeout" : "server_unreachable"), "bad");
    schedulePoll(false);
    return;
  }
  showModelsMsg("");
  if (!managed) return;

  $("addBlock").hidden = !res.management;
  renderModelList(res);
  renderSuggestions(res);
  renderJobs(res.jobs || []);
}

function renderModelList(res) {
  const list = $("modelList");
  list.textContent = "";
  $("noModels").hidden = res.models.length > 0;
  const selected = res.models.some((m) => m.id === settings.model) ? settings.model : res.default;

  res.models.forEach((m) => {
    const { name, org } = ST.splitModelId(m.id);
    const li = document.createElement("li");
    li.className = "model" + (m.id === selected ? " selected" : "");

    const infoEl = document.createElement("div");
    infoEl.className = "info";
    const nameEl = document.createElement("div");
    nameEl.className = "name";
    nameEl.textContent = name;
    nameEl.title = m.id;
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.append(document.createTextNode([org, ST.formatBytes(m.size)].filter(Boolean).join(" · ")));
    if (m.id === selected) meta.append(badge(t("badge_selected"), "accent"));
    if (m.default) meta.append(badge(t("badge_default")));
    if (m.loaded) meta.append(badge(t("badge_loaded"), "ok"));
    infoEl.append(nameEl, meta);

    const actions = document.createElement("div");
    actions.className = "actions";
    if (m.id !== selected) {
      const use = button(t("use_model"), "btn ghost sm", async () => {
        settings = await ST.setSettings({ model: m.id });
        renderModelList(info);
      });
      actions.append(use);
    }
    if (res.management && !m.default) {
      const del = button(t("delete_model"), "btn danger sm", () => deleteModel(m, name));
      actions.append(del);
    }
    li.append(infoEl, actions);
    list.append(li);
  });
}

function badge(text, kind) {
  const b = document.createElement("span");
  b.className = "badge" + (kind ? " " + kind : "");
  b.textContent = text;
  return b;
}

function button(text, cls, onClick) {
  const b = document.createElement("button");
  b.className = cls;
  b.textContent = text;
  b.addEventListener("click", onClick);
  return b;
}

async function deleteModel(m, name) {
  if (!confirm(t("confirm_delete", name, ST.formatBytes(m.size)))) return;
  const res = await ST.serverRequest(settings.serverUrl, { st_action: "delete_model", id: m.id }, 20000);
  if (!res.ok) {
    showModelsMsg(errText(res.error, res.detail), "bad");
    return;
  }
  if (settings.model === m.id) settings = await ST.setSettings({ model: "" });
  refreshModels();
}

function renderSuggestions(res) {
  const box = $("suggestions");
  box.textContent = "";
  const installed = new Set(res.models.map((m) => m.id));
  ST.SUGGESTED_MODELS.filter((id) => !installed.has(id)).forEach((id) => {
    const chip = button(ST.splitModelId(id).name, "chip", () => {
      $("addSource").value = id;
      $("addSource").focus();
    });
    chip.title = id;
    box.append(chip);
  });
}

async function startDownload(source) {
  source = String(source || "").trim();
  if (!source) return;
  setMsg($("addMsg"), t("server_checking"));
  $("addBtn").disabled = true;
  const res = await ST.serverRequest(settings.serverUrl, { st_action: "download_model", source }, 20000);
  $("addBtn").disabled = false;
  if (!res.ok) {
    setMsg($("addMsg"), errText(res.error, res.detail), "bad");
    return;
  }
  setMsg($("addMsg"), "");
  $("addSource").value = "";
  refreshModels();
}

function renderJobs(jobs) {
  const list = $("jobList");
  list.textContent = "";
  let running = false;
  let finished = false;

  jobs.forEach((j) => {
    const active = !["ready", "error"].includes(j.state);
    running = running || active;
    if (knownJobState[j.id] && knownJobState[j.id] !== j.state && j.state === "ready") finished = true;
    knownJobState[j.id] = j.state;

    const li = document.createElement("li");
    li.className = "job " + j.state;
    const top = document.createElement("div");
    top.className = "top-line";
    const name = document.createElement("span");
    name.className = "name";
    name.textContent = j.id.startsWith("url:") ? j.source : j.id;
    const status = document.createElement("span");
    status.className = "hint";
    status.textContent = jobText(j);
    top.append(name, status);
    li.append(top);

    if (active) {
      const track = document.createElement("div");
      track.className = "bar-track";
      const fill = document.createElement("div");
      fill.className = "bar-fill";
      if (j.state === "downloading" && j.total) {
        fill.style.width = Math.min(100, (100 * j.downloaded) / j.total).toFixed(1) + "%";
      } else {
        fill.classList.add("indeterminate");
      }
      track.append(fill);
      li.append(track);
    }
    if (j.state === "error") {
      const row = document.createElement("div");
      row.className = "row";
      row.append(button(t("retry"), "btn ghost sm", () => startDownload(j.source)));
      li.append(row);
    }
    list.append(li);
  });

  $("keepOpen").hidden = !running;
  if (finished) {
    // a model just finished: the list has changed
    setTimeout(refreshModels, 300);
  }
  schedulePoll(running);
}

function jobText(j) {
  switch (j.state) {
    case "downloading":
      return j.total
        ? t("job_downloading", ST.formatBytes(j.downloaded), ST.formatBytes(j.total))
        : t("job_downloading_nosize", ST.formatBytes(j.downloaded));
    case "converting": return t("job_converting");
    case "extracting": return t("job_extracting");
    case "ready": return t("job_ready");
    case "error": return t("job_error", errText(j.error, j.detail));
    default: return j.state;
  }
}

// While something downloads, ask every 2 s. Besides showing progress, this keeps
// servers that start on demand awake until the download ends.
function schedulePoll(active) {
  clearTimeout(pollTimer);
  if (active) pollTimer = setTimeout(refreshModels, 2000);
}

// ----------------------------------------------------------------------------- subtitles

function initSubtitles() {
  const preview = $("preview").firstElementChild;
  const paint = () => {
    preview.style.fontSize = settings.fontSize + "px";
    preview.style.lineHeight = Math.round(settings.fontSize * 1.38) + "px";
    document.querySelectorAll("#lines button").forEach((b) => {
      b.classList.toggle("on", Number(b.dataset.v) === Number(settings.captionLines));
    });
  };
  $("fontSize").value = settings.fontSize;
  $("saveSrt").checked = settings.saveSrt;
  $("useVad").checked = settings.useVad;
  paint();

  $("lines").addEventListener("click", async (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    settings = await ST.setSettings({ captionLines: Number(b.dataset.v) });
    paint();
  });
  $("fontSize").addEventListener("input", (e) => { settings.fontSize = Number(e.target.value); paint(); });
  $("fontSize").addEventListener("change", async (e) => { settings = await ST.setSettings({ fontSize: Number(e.target.value) }); });
  $("saveSrt").addEventListener("change", async (e) => { settings = await ST.setSettings({ saveSrt: e.target.checked }); });
  $("useVad").addEventListener("change", async (e) => { settings = await ST.setSettings({ useVad: e.target.checked }); });
  $("resetPos").addEventListener("click", async () => {
    await ext.storage.local.remove("overlayPos");
    $("resetMsg").textContent = t("position_reset_done");
  });
}

// --------------------------------------------------------------------------- performance

function initPerformance() {
  $("precision").value = settings.precision;
  $("translatorDevice").value = settings.translatorDevice;
  $("precision").addEventListener("change", async (e) => { settings = await ST.setSettings({ precision: e.target.value }); });
  $("translatorDevice").addEventListener("change", async (e) => { settings = await ST.setSettings({ translatorDevice: e.target.value }); });
}

// ----------------------------------------------------------------------------- interface

function initInterface() {
  $("uiLang").value = settings.uiLang;
  $("uiLang").addEventListener("change", async (e) => {
    settings = await ST.setSettings({ uiLang: e.target.value });
    location.reload();
  });
}

function initToc() {
  const links = Array.from(document.querySelectorAll(".toc a"));
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      links.forEach((a) => a.classList.toggle("on", a.getAttribute("href") === "#" + en.target.id));
    });
  }, { rootMargin: "-20% 0px -70% 0px" });
  document.querySelectorAll(".panel").forEach((p) => obs.observe(p));
  if (location.hash) {
    const el = document.querySelector(location.hash);
    if (el) setTimeout(() => el.scrollIntoView(), 50);
  }
}
