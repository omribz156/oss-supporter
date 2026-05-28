#!/usr/bin/env python3
"""Search for generated-file and source-template hints before patching."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


KEYWORDS = re.compile(r"generate|generated|template|templates|codegen|schema|docs-gen|tfplugindocs|openapi", re.I)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".py", ".ps1", ".go", ".js", ".ts", ".tsx"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "target", "dist", "build"}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.repo).resolve()

    print(f"Source-truth hints for {root}")
    for touched in args.touched:
        print_touched_hint(touched)

    print("\nRepo hints:")
    for path, line, text in find_hints(root, limit=args.limit):
        print(f"- {path.relative_to(root)}:{line}: {text}")
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find source/template/generator hints.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository path.")
    parser.add_argument("--touched", action="append", default=[], help="Path you expect to touch.")
    parser.add_argument("--limit", type=int, default=40, help="Maximum repo hints.")
    return parser.parse_args(argv)


def print_touched_hint(path: str) -> None:
    print(f"\nTouched: {path}")
    if re.search(r"docs|README|generated|dist|api|schema", path, re.I):
        print("- Risk: visible/generated surface; search templates or generators before patch.")
    if re.search(r"\.(md|rst|adoc)$", path, re.I):
        print("- Check: docs source, snippets, and build/generation commands.")
    if re.search(r"\.(json|ya?ml)$", path, re.I):
        print("- Check: schema/source generator and formatting command.")


def find_hints(root: Path, limit: int) -> list[tuple[Path, int, str]]:
    results: list[tuple[Path, int, str]] = []
    for path in root.rglob("*"):
        if len(results) >= limit:
            break
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            if KEYWORDS.search(line):
                results.append((path, index, line.strip()[:180]))
                if len(results) >= limit:
                    break
    return results


if __name__ == "__main__":
    sys.exit(main())
