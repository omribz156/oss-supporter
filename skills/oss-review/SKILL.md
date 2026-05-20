---
name: oss-review
description: Check status on already-sent OSS comments and PRs, read maintainer comments, reviews, inline threads, CI results, and merge/closure state, then make focused fixes or cleanup records. Use when checking current open status, updates, review follow-up, CI triage, merged/closed cleanup, or whether submitted work still needs action.
---

# OSS Review

## Job

Review public work already sent. Decide whether each item is clear, waiting,
merged/done, blocked, or needs a focused fix. Patch and reply when feedback is
actionable and small.

Use `oss-pr-flow` for first-time implementation. Use `oss-scout` for finding
new leads.

## First Reads

When working inside an OSS Supporter-style workbench, read:

- project instructions or `AGENTS.md`
- shared lead claims
- review/maintainer lessons
- active scan/slice files for the target
- review follow-up and cleanup docs

Suggested public docs in this repo:

- `docs/review-followup.md`
- `docs/public-voice.md`
- `templates/status-entry.md`
- `tools/status/README.md`

## Status Loop

1. Build the open set from claims, active ledgers, and slice receipts.
2. For each PR/comment, fetch current public state before deciding.
3. Separate maintainer feedback, CI state, mergeability, legal/account gates, bot noise, and unrelated failures.
4. If feedback is actionable and small, patch locally, verify, push, and reply with what changed.
5. If blocked on user/legal/account action, mark `watch` or `blocked-user`; do not act for the user.
6. If merged/closed/dropped, update claim and slice outcome, then clean bulky local clones when safe.
7. If no action is needed, report `clear / waiting for review`.

## Status Query

Use equivalent forge/API commands. For GitHub CLI:

```bash
gh pr view N --repo OWNER/REPO --json url,state,mergeStateStatus,reviewDecision,isDraft,comments,reviews,statusCheckRollup
gh pr checks N --repo OWNER/REPO
gh pr view N --repo OWNER/REPO --comments
gh api repos/OWNER/REPO/pulls/N/comments
gh issue view N --repo OWNER/REPO --json state,comments,labels,assignees,updatedAt,url
```

For inline review threads, fetch pull comments as well as top-level reviews. A
`CHANGES_REQUESTED` state is not enough context by itself.

## Decision Words

- `clear`: no requested action; waiting for maintainer or CI
- `fix`: actionable maintainer/CI feedback; patch now if small
- `blocked-user`: legal/account/private action needed
- `blocked-maintainer`: needs maintainer decision or missing permission
- `merged`: update receipts and cleanup
- `closed/dropped`: record outcome and cleanup
- `unclear`: gather one more specific source, then decide

## CI Interpretation

- Patch-specific checks first.
- Broad matrix failures need logs before code changes.
- Compare failure scope against untouched areas.
- Bot-only “review required” is usually waiting, not action.
- CLA/DCO failures are user/legal gates unless the fix is a commit signoff the operator explicitly approved.

## Fix Feedback

Before patching:

- fetch top-level reviews
- fetch inline pull comments
- fetch issue/PR comments
- check CI logs only for failing checks tied to the patch
- read local diff and current branch before editing

Patch discipline:

- address the exact requested change
- avoid drive-by refactors
- preserve PR template/legal text
- use body files or structured API input for multiline public text
- add/update focused tests when behavior is affected

## Public Reply Rule

Patch first, verify second, reply third.

Keep replies short:

```text
Thanks, fixed in the latest push.

Changed <specific thing>. Verified with `<command>`.
```

Mention agent assistance when opening/updating substantive public work or when
venue/policy expects it. Do not make every tiny review reply about the tool.

## Cleanup Rule

After merge/close/drop:

- update claims
- update slice outcome
- move active items to done/watch as appropriate
- keep public-action links
- delete bulky local clones only when another patch is unlikely
- add reusable maintainer feedback to review lessons
