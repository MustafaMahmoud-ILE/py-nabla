# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-18

### Added
- **Parser Evolution**: Support for summations, products, limits (including one-sided), and piecewise (`cases`) environments.
- **Calculus Mastery**: Added mixed partial derivatives, Taylor series expansion, and definite/indefinite integration.
- **Linear Algebra**: Comprehensive support for matrix environments (`bmatrix`, `pmatrix`, `vmatrix`, `Bmatrix`).
- **Nabla Operators**: Implementation of gradient, divergence, curl, and laplacian notation.
- **Rendering Engine**: New `NablaLatexPrinter` with support for Leibniz, Prime, and Dot notation.
- **Plotting Module**: Added `plot` (2D), `plot3d` (surfaces/contours), and `plot_parametric`.
- **Expression API**: New methods `solve()`, `evaluate()` (with implicit NumPy vectorization), `lambdify()`, `expand()`, `factor()`, `simplify()`.
- **Developer Tools**: Visual syntax error pointers in `NablaParseError`.

### Changed
- **Renamed Package**: Migrated from `nabla` to `py-nabla` to avoid PyPI collisions.
- **Project Structure**: Refactored into specialized modules: `core`, `parser`, `rendering`, `plotting`, `numeric`.
- **Licensing**: Standardized as MIT License.

## [0.1.0-alpha] - 2026-04-18

### Added
- Initial alpha release on TestPyPI.
- Core Earley parser with basic LaTeX support (fractions, powers, basic trig).
- Basic SymPy integration.
- GitHub Actions CI/CD pipeline.
