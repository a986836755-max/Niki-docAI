# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `ext...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
from . import LanguageDefinition

class RustDefinition(LanguageDefinition):
    ID = "rust"
    EXTENSIONS = [".rs"]
    CLASS_TYPES = ["struct_item", "trait_item", "impl_item"]
    SCM_QUERY = """
(struct_item
  (visibility_modifier)? @visibility
  name: (type_identifier) @name
) @struct_def

(trait_item
  (visibility_modifier)? @visibility
  name: (type_identifier) @name
) @class_def

(function_item
  (visibility_modifier)? @visibility
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type_identifier)? @ret
) @func_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        # Rust default is private, unless pub is present
        return 'pub' in visibility.lower()
