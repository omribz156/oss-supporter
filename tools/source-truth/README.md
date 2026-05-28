# Source Truth Check

Search before editing docs, generated files, schemas, or examples.

```bash
python tools/source-truth/source_truth_check.py path/to/repo --touched docs/example.md
```

This helps catch the common review failure where a visible file is generated
from a template elsewhere.
