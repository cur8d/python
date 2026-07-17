import os
import re
import shutil
import subprocess
from pathlib import Path

from click import ClickException, UsageError, command, confirm, echo, option, secho


def _get_git_config(key: str) -> str:
    try:
        return subprocess.check_output(["/usr/bin/git", "config", key], text=True, timeout=5).strip()  # noqa: S603
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def _get_default_github() -> str:
    # Try git config first
    username = _get_git_config("github.user") or _get_git_config("user.name")
    if username and re.match(r"^[a-zA-Z0-9-]+$", username):
        return username

    # Try to extract from remote URL
    try:
        url = subprocess.check_output(  # noqa: S603
            ["/usr/bin/git", "remote", "get-url", "origin"], text=True, timeout=5
        ).strip()
        if "github.com" in url:
            if url.startswith("https"):
                return url.split("/")[-2]
            if url.startswith("git@"):
                return url.split(":")[-1].split("/")[0]
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass

    return ""


def _validate_inputs(name: str, description: str, author: str, email: str, github: str):
    # Validate inputs to prevent configuration injection
    for label, value in [
        ("name", name),
        ("description", description),
        ("author", author),
        ("email", email),
        ("github", github),
    ]:
        if len(value) > 100:
            raise UsageError(f"Invalid {label}: maximum length is 100 characters.")
        if not value.isprintable():
            raise UsageError(f"Invalid {label}: control characters are not allowed.")
        if label != "description" and '"' in value:
            raise UsageError(f"Invalid {label}: double quotes are not allowed.")

    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise UsageError(
            f"Invalid project name '{name}'. Only alphanumeric characters, dashes, and underscores are allowed."
        )

    if not re.match(r"^[a-zA-Z0-9-]+$", github):
        raise UsageError(f"Invalid GitHub username '{github}'. Only alphanumeric characters and dashes are allowed.")

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise UsageError(f"Invalid email address '{email}'.")


def _perform_replacements(source: str, github: str, name: str, description: str, author: str, email: str):
    # Sanitize for TOML double-quoted strings (escape backslashes and double quotes)
    def toml_escape(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    escaped_description = toml_escape(description)
    escaped_author = toml_escape(author)
    escaped_email = toml_escape(email)

    # 1. Update docs/reference/app.md
    path_ref = Path("docs/reference/app.md")
    if path_ref.exists():
        content = path_ref.read_text()
        new_content = re.sub(r"^::: project\.app", lambda _, r=f"::: {source}.app": r, content, flags=re.MULTILINE)
        if new_content != content:
            path_ref.write_text(new_content)
        secho("  Updated docs/reference/app.md ✅", fg="blue")
    else:
        secho("  Warning: File docs/reference/app.md not found, skipping. ⚠️", fg="yellow")

    # 2. Update mkdocs.yml
    path_mkdocs = Path("mkdocs.yml")
    if path_mkdocs.exists():
        content = path_mkdocs.read_text()
        new_content = re.sub(
            r"^repo_name: .*",
            lambda _, r=f"repo_name: {github}/{name}": r,
            content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r"^repo_url: .*",
            lambda _, r=f"repo_url: https://github.com/{github}/{name}": r,
            new_content,
            flags=re.MULTILINE,
        )
        if new_content != content:
            path_mkdocs.write_text(new_content)
        secho("  Updated mkdocs.yml ✅", fg="blue")
    else:
        secho("  Warning: File mkdocs.yml not found, skipping. ⚠️", fg="yellow")

    # 3. Update pyproject.toml
    path_pyproject = Path("pyproject.toml")
    if path_pyproject.exists():
        content = path_pyproject.read_text()
        new_content = re.sub(
            r"^source = \[.*\]",
            lambda _, r=f'source = ["{source}"]': r,
            content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r'^app = "project\.app:main"',
            lambda _, r=f'app = "{source}.app:main"': r,
            new_content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r'^name = ".*"',
            lambda _, r=f'name = "{source}"': r,
            new_content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r'^description = ".*"',
            lambda _, r=f'description = "{escaped_description}"': r,
            new_content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r"^authors = \[.*\]",
            lambda _, r=f'authors = ["{escaped_author} <{escaped_email}>"]': r,
            new_content,
            flags=re.MULTILINE,
        )
        if new_content != content:
            path_pyproject.write_text(new_content)
        secho("  Updated pyproject.toml ✅", fg="blue")
    else:
        secho("  Warning: File pyproject.toml not found, skipping. ⚠️", fg="yellow")

    # 4. Update docs/README.md
    path_readme = Path("docs/README.md")
    if path_readme.exists():
        content = path_readme.read_text()
        new_content = re.sub(r"^# .*", lambda _, r=f"# {description}": r, content, flags=re.MULTILINE)
        if new_content != content:
            path_readme.write_text(new_content)
        secho("  Updated docs/README.md ✅", fg="blue")
    else:
        secho("  Warning: File docs/README.md not found, skipping. ⚠️", fg="yellow")

    # 5. Update .github/CODEOWNERS
    path_owners = Path(".github/CODEOWNERS")
    if path_owners.exists():
        content = path_owners.read_text()
        new_content = re.sub(r"@.*", lambda _, r=f"@{github}": r, content, flags=re.MULTILINE)
        if new_content != content:
            path_owners.write_text(new_content)
        secho("  Updated .github/CODEOWNERS ✅", fg="blue")
    else:
        secho("  Warning: File .github/CODEOWNERS not found, skipping. ⚠️", fg="yellow")

    # 6. Update .github/FUNDING.yml
    path_funding = Path(".github/FUNDING.yml")
    if path_funding.exists():
        content = path_funding.read_text()
        new_content = re.sub(r"^github: \[.*\]", lambda _, r=f"github: [{github}]": r, content, flags=re.MULTILINE)
        if new_content != content:
            path_funding.write_text(new_content)
        secho("  Updated .github/FUNDING.yml ✅", fg="blue")
    else:
        secho("  Warning: File .github/FUNDING.yml not found, skipping. ⚠️", fg="yellow")


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
    _validate_inputs(name, description, author, email, github)

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
        raise ClickException(f"Error: Neither 'project' nor '{source}' directory found.")

    # 2. File modifications
    _perform_replacements(source, github, name, description, author, email)

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
