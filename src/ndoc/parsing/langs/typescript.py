from . import LanguageDefinition

class TypescriptDefinition(LanguageDefinition):
    ID = "typescript"
    EXTENSIONS = [".ts", ".tsx"]
    CLASS_TYPES = ["class_declaration", "interface_declaration", "enum_declaration"]
    SCM_QUERY = """
(class_declaration
  name: (type_identifier) @name
) @class_def

(interface_declaration
  name: (type_identifier) @name
) @class_def

(enum_declaration
  name: (identifier) @name
) @struct_def

(function_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
  return_type: (type_annotation)? @ret
) @func_def

(method_definition
  ((accessibility_modifier) @visibility)?
  name: (_) @name
  parameters: (formal_parameters) @params
  return_type: (type_annotation)? @ret
) @func_def

(public_field_definition
  ((accessibility_modifier) @visibility)?
  name: (_) @field_name
  type: (type_annotation)? @field_type
  value: (_)? @field_value
) @field_def

(variable_declarator
  name: (identifier) @name
  value: [
    (function_expression
      parameters: (formal_parameters) @params
      return_type: (type_annotation)? @ret
    )
    (arrow_function
      parameters: [
        (formal_parameters)
        (identifier)
      ] @params
      return_type: (type_annotation)? @ret
    )
  ]
) @func_def

(variable_declarator
  name: (identifier) @field_name
  value: [
    (number)
    (string)
    (true)
    (false)
    (null)
    (array)
    (object)
  ] @field_value
) @field_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        if name.startswith('#') or name.startswith('_'):
            return False
        return True
