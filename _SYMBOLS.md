# Symbol Index
> 最后更新 (Last Updated): 2026-01-31 16:47:56

## @OVERVIEW
*   **Total Public Symbols**: 341

## Root
*   **[debug_scanner.py](debug_scanner.py#L1)**
    *   FUN **test** `()` [🔗162]
*   **[debug_symbols.py](debug_symbols.py#L1)**
    *   VAR **file_path** ` = Path("src/ndoc/atoms/deps/stats.py")` [🔗146]
    *   VAR **content** ` = read_text(file_path)` [🔗375]
    *   VAR **tree** ` = parse_code(content, file_path)` [🔗174]
    *   VAR **symbols** ` = extract_symbols(tree, content.encode("utf-8"), file_path)` [🔗128]
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**
    *   FUN **test_func** `(a: int, b: str) -> bool` [🔗7]
    *   CLS **TestClass** [🔗7]
    *   VAR **field** `: int = 10` [🔗186]
    *   MET **test_method** `(self)` [🔗3]
*   **[test_python_fix.py](test_python_fix.py#L1)**
    *   FUN **test_python_parsing** `()` [🔗4]
*   **[test_regex.py](test_regex.py#L1)**
    *   VAR **TAG_REGEX** ` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)` [🔗14]
    *   VAR **text** ` = """
Inner docstring for test_func.
    @INTERNAL
"""` [🔗397]
    *   VAR **matches** ` = list(TAG_REGEX.finditer(text))` [🔗40]
    *   VAR **text2** ` = """
# @CORE
# This is a core function.
"""` [🔗7]
    *   VAR **matches2** ` = list(TAG_REGEX.finditer(text2))` [🔗5]

## src/ndoc
*   **[daemon.py](src/ndoc/daemon.py#L1)**
    *   CLS **DocChangeHandler** [🔗4]
    *   MET **on_any_event** `(self, event: FileSystemEvent)` [🔗3]
    *   MET **trigger_update** `(self)` [🔗4]
    *   MET **run_update** `(self)` [🔗4]
    *   FUN **start_watch_mode** `(config: ProjectConfig)` [🔗5]
*   **[entry.py](src/ndoc/entry.py#L1)**
    *   FUN **main** `()` [🔗85]

## src/ndoc/atoms
*   **[cache.py](src/ndoc/atoms/cache.py#L1)**
    *   CLS **FileCache** [🔗9]
    *   MET **load** `(self)` [🔗31]
    *   MET **save** `(self)` [🔗22]
    *   MET **get_file_hash** `(self, file_path: Path) -> str` [🔗5]
    *   MET **is_changed** `(self, file_path: Path) -> bool` [🔗4]
    *   MET **update** `(self, file_path: Path, result: Any)` [🔗53]
    *   MET **get** `(self, file_path: Path) -> Optional[Any]` [🔗155]
*   **[fs.py](src/ndoc/atoms/fs.py#L1)**
    *   CLS **FileFilter** [🔗14]
    *   VAR **ignore_patterns** `: Set[str] = field(default_factory=set)` [🔗58]
    *   VAR **allow_extensions** `: Set[str] = field(default_factory=set)` [🔗8]
    *   VAR **spec** `: Optional[pathspec.PathSpec] = None` [🔗14]
    *   PRP **has_extension_filter** `(self) -> bool` [🔗5]
    *   FUN **load_gitignore** `(root: Path) -> Optional[pathspec.PathSpec]` [🔗5]
    *   FUN **should_ignore** `(path: Path, filter_config: FileFilter, root: Path = None) -> bool` [🔗7]
    *   FUN **list_dir** `(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]` [🔗4]
    *   FUN **walk_files** `(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]` [🔗13]
    *   FUN **get_relative_path** `(path: Path, root: Path) -> str` [🔗6]
*   **[io.py](src/ndoc/atoms/io.py#L1)**
    *   FUN **set_dry_run** `(enabled: bool) -> None` [🔗4]
    *   FUN **safe_io** `(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any` [🔗8]
    *   FUN **read_text** `(path: Path) -> Optional[str]` [🔗38]
    *   FUN **read_head** `(path: Path, n_bytes: int = 2048) -> Optional[str]` [🔗5]
    *   FUN **write_text** `(path: Path, content: str) -> bool` [🔗23]
    *   FUN **read_lines** `(path: Path) -> List[str]` [🔗3]
    *   FUN **append_text** `(path: Path, content: str) -> bool` [🔗4]
    *   FUN **update_section** `(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool` [🔗7]
    *   FUN **update_header_timestamp** `(path: Path) -> bool` [🔗9]
    *   FUN **delete_file** `(path: Path) -> bool` [🔗5]
*   **[llm.py](src/ndoc/atoms/llm.py#L1)**
    *   FUN **call_llm** `(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]` [🔗5]
*   **[lsp.py](src/ndoc/atoms/lsp.py#L1)**
    *   CLS **LSPService** [🔗10]
    *   MET **index_project** `(self, files: List[Path])` [🔗5]
    *   MET **find_definitions** `(self, name: str) -> List[Symbol]` [🔗4]
    *   MET **get_reference_count** `(self, name: str) -> int` [🔗4]
    *   MET **find_references** `(self, name: str) -> List[Dict[str, Any]]` [🔗4]
    *   FUN **get_service** `(root: Path) -> LSPService` [🔗5]
*   **[scanner.py](src/ndoc/atoms/scanner.py#L1)**
    *   CLS **TokenRule** [🔗4]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **pattern** `: Pattern` [🔗52]
    *   VAR **group_map** `: Dict[str, int]` [🔗4]
    *   CLS **ScanResult** [🔗14]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗54]
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)` [🔗60]
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)` [🔗128]
    *   VAR **docstring** `: str = ""` [🔗70]
    *   VAR **summary** `: str = ""` [🔗77]
    *   VAR **todos** `: List[dict] = field(default_factory=list)` [🔗69]
    *   VAR **calls** `: List[str] = field(default_factory=list)` [🔗57]
    *   VAR **imports** `: List[str] = field(default_factory=list)` [🔗41]
    *   VAR **is_core** `: bool = False` [🔗24]
    *   FUN **get_cache** `(root: Path) -> cache.FileCache` [🔗4]
    *   FUN **scan_file** `(file_path: Path, root: Path, force: bool = False) -> ScanResult` [🔗11]
    *   FUN **extract_todos** `(content: str) -> List[dict]` [🔗4]
    *   FUN **extract_docstring** `(content: str) -> str` [🔗14]
    *   VAR **SECTION_REGEX** ` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->", re.DOTALL
)` [🔗4]
    *   VAR **DOCSTRING_PATTERNS** ` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.compile(r"^\s*'''(.*?)'''", re.DOTALL),
]` [🔗4]
    *   FUN **parse_tags** `(content: str) -> List[Tag]` [🔗5]
    *   FUN **parse_sections** `(content: str) -> Dict[str, Section]` [🔗4]
    *   FUN **extract_summary** `(content: str, docstring: str) -> str` [🔗5]
    *   FUN **regex_scan** `(content: str, ext: str) -> List[Symbol]` [🔗4]
    *   FUN **scan_file_content** `(content: str, file_path: Optional[Path] = None) -> ScanResult` [🔗8]
*   **[text_utils.py](src/ndoc/atoms/text_utils.py#L1)**
    *   VAR **TAG_REGEX** ` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)` [🔗14]
    *   FUN **clean_docstring** `(raw: str) -> str` [🔗8]
    *   FUN **extract_tags_from_text** `(text: str, line_offset: int = 0) -> List[Tag]` [🔗7]

## src/ndoc/atoms/ast
*   **[base.py](src/ndoc/atoms/ast/base.py#L1)**
    *   VAR **tspython** ` = None` [🔗6]
    *   VAR **tscpp** ` = None` [🔗6]
    *   VAR **tsjs** ` = None` [🔗6]
    *   VAR **tsts** ` = None` [🔗6]
    *   VAR **tsgo** ` = None` [🔗6]
    *   VAR **tsrust** ` = None` [🔗6]
    *   VAR **tsdart** ` = None` [🔗6]
    *   VAR **tscsharp** ` = None` [🔗6]
    *   VAR **tsjava** ` = None` [🔗6]
    *   FUN **get_language** `(lang_key: str) -> Optional[Language]` [🔗13]
    *   CLS **AstNode** [🔗16]
    *   VAR **type** `: str` [🔗1000]
    *   VAR **text** `: str` [🔗397]
    *   VAR **start_point** `: tuple[int, int]` [🔗9]
    *   VAR **end_point** `: tuple[int, int]` [🔗7]
    *   VAR **children** `: list['AstNode'] = field(default_factory=list)` [🔗71]
    *   PRP **start_line** `(self) -> int` [🔗3]
    *   PRP **end_line** `(self) -> int` [🔗3]
    *   FUN **get_parser** `(lang_key: str = 'python') -> Optional[Parser]` [🔗7]
    *   FUN **parse_code** `(content: str, file_path: Optional[Path] = None) -> Optional[Tree]` [🔗17]
    *   FUN **get_lang_key** `(file_path: Path) -> Optional[str]` [🔗9]
    *   FUN **query_tree** `(tree: Tree, query_scm: str, lang_key: str = 'python') -> list[dict]` [🔗10]
*   **[discovery.py](src/ndoc/atoms/ast/discovery.py#L1)**
    *   FUN **find_calls** `(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗8]
    *   FUN **find_imports** `(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗8]
*   **[symbols.py](src/ndoc/atoms/ast/symbols.py#L1)**
    *   FUN **extract_symbols** `(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]` [🔗19]
*   **[utils.py](src/ndoc/atoms/ast/utils.py#L1)**
    *   VAR **MAX_VALUE_LENGTH** ` = 60` [🔗11]
    *   VAR **MAX_CONTENT_LENGTH** ` = 200` [🔗8]
    *   FUN **truncate** `(text: str, max_len: int = 100) -> str` [🔗11]
    *   FUN **node_to_data** `(node: Node, include_children: bool = False) -> AstNode` [🔗7]

## src/ndoc/atoms/deps
*   **[core.py](src/ndoc/atoms/deps/core.py#L1)**
    *   VAR **SOURCE_PARSERS** ` = {
    '.py': extract_imports,
    '.dart': extract_dart_imports,
    '.cpp': extract_cpp_includes,
    '.h': extract_cpp_includes,
    '.hpp': extract_cpp_includes,
    '.c': extract_cpp_includes,
    '.cc': extract_cpp_includes,
    '.cs': extract_csharp_usings,
}` [🔗10]
    *   FUN **extract_dependencies** `(content: str, file_path: Path) -> List[str]` [🔗7]
    *   FUN **get_project_dependencies** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]` [🔗7]
*   **[manifests.py](src/ndoc/atoms/deps/manifests.py#L1)**
    *   FUN **parse_requirements_txt** `(file_path: Path) -> List[str]` [🔗8]
    *   FUN **parse_pyproject_toml** `(file_path: Path) -> List[str]` [🔗8]
    *   FUN **parse_package_json** `(file_path: Path) -> List[str]` [🔗8]
    *   FUN **parse_pubspec_yaml** `(file_path: Path) -> List[str]` [🔗8]
    *   FUN **parse_cmake_lists** `(file_path: Path) -> List[str]` [🔗8]
    *   FUN **parse_csproj** `(file_path: Path) -> List[str]` [🔗8]
*   **[parsers.py](src/ndoc/atoms/deps/parsers.py#L1)**
    *   FUN **extract_imports** `(content: str) -> List[str]` [🔗11]
    *   FUN **extract_cpp_includes** `(content: str) -> List[str]` [🔗22]
    *   FUN **extract_dart_imports** `(content: str) -> List[str]` [🔗10]
    *   FUN **extract_csharp_usings** `(content: str) -> List[str]` [🔗10]
*   **[stats.py](src/ndoc/atoms/deps/stats.py#L1)**
    *   VAR **DEFAULT_IGNORE_PATTERNS** ` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env', '.env', 
    'dist', 'build', 'target', 'out', 
    '.dart_tool', '.pub-cache', 
    'coverage', 'tmp', 'temp'
}` [🔗9]
    *   VAR **LANGUAGE_EXTENSIONS** ` = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React',
    '.tsx': 'React TS',
    '.html': 'HTML',
    '.css': 'CSS',
    '.scss': 'Sass',
    '.md': 'Markdown',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.sh': 'Shell',
    '.bat': 'Batch',
    '.ps1': 'PowerShell',
    '.rs': 'Rust',
    '.go': 'Go',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++ Header',
    '.dart': 'Dart',
    '.cmake': 'CMake',
    '.cs': 'C#',
    '.csproj': 'C# Project',
}` [🔗9]
    *   FUN **detect_languages** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]` [🔗7]

## src/ndoc/atoms/langs
*   **[__init__.py](src/ndoc/atoms/langs/__init__.py#L1)**
    *   CLS **LanguageDefinition** [🔗33]
    *   VAR **ID** `: str = ""` [🔗561]
    *   VAR **EXTENSIONS** `: List[str] = []` [🔗31]
    *   VAR **SCM_QUERY** `: str = ""` [🔗32]
    *   VAR **CALL_QUERY** `: str = ""` [🔗13]
    *   VAR **SCM_IMPORTS** `: str = ""` [🔗13]
    *   VAR **CLASS_TYPES** `: List[str] = []` [🔗31]
    *   VAR **ASYNC_KEYWORDS** `: List[str] = ["async"]` [🔗4]
    *   STA **get_visibility** `(captures: Dict[str, Any], content_bytes: bytes) -> str` [🔗4]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
    *   CLM **is_async** `(cls, node_text: str) -> bool` [🔗4]
    *   STA **extract_docstring** `(node: Any, content_bytes: bytes) -> Optional[str]` [🔗14]
    *   STA **format_signature** `(params_text: Optional[str], return_text: Optional[str]) -> str` [🔗8]
    *   FUN **register_language** `(lang_cls: Type[LanguageDefinition])` [🔗4]
    *   FUN **load_languages** `()` [🔗6]
    *   FUN **get_lang_def** `(lang_id: str) -> Optional[Type[LanguageDefinition]]` [🔗9]
    *   FUN **get_lang_id_by_ext** `(ext: str) -> Optional[str]` [🔗5]
    *   FUN **get_all_extensions** `() -> List[str]` [🔗3]
*   **[cpp.py](src/ndoc/atoms/langs/cpp.py#L1)**
    *   CLS **CppDefinition** [🔗3]
    *   VAR **ID** ` = "cpp"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".cpp", ".c", ".h", ".hpp"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_specifier", "struct_specifier"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(call_expression
  function: [
    (identifier) @call_name
    (field_expression) @call_name
    (scoped_identifier) @call_name
  ]
)
"""` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(preproc_include) @import
"""` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[csharp.py](src/ndoc/atoms/langs/csharp.py#L1)**
    *   CLS **CSharpDefinition** [🔗3]
    *   VAR **ID** ` = "c_sharp"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".cs"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(invocation_expression
  function: [(identifier) (member_access_expression)] @call_name
)
(object_creation_expression
  type: [(identifier) (predefined_type)] @call_name
)
"""` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(using_directive) @import
"""` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[dart.py](src/ndoc/atoms/langs/dart.py#L1)**
    *   CLS **DartDefinition** [🔗3]
    *   VAR **ID** ` = "dart"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".dart"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_definition", "mixin_declaration", "enum_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_definition name: (identifier) @name) @class_def
(mixin_declaration name: (identifier) @name) @struct_def
(enum_declaration name: (identifier) @name) @struct_def
(function_definition name: (identifier) @name) @func_def
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[go.py](src/ndoc/atoms/langs/go.py#L1)**
    *   CLS **GoDefinition** [🔗3]
    *   VAR **ID** ` = "go"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".go"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["type_declaration", "type_spec"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[java.py](src/ndoc/atoms/langs/java.py#L1)**
    *   CLS **JavaDefinition** [🔗3]
    *   VAR **ID** ` = "java"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".java"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[javascript.py](src/ndoc/atoms/langs/javascript.py#L1)**
    *   CLS **JavascriptDefinition** [🔗3]
    *   VAR **ID** ` = "javascript"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".js", ".jsx"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[python.py](src/ndoc/atoms/langs/python.py#L1)**
    *   CLS **PythonDefinition** [🔗3]
    *   VAR **ID** ` = "python"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".py"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_definition"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(call
  function: [(identifier) (attribute)] @call_name
)
"""` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(import_statement) @import
(import_from_statement) @import
"""` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
    *   STA **extract_docstring** `(node: Any, content_bytes: bytes) -> Optional[str]` [🔗14]
    *   STA **format_signature** `(params_text: Optional[str], return_text: Optional[str]) -> str` [🔗8]
*   **[rust.py](src/ndoc/atoms/langs/rust.py#L1)**
    *   CLS **RustDefinition** [🔗3]
    *   VAR **ID** ` = "rust"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".rs"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["struct_item", "trait_item", "impl_item"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[typescript.py](src/ndoc/atoms/langs/typescript.py#L1)**
    *   CLS **TypescriptDefinition** [🔗3]
    *   VAR **ID** ` = "typescript"` [🔗561]
    *   VAR **EXTENSIONS** ` = [".ts", ".tsx"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
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
"""` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]

## src/ndoc/flows
*   **[archive_flow.py](src/ndoc/flows/archive_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[clean_flow.py](src/ndoc/flows/clean_flow.py#L1)**
    *   VAR **GENERATED_FILES** ` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md",
    "_NEXT.md",
    "_SYMBOLS.md",
    "_DATA.md",
    "_STATS.md",
    "_SYNTAX.md",
    # _ARCH.md is typically manual or hybrid, avoiding delete for safety unless confirmed
]` [🔗5]
    *   FUN **run** `(config: ProjectConfig, target: str = None, force: bool = False) -> bool` [🔗141]
*   **[config_flow.py](src/ndoc/flows/config_flow.py#L1)**
    *   VAR **RULES_TEMPLATE** ` = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFIG @RULES

## Scanning Rules (扫描规则)
> 定义哪些文件应该被忽略或包含。

- `!IGNORE`: .git, .vscode, .idea, __pycache__, node_modules, dist, build, .venv, venv
- `!INCLUDE`: .py, .md, .json, .js, .ts, .html, .css, .yml, .yaml, .toml

## Documentation Style (文档风格)
> 定义生成的文档样式。

- `!LANG`: Chinese (zh-CN)

## ALM & Memory Rules (ALM与记忆规则)
> 定义项目生命周期与自动归档规则。

- `MEMORY文档对齐`: 定期更新_MEMORY.md，每当_NEXT.md中一项功能/模块完成，将其归档入_MEMORY.md。
- `交付即更新`: 在完成代码修改后，习惯性运行 `ndoc all`，确保改动被即时索引。

## Special Keywords (特殊关键字)
> 用于控制特定目录的文档生成行为。

- `@AGGREGATE`: **Recursive Aggregation**. 当目录包含此标记时，不为子目录生成单独的 `_AI.md`，而是将其内容递归聚合到父级 `_AI.md` 中。
- `@CHECK_IGNORE`: **Audit Ignore**. 当目录包含此标记时，完全跳过该目录及其子目录的 `_AI.md` 生成。
"""` [🔗4]
    *   FUN **load_project_config** `(root_path: Path) -> ProjectConfig` [🔗4]
    *   FUN **ensure_rules_file** `(root_path: Path, force: bool = False) -> bool` [🔗5]
*   **[context_flow.py](src/ndoc/flows/context_flow.py#L1)**
    *   FUN **format_file_summary** `(ctx: FileContext, root: Optional[Path] = None) -> str` [🔗4]
    *   FUN **format_symbol_list** `(ctx: FileContext) -> str` [🔗4]
    *   FUN **format_dependencies** `(ctx: FileContext) -> str` [🔗4]
    *   FUN **generate_dir_content** `(context: DirectoryContext) -> str` [🔗4]
    *   FUN **cleanup_legacy_map** `(file_path: Path) -> None` [🔗4]
    *   FUN **process_directory** `(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False) -> Optional[DirectoryContext]` [🔗6]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
    *   FUN **update_directory** `(path: Path, config: ProjectConfig) -> bool` [🔗4]
*   **[data_flow.py](src/ndoc/flows/data_flow.py#L1)**
    *   CLS **DataDefinition** [🔗6]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **type** `: str` [🔗1000]
    *   VAR **path** `: str` [🔗416]
    *   VAR **docstring** `: str` [🔗70]
    *   VAR **fields** `: List[str]` [🔗34]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
    *   FUN **get_plural** `(name: str) -> str` [🔗4]
*   **[deps_flow.py](src/ndoc/flows/deps_flow.py#L1)**
    *   FUN **collect_imports** `(root: Path) -> Dict[str, List[str]]` [🔗4]
    *   FUN **build_dependency_graph** `(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]` [🔗4]
    *   FUN **generate_mermaid_graph** `(graph: Dict[str, Set[str]]) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[doctor_flow.py](src/ndoc/flows/doctor_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[init_flow.py](src/ndoc/flows/init_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗141]
*   **[map_flow.py](src/ndoc/flows/map_flow.py#L1)**
    *   CLS **MapContext** [🔗8]
    *   VAR **root** `: Path` [🔗247]
    *   VAR **ignore_patterns** `: List[str]` [🔗58]
    *   FUN **format_dir_entry** `(name: str, level: int) -> str` [🔗4]
    *   FUN **format_file_entry** `(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str` [🔗4]
    *   FUN **extract_file_summary** `(path: Path) -> str` [🔗4]
    *   FUN **build_tree_lines** `(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]` [🔗5]
    *   FUN **generate_tree_content** `(config: ProjectConfig) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[plan_flow.py](src/ndoc/flows/plan_flow.py#L1)**
    *   VAR **PLAN_SYSTEM_PROMPT** ` = """
You are a senior software architect and project manager. 
Your task is to take a high-level "Objective" and break it down into actionable tasks for a developer.
These tasks will be added to the project's `_NEXT.md` roadmap.

Rules:
1. Keep tasks specific and actionable.
2. Group tasks logically into a new section.
3. Use Markdown format with checkboxes: * [ ] #task-id: description.
4. Each task MUST have a unique `#task-id` (e.g., #refactor-auth, #ui-login).
5. Output ONLY the new section content in Markdown, starting with a level 3 header `###`.

Current context:
You are working on Niki-docAI, a tool that generates documentation context for AI assistants.
"""` [🔗4]
    *   FUN **run** `(config: ProjectConfig, objective: str) -> bool` [🔗141]
*   **[stats_flow.py](src/ndoc/flows/stats_flow.py#L1)**
    *   FUN **check_should_update** `(root_path: Path, force: bool) -> bool` [🔗4]
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗141]
*   **[symbols_flow.py](src/ndoc/flows/symbols_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[syntax_flow.py](src/ndoc/flows/syntax_flow.py#L1)**
    *   VAR **SYNTAX_TEMPLATE** ` = r"""# PROJECT SYNTAX
> @CONTEXT: DSL 定义 | @TAGS: @SYNTAX @OP

<!-- NIKI_VERSION: 2.0.0 -->

## @MOD
| Mod | Meaning | Concept |
| :--- | :--- | :--- |
| `PUB:` | **Public**: 公开接口 (Exported API) | Scope: Global |
| `PRV:` | **Private**: 私有实现 (Internal Impl) | Scope: Local |
| `GET->`| **Getter**: 读取/属性 (Property) | Flow: Output |

## @KIND
| Kind | Meaning | Context |
| :--- | :--- | :--- |
| `CLS` | **Class**: 类定义 | Object/Type |
| `STC` | **Struct**: 结构体/数据 | Data/Schema |
| `FUN` | **Function**: 函数/方法 | Action/Logic |
| `VAR` | **Variable**: 变量/属性 | State/Data |
| `MOD` | **Module**: 模块/文件 | Container |

## @OP
| Op | Meaning |
| :--- | :--- |
| `->` | **Flow**: 流向 (Logic -> Comp) |
| `<-` | **Read**: 读取 (Sys <- Comp) |
| `=>` | **Map**: 映射 (ID => Sprite) |
| `>>` | **Move**: 移动/转移 (Ptr >> Sys) |
| `?` | **Check**: 检查 (Dirty?) |
| `!` | **Ban**: 禁止 (!Draw) |

## @TAGS
> 全局标签定义。AI 必须遵循这些语义。

### Structural (结构类)
- `@DOMAIN`: **Scope**. 边界/领域 (Boundary/Domain).
- `@MODULE`: **Module**. 独立单元 (Independent unit).
- `@API`: **Public**. 公共接口 (Public Interface).
- `@AGGREGATE`: **Recursive**. 包含子目录 (Include subdirs).
- `@ARCH`: **Architecture**. 文件列表/图谱 (File list/Graph).
- `@MAP`: **Navigation**. 链接/结构 (Links/Structure).
- `@TREE`: **Directory Tree**. 项目层级 (Project hierarchy).
- `@GRAPH`: **Dependency Graph**. 可视化关系 (Visual relationships).
- `@INDEX`: **Index**. 交叉引用 (Cross-reference).

### Constraint (约束类)
- `!RULE`: **Constraint**. 强制规则 (Mandatory rule).
- `!CONST`: **Invariant**. 不可变事实 (Immutable fact).

### Semantic (语义类)
- `@OVERVIEW`: **Summary**. 核心职责/存在意义 (Core responsibility).
- `@VISION`: **Vision**. 长期目标 (Long-term goal).
- `@USAGE`: **Usage**. 示例/用法 (Examples/How-to).
- `@FLOW`: **Process**. 时序/数据流 (Sequence/Data flow).
- `@STATE`: **State**. 状态机/变量 (State machine/Variables).
- `@EVENT`: **Event**. 发射/处理的事件 (Emitted/Handled events).
- `@DEF`: **Term**. 定义/概念 (Definition/Concept).
- `@TERM`: **Glossary**. 术语定义 (Term definition).
- `@TECH`: **Technology**. 技术栈信息 (Stack info).
- `@STACK`: **Stack**. 依赖/版本 (Dependencies/Versions).
- `@ANALYSIS`: **Analysis**. 洞察/指标 (Insights/Metrics).

### Evolutionary (演进类)
- `!TODO`: **Debt**. 已知问题 (Known issue).
- `@PLAN`: **Roadmap**. 未来计划 (Future plan).
- `@BACKLOG`: **Backlog**. 待办事项 (Future tasks).
- `@MEMORY`: **ADR**. 决策记录 (Decision record).
- `@ADR`: **Decision**. 决策记录 (Record of decisions).
- `@DEPRECATED`: **No**. 请勿使用 (Do not use).
- `@EXPERIMENTAL`: **WIP**. 不稳定 (Unstable).
- `@LEGACY`: **Legacy**. 旧代码 (Old code).

### Meta (元数据类)
- `@META`: **Metadata**. 文件属性 (File attributes).
- `@CONFIG`: **Configuration**. 设置/规则 (Settings/Rules).
- `@CHECK_IGNORE`: **Audit Ignore**. 审计忽略 (Audit Ignore).
- `@CONTEXT`: **Context**. 范围定义 (Scope definition).
- `@TAGS`: **Tag Def**. 标签字典 (Tag dictionary).
- `@SYNTAX`: **Syntax**. DSL 规则 (DSL rules).
- `@OP`: **Operator**. DSL 操作符 (DSL operators).
- `@TOOL`: **Tooling**. CLI 指令 (CLI instructions).

### Live Markers (自动仪表盘)
- `<!-- NIKI_AUTO_DOC_START -->`: **Generic**. 自动生成块开始 (Start of auto-gen block).
- `<!-- NIKI_AUTO_DOC_END -->`: **Generic**. 自动生成块结束 (End of auto-gen block).
- `<!-- NIKI_TODO_START -->`: **Todo**. 任务聚合开始 (Start of task aggregation).
- `<!-- NIKI_CTX_START -->`: **Context**. 实时上下文开始 (Start of live context).
- `<!-- NIKI_MAP_START -->`: **Map**. 文件树开始 (Start of file tree).

### @DISCOVERED
> 从文件头自动发现的标签。
- `@UNKNOWN`: **Unknown**. 占位符 (Placeholder).
- `@TODO`: **Unreviewed**. 发现于 [_NEXT.md] (Found in ...).
"""` [🔗4]
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗141]
*   **[tech_flow.py](src/ndoc/flows/tech_flow.py#L1)**
    *   FUN **generate_tech_content** `(config: ProjectConfig) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[todo_flow.py](src/ndoc/flows/todo_flow.py#L1)**
    *   CLS **TodoItem** [🔗14]
    *   VAR **file_path** `: Path` [🔗146]
    *   VAR **line** `: int` [🔗326]
    *   VAR **type** `: str` [🔗1000]
    *   VAR **content** `: str` [🔗375]
    *   VAR **task_id** `: Optional[str] = None` [🔗19]
    *   PRP **priority_icon** `(self) -> str` [🔗4]
    *   FUN **collect_todos** `(root: Path, ignore_patterns: List[str]) -> List[TodoItem]` [🔗4]
    *   FUN **format_todo_lines** `(todos: List[TodoItem], root: Path) -> str` [🔗4]
    *   FUN **sync_tasks** `(config: ProjectConfig, todos: List[TodoItem]) -> bool` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]
*   **[update_flow.py](src/ndoc/flows/update_flow.py#L1)**
    *   FUN **run** `() -> bool` [🔗141]
*   **[verify_flow.py](src/ndoc/flows/verify_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗141]

## src/ndoc/models
*   **[config.py](src/ndoc/models/config.py#L1)**
    *   CLS **ScanConfig** [🔗13]
    *   VAR **root_path** `: Path` [🔗93]
    *   VAR **ignore_patterns** `: List[str] = field(default_factory=lambda: [
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "ndoc_legacy" # Explicitly ignore legacy
    ])` [🔗58]
    *   VAR **extensions** `: List[str] = field(default_factory=list)` [🔗69]
    *   CLS **ProjectConfig** [🔗103]
    *   VAR **scan** `: ScanConfig` [🔗70]
    *   VAR **name** `: str = "Project"` [🔗1545]
    *   VAR **version** `: str = "0.1.0"` [🔗187]
*   **[context.py](src/ndoc/models/context.py#L1)**
    *   CLS **Tag** [🔗43]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **args** `: List[str] = field(default_factory=list)` [🔗98]
    *   VAR **line** `: int = 0` [🔗326]
    *   VAR **raw** `: str = ""` [🔗36]
    *   CLS **Section** [🔗24]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **content** `: str` [🔗375]
    *   VAR **raw** `: str` [🔗36]
    *   VAR **start_pos** `: int` [🔗5]
    *   VAR **end_pos** `: int` [🔗5]
    *   CLS **Symbol** [🔗76]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **kind** `: str` [🔗141]
    *   VAR **line** `: int` [🔗326]
    *   VAR **docstring** `: Optional[str] = None` [🔗70]
    *   VAR **signature** `: Optional[str] = None` [🔗37]
    *   VAR **parent** `: Optional[str] = None` [🔗182]
    *   VAR **is_core** `: bool = False` [🔗24]
    *   VAR **visibility** `: str = "public"` [🔗156]
    *   VAR **lang** `: str = "unknown"` [🔗43]
    *   VAR **decorators** `: List[str] = field(default_factory=list)` [🔗10]
    *   VAR **bases** `: List[str] = field(default_factory=list)` [🔗20]
    *   VAR **full_content** `: str = ""` [🔗6]
    *   VAR **path** `: Optional[str] = None` [🔗416]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗54]
    *   PRP **is_public** `(self) -> bool` [🔗38]
    *   CLS **FileContext** [🔗21]
    *   VAR **path** `: Path` [🔗416]
    *   VAR **rel_path** `: str` [🔗32]
    *   VAR **content** `: Optional[str] = None` [🔗375]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗54]
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)` [🔗60]
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)` [🔗128]
    *   VAR **docstring** `: Optional[str] = None` [🔗70]
    *   VAR **is_core** `: bool = False` [🔗24]
    *   VAR **ast_tree** `: Any = None` [🔗4]
    *   VAR **title** `: Optional[str] = None` [🔗311]
    *   VAR **description** `: Optional[str] = None` [🔗52]
    *   PRP **has_content** `(self) -> bool` [🔗7]
    *   CLS **DirectoryContext** [🔗12]
    *   VAR **path** `: Path` [🔗416]
    *   VAR **files** `: List[FileContext] = field(default_factory=list)` [🔗293]
    *   VAR **subdirs** `: List[Path] = field(default_factory=list)` [🔗20]
    *   PRP **name** `(self) -> str` [🔗1545]

## tests
*   **[conftest.py](tests/conftest.py#L1)**
    *   VAR **root** ` = Path(__file__).parent.parent` [🔗247]
*   **[test_ast.py](tests/test_ast.py#L1)**
    *   VAR **SAMPLE_CODE** ` = """
class MyClass:
    '''Class Docstring'''
    
    def method_one(self, a, b):
        '''Method One Doc'''
        return a + b
        
    @property
    def prop_one(self):
        '''Property One Doc'''
        return 1
        
    @classmethod
    def class_method(cls):
        '''Class Method Doc'''
        pass
        
    @staticmethod
    def static_method():
        pass

def global_func(x: int) -> int:
    '''Global Func Doc'''
    return x * 2
"""` [🔗5]
    *   FUN **test_extract_symbols_basic** `()` [🔗3]
    *   FUN **test_extract_complex_api** `()` [🔗3]
    *   FUN **find_sym** `(name)` [🔗7]
    *   FUN **find_member** `(cls_name, name)` [🔗6]
*   **[test_csharp_api.py](tests/test_csharp_api.py#L1)**
    *   FUN **test_csharp_extraction** `()` [🔗4]
*   **[test_scanner.py](tests/test_scanner.py#L1)**
    *   VAR **SAMPLE_CONTENT** ` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<!-- NIKI_TEST_END -->

class TestClass:
    '''Doc'''
    pass
"""` [🔗4]
    *   FUN **test_scan_file_content_mixed** `()` [🔗3]
    *   FUN **test_scan_file_content_text_only** `()` [🔗3]

## tests/fixtures
*   **[complex_api.py](tests/fixtures/complex_api.py#L1)**
    *   CLS **User** [🔗17]
    *   VAR **name** `: str` [🔗1545]
    *   VAR **age** `: int = 18` [🔗6]
    *   PRP **is_adult** `(self) -> bool` [🔗3]
    *   ASY **fetch_data** `(self) -> dict` [🔗4]
    *   CLM **from_dict** `(cls, data: dict) -> "User"` [🔗7]
    *   CLS **Database** [🔗6]
    *   VAR **connection_string** `: str = "localhost:5432"` [🔗3]
    *   MET **connect** `(self)` [🔗11]
    *   FUN **global_func** `(x: int, y: int) -> int` [🔗7]
    *   ASY **global_async_func** `()` [🔗4]
