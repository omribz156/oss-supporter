# Status Tools

Small GitHub CLI helpers for checking already-sent OSS work without re-reading
every PR thread by hand.

Requirements:

- PowerShell 7+ or Windows PowerShell
- GitHub CLI (`gh`) authenticated for public repo reads

## Compact Sweep

```powershell
./tools/status/oss-status.ps1 -LeadClaimsPath work/lead-claims.md
```

The script reads a Markdown claims table, dedupes PR/issue links, queries
GitHub, and prints compact rows:

```text
action | target | state | review | merge | checks | comments/reviews | last signal
```

Useful actions:

- `clear`: open and merge-clean; no obvious action
- `watch`: waiting for review, maintainer, checks, or merge
- `blocked-user`: waiting on a user-only legal/account gate
- `watch-merge`: approved and likely waiting for merge
- `check-ci`: failing checks need interpretation
- `fix-review`: review state says changes requested; fetch inline comments
- `cleanup-merged` / `cleanup-closed`: update receipts and cleanup

Include a separate active ledger when your workbench keeps open PRs outside the
claims file:

```powershell
./tools/status/oss-status.ps1 `
  -LeadClaimsPath work/lead-claims.md `
  -ActiveLedgerPath work/active-issues.md
```

Write JSON:

```powershell
./tools/status/oss-status.ps1 `
  -LeadClaimsPath work/lead-claims.md `
  -JsonOut work/status-snapshot.local.json
```

Parse links without GitHub calls:

```powershell
./tools/status/oss-status.ps1 -LeadClaimsPath work/lead-claims.md -ListRefsOnly
```

## PR Detail

```powershell
./tools/status/oss-pr-detail.ps1 -Repo owner/repo -Number 123
```

Fetches compact PR detail: review state, merge state, check summary, inline
comment locations, and commit headlines.

Include public comment/review bodies only when needed:

```powershell
./tools/status/oss-pr-detail.ps1 -Repo owner/repo -Number 123 -IncludeBodies
```

Write JSON:

```powershell
./tools/status/oss-pr-detail.ps1 `
  -Repo owner/repo `
  -Number 123 `
  -JsonOut work/pr-123.local.json
```

## Privacy

These scripts query public GitHub state. Keep outputs under ignored local paths
such as `work/` or `*.local.json` until reviewed.
