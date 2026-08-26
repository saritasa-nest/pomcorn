# Developing on local PC

[How to contribute](contributing.md)

## Setup virtual environment

We use [uv](https://docs.astral.sh/uv/) to manage the dependencies.

To set up venv you would need to run `sync` command:

```bash
uv sync --all-packages --all-groups --all-extras
```

To activate your `virtualenv`

```bash
source .venv/bin/activate
```

Init project

```bash
inv project.init
```

## Style checks

!!! note
    For common actions in the project used [invoke](https://pypi.org/project/invoke/).

We use `pre-commit` for quality control.
To run checks:

```bash
inv pre-commit.run-hooks
```

## Local Documentation

To build local documentation, use:

```bash
inv docs.build
```

To serve built documentation on localhost, use:

```bash
inv docs.serve
```
