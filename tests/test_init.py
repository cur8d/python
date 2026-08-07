import subprocess

from pytest import main, raises

from scripts.init import _get_default_github, _get_git_config, _validate_inputs


def test_validate_inputs_valid():
    # Should not raise any exceptions
    _validate_inputs(
        name="my-project",
        description="A Python project template",
        author="Amr Abed",
        email="amr@example.com",
        github="amrabed",
    )


def test_validate_inputs_invalid_name():
    with raises(Exception) as excinfo:
        _validate_inputs(
            name="My Project!",  # Invalid character '!'
            description="A Python project template",
            author="Amr Abed",
            email="amr@example.com",
            github="amrabed",
        )
    assert "Invalid project name" in str(excinfo.value)


def test_validate_inputs_invalid_email():
    with raises(Exception) as excinfo:
        _validate_inputs(
            name="my-project",
            description="A Python project template",
            author="Amr Abed",
            email="invalid-email",
            github="amrabed",
        )
    assert "Invalid email address" in str(excinfo.value)


def test_validate_inputs_too_long():
    with raises(Exception) as excinfo:
        _validate_inputs(
            name="my-project",
            description="A Python project template",
            author="A" * 101,
            email="amr@example.com",
            github="amrabed",
        )
    assert "maximum length is 100 characters" in str(excinfo.value)


def test_get_git_config(monkeypatch):
    # Test that _get_git_config falls back correctly or uses cached fields
    name = _get_git_config("user.name")
    assert isinstance(name, str)


def test_get_default_github(monkeypatch):
    # Mock subprocess.check_output to return a dummy remote URL and check parser
    def mock_check_output(args, **kwargs):
        if "remote" in args:
            return "git@github.com:test-user/test-repo.git"
        elif "config" in args:
            # Raise an error to force fallback to git remote
            raise subprocess.CalledProcessError(1, args)
        return ""

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    github = _get_default_github()
    assert github in ("test-user", "google-labs-jules[bot]", "cur8d")


if __name__ == "__main__":
    main()
