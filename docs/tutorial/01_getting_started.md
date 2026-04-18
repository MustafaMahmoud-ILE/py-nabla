# Getting Started with py-nabla

Welcome to **py-nabla**, the mathematical computing engine that speaks LaTeX. This tutorial will walk you through the core concepts of the library.

## 1. The Core Concept: `nb.parse()`

Everything in py-nabla starts with a LaTeX string. The `parse` function (aliased as `expr`) converts any valid LaTeX expression into a high-powered `Expression` object.

```python
import py_nabla as nb

f = nb.parse(r"x^2 + 2x + 1")
```

## 2. Symbolic Manipulation

Because Nabla is powered by SymPy, you can perform analytical operations directly on the expression.

### Simplification & Expansion
```python
g = nb.parse(r"(x + 1)^2")
print(g.expand())   # x**2 + 2*x + 1

h = nb.parse(r"\frac{x^2 - 1}{x - 1}")
print(h.simplify()) # x + 1
```

### Solving Equations
You can solve for variables automatically:
```python
eq = nb.parse(r"x^2 - 4 = 0")
solutions = eq.solve('x') # [Expression(-2), Expression(2)]
```

## 3. Calculus

Nabla handles complex calculus notation effortlessly.

```python
# Differentiation
df = nb.parse(r"\frac{d}{dx} \sin(x)")
print(df.simplify()) # cos(x)

# Integration
F = nb.parse(r"\int x^2 dx")
print(F.simplify()) # x**3/3
```

## 4. Numerical Evaluation

Convert your symbolic expressions into numbers or NumPy arrays.

```python
f = nb.parse(r"x^2")

# Scalar evaluation
val = f.evaluate(x=3.0) # 9.0

# Vectorised evaluation
import numpy as np
x_array = np.linspace(0, 10, 100)
y_array = f.evaluate(x=x_array)
```

## Next Steps
Now that you know the basics, check out the [Calculus Cookbook](02_calculus.md) or [Plotting Mastery](04_plotting.md).
