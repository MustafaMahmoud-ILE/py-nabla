from lark import Transformer, v_args
import sympy
from sympy import Symbol, Integer, Float, Rational, Derivative, Integral, Limit, Matrix, sin, cos, tan, cot, sec, csc, asin, acos, atan, sinh, cosh, tanh, log, exp, sqrt, pi, oo, E

class LaTeXTransformer(Transformer):
    """
    Transforms Lark AST nodes into SymPy expressions.
    """
    
    def __init__(self, context=None):
        super().__init__()
        self.context = context or {}

    def add(self, args):
        return args[0] + args[1]

    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def neg(self, args):
        return -args[0]

    def div(self, args):
        return args[0] / args[1]

    def implicit_mul(self, args):
        return args[0] * args[1]

    def power(self, args):
        return args[0] ** args[1]

    def absolute(self, args):
        return sympy.Abs(args[0])

    def infinity(self, args):
        return oo

    def eq(self, args):
        return sympy.Eq(args[0], args[1])

    def lt(self, args):
        return sympy.Lt(args[0], args[1])

    def gt(self, args):
        return sympy.Gt(args[0], args[1])

    def SYMBOL(self, token):
        # Handle constants like pi
        val = token.value
        if val == 'e':
            return sympy.E
        return Symbol(val)

    def DIFFERENTIAL(self, token):
        # Extract x from dx, dy, dt
        val = token.value
        if val.startswith('d') and len(val) > 1:
            return Symbol(val[1:])
        return Symbol(val)

    def NUMBER(self, token):
        if '.' in token.value:
            return Float(token.value)
        return Integer(token.value)

    def greek_letter(self, args):
        # Remove the backslash from \alpha etc.
        name = args[0].value.lstrip('\\')
        if name == 'pi':
            return pi
        return Symbol(name)

    def fraction(self, args):
        # Use Rational if both are integers, otherwise simple division
        num, den = args
        if isinstance(num, Integer) and isinstance(den, Integer):
            return Rational(num, den)
        return num / den

    def function(self, args):
        func_name = args[0].value.lstrip('\\')
        expr = args[1]
        
        mapping = {
            'sin': sin, 'cos': cos, 'tan': tan, 'cot': cot, 'sec': sec, 'csc': csc,
            'arcsin': asin, 'arccos': acos, 'arctan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'log': log, 'ln': log, 'exp': exp, 'sqrt': sqrt
        }
        
        if func_name in mapping:
            return mapping[func_name](expr)
        
        # Generic function if not in mapping
        return sympy.Function(func_name)(expr)

    def derivative(self, args):
        # args: [order?, var, operand?]
        if len(args) >= 2:
            return sympy.diff(args[-1], args[-2])
        elif len(args) == 1:
            return sympy.diff(1, args[0])
        return 1

    def partial_derivative(self, args):
        if len(args) >= 2:
            return sympy.diff(args[-1], args[-2])
        elif len(args) == 1:
            return sympy.diff(1, args[0])
        return 1

    def integral(self, args):
        # args looks like: [limits?, expr, DIFFERENTIAL]
        var = args[-1]
        expr = args[-2]
        
        # Check for limits
        for arg in args:
            if isinstance(arg, tuple) and len(arg) == 2: # result from self.limits
                lower, upper = arg
                return sympy.integrate(expr, (var, lower, upper))
        
        return sympy.integrate(expr, var)

    def limits(self, args):
        # Result of "_" atom "^" atom or similar
        if len(args) == 2:
            return (args[0], args[1]) # (lower, upper)
        return (None, None) 

    def matrix(self, args):
        rows = args[0]
        return Matrix(rows)

    def matrix_rows(self, args):
        return args

    def matrix_row(self, args):
        return args
        
    def vector(self, args):
        return Symbol(args[0].value)

    def limit(self, args):
        var, target, expr = args
        return Limit(expr, Symbol(var.value), target).doit()

    def GREEK_LOWER(self, token): return token
    def GREEK_UPPER(self, token): return token
    def FUNC_NAME(self, token): return token
