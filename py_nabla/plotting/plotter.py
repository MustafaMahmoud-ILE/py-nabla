"""
Plotting utilities for py-nabla mathematical expressions.

Provides 2D, 3D, and parametric plotting with publication-ready defaults.
Requires: pip install py-nabla[plotting]  (matplotlib)
"""

from typing import Union, List, Optional, Tuple, Callable
import numpy as np


def _ensure_matplotlib():
    """Raise a helpful error if matplotlib is not installed."""
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        raise ImportError(
            "Plotting requires matplotlib.\n"
            "Install with:  pip install py-nabla[plotting]\n"
            "or:            pip install matplotlib"
        )


def _eval(expr, var_map: dict) -> np.ndarray:
    """Evaluate a py-nabla Expression or callable with given variable map."""
    from py_nabla.core.expression import Expression
    if isinstance(expr, Expression):
        return np.array(expr.evaluate(**var_map), dtype=float)
    elif callable(expr):
        return expr(*var_map.values())
    raise TypeError(f"Expected Expression or callable, got {type(expr).__name__}")


# ================================================================
# PLOT STYLES
# ================================================================

STYLES = {
    "default": {},
    "publication": {
        "figure.dpi": 150,
        "font.family": "serif",
        "font.size": 12,
        "axes.linewidth": 1.2,
        "lines.linewidth": 2.0,
        "grid.alpha": 0.3,
    },
    "minimal": {
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.2,
    },
}


def _apply_style(plt, style: str):
    """Apply a named style dict via rcParams."""
    params = STYLES.get(style, {})
    plt.rcParams.update(params)


# ================================================================
# 2D PLOT
# ================================================================

def plot(
    *expressions: Union["Expression", Callable],  # type: ignore[name-defined]
    domain: Optional[Tuple[float, float]] = None,
    var: str = "x",
    num_points: int = 1000,
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    style: str = "default",
    grid: bool = True,
    legend: bool = True,
    figsize: Tuple[float, float] = (10, 6),
    save: Optional[str] = None,
    show: bool = True,
    **kwargs,
):
    """
    Plot one or more mathematical functions in 2D.

    Args:
        *expressions: py-nabla Expression objects or callables.
        domain      : ``(x_min, x_max)`` range (default: ``(-10, 10)``).
        var         : Name of the independent variable (default: ``'x'``).
        num_points  : Number of evaluation points (default: 1000).
        labels      : Legend labels for each function.
        title       : Plot title.
        xlabel      : X-axis label (default: variable name).
        ylabel      : Y-axis label.
        style       : ``'default'`` | ``'publication'`` | ``'minimal'``.
        grid        : Show grid (default: ``True``).
        legend      : Show legend when multiple functions plotted.
        figsize     : Figure size in inches.
        save        : File path to save the figure (e.g. ``'plot.png'``).
        show        : Display figure interactively (default: ``True``).
        **kwargs    : Extra keyword arguments forwarded to ``ax.plot()``.

    Returns:
        ``matplotlib.figure.Figure``

    Examples:
        >>> import py_nabla as nb
        >>> import numpy as np
        >>> f = nb.parse(r"\\sin(x)")
        >>> g = nb.parse(r"\\cos(x)")
        >>> nb.plot(f, g, domain=(0, 2*np.pi), labels=["sin", "cos"])
    """
    plt = _ensure_matplotlib()
    _apply_style(plt, style)

    dom = domain if domain is not None else (-10.0, 10.0)
    x_vals = np.linspace(dom[0], dom[1], num_points)

    fig, ax = plt.subplots(figsize=figsize)

    for i, expr in enumerate(expressions):
        y_vals = _eval(expr, {var: x_vals})

        label_i = None
        if labels and i < len(labels):
            label_i = labels[i]
        elif len(expressions) > 1:
            label_i = f"f_{i+1}"

        ax.plot(x_vals, y_vals, label=label_i, **kwargs)

    ax.set_xlabel(xlabel or var, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)
    if grid:
        ax.grid(True, alpha=0.3)
    if legend and len(expressions) > 1:
        ax.legend(fontsize=10)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig


# ================================================================
# 3D SURFACE PLOT
# ================================================================

