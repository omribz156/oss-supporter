#!/usr/bin/env python3
"""Run the public repo's lightweight checks."""

from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "tools/token-meter/tests/test_token_meter.py"],
    [sys.executable, "tools/public-boundary/tests/test_check_public_boundary.py"],
    [sys.executable, "tools/lead-score/tests/test_lead_score.py"],
    [sys.executable, "tools/repo-capability/tests/test_repo_capability.py"],
    [sys.executable, "tools/pr-body-builder/tests/test_pr_body_builder.py"],
    [sys.executable, "tools/cleanup-doctor/tests/test_cleanup_doctor.py"],
    [sys.executable, "tools/public-boundary/check_public_boundary.py"],
]


def main() -> int:
    for command in COMMANDS:
        print("+ " + " ".join(command))
        result = subprocess.run(command)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
