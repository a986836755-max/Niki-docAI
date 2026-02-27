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
