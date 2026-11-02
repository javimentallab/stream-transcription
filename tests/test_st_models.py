"""Model management on the server: what it accepts to download, and archives that try to escape."""
import importlib.util
import io
import os
import tarfile
import tempfile
import unittest
import zipfile

RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "server", "whisper_live", "st_models.py")
_spec = importlib.util.spec_from_file_location("st_models", RUTA)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)


class Source(unittest.TestCase):
    def test_repo(self):
        self.assertEqual(M._parse_source("Systran/faster-whisper-small"), ("hf", "Systran/faster-whisper-small", None))

    def test_spaces(self):
        self.assertEqual(M._parse_source("  Systran/faster-whisper-small "), ("hf", "Systran/faster-whisper-small", None))

    def test_hugging_face_url(self):
        kind, repo, _rev = M._parse_source("https://huggingface.co/Systran/faster-whisper-small")
        self.assertEqual((kind, repo), ("hf", "Systran/faster-whisper-small"))

    def test_hugging_face_url_with_revision(self):
        kind, repo, rev = M._parse_source("https://huggingface.co/Systran/faster-whisper-small/tree/abc123")
        self.assertEqual((kind, repo, rev), ("hf", "Systran/faster-whisper-small", "abc123"))

    def test_archive(self):
        self.assertEqual(M._parse_source("https://x.example/models/my%20model.tar.gz"), ("url", "https://x.example/models/my%20model.tar.gz", "my-20model"))

    def test_url_that_is_not_an_archive(self):
        with self.assertRaisesRegex(ValueError, "unsupported_url"):
            M._parse_source("https://x.example/model.exe")

    def test_nonsense(self):
        for bad in (5, None, "", "not valid!", "../../etc/passwd", "file:///etc/passwd"):
            with self.assertRaisesRegex(ValueError, "invalid_source", msg=repr(bad)):
                M._parse_source(bad)

    def test_slug_cannot_climb(self):
        _k, _u, slug = M._parse_source("https://x.example/..%2F..%2Fevil.zip")
        self.assertNotIn("/", slug)
        self.assertNotIn("\\", slug)
        self.assertFalse(slug.startswith("."))


class CacheDir(unittest.TestCase):
    def test_names(self):
        self.assertEqual(M._repo_id_from_cache_dir("models--Systran--faster-whisper-small"), "Systran/faster-whisper-small")
        self.assertEqual(M._repo_id_from_cache_dir("models--a--b--c"), "a/b--c")
        self.assertEqual(M._repo_id_from_cache_dir("models--solo"), "solo")
        self.assertEqual(M._repo_id_from_cache_dir("plain"), "plain")


class SafeExtract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dest = os.path.join(self.tmp.name, "dest")
        os.makedirs(self.dest)

    def tearDown(self):
        self.tmp.cleanup()

    def zip_con(self, *nombres):
        p = os.path.join(self.tmp.name, "a.zip")
        with zipfile.ZipFile(p, "w") as z:
            for n in nombres:
                z.writestr(n, "x")
        return p

    def tar_con(self, nombre, tipo=tarfile.REGTYPE, enlace=""):
        p = os.path.join(self.tmp.name, "a.tar")
        with tarfile.open(p, "w") as t:
            i = tarfile.TarInfo(nombre)
            i.type = tipo
            i.linkname = enlace
            i.size = 1 if tipo == tarfile.REGTYPE else 0
            t.addfile(i, io.BytesIO(b"x") if tipo == tarfile.REGTYPE else None)
        return p

    def fuera(self):
        return sorted(set(os.listdir(self.tmp.name)) - {"dest", "a.zip", "a.tar"})

    def test_normal_zip(self):
        M._safe_extract(self.zip_con("m/model.bin"), self.dest)
        self.assertTrue(os.path.exists(os.path.join(self.dest, "m", "model.bin")))

    def test_normal_tar(self):
        M._safe_extract(self.tar_con("m.bin"), self.dest)
        self.assertTrue(os.path.exists(os.path.join(self.dest, "m.bin")))

    def test_zip_that_climbs(self):
        with self.assertRaisesRegex(ValueError, "bad_archive"):
            M._safe_extract(self.zip_con("ok.bin", "../evil.txt"), self.dest)
        self.assertEqual(self.fuera(), [])
        self.assertEqual(os.listdir(self.dest), [], "nothing is extracted when one entry is bad")

    def test_tar_that_climbs(self):
        with self.assertRaisesRegex(ValueError, "bad_archive"):
            M._safe_extract(self.tar_con("../evil.txt"), self.dest)
        self.assertEqual(self.fuera(), [])

    def test_folder_with_a_similar_name(self):
        with self.assertRaisesRegex(ValueError, "bad_archive"):
            M._safe_extract(self.zip_con("../dest-evil/x.txt"), self.dest)

    def test_tar_with_links(self):
        for tipo in (tarfile.SYMTYPE, tarfile.LNKTYPE):
            with self.assertRaisesRegex(ValueError, "bad_archive"):
                M._safe_extract(self.tar_con("l", tipo, "/etc/passwd"), self.dest)


class Requested(unittest.TestCase):
    def tearDown(self):
        M.set_request({})

    def test_precision(self):
        M.set_request({"st_precision": "int8"})
        self.assertEqual(M.precision_for("cuda", "float16"), "int8_float16")
        self.assertEqual(M.precision_for("cpu", "float32"), "int8")
        M.set_request({"st_precision": "float16"})
        self.assertEqual(M.precision_for("cuda", "int8"), "float16")
        self.assertEqual(M.precision_for("cpu", "int8"), "int8")
        M.set_request({})
        self.assertEqual(M.precision_for("cuda", "float16"), "float16")

    def test_translator_device(self):
        self.assertFalse(M.translator_on_cpu())
        M.set_request({"st_translator_device": "cpu"})
        self.assertTrue(M.translator_on_cpu())

    def test_options_that_are_not_a_dict(self):
        M.set_request("nonsense")
        self.assertEqual(M.requested("x", "d"), "d")


if __name__ == "__main__":
    unittest.main()
