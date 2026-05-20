#!/usr/bin/env python3
"""Aggregate Codex JSONL token usage without publishing raw logs."""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


TOOL_VERSION = "0.1.0"


@dataclasses.dataclass
class TokenTotals:
    input: int = 0
    cached_input: int = 0
    output: int = 0
    reasoning_output: int = 0
    total: int = 0

    def add(self, other: "TokenTotals") -> None:
        self.input += other.input
        self.cached_input += other.cached_input
        self.output += other.output
        self.reasoning_output += other.reasoning_output
        self.total += other.total

    def to_dict(self) -> dict[str, int]:
        return {
            "input": self.input,
            "cached_input": self.cached_input,
            "output": self.output,
            "reasoning_output": self.reasoning_output,
            "total": self.total,
        }


@dataclasses.dataclass
class SessionFile:
    path: Path
    session_id: str
    size: int
    modified: float


@dataclasses.dataclass
class ParsedSession:
    matched: bool
    totals: TokenTotals
    by_day: dict[str, TokenTotals]
    by_model: dict[str, TokenTotals]
    warnings: list[str]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = build_report(args)

    if args.json_out:
        write_text(Path(args.json_out), json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.markdown_out:
        write_text(Path(args.markdown_out), render_markdown(result))

    if not args.json_out and not args.markdown_out:
        print(render_console(result))

    if args.fail_on_warnings and result["scan"]["warnings"]:
        return 2
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate Codex JSONL token usage into privacy-safe impact totals."
    )
    parser.add_argument("--codex-home", help="Codex home directory. Defaults to CODEX_HOME or ~/.codex.")
    parser.add_argument(
        "--sessions-root",
        action="append",
        help="Additional session root to scan. Can be passed more than once.",
    )
    parser.add_argument(
        "--include-cwd",
        action="append",
        default=[],
        help="Only include sessions whose session metadata/turn context cwd contains this text.",
    )
    parser.add_argument(
        "--include-cwd-regex",
        action="append",
        default=[],
        help="Only include sessions whose cwd matches this regex. Can be passed more than once.",
    )
    parser.add_argument("--since", help="Include token rows on or after YYYY-MM-DD.")
    parser.add_argument("--until", help="Include token rows on or before YYYY-MM-DD.")
    parser.add_argument("--json-out", help="Write sanitized JSON report.")
    parser.add_argument("--markdown-out", help="Write sanitized Markdown report.")
    parser.add_argument("--fail-on-warnings", action="store_true", help="Exit 2 when parse warnings exist.")
    return parser.parse_args(argv)


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    since = parse_day(args.since, "--since") if args.since else None
    until = parse_day(args.until, "--until") if args.until else None
    if since and until and since > until:
        raise SystemExit("--since must be before or equal to --until")

    include_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in args.include_cwd_regex]
    include_texts = [text.lower() for text in args.include_cwd]

    files = dedupe_session_files(discover_jsonl_files(args))
    totals = TokenTotals()
    by_day: dict[str, TokenTotals] = defaultdict(TokenTotals)
    by_model: dict[str, TokenTotals] = defaultdict(TokenTotals)
    warnings: list[str] = []
    sessions_matched = 0

    for session_file in files:
        parsed = parse_session_file(
            session_file.path,
            since=since,
            until=until,
            include_texts=include_texts,
            include_regexes=include_regexes,
        )
        warnings.extend(parsed.warnings)
        if not parsed.matched:
            continue
        sessions_matched += 1
        totals.add(parsed.totals)
        merge_totals(by_day, parsed.by_day)
        merge_totals(by_model, parsed.by_model)

    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    return {
        "schema": "oss-supporter-token-meter/v1",
        "tool": {"name": "token-meter", "version": TOOL_VERSION},
        "generated_at": generated_at,
        "filters": {
            "since": args.since,
            "until": args.until,
            "include_cwd": args.include_cwd,
            "include_cwd_regex": args.include_cwd_regex,
        },
        "scan": {
            "source": "codex-jsonl",
            "files_considered": len(files),
            "sessions_matched": sessions_matched,
            "warnings": len(warnings),
        },
        "tokens": totals.to_dict(),
        "by_day": {key: by_day[key].to_dict() for key in sorted(by_day)},
        "by_model": {key: by_model[key].to_dict() for key in sorted(by_model)},
        "notes": [
            "Counts are aggregate estimates from local Codex JSONL logs.",
            "Raw prompts, responses, paths, and session IDs are intentionally omitted.",
            "Cached input is reported separately because pricing may differ.",
        ],
    }


