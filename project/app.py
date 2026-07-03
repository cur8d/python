from click import UsageError, command, option, secho, version_option


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
@version_option(None, "-V", "--version")
def main(name: str = "World"):
    """
    Say hello to the given name.

    Args:
      name: the name to be greeted
    """
    name = name.strip() or "World"

    if len(name) > 100:
        raise UsageError(f"Name too long ({len(name)}/100 characters). Please keep it under 100.")
    if any(not c.isprintable() for c in name):
        raise UsageError("Invalid name: control characters are not allowed.")

    secho("Hello ", nl=False)
    secho(name, fg="cyan", bold=True, nl=False)
    secho("! 👋", fg="green", bold=True)


if __name__ == "__main__":
    main()
