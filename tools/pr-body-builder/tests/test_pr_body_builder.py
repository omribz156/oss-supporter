from __future__ import annotations

import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pr_body_builder


class PrBodyBuilderTests(unittest.TestCase):
    def test_renders_body(self) -> None:
        body = pr_body_builder.render_body(["change"], ["test"], "#1")

        self.assertIn("Summary:\n- change", body)
        self.assertIn("Verification:\n- test", body)
        self.assertIn("Fixes #1.", body)


if __name__ == "__main__":
    unittest.main()
