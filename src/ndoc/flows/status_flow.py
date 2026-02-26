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
import time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

from ..core import fs, io
from ..core.logger import logger
from ..parsing import scanner
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
    final_ignore = ignore_patterns + ["_STATUS.md", "_NEXT.md", "_TODO.md"]
    valid_langs = {'python', 'javascript', 'typescript', 'text', 'config', 'web', 'c', 'cpp', 'java', 'c_sharp', 'go', 'rust', 'dart'}

    for file_path, lang in fs.scan_project_files(root, final_ignore):
        if lang not in valid_langs and lang != 'unknown':
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

def sync_tasks(status_file: Path, todos: List[TodoItem]) -> bool:
    return sync_task_checkboxes(status_file, todos)

def sync_next_tasks(next_file: Path, todos: List[TodoItem]) -> bool:
    return sync_task_checkboxes(next_file, todos, log_prefix="Auto-completing task #")

def update_next_file(config: ProjectConfig, todos: Optional[List[TodoItem]] = None) -> bool:
    next_file = config.scan.root_path / "_NEXT.md"
    if todos is None:
        todos = collect_todos(config.scan.root_path, config.scan.ignore_patterns)

    logger.info("Syncing tasks with code status...")
    sync_next_tasks(next_file, todos)

    active_todos = [t for t in todos if t.type != "DONE"]
    content = format_todo_lines(active_todos, config.scan.root_path)

    start_marker = "<!-- NIKI_TODO_START -->"
    end_marker = "<!-- NIKI_TODO_END -->"

    logger.info(f"Updating TODOS in {next_file} ({len(active_todos)} active found)...")

    if not next_file.exists():
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

# --- STATS LOGIC ---

