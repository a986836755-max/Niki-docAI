import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root / "src"))

# Ensure local libs are prioritized for tests
lib_path = root / ".ndoc" / "lib"
if lib_path.exists():
    sys.path.insert(0, str(lib_path))
    
    # Force tree_sitter to be loaded from local lib if present
    # This prevents conflicts with global site-packages
    try:
        import tree_sitter
        # Check if it's the wrong one
        if not str(tree_sitter.__file__).startswith(str(lib_path)):
            # Reload
            del sys.modules["tree_sitter"]
            import tree_sitter
            print(f"Reloaded tree_sitter from: {tree_sitter.__file__}")
    except ImportError:
        pass
