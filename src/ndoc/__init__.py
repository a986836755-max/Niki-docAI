"""
Niki-docAI Source Root.
"""

# Automatically initialize environment on package import
# This ensures spawned processes (multiprocessing) have correct paths
try:
    from .core.bootstrap import ensure_cli_environment
    ensure_cli_environment()
except ImportError:
    # Avoid circular import issues during setup/install if dependencies are missing
    pass
