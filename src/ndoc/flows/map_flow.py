"""
Flow: Map Generation.
业务流：生成项目结构图 (_MAP.md)。
"""
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Callable, Dict
from concurrent.futures import ThreadPoolExecutor

from ..atoms import fs, io, scanner
from ..models.config import ProjectConfig

# --- Data Structures (Pipeline Config) ---

@dataclass
class MapContext:
    root: Path
    ignore_patterns: List[str]
    # No state, just configuration data

# --- Transformations (Pure Functions) ---

def format_dir_entry(name: str, level: int) -> str:
    """Format directory entry: * **name/**"""
    indent = "    " * level
    return f"{indent}*   **{name}/**"

def format_file_entry(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str:
    """
    Format file entry: * [`name`](path#L1) - summary
    Uses provided summary cache or skips summary extraction.
    """
    indent = "    " * level
    name = path.name
    
    # Calculate relative path for link
    try:
        rel_path = path.relative_to(root).as_posix()
    except ValueError:
        rel_path = name # Fallback
    
    summary = ""
    if summary_cache and path in summary_cache:
        raw_summary = summary_cache[path]
        if raw_summary:
            # Truncate if too long
            if len(raw_summary) > 50:
                raw_summary = raw_summary[:47] + "..."
            summary = f" - *{raw_summary}*"
    
    # Link with #L1
    return f"{indent}*   [`{name}`]({rel_path}#L1){summary}"

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

# --- Engine (Recursive Pipeline) ---

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
            lines.append(format_dir_entry(entry.name, level))
            # Recurse
            lines.extend(build_tree_lines(entry, context, level + 1, summary_cache))
        else:
            # Pass context.root for relative path calculation
            lines.append(format_file_entry(entry, context.root, level, summary_cache))
            
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

# --- Entry Point (Flow) ---

def run(config: ProjectConfig) -> bool:
    """
    执行 Map 生成流 (Execute Map Flow).
    Pipeline: Config -> Generate -> Update IO.
    """
    map_file = config.scan.root_path / "_MAP.md"
    
    # 1. Generate Content (Pure)
    tree_content = generate_tree_content(config)
    
    # 2. Define Markers (Data)
    start_marker = "<!-- NIKI_MAP_START -->"
    end_marker = "<!-- NIKI_MAP_END -->"
    
    # 3. Execute IO (Side Effect)
    print(f"Updating MAP at {map_file}...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not map_file.exists():
        template = f"""# Project Map
> @CONTEXT: Map | Project Structure
> 最后更新 (Last Updated): {timestamp}

## @STRUCTURE
{start_marker}
{tree_content}
{end_marker}
"""
        return io.write_text(map_file, template)
    else:
        # Update body
        success = io.update_section(map_file, start_marker, end_marker, tree_content)
        # Update header timestamp
        if success:
            io.update_header_timestamp(map_file)
        return success
