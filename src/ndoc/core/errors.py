"""
Custom exceptions for ndoc.
"""

class NdocError(Exception):
    """Base class for all ndoc exceptions."""
    pass

class ConfigurationError(NdocError):
    """Raised when there is an error in the configuration."""
    pass

class FileSystemError(NdocError):
    """Raised when there is an error with file system operations."""
    pass

class ParsingError(NdocError):
    """Raised when there is an error parsing code."""
    pass

class DependencyError(NdocError):
    """Raised when there is an error resolving dependencies."""
    pass
