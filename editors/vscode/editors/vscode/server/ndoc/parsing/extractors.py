# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# - DOD Architecture: `scanner.py` (Engine) MUST NOT contain business logic. It delegates to `extractors.py` (Pure Logi...
# - Pure Extractors: Functions in `extractors.py` must be pure (no side effects, no I/O).
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Pure Logic Extractors.
纯逻辑提取器 (无副作用，无 IO).
"""
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..models.scan import ScanResult
from ..models.symbol import Tag, Symbol
from ..models.context import Section
from ..core.text_utils import clean_docstring, extract_tags_from_text
from .ast import parse_code, extract_symbols
from . import universal

# --- Regex Patterns ---

# Group 1: Name (e.g. MAP)
# Group 2: Content
SECTION_REGEX = re.compile(
    r"<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->", re.DOTALL
)

# Docstrings: """...""" or '''...'''
DOCSTRING_PATTERNS = [
    re.compile(r'^\s*"""(.*?)"""', re.DOTALL),
    re.compile(r"^\s*'''(.*?)'''", re.DOTALL),
]

# --- Extractor Functions ---

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
    tree = parse_code(content, path)
    if tree:
        # Use new API: extract_symbols(tree, content_bytes, path) -> List[Symbol]
        result.symbols = extract_symbols(tree, bytes(content, "utf8"), path)
    else:
        # Fallback regex scan
        result.symbols = regex_scan(content, path.suffix.lower(), path)

    # Extract File-level Docstring
    result.docstring = extract_docstring(content)
    
    # 2. Extract Imports (Universal Adapter)
    result.imports = sorted(list(universal.extract_imports(content, path)))

    # 3. Text Processing (Tags, Todos, Memories)
    tags = extract_tags_from_text(content)
    result.tags = tags
    
    # Extract sections (<!-- NIKI_XXX_START -->)
    result.sections = parse_sections(content)
    
    # Check for @CORE tag
    for tag in tags:
        if tag.name == '@CORE':
            result.is_core = True
            break
            
    # Extract TODOs
    # Re-using regex for simplicity in this flow, or could use extract_todos()
    # The original implementation used a local loop. Let's reuse extract_todos!
    todos_list = extract_todos(content)
    result.todos = todos_list
            
    # Extract Memories (!RULE, !WARN)
    # Reuse extract_memories
    memories_list = extract_memories(content)
    result.memories = memories_list
    
    # Extract Special Comments
    specials = extract_special_comments(content)
    # Merge if not already covered
    # extract_special_comments also extracts TODOs, but extract_todos is more specific/robust?
    # Actually extract_special_comments has TODOs too.
    # But let's stick to what we extracted.
    result.decisions = specials['decisions']
    result.intents = specials['intents']
    result.lessons = specials['lessons']
    
    # Summary
    result.summary = extract_summary(content, result.docstring)

    return result
