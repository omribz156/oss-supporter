import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tools" / "token-meter" / "token_meter.py"
FIXTURE_HOME = pathlib.Path(__file__).resolve().parent / "fixtures" / "codex-home"


spec = importlib.util.spec_from_file_location("token_meter", MODULE_PATH)
token_meter = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = token_meter
spec.loader.exec_module(token_meter)


class TokenMeterTests(unittest.TestCase):
    def test_filters_by_cwd_and_aggregates_last_or_total_delta(self):
        args = token_meter.parse_args([
            "--codex-home",
            str(FIXTURE_HOME),
            "--include-cwd",
            "oss-supporter",
        ])

        report = token_meter.build_report(args)

        self.assertEqual(report["scan"]["sessions_matched"], 1)
        self.assertEqual(report["tokens"]["input"], 160)
        self.assertEqual(report["tokens"]["cached_input"], 40)
        self.assertEqual(report["tokens"]["output"], 15)
        self.assertEqual(report["tokens"]["reasoning_output"], 5)
        self.assertEqual(report["tokens"]["total"], 175)
        self.assertEqual(report["by_model"]["gpt-test"]["total"], 110)
        self.assertEqual(report["by_model"]["gpt-next"]["total"], 65)

    def test_date_filter_excludes_rows(self):
        args = token_meter.parse_args([
            "--codex-home",
            str(FIXTURE_HOME),
            "--include-cwd",
            "oss-supporter",
            "--since",
            "2026-05-21",
        ])

        report = token_meter.build_report(args)

        self.assertEqual(report["scan"]["sessions_matched"], 1)
        self.assertEqual(report["tokens"]["total"], 0)

    def test_date_filter_keeps_cumulative_delta_baseline(self):
        args = token_meter.parse_args([
            "--codex-home",
            str(FIXTURE_HOME),
            "--include-cwd",
            "oss-supporter",
            "--since",
            "2026-05-20",
        ])

        report = token_meter.build_report(args)

        self.assertEqual(report["scan"]["sessions_matched"], 1)
        self.assertEqual(report["tokens"]["input"], 60)
        self.assertEqual(report["tokens"]["cached_input"], 20)
        self.assertEqual(report["tokens"]["output"], 5)
        self.assertEqual(report["tokens"]["reasoning_output"], 1)
        self.assertEqual(report["tokens"]["total"], 65)


if __name__ == "__main__":
    unittest.main()
