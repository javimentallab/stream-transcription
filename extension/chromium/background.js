// Chromium service worker: starts/stops the capture, keeps the run state and relays
// between the offscreen document (audio + WebSocket) and the overlay in the tab.
"use strict";

importScripts("common.js", "i18n.js", "engine-common.js");

const OFFSCREEN_URL = "offscreen.html";

async function hasOffscreen() {
  if (chrome.runtime.getContexts) {
    const ctx = await chrome.runtime.getContexts({ contextTypes: ["OFFSCREEN_DOCUMENT"] });
    return ctx.length > 0;
  }
  return chrome.offscreen.hasDocument ? chrome.offscreen.hasDocument() : false;
}

async function ensureOffscreen() {
  if (await hasOffscreen()) return;
  await chrome.offscreen.createDocument({
    url: OFFSCREEN_URL,
    reasons: ["USER_MEDIA"],
    justification: "Capture the tab audio and stream it to the transcription server.",
  });
}

async function closeOffscreen() {
  if (await hasOffscreen()) {
    try { await chrome.offscreen.closeDocument(); } catch (e) { /* already gone */ }
  }
}

function toTab(tabId, msg) {
  if (typeof tabId !== "number") return Promise.resolve();
  return chrome.tabs.sendMessage(tabId, Object.assign({ st: "overlay" }, msg)).catch(() => {});
}

async function injectOverlay(tabId) {
  await chrome.scripting.executeScript({ target: { tabId }, files: ["overlay.js"] });
}

async function start(tabId, streamId) {
  const settings = await ST.getSettings();
  await ST.i18n.init();
  await stop({ quiet: true });

  if (!settings.serverUrl) {
    await Engine.setRun({ state: "error", error: "no_server", tabId: null });
    return;
  }
  if (!streamId) {
    await Engine.setRun({ state: "error", error: "capture", tabId: null });
    return;
  }
  try {
    await injectOverlay(tabId);
  } catch (e) {
    await Engine.setRun({ state: "error", error: "capture", tabId: null });
    return;
  }

  await Engine.setRun({ state: "connecting", tabId, detectedLang: null, error: null });
  await toTab(tabId, {
    op: "show", lines: settings.captionLines, fontSize: settings.fontSize,
    saveSrt: settings.saveSrt, status: ST.t("status_connecting"),
  });

  try {
    await ensureOffscreen();
    const msg = {
      target: "offscreen", cmd: "start", streamId,
      options: Engine.wsOptions(settings), serverUrl: settings.serverUrl,
      translating: Engine.isTranslating(settings),
    };
    // A just-created offscreen document may not be listening yet.
    for (let i = 0; ; i++) {
      try {
        await chrome.runtime.sendMessage(msg);
        break;
      } catch (e) {
        if (i >= 30) throw e;
        await new Promise((r) => setTimeout(r, 100));
      }
    }
  } catch (e) {
    console.error("[stream-transcription] could not start the offscreen engine", e);
    await Engine.setRun({ state: "error", error: "capture" });
    await toTab(tabId, { op: "stop" });
  }
}

async function stop({ quiet = false } = {}) {
  const { runState } = await chrome.storage.local.get("runState");
  const settings = await ST.getSettings();
  try { await chrome.runtime.sendMessage({ target: "offscreen", cmd: "stop" }); } catch (e) { /* none */ }
  await closeOffscreen();
  if (runState && typeof runState.tabId === "number") {
    await toTab(runState.tabId, { op: "stop", saveSrt: settings.saveSrt });
  }
  if (!quiet || (runState && runState.state !== "error")) {
    await Engine.setRun({ state: "idle", tabId: null, error: null });
  }
}

// Messages from the engine running in the offscreen document.
async function onEngine(msg) {
  const { runState } = await chrome.storage.local.get("runState");
  const tabId = runState && runState.tabId;
  if (!tabId) return;
  await ST.i18n.init();

  if (msg.evt === "state") {
    await Engine.setRun({ state: msg.state, error: msg.error || null, detail: msg.detail || null });
    const text = Engine.overlayStatus(msg);
    if (text !== undefined) await toTab(tabId, { op: "status", text, bad: ["error", "stalled", "noresponse"].includes(msg.state) });
  } else if (msg.evt === "segments") {
    await toTab(tabId, { op: "segments", segments: msg.segments });
  } else if (msg.evt === "language") {
    await Engine.setRun({ detectedLang: msg.lang });
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (!msg) return;
  if (msg.from === "engine") {
    onEngine(msg);
    return;
  }
  switch (msg.cmd) {
    case "start":
      start(msg.tabId, msg.streamId);
      break;
    case "stop":
      stop();
      break;
    case "verify":
      (async () => {
        const { runState } = await chrome.storage.local.get("runState");
        if (runState && Engine.ACTIVE.includes(runState.state) && !(await hasOffscreen())) {
          await Engine.setRun({ state: "idle", tabId: null });
        }
      })();
      break;
    case "style":
      chrome.storage.local.get("runState").then(({ runState }) => {
        if (runState && runState.tabId) {
          toTab(runState.tabId, { op: "style", lines: msg.captionLines, fontSize: msg.fontSize });
        }
      });
      break;
  }
  sendResponse({});
});

chrome.tabs.onRemoved.addListener(async (tabId) => {
  const { runState } = await chrome.storage.local.get("runState");
  if (runState && runState.tabId === tabId) stop();
});

// A reload or a navigation wipes the overlay. Put it back if we still may; otherwise stop.
chrome.tabs.onUpdated.addListener(async (tabId, info) => {
  if (info.status !== "complete") return;
  const { runState } = await chrome.storage.local.get("runState");
  if (!runState || runState.tabId !== tabId || !Engine.ACTIVE.includes(runState.state)) return;
  const settings = await ST.getSettings();
  try {
    await injectOverlay(tabId);
    await toTab(tabId, {
      op: "show", lines: settings.captionLines, fontSize: settings.fontSize, saveSrt: settings.saveSrt,
    });
  } catch (e) {
    stop();
  }
});

// Nothing survives a browser restart: no stale "REC" badge.
chrome.runtime.onStartup.addListener(() => Engine.setRun({ state: "idle", tabId: null }));
chrome.runtime.onInstalled.addListener(() => Engine.setRun({ state: "idle", tabId: null }));
