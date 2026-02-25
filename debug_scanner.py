# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
# - 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - LSP 适配：所有 IDE 插件相关的语义能力通过 `ndoc.lsp_server` 暴露。
# - 架构感知：IDE 插件应优先使用 `_MAP.md` 和 `_AI.md` 进行语义增强，而非仅依赖语法树。
# ------------------------------------------------------------------------------
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ndoc.atoms import scanner
from ndoc.models.context import Symbol

def test():
    root = Path(__file__).parent.resolve()
    test_file = root / "test_enhanced_doc.py"
    
    print(f"Scanning {test_file}...")
    result = scanner.scan_file(test_file, root, force=True)
    
    print(f"\nFile Tags: {[t.name for t in result.tags]}")
    print(f"Is Core: {result.is_core}")
    
    print("\nSymbols:")
    for sym in result.symbols:
        tags_str = ", ".join([f"{t.name}({' '.join(t.args)})" if t.args else t.name for t in sym.tags])
        print(f"- [{sym.kind}] {sym.name}")
        doc_prev = (sym.docstring[:50].replace('\n', '\\n') + "...") if sym.docstring else "None"
        print(f"  Docstring: {doc_prev}")
        print(f"  Tags: {tags_str}")
        print(f"  Is Public: {sym.is_public}")

if __name__ == "__main__":
    test()
