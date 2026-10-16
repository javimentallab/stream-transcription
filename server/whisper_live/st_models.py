"""
Stream Transcription - model management for a WhisperLive server.

Lets the browser extension list the Whisper models installed on the server, download new
ones (from Hugging Face or from a direct .zip/.tar.gz link) and delete them. Models in
Hugging Face *transformers* format (fine-tuned Whisper checkpoints) are converted to
CTranslate2 on the fly, because that is the only format faster-whisper can load.

Protocol: the extension opens a normal WhisperLive WebSocket and sends, as its FIRST
message, a JSON object with an ``st_action`` key instead of the usual transcription
options. The server answers with a single JSON object and closes the connection:

    {"st_action": "list_models"}
    {"st_action": "download_model", "source": "<repo id | HF url | archive url>"}
    {"st_action": "delete_model", "id": "<model id>"}

Environment variables:
    ST_MODELS_DIR       where converted / archive models live
                        (default: ~/.cache/stream-transcription)
    ST_ALLOW_MANAGEMENT "0" disables download/delete (listing still works). Default "1".
    HF_TOKEN            optional, for gated or private Hugging Face repos.
"""

import fnmatch
import json
import logging
import os
import re
import shutil
import tarfile
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import zipfile

PROTOCOL_VERSION = 1

ST_ROOT = os.path.expanduser(
    os.environ.get("ST_MODELS_DIR", "~/.cache/stream-transcription"))
CONVERTED_DIR = os.path.join(ST_ROOT, "converted")
ARCHIVE_DIR = os.path.join(ST_ROOT, "models")
ALLOW_MANAGEMENT = os.environ.get("ST_ALLOW_MANAGEMENT", "1") not in ("0", "false", "no")

_REPO_RE = re.compile(r"^[A-Za-z0-9][\w.-]{0,95}/[\w.-]{1,96}$")
_HF_URL_RE = re.compile(
    r"^https?://(?:www\.)?huggingface\.co/([\w.-]+/[\w.-]+)(?:/(?:tree|blob)/([^/?#]+))?/?(?:[?#].*)?$")
_ARCHIVE_EXT = (".zip", ".tar.gz", ".tgz", ".tar")

# Files of a transformers Whisper checkpoint that the converter needs. Everything else
# (flax, tf, onnx, coreml, ggml...) can be several GB and is useless here.
_TRANSFORMERS_FILES = (
    "config.json", "generation_config.json", "preprocessor_config.json",
    "tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt",
    "normalizer.json", "added_tokens.json", "special_tokens_map.json",
)
_SKIP_PATTERNS = (
    "*.msgpack", "*.h5", "*.onnx", "*.onnx_data", "*.ot", "*.tflite", "*.gguf",
    "ggml*", "*.mlmodelc/*", "*.mlpackage/*", "*.pt", "*.ckpt",
)

_jobs = {}          # model id -> job dict (see _new_job)
_jobs_lock = threading.Lock()
_hub_root_cache = None


# --------------------------------------------------------------------------------------
# Locating models
# --------------------------------------------------------------------------------------

def _hub_root(default_path=None):
    """The Hugging Face hub cache directory the server already uses."""
    global _hub_root_cache
    if default_path:
        parts = os.path.abspath(default_path).split(os.sep)
        if "hub" in parts:
            _hub_root_cache = os.sep.join(parts[:parts.index("hub") + 1])
    if _hub_root_cache:
        return _hub_root_cache
    try:
        from huggingface_hub import constants
        return constants.HF_HUB_CACHE
    except Exception:
        return os.path.expanduser("~/.cache/huggingface/hub")


def _dir_size(path):
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def _is_ct2_whisper(path):
    """True if ``path`` holds a CTranslate2 Whisper model faster-whisper can load."""
    if not os.path.isfile(os.path.join(path, "model.bin")):
        return False
    cfg_path = os.path.join(path, "config.json")
    if not os.path.isfile(cfg_path):
        return True     # old conversions have no config.json; give them the benefit
    try:
        with open(cfg_path, encoding="utf-8") as fh:
            cfg = json.load(fh)
    except Exception:
        return True
    # A CT2 Whisper config carries these; a CT2 translation model (e.g. NLLB) does not.
    return any(k in cfg for k in ("lang_ids", "suppress_ids", "alignment_heads",
                                  "suppress_ids_begin"))


def _transformers_model_type(path):
    try:
        with open(os.path.join(path, "config.json"), encoding="utf-8") as fh:
            return json.load(fh).get("model_type")
    except Exception:
        return None


