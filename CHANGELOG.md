# Changelog

All notable changes to Stream Transcription. Versions follow [semantic versioning](https://semver.org/).

## 2.2.0 — 2026-11-07

### Added
- **Check for updates**, at the bottom of the popup and in Settings → About. Only when you press it, the
  extension asks GitHub for the number of the latest release and says whether a newer one exists.
  **Update** then opens the page to get it: the add-on's page on Firefox Add-ons in Firefox (which also
  updates it by itself), or the release on GitHub in Chromium. The extension never downloads code or
  replaces itself, and nothing is checked in the background.
- In Settings → About, the same check says whether your Stream Transcription server is up to date, behind,
  or too old to report its version, and shows the commands to update it.
- The server reports its version with every answer to the extension.

### Changed
- The privacy policy and the README explain the request to GitHub.

### Security
- No vulnerabilities fixed in this release. No new permissions.

## 2.1.1 — 2026-11-02

### Fixed
- Extension: session ids no longer rely on `Math.random`.
- Server: errors no longer send exception text to clients; the details go to the server log.
- Server image: the NVIDIA wheels are pinned and declared in `NOTICE`.

### Added
- The Firefox Add-ons listing in 13 languages; a security policy, a contributing guide, tests in CI and
  CodeQL, with every GitHub Action pinned by commit.

### Security
- The three CodeQL alerts above (weak randomness for session ids, exception text sent to clients).

## 2.1.0 — 2026-10-31

### Added
- The interface in 13 more languages: Portuguese, French, German, Italian, Dutch, Polish, Russian,
  Ukrainian, Chinese, Japanese, Korean, Thai and Hindi, besides English and Spanish.

### Changed
- Firefox: minimum version 140 (Android 142).

## 2.0.0 — 2026-10-16

First release: live subtitles for any browser tab, transcribed and translated by your own WhisperLive
server, with model management from the extension, int8 precision, the translator on the CPU and clear
VRAM warnings.
