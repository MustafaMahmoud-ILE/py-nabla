# Testing Guide for py-nabla ∇

This document outlines the official testing procedures and architecture for the `py-nabla` project. Maintaining a pristine success rate on these tests is **mandatory** before merging any new code or tagging a release.

## 🚀 Quick Start

To run the entire test suite including coverage reporting:
```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run the complete suite
pytest tests/ -v --tb=short --cov=py_nabla --cov-report=term-missing
```

## 📂 Test Suite Architecture

Our testing framework relies on `pytest` and is divided into several specialized domains:

### 1. Unit Tests (`tests/unit/`)
The foundation of the project. Every core function must be tested here in isolation.
*   `test_expression.py`: Validates the `Expression` class API (`diff`, `integrate`, `solve`, `evaluate`, algebra, limits).
*   `test_parser.py`: Ensures the Lark grammar and SymPy transformer convert LaTeX strings correctly.

### 2. Robustness Tests (`tests/test_robustness.py`)
Validates the resilience of the engine against:
*   Bizarre or multi-layered nesting (e.g., radicals inside fractions).
*   Missing brackets and implicit LaTeX shortcuts (`\frac12`).
*   Empty strings and malformed inputs (ensuring a descriptive `NablaParseError` is raised).
*   Handling of non-mathematical Unicode characters and emojis.

### 3. Performance Tests (`tests/integration/test_performance.py`)
Ensures the engine meets response time SLAs.
*   **Vectorization Throughput**: Evaluates million-point arrays under 0.5s.
*   **Parser Speed**: Ensures the Earley parser handles standard equations swiftly.
*   **Memory Bounding**: Verifies the creation of large expressions doesn't leak memory.

### 4. Extreme QA & Stress Tests
We have custom scripts designed to push the library to its limits:
*   `tests/stress_test.py`: Fires "Boss Level" extreme mathematical formulas at the engine (nested matrices, double summations, absolute mixed partials).
*   `tests/final_qa.py`: Validates Python operator overloading (`+`, `-`, `*`, `==`) behaves correctly natively, checks the accuracy of Visual Error Pointers, and verifies package installation integrity.

### 5. Documentation Verification (`tests/verify_tutorials.py`)
Ensures that **every code snippet** shown in the `docs/tutorial/` Markdown files actually works and evaluates correctly against the live codebase.

## 🛠️ Adding New Tests

When contributing a new feature or fixing a bug:

1.  **Bug Fixes**: Reproduce the bug in a new test function inside `tests/test_robustness.py` or the appropriate unit file. Name it `test_bug_description`.
2.  **New Features**: Provide comprehensive unit test coverage.
3.  **Edge Cases**: Always consider testing inputs that are `0`, negative, infinity, or empty strings.
4.  **Operator Overloading**: Any additions to `Expression` operator methods must pass the `final_qa.py` checks. Ensure you test equality (`__eq__`) to maintain boolean resolution.

## 🛑 Testing Criteria for Production Release

Before any new version is released:
1.  All Pytest suites must pass (`100%`).
2.  Code coverage (`--cov`) must maintain its current threshold (or improve).
3.  The Stress Test (`python tests/stress_test.py`) must pass flawlessly.
4.  The QA Blitz (`python tests/final_qa.py`) must pass without exceptions.

---
*“A mathematical engine is only as strong as its weakest edge case.”*