def _snapshot_dirs(repo_dir):
    snaps = os.path.join(repo_dir, "snapshots")
    if not os.path.isdir(snaps):
        return []
    out = [os.path.join(snaps, s) for s in os.listdir(snaps)]
    out = [p for p in out if os.path.isdir(p)]
    # newest first
    out.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return out


def _repo_id_from_cache_dir(name):
    # models--Systran--faster-whisper-small -> Systran/faster-whisper-small
    parts = name.split("--")[1:]
    if len(parts) >= 2:
        return parts[0] + "/" + "--".join(parts[1:])
    return parts[0] if parts else name


def _scan(default_path=None):
    """Return {id: info} of every usable model on disk."""
    models = {}

    hub = _hub_root(default_path)
    if hub and os.path.isdir(hub):
        for entry in sorted(os.listdir(hub)):
            if not entry.startswith("models--"):
                continue
            repo_dir = os.path.join(hub, entry)
            for snap in _snapshot_dirs(repo_dir):
                if _is_ct2_whisper(snap):
                    mid = _repo_id_from_cache_dir(entry)
                    models[mid] = {
                        "id": mid, "path": snap, "source": "huggingface",
                        "size": _dir_size(os.path.join(repo_dir, "blobs")) or _dir_size(snap),
                    }
                    break

    if os.path.isdir(CONVERTED_DIR):
        for entry in sorted(os.listdir(CONVERTED_DIR)):
            path = os.path.join(CONVERTED_DIR, entry)
            if os.path.isdir(path) and _is_ct2_whisper(path):
                mid = entry.replace("--", "/", 1)
                models[mid] = {"id": mid, "path": path, "source": "converted",
                               "size": _dir_size(path)}

    if os.path.isdir(ARCHIVE_DIR):
        for entry in sorted(os.listdir(ARCHIVE_DIR)):
            path = os.path.join(ARCHIVE_DIR, entry)
            if os.path.isdir(path) and _is_ct2_whisper(path):
                mid = "url:" + entry
                models[mid] = {"id": mid, "path": path, "source": "url",
                               "size": _dir_size(path)}

    return models


def _id_for_path(path, models):
    if not path:
        return None
    norm = os.path.normpath(path)
    for m in models.values():
        if os.path.normpath(m["path"]) == norm:
            return m["id"]
    return None


def _loaded_path():
    try:
        from whisper_live.backend.faster_whisper_backend import ServeClientFasterWhisper
        return getattr(ServeClientFasterWhisper, "SINGLE_MODEL_REF", None)
    except Exception:
        return None


def _in_use_path():
    """Path of the model a live transcription is using right now (None if idle)."""
    try:
        from whisper_live.backend.faster_whisper_backend import ServeClientFasterWhisper
        if getattr(ServeClientFasterWhisper, "SINGLE_MODEL_USERS", 1) > 0:
            return getattr(ServeClientFasterWhisper, "SINGLE_MODEL_REF", None)
    except Exception:
        pass
    return None


def resolve(requested, default_path):
    """
    Map what a client asks for to something faster-whisper can load.

    Accepts a model id from ``list_models`` ("Systran/faster-whisper-small",
    "url:my-model"), a legacy size name ("small", "large-v3"), or an absolute path that
    exists on the server. Anything not installed falls back to ``default_path``: the
    server never downloads during a transcription request (it takes minutes and the
    client is waiting).
    """
    if not requested or not isinstance(requested, str) or not requested.strip():
        return default_path
    requested = requested.strip()

    if os.path.isabs(requested) and os.path.isdir(requested) and _is_ct2_whisper(requested):
        return requested

    models = _scan(default_path)
    if requested in models:
        return models[requested]["path"]

    low = requested.lower()
    for mid, info in models.items():
        tail = mid.split("/")[-1].split(":")[-1].lower()
        if tail in (low, "faster-whisper-" + low):
            return info["path"]

    if default_path:
        logging.info("[stream-transcription] model '%s' is not installed; using the "
                     "default one", requested)
        return default_path
    # No default model configured: let faster-whisper handle size names itself
    # ("small", "medium"...). It downloads them on first use, as upstream does.
    return requested


# --------------------------------------------------------------------------------------
# Jobs (download / convert) - run in background threads
# --------------------------------------------------------------------------------------

def _new_job(mid, source):
    return {
        "id": mid, "source": source, "state": "downloading",
        "downloaded": 0, "total": 0, "error": None, "detail": None,
        "started": time.time(), "updated": time.time(),
    }


def _update(job, **kw):
    with _jobs_lock:
        job.update(kw)
        job["updated"] = time.time()


