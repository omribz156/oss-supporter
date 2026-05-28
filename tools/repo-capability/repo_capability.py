#!/usr/bin/env python3
"""Detect a repository's likely verification commands and local blockers."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Any


TOOL_VERSION = "0.1.0"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(Path(args.repo).resolve())

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif args.markdown:
        print_markdown(report)
    else:
        print_text(report)
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect repo stack and likely verification commands.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--markdown", action="store_true", help="Emit Markdown.")
    return parser.parse_args(argv)


def build_report(root: Path) -> dict[str, Any]:
    signals: set[str] = set()
    commands: list[str] = []
    blockers: list[str] = []
    notes: list[str] = []

    def exists(name: str) -> bool:
        return (root / name).exists()

    if exists("package.json"):
        signals.add("javascript")
        package = read_json(root / "package.json")
        runner = "pnpm" if exists("pnpm-lock.yaml") else "yarn" if exists("yarn.lock") else "npm"
        scripts = (package or {}).get("scripts", {})
        if isinstance(scripts, dict):
            for name in ("test", "build", "lint", "typecheck", "format", "check"):
                if name in scripts:
                    commands.append(f"{runner} run {name}")
    if exists("pnpm-lock.yaml"):
        signals.add("pnpm")
    if exists("package-lock.json"):
        signals.add("npm")
    if exists("yarn.lock"):
        signals.add("yarn")
    if exists("go.mod"):
        signals.add("go")
        commands.append("go test ./...")
    if exists("Cargo.toml"):
        signals.add("rust")
        commands.extend(["cargo test", "cargo fmt --check"])
    if exists("pyproject.toml") or exists("requirements.txt"):
        signals.add("python")
        commands.append("uv run pytest" if has_tool("uv") else "python -m pytest")
    if exists("composer.json"):
        signals.add("php")
        commands.append("composer test")
    if exists("Makefile") or exists("GNUmakefile"):
        signals.add("make")
        commands.append("make test")
    if (root / ".github" / "workflows").exists():
        signals.add("github-actions")

    missing_tool_rules = {
        "docker": "Docker unavailable; integration/testcontainers/live-env tests may be blocked.",
        "php": "PHP unavailable for PHP checks.",
        "composer": "Composer unavailable for PHP dependency/test checks.",
        "helm": "Helm unavailable for chart lint/template checks.",
        "terraform": "Terraform unavailable for fmt/validate/provider-doc checks.",
        "make": "make unavailable from this shell.",
    }

    if "php" not in signals:
        missing_tool_rules.pop("php")
        missing_tool_rules.pop("composer")
    if not any(root.rglob("Chart.yaml")):
        missing_tool_rules.pop("helm")
    if not any(root.rglob("*.tf")):
        missing_tool_rules.pop("terraform")
    if "make" not in signals:
        missing_tool_rules.pop("make")

    for tool, message in missing_tool_rules.items():
        if not has_tool(tool):
            blockers.append(message)

    if platform.system().lower().startswith("win"):
        notes.append("Windows host: Linux-only tests may fail on syscall, netlink, path, or shell assumptions.")

    return {
        "schema": "oss-supporter-repo-capability/v1",
        "tool": {"name": "repo-capability", "version": TOOL_VERSION},
        "repo": str(root),
        "signals": sorted(signals),
        "suggested_commands": sorted(set(commands)),
        "blockers": sorted(set(blockers)),
        "notes": notes,
    }


def has_tool(name: str) -> bool:
    return shutil.which(name) is not None


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def print_text(report: dict[str, Any]) -> None:
    print(f"Repo: {report['repo']}")
    print(f"Signals: {', '.join(report['signals']) or '-'}")
    print("Suggested commands:")
    for command in report["suggested_commands"] or ["-"]:
        print(f"- {command}")
    print("Blockers:")
    for blocker in report["blockers"] or ["-"]:
        print(f"- {blocker}")
    if report["notes"]:
        print("Notes:")
        for note in report["notes"]:
            print(f"- {note}")


def print_markdown(report: dict[str, Any]) -> None:
    print("## Repo Capability")
    print()
    print(f"- Repo: `{report['repo']}`")
    print(f"- Signals: {', '.join(f'`{item}`' for item in report['signals']) or '-'}")
    print()
    print("### Suggested Commands")
    for command in report["suggested_commands"] or ["-"]:
        print(f"- `{command}`" if command != "-" else "-")
    print()
    print("### Blockers")
    for blocker in report["blockers"] or ["-"]:
        print(f"- {blocker}")
    if report["notes"]:
        print()
        print("### Notes")
        for note in report["notes"]:
            print(f"- {note}")


if __name__ == "__main__":
    sys.exit(main())
