# Cleanup Doctor

Dry-run scanner for old heavy folders such as `repo/`, `node_modules`, `.venv`,
and build caches.

```bash
python tools/cleanup-doctor/cleanup_doctor.py --root path/to/workbench --older-than-days 14
python tools/cleanup-doctor/cleanup_doctor.py --root path/to/workbench --markdown
```

It never deletes. Use it to decide what your private cleanup scripts should
remove after public receipts are recorded.
