# Design: Agent Skills for cur8d Python

## Architecture Overview

```mermaid
flowchart TD
    User["Developer Prompt / Issue"] --> Agent["AI Agent (Claude Code, Cursor, Antigravity)"]
    Agent --> Registry[".agents/skills/ Index"]

    subgraph Skills [".agents/skills/"]
        Init["init-project"]
        Module["add-module"]
        CLI["add-cli-command"]
        Verify["verify-and-fix"]
    end

    Registry --> Init & Module & CLI & Verify

    Init -->|"Executes"| Scripts["scripts/init.py<br/>pyproject.toml, zensical.toml"]
    Module -->|"Scaffolds"| Domain["project/<module>/<br/>tests/test_<module>.py"]
    CLI -->|"Configures"| Entry["project/app.py<br/>pyproject.toml [project.scripts]"]
    Verify -->|"Executes"| Tasks["mise run verify (ruff + pyright + pytest)"]
```

## Directory Structure

Skills will be placed in `.agents/skills/` to ensure immediate compatibility with `skills.sh`, Claude Code, Cursor, and other agent platforms:

```text
python/
├── .agents/
│   └── skills/
│       ├── init-project/
│       │   └── SKILL.md
│       ├── add-module/
│       │   └── SKILL.md
│       ├── add-cli-command/
│       │   └── SKILL.md
│       └── verify-and-fix/
│           └── SKILL.md
├── project/
├── tests/
├── scripts/
├── pyproject.toml
└── mise.toml
```

## Skill Definitions

### 1. `init-project`
- **Frontmatter**:
  ```yaml
  ---
  name: init-project
  description: Initializes and customizes a new Python project repository from the cur8d/python template. Use whenever asked to initialize, bootstrap, or fork this template into a new project.
  category: system
  tags: [scaffolding, template, init, python, cur8d]
  ---
  ```
- **Rules**:
  - Leverages `uv run python scripts/init.py` or interactive flags.
  - Updates project names, descriptions, author info, and repository remotes.
  - Runs `uv sync` to prepare virtual environment.

### 2. `add-module`
- **Frontmatter**:
  ```yaml
  ---
  name: add-module
  description: Scaffolds a new domain service, model, or utility module adhering to cur8d standards with type annotations, docstrings, and comprehensive pytest tests. Use whenever asked to add, create, or scaffold a module or service.
  category: coding
  tags: [python, uv, pyright, pytest, cur8d]
  ---
  ```
- **Rules**:
  - Full typing support (`pyright` strict typing without `Any` wherever possible).
  - Docstrings following Google/PEP 257 format.
  - Test suite in `tests/` verifying nominal cases, edge cases, and exception handling.

### 3. `add-cli-command`
- **Frontmatter**:
  ```yaml
  ---
  name: add-cli-command
  description: Adds a new CLI command or subcommand using Click with structured arguments, options, help text, and CliRunner tests. Use whenever asked to add or modify CLI commands.
  category: coding
  tags: [python, click, cli, cur8d]
  ---
  ```
- **Rules**:
  - Leverages Click decorators (`@click.command`, `@click.option`, `@click.argument`).
  - Registers entry points in `pyproject.toml` under `[project.scripts]`.
  - Scaffolds tests using `click.testing.CliRunner`.

### 4. `verify-and-fix`
- **Frontmatter**:
  ```yaml
  ---
  name: verify-and-fix
  description: Runs repository verification checks (ruff, pyright, pytest, coverage) and iteratively resolves errors and lint warnings. Use whenever asked to verify, check, or fix code quality or test issues.
  category: coding
  tags: [python, ruff, pyright, testing, cur8d]
  ---
  ```
- **Rules**:
  - Executes `mise run verify`.
  - Runs `uv run ruff check --fix` and `uv run ruff format`.
  - Reports status and preserves all existing docstrings and comments.
