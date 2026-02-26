
import sys
import importlib
import pkg_resources

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print("-" * 60)

langs = [
    "tree_sitter_python", 
    "tree_sitter_javascript", 
    "tree_sitter_cpp", 
    "tree_sitter_rust"
]

for lang in langs:
    try:
        mod = importlib.import_module(lang)
        print(f"✅ {lang} imported successfully.")
        print(f"   Path: {mod.__file__}")
        if hasattr(mod, 'language'):
            print(f"   Has language(): YES")
        else:
            print(f"   Has language(): NO (Available attributes: {dir(mod)})")
            
    except ImportError as e:
        print(f"❌ {lang} import failed: {e}")
        
print("-" * 60)
try:
    import tree_sitter
    print(f"tree_sitter package version: {tree_sitter.__version__ if hasattr(tree_sitter, '__version__') else 'unknown'}")
    print(f"tree_sitter path: {tree_sitter.__file__}")
except ImportError:
    print("❌ tree_sitter package not found")
