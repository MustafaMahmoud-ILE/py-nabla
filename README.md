# ∇ py-nabla: Mathematics in the language of thought.

[![PyPI version](https://img.shields.io/pypi/v/py-nabla.svg)](https://pypi.org/project/py-nabla/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/MustafaMahmoud-ILE/py-nabla/actions/workflows/python-test.yml/badge.svg)](https://github.com/MustafaMahmoud-ILE/py-nabla/actions)
[![Documentation](https://img.shields.io/badge/docs-v1.1.0--alpha-green.svg)](https://github.com/MustafaMahmoud-ILE/py-nabla#readme)

**py-nabla** is a production-grade mathematical computing engine that bridges the gap between **LaTeX notation** and **Python execution**. Write math exactly as you think it; execute it with the power of SymPy and NumPy.

---

## 🔥 Why py-nabla?

Translating complex LaTeX equations into nested Python code is brittle, time-consuming, and error-prone. One misplaced parenthesis in a symbolic expression can lead to hours of debugging.

**py-nabla eliminates this friction.**

- **Parse Naturally**: High-fidelity Earley parser for complex LaTeX (vmatrix, cases, summations, mixed partials).
- **Compute Symbolically**: Full integration with SymPy for calculus, algebra, and simplification.
- **Execute Numerically**: Instant vectorization via NumPy for high-performance evaluation.
- **Visualize Beautifully**: Built-in 2D/3D plotting engine with publication-ready aesthetics.
- **Render Professionally**: Bidirectional LaTeX conversion with support for Leibniz, Prime, and Newton (dot) notations.

---

## 🛠️ Installation

```bash
# Core engine
pip install py-nabla

# With plotting support (recommended)
pip install py-nabla[plotting]

# Install all development dependencies
pip install py-nabla[all]
```

---

## ✨ Quickstart: The "Wow" Moment

Differentiate a complex expression, simplify it, and plot it in seconds:

```python
import py_nabla as nb
import numpy as np

# 1. Parse your LaTeX
f = nb.parse(r"\frac{d}{dx} \left( x^2 \sin(x) \right)")

# 2. Compute analytically
print(f"Derivative: {f.simplify()}") 
# Result: 2*x*sin(x) + x**2*cos(x)

# 3. Render back to LaTeX (Leibniz style)
print(f.latex(mode='display'))

# 4. Solve Differential Equations (v1.1.0+)
# Solve y'' + y = 0 natively
eq = nb.parse(r"y'' + y = 0")
print(f"Solution: {eq.dsolve()}") # y(t) = C1*sin(t) + C2*cos(t)

# 5. Plot instantly
nb.plot(f, domain=(-2, 2), title="Differentiated Waveform")
```

---

## 💎 Production Features (v1.1.0-alpha)

### 🧠 Advanced Parser
- **Calculus**: Support for $\int, \iint, \oint$, $\lim_{x \to a}$, $\sum, \prod$, and partial derivatives.
- **Differential/Integral Equations**: Solve ODEs and IDEs using `dsolve()` with a built-in **Laplace Transform** engine. Supports Newton's prime notation ($y', y''$) natively.
- **Linear Algebra**: Matrix environments (`bmatrix`, `pmatrix`, `vmatrix`) and vector notations.
- **Piecewise**: Support for `\begin{cases}` environments.
- **Ambiguity Resolution**: Intelligent splitting of multi-char symbols (e.g., `2weight` $\to 2 \cdot w \cdot e \cdot i \cdot g \cdot h \cdot t$).

### 🪄 Publication Rendering
Beautiful bidirectional conversion with custom styles:
- **Derivative Styles**: Choose between `leibniz` ($\frac{dy}{dx}$), `prime` ($y'$), or `dot` ($\dot{y}$).
- **Multiple Modes**: `inline`, `display`, `equation`, or `align`.

### 📊 Plotting Engine
- **2D Plots**: Multi-function plotting with automatic labeling.
- **3D Plots**: Surface, wireframe, and contour plots for multivariable functions.
- **Parametric**: Plot complex curves like circles, spirals, or Lissajous figures.

---

## 📚 Documentation & Tutorials

- [Getting Started Guide](docs/tutorial/01_getting_started.md)
- [Calculus Cookbook](docs/tutorial/02_calculus.md)
- [Linear Algebra Mastery](docs/tutorial/03_linear_algebra.md)
- [Advanced Plotting](docs/tutorial/04_plotting.md)
- [Differential & Integral Equations](docs/tutorial/05_differential_and_integral_equations.md)

---

## 🤝 Contributing

We welcome contributions from the mathematical and open-source communities! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, and our [Testing Guide](TESTING.md) before submitting code.

## 📄 License

py-nabla is released under the **MIT License**.
