import py_nabla as nb
from sympy import symbols, Function, Eq, exp, sin, cos, besselj, bessely

def extreme_math_validation():
    print("--- py-nabla EXTREME MATHEMATICAL VALIDATION ---")
    
    # 1. Bessel's Differential Equation (Order 0)
    # t^2 y'' + t y' + t^2 y = 0
    print("\n[1] Validating Bessel Differential Equation (Cylindrical Physics)...")
    bessel_eq = nb.parse(r"t^2 y'' + t y' + t^2 y = 0")
    # Series solution is typical for Bessel if analytical fails, but SymPy handles Besselj
    bessel_sol = bessel_eq.dsolve(indep_var='t', method='analytical')
    print(f"Bessel Solution: {bessel_sol.latex()}")

    # 2. Volterra Integral Equation of the Second Kind (Convolution)
    # y(t) = exp(t) + \int_0^t sin(t-tau) y(tau) dtau
    print("\n[2] Validating Volterra Integral Equation (Convolution Theorem)...")
    volterra_eq = nb.parse(r"y = \exp{t} + \int_0^t \sin{t-\tau} y(\tau) d\tau")
    volterra_sol = volterra_eq.dsolve(method='laplace')
    print(f"Volterra Solution: {volterra_sol.latex()}")

    # 3. High-Order Linear ODE (6th Order)
    # y^{(6)} - y = 0
    print("\n[3] Validating 6th Order Linear ODE (Structural Stability)...")
    sixth_order = nb.parse(r"y^{ (6) } - y = 0")
    sixth_sol = sixth_order.dsolve()
    print(f"6th Order Solution: {sixth_sol.latex()}")

    # 4. Quantum Harmonic Oscillator (Hermite-like setup)
    # y'' - t^2 y = -E y => y'' + (E - t^2)y = 0
    print("\n[4] Validating Quantum SHO (Special Functions)...")
    sho_eq = nb.parse(r"y'' + (E - t^2) y = 0")
    # This usually yields Weber functions / Parabolic Cylinder functions
    sho_sol = sho_eq.dsolve(indep_var='t', method='analytical')
    print(f"Quantum SHO Solution: {sho_sol.latex()}")

if __name__ == "__main__":
    extreme_math_validation()
