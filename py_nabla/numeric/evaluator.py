from typing import List, Union
from sympy import lambdify
import numpy as np

def vectorize(expression, variables: Union[str, List[str]]):
    r"""
    Converts a Nabla Expression into a high-performance vectorized NumPy function.
    
    Args:
        expression: Nabla Expression or SymPy Expr
        variables: List of variable names to use as function arguments
        
    Returns:
        A callable function that accepts NumPy arrays.
        
    Example:
        >>> f = expr(r"x^2 + \sin(x)")
        >>> g = f.to_numpy(['x'])
        >>> g(np.array([1, 2, 3]))
    """
    from ..core.expression import Expression
    
    expr = expression._expr if isinstance(expression, Expression) else expression
    
    if isinstance(variables, str):
        variables = [variables]
        
    # Using 'numpy' as the backend for vectorization
    return lambdify(variables, expr, modules='numpy')

class NumericalEvaluator:
    """
    Handles advanced numerical operations like solving ODEs or root finding.
    (Future placeholder for Phase 3/4 expansions)
    """
    pass
