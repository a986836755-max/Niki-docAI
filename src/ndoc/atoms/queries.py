# Language SCM Queries for Tree-sitter

PYTHON_SCM = """
(class_definition
  name: (identifier) @name
) @class_def

(function_definition
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type)? @ret
) @func_def

(decorated_definition
  (decorator) @deco
  (function_definition
    name: (identifier) @name
    parameters: (parameters) @params
    return_type: (type)? @ret
  ) @func_def
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
(class_definition
    body: (block
        (expression_statement
            (annotated_assignment
                left: (identifier) @field_name
                type: (type) @field_type
                value: (_)? @field_value
            ) @field_def
        )
    )
)
"""

CPP_SCM = """
(class_specifier
  name: (type_identifier) @name
) @class_def

(struct_specifier
  name: (type_identifier) @name
) @class_def

(function_definition
  declarator: (function_declarator
    declarator: (identifier) @name
    parameters: (parameter_list) @params
  )
  type: (_)? @ret
) @func_def

(function_definition
  declarator: (function_declarator
    declarator: (field_identifier) @name
    parameters: (parameter_list) @params
  )
  type: (_)? @ret
) @func_def
"""

JAVASCRIPT_SCM = """
(class_declaration
  name: (identifier) @name
) @class_def

(function_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(method_definition
  name: (property_identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(variable_declarator
  name: (identifier) @name
  value: [(arrow_function) (function)]
) @func_def
"""

TYPESCRIPT_SCM = """
(class_declaration
  name: (type_identifier) @name
) @class_def

(interface_declaration
  name: (type_identifier) @name
) @class_def

(function_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
  return_type: (type_annotation)? @ret
) @func_def

(method_definition
  name: (property_identifier) @name
  parameters: (formal_parameters) @params
  return_type: (type_annotation)? @ret
) @func_def
"""

GO_SCM = """
(type_declaration
  (type_spec
    name: (type_identifier) @name
    type: (struct_type)
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

RUST_SCM = """
(struct_item
  name: (type_identifier) @name
) @class_def

(trait_item
  name: (type_identifier) @name
) @class_def

(function_item
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type_identifier)? @ret
) @func_def
"""

# Map language keys to SCM
QUERY_MAP = {
    "python": PYTHON_SCM,
    "cpp": CPP_SCM,
    "javascript": JAVASCRIPT_SCM,
    "typescript": TYPESCRIPT_SCM,
    "go": GO_SCM,
    "rust": RUST_SCM
}
