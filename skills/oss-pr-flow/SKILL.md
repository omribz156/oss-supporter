---
name: oss-pr-flow
description: Execute a validated OSS contribution from claim to public action and cleanup. Use when a target has been chosen and the agent needs to create a slice, inspect policy, patch code/docs/tests, verify locally, write a PR or comment, disclose assistance, update ledgers, and watch the item.
---

# OSS PR Flow

## Job

Turn a validated OSS target into a focused public contribution with receipts.
Keep scope tight, verify honestly, disclose assistance, and update durable
memory.

Use `oss-scout` first when the target is not yet validated.

## First Reads

When working inside an OSS Supporter-style workbench, read:

- project instructions or `AGENTS.md`
- shared lead claims
- review/maintainer lessons
- validation gates, public voice, and review follow-up docs

Suggested public docs in this repo:

- `docs/validation-gates.md`
- `docs/public-voice.md`
- `docs/review-followup.md`
- `templates/work-slice.md`
- `templates/pr-body.md`
- `templates/issue-comment.md`

## Public Action Gates

Proceed after validation for:

- focused comments offering help
- reproductions or narrowed triage notes
- small docs, tests, CI, or bug fixes
- routine maintainer feedback updates

Ask the operator before:

- account creation
- spending money
- private identity/payment/account details
- live security probes
- large refactors or product-direction changes
- legal/CLA actions that require the operator personally

## Flow

1. Confirm the target claim exists, or add it before clone/install/patch/comment.
2. Create a work slice using `templates/work-slice.md` or the local equivalent.
3. Read project policy: license, contribution docs, PR template, DCO/CLA signals, AI rules, and maintainer comments.
4. Clone or inspect only after validation gates pass.
5. Patch the smallest behavior that answers the issue. Do not redesign adjacent code silently.
6. Add tests where they lower review burden; keep tests focused.
7. Run focused verification first, then broader checks when cheap and relevant.
8. Prepare public text with summary, verification, and disclosure near the end.
9. Push/open PR or post comment only after reviewing final diff and public text.
10. Update slice, claims, scan notes, and follow-up ledger.

## Verification Language

Say exactly what ran and what did not run. If a command failed for environment
reasons, include the failure and substitute verification. Do not hide unrelated
warnings; label them as existing only when you checked.

## Public Text

PR body shape:

```text
Summary:
- <change>
- <test/docs coverage>

Verification:
- <command or source check>

Notes:
- <known limitation, if any>

This was implemented with agent assistance, with the patch kept focused and
manually reviewed before sending.
```

Issue comment shape:

```text
I traced this through <file/source> and can take a focused pass on <scope>.

The likely fix is <short concrete direction>. I will keep it limited to
<boundary>. This would be agent-assisted, with the final patch manually
reviewed before posting.
```

Avoid agent theater, generic implementation-plan boilerplate, hype, fake
certainty, pressure on maintainers, unexpanded acronyms, and paraphrased
legal/template declarations.

## Review Feedback

Before replying to review, fetch top-level reviews, issue comments, and inline
pull comments. Patch first when feedback is valid and small. Reply with what
changed and what verification ran.

## Cleanup

After merge/close/drop:

- update claims
- update slice outcome
- move active items to done/watch as appropriate
- keep public-action links
- delete bulky local clones only when another patch is unlikely
- add reusable maintainer feedback to review lessons
