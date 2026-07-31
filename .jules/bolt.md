## 2025-07-17 - Efficiency of str.isprintable()
**Learning:** Checking for printable characters via `not value.isprintable()` is ~15-18x faster than manual character-by-character iteration with `any(not c.isprintable() for c in value)` in Python.
**Action:** Always prefer the built-in `str.isprintable()` method over manual loops or generators for character validation.

## 2025-07-17 - Grouped I/O in scripts/init.py
**Learning:** Performing multiple consecutive file reads/writes on the same files (`pyproject.toml`, `mkdocs.yml`) causes redundant disk I/O overhead.
**Action:** Group file modifications by file path to perform exactly one read and one write operation per file.

## 2025-07-17 - Batch Git Config Subprocess Invocations in scripts/init.py
**Learning:** Sequential `subprocess` querying of Git configuration parameters (`user.name`, `user.email`, `github.user`) during interactive CLI initialization is slow (~3x overhead). Running a single batch subprocess query via `git config --get-regexp` and caching the result reduces the initialization delay significantly. Additionally, using an initialization flag prevents redundant subprocess calls when all configs are missing (e.g. in empty or CI environments).
**Action:** Cache git configuration queries globally on first use with an explicit initialization flag.
