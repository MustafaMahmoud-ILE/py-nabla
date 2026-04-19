## 🎯 Comprehensive QA & Test Suite Audit Required

We need a thorough and detailed test report for `py-nabla` v1.0.1 to ensure robust production stability.

### 📋 Objective

1. **Current Test Suite Inventory:**
   Please provide a breakdown of all current test files (e.g., `test_parser.py`, `test_expression.py`), including the number of tests in each and a brief summary of what they cover (edge cases, performance, robustness, etc.).

2. **Full Test Execution & Coverage:**
   Execute the full test suite with coverage reporting enabled:
   ```bash
   pytest tests/ -v --tb=short --cov=py_nabla --cov-report=term-missing
   ```

3. **Results Reporting:**
   Present the results in a markdown table detailing:
   * Test File
   * Total Tests
   * Passed ✅ / Failed ❌
   * Notes / Execution Time

### 🔍 Specific Areas to Validate

Please ensure the following critical areas are covered, adding tests if they are missing:
- [ ] **Edge Cases:** Empty strings, bizarre Unicode characters, missing brackets.
- [ ] **Performance:** Time taken to parse and simplify deeply nested or highly complex expressions.
- [ ] **NumPy Integration:** Verification that vectorized numerical evaluation with NumPy arrays functions flawlessly.
- [ ] **Error Handling:** Ensure `NablaParseError` messages are descriptive and include accurate visual pointers.
- [ ] **Operator Overloading:** Validate programmatic operations like `f + g`, `f * 2`, and specifically equality checking (`==`).
- [ ] **Multi-Variable Calculus:** Test expressions involving multiple variables natively (e.g., `x, y, z`).
- [ ] **Compatibility:** Ensure stable execution across Python 3.9, 3.10, 3.11, and 3.12.

### 🐛 Known Issues to Address Immediately (Priority 1)

* **Logical Equality (`__eq__`) Bug:**
  Currently, `f == g` returns an `Expression` containing a SymPy `Eq` object instead of a boolean value. This breaks standard assertion checks and conditional logic. 
  *Severity:* 🔴 High

### 📊 Expected Deliverables
A comprehensive markdown report detailing the overall statistics (Total, Passed, Failed, Code Coverage %), a prioritized list of discovered issues, and a list of the 5 slowest tests using `--durations=5`. 

Thank you! 🙏
