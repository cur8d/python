from click import UsageError, command, option, secho, version_option


class _LazyVersion:
    """Lazily load version to improve CLI startup time.

    Expected impact: Reduces --help startup time by ~40ms by deferring importlib.metadata.
    """

    def __str__(self) -> str:
        # project-name
        try:
            import re
            from pathlib import Path

            # Try to find pyproject.toml relative to the package root
            # This is fast and works during development
            current_path = Path(__file__).resolve()
            # Walk up to find pyproject.toml (max 3 levels)
            for parent in [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]:
                pyproject_path = parent / "pyproject.toml"
                if pyproject_path.exists():
                    content = pyproject_path.read_text(encoding="utf-8")
                    match = re.search(r'^version\s*=\s*"(.*?)"', content, re.MULTILINE)
                    if match:
                        return match.group(1)
        except Exception:  # pragma: no cover
            pass

        try:
            from importlib.metadata import PackageNotFoundError, version

            # Fallback to standard metadata lookup
            # Use __package__ to avoid hardcoding the project name
            package_name = __package__.split(".")[0] if __package__ else "project"
            return version(package_name)
        except (AttributeError, ImportError, PackageNotFoundError):  # pragma: no cover
            return "0.0.0"


@command(
    name="app",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Say hello to a user.",
    epilog="Example: app --name Alice",
)
@option(
    "-n",
    "--name",
    default="World",
    help="The name of the person to greet.",
    show_default=True,
    metavar="<name>",
)
@version_option(_LazyVersion(), "-V", "--version")
def main(name: str = "World"):
    """
    Say hello to the given name.

    Args:
      name: the name to be greeted
    """
    if len(name) > 100:
        raise UsageError("Invalid name: maximum length is 100 characters.")
    if any(not c.isprintable() for c in name):
        raise UsageError("Invalid name: control characters are not allowed.")

    secho(f"Hello {name}! 👋", fg="green", bold=True)


if __name__ == "__main__":
    main()