def discover_jsonl_files(args: argparse.Namespace) -> list[Path]:
    roots: list[Path] = []
    if args.codex_home:
        codex_home = Path(args.codex_home).expanduser()
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()

    roots.append(codex_home / "sessions")
    roots.append(codex_home / "archived_sessions")
    for root in args.sessions_root or []:
        roots.append(Path(root).expanduser())

    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() == ".jsonl":
            files.append(root)
            continue
        if root.is_dir():
            files.extend(path for path in root.rglob("*.jsonl") if path.is_file())
    return sorted(set(files), key=lambda path: str(path).lower())


def dedupe_session_files(paths: Iterable[Path]) -> list[SessionFile]:
    by_id: dict[str, SessionFile] = {}
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            continue
        session_id = read_session_id(path) or session_id_from_filename(path) or str(path.resolve())
        candidate = SessionFile(path=path, session_id=session_id, size=stat.st_size, modified=stat.st_mtime)
        existing = by_id.get(session_id)
        if existing is None or (candidate.size, candidate.modified) > (existing.size, existing.modified):
            by_id[session_id] = candidate
    return sorted(by_id.values(), key=lambda item: str(item.path).lower())


def read_session_id(path: Path) -> str | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if index > 25:
                    return None
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") != "session_meta":
                    continue
                payload = obj.get("payload")
                if isinstance(payload, dict):
                    value = payload.get("id")
                    if isinstance(value, str) and value:
                        return value
    except OSError:
        return None
    return None


