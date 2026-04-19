import pytest
from py_nabla import expr, NablaExpression
from py_nabla.core.exceptions import NablaParseError
from sympy import simplify, sympify, pi, oo, Rational, symbols, powsimp

def test_deep_nesting():
    """Test multiple levels of fractions and radicals."""
    latex = r"\sqrt{\frac{1}{\sqrt{\frac{1}{x}}}}"
    x_sym = symbols('x')
    result = expr(latex)
    # Check value at x=16 (should be 2.0)
    assert abs(result.evaluate({x_sym: 16}) - 2.0) < 1e-10, f"Failed deep nesting: got {result._expr}"

def test_lazy_latex_parsing():
    """Test brace-less exponents and fractions."""
    # x^12 should become x^{12}
    assert expr(r"x^12")._expr == sympify("x**12")
    # \frac12 should become \frac{1}{2}
    assert expr(r"\frac12")._expr == sympify("1/2")

def test_greek_variants():
    """Test various greek letter cases."""
    latex = r"\alpha + \beta + \gamma = \pi"
    result = expr(latex)
    assert "Eq(alpha + beta + gamma, pi)" in str(result._expr)

def test_infinity_parsing():
    """Test infinity symbol support."""
    latex = r"\int_0^\infty e^{-x} dx"
    result = expr(latex)
    # Integral of e^-x from 0 to inf is 1
    assert result.evaluate() == 1.0 or result.evaluate() == 1

def test_mismatched_delimiters():
    """Test that malformed LaTeX raises NablaParseError."""
    # This should trigger an UnexpectedEOF or UnexpectedToken
    with pytest.raises(NablaParseError):
        expr(r"\frac{1}{2") 

def test_complex_calculus():
    """Stress test with nested calculus operators."""
    # d/dx sin(x^2) = 2x cos(x^2)
    latex = r"\frac{d}{dx} \sin(x^2)"
    result = expr(latex)
    assert "2*x*cos(x**2)" in str(result.simplify())

def test_multi_character_splitting():
    """Test implicit multiplication of multi-character strings.

    'weight' preprocesses into 'w*e*i*g*h*t'.
    'e' maps to Euler's number E; all other letters remain plain symbols.
    SymPy sorts multiplicands alphabetically, so result is 2*E*g*h*i*t*w.
    """
    f = expr(r"2weight")
    result_str = str(f._expr)
    # E (Euler's number) must be present — confirms 'e' → E mapping
    assert "E" in result_str
    # The remaining letters (g, h, i, t, w) must all appear
    for letter in ("g", "h", "i", "t", "w"):
        assert letter in result_str, f"Letter '{letter}' missing from {result_str}"

def test_empty_string():
    """Test empty string raises NablaParseError."""
    with pytest.raises(NablaParseError):
        expr("")
    with pytest.raises(NablaParseError):
        expr("   ")

def test_unicode_handling():
    """Test unicode characters are parsed or raise appropriately."""
    # If the user enters a non-math unicode character like Arabic or emojis
    with pytest.raises(NablaParseError):
        expr("x + 😊")

def test_eq_returns_boolean():
    """Test that == operator correctly returns a boolean value."""
    f = expr("x^2")
    g = expr("x^2")
    assert (f == g) is True
    
    h = expr("x^3")
    assert (f == h) is False
