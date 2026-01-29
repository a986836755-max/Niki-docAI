"""
Flow: Todo Aggregation.
业务流：聚合代码中的 TODO/FIXME 标记到 _NEXT.md。
"""
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

from ..atoms import fs, io, scanner
from ..models.config import ProjectConfig

# --- Data Structures ---

@dataclass
class TodoItem:
    file_path: Path
    line: int
    type: str  # TODO, FIXME, etc.
    content: str
    
    @property
    def priority_icon(self) -> str:
        """Get icon based on type."""
        icons = {
            "FIXME": "🔴", # High
            "XXX": "🟣",   # Critical
            "HACK": "🚧",  # Warning
            "TODO": "🔵",  # Medium
            "NOTE": "ℹ️"   # Info
        }
        return icons.get(self.type, "⚪")

# --- Engine ---

def collect_todos(root: Path, ignore_patterns: List[str]) -> List[TodoItem]:
    """
    Collect all TODOs from project.
    """
    todos = []
    filter_config = fs.FileFilter(
        ignore_patterns=set(ignore_patterns + ["_NEXT.md", "_TODO.md"]) # Avoid self-referencing
    )
    
    # Reuse map_flow logic? Or simple fs walk.
    # We need to scan all files.
    
    # 1. Get all files
    # Use walk_files instead of list_files_recursive which doesn't exist
    files = fs.walk_files(root, list(filter_config.ignore_patterns))
    
    for file_path in files:
        # Only scan text files (skip binary, images, etc.)
        # Naive check by extension?
        if file_path.suffix not in ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.ts', '.html', '.css']:
            continue
            
        try:
            content = io.read_text(file_path)
            if not content:
                continue
                
            # Use scanner
            # Optimization: maybe just use extract_todos directly without full scan?
            # Yes, scanner.extract_todos is static-ish
            raw_todos = scanner.extract_todos(content)
            
            for t in raw_todos:
                todos.append(TodoItem(
                    file_path=file_path,
                    line=t['line'],
                    type=t['type'],
                    content=t['content']
                ))
        except Exception as e:
            # Ignore read errors
            pass
            
    return todos

def format_todo_lines(todos: List[TodoItem], root: Path) -> str:
    """
    Format todos into Markdown list.
    Format: * 🔴 **FIXME** `[path:line](path#Lline)`: content
    """
    if not todos:
        return "* *No code todos found.*"
        
    lines = []
    
    # Sort by priority (FIXME > XXX > HACK > TODO > NOTE)
    priority_order = {"FIXME": 0, "XXX": 1, "HACK": 2, "TODO": 3, "NOTE": 4}
    sorted_todos = sorted(todos, key=lambda x: (priority_order.get(x.type, 99), x.file_path, x.line))
    
    for todo in sorted_todos:
        rel_path = todo.file_path.relative_to(root).as_posix()
        # Markdown link to line
        link = f"[{rel_path}:{todo.line}]({rel_path}#L{todo.line})"
        
        line = f"*   {todo.priority_icon} **{todo.type}** {link}: {todo.content}"
        lines.append(line)
        
    return "\n".join(lines)

# --- Entry Point ---

def run(config: ProjectConfig) -> bool:
    """
    Execute Todo Flow.
    """
    next_file = config.scan.root_path / "_NEXT.md"
    
    # 1. Collect
    todos = collect_todos(config.scan.root_path, config.scan.ignore_patterns)
    
    # 2. Format
    content = format_todo_lines(todos, config.scan.root_path)
    
    # 3. Inject
    start_marker = "<!-- NIKI_TODO_START -->"
    end_marker = "<!-- NIKI_TODO_END -->"
    
    print(f"Updating TODOS in {next_file} ({len(todos)} found)...")
    
    if not next_file.exists():
        # Create if missing
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        template = f"""# Todo List
> @CONTEXT: Todos | _NEXT.md
> 最后更新 (Last Updated): {timestamp}

{start_marker}
{content}
{end_marker}
"""
        return io.write_text(next_file, template)
    
    success = io.update_section(next_file, start_marker, end_marker, content)
    if success:
        io.update_header_timestamp(next_file)
    return success
