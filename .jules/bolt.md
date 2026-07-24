## 2025-07-17 - Efficiency of str.isprintable()
**Learning:** Checking for printable characters via `not value.isprintable()` is ~15-18x faster than manual character-by-character iteration with `any(not c.isprintable() for c in value)` in Python.
**Action:** Always prefer the built-in `str.isprintable()` method over manual loops or generators for character validation.

## 2025-07-17 - Grouped I/O in scripts/init.py
**Learning:** Performing multiple consecutive file reads/writes on the same files (`pyproject.toml`, `mkdocs.yml`) causes redundant disk I/O overhead.
**Action:** Group file modifications by file path to perform exactly one read and one write operation per file.

## 2025-07-18 - Batching Subprocess Calls for Git Configuration
**Learning:** Querying git configuration values sequentially using multiple separate subprocess invocations (`git config <key>`) incurs significant process spawning overhead (~10ms per invocation). Batching these lookups using a single POSIX-compatible regex command (`git config --get-regexp`) reduces process creation overhead by 3x (~9ms down to ~3ms) and allows caching the configuration results in-memory.
**Action:** Prefer batching multiple subprocess lookups into a single call with regex or structured output and cache them at module level when possible.
