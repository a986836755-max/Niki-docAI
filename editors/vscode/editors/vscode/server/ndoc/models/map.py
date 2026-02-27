# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - POD Only: Models must be Plain Old Data (dataclasses/pydantic). No business logic methods allowed.
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Models: Map Context.
模型层：项目结构图生成所需的上下文配置。
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class MapContext:
    root: Path
    ignore_patterns: List[str]
