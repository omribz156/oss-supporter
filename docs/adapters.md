# Adapters

OSS Supporter is agent-agnostic. The playbook should work with any assistant,
editor, CLI, or manual workflow that follows the validation and publication
gates.

Tools can still be source-specific. Each adapter should make that boundary
clear.

## Included

| Adapter | Source | Output | Notes |
| --- | --- | --- | --- |
| `tools/token-meter` | Codex JSONL logs | sanitized JSON / Markdown aggregate token reports | local-only by default; `.local.*` outputs are ignored |

## Adapter Rules

- Keep raw logs local.
- Publish aggregate values only after review.
- Do not include prompts, responses, raw paths, account IDs, or session IDs.
- Document source format and assumptions.
- Prefer standard-library implementations where possible.
- Keep outputs portable across Linux, macOS, and Windows.

## Future Adapters

Useful next adapters:

- Claude usage export parser
- OpenAI API usage export parser
- local ledger summarizer for PR/comment counts
- public impact badge generator
