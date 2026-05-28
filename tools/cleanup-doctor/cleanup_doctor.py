#!/usr/bin/env python3
"""Dry-run scanner for heavy reinstallable folders."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path


TARGET_NAMES = {"node_modules", ".venv", "venv", "target", ".next", ".turbo", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".gradle", "repo"}
SKIP_DIRS = {".git"}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    cutoff = dt.datetime.now() - dt.timedelta(days=args.older_than_days)
    rows = []

    for path in root.rglob("*"):
        if not path.is_dir() or path.name not in TARGET_NAMES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        modified = dt.datetime.fromtimestamp(path.stat().st_mtime)
        if modified > cutoff:
            continue
        size, files = directory_size(path)
        rows.append((size, files, path, modified))

    rows.sort(reverse=True, key=lambda row: row[0])
    if args.markdown:
        print("| Size | Files | Age days | Path |")
        print("| ---: | ---: | ---: | --- |")
    else:
        print("size | files | age_days | path")
    for size, files, path, modified in rows[: args.top]:
        age = (dt.datetime.now() - modified).days
        print(f"| {format_bytes(size)} | {files} | {age} | `{path}` |" if args.markdown else f"{format_bytes(size)} | {files} | {age} | {path}")
    print("\nDry-run only. Delete manually or with your private cleanup tooling after checking receipts.")
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find old heavy local folders.")
    parser.add_argument("--root", default=".", help="Root to scan.")
    parser.add_argument("--older-than-days", type=int, default=7)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--markdown", action="store_true")
    return parser.parse_args(argv)


def directory_size(path: Path) -> tuple[int, int]:
    total = 0
    files = 0
    for current_root, dirs, filenames in os.walk(path):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for filename in filenames:
            try:
                total += (Path(current_root) / filename).stat().st_size
                files += 1
            except OSError:
                continue
    return total, files


def format_bytes(value: int) -> str:
    if value >= 1024**3:
        return f"{value / 1024**3:.2f} GB"
    if value >= 1024**2:
        return f"{value / 1024**2:.1f} MB"
    if value >= 1024:
        return f"{value / 1024:.1f} KB"
    return f"{value} B"


if __name__ == "__main__":
    sys.exit(main())
