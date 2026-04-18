from .parser.parser import LaTeXParser
from .core.expression import Expression as NablaExpression

__version__ = "0.1.0"

# Global parser instance
_default_parser = LaTeXParser()

def expr(latex_str: str) -> NablaExpression:
    """
    Parses a LaTeX string into a Nabla Expression.
    
    Example:
        >>> f = expr(r"\frac{d}{dx}(x^2)")
        >>> print(f.simplify())
        2*x
    """
    sympy_expr = _default_parser.parse(latex_str)
    return NablaExpression(sympy_expr, _latex_source=latex_str)

# Alias for consistent API
parse = expr

def symbols(names: str):
    """
    Creates symbolic variables.
    Equivalent to sympy.symbols.
    """
    from sympy import symbols as sympy_symbols
    return sympy_symbols(names)

def render(expression: NablaExpression, mode: str = 'inline') -> str:
    """
    Renders an expression as LaTeX.
    """
    return expression.latex()

# Placeholder for plotting to prevent import errors if called
def plot(*args, **kwargs):
    from .plotting.plotter import plot as _plot
    return _plot(*args, **kwargs)

__all__ = ["expr", "parse", "symbols", "render", "plot", "NablaExpression"]
