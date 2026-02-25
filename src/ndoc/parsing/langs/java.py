# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `ext...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
from . import LanguageDefinition

class JavaDefinition(LanguageDefinition):
    ID = "java"
    EXTENSIONS = [".java"]
    CLASS_TYPES = ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]
    SCM_QUERY = """
(class_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(interface_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(enum_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(method_declaration
  (modifiers)? @visibility
  type: [
    (type_identifier)
    (void_type)
    (generic_type)
  ]? @ret
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(constructor_declaration
  (modifiers)? @visibility
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(field_declaration
  (modifiers)? @visibility
  type: (_) @field_type
  (variable_declarator
    name: (identifier) @field_name
    value: (_)? @field_value
  )
) @field_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        return True
