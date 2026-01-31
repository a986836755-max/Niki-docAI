from . import LanguageDefinition

class CppDefinition(LanguageDefinition):
    ID = "cpp"
    EXTENSIONS = [".cpp", ".c", ".h", ".hpp"]
    CLASS_TYPES = ["class_specifier", "struct_specifier"]
    SCM_QUERY = """
(class_specifier
  name: (type_identifier) @name
) @class_def

(struct_specifier
  name: (type_identifier) @name
) @struct_def

(function_definition
  declarator: (function_declarator
    declarator: [
      (identifier) @name
      (qualified_identifier) @name
      (destructor_name) @name
    ]
  )
) @func_def

(declaration
  declarator: (function_declarator
    declarator: [
      (identifier) @name
      (qualified_identifier) @name
      (destructor_name) @name
    ]
  )
) @func_def

(field_declaration
  declarator: (function_declarator
    declarator: [
      (identifier) @name
      (destructor_name) @name
    ]
  )
) @func_def

(field_declaration
  type: (_) @field_type
  declarator: (field_identifier) @field_name
) @field_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        return True
