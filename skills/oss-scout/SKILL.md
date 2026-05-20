---
name: oss-scout
description: Find, validate, and rank open-source contribution leads before cloning, installing dependencies, commenting, or opening PRs. Use when scanning GitHub or another public forge for useful OSS support work, triaging issues, finding company/community targets, or deciding whether a target is worth touching.
---

# OSS Scout

## Job

Find targets where a small public action lowers maintainer burden. Reject weak
leads early. Record claims before any expensive or public step.

Use this as the scouting half of the OSS Supporter flow. For implementation
after a target is chosen, switch to `oss-pr-flow`.

## First Reads

When working inside an OSS Supporter-style workbench, read:

- project instructions or `AGENTS.md`
- shared lead claims
- review/maintainer lessons if a lead is close to public action
- validation gates and public voice docs

Suggested public docs in this repo:

- `docs/validation-gates.md`
- `docs/public-voice.md`
- `templates/lead-claim.md`

## Scout Loop

1. Define the lane: one-off, durable relationship, company-backed, local/community OSS, ecosystem, or specific repo/org.
2. Search metadata first. Prefer repo state, issue state, labels, comment count, last update, assignees, and duplicate PR checks.
3. Reject before clone, dependency install, body-heavy issue reads, or implementation planning.
4. Check shared claims before proceeding. Do not collide with existing public action.
5. For viable targets, decide the smallest useful action: comment, repro, docs, test, CI, or code.
6. Record viable leads and skips in a scan note or ledger.
7. If proceeding beyond scouting, claim the exact `owner/repo#issue` and hand off to `oss-pr-flow`.

## Reject Fast

Hard reject when:

- repo is archived, read-only, transfer-confused, or not PR-able
- default branch is stale and the issue has no fresh maintainer activity
- issue is closed, assigned with active work, or already covered by an open PR
- thread is crowded with drive-by comments and no maintainer response
- issue is vague, huge, product-directional, or requires maintainer-only context
- repo looks like contribution bait, classroom work, generated fixtures, or no real product
- project policy rejects AI-assisted contributions
- work requires account creation, payment, private identity, unclear legal action, or live security probing

Quarantine when the lead might be useful but likely expensive: vague good-first
issues, stale external review queues, heavyweight setup for tiny docs changes,
or cross-repo tasks that may already be claimed.

## Metadata Commands

Use equivalent forge/API commands. For GitHub CLI:

```bash
gh repo view OWNER/REPO --json isArchived,archivedAt,isFork,pushedAt,defaultBranchRef,viewerPermission,licenseInfo,hasIssuesEnabled
gh issue view N --repo OWNER/REPO --json state,title,labels,assignees,comments,updatedAt,author,url
gh pr list --repo OWNER/REPO --state open --search "ISSUE_OR_KEYWORD" --json number,title,url,author,updatedAt
```

Only fetch issue bodies when metadata survives rejection and the body is needed
for evidence.

## Scout Output

Keep outputs lean:

```text
| Target | Status | Why | Risk | Next action |
| --- | --- | --- | --- | --- |
| owner/repo#123 | viable | clear bug, no PR, repo active | needs focused repro | claim + patch |
```

Status words:

- `viable`: worth claiming or handing to PR flow now
- `watch`: good but needs maintainer reply, CI/status change, or user/legal action
- `quarantine`: maybe useful but likely compute sink
- `skip`: rejected with one concrete reason
- `sent`: public action already made
- `done`: merged, closed, dropped, or fully recorded

End with the strongest next target, not a giant backlog.

## Parallel Scouts

Use subagents or parallel workers only when your environment supports it and the
questions are narrow and independent. Scouts may research, inspect, summarize,
and recommend. They must not post, patch, contact maintainers, spend money, run
live security probes, or make final reputation calls.
