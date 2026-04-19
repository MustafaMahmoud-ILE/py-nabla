# Fractional Calculus with py-nabla

`py-nabla` v1.1.0 introduces full support for **Fractional Calculus**. You can now parse and solve equations involving derivatives of non-integer order (e.g., $d^{1/2}/dt^{1/2}$), which are widely used in modeling viscoelastic materials, anomalous diffusion, and signal processing.

## 1. Notation Support

`py-nabla` supports multiple LaTeX notations for fractional differentiation:

- **Fractional Leibniz**: `\frac{d^{1/2}}{dt^{1/2}} y` $\to \frac{d^{1/2}}{dt^{1/2}} y$
- **Fractional Prime**: `y^{(0.5)}` $\to y^{(0.5)}$ or `y^{(1/2)}`

## 2. Mathematical Definition: Caputo

By default, the engine uses the **Caputo** definition of the fractional derivative:
$$^C D_t^\alpha f(t) = \frac{1}{\Gamma(n-\alpha)} \int_0^t (t-\tau)^{n-\alpha-1} f^{(n)}(\tau) d\tau$$
where $n = \lceil \alpha \rceil$.

This definition is chosen for its engineering robustness, as it allows for the use of standard, physically meaningful initial conditions ($y(0), y'(0), \dots$) in Laplace transform methods.

## 3. Solving Fractional Differential Equations (FDEs)

You can solve FDEs analytically using the built-in Laplace engine. 

### Example: Fractional Relaxation Equation
The fractional relaxation equation is a classic benchmark. For $\alpha=1/2$:
$$\frac{d^{1/2}}{dt^{1/2}} y + y = 0, \quad y(0) = 1$$

```python
import py_nabla as nb

# Parse the equation
eq = nb.parse(r"\frac{d^{1/2}}{dt^{1/2}} y + y = 0")

# Solve with initial conditions
solution = eq.dsolve(ics={nb.parse(r"y(0)"): 1})

print(f"Solution: {solution.sympy}")
# Output: Eq(y(t), exp(t)*erfc(sqrt(t)))
```

## 4. Why use Fractional Calculus?

- **Memory Effects**: Standard derivatives are local; fractional derivatives carry the "history" of the process (the integral kernel).
- **Viscoelasticity**: Better modeling of polymers and biological tissues compared to standard spring-dashpot models.
- **Anomalous Diffusion**: Useful in physics for non-Gaussian diffusion processes.

---

With `py-nabla`, you have a world-class fractional engine in your pocket, powered by high-fidelity LaTeX parsing and SymPy's symbolic rigor.
