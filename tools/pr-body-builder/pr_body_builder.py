#!/usr/bin/env python3
"""Build a newline-safe OSS Supporter PR body."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DISCLOSURE = "Implemented with agent assistance and manually reviewed before submission."


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = args.summary or []
    verification = args.verify or []

    if args.slice_readme:
        text = Path(args.slice_readme).read_text(encoding="utf-8")
        summary = summary or section_lines(text, "Changes")
        verification = verification or section_lines(text, "Verification")

    body = render_body(summary or ["<summary item>"], verification or ["<verification command or note>"], args.fixes)

    if args.out:
        Path(args.out).write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build safe PR body text.")
    parser.add_argument("--slice-readme", help="Read Summary/Verification from a slice README.")
    parser.add_argument("--summary", action="append", default=[], help="Summary bullet. Repeatable.")
    parser.add_argument("--verify", action="append", default=[], help="Verification bullet. Repeatable.")
    parser.add_argument("--fixes", help="Issue reference, for example #123.")
    parser.add_argument("--out", help="Write body to a file.")
    return parser.parse_args(argv)


def section_lines(text: str, name: str) -> list[str]:
    match = re.search(rf"(?ms)^##\s+{re.escape(name)}\s*\n(?P<body>.*?)(?=^##\s+|\Z)", text)
    if not match:
        return []
    return [clean_bullet(line) for line in match.group("body").splitlines() if line.strip()]


def clean_bullet(value: str) -> str:
    return re.sub(r"^\s*[-*]\s*", "", value.strip())


def render_body(summary: list[str], verification: list[str], fixes: str | None = None) -> str:
    lines = ["Summary:"]
    lines.extend(f"- {clean_bullet(item)}" for item in summary)
    lines.append("")
    lines.append("Verification:")
    lines.extend(f"- {clean_bullet(item)}" for item in verification)
    if fixes:
        lines.append("")
        lines.append(f"Fixes {fixes}.")
    lines.append("")
    lines.append(DISCLOSURE)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
