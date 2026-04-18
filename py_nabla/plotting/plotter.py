import matplotlib.pyplot as plt
import numpy as np
from typing import Union, Tuple, List

def plot(expression, 
         range_tuple: Tuple[str, float, float], 
         points: int = 100, 
         title: str = None,
         **kwargs):
    """
    Plots a Nabla Expression over a specified range.
    
    Args:
        expression: Nabla Expression
        range_tuple: (variable_name, start, end)
        points: Number of points for the plot
        title: Plot title
    """
    var_name, start, end = range_tuple
    
    # Vectorize the expression
    f_np = expression.to_numpy([var_name])
    
    # Generate data
    x = np.linspace(start, end, points)
    y = f_np(x)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, **kwargs)
    
    if title:
        plt.title(title)
    else:
        plt.title(f"$f({var_name}) = {expression.latex()}$")
        
    plt.xlabel(f"${var_name}$")
    plt.grid(True, alpha=0.3)
    
    return plt.gcf()
