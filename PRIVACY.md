# Privacy policy — Stream Transcription

*Last updated: 7 November 2026*

Stream Transcription does not collect, store or share any personal data with its developer or
with any third party.

**What the extension sends, and where.** When you press *Start subtitles*, the audio of the
current tab is streamed to the server address you typed in the extension (usually a
WhisperLive server on your own computer or local network), and the subtitles come back from
it. Nothing is sent anywhere else. The extension contacts no server of its own, has no
analytics and no tracking.

**What it stores.** Your settings (server address, chosen model and languages, subtitle size
and position) are kept in your browser's extension storage. If you turn on *Save subtitles*,
an `.srt` file is downloaded to your computer when you stop.

**Update checks.** Only when you press *Check for updates*, the extension asks GitHub
(api.github.com) for the number of the latest release. The request carries no data about you
or your use of the extension; like any web request, GitHub sees your IP address and your
browser's name. Nothing is checked in the background.

**Model downloads.** When you ask to add a model, the request goes to your server, and your
server downloads it from Hugging Face or from the link you gave.

**Contact.** Open an issue at https://github.com/javimentallab/stream-transcription/issues

---

## Política de privacidad (español)

Stream Transcription no recoge, guarda ni comparte datos personales con su desarrollador ni con
terceros. Al pulsar *Activar subtítulos*, el audio de la pestaña se envía a la dirección de
servidor que hayas escrito (normalmente un servidor WhisperLive en tu ordenador o tu red) y de
él vuelven los subtítulos; no se envía nada a ningún otro sitio. Solo cuando pulsas *Buscar
actualizaciones*, la extensión pregunta a GitHub (api.github.com) el número de la última versión;
esa consulta no lleva datos tuyos ni de tu uso, aunque, como toda petición web, GitHub ve tu
dirección IP y el nombre de tu navegador. Los ajustes se guardan en el
almacenamiento de extensiones de tu navegador. Si activas *Guardar los subtítulos*, al parar se
descarga un fichero `.srt` a tu ordenador.
