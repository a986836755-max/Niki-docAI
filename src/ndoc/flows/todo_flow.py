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
Flow: Todo Aggregation.
业务流：聚合代码中的 TODO/FIXME 标记到 _NEXT.md。
"""
from typing import List
from pathlib import Path
from ..models.config import ProjectConfig
from . import status_flow

TodoItem = status_flow.TodoItem

def collect_todos(root: Path, ignore_patterns: List[str]) -> List[TodoItem]:
    return status_flow.collect_todos(root, ignore_patterns)

def format_todo_lines(todos: List[TodoItem], root: Path) -> str:
    return status_flow.format_todo_lines(todos, root)

def sync_tasks(config: ProjectConfig, todos: List[TodoItem]) -> bool:
    return status_flow.sync_next_tasks(config.scan.root_path / "_NEXT.md", todos)

def run(config: ProjectConfig) -> bool:
    return status_flow.update_next_file(config)
