# Documentation Architecture - Project Nabla 📚

This document outlines the blueprint for Nabla's official documentation. We recommend using **MkDocs** with the **Material for MkDocs** theme for its speed, searchability, and premium aesthetic.

## 🛠️ Technology Stack
*   **Documentation Engine**: [MkDocs](https://www.mkdocs.org/)
*   **Theme**: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
*   **API Reference**: [mkdocstrings](https://mkdocstrings.github.io/) with the Python handler.
*   **Math Rendering**: [MathJax](https://www.mathjax.org/) or [KaTeX](https://katex.org/).
*   **Diagrams**: [Mermaid.js](https://mermaid.js.org/).

---

## 🏗️ Site Structure (`mkdocs.yml`)

```yaml
site_name: Nabla
theme:
  name: material
  palette:
    primary: teal
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - content.code.copy
    - search.highlight

nav:
  - 🏠 Home: index.md
  - 🏁 Getting Started:
      - Installation: getting-started/installation.md
      - 5-Minute Tutorial: getting-started/tutorial.md
      - Basic Concepts: getting-started/concepts.md
  - 📖 User Guide:
      - LaTeX Support Matrix: guide/latex-support.md
      - Symbolic Manipulation: guide/symbolic.md
      - Numerical Evaluation: guide/numerical.md
      - Calculus & Optimization: guide/calculus.md
      - Integration with NumPy: guide/numpy.md
      - Visualization: guide/plotting.md
  - 🛠️ Developer Guide:
      - Architecture Overview: dev/architecture.md
      - Extending the Grammar: dev/grammar.md
      - Contributing: dev/contributing.md
  - 📝 API Reference:
      - Core Expression: api/expression.md
      - Parser Engine: api/parser.md
      - Plotting: api/plotting.md
  - 🗞️ Blog:
      - Announcing v0.1.0-alpha: blog/v0.1.0-alpha-announcement.md
  - 🆘 Help:
      - Troubleshooting: help/troubleshooting.md
      - FAQs: help/faq.md
```

---

## 🗺️ Content Roadmap

### 1. Getting Started
*   **Tutorial**: A "Hello World" of math. Parse `x^2 + 2x + 1`, simplify it to `(x+1)^2`, and plot it.
*   **Concepts**: Explain the relationship between the `LaTeXPreprocessor`, `Lark Parser`, and `SymPy`.

### 2. User Guide Highlights
*   **LaTeX Support Matrix**: A searchable table of all supported LaTeX commands (e.g., `\frac`, `\sqrt`, `\int`).
*   **Symbolic Power**: Visualizing simplification steps using Nabla's `simplify()` method.
*   **Calculus Section**: Detailed examples of multi-variable differentiation and definite vs. indefinite integrals.

### 3. Developer Guide
*   **The Earley Parser**: Deep dive into `grammar.lark`. How the parser handles operator precedence and whitespace.
*   **Transforming AST**: Explaining the `LaTeXTransformer` logic for converting Lark nodes into SymPy objects.

### 4. API Reference
*   Automated extraction of docstrings from:
    *   `nabla.core.expression.Expression`
    *   `nabla.parser.parser.LaTeXParser`
    *   `nabla.plotting.plotter.plot`

---

## 🎨 Design Aesthetics
*   **Dark Mode Support**: Essential for developers.
*   **Mathematical Proofs**: Use HSL tailored colors for highlight boxes (Admonitions).
*   **Interactive Examples**: Integration with [Pyodide](https://pyodide.org/) for running Nabla directly in the browser.

---

## 📦 Deployment Plan (CI/CD)
*   **GitHub Actions**: Automate documentation building on every push to `main`.
*   **Hosting**: Deploy to [GitHub Pages](https://pages.github.com/) or [Vercel](https://vercel.com/).
*   **Versioned Docs**: Use [mike](https://github.com/jimporter/mike) to support multiple version documentations (e.g., `v0.1.0` vs `latest`).
