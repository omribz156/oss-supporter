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

- [lead-score](lead-score/README.md): score one GitHub issue before clone/build effort
- [repo-capability](repo-capability/README.md): detect likely verification commands and local blockers
- [source-truth](source-truth/README.md): search generated/template/source hints before patching
- [pr-body-builder](pr-body-builder/README.md): generate safe PR body files
- [token-meter](token-meter/README.md): local aggregate Codex JSONL usage exporter
- [status](status/README.md): GitHub CLI helpers for compact PR/comment follow-up
- [public-boundary](public-boundary/README.md): privacy/safety scanner before publishing
- [cleanup-doctor](cleanup-doctor/README.md): dry-run heavy-folder scanner

Adapter notes live in [docs/adapters.md](../docs/adapters.md).

Planned tools:

- public impact snapshot generator
- status ledger formatter

Before publishing copied workbench material, run:

```bash
python tools/public-boundary/check_public_boundary.py
```
