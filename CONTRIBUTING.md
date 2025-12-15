# Contributing
Contributions are welcome. CRNStudio aims to maintain a small, explicit public API and a high standard of correctness.

## Development setup

Install development dependencies:

pip install -e .[dev]

## Code quality and tests

Before submitting changes, ensure the following checks pass:

ruff format
ruff check
mypy
pytest

Continuous integration enforces these checks on all pull requests.

## Design principles

- Keep abstractions explicit and minimal

- Avoid hidden coupling between modules

- Prefer correctness and auditability over convenience

- Add tests for new functionality and bug fixes