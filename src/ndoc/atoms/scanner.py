"""
Atoms: Content Scanner.
原子能力：内容扫描器。
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Pattern, Dict, Any, Iterator
from pathlib import Path
from ..models.context import Tag, Section, Symbol
from ..atoms.ast import parse_code, extract_symbols
from ..atoms import cache

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
    todos: List[dict] = field(default_factory=list)  # New: Captured TODOs
    is_core: bool = False # Whether file is marked as @CORE


# --- Global Cache ---
_CACHE: Optional[cache.FileCache] = None

def get_cache(root: Path) -> cache.FileCache:
    global _CACHE
    if _CACHE is None:
        cache_dir = root / ".ndoc" / "cache"
        _CACHE = cache.FileCache(cache_dir)
    return _CACHE

# --- Core Logic ---

def scan_file(file_path: Path, root: Path) -> ScanResult:
    """
    扫描单个文件，支持缓存 (Scan single file with cache support).
    """
    c = get_cache(root)
    if not c.is_changed(file_path):
        cached_data = c.get(file_path)
        if cached_data:
            # Reconstruct ScanResult from dict
            # This is a bit tedious with nested objects, 
            # for now let's just return a fresh scan if cache fails to deserialize perfectly
            try:
                # Basic reconstruction for tags and symbols
                tags = [Tag(**t) for t in cached_data.get('tags', [])]
                symbols = [Symbol(**s) for s in cached_data.get('symbols', [])]
                sections = {k: Section(**v) for k, v in cached_data.get('sections', {}).items()}
                
                return ScanResult(
                    tags=tags,
                    sections=sections,
                    symbols=symbols,
                    docstring=cached_data.get('docstring', ""),
                    summary=cached_data.get('summary', ""),
                    todos=cached_data.get('todos', []),
                    is_core=cached_data.get('is_core', False)
                )
            except Exception:
                pass

    # Perform fresh scan
    from ..atoms import io
    content = io.read_text(file_path)
    if content is None:
        return ScanResult()
        
    result = scan_file_content(content, file_path)
    
    # Save to cache
    # Convert result to dict for JSON serialization
    cache_data = {
        'tags': [vars(t) for t in result.tags],
        'sections': {k: vars(v) for k, v in result.sections.items()},
        'symbols': [vars(s) for s in result.symbols],
        'docstring': result.docstring,
        'summary': result.summary,
        'todos': result.todos,
        'is_core': result.is_core
    }
    c.update(file_path, cache_data)
    c.save()
    
    return result


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


def extract_docstring(content: str) -> str:
    """
    提取文件顶部的 Docstring.
    Supports Python (\"\"\" or \'\'\'), JS/C (/** ... */ or /* ... */), and C++ (///).
    """
    subset = content[:2000].strip()  # Optimization: only check header
    
    # 1. Python style
    for pattern in DOCSTRING_PATTERNS:
        match = pattern.search(subset)
        if match:
            return match.group(1).strip()
    
    # 2. JS/C-style Block Comment (JSDoc / Doxygen)
    if subset.startswith('/**') or subset.startswith('/*'):
        end_idx = subset.find('*/')
        if end_idx != -1:
            raw = subset[:end_idx+2]
            # Clean JSDoc / Doxygen
            if raw.startswith('/**'):
                lines = raw[3:-2].split('\n')
                cleaned = [line.strip().lstrip('*').strip() for line in lines]
                return "\n".join(cleaned).strip()
            else:
                return raw[2:-2].strip()

    # 3. C++ style Triple-Slash (Doxygen)
    if subset.startswith('///'):
        lines = []
        for line in subset.split('\n'):
            line = line.strip()
            if line.startswith('///'):
                lines.append(line[3:].strip())
            elif not line:
                continue
            else:
                break
        return "\n".join(lines).strip()

    return ""


# 1. Tags: @TAG or !TAG
# Matches: # @TAG args, // @TAG args, <!-- @TAG args -->, > @TAG args
TAG_REGEX = re.compile(
    r"^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$",
    re.MULTILINE,
)

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
    Implementation: Generator Pipeline.
    """

    def _extract_args(args_str: Optional[str]) -> List[str]:
        if not args_str:
            return []
        return [a.strip() for a in args_str.split() if a.strip()]

    tags = []
    for match in TAG_REGEX.finditer(content):
        name = match.group(1)
        args_str = match.group(2)
        raw = match.group(0).strip()

        # Calculate line number (Performance note: this is O(N) per match, acceptable for small files)
        line_number = content.count("\n", 0, match.start()) + 1

        tags.append(
            Tag(name=name, args=_extract_args(args_str), line=line_number, raw=raw)
        )
    return tags


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


def regex_scan(content: str, ext: str) -> List[Symbol]:
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
            symbols.append(Symbol(name=name, kind=kind, line=line))
            
    return symbols


def scan_file_content(content: str, file_path: Optional[Path] = None) -> ScanResult:
    """
    全量扫描文件内容 (Full scan of file content).
    Implementation: Parallel extraction pipeline.
    """
    # 1. Generic Text Analysis (Regex)
    tags = parse_tags(content)
    sections = parse_sections(content)
    docstring = extract_docstring(content)
    summary = extract_summary(content, docstring)
    todos = extract_todos(content)
    
    # 2. Structural Analysis (AST) - Optional
    symbols = []
    # Now supports multiple languages, let ast.py decide based on extension
    if file_path:
        tree = None
        try:
            tree = parse_code(content, file_path)
        except Exception as e:
            print(f"AST Parse Error in {file_path}: {e}")
            pass
            
        if tree:
            try:
                symbols = extract_symbols(tree, content.encode("utf-8"), file_path)
            except Exception as e:
                print(f"AST Extraction Error in {file_path}: {e}")
                pass
        
        # Fallback to Regex if AST failed or returned nothing (and it's a target language)
        if not symbols:
            ext = file_path.suffix.lower()
            if ext in ('.dart', '.fbs'):
                symbols = regex_scan(content, ext)

    # 3. Finalize
    is_core = any(t.name == "@CORE" for t in tags) or "@CORE" in docstring
    
    # Mark symbols as core if they have @CORE in their docstring
    for sym in symbols:
        if sym.docstring and "@CORE" in sym.docstring:
            sym.is_core = True

    return ScanResult(
        tags=tags,
        sections=sections,
        symbols=symbols,
        docstring=docstring,
        summary=summary,
        todos=todos,
        is_core=is_core
    )
