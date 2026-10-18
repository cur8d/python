---
name: init-project
description: Initializes and customizes a new Python project repository from the cur8d/python template. Use whenever the user asks to initialize, bootstrap, or configure a newly cloned or forked Python project.
category: system
tags: [scaffolding, template, init, python, uv, cur8d]
---

# Initialize Project from cur8d/python Template

This skill guides you through transforming a newly cloned or forked `cur8d/python` repository into a customized, standalone Python project.

## Prerequisites

- Python 3.12+ and `uv` installed
- `mise` installed
- Clean git working tree

## Workflow

### 1. Gather Project Parameters
Identify or ask the user for:
- **Project Name** (kebab-case or snake_case, e.g., `my-service`)
- **Description** (one-line summary, e.g., `Fast asynchronous data processing service`)
- **Author Name** and **Email** (fallback to current git user: `git config user.name`, `git config user.email`)
- **GitHub Username / Org** (e.g., `cur8d` or your personal handle)

### 2. Execute Template Initialization
Run the initialization script using `uv`:

```bash
uv run python scripts/init.py \
  --name "<project-name>" \
  --description "<project-description>" \
  --author "<author-name>" \
  --email "<author-email>" \
  --github "<github-username>"
```

*(Or simply run `mise run init` or `uv run python scripts/init.py` to use interactive prompts with git defaults).*

The script will:
- Rename `project/` to the sanitized project name (e.g., `my_service/`).
- Update package metadata, scripts, and dependencies in `pyproject.toml`.
- Update repository references in `mkdocs.yml`, `docs/README.md`, and `.github/CODEOWNERS`.
- Remove `scripts/init.py` upon successful completion.

### 3. Sync Environment & Dependencies
Synchronize the virtual environment and lockfile:

```bash
uv sync
```

### 4. Verify Baseline
Run repository verification:

```bash
mise run verify
```

## Boundaries

✅ **Always do:**
- Always run `mise run verify` after initialization to ensure package imports and tests pass.
- Always check `git config` for author defaults before prompting.
- Always run `uv sync` to refresh the virtual environment.

🚫 **Never do:**
- Never run the initialization script with invalid names (only alphanumeric characters, dashes, and underscores allowed).
- Never push initial changes to the upstream `cur8d/python` template repository.
