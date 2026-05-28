#!/usr/bin/env python3
"""Check a public OSS Supporter repo for common private-workbench leaks."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "private",
    "scratch",
    "tmp",
    "work",
}

SKIP_PARTS = {
    ("impact", "raw"),
    ("tools", "token-meter", "tests", "fixtures"),
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".ps1",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".svg",
}

CONTENT_RULES = [
    ("private-windows-path", re.compile(r"[A-Za-z]:\\(?:Users|projects)\\", re.IGNORECASE)),
    ("raw-codex-directive", re.compile(r"^::git-", re.MULTILINE)),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("openai-token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("generic-secret-assignment", re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*=\s*['\"][^'\"\s]{12,}['\"]")),
]


@dataclass
class Finding:
    path: Path
    rule: str
    line: int | None
    detail: str


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    findings = scan(root)

    if findings:
        for finding in findings:
            where = str(finding.path.relative_to(root))
            if finding.line:
                where = f"{where}:{finding.line}"
            print(f"{where} | {finding.rule} | {finding.detail}")
        print(f"\n{len(findings)} public-boundary finding(s).")
        return 1

    print("public-boundary: clean")
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan for private data before publishing.")
    parser.add_argument("--root", default=".", help="Repository root to scan.")
    return parser.parse_args(argv)


def scan(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_publishable_files(root):
        rel = path.relative_to(root)

        if ".local." in path.name:
            findings.append(Finding(path, "local-artifact", None, "local review artifact should stay untracked"))
        if path.suffix.lower() in {".jsonl", ".log"}:
            findings.append(Finding(path, "raw-log-file", None, "raw logs/transcripts should stay out of the public repo"))

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding(path, "binary-or-non-utf8", None, "unexpected non-UTF-8 public text file"))
            continue

        for rule, pattern in CONTENT_RULES:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                detail = match.group(0).splitlines()[0][:120]
                findings.append(Finding(path, rule, line, detail))

    return findings


def iter_publishable_files(root: Path):
    git_files = list_git_publishable_files(root)
    if git_files is not None:
        for path in git_files:
            if should_scan_path(root, path):
                yield path
        return

    for path in root.rglob("*"):
        if path.is_file() and should_scan_path(root, path):
            yield path


def list_git_publishable_files(root: Path) -> list[Path] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    return [root / line for line in result.stdout.splitlines() if line]


def should_scan_path(root: Path, path: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return False

    if any(part in SKIP_DIRS for part in rel_parts):
        return False
    if any(rel_parts[: len(skip)] == skip for skip in SKIP_PARTS):
        return False
    return path.is_file()


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_scan_path(root, path):
            yield path


if __name__ == "__main__":
    sys.exit(main())
