import pytest
from py_nabla import parse
from py_nabla.solvers.solver_exceptions import NablaSolveError

def test_first_order_linear():
    """y' + y = 0 => Laplace should yield constants."""
    eq = parse(r"y' + y = 0")
    sol = eq.dsolve(method='laplace')
    assert "C_1" in str(sol.sympy)

def test_second_order_linear():
    """y'' + y = 0 => harmonic oscillator."""
    eq = parse(r"y'' + y = 0")
    sol = eq.dsolve(method='laplace')
    # Should contain C_1 and C_2 with sin and cos
    assert "C_1" in str(sol.sympy)
    assert "C_2" in str(sol.sympy)
    assert "sin" in str(sol.sympy) or "cos" in str(sol.sympy)

def test_laplace_fallback():
    """y' = y^2 is nonlinear and laplace should fail and fallback to analytical."""
    eq = parse(r"y' = y^2")
    # Will throw UserWarning on fallback
    with pytest.warns(UserWarning):
        sol = eq.dsolve(method='laplace')
    assert "y" in str(sol.sympy)

def test_series_solution():
    """Test nth term taylor expansion."""
    eq = parse(r"y' = y")
    sol = eq.dsolve(method='series', series_order=3)
    # Series includes O(t**3)
    assert "O" in str(sol.sympy)

def test_dummy_variable_scoping():
    """Ensure integration limits are bound."""
    eq1 = parse(r"\int_0^t y(\tau) d\tau")
    # Should not evaluate automatically
    assert "Integral" in str(eq1.sympy)

def test_integro_differential():
    """y'(t) + \int y(\tau) d\tau = 0"""
    eq = parse(r"y' + \int_0^t y(\tau) d\tau = 0")
    sol = eq.dsolve(method='laplace')
    assert "C" in str(sol.sympy)
