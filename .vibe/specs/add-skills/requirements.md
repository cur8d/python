# Requirements: Agent Skills for cur8d Python

## Overview

Equip the `cur8d/python` repository with modular Agent Skills following the open standard (compatible with `skills.sh`, Claude Code, Cursor, GitHub Copilot, and Google Antigravity). These skills enable AI agents to autonomously initialize new projects from this template, scaffold domain modules and Click CLI commands, and run automated verification and auto-repair.

## User Goals

1. Enable developers and AI agents to initialize a new standalone Python project from this template with customized package name, description, author, and git setup.
2. Enable agents to scaffold new domain services/modules with type annotations and clean architecture.
3. Enable agents to add new CLI commands and subcommands with Click and register them in `pyproject.toml`.
4. Provide an iterative code verification and auto-remediation skill executing `mise run verify` (ruff check/format, pyright, pytest).
5. Support distribution via `npx skills add cur8d/python` and project-level discovery under `.agents/skills/`.

## Functional Requirements

1. **`init-project` Skill**:
   - Location: `.agents/skills/init-project/SKILL.md`
   - Guides the agent through customizing the template into a standalone repository.
   - Executes `uv run python scripts/init.py` (with flags `--project-name`, `--description`, `--author` or interactive prompts).
   - Replaces placeholders in `pyproject.toml`, `mkdocs.yml`, `docs/README.md`, and renames the `project/` directory if needed.
   - Resets git tracking and installs fresh dependencies using `uv sync`.

2. **`add-module` Skill**:
   - Location: `.agents/skills/add-module/SKILL.md`
   - Instructions for the agent to scaffold a new domain module under `project/<module_name>/`.
   - Requires full type annotations (`pyright`-compliant) and Google/PEP 257 style docstrings.
   - Requires matching unit tests under `tests/test_<module_name>.py` with complete test coverage.

3. **`add-cli-command` Skill**:
   - Location: `.agents/skills/add-cli-command/SKILL.md`
   - Instructions to add a new CLI command or subcommand using Click in `project/app.py` or `project/cli/`.
   - Wires CLI parameters, help texts, and error handling.
   - Registers script entry points under `[project.scripts]` in `pyproject.toml` if creating a standalone binary.
   - Scaffolds CLI runner tests in `tests/test_cli.py` using Click's `CliRunner`.

4. **`verify-and-fix` Skill**:
   - Location: `.agents/skills/verify-and-fix/SKILL.md`
   - Step-by-step diagnostic and auto-repair workflow for Python projects:
     1. Run `mise run verify` (linting, type checking, security audits, test suite).
     2. Automatically format and fix mechanical issues using `uv run ruff check --fix` and `uv run ruff format`.
     3. Diagnose and fix type errors identified by `pyright`.
     4. Resolve any test failures or coverage drops reported by `pytest`.

5. **Integration & Discoverability**:
   - Update `AGENTS.md` and `docs/README.md` to document the newly added skills and how to consume them via `npx skills`.

## Non-Functional Requirements

- All skills must include valid YAML frontmatter (`name`, `description`, `category`, `tags`).
- Descriptions must be trigger-rich and action-oriented for progressive disclosure.
- Must keep each `SKILL.md` file concise (under 500 lines).
- Must adhere strictly to existing repository validation (`mise run verify` must pass).
