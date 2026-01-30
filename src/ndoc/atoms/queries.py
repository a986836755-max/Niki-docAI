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

JAVASCRIPT_SCM = """
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

CSHARP_SCM = """
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
  name: (identifier) @name
  parameters: (parameter_list) @params
  type: (_)? @ret
) @func_def

(constructor_declaration
  name: (identifier) @name
  parameters: (parameter_list) @params
) @func_def
"""

TYPESCRIPT_SCM = """
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
  name: (_) @name
  parameters: (formal_parameters) @params
  return_type: (type_annotation)? @ret
) @func_def

(public_field_definition
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

GO_SCM = """
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

RUST_SCM = """
(struct_item
  name: (type_identifier) @name
) @struct_def

(trait_item
  name: (type_identifier) @name
) @class_def

(function_item
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type_identifier)? @ret
) @func_def
"""

DART_SCM = """
(class_definition name: (identifier) @name) @class_def
(mixin_declaration name: (identifier) @name) @struct_def
(enum_declaration name: (identifier) @name) @struct_def
(function_definition name: (identifier) @name) @func_def
"""

JAVA_SCM = """
(class_declaration
  name: (identifier) @name
) @class_def

(interface_declaration
  name: (identifier) @name
) @class_def

(enum_declaration
  name: (identifier) @name
) @class_def

(record_declaration
  name: (identifier) @name
) @class_def

(method_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
  type: [
    (type_identifier)
    (void_type)
    (generic_type)
  ]? @ret
) @func_def

(constructor_declaration
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(field_declaration
  type: (_) @field_type
  (variable_declarator
    name: (identifier) @field_name
    value: (_)? @field_value
  )
) @field_def
"""

# Map language keys to SCM
QUERY_MAP = {
    "python": PYTHON_SCM,
    "cpp": CPP_SCM,
    "javascript": JAVASCRIPT_SCM,
    "typescript": TYPESCRIPT_SCM,
    "go": GO_SCM,
    "rust": RUST_SCM,
    "dart": DART_SCM,
    "c_sharp": CSHARP_SCM,
    "java": JAVA_SCM
}
