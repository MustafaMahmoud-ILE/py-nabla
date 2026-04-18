"""
Custom LaTeX renderer for py-nabla.

Extends SymPy's built-in LaTeX printer with publication-quality output,
multi-style derivatives (Leibniz, prime, dot), and multiple output modes.
"""

from typing import Optional, Dict, Any
from sympy.printing.latex import LatexPrinter as _BaseLatexPrinter
from sympy import (
    Derivative, Integral, Limit, Sum, Product,
    Matrix, Abs, Add, Mul, Pow, Eq
)


class NablaLatexPrinter(_BaseLatexPrinter):
    """
    Enhanced LaTeX printer with py-nabla styling.

    Settings (pass as dict to constructor):
        derivative_style : 'leibniz' (default) | 'prime' | 'dot'
        mul_symbol       : 'dot' | 'times' | None  (default: None = thin space)
        fold_short_frac  : bool  (default: True)
    """

    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        defaults: Dict[str, Any] = {
            "derivative_style": "leibniz",
            "mul_symbol": None,
            "fold_short_frac": True,
        }
        if settings:
            # Pop custom keys before passing to base class
            self._derivative_style = settings.pop("derivative_style", "leibniz")
        else:
            self._derivative_style = "leibniz"
            settings = {}
        defaults.update(settings)
        super().__init__(defaults)

    # ================================================================
    # DERIVATIVES
    # ================================================================

    def _print_Derivative(self, expr):
        style = self._derivative_style
        if style == "prime":
            return self._derivative_prime(expr)
        if style == "dot":
            return self._derivative_dot(expr)
        return self._derivative_leibniz(expr)

    def _derivative_leibniz(self, expr):
        """Render as Leibniz notation: d/dx f or ∂/∂x f."""
        func = expr.expr
        variables = expr.variable_count  # list of (var, count) pairs

        # Determine if partial
        is_partial = len(variables) > 1 or (
            len(variables) == 1 and variables[0][1] > 1
            and not isinstance(func, (Add, Mul))
        )
        # Use partial symbol for multi-variable
        d_sym = r"\partial" if (len(variables) > 1) else "d"
        total_order = sum(count for _, count in variables)

        # Numerator
        if total_order == 1:
            numerator = f"{d_sym}"
        else:
            numerator = f"{d_sym}^{{{total_order}}}"

        # Denominator
        denom_parts = []
        for var, count in variables:
            var_latex = self._print(var)
            if count == 1:
                denom_parts.append(f"{d_sym} {var_latex}")
            else:
                denom_parts.append(f"{d_sym} {var_latex}^{{{count}}}")
        denominator = " ".join(denom_parts)

        func_latex = self._print(func)
        if isinstance(func, (Add, Mul)):
            func_latex = r"\left(%s\right)" % func_latex

        return r"\frac{%s}{%s} %s" % (numerator, denominator, func_latex)

    def _derivative_prime(self, expr):
        """Render as prime notation: f', f'', f^{(n)}."""
        func = expr.expr
        order = sum(count for _, count in expr.variable_count)
        func_latex = self._print(func)
        if order == 1:
            return f"{func_latex}'"
        if order == 2:
            return f"{func_latex}''"
        if order == 3:
            return f"{func_latex}'''"
        return f"{func_latex}^{{({order})}}"

    def _derivative_dot(self, expr):
        """Render as Newton dot notation: ẋ, ẍ."""
        func = expr.expr
        order = sum(count for _, count in expr.variable_count)
        func_latex = self._print(func)
        if order == 1:
            return r"\dot{%s}" % func_latex
        if order == 2:
            return r"\ddot{%s}" % func_latex
        if order == 3:
            return r"\dddot{%s}" % func_latex
        # Fallback for ≥4th order
        return self._derivative_leibniz(expr)

    # ================================================================
    # INTEGRALS (improved spacing)
    # ================================================================

    def _print_Integral(self, expr):
        func = expr.function
        func_latex = self._print(func)
        limits = expr.limits

        integral_sym = r"\int"
        limit_str = ""
        var_parts = []

        for lim in limits:
            var = lim[0]
            var_latex = self._print(var)
            var_parts.append(r"\, d%s" % var_latex)
            if len(lim) == 3:
                lower = self._print(lim[1])
                upper = self._print(lim[2])
                limit_str += "_{%s}^{%s}" % (lower, upper)

        return r"%s%s %s %s" % (
            integral_sym, limit_str, func_latex, " ".join(var_parts)
        )

    # ================================================================
    # LIMITS
    # ================================================================

    def _print_Limit(self, expr):
        func, var, point = expr.args[0], expr.args[1], expr.args[2]
        direction = expr.args[3] if len(expr.args) > 3 else None

        var_latex = self._print(var)
        point_latex = self._print(point)
        func_latex = self._print(func)

        dir_str = ""
        if direction == "+":
            dir_str = "^+"
        elif direction == "-":
            dir_str = "^-"

        return r"\lim_{%s \to %s%s} %s" % (
            var_latex, point_latex, dir_str, func_latex
        )

    # ================================================================
    # SUMMATIONS & PRODUCTS
    # ================================================================

    def _print_Sum(self, expr):
        func = expr.function
        lim = expr.limits[0]
        var, lower, upper = lim[0], lim[1], lim[2]
        return r"\sum_{%s=%s}^{%s} %s" % (
            self._print(var), self._print(lower),
            self._print(upper), self._print(func)
        )

    def _print_Product(self, expr):
        func = expr.function
        lim = expr.limits[0]
        var, lower, upper = lim[0], lim[1], lim[2]
        return r"\prod_{%s=%s}^{%s} %s" % (
            self._print(var), self._print(lower),
            self._print(upper), self._print(func)
        )

    # ================================================================
    # MATRICES
    # ================================================================

    def _print_Matrix(self, expr):
        rows = []
        for row in expr.tolist():
            rows.append(" & ".join(self._print(item) for item in row))
        body = r" \\ ".join(rows)
        return r"\begin{bmatrix} %s \end{bmatrix}" % body


