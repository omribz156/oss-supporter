![OSS Supporter banner](assets/oss-supporter-banner.svg)

# OSS Supporter

**Use spare tokens for good.**

[![License: MIT](https://img.shields.io/badge/license-MIT-0f766e.svg)](LICENSE)
[![Agent agnostic](https://img.shields.io/badge/agent-agnostic-2563eb.svg)](#what-this-is)
[![OS agnostic](https://img.shields.io/badge/os-linux%20%7C%20macOS%20%7C%20windows-7c3aed.svg)](#what-this-is)
[![Maintainer first](https://img.shields.io/badge/default-maintainer%20first-f59e0b.svg)](docs/validation-gates.md)

Turn unused agent/model capacity into careful open source maintenance.
OSS Supporter is an operating playbook for finding small, useful OSS work,
validating it, doing it well, and leaving maintainers with less burden than
before.

It is model-agnostic, agent-agnostic, and OS-agnostic: use any assistant, CLI,
editor, or manual workflow that can follow the gates.

## Current Impact

Latest public receipt: [May 2026](impact/2026-05.md), updated through
2026-05-24.

| Tokens used | Projects touched | PR/status records tracked | PRs merged | Source-backed comments |
| ---: | ---: | ---: | ---: | ---: |
| 1,030,308,708 | 70 | 116 | 29 | 18 |

Recent accepted work includes focused fixes in
[OpenTelemetry JS](https://github.com/open-telemetry/opentelemetry-js/pull/6722),
[containerd/nerdctl](https://github.com/containerd/nerdctl/pull/4909),
[Microsoft Physical AI Toolchain](https://github.com/microsoft/physical-ai-toolchain/pulls?q=is%3Apr+author%3Aomribz156),
[Elastic CLI](https://github.com/elastic/cli/pulls?q=is%3Apr+author%3Aomribz156),
[Loxia OnBuzz](https://github.com/Loxia-ai/onbuzz-community/pulls?q=is%3Apr+author%3Aomribz156),
[Open QA](https://github.com/MyNameIsEdi/open-qa/pulls?q=is%3Apr+author%3Aomribz156),
and [shadcn-vue](https://github.com/unovue/shadcn-vue/pull/1827).

## Start In One Paste

Give this repo link to your agent, then paste:

```text
You are helping me use OSS Supporter.

Read this repo as the public playbook. Keep private workbench files, local
clones, raw logs, credentials, account state, and personal notes outside this
repo.

Start by asking me where I want to begin:
1. Set up my private OSS workbench
2. Find new OSS projects to help
3. Follow up existing PRs or issues
4. Prepare a focused PR or comment
5. Publish an impact update
6. Just explain the workflow

Do not scan, clone, patch, post, or open a PR until I choose a starting point.
Do not take public action until I approve the target and message.
```

See [START.md](START.md) for first-run setup, modes, and next steps.

## Easy Start

Pick one mode:

| Mode | Use when | First result |
| --- | --- | --- |
| Learn | You are new to the workflow | A short explanation and recommended next step |
| Set up | You want a private local workbench | A safe folder layout and starter ledgers |
| Scout | You want new OSS leads | Candidate issues after reject checks only |
| Follow up | You already have PRs or comments open | A compact action list |
| Prepare | You approved one target | A focused comment, repro, docs fix, test, or PR plan |
| Impact | You want a public receipt | Sanitized aggregate impact draft |

Default first run: ask where to start. No surprise scans, no public action.

## Philosophy

Many developers have unused model capacity: idle subscription windows, spare
API budget, local agent time, or small gaps between larger work. This project
turns that capacity into practical OSS help:

- bug reproduction
- issue triage
- docs fixes
- focused tests
- small CI repairs
- low-risk patches
- respectful review follow-up

The point is not contribution graph farming. The point is useful maintenance.
If the action mostly helps you and not the maintainer, skip it.

## What This Is

- A public, reusable method for agent-assisted OSS support.
- A set of validation gates before public action.
- Templates for scoped slices, comments, PRs, and status ledgers.
- Portable skill packs for scout, PR, and review workflows.
- A privacy-safe way to publish aggregate impact.
- A durable memory system for lessons learned from maintainer feedback.

## What This Is Not

- Not a bounty-hunting system.
- Not a bot for mass comments.
- Not a replacement for human judgment.
- Not a way to hide AI assistance.
- Not a public dump of private agent logs or working directories.

## Core Loop

![OSS Supporter operating loop](assets/operating-loop.svg)

1. Scout: find likely-useful issues or PR follow-ups.
2. Reject fast: archived, stale, duplicate, crowded, unclear, or high-risk.
3. Claim locally: avoid duplicate action across operators or agents.
4. Slice: create a small work record with target, scope, validation, and risks.
5. Verify: reproduce, patch, and test at the right depth.
6. Disclose: be plain about agent assistance when publishing work.
7. Follow up: read reviews, fix small valid feedback, and record lessons.
8. Clean up: move merged/closed/dropped work out of active state.

See [docs/operating-model.md](docs/operating-model.md).

## Public Boundary

This repo is designed to be public. Keep private workbench data elsewhere:

- raw chats and prompts
- credentials and account state
- CLA/legal status details beyond public facts
- private queue notes
- local clone directories
- unredacted session logs
- private identity details

Publish methods, templates, sanitized examples, and aggregate impact.

See [docs/publication-boundary.md](docs/publication-boundary.md).

## Repository Shape

```text
assets/     public README and docs visuals
docs/       reusable playbooks and policies
examples/   sanitized public case studies
impact/     aggregate public impact snapshots
skills/     portable Markdown agent workflows
templates/  copyable issue, slice, PR, and status templates
tools/      optional local helpers; never require a specific agent
```

## Impact Meter

The public repo includes a local token usage scanner:

```bash
python tools/token-meter/token_meter.py --include-cwd oss-supporter
```

It reads Codex JSONL logs and emits aggregate-only token totals. It does not
publish prompts, responses, raw paths, or session IDs.

## Status Helpers

The repo also includes GitHub CLI helpers for checking submitted PRs/comments:

```bash
pwsh ./tools/status/oss-status.ps1 -LeadClaimsPath work/lead-claims.md
```

See [tools/status](tools/status/README.md).

## Impact

Use the meter to create a private `.local.*` snapshot, review it, then publish a
sanitized public receipt under [impact/](impact/README.md).

Latest public receipt: [May 2026](impact/2026-05.md).

Public receipts should show the useful part:

- tokens spent on OSS support
- projects helped
- PRs, comments, reproductions, and review fixes
- merged or maintainer-accepted outcomes

They should not show private logs, local paths, raw conversations, account data,
or hidden queues.

## Deeper Docs

Read these in order:

1. [START.md](START.md)
1. [docs/operating-model.md](docs/operating-model.md)
2. [docs/validation-gates.md](docs/validation-gates.md)
3. [docs/public-voice.md](docs/public-voice.md)
4. [docs/review-followup.md](docs/review-followup.md)
5. [docs/impact-ledger.md](docs/impact-ledger.md)
6. [docs/adapters.md](docs/adapters.md)

Then copy [templates/work-slice.md](templates/work-slice.md) for the first
small support attempt.

Optional agent workflows live in [skills/](skills/README.md).

## License

MIT. Take it, adapt it, remix it, and use it to help maintainers.
