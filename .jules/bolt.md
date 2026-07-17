## 2025-07-17 - Efficiency of str.isprintable()
**Learning:** Checking for printable characters via `not value.isprintable()` is ~15-18x faster than manual character-by-character iteration with `any(not c.isprintable() for c in value)` in Python.
**Action:** Always prefer the built-in `str.isprintable()` method over manual loops or generators for character validation.

## 2025-07-17 - Grouped I/O in scripts/init.py
**Learning:** Performing multiple consecutive file reads/writes on the same files (`pyproject.toml`, `mkdocs.yml`) causes redundant disk I/O overhead.
**Action:** Group file modifications by file path to perform exactly one read and one write operation per file.
