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

# --- Core Logic ---

def extract_todos(content: str) -> List[dict]:
    """
    提取 TODO/FIXME 等标记.
    Capture groups: (Marker, Priority/Content)
    Returns: List of dict(line, type, content)
    """
    todos = []
    # Pattern: (comment_char) (whitespace) (MARKER) (colon?) (whitespace) (content)
    # Markers: TODO, FIXME, XXX, HACK, NOTE
    # Case-insensitive for markers? Let's stick to upper case for convention, or loose.
    # Let's use strict upper case to avoid false positives in normal text.
    pattern = re.compile(r'^\s*(?:#|//|<!--)\s*(TODO|FIXME|XXX|HACK|NOTE)\b:?\s*(.*)$', re.MULTILINE)
    
    for match in pattern.finditer(content):
        # Calculate line number
        start_index = match.start()
        line_num = content.count('\n', 0, start_index) + 1
        
        marker = match.group(1)
        text = match.group(2).strip()
        
        todos.append({
            "line": line_num,
            "type": marker,
            "content": text
        })
    return todos

def extract_docstring(content: str) -> str:
    """
    提取文件顶部的 Docstring.
    """
    subset = content[:2000] # Optimization: only check header
    for pattern in DOCSTRING_PATTERNS:
        match = pattern.search(subset)
        if match:
            return match.group(1).strip()
    return ""

# 1. Tags: @TAG or !TAG
# Matches: # @TAG args, // @TAG args, <!-- @TAG args -->, > @TAG args
TAG_REGEX = re.compile(
    r'^\s*(?:#+|//|<!--|>)?\s*([@!][A-Z_]+)(?:\s+(.*?))?(?:\s*(?:-->))?\s*$', 
    re.MULTILINE
)

# 2. Sections: <!-- NIKI_NAME_START --> ... <!-- NIKI_NAME_END -->
# Group 1: Name (e.g. MAP)
# Group 2: Content
SECTION_REGEX = re.compile(
    r'<!--\s*NIKI_([A-Z0-9_]+)_START\s*-->(.*?)<!--\s*NIKI_\1_END\s*-->',
    re.DOTALL
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
        line_number = content.count('\n', 0, match.start()) + 1
        
        tags.append(Tag(
            name=name,
            args=_extract_args(args_str),
            line=line_number,
            raw=raw
        ))
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
            content=inner_content, # Keep raw content including newlines
            raw=match.group(0),
            start_pos=match.start(),
            end_pos=match.end()
        )
    return sections

def extract_docstring(content: str) -> str:
    """
    提取文件顶部的 Docstring.
    """
    subset = content[:2000] # Optimization: only check header
    for pattern in DOCSTRING_PATTERNS:
        match = pattern.search(subset)
        if match:
            return match.group(1).strip()
    return ""

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
    match = re.search(r'^\s*(?:#+|//|<!--|>)?\s*@SUMMARY\s+(.*?)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
        
    # 2. Docstring first line
    if docstring:
        lines = docstring.strip().split('\n')
        if lines:
            return lines[0].strip()
            
    return ""

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
    if file_path and file_path.suffix == '.py':
        try:
            tree = parse_code(content)
            # extract_symbols requires bytes for accurate byte offsets if needed,
            # though our implementation uses AST nodes which map to byte offsets usually.
            # But let's check extract_symbols signature: (tree, content_bytes)
            symbols = extract_symbols(tree, content.encode('utf-8'))
        except Exception as e:
            # Fallback or log warning? For now, silent fail or minimal logging is safer for a scanner
            # to avoid crashing the whole process on one bad file.
            # But in dev, we might want to know.
            print(f"AST Scan Error in {file_path}: {e}")
            pass

    return ScanResult(
        tags=tags,
        sections=sections,
        symbols=symbols,
        docstring=docstring,
        summary=summary,
        todos=todos
    )
