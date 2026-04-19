from typing import Optional, Union, Tuple, Dict, Any, List, Callable
from sympy import (
    Expr, latex as sympy_latex, simplify, diff, integrate,
    expand, factor, solve as sympy_solve, series as sympy_series,
    Symbol as SympySymbol, symbols as sympy_symbols,
    limit as sympy_limit, oo
)
import numpy as np


class Expression:
    """
    Core py-nabla Expression class.

    Wraps a SymPy expression and provides a clean, intuitive API for
    symbolic computation, numerical evaluation, and LaTeX rendering.

    All operations return **new** Expression objects (immutable pattern).

    Examples:
        >>> import py_nabla as nb
        >>> f = nb.parse(r"x^2 + 1")
        >>> f.diff('x')
        Expression(2*x)
        >>> f.evaluate(x=3)
        10.0
    """

    def __init__(
        self,
        sympy_expr: Expr,
        _latex_source: Optional[str] = None,
        _steps: Optional[list] = None,
    ):
        self._expr = sympy_expr
        self._latex_source = _latex_source
        self._steps = _steps or []

    # ================================================================
    # CALCULUS OPERATIONS
    # ================================================================

    def diff(
        self,
        var: Union[str, SympySymbol],
        order: int = 1,
    ) -> "Expression":
        """
        Differentiate the expression.

        Args:
            var: Variable to differentiate with respect to.
            order: Derivative order (default: 1).

        Returns:
            New Expression containing the derivative.

        Examples:
            >>> f = nb.parse(r"x^3 + x^2")
            >>> f.diff('x')
            Expression(3*x**2 + 2*x)
            >>> f.diff('x', order=2)
            Expression(6*x + 2)
        """
        if isinstance(var, str):
            var = SympySymbol(var)
        result = diff(self._expr, var, order)
        return Expression(result)

    def integrate(
        self,
        var: Union[str, SympySymbol],
        limits: Optional[Tuple[Any, Any]] = None,
    ) -> "Expression":
        """
        Integrate the expression.

        Args:
            var: Integration variable.
            limits: Optional ``(lower, upper)`` for a definite integral.

        Returns:
            New Expression with the integral result.

        Examples:
            >>> f = nb.parse(r"x^2")
            >>> f.integrate('x')
            Expression(x**3/3)
            >>> f.integrate('x', limits=(0, 1))
            Expression(1/3)
        """
        if isinstance(var, str):
            var = SympySymbol(var)
        if limits is not None:
            result = integrate(self._expr, (var, limits[0], limits[1]))
        else:
            result = integrate(self._expr, var)
        return Expression(result)

    def limit(
        self,
        var: Union[str, SympySymbol],
        point: Any,
        direction: str = "+-",
    ) -> "Expression":
        """
        Compute the limit of the expression.

        Args:
            var: Limit variable.
            point: Limit point. Use ``'oo'`` or ``float('inf')`` for infinity.
            direction: ``'+'``, ``'-'``, or ``'+-'`` (both sides).

        Returns:
            New Expression with the limit value.

        Examples:
            >>> f = nb.parse(r"\\frac{\\sin(x)}{x}")
            >>> f.limit('x', 0)
            Expression(1)
        """
        if isinstance(var, str):
            var = SympySymbol(var)
        if point in ('oo', float('inf'), 'inf', '+oo'):
            point = oo
        elif point in ('-oo', float('-inf'), '-inf'):
            point = -oo
        result = sympy_limit(self._expr, var, point, direction)
        return Expression(result)

    def series(
        self,
        var: Union[str, SympySymbol],
        point: float = 0,
        order: int = 6,
    ) -> "Expression":
        """
        Compute the Taylor / Laurent series expansion.

        Args:
            var: Expansion variable.
            point: Expansion point (default: 0).
            order: Number of terms (default: 6).

        Returns:
            New Expression with the series (including O-term).

        Examples:
            >>> f = nb.parse(r"\\sin(x)")
            >>> f.series('x', order=5)
            Expression(x - x**3/6 + O(x**5))
        """
        if isinstance(var, str):
            var = SympySymbol(var)
        result = sympy_series(self._expr, var, point, order)
        return Expression(result)

    # ================================================================
    # ALGEBRAIC OPERATIONS
    # ================================================================

    def simplify(self, **kwargs) -> "Expression":
        """
        Simplify the expression.

        Examples:
            >>> f = nb.parse(r"\\frac{x^2 - 1}{x - 1}")
            >>> f.simplify()
            Expression(x + 1)
        """
        return Expression(simplify(self._expr, **kwargs))

    def expand(self, **kwargs) -> "Expression":
        """
        Expand the expression.

        Examples:
            >>> f = nb.parse(r"(x + y)^2")
            >>> f.expand()
            Expression(x**2 + 2*x*y + y**2)
        """
        return Expression(expand(self._expr, **kwargs))

    def factor(self, **kwargs) -> "Expression":
        """
        Factor the expression.

        Examples:
            >>> f = nb.parse(r"x^2 - 1")
            >>> f.factor()
            Expression((x - 1)*(x + 1))
        """
        return Expression(factor(self._expr, **kwargs))

    def solve(
        self,
        var: Optional[Union[str, SympySymbol]] = None,
        **kwargs,
    ) -> List["Expression"]:
        """
        Solve the expression (or equation) for a variable.

        Args:
            var: Variable to solve for. Auto-detected if only one free symbol.
            **kwargs: Additional options forwarded to ``sympy.solve``.

        Returns:
            List of solution Expressions.

        Examples:
            >>> eq = nb.parse(r"x^2 - 4 = 0")
            >>> eq.solve('x')
            [Expression(-2), Expression(2)]
        """
        if var is None:
            free = self._expr.free_symbols
            if len(free) == 1:
                var = list(free)[0]
            elif len(free) == 0:
                return []
            else:
                raise ValueError(
                    f"Multiple free variables {free}. Specify which to solve for."
                )
        solutions = sympy_solve(self._expr, var, **kwargs)
        return [Expression(sol) for sol in solutions]

    # ================================================================
    # NUMERICAL EVALUATION
    # ================================================================

    def evaluate(
        self,
        substitutions: Optional[Dict[Any, Any]] = None,
        **kwargs,
    ) -> Union["Expression", float, complex, np.ndarray]:
        """
        Numerically evaluate the expression.

        Supports scalar substitutions and vectorised NumPy arrays.

        Args:
            substitutions: Dictionary mapping variables to values.
            **kwargs: Keyword substitutions (e.g., ``x=2``).

        Returns:
            ``float``, ``complex``, ``np.ndarray``, or a remaining Expression.

        Examples:
            >>> f = nb.parse(r"x^2 + 1")
            >>> f.evaluate(x=3)
            10.0
            >>> f.evaluate(x=np.linspace(0, 1, 5))
            array([1.  , 1.0625, 1.25, 1.5625, 2.  ])
        """
        all_subs = dict(substitutions or {})
        all_subs.update(kwargs)

        # Vectorised path for NumPy arrays
        has_array = any(isinstance(v, np.ndarray) for v in all_subs.values())
        if has_array:
            return self._vectorized_evaluate(all_subs)

        result = self._expr.subs(all_subs)
        if result.is_number:
            val = complex(result.evalf())
            return val.real if val.imag == 0 else val
        return Expression(result)

    def _vectorized_evaluate(self, subs: Dict) -> np.ndarray:
        """Internal: evaluate using lambdify for NumPy arrays."""
        from sympy import lambdify
        vars_list = list(subs.keys())
        func = lambdify(vars_list, self._expr, modules='numpy')
        return func(*[subs[v] for v in vars_list])

    def lambdify(
        self,
        vars: List[Union[str, SympySymbol]],
        modules: str = "numpy",
    ) -> Callable:
        """
        Create a fast, NumPy-compatible callable function.

        Args:
            vars: Ordered list of variable names.
            modules: Backend (``'numpy'``, ``'math'``, etc.).

        Returns:
            A Python callable.

        Examples:
            >>> f = nb.parse(r"x^2 + y^2")
            >>> func = f.lambdify(['x', 'y'])
            >>> func(3, 4)
            25.0
        """
        from sympy import lambdify as sympy_lambdify
        return sympy_lambdify(vars, self._expr, modules=modules)

    # ================================================================
    # RENDERING
    # ================================================================

    def latex(self, mode: str = 'raw', **options) -> str:
        """
        Render the expression as a LaTeX string.

        Args:
            mode: Output mode — ``'raw'``, ``'inline'`` ($...$),
                  ``'display'`` ($$...$$).
            **options: Forwarded to the LaTeX printer.

        Returns:
            LaTeX string.

        Examples:
            >>> f = nb.parse(r"x^2")
            >>> f.diff('x').latex(mode='inline')
            '$2 x$'
        """
        raw = sympy_latex(self._expr, **options)
        if mode == 'inline':
            return f"${raw}$"
        if mode == 'display':
            return f"$${raw}$$"
        return raw

    # ================================================================
    # DUNDER METHODS
    # ================================================================

    def __repr__(self) -> str:
        return f"Expression({self._expr})"

    def __str__(self) -> str:
        return str(self._expr)

    def _repr_latex_(self) -> str:
        """Jupyter / IPython rich display."""
        return f"$${sympy_latex(self._expr)}$$"

    # ================================================================
    # OPERATOR OVERLOADING
    # ================================================================

    def _coerce(self, other):
        return other._expr if isinstance(other, Expression) else other

    def __add__(self, other):      return Expression(self._expr + self._coerce(other))
    def __radd__(self, other):     return Expression(other + self._expr)
    def __sub__(self, other):      return Expression(self._expr - self._coerce(other))
    def __rsub__(self, other):     return Expression(other - self._expr)
    def __mul__(self, other):      return Expression(self._expr * self._coerce(other))
    def __rmul__(self, other):     return Expression(other * self._expr)
    def __truediv__(self, other):  return Expression(self._expr / self._coerce(other))
    def __rtruediv__(self, other): return Expression(other / self._expr)
    def __pow__(self, other):      return Expression(self._expr ** self._coerce(other))
    def __rpow__(self, other):     return Expression(other ** self._expr)
    def __neg__(self):             return Expression(-self._expr)
    def __pos__(self):             return self

    def __eq__(self, other) -> bool:  # type: ignore[override]
        """Check structural equality of expressions."""
        return self._expr == self._coerce(other)

    def equation(self, other) -> "Expression":
        """Create a SymPy Eq (symbolic equation)."""
        from sympy import Eq
        return Expression(Eq(self._expr, self._coerce(other)))

    def __hash__(self):
        return hash(self._expr)

    # ================================================================
    # PROPERTIES
    # ================================================================

    @property
    def free_symbols(self):
        """Set of free symbolic variables in the expression."""
        return self._expr.free_symbols

    @property
    def is_number(self) -> bool:
        """``True`` if the expression contains no free symbols."""
        return bool(self._expr.is_number)

    @property
    def complexity(self) -> int:
        """Rough measure of expression complexity (character count)."""
        return len(str(self._expr))

    @property
    def sympy(self) -> Expr:
        """Access the underlying SymPy expression directly."""
        return self._expr