def generate_stats_section(stats: Dict, root: Path = None) -> str:
    ai_coverage = stats.get("ai_coverage", 0.0)
    doc_ratio = stats.get("ratio", 0.0)

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
| **Files** | {stats["total_files"]} | Total file count |
| **AI Context** | {stats["ai_doc_files"]} nodes | _AI.md count |
| **AI Coverage** | {ai_coverage:.1f}% | Directory coverage |
| **Doc Ratio** | {doc_ratio:.1f}% | Context lines / Code lines |
{arch_health}"""

def should_update_stats(root_path: Path, force: bool) -> bool:
    if force:
        return True
    
    rules_path = root_path / "_RULES.md"
    rules_content = io.read_text(rules_path) or ""
    
    match = re.search(r"!STATS_INTERVAL:\s*(\d+)([hms])", rules_content)
    if not match:
        interval_seconds = 3600 
    else:
        val = int(match.group(1))
        unit = match.group(2)
        if unit == 'h':
            interval_seconds = val * 3600
        elif unit == 'm':
            interval_seconds = val * 60
        else:
            interval_seconds = val

    stats_path = root_path / "_STATS.md"
    if not stats_path.exists():
        return True
        
    try:
        mtime = stats_path.stat().st_mtime
        now = time.time()
        if (now - mtime) < interval_seconds:
            return False
    except:
        return True
        
    return True

def collect_full_stats(config: ProjectConfig) -> Dict:
    root_path = config.scan.root_path
    total_files = 0
    total_lines = 0
    total_size = 0
    doc_files = 0
    doc_lines = 0
    src_files = 0
    src_lines = 0
    ai_doc_files = 0
    ai_doc_lines = 0
    ai_doc_size = 0
    total_dirs_scanned = 0
    dirs_with_ai = 0

    ignore_patterns = set(config.scan.ignore_patterns)
    include_exts = set(config.scan.extensions)

    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ignore_patterns and not d.startswith('.')]
        
        total_dirs_scanned += 1
        has_ai_in_this_dir = False
        
        for file in files:
            file_path = Path(root) / file
            
            if any(p in str(file_path) for p in ignore_patterns):
                continue
                
            total_files += 1
            try:
                size = file_path.stat().st_size
                total_size += size
                
                is_text = False
                lines_count = 0
                
                if file == '_AI.md':
                    has_ai_in_this_dir = True
                    ai_doc_files += 1
                    is_text = True
                elif file.endswith('.md'):
                    doc_files += 1
                    is_text = True
                elif file_path.suffix in include_exts:
                    src_files += 1
                    is_text = True
                
                if is_text:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines_count = sum(1 for _ in f)
                            total_lines += lines_count
                            
                            if file == '_AI.md':
                                ai_doc_lines += lines_count
                                ai_doc_size += size
                            elif file.endswith('.md'):
                                doc_lines += lines_count
                            elif file_path.suffix in include_exts:
                                src_lines += lines_count
                    except:
                        pass
                        
            except Exception as e:
                pass
        
        if has_ai_in_this_dir:
            dirs_with_ai += 1

    estimated_tokens = total_size // 4
    ai_estimated_tokens = ai_doc_size // 4
    
    ratio = 0.0
    if src_lines > 0:
        ratio = ((doc_lines + ai_doc_lines) / src_lines) * 100
    
    ai_coverage = 0.0
    if total_dirs_scanned > 0:
        ai_coverage = (dirs_with_ai / total_dirs_scanned) * 100

    return {
        "total_files": total_files,
        "total_lines": total_lines,
        "total_size": total_size,
        "estimated_tokens": estimated_tokens,
        "ai_doc_files": ai_doc_files,
        "ai_doc_lines": ai_doc_lines,
        "ai_estimated_tokens": ai_estimated_tokens,
        "ai_coverage": ai_coverage,
        "dirs_with_ai": dirs_with_ai,
        "total_dirs_scanned": total_dirs_scanned,
        "doc_files": doc_files,
        "doc_lines": doc_lines,
        "src_files": src_files,
        "src_lines": src_lines,
        "ratio": ratio
    }

def format_stats_report(stats: Dict) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# 项目统计报告 (Project Statistics)
> @CONTEXT: Project Metrics | @TAGS: @STATS @AUTO
> 最后更新 (Last Updated): {timestamp}

## 核心指标 (Core Metrics)

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **总文件数** | {stats["total_files"]} | 包含代码和文档 |
| **总行数** | {stats["total_lines"]} | 代码 + 文档总行数 |
| **项目体积** | {stats["total_size"] / 1024:.2f} KB | 磁盘占用 |
| **预估 Token** | ~{stats["estimated_tokens"]} | 全局上下文开销 (Size/4) |

## AI 上下文统计 (AI Context Stats)
> 针对 `_AI.md` 递归上下文文件的专项统计。

| 指标 (Metric) | 数值 (Value) | 说明 (Description) |
| :--- | :--- | :--- |
| **_AI.md 文件数** | {stats["ai_doc_files"]} | 局部上下文节点数 |
| **_AI.md 总行数** | {stats["ai_doc_lines"]} | 上下文总厚度 |
| **_AI.md Token** | ~{stats["ai_estimated_tokens"]} | 上下文 Token 开销 |
| **目录覆盖率** | {stats["ai_coverage"]:.1f}% ({stats["dirs_with_ai"]}/{stats["total_dirs_scanned"]}) | 包含 `_AI.md` 的目录比例 |

## 全局组成 (Global Composition)

| 类型 (Type) | 文件数 (Files) | 行数 (Lines) | 占比 (Ratio) |
| :--- | :--- | :--- | :--- |
| **源代码 (Source)** | {stats["src_files"]} | {stats["src_lines"]} | - |
| **文档 (Docs)** | {stats["doc_files"] + stats["ai_doc_files"]} | {stats["doc_lines"] + stats["ai_doc_lines"]} | {stats["ratio"]:.1f}% (Doc/Code) |

## 健康度检查 (Health Check)

- **AI 上下文覆盖率**: {stats["ai_coverage"]:.1f}%
  - {"✅ 覆盖良好 (>50%)" if stats["ai_coverage"] > 50 else "⚠️ 覆盖率较低 (<50%)，建议补充 `_AI.md`"}
- **文档/代码比率**: {stats["ratio"]:.1f}%
  - {"✅ 文档丰富 (>20%)" if stats["ratio"] > 20 else "⚠️ 文档较少 (<20%)"}
"""

def update_stats_file(config: ProjectConfig, force: bool = False) -> bool:
    root_path = config.scan.root_path
    
    if not should_update_stats(root_path, force):
        return True

    logger.info(f"Calculating statistics for {config.name}...")
    stats = collect_full_stats(config)
    content = format_stats_report(stats)
    
    stats_path = root_path / "_STATS.md"
    if io.write_text(stats_path, content):
        print(f"✅ Statistics updated: {stats_path.name}")
    
    return True

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
    stats = collect_full_stats(config)
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
        
    logger.info(f"Status Board updated: {target_file.name}")
    return True
