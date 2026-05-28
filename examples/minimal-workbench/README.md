# Minimal Private Workbench Example

Fake example only. Copy the shape into a private folder outside this public repo.

```text
workbench/
  support/
    lead-claims.md
    review-lessons.md
  active-issues.md
  slices/
    one-off/
      2026-05-28-example-doc-fix/
        README.md
```

Try the status parser against the sample claims file:

```powershell
pwsh ../../tools/status/oss-status.ps1 `
  -LeadClaimsPath support/lead-claims.md `
  -ListRefsOnly
```

The links are real public examples, but this folder is not a live queue.
