# Workflow Helpers

Optional helpers for the repetitive parts of OSS support. They are deliberately
small, local, and preview-first.

## Before Choosing A Target

```bash
python tools/lead-score/lead_score.py owner/repo#123
```

Use this to catch archived repos, stale issues, crowded threads, and duplicate
PRs before cloning or planning.

## Before Promising Verification

```bash
python tools/repo-capability/repo_capability.py path/to/repo
```

Use this to detect likely commands and missing local tools. Public PR text
should say what actually ran and what could not run.

## Before Editing Docs Or Generated Files

```bash
python tools/source-truth/source_truth_check.py path/to/repo --touched docs/example.md
```

Use this when touching docs, generated files, schemas, examples, or checked-in
outputs. It nudges you to search for templates and generators first.

## Before Opening A PR

```bash
python tools/pr-body-builder/pr_body_builder.py \
  --summary "Fix the focused issue" \
  --verify "git diff --check" \
  --fixes "#123" \
  --out work/pr-body.local.md
```

Use body files for multiline Markdown. Review project PR templates and legal
text separately.

## Before Publishing This Public Repo

```bash
python tools/public-boundary/check_public_boundary.py
```

Use this before committing copied workbench material.

## Before Cleaning A Workbench

```bash
python tools/cleanup-doctor/cleanup_doctor.py --root path/to/workbench
```

This is dry-run only. Delete after receipts are recorded and follow-up work is
unlikely.
