"""
Comprehensive unit tests for the Expression class.

Covers: calculus operations, algebraic operations,
        numerical evaluation, operator overloading, and properties.
"""

import pytest
import numpy as np
from py_nabla import parse, symbols
from py_nabla.core.expression import Expression


# ================================================================
# FIXTURES
# ================================================================

@pytest.fixture
def poly():
    """f(x) = x^2 + 2x + 1"""
    return parse(r"x^2 + 2x + 1")

@pytest.fixture
def trig():
    """f(x) = sin(x)"""
    return parse(r"\sin(x)")


# ================================================================
# BASIC CREATION
# ================================================================

class TestExpressionCreation:

    def test_creation_returns_expression(self):
        f = parse(r"x^2")
        assert isinstance(f, Expression)

    def test_repr_contains_class_name(self):
        f = parse(r"x + 1")
        assert "Expression" in repr(f)

    def test_str_is_sympy_form(self):
        f = parse(r"x + 1")
        assert "x" in str(f)

    def test_latex_source_preserved(self):
        src = r"\int x^2 dx"
        f = parse(src)
        assert f._latex_source == src

    def test_sympy_property(self):
        f = parse(r"x")
        import sympy
        assert isinstance(f.sympy, sympy.Basic)


# ================================================================
# CALCULUS
# ================================================================

class TestDifferentiation:

    @pytest.mark.parametrize("latex,var,expected_sympy", [
        (r"x^2",         'x', "2*x"),
        (r"x^3 + x^2",   'x', "3*x**2 + 2*x"),
        (r"\sin(x)",     'x', "cos(x)"),
        (r"\cos(x)",     'x', "-sin(x)"),
        (r"\ln(x)",      'x', "1/x"),
    ])
    def test_first_derivative(self, latex, var, expected_sympy):
        import sympy
        f = parse(latex)
        df = f.diff(var)
        # Check algebraic equality by simplifying the difference
        expected = sympy.sympify(expected_sympy)
        diff_expr = sympy.simplify(df._expr - expected)
        assert diff_expr == 0, (
            f"Got {df._expr}, expected {expected}, difference: {diff_expr}"
        )

    def test_second_derivative(self):
        f = parse(r"x^4")
        d2f = f.diff('x', order=2)
        assert str(d2f) == "12*x**2"

    def test_third_derivative(self):
        f = parse(r"x^3")
        d3f = f.diff('x', order=3)
        assert abs(float(str(d3f)) - 6.0) < 1e-10

    def test_diff_returns_expression(self):
        f = parse(r"x^2")
        assert isinstance(f.diff('x'), Expression)


class TestIntegration:

    @pytest.mark.parametrize("latex,var,expected_sympy", [
        (r"x",           'x', "x**2/2"),
        (r"\sin(x)",     'x', "-cos(x)"),
        (r"\cos(x)",     'x', "sin(x)"),
    ])
    def test_indefinite_integral(self, latex, var, expected_sympy):
        import sympy
        f = parse(latex)
        F = f.integrate(var)
        expected = sympy.sympify(expected_sympy)
        diff_expr = sympy.simplify(F._expr - expected)
        assert diff_expr == 0, (
            f"Got {F._expr}, expected {expected}, difference: {diff_expr}"
        )

    def test_definite_integral(self):
        f = parse(r"x")
        area = f.integrate('x', limits=(0, 2))
        assert float(area.evaluate()) == pytest.approx(2.0)

    def test_integral_of_constant(self):
        f = parse(r"1")
        F = f.integrate('x', limits=(0, 5))
        assert float(F.evaluate()) == pytest.approx(5.0)


class TestLimits:

    def test_limit_at_zero(self):
        f = parse(r"x^2")
        lim = f.limit('x', 0)
        assert float(lim.evaluate()) == pytest.approx(0.0)

    def test_classic_sinc_limit(self):
        f = parse(r"\frac{\sin(x)}{x}")
        lim = f.limit('x', 0)
        assert float(lim.evaluate()) == pytest.approx(1.0)

    def test_limit_at_infinity(self):
        f = parse(r"\frac{1}{x}")
        lim = f.limit('x', 'oo')
        assert float(lim.evaluate()) == pytest.approx(0.0)


class TestSeries:

    def test_series_returns_expression(self):
        f = parse(r"\sin(x)")
        s = f.series('x', order=5)
        assert isinstance(s, Expression)

    def test_sin_series_contains_x(self):
        f = parse(r"\sin(x)")
        s = f.series('x', order=3)
        assert 'x' in str(s)


# ================================================================
# ALGEBRAIC OPERATIONS
# ================================================================

class TestAlgebra:

    def test_simplify(self):
        f = parse(r"x^2 - x^2 + 1")
        result = f.simplify()
        assert str(result) == "1"

    def test_expand(self):
        f = parse(r"(x + 1)^2")
        expanded = f.expand()
        s = str(expanded)
        assert "x**2" in s
        assert "2*x" in s
        assert "1" in s

    def test_factor(self):
        f = parse(r"x^2 - 1")
        factored = f.factor()
        s = str(factored)
        assert "(x - 1)" in s or "(x + 1)" in s

    def test_solve_quadratic(self):
        eq = parse(r"x^2 - 4")
        solutions = eq.solve('x')
        values = sorted([float(s.evaluate()) for s in solutions])
        assert values == pytest.approx([-2.0, 2.0])

    def test_solve_linear(self):
        eq = parse(r"2x - 6")
        solutions = eq.solve('x')
        assert float(solutions[0].evaluate()) == pytest.approx(3.0)

    def test_solve_auto_detect_variable(self):
        eq = parse(r"x - 5")
        solutions = eq.solve()
        assert float(solutions[0].evaluate()) == pytest.approx(5.0)


