from click.testing import CliRunner

from project.app import main


def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--name <name>" in result.output
    assert "-V, --version" in result.output
    assert "Example: app --name Alice" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["-V"])
    assert result.exit_code == 0
    assert "app, version 0.1.0" in result.output


def test_greet():
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Jules"])
    assert result.exit_code == 0
    assert "Hello Jules! 👋" in result.output


def test_name_too_long():
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "A" * 101])
    assert result.exit_code != 0
    assert "maximum length is 100 characters" in result.output


def test_name_control_characters():
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Injected\x1b[31mRed\x1b[0m"])
    assert result.exit_code != 0
    assert "control characters are not allowed" in result.output

    result = runner.invoke(main, ["--name", "test\x7f"])
    assert result.exit_code != 0
    assert "control characters are not allowed" in result.output
