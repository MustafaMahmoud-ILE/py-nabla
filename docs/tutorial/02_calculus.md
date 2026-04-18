# Calculus Cookbook with py-nabla

This guide covers advanced calculus operations using py-nabla's LaTeX-first engine.

## 1. Differentiation

Nabla supports ordinary and partial derivatives with various notations.

### Ordinary Derivatives
```python
import py_nabla as nb

# Parse Leibniz notation
f = nb.parse(r"\frac{d}{dx} \sin(x^2)")
print(f.simplify()) # 2*x*cos(x**2)
```

### Partial Derivatives
```python
# Multivariable derivative
f = nb.parse(r"\frac{\partial}{\partial x} (x^2 y + y^2)")
print(f.simplify()) # 2*x*y
```

### Mixed Partials
```python
f = nb.parse(r"\frac{\partial^2}{\partial x \partial y} (x^2 y^3)")
print(f.simplify()) # 6*x*y**2
```

## 2. Integration

Nabla can compute both indefinite and definite integrals.

### Indefinite Integrals
```python
f = nb.parse(r"\int \cos(x) dx")
print(f.simplify()) # sin(x)
```

### Definite Integrals
```python
# Integral from 0 to pi of sin(x)
f = nb.parse(r"\int_0^\pi \sin(x) dx")
print(f.evaluate()) # 2.0
```

## 3. Limits and Series

### Limits
```python
# Limit at infinity
f = nb.parse(r"\lim_{x \to \infty} \frac{1}{x}")
print(f.evaluate()) # 0.0

# One-sided limits
f = nb.parse(r"\lim_{x \to 0^+} \frac{1}{x}")
print(f.evaluate()) # inf (oo)
```

### Taylor Series
```python
f = nb.parse(r"\ln(1+x)")
# Expand around 0, up to order 4
print(f.series('x', point=0, order=4))
# x - x**2/2 + x**3/3 + O(x**4)
```

## 4. Summations and Products

```python
# Finite summation
sum_expr = nb.parse(r"\sum_{i=1}^{10} i")
print(sum_expr.evaluate()) # 55.0

# Infinite product (symbolic)
prod_expr = nb.parse(r"\prod_{n=1}^{\infty} x^n")
```
