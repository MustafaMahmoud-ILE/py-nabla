class NablaError(Exception):
    """Base class for all Nabla exceptions."""
    pass

class NablaParseError(NablaError):
    """Exception raised when LaTeX parsing fails."""
    def __init__(self, latex_input: str, line: int, column: int, msg: str):
        self.latex_input = latex_input
        self.line = line
        self.column = column
        self.msg = msg
        
        # Build a visual pointer to the error
        # Example:
        # Error parsing LaTeX at line 1, col 5:
        # 'x + + y'
        #      ^-- Unexpected characters
        base_msg = f"\nError parsing LaTeX at line {line}, col {column}:"
        input_line = f"\n'{latex_input}'"
        pointer = f"\n {' ' * (column)}^-- {msg}"
        
        self.message = base_msg + input_line + pointer
        super().__init__(self.message)

class NablaEvaluationError(NablaError):
    """Exception raised during numerical or symbolic evaluation."""
    pass

class NablaConfigurationError(NablaError):
    """Exception raised for configuration or setup issues."""
    pass
