"""
py-nabla Plotting Demo

Demonstrates 2D, 3D, and parametric plotting capabilities.
"""

import py_nabla as nb
import numpy as np

# Note: This script requires matplotlib (pip install py-nabla[plotting])
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Skipping plotting demo: matplotlib not installed.")
    exit(0)

print("=== nabla py-nabla Rendering Demo ===\n")

# 1. Standard 2D Plot
f1 = nb.parse(r"\sin(x)")
f2 = nb.parse(r"\cos(x)")
print("Generating 2D plot of sin(x) and cos(x)...")
nb.plot(f1, f2, domain=(-np.pi, np.pi), labels=["Sine", "Cosine"], show=False, save="docs/media/plot_2d.png")

# 2. 3D Surface Plot
f3d = nb.parse(r"x^2 + y^2")
print("Generating 3D surface plot of x^2 + y^2...")
nb.plot3d(f3d, domain_x=(-5, 5), domain_y=(-5, 5), title="Paraboloid", show=False, save="docs/media/plot_3d.png")

# 3. Parametric Plot (Lissajous Figure)
x_t = nb.parse(r"\sin(3t)")
y_t = nb.parse(r"\sin(2t)")
print("Generating parametric plot...")
nb.plot_parametric(x_t, y_t, domain=(0, 2*np.pi), title="Lissajous Figure", show=False, save="docs/media/plot_parametric.png")

print("\nPlots saved to docs/media/")
