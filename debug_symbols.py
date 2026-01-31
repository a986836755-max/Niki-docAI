
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path.cwd() / "src"))

from ndoc.atoms.ast import parse_code, extract_symbols, MAX_VALUE_LENGTH
from ndoc.atoms.io import read_text

print(f"DEBUG: MAX_VALUE_LENGTH = {MAX_VALUE_LENGTH}")

file_path = Path("src/ndoc/atoms/deps/stats.py")
content = read_text(file_path)
tree = parse_code(content, file_path)
symbols = extract_symbols(tree, content.encode("utf-8"), file_path)

for sym in symbols:
    if sym.name == "LANGUAGE_EXTENSIONS":
        print(f"Name: {sym.name}")
        print(f"Kind: {sym.kind}")
        print(f"Signature: {sym.signature}")
        print(f"Full Content Length: {len(sym.full_content)}")
        print(f"Signature Length: {len(sym.signature) if sym.signature else 0}")
