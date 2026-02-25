# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Lightweight LSP-like features.
原子能力：轻量级 LSP 特性（定义跳转、引用查找等）。
"""
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..models.symbol import Symbol
from ..parsing import scanner
from ..core import io

class LSPService:
    def __init__(self, root: Path):
        self.root = Path(root) if isinstance(root, str) else root
        self._symbol_cache: Dict[str, List[Symbol]] = {}
        self._indexed_files: List[Path] = []
        # self._file_content_cache: Dict[Path, str] = {} # Removed for memory optimization
        self._reference_counts: Dict[str, int] = {}
        self._is_indexed = False
        self.semantic_index = None # Cache for semantic index (rules)

    def index_project(self, files: List[Path]):
        """
        Build a global symbol index for fast lookup using optimized Parallel Scanner.
        """
        self._symbol_cache.clear()
        self._reference_counts.clear()
        
        self._indexed_files = list(files)
        
        print(f"LSP: Indexing project (Parallel + Cached)...")
        
        # Use scanner.scan_project which is now parallel and cached
        # This is Phase 3 Optimization: Lazy Load & Parallel
        # We rely on scanner's internal cache (SQLite) to be fast
        scan_results = scanner.scan_project(self.root)
        
        # 1. First pass: Index symbols
        for f, result in scan_results.items():
            for sym in result.symbols:
                if sym.name not in self._symbol_cache:
                    self._symbol_cache[sym.name] = []
                self._symbol_cache[sym.name].append(sym)
        
        print(f"LSP: Found {len(self._symbol_cache)} unique symbols.")
        
        # 2. Second pass: Aggregate reference counts from pre-calculated tokens
        # No need to read file content or run regex again!
        for f, result in scan_results.items():
            for word, count in result.tokens.items():
                if word in self._symbol_cache:
                    self._reference_counts[word] = self._reference_counts.get(word, 0) + count
                    
        self._is_indexed = True
        print(f"LSP: Pre-calculated reference counts for {len(self._reference_counts)} symbols.")

    def find_definitions(self, name: str) -> List[Symbol]:
        """
        Find definition of a symbol by name.
        """
        return self._symbol_cache.get(name, [])

    def get_reference_count(self, name: str) -> int:
        """
        Get pre-calculated reference count.
        """
        return self._reference_counts.get(name, 0)

    def get_context_for_file(self, file_path: Path) -> str:
        """
        Get 'Memory Context' (Rules, Warns) for a file.
        This can be used by IDE plugins to display 'Mental Context'.
        """
        from ..flows import prompt_flow
        from ..models.config import ProjectConfig, ScanConfig
        
        # We need a minimal config to use prompt_flow
        # Assuming defaults are okay or we can infer from root
        config = ProjectConfig(scan=ScanConfig(root_path=self.root))
        return prompt_flow.get_context_prompt(file_path, config)

    def find_references(self, name: str) -> List[Dict[str, Any]]:
        """
        Find references to a symbol using Grep-like search across indexed files.
        """
        import re
        references = []
        pattern = re.compile(r'\b' + re.escape(name) + r'\b')

        for fpath, content in self._file_content_cache.items():
            for i, line in enumerate(content.splitlines()):
                if pattern.search(line):
                    references.append({
                        "path": fpath,
                        "line": i + 1,
                        "content": line.strip()
                    })
        return references

# Global instance for easy access
_INSTANCE: Optional[LSPService] = None

def get_service(root: Path) -> LSPService:
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = LSPService(root)
    return _INSTANCE
