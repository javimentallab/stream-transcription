// Interface texts. Uses the _locales/*/messages.json files, but loads them itself so the
// user can pick the interface language in the settings instead of always following the
// browser's. Placeholders are written {0}, {1}...
"use strict";

(function () {
  const SUPPORTED = ["en", "es"];
  let messages = {};
  let fallback = {};

  async function load(lang) {
    const res = await fetch(ext.runtime.getURL(`_locales/${lang}/messages.json`));
    return res.json();
  }

  function pickLang(setting) {
    if (SUPPORTED.includes(setting)) return setting;
    const ui = (ext.i18n && ext.i18n.getUILanguage ? ext.i18n.getUILanguage() : navigator.language) || "en";
    const base = ui.toLowerCase().split(/[-_]/)[0];
    return SUPPORTED.includes(base) ? base : "en";
  }

  const I = {
    lang: "en",

    async init() {
      const settings = await ST.getSettings();
      I.lang = pickLang(settings.uiLang);
      fallback = await load("en");
      messages = I.lang === "en" ? fallback : await load(I.lang);
      if (globalThis.document) document.documentElement.lang = I.lang;
      return I.lang;
    },

    t(key, ...args) {
      const entry = messages[key] || fallback[key];
      let s = entry ? entry.message : key;
      args.forEach((a, i) => { s = s.split(`{${i}}`).join(String(a)); });
      return s;
    },

    // <x data-i18n="key">, data-i18n-placeholder, data-i18n-title, data-i18n-aria
    apply(root = document) {
      root.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = I.t(el.dataset.i18n); });
      root.querySelectorAll("[data-i18n-placeholder]").forEach((el) => { el.placeholder = I.t(el.dataset.i18nPlaceholder); });
      root.querySelectorAll("[data-i18n-title]").forEach((el) => { el.title = I.t(el.dataset.i18nTitle); });
      root.querySelectorAll("[data-i18n-aria]").forEach((el) => { el.setAttribute("aria-label", I.t(el.dataset.i18nAria)); });
    },
  };

  ST.i18n = I;
  ST.t = (...a) => I.t(...a);
})();
