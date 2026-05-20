param(
  [Parameter(Mandatory = $true)]
  [string]$Repo,

  [Parameter(Mandatory = $true)]
  [int]$Number,

  [string]$JsonOut = "",
  [switch]$IncludeBodies
)

$ErrorActionPreference = "Stop"

function Invoke-GhJson {
  param([string[]]$GhArgs)

  $output = & gh @GhArgs
  if ($LASTEXITCODE -ne 0) {
    throw ($output -join "`n")
  }

  return ($output -join "`n") | ConvertFrom-Json
}

function Compress-Body {
  param([string]$Body)

  if (-not $IncludeBodies) {
    return ""
  }
  return ($Body -replace "\s+", " ").Trim()
}

$pr = Invoke-GhJson -GhArgs @("pr", "view", "$Number", "--repo", $Repo, "--json", "url,title,state,mergedAt,mergeStateStatus,reviewDecision,isDraft,author,headRefName,baseRefName,comments,reviews,statusCheckRollup,commits,updatedAt")
$inlineComments = Invoke-GhJson -GhArgs @("api", "repos/$Repo/pulls/$Number/comments")

$failedChecks = @($pr.statusCheckRollup | Where-Object { $_.conclusion -in @("FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED") })
$pendingChecks = @($pr.statusCheckRollup | Where-Object { $_.status -and $_.status -ne "COMPLETED" })

$result = [pscustomobject]@{
  Repo = $Repo
  Number = $Number
  Url = $pr.url
  Title = $pr.title
  State = if ($pr.mergedAt) { "MERGED" } else { $pr.state }
  ReviewDecision = $pr.reviewDecision
  MergeStateStatus = $pr.mergeStateStatus
  Draft = $pr.isDraft
  Author = $pr.author.login
  Branch = $pr.headRefName
  Base = $pr.baseRefName
  UpdatedAt = $pr.updatedAt
  Comments = @($pr.comments | ForEach-Object {
    [pscustomobject]@{
      Author = $_.author.login
      CreatedAt = $_.createdAt
      Body = Compress-Body $_.body
    }
  })
  Reviews = @($pr.reviews | ForEach-Object {
    [pscustomobject]@{
      Author = $_.author.login
      State = $_.state
      SubmittedAt = $_.submittedAt
      Body = Compress-Body $_.body
    }
  })
  InlineComments = @($inlineComments | ForEach-Object {
    [pscustomobject]@{
      Author = $_.user.login
      Path = $_.path
      Line = $_.line
      CreatedAt = $_.created_at
      Body = Compress-Body $_.body
      Url = $_.html_url
    }
  })
  FailedChecks = @($failedChecks | ForEach-Object {
    [pscustomobject]@{
      Name = $_.name
      Conclusion = $_.conclusion
      Status = $_.status
      Url = $_.detailsUrl
    }
  })
  PendingChecks = @($pendingChecks | ForEach-Object {
    [pscustomobject]@{
      Name = $_.name
      Status = $_.status
      Url = $_.detailsUrl
    }
  })
  Commits = @($pr.commits | ForEach-Object {
    [pscustomobject]@{
      Oid = $_.oid
      Message = ($_.messageHeadline -replace "\s+", " ").Trim()
    }
  })
}

if ($JsonOut) {
  $dir = Split-Path -Parent $JsonOut
  if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
  }
  $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $JsonOut -Encoding utf8
}

$result | ConvertTo-Json -Depth 8
