# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# *   **Enhanced Symbol Context**: `scanner.py` 在重建缓存符号时必须确保 `path` 属性被正确填充，否则会导致下游 CLI 工具 (如 `lsp` 指令) 在解析相对路径时崩溃。
# *   **LSP Service Hotness**: `lsp.py` 提供轻量级引用计数。该计数基于全局词频统计，虽然不是 100% 精确的定义引用，但在大规模 codebase 中能有效反映符号的“热度”和影响力。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Content Scanner.
原子能力：内容扫描器。
"""

import re
import os
import concurrent.futures
from dataclasses import dataclass, field
from typing import List, Optional, Pattern, Dict, Any, Tuple
from pathlib import Path
from ..models.symbol import Tag, Symbol
from ..models.context import Section
from .ast import parse_code, extract_symbols
from ..brain import cache
from ..core.text_utils import clean_docstring, extract_tags_from_text
from . import universal # Import universal parser

# --- Data Structures (Logic as Data) ---


@dataclass
class TokenRule:
    """
    词法分析规则 (Lexical Analysis Rule).
    """

    name: str
    pattern: Pattern
    group_map: Dict[str, int]  # Map logical names to regex groups


@dataclass
class ScanResult:
    """
    扫描结果 (Scan Result).
    """

    tags: List[Tag] = field(default_factory=list)
    sections: Dict[str, Section] = field(default_factory=dict)
    symbols: List[Symbol] = field(default_factory=list)
    docstring: str = ""
    summary: str = ""
    todos: List[dict] = field(default_factory=list)  # Captured TODOs
    memories: List[dict] = field(default_factory=list) # Captured Memories (!RULE, !WARN)
    decisions: List[dict] = field(default_factory=list) # Captured @DECISION
    intents: List[str] = field(default_factory=list) # Captured @INTENT
    lessons: List[dict] = field(default_factory=list) # Captured @LESSON
    calls: List[str] = field(default_factory=list)  # Captured calls
    imports: List[str] = field(default_factory=list)  # Captured imports
    tokens: Dict[str, int] = field(default_factory=dict) # Token frequency map for LSP
    is_core: bool = False # Whether file is marked as @CORE


# --- Global Cache ---
_CACHE: Optional[cache.FileCache] = None

def get_cache(root: Path, cache_dir: Path = None) -> cache.FileCache:
    global _CACHE
    if cache_dir is None:
        # Use a new cache directory to avoid locks on the old one
        cache_dir = root / ".ndoc" / "cache_v2"
        
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Warning: Failed to create cache directory {cache_dir}: {e}")
        return None
    
    # Use global cache instance
    if _CACHE is None or getattr(_CACHE, 'cache_dir', None) != cache_dir:
        from ..brain import cache
        try:
            # Rotate DB name to avoid I/O locks during dev
            _CACHE = cache.FileCache(cache_dir, db_name="ndoc_cache.db")
        except Exception as e:
            print(f"Warning: Failed to initialize cache: {e}")
            return None
        
    return _CACHE

# --- Helper Functions for Parallel Execution ---

def _reconstruct_result(cached_data: dict, file_path: Path) -> ScanResult:
    """Helper to reconstruct ScanResult from cached dict."""
    tags = [Tag(**t) for t in cached_data.get('tags', []) if isinstance(t, dict)]
    symbols = []
    for s in cached_data.get('symbols', []):
        if isinstance(s, dict):
            # Ensure path is set even if not in cache
            if 'path' not in s or not s['path']:
                s['path'] = str(file_path)
            symbols.append(Symbol(**s))
    sections = {k: Section(**v) for k, v in cached_data.get('sections', {}).items() if isinstance(v, dict)}
    
    return ScanResult(
        tags=tags,
        sections=sections,
        symbols=symbols,
        docstring=cached_data.get('docstring', ""),
        summary=cached_data.get('summary', ""),
        todos=cached_data.get('todos', []),
        memories=cached_data.get('memories', []),
        decisions=cached_data.get('decisions', []),
        intents=cached_data.get('intents', []),
        lessons=cached_data.get('lessons', []),
        calls=cached_data.get('calls', []),
        imports=cached_data.get('imports', []),
        tokens=cached_data.get('tokens', {}),
        is_core=cached_data.get('is_core', False)
    )

def _scan_worker(args: Tuple[Path, Path]) -> Tuple[Path, Optional[dict]]:
    """
    Worker function for parallel scanning.
    Args:
        args: Tuple of (file_path: Path, root: Path)
    Returns:
        Tuple[Path, Optional[dict]]: (file_path, serialized_scan_result)
    """
    file_path, root = args
    try:
        # Avoid circular imports inside worker
        from ..core import io
        content = io.read_text(file_path)
        if content is None:
            return file_path, None
            
        # Perform fresh scan (CPU intensive)
        # Note: scan_file_content is defined in this module
        result = scan_file_content(content, file_path)
        
        # Serialize immediately
        cache_data = {
            'tags': [vars(t) for t in result.tags],
            'sections': {k: vars(v) for k, v in result.sections.items()},
            'symbols': [vars(s) for s in result.symbols],
            'docstring': result.docstring,
            'summary': result.summary,
            'todos': result.todos,
            'memories': result.memories,
            'decisions': result.decisions,
            'intents': result.intents,
            'lessons': result.lessons,
            'calls': result.calls,
            'imports': result.imports,
            'tokens': result.tokens,
            'is_core': result.is_core
        }
        return file_path, cache_data
    except Exception as e:
        # In case of worker failure, LOG IT and return None
        # We use print here because logging might not be configured in worker process
        print(f"❌ [Worker Error] Failed to scan {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return file_path, None

def scan_project(root: Path, ignore_patterns: List[str] = None) -> Dict[Path, ScanResult]:
    """
    Scan the entire project (High-level API) with Parallel Execution.
    """
    from ..core import fs
    
    # Phase 1: Check Cache (Main Process)
    c = get_cache(root)
    results = {}
    
    if ignore_patterns is None:
        ignore_patterns = []
        
    all_files = list(fs.walk_files(root, ignore_patterns))
    tasks = []
    
    # 1. Check Cache (Main Process)
    # Skipped in debug to avoid DB locks
    for file_path in all_files:
        # Cache Miss: Add to tasks
        tasks.append((file_path, root))
        
    # Phase 1.5: Ensure Languages (Main Process)
    # Detect required languages to trigger auto-build BEFORE parallel execution
    from .langs import get_lang_id_by_ext
    from ..core.capabilities import CapabilityManager
    
    needed_langs = set()
    for file_path in all_files:
        lang = get_lang_id_by_ext(file_path.suffix.lower())
        if lang:
            needed_langs.add(lang)
            
    if needed_langs:
        # Trigger capability check/build in main process
        # We iterate to allow individual handling (e.g. Dart native build)
        for lang in needed_langs:
            CapabilityManager.get_language(lang, auto_install=True)

    # Phase 2: Parallel Scanning
    # If workers=1, run sequential (easier for debugging)
    if tasks:
        # Use ProcessPoolExecutor
        # Max workers = CPU count (default) or 4 minimum
        max_workers = os.cpu_count() or 4
        
        # We use map to keep order, though not strictly required
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_results = executor.map(_scan_worker, tasks)
            
            for file_path, cache_data in future_results:
                if cache_data:
                    # Update Cache (Main Process)
                    if c:
                        c.update(file_path, cache_data)
                    # Reconstruct Result
                    results[file_path] = _reconstruct_result(cache_data, file_path)
                else:
                    # Failed scan
                    results[file_path] = ScanResult()

    # 3. Save Cache (Main Process)
    if c:
        c.save()
            
    return results

# --- Core Logic ---

def scan_file(file_path: Path, root: Path, force: bool = False) -> ScanResult:
    """
    扫描单个文件，支持缓存 (Scan single file with cache support).
    """
    c = get_cache(root)
    if c and not force and not c.is_changed(file_path):
        cached_data = c.get(file_path)
        if cached_data:
            try:
                return _reconstruct_result(cached_data, file_path)
            except Exception:
                pass

    # Perform fresh scan (Synchronous reuse of worker logic)
    _, cache_data = _scan_worker((file_path, root))
    
    if cache_data:
        if c:
            c.update(file_path, cache_data)
            c.save()
        return _reconstruct_result(cache_data, file_path)
        
    return ScanResult()


def extract_todos(content: str) -> List[dict]:
    """
    提取 TODO/FIXME 等标记.
    Capture groups: (Marker, TaskID?, Priority/Content)
    Returns: List of dict(line, type, task_id, content)
    """
    todos = []
    # Pattern: (comment_char) (whitespace) (MARKER) ( (task_id)? ) (colon?) (whitespace) (content)
    # Example: // TODO(#task-123): fix this
    pattern = re.compile(
        r"^\s*(?:#|//|<!--)\s*(TODO|FIXME|XXX|HACK|NOTE|DONE)\b(?:\(#([\w-]+)\))?:?\s*(.*)$", re.MULTILINE
    )

    for match in pattern.finditer(content):
        # Calculate line number
        start_index = match.start()
        line_num = content.count("\n", 0, start_index) + 1

        marker = match.group(1)
        task_id = match.group(2)
        text = match.group(3).strip()

        todos.append({
            "line": line_num, 
            "type": marker, 
            "task_id": task_id,
            "content": text
        })
    return todos


def extract_memories(content: str) -> List[dict]:
    """
    提取 !RULE / !WARN / !INTENT 等记忆标记.
    Capture groups: (Marker, Content)
    Returns: List of dict(line, type, content)
    """
    memories = []
    # Pattern: (comment_char) (whitespace) (!MARKER) (colon?) (whitespace) (content)
    # Example: // !RULE: content
    # Markers: !RULE, !WARN, !INTENT
    pattern = re.compile(
        r"^\s*(?:#|//|<!--)\s*!(RULE|WARN|INTENT):?\s*(.*)$", re.MULTILINE
    )

    for match in pattern.finditer(content):
        start_index = match.start()
        line_num = content.count("\n", 0, start_index) + 1
        
        marker = match.group(1)
        text = match.group(2).strip()
        
        memories.append({
            "line": line_num,
            "type": marker,
            "content": text
        })
    return memories



def extract_docstring(content: str) -> str:
    """
    提取文件顶部的 Docstring (Extract file-level docstring).
    Supports:
    - Python/Ruby/Shell (# comments)
    - Python/JS/Dart (Block comments or Triple quotes)
    - C++/Dart/Rust (/// or // comments)
    """
    subset = content[:2000].strip()  # Optimization: only check header
    if not subset:
        return ""

    # 1. Check for Triple Quotes (Python/JS/Dart)
    for pattern in DOCSTRING_PATTERNS:
        match = pattern.search(subset)
        if match:
            return clean_docstring(match.group(0))

    # 2. Check for Block Comments (/** ... */ or /* ... */)
    if subset.startswith('/*'):
        end_idx = subset.find('*/')
        if end_idx != -1:
            return clean_docstring(subset[:end_idx+2])

    # 3. Check for Line Comments (///, //, or #)
    lines = subset.split('\n')
    doc_lines = []
    
    # Identify the comment style of the first line
    first_line = lines[0].strip()
    comment_prefix = None
    if first_line.startswith('///'):
        comment_prefix = '///'
    elif first_line.startswith('//'):
        comment_prefix = '//'
    elif first_line.startswith('#'):
        # Skip shebang
        if first_line.startswith('#!'):
            if len(lines) > 1:
                lines = lines[1:]
                first_line = lines[0].strip()
                if first_line.startswith('#'):
                    comment_prefix = '#'
        else:
            comment_prefix = '#'
            
    if comment_prefix:
        for line in lines:
            line = line.strip()
            if line.startswith(comment_prefix):
                doc_lines.append(line[len(comment_prefix):].strip())
            elif not line:
                continue
            else:
                break
        return "\n".join(doc_lines).strip()

    return ""


# 2. Sections: <!-- NIKI_NAME_START --> ... <!-- NIKI_NAME_END -->
# Group 1: Name (e.g. MAP)
# Group 2: Content
SECTION_REGEX = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->", re.DOTALL
)

# 3. Docstrings: """...""" or '''...'''
DOCSTRING_PATTERNS = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.compile(r"^\s*'''(.*?)'''", re.DOTALL),
]

# --- Engine (Pipeline) ---


def parse_tags(content: str) -> List[Tag]:
    """
    从内容中提取标签 (Extract tags from content).
    Uses utility function for consistency.
    """
    return extract_tags_from_text(content)


def parse_sections(content: str) -> Dict[str, Section]:
    """
    提取被标记包裹的片段 (Extract marked sections).
    Pattern: <!-- NIKI_XXX_START --> ... <!-- NIKI_XXX_END -->
    """
    sections = {}
    for match in SECTION_REGEX.finditer(content):
        name = match.group(1)
        inner_content = match.group(2)

        sections[name] = Section(
            name=name,
            content=inner_content,  # Keep raw content including newlines
            raw=match.group(0),
            start_pos=match.start(),
            end_pos=match.end(),
        )
    return sections


def extract_summary(content: str, docstring: str) -> str:
    """
    提取文件摘要 (Extract summary).
    Priority:
    1. @SUMMARY tag
    2. Docstring first line
    3. Empty
    """
    # 1. @SUMMARY tag
    # Use simple regex for this specific tag to avoid full parse overhead if called independently
    match = re.search(
        r"^\s*(?:#+|//|<!--|>)?\s*@SUMMARY\s+(.*?)$", content, re.MULTILINE
    )
    if match:
        return match.group(1).strip()

    # 2. Docstring first line
    if docstring:
        lines = docstring.strip().split("\n")
        if lines:
            return lines[0].strip()

    return ""


def extract_special_comments(content: str) -> Dict[str, List[Any]]:
    """
    Extract special comments like TODO, @DECISION, @INTENT, @LESSON.
    """
    todos = []
    memories = [] # !RULE, !WARN
    decisions = []
    intents = []
    lessons = []
    
    # 1. TODOs
    todo_pattern = re.compile(r"^\s*(?:#+|//|<!--)\s*(TODO|FIXME|HACK|NOTE|XXX)\s*:?\s*(.*?)$", re.MULTILINE | re.IGNORECASE)
    for match in todo_pattern.finditer(content):
        tag = match.group(1).upper()
        text = match.group(2).strip()
        line = content[:match.start()].count('\n') + 1
        todos.append({"tag": tag, "content": text, "line": line})

    # 2. Memories (!RULE, !WARN) - Extracted via parse_tags usually, but we want line context
    # Actually parse_tags handles !RULE. But here we want content text.
    # Let's rely on standard tag extraction for !RULE.

    # 3. Decisions (@DECISION)
    decision_pattern = re.compile(r"^\s*(?:#+|//|<!--)\s*@DECISION\s*:?\s*(.*?)$", re.MULTILINE)
    for match in decision_pattern.finditer(content):
        text = match.group(1).strip()
        line = content[:match.start()].count('\n') + 1
        decisions.append({"content": text, "line": line})

    # 4. Intents (@INTENT)
    intent_pattern = re.compile(r"^\s*(?:#+|//|<!--)\s*@INTENT\s*:?\s*(.*?)$", re.MULTILINE)
    for match in intent_pattern.finditer(content):
        text = match.group(1).strip()
        # Intent is usually a keyword or short phrase
        intents.append(text)

    # 5. Lessons (@LESSON)
    lesson_pattern = re.compile(r"^\s*(?:#+|//|<!--)\s*@LESSON\s*:?\s*(.*?)$", re.MULTILINE)
    for match in lesson_pattern.finditer(content):
        text = match.group(1).strip()
        line = content[:match.start()].count('\n') + 1
        lessons.append({"content": text, "line": line})

    return {
        "todos": todos,
        "decisions": decisions,
        "intents": intents,
        "lessons": lessons
    }


def regex_scan(content: str, ext: str, file_path: Optional[Path] = None) -> List[Symbol]:
    """
    Fallback regex scanner for unsupported languages (FlatBuffers).
    AST based languages are handled in scan_file_content.
    """
    symbols = []
    
    if ext == '.fbs':
        # table/struct/enum Name
        for m in re.finditer(r'^\s*(table|struct|enum)\s+(\w+)', content, re.MULTILINE):
            kind = m.group(1)
            name = m.group(2)
            line = content[:m.start()].count('\n') + 1
            symbols.append(Symbol(name=name, kind=kind, line=line, path=str(file_path) if file_path else None))
            
    elif ext == '.dart':
        # class/mixin Name
        # Support abstract class
        for m in re.finditer(r'^\s*(?:abstract\s+)?(class|mixin|enum)\s+(\w+)', content, re.MULTILINE):
            kind = m.group(1)
            name = m.group(2)
            line = content[:m.start()].count('\n') + 1
            symbols.append(Symbol(name=name, kind=kind, line=line, path=str(file_path) if file_path else None))
            
    return symbols


def scan_file_content(content: str, path: Path) -> ScanResult:
    """
    Scan file content in-memory.
    Uses AST parsing and Text extraction.
    """
    result = ScanResult()
    
    # 1. AST Parsing (Symbols & Structure)
    # This now handles C++, Dart, Python, etc. via Tree-sitter
    tree = parse_code(content, path)
    if tree:
        # Use new API: extract_symbols(tree, content_bytes, path) -> List[Symbol]
        result.symbols = extract_symbols(tree, bytes(content, "utf8"), path)
    else:
        # Fallback regex scan for supported languages (FlatBuffers)
        result.symbols = regex_scan(content, path.suffix.lower(), path)

    # Extract File-level Docstring
    result.docstring = extract_docstring(content)
    
    # 2. Extract Imports (Universal Adapter)
    # Use universal.extract_imports to support multi-language dependency extraction
    result.imports = sorted(list(universal.extract_imports(content, path)))

    # 3. Text Processing (Tags, Todos, Memories)
    # ... (Keep existing text processing logic)
    
    # Extract tags (e.g. @API, !RULE)
    # Note: text_utils.extract_tags_from_text is regex based, works for comments in any language
    # providing they use standard comment markers or just appear in text.
    tags = extract_tags_from_text(content)
    result.tags = tags
    
    # Check for @CORE tag
    for tag in tags:
        if tag.name == '@CORE':
            result.is_core = True
            break
            
    # Extract TODOs
    # Simple regex for TODOs
    # TODO: Move to text_utils or dedicated todo parser
    # Format: TODO: ... or FIXME: ...
    # We can use a simple regex for now
    todo_pattern = re.compile(r"(?i)\b(TODO|FIXME|XXX|HACK|NOTE)\b[:\s]*(.*)")
    for i, line in enumerate(content.splitlines()):
        match = todo_pattern.search(line)
        if match:
            kind, text = match.groups()
            result.todos.append({
                'line': i + 1,
                'type': kind.upper(),
                'content': text.strip()
            })
            
    # Extract Memories (!RULE, !WARN)
    # Format: !RULE: ...
    rule_pattern = re.compile(r"(?i)\b!(RULE|WARN|CONST|LIMIT)\b[:\s]*(.*)")
    for i, line in enumerate(content.splitlines()):
        match = rule_pattern.search(line)
        if match:
            kind, text = match.groups()
            result.memories.append({
                'line': i + 1,
                'type': kind.upper(),
                'content': text.strip()
            })

    return result
