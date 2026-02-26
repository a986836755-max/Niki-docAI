# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `ext...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
from . import LanguageDefinition

class DartDefinition(LanguageDefinition):
    ID = "dart"
    EXTENSIONS = [".dart"]
    CLASS_TYPES = ["class_definition", "mixin_declaration", "enum_declaration"]
    SCM_QUERY = """
(class_definition name: (identifier) @name) @class_def
(enum_declaration name: (identifier) @name) @struct_def
(function_signature name: (identifier) @name) @func_def
"""
    SCM_IMPORTS = """
(import_or_export) @import
"""

    @staticmethod
    def clean_import(import_text: str) -> str:
        # Input: "import 'package:flutter/material.dart';" or "'package:flutter/material.dart'"
        # We want: "package:flutter/material.dart"
        clean = import_text.strip()
        if clean.startswith("import ") or clean.startswith("export "):
            # Extract content inside quotes
            import re
            m = re.search(r"['\"](.*?)['\"]", clean)
            if m:
                return m.group(1)
        # Fallback for just string literal capture
        return clean.strip("'\"")
