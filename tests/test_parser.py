import pytest
import json
import os
from nabla import expr
from sympy import simplify, sympify

def load_test_cases():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'latex_test_cases.json')
    with open(fixture_path, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("category", ["basic_arithmetic", "derivatives", "integrals", "functions", "implicit_multiplication"])
def test_latex_parsing(category):
    test_cases = load_test_cases()
    cases = test_cases.get(category, [])
    
    for case in cases:
        latex_input = case["input"]
        expected_str = case["expected"]
        
        # Parse LaTeX using Nabla
        result_expr = expr(latex_input)
        
        # Compare with expected sympified expression
        expected_expr = sympify(expected_str)
        
        # Use simplify for robust comparison
        assert simplify(result_expr._expr - expected_expr) == 0, f"Failed parsing: {latex_input}. Expected: {expected_str}, Got: {result_expr._expr}"
