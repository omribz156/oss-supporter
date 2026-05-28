from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import repo_capability


class RepoCapabilityTests(unittest.TestCase):
    def test_detects_package_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest","build":"tsc"}}', encoding="utf-8")

            report = repo_capability.build_report(root)

            self.assertIn("javascript", report["signals"])
            self.assertIn("npm run test", report["suggested_commands"])
            self.assertIn("npm run build", report["suggested_commands"])


if __name__ == "__main__":
    unittest.main()
