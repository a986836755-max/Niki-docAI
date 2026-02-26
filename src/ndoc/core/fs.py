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
Atoms: File System Traversal.
原子能力：文件系统遍历。
"""
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterator, List, Set, Pattern, Callable, Optional, Tuple
import pathspec

# --- Unified File Scanning ---

def scan_project_files(root: Path, ignore_patterns: List[str], allow_extensions: Optional[Set[str]] = None) -> Iterator[Tuple[Path, str]]:
    """
    Unified generator to scan project files.
    Handles .gitignore, ignore_patterns, binary filtering, and extension filtering.
    
    Yields:
        (file_path: Path, language: str)
        language is inferred from extension (e.g., 'python', 'javascript', 'text', 'unknown')
    """
    # 1. Setup Filter
    # Always ignore common junk
    default_ignores = {'.git', '__pycache__', 'venv', 'env', 'node_modules', 'dist', 'build', 'site-packages', '.idea', '.vscode'}
    final_ignores = default_ignores.union(set(ignore_patterns))
    
    filter_config = FileFilter(
        ignore_patterns=final_ignores,
        allow_extensions=allow_extensions or set()
    )
    filter_config.spec = load_gitignore(root)
    
    # 2. Walk
    # Use walk_files (which returns list) or reimplement as generator for efficiency?
    # Let's reimplement as generator using os.walk for true laziness
    
    for dirpath, dirnames, filenames in os.walk(root):
        # In-place filter dirnames to prune traversal
        # Need to check relative path for gitignore
        # This is complex with pathspec for directories.
        # Simple name check first
        dirnames[:] = [d for d in dirnames if d not in final_ignores and not d.startswith('.')]
        
        # TODO: Advanced directory filtering with gitignore
        
        for f in filenames:
            path = Path(dirpath) / f
            
            # Check ignore
            if should_ignore(path, filter_config, root):
                continue
                
            # Check extension whitelist (if provided)
            if allow_extensions and path.suffix not in allow_extensions:
                continue
                
            # Infer language / Check binary
            lang = _infer_language(path)
            if lang == 'binary':
                continue
                
            yield path, lang

def _infer_language(path: Path) -> str:
    """Simple extension to language mapping."""
    ext = path.suffix.lower()
    if ext in ('.py', '.pyi'): return 'python'
    if ext in ('.js', '.jsx', '.mjs'): return 'javascript'
    if ext in ('.ts', '.tsx'): return 'typescript'
    if ext in ('.md', '.txt', '.rst'): return 'text'
    if ext in ('.json', '.yaml', '.yml', '.toml'): return 'config'
    if ext in ('.html', '.css', '.scss'): return 'web'
    if ext in ('.c', '.h'): return 'c'
    if ext in ('.cpp', '.hpp', '.cc'): return 'cpp'
    if ext == '.java': return 'java'
    if ext == '.cs': return 'c_sharp'
    if ext == '.go': return 'go'
    if ext == '.rs': return 'rust'
    if ext == '.dart': return 'dart'
    
    # Binary check (naive)
    if ext in ('.pyc', '.exe', '.dll', '.so', '.dylib', '.bin', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz'):
        return 'binary'
        
    return 'unknown'

# --- Data Structures (Logic as Data) ---

@dataclass
class FileFilter:
    """
    文件过滤器配置 (File Filter Configuration).
    """
    ignore_patterns: Set[str] = field(default_factory=set)
    allow_extensions: Set[str] = field(default_factory=set)
    spec: Optional[pathspec.PathSpec] = None

    @property
    def has_extension_filter(self) -> bool:
        return bool(self.allow_extensions)

# --- Engine (Pipeline) ---

def load_gitignore(root: Path) -> Optional[pathspec.PathSpec]:
    """Load .gitignore from root directory."""
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                return pathspec.PathSpec.from_lines('gitwildmatch', f)
        except Exception:
            pass
    return None

def should_ignore(path: Path, filter_config: FileFilter, root: Path = None) -> bool:
    """
    检查是否应该忽略 (Check if should ignore).
    Implementation: Table lookup (Set) + Gitignore (PathSpec).
    """
    name = path.name
    
    # 1. Hidden file check (Rule)
    if name.startswith('.') and name != '.':
        return True
        
    # 2. Ignore list lookup (Data)
    if name in filter_config.ignore_patterns:
        return True

    # 3. .gitignore check (Logic as Data)
    if filter_config.spec and root:
        try:
            rel_path = path.relative_to(root).as_posix()
            if filter_config.spec.match_file(rel_path):
                return True
        except ValueError:
            pass
            
    return False

def list_dir(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]:
    """
    列出目录内容并应用过滤 (List directory contents with filtering).
    Returns sorted list: Directories first, then files.
    """
    if not path.is_dir():
        return []

    # Auto-load gitignore if not provided and we are at root
    if not filter_config.spec and root and path == root:
        filter_config.spec = load_gitignore(root)

    try:
        entries = path.iterdir()
    except PermissionError:
        return []

    filtered_entries = []
    for entry in entries:
        # Check ignore patterns
        if should_ignore(entry, filter_config, root):
            continue
            
        # Check extensions (files only)
        if entry.is_file() and filter_config.has_extension_filter:
            if entry.suffix.lower() not in filter_config.allow_extensions:
                continue
                
        filtered_entries.append(entry)

    # Sort: Directories first (is_file=False), then files (is_file=True), then by name
    return sorted(filtered_entries, key=lambda x: (x.is_file(), x.name))

def walk_files(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]:
    """
    遍历目录并返回文件路径 (Walk directory and yield file paths).
    Implementation: Generator Pipeline.
    
    Args:
        root: 根目录
        ignore_patterns: 忽略列表
        extensions: 允许的扩展名列表
        
    Yields:
        Path: 文件路径
    """
    if not root.exists():
        return

    # 1. Prepare Data (Config Construction)
    config = FileFilter(
        ignore_patterns=set(ignore_patterns),
        allow_extensions=set(e.lower() for e in extensions) if extensions else set()
    )

    # 2. Execute Pipeline (Walk -> Filter -> Yield)
    # Load gitignore if available
    config.spec = load_gitignore(root)

    for entry in os.walk(root):
        dirpath, dirnames, filenames = entry
        curr_dir = Path(dirpath)
        
        # Prune directories
        to_remove = []
        for d in dirnames:
            d_path = curr_dir / d
            if should_ignore(d_path, config, root):
                to_remove.append(d)
        
        for d in to_remove:
            dirnames.remove(d)
        
        # Filter files
        for f in filenames:
            f_path = curr_dir / f
            if should_ignore(f_path, config, root):
                continue
                
            # Extension check (Data Lookup)
            if config.has_extension_filter:
                if f_path.suffix.lower() not in config.allow_extensions:
                    continue
            
            yield f_path

def get_relative_path(path: Path, root: Path) -> str:
    """
    获取相对路径字符串 (Get relative path string).
    
    Args:
        path: 目标路径
        root: 根路径
        
    Returns:
        str: 相对路径字符串
    """
    try:
        rel = path.relative_to(root)
        return rel.as_posix()
    except ValueError:
        return path.as_posix()
