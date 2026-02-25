# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure ...
# *   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and install...
# *   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Status Board Generation.
业务流：生成项目状态看板 (_STATUS.md)。
合并原有的 Next (Todo) 和 Stats Flow。
"""
import re
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from ..atoms import fs, io, scanner
from ..brain import checker
from ..models.config import ProjectConfig
from .deps_flow import collect_imports, build_dependency_graph, find_circular_dependencies

# --- TODO/NEXT LOGIC ---

@dataclass
class TodoItem:
    file_path: Path
    line: int
    type: str  # TODO, FIXME, etc.
    content: str
    task_id: Optional[str] = None
    
    @property
    def priority_icon(self) -> str:
        icons = {
            "FIXME": "🔴", # High
            "XXX": "🟣",   # Critical
            "HACK": "🚧",  # Warning
            "TODO": "🔵",  # Medium
            "NOTE": "ℹ️"   # Info
        }
        return icons.get(self.type, "⚪")

def collect_todos(root: Path, ignore_patterns: List[str]) -> List[TodoItem]:
    todos = []
    # Avoid self-referencing _STATUS.md and legacy files
    ignore = set(ignore_patterns + ["_STATUS.md", "_NEXT.md", "_TODO.md"])
    files = fs.walk_files(root, list(ignore))
    
    for file_path in files:
        if file_path.suffix not in ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.ts', '.html', '.css', '.rs', '.go', '.java', '.c', '.cpp', '.cs']:
            continue
            
        try:
            scan_result = scanner.scan_file(file_path, root)
            raw_todos = scan_result.todos
            
            for t in raw_todos:
                todos.append(TodoItem(
                    file_path=file_path,
                    line=t['line'],
                    type=t['type'],
                    task_id=t.get('task_id'),
                    content=t['content']
                ))
        except Exception:
            pass
    return todos

def format_todo_lines(todos: List[TodoItem], root: Path) -> str:
    if not todos:
        return "* *No code todos found.*"
    lines = []
    priority_order = {"FIXME": 0, "XXX": 1, "HACK": 2, "TODO": 3, "NOTE": 4}
    sorted_todos = sorted(todos, key=lambda x: (priority_order.get(x.type, 99), x.file_path, x.line))
    
    for todo in sorted_todos:
        rel_path = todo.file_path.relative_to(root).as_posix()
        link = f"[{rel_path}:{todo.line}]({rel_path}#L{todo.line})"
        line = f"*   {todo.priority_icon} **{todo.type}** {link}: {todo.content}"
        lines.append(line)
    return "\n".join(lines)

def sync_tasks(status_file: Path, todos: List[TodoItem]) -> bool:
    """
    Sync checkboxes in _STATUS.md based on code status.
    """
    if not status_file.exists():
        return False

    content = io.read_text(status_file)
    if not content:
        return False

    active_ids = {t.task_id for t in todos if t.task_id and t.type != "DONE"}
    done_ids = {t.task_id for t in todos if t.task_id and t.type == "DONE"}

    lines = content.splitlines()
    new_lines = []
    modified = False

    task_pattern = re.compile(r"^(\s*\*\s*\[\s*\]\s*)#([\w-]+)(.*)$")

    for line in lines:
        match = task_pattern.match(line)
        if match:
            prefix, task_id, suffix = match.groups()
            should_complete = False
            if task_id in done_ids:
                should_complete = True
            elif task_id not in active_ids and len(active_ids | done_ids) > 0:
                should_complete = True
            
            if should_complete:
                new_line = line.replace("[ ]", "[x]")
                new_lines.append(new_line)
                modified = True
                continue
        
        new_lines.append(line)

    if modified:
        return io.write_text(status_file, "\n".join(new_lines))
    return True

# --- STATS LOGIC ---

def calculate_stats(root_path: Path, ignore_patterns: List[str]) -> Dict:
    stats = {
        "files": 0, "lines": 0, "size": 0,
        "ai_files": 0, "ai_lines": 0,
        "src_files": 0, "src_lines": 0,
        "dirs_scanned": 0, "dirs_with_ai": 0
    }
    
    ignore = set(ignore_patterns)
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ignore and not d.startswith('.')]
        stats["dirs_scanned"] += 1
        has_ai = False
        
        for file in files:
            if any(p in file for p in ignore): continue
            
            fpath = Path(root) / file
            stats["files"] += 1
            try:
                size = fpath.stat().st_size
                stats["size"] += size
                
                is_text = False
                lines = 0
                
                if file == '_AI.md':
                    has_ai = True
                    stats["ai_files"] += 1
                    is_text = True
                elif file.endswith('.py') or file.endswith('.ts') or file.endswith('.js') or file.endswith('.rs') or file.endswith('.go'):
                    stats["src_files"] += 1
                    is_text = True
                
                if is_text:
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                            stats["lines"] += lines
                            if file == '_AI.md': stats["ai_lines"] += lines
                            elif file != '_AI.md': stats["src_lines"] += lines
                    except: pass
            except: pass
        
        if has_ai: stats["dirs_with_ai"] += 1
        
    return stats

def generate_stats_section(stats: Dict, root: Path = None) -> str:
    ai_coverage = 0.0
    if stats["dirs_scanned"] > 0:
        ai_coverage = (stats["dirs_with_ai"] / stats["dirs_scanned"]) * 100
        
    doc_ratio = 0.0
    if stats["src_lines"] > 0:
        doc_ratio = (stats["ai_lines"] / stats["src_lines"]) * 100

    # Architecture Health Check
    arch_health = ""
    if root:
        try:
            # 1. Check Circular Dependencies
            import_map = collect_imports(root)
            graph = build_dependency_graph(import_map)
            cycles = find_circular_dependencies(graph)
            
            cycle_status = f"✅ None" if not cycles else f"❌ **{len(cycles)} Detected**"
            
            # 2. Check Architecture Rules (Layering)
            # Need to scan all files to build FileContext list? 
            # That might be slow. We can do a quick check on imports or skip for now if too heavy.
            # Let's trust checker.py if we can feed it data.
            # For now, just circular deps is a good start for Arch Health.
            
            arch_health = f"""
