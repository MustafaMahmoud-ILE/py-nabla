# Advanced Math Validation: Fractional Calculus & Integro-Differential Equations

This document documents the successful integration and validation of fractional calculus into the `py-nabla` engine (v1.1.0-alpha).

## 1. Objective
To extend the symbolic engine to support non-integer differentiation and solve fractional differential equations (FDEs) analytically using the Laplace Transform method.

## 2. Implemented Features
- **Fractional Operator Support**: Parser support for $d^\alpha/dt^\alpha$ using `\frac{d^\alpha}{dt^\alpha}` and `y^{(\alpha)}`.
- **Caputo Derivative**: Implementation of the Caputo fractional derivative in `core/fractional.py`.
- **Fractional Laplace Solver**: Hardened `LaplaceSolver` to handle non-integer power algebraic equations and perform inverse transforms via Meijer G-functions.

## 3. Validation Test Case: Fractional Relaxation
The "Stress Test" involves the fractional relaxation equation, which is a fundamental benchmark in fractional calculus.

**Equation**:
$$\frac{d^{1/2}y}{dt^{1/2}} + y = 0, \quad y(0) = 1$$

**Expected Analytical Solution**:
$$y(t) = E_{1/2}(-t^{1/2}) = e^t \text{erfc}(\sqrt{t})$$

### Execution Log
```python
import py_nabla as nb
eq = nb.parse(r"\frac{d^{1/2}}{dt^{1/2}} y + y = 0")
sol = eq.dsolve(ics={nb.parse(r"y(0)"): 1})
print(sol.sympy)
```

**Result**:
`Eq(y(t), exp(t)*erfc(sqrt(t)))`

## 4. Stability Test Case: Higher-Order Standard ODE
To ensure no regressions occurred in integer-order calculus, the solver was verified against a second-order oscillator equation.

**Equation**:
$$y'' + y = 0, \quad y(0) = C_1, \quad y'(0) = C_2$$

**Result**:
`Eq(y(t), C_1*cos(t) + C_2*sin(t))`
*Status: PASSED*

## 5. Technical Achievements
- **Symbolic Resilience**: Enforced `Rational` arithmetic to prevent floating-point errors in non-integer differentiation orders.
- **Recursive Expansion Engine**: Implemented `deep_force_lt` to handle arbitrary derivative orders (standard and fractional) within the Laplace domain.
- **Robust IC Mapping**: Developed a hybrid identity-string matching system for initial conditions, correctly handling `Subs` and complex derivative nodes.

## 6. Conclusion
`py-nabla` is now a robust symbolic engine capable of solving complex fractional differential equations and standard higher-order ODEs with high precision and automated initial condition handling.
