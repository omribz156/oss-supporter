# Repo Capability

Preflight a target repo before promising local verification.

```bash
python tools/repo-capability/repo_capability.py path/to/repo
python tools/repo-capability/repo_capability.py path/to/repo --markdown
```

It reports:

- detected stack signals
- likely verification commands
- missing local tools that may block full tests
- platform notes

Use this after a target survives validation and before writing public
verification language.
