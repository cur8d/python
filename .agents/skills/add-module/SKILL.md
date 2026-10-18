---
name: add-module
description: Scaffolds a new domain service, model, or utility module adhering to cur8d standards with strict type annotations, PEP 257 docstrings, and comprehensive pytest tests. Use whenever the user asks to add, create, or implement a new Python module, class, or service.
category: coding
tags: [python, uv, pyright, pytest, cur8d]
---

# Add Module to cur8d/python Project

This skill guides you through scaffolding a new Python module or domain service within the `project/` directory, adhering to `pyright` strict typing, Google/PEP 257 docstrings, and `pytest` testing standards.

## Prerequisites

- Python 3.12+ and `uv` installed
- `mise` installed

## Workflow

### 1. Determine Module Name & Location
Identify the module purpose and create the target source file:
- For simple modules: `project/<module_name>.py`
- For complex packages: `project/<package_name>/__init__.py` and `project/<package_name>/service.py`

### 2. Implement the Module
Follow cur8d Python conventions:
- **Strict Typing**: Provide full type hints on all function parameters and return types (`pyright` compliant). Avoid `Any` where possible.
- **Docstrings**: Document classes and public functions following Google/PEP 257 docstring style:
  ```python
  """Module summary description.

  Detailed explanation if applicable.
  """


  def process_data(payload: dict[str, str], count: int = 1) -> list[str]:
      """Process a data dictionary and return formatted strings.

      Args:
          payload: Key-value dictionary containing input records.
          count: Repetition multiplier.

      Returns:
          A list of processed string outputs.

      Raises:
          ValueError: If payload is empty.
      """
      if not payload:
          raise ValueError("Payload must not be empty")
      return [f"{k}={v}" for k, v in payload.items()] * count
  ```

### 3. Implement Unit Tests
Create matching test file under `tests/test_<module_name>.py`:
- Use `pytest` style test functions (`def test_<scenario>():`).
- Cover happy path, edge cases (empty collections, boundary limits), and error conditions (`pytest.raises`).
- Ensure test file ends with:
  ```python
  if __name__ == "__main__":
      pytest.main()
  ```

### 4. Verify Quality Gates
Run repository verification:

```bash
mise run verify
```

Fix any `pyright` type issues or `ruff` formatting warnings.

## Boundaries

✅ **Always do:**
- Always add comprehensive type hints for all function signatures.
- Always include matching unit tests in `tests/` covering nominal, edge, and error cases.
- Always run `mise run verify` before committing.

🚫 **Never do:**
- Never use `unittest.TestCase` classes; use native pytest test functions.
- Never suppress pyright or ruff checks without explicit justification.
