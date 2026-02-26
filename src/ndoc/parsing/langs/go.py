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
