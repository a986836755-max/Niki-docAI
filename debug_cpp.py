
import sys
import importlib
from pathlib import Path

# Add local lib to path
lib_dir = Path.cwd() / ".ndoc" / "lib"
if lib_dir.exists():
    sys.path.insert(0, str(lib_dir))

try:
    import tree_sitter_cpp
    print(f"tree_sitter_cpp imported from: {tree_sitter_cpp.__file__}")
    print(f"Dir: {dir(tree_sitter_cpp)}")
    
    if hasattr(tree_sitter_cpp, 'language'):
        lang_ptr = tree_sitter_cpp.language()
        print(f"language() returns: {lang_ptr} (Type: {type(lang_ptr)})")
        
        from tree_sitter import Language
        try:
            lang = Language(lang_ptr)
            print(f"✅ Successfully created Language(ptr)")
        except Exception as e:
            print(f"❌ Failed to create Language(ptr): {e}")
            
        try:
            lang = Language(lang_ptr, "cpp")
            print(f"✅ Successfully created Language(ptr, name)")
        except Exception as e:
            print(f"❌ Failed to create Language(ptr, name): {e}")

except ImportError as e:
    print(f"Failed to import tree_sitter_cpp: {e}")
