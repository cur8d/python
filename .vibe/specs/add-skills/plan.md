# Implementation Plan: Agent Skills for cur8d Python

Establish structured Agent Skills in `cur8d/python` so AI coding agents can reliably initialize projects from the template, build domain modules and CLI commands, and run automated verification and repair.

## Proposed Changes

### Skills Scaffolding

#### [NEW] `.agents/skills/init-project/SKILL.md`
- Instructions for customizing the template into a standalone Python project repository using `scripts/init.py`.

#### [NEW] `.agents/skills/add-module/SKILL.md`
- Instructions for creating new domain modules, models, and services with type annotations, docstrings, and comprehensive pytest unit tests.

#### [NEW] `.agents/skills/add-cli-command/SKILL.md`
- Instructions for adding CLI commands/subcommands via Click, registering entry points in `pyproject.toml`, and testing with `CliRunner`.

#### [NEW] `.agents/skills/verify-and-fix/SKILL.md`
- Automated diagnostic and remediation steps for linting (ruff), type checking (pyright), and testing (pytest).

---

### Documentation & Agents Guidance

#### [MODIFY] `AGENTS.md`
- Document the newly introduced skills under `.agents/skills/`.
- Provide guidance on using `npx skills add cur8d/python` or invoking skills directly.

#### [MODIFY] `docs/README.md`
- Add an "Agent Skills" section explaining how developers and agents can consume the repository's built-in skills.

---

### Verification Plan

#### Automated Verification
- Run `mise run verify` (linting with ruff, type checks with pyright, and pytest suite execution).
- Run `npx skills ls` to confirm skills are detected by the skills CLI.
