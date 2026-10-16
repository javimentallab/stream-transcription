#!/usr/bin/env python3
"""Builds the two packages from extension/shared + extension/<browser>:

    dist/chromium/  + dist/stream-transcription-chromium-<version>.zip  (Brave, Chrome, Edge…)
    dist/firefox/   + dist/stream-transcription-firefox-<version>.zip   (Firefox, Zen, LibreWolf…)

Before building it regenerates the texts and the icons, and checks that every text key
used in the code exists in both languages.
Run:  python tools/build.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EXT = os.path.join(ROOT, "extension")
DIST = os.path.join(ROOT, "dist")
TOOLS = os.path.join(ROOT, "tools")


def run_tool(name):
    subprocess.run([sys.executable, "-I", os.path.join(TOOLS, name)], check=True)


def check_keys():
    """Every t("key") / data-i18n="key" in the code must exist in en and es."""
    msgs = {}
    for lang in ("en", "es"):
        with open(os.path.join(EXT, "shared", "_locales", lang, "messages.json"), encoding="utf-8") as fh:
            msgs[lang] = json.load(fh)
    used = set()
    dynamic_prefixes = ("status_", "err_")
    for folder, _dirs, files in os.walk(EXT):
        if "_locales" in folder:
            continue
        for f in files:
            if not f.endswith((".js", ".html", ".json")):
                continue
            with open(os.path.join(folder, f), encoding="utf-8") as fh:
                src = fh.read()
            used |= set(re.findall(r'\bt\("([a-z0-9_]+)"\s*[,)]', src))
            used |= set(re.findall(r'data-i18n(?:-placeholder|-title|-aria)?="([a-z0-9_]+)"', src))
            used |= set(re.findall(r"__MSG_([A-Za-z0-9_]+)__", src))
    used.discard("key")   # the example in i18n.js's comment
    missing = [(lang, k) for k in sorted(used) for lang in msgs if k not in msgs[lang]]
    if missing:
        raise SystemExit("missing texts: " + ", ".join(f"{lang}:{k}" for lang, k in missing))
    unused = sorted(k for k in msgs["en"] if k not in used and not k.startswith(dynamic_prefixes))
    if unused:
        print("note: texts not referenced directly:", ", ".join(unused))


def build(browser):
    out = os.path.join(DIST, browser)
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(EXT, "shared"), out)
    shutil.copytree(os.path.join(EXT, browser), out, dirs_exist_ok=True)
    with open(os.path.join(out, "manifest.json"), encoding="utf-8") as fh:
        version = json.load(fh)["version"]
    zpath = os.path.join(DIST, f"stream-transcription-{browser}-{version}.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _dirs, files in os.walk(out):
            for f in sorted(files):
                full = os.path.join(folder, f)
                # forward slashes and no leading "./": AMO rejects anything else
                z.write(full, os.path.relpath(full, out).replace(os.sep, "/"))
    print(f"{browser}: {out}  ->  {os.path.basename(zpath)}")


def main():
    run_tool("i18n-messages.py")
    run_tool("make-icons.py")
    check_keys()
    os.makedirs(DIST, exist_ok=True)
    for browser in ("chromium", "firefox"):
        build(browser)


if __name__ == "__main__":
    main()
