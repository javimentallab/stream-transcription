// Subtitle overlay drawn on top of the page. Shared by Chromium (injected on start) and
// Firefox (declared content script). Lives in a shadow root so page CSS can't touch it.
"use strict";

(function () {
  if (window.__stOverlay) return;   // Chromium re-injects this file on every start

  const api = globalThis.browser || globalThis.chrome;

  let host = null;      // element in the page
  let box = null;       // draggable container (inside the shadow root)
  let clip = null;
  let textEl = null;
  let statusEl = null;
  let lines = 2;
  let fontSize = 22;
  let saveSrt = false;
  let srt = [];
  let lastIncomplete = null;
  let hasText = false;

  const CSS = `
    :host { all: initial; }
    [hidden] { display: none !important; }
    .box {
      position: fixed; left: 50%; top: 85%; transform: translate(-50%, -50%);
      width: min(96vw, 1100px); z-index: 2147483647; text-align: center;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
      font-weight: 600; letter-spacing: .01em; color: #fff; cursor: move; user-select: none;
    }
    .clip { overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; }
    .para { margin: 0; }
    .line {
      background: rgba(0, 0, 0, .74); padding: .08em .45em; border-radius: .25em;
      -webkit-box-decoration-break: clone; box-decoration-break: clone;
      text-shadow: 0 1px 2px rgba(0, 0, 0, .9);
    }
    .status {
      display: inline-flex; align-items: center; gap: .5em; font-size: 14px; font-weight: 600;
      background: rgba(0, 0, 0, .7); padding: 5px 12px; border-radius: 99px; color: #ddd;
    }
    .status::before {
      content: ""; width: 8px; height: 8px; border-radius: 50%; background: #e6b13a;
      animation: p 1.2s infinite;
    }
    .status.bad { font-size: 15px; color: #fff; background: rgba(120, 20, 20, .88); border-radius: 10px;
                  max-width: 640px; text-align: left; line-height: 1.4; padding: 8px 14px; margin-top: 6px; }
    .status.bad::before { background: #ff6b6b; animation: none; flex: none; }
    @keyframes p { 50% { opacity: .2; } }
  `;

  function fullscreenParent() {
    let el = document.fullscreenElement || document.webkitFullscreenElement || null;
    // Children of a fullscreen <video> are not painted: hang from its parent instead.
    if (el && /^(VIDEO|AUDIO|IMG|CANVAS)$/.test(el.tagName)) el = el.parentElement;
    return el || document.documentElement;
  }

  // In fullscreen the browser only paints the fullscreen element and its descendants, so
  // the overlay has to move inside it (and back out when leaving fullscreen).
  function anchor() {
    if (!host) return;
    const parent = fullscreenParent();
    if (host.parentNode !== parent) parent.appendChild(host);
  }
  document.addEventListener("fullscreenchange", anchor);
  document.addEventListener("webkitfullscreenchange", anchor);

  function applyStyle() {
    if (!box) return;
    const lh = Math.round(fontSize * 1.38);
    box.style.fontSize = fontSize + "px";
    box.style.lineHeight = lh + "px";
    clip.style.maxHeight = lh * lines + "px";
  }

  async function restorePosition() {
    try {
      const { overlayPos } = await api.storage.local.get("overlayPos");
      if (overlayPos && box) {
        box.style.left = overlayPos.x * 100 + "%";
        box.style.top = overlayPos.y * 100 + "%";
        clampIntoView();
      }
    } catch (e) { /* ignore */ }
  }

  function makeDraggable() {
    let sx = 0, sy = 0, startL = 0, startT = 0;
    const move = (e) => {
      const x = startL + (e.clientX - sx);
      const y = startT + (e.clientY - sy);
      box.style.left = x + "px";
      box.style.top = y + "px";
    };
    const up = () => {
      document.removeEventListener("mousemove", move, true);
      document.removeEventListener("mouseup", up, true);
      const r = box.getBoundingClientRect();
      const pos = {
        x: (r.left + r.width / 2) / window.innerWidth,
        y: (r.top + r.height / 2) / window.innerHeight,
      };
      box.style.left = pos.x * 100 + "%";
      box.style.top = pos.y * 100 + "%";
      api.storage.local.set({ overlayPos: pos }).catch(() => {});
    };
    box.addEventListener("mousedown", (e) => {
      if (e.button !== 0) return;
      e.preventDefault();
      const r = box.getBoundingClientRect();
      sx = e.clientX; sy = e.clientY;
      startL = r.left + r.width / 2; startT = r.top + r.height / 2;
      document.addEventListener("mousemove", move, true);
      document.addEventListener("mouseup", up, true);
    });
  }

  // A window moved to another screen (other resolution / DPI) can leave the overlay
  // outside the viewport: then it goes back to the default spot.
  function clampIntoView() {
    if (!box) return;
    const r = box.getBoundingClientRect();
    const m = 24;
    const visible = r.right > m && r.left < innerWidth - m && r.bottom > m && r.top < innerHeight - m;
    if (!visible) {
      box.style.left = "50%";
      box.style.top = "85%";
    }
  }
  window.addEventListener("resize", clampIntoView);

  function create() {
    if (host) return;
    host = document.createElement("stream-transcription-overlay");
    const root = host.attachShadow({ mode: "open" });
    const style = document.createElement("style");
    style.textContent = CSS;
    box = document.createElement("div");
    box.className = "box";
    clip = document.createElement("div");
    clip.className = "clip";
    const para = document.createElement("p");
    para.className = "para";
    textEl = document.createElement("span");
    textEl.className = "line";
    textEl.hidden = true;
    para.appendChild(textEl);
    clip.appendChild(para);
    statusEl = document.createElement("div");
    statusEl.className = "status";
    statusEl.hidden = true;
    box.append(clip, statusEl);
    root.append(style, box);
    applyStyle();
    makeDraggable();
    anchor();
    restorePosition();
  }

  function destroy() {
    if (host) host.remove();
    host = box = clip = textEl = statusEl = null;
    hasText = false;
  }

  function setStatus(text, bad) {
    if (!statusEl) return;
    if (!text || (hasText && !bad)) {
      statusEl.hidden = true;
      return;
    }
    statusEl.textContent = text;
    statusEl.classList.toggle("bad", !!bad);
    statusEl.hidden = false;
  }

  function showSegments(segments) {
    if (!textEl || !Array.isArray(segments)) return;
    if (saveSrt) collect(segments);
    const text = segments.map((s) => (s && s.text) || "").join(" ").replace(/\s+/g, " ").trim();
    if (!text) return;
    hasText = true;
    statusEl.hidden = true;
    textEl.hidden = false;
    textEl.textContent = text;
  }

  // ------------------------------------------------------------------------------- SRT
  function collect(segments) {
    segments.forEach((seg) => {
      if (!seg || !seg.text) return;
      const last = srt[srt.length - 1];
      if (seg.completed === true) {
        if (!last || parseFloat(seg.start) >= parseFloat(last.end)) {
          srt.push({ start: seg.start, end: seg.end, text: seg.text });
        }
        lastIncomplete = null;
      } else {
        lastIncomplete = seg;
      }
    });
  }

  function fmt(sec) {
    const d = new Date(Math.max(0, parseFloat(sec) || 0) * 1000);
    const p = (n, l = 2) => String(n).padStart(l, "0");
    return `${p(d.getUTCHours())}:${p(d.getUTCMinutes())}:${p(d.getUTCSeconds())},${p(d.getUTCMilliseconds(), 3)}`;
  }

  function downloadSrt() {
    const last = srt[srt.length - 1];
    if (lastIncomplete && lastIncomplete.text && lastIncomplete.text.trim() &&
        (!last || parseFloat(lastIncomplete.start) >= parseFloat(last.end))) {
      srt.push(lastIncomplete);
    }
    if (!srt.length) return;
    const body = srt.map((s, i) =>
      `${i + 1}\n${fmt(s.start)} --> ${fmt(s.end)}\n${String(s.text).trim().replace(/[\r\n]+/g, " ")}`
    ).join("\n\n") + "\n";
    const url = URL.createObjectURL(new Blob([body], { type: "text/plain;charset=utf-8" }));
    const a = document.createElement("a");
    const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-");
    a.href = url;
    a.download = `subtitles-${stamp}.srt`;
    a.style.display = "none";
    document.documentElement.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1000);
  }

  // --------------------------------------------------------------------------- messages
  api.runtime.onMessage.addListener((msg) => {
    if (!msg || msg.st !== "overlay") return;
    switch (msg.op) {
      case "show":
        lines = msg.lines || lines;
        fontSize = msg.fontSize || fontSize;
        saveSrt = !!msg.saveSrt;
        srt = [];
        lastIncomplete = null;
        destroy();
        create();
        setStatus(msg.status);
        break;
      case "status":
        create();
        setStatus(msg.text, msg.bad);
        break;
      case "segments":
        create();
        showSegments(msg.segments);
        break;
      case "style":
        if (msg.lines) lines = msg.lines;
        if (msg.fontSize) fontSize = msg.fontSize;
        applyStyle();
        break;
      case "stop":
        if (saveSrt) downloadSrt();
        srt = [];
        destroy();
        break;
    }
  });

  window.__stOverlay = true;
})();
