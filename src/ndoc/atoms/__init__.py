# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Core Building Blocks.
原子能力层：项目的核心构建块。
Legacy re-exports for backward compatibility during refactor.
"""

# Re-export core modules
from ..core import fs
from ..core import io
from ..core import capabilities
from ..core.capabilities import CapabilityManager
from ..core import text_utils

# Re-export parsing modules
from ..parsing import scanner
from ..parsing import ast
from ..parsing import deps
from ..parsing import langs

# Re-export brain modules
from ..brain import cache
from ..brain import checker
from ..brain import hippocampus
from ..brain import index
from ..brain import llm

# Re-export interfaces
from ..interfaces import lsp
