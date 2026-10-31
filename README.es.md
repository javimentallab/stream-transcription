# Stream Transcription

**Subtítulos en directo para cualquier pestaña del navegador, transcritos y traducidos por tu propio servidor Whisper.**

Mira un directo de Twitch, un vídeo de YouTube o una llamada en un idioma que no hablas y
léelo en el tuyo, en tiempo real. El audio no sale de tu red: solo va al servidor
[WhisperLive](https://github.com/collabora/WhisperLive) que tú montes.

[English version](README.md)

![Subtítulos traducidos sobre un directo](store/screenshot-1-subtitles.png)

## Qué hace

- **Subtítulos encima de cualquier web**: Twitch, YouTube, Kick, cualquier `<video>`… Siguen
  en pantalla completa, se pueden arrastrar, y eliges de 1 a 4 líneas y el tamaño del texto.
- **Traducción**: la del propio Whisper al inglés, o a unos 100 idiomas con el traductor del
  servidor.
- **Cualquier modelo Whisper, desde la extensión**: pega el nombre o el enlace de un modelo de
  Hugging Face (`Systran/faster-whisper-large-v3`, uno ajustado para tu idioma, un `.zip`
  directo…) y el servidor lo descarga; los modelos normales (*transformers*) se convierten
  solos al formato de faster-whisper. Luego lo eliges de una lista. Sin rutas ni terminal.
- **Cabe en gráficas modestas**: la opción «int8» gasta la mitad de memoria con el mismo
  texto, el traductor puede ir en el procesador, y si el modelo no cabe sale un **aviso de
  VRAM** en vez de unos subtítulos que se congelan sin decir nada.
- **Guarda los subtítulos** en un `.srt` al parar.
- Interfaz en castellano, inglés, portugués, francés, alemán, italiano, neerlandés, polaco, ruso, ucraniano,
  chino, japonés, coreano, tailandés e hindi; sigue al navegador o se elige en los ajustes.
- Sin cuentas, sin rastreo, sin estadísticas. Código abierto (MIT).

## Instalar la extensión

- **Firefox** (y Zen, LibreWolf, Floorp…): [addons.mozilla.org](https://addons.mozilla.org/firefox/addon/stream-transcription/)
- **Chromium** (Chrome, Brave, Edge, Opera, Vivaldi…): descarga
  `stream-transcription-chromium-<versión>.zip` de la
  [última versión](https://github.com/javimentallab/stream-transcription/releases/latest),
  descomprímelo, abre `chrome://extensions`, activa el **Modo de desarrollador** y pulsa
  **Cargar descomprimida** sobre la carpeta.

Después pulsa el icono de la extensión, escribe la dirección de tu servidor (p. ej.
`192.168.1.10:9090`) y **Conectar**.

## Servidor

Necesitas un servidor WhisperLive, mejor en un ordenador con tarjeta gráfica NVIDIA (los
modelos pequeños también van solo con el procesador). Dos opciones:

### Opción A — servidor de Stream Transcription (recomendada)

WhisperLive más los parches que hacen funcionar todo lo de la extensión (gestión de modelos,
cambio de modelo, int8, traductor en el procesador, avisos de VRAM). Con Docker y el
[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```sh
git clone https://github.com/javimentallab/stream-transcription.git
cd stream-transcription/server
docker compose up -d --build
```

El primer arranque descarga el modelo por defecto (`Systran/faster-whisper-small`, ~0,5 GB).
El servidor escucha en el puerto **9090**, funciona con un usuario sin privilegios y guarda
los modelos en el volumen de Docker `models` (la antigua carpeta `server/models/` ya no se usa
y se puede borrar; los modelos se vuelven a descargar). Opciones en `docker-compose.yml`:

| Variable | Por defecto | Qué hace |
|---|---|---|
| `ST_DEFAULT_MODEL` | `Systran/faster-whisper-small` | Modelo que se descarga y se usa por defecto |
| `ST_ALLOW_MANAGEMENT` | `1` | `0` = la extensión puede ver los modelos pero no descargarlos ni borrarlos |
| `ST_MAX_CLIENTS` | `4` | Transcripciones a la vez |
| `HF_TOKEN` | — | Para modelos de Hugging Face restringidos o privados |

Quien llegue al puerto puede usar el servidor (y, con la gestión activada, descargar o borrar
modelos): déjalo dentro de tu red o detrás de un cortafuegos.

### Opción B — WhisperLive tal cual

La extensión también funciona con un WhisperLive sin modificar. En ese caso escribes un
tamaño de modelo (`tiny`, `small`, `medium`, `large-v3`…) en vez de elegirlo de una lista, y
no hay gestión de modelos ni opciones de rendimiento.

## ¿Cuánta memoria gráfica?

| Modelo | VRAM (float16) | Con «Ahorrar memoria (int8)» |
|---|---|---|
| small | ~1 GB | ~0,6 GB |
| medium | ~2 GB | ~1,2 GB |
| large-v3 / turbo | ~4 GB | ~2,3 GB |

El traductor suma ~0,7 GB en la gráfica (o nada, si lo pones en el procesador).

## Privacidad

La extensión envía el audio de la pestaña **solo** a la dirección de servidor que escribas, y
nada a ningún otro sitio. Guarda sus ajustes en tu navegador. Ver [PRIVACY.md](PRIVACY.md).

## Compilar

```sh
python tools/build.py
```

Genera `dist/chromium`, `dist/firefox` y sus zips a partir de `extension/shared` más la
carpeta de cada navegador. Los textos en inglés y castellano están juntos en
`tools/i18n-messages.py`, y los demás idiomas en `tools/i18n-more.py`; el script comprueba cada clave y
hueco contra el inglés.

## Créditos y licencia

MIT ([LICENSE](LICENSE)). Hecho sobre [WhisperLive](https://github.com/collabora/WhisperLive), de Collabora (MIT, ver
[NOTICE](NOTICE)), y
[faster-whisper](https://github.com/SYSTRAN/faster-whisper). La traducción usa
[SMALL100](https://huggingface.co/alirezamsh/small100).
