#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "cleanup_doctor.py"
SPEC = importlib.util.spec_from_file_location("cleanup_doctor", MODULE_PATH)
assert SPEC and SPEC.loader
cleanup_doctor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cleanup_doctor)


class CleanupDoctorTest(unittest.TestCase):
    def test_directory_size_counts_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            (root / "repo").mkdir()
            (root / "repo" / "a.txt").write_text("hello", encoding="utf-8")
            size, files = cleanup_doctor.directory_size(root / "repo")
        self.assertEqual(size, 5)
        self.assertEqual(files, 1)

    def test_format_bytes(self) -> None:
        self.assertEqual(cleanup_doctor.format_bytes(512), "512 B")
        self.assertEqual(cleanup_doctor.format_bytes(2048), "2.0 KB")


if __name__ == "__main__":
    unittest.main()
