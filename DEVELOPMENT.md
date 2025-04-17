# For Developers

## Dependencies

- `Python`: 3.10 or higher
- `poetry`: This project uses Poetry for dependency management.

### Recommended Dependencies

- `make`: Makefile is used for managing tasks.

## Development Setup

```bash
# After cloning the repository
poetry install --group dev
```

## Tests

```bash
poetry run pytest tests
# or
make test
```

## Coding Style

use `black` for formatting and `isort` for import sorting.
use `flake8` for linting and `mypy` for type checking.

```bash
# formatting
poetry run isort src tests && poetry run black src tests
# or
make format

# linting & type checking
poetry run flake8 src tests
poetry run mypy src tests
# or
make check
```

## CI

CI which is configured in [.github/workflows/ci.yml](https://github.com/Seika139/env_loader/actions/workflows/ci.yml) will be triggered on push or pull request to the main branch.

## Git Commit Guidelines

Not yet defined.
