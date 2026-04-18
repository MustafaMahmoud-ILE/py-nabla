"""
py-nabla Rendering Styles Demo

Demonstrates the custom NablaLatexPrinter with different derivative styles
and output modes (inline, display, equation, align).
"""

import py_nabla as nb

print("=== nabla py-nabla Rendering Demo ===\n")

# Use a complex multivariable function
f = nb.parse(r"f(x, t) = \sin(kx - \omega t)")

# 1. Leibniz Style (Default) - Standard for Calculus
print("--- Leibniz Style (Default) ---")
df_x = f.diff('x')
print(f"df/dx: {nb.render_latex(df_x, derivative_style='leibniz')}")

# 2. Prime Style - Compact for single variable
print("\n--- Prime Style ---")
print(f"f': {nb.render_latex(df_x, derivative_style='prime')}")

# 3. Dot Style - Newton's notation for time derivatives
print("\n--- Dot Style (Newton) ---")
df_t = f.diff('t')
print(f"df/dt: {nb.render_latex(df_t, derivative_style='dot')}")

# 4. Output Modes
print("\n--- Output Modes ---")
print(f"Inline ($...$):  {nb.render_latex(f, mode='inline')}")
print(f"Display ($$...$$): {nb.render_latex(f, mode='display')}")
print(f"Equation Env:    \n{nb.render_latex(f, mode='equation', label='eq:wave')}")
