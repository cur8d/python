# Python Project Template
![Python](https://img.shields.io/badge/python-3.12+-3776AB.svg?logo=python&style=flat-square)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg?logo=ruff&style=flat-square)](https://docs.astral.sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](/LICENSE)

A Python project template that comes out of the box with configuration for:

- Packaging and dependency management using [uv](https://docs.astral.sh/uv)
- Development environment and task management using [mise](https://mise.jdx.dev)
- Command Line Interface (CLI) using [click](https://click.palletsprojects.com)
- Testing using [pytest](https://pytest.org)
- Code coverage using [coverage](https://coverage.readthedocs.io)
- Fomatting, import sorting, and linting using [ruff](https://docs.astral.sh/ruff) 
- Type checking using [pyright](https://microsoft.github.io/pyright)
- Pre-commit validations using [pre-commit](https://pre-commit.com)
- Workflow automation using [GitHub Actions](https://github.com/features/actions)
- Automated dependency update using [Dependabot](https://docs.github.com/en/code-security/dependabot)
- Dockerized development environment using [Dev containers](https://code.visualstudio.com/docs/devcontainers/containers)
- Automatic documentation from code using [mkdocs](https://www.mkdocs.org) and [mkdocstrings](https://mkdocstrings.github.io)
- Documentation auto-deployment to [GiHub Pages](https://pages.github.com)
- App container using [Docker](https://docker.com)


### GitHub files
The repository also comes pre-loaded with these GitHub files:

- Pull request template
- Issue templates
    + Bug report
    + Feature request
    + Question
- Contributing guidelines
- Funding file
- Code owners
- MIT License

## How to use
Click this button to create a new repository for your project, then clone the new repository. Enjoy!

[![Use this template]( https://img.shields.io/badge/Use%20this%20template-238636?style=for-the-badge)](https://github.com/amrabed/python/generate)

### Initialize the project
After cloning the repository, initialize the project by running:
```bash
mise run project
```
The script will interactively prompt you for the following details, with smart defaults based on your environment:

Parameter | Description
--- | ---
`name` | Project new name (defaults to current directory name)
`description` | Project short description
`author` | Author name (defaults to `git config user.name`)
`email`| Author email (defaults to `git config user.email`)
`github`| GitHub username (for GitHub funding)

You can also pass these as flags:
```bash
mise run project --name "my-project" --description "A cool project" --author "Alice" --email "alice@example.com" --github "alice"
```


## Prerequisites
### Dev container
- Docker

### Local environment
- [mise](https://mise.jdx.dev)

## Setup

### Install / Update dependencies
To install the project dependencies, run:
```bash
mise run install
```

To update the project dependencies, run:
```bash
mise run update
```

### Install pre-commit hooks
To install the pre-commit hooks for the project to format and lint your code automatically before commiting, run: 
```bash
mise run precommit
```

### Activate virtual environment
Mise automatically creates and activates the virtual environment if you have `mise activate` set up in your shell. Otherwise, you can run tasks using `mise run <task>` or commands using `mise exec -- <command>`.

### Format and Lint code
To format and lint project code, run:
```bash
mise run lint
```

### Run tests with coverage
To run the unit tests defined under the [tests](../tests/) folder and show coverage report, run:
```bash
mise run test
```

## Running the project
A mise task, with the name `app`, is defined in the [mise.toml](../mise.toml) file, to let you to run the project.

### Local / Dev container
Try running `mise run app -- -h` or `mise run app -- --help` to get the help message of your app:
```bash
Usage: app [OPTIONS]

  Say hello to a user.

Options:
  -n, --name <name>  The name of the person to greet.  [default: World]
  -V, --version      Show the version and exit.
  -h, --help         Show this message and exit.

  Example: app --name Alice
```

### Docker
To run in a Docker container, use:
```bash
docker compose run app -h
```

## Generating documentation
To generate and publish the project documentation to GitHub pages, run:
```bash
mise run docs
```
That pushes the new documentation to the gh-pages branch. 
Make sure GitHub Pages is enableed in your repository settings and using the gh-pages branch for the documentation to be publicly available.

### Local
To serve the documentation on a local server, run:
```bash
mise run local-docs
```

## Project Structure

```
├── .devcontainer                   # Dev container folder
│   ├── devcontainer.json           # Dev container configuration
│   └── Dockerfile                  # Dev container Dockerfile
├── .github                         # Github folder
│   ├── dependabot.yaml             # Dependabot configuration
│   ├── CODEOWNERS                  # Code owners
│   ├── FUNDING.md                  # GitHub funding
│   ├── PULL_REQUEST_TEMPLATE.md    # Pull request template
│   ├── ISSUE_TEMPLATE              # Issue templates
│   │   ├── bug.md                  # Bug report template
│   │   ├── feature.md              # Feature request template
│   │   └── question.md             # Question template
│   └── workflows                   # Github Actions Workflows
│       ├── check.yml               # Workflow to validate code on push
│       └── docs.yml                # Woukflow to publish documentation
├── .gitignore                      # Git-ignored file list
├── .pre-commit-config.yaml         # Pre-commit configuration file
├── .vscode                         # VS code folder
│   └── settings.json               # VS code settings
├── .dockerignore                   # Docker-ignored file list
├── compose.yml                     # Docker-compose file
├── Dockerfile                      # App container Dockerfile
├── LICENSE                         # Project license
├── mise.toml                       # Mise configuration and tasks
├── pyproject.toml                  # Configuration file for different tools
├── docs                            # Documentaion folder
│   ├── mkdocs.yml                  # mkdocs configuration file
│   ├── README.md                   # Read-me file & Documentation home page
│   ├── CONTRIBUTING.md             # Contributing guidelines
│   └── reference                   # Reference section
│       └── app.md                  # App reference page
├── project                         # Main project folder
│   ├── __init__.py                 # Init file of the main package
│   └── app.py                      # Main Python file of the project
└── tests                           # Test folder
    ├── __init__.py                 # Init file fo the test package
    ├── conftest.py                 # Pytest configuration, and fixtures, and hooks
    └── test_app.py                 # Sample test file
```