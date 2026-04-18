import os
from lark import Lark, exceptions
from .preprocessor import LaTeXPreprocessor
from .transformer import LaTeXTransformer
from ..core.exceptions import NablaParseError
from ..utils.logger import logger

class LaTeXParser:
    """
    Orchestrates the conversion from LaTeX string to SymPy expression.
    """
    
    def __init__(self, custom_symbols=None):
        self.preprocessor = LaTeXPreprocessor(custom_symbols=custom_symbols)
        
        # Load grammar from file
        grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.lark')
        with open(grammar_path, 'r') as f:
            self.grammar = f.read()
            
        self.lark_parser = Lark(self.grammar, start='start', parser='earley', ambiguity='resolve')
        self.transformer = LaTeXTransformer()

    def parse(self, latex_str: str):
        """
        Parses a LaTeX mathematical expression.
        """
        logger.debug(f"Starting parse of LaTeX string: {latex_str}")
        
        # 1. Preprocess (Normalization and Token Splitting)
        clean_latex = self.preprocessor.preprocess(latex_str)
        logger.debug(f"Preprocessed LaTeX: {clean_latex}")
        
        # 2. Parse into AST
        try:
            ast = self.lark_parser.parse(clean_latex)
            logger.debug("Lark AST generated successfully.")
            
            # 3. Transform AST to SymPy
            sympy_expr = self.transformer.transform(ast)
            logger.debug(f"Transformation to SymPy successful: {sympy_expr}")
            
            return sympy_expr
            
        except (exceptions.UnexpectedCharacters, exceptions.UnexpectedToken, exceptions.UnexpectedEOF) as e:
            logger.error(f"Parsing failed: {str(e)}")
            raise NablaParseError(
                latex_input=clean_latex,
                line=getattr(e, 'line', 1),
                column=getattr(e, 'column', 1),
                msg=str(e).split('\n')[0]
            ) from None
        except Exception as e:
            logger.error(f"Internal parsing error: {str(e)}")
            raise
