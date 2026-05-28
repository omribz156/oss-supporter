#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "lead_score.py"
SPEC = importlib.util.spec_from_file_location("lead_score", MODULE_PATH)
assert SPEC and SPEC.loader
lead_score = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lead_score)


class LeadScoreTest(unittest.TestCase):
    def test_invalid_target_is_error_without_network(self) -> None:
        result = lead_score.score_target("not-a-target")
        self.assertEqual(result["decision"], "error")
        self.assertIn("owner/repo#123", result["risks"][0])

    def test_markdown_output(self) -> None:
        result = {"target": "x/y#1", "decision": "watch", "score": 2, "reasons": ["clear"], "risks": []}
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            lead_score.print_markdown(result)
        self.assertIn("## Lead Score: `x/y#1`", buffer.getvalue())
        self.assertIn("- Decision: `watch`", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
