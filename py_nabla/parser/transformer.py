from lark import Transformer, v_args
import sympy
from sympy import (
    Symbol, Integer, Float, Rational, Derivative, Integral,
    Limit, Matrix, Sum, Product, Piecewise,
    sin, cos, tan, cot, sec, csc, asin, acos, atan,
    sinh, cosh, tanh, coth, log, exp, sqrt,
    Abs, floor, ceiling, binomial, factorial,
    pi, oo, E, diff, integrate, symbols as sympy_symbols
)


class LaTeXTransformer(Transformer):
    """
    Transforms Lark parse tree (AST) nodes into SymPy expressions.
    
    Each method handles one grammar rule and receives a list of
    already-transformed children as `args`.
    """

    def __init__(self, context=None):
        super().__init__()
        self.context = context or {}

    # ================================================================
    # ARITHMETIC
    # ================================================================

    def add(self, args): return args[0] + args[1]
    def sub(self, args): return args[0] - args[1]
    def mul(self, args): return args[0] * args[1]
    def div(self, args): return args[0] / args[1]
    def neg(self, args): return -args[0]
    def implicit_mul(self, args): return args[0] * args[1]

    def power(self, args): return args[0] ** args[1]

    def subscript(self, args):
        # a_b  →  keep as Symbol(a_b) for now
        base = args[0]
        sub = args[1]
        return Symbol(f"{base}_{sub}")

    def parens(self, args): return args[0]

    # ================================================================
    # RELATIONS
    # ================================================================

    def eq(self, args): return sympy.Eq(args[0], args[1])
    def lt(self, args): return sympy.Lt(args[0], args[1])
    def gt(self, args): return sympy.Gt(args[0], args[1])
    def leq(self, args): return sympy.Le(args[0], args[1])
    def geq(self, args): return sympy.Ge(args[0], args[1])
    def neq(self, args): return sympy.Ne(args[0], args[1])

    # ================================================================
    # TERMINALS
    # ================================================================

    def SYMBOL(self, token):
        val = token.value
        # 'e' is Euler's number; 'i' stays as a regular symbol
        # (users who want imaginary unit should write \\sqrt{-1})
        if val == 'e':
            return E
        return Symbol(val)

    def NUMBER(self, token):
        if '.' in token.value:
            return Float(token.value)
        return Integer(token.value)

    def DIFFERENTIAL(self, token):
        val = token.value  # e.g. "dx", "dy", "d\\theta"
        if val.startswith('d'):
            inner = val[1:]
            greek_map = {'\\theta': 'theta', '\\phi': 'phi'}
            return Symbol(greek_map.get(inner, inner))
        return Symbol(val)

    def greek_letter(self, args):
        name = args[0].value.lstrip('\\')
        greek_constants = {'pi': pi, 'infty': oo}
        greek_map = {
            'varepsilon': 'epsilon', 'vartheta': 'theta',
            'varpi': 'pi', 'varrho': 'rho', 'varsigma': 'sigma',
            'varphi': 'phi',
        }
        canon = greek_map.get(name, name)
        return greek_constants.get(canon, Symbol(canon))

    def infinity(self, args): return oo

    # Passthrough tokens for grammar helpers
    def GREEK_LOWER(self, token): return token
    def GREEK_UPPER(self, token): return token
    def FUNC_NAME(self, token): return token
    def SIDE(self, token): return token.value

    # ================================================================
    # FRACTION
    # ================================================================

    def fraction(self, args):
        num, den = args[0], args[1]
        if isinstance(num, Integer) and isinstance(den, Integer):
            return Rational(num, den)
        return num / den

    # ================================================================
    # DERIVATIVES (ordinary)
    # ================================================================

    def derivative(self, args):
        # args may be: [var_symbol, operand] or [operand, var_symbol]
        # The DIFFERENTIAL always gives us the variable.
        # We gather Symbol and non-Symbol args.
        if not args:
            return Integer(1)
        # Last arg is the function; second-to-last (if Symbol) is var
        if len(args) >= 2:
            # Find the differential variable (a Symbol from DIFFERENTIAL)
            var = args[-2] if isinstance(args[-2], sympy.Basic) else args[0]
            func = args[-1]
            return Derivative(func, var, evaluate=False)
        return Derivative(args[0], Symbol('x'), evaluate=False)  # fallback

    def first_prime(self, args):
        return Derivative(args[0], Symbol('t'), 1, evaluate=False)

    def second_prime(self, args):
        return Derivative(args[0], Symbol('t'), 2, evaluate=False)

    def nth_prime(self, args):
        return Derivative(args[0], Symbol('t'), int(str(args[-1])), evaluate=False)

    # ================================================================
    # PARTIAL DERIVATIVES
    # ================================================================

    def partial_derivative(self, args):
        """∂f/∂x  →  Derivative(f, x)"""
        if len(args) >= 2:
            return Derivative(args[-1], args[-2], evaluate=False)
        return Derivative(args[0], Symbol('x'), evaluate=False)

    def mixed_partial(self, args):
        """∂²f/∂x∂y  →  Derivative(f, x, y)"""
        # args: [expr, SYMBOL1, SYMBOL2] or [SYMBOL1, SYMBOL2, expr]
        # Collect symbols and expression
        syms = [a for a in args if isinstance(a, sympy.Symbol)]
        exprs = [a for a in args if not isinstance(a, sympy.Symbol)]
        if exprs and syms:
            result = exprs[0]
            return Derivative(result, *syms, evaluate=False)
        return Integer(0)

    # ================================================================
    # INTEGRALS
    # ================================================================

    def integral(self, args):
        # args: [limits_tuple?, expr, var_symbol]
        var = args[-1]    # DIFFERENTIAL is last
        expr = args[-2]   # expression is second-to-last

        # Use Dummy to prevent variable leakage if limits exist
        dummy_var = sympy.Dummy(var.name)
        expr_dummy = expr.subs(var, dummy_var)

        # Look for limits tuple
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2:
                lower, upper = arg
                return Integral(expr_dummy, (dummy_var, lower, upper))

        return Integral(expr, var)

    def double_integral(self, args):
        var1 = args[-1]
        var2 = args[-2]
        expr = args[-3]
        return Integral(expr, var2, var1)

    def contour_integral(self, args):
        # Treat like a regular integral for now
        return self.integral(args)

    def limits(self, args):
        if len(args) == 2:
            return (args[0], args[1])
        return (None, None)

    # ================================================================
    # LIMITS
    # ================================================================

    def limit(self, args):
        var_token, target, expr = args
        var = Symbol(var_token.value) if hasattr(var_token, 'value') else var_token
        return Limit(expr, var, target).doit()

    def onesided_limit(self, args):
        var_token, target, side, expr = args
        var = Symbol(var_token.value) if hasattr(var_token, 'value') else var_token
        direction = side if isinstance(side, str) else side.value
        return Limit(expr, var, target, direction).doit()

    # ================================================================
    # SUMMATIONS & PRODUCTS
    # ================================================================

    def summation(self, args):
        """\\sum_{i=a}^{b} f(i)  →  Sum(f, (i, a, b))"""
        # args: [var_token, lower, upper, expr]
        var_token = args[0]
        lower = args[1]
        upper = args[2]
        expr = args[3]
        var = Symbol(var_token.value) if hasattr(var_token, 'value') else var_token
        return Sum(expr, (var, lower, upper)).doit()

    def product(self, args):
        """\\prod_{i=a}^{b} f(i)  →  Product(f, (i, a, b))"""
        var_token = args[0]
        lower = args[1]
        upper = args[2]
        expr = args[3]
        var = Symbol(var_token.value) if hasattr(var_token, 'value') else var_token
        return Product(expr, (var, lower, upper)).doit()

    # ================================================================
    # FUNCTIONS
    # ================================================================

    def function(self, args):
        func_name_token = args[0]
        expr = args[1]
        func_name = func_name_token.value.lstrip('\\')

        mapping = {
            'sin': sin, 'cos': cos, 'tan': tan,
            'cot': cot, 'sec': sec, 'csc': csc,
            'arcsin': asin, 'arccos': acos, 'arctan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh, 'coth': coth,
            'log': log, 'ln': log, 'exp': exp, 'sqrt': sqrt,
            'abs': Abs, 'det': sympy.det, 'tr': sympy.trace,
        }

        if func_name in mapping:
            return mapping[func_name](expr)
        return sympy.Function(func_name)(expr)

    # ================================================================
    # MATRICES
    # ================================================================

    def matrix(self, args):
        rows = args[0]
        return Matrix(rows)

    def matrix_rows(self, args):
        return list(args)

    def matrix_row(self, args):
        return list(args)

    # ================================================================
    # VECTORS
    # ================================================================

    def vector(self, args):
        val = args[0].value if hasattr(args[0], 'value') else args[0].name
        return Symbol(val)

    # ================================================================
    # DOT NOTATION (time derivatives)
    # ================================================================

    def dot_deriv(self, args):
        """\\dot{x}  →  Symbol(x_dot)"""
        val = args[0].value if hasattr(args[0], 'value') else args[0].name
        return Symbol(f"{val}_dot")

    def ddot_deriv(self, args):
        """\\ddot{x}  →  Symbol(x_ddot)"""
        val = args[0].value if hasattr(args[0], 'value') else args[0].name
        return Symbol(f"{val}_ddot")

    # ================================================================
    # NABLA OPERATOR
    # ================================================================

    def gradient(self, args):
        """\\nabla f  →  gradient (returns symbol for now)"""
        expr = args[0]
        return sympy.Function('grad')(expr)

    def divergence(self, args):
        expr = args[0]
        return sympy.Function('div')(expr)

    def curl(self, args):
        expr = args[0]
        return sympy.Function('curl')(expr)

    def laplacian(self, args):
        expr = args[0]
        # Try computing actual Laplacian symbolically
        free = expr.free_symbols if hasattr(expr, 'free_symbols') else []
        if free:
            result = sum(diff(expr, var, 2) for var in free)
            return result
        return sympy.Function('laplacian')(expr)

    def nabla_op(self, args): return args[0]

    # ================================================================
    # PIECEWISE FUNCTIONS
    # ================================================================

    def piecewise(self, args):
        """\\begin{cases}..."""
        cases = args[0]  # list of (expr, condition) pairs
        # Last case defaults to True if not already a boolean
        if cases:
            # Normalize: if last condition is not True, add True catch-all
            last_cond = cases[-1][1]
            if last_cond is not sympy.true:
                cases.append((Integer(0), sympy.true))
        return Piecewise(*cases)

    def case_rows(self, args):
        return list(args)

    def case_row(self, args):
        # (expression, condition_expression)
        return (args[0], args[1])

    # ================================================================
    # SPECIAL FUNCTIONS
    # ================================================================

    def absolute(self, args):
        return Abs(args[0])

    def floor(self, args):
        return floor(args[0])

    def ceiling(self, args):
        return ceiling(args[0])

    def binomial(self, args):
        return binomial(args[0], args[1])
