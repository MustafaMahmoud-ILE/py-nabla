import sympy as sp
import py_nabla as nb
from py_nabla.solvers.laplace_solver import LaplaceSolver
import traceback

print("--- Final Deep Diagnosis ---")
solver = LaplaceSolver()
eq = nb.parse(r"\frac{d^{1/2}}{dt^{1/2}} y + y = 0")
ics = {nb.parse(r'y(0)'): 1}

try:
    print(f"Eq: {eq.sympy}")
    print(f"ICs: {ics}")
    
    # Trace inside solve
    # 1. Map symbols
    t = sp.Symbol('t', real=True, positive=True)
    s = solver.s
    y_sym = sp.Symbol('y')
    y_func = sp.Function('y')(t)
    Y_s = sp.Symbol('Y_LAPLACE_INTERNAL')
    
    eq_func = solver._symbol_to_applied_function(eq.sympy, y_sym, t)
    print(f"Eq Func: {eq_func}")
    
    # 2. LT
    from sympy.integrals.transforms import laplace_transform
    L_eq = laplace_transform(eq_func, t, s, noconds=True)
    print(f"L(eq): {L_eq}")
    
    # 2.5 Force
    from py_nabla.solvers.laplace_solver import FractionalDerivative
    from sympy.integrals.transforms import LaplaceTransform
    def force_lt(node):
        if isinstance(node, LaplaceTransform) and isinstance(node.args[0], FractionalDerivative):
            return node.args[0]._eval_laplace_transform(node.args[1], node.args[2])
        return node
    
    alg_eq = L_eq.replace(lambda x: isinstance(x, LaplaceTransform), force_lt)
    print(f"Alg Eq: {alg_eq}")

    # 4. Substitution
    def y_transform_replacer(node):
        if node.__class__.__name__ == "LaplaceTransform":
            if hasattr(node.args[0], "func") and str(node.args[0].func) == "y":
                return Y_s
        return node
    
    alg_subs = alg_eq.replace(lambda x: x.__class__.__name__ == "LaplaceTransform", y_transform_replacer)
    print(f"Alg Subs (Y_s): {alg_subs}")
    
    # IC Replace
    ic_sym = sp.Symbol('C_1')
    def ic_replacer(node):
        if hasattr(node, "func") and str(node.func) == "y":
            if hasattr(node, "args") and node.args == (0,):
                return ic_sym
        return node
    alg_subs = alg_subs.replace(lambda x: hasattr(x, "func"), ic_replacer)
    print(f"Alg Subs (C_1): {alg_subs}")
    
    # IC Values
    alg_subs = alg_subs.subs(ic_sym, 1)
    print(f"Alg Subs (Final): {alg_subs}")
    
    # Solve
    Y_sol = sp.solve(alg_subs, Y_s)
    print(f"Y_sol: {Y_sol}")
    
    # Inverse
    Y_expr = Y_sol[0]
    y_t = sp.inverse_laplace_transform(Y_expr, s, t)
    print(f"y_t: {y_t}")
    print(f"Has InverseLaplaceTransform? {y_t.has(sp.InverseLaplaceTransform)}")

except Exception:
    traceback.print_exc()
