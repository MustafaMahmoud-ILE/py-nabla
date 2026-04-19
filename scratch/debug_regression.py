import sympy as sp
from py_nabla import parse
from py_nabla.solvers.laplace_solver import LaplaceSolver

def debug_test():
    eq = parse(r"y' + y = 0")
    print(f"Parsed eq: {eq.sympy}")
    # Simulate internal logic
    solver = LaplaceSolver()
    t = sp.Symbol('t', real=True, positive=True)
    s = solver.s
    y_sym = sp.Symbol('y')
    
    # Trace solve
    # y_func = sp.Function('y')(t)
    # Y_s = sp.Symbol('Y_LAPLACE_INTERNAL')
    
    sol = eq.dsolve(method='laplace')
    print(f"Solution: {sol.sympy}")

if __name__ == "__main__":
    debug_test()
