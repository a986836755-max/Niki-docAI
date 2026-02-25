# Context: langs
> @CONTEXT: Local | langs | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:53

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
*   **Python Dual Docstrings**: Python 模块应同时支持传统的 `#` 注释（位于定义上方）和 PEP 257 定义的内部字符串字面量（定义内部第一行）。`python.py` 已经增强了 `extract_docstring` 来合并这两者，确保语义提取的完整性。

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: pkgutil, typing, core.text_utils, pathlib, tree_sitter, importlib
    *   `@API`
        *   `PUB:` CLS **LanguageDefinition** [🔗30]
            *   `VAL->` VAR **ID**`: str = ""`
            *   `VAL->` VAR **EXTENSIONS**`: List[str] = []` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**`: str = ""` [🔗22]
            *   `VAL->` VAR **CALL_QUERY**`: str = ""` [🔗10]
            *   `VAL->` VAR **SCM_IMPORTS**`: str = ""` [🔗9]
            *   `VAL->` VAR **CLASS_TYPES**`: List[str] = []` [🔗21]
            *   `VAL->` VAR **ASYNC_KEYWORDS**`: List[str] = ["async"]` [🔗3]
            *   `PUB:` STA **get_visibility**`(captures: Dict[str, Any], content_bytes: bytes) -> str` [🔗3]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
            *   `PUB:` CLM **is_async**`(cls, node_text: str) -> bool` [🔗3]
            *   `PUB:` STA **extract_docstring**`(node: Any, content_bytes: bytes) -> Optional[str]` [🔗12]
            *   `PUB:` STA **format_signature**`(params_text: Optional[str], return_text: Optional[str]) -> str` [🔗6]
        *   `VAL->` VAR _LANG_REGISTRY`: Dict[str, Type[LanguageDefinition]] = {}` [🔗6]
        *   `VAL->` VAR _EXT_TO_LANG`: Dict[str, str] = {}` [🔗8]
        *   `PUB:` FUN **register_language**`(lang_cls: Type[LanguageDefinition])` [🔗3]
        *   `PUB:` FUN **load_languages**`()` [🔗5]
        *   `PUB:` FUN **get_lang_def**`(lang_id: str) -> Optional[Type[LanguageDefinition]]` [🔗10]
        *   `PUB:` FUN **get_lang_id_by_ext**`(ext: str) -> Optional[str]` [🔗6]
        *   `PUB:` FUN **get_all_extensions**`() -> List[str]` [🔗2]
*   **[cpp.py](cpp.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **CppDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "cpp"`
            *   `VAL->` VAR **EXTENSIONS**` = [".cpp", ".c", ".h", ".hpp"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_specifier", "struct_specifier"]` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_specifier
  name: (type_identifier) @name
) @clas...` [🔗22]
            *   `VAL->` VAR **CALL_QUERY**` = """
(call_expression
  function: [
    (identifier) @call_na...` [🔗10]
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(preproc_include) @import
"""` [🔗9]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[csharp.py](csharp.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **CSharpDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "c_sharp"`
            *   `VAL->` VAR **EXTENSIONS**` = [".cs"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "struct_declaration", "interface_decla...` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(namespace_declaration
  [(qualified_name) (identifier)]...` [🔗22]
            *   `VAL->` VAR **CALL_QUERY**` = """
(invocation_expression
  function: [(identifier) (member...` [🔗10]
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(using_directive) @import
"""` [🔗9]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[dart.py](dart.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **DartDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "dart"`
            *   `VAL->` VAR **EXTENSIONS**` = [".dart"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition", "mixin_declaration", "enum_declaration"...` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_definition name: (identifier) @name) @class_def
(...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[go.py](go.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **GoDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "go"`
            *   `VAL->` VAR **EXTENSIONS**` = [".go"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["type_declaration", "type_spec"]` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(type_declaration
  (type_spec
    name: (type_identifie...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[java.py](java.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **JavaDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "java"`
            *   `VAL->` VAR **EXTENSIONS**` = [".java"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declara...` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  (modifiers)? @visibility
  name: (i...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[javascript.py](javascript.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **JavascriptDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "javascript"`
            *   `VAL->` VAR **EXTENSIONS**` = [".js", ".jsx"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration"]` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  name: (identifier) @name
) @class_d...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[python.py](python.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: tree_sitter, typing, core.text_utils
    *   `@API`
        *   `PUB:` CLS **PythonDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "python"`
            *   `VAL->` VAR **EXTENSIONS**` = [".py"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_definition"]` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_definition
  name: (identifier) @name
  superclas...` [🔗22]
            *   `VAL->` VAR **CALL_QUERY**` = """
(call
  function: [(identifier) (attribute)] @call_name
...` [🔗10]
            *   `VAL->` VAR **SCM_IMPORTS**` = """
(import_statement) @import
(import_from_statement) @impo...` [🔗9]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
            *   `PUB:` STA **extract_docstring**`(node: Any, content_bytes: bytes) -> Optional[str]` [🔗12]
            *   `PUB:` STA **format_signature**`(params_text: Optional[str], return_text: Optional[str]) -> str` [🔗6]
*   **[rust.py](rust.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **RustDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "rust"`
            *   `VAL->` VAR **EXTENSIONS**` = [".rs"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["struct_item", "trait_item", "impl_item"]` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(struct_item
  (visibility_modifier)? @visibility
  name...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
*   **[typescript.py](typescript.py#L1)**: <NIKI_AUTO_HEADER_START>
    *   `@API`
        *   `PUB:` CLS **TypescriptDefinition** [🔗2]
            *   `VAL->` VAR **ID**` = "typescript"`
            *   `VAL->` VAR **EXTENSIONS**` = [".ts", ".tsx"]` [🔗21]
            *   `VAL->` VAR **CLASS_TYPES**` = ["class_declaration", "interface_declaration", "enum_declara...` [🔗21]
            *   `VAL->` VAR **SCM_QUERY**` = """
(class_declaration
  name: (type_identifier) @name
) @cl...` [🔗22]
            *   `PUB:` STA **is_public**`(name: str, visibility: str) -> bool` [🔗27]
<!-- NIKI_AUTO_Context_END -->