# ================================================================
# PUBLIC API
# ================================================================

def render_latex(
    expr,
    mode: str = "inline",
    derivative_style: str = "leibniz",
    label: Optional[str] = None,
    **printer_options,
) -> str:
    """
    Render a SymPy expression (or py-nabla Expression) as LaTeX.

    Args:
        expr        : SymPy expression or py-nabla Expression object.
        mode        : Output mode:
                      ``'raw'``      — bare LaTeX string, no delimiters
                      ``'inline'``   — ``$...$``
                      ``'display'``  — ``$$...$$``
                      ``'equation'`` — ``\\begin{equation}...\\end{equation}``
                      ``'align'``    — ``\\begin{align}...\\end{align}``
        derivative_style : ``'leibniz'`` | ``'prime'`` | ``'dot'``
        label       : Optional ``\\label{...}`` for equation/align mode.
        **printer_options : Extra options forwarded to the printer.

    Returns:
        LaTeX string.

    Examples:
        >>> from sympy import symbols, sin
        >>> x = symbols('x')
        >>> render_latex(sin(x)**2, mode='inline')
        '$\\\\sin^{2}{\\\\left(x \\\\right)}$'
        >>> render_latex(sin(x), mode='display')
        '$$\\\\sin{\\\\left(x \\\\right)}$$'
    """
    # Unwrap py-nabla Expression objects
    from py_nabla.core.expression import Expression as NablaExpr
    if isinstance(expr, NablaExpr):
        expr = expr._expr

    printer = NablaLatexPrinter(
        settings={"derivative_style": derivative_style, **printer_options}
    )
    raw = printer.doprint(expr)

    if mode == "raw":
        return raw
    if mode == "inline":
        return f"${raw}$"
    if mode == "display":
        return f"$${raw}$$"
    if mode == "equation":
        label_str = f"\\label{{{label}}}" if label else ""
        return f"\\begin{{equation}}{label_str}\n  {raw}\n\\end{{equation}}"
    if mode == "align":
        label_str = f"\\label{{{label}}}" if label else ""
        return f"\\begin{{align}}{label_str}\n  {raw}\n\\end{{align}}"
    raise ValueError(f"Unknown mode: {mode!r}. Choose from: raw, inline, display, equation, align.")
