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

def _extract_rule_block(content: str) -> List[str]:
    lines = content.splitlines()
    in_block = False
    collected: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## !RULE"):
            in_block = True
            continue
        if in_block and stripped.startswith("## "):
            break
        if in_block:
            if not stripped:
                continue
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue
            collected.append(line.rstrip())
    return collected

class LSPService:
    def __init__(self, root: Path):
        self.root = Path(root) if isinstance(root, str) else root
        self._symbol_cache: Dict[str, List[Symbol]] = {}
        self._indexed_files: List[Path] = []
        # self._file_content_cache: Dict[Path, str] = {} # Removed for memory optimization
        self._reference_counts: Dict[str, int] = {}
        self._is_indexed = False
        self.semantic_index = None # Cache for semantic index (rules)
        self._context_cache: Dict[Path, str] = {}
        self._context_cache_deps: Dict[Path, Dict[Path, float]] = {}
        self._ai_rule_cache: Dict[Path, List[str]] = {}
        self._ai_rule_mtime: Dict[Path, float] = {}

    def index_project(self, files: Optional[List[Path]] = None):
        """
        Build a global symbol index for fast lookup using optimized Parallel Scanner.
        """
        self._symbol_cache.clear()
        self._reference_counts.clear()
        
        self._indexed_files = list(files) if files else []
        
        print(f"LSP: Indexing project (Parallel + Cached)...")
        scan_results = {}
        target_files = files
        if target_files is None:
            try:
                from ..flows import config_flow
                from ..core import fs
                config = config_flow.load_project_config(self.root)
                target_files = list(fs.walk_files(self.root, config.scan.ignore_patterns, extensions=config.scan.extensions))
            except Exception:
                target_files = []

        if target_files:
            try:
                from ..parsing.langs import get_lang_id_by_ext
                from ..core.capabilities import CapabilityManager
                needed_langs = set()
                for file_path in target_files:
                    lang = get_lang_id_by_ext(file_path.suffix.lower())
                    if lang:
                        needed_langs.add(lang)
                if needed_langs:
                    CapabilityManager.ensure_languages(needed_langs, auto_install=False)
            except Exception:
                pass
            for file_path in target_files:
                result = scanner.scan_file(file_path, self.root)
                if result:
                    scan_results[file_path] = result
        else:
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

    def invalidate_context_cache(self, changed_path: Optional[Path] = None) -> None:
        if not changed_path:
            self._context_cache.clear()
            self._context_cache_deps.clear()
            self._ai_rule_cache.clear()
            self._ai_rule_mtime.clear()
            return
        changed_path = Path(changed_path)
        self._ai_rule_cache.pop(changed_path, None)
        self._ai_rule_mtime.pop(changed_path, None)
        to_remove = []
        for file_path, deps in self._context_cache_deps.items():
            if changed_path in deps:
                to_remove.append(file_path)
        for file_path in to_remove:
            self._context_cache.pop(file_path, None)
            self._context_cache_deps.pop(file_path, None)

    def _get_ai_rules(self, ai_path: Path) -> List[str]:
        try:
            mtime = ai_path.stat().st_mtime
        except OSError:
            return []
        cached_mtime = self._ai_rule_mtime.get(ai_path)
        if cached_mtime == mtime and ai_path in self._ai_rule_cache:
            return self._ai_rule_cache[ai_path]
        content = io.read_text(ai_path)
        rules = _extract_rule_block(content)
        self._ai_rule_cache[ai_path] = rules
        self._ai_rule_mtime[ai_path] = mtime
        return rules

    def get_context_for_file(self, file_path: Path) -> str:
        context_parts = []
        try:
            root = self.root
            current = file_path.parent if file_path.is_file() else file_path
            ai_paths = []
            while str(current).startswith(str(root)):
                candidate = current / "_AI.md"
                if candidate.exists():
                    ai_paths.append(candidate)
                if current == root:
                    break
                current = current.parent

            deps: Dict[Path, float] = {}
            for ai_path in ai_paths:
                try:
                    deps[ai_path] = ai_path.stat().st_mtime
                except OSError:
                    deps[ai_path] = -1.0

            cached = self._context_cache.get(file_path)
            cached_deps = self._context_cache_deps.get(file_path)
            if cached and cached_deps == deps:
                return cached

            for ai_path in reversed(ai_paths):
                rules = self._get_ai_rules(ai_path)
                if not rules:
                    continue
                try:
                    rel = ai_path.relative_to(root)
                    display_path = rel.as_posix()
                except ValueError:
                    display_path = str(ai_path)
                context_parts.append(f"### {display_path}")
                context_parts.extend(rules)
                context_parts.append("")
        except Exception:
            pass
        result = "\n".join(context_parts).strip()
        self._context_cache[file_path] = result
        self._context_cache_deps[file_path] = deps if 'deps' in locals() else {}
        return result

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
