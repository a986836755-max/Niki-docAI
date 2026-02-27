"""
Core: Map Builder.
核心层：项目结构树构建逻辑。
"""
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

from ..core import fs, io
from ..parsing import scanner
from ..models.map import MapContext
from ..views import map as map_view
from ..models.config import ProjectConfig

def extract_file_summary(path: Path) -> str:
    """Helper for parallel summary extraction."""
    try:
        # Use read_head for performance
        content = io.read_head(path, 4096)
        if content:
            docstring = scanner.extract_docstring(content)
            return scanner.extract_summary(content, docstring) or ""
    except Exception:
        pass
    return ""

def build_tree_lines(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]:
    """
    递归构建树行列表 (Recursively build tree lines).
    Implementation: Recursive Pipeline.
    """
    lines = []
    
    # 1. Construct Filter (Data)
    filter_config = fs.FileFilter(ignore_patterns=set(context.ignore_patterns))

    # 2. Get Entries (IO + Filter + Sort via Atom)
    entries = fs.list_dir(current_path, filter_config, root=context.root)

    for entry in entries:
        # 3. Transform (Format)
        if entry.is_dir():
            lines.append(map_view.format_dir_entry(entry.name, level))
            # Recurse
            lines.extend(build_tree_lines(entry, context, level + 1, summary_cache))
        else:
            # Pass context.root for relative path calculation
            lines.append(map_view.format_file_entry(entry, context.root, level, summary_cache))
            
    return lines

def generate_tree_content(config: ProjectConfig) -> str:
    """
    生成树内容 (Generate tree content).
    Pipeline: Config -> Context -> Parallel Summary Scan -> Build Lines -> Join.
    """
    context = MapContext(
        root=config.scan.root_path,
        ignore_patterns=config.scan.ignore_patterns
    )
    
    # 1. Pre-collect all files for parallel summary extraction
    all_files = list(fs.walk_files(context.root, context.ignore_patterns))
    
    # 2. Parallel Extraction (Speed up IO-bound tasks)
    summary_cache = {}
    if all_files:
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(extract_file_summary, all_files))
            summary_cache = dict(zip(all_files, results))
    
    # 3. Build tree using cache
    lines = build_tree_lines(context.root, context, summary_cache=summary_cache)
    return "\n".join(lines)
