import sympy as sp
import warnings
from typing import Dict, Union, Optional
from sympy import laplace_transform, inverse_laplace_transform, Symbol, Function, Eq, Derivative, Integral

from .solver_exceptions import (
    NablaSolveError,
    LaplaceTransformError,
    NonlinearODEError,
    InvalidInitialConditionsError
)

class LaplaceSolver:
    """Advanced ODE/IDE solver using Laplace Transform."""
    
    def __init__(self):
        self.s = Symbol('s')

    def _determine_order(self, expr: sp.Expr, func: sp.Function, indep_var: sp.Symbol) -> int:
        """Determines the max order of the derivative of func with respect to indep_var."""
        max_order = 0
        def find_derivs(node):
            nonlocal max_order
            if isinstance(node, Derivative) and node.args[0] == func:
                # Count instances of indep_var in differentiation arguments
                order = sum(1 for var in node.args[1:] if var == indep_var)
                if order > max_order:
                    max_order = order
            for arg in node.args:
                if isinstance(arg, sp.Basic):
                    find_derivs(arg)
        find_derivs(expr)
        return max_order

    def _symbol_to_applied_function(self, expr, symbol, func):
        """Converts Symbol y to Function y(t) inside evaluating expressions."""
        def replacer(node, local_var=None):
            if isinstance(node, Derivative):
                if node.args[0] == symbol:
                    # Differentiation is wrt to args[1:], keep it
                    new_args = [func.func(local_var) if local_var else func] + [replacer(a, local_var) if isinstance(a, sp.Basic) else a for a in node.args[1:]]
                    return Derivative(*new_args, evaluate=False)
            elif isinstance(node, Integral):
                # Check for dummy variables in limits
                if len(node.args) > 1 and isinstance(node.args[1], tuple) and len(node.args[1]) > 0:
                    dummy = node.args[1][0]
                    # Pass the dummy down to children so y becomes y(dummy)
                    new_args = [replacer(node.args[0], dummy)] + list(node.args[1:])
                    return Integral(*new_args)
            elif node == symbol:
                return func.func(local_var) if local_var else func
            
            new_args = [replacer(arg, local_var) if isinstance(arg, sp.Basic) else arg for arg in node.args]
            return node.func(*new_args) if new_args else node

        return replacer(expr)

    def _apply_laplace_integral_theorem(self, expr, transform_func, indep_var, s_var):
        """
        Replaces LaplaceTransform(Integral(y(tau), (tau, 0, t)), t, s)
        with Y(s)/s natively.
        """
        def replacer(node):
            # Target is explicitly LaplaceTransform(Integral(...))
            from sympy.integrals.transforms import LaplaceTransform
            if isinstance(node, LaplaceTransform):
                integrand = node.args[0]
                if isinstance(integrand, Integral):
                    # Check if the structure matches \int_0^t y(tau)
                    int_body = integrand.args[0]
                    var_bound = integrand.args[1]
                    if len(var_bound) == 3:
                        tau_var, lower, upper = var_bound
                        if upper == indep_var and lower == 0:
                            # It's a standard IDE integral from 0 to t
                            # We replace it with Y(s)/s
                            # But wait, what if the integrand is f(t-\tau) y(\tau)? (Convolution).
                            # If it's just y(\tau), then the transform is Y(s)/s
                            # We can generalize later, for now we map direct functions.
                            if int_body.subs(tau_var, indep_var) == transform_func:
                                return sp.Symbol('Y_LAPLACE_INTERNAL') / s_var
            
            new_args = [replacer(arg) if isinstance(arg, sp.Basic) else arg for arg in node.args]
            return node.func(*new_args) if new_args else node
            
        return replacer(expr)

    def solve(self, sympy_expr, func_name: str, var_name: str, initial_conditions: Optional[Dict] = None):
        """
        Main solver pipeline.
        """
        t = Symbol(var_name)
        s = self.s
        y_sym = Symbol(func_name)
        y_func = Function(func_name)(t)
        Y_s = Symbol('Y_LAPLACE_INTERNAL')

        # 1. Map symbols to functions (y -> y(t))
        eq_func = self._symbol_to_applied_function(sympy_expr, y_sym, y_func)

        # 2. Extract ODE Form (Eq or Expr=0)
        if isinstance(eq_func, Eq):
            lhs_lap = laplace_transform(eq_func.lhs, t, s, noconds=True)
            rhs_lap = laplace_transform(eq_func.rhs, t, s, noconds=True)
            alg_eq = lhs_lap - rhs_lap
        else:
            alg_eq = laplace_transform(eq_func, t, s, noconds=True)

        if alg_eq is None:
            raise LaplaceTransformError("Could not compute Laplace Transform of the equation.")

        # 3. Handle Integrals
        alg_eq = self._apply_laplace_integral_theorem(alg_eq, y_func, t, s)

        # 4. Substitute generic Initial Conditions
        order = self._determine_order(eq_func, y_func, t)
        target_transform = laplace_transform(y_func, t, s, noconds=True)

        alg_subs = alg_eq.subs(target_transform, Y_s)
        
        from sympy import Subs
        for i in range(order):
            ic_sym = Symbol(f'C_{i+1}')
            # Function(func_name)(0) for y(0)
            if i == 0:
                alg_subs = alg_subs.subs(Function(func_name)(0), ic_sym)
                alg_subs = alg_subs.subs(y_func.subs(t, 0), ic_sym)
            else:
                # laplace yields Subs(Derivative(y(t), t), t, 0) for higher order ICs
                subs_expr = Subs(Derivative(y_func, t, i), t, 0)
                alg_subs = alg_subs.subs(subs_expr, ic_sym)
                # Fallback to direct replacement of evaluated diff
                alg_subs = alg_subs.replace(Derivative(y_func, t, i).subs(t, 0), ic_sym)


        # 5. Solve for Y(s) algebraically
        try:
            Y_sol = sp.solve(alg_subs, Y_s)
        except Exception:
            raise NablaSolveError("Failed to solve algebraic equation in s-domain.")

        if not Y_sol:
            raise LaplaceTransformError("No solution found for Y(s). Equation may be nonlinear.")
        
        Y_expr = Y_sol[0]
        from sympy.integrals.transforms import LaplaceTransform
        if Y_expr.has(LaplaceTransform):
            raise LaplaceTransformError("Nonlinear or unsolvable laplace form.")
        
        # Partial fractions sometimes help inverse Laplace
        try:
            Y_expr = sp.apart(Y_expr, s)
        except Exception:
            pass

        # 6. Inverse Laplace Transform
        y_t = inverse_laplace_transform(Y_expr, s, t)

        from sympy.integrals.transforms import InverseLaplaceTransform
        if isinstance(y_t, InverseLaplaceTransform) or y_t.has(InverseLaplaceTransform): # It failed to evaluate
            raise LaplaceTransformError("Inverse Laplace Transform failed analytically.")

        from sympy import Subs
        for i in range(order):
            ic_sym = Symbol(f'C_{i+1}')
            if i == 0:
                y_t = y_t.replace(Function(func_name)(0), ic_sym)
                y_t = y_t.replace(y_func.subs(t, 0), ic_sym)
            else:
                y_t = y_t.replace(Subs(Derivative(y_func, t, i), t, 0), ic_sym)
                y_t = y_t.replace(Derivative(y_func, t, i).subs(t, 0), ic_sym)

        return Eq(y_func, y_t)
