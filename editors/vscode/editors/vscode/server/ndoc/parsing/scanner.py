# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - DOD Architecture: `scanner.py` (Engine) MUST NOT contain business logic. It delegates to `extractors.py` (Pure Logi...
# - Pure Extractors: Functions in `extractors.py` must be pure (no side effects, no I/O).
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Content Scanner Engine.
原子能力：内容扫描引擎 (IO & Parallelism).

REFACTORED (DOD):
- Data Models -> ndoc.models.scan
- Pure Logic -> ndoc.parsing.extractors
- Engine -> ndoc.parsing.scanner (This file)
"""

import os
import concurrent.futures
from typing import List, Optional, Dict, Tuple
from pathlib import Path

from ..models.symbol import Tag, Symbol
from ..models.context import Section
from ..core import cache

# --- Import Data Models (DOD Step 1) ---
from ..models.scan import ScanResult, TokenRule

# --- Import Pure Extractors (DOD Step 2) ---
from .extractors import (
    extract_todos,
    extract_memories,
    extract_docstring,
    extract_summary,
    extract_special_comments,
    regex_scan,
    scan_file_content,
    parse_tags,
    parse_sections
)

# --- Global Cache ---
_CACHE: Optional[cache.FileCache] = None

def get_cache(root: Path, cache_dir: Path = None) -> cache.FileCache:
    global _CACHE
    if cache_dir is None:
        # Allow override via env var for testing/benchmarking
        env_cache = os.environ.get("NDOC_CACHE_DIR")
        if env_cache:
            cache_dir = Path(env_cache)
        else:
            # Use a new cache directory to avoid locks on the old one
            cache_dir = root / ".ndoc" / "cache_v2"
        
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        # print(f"Warning: Failed to create cache directory {cache_dir}: {e}")
        return None
    
    # Use global cache instance
    if _CACHE is None or getattr(_CACHE, 'cache_dir', None) != cache_dir:
        from ..core import cache
        try:
            # Rotate DB name to avoid I/O locks during dev
            _CACHE = cache.FileCache(cache_dir, db_name="ndoc_cache.db")
        except Exception as e:
            # print(f"Warning: Failed to initialize cache: {e}")
            return None
        
    return _CACHE

# --- Helper Functions for Parallel Execution ---

def _reconstruct_result(cached_data: dict, file_path: Path) -> ScanResult:
    """Helper to reconstruct ScanResult from cached dict."""
    tags = [Tag(**t) for t in cached_data.get('tags', []) if isinstance(t, dict)]
    symbols = []
    for s in cached_data.get('symbols', []):
        if isinstance(s, dict):
            # Ensure path is set even if not in cache
            if 'path' not in s or not s['path']:
                s['path'] = str(file_path)
            symbols.append(Symbol(**s))
    sections = {k: Section(**v) for k, v in cached_data.get('sections', {}).items() if isinstance(v, dict)}
    
    return ScanResult(
        tags=tags,
        sections=sections,
        symbols=symbols,
        docstring=cached_data.get('docstring', ""),
        summary=cached_data.get('summary', ""),
        todos=cached_data.get('todos', []),
        memories=cached_data.get('memories', []),
        decisions=cached_data.get('decisions', []),
        intents=cached_data.get('intents', []),
        lessons=cached_data.get('lessons', []),
        calls=cached_data.get('calls', []),
        imports=cached_data.get('imports', []),
        tokens=cached_data.get('tokens', {}),
        is_core=cached_data.get('is_core', False)
    )

def _scan_worker(args: Tuple[Path, Path]) -> Tuple[Path, Optional[dict]]:
    """
    Worker function for parallel scanning.
    Args:
        args: Tuple of (file_path: Path, root: Path)
    Returns:
        Tuple[Path, Optional[dict]]: (file_path, serialized_scan_result)
    """
    file_path, root = args
    try:
        # Avoid circular imports inside worker
        from ..core import io
        content = io.read_text(file_path)
        if content is None:
            return file_path, None
            
        # Perform fresh scan (CPU intensive)
        # Note: scan_file_content is imported from .extractors
        result = scan_file_content(content, file_path)
        
        # Serialize immediately
        cache_data = {
            'tags': [vars(t) for t in result.tags],
            'sections': {k: vars(v) for k, v in result.sections.items()},
            'symbols': [vars(s) for s in result.symbols],
            'docstring': result.docstring,
            'summary': result.summary,
            'todos': result.todos,
            'memories': result.memories,
            'decisions': result.decisions,
            'intents': result.intents,
            'lessons': result.lessons,
            'calls': result.calls,
            'imports': result.imports,
            'tokens': result.tokens,
            'is_core': result.is_core
        }
        return file_path, cache_data
    except Exception as e:
        # In case of worker failure, LOG IT and return None
        # We use print here because logging might not be configured in worker process
        print(f"❌ [Worker Error] Failed to scan {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return file_path, None

def scan_project(root: Path, ignore_patterns: List[str] = None) -> Dict[Path, ScanResult]:
    """
    Scan the entire project (High-level API) with Parallel Execution.
    """
    from ..core import fs
    
    # Phase 1: Check Cache (Main Process)
    c = get_cache(root)
    results = {}
    
    if ignore_patterns is None:
        ignore_patterns = []
        
    all_files = list(fs.walk_files(root, ignore_patterns))
    tasks = []
    
    # 1. Check Cache (Main Process)
    # Filter files that actually need scanning
    for file_path in all_files:
        if c and not c.is_changed(file_path):
            cached_data = c.get(file_path)
            if cached_data:
                try:
                    results[file_path] = _reconstruct_result(cached_data, file_path)
                    continue
                except Exception:
                    pass
        
        # Cache Miss: Add to tasks
        tasks.append((file_path, root))
        
    # Phase 1.5: Ensure Languages (Main Process)
    # Detect required languages to trigger auto-build BEFORE parallel execution
    from .langs import get_lang_id_by_ext
    from ..core.capabilities import CapabilityManager
    
    needed_langs = set()
    for file_path in all_files:
        lang = get_lang_id_by_ext(file_path.suffix.lower())
        if lang:
            needed_langs.add(lang)
            
    if needed_langs:
        # Trigger capability check/build in main process
        # We iterate to allow individual handling (e.g. Dart native build)
        for lang in needed_langs:
            CapabilityManager.get_language(lang, auto_install=True)

    # Phase 2: Parallel Scanning
    # If workers=1, run sequential (easier for debugging)
    use_parallel = os.environ.get("NDOC_PARALLEL", "1") != "0"
    
    if tasks:
        # Use ProcessPoolExecutor
        # Max workers = CPU count (default) or 4 minimum
        max_workers = os.cpu_count() or 4
        
        # We use map to keep order, though not strictly required
        if use_parallel and max_workers > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                future_results = executor.map(_scan_worker, tasks)
                
                for file_path, cache_data in future_results:
                    if cache_data:
                        # Update Cache (Main Process)
                        if c:
                            c.update(file_path, cache_data)
                        # Reconstruct Result
                        results[file_path] = _reconstruct_result(cache_data, file_path)
                    else:
                        # Failed scan
                        results[file_path] = ScanResult()
        else:
            # Sequential Fallback
            for i, task in enumerate(tasks):
                file_path, cache_data = _scan_worker(task)
                if cache_data:
                    if c:
                        c.update(file_path, cache_data)
                    results[file_path] = _reconstruct_result(cache_data, file_path)
                else:
                    results[file_path] = ScanResult()

    # 3. Save Cache (Main Process)
    if c:
        c.save()
            
    return results

def scan_file(file_path: Path, root: Path, force: bool = False) -> ScanResult:
    """
    扫描单个文件，支持缓存 (Scan single file with cache support).
    """
    c = get_cache(root)
    if c and not force and not c.is_changed(file_path):
        cached_data = c.get(file_path)
        if cached_data:
            try:
                return _reconstruct_result(cached_data, file_path)
            except Exception:
                pass

    # Perform fresh scan (Synchronous reuse of worker logic)
    _, cache_data = _scan_worker((file_path, root))
    
    if cache_data:
        if c:
            c.update(file_path, cache_data)
            c.save()
        return _reconstruct_result(cache_data, file_path)
        
    return ScanResult()
