from . import LanguageDefinition

class CppDefinition(LanguageDefinition):
    ID = "cpp"
    EXTENSIONS = [".cpp", ".c", ".h", ".hpp"]
    CLASS_TYPES = ["class_specifier", "struct_specifier"]
    # DEBUG: Disabled SCM_QUERY to prevent blocking on missing parser
    SCM_QUERY = ""
    CALL_QUERY = """
(call_expression
  function: [
    (identifier) @call_name
    (field_expression) @call_name
    (scoped_identifier) @call_name
  ]
)
"""
    SCM_IMPORTS = """
(preproc_include
  path: (_) @import
)
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        return True
