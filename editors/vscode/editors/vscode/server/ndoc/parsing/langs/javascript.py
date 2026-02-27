from . import LanguageDefinition

class JavascriptDefinition(LanguageDefinition):
    ID = "javascript"
    EXTENSIONS = [".js", ".jsx"]
    CLASS_TYPES = ["class_declaration"]
    SCM_QUERY = """
(class_declaration
  name: (identifier) @name
) @class_def

(function_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(method_definition
  name: (_) @name
  parameters: (formal_parameters) @params
) @func_def

(field_definition
  property: (_) @field_name
  value: (_)? @field_value
) @field_def

(variable_declarator
  name: (identifier) @name
  value: [
    (function_expression
      parameters: (formal_parameters) @params
    )
    (arrow_function
      parameters: [
        (formal_parameters)
        (identifier)
      ] @params
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
        # JS private fields start with #
        if name.startswith('#') or name.startswith('_'):
            return False
        return True
