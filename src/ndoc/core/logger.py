"""
Standardized logging for ndoc.
"""
import logging
import sys
from typing import Optional

# Default log format
LOG_FORMAT = "%(levelname)s: %(message)s"
# Detailed format for debug
DEBUG_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setup_logger(name: str = "ndoc", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and return a logger with the given name and level.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger is already configured
    if logger.handlers:
        return logger
        
    logger.setLevel(level)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Use different format based on level
    if level <= logging.DEBUG:
        formatter = logging.Formatter(DEBUG_LOG_FORMAT)
    else:
        formatter = logging.Formatter(LOG_FORMAT)
        
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Global logger instance
logger = setup_logger()

def set_log_level(level: int):
    """Update global log level."""
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
