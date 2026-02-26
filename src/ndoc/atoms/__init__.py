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
Atoms: DEPRECATED (Refactoring in progress).
This module was a 'God Module' re-exporting everything.
Consumers should import directly from:
- ndoc.core
- ndoc.parsing
- ndoc.brain
- ndoc.interfaces
"""
# Intentionally empty to force direct imports and break circular dependencies.
