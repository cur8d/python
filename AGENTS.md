# AGENTS.md

This file provides guidelines for AI coding agents (e.g., GitHub Copilot, Cursor, Codex) working in this repository.

---

## Project Overview

This is a **Python project template** that provides a pre-configured, production-ready starting point for Python applications. It includes out-of-the-box support for:

- **Packaging & dependency management** via [uv](https://docs.astral.sh/uv)
- **CLI** via [click](https://click.palletsprojects.com)
- **Testing & coverage** via [pytest](https://pytest.org) and [coverage](https://coverage.readthedocs.io)
- **Linting, formatting & import sorting** via [ruff](https://docs.astral.sh/ruff)
- **Type checking** via [pyright](https://microsoft.github.io/pyright)
- **Pre-commit hooks** via [pre-commit](https://pre-commit.com)
- **Documentation** via [MkDocs](https://www.mkdocs.org) with [mkdocstrings](https://mkdocstrings.github.io), auto-deployed to GitHub Pages
- **CI/CD** via GitHub Actions
- **Containerisation** via Docker and Dev Containers
- **Environment & Task Management** via [mise](https://mise.jdx.dev)

---

## Project Structure

```
├── .devcontainer/              # Dev container configuration
├── .github/                    # GitHub-specific files (Actions, templates, Dependabot)
├── .vscode/                    # VS Code settings
├── docs/                       # Documentation source
│   ├── README.md               # Project README and MkDocs home page
│   ├── CONTRIBUTING.md         # Contributing guidelines
│   └── reference/              # Auto-generated API reference pages
├── project/                    # Main source package (renamed via `mise run project`)
│   ├── __init__.py
│   └── app.py                  # CLI entry point
├── tests/                      # Test suite
│   ├── conftest.py             # Shared pytest fixtures and hooks
│   └── test_app.py             # Sample tests
├── compose.yml                 # Docker Compose file
├── Dockerfile                  # App container
├── mise.toml                   # Workflow automation tasks
├── mkdocs.yml                  # MkDocs configuration
├── pyproject.toml              # Project metadata, dependencies, and tool configuration
└── uv.lock                     # Locked dependency versions (do not edit manually)
```

> **Note:** The `project/` folder is the template placeholder. After initialising a real project with `mise run project name=...`, it is renamed to the chosen package name.

---

## Setup

### Prerequisites

- [mise](https://mise.jdx.dev)
- Docker (for Dev Container or containerised runs)

### First-time setup

```bash
# Install tools, project dependencies, and pre-commit hooks
mise run dev
```

### Rename the template for a new project (run once)

```bash
mise run project --name "my-project" --description "My app" --author "Your Name" --email "you@example.com" --github "your-username"
```

---

## Common Commands

| Task | Command | Alias |
|---|---|---|
| Install dependencies | `mise run install` | `i` |
| Update dependencies | `mise run update` | `u` |
| Lint and format | `mise run lint` | `l` |
| Run tests with coverage | `mise run test` | `t` |
| Run app locally | `mise run app` | `a` |
| Run app in Docker | `docker compose run app` | |
| Serve docs locally | `mise run local-docs` | `d` |
| Deploy docs to GitHub Pages | `mise run docs` | |
| Setup dev environment | `mise run dev` | |
| Full setup from scratch | `mise run all` | |
| Initialize the project | `mise run project` | `p` |

> Refer to `docs/README.md` for the full list of available targets. Add new targets to `mise.toml` as needed.

---

## Code Style

- **Line length**: 120 characters (configured in `pyproject.toml` under `[tool.ruff]`)
- **Linter/formatter**: `ruff` — enforces `E` (pycodestyle errors) and `I` (isort) rules
- **Type checker**: `pyright` — all imports must resolve; missing imports are errors
- **Pre-commit**: hooks run `ruff` automatically before every commit
- Run `mise run lint` to format, sort imports, and check types manually
- All public functions and classes must have docstrings (used by `mkdocstrings` for API docs)

---

## Testing

- Tests live in the `tests/` directory and mirror the source structure
- Run the full test suite with coverage using `mise run test` (runs `pytest` via `coverage`)
- Coverage is measured with branch coverage enabled; the report is printed to the terminal and exported as `coverage.xml`
- Shared fixtures belong in `tests/conftest.py`
- Test files must be named `test_*.py`

---

## Git Workflow

- Work on feature branches; open a pull request to `main`
- Pre-commit hooks enforce formatting and linting on every commit
- CI (`.github/workflows/check.yml`) runs lint and tests on every push
- Do not commit directly to `main`

---

## Dependencies

- Always use uv for dependency management (`uv add <package>`)
- Use Pydantic for data models
- Use Pydantic-settings for environment variable configuration in a `settings.py` file

## Testing Guidelines

- Use pytest, not unittest
- Use `pytest` monkeypatch and `pytest-mock` for mocking instead of `unittest.MagicMock`
- Do not cheat! Never modify source code just to make a failing test pass. Fix real bugs in source code and fix incorrect assertions in tests

## Mise Tasks

Use `mise` tasks for all common workflows: lint, test, run locally, and deploy. Refer to `docs/README.md` for currently available tasks. Add new tasks to `mise.toml` as needed.

## Notes

- Python 3.12+ required
- Dependencies are managed via `pyproject.toml` and locked in `uv.lock`
- Do not edit `uv.lock` directly; use `mise run update` to update dependencies

## Coding Conventions

### Field descriptions

Every field in a Pydantic model or pydantic-settings class must be documented using `Field(description="...")`. This makes descriptions machine-readable and visible in generated JSON schemas.

```python
from uuid import uuid4
from pydantic import BaseModel, Field

class Item(BaseModel, populate_by_name=True, alias_generator=to_camel):
    id: str = Field(description="Unique item identifier.", default_factory=lambda:str(uuid4()))
    name: str = Field(description="Human-readable item name.")
```

### camelCase alias convention

All `BaseModel` subclasses must be defined with `populate_by_name=True` and `alias_generator=to_camel` so that JSON payloads can use camelCase while Python attributes use snake_case. Always serialise with `model_dump(by_alias=True, exclude_none=True)` to produce camelCase JSON output and omit unset optional fields.

```python
from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

class Item(BaseModel, populate_by_name=True, alias_generator=to_camel):
    item_id: str = Field(description="Unique item identifier.", default_factory=str(uuid4()))
    # Accepts {"itemId": "..."} from JSON; attribute is item.item_id
    # model_dump() → {"item_id": ...}
    # model_dump(by_alias=True, exclude_none=True) → {"itemId": ...}
```

### No `model_config` class attribute

Do not use `model_config = ConfigDict(...)` or `model_config = SettingsConfigDict(...)`. Pass configuration options as keyword arguments to the base class instead.

```python
# Good
class Item(BaseModel, extra="allow", populate_by_name=True, alias_generator=to_camel): ...
class Settings(BaseSettings, case_sensitive=False): ...

# Bad
class Item(BaseModel):
    model_config = ConfigDict(extra="allow")
```

### Import style

Do not add unnecessary imports like `from __future__ import annotations`. Always use explicit `from x import y` form:

```python
from json import dumps, loads
from pytest import fixture, main, raises
from aws_cdk.aws_lambda import Code, Function, Runtime
```

### Test file main block

Every test file must end with:

```python
if __name__ == "__main__":
    main()
```
