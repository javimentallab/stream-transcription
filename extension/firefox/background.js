// Firefox background page: starts/stops the engine in the tab's content script, keeps
// the run state and relays engine events to the overlay.
"use strict";

const CONTENT_FILES = ["common.js", "engine-common.js", "overlay.js", "content.js"];

function toTab(tabId, msg) {
  if (typeof tabId !== "number") return Promise.resolve();
  return browser.tabs.sendMessage(tabId, msg).catch(() => {});
}

async function ping(tabId) {
  try {
    return await browser.tabs.sendMessage(tabId, { st: "engine", cmd: "ping" });
  } catch (e) {
    return null;
  }
}

// Tabs opened before the add-on was installed have no content script yet.
async function ensureContent(tabId) {
  if (await ping(tabId)) return true;
  try {
    for (const file of CONTENT_FILES) await browser.tabs.executeScript(tabId, { file });
  } catch (e) {
    return false;
  }
  return !!(await ping(tabId));
}

async function start(tabId) {
  const settings = await ST.getSettings();
  await ST.i18n.init();
  await stop({ quiet: true });

  if (!settings.serverUrl) {
    await Engine.setRun({ state: "error", error: "no_server", tabId: null });
    return;
  }
  if (!(await ensureContent(tabId))) {
    await Engine.setRun({ state: "error", error: "capture", tabId: null });
    return;
  }
  await Engine.setRun({ state: "connecting", tabId, detectedLang: null, error: null, startedAt: Date.now() });
  await toTab(tabId, {
    st: "overlay", op: "show", lines: settings.captionLines, fontSize: settings.fontSize,
    saveSrt: settings.saveSrt, status: ST.t("status_connecting"),
  });
  await toTab(tabId, {
    st: "engine", cmd: "start", serverUrl: settings.serverUrl,
    options: Engine.wsOptions(settings), translating: Engine.isTranslating(settings),
  });
}

async function stop({ quiet = false } = {}) {
  const { runState } = await browser.storage.local.get("runState");
  const settings = await ST.getSettings();
  if (runState && typeof runState.tabId === "number") {
    await toTab(runState.tabId, { st: "engine", cmd: "stop" });
    await toTab(runState.tabId, { st: "overlay", op: "stop", saveSrt: settings.saveSrt });
  }
  if (!quiet || (runState && runState.state !== "error")) {
    await Engine.setRun({ state: "idle", tabId: null, error: null });
  }
}

async function onEngine(msg, sender) {
  const { runState } = await browser.storage.local.get("runState");
  const tabId = runState && runState.tabId;
  if (!tabId || !sender.tab || sender.tab.id !== tabId) return;
  await ST.i18n.init();

  if (msg.evt === "hello") {
    // A fresh content script in the capturing tab = the page was reloaded and the
    // engine went with it. (Ignore our own injection right at start.)
    if (Engine.ACTIVE.includes(runState.state) && Date.now() - (runState.startedAt || 0) > 5000) {
      await Engine.setRun({ state: "idle", tabId: null });
    }
  } else if (msg.evt === "state") {
    await Engine.setRun({ state: msg.state, error: msg.error || null, detail: msg.detail || null });
    const text = Engine.overlayStatus(msg);
    if (text !== undefined) {
      await toTab(tabId, { st: "overlay", op: "status", text, bad: ["error", "stalled", "noresponse"].includes(msg.state) });
    }
  } else if (msg.evt === "segments") {
    await toTab(tabId, { st: "overlay", op: "segments", segments: msg.segments });
  } else if (msg.evt === "language") {
    await Engine.setRun({ detectedLang: msg.lang });
  }
}

browser.runtime.onMessage.addListener((msg, sender) => {
  if (!msg) return;
  if (msg.from === "engine") {
    onEngine(msg, sender);
    return;
  }
  switch (msg.cmd) {
    case "start":
      start(msg.tabId);
      break;
    case "stop":
      stop();
      break;
    case "verify":
      (async () => {
        const { runState } = await browser.storage.local.get("runState");
        if (runState && Engine.ACTIVE.includes(runState.state)) {
          const res = await ping(runState.tabId);
          if (!res || !res.capturing) await Engine.setRun({ state: "idle", tabId: null });
        }
      })();
      break;
    case "style":
      browser.storage.local.get("runState").then(({ runState }) => {
        if (runState && runState.tabId) {
          toTab(runState.tabId, { st: "overlay", op: "style", lines: msg.captionLines, fontSize: msg.fontSize });
        }
      });
      break;
  }
});

browser.tabs.onRemoved.addListener(async (tabId) => {
  const { runState } = await browser.storage.local.get("runState");
  if (runState && runState.tabId === tabId) Engine.setRun({ state: "idle", tabId: null });
});

browser.runtime.onStartup.addListener(() => Engine.setRun({ state: "idle", tabId: null }));
browser.runtime.onInstalled.addListener(() => Engine.setRun({ state: "idle", tabId: null }));
