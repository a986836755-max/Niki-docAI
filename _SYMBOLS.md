# Symbol Index
> 最后更新 (Last Updated): 2026-01-30 23:27:47

## @OVERVIEW
*   **Total Public Symbols**: 589

## Root
*   **[test_python_fix.py](test_python_fix.py#L1)**
    *   FUN **test_python_parsing** `()`

## src/ndoc
*   **[daemon.py](src/ndoc/daemon.py#L1)**
    *   CLS **DocChangeHandler**
    *   MET **on_any_event** `(self, event: FileSystemEvent)`
    *   MET **trigger_update** `(self)`
    *   MET **run_update** `(self)`
    *   FUN **start_watch_mode** `(config: ProjectConfig)`
*   **[entry.py](src/ndoc/entry.py#L1)**
    *   FUN **main** `()`

## src/ndoc/atoms
*   **[ast.py](src/ndoc/atoms/ast.py#L1)**
    *   VAR **tspython** ` = None`
    *   VAR **tscpp** ` = None`
    *   VAR **tsjs** ` = None`
    *   VAR **tsts** ` = None`
    *   VAR **tsgo** ` = None`
    *   VAR **tsrust** ` = None`
    *   VAR **tsdart** ` = None`
    *   VAR **tscsharp** ` = None`
    *   VAR **tsjava** ` = None`
    *   FUN **get_language** `(lang_key: str) -> Optional[Language]`
    *   CLS **AstNode**
    *   VAR **type** `: str`
    *   VAR **text** `: str`
    *   VAR **start_point** `: tuple[int, int]`
    *   VAR **end_point** `: tuple[int, int]`
    *   VAR **children** `: List['AstNode'] = field(default_factory=list)`
    *   PRP **start_line** `(self) -> int`
    *   PRP **end_line** `(self) -> int`
    *   FUN **get_parser** `(lang_key: str = 'python') -> Optional[Parser]`
    *   FUN **parse_code** `(content: str, file_path: Optional[Path] = None) -> Optional[Tree]`
    *   FUN **query_tree** `(tree: Tree, query_scm: str, lang_key: str = 'python') -> List[Dict[str, Node]]`
    *   FUN **node_to_data** `(node: Node, include_children: bool = False) -> AstNode`
    *   FUN **extract_symbols** `(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]`
*   **[cache.py](src/ndoc/atoms/cache.py#L1)**
    *   CLS **FileCache**
    *   MET **load** `(self)`
    *   MET **save** `(self)`
    *   MET **get_file_hash** `(self, file_path: Path) -> str`
    *   MET **is_changed** `(self, file_path: Path) -> bool`
    *   MET **update** `(self, file_path: Path, result: Any)`
    *   MET **get** `(self, file_path: Path) -> Optional[Any]`
*   **[deps.py](src/ndoc/atoms/deps.py#L1)**
    *   VAR **DEFAULT_IGNORE_PATTERNS** ` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_modules', 'venv', 'env', '.env', 
    'dist', 'build', 'target', 'out', 
    '.dart_tool', '.pub-cache', 
    'coverage', 'tmp', 'temp'
}`
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
}`
    *   FUN **detect_languages** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]`
    *   FUN **extract_imports** `(content: str) -> List[str]`
    *   FUN **parse_requirements_txt** `(file_path: Path) -> List[str]`
    *   FUN **parse_pyproject_toml** `(file_path: Path) -> List[str]`
    *   FUN **parse_package_json** `(file_path: Path) -> List[str]`
    *   FUN **parse_pubspec_yaml** `(file_path: Path) -> List[str]`
    *   FUN **parse_cmake_lists** `(file_path: Path) -> List[str]`
    *   FUN **extract_cpp_includes** `(content: str) -> List[str]`
    *   FUN **extract_dart_imports** `(content: str) -> List[str]`
    *   FUN **extract_csharp_usings** `(content: str) -> List[str]`
    *   FUN **parse_csproj** `(file_path: Path) -> List[str]`
    *   VAR **SOURCE_PARSERS** ` = {
    '.py': extract_imports,
    '.dart': extract_dart_imports,
    '.cpp': extract_cpp_includes,
    '.h': extract_cpp_includes,
    '.hpp': extract_cpp_includes,
    '.c': extract_cpp_includes,
    '.cc': extract_cpp_includes,
    '.cs': extract_csharp_usings,
}`
    *   FUN **extract_dependencies** `(content: str, file_path: Path) -> List[str]`
    *   FUN **get_project_dependencies** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]`
*   **[fs.py](src/ndoc/atoms/fs.py#L1)**
    *   CLS **FileFilter**
    *   VAR **ignore_patterns** `: Set[str] = field(default_factory=set)`
    *   VAR **allow_extensions** `: Set[str] = field(default_factory=set)`
    *   VAR **spec** `: Optional[pathspec.PathSpec] = None`
    *   PRP **has_extension_filter** `(self) -> bool`
    *   FUN **load_gitignore** `(root: Path) -> Optional[pathspec.PathSpec]`
    *   FUN **should_ignore** `(path: Path, filter_config: FileFilter, root: Path = None) -> bool`
    *   FUN **list_dir** `(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]`
    *   FUN **walk_files** `(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]`
    *   FUN **get_relative_path** `(path: Path, root: Path) -> str`
*   **[io.py](src/ndoc/atoms/io.py#L1)**
    *   FUN **set_dry_run** `(enabled: bool) -> None`
    *   FUN **safe_io** `(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any`
    *   FUN **read_text** `(path: Path) -> Optional[str]`
    *   FUN **read_head** `(path: Path, n_bytes: int = 2048) -> Optional[str]`
    *   FUN **write_text** `(path: Path, content: str) -> bool`
    *   FUN **read_lines** `(path: Path) -> List[str]`
    *   FUN **append_text** `(path: Path, content: str) -> bool`
    *   FUN **update_section** `(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool`
    *   FUN **update_header_timestamp** `(path: Path) -> bool`
    *   FUN **delete_file** `(path: Path) -> bool`
*   **[llm.py](src/ndoc/atoms/llm.py#L1)**
    *   FUN **call_llm** `(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]`
*   **[scanner.py](src/ndoc/atoms/scanner.py#L1)**
    *   CLS **TokenRule**
    *   VAR **name** `: str`
    *   VAR **pattern** `: Pattern`
    *   VAR **group_map** `: Dict[str, int]`
    *   CLS **ScanResult**
    *   VAR **tags** `: List[Tag] = field(default_factory=list)`
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)`
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)`
    *   VAR **docstring** `: str = ""`
    *   VAR **summary** `: str = ""`
    *   VAR **todos** `: List[dict] = field(default_factory=list)`
    *   VAR **is_core** `: bool = False`
    *   FUN **get_cache** `(root: Path) -> cache.FileCache`
    *   FUN **scan_file** `(file_path: Path, root: Path) -> ScanResult`
    *   FUN **extract_todos** `(content: str) -> List[dict]`
    *   FUN **extract_docstring** `(content: str) -> str`
    *   VAR **TAG_REGEX** ` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)`
    *   VAR **SECTION_REGEX** ` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->", re.DOTALL
)`
    *   VAR **DOCSTRING_PATTERNS** ` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.compile(r"^\s*'''(.*?)'''", re.DOTALL),
]`
    *   FUN **parse_tags** `(content: str) -> List[Tag]`
    *   FUN **parse_sections** `(content: str) -> Dict[str, Section]`
    *   FUN **extract_summary** `(content: str, docstring: str) -> str`
    *   FUN **regex_scan** `(content: str, ext: str) -> List[Symbol]`
    *   FUN **scan_file_content** `(content: str, file_path: Optional[Path] = None) -> ScanResult`

## src/ndoc/atoms/langs
*   **[__init__.py](src/ndoc/atoms/langs/__init__.py#L1)**
    *   CLS **LanguageDefinition**
    *   VAR **ID** `: str = ""`
    *   VAR **EXTENSIONS** `: List[str] = []`
    *   VAR **SCM_QUERY** `: str = ""`
    *   VAR **CLASS_TYPES** `: List[str] = []`
    *   VAR **ASYNC_KEYWORDS** `: List[str] = ["async"]`
    *   STA **get_visibility** `(captures: Dict[str, Any], content_bytes: bytes) -> str`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
    *   CLM **is_async** `(cls, node_text: str) -> bool`
    *   STA **extract_docstring** `(node: Any, content_bytes: bytes) -> Optional[str]`
    *   STA **format_signature** `(params_text: Optional[str], return_text: Optional[str]) -> str`
    *   FUN **register_language** `(lang_cls: Type[LanguageDefinition])`
    *   FUN **load_languages** `()`
    *   FUN **get_lang_def** `(lang_id: str) -> Optional[Type[LanguageDefinition]]`
    *   FUN **get_lang_id_by_ext** `(ext: str) -> Optional[str]`
    *   FUN **get_all_extensions** `() -> List[str]`
*   **[cpp.py](src/ndoc/atoms/langs/cpp.py#L1)**
    *   CLS **CppDefinition**
    *   VAR **ID** ` = "cpp"`
    *   VAR **EXTENSIONS** ` = [".cpp", ".c", ".h", ".hpp"]`
    *   VAR **CLASS_TYPES** ` = ["class_specifier", "struct_specifier"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[csharp.py](src/ndoc/atoms/langs/csharp.py#L1)**
    *   CLS **CSharpDefinition**
    *   VAR **ID** ` = "c_sharp"`
    *   VAR **EXTENSIONS** ` = [".cs"]`
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]`
    *   VAR **SCM_QUERY** ` = """
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
  (modifier_list)? @visibility
  name: (identifier) @name
  parameters: (parameter_list) @params
  type: (_)? @ret
) @func_def

(constructor_declaration
  (modifier_list)? @visibility
  name: (identifier) @name
  parameters: (parameter_list) @params
) @func_def
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[dart.py](src/ndoc/atoms/langs/dart.py#L1)**
    *   CLS **DartDefinition**
    *   VAR **ID** ` = "dart"`
    *   VAR **EXTENSIONS** ` = [".dart"]`
    *   VAR **CLASS_TYPES** ` = ["class_definition", "mixin_declaration", "enum_declaration"]`
    *   VAR **SCM_QUERY** ` = """
(class_definition name: (identifier) @name) @class_def
(mixin_declaration name: (identifier) @name) @struct_def
(enum_declaration name: (identifier) @name) @struct_def
(function_definition name: (identifier) @name) @func_def
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[go.py](src/ndoc/atoms/langs/go.py#L1)**
    *   CLS **GoDefinition**
    *   VAR **ID** ` = "go"`
    *   VAR **EXTENSIONS** ` = [".go"]`
    *   VAR **CLASS_TYPES** ` = ["type_declaration", "type_spec"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[java.py](src/ndoc/atoms/langs/java.py#L1)**
    *   CLS **JavaDefinition**
    *   VAR **ID** ` = "java"`
    *   VAR **EXTENSIONS** ` = [".java"]`
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[javascript.py](src/ndoc/atoms/langs/javascript.py#L1)**
    *   CLS **JavascriptDefinition**
    *   VAR **ID** ` = "javascript"`
    *   VAR **EXTENSIONS** ` = [".js", ".jsx"]`
    *   VAR **CLASS_TYPES** ` = ["class_declaration"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[python.py](src/ndoc/atoms/langs/python.py#L1)**
    *   CLS **PythonDefinition**
    *   VAR **ID** ` = "python"`
    *   VAR **EXTENSIONS** ` = [".py"]`
    *   VAR **CLASS_TYPES** ` = ["class_definition"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
    *   STA **extract_docstring** `(node: Any, content_bytes: bytes) -> Optional[str]`
    *   STA **format_signature** `(params_text: Optional[str], return_text: Optional[str]) -> str`
*   **[rust.py](src/ndoc/atoms/langs/rust.py#L1)**
    *   CLS **RustDefinition**
    *   VAR **ID** ` = "rust"`
    *   VAR **EXTENSIONS** ` = [".rs"]`
    *   VAR **CLASS_TYPES** ` = ["struct_item", "trait_item", "impl_item"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`
*   **[typescript.py](src/ndoc/atoms/langs/typescript.py#L1)**
    *   CLS **TypescriptDefinition**
    *   VAR **ID** ` = "typescript"`
    *   VAR **EXTENSIONS** ` = [".ts", ".tsx"]`
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declaration"]`
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
"""`
    *   STA **is_public** `(name: str, visibility: str) -> bool`

## src/ndoc/flows
*   **[archive_flow.py](src/ndoc/flows/archive_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[clean_flow.py](src/ndoc/flows/clean_flow.py#L1)**
    *   VAR **GENERATED_FILES** ` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md",
    "_NEXT.md",
    # _ARCH.md is typically manual or hybrid, avoiding delete for safety unless confirmed
]`
    *   FUN **run** `(config: ProjectConfig, target: str = None, force: bool = False) -> bool`
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
"""`
    *   FUN **load_project_config** `(root_path: Path) -> ProjectConfig`
    *   FUN **ensure_rules_file** `(root_path: Path, force: bool = False) -> bool`
*   **[context_flow.py](src/ndoc/flows/context_flow.py#L1)**
    *   FUN **format_file_summary** `(ctx: FileContext, root: Optional[Path] = None) -> str`
    *   FUN **format_symbol_list** `(ctx: FileContext) -> str`
    *   FUN **format_dependencies** `(ctx: FileContext) -> str`
    *   FUN **generate_dir_content** `(context: DirectoryContext) -> str`
    *   FUN **cleanup_legacy_map** `(file_path: Path) -> None`
    *   FUN **process_directory** `(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False) -> Optional[DirectoryContext]`
    *   FUN **run** `(config: ProjectConfig) -> bool`
    *   FUN **update_directory** `(path: Path, config: ProjectConfig) -> bool`
*   **[data_flow.py](src/ndoc/flows/data_flow.py#L1)**
    *   CLS **DataDefinition**
    *   VAR **name** `: str`
    *   VAR **type** `: str`
    *   VAR **path** `: str`
    *   VAR **docstring** `: str`
    *   VAR **fields** `: List[str]`
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[deps_flow.py](src/ndoc/flows/deps_flow.py#L1)**
    *   FUN **collect_imports** `(root: Path) -> Dict[str, List[str]]`
    *   FUN **build_dependency_graph** `(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
    *   FUN **generate_mermaid_graph** `(graph: Dict[str, Set[str]]) -> str`
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[doctor_flow.py](src/ndoc/flows/doctor_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[init_flow.py](src/ndoc/flows/init_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool`
*   **[map_flow.py](src/ndoc/flows/map_flow.py#L1)**
    *   CLS **MapContext**
    *   VAR **root** `: Path`
    *   VAR **ignore_patterns** `: List[str]`
    *   FUN **format_dir_entry** `(name: str, level: int) -> str`
    *   FUN **format_file_entry** `(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str`
    *   FUN **extract_file_summary** `(path: Path) -> str`
    *   FUN **build_tree_lines** `(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]`
    *   FUN **generate_tree_content** `(config: ProjectConfig) -> str`
    *   FUN **run** `(config: ProjectConfig) -> bool`
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
"""`
    *   FUN **run** `(config: ProjectConfig, objective: str) -> bool`
*   **[stats_flow.py](src/ndoc/flows/stats_flow.py#L1)**
    *   FUN **check_should_update** `(root_path: Path, force: bool) -> bool`
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool`
*   **[symbols_flow.py](src/ndoc/flows/symbols_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool`
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
"""`
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool`
*   **[tech_flow.py](src/ndoc/flows/tech_flow.py#L1)**
    *   FUN **generate_tech_content** `(config: ProjectConfig) -> str`
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[todo_flow.py](src/ndoc/flows/todo_flow.py#L1)**
    *   CLS **TodoItem**
    *   VAR **file_path** `: Path`
    *   VAR **line** `: int`
    *   VAR **type** `: str`
    *   VAR **content** `: str`
    *   VAR **task_id** `: Optional[str] = None`
    *   PRP **priority_icon** `(self) -> str`
    *   FUN **collect_todos** `(root: Path, ignore_patterns: List[str]) -> List[TodoItem]`
    *   FUN **format_todo_lines** `(todos: List[TodoItem], root: Path) -> str`
    *   FUN **sync_tasks** `(config: ProjectConfig, todos: List[TodoItem]) -> bool`
    *   FUN **run** `(config: ProjectConfig) -> bool`
*   **[update_flow.py](src/ndoc/flows/update_flow.py#L1)**
    *   FUN **run** `() -> bool`
*   **[verify_flow.py](src/ndoc/flows/verify_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool`

## src/ndoc/models
*   **[config.py](src/ndoc/models/config.py#L1)**
    *   CLS **ScanConfig**
    *   VAR **root_path** `: Path`
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
    ])`
    *   VAR **extensions** `: List[str] = field(default_factory=list)`
    *   CLS **ProjectConfig**
    *   VAR **scan** `: ScanConfig`
    *   VAR **name** `: str = "Project"`
    *   VAR **version** `: str = "0.1.0"`
*   **[context.py](src/ndoc/models/context.py#L1)**
    *   CLS **Tag**
    *   VAR **name** `: str`
    *   VAR **args** `: List[str] = field(default_factory=list)`
    *   VAR **line** `: int = 0`
    *   VAR **raw** `: str = ""`
    *   CLS **Section**
    *   VAR **name** `: str`
    *   VAR **content** `: str`
    *   VAR **raw** `: str`
    *   VAR **start_pos** `: int`
    *   VAR **end_pos** `: int`
    *   CLS **Symbol**
    *   VAR **name** `: str`
    *   VAR **kind** `: str`
    *   VAR **line** `: int`
    *   VAR **docstring** `: Optional[str] = None`
    *   VAR **signature** `: Optional[str] = None`
    *   VAR **parent** `: Optional[str] = None`
    *   VAR **is_core** `: bool = False`
    *   VAR **visibility** `: str = "public"`
    *   VAR **lang** `: str = "unknown"`
    *   VAR **decorators** `: List[str] = field(default_factory=list)`
    *   VAR **bases** `: List[str] = field(default_factory=list)`
    *   VAR **full_content** `: str = ""`
    *   PRP **is_public** `(self) -> bool`
    *   CLS **FileContext**
    *   VAR **path** `: Path`
    *   VAR **rel_path** `: str`
    *   VAR **content** `: Optional[str] = None`
    *   VAR **tags** `: List[Tag] = field(default_factory=list)`
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)`
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)`
    *   VAR **docstring** `: Optional[str] = None`
    *   VAR **is_core** `: bool = False`
    *   VAR **ast_tree** `: Any = None`
    *   VAR **title** `: Optional[str] = None`
    *   VAR **description** `: Optional[str] = None`
    *   PRP **has_content** `(self) -> bool`
    *   CLS **DirectoryContext**
    *   VAR **path** `: Path`
    *   VAR **files** `: List[FileContext] = field(default_factory=list)`
    *   VAR **subdirs** `: List[Path] = field(default_factory=list)`
    *   PRP **name** `(self) -> str`

## tests
*   **[conftest.py](tests/conftest.py#L1)**
    *   VAR **root** ` = Path(__file__).parent.parent`
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
"""`
    *   FUN **test_extract_symbols_basic** `()`
    *   FUN **test_extract_complex_api** `()`
    *   FUN **find_sym** `(name)`
    *   FUN **find_member** `(cls_name, name)`
*   **[test_scanner.py](tests/test_scanner.py#L1)**
    *   VAR **SAMPLE_CONTENT** ` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<!-- NIKI_TEST_END -->

class TestClass:
    '''Doc'''
    pass
"""`
    *   FUN **test_scan_file_content_mixed** `()`
    *   FUN **test_scan_file_content_text_only** `()`

## tests/fixtures
*   **[complex_api.py](tests/fixtures/complex_api.py#L1)**
    *   CLS **User**
    *   VAR **name** `: str`
    *   VAR **age** `: int = 18`
    *   PRP **is_adult** `(self) -> bool`
    *   ASY **fetch_data** `(self) -> dict`
    *   CLM **from_dict** `(cls, data: dict) -> "User"`
    *   CLS **Database**
    *   VAR **connection_string** `: str = "localhost:5432"`
    *   MET **connect** `(self)`
    *   FUN **global_func** `(x: int, y: int) -> int`
    *   ASY **global_async_func** `()`

## vendors/tree-sitter-dart
*   **[grammar.js](vendors/tree-sitter-dart/grammar.js#L1)**
    *   VAR **DART_PREC** ` = {
    IMPORT_EXPORT: 19,
    TYPE_IDENTIFIER: 18, //was: 17
    DOT_IDENTIFIER: 19, //was: 18
    UNARY_POSTFIX: 17,
    UNARY_PREFIX: 16,
    Multiplicative: 15, // *, /, ˜/, % Left
    Additive: 14, // +, - Left
    Shift: 13, // <<, >>, >>> Left
    TYPE_ARGUMENTS: 13,
    Bitwise_AND: 12, // & Left
    Bitwise_XOR: 11, // ˆ Left
    Bitwise_Or: 10, // | Left
    RelationalTypeCast: 9, // <, >, <=, >=, as, is, is! None 8
    RelationalTypeTest: 9,
    Relational: 8, // <, >, <=, >=, as, is, is! None 8
    Equality: 7, // ==, != None 7
    Logical_AND: 6, // AND && Left
    Logical_OR: 5, // Or || Left
    If: 4, //-null ?? Left
    Conditional: 3, // e1?e2:e3 Right 3
    Cascade: 2, // .. Left
    Assignment: 1, // =, *=, /=, +=, -=, &=, ˆ=, etc. Right
    BUILTIN: 0,
    TRY: 0,
    // Added by Ben for experimentation.
    SELECTOR_IN_PRIMARY: 1,
    SELECTOR_IN_ASSIGNMENT: 0,
    TYPE_ARGS: 1
}`
    *   FUN **sep1** `(rule, separator)`
    *   FUN **sep2** `(rule, separator)`
    *   FUN **commaSep1** `(rule)`
    *   FUN **commaSep** `(rule)`
    *   FUN **commaSep2TrailingComma** `(rule)`
    *   FUN **commaSep1TrailingComma** `(rule)`
    *   FUN **commaSepTrailingComma** `(rule)`
    *   FUN **pureBinaryRun** `(rule, separator, precedence)`
    *   FUN **binaryRunLeft** `(rule, separator, superItem, precedence)`
*   **[setup.py](vendors/tree-sitter-dart/setup.py#L1)**
    *   CLS **Build**
    *   MET **run** `(self)`
    *   CLS **BdistWheel**
    *   MET **get_tag** `(self)`

## vendors/tree-sitter-dart/assets
*   **[playground.js](vendors/tree-sitter-dart/assets/playground.js#L1)**
    *   VAR **COLORS_BY_INDEX** ` = [
    'blue',
    'chocolate',
    'darkblue',
    'darkcyan',
    'darkgreen',
    'darkred',
    'darkslategray',
    'dimgray',
    'green',
    'indigo',
    'navy',
    'red',
    'sienna',
  ]`
    *   VAR **languagesByName** ` = {}`
    *   VAR **treeRows** ` = null`
    *   VAR **parseCount** ` = 0`
    *   VAR **isRendering** ` = 0`
    *   ASY **handleLanguageChange** `()`
    *   ASY **handleCodeChange** `(editor, changes)`
    *   ASY **renderTree** `()`
    *   VAR **row** ` = ''`
    *   VAR **rows** ` = []`
    *   VAR **finishedRow** ` = false`
    *   VAR **visitedChildren** ` = false`
    *   VAR **indentLevel** ` = 0`
    *   VAR **i** ` = 0`
    *   FUN **runTreeQuery** `(_, startRow, endRow)`
    *   FUN **handleQueryChange** `()`
    *   VAR **row** ` = 0`
    *   VAR **endPosition** ` = {
          line: startPosition.line,
          ch: startPosition.ch + (error.length || Infinity)
        }`
    *   FUN **handleCursorMovement** `()`
    *   VAR **start** ` = {row: selection.anchor.line, column: selection.anchor.ch}`
    *   VAR **end** ` = {row: selection.head.line, column: selection.head.ch}`
    *   FUN **handleTreeClick** `(event)`
    *   FUN **handleLoggingChange** `()`
    *   FUN **handleQueryEnableChange** `()`
    *   FUN **treeEditForEditorChange** `(change)`
    *   VAR **startPosition** ` = {row: change.from.line, column: change.from.ch}`
    *   VAR **oldEndPosition** ` = {row: change.to.line, column: change.to.ch}`
    *   VAR **newEndPosition** ` = {
      row: startPosition.row + newLineCount - 1,
      column: newLineCount === 1
        ? startPosition.column + lastLineLength
        : lastLineLength
    }`
    *   VAR **i** ` = 0`
    *   VAR **i** ` = 0`
    *   FUN **colorForCaptureName** `(capture)`
    *   FUN **loadState** `()`
    *   FUN **saveState** `()`
    *   FUN **saveQueryState** `()`
    *   FUN **debounce** `(func, wait, immediate)`
    *   FUN **later** `()`
*   **[tree-sitter.js](vendors/tree-sitter-dart/assets/tree-sitter.js#L1)**
    *   CLS **Parser**
    *   MET **constructor** `()`
    *   MET **initialize** `()`
    *   MET **init** `(r)`
    *   MET **u** `(e,t)`
    *   MET **b** `(e,t)`
    *   MET **E** `(e)`
    *   MET **x** `(e,t,r,n)`
    *   MET **N** `(e,t,r)`
    *   MET **k** `(e,t)`
    *   MET **$** `(e,t,r)`
    *   MET **j** `(e,t)`
    *   MET **U** `(e,t,r,n)`
    *   MET **D** `(e,t,r)`
    *   MET **z** `(e)`
    *   MET **G** `(e)`
    *   MET **H** `(e)`
    *   MET **ne** `(e)`
    *   MET **se** `(e)`
    *   MET **oe** `(e)`
    *   MET **le** `(e)`
    *   MET **de** `(e)`
    *   MET **ce** `(e)`
    *   MET **pe** `(e)`
    *   MET **he** `(e)`
    *   MET **r** `()`
    *   MET **we** `()`
    *   MET **ye** `(e)`
    *   MET **Me** `(e,t)`
    *   MET **ve** `(e,t,r)`
    *   MET **Ie** `(e)`
    *   MET **Ae** `(e,t)`
    *   MET **Se** `(e,t)`
    *   MET **xe** `(e,t)`
    *   MET **n** `()`
    *   MET **c** `(e)`
    *   MET **Ne** `(e,t)`
    *   MET **s** `(e)`
    *   MET **o** `()`
    *   MET **Pe** `()`
    *   MET **qe** `()`
    *   MET **Te** `(e,t)`
    *   MET **Le** `(e)`
    *   MET **We** `(e)`
    *   MET **Oe** `(e)`
    *   MET **t** `(e,t)`
    *   MET **r** `(e)`
    *   MET **n** `(t)`
    *   MET **He** `(e)`
    *   MET **Ke** `(e)`
    *   MET **t** `()`
    *   MET **Ve** `(e,t)`
    *   CLS **ParserImpl**
    *   MET **init** `()`
    *   MET **initialize** `()`
    *   MET **delete** `()`
    *   MET **setLanguage** `(e)`
    *   MET **getLanguage** `()`
    *   MET **parse** `(e,t,r)`
    *   MET **reset** `()`
    *   MET **setTimeoutMicros** `(e)`
    *   MET **getTimeoutMicros** `()`
    *   MET **setLogger** `(e)`
    *   MET **getLogger** `()`
    *   CLS **Tree**
    *   MET **constructor** `(e,t,r,n)`
    *   MET **copy** `()`
    *   MET **delete** `()`
    *   MET **edit** `(e)`
    *   MET **rootNode** `()`
    *   MET **getLanguage** `()`
    *   MET **walk** `()`
    *   MET **getChangedRanges** `(e)`
    *   CLS **Node**
    *   MET **constructor** `(e,t)`
    *   MET **typeId** `()`
    *   MET **type** `()`
    *   MET **endPosition** `()`
    *   MET **endIndex** `()`
    *   MET **text** `()`
    *   MET **isNamed** `()`
    *   MET **hasError** `()`
    *   MET **hasChanges** `()`
    *   MET **isMissing** `()`
    *   MET **equals** `(e)`
    *   MET **child** `(e)`
    *   MET **namedChild** `(e)`
    *   MET **childForFieldId** `(e)`
    *   MET **childForFieldName** `(e)`
    *   MET **childCount** `()`
    *   MET **namedChildCount** `()`
    *   MET **firstChild** `()`
    *   MET **firstNamedChild** `()`
    *   MET **lastChild** `()`
    *   MET **lastNamedChild** `()`
    *   MET **children** `()`
    *   MET **namedChildren** `()`
    *   MET **descendantsOfType** `(e,t,r)`
    *   MET **nextSibling** `()`
    *   MET **previousSibling** `()`
    *   MET **nextNamedSibling** `()`
    *   MET **previousNamedSibling** `()`
    *   MET **parent** `()`
    *   MET **descendantForIndex** `(e,t=e)`
    *   MET **namedDescendantForIndex** `(e,t=e)`
    *   MET **descendantForPosition** `(e,t=e)`
    *   MET **namedDescendantForPosition** `(e,t=e)`
    *   MET **walk** `()`
    *   MET **toString** `()`
    *   CLS **TreeCursor**
    *   MET **constructor** `(e,t)`
    *   MET **delete** `()`
    *   MET **reset** `(e)`
    *   MET **nodeType** `()`
    *   MET **nodeTypeId** `()`
    *   MET **nodeId** `()`
    *   MET **nodeIsNamed** `()`
    *   MET **nodeIsMissing** `()`
    *   MET **nodeText** `()`
    *   MET **startPosition** `()`
    *   MET **endPosition** `()`
    *   MET **startIndex** `()`
    *   MET **endIndex** `()`
    *   MET **currentNode** `()`
    *   MET **currentFieldId** `()`
    *   MET **currentFieldName** `()`
    *   MET **gotoFirstChild** `()`
    *   MET **gotoNextSibling** `()`
    *   MET **gotoParent** `()`
    *   CLS **Language**
    *   MET **constructor** `(e,t)`
    *   MET **version** `()`
    *   MET **fieldCount** `()`
    *   MET **fieldIdForName** `(e)`
    *   MET **fieldNameForId** `(e)`
    *   MET **idForNodeType** `(e,t)`
    *   MET **nodeTypeCount** `()`
    *   MET **nodeTypeForId** `(e)`
    *   MET **nodeTypeIsNamed** `(e)`
    *   MET **nodeTypeIsVisible** `(e)`
    *   MET **query** `(e)`
    *   MET **load** `(e)`
    *   CLS **Query**
    *   MET **constructor** `(e,t,r,n,s,o,_,a)`
    *   MET **delete** `()`
    *   MET **matches** `(e,t,r,n)`
    *   MET **captures** `(e,t,r,n)`
    *   MET **predicatesForPattern** `(e)`
    *   MET **didExceedMatchLimit** `()`
    *   MET **mt** `(e,t,r)`
    *   MET **ft** `(e,t,r,n)`
    *   MET **pt** `(e)`
    *   MET **ht** `(e)`
    *   MET **gt** `(e)`
    *   MET **wt** `(e,t=lt)`
    *   MET **yt** `(e,t=lt)`
    *   MET **Mt** `(e)`
    *   MET **bt** `(e,t)`
    *   MET **vt** `(e)`
    *   MET **Et** `(e,t)`
    *   MET **It** `(e)`

## vendors/tree-sitter-dart/bindings/c
*   **[tree-sitter-dart.h](vendors/tree-sitter-dart/bindings/c/tree-sitter-dart.h#L1)**
    *   STC **TSLanguage**

## vendors/tree-sitter-dart/bindings/go
*   **[binding.go](vendors/tree-sitter-dart/bindings/go/binding.go#L1)**
    *   FUN **Language** `() -> unsafe.Pointer`
*   **[binding_test.go](vendors/tree-sitter-dart/bindings/go/binding_test.go#L1)**
    *   FUN **TestCanLoadGrammar** `(t *testing.T)`

## vendors/tree-sitter-dart/bindings/python/tree_sitter_dart
*   **[binding.c](vendors/tree-sitter-dart/bindings/python/tree_sitter_dart/binding.c#L1)**
    *   STC **TSLanguage**
    *   STC **PyModuleDef**
    *   FUN **PyInit__binding**

## vendors/tree-sitter-dart/bindings/swift/TreeSitterDart
*   **[dart.h](vendors/tree-sitter-dart/bindings/swift/TreeSitterDart/dart.h#L1)**
    *   STC **TSLanguage**

## vendors/tree-sitter-dart/src
*   **[parser.c](vendors/tree-sitter-dart/src/parser.c#L1)**
    *   FUN **ts_lex**
    *   FUN **ts_lex_keywords**
    *   FUN **tree_sitter_dart_external_scanner_destroy**
    *   FUN **tree_sitter_dart_external_scanner_scan**
    *   FUN **tree_sitter_dart_external_scanner_serialize**
    *   FUN **tree_sitter_dart_external_scanner_deserialize**
*   **[scanner.c](vendors/tree-sitter-dart/src/scanner.c#L1)**
    *   FUN **tree_sitter_dart_external_scanner_destroy**
    *   FUN **tree_sitter_dart_external_scanner_reset**
    *   FUN **tree_sitter_dart_external_scanner_serialize**
    *   FUN **tree_sitter_dart_external_scanner_deserialize**
    *   FUN **advance**
    *   FUN **skip**
    *   FUN **scan_multiline_comments**
    *   FUN **scan_templates**
    *   FUN **tree_sitter_dart_external_scanner_scan**

## vendors/tree-sitter-dart/src/tree_sitter
*   **[parser.h](vendors/tree-sitter-dart/src/tree_sitter/parser.h#L1)**
    *   STC **TSLanguage**
    *   STC **TSLanguageMetadata**
    *   VAR **major_version** `: uint8_t`
    *   VAR **minor_version** `: uint8_t`
    *   VAR **patch_version** `: uint8_t`
    *   VAR **field_id** `: TSFieldId`
    *   VAR **child_index** `: uint8_t`
    *   VAR **inherited** `: bool`
    *   VAR **index** `: uint16_t`
    *   VAR **length** `: uint16_t`
    *   VAR **visible** `: bool`
    *   VAR **named** `: bool`
    *   VAR **supertype** `: bool`
    *   STC **TSLexer**
    *   STC **TSLexer**
    *   VAR **lookahead** `: int32_t`
    *   VAR **result_symbol** `: TSSymbol`
    *   VAR **shift** `: struct {
    uint8_t type;
    TSStateId state;
    bool extra;
    bool repetition;
  }`
    *   VAR **type** `: uint8_t`
    *   VAR **state** `: TSStateId`
    *   VAR **extra** `: bool`
    *   VAR **repetition** `: bool`
    *   VAR **reduce** `: struct {
    uint8_t type;
    uint8_t child_count;
    TSSymbol symbol;
    int16_t dynamic_precedence;
    uint16_t production_id;
  }`
    *   VAR **type** `: uint8_t`
    *   VAR **child_count** `: uint8_t`
    *   VAR **symbol** `: TSSymbol`
    *   VAR **dynamic_precedence** `: int16_t`
    *   VAR **production_id** `: uint16_t`
    *   VAR **type** `: uint8_t`
    *   VAR **lex_state** `: uint16_t`
    *   VAR **external_lex_state** `: uint16_t`
    *   VAR **lex_state** `: uint16_t`
    *   VAR **external_lex_state** `: uint16_t`
    *   VAR **reserved_word_set_id** `: uint16_t`
    *   VAR **action** `: TSParseAction`
    *   VAR **entry** `: struct {
    uint8_t count;
    bool reusable;
  }`
    *   VAR **count** `: uint8_t`
    *   VAR **reusable** `: bool`
    *   VAR **start** `: int32_t`
    *   VAR **end** `: int32_t`
    *   STC **TSLanguage**
    *   VAR **abi_version** `: uint32_t`
    *   VAR **symbol_count** `: uint32_t`
    *   VAR **alias_count** `: uint32_t`
    *   VAR **token_count** `: uint32_t`
    *   VAR **external_token_count** `: uint32_t`
    *   VAR **state_count** `: uint32_t`
    *   VAR **large_state_count** `: uint32_t`
    *   VAR **production_id_count** `: uint32_t`
    *   VAR **field_count** `: uint32_t`
    *   VAR **max_alias_sequence_length** `: uint16_t`
    *   VAR **keyword_capture_token** `: TSSymbol`
    *   VAR **external_scanner** `: struct {
    const bool *states;
    const TSSymbol *symbol_map;
    void *(*create)(void);
    void (*destroy)(void *);
    bool (*scan)(void *, TSLexer *, const bool *symbol_whitelist);
    unsigned (*serialize)(void *, char *);
    void (*deserialize)(void *, const char *, unsigned);
  }`
    *   VAR **max_reserved_word_set_size** `: uint16_t`
    *   VAR **supertype_count** `: uint32_t`
    *   VAR **metadata** `: TSLanguageMetadata`
    *   FUN **set_contains**
