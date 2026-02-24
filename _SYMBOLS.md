# Symbol Index
> 最后更新 (Last Updated): 2026-02-24 15:04:15

## @OVERVIEW
*   **Total Public Symbols**: 385

## Root
*   **[debug_scanner.py](debug_scanner.py#L1)**
    *   FUN **test** `()` [🔗161]
*   **[debug_symbols.py](debug_symbols.py#L1)**
    *   VAR **file_path** ` = Path("src/ndoc/atoms/deps/stats.py")` [🔗181]
    *   VAR **content** ` = read_text(file_path)` [🔗401]
    *   VAR **tree** ` = parse_code(content, file_path)` [🔗133]
    *   VAR **symbols** ` = extract_symbols(tree, content.encode("utf-8"), file_path)` [🔗129]
*   **[test_enhanced_doc.py](test_enhanced_doc.py#L1)**
    *   FUN **test_func** `(a: int, b: str) -> bool` [🔗7]
    *   CLS **TestClass** [🔗5]
    *   VAR **field** `: int = 10` [🔗183]
    *   MET **test_method** `(self)` [🔗3]
*   **[test_python_fix.py](test_python_fix.py#L1)**
    *   FUN **test_python_parsing** `()` [🔗4]
*   **[test_regex.py](test_regex.py#L1)**
    *   VAR **TAG_REGEX** ` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s...` [🔗14]
    *   VAR **text** ` = """
Inner docstring for test_func.
    @INTERNAL
"""` [🔗400]
    *   VAR **matches** ` = list(TAG_REGEX.finditer(text))` [🔗40]
    *   VAR **text2** ` = """
# @CORE
# This is a core function.
"""` [🔗7]
    *   VAR **matches2** ` = list(TAG_REGEX.finditer(text2))` [🔗5]

## editors/vscode/out
*   **[extension.js](editors/vscode/out/extension.js#L1)**
    *   VAR **result** ` = {}` [🔗142]
    *   FUN **activate** `(context)` [🔗13]
    *   VAR **serverOptions** ` = {
        command: pythonPath,
        args: ['-m', 'ndoc.ls...` [🔗8]
    *   VAR **clientOptions** ` = {
        documentSelector: [
            { scheme: 'file', ...` [🔗8]
    *   FUN **deactivate** `()` [🔗9]

## editors/vscode/src
*   **[extension.ts](editors/vscode/src/extension.ts#L1)**
    *   FUN **activate** `(context: vscode.ExtensionContext)` [🔗13]
    *   VAR **serverOptions** ` = {
        command: pythonPath,
        args: ['-m', 'ndoc.ls...` [🔗8]
    *   VAR **clientOptions** ` = {
        documentSelector: [
            { scheme: 'file', ...` [🔗8]
    *   FUN **deactivate** `() -> : Thenable<void> | undefined` [🔗9]

## samples
*   **[sample_csharp.cs](samples/sample_csharp.cs#L1)**
    *   NSP **MyProject.Core**
    *   CLS **SampleService** [🔗6]
    *   PRP **Name** ` -> string` [🔗19]
    *   MET **SampleService()** `(string id)`
    *   MET **DoWork** `(int count, string message = "default") -> void` [🔗3]
    *   MET **Dispose** `() -> void` [🔗6]
    *   ENM **ServiceStatus** [🔗5]

## src/ndoc
*   **[daemon.py](src/ndoc/daemon.py#L1)**
    *   CLS **DocChangeHandler** [🔗4]
    *   MET **on_any_event** `(self, event: FileSystemEvent)` [🔗3]
    *   MET **trigger_update** `(self)` [🔗4]
    *   MET **run_update** `(self)` [🔗4]
    *   FUN **start_watch_mode** `(config: ProjectConfig)` [🔗5]
*   **[entry.py](src/ndoc/entry.py#L1)**
    *   FUN **main** `()` [🔗94]
*   **[lsp_server.py](src/ndoc/lsp_server.py#L1)**
    *   VAR **BASE_DIR** ` = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."...` [🔗5]
    *   CLS **NDocLanguageServer** [🔗21]
    *   VAR **server** ` = NDocLanguageServer("ndoc-ai-server", "v0.1.0")` [🔗20]
    *   FUN **lsp_initialize** `(ls: NDocLanguageServer, params)` [🔗3]
    *   FUN **check_architecture** `(ls: NDocLanguageServer, doc_uri: str)` [🔗5]
    *   FUN **did_open** `(ls: NDocLanguageServer, params)` [🔗3]
    *   FUN **did_save** `(ls: NDocLanguageServer, params: DidSaveTextDocumentParams)` [🔗3]
    *   FUN **hover** `(ls: NDocLanguageServer, params: HoverParams)` [🔗51]
    *   FUN **main** `()` [🔗94]

## src/ndoc/atoms
*   **[cache.py](src/ndoc/atoms/cache.py#L1)**
    *   CLS **FileCache** [🔗9]
    *   MET **load** `(self)` [🔗33]
    *   MET **save** `(self)` [🔗23]
    *   MET **get_file_hash** `(self, file_path: Path) -> str` [🔗5]
    *   MET **is_changed** `(self, file_path: Path) -> bool` [🔗4]
    *   MET **update** `(self, file_path: Path, result: Any)` [🔗53]
    *   MET **get** `(self, file_path: Path) -> Optional[Any]` [🔗169]
*   **[capabilities.py](src/ndoc/atoms/capabilities.py#L1)**
    *   CLS **CapabilityManager** [🔗21]
    *   VAR **LANGUAGE_PACKAGES** ` = {
        "python": "tree-sitter-python",
        "javascrip...` [🔗5]
    *   CLM **ensure_languages** `(cls, lang_names: set[str], auto_install: bool = True)` [🔗9]
    *   CLM **get_language** `(cls, lang_name: str, auto_install: bool = False) -> Optional[Language]` [🔗21]
*   **[fs.py](src/ndoc/atoms/fs.py#L1)**
    *   CLS **FileFilter** [🔗14]
    *   VAR **ignore_patterns** `: Set[str] = field(default_factory=set)` [🔗62]
    *   VAR **allow_extensions** `: Set[str] = field(default_factory=set)` [🔗8]
    *   VAR **spec** `: Optional[pathspec.PathSpec] = None` [🔗13]
    *   PRP **has_extension_filter** `(self) -> bool` [🔗5]
    *   FUN **load_gitignore** `(root: Path) -> Optional[pathspec.PathSpec]` [🔗5]
    *   FUN **should_ignore** `(path: Path, filter_config: FileFilter, root: Path = None) -> bool` [🔗7]
    *   FUN **list_dir** `(path: Path, filter_config: FileFilter, root: Path = None) -> List[Path]` [🔗4]
    *   FUN **walk_files** `(root: Path, ignore_patterns: List[str], extensions: List[str] = None) -> Iterator[Path]` [🔗18]
    *   FUN **get_relative_path** `(path: Path, root: Path) -> str` [🔗6]
*   **[io.py](src/ndoc/atoms/io.py#L1)**
    *   FUN **set_dry_run** `(enabled: bool) -> None` [🔗4]
    *   FUN **safe_io** `(operation: Callable[..., Any], error_msg: str, *args: Any, **kwargs: Any) -> Any` [🔗8]
    *   FUN **read_text** `(path: Path) -> Optional[str]` [🔗41]
    *   FUN **read_head** `(path: Path, n_bytes: int = 2048) -> Optional[str]` [🔗5]
    *   FUN **write_text** `(path: Path, content: str) -> bool` [🔗24]
    *   FUN **read_lines** `(path: Path) -> List[str]` [🔗3]
    *   FUN **append_text** `(path: Path, content: str) -> bool` [🔗4]
    *   FUN **update_section** `(path: Path, start_marker: str, end_marker: str, new_content: str) -> bool` [🔗9]
    *   FUN **update_header_timestamp** `(path: Path) -> bool` [🔗9]
    *   FUN **delete_file** `(path: Path) -> bool` [🔗5]
*   **[llm.py](src/ndoc/atoms/llm.py#L1)**
    *   FUN **call_llm** `(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]` [🔗5]
*   **[lsp.py](src/ndoc/atoms/lsp.py#L1)**
    *   CLS **LSPService** [🔗12]
    *   MET **index_project** `(self, files: List[Path])` [🔗9]
    *   MET **find_definitions** `(self, name: str) -> List[Symbol]` [🔗5]
    *   MET **get_reference_count** `(self, name: str) -> int` [🔗6]
    *   MET **get_context_for_file** `(self, file_path: Path) -> str` [🔗3]
    *   MET **find_references** `(self, name: str) -> List[Dict[str, Any]]` [🔗4]
    *   FUN **get_service** `(root: Path) -> LSPService` [🔗9]
*   **[scanner.py](src/ndoc/atoms/scanner.py#L1)**
    *   CLS **TokenRule** [🔗4]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **pattern** `: Pattern` [🔗56]
    *   VAR **group_map** `: Dict[str, int]` [🔗4]
    *   CLS **ScanResult** [🔗14]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗52]
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)` [🔗59]
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)` [🔗129]
    *   VAR **docstring** `: str = ""` [🔗70]
    *   VAR **summary** `: str = ""` [🔗77]
    *   VAR **todos** `: List[dict] = field(default_factory=list)` [🔗67]
    *   VAR **memories** `: List[dict] = field(default_factory=list)` [🔗24]
    *   VAR **calls** `: List[str] = field(default_factory=list)` [🔗55]
    *   VAR **imports** `: List[str] = field(default_factory=list)` [🔗40]
    *   VAR **is_core** `: bool = False` [🔗21]
    *   FUN **get_cache** `(root: Path) -> cache.FileCache` [🔗4]
    *   FUN **scan_file** `(file_path: Path, root: Path, force: bool = False) -> ScanResult` [🔗11]
    *   FUN **extract_todos** `(content: str) -> List[dict]` [🔗4]
    *   FUN **extract_memories** `(content: str) -> List[dict]` [🔗4]
    *   FUN **extract_docstring** `(content: str) -> str` [🔗14]
    *   VAR **SECTION_REGEX** ` = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<...` [🔗4]
    *   VAR **DOCSTRING_PATTERNS** ` = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.comp...` [🔗4]
    *   FUN **parse_tags** `(content: str) -> List[Tag]` [🔗5]
    *   FUN **parse_sections** `(content: str) -> Dict[str, Section]` [🔗4]
    *   FUN **extract_summary** `(content: str, docstring: str) -> str` [🔗5]
    *   FUN **regex_scan** `(content: str, ext: str) -> List[Symbol]` [🔗4]
    *   FUN **scan_file_content** `(content: str, file_path: Optional[Path] = None) -> ScanResult` [🔗8]
*   **[text_utils.py](src/ndoc/atoms/text_utils.py#L1)**
    *   VAR **TAG_REGEX** ` = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s...` [🔗14]
    *   FUN **clean_docstring** `(raw: str) -> str` [🔗8]
    *   FUN **extract_tags_from_text** `(text: str, line_offset: int = 0) -> List[Tag]` [🔗7]

## src/ndoc/atoms/ast
*   **[base.py](src/ndoc/atoms/ast/base.py#L1)**
    *   FUN **get_language** `(lang_key: str) -> Optional[Language]` [🔗21]
    *   CLS **AstNode** [🔗14]
    *   VAR **type** `: str` [🔗980]
    *   VAR **text** `: str` [🔗400]
    *   VAR **start_point** `: tuple[int, int]` [🔗9]
    *   VAR **end_point** `: tuple[int, int]` [🔗7]
    *   VAR **children** `: list['AstNode'] = field(default_factory=list)` [🔗71]
    *   PRP **start_line** `(self) -> int` [🔗3]
    *   PRP **end_line** `(self) -> int` [🔗3]
    *   FUN **get_parser** `(lang_key: str = 'python') -> Optional[Parser]` [🔗8]
    *   FUN **parse_code** `(content: str, file_path: Optional[Path] = None) -> Optional[Tree]` [🔗17]
    *   FUN **get_lang_key** `(file_path: Path) -> Optional[str]` [🔗8]
    *   FUN **query_tree** `(tree: Tree, query_scm: str, lang_key: str = 'python') -> list[dict]` [🔗9]
*   **[discovery.py](src/ndoc/atoms/ast/discovery.py#L1)**
    *   FUN **find_calls** `(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗7]
    *   FUN **find_imports** `(tree: Tree, lang_key: str = 'python') -> List[str]` [🔗7]
*   **[symbols.py](src/ndoc/atoms/ast/symbols.py#L1)**
    *   FUN **extract_symbols** `(tree: Tree, content_bytes: bytes, file_path: Optional[Path] = None) -> List[Symbol]` [🔗18]
*   **[utils.py](src/ndoc/atoms/ast/utils.py#L1)**
    *   VAR **MAX_VALUE_LENGTH** ` = 60` [🔗10]
    *   VAR **MAX_CONTENT_LENGTH** ` = 200` [🔗7]
    *   FUN **truncate** `(text: str, max_len: int = 100) -> str` [🔗10]
    *   FUN **node_to_data** `(node: Node, include_children: bool = False) -> AstNode` [🔗6]

## src/ndoc/atoms/deps
*   **[core.py](src/ndoc/atoms/deps/core.py#L1)**
    *   VAR **SOURCE_PARSERS** ` = {
    '.py': extract_imports,
    '.dart': extract_dart_impo...` [🔗9]
    *   FUN **extract_dependencies** `(content: str, file_path: Path) -> List[str]` [🔗6]
    *   FUN **get_project_dependencies** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, List[str]]` [🔗6]
*   **[manifests.py](src/ndoc/atoms/deps/manifests.py#L1)**
    *   FUN **parse_requirements_txt** `(file_path: Path) -> List[str]` [🔗7]
    *   FUN **parse_pyproject_toml** `(file_path: Path) -> List[str]` [🔗7]
    *   FUN **parse_package_json** `(file_path: Path) -> List[str]` [🔗7]
    *   FUN **parse_pubspec_yaml** `(file_path: Path) -> List[str]` [🔗7]
    *   FUN **parse_cmake_lists** `(file_path: Path) -> List[str]` [🔗7]
    *   FUN **parse_csproj** `(file_path: Path) -> List[str]` [🔗7]
*   **[parsers.py](src/ndoc/atoms/deps/parsers.py#L1)**
    *   FUN **extract_imports** `(content: str) -> List[str]` [🔗10]
    *   FUN **extract_cpp_includes** `(content: str) -> List[str]` [🔗11]
    *   FUN **extract_dart_imports** `(content: str) -> List[str]` [🔗7]
    *   FUN **extract_csharp_usings** `(content: str) -> List[str]` [🔗7]
*   **[stats.py](src/ndoc/atoms/deps/stats.py#L1)**
    *   VAR **DEFAULT_IGNORE_PATTERNS** ` = {
    '.git', '.vscode', '.idea', '__pycache__', 
    'node_...` [🔗8]
    *   VAR **LANGUAGE_EXTENSIONS** ` = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': '...` [🔗9]
    *   FUN **detect_languages** `(root_path: Path, ignore_patterns: Set[str] = None) -> Dict[str, float]` [🔗7]

## src/ndoc/atoms/langs
*   **[__init__.py](src/ndoc/atoms/langs/__init__.py#L1)**
    *   CLS **LanguageDefinition** [🔗33]
    *   VAR **ID** `: str = ""` [🔗559]
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
    *   FUN **get_lang_id_by_ext** `(ext: str) -> Optional[str]` [🔗7]
    *   FUN **get_all_extensions** `() -> List[str]` [🔗3]
*   **[cpp.py](src/ndoc/atoms/langs/cpp.py#L1)**
    *   CLS **CppDefinition** [🔗3]
    *   VAR **ID** ` = "cpp"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".cpp", ".c", ".h", ".hpp"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_specifier", "struct_specifier"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_specifier
  name: (type_identifier) @name
) @clas...` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(call_expression
  function: [
    (identifier) @call_na...` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(preproc_include) @import
"""` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[csharp.py](src/ndoc/atoms/langs/csharp.py#L1)**
    *   CLS **CSharpDefinition** [🔗3]
    *   VAR **ID** ` = "c_sharp"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".cs"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "struct_declaration", "interface_decla...` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(namespace_declaration
  [(qualified_name) (identifier)]...` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(invocation_expression
  function: [(identifier) (member...` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(using_directive) @import
"""` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[dart.py](src/ndoc/atoms/langs/dart.py#L1)**
    *   CLS **DartDefinition** [🔗3]
    *   VAR **ID** ` = "dart"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".dart"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_definition", "mixin_declaration", "enum_declaration"...` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_definition name: (identifier) @name) @class_def
(...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[go.py](src/ndoc/atoms/langs/go.py#L1)**
    *   CLS **GoDefinition** [🔗3]
    *   VAR **ID** ` = "go"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".go"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["type_declaration", "type_spec"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(type_declaration
  (type_spec
    name: (type_identifie...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[java.py](src/ndoc/atoms/langs/java.py#L1)**
    *   CLS **JavaDefinition** [🔗3]
    *   VAR **ID** ` = "java"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".java"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declara...` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_declaration
  (modifiers)? @visibility
  name: (i...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[javascript.py](src/ndoc/atoms/langs/javascript.py#L1)**
    *   CLS **JavascriptDefinition** [🔗3]
    *   VAR **ID** ` = "javascript"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".js", ".jsx"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_declaration
  name: (identifier) @name
) @class_d...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[python.py](src/ndoc/atoms/langs/python.py#L1)**
    *   CLS **PythonDefinition** [🔗3]
    *   VAR **ID** ` = "python"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".py"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_definition"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_definition
  name: (identifier) @name
  superclas...` [🔗32]
    *   VAR **CALL_QUERY** ` = """
(call
  function: [(identifier) (attribute)] @call_name
...` [🔗13]
    *   VAR **SCM_IMPORTS** ` = """
(import_statement) @import
(import_from_statement) @impo...` [🔗13]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
    *   STA **extract_docstring** `(node: Any, content_bytes: bytes) -> Optional[str]` [🔗14]
    *   STA **format_signature** `(params_text: Optional[str], return_text: Optional[str]) -> str` [🔗8]
*   **[rust.py](src/ndoc/atoms/langs/rust.py#L1)**
    *   CLS **RustDefinition** [🔗3]
    *   VAR **ID** ` = "rust"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".rs"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["struct_item", "trait_item", "impl_item"]` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(struct_item
  (visibility_modifier)? @visibility
  name...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]
*   **[typescript.py](src/ndoc/atoms/langs/typescript.py#L1)**
    *   CLS **TypescriptDefinition** [🔗3]
    *   VAR **ID** ` = "typescript"` [🔗559]
    *   VAR **EXTENSIONS** ` = [".ts", ".tsx"]` [🔗31]
    *   VAR **CLASS_TYPES** ` = ["class_declaration", "interface_declaration", "enum_declara...` [🔗31]
    *   VAR **SCM_QUERY** ` = """
(class_declaration
  name: (type_identifier) @name
) @cl...` [🔗32]
    *   STA **is_public** `(name: str, visibility: str) -> bool` [🔗38]

## src/ndoc/flows
*   **[archive_flow.py](src/ndoc/flows/archive_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[capability_flow.py](src/ndoc/flows/capability_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig, auto_install: bool = True) -> bool` [🔗154]
    *   FUN **check_single_file** `(file_path: Path, auto_install: bool = True)` [🔗6]
*   **[clean_flow.py](src/ndoc/flows/clean_flow.py#L1)**
    *   VAR **GENERATED_FILES** ` = [
    "_AI.md",
    "_MAP.md",
    "_TECH.md",
    "_DEPS.md...` [🔗5]
    *   FUN **run** `(config: ProjectConfig, target: str = None, force: bool = False) -> bool` [🔗154]
*   **[config_flow.py](src/ndoc/flows/config_flow.py#L1)**
    *   VAR **RULES_TEMPLATE** ` = """# Project Rules
> @CONTEXT: Configuration | @TAGS: @CONFI...` [🔗4]
    *   FUN **load_project_config** `(root_path: Path) -> ProjectConfig` [🔗4]
    *   FUN **ensure_rules_file** `(root_path: Path, force: bool = False) -> bool` [🔗5]
*   **[context_flow.py](src/ndoc/flows/context_flow.py#L1)**
    *   FUN **format_file_summary** `(ctx: FileContext, root: Optional[Path] = None) -> str` [🔗4]
    *   FUN **format_symbol_list** `(ctx: FileContext) -> str` [🔗4]
    *   FUN **format_dependencies** `(ctx: FileContext) -> str` [🔗4]
    *   FUN **generate_dir_content** `(context: DirectoryContext) -> str` [🔗4]
    *   FUN **cleanup_legacy_map** `(file_path: Path) -> None` [🔗4]
    *   FUN **process_directory** `(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False) -> Optional[DirectoryContext]` [🔗6]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
    *   FUN **update_directory** `(path: Path, config: ProjectConfig) -> bool` [🔗4]
*   **[data_flow.py](src/ndoc/flows/data_flow.py#L1)**
    *   CLS **DataDefinition** [🔗6]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **type** `: str` [🔗980]
    *   VAR **path** `: str` [🔗446]
    *   VAR **docstring** `: str` [🔗70]
    *   VAR **fields** `: List[str]` [🔗33]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
    *   FUN **get_plural** `(name: str) -> str` [🔗4]
*   **[deps_flow.py](src/ndoc/flows/deps_flow.py#L1)**
    *   FUN **collect_imports** `(root: Path) -> Dict[str, List[str]]` [🔗4]
    *   FUN **build_dependency_graph** `(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]` [🔗4]
    *   FUN **generate_mermaid_graph** `(graph: Dict[str, Set[str]]) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[doctor_flow.py](src/ndoc/flows/doctor_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[init_flow.py](src/ndoc/flows/init_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗154]
*   **[map_flow.py](src/ndoc/flows/map_flow.py#L1)**
    *   CLS **MapContext** [🔗8]
    *   VAR **root** `: Path` [🔗260]
    *   VAR **ignore_patterns** `: List[str]` [🔗62]
    *   FUN **format_dir_entry** `(name: str, level: int) -> str` [🔗4]
    *   FUN **format_file_entry** `(path: Path, root: Path, level: int, summary_cache: Dict[Path, str] = None) -> str` [🔗4]
    *   FUN **extract_file_summary** `(path: Path) -> str` [🔗4]
    *   FUN **build_tree_lines** `(current_path: Path, context: MapContext, level: int = 0, summary_cache: Dict[Path, str] = None) -> List[str]` [🔗5]
    *   FUN **generate_tree_content** `(config: ProjectConfig) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[plan_flow.py](src/ndoc/flows/plan_flow.py#L1)**
    *   VAR **PLAN_SYSTEM_PROMPT** ` = """
You are a senior software architect and project manager....` [🔗4]
    *   FUN **run** `(config: ProjectConfig, objective: str) -> bool` [🔗154]
*   **[prompt_flow.py](src/ndoc/flows/prompt_flow.py#L1)**
    *   VAR **RULE_MARKER** ` = "## !RULE"` [🔗3]
    *   VAR **CTX_START** ` = "<!-- NIKI_CTX_START -->"` [🔗3]
    *   FUN **extract_rules_from_ai** `(ai_path: Path) -> str` [🔗6]
    *   FUN **get_context_prompt** `(file_path: Path, config: ProjectConfig) -> str` [🔗5]
    *   FUN **run** `(file_path: str, config: ProjectConfig) -> bool` [🔗154]
*   **[stats_flow.py](src/ndoc/flows/stats_flow.py#L1)**
    *   FUN **check_should_update** `(root_path: Path, force: bool) -> bool` [🔗4]
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗154]
*   **[symbols_flow.py](src/ndoc/flows/symbols_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[syntax_flow.py](src/ndoc/flows/syntax_flow.py#L1)**
    *   VAR **SYNTAX_TEMPLATE** ` = r"""# PROJECT SYNTAX
> @CONTEXT: DSL 定义 | @TAGS: @SYNTAX @OP...` [🔗4]
    *   FUN **run** `(config: ProjectConfig, force: bool = False) -> bool` [🔗154]
*   **[tech_flow.py](src/ndoc/flows/tech_flow.py#L1)**
    *   FUN **generate_tech_content** `(config: ProjectConfig) -> str` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[todo_flow.py](src/ndoc/flows/todo_flow.py#L1)**
    *   CLS **TodoItem** [🔗14]
    *   VAR **file_path** `: Path` [🔗181]
    *   VAR **line** `: int` [🔗336]
    *   VAR **type** `: str` [🔗980]
    *   VAR **content** `: str` [🔗401]
    *   VAR **task_id** `: Optional[str] = None` [🔗19]
    *   PRP **priority_icon** `(self) -> str` [🔗4]
    *   FUN **collect_todos** `(root: Path, ignore_patterns: List[str]) -> List[TodoItem]` [🔗4]
    *   FUN **format_todo_lines** `(todos: List[TodoItem], root: Path) -> str` [🔗4]
    *   FUN **sync_tasks** `(config: ProjectConfig, todos: List[TodoItem]) -> bool` [🔗4]
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]
*   **[update_flow.py](src/ndoc/flows/update_flow.py#L1)**
    *   FUN **run** `() -> bool` [🔗154]
*   **[verify_flow.py](src/ndoc/flows/verify_flow.py#L1)**
    *   FUN **run** `(config: ProjectConfig) -> bool` [🔗154]

## src/ndoc/models
*   **[config.py](src/ndoc/models/config.py#L1)**
    *   CLS **ScanConfig** [🔗17]
    *   VAR **root_path** `: Path` [🔗114]
    *   VAR **ignore_patterns** `: List[str] = field(default_factory=lambda: [
        ".git",
        "__p...` [🔗62]
    *   VAR **extensions** `: List[str] = field(default_factory=list)` [🔗75]
    *   CLS **ProjectConfig** [🔗118]
    *   VAR **scan** `: ScanConfig` [🔗79]
    *   VAR **name** `: str = "Project"` [🔗1428]
    *   VAR **version** `: str = "0.1.0"` [🔗204]
*   **[context.py](src/ndoc/models/context.py#L1)**
    *   CLS **Tag** [🔗39]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **args** `: List[str] = field(default_factory=list)` [🔗109]
    *   VAR **line** `: int = 0` [🔗336]
    *   VAR **raw** `: str = ""` [🔗36]
    *   CLS **Section** [🔗23]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **content** `: str` [🔗401]
    *   VAR **raw** `: str` [🔗36]
    *   VAR **start_pos** `: int` [🔗5]
    *   VAR **end_pos** `: int` [🔗4]
    *   CLS **Symbol** [🔗74]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **kind** `: str` [🔗143]
    *   VAR **line** `: int` [🔗336]
    *   VAR **docstring** `: Optional[str] = None` [🔗70]
    *   VAR **signature** `: Optional[str] = None` [🔗36]
    *   VAR **parent** `: Optional[str] = None` [🔗183]
    *   VAR **is_core** `: bool = False` [🔗21]
    *   VAR **visibility** `: str = "public"` [🔗121]
    *   VAR **lang** `: str = "unknown"` [🔗59]
    *   VAR **decorators** `: List[str] = field(default_factory=list)` [🔗9]
    *   VAR **bases** `: List[str] = field(default_factory=list)` [🔗18]
    *   VAR **full_content** `: str = ""` [🔗6]
    *   VAR **path** `: Optional[str] = None` [🔗446]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗52]
    *   PRP **is_public** `(self) -> bool` [🔗38]
    *   CLS **FileContext** [🔗21]
    *   VAR **path** `: Path` [🔗446]
    *   VAR **rel_path** `: str` [🔗34]
    *   VAR **content** `: Optional[str] = None` [🔗401]
    *   VAR **tags** `: List[Tag] = field(default_factory=list)` [🔗52]
    *   VAR **sections** `: Dict[str, Section] = field(default_factory=dict)` [🔗59]
    *   VAR **symbols** `: List[Symbol] = field(default_factory=list)` [🔗129]
    *   VAR **docstring** `: Optional[str] = None` [🔗70]
    *   VAR **description** `: Optional[str] = None` [🔗56]
    *   VAR **is_core** `: bool = False` [🔗21]
    *   VAR **memories** `: List[Dict[str, Any]] = field(default_factory=list)` [🔗24]
    *   VAR **ast_tree** `: Any = None` [🔗3]
    *   VAR **title** `: Optional[str] = None` [🔗311]
    *   VAR **description** `: Optional[str] = None` [🔗56]
    *   PRP **has_content** `(self) -> bool` [🔗7]
    *   CLS **DirectoryContext** [🔗12]
    *   VAR **path** `: Path` [🔗446]
    *   VAR **files** `: List[FileContext] = field(default_factory=list)` [🔗306]
    *   VAR **subdirs** `: List[Path] = field(default_factory=list)` [🔗18]
    *   PRP **name** `(self) -> str` [🔗1428]

## tests
*   **[conftest.py](tests/conftest.py#L1)**
    *   VAR **root** ` = Path(__file__).parent.parent` [🔗260]
*   **[test_ast.py](tests/test_ast.py#L1)**
    *   VAR **SAMPLE_CODE** ` = """
class MyClass:
    '''Class Docstring'''
    
    def me...` [🔗5]
    *   FUN **test_extract_symbols_basic** `()` [🔗3]
    *   FUN **test_extract_complex_api** `()` [🔗3]
    *   FUN **find_sym** `(name)` [🔗7]
    *   FUN **find_member** `(cls_name, name)` [🔗6]
*   **[test_capabilities.py](tests/test_capabilities.py#L1)**
    *   CLS **TestCapabilityManager** [🔗3]
    *   MET **test_get_language_installed** `(self)` [🔗3]
    *   MET **test_try_import_python** `(self)` [🔗3]
    *   MET **test_try_import_unknown** `(self)` [🔗3]
*   **[test_capability_flow.py](tests/test_capability_flow.py#L1)**
    *   CLS **TestCapabilityFlow** [🔗3]
    *   MET **setUp** `(self)` [🔗3]
    *   MET **test_run_detects_languages** `(self, mock_ensure, mock_walk)` [🔗3]
    *   MET **test_check_single_file** `(self, mock_ensure)` [🔗3]
    *   MET **test_check_single_file_unknown** `(self, mock_ensure)` [🔗3]
*   **[test_csharp_api.py](tests/test_csharp_api.py#L1)**
    *   FUN **test_csharp_extraction** `()` [🔗4]
*   **[test_lsp_server.py](tests/test_lsp_server.py#L1)**
    *   FUN **log** `(msg)` [🔗31]
    *   FUN **read_stream** `(stream, name)` [🔗5]
    *   FUN **test_lsp** `()` [🔗4]
*   **[test_scanner.py](tests/test_scanner.py#L1)**
    *   VAR **SAMPLE_CONTENT** ` = """
# @TAG arg1 arg2
<!-- NIKI_TEST_START -->
Some Content
<...` [🔗4]
    *   FUN **test_scan_file_content_mixed** `()` [🔗3]
    *   FUN **test_scan_file_content_text_only** `()` [🔗3]

## tests/fixtures
*   **[complex_api.py](tests/fixtures/complex_api.py#L1)**
    *   CLS **User** [🔗17]
    *   VAR **name** `: str` [🔗1428]
    *   VAR **age** `: int = 18` [🔗6]
    *   PRP **is_adult** `(self) -> bool` [🔗3]
    *   ASY **fetch_data** `(self) -> dict` [🔗4]
    *   CLM **from_dict** `(cls, data: dict) -> "User"` [🔗7]
    *   CLS **Database** [🔗6]
    *   VAR **connection_string** `: str = "localhost:5432"` [🔗3]
    *   MET **connect** `(self)` [🔗11]
    *   FUN **global_func** `(x: int, y: int) -> int` [🔗5]
    *   ASY **global_async_func** `()` [🔗4]