def _public_jobs():
    now = time.time()
    with _jobs_lock:
        # finished jobs stay visible for 10 minutes so the page can show the outcome
        for mid in [k for k, j in _jobs.items()
                    if j["state"] in ("ready", "error") and now - j["updated"] > 600]:
            del _jobs[mid]
        return [dict(j) for j in _jobs.values()]


def _parse_source(source):
    """-> ("hf", repo_id, revision) | ("url", url, slug)  or raise ValueError."""
    if not isinstance(source, str):
        raise ValueError("invalid_source")
    s = source.strip()
    m = _HF_URL_RE.match(s)
    if m:
        return "hf", m.group(1), m.group(2)
    if _REPO_RE.match(s):
        return "hf", s, None
    if re.match(r"^https?://", s, re.I):
        path = urllib.parse.urlparse(s).path
        name = os.path.basename(path)
        low = name.lower()
        for ext in _ARCHIVE_EXT:
            if low.endswith(ext):
                slug = re.sub(r"[^\w.-]+", "-", name[: -len(ext)]).strip("-.") or "model"
                return "url", s, slug[:80]
        raise ValueError("unsupported_url")
    raise ValueError("invalid_source")


def _plan_hf_files(repo_id, revision):
    """Decide which files of a repo to fetch. Returns (kind, [filenames], total_bytes)."""
    from huggingface_hub import HfApi
    info = HfApi().model_info(repo_id, revision=revision, files_metadata=True)
    siblings = {s.rfilename: (s.size or 0) for s in (info.siblings or [])}
    names = set(siblings)

    def skipped(n):
        return any(fnmatch.fnmatch(n, p) for p in _SKIP_PATTERNS)

    if "model.bin" in names:
        kind = "ct2"
        files = [n for n in names if "/" not in n and not skipped(n)]
    elif "config.json" in names:
        kind = "transformers"
        weights = [n for n in names if "/" not in n and n.endswith(".safetensors")]
        if not weights:
            weights = [n for n in names if "/" not in n
                       and re.match(r"pytorch_model.*\.bin$", n)]
        if not weights:
            raise ValueError("no_weights")
        weights += [n for n in names if n.endswith(".safetensors.index.json")
                    or n == "pytorch_model.bin.index.json"]
        files = [n for n in names if n in _TRANSFORMERS_FILES] + weights
    else:
        raise ValueError("not_whisper")
    return kind, sorted(set(files)), sum(siblings.get(n, 0) for n in files)


def _convert(src_dir, out_dir, job):
    """Transformers Whisper checkpoint -> CTranslate2 (float16)."""
    _update(job, state="converting")
    if _transformers_model_type(src_dir) != "whisper":
        raise ValueError("not_whisper")
    import ctranslate2
    tmp_out = out_dir + ".partial"
    shutil.rmtree(tmp_out, ignore_errors=True)
    # faster-whisper wants tokenizer.json. Some fine-tunes only ship vocab.json +
    # merges.txt: build it with the fast tokenizer so it does not fall back to a hub
    # download at load time.
    if not os.path.isfile(os.path.join(src_dir, "tokenizer.json")):
        try:
            from transformers import WhisperTokenizerFast
            WhisperTokenizerFast.from_pretrained(src_dir).save_pretrained(src_dir)
        except Exception as e:
            logging.warning("[stream-transcription] could not build tokenizer.json: %s", e)
    copy = [f for f in ("tokenizer.json", "preprocessor_config.json")
            if os.path.isfile(os.path.join(src_dir, f))]
    class _Converter(ctranslate2.converters.TransformersConverter):
        # Recent CTranslate2 calls from_pretrained(..., dtype=...), a keyword that
        # transformers only understands since 4.56 (before it was torch_dtype).
        def load_model(self, model_class, model_name_or_path, **kwargs):
            try:
                return model_class.from_pretrained(model_name_or_path, **kwargs)
            except TypeError as e:
                if "dtype" not in kwargs or "dtype" not in str(e):
                    raise
                kwargs["torch_dtype"] = kwargs.pop("dtype")
                return model_class.from_pretrained(model_name_or_path, **kwargs)

    _Converter(src_dir, copy_files=copy, load_as_float16=True).convert(
        tmp_out, quantization="float16", force=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.replace(tmp_out, out_dir)


def _run_hf_job(job, repo_id, revision, hub):
    from huggingface_hub import snapshot_download
    try:
        kind, files, total = _plan_hf_files(repo_id, revision)
        _update(job, total=total, detail=kind)
        repo_dir = os.path.join(hub, "models--" + repo_id.replace("/", "--"))
        stop = threading.Event()

        def watch():
            while not stop.wait(1.0):
                blobs = os.path.join(repo_dir, "blobs")
                if os.path.isdir(blobs):
                    _update(job, downloaded=min(_dir_size(blobs), total or 1 << 62))

        watcher = threading.Thread(target=watch, daemon=True)
        watcher.start()
        try:
            snap = snapshot_download(repo_id, revision=revision, cache_dir=hub,
                                     allow_patterns=files)
        finally:
            stop.set()
        _update(job, downloaded=total)

        if kind == "ct2":
            if not _is_ct2_whisper(snap):
                raise ValueError("not_whisper")
        else:
            out = os.path.join(CONVERTED_DIR, repo_id.replace("/", "--"))
            os.makedirs(CONVERTED_DIR, exist_ok=True)
            _convert(snap, out, job)
            # the original weights are no longer needed and can be several GB
            shutil.rmtree(repo_dir, ignore_errors=True)
        _update(job, state="ready")
        logging.info("[stream-transcription] model %s installed", repo_id)
    except Exception as e:
        _fail(job, e)
        # Leave nothing half-done behind (it would eat disk and never show up in the
        # list). A network error keeps the partial download so a retry resumes it.
        if job.get("error") != "network_error":
            shutil.rmtree(os.path.join(hub, "models--" + repo_id.replace("/", "--")),
                          ignore_errors=True)
            shutil.rmtree(os.path.join(CONVERTED_DIR, repo_id.replace("/", "--")) + ".partial",
                          ignore_errors=True)


def _safe_extract(archive_path, dest):
    dest_abs = os.path.abspath(dest)

    def check(name):
        target = os.path.abspath(os.path.join(dest, name))
        if not (target == dest_abs or target.startswith(dest_abs + os.sep)):
            raise ValueError("bad_archive")

    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path) as zf:
            for n in zf.namelist():
                check(n)
            zf.extractall(dest)
    else:
        with tarfile.open(archive_path) as tf:
            for mbr in tf.getmembers():
                check(mbr.name)
                if mbr.issym() or mbr.islnk() or mbr.isdev():
                    raise ValueError("bad_archive")
            tf.extractall(dest)


