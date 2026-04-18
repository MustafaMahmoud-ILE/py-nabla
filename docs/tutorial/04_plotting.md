# Visualizing Mathematics with py-nabla

py-nabla includes a powerful plotting engine built on top of Matplotlib, designed to create publication-quality visualizations directly from LaTeX expressions.

## 1. 2D Plotting

The `nb.plot()` function is the primary tool for 2D visualization.

```python
import py_nabla as nb
import numpy as np

f = nb.parse(r"\sin(x)")
g = nb.parse(r"\cos(x)")

# Basic plot
nb.plot(f, domain=(-2*np.pi, 2*np.pi))

# Multi-function plot with custom styling
nb.plot(f, g, 
        domain=(-5, 5), 
        labels=["Sine", "Cosine"],
        title="Trigonometric Functions",
        style="publication")
```

## 2. 3D Surface Plotting

Use `nb.plot3d()` for functions of two variables, $f(x, y)$.

```python
f = nb.parse(r"x^2 + y^2")

# Surface plot
nb.plot3d(f, domain_x=(-2, 2), domain_y=(-2, 2), title="Paraboloid")

# Contour plot
nb.plot3d(f, style='contour', colormap='magma')
```

## 3. Parametric Plotting

Parametric curves $(x(t), y(t))$ can be plotted using `nb.plot_parametric()`.

```python
# Unit circle
x_t = nb.parse(r"\cos(t)")
y_t = nb.parse(r"\sin(t)")
nb.plot_parametric(x_t, y_t, domain=(0, 2*np.pi), title="Circle")

# Lissajous Figure
x_l = nb.parse(r"\sin(3t)")
y_l = nb.parse(r"\sin(2t)")
nb.plot_parametric(x_l, y_l, title="Lissajous Figure")
```

## 4. Customizing Aesthetics

You can pass keyword arguments directly to Matplotlib through Nabla's plotting functions.

```python
f = nb.parse(r"x^2")
nb.plot(f, color='red', linestyle='--', linewidth=3)
```

### Plotting Styles
Nabla comes with predefined styles:
- `default`: Standard Matplotlib
- `publication`: High DOI, serif fonts, thick lines
- `minimal`: No top/right spines, clean grid
