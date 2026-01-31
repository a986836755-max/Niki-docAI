# Context: langs
> @CONTEXT: Local | langs | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-31 16:49:04

## !RULE
*   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `extract_docstring` 来合并这两者，确保语义提取的完整性。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Language Definition Protocol. @DEP: typing.List, typing.Type, typing.Any, pkgutil, typing, text_utils, pathlib.Path, importlib, typing.Dict, tree_sitter.Node, typing.Optional, tree_sitter, pathlib, text_utils.clean_docstring
    *   `@API`
        *   `PUB:` CLS **LanguageDefinition**
            *   `VAL->` VAR **ID**`: str = ""`
            *   `VAL->` VAR **EXTENSIONS**`: List[str] = []`
            *   `VAL->` VAR **SCM_QUERY**`: str = ""`
            *   `VAL->` VAR **CALL_QUERY**`: str = ""`
            *   `VAL->` VAR **SCM_IMPORTS**`: str = ""`
            *   `VAL->` VAR **CLASS_TYPES**`: List[str] = []`
            *   `VAL->` VAR **ASYNC_KEYWORDS**`: List[str] = ["async"]`
            *   `PUB:` STA **get_visibility**`(captures: Dict[str, Any], content_bytes: bytes) -> str`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
            *   `PUB:` CLM **is_async**`(cls, node_text: str) -> bool`
            *   `PUB:` STA **extract_docstring**`(node: Any, content_bytes: bytes) -> Optional[str]`
            *   `PUB:` STA **format_signature**`(params_text: Optional[str], return_text: Optional[str]) -> str`
        *   `VAL->` VAR _LANG_REGISTRY`: Dict[str, Type[LanguageDefinition]] = {}`
        *   `VAL->` VAR _EXT_TO_LANG`: Dict[str, str] = {}`
        *   `PUB:` FUN **register_language**`(lang_cls: Type[LanguageDefinition])`
        *   `PUB:` FUN **load_languages**`()`
        *   `PUB:` FUN **get_lang_def**`(lang_id: str) -> Optional[Type[LanguageDefinition]]`
        *   `PUB:` FUN **get_lang_id_by_ext**`(ext: str) -> Optional[str]`
        *   `PUB:` FUN **get_all_extensions**`() -> List[str]`
*   **[cpp.py](cpp.py#L1)**
    *   `@API`
        *   `PUB:` CLS **CppDefinition**
            *   `VAL->` VAR **ID**` = "cpp"`
            *   `VAL->` VAR **EXTENSIONS**` = [".cpp", ".c", ".h", ".hpp"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_specifier", "struct_specifier"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `VAL->` VAR **CALL_QUERY**` = """
(call_expression
  function: [
    (identifier) @call_name
    (field_expression) @call_name
    (scoped_identifier) @call_name
  ]
)
"""`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(preproc_include) @import
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[csharp.py](csharp.py#L1)**
    *   `@API`
        *   `PUB:` CLS **CSharpDefinition**
            *   `VAL->` VAR **ID**` = "c_sharp"`
            *   `VAL->` VAR **EXTENSIONS**` = [".cs"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `VAL->` VAR **CALL_QUERY**` = """
(invocation_expression
  function: [(identifier) (member_access_expression)] @call_name
)
(object_creation_expression
  type: [(identifier) (predefined_type)] @call_name
)
"""`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(using_directive) @import
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[dart.py](dart.py#L1)**
    *   `@API`
        *   `PUB:` CLS **DartDefinition**
            *   `VAL->` VAR **ID**` = "dart"`
            *   `VAL->` VAR **EXTENSIONS**` = [".dart"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition", "mixin_declaration", "enum_declaration"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_definition name: (identifier) @name) @class_def
(mixin_declaration name: (identifier) @name) @struct_def
(enum_declaration name: (identifier) @name) @struct_def
(function_definition name: (identifier) @name) @func_def
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[go.py](go.py#L1)**
    *   `@API`
        *   `PUB:` CLS **GoDefinition**
            *   `VAL->` VAR **ID**` = "go"`
            *   `VAL->` VAR **EXTENSIONS**` = [".go"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["type_declaration", "type_spec"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[java.py](java.py#L1)**
    *   `@API`
        *   `PUB:` CLS **JavaDefinition**
            *   `VAL->` VAR **ID**` = "java"`
            *   `VAL->` VAR **EXTENSIONS**` = [".java"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(interface_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(enum_declaration
  (modifiers)? @visibility
  name: (identifier) @name
) @class_def

(method_declaration
  (modifiers)? @visibility
  type: [
    (type_identifier)
    (void_type)
    (generic_type)
  ]? @ret
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(constructor_declaration
  (modifiers)? @visibility
  name: (identifier) @name
  parameters: (formal_parameters) @params
) @func_def

(field_declaration
  (modifiers)? @visibility
  type: (_) @field_type
  (variable_declarator
    name: (identifier) @field_name
    value: (_)? @field_value
  )
) @field_def
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[javascript.py](javascript.py#L1)**
    *   `@API`
        *   `PUB:` CLS **JavascriptDefinition**
            *   `VAL->` VAR **ID**` = "javascript"`
            *   `VAL->` VAR **EXTENSIONS**` = [".js", ".jsx"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[python.py](python.py#L1)** @DEP: typing.Any, typing, tree_sitter.Node, typing.Optional, tree_sitter
    *   `@API`
        *   `PUB:` CLS **PythonDefinition**
            *   `VAL->` VAR **ID**` = "python"`
            *   `VAL->` VAR **EXTENSIONS**` = [".py"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `VAL->` VAR **CALL_QUERY**` = """
(call
  function: [(identifier) (attribute)] @call_name
)
"""`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(import_statement) @import
(import_from_statement) @import
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
            *   `PUB:` STA **extract_docstring**`(node: Any, content_bytes: bytes) -> Optional[str]`
            *   `PUB:` STA **format_signature**`(params_text: Optional[str], return_text: Optional[str]) -> str`
*   **[rust.py](rust.py#L1)**
    *   `@API`
        *   `PUB:` CLS **RustDefinition**
            *   `VAL->` VAR **ID**` = "rust"`
            *   `VAL->` VAR **EXTENSIONS**` = [".rs"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["struct_item", "trait_item", "impl_item"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
(struct_item
  (visibility_modifier)? @visibility
  name: (type_identifier) @name
) @struct_def

(trait_item
  (visibility_modifier)? @visibility
  name: (type_identifier) @name
) @class_def

(function_item
  (visibility_modifier)? @visibility
  name: (identifier) @name
  parameters: (parameters) @params
  return_type: (type_identifier)? @ret
) @func_def
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[typescript.py](typescript.py#L1)**
    *   `@API`
        *   `PUB:` CLS **TypescriptDefinition**
            *   `VAL->` VAR **ID**` = "typescript"`
            *   `VAL->` VAR **EXTENSIONS**` = [".ts", ".tsx"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declaration"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
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
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
<!-- NIKI_AUTO_Context_END -->
