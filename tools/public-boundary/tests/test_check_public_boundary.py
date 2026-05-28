from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_public_boundary import scan


class PublicBoundaryTests(unittest.TestCase):
    def test_clean_public_markdown_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Public aggregate docs only.\n", encoding="utf-8")

            self.assertEqual(scan(root), [])

    def test_private_path_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "C:" + r"\projects\oss-supporter\work"
            (root / "README.md").write_text(f"Do not publish {private_path}", encoding="utf-8")

            findings = scan(root)

            self.assertEqual(findings[0].rule, "private-windows-path")


if __name__ == "__main__":
    unittest.main()
