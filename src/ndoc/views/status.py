"""
View: Status Reports.
视图层：状态看板与统计报告渲染。
"""
from typing import List, Dict
from datetime import datetime
from pathlib import Path
from ..models.status import TodoItem
from ..core.templates import render_document

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

def format_stats_report(stats: Dict) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Pre-calculate derived values
    total_doc_files = stats["doc_files"] + stats["ai_doc_files"]
    total_doc_lines = stats["doc_lines"] + stats["ai_doc_lines"]
    
    health_ai_coverage = "✅ 覆盖良好 (>50%)" if stats["ai_coverage"] > 50 else "⚠️ 覆盖率较低 (<50%)，建议补充 `_AI.md`"
    health_doc_ratio = "✅ 文档丰富 (>20%)" if stats["ratio"] > 20 else "⚠️ 文档较少 (<20%)"
    
    return render_document(
        "stats.md.tpl",
        title="项目统计报告 (Project Statistics)",
        context="Project Metrics",
        tags="@STATS @AUTO",
        timestamp=timestamp,
        total_files=stats["total_files"],
        total_lines=stats["total_lines"],
        total_size_kb=stats["total_size"] / 1024,
        estimated_tokens=stats["estimated_tokens"],
        ai_doc_files=stats["ai_doc_files"],
        ai_doc_lines=stats["ai_doc_lines"],
        ai_estimated_tokens=stats["ai_estimated_tokens"],
        ai_coverage=stats["ai_coverage"],
        dirs_with_ai=stats["dirs_with_ai"],
        total_dirs_scanned=stats["total_dirs_scanned"],
        src_files=stats["src_files"],
        src_lines=stats["src_lines"],
        total_doc_files=total_doc_files,
        total_doc_lines=total_doc_lines,
        ratio=stats["ratio"],
        health_ai_coverage=health_ai_coverage,
        health_doc_ratio=health_doc_ratio
    )
