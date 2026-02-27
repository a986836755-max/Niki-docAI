# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - POD Only: Models must be Plain Old Data (dataclasses/pydantic). No business logic methods allowed.
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Models: Status & Tasks.
模型层：状态看板与任务数据结构。
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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
