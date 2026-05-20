# Skills

Portable agent skill packs for OSS Supporter.

These are plain Markdown workflows. Agents that understand `SKILL.md` can load
them directly; other agents can read or paste the instructions as task context.

## Included

| Skill | Use When |
| --- | --- |
| [oss-scout](oss-scout/SKILL.md) | Finding and validating new OSS contribution leads |
| [oss-pr-flow](oss-pr-flow/SKILL.md) | Turning a validated lead into a focused PR/comment |
| [oss-review](oss-review/SKILL.md) | Checking already-sent work, reviews, CI, and cleanup |

## Design Rules

- Agent-agnostic: no required model, vendor, editor, or operating system.
- Human-accountable: the operator owns judgment and public action.
- Public-safe: no raw logs, private paths, account data, or hidden queues.
- Maintainer-first: do not create work just to create a contribution.

## Suggested Use

For a new lead:

1. Load `oss-scout`.
2. If viable, load `oss-pr-flow`.
3. After posting, use `oss-review` for follow-up.

For existing public work:

1. Load `oss-review`.
2. Patch only small actionable feedback.
3. Record merged, closed, dropped, or blocked outcomes.
