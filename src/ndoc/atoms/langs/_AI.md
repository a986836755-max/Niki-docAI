# Context: langs
> @CONTEXT: Local | langs | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:54

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `extract_docstring` 来合并这两者，确保语义提取的完整性。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: text_utils, pkgutil, pathlib, typing, importlib, tree_sitter
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
) @clas...`
            *   `VAL->` VAR **CALL_QUERY**` = """
(call_expression
  function: [
    (identifier) @call_na...`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(preproc_include) @import
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[csharp.py](csharp.py#L1)**
    *   `@API`
        *   `PUB:` CLS **CSharpDefinition**
            *   `VAL->` VAR **ID**` = "c_sharp"`
            *   `VAL->` VAR **EXTENSIONS**` = [".cs"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "struct_declaration", "interface_decla...`
            *   `VAL->` VAR **SCM_QUERY**` = """
(namespace_declaration
  [(qualified_name) (identifier)]...`
            *   `VAL->` VAR **CALL_QUERY**` = """
(invocation_expression
  function: [(identifier) (member...`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(using_directive) @import
"""`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[dart.py](dart.py#L1)**
    *   `@API`
        *   `PUB:` CLS **DartDefinition**
            *   `VAL->` VAR **ID**` = "dart"`
            *   `VAL->` VAR **EXTENSIONS**` = [".dart"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition", "mixin_declaration", "enum_declaration"...`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_definition name: (identifier) @name) @class_def
(...`
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
    name: (type_identifie...`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[java.py](java.py#L1)**
    *   `@API`
        *   `PUB:` CLS **JavaDefinition**
            *   `VAL->` VAR **ID**` = "java"`
            *   `VAL->` VAR **EXTENSIONS**` = [".java"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declara...`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  (modifiers)? @visibility
  name: (i...`
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
) @class_d...`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[python.py](python.py#L1)** @DEP: tree_sitter, typing
    *   `@API`
        *   `PUB:` CLS **PythonDefinition**
            *   `VAL->` VAR **ID**` = "python"`
            *   `VAL->` VAR **EXTENSIONS**` = [".py"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition"]`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_definition
  name: (identifier) @name
  superclas...`
            *   `VAL->` VAR **CALL_QUERY**` = """
(call
  function: [(identifier) (attribute)] @call_name
...`
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(import_statement) @import
(import_from_statement) @impo...`
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
  name...`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
*   **[typescript.py](typescript.py#L1)**
    *   `@API`
        *   `PUB:` CLS **TypescriptDefinition**
            *   `VAL->` VAR **ID**` = "typescript"`
            *   `VAL->` VAR **EXTENSIONS**` = [".ts", ".tsx"]`
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declara...`
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  name: (type_identifier) @name
) @cl...`
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool`
<!-- NIKI_AUTO_Context_END -->
