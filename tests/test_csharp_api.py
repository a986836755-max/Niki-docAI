import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ndoc.atoms import ast, io

def test_csharp_extraction():
    sample_file = Path(__file__).parent / "sample_csharp.cs"
    content = io.read_text(sample_file)
    
    tree = ast.parse_code(content, sample_file)
    if not tree:
        print("❌ Failed to parse C# code")
        return

    symbols = ast.extract_symbols(tree, content.encode('utf8'), sample_file)
    
    print(f"Total symbols found: {len(symbols)}")
    for sym in symbols:
        visibility = "public" if sym.is_public else "non-public"
        parent = f" in {sym.parent}" if sym.parent else ""
        print(f"- [{sym.kind}] {sym.name}{parent} ({visibility})")
        if sym.bases:
            print(f"  Bases: {', '.join(sym.bases)}")
        if sym.signature:
            print(f"  Signature: {sym.signature}")

if __name__ == "__main__":
    test_csharp_extraction()
