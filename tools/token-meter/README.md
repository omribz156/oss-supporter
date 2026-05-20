# Token Meter

Privacy-first local usage scanner for Codex JSONL logs.

It reads local session logs, aggregates token counts, and writes sanitized JSON
or Markdown impact snapshots. It does not publish prompts, responses, raw paths,
session IDs, or transcript content.

## Supported Source

Codex JSONL logs:

- `$CODEX_HOME/sessions/**/*.jsonl`
- `$CODEX_HOME/archived_sessions/*.jsonl`
- `~/.codex/sessions/**/*.jsonl`
- `~/.codex/archived_sessions/*.jsonl`

The parser uses `event_msg` rows where `payload.type == "token_count"` and
counts `payload.info.last_token_usage`. If `last_token_usage` is missing, it
falls back to a safe delta from `total_token_usage`.

## Usage

```bash
python tools/token-meter/token_meter.py --include-cwd oss-supporter
```

Write files:

```bash
python tools/token-meter/token_meter.py \
  --include-cwd oss-supporter \
  --json-out impact/oss-supporter-impact.local.json \
  --markdown-out impact/oss-supporter-impact.local.md
```

Limit by date:

```bash
python tools/token-meter/token_meter.py --since 2026-05-01 --until 2026-05-31
```

Use a custom Codex home:

```bash
python tools/token-meter/token_meter.py --codex-home /path/to/.codex
```

## Output

The JSON output contains:

- scan metadata
- applied filters
- total input, cached input, output, reasoning output, and total tokens
- totals by day
- totals by model
- warning count

It intentionally does not include:

- prompts
- responses
- raw local paths
- raw session IDs
- raw JSONL rows

## Notes

Token counts are usage estimates from local logs, not invoices. Cached input is
reported separately because providers often price it differently.
