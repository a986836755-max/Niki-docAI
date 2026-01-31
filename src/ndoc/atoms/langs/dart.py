from . import LanguageDefinition

class DartDefinition(LanguageDefinition):
    ID = "dart"
    EXTENSIONS = [".dart"]
    CLASS_TYPES = ["class_definition", "mixin_declaration", "enum_declaration"]
    SCM_QUERY = """
(class_definition name: (identifier) @name) @class_def
(mixin_declaration name: (identifier) @name) @struct_def
(enum_declaration name: (identifier) @name) @struct_def
(function_definition name: (identifier) @name) @func_def
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        return not name.startswith('_')
