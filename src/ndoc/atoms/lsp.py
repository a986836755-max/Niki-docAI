"""
Atoms: Lightweight LSP-like features.
原子能力：轻量级 LSP 特性（定义跳转、引用查找等）。
"""
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..models.context import Symbol
from . import scanner

class LSPService:
    def __init__(self, root: Path):
        self.root = root
        self._symbol_cache: Dict[str, List[Symbol]] = {}
        self._indexed_files: List[Path] = []
        self._file_content_cache: Dict[Path, str] = {}
        self._reference_counts: Dict[str, int] = {}
        self._is_indexed = False

    def index_project(self, files: List[Path]):
        """
        Build a global symbol index for fast lookup.
        """
        self._symbol_cache.clear()
        self._file_content_cache.clear()
        self._reference_counts.clear()
        self._indexed_files = files
        from . import io
        import re

        print(f"LSP: Indexing {len(files)} files...")
        # 1. First pass: Index symbols and cache content
        for f in files:
            content = io.read_text(f)
            if content:
                self._file_content_cache[f] = content
            
            # Use scan_file to benefit from cache
            scan_result = scanner.scan_file(f, self.root)
            for sym in scan_result.symbols:
                if sym.name not in self._symbol_cache:
                    self._symbol_cache[sym.name] = []
                self._symbol_cache[sym.name].append(sym)
        
        print(f"LSP: Found {len(self._symbol_cache)} unique symbols.")
        # 2. Second pass: Pre-calculate reference counts (Global Word Count)
        word_pattern = re.compile(r'\b\w+\b')
        for content in self._file_content_cache.values():
            for word in word_pattern.findall(content):
                if word in self._symbol_cache:
                    self._reference_counts[word] = self._reference_counts.get(word, 0) + 1
                    
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
