"""
Core: Task Management.
核心层：任务扫描与同步逻辑。
"""
import re
from pathlib import Path
from typing import List, Optional, Set

from ..core import fs, io
from ..core.logger import logger
from ..parsing import scanner
from ..models.status import TodoItem

def collect_todos(root: Path, ignore_patterns: List[str]) -> List[TodoItem]:
    todos = []
    # Avoid self-referencing _STATUS.md and legacy files
    final_ignore = ignore_patterns + ["_STATUS.md", "_NEXT.md", "_TODO.md"]
    valid_langs = {'python', 'javascript', 'typescript', 'text', 'config', 'web', 'c', 'cpp', 'java', 'c_sharp', 'go', 'rust', 'dart'}

    # Use fs.scan_project_files which is optimized
    for file_path, lang in fs.scan_project_files(root, final_ignore):
        if lang not in valid_langs and lang != 'unknown':
            continue
            
        try:
            # Use scanner which is cached
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

def sync_task_checkboxes(target_file: Path, todos: List[TodoItem], log_prefix: Optional[str] = None) -> bool:
    if not target_file.exists():
        return False

    content = io.read_text(target_file)
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
                if log_prefix:
                    logger.info(f"{log_prefix}{task_id}")
                continue
        
        new_lines.append(line)

    if modified:
        return io.write_text(target_file, "\n".join(new_lines))
    return True

def remove_stats_section(status_file: Path) -> bool:
    content = io.read_text(status_file)
    if not content:
        return False
    pattern = re.compile(r"\n?<!-- NIKI_STATS_START -->.*?<!-- NIKI_STATS_END -->\n?", re.DOTALL)
    updated = pattern.sub("", content)
    if updated != content:
        return io.write_text(status_file, updated)
    return True
