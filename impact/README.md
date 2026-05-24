# Impact

This directory holds public aggregate impact snapshots.

Snapshots should be generated from private workbench data, reviewed by a human,
and committed only after sanitization.

Do not commit raw logs or session files.

## Public Receipt Flow

1. Generate a local snapshot:

   ```bash
   python tools/token-meter/token_meter.py \
     --include-cwd oss-supporter \
     --json-out impact/YYYY-MM.local.json \
     --markdown-out impact/YYYY-MM.local.md
   ```

2. Review the `.local.*` files privately.

3. Copy only safe aggregate values into a public file:

   ```text
   impact/YYYY-MM.md
   ```

4. Link the newest public snapshot from this file and the main README.

## Published Snapshots

Add newest first:

| Period | Snapshot | Tokens | Projects Helped | PRs Merged |
| --- | --- | ---: | ---: | ---: |
| 2026-05 | [snapshot](2026-05.md) | 1,030,308,708 | 70 | 29 |

Template: [impact-snapshot.md](../templates/impact-snapshot.md).

## Publish Checklist

- aggregate counts only
- public project links only
- no raw prompts or responses
- no private local paths
- no session IDs
- no account, token, or CLA details
- no hidden queues or private notes
