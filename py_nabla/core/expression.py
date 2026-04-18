from typing import Optional, Union, Tuple, Dict, Any
from sympy import Expr, latex, simplify, diff, integrate, Symbol as SympySymbol
from dataclasses import dataclass
import numpy as np

@dataclass
class Expression:
    """
    Core Nabla Expression class wrapping a SymPy expression.
    Enables bidirectional LaTeX conversion and lazy evaluation.
    """
    _expr: Expr
    _latex_source: Optional[str] = None
    _steps: Optional[list] = None

    def simplify(self) -> 'Expression':
        """Simplifies the mathematical expression."""
        return Expression(simplify(self._expr))

    def diff(self, var: Union[str, SympySymbol], order: int = 1) -> 'Expression':
        """Differentiates the expression."""
        return Expression(diff(self._expr, var, order))

    def integrate(self, var: Union[str, SympySymbol], 
                  limits: Optional[Tuple[Any, Any]] = None) -> 'Expression':
        """Integrates the expression."""
        if limits:
            return Expression(integrate(self._expr, (var, limits[0], limits[1])))
        return Expression(integrate(self._expr, var))

    def evaluate(self, substitutions: Optional[Dict[Any, Any]] = None, **kwargs) -> Union['Expression', float, complex, np.ndarray]:
        """
        Evaluate the expression numerically.
        Returns a Nabla Expression if variables remain, otherwise a numeric type.
        """
        # Combine dictionary substitutions and keyword arguments
        all_subs = (substitutions or {}).copy()
        all_subs.update(kwargs)
        
        result = self._expr.subs(all_subs)
        
        # If the result is purely numeric (no Symbols left)
        if result.is_number:
            # Prefer complex if there's an imaginary part, otherwise float
            if result.is_complex and not result.is_real:
                return complex(result.evalf())
            return float(result.evalf())
        
        # If variables remain, return a new Expression (Lazy Evaluation)
        return Expression(result)

    def to_numpy(self, *args):
        """
        Converts to a vectorized NumPy function using lambdify.
        """
        from ..numeric.evaluator import vectorize
        return vectorize(self, *args)

    def latex(self) -> str:
        """Returns the LaTeX representation."""
        # Using sympy's default for now, will enhance in Phase 4
        return latex(self._expr)

    def __repr__(self) -> str:
        return f"Expression({self._expr})"

    def __str__(self) -> str:
        return str(self._expr)

    def _repr_latex_(self) -> str:
        """Hook for Jupyter Notebook rendering."""
        return f"$${latex(self._expr)}$$"

    # Operator overloading for natural math
    def __add__(self, other): return Expression(self._expr + self._to_sympy(other))
    def __sub__(self, other): return Expression(self._expr - self._to_sympy(other))
    def __mul__(self, other): return Expression(self._expr * self._to_sympy(other))
    def __truediv__(self, other): return Expression(self._expr / self._to_sympy(other))
    def __pow__(self, other): return Expression(self._expr ** self._to_sympy(other))

    def _to_sympy(self, other):
        if isinstance(other, Expression):
            return other._expr
        return other
