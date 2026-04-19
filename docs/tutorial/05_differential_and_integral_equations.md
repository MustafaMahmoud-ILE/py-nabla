# Differential and Integral Equations

`py-nabla` v1.1.0 introduces a phenomenally powerful Mathematical Solve Engine powered internally by **Laplace Transforms**. You can now solve Ordinary Differential Equations (ODEs) of any order, as well as complex Integral Equations (IDEs), natively!

## 1. Traditional Differential Equations (ODEs)

You can write differential equations exactly as you would on a chalkboard. 
`py-nabla` understands both the classic **Leibniz Notation** ($\frac{dy}{dt}$) and the rapid **Newton Prime Notation** ($y'$).

```python
import py_nabla as nb

# Simple First-Order ODE
# y' = y
eq = nb.parse(r"y' = y")
solution = eq.dsolve()
print(solution) 
# Output: Eq(y(t), C_1*exp(t))
```

### Automatic Constants
Notice how `py-nabla` automatically inserted the constant `C_1`. The engine detects the order of the equation and seamlessly injects $C_1, C_2...$ whenever analytical integration bounds or initial conditions are not provided!

### Harmonic Oscillators & Higher Order Equations
```python
# y'' + \omega^2 y = 0
oscillator = nb.parse(r"y'' + \omega^2 y = 0")
sol = oscillator.dsolve(indep_var='t')
print(sol.latex()) 
# LaTeX: y(t) = C_{1} \sin({\omega t}) + C_{2} \cos({\omega t})
```

## 2. Advanced: Integro-Differential Equations (IDEs)

Very few engines can directly solve equations containing both derivatives and integrals. Because `py-nabla` leverages Laplace Transforms at its core, these become trivial:

```python
# y' + integral of y over tau = t
# Initial assumption: y(0) = C_1
eq_ide = nb.parse(r"y' + \int_0^t y(\tau) d\tau = t")

# The internal engine transforms \int_0^t y(\tau) d\tau exactly into Y(s)/s.
sol_ide = eq_ide.dsolve(method='laplace')
print(sol_ide)
# Output solves for y(t) with exponential/trig compositions natively!
```

> **Note on Dummy Variables:** Always ensure your integral variable (e.g. $\tau$) is distinct from the free independent variable ($t$). `py-nabla` rigidly protects dummy scopes to prevent mathematical leakage.

## 3. Providing Custom Initial Conditions (ICs)

If you know the initial state of your system, inject it directly to bypass `C_1` generic generation:

```python
from sympy import Function, Symbol

t = Symbol('t')
y = Function('y')

# y'' + y = 0, y(0)=1, y'(0)=0
eq = nb.parse(r"y'' + y = 0")
sol = eq.dsolve(
    initial_conditions={
        y(0): 1,
        y(t).diff(t).subs(t, 0): 0
    }
)
print(sol) # Eq(y(t), cos(t))
```

## 4. Power Series Approximations

When analytical Laplace integration isn't viable (particularly for highly nonlinear equations), `py-nabla` features a built-in fallback router that can approximate the neighborhood using robust Power Series (Taylor/Maclaurin).

```python
# y' = y
eq_nonlinear = nb.parse(r"y' = y")

# Solve via Nth-term approximation
sol_series = eq_nonlinear.dsolve(method='series', series_order=5)

print(sol_series)
# Output: Eq(y(t), C_1 + C_1*t + C_1*t**2/2 + C_1*t**3/6 + C_1*t**4/24 + O(t**5))
```

---

With these capabilities, `py-nabla` bridges the gap between pure symbolic representation and rigid numerical simulation!
