# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `ext...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
from . import LanguageDefinition

class GoDefinition(LanguageDefinition):
    ID = "go"
    EXTENSIONS = [".go"]
    CLASS_TYPES = ["type_declaration", "type_spec"]
    SCM_QUERY = """
(type_declaration
  (type_spec
    name: (type_identifier) @name
    type: (struct_type)
  )
) @struct_def

(type_declaration
  (type_spec
    name: (type_identifier) @name
    type: (interface_type)
  )
) @class_def

(function_declaration
  name: (identifier) @name
  parameters: (parameter_list) @params
  result: (_)? @ret
) @func_def

(method_declaration
  name: (field_identifier) @name
  parameters: (parameter_list) @params
  result: (_)? @ret
) @func_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        # Go visibility is based on first character being uppercase
        if not name:
            return False
        return name[0].isupper()
