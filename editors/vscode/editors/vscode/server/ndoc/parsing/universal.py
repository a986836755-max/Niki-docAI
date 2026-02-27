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
Parsing: Universal AST Adapter.
感知层：通用 AST 适配器，基于 _LANGS.json 驱动多语言解析。
"""
import re
from pathlib import Path
from typing import List, Set, Optional
from ..core.capabilities import CapabilityManager
from .langs import get_lang_id_by_ext

# Load language specs
_LANG_SPECS = {}
_EXT_MAP = {}

def get_language_for_file(path: Path) -> Optional[str]:
    """Get language ID from file extension."""
    return get_lang_id_by_ext(path.suffix.lower())

# Regex Patterns for Imports
# Optimized for robust extraction without full AST
REGEX_PATTERNS = {
    'python': [
        r"^\s*import\s+([\w\s,]+)",                   # import os, sys
        r"^\s*from\s+([\w.]+)\s+import\s+([\w\s,]+)", # from os import path
        r"^\s*from\s+(\.+)\s+import\s+([\w\s,]+)",    # from . import io
    ],
    'dart': [
        r"^\s*import\s+['\"](.*?)['\"]",              # import 'package:...'
        r"^\s*export\s+['\"](.*?)['\"]",              # export '...'
        r"^\s*part\s+['\"](.*?)['\"]",                # part '...'
    ],
    'cpp': [
        r'^\s*#\s*include\s*[<"]([^>"]+)[>"]'         # #include <vector> or "header.h"
    ],
    'c_sharp': [
        r"^\s*using\s+([\w\.]+)\s*;"                  # using System.IO;
    ],
    'java': [
        r"^\s*import\s+([\w\.\*]+)\s*;"               # import java.util.List; or java.io.*;
    ],
    'javascript': [
        r"^\s*import\s+.*\s+from\s+['\"](.*?)['\"]",  # import { x } from 'y'
        r"^\s*import\s+['\"](.*?)['\"]",              # import 'y'
        r"require\(['\"](.*?)['\"]\)",                # require('y')
        r"import\(['\"](.*?)['\"]\)"                  # import('y')
    ],
    'typescript': [
        r"^\s*import\s+.*\s+from\s+['\"](.*?)['\"]",
        r"^\s*import\s+['\"](.*?)['\"]",
        r"require\(['\"](.*?)['\"]\)",
        r"import\(['\"](.*?)['\"]\)"
    ],
    'go': [
        r'^\s*import\s+"([^"]+)"',                    # import "fmt"
        r'^\s*import\s+\(\s*([\s\S]*?)\s*\)'          # import ( "fmt" \n "os" )
    ],
    'rust': [
        r"^\s*use\s+([\w:]+)(?:::\{.*\})?;",          # use std::io;
        r"^\s*(?:pub\s+)?mod\s+([\w]+);"              # mod utils; pub mod network;
    ],
    'flatbuffers': [
        r'^\s*include\s+"([^"]+)"\s*;'                # include "other.fbs";
    ]
}

def _extract_python_imports(content: str) -> Set[str]:
    """Specific extractor for Python to handle multi-line imports and relative imports."""
    imports = set()
    lines = content.splitlines()
    
    for line in lines:
        line = line.strip()
        # import x, y
        m1 = re.match(r"^import\s+([\w\s,]+)", line)
        if m1:
            for part in m1.group(1).split(','):
                imports.add(part.strip())
            continue
            
        # from x import y
        m2 = re.match(r"^from\s+([\w.]+)\s+import", line)
        if m2:
            imports.add(m2.group(1))
            continue

        # from . import y (Relative)
        m3 = re.match(r"^from\s+(\.+)\s+import", line)
        if m3:
            # We just record '.' or '..' as the dependency for now
            # The caller (deps_flow) needs to resolve this relative to file path
            imports.add(m3.group(1)) 
            continue
            
        # from ..core import y
        m4 = re.match(r"^from\s+(\.+[\w]+)\s+import", line)
        if m4:
             imports.add(m4.group(1))
             continue
             
    return imports

def _extract_go_imports(content: str) -> Set[str]:
    """Specific extractor for Go to handle import blocks."""
    imports = set()
    
    # 1. Remove single-line comments // ...
    # Be careful not to remove http:// inside strings, but for imports usually safe-ish
    # Better: process line by line
    
    # Single line: import "fmt"
    for m in re.finditer(r'^\s*import\s+(?:[\w.]+\s+)?"([^"]+)"', content, re.MULTILINE):
        imports.add(m.group(1))
        
    # Block import
    block_pattern = re.compile(r'^\s*import\s+\(\s*([\s\S]*?)\s*\)', re.MULTILINE)
    for match in block_pattern.finditer(content):
        block_content = match.group(1)
        # Extract strings inside block
        for line in block_content.splitlines():
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            # Handle inline comments: "fmt" // comment
            line = line.split('//')[0]
            
            # "path/to/lib" or alias "path/to/lib"
            # Match strictly "path" at end or alias "path"
            m_str = re.search(r'(?:[\w.]+\s+)?"([^"]+)"', line)
            if m_str:
                imports.add(m_str.group(1))
                
    return imports

def extract_imports(content: str, path: Path) -> Set[str]:
    """
    Extract imported modules using regex heuristics based on language specs.
    Supports: Python, C++, Dart, Java, C#, JS, TS, Go, Rust.
    """
    lang_name = get_language_for_file(path)
    if not lang_name:
        return set()
    
    # 1. Specialized Parsers
    if lang_name == 'python':
        return _extract_python_imports(content)
    if lang_name == 'go':
        return _extract_go_imports(content)
        
    # 2. Generic Regex Parser
    patterns = REGEX_PATTERNS.get(lang_name, [])
    imports = set()
    
    for pattern in patterns:
        try:
            for match in re.finditer(pattern, content, re.MULTILINE):
                # Group 1 is usually the module name/path
                if match.lastindex and match.lastindex >= 1:
                    imports.add(match.group(1))
        except Exception:
            pass
            
    return imports

def extract_definitions(content: str, path: Path) -> List[str]:
    """
    Extract top-level definitions (classes/functions) for summary.
    Using Tree-sitter when available, fallback to Regex.
    """
    lang_name = get_language_for_file(path)
    if not lang_name:
        return []
    
    # Try Tree-sitter
    ts_lang = CapabilityManager.get_language(lang_name, auto_install=False)
    if ts_lang:
        try:
            from tree_sitter import Parser
            parser = Parser(ts_lang)
            tree = parser.parse(bytes(content, "utf8"))
            
            defs = []
            
            # Generic traversal for common node types
            
            def visit(node):
                name = None
                
                # Python
                if lang_name == 'python':
                    if node.type in ('class_definition', 'function_definition'):
                        # (class_definition name: (identifier) @name)
                        for child in node.children:
                            if child.type == 'identifier':
                                name = content[child.start_byte:child.end_byte]
                                break
                
                # JavaScript / TypeScript / Java / C# / C++ / Dart
                elif lang_name in ('javascript', 'typescript', 'java', 'c_sharp', 'cpp', 'dart'):
                    if node.type in ('class_declaration', 'function_declaration', 'interface_declaration', 'enum_declaration', 'method_definition'):
                         for child in node.children:
                            if child.type == 'identifier' or child.type == 'type_identifier':
                                name = content[child.start_byte:child.end_byte]
                                break
                                
                # Go
                elif lang_name == 'go':
                    if node.type in ('function_declaration', 'type_declaration'):
                        # Go type decl is complex, simplified check
                        for child in node.children:
                            if child.type == 'identifier':
                                name = content[child.start_byte:child.end_byte]
                                break
                                
                if name:
                    # Prefix with type for clarity? e.g. "class Foo"
                    # For now just name to match previous behavior
                    defs.append(name)
                    
                # Recurse only if it's a top-level-ish container or we want nested
                # For summary, top-level is preferred, but let's recurse to find classes inside modules
                for child in node.children:
                    visit(child)
                    
            visit(tree.root_node)
            
            if defs:
                return defs
                
        except Exception:
            # print(f"Tree-sitter definition extraction failed: {e}")
            pass

    # Fallback to Regex
    defs = []
    # Python
    if lang_name == "python":
        for m in re.finditer(r'^\s*(?:class|def)\s+(\w+)', content, re.MULTILINE):
            defs.append(m.group(1))
    
    # C-like (Java, C#, JS, TS, Dart, C++)
    elif lang_name in ("java", "c_sharp", "javascript", "typescript", "dart", "cpp"):
         for m in re.finditer(r'^\s*(?:class|interface|struct|enum|function)\s+(\w+)', content, re.MULTILINE):
            defs.append(m.group(1))

    # Go
    elif lang_name == "go":
        for m in re.finditer(r'^\s*(?:func|type)\s+(\w+)', content, re.MULTILINE):
            defs.append(m.group(1))

    # Rust
    elif lang_name == "rust":
        for m in re.finditer(r'^\s*(?:fn|struct|enum|trait|mod)\s+(\w+)', content, re.MULTILINE):
            defs.append(m.group(1))

    # FlatBuffers
    elif lang_name == "flatbuffers":
        for m in re.finditer(r'^\s*(?:table|struct|enum|union)\s+(\w+)', content, re.MULTILINE):
            defs.append(m.group(1))
            
    return defs
