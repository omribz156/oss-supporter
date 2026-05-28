# Lead Score

Score one GitHub issue before cloning or planning.

```bash
python tools/lead-score/lead_score.py owner/repo#123
python tools/lead-score/lead_score.py owner/repo#123 --markdown
```

Requires authenticated `gh`.

The score checks repo activity, issue state, freshness, comment crowding, labels,
and duplicate open PRs. It is a triage aid, not an autopilot.
