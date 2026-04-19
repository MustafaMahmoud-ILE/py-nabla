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
try:
    from ..core.fractional import FractionalDerivative
except ImportError:
    # Fallback for direct script execution
    from py_nabla.core.fractional import FractionalDerivative

class LaplaceSolver:
    """Advanced ODE/IDE solver using Laplace Transform."""
    
    def __init__(self):
        self.s = Symbol('s')

    def _determine_order(self, expr, func, indep_var) -> int:
        """Determines the max order of the derivative."""
        max_order = 0
        func_name = str(func.func) if hasattr(func, "func") else str(func)
        var_name = str(indep_var)
        
        def find_derivs(node):
            nonlocal max_order
            if isinstance(node, Derivative):
                target = node.args[0]
                is_match = False
                if str(target) == func_name or str(target) == f"{func_name}({indep_var})":
                    is_match = True
                elif hasattr(target, "func") and str(target.func) == func_name:
                    is_match = True
                
                if is_match:
                    order = sum(1 for v in getattr(node, "variables", []) if str(v) == var_name)
                    if order > max_order: max_order = order
            elif node.__class__.__name__ == "FractionalDerivative":
                target = getattr(node, "expr", None)
                if str(target) == func_name or (hasattr(target, "func") and str(target.func) == func_name):
                    order_val = sp.nsimplify(node.order)
                    order = int(sp.ceiling(order_val))
                    if order > max_order: max_order = order
            
            for arg in getattr(node, "args", []):
                if isinstance(arg, sp.Basic): find_derivs(arg)
        
        find_derivs(expr)
        return max_order

    def _symbol_to_applied_function(self, expr, symbol, indep_var):
        y_f = sp.Function(symbol.name)
        
        def replacer(node):
            if isinstance(node, sp.Symbol) and node.name == symbol.name:
                return y_f(indep_var)
            if isinstance(node, Integral):
                new_args = [replacer(arg) if isinstance(arg, sp.Basic) else arg for arg in node.args]
                return Integral(*new_args)
            return node
        
        return expr.replace(lambda x: isinstance(x, (sp.Symbol, Integral)), replacer)

    def _apply_laplace_integral_theorem(self, expr, transform_func, indep_var, s_var):
        def replacer(node):
            if node.__class__.__name__ == "LaplaceTransform":
                integrand = node.args[0]
                if isinstance(integrand, Integral):
                    body, limits = integrand.args[0], integrand.args[1]
                    if len(limits) == 3 and limits[1] == 0 and limits[2] == indep_var:
                        tau_var = limits[0]
                        y_tau = transform_func.subs(indep_var, tau_var)
                        from sympy import Wild
                        G = Wild('G', exclude=[tau_var])
                        match = body.match(G * y_tau)
                        if match and G in match:
                            g_t = match[G].subs(indep_var - tau_var, indep_var)
                            if not g_t.has(tau_var):
                                G_s = laplace_transform(g_t, indep_var, s_var, noconds=True)
                                if hasattr(G_s, "__iter__") and not isinstance(G_s, sp.Basic): G_s = G_s[0]
                                return G_s * sp.Symbol('Y_LAPLACE_INTERNAL')
            return node
        return expr.replace(lambda x: x.__class__.__name__ == "LaplaceTransform", replacer)

    def solve(self, sympy_expr, func_name: str, var_name: str, ics: Optional[Dict] = None):
        t = Symbol(var_name, real=True, positive=True)
        s = self.s
        y_sym = Symbol(func_name)
        y_func = Function(func_name)(t)
        Y_s = Symbol('Y_LAPLACE_INTERNAL')

        eq_mapped = self._symbol_to_applied_function(sympy_expr, y_sym, t)
        
        # Normalize Eq(lhs, rhs) -> lhs - rhs
        if hasattr(eq_mapped, 'lhs') and hasattr(eq_mapped, 'rhs'):
            target_expr = eq_mapped.lhs - eq_mapped.rhs
        else:
            target_expr = eq_mapped

        def safe_lt(e, t_var, s_var):
            from sympy.integrals.transforms import laplace_transform
            res = laplace_transform(e, t_var, s_var, noconds=True)
            if hasattr(res, "__iter__") and not isinstance(res, sp.Basic): return res[0]
            if isinstance(res, sp.Tuple): return res[0]
            return res

        alg_eq = safe_lt(target_expr, t, s)
        if alg_eq is None: raise LaplaceTransformError("Could not compute Laplace Transform.")

        # Force evaluation of LaplaceTransform nodes that are still symbolic
        from sympy.integrals.transforms import LaplaceTransform, laplace_transform
        from sympy import Subs
        def deep_force_lt(expr):
            def replacer(node):
                tag = str(type(node))
                if "LaplaceTransform" in tag:
                    arg = node.args[0]
                    # If it's a custom fractional derivative, use its own logic
                    if "FractionalDerivative" in str(type(arg)):
                        lt_res = arg._eval_laplace_transform(node.args[1], node.args[2])
                        if hasattr(lt_res, "__iter__") and not isinstance(lt_res, sp.Basic): lt_res = lt_res[0]
                        return lt_res
                    # If it's a standard derivative, force expansion manually
                    elif isinstance(arg, Derivative):
                        t_var, s_var = node.args[1], node.args[2]
                        target = arg.args[0]
                        if len(arg.variables) == 1:
                            # Base case: f'
                            return s_var * LaplaceTransform(target, t_var, s_var) - target.subs(t_var, 0)
                        else:
                            # Recursive case: f^(n)
                            # Reduce order by 1
                            lower_deriv = Derivative(target, *arg.variables[:-1])
                            return s_var * LaplaceTransform(lower_deriv, t_var, s_var) - Subs(lower_deriv, t_var, 0)
                    elif isinstance(arg, sp.Add):
                        return sum(deep_force_lt(LaplaceTransform(a, node.args[1], node.args[2])) for a in arg.args)
                return node
            
            new_expr = expr.replace(lambda x: "LaplaceTransform" in str(type(x)), replacer)
            if new_expr != expr:
                return deep_force_lt(new_expr)
            return new_expr

        alg_eq = deep_force_lt(alg_eq)
        alg_eq = self._apply_laplace_integral_theorem(alg_eq, y_func, t, s)

        # Map LaplaceTransform(y) -> Y_s
        def y_transform_replacer(node):
            if node.__class__.__name__ == "LaplaceTransform":
                content = node.args[0]
                if (hasattr(content, "func") and str(content.func) == func_name) or (str(content) == f"{func_name}({t})") or (str(content) == func_name):
                    return Y_s
            return node
        
        alg_subs = alg_eq.replace(lambda x: x.__class__.__name__ == "LaplaceTransform" or "LaplaceTransform" in str(type(x)), y_transform_replacer)
        
        # Map Initial Conditions
        order = self._determine_order(eq_mapped, y_func, t)
        for i in range(order):
            ic_sym = Symbol(f'C_{i+1}')
            if i == 0:
                def ic_replacer(node):
                    name = str(getattr(node, "func", node))
                    if name == func_name or name == f"{func_name}(t)":
                        if getattr(node, "args", None) == (0,):
                            return ic_sym
                    return node
                # Target specifically Function applications or Symbol-like results at 0
                alg_subs = alg_subs.replace(lambda x: hasattr(x, "func") and str(x.func) == func_name, ic_replacer)
                alg_subs = alg_subs.subs(Function(func_name)(0), ic_sym)
            else:
                from sympy import Subs
                target_deriv = Derivative(y_func, t, i)
                target_subs = Subs(target_deriv, t, 0)
                def subs_replacer(node):
                    if isinstance(node, Subs):
                        if str(node.expr) == str(target_deriv) and str(node.variables[0]) == str(t) and node.point == (0,):
                            return ic_sym
                    if isinstance(node, Derivative):
                        if str(node) == str(target_deriv.subs(t, 0)):
                            return ic_sym
                    return node
                alg_subs = alg_subs.replace(lambda x: isinstance(x, (Subs, Derivative)), subs_replacer)
                alg_subs = alg_subs.subs(target_subs, ic_sym)
                alg_subs = alg_subs.subs(target_deriv.subs(t, 0), ic_sym)
        
        
        
        

        # Substitute IC values
        if ics:
            for k, v in ics.items():
                k_norm = k.sympy if hasattr(k, 'sympy') else k
                v_norm = v.sympy if hasattr(v, 'sympy') else v
                if str(k_norm) == f"{func_name}(0)" or k_norm == Function(func_name)(0) or str(k_norm) == "0":
                    alg_subs = alg_subs.subs(Symbol('C_1'), v_norm)
                for idx in range(1, order):
                    if str(k_norm) == f"Derivative({func_name}(t), t, {idx}).subs(t, 0)":
                        alg_subs = alg_subs.subs(Symbol(f'C_{idx+1}'), v_norm)
        
        
        try:
            Y_sol = sp.solve(alg_subs, Y_s)
        except Exception:
            raise NablaSolveError("Failed to solve in s-domain.")

        if not Y_sol: raise LaplaceTransformError("No solution found for Y(s).")
        
        Y_expr = sp.nsimplify(Y_sol[0]).factor()
        y_final = inverse_laplace_transform(Y_expr, s, t)
        
        from sympy.integrals.transforms import InverseLaplaceTransform
        if hasattr(y_final, "has") and y_final.has(InverseLaplaceTransform):
            raise LaplaceTransformError("Inverse Laplace failed to find closed-form solution.")

        return Eq(y_func, y_final)
