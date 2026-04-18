"""
Verification script for all tutorial snippets in docs/tutorial/*.md
"""
import py_nabla as nb
import numpy as np
import sympy

def verify_all():
    print("--- Verifying 01_getting_started.md ---")
    f = nb.parse(r"x^2 + 2x + 1")
    g = nb.parse(r"(x + 1)^2")
    assert str(g.expand()) == "x**2 + 2*x + 1"
    h = nb.parse(r"\frac{x^2 - 1}{x - 1}")
    assert str(h.simplify()) == "x + 1"
    eq = nb.parse(r"x^2 - 4 = 0")
    sols = eq.solve('x')
    assert len(sols) == 2
    
    print("--- Verifying 02_calculus.md ---")
    df = nb.parse(r"\frac{d}{dx} \sin(x^2)")
    assert str(df.simplify()) == "2*x*cos(x**2)"
    pf = nb.parse(r"\frac{\partial}{\partial x} (x^2 y + y^2)")
    assert str(pf.simplify()) == "2*x*y"
    F = nb.parse(r"\int \cos(x) dx")
    assert str(F.simplify()) == "sin(x)"
    area = nb.parse(r"\int_0^\pi \sin(x) dx")
    assert float(area.evaluate()) == pytest_approx(2.0)
    
    print("--- Verifying 03_linear_algebra.md ---")
    C = nb.parse(r"\begin{bmatrix} 1 & 2 \end{bmatrix}")
    D = nb.parse(r"\begin{bmatrix} 3 \\ 4 \end{bmatrix}")
    assert str(C * D) == "Matrix([[11]])"
    det_M = nb.parse(r"\det \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
    assert float(det_M.evaluate()) == pytest_approx(-2.0)
    laplacian = nb.parse(r"\nabla^2 (x^2 + y^2)")
    assert int(laplacian.simplify()) == 4
    cases_f = nb.parse(r"\begin{cases} 0 & x < 0 \\ 1 & x \geq 0 \end{cases}")
    assert cases_f.evaluate(x=-1) == 0
    assert cases_f.evaluate(x=1) == 1

    print("\n✅ All tutorial snippets verified successfully!")

def pytest_approx(val):
    from pytest import approx
    return approx(val)

if __name__ == "__main__":
    try:
        verify_all()
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