def _find_model_root(base):
    for root, _dirs, files in os.walk(base):
        if "model.bin" in files and _is_ct2_whisper(root):
            return root, "ct2"
    for root, _dirs, files in os.walk(base):
        if "config.json" in files and _transformers_model_type(root) == "whisper":
            return root, "transformers"
    return None, None


def _run_url_job(job, url, slug):
    tmpdir = tempfile.mkdtemp(prefix="st-dl-", dir=ST_ROOT)
    try:
        archive = os.path.join(tmpdir, "archive")
        req = urllib.request.Request(url, headers={"User-Agent": "stream-transcription"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(archive, "wb") as fh:
            total = int(resp.headers.get("Content-Length") or 0)
            _update(job, total=total)
            got = 0
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                fh.write(chunk)
                got += len(chunk)
                _update(job, downloaded=got)
        _update(job, state="extracting")
        extracted = os.path.join(tmpdir, "x")
        os.makedirs(extracted)
        _safe_extract(archive, extracted)
        os.remove(archive)
        root, kind = _find_model_root(extracted)
        if not root:
            raise ValueError("not_whisper")
        out = os.path.join(ARCHIVE_DIR, slug)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        if kind == "ct2":
            shutil.rmtree(out, ignore_errors=True)
            shutil.move(root, out)
        else:
            _convert(root, out, job)
        _update(job, state="ready")
        logging.info("[stream-transcription] model url:%s installed", slug)
    except Exception as e:
        _fail(job, e)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _fail(job, exc):
    code = str(exc) if isinstance(exc, ValueError) and re.match(r"^[a-z_]+$", str(exc)) else None
    if code is None:
        name = type(exc).__name__
        if "RepositoryNotFound" in name or "RevisionNotFound" in name:
            code = "repo_not_found"
        elif "GatedRepo" in name:
            code = "gated_repo"
        elif "HTTPError" in name or "URLError" in name or "Connection" in name:
            code = "network_error"
        elif "convert" in (job.get("state") or ""):
            code = "convert_failed"
        else:
            code = "download_failed"
    logging.error("[stream-transcription] job %s failed: %s", job["id"], exc)
    _update(job, state="error", error=code, detail=str(exc)[:300])


# --------------------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------------------

def list_models(default_path):
    models = _scan(default_path)
    default_id = _id_for_path(default_path, models)
    loaded_id = _id_for_path(_loaded_path(), models)
    jobs = _public_jobs()
    busy = {j["id"] for j in jobs if j["state"] not in ("ready", "error")}
    out = []
    for m in models.values():
        if m["id"] in busy:
            continue    # half-downloaded: model.bin may exist before the rest

        out.append({
            "id": m["id"], "source": m["source"], "size": m["size"],
            "default": m["id"] == default_id, "loaded": m["id"] == loaded_id,
        })
    out.sort(key=lambda m: (not m["default"], m["size"]))
    return {"ok": True, "models": out, "jobs": jobs,
            "default": default_id, "loaded": loaded_id}


def download_model(source, default_path):
    if not ALLOW_MANAGEMENT:
        return {"ok": False, "error": "management_disabled"}
    try:
        kind, a, b = _parse_source(source)
    except ValueError as e:
        return {"ok": False, "error": str(e)}

    mid = a if kind == "hf" else "url:" + b
    with _jobs_lock:
        cur = _jobs.get(mid)
        if cur and cur["state"] not in ("ready", "error"):
            return {"ok": False, "error": "already_downloading"}
    if mid in _scan(default_path):
        return {"ok": False, "error": "already_installed"}

    os.makedirs(ST_ROOT, exist_ok=True)
    job = _new_job(mid, source.strip())
    with _jobs_lock:
        _jobs[mid] = job
    if kind == "hf":
        target = _run_hf_job
        args = (job, a, b, _hub_root(default_path))
    else:
        target = _run_url_job
        args = (job, a, b)
    threading.Thread(target=target, args=args, daemon=True,
                     name="st-download-" + mid).start()
    return {"ok": True, "job": dict(job)}


def delete_model(mid, default_path):
    if not ALLOW_MANAGEMENT:
        return {"ok": False, "error": "management_disabled"}
    models = _scan(default_path)
    info = models.get(mid)
    if not info:
        return {"ok": False, "error": "not_found"}
    if os.path.normpath(info["path"]) == os.path.normpath(default_path or ""):
        return {"ok": False, "error": "is_default"}
    busy = _in_use_path()
    if busy and os.path.normpath(busy) == os.path.normpath(info["path"]):
        return {"ok": False, "error": "in_use"}

    if info["source"] == "huggingface":
        # .../hub/models--org--name/snapshots/<hash> -> .../hub/models--org--name
        target = os.path.dirname(os.path.dirname(info["path"]))
    else:
        target = info["path"]
    shutil.rmtree(target, ignore_errors=True)
    logging.info("[stream-transcription] model %s deleted", mid)
    return {"ok": True}


# --------------------------------------------------------------------------------------
# Per-request options (precision, translator device)
# --------------------------------------------------------------------------------------
# The transcription and translation clients are built in the same thread that read the
# client's options, so a thread-local is enough to hand them over without changing
# every constructor's signature.

_request = threading.local()


def set_request(options):
    _request.options = options if isinstance(options, dict) else {}


def requested(key, default=None):
    return getattr(_request, "options", {}).get(key, default)


def precision_for(device, current):
    """'st_precision': auto | int8 (half the memory, same output) | float16."""
    want = requested("st_precision", "auto")
    if want == "int8":
        return "int8_float16" if device == "cuda" else "int8"
    if want == "float16" and device == "cuda":
        return "float16"
    return current


def translator_on_cpu():
    """'st_translator_device': auto | cpu. The CPU frees ~0.7 GB of GPU memory."""
    return requested("st_translator_device", "auto") == "cpu"


def report_chunk_error(client, exc):
    """
    Called when transcribing a chunk fails. Upstream only logs it, so with the GPU out of
    memory the client sits on "listening" forever without a single subtitle. Tell it once.
    """
    if "out of memory" not in str(exc).lower() or getattr(client, "_st_oom_reported", False):
        return
    client._st_oom_reported = True
    try:
        client.websocket.send(json.dumps({
            "uid": client.client_uid, "status": "ERROR",
            "message": "Failed to transcribe: GPU out of memory",
        }))
    except Exception:
        pass


def handle_control(websocket, options, default_path):
    """Answer one control request. Returns True if ``options`` was one."""
    if not isinstance(options, dict) or "st_action" not in options:
        return False
    action = options.get("st_action")
    try:
        if action == "list_models":
            reply = list_models(default_path)
        elif action == "download_model":
            reply = download_model(options.get("source"), default_path)
        elif action == "delete_model":
            reply = delete_model(options.get("id"), default_path)
        else:
            reply = {"ok": False, "error": "unknown_action"}
    except Exception as e:
        logging.exception("[stream-transcription] %s failed", action)
        reply = {"ok": False, "error": "server_error", "detail": str(e)[:300]}
    reply["st"] = PROTOCOL_VERSION
    reply["management"] = ALLOW_MANAGEMENT
    try:
        websocket.send(json.dumps(reply))
    except Exception:
        pass
    return True
