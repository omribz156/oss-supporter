param(
  [string]$LeadClaimsPath = "work/lead-claims.md",
  [string]$ActiveLedgerPath = "",
  [string[]]$Statuses = @("active", "sent", "watch", "blocked-user"),
  [string]$JsonOut = "",
  [switch]$IncludePromoted,
  [switch]$ClaimsOnly,
  [switch]$ListRefsOnly
)

$ErrorActionPreference = "Stop"

function Split-MarkdownRow {
  param([string]$Line)

  $trimmed = $Line.Trim()
  if (-not $trimmed.StartsWith("|")) {
    return @()
  }

  return $trimmed.Trim("|").Split("|") | ForEach-Object { $_.Trim() }
}

function Get-PlainText {
  param([string]$Text)

  return ($Text -replace "\[([^\]]+)\]\([^)]+\)", '$1') -replace [char]0x60, ""
}

function Get-PrRefs {
  param([string]$Text)

  $pattern = 'https://github\.com/([^/\s\)]+)/([^/\s\)]+)/pull/(\d+)'
  [regex]::Matches($Text, $pattern) | ForEach-Object {
    [pscustomobject]@{
      Kind = "pr"
      Owner = $_.Groups[1].Value
      Repo = $_.Groups[2].Value
      Number = [int]$_.Groups[3].Value
      Url = $_.Value
    }
  }
}

function Get-IssueRefs {
  param([string]$Text)

  $pattern = 'https://github\.com/([^/\s\)]+)/([^/\s\)]+)/issues/(\d+)'
  [regex]::Matches($Text, $pattern) | ForEach-Object {
    [pscustomobject]@{
      Kind = "issue"
      Owner = $_.Groups[1].Value
      Repo = $_.Groups[2].Value
      Number = [int]$_.Groups[3].Value
      Url = $_.Value
    }
  }
}

function Invoke-GhJson {
  param([string[]]$GhArgs)

  $output = & gh @GhArgs
  if ($LASTEXITCODE -ne 0) {
    throw ($output -join "`n")
  }

  return ($output -join "`n") | ConvertFrom-Json
}

function Summarize-Checks {
  param($Checks)

  if (-not $Checks) {
    return "none"
  }

  $failed = @($Checks | Where-Object { $_.conclusion -in @("FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED") })
  $pending = @($Checks | Where-Object { $_.status -and $_.status -ne "COMPLETED" })
  $passed = @($Checks | Where-Object { $_.conclusion -in @("SUCCESS", "SKIPPED", "NEUTRAL") })

  $parts = @()
  if ($failed.Count) { $parts += "fail:$($failed.Count)" }
  if ($pending.Count) { $parts += "pending:$($pending.Count)" }
  if ($passed.Count) { $parts += "pass:$($passed.Count)" }
  if (-not $parts.Count) { return "unknown:$(@($Checks).Count)" }

  return ($parts -join " ")
}

function Get-FailedCheckNames {
  param($Checks)

  @($Checks | Where-Object { $_.conclusion -in @("FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED") } | ForEach-Object { $_.name }) -join "; "
}

function Get-Action {
  param(
    [string]$Kind,
    [string]$State,
    [string]$ReviewDecision,
    [string]$MergeStateStatus,
    [string]$Checks,
    [string]$FailedNames
  )

  if ($State -eq "MERGED") { return "cleanup-merged" }
  if ($State -eq "CLOSED") { return "cleanup-closed" }
  if ($ReviewDecision -eq "CHANGES_REQUESTED") { return "fix-review" }
  if ($Checks -like "fail:*") {
    if ($FailedNames -match "(CLA|DCO|EasyCLA|license|legal)") { return "blocked-user" }
    return "check-ci"
  }
  if ($Kind -eq "issue-comment") { return "watch-comment" }
  if ($ReviewDecision -eq "APPROVED") { return "watch-merge" }
  if ($MergeStateStatus -eq "CLEAN") { return "clear" }

  return "watch"
}

