from typing import Any, Optional
from . import LanguageDefinition

class PythonDefinition(LanguageDefinition):
    ID = "python"
    EXTENSIONS = [".py"]
    CLASS_TYPES = ["class_definition"]
    SCM_QUERY = """
(class_definition
  name: (identifier) @name
  superclasses: (argument_list)? @superclasses
) @class_def

(function_definition
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type)? @ret
) @func_def

(decorated_definition
  (decorator) @deco
  [
    (function_definition
      name: (identifier) @name
      parameters: (parameters) @params
      return_type: (type)? @ret
    ) @func_def
    (class_definition
      name: (identifier) @name
      superclasses: (argument_list)? @superclasses
    ) @class_def
  ]
)

(class_definition
  body: (block
    (expression_statement
      (assignment
        left: (identifier) @field_name
        type: (type)? @field_type
        right: (_)? @field_value
      ) @field_def
    )
  )
)

(assignment
  left: (identifier) @field_name
  type: (type)? @field_type
  right: (_)? @field_value
) @field_def
"""

    CALL_QUERY = """
(call
  function: [(identifier) (attribute)] @call_name
)
"""
    SCM_IMPORTS = """
(import_statement) @import
(import_from_statement) @import
"""

    @staticmethod
    def is_public(name: str, visibility: str) -> bool:
        return not name.startswith('_')

    @staticmethod
    def extract_docstring(node: Any, content_bytes: bytes) -> Optional[str]:
        """
        Extract Python docstring (Both comments above and inner string literal).
        """
        from tree_sitter import Node
        if not isinstance(node, Node):
            return None

        doc_parts = []
        
        # 1. Check comments above (Using base class logic)
        # We need to call the base class static method explicitly
        base_doc = LanguageDefinition.extract_docstring(node, content_bytes)
        if base_doc:
            doc_parts.append(base_doc)

        # 2. Check inner string literal
        inner_doc = None
        block = node.child_by_field_name('body')
        if block:
            for child in block.children:
                if child.type == 'expression_statement':
                    if child.child_count > 0 and child.children[0].type == 'string':
                        string_node = child.children[0]
                        raw = string_node.text.decode('utf8')
                        if raw.startswith('"""') or raw.startswith("'''"):
                            inner_doc = raw[3:-3].strip()
                        elif raw.startswith('"') or raw.startswith("'"):
                            inner_doc = raw[1:-1].strip()
                        break
        
        if inner_doc:
            doc_parts.append(inner_doc)
            
        return "\n\n".join(doc_parts) if doc_parts else None

    @staticmethod
    def format_signature(params_text: Optional[str], return_text: Optional[str]) -> str:
        """
        Format Python signature.
        """
        sig = ""
        if params_text:
            sig = " ".join(params_text.split())
        if return_text:
            r_text = return_text.strip()
            # Python return types can start with ':' or be just the type
            sig += f" {r_text}" if r_text.startswith(':') else f" -> {r_text}"
        return sig
