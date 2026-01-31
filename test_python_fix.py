
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(os.getcwd()) / "src"))

from ndoc.atoms import ast, queries

def test_python_parsing():
    code = """
class MyClass:
    \"\"\"Class docstring\"\"\"
    def my_method(self, a: int) -> str:
        \"\"\"Method docstring\"\"\"
        return "hello"

def my_function(x, y=10):
    return x + y

@decorator
def decorated_func():
    pass

MY_VAR = 100
MY_TYPED_VAR: int = 200
"""
    print("--- Testing Python Parsing ---")
    
    # 1. Parse code
    tree = ast.parse_code(code, Path("test.py"))
    if not tree:
        print("Failed to parse code")
        return

    print(f"Tree root type: {tree.root_node.type}")
    
    # 2. Extract symbols
    symbols = ast.extract_symbols(tree, code.encode('utf8'), Path("test.py"))
    
    print(f"Found {len(symbols)} symbols:")
    for sym in symbols:
        print(f"- {sym.kind}: {sym.name} (line {sym.line})")
        if sym.signature:
            print(f"  Signature: {sym.signature}")
        if sym.docstring:
            print(f"  Doc: {sym.docstring[:50]}...")

if __name__ == "__main__":
    test_python_parsing()
