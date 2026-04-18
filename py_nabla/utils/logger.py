import logging
import sys

def setup_logger(name: str = "nabla"):
    """
    Configures a professional logger for the Nabla library.
    By default, it logs to stderr with a clean format.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    # Default level is WARNING, users can set it to DEBUG for decision tracking
    logger.setLevel(logging.WARNING)
    return logger

# Global logger instance
logger = setup_logger()

def set_debug_mode(enabled: bool = True):
    """Convenience function to enable/disable debug logging."""
    if enabled:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
