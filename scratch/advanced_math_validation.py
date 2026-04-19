import py_nabla as nb
from sympy import symbols, Function

def advanced_math_validation():
    print("--- py-nabla ADVANCED MATHEMATICAL VALIDATION ---")
    
    # 1. Quantum Mechanics: Airy's Equation
    # y'' - t*y = 0
    print("\n[1] Validating Airy Equation (Quantum Physics)...")
    airy_eq = nb.parse(r"y'' - t y = 0")
    airy_sol = airy_eq.dsolve(indep_var='t')
    print(f"Analytical Solution: {airy_sol.latex()}")

    # 2. Electrical Engineering: Integro-Differential Equation
    # i'(t) + 3*i(t) + 2 * \int_0^t i(tau) dtau = 1
    print("\n[2] Validating RLC Circuit (Integro-Differential)...")
    rlc_eq = nb.parse(r"i' + 3 i + 2 \int_0^t i(\tau) d\tau = 1")
    rlc_sol = rlc_eq.dsolve(func_var='i')
    print(f"IDE Solution: {rlc_sol.latex()}")

    # 3. Higher Order Harmonic: 4th Order
    # y'''' - y = 0
    print("\n[3] Validating 4th Order Linear ODE...")
    fourth_order = nb.parse(r"y^{ (4) } - y = 0")
    fourth_sol = fourth_order.dsolve()
    print(f"4th Order Solution: {fourth_sol.latex()}")

    # 4. Nonlinear Fallback: Logistic Growth
    # y' = y (1 - y)
    print("\n[4] Validating Nonlinear Power Series Fallback...")
    logistic = nb.parse(r"y' = y (1 - y)")
    # Should fallback to analytical or series
    logistic_sol = logistic.dsolve(method='series', series_order=4)
    print(f"Series Solution: {logistic_sol.latex()}")

if __name__ == "__main__":
    advanced_math_validation()
