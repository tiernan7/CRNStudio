# Agent Guidelines

- Use `pytest` to run the test suite. There are no additional flags required.
- Run `ruff check` and `ruff format` to ensure linting and formatting compliance.
- Run `mypy` for static type checking.
- Add concise Google-style docstrings for all public modules, classes, and functions.
- Keep the public API small and explicit by updating `__all__` where appropriate.
- Follow the src/ layout and avoid placing application code outside `src/`.
- Prefer deterministic, easily reproducible tests.
