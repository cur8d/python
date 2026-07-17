from click.testing import CliRunner
from pytest import main

from project.app import main as app_main


def test_help():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--help"])
    assert result.exit_code == 0
    assert "--name <name>" in result.output
    assert "-V, --version" in result.output
    assert "Example: app --name Alice" in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(app_main, ["-V"])
    assert result.exit_code == 0
    assert "app, version 0.1.0" in result.output


def test_greet():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--name", "Jules"])
    assert result.exit_code == 0
    assert "Hello Jules! 👋" in result.output


def test_name_too_long():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--name", "A" * 101])
    assert result.exit_code != 0
    assert "maximum length is 100 characters" in result.output


def test_name_control_characters():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--name", "Injected\x1b[31mRed\x1b[0m"])
    assert result.exit_code != 0
    assert "control characters are not allowed" in result.output

    result = runner.invoke(app_main, ["--name", "test\x7f"])
    assert result.exit_code != 0
    assert "control characters are not allowed" in result.output


def test_greet_trimming():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--name", "   Jules   "])
    assert result.exit_code == 0
    assert "Hello Jules! 👋" in result.output


def test_greet_empty_fallback():
    runner = CliRunner()
    result = runner.invoke(app_main, ["--name", ""])
    assert result.exit_code == 0
    assert "Hello World! 👋" in result.output

    result = runner.invoke(app_main, ["--name", "   "])
    assert result.exit_code == 0
    assert "Hello World! 👋" in result.output


if __name__ == "__main__":
    main()
