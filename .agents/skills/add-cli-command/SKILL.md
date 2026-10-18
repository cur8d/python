---
name: add-cli-command
description: Adds a new CLI command or subcommand using Click with structured arguments, options, help text, and CliRunner tests. Use whenever the user asks to add or modify CLI commands or entry points.
category: coding
tags: [python, click, cli, cur8d]
---

# Add CLI Command to cur8d/python

This skill guides you through adding and testing Click-based CLI commands, arguments, options, and entry points in `cur8d/python`.

## Prerequisites

- Python 3.12+ and `uv` installed
- `click` installed in project dependencies

## Workflow

### 1. Define the Command
In `project/app.py` (or a dedicated `project/cli/` module):
- Use Click decorators:
  ```python
  import click


  @click.command()
  @click.argument("name")
  @click.option("--count", default=1, help="Number of greetings.")
  def greet(name: str, count: int) -> None:
      """Greet a user by name."""
      for _ in range(count):
          click.echo(f"Hello, {name}!")
  ```

### 2. Group Subcommands (If Building a Multi-Command CLI)
If organizing subcommands:
```python
@click.group()
def cli() -> None:
    """Main CLI group."""
    pass


cli.add_command(greet)
```

### 3. Register Entry Point in `pyproject.toml`
If the command should be available as a binary executable:
```toml
[project.scripts]
my-command = "project.app:greet"
```

Then synchronize the environment:
```bash
uv sync
```

### 4. Implement Unit Tests
Test the command using Click's `CliRunner` in `tests/test_cli.py` (or `tests/test_app.py`):
```python
from click.testing import CliRunner
from project.app import greet


def test_greet_command():
    runner = CliRunner()
    result = runner.invoke(greet, ["Alice", "--count", "2"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.output
```

### 5. Verify Quality Gates
Run repository verification:

```bash
mise run verify
```

## Boundaries

✅ **Always do:**
- Always provide helpful docstrings and option `help="..."` text for every CLI parameter.
- Always use `click.testing.CliRunner` to test exit codes and output strings.
- Always run `uv sync` after updating `[project.scripts]`.

🚫 **Never do:**
- Never use raw `sys.argv` parsing when Click is available.
- Never write CLI commands without automated test coverage.
