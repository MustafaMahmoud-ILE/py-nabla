from py_nabla.parser.parser import LaTeXParser
import sympy

parser = LaTeXParser()
# Set debug mode
from py_nabla.utils.logger import set_debug_mode
set_debug_mode(True)

latex = r"\frac{d}{dx} \sin(x^2)"
print(f"Testing: {latex}")
try:
    res = parser.parse(latex)
    print(f"Result: {res}")
    print(f"Simplified: {sympy.simplify(res)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
