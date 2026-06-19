from click import UsageError, command, option, secho, version_option


class _LazyVersion:
    """Lazily retrieves the version from pyproject.toml or package metadata.

    This class avoids the overhead of importing `importlib.metadata`, `re`, or `pathlib`
    on the standard execution path, only performing the lookup when the version is
    actually requested.
    """

    def __init__(self):
        self._version = None

    def __str__(self) -> str:
        if self._version is None:
            import os
            import re

            # 1. Try to get version from pyproject.toml (for development/script runs)
            # This is faster than importlib.metadata and avoids RuntimeError in script mode
            try:
                # project/app.py -> pyproject.toml is two levels up
                root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                pyproject_path = os.path.join(root_dir, "pyproject.toml")
                with open(pyproject_path, encoding="utf-8") as f:
                    content = f.read()
                match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
                if match:
                    self._version = match.group(1)
            except Exception:  # noqa: S110
                pass

            # 2. Fallback to metadata (for installed package)
            if not self._version:
                try:
                    from importlib import metadata

                    self._version = metadata.version("project")
                except Exception:
                    self._version = "0.0.0"

        return self._version


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
    if any(c < " " for c in name):
        raise UsageError("Invalid name: control characters are not allowed.")

    secho(f"Hello {name}! 👋", fg="green", bold=True)


if __name__ == "__main__":
    main()
