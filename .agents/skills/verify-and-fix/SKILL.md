---
name: verify-and-fix
description: Runs repository verification checks (ruff, pyright, pytest, coverage) and iteratively resolves errors, formatting, and lint warnings. Use whenever the user asks to verify, test, lint, or fix code quality issues.
category: coding
tags: [python, ruff, pyright, pytest, quality, cur8d]
---

# Verify and Fix Code in cur8d/python

This skill guides you through executing comprehensive repository verification checks, diagnosing failures, and automatically remediating formatting, typing, and test issues.

## Prerequisites

- Python 3.12+ and `uv` installed
- `mise` installed

## Workflow

### 1. Execute Verification Suite
Run the centralized verification task:

```bash
mise run verify
```

*(This runs linting, formatting check, type checking with pyright, and pytest suite with coverage).*

### 2. Auto-Fix Formatting and Mechanical Lint Issues
If `ruff` reports formatting or mechanical rule violations:

```bash
# Auto-fix linting issues
uv run ruff check --fix .

# Auto-format codebase
uv run ruff format .
```

### 3. Diagnose and Fix Type Errors
If `pyright` reports type errors:
- Review the specific line numbers and error codes reported.
- Add missing type hints, narrow optional types using `if x is not None:` or `assert`, or update type aliases.
- Re-run pyright to verify resolution:
  ```bash
  uv run pyright
  ```

### 4. Diagnose and Fix Test Failures
If `pytest` fails:
- Run failing tests directly with verbose output:
  ```bash
  uv run pytest tests/test_failing.py -v
  ```
- Inspect stack traces and assertions.
- Fix underlying bugs in implementation or update tests if requirements changed legitimately.

### 5. Final Pass
Confirm all quality gates pass:

```bash
mise run verify
```

## Boundaries

✅ **Always do:**
- Always run `uv run ruff check --fix` and `uv run ruff format` before manual edits for style issues.
- Always maintain or improve test coverage.
- Always ensure all checks pass prior to opening a PR.

🚫 **Never do:**
- Never silence errors using `# type: ignore` or `# noqa` without explaining the root cause.
- Never modify tests to pass artificially without fixing the underlying bug.
