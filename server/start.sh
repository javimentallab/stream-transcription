#!/bin/sh
# Downloads the default model the first time (later starts reuse the cache) and starts
# WhisperLive in single-model mode, which is what lets clients switch models.
set -e

MODEL="${ST_DEFAULT_MODEL:-Systran/faster-whisper-small}"
echo "[stream-transcription] default model: $MODEL"
MODEL_PATH=$(python -c "from huggingface_hub import snapshot_download; print(snapshot_download('$MODEL'))")

exec python run_server.py \
  --port 9090 \
  --backend faster_whisper \
  --max_clients "${ST_MAX_CLIENTS:-4}" \
  --max_connection_time "${ST_MAX_CONNECTION_TIME:-86400}" \
  --faster_whisper_custom_model_path "$MODEL_PATH"
