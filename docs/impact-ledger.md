# Impact Ledger

Impact should be public, aggregate, and honest.

## Track

- issues triaged
- PRs opened
- PRs merged
- review fixes made
- projects helped
- maintainers unblocked
- estimated tokens used for OSS support
- estimated cost, when calculable

## Do Not Track Publicly

- raw prompts
- raw logs
- private session IDs
- account IDs
- hidden queues
- private maintainer contact

## Suggested Snapshot

```json
{
  "period": "2026-05",
  "scope": "oss-supporter",
  "tokens": {
    "input": 0,
    "cached_input": 0,
    "output": 0,
    "estimated_cost_usd": null
  },
  "public_help": {
    "comments": 0,
    "prs_opened": 0,
    "prs_merged": 0,
    "review_fixes": 0,
    "projects_helped": 0
  }
}
```

## Local Token Meter

The first included helper is [tools/token-meter](../tools/token-meter/README.md).
It scans local Codex JSONL logs and emits aggregate-only token totals.

Example:

```bash
python tools/token-meter/token_meter.py \
  --include-cwd oss-supporter \
  --json-out impact/oss-supporter-impact.local.json \
  --markdown-out impact/oss-supporter-impact.local.md
```

Review generated files before publishing. Files ending in `.local.*` are ignored
by default.

## Public Display

The public display should be a receipt, not a transcript.

Recommended shape:

1. Generate `impact/YYYY-MM.local.md` and `impact/YYYY-MM.local.json`.
2. Review locally.
3. Copy safe totals into [templates/impact-snapshot.md](../templates/impact-snapshot.md).
4. Save as `impact/YYYY-MM.md`.
5. Add the new row to [impact/README.md](../impact/README.md).

Good public metrics:

- tokens used
- projects helped
- issues triaged
- reproductions posted
- PRs opened
- PRs merged
- review fixes shipped

Keep the story concrete, but sanitized. A useful line is:

```text
This month, spare agent capacity helped triage X issues and merge Y focused PRs
across Z projects.
```
