"""
Flow: Map Generation.
业务流：生成项目结构图 (_MAP.md)。
"""
from pathlib import Path
from dataclasses import dataclass
from typing import List, Callable

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

def format_file_entry(path: Path, level: int) -> str:
    """
    Format file entry: * `name` - summary
    Reads first few lines to extract summary using scanner.
    """
    indent = "    " * level
    name = path.name
    
    # Skip summary for meta files to keep map clean?
    # Or maybe useful to see what _TECH.md is.
    
    summary = ""
    try:
        content = io.read_text(path)
        if content:
            # Only need partial scan for summary, but scanner does full.
            # Optimization: pass content to scanner.extract_summary directly?
            # But we need docstring first.
            docstring = scanner.extract_docstring(content)
            raw_summary = scanner.extract_summary(content, docstring)
            if raw_summary:
                # Truncate if too long
                if len(raw_summary) > 50:
                    raw_summary = raw_summary[:47] + "..."
                summary = f" - *{raw_summary}*"
    except Exception:
        pass

    return f"{indent}*   `{name}`{summary}"

# --- Engine (Recursive Pipeline) ---

def build_tree_lines(current_path: Path, context: MapContext, level: int = 0) -> List[str]:
    """
    递归构建树行列表 (Recursively build tree lines).
    Implementation: Recursive Pipeline.
    """
    lines = []
    
    # 1. Construct Filter (Data)
    filter_config = fs.FileFilter(ignore_patterns=set(context.ignore_patterns))

    # 2. Get Entries (IO + Filter + Sort via Atom)
    entries = fs.list_dir(current_path, filter_config)

    for entry in entries:
        # 3. Transform (Format)
        if entry.is_dir():
            lines.append(format_dir_entry(entry.name, level))
            # Recurse
            lines.extend(build_tree_lines(entry, context, level + 1))
        else:
            lines.append(format_file_entry(entry, level))
            
    return lines

def generate_tree_content(config: ProjectConfig) -> str:
    """
    生成树内容 (Generate tree content).
    Pipeline: Config -> Context -> Build Lines -> Join.
    """
    context = MapContext(
        root=config.scan.root_path,
        ignore_patterns=config.scan.ignore_patterns
    )
    
    lines = build_tree_lines(context.root, context)
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
    
    if not map_file.exists():
        template = f"""# Project Map
> @CONTEXT: Map | Project Structure

## @STRUCTURE
{start_marker}
{tree_content}
{end_marker}
"""
        return io.write_text(map_file, template)
    else:
        return io.update_section(map_file, start_marker, end_marker, tree_content)
