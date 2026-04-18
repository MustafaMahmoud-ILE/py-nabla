# Contributing to Nabla

Thank you for your interest in Nabla! As a LaTeX-first mathematical engine, we aim for absolute precision and ease of use.

## Development Workflow

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. **Install dependencies** in editable mode:
   ```bash
   pip install -e .[dev,plotting,numeric]
   ```
4. **Create a branch** for your feature or bugfix.
5. **Run tests** before submitting:
   ```bash
   pytest
   ```
6. **Submit a Pull Request**.

## Testing Guidelines

We prioritize robustness. If you add a new LaTeX construct, please add:
1. A test case in `tests/fixtures/latex_test_cases.json`.
2. A "stress test" in `tests/test_robustness.py` if the construct is complex or has potential ambiguities.

## Code Style

We use `black` for formatting and `mypy` for type checking. Please ensure your code passes both before submitting.

## Reporting Bugs

Please use the GitHub Issue tracker and include:
1. The LaTeX string that caused the issue.
2. The expected result vs. the actual result.
3. The environment (Python version, OS).