# ================================================================
# NUMERICAL EVALUATION
# ================================================================

class TestNumericalEval:

    def test_scalar_float(self):
        f = parse(r"x^2 + 1")
        assert f.evaluate(x=2) == pytest.approx(5.0)

    def test_scalar_zero(self):
        f = parse(r"x^2")
        assert f.evaluate(x=0) == pytest.approx(0.0)

    def test_keyword_substitution(self):
        f = parse(r"x + y")
        assert f.evaluate(x=3, y=4) == pytest.approx(7.0)

    def test_dict_substitution(self):
        f = parse(r"x + 1")
        from sympy import Symbol
        assert f.evaluate(substitutions={Symbol('x'): 5}) == pytest.approx(6.0)

    def test_numpy_array_vectorised(self):
        f = parse(r"x^2")
        x = np.array([1.0, 2.0, 3.0])
        y = f.evaluate(x=x)
        np.testing.assert_allclose(y, np.array([1.0, 4.0, 9.0]))

    def test_evaluate_returns_remaining_expr(self):
        f = parse(r"x^2 + y^2")
        result = f.evaluate(x=3)  # y still free
        assert isinstance(result, Expression)

    def test_complex_result(self):
        f = parse(r"x^2 + 1")
        # x = i -> i^2 + 1 = -1 + 1 = 0
        import sympy
        result = f.evaluate(substitutions={sympy.Symbol('x'): sympy.I})
        assert result == pytest.approx(0.0)


class TestLambdify:

    def test_lambdify_creates_callable(self):
        f = parse(r"x^2")
        func = f.lambdify(['x'])
        assert callable(func)

    def test_lambdify_scalar(self):
        f = parse(r"x^2 + 1")
        func = f.lambdify(['x'])
        assert func(3) == pytest.approx(10.0)

    def test_lambdify_numpy(self):
        f = parse(r"x^2")
        func = f.lambdify(['x'])
        x = np.linspace(0, 2, 5)
        np.testing.assert_allclose(func(x), x**2)

    def test_lambdify_multivariable(self):
        f = parse(r"x^2 + y^2")
        func = f.lambdify(['x', 'y'])
        assert func(3, 4) == pytest.approx(25.0)


# ================================================================
# OPERATOR OVERLOADING
# ================================================================

class TestOperators:

    def test_add_expressions(self):
        f = parse(r"x")
        g = parse(r"y")
        h = f + g
        assert isinstance(h, Expression)
        assert "x" in str(h) and "y" in str(h)

    def test_add_scalar(self):
        f = parse(r"x")
        h = f + 5
        assert "x" in str(h)

    def test_radd(self):
        f = parse(r"x")
        h = 5 + f
        assert isinstance(h, Expression)

    def test_sub_expressions(self):
        f = parse(r"x")
        g = parse(r"y")
        h = f - g
        assert str(h) == "x - y"

    def test_mul_expressions(self):
        f = parse(r"x")
        g = parse(r"y")
        h = f * g
        assert str(h) == "x*y"

    def test_mul_scalar(self):
        f = parse(r"x")
        h = 3 * f
        assert isinstance(h, Expression)

    def test_truediv(self):
        f = parse(r"x")
        g = parse(r"y")
        h = f / g
        assert "x" in str(h) and "y" in str(h)

    def test_pow(self):
        f = parse(r"x")
        h = f ** 3
        assert str(h) == "x**3"

    def test_neg(self):
        f = parse(r"x")
        h = -f
        assert str(h) == "-x"

    def test_chained(self):
        f = parse(r"x")
        result = 2 * f**2 + 3 * f - 1
        assert isinstance(result, Expression)


# ================================================================
# RENDERING
# ================================================================

class TestRendering:

    def test_raw_latex(self):
        f = parse(r"x^2")
        raw = f.latex(mode='raw')
        assert '\\' in raw or 'x' in raw

    def test_inline_latex(self):
        f = parse(r"x^2")
        inline = f.latex(mode='inline')
        assert inline.startswith('$') and inline.endswith('$')

    def test_display_latex(self):
        f = parse(r"x^2")
        display = f.latex(mode='display')
        assert display.startswith('$$') and display.endswith('$$')

    def test_jupyter_hook(self):
        f = parse(r"x^2")
        r = f._repr_latex_()
        assert r.startswith('$$')


# ================================================================
# PROPERTIES
# ================================================================

class TestProperties:

    def test_free_symbols(self):
        f = parse(r"x^2 + y")
        names = {str(s) for s in f.free_symbols}
        assert 'x' in names
        assert 'y' in names

    def test_is_number_true(self):
        f = parse(r"42")
        assert f.is_number is True

    def test_is_number_false(self):
        f = parse(r"x + 1")
        assert f.is_number is False

    def test_complexity_positive(self):
        f = parse(r"x^2 + y^2 + z^2")
        assert f.complexity > 0
