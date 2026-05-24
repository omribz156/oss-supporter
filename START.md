# Start Here

OSS Supporter is a public playbook. It is not your live workbench.

Use this page when you give the repo link to an agent or assistant and want it
to start cleanly without guessing.

## One-Paste Agent Start

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

## What The Agent Should Do Next

The first response should be a question, not a scan.

Good first response:

```text
I read the OSS Supporter playbook. Where would you like to start: setup,
scouting, follow-up, preparing one public action, impact, or learning the flow?
```

## Modes

### Learn

Explain the workflow in plain language and recommend the safest first step.

Use when:

- the operator is new
- no local workbench exists yet
- the goal is still unclear

### Set Up

Create a private workbench outside this public repo.

Suggested private shape:

```text
workbench/
  support/
    lead-claims.md
    review-lessons.md
  slices/
  artifacts/
```

Keep raw logs, local clones, credentials, and private notes there, not here.

### Scout

Find candidate OSS work, but stop after validation.

The scout result should include:

- repo and issue link
- why it might help maintainers
- reject-check result
- duplicate PR/comment check
- recommended action
- risk level

No public action in scout mode.

### Follow Up

Check already-open PRs, comments, and review threads.

The result should be:

- merged
- waiting on maintainer
- needs operator action
- needs patch
- blocked by legal/account/user-only step
- safe to clean up

### Prepare

Turn one approved target into a focused action.

Possible actions:

- source-backed issue comment
- reproduction note
- docs fix
- narrow test
- small code patch
- review-feedback update

Verify before public action. Keep the message short and transparent.

### Impact

Create a public-safe receipt from private records.

Publish aggregates only:

- tokens or compute spent
- projects helped
- comments, PRs, reproductions, review fixes
- merged or maintainer-accepted outcomes

Do not publish prompts, responses, session IDs, raw paths, credentials, or
private queues.

## Next Docs

After the first choice, read only what is needed:

- [docs/operating-model.md](docs/operating-model.md) for the full loop
- [docs/validation-gates.md](docs/validation-gates.md) before choosing a target
- [docs/public-voice.md](docs/public-voice.md) before posting
- [docs/review-followup.md](docs/review-followup.md) when maintainers reply
- [docs/impact-ledger.md](docs/impact-ledger.md) before publishing impact
- [docs/publication-boundary.md](docs/publication-boundary.md) when unsure what belongs in public
