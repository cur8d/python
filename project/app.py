from click import UsageError, command, option, secho, version_option


class _LazyVersion:
    """Lazy version loader to avoid overhead and handle missing metadata."""

    def __str__(self) -> str:
        import re
        from importlib.metadata import PackageNotFoundError, version
        from pathlib import Path

        # Try pyproject.toml first (dev/script run)
        pyproject = Path(__file__).parent.parent / "pyproject.toml"
        if pyproject.exists():
            with pyproject.open(encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'^version\s*=\s*"(.*)"', content, re.MULTILINE)
                if match:
                    return match.group(1)

        # Fallback to importlib.metadata (installed package)
        try:
            return version("project")  # project-name
        except PackageNotFoundError:
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
        msg = "Invalid name: maximum length is 100 characters."
        raise UsageError(msg)
    if any(not c.isprintable() for c in name):
        msg = "Invalid name: control characters are not allowed."
        raise UsageError(msg)

    secho(f"Hello {name}! 👋", fg="green", bold=True)


if __name__ == "__main__":
    main()
