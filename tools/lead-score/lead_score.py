#!/usr/bin/env python3
"""Score a GitHub issue before spending clone/build time."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


TARGET_RE = re.compile(r"^([^/]+)/([^#]+)#(\d+)$")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = score_target(args.target)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif args.markdown:
        print_markdown(result)
    else:
        print_text(result)
    return 0 if result["decision"] != "error" else 2


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score one GitHub issue for OSS Supporter fit.")
    parser.add_argument("target", help="owner/repo#123")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true", help="Emit Markdown.")
    return parser.parse_args(argv)


def score_target(target: str) -> dict[str, Any]:
    match = TARGET_RE.match(target)
    if not match:
        return {"target": target, "decision": "error", "score": -100, "risks": ["Target must look like owner/repo#123."]}

    owner, repo, number = match.groups()
    repo_name = f"{owner}/{repo}"
    try:
        repo_data = gh_json(["repo", "view", repo_name, "--json", "isArchived,pushedAt,hasIssuesEnabled"])
        issue = gh_json(["issue", "view", number, "--repo", repo_name, "--json", "state,title,labels,comments,updatedAt,url,body"])
        dupes = gh_json(["pr", "list", "--repo", repo_name, "--state", "open", "--search", number, "--json", "number,title,url,updatedAt"])
    except RuntimeError as exc:
        return {"target": target, "decision": "error", "score": -100, "risks": [str(exc)]}

    score = 0
    reasons: list[str] = []
    risks: list[str] = []

    if repo_data.get("isArchived"):
        score -= 100
        risks.append("Repo archived.")
    else:
        score += 2
        reasons.append("Repo active.")

    if issue.get("state") != "OPEN":
        score -= 100
        risks.append(f"Issue is {issue.get('state')}.")
    else:
        score += 2
        reasons.append("Issue open.")

    if days_since(repo_data.get("pushedAt")) > 180:
        score -= 8
        risks.append("Default branch stale.")
    else:
        score += 2
        reasons.append("Recent repo push.")

    if days_since(issue.get("updatedAt")) > 120:
        score -= 4
        risks.append("Issue stale.")
    comment_count = len(issue.get("comments") or [])
    if comment_count > 12:
        score -= 3
        risks.append(f"Crowded issue: {comment_count} comments.")
    elif comment_count == 0:
        score += 1

    if dupes:
        score -= 8
        risks.append("Open PR mentions target: " + ", ".join(f"#{item['number']}" for item in dupes))
    else:
        score += 2
        reasons.append("No open PR found by issue-number search.")

    labels = [label["name"] for label in issue.get("labels", [])]
    if re.search(r"bug|docs|documentation|good first issue|help wanted", " ".join(labels), re.I):
        score += 1
    if len(issue.get("body") or "") < 80:
        score -= 2
        risks.append("Thin issue body.")

    decision = "proceed" if score >= 6 else "watch" if score >= 1 else "skip"
    return {
        "target": target,
        "decision": decision,
        "score": score,
        "title": issue.get("title"),
        "url": issue.get("url"),
        "labels": labels,
        "reasons": reasons,
        "risks": risks,
    }


def gh_json(args: list[str]) -> Any:
    result = subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def days_since(value: str | None) -> int:
    if not value:
        return 9999
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - parsed).days


def print_text(result: dict[str, Any]) -> None:
    print(f"Target: {result['target']}")
    print(f"Decision: {result['decision']}")
    print(f"Score: {result['score']}")
    if result.get("title"):
        print(f"Title: {result['title']}")
    print("Reasons:")
    for item in result.get("reasons") or ["-"]:
        print(f"- {item}")
    print("Risks:")
    for item in result.get("risks") or ["-"]:
        print(f"- {item}")


def print_markdown(result: dict[str, Any]) -> None:
    print(f"## Lead Score: `{result['target']}`")
    print()
    print(f"- Decision: `{result['decision']}`")
    print(f"- Score: `{result['score']}`")
    if result.get("title"):
        print(f"- Title: {result['title']}")
    if result.get("url"):
        print(f"- URL: {result['url']}")
    print()
    print("### Reasons")
    for item in result.get("reasons") or ["-"]:
        print(f"- {item}")
    print()
    print("### Risks")
    for item in result.get("risks") or ["-"]:
        print(f"- {item}")


if __name__ == "__main__":
    sys.exit(main())