def session_id_from_filename(path: Path) -> str | None:
    match = re.search(r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", path.name)
    return match.group(1) if match else None


def parse_session_file(
    path: Path,
    *,
    since: dt.date | None,
    until: dt.date | None,
    include_texts: list[str],
    include_regexes: list[re.Pattern[str]],
) -> ParsedSession:
    totals = TokenTotals()
    by_day: dict[str, TokenTotals] = defaultdict(TokenTotals)
    by_model: dict[str, TokenTotals] = defaultdict(TokenTotals)
    warnings: list[str] = []
    cwd_values: list[str] = []
    current_model = "unknown"
    previous_total: TokenTotals | None = None

    try:
        handle = path.open("r", encoding="utf-8")
    except OSError as exc:
        return ParsedSession(False, totals, by_day, by_model, [f"unreadable file skipped: {exc.__class__.__name__}"])

    with handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                warnings.append(f"invalid json line skipped at line {line_number}")
                continue

            obj_type = obj.get("type")
            payload = obj.get("payload")
            if not isinstance(payload, dict):
                continue

            if obj_type == "session_meta":
                remember_cwd(payload, cwd_values)
                current_model = model_from_payload(payload) or current_model
                continue

            if obj_type == "turn_context":
                remember_cwd(payload, cwd_values)
                current_model = model_from_payload(payload) or current_model
                continue

            if obj_type != "event_msg" or payload.get("type") != "token_count":
                continue

            info = payload.get("info")
            if not isinstance(info, dict):
                continue

            day = day_from_timestamp(obj.get("timestamp"))
            if day is None:
                warnings.append(f"token row without parseable timestamp at line {line_number}")
                continue
            total_usage = totals_from_mapping(info.get("total_token_usage"))
            usage = usage_from_info(info, previous_total)
            if total_usage.total > 0:
                previous_total = total_usage
            if since and day < since:
                continue
            if until and day > until:
                continue
            if usage.total <= 0:
                continue

            totals.add(usage)
            by_day[day.isoformat()].add(usage)
            by_model[current_model].add(usage)

    matched = cwd_matches(cwd_values, include_texts, include_regexes)
    if not matched:
        return ParsedSession(False, TokenTotals(), {}, {}, warnings)
    return ParsedSession(True, totals, by_day, by_model, warnings)


def remember_cwd(payload: dict[str, Any], cwd_values: list[str]) -> None:
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd:
        cwd_values.append(cwd)


def model_from_payload(payload: dict[str, Any]) -> str | None:
    model = payload.get("model")
    if isinstance(model, str) and model:
        return model
    collaboration = payload.get("collaboration_mode")
    if isinstance(collaboration, dict):
        settings = collaboration.get("settings")
        if isinstance(settings, dict):
            model = settings.get("model")
            if isinstance(model, str) and model:
                return model
    return None


def cwd_matches(cwd_values: list[str], include_texts: list[str], include_regexes: list[re.Pattern[str]]) -> bool:
    if not include_texts and not include_regexes:
        return True
    haystack = "\n".join(cwd_values)
    haystack_lower = haystack.lower()
    return any(text in haystack_lower for text in include_texts) or any(
        pattern.search(haystack) for pattern in include_regexes
    )


def usage_from_info(info: dict[str, Any], previous_total: TokenTotals | None) -> TokenTotals:
    last = totals_from_mapping(info.get("last_token_usage"))
    if last.total > 0:
        return last

    current_total = totals_from_mapping(info.get("total_token_usage"))
    if current_total.total <= 0:
        return TokenTotals()
    if previous_total is None:
        return current_total
    return TokenTotals(
        input=max(0, current_total.input - previous_total.input),
        cached_input=max(0, current_total.cached_input - previous_total.cached_input),
        output=max(0, current_total.output - previous_total.output),
        reasoning_output=max(0, current_total.reasoning_output - previous_total.reasoning_output),
        total=max(0, current_total.total - previous_total.total),
    )


def totals_from_mapping(value: Any) -> TokenTotals:
    if not isinstance(value, dict):
        return TokenTotals()
    return TokenTotals(
        input=to_int(value.get("input_tokens")),
        cached_input=to_int(value.get("cached_input_tokens", value.get("cache_read_input_tokens"))),
        output=to_int(value.get("output_tokens")),
        reasoning_output=to_int(value.get("reasoning_output_tokens")),
        total=to_int(value.get("total_tokens")),
    )


def to_int(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def day_from_timestamp(value: Any) -> dt.date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    return parse_day(value[:10], "timestamp")


def parse_day(value: str, label: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"{label} must be YYYY-MM-DD") from exc


def merge_totals(target: dict[str, TokenTotals], source: dict[str, TokenTotals]) -> None:
    for key, totals in source.items():
        target[key].add(totals)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_console(report: dict[str, Any]) -> str:
    tokens = report["tokens"]
    return "\n".join(
        [
            "OSS Supporter token meter",
            f"Generated: {report['generated_at']}",
            f"Sessions matched: {report['scan']['sessions_matched']}",
            f"Files considered: {report['scan']['files_considered']}",
            f"Input: {tokens['input']:,}",
            f"Cached input: {tokens['cached_input']:,}",
            f"Output: {tokens['output']:,}",
            f"Reasoning output: {tokens['reasoning_output']:,}",
            f"Total: {tokens['total']:,}",
            f"Warnings: {report['scan']['warnings']}",
        ]
    )


def render_markdown(report: dict[str, Any]) -> str:
    tokens = report["tokens"]
    lines = [
        "# Token Impact Snapshot",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Source: `{report['scan']['source']}`",
        f"- Sessions matched: `{report['scan']['sessions_matched']}`",
        f"- Files considered: `{report['scan']['files_considered']}`",
        f"- Warnings: `{report['scan']['warnings']}`",
        "",
        "## Totals",
        "",
        "| Metric | Tokens |",
        "| --- | ---: |",
        f"| Input | {tokens['input']:,} |",
        f"| Cached input | {tokens['cached_input']:,} |",
        f"| Output | {tokens['output']:,} |",
        f"| Reasoning output | {tokens['reasoning_output']:,} |",
        f"| Total | {tokens['total']:,} |",
        "",
        "## By Day",
        "",
        "| Day | Total | Input | Cached input | Output |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for day, day_tokens in report["by_day"].items():
        lines.append(
            f"| {day} | {day_tokens['total']:,} | {day_tokens['input']:,} | "
            f"{day_tokens['cached_input']:,} | {day_tokens['output']:,} |"
        )
    lines.extend(
        [
            "",
            "## By Model",
            "",
            "| Model | Total | Input | Cached input | Output |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for model, model_tokens in report["by_model"].items():
        lines.append(
            f"| {model} | {model_tokens['total']:,} | {model_tokens['input']:,} | "
            f"{model_tokens['cached_input']:,} | {model_tokens['output']:,} |"
        )
    lines.extend(
        [
            "",
            "## Privacy",
            "",
            "This snapshot is aggregate-only. It omits prompts, responses, raw paths,",
            "session IDs, and transcript content.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
