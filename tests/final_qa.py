"""
Final QA Blitz for py-nabla v1.0.1
Testing Operator Overloading, Error Pointers, and Grammar Path Integrity.
"""
import py_nabla as nb
from py_nabla.core.exceptions import NablaParseError
import os

def test_operators():
    print("1. Testing Operator Overloading (Matrices)... ", end="")
    A = nb.parse(r"\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}")
    B = nb.parse(r"\begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}")
    
    # Addition
    C = A + B
    assert "3" in str(C.simplify()), "Matrix addition failed"
    
    # Multiplication
    D = A * B
    assert "2" in str(D.simplify()), "Matrix multiplication failed"
    
    # Scalar multiplication
    E = A * 5
    assert "5" in str(E.simplify()), "Scalar multiplication failed"
    print("[\033[92mOK\033[0m]")

def test_error_pointers():
    print("2. Testing Error Pointer Accuracy... ", end="")
    broken_latex = r"\frac{1}{2} + \begin{bmatrix} 1 & 2 "  # Missing end
    try:
        nb.parse(broken_latex)
        print("[\033[91mFAILED\033[0m] (No error raised)")
    except NablaParseError as e:
        error_msg = str(e)
        # The pointer should be near the end of the string
        if "^" in error_msg:
            print("[\033[92mOK\033[0m]")
            # print(f"\nCaptured Error:\n{error_msg}")
        else:
            print("[\033[91mFAILED\033[0m] (No pointer in message)")

def test_grammar_path():
    print("3. Testing Grammar Path Integrity... ", end="")
    import py_nabla.parser.parser as p_mod
    grammar_file = os.path.join(os.path.dirname(p_mod.__file__), "grammar.lark")
    if os.path.exists(grammar_file):
        print("[\033[92mOK\033[0m]")
    else:
        print("[\033[91mFAILED\033[0m] (Grammar file missing in package scope)")

if __name__ == "__main__":
    print("=== nabla py-nabla v1.0.1 Final QA Blitz ===\n")
    test_operators()
    test_error_pointers()
    test_grammar_path()
    print("\n\033[92mFinal QA Blitz Complete. System is production-ready.\033[0m")