def plot3d(
    expression: Union["Expression", Callable],  # type: ignore[name-defined]
    domain_x: Tuple[float, float] = (-5.0, 5.0),
    domain_y: Tuple[float, float] = (-5.0, 5.0),
    var_x: str = "x",
    var_y: str = "y",
    num_points: int = 60,
    title: Optional[str] = None,
    style: str = "surface",
    colormap: str = "viridis",
    figsize: Tuple[float, float] = (10, 8),
    save: Optional[str] = None,
    show: bool = True,
    **kwargs,
):
    """
    Create a 3D surface plot of a function f(x, y).

    Args:
        expression : py-nabla Expression or callable ``f(x, y)``.
        domain_x   : ``(x_min, x_max)`` (default: ``(-5, 5)``).
        domain_y   : ``(y_min, y_max)`` (default: ``(-5, 5)``).
        var_x      : X variable name (default: ``'x'``).
        var_y      : Y variable name (default: ``'y'``).
        num_points : Grid resolution per axis (default: 60).
        title      : Plot title.
        style      : ``'surface'`` | ``'wireframe'`` | ``'contour'``.
        colormap   : Matplotlib colormap name (default: ``'viridis'``).
        figsize    : Figure size in inches.
        save       : File path to save figure.
        show       : Display interactively.
        **kwargs   : Extra keyword arguments to Axes3D plot call.

    Returns:
        ``matplotlib.figure.Figure``

    Examples:
        >>> f = nb.parse(r"x^2 + y^2")
        >>> nb.plot3d(f, domain_x=(-2, 2), domain_y=(-2, 2))
    """
    plt = _ensure_matplotlib()
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    x = np.linspace(domain_x[0], domain_x[1], num_points)
    y = np.linspace(domain_y[0], domain_y[1], num_points)
    X, Y = np.meshgrid(x, y)

    from py_nabla.core.expression import Expression
    if isinstance(expression, Expression):
        Z = expression.evaluate(**{var_x: X, var_y: Y})
    elif callable(expression):
        Z = expression(X, Y)
    else:
        raise TypeError(f"Expected Expression or callable, got {type(expression).__name__}")

    Z = np.array(Z, dtype=float)

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    if style == "surface":
        surf = ax.plot_surface(X, Y, Z, cmap=colormap, **kwargs)
        fig.colorbar(surf, shrink=0.5)
    elif style == "wireframe":
        ax.plot_wireframe(X, Y, Z, **kwargs)
    elif style == "contour":
        ax.contour3D(X, Y, Z, 50, cmap=colormap, **kwargs)
    else:
        raise ValueError(f"Unknown style: {style!r}. Choose 'surface', 'wireframe', or 'contour'.")

    ax.set_xlabel(var_x, fontsize=12)
    ax.set_ylabel(var_y, fontsize=12)
    ax.set_zlabel(f"f({var_x},{var_y})", fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)

    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig


# ================================================================
# PARAMETRIC PLOT
# ================================================================

def plot_parametric(
    x_expr: Union["Expression", Callable],  # type: ignore[name-defined]
    y_expr: Union["Expression", Callable],
    domain: Tuple[float, float] = (0.0, 6.283185307179586),  # 0 to 2π
    var: str = "t",
    num_points: int = 1000,
    title: Optional[str] = None,
    figsize: Tuple[float, float] = (8, 8),
    save: Optional[str] = None,
    show: bool = True,
    **kwargs,
):
    """
    Plot a parametric curve (x(t), y(t)).

    Args:
        x_expr     : Expression or callable for x coordinate.
        y_expr     : Expression or callable for y coordinate.
        domain     : Parameter range ``(t_min, t_max)`` (default: ``[0, 2π]``).
        var        : Parameter variable name (default: ``'t'``).
        num_points : Evaluation points (default: 1000).
        title      : Plot title.
        figsize    : Figure size.
        save       : Save path.
        show       : Display interactively.
        **kwargs   : Extra keyword arguments to ``ax.plot()``.

    Returns:
        ``matplotlib.figure.Figure``

    Examples:
        >>> # Unit circle
        >>> x = nb.parse(r"\\cos(t)")
        >>> y = nb.parse(r"\\sin(t)")
        >>> nb.plot_parametric(x, y, domain=(0, 2*np.pi))

        >>> # Lissajous figure
        >>> x = nb.parse(r"\\sin(3t)")
        >>> y = nb.parse(r"\\sin(2t)")
        >>> nb.plot_parametric(x, y)
    """
    plt = _ensure_matplotlib()

    t_vals = np.linspace(domain[0], domain[1], num_points)
    x_vals = _eval(x_expr, {var: t_vals})
    y_vals = _eval(y_expr, {var: t_vals})

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x_vals, y_vals, **kwargs)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    if title:
        ax.set_title(title, fontsize=14)

    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
    if show:
        plt.show()

    return fig
