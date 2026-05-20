# Tools

Tools in this repo should be optional and portable.

Rules:

- no agent/vendor lock-in
- no raw log publishing
- privacy-safe defaults
- dry-run or preview output before writing public files
- document input and output formats
- support Linux, macOS, and Windows where practical

Included tools:

- [token-meter](token-meter/README.md): local aggregate Codex JSONL usage exporter
- [status](status/README.md): GitHub CLI helpers for compact PR/comment follow-up

Adapter notes live in [docs/adapters.md](../docs/adapters.md).

Planned tools:

- public impact snapshot generator
- public repo export checker
- status ledger formatter
