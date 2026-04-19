import sympy as sp

t, s = sp.symbols('t s')
y = sp.Function('y')(t)
Y = sp.Function('Y')(s)

# Test 1: Simple ODE using standard dsolve
eq1 = sp.Eq(y.diff(t) + y, t)
sol1 = sp.dsolve(eq1)
print(f"Standard dsolve: {sol1}")

# Test 2: Laplace transform of a derivative manually
lap_deriv = sp.laplace_transform(y.diff(t), t, s, noconds=True)
print(f"Laplace of y'(t): {lap_deriv}")

lap_deriv_simp = sp.laplace_transform(y.diff(t, 2), t, s, noconds=True)
print(f"Laplace of y''(t): {lap_deriv_simp}")

# Test 3: Integro-Differential Equation
# y'(t) + \int_0^t y(\tau) d\tau = 1
tau = sp.Symbol('tau')
integral = sp.Integral(y.subs(t, tau), (tau, 0, t))
ide = y.diff(t) + integral - 1
print(f"IDE: {ide}")

lap_ide = sp.laplace_transform(ide, t, s, noconds=True)
print(f"Laplace of IDE: {lap_ide}")

# Check if we can solve it algebraically for Y(s)
# Replace laplace_transform(y(t), t, s) with Y(s)
L_y = sp.laplace_transform(y, t, s, noconds=True)
alg_eq = sp.Eq(lap_ide, 0).subs(L_y, Y)
print(f"Algebraic Eq: {alg_eq}")

# There's a problem: laplace_transform of y'(t) is left unevaluated or as LaplaceTransform(Derivative(y(t), t), t, s)
# Actually, SymPy doesn't automatically substitute the initial conditions into laplace_transform(Derivative(...)). 
# We need to test if it does.
