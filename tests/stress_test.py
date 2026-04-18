"""
Stress Test for py-nabla 1.0.0
A series of extreme cases to find potential parser breaking points.
"""
import py_nabla as nb
import sys

STRESS_CASES = [
    # 1. Deep Radical Nesting
    (r"\sqrt{\sqrt{\sqrt{\sqrt{x+1}}}}", "Deep Radicals"),
    
    # 2. Matrix of Integrals
    (r"\begin{bmatrix} \int x dx & \int y dy \\ \int z dz & \int w dw \end{bmatrix}", "Matrix of Integrals"),
    
    # 3. Double Summations
    (r"\sum_{i=1}^{n} \sum_{j=1}^{m} x_{ij}", "Double Summations"),
    
    # 4. Pendulum Equation (Dot notation + Greek)
    (r"\ddot{\theta} + \frac{g}{L} \sin(\theta) = 0", "Physics Equation"),
    
    # 5. Nabla Vector Identity
    (r"\nabla \times (\nabla \times \vec{A})", "Vector Identity"),
    
    # 6. Piecewise with Matrix Logic
    (r"\begin{cases} \begin{bmatrix} 1 & 0 \end{bmatrix} & x < 0 \\ \begin{bmatrix} 0 & 1 \end{bmatrix} & x \geq 0 \end{cases}", "Piecewise Matrices"),
    
    # 7. Extreme Implicit Multiplication
    (r"2xy \sin(z) \cos(w) e^u \log(v)", "Massive Implicit Mul"),
    
    # 8. Nested Fractions and Binomials
    (r"\binom{n}{k} \cdot \frac{\frac{a}{b}}{\frac{c}{d}}", "Nested Fractions"),
    
    # 9. Limits with Infinity and Powers
    (r"\lim_{x \to \infty} (1 + \frac{1}{x})^x", "Euler Limit"),

    # 10. Mixed Partial of Absolute Piecewise
    (r"\frac{\partial^2}{\partial x \partial y} |\sin(x) \cos(y)|", "Mixed Partial Abs"),
]

def run_stress_test():
    print("=== nabla py-nabla Phase 5: Stress Testing ===\n")
    failed = 0
    passed = 0
    
    for i, (latex, desc) in enumerate(STRESS_CASES, 1):
        print(f"Test {i:02}: {desc:<25} ", end="")
        try:
            expr = nb.parse(latex)
            # Try a basic simplification to force transformer/sympy evaluation
            _ = expr.simplify()
            print("[\033[92mPASSED\033[0m]")
            passed += 1
        except Exception as e:
            print("[\033[91mFAILED\033[0m]")
            print(f"   Error: {type(e).__name__}: {str(e)}")
            failed += 1
            
    print(f"\nFinal Result: {passed} Passed, {failed} Failed.")
    if failed == 0:
        print("\033[92mSystem is incredibly robust! Nabla survived the stress test.\033[0m")
    else:
        print("\033[91mWeak points detected. Optimization required.\033[0m")

if __name__ == "__main__":
    run_stress_test()
