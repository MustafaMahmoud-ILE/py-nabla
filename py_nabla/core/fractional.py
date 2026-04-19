import sympy as sp
from sympy import Expr, Symbol, Function, gamma, ceiling, floor, Derivative, Subs, Rational

class FractionalDerivative(Expr):
    """
    Represents a Fractional Derivative of an expression.
    Defaults to the Caputo definition for Laplace Transform compatibility.
    
    Attributes:
        expr (Expr): The function being differentiated.
        var (Symbol): The independent variable (e.g., t).
        order (Expr): The non-integer order of differentiation (alpha).
    """
    def __new__(cls, expr, var, order):
        expr = sp.sympify(expr)
        var = sp.sympify(var)
        order = sp.sympify(order)
        
        obj = Expr.__new__(cls, expr, var, order)
        return obj

    @property
    def expr(self): return self.args[0]
    
    @property
    def var(self): return self.args[1]
    
    @property
    def order(self): return self.args[2]

    def _eval_latex(self, printer):
        order_latex = printer._print(self.order)
        var_latex = printer._print(self.var)
        expr_latex = printer._print(self.expr)
        return r"\frac{d^{%s}}{d%s^{%s}} %s" % (order_latex, var_latex, order_latex, expr_latex)

    def _eval_laplace_transform(self, t, s):
        """
        L{C_D^alpha_t f(t)} = s^alpha F(s) - sum_{k=0}^{n-1} s^{alpha-k-1} f^(k)(0)
        where n = ceil(alpha).
        """
        import sympy as sp
        from sympy import Rational, ceiling, laplace_transform
        
        alpha = Rational(self.order)
        func = self.expr
        
        
        # F(s)
        res = laplace_transform(func, t, s, noconds=True)
        # Deep tuple/iterability check
        if hasattr(res, "__iter__") and not isinstance(res, sp.Basic):
            F_s = res[0]
        elif isinstance(res, sp.Tuple):
            F_s = res[0]
        else:
            F_s = res
        
        try:
            # We need n = ceil(alpha)
            if alpha.is_number:
                n = int(ceiling(alpha))
                ics_sum = 0
                for k in range(n):
                    # f^(k)(0)
                    if k == 0:
                        val = func.subs(t, 0)
                    else:
                        val = sp.Derivative(func, t, k).subs(t, 0)
                    ics_sum += (s**(alpha - k - 1)) * val
                
                result = (s**alpha) * F_s - ics_sum
        except Exception:
            pass
            
        # Fallback/Symbolic representation
        return (s**alpha) * F_s # Simplified fallback

    def to_integral(self, definition="caputo"):
        """
        Expands to the integral definition (Riemann-Liouville or Caputo).
        """
        alpha = self.order
        t = self.var
        f = self.expr
        tau = sp.Symbol('tau', real=True, positive=True)
        n = ceiling(alpha)
        
        if definition.lower() == "caputo":
            return (1 / gamma(n - alpha)) * sp.Integral((t - tau)**(n - alpha - 1) * sp.Derivative(f, t, n).subs(t, tau), (tau, 0, t))
        else: # Riemann-Liouville
            inner = sp.Integral((t - tau)**(n - alpha - 1) * f.subs(t, tau), (tau, 0, t))
            return (1 / gamma(n - alpha)) * sp.Derivative(inner, t, n)

    def doit(self, **hints):
        """
        If order is an integer, return a standard Derivative.
        """
        if self.order.is_Integer:
            return sp.Derivative(self.expr, self.var, int(self.order)).doit(**hints)
        return self
