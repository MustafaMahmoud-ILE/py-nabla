"""
py-nabla Calculus Demo

Demonstrates parsing, differentiating, and integrating complex
LaTeX expressions, including mixed partials and limits.
"""

import py_nabla as nb

print("=== nabla py-nabla Calculus Demo ===\n")

# 1. Fundamental Theorem of Calculus
f_latex = r"\frac{d}{dx} \int_0^x \sin(t^2) dt"
f = nb.parse(f_latex)
print(f"Expression: {f_latex}")
print(f"Result:     {f.simplify()}")
print("-" * 40)

# 2. Mixed Partial Derivatives
partial_latex = r"\frac{\partial^2}{\partial x \partial y} (x^2 y + y^2 x)"
p = nb.parse(partial_latex)
print(f"Expression: {partial_latex}")
print(f"Result:     {p.simplify()}")
print("-" * 40)

# 3. Limits
limit_latex = r"\lim_{x \to 0} \frac{\sin(x)}{x}"
l = nb.parse(limit_latex)
print(f"Expression: {limit_latex}")
print(f"Result:     {l.evaluate()}")
print("-" * 40)

# 4. Series Expansion
series_latex = r"\exp(x)"
s = nb.parse(series_latex)
expansion = s.series('x', point=0, order=5)
print(f"Expression: {series_latex}")
print(f"Taylor Series (O(x^5)): {expansion}")
print("-" * 40)
