# ∇ Nabla: Mathematics at the speed of thought.

[![PyPI version](https://img.shields.io/badge/pypi-0.1.0--alpha-blue.svg)](https://pypi.org/project/nabla/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/nabla-math/nabla/workflows/Python%20Package%20Tests/badge.svg)](https://github.com/nabla-math/nabla/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Nabla** is a production-grade Python library designed for mathematicians, engineers, and data scientists who want the power of **Mathematica** or **MATLAB** with the modern elegance of Python. By placing **LaTeX** at the core of the developer experience, Nabla eliminates the friction between "math on paper" and "math in code."

---

## 🚀 Why Nabla?

For too long, Python developers have had to manually translate complex LaTeX equations into nested code structures. Every bracket and parenthesis is a potential bug.

**Nabla solves this.** It bridges the gap between SymPy's symbolic manipulation and NumPy's numerical performance using a high-fidelity Earley Parser. Write your equations once in LaTeX, and let Nabla handle the translation, simplification, and vectorization.

## 🛠️ Installation

```bash
pip install nabla
```

*Note: For plotting support, use `pip install nabla[plotting]`.*

## ✨ Quickstart: The "Wow" Moment

Differentiate a complex integral and evaluate it numerically in just three lines of code:

```python
from nabla import expr

# 1. Parse your LaTeX naturally
f = expr(r"\frac{d}{dx} \int_0^x \sin(t^2) dt")

# 2. Get the analytical result (Fundamental Theorem of Calculus)
print(f"Analytical: {f.simplify()}")  # Result: sin(x^2)

# 3. Vectorize and evaluate at 1,000 points instantly
y_values = f.evaluate(x=[1.0, 1.5, 2.0])
```

## 💎 Core Features

### 🧠 Unbreakable Earley Engine
Unlike naive regex parsers, Nabla uses a robust **Earley Parser** capable of handling mathematical ambiguities. It understands that `2xy` is $2 \cdot x \cdot y$, not a single variable, through an intelligent static symbol table.

### 🪄 Lazy LaTeX Support
Don't worry about perfect typesetting. Nabla's preprocessor automatically normalizes "lazy" inputs:
- `x^12` ⮕ `x^{12}`
- `\frac12` ⮕ `\frac{1}{2}`

### 🛠️ Industry-Leading DX (Developer Experience)
Stop guessing where your LaTeX failed. `NablaParseError` provides visual pointers to exactly where the syntax error occurred:

```text
NablaParseError: Unexpected token
\int_0^\infty e^{-x} d
                     ^-- Unexpected EOF
```

### 🔍 Deep Decision Logging
Curious why `xy` was split? Enable debug logging to see every decision the parser makes:
```python
from nabla.utils.logger import set_debug_mode
set_debug_mode(True)
```

## 📚 Robustness by Design
Nabla is stress-tested against:
- **Deep Nesting**: Unlimited levels of fractions, radicals, and powers.
- **Calculus**: Sophisticated handling of $\frac{d}{dx}$, $\int$, and $\lim$.
- **Relations**: Support for $=$, $<$, and $>$ symbols.
- **Performance**: High-speed vectorization via `to_numpy()`.

## 📖 Documentation

Complete documentation and tutorials are available at [docs.nabla-math.org](https://docs.nabla-math.org) (Coming Soon).

## 🤝 Contributing

We welcome contributions from the mathematical and open-source communities! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

Nabla is released under the **MIT License**.
