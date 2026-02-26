from . import LanguageDefinition

class CSharpDefinition(LanguageDefinition):
    ID = "c_sharp"
    EXTENSIONS = [".cs"]
    CLASS_TYPES = ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]
    SCM_QUERY = """
(namespace_declaration
  [(qualified_name) (identifier)] @name
) @namespace_def

(class_declaration
  [(modifier) @visibility]*
  (identifier) @name
  [(base_list)]? @bases
) @class_def

(struct_declaration
  [(modifier) @visibility]*
  (identifier) @name
) @struct_def

(interface_declaration
  [(modifier) @visibility]*
  (identifier) @name
) @class_def

(record_declaration
  [(modifier) @visibility]*
  (identifier) @name
) @record_def

(enum_declaration
  [(modifier) @visibility]*
  (identifier) @name
) @enum_def

(method_declaration
  [(modifier) @visibility]*
  [(predefined_type) (identifier) (array_type) (generic_name)] @ret
  (identifier) @name
  (parameter_list) @params
) @func_def

(constructor_declaration
  [(modifier) @visibility]*
  (identifier) @name
  (parameter_list) @params
) @func_def

(property_declaration
  [(modifier) @visibility]*
  [(predefined_type) (identifier) (array_type) (generic_name)] @ret
  (identifier) @name
) @property_def
"""
    CALL_QUERY = """
(invocation_expression
  function: [(identifier) (member_access_expression)] @call_name
)
(object_creation_expression
  type: [(identifier) (predefined_type)] @call_name
)
"""
    SCM_IMPORTS = """
(using_directive) @import
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        v_lower = visibility.lower()
        if 'private' in v_lower or 'protected' in v_lower:
            return False
        return True
