import re
from typing import Set
from ..utils.logger import logger

class LaTeXPreprocessor:
    """
    Normalizes LaTeX input and handles implicit multiplication through token splitting.
    """
    
    # Predefined symbols and functions that should not be split
    ATOMIC_SYMBOLS: Set[str] = {
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", 
        "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", 
        "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
        "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
        "sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan",
        "sinh", "cosh", "tanh", "log", "ln", "exp", "sqrt", "lim", "to", "partial",
        "d", "dx", "dy", "dz", "dt"
    }

    def __init__(self, custom_symbols: Set[str] = None):
        self.symbols = self.ATOMIC_SYMBOLS.copy()
        if custom_symbols:
            self.symbols.update(custom_symbols)

    def preprocess(self, latex_str: str) -> str:
        """
        Main preprocessing pipeline.
        """
        logger.debug(f"Preprocessing input: {latex_str}")
        
        # 1. Basic normalization (remove \left, \right, excessive spaces)
        latex_str = self._normalize(latex_str)
        
        # 2. Lazy LaTeX canonicalization (x^12 -> x^{12})
        latex_str = self._canonicalize(latex_str)
        
        # 3. Handle implicit multiplication (Token Splitting)
        latex_str = self._apply_token_splitting(latex_str)
        
        logger.debug(f"Preprocessing result: {latex_str}")
        return latex_str

    def _normalize(self, text: str) -> str:
        r"""Basic LaTeX cleaning."""
        text = text.replace(r"\left", "").replace(r"\right", "")
        text = text.replace("{}", "")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _canonicalize(self, text: str) -> str:
        """
        Converts lazy LaTeX into canonical forms.
        Examples:
            x^12 -> x^{12}
            \frac12 -> \frac{1}{2}
        """
        # 1. Naked exponents: x^12 -> x^{12}
        # Matches a symbol/number followed by ^ and then multiple digits
        # Only if the exponent is not already in braces
        text = re.sub(r"([a-zA-Z0-9])\^([0-9]{2,})", r"\1^{\2}", text)
        if re.search(r"[a-zA-Z0-9]\^([0-9]{2,})", text):
            logger.debug("Automatic brace injection for naked exponent.")
            
        # 2. Naked fractions: \frac12 -> \frac{1}{2}
        # Limited to single digits for safety
        text = re.sub(r"\\frac([0-9])([0-9])", r"\\frac{\1}{\2}", text)
        
        return text

    def _apply_token_splitting(self, text: str) -> str:
        r"""
        Injects explicit '*' where implicit multiplication is detected.
        Example: 2x -> 2*x, xy -> x*y, 2\sin(x) -> 2*\sin(x)
        """
        # 1. Protect commands (e.g., \sin)
        commands = re.findall(r"\\[a-zA-Z]+", text)
        for i, cmd in enumerate(commands):
            # Using __i__ which has no letters, so it won't be split
            text = text.replace(cmd, f" ___{i}___ ")
            
        # 2. Split character sequences
        def split_match(match):
            seq = match.group(0)
            if seq in self.symbols:
                return seq
            
            logger.debug(f"Splitting implicit product sequence: {seq}")
            return " ".join(list(seq))

        text = re.sub(r"[a-zA-Z]{2,}", split_match, text)
        
        # 3. Restore commands
        for i, cmd in enumerate(commands):
            text = text.replace(f" ___{i}___ ", cmd)
            
        # 4. Final cleanup of extra spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text
