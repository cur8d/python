# Requirements: Agent Skills for cur8d Python

## Overview

Equip the `cur8d/python` repository with modular Agent Skills following the open standard (compatible with `skills.sh`, Claude Code, Cursor, GitHub Copilot, and Google Antigravity). These skills enable AI agents to autonomously scaffold, extend, test, and maintain modern Python projects adhering to cur8d's standards (uv, ruff, pyright, pytest, and Click).

## User Goals

1. Enable developers and AI agents to quickly scaffold new domain services/modules with type annotations and clean separation of concerns.
2. Enable agents to add new CLI commands and subcommands with Click and register them in `pyproject.toml`.
3. Provide an iterative code verification and auto-remediation skill that executes `mise run verify` (or `ruff check --fix`, `ruff format`, `pyright`, and `pytest --cov`).
4. Support distribution via `npx skills add cur8d/python` and project-level discovery under `.agents/skills/`.

## Functional Requirements

1. **`add-module` Skill**:
   - Location: `.agents/skills/add-module/SKILL.md`
   - Instructions for the agent to scaffold a new domain module under `project/<module_name>/`.
   - Requires full type annotations (`pyright`-compliant) and Google/PEP 257 style docstrings.
   - Requires matching unit tests under `tests/test_<module_name>.py` with complete test coverage.

2. **`add-cli-command` Skill**:
   - Location: `.agents/skills/add-cli-command/SKILL.md`
   - Instructions to add a new CLI command or subcommand using Click in `project/app.py` or `project/cli/`.
   - Wires CLI parameters, help texts, and error handling.
   - Registers script entry points under `[project.scripts]` in `pyproject.toml` if creating a standalone binary.
   - Scaffolds CLI runner tests in `tests/test_cli.py` using Click's `CliRunner`.

3. **`verify-and-fix` Skill**:
   - Location: `.agents/skills/verify-and-fix/SKILL.md`
   - Step-by-step diagnostic and auto-repair workflow for Python projects:
     1. Run `mise run verify` (linting, type checking, security audits, test suite).
     2. Automatically format and fix mechanical issues using `uv run ruff check --fix` and `uv run ruff format`.
     3. Diagnose and fix type errors identified by `pyright`.
     4. Resolve any test failures or coverage drops reported by `pytest`.

4. **Integration & Discoverability**:
   - Update `AGENTS.md` and `docs/README.md` to document the newly added skills and how to consume them via `npx skills`.

## Non-Functional Requirements

- All skills must include valid YAML frontmatter (`name`, `description`, `category`, `tags`).
- Descriptions must be trigger-rich and action-oriented for progressive disclosure.
- Must keep each `SKILL.md` file concise (under 500 lines).
- Must adhere strictly to existing repository validation (`mise run verify` must pass).
