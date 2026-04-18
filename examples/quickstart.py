from nabla import expr, symbols, render, plot
import matplotlib.pyplot as plt

def demo():
    print("=== Nabla Quickstart Demo ===")
    
    # 1. Parsing and Symbolic Manipulation
    print("\n1. Parsing LaTeX:")
    f = expr(r"\frac{d}{dx}(x^2 \sin(x))")
    print(f"Input LaTeX: {f.latex()}")
    
    simplified = f.simplify()
    print(f"Simplified (SymPy): {simplified}")
    print(f"Simplified LaTeX: {simplified.latex()}")

    # 2. Integration
    print("\n2. Definite Integral:")
    g = expr(r"\int_0^\pi \sin(x) dx")
    result = g.evaluate()
    print(fr"Result of \int_0^\pi \sin(x) dx: {result}")

    # 3. Numeric Evaluation and Lazy Evaluation
    print("\n3. Numeric Substitution:")
    h = expr(r"x^2 + 2x + 1")
    lazy = h.evaluate(x=symbols('y'))
    print(f"Evaluated with y: {lazy} (Type: {type(lazy)})")
    
    float_val = h.evaluate(x=1.5)
    print(f"Evaluated at x=1.5: {float_val} (Type: {type(float_val)})")

    # 4. Plotting
    print("\n4. Generating Plot (plotting/demo.png)...")
    p = expr(r"\sin(x) + \frac{1}{2}\cos(2x)")
    fig = plot(p, ('x', -2*3.14, 2*3.14), color='teal', linewidth=2)
    plt.savefig('nabla_demo_plot.png')
    print("Plot saved as nabla_demo_plot.png")

if __name__ == "__main__":
    demo()