## 4. Architecture Health
| Metric | Status | Details |
| :--- | :--- | :--- |
| **Circular Deps** | {cycle_status} | Dependency cycles |
"""
        except Exception as e:
            arch_health = f"\n<!-- Arch check failed: {e} -->"

    return f"""## 3. Project Health (Metrics)
| Metric | Value | Description |
| :--- | :--- | :--- |
| **Files** | {stats["files"]} | Total file count |
| **AI Context** | {stats["ai_files"]} nodes | _AI.md count |
| **AI Coverage** | {ai_coverage:.1f}% | Directory coverage |
| **Doc Ratio** | {doc_ratio:.1f}% | Context lines / Code lines |
{arch_health}"""

# --- MAIN FLOW ---

def run(config: ProjectConfig) -> bool:
    """Execute Status Flow"""
    target_file = config.scan.root_path / "_STATUS.md"
    root = config.scan.root_path
    
    print(f"Generating Status Board in {root}...")
    
    # 1. Collect Todos
    todos = collect_todos(root, config.scan.ignore_patterns)
    active_todos = [t for t in todos if t.type != "DONE"]
    
    # 2. Sync existing checkboxes
    if target_file.exists():
        sync_tasks(target_file, todos)
        
    # 3. Stats
    stats = calculate_stats(root, config.scan.ignore_patterns)
    stats_content = generate_stats_section(stats, root)
    
    # 4. Generate Content
    todo_content = format_todo_lines(active_todos, root)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Preserve existing Manual sections? 
    # For _STATUS.md, we might want to keep manual "Sprint Plan" at top.
    # We'll use sections to update parts.
    
    if not target_file.exists():
        content = f"""# Project Status Board
> @CONTEXT: Status | Time View
> 最后更新 (Last Updated): {timestamp}

## 1. Active Sprint (Sprint Plan)
> Manually add your sprint goals here.
*   [ ] Example Task 1

## 2. Code Tasks (Auto-aggregated)
<!-- NIKI_TODO_START -->
{todo_content}
<!-- NIKI_TODO_END -->

<!-- NIKI_STATS_START -->
{stats_content}
<!-- NIKI_STATS_END -->

---
*Generated by Niki-docAI*
"""
        io.write_text(target_file, content)
    else:
        # Update TODO section
        io.update_section(target_file, "<!-- NIKI_TODO_START -->", "<!-- NIKI_TODO_END -->", todo_content)
        # Update Stats section
        io.update_section(target_file, "<!-- NIKI_STATS_START -->", "<!-- NIKI_STATS_END -->", stats_content)
        # Update timestamp
        io.update_header_timestamp(target_file)
        
    print(f"✅ Status Board updated: {target_file.name}")
    return True
