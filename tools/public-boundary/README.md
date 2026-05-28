# Public Boundary Checker

Small dependency-free scanner for the public repo boundary.

It catches common mistakes before publishing:

- tracked `.local.*` impact exports
- raw `.jsonl` / `.log` files
- private local paths
- Codex session paths
- raw Codex app directives
- obvious token/secret literals

Run from the repo root:

```bash
python tools/public-boundary/check_public_boundary.py
```

Use it before committing public impact updates or copying files from a private
workbench.

The checker is intentionally conservative and easy to port. If it flags a false
positive, prefer rewriting the public text to be less private rather than adding
large allowlists.
