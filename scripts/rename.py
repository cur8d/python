import os
import re
import shutil
import subprocess
from pathlib import Path

from click import ClickException, UsageError, command, confirm, echo, option, secho


def _get_git_config(key: str) -> str:
    try:
        return subprocess.check_output(["/usr/bin/git", "config", key], text=True).strip()  # noqa: S603
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _get_default_github() -> str:
    # Try git config first
    username = _get_git_config("github.user") or _get_git_config("user.name")
    if username and re.match(r"^[a-zA-Z0-9-]+$", username):
        return username

    # Try to extract from remote URL
    try:
        url = subprocess.check_output(  # noqa: S603
            ["/usr/bin/git", "remote", "get-url", "origin"], text=True
        ).strip()
        if "github.com" in url:
            if url.startswith("https"):
                return url.split("/")[-2]
            if url.startswith("git@"):
                return url.split(":")[-1].split("/")[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return ""


@command(context_settings={"help_option_names": ["-h", "--help"]})
@option(
    "--name",
    prompt="Project name",
    default=lambda: Path.cwd().name,
    help="Project new name",
)
@option(
    "--description",
    prompt="Project description",
    default="A Python project",
    help="Project short description",
)
@option(
    "--author",
    prompt="Author name",
    default=lambda: _get_git_config("user.name"),
    help="Author name",
)
@option(
    "--email",
    prompt="Author email",
    default=lambda: _get_git_config("user.email"),
    help="Author email",
)
@option(
    "--github",
    prompt="GitHub username",
    default=_get_default_github,
    help="GitHub username",
)
def main(name: str, description: str, author: str, email: str, github: str):
    # Validate inputs to prevent configuration injection
    for label, value in [
        ("name", name),
        ("description", description),
        ("author", author),
        ("email", email),
        ("github", github),
    ]:
        if len(value) > 100:
            msg = f"Invalid {label}: maximum length is 100 characters."
            raise UsageError(msg)
        if any(not c.isprintable() for c in value):
            msg = f"Invalid {label}: control characters are not allowed."
            raise UsageError(msg)
        if label != "description" and '"' in value:
            msg = f"Invalid {label}: double quotes are not allowed."
            raise UsageError(msg)

    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        msg = f"Invalid project name '{name}'. Only alphanumeric characters, dashes, and underscores are allowed."
        raise UsageError(msg)

    if not re.match(r"^[a-zA-Z0-9-]+$", github):
        msg = f"Invalid GitHub username '{github}'. Only alphanumeric characters and dashes are allowed."
        raise UsageError(msg)

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        msg = f"Invalid email address '{email}'."
        raise UsageError(msg)

    # Sanitize for TOML double-quoted strings (escape backslashes and double quotes)
    def toml_escape(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    description = toml_escape(description)
    author = toml_escape(author)
    email = toml_escape(email)

    source = name.replace("-", "_").lower()

    secho("\nProject Configuration:", bold=True)

    def print_field(label: str, value: str):
        secho(f"  {label:<14}", nl=False, bold=True)
        secho(value, fg="cyan")

    print_field("Name:", name)
    print_field("Source:", source)
    print_field("Description:", description)
    print_field("Author:", f"{author} <{email}>")
    print_field("GitHub:", github)
    echo()

    if not confirm("Do you want to proceed with these settings?", default=True):
        secho("Aborted! ❌", fg="red")
        return

    secho(f"\nInitializing project '{name}'... 🚀", fg="green", bold=True)

    # 1. Rename project directory
    if Path("project").is_dir():
        shutil.move("project", source)
        secho(f"Renamed 'project' directory to '{source}'", fg="blue")
    elif not Path(source).is_dir():
        msg = f"Error: Neither 'project' nor '{source}' directory found."
        raise ClickException(msg)

    # 2. File modifications
    replacements = [
        ("docs/reference/app.md", r"^::: project\.app", f"::: {source}.app"),
        ("mkdocs.yml", r"^repo_name: .*", f"repo_name: {github}/{name}"),
        ("mkdocs.yml", r"^repo_url: .*", f"repo_url: https://github.com/{github}/{name}"),
        ("pyproject.toml", r"^source = \[.*\]", f'source = ["{source}"]'),
        ("pyproject.toml", r'^app = "project\.app:main"', f'app = "{source}.app:main"'),
        (f"project/app.py", r'version\("project"\)  # project-name', f'version("{source}")  # project-name'),
        ("pyproject.toml", r'^name = ".*"', f'name = "{source}"'),
        ("pyproject.toml", r'^description = ".*"', f'description = "{description}"'),
        ("pyproject.toml", r"^authors = \[.*\]", f'authors = [{{name = "{author}", email = "{email}"}}]'),
        ("docs/README.md", r"^# .*", f"# {description}"),
        (".github/CODEOWNERS", r"@.*", f"@{github}"),
        (".github/FUNDING.yml", r"^github: \[.*\]", f"github: [{github}]"),
    ]

    for filepath, pattern, replacement in replacements:
        path = Path(filepath)
        if not path.exists():
            secho(f"  Warning: File {filepath} not found, skipping. ⚠️", fg="yellow")
            continue

        content = path.read_text()
        # Use a lambda for replacement to avoid regex backreference injection
        # Use a default argument to capture the current value of replacement
        new_content = re.sub(pattern, lambda _, r=replacement: r, content, flags=re.MULTILINE)
        path.write_text(new_content)
        secho(f"  Updated {filepath} ✅", fg="blue")

    secho("\nProject initialization complete! ✨", fg="green", bold=True)

    secho("\nNext steps:", bold=True)
    secho("  1. Install dependencies:     ", nl=False)
    secho("mise run install", fg="cyan")
    secho("  2. Run your new app:         ", nl=False)
    secho("mise run app", fg="cyan")
    secho("  3. View documentation:       ", nl=False)
    secho("mise run local-docs", fg="cyan")
    secho("  4. Explore the codebase in:  ", nl=False)
    secho(f"./{source}\n", fg="cyan")


if __name__ == "__main__":
    main()
