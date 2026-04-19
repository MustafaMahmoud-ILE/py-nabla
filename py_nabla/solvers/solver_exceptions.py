"""
Exceptions for py-nabla differential and integral equation solvers.
"""

class NablaSolveError(Exception):
    """Base solver error for nabla resolution failures."""
    pass

class LaplaceTransformError(NablaSolveError):
    """Raised when the Laplace transform is not applicable or fails."""
    pass

class NonlinearODEError(NablaSolveError):
    """Raised when the ODE is nonlinear and requires routing to a different solver."""
    pass

class InvalidInitialConditionsError(NablaSolveError):
    """Raised when initial conditions provided are incomplete, redundant, or impossible to bind."""
    pass
