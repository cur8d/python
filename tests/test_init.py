from pathlib import Path

import pytest
from click import UsageError

import scripts.init as init


def test_validate_inputs():
    # Valid inputs should pass without exception
    init._validate_inputs(
        name="my-project",
        description="A cool project",
        author="Alice Smith",
        email="alice@example.com",
        github="alice-smith",
    )

    # Test length validation (>100 characters)
    with pytest.raises(UsageError, match="Invalid name: maximum length is 100 characters"):
        init._validate_inputs("a" * 101, "desc", "author", "email@test.com", "gh")

    # Test non-printable characters validation
    with pytest.raises(UsageError, match="Invalid description: control characters are not allowed"):
        init._validate_inputs("name", "desc\x01", "author", "email@test.com", "gh")

    # Test double quote validation (not allowed in name/author/email/github)
    with pytest.raises(UsageError, match="Invalid author: double quotes are not allowed"):
        init._validate_inputs("name", "desc", 'author"with"quotes', "email@test.com", "gh")

    # Double quotes are allowed in description
    init._validate_inputs("name", 'description with "quotes"', "author", "email@test.com", "gh")

    # Test project name format
    with pytest.raises(UsageError, match="Invalid project name"):
        init._validate_inputs("Invalid_Project_Name!", "desc", "author", "email@test.com", "gh")

    # Test github username format
    with pytest.raises(UsageError, match="Invalid GitHub username"):
        init._validate_inputs("name", "desc", "author", "email@test.com", "invalid_username")

    # Test email format
    with pytest.raises(UsageError, match="Invalid email address"):
        init._validate_inputs("name", "desc", "author", "not-an-email", "gh")


def test_get_git_config(monkeypatch):
    # Clear cache first to ensure a clean state
    monkeypatch.setattr(init, "_git_config_loaded", False)
    monkeypatch.setattr(init, "_git_config_cache", {})

    # Mock subprocess.check_output
    def mock_check_output(args, **kwargs):
        if "config" in args and "--get-regexp" in args:
            return "user.name Bob Jones\nuser.email bob@example.com\ngithub.user bobjones\n"
        raise ValueError("Unexpected command")

    monkeypatch.setattr(init, "check_output", mock_check_output)

    assert init._get_git_config("user.name") == "Bob Jones"
    assert init._get_git_config("user.email") == "bob@example.com"
    assert init._get_git_config("github.user") == "bobjones"

    # Uncached custom key should invoke check_output directly
    monkeypatch.setattr(init, "check_output", lambda args, **kwargs: "custom-value" if "custom.key" in args else "")
    assert init._get_git_config("custom.key") == "custom-value"


def test_get_default_github(monkeypatch):
    # Case 1: valid username in git config
    monkeypatch.setattr(init, "_git_config_loaded", True)
    monkeypatch.setattr(init, "_git_config_cache", {"github.user": "jane-doe"})
    assert init._get_default_github() == "jane-doe"

    # Case 2: invalid username in git config, fallback to remote URL (HTTPS format)
    monkeypatch.setattr(init, "_git_config_cache", {})

    def mock_check_output(args, **kwargs):
        if "remote" in args and "get-url" in args:
            return "https://github.com/some-org/some-repo.git\n"
        raise ValueError("Unexpected command")

    monkeypatch.setattr(init, "check_output", mock_check_output)
    assert init._get_default_github() == "some-org"

    # Case 3: invalid username in git config, fallback to remote URL (SSH format)
    def mock_check_output_ssh(args, **kwargs):
        if "remote" in args and "get-url" in args:
            return "git@github.com:ssh-user/some-repo.git\n"
        raise ValueError("Unexpected")

    monkeypatch.setattr(init, "check_output", mock_check_output_ssh)
    assert init._get_default_github() == "ssh-user"


def test_perform_replacements(tmp_path, monkeypatch):
    # Change current working directory to tmp_path so the script modifies files there
    monkeypatch.chdir(tmp_path)

    # Set up mocked files that would be modified by the script
    docs_ref = tmp_path / "docs" / "reference"
    docs_ref.mkdir(parents=True)
    app_md = docs_ref / "app.md"
    app_md.write_text("::: project.app\nsome other content")

    mkdocs_yml = tmp_path / "mkdocs.yml"
    mkdocs_yml.write_text("repo_name: original/repo\nrepo_url: https://github.com/original/repo\n")

    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text(
        'source = ["project"]\n'
        'app = "project.app:main"\n'
        'name = "project"\n'
        'description = "original description"\n'
        'authors = ["Original Author <email>"]\n'
    )

    docs_readme = tmp_path / "docs" / "README.md"
    docs_readme.parent.mkdir(parents=True, exist_ok=True)
    docs_readme.write_text("# Old Description\nsome doc content")

    github_dir = tmp_path / ".github"
    github_dir.mkdir()
    codeowners = github_dir / "CODEOWNERS"
    codeowners.write_text("@original_owner")

    funding_yml = github_dir / "FUNDING.yml"
    funding_yml.write_text("github: [original_owner]")

    # Run perform replacements
    init._perform_replacements(
        source="my_new_source",
        github="new-github",
        name="my-new-name",
        description='New "escaped" Description',
        author="New Author",
        email="new@example.com",
    )

    # Assertions to verify correct updates
    assert "::: my_new_source.app" in app_md.read_text()
    assert "repo_name: new-github/my-new-name" in mkdocs_yml.read_text()
    assert "repo_url: https://github.com/new-github/my-new-name" in mkdocs_yml.read_text()

    pyproject_content = pyproject_toml.read_text()
    assert 'source = ["my_new_source"]' in pyproject_content
    assert 'app = "my_new_source.app:main"' in pyproject_content
    assert 'name = "my_new_source"' in pyproject_content
    assert 'description = "New \\"escaped\\" Description"' in pyproject_content
    assert 'authors = ["New Author <new@example.com>"]' in pyproject_content

    assert '# New "escaped" Description' in docs_readme.read_text()
    assert "@new-github" in codeowners.read_text()
    assert "github: [new-github]" in funding_yml.read_text()


if __name__ == "__main__":
    import pytest

    pytest.main()
