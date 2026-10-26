# Stream Transcription server = WhisperLive (Collabora) + the Stream Transcription patches:
#   - the browser extension can list / download / delete Whisper models (whisper_live/st_models.py)
#   - the model the client picks is really used, and switching frees the previous one
#   - one shared copy of the translator for every client
#   - per-client options: int8 precision, translator on the CPU
#   - "out of memory" errors are reported to the client instead of silently freezing
#
# Base image pinned by digest: the patched files are written against this exact version.
FROM ghcr.io/collabora/whisperlive-gpu@sha256:fb95a19a7cb13839d074d6f94d3e546bfc92014a9f4dee24f153de208fe456cc

# That image ships CUDA 13 (torch) but faster-whisper's CTranslate2 is built against
# CUDA 12 and looks for libcublas.so.12; the image's LD_LIBRARY_PATH already points to
# where this wheel installs it.
RUN pip install --no-cache-dir nvidia-cublas-cu12

COPY whisper_live/ /app/whisper_live/
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Runs as an unprivileged user. uid 1000 so a bind-mounted folder owned by the usual
# desktop user also works; the named volume in docker-compose.yml takes this ownership.
RUN useradd --uid 1000 --create-home st \
 && mkdir -p /home/st/.cache \
 && chown st:st /home/st/.cache
USER st

# Models (Hugging Face cache + converted ones) live here: mount a volume to keep them.
VOLUME /home/st/.cache
EXPOSE 9090
# The first start downloads the default model before listening, hence the long start period.
# A real WebSocket handshake (a bare TCP connect makes the server log a traceback); every
# probe still logs a connect/disconnect, so it runs every 5 minutes once started.
HEALTHCHECK --interval=5m --start-interval=30s --timeout=5s --start-period=10m --retries=3 \
  CMD python -c "from websockets.sync.client import connect; connect('ws://127.0.0.1:9090', open_timeout=3).close()"
CMD ["/app/start.sh"]
