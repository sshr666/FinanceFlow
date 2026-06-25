# Contributing to FinanceFlow

Thank you for considering contributing to FinanceFlow! We welcome contributions of all kinds: bug fixes, features, documentation, and more.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Conventions](#commit-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project is committed to providing a welcoming and inclusive experience for everyone. Be respectful, constructive, and considerate in all interactions.

## Getting Started

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://code.swecha.org/your-username/FinanceFlow.git
   cd FinanceFlow
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://code.swecha.org/shreya_sengupta/FinanceFlow.git
   ```

## Development Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov pre-commit ruff mypy bandit vulture pip-audit

# Configure environment
cp .env.example .env

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Run the app to verify
streamlit run app.py
```

## Project Structure

```
finance-flow/
├── app.py                 # Streamlit entry point
├── pages/                 # UI pages (dashboard, transactions, analytics, etc.)
├── database/              # SQLAlchemy models, CRUD, connection
├── analytics/             # Metrics, charts, insights logic
├── utils/                 # Helpers, validators, empty states
├── config/                # Environment config, styling, categories
├── tests/                 # pytest test suite
└── ...
```

## Coding Standards

- **Python**: 3.11+
- **Formatting & Linting**: [Ruff](https://docs.astral.sh/ruff) is used for both. Run before committing:
  ```bash
  ruff check . --fix
  ruff format .
  ```
- **Type Checking**: [mypy](https://mypy-lang.org) with `--ignore-missing-imports`:
  ```bash
  mypy analytics/ config/ database/ pages/ utils/ app.py --ignore-missing-imports
  ```
- **Pre-commit**: All hooks defined in `.pre-commit-config.yaml` run automatically on commit.
- **Naming**: Follow PEP 8 — `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants.
- **Imports**: Group in order — standard library, third-party, local. Ruff enforces this.

## Commit Conventions

This project uses [Conventional Commits](https://www.conventionalcommits.org) with [commitizen](https://commitizen-tools.github.io/commitizen) enforcement.

Format: `<type>(<scope>): <description>`

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`

**Examples**:
```
feat(transactions): add CSV export
fix(budgets): correct overspending calculation
docs(readme): update installation steps
test(analytics): add coverage for monthly trends
```

A `.gitmessage` template is provided — you can configure git to use it:
```bash
git config commit.template .gitmessage
```

## Pull Request Process

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes, keeping them focused and atomic.
3. Run all checks locally:
   ```bash
   pre-commit run --all-files
   python -m pytest tests/ -v
   ```
4. Push your branch and open a merge request targeting `main`.
5. Ensure the CI pipeline passes (lint, typecheck, test, security, quality stages).
6. Request review from a maintainer.

## Testing

All tests are in the `tests/` directory and use pytest.

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest tests/test_transactions.py -v
```

When adding new functionality, include corresponding tests. Tests follow the pattern `test_<module>.py` and use the fixtures defined in `tests/conftest.py`.

## Reporting Issues

- Use the issue tracker on [Codeberg](https://code.swecha.org/shreya_sengupta/FinanceFlow/issues).
- Search existing issues before opening a new one.
- Provide a clear title, steps to reproduce, expected vs actual behavior, and environment details (OS, Python version).
- Include screenshots or error logs when applicable.
- Label the issue appropriately (bug, enhancement, question, etc.).