function Get-LastSignal {
  param(
    $Comments,
    $Reviews
  )

  $signals = @()
  foreach ($comment in @($Comments)) {
    $signals += [pscustomobject]@{
      At = [datetime]$comment.createdAt
      Text = "comment:$($comment.author.login)"
    }
  }
  foreach ($review in @($Reviews)) {
    $signals += [pscustomobject]@{
      At = [datetime]$review.submittedAt
      Text = "review:$($review.author.login):$($review.state)"
    }
  }

  $last = $signals | Sort-Object At -Descending | Select-Object -First 1
  if (-not $last) { return "" }

  return "$($last.Text)@$($last.At.ToString("yyyy-MM-dd"))"
}

function Get-ClaimRows {
  param([string]$Path)

  foreach ($line in Get-Content -LiteralPath $Path) {
    if ($line -notmatch "^\| " -or $line -match "^\| ---") { continue }
    $cells = @(Split-MarkdownRow $line)
    if ($cells.Count -lt 5 -or $cells[0] -eq "Lead") { continue }
    if (-not $wantedStatuses.Contains($cells[1])) { continue }

    [pscustomobject]@{
      Lead = $cells[0]
      Status = $cells[1]
      Owner = $cells[2]
      Notes = $cells[3]
      Updated = $cells[4]
      Raw = $line
    }
  }
}

function Get-ActiveLedgerRows {
  param([string]$Path)

  $inActivePrs = $false
  foreach ($line in Get-Content -LiteralPath $Path) {
    if ($line -match "^## Active PRs") {
      $inActivePrs = $true
      continue
    }
    if ($inActivePrs -and $line -match "^## ") {
      break
    }
    if (-not $inActivePrs -or $line -notmatch "^\| " -or $line -match "^\| ---") {
      continue
    }

    $cells = @(Split-MarkdownRow $line)
    if ($cells.Count -lt 5 -or $cells[0] -eq "Lead") { continue }

    [pscustomobject]@{
      Lead = $cells[0]
      Status = "active-ledger"
      Owner = "operator"
      Notes = "$($cells[1]) $($cells[2]) $($cells[3]) $($cells[4])"
      Updated = ""
      Raw = $line
    }
  }
}

if (-not (Test-Path -LiteralPath $LeadClaimsPath)) {
  throw "Missing lead claims file: $LeadClaimsPath. Copy templates/lead-claim.md or point -LeadClaimsPath at your private ledger."
}

$wantedStatuses = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($status in $Statuses) { [void]$wantedStatuses.Add($status) }
if ($IncludePromoted) { [void]$wantedStatuses.Add("promoted") }

$rows = @(Get-ClaimRows $LeadClaimsPath)

if (-not $ClaimsOnly -and $ActiveLedgerPath -and (Test-Path -LiteralPath $ActiveLedgerPath)) {
  $rows += @(Get-ActiveLedgerRows $ActiveLedgerPath)
}

$seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$results = foreach ($row in $rows) {
  $combined = "$($row.Lead) $($row.Notes)"
  $prs = @(Get-PrRefs $combined)

  if ($prs.Count -gt 0) {
    foreach ($pr in $prs) {
      $key = "pr:$($pr.Owner)/$($pr.Repo)#$($pr.Number)"
      if (-not $seen.Add($key)) { continue }

      $repoName = "$($pr.Owner)/$($pr.Repo)"
      if ($ListRefsOnly) {
        [pscustomobject]@{
          Target = "$(Get-PlainText $row.Lead) -> $repoName#$($pr.Number)"
          ClaimStatus = $row.Status
          Kind = "pr"
          Url = $pr.Url
        }
        continue
      }

      try {
        $data = Invoke-GhJson -GhArgs @("pr", "view", "$($pr.Number)", "--repo", $repoName, "--json", "url,state,mergedAt,mergeStateStatus,reviewDecision,isDraft,comments,reviews,statusCheckRollup,updatedAt")
        $state = if ($data.mergedAt) { "MERGED" } else { $data.state }
        $checks = Summarize-Checks $data.statusCheckRollup
        $failedNames = Get-FailedCheckNames $data.statusCheckRollup

        [pscustomobject]@{
          Target = "$(Get-PlainText $row.Lead) -> $repoName#$($pr.Number)"
          ClaimStatus = $row.Status
          Kind = "pr"
          State = $state
          Review = if ($data.reviewDecision) { $data.reviewDecision } else { "" }
          Merge = if ($data.mergeStateStatus) { $data.mergeStateStatus } else { "" }
          Checks = $checks
          FailedChecks = $failedNames
          Comments = @($data.comments).Count
          Reviews = @($data.reviews).Count
          LastSignal = Get-LastSignal $data.comments $data.reviews
          UpdatedAt = $data.updatedAt
          Action = Get-Action "pr" $state $data.reviewDecision $data.mergeStateStatus $checks $failedNames
          Url = $data.url
        }
      } catch {
        [pscustomobject]@{
          Target = "$(Get-PlainText $row.Lead) -> $repoName#$($pr.Number)"
          ClaimStatus = $row.Status
          Kind = "pr"
          State = "ERROR"
          Review = ""
          Merge = ""
          Checks = "error"
          FailedChecks = ""
          Comments = 0
          Reviews = 0
          LastSignal = ""
          UpdatedAt = ""
          Action = "inspect-error"
          Url = $pr.Url
          Error = $_.Exception.Message
        }
      }
    }
    continue
  }

  $issues = @(Get-IssueRefs $combined)
  if ($issues.Count -gt 0) {
    $issue = $issues[0]
    $key = "issue:$($issue.Owner)/$($issue.Repo)#$($issue.Number)"
    if (-not $seen.Add($key)) { continue }

    $repoName = "$($issue.Owner)/$($issue.Repo)"
    if ($ListRefsOnly) {
      [pscustomobject]@{
        Target = "$(Get-PlainText $row.Lead) -> $repoName#$($issue.Number)"
        ClaimStatus = $row.Status
        Kind = "issue-comment"
        Url = $issue.Url
      }
      continue
    }

    try {
      $data = Invoke-GhJson -GhArgs @("issue", "view", "$($issue.Number)", "--repo", $repoName, "--json", "url,state,comments,updatedAt")
      [pscustomobject]@{
        Target = "$(Get-PlainText $row.Lead) -> $repoName#$($issue.Number)"
        ClaimStatus = $row.Status
        Kind = "issue-comment"
        State = $data.state
        Review = ""
        Merge = ""
        Checks = "n/a"
        FailedChecks = ""
        Comments = @($data.comments).Count
        Reviews = 0
        LastSignal = Get-LastSignal $data.comments @()
        UpdatedAt = $data.updatedAt
        Action = Get-Action "issue-comment" $data.state "" "" "n/a" ""
        Url = $data.url
      }
    } catch {
      [pscustomobject]@{
        Target = "$(Get-PlainText $row.Lead) -> $repoName#$($issue.Number)"
        ClaimStatus = $row.Status
        Kind = "issue-comment"
        State = "ERROR"
        Review = ""
        Merge = ""
        Checks = "error"
        FailedChecks = ""
        Comments = 0
        Reviews = 0
        LastSignal = ""
        UpdatedAt = ""
        Action = "inspect-error"
        Url = $issue.Url
        Error = $_.Exception.Message
      }
    }
  }
}

if ($JsonOut) {
  $dir = Split-Path -Parent $JsonOut
  if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
  }
  $results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonOut -Encoding utf8
}

if ($ListRefsOnly) {
  $results | Sort-Object Kind, Target | Format-Table -AutoSize
  return
}

$results |
  Sort-Object Action, Target |
  ForEach-Object {
    $review = if ($_.Review) { $_.Review } else { "-" }
    $merge = if ($_.Merge) { $_.Merge } else { "-" }
    $signal = if ($_.LastSignal) { $_.LastSignal } else { "-" }
    "{0} | {1} | {2} | review:{3} | merge:{4} | checks:{5} | c/r:{6}/{7} | {8}" -f $_.Action, $_.Target, $_.State, $review, $merge, $_.Checks, $_.Comments, $_.Reviews, $signal
  }
