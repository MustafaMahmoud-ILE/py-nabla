"""
py-nabla: Mathematical Computing in the Language of Thought.

A Python library for symbolic and numerical mathematics with a LaTeX-first
interface, powered by SymPy and NumPy.

Quick start::

    import py_nabla as nb

    f = nb.parse(r"\\frac{d}{dx}(x^2 + \\sin(x))")
    print(f.simplify())        # 2*x + cos(x)
    print(f.latex())           # $2 x + \\cos{\\left(x \\right)}$
    print(f.evaluate(x=1.0))   # 2.5403...
"""

__version__ = "1.0.1"
__author__ = "Nabla Team"
__email__ = "info@nabla-math.org"
__license__ = "MIT"
__url__ = "https://github.com/MustafaMahmoud-ILE/py-nabla"

# ── Core engine ──────────────────────────────────────────────────────────────
from .parser.parser import LaTeXParser
from .core.expression import Expression
from .core.expression import Expression as NablaExpression  # backwards compat alias

_default_parser = LaTeXParser()


def parse(latex_str: str) -> Expression:
    """
    Parse a LaTeX mathematical expression into a py-nabla Expression.

    This is the main entry point for the library.

    Args:
        latex_str: A LaTeX mathematical expression as a string.

    Returns:
        An :class:`~py_nabla.core.expression.Expression` object.

    Raises:
        :class:`~py_nabla.core.exceptions.NablaParseError`: If the input
            cannot be parsed.

    Examples:
        >>> import py_nabla as nb
        >>> f = nb.parse(r"x^2 + 1")
        >>> f.diff('x')
        Expression(2*x)
        >>> f.evaluate(x=3)
        10.0
    """
    sympy_expr = _default_parser.parse(latex_str)
    return Expression(sympy_expr, _latex_source=latex_str)


# Alias for backwards compatibility
expr = parse

from sympy import symbols  # re-exported for convenience  # noqa: E402

# ── Rendering ─────────────────────────────────────────────────────────────────
from .rendering import render_latex  # noqa: E402

# ── Plotting (optional) ───────────────────────────────────────────────────────
try:
    from .plotting import plot, plot3d, plot_parametric
    _PLOTTING_AVAILABLE = True
except ImportError:
    _PLOTTING_AVAILABLE = False

    def _no_plot(*args, **kwargs):
        raise ImportError(
            "Plotting requires matplotlib.\n"
            "Install it with:  pip install py-nabla[plotting]\n"
            "or:               pip install matplotlib"
        )

    plot = plot3d = plot_parametric = _no_plot  # type: ignore[assignment]

# ── Public API ────────────────────────────────────────────────────────────────
__all__ = [
    # Version
    "__version__",
    # Core
    "parse",
    "expr",
    "symbols",
    "Expression",
    # Rendering
    "render_latex",
    # Plotting
    "plot",
    "plot3d",
    "plot_parametric",
]
