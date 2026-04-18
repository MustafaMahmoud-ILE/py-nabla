"""
py-nabla Linear Algebra Demo

Demonstrates matrix environments, determinants, and vector operations.
"""

import py_nabla as nb

print("=== nabla py-nabla Linear Algebra Demo ===\n")

# 1. Matrix Inversion and Determinant
matrix_latex = r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}"
A = nb.parse(matrix_latex)
print(f"Matrix A:  {matrix_latex}")
print(f"Determinant: {nb.parse(r'\\det' + matrix_latex).simplify()}")
print("-" * 40)

# 2. Matrix Multiplication
B = nb.parse(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
C = nb.parse(r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}")
result = B * C
print(f"B * C = {result}")
print("-" * 40)

# 3. Piecewise Functions (Cases)
piecewise_latex = r"""
\begin{cases} 
  x^2 & x < 0 \\ 
  x   & x \geq 0 
\end{cases}
"""
f = nb.parse(piecewise_latex)
print(f"Piecewise Function: {piecewise_latex}")
print(f"f(-2) = {f.evaluate(x=-2)}")
print(f"f( 2) = {f.evaluate(x=2)}")
print("-" * 40)
