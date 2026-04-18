# Linear Algebra with py-nabla

py-nabla provides first-class support for matrix environments and linear algebra operations directly from LaTeX.

## 1. Matrix Creation

Nabla supports standard LaTeX matrix environments: `bmatrix`, `pmatrix`, `vmatrix`, `Bmatrix`, and `matrix`.

```python
import py_nabla as nb

# Square matrix
A = nb.parse(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}")

# Identity/Numeric matrix
B = nb.parse(r"\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}")
```

## 2. Basic Operations

### Matrix Multiplication
```python
C = nb.parse(r"\begin{bmatrix} 1 & 2 \end{bmatrix}")
D = nb.parse(r"\begin{bmatrix} 3 \\ 4 \end{bmatrix}")
print(C * D) # Matrix([[11]])
```

### Trace and Determinant
```python
M = nb.parse(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")

# Using LaTeX commands
det_M = nb.parse(r"\det \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
print(det_M.evaluate()) # -2.0

tr_M = nb.parse(r"\tr \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
print(tr_M.evaluate()) # 5.0
```

## 3. Vectors and Nabla Operator

### Vector Notation
```python
v = nb.parse(r"\vec{v}")
u = nb.parse(r"\mathbf{u}")
```

### Nabla Operations
Nabla supports gradient, divergence, and curl notation.

```python
# Gradient
grad = nb.parse(r"\nabla f")
print(grad) # grad(f)

# Laplacian
laplacian = nb.parse(r"\nabla^2 (x^2 + y^2)")
print(laplacian.simplify()) # 4
```

## 4. Piecewise Functions

Complex piecewise definitions are handled via the `cases` environment.

```python
f = nb.parse(r"""
\begin{cases}
  0 & x < 0 \\
  1 & x \geq 0
\end{cases}
""")

print(f.evaluate(x=-1)) # 0
print(f.evaluate(x=1))  # 1
```
