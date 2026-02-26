"""
Atoms: Lightweight LSP-like features.
原子能力：轻量级 LSP 特性（定义跳转、引用查找等）。
"""
from typing import List, Optional, Dict, Any
from pathlib import Path
import time
from ..models.symbol import Symbol
from ..parsing import scanner
from ..core import io
from ..core.logger import logger

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

    def index_project(self, files: Optional[List[Path]] = None, config: Any = None):
        """
        Build a global symbol index for fast lookup using optimized Parallel Scanner.
        """
        start_time = time.time()
        self._symbol_cache.clear()
        self._reference_counts.clear()
        
        self._indexed_files = list(files) if files else []
        
        # print(f"LSP: Indexing project (Parallel + Cached)...")
        # print("DEBUG: LSP index_project start")
        scan_results = {}
        target_files = files
        
        t0 = time.time()
        if target_files is None:
            try:
                # print("DEBUG: Loading config...")
                # Avoid circular import by passing config
                if config:
                    from ..core import fs
                    # print("DEBUG: Walking files...")
                    target_files = list(fs.walk_files(self.root, config.scan.ignore_patterns, extensions=config.scan.extensions))
                    # print(f"DEBUG: Found {len(target_files)} target files")
                else:
                    # Fallback (Basic scan without ignore patterns)
                    from ..core import fs
                    target_files = list(fs.walk_files(self.root, []))
            except Exception:
                target_files = []
        t1 = time.time()
        logger.debug(f"LSP File walking took {t1 - t0:.4f}s")

        if target_files:
            try:
                # print("DEBUG: Checking langs...")
                from ..parsing.langs import get_lang_id_by_ext
                from ..core.capabilities import CapabilityManager
                needed_langs = set()
                # Optimized check: Only check langs if cache is invalid or missing?
                # But we need langs loaded to scan.
                # Let's rely on scanner.scan_project doing the check efficiently.
                pass 
            except Exception:
                pass
            
            # Use scan_project if scanning whole root, or manual loop if specific files
            # Actually scanner.scan_project handles cache efficiently now.
            # But here we have specific list of files.
            
            # Let's use scanner.scan_project logic but for specific files
            # OR just call scan_file which now checks cache
            
            t2 = time.time()
            # Batch optimization: pre-load cache
            scanner.get_cache(self.root)
            t3 = time.time()
            logger.debug(f"LSP Cache load took {t3 - t2:.4f}s")
            
            # Check which files actually need scanning (Cache Miss)
            files_to_scan = []
            cached_results = {}
            c = scanner.get_cache(self.root)
            
            t4 = time.time()
            for file_path in target_files:
                if c and not c.is_changed(file_path):
                    data = c.get(file_path)
                    if data:
                        cached_results[file_path] = scanner._reconstruct_result(data, file_path)
                        continue
                files_to_scan.append(file_path)
            t5 = time.time()
            # print(f"DEBUG: Cache check & reconstruction took {t5 - t4:.4f}s")

            if files_to_scan:
                logger.info(f"LSP: Scanning {len(files_to_scan)} changed files...")
                # Ensure langs for changed files
                try:
                    from ..parsing.langs import get_lang_id_by_ext
                    from ..core.capabilities import CapabilityManager
                    needed = set()
                    for fp in files_to_scan:
                        lid = get_lang_id_by_ext(fp.suffix.lower())
                        if lid: needed.add(lid)
                    if needed:
                        CapabilityManager.ensure_languages(needed, auto_install=False)
                except:
                    pass

                t6 = time.time()
                for file_path in files_to_scan:
                    result = scanner.scan_file(file_path, self.root)
                    if result:
                        scan_results[file_path] = result
                t7 = time.time()
                logger.debug(f"LSP Actual scanning took {t7 - t6:.4f}s")
            
            # Merge cached results
            scan_results.update(cached_results)
            
        elif files is not None and not files:
            # Explicitly empty list passed, do nothing
            scan_results = {}
        else:
            scan_results = scanner.scan_project(self.root)
            self._indexed_files = list(scan_results.keys())
        
        # 1. First pass: Index symbols
        t8 = time.time()
        count_sym = 0
        for f, result in scan_results.items():
            for sym in result.symbols:
                sym.path = f
                if sym.name not in self._symbol_cache:
                    self._symbol_cache[sym.name] = []
                self._symbol_cache[sym.name].append(sym)
                count_sym += 1
        
        # print(f"LSP: Found {len(self._symbol_cache)} unique symbols.")
        # print(f"LSP: Found {len(self._symbol_cache)} unique symbols ({count_sym} total).")
        
        # 2. Second pass: Aggregate reference counts from pre-calculated tokens
        # No need to read file content or run regex again!
        for f, result in scan_results.items():
            for word, count in result.tokens.items():
                if word in self._symbol_cache:
                    self._reference_counts[word] = self._reference_counts.get(word, 0) + count
        
        t9 = time.time()
        logger.debug(f"LSP Index building took {t9 - t8:.4f}s")
                    
        self._is_indexed = True
        end_time = time.time()
        logger.info(f"LSP: Index built in {end_time - start_time:.4f}s ({len(self._symbol_cache)} symbols, {len(self._reference_counts)} refs)")
        # print(f"LSP: Pre-calculated reference counts for {len(self._reference_counts)} symbols.")

    def update_file(self, file_path: Path):
        """
        Incrementally update index for a single file.
        Used by Watcher.
        """
        # 1. Re-scan file (will update cache automatically)
        result = scanner.scan_file(file_path, self.root, force=True)
        
        # 2. Update memory index?
        # This is tricky because removing old symbols requires tracking which symbols belonged to this file.
        # For now, we can just append new symbols (might cause duplicates in search results, but acceptable for MVP)
        # Ideally, we should remove old entries first.
        
        # Remove old symbols from this file
        for name, syms in self._symbol_cache.items():
            self._symbol_cache[name] = [s for s in syms if str(s.path) != str(file_path)]
            
        # Add new symbols
        for sym in result.symbols:
            if sym.name not in self._symbol_cache:
                self._symbol_cache[sym.name] = []
            self._symbol_cache[sym.name].append(sym)
            
        # Update reference counts?
        # Would require diffing tokens. Complex.
        # For now, maybe just skip updating ref counts in watch mode, or re-index whole project periodically?
        # Let's skip ref count update for single file to keep it fast.
        pass

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

        for fpath in self._indexed_files:
            try:
                content = io.read_text(fpath)
                if not content: continue
                for i, line in enumerate(content.splitlines()):
                    if pattern.search(line):
                        references.append({
                            "path": str(fpath),
                            "line": i + 1,
                            "content": line.strip()
                        })
            except Exception:
                continue
        return references

# Global instance for easy access
_INSTANCE: Optional[LSPService] = None

def get_service(root: Path) -> LSPService:
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = LSPService(root)
    return _INSTANCE
