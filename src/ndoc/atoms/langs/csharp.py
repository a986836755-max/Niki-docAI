from . import LanguageDefinition

class CSharpDefinition(LanguageDefinition):
    ID = "c_sharp"
    EXTENSIONS = [".cs"]
    CLASS_TYPES = ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]
    SCM_QUERY = """
(class_declaration
  name: (identifier) @name
) @class_def

(struct_declaration
  name: (identifier) @name
) @struct_def

(interface_declaration
  name: (identifier) @name
) @class_def

(record_declaration
  name: (identifier) @name
) @struct_def

(method_declaration
  (modifier_list)? @visibility
  name: (identifier) @name
  parameters: (parameter_list) @params
  type: (_)? @ret
) @func_def

(constructor_declaration
  (modifier_list)? @visibility
  name: (identifier) @name
  parameters: (parameter_list) @params
) @func_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        return True
