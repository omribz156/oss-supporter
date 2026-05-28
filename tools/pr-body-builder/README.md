# PR Body Builder

Build a safe body file for `gh pr create --body-file`.

```bash
python tools/pr-body-builder/pr_body_builder.py \
  --summary "Fix the narrow issue" \
  --verify "git diff --check" \
  --fixes "#123" \
  --out work/pr-body.local.md
```

The output keeps summary, verification, and disclosure in a consistent shape.
It is a draft, not a substitute for reviewing project templates and legal text.
