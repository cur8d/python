## 2025-07-17 - Efficiency of str.isprintable()
**Learning:** Checking for printable characters via `not value.isprintable()` is ~15-18x faster than manual character-by-character iteration with `any(not c.isprintable() for c in value)` in Python.
**Action:** Always prefer the built-in `str.isprintable()` method over manual loops or generators for character validation.

## 2025-07-17 - Grouped I/O in scripts/init.py
**Learning:** Performing multiple consecutive file reads/writes on the same files (`pyproject.toml`, `mkdocs.yml`) causes redundant disk I/O overhead.
**Action:** Group file modifications by file path to perform exactly one read and one write operation per file.

## 2025-07-18 - Batching Git Config Queries in Project Initialization
**Learning:** Querying multiple git configuration options sequentially via individual subprocess calls (`subprocess.check_output`) introduces substantial process spawning overhead (averaging ~3-5ms per call). Fetching all needed keys in a single batch call using `git config --get-regexp` reduces overhead by ~3x.
**Action:** Always batch git configuration queries using `--get-regexp` and cache the results to prevent redundant subprocess spawns during setup.

## 2025-07-19 - Pre-compiled Regex Patterns at Module Scope
**Learning:** Compiling regex patterns once at the module level rather than on-the-fly inside functions or loops yields ~1.14x speedup, avoiding redundant internal cache dictionary lookups and syntax validation in python's `re` module.
**Action:** Always pre-compile regex patterns at the module scope for repeated validation or multi-file replacement operations.
