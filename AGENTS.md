# Agent Notes

These notes are for any assistant, model, script, or human operator working in
this public repo.

## Style

- Keep docs clear, short, and reusable.
- Avoid naming private tools as requirements.
- Prefer "agent", "assistant", and "operator" over vendor-specific names.
- Keep examples sanitized.
- Do not add private repo paths, private issue queues, credentials, or raw logs.

## Public Repo Boundary

This repository is the public method and versioned artifact. It should not become
the live workbench.

Allowed:

- playbooks
- templates
- sanitized case studies
- aggregate impact snapshots
- local helper scripts with privacy-safe defaults

Not allowed:

- raw model transcripts
- private session files
- local clone folders
- credentials or account metadata
- unpublished queue strategy
- personal legal/account details

## Portability

Everything should work conceptually on Linux, macOS, and Windows. If a tool is
implemented for one runtime, document the data contract so another runtime can
reimplement it.

## Public Action

Do not automate public comments, PRs, or issue replies from this repo without a
human/operator review gate.
