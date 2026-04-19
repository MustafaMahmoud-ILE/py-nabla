import sympy as sp

# 1. Traditional way with Functions
x = sp.Symbol('x')
f = sp.Function('f')(x)
eq1 = sp.Eq(f.diff(x), 2*f)
sol1 = sp.dsolve(eq1)
print(f"Sol1: {sol1}")

# 2. Can we build it from Symbols then replace?
y = sp.Symbol('y')
# Unevaluated derivative of y (symbol) wrt x
deriv = sp.Derivative(y, x)
eq2 = sp.Eq(deriv, 2*y)
print(f"Eq2 (with symbols): {eq2}")

# Let's write a replacement function
def symbol_to_function(expr, sym_name, var_sym):
    target_sym = sp.Symbol(sym_name)
    target_func = sp.Function(sym_name)(var_sym)
    
    def replacer(node):
        if isinstance(node, sp.Derivative):
            # If we are taking derivative of the symbol, replace it with derivative of the function
            if node.args[0] == target_sym:
                return sp.Derivative(target_func, *node.args[1:])
        elif node == target_sym:
            return target_func
        
        # Recursively apply to arguments
        new_args = [replacer(arg) if isinstance(arg, sp.Basic) else arg for arg in node.args]
        return node.func(*new_args) if new_args else node

    return replacer(expr)

eq2_func = symbol_to_function(eq2, 'y', x)
print(f"Eq2 (transformed): {eq2_func}")

sol2 = sp.dsolve(eq2_func)
print(f"Sol2: {sol2}")

# 3. Special functions
# Airy equation: y'' - x*y = 0
deriv2 = sp.Derivative(y, x, x)
eq_airy = sp.Eq(deriv2 - x*y, 0)
eq_airy_func = symbol_to_function(eq_airy, 'y', x)
sol_airy = sp.dsolve(eq_airy_func)
print(f"Airy Sol: {sol_airy}")

