# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Parsing: Universal AST Adapter.
感知层：通用 AST 适配器，基于 _LANGS.json 驱动多语言解析。
"""
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from ..core import io
from ..core.capabilities import CapabilityManager

# Load language specs
_LANG_SPECS = {}
_EXT_MAP = {}

def _load_specs():
    if _LANG_SPECS:
        return
    
    spec_path = Path(__file__).parent / "_LANGS.json"
    if not spec_path.exists():
        return
        
    try:
        content = io.read_text(spec_path)
        specs = json.loads(content)
        for lang, config in specs.items():
            _LANG_SPECS[lang] = config
            for ext in config.get("extensions", []):
                _EXT_MAP[ext] = lang
    except Exception as e:
        print(f"❌ Failed to load language specs: {e}")

# Initialize specs
_load_specs()

def get_language_for_file(path: Path) -> Optional[str]:
    return _EXT_MAP.get(path.suffix.lower())

def extract_imports(content: str, path: Path) -> Set[str]:
    """
    Extract imported modules using regex heuristics based on language specs.
    (Full AST parsing would be better but requires tree-sitter bindings for all languages)
    """
    lang_name = get_language_for_file(path)
    if not lang_name:
        return set()
        
    # Try Tree-sitter first (for Python only as POC)
    if lang_name == "python":
        ts_lang = CapabilityManager.get_language("python", auto_install=False)
        if ts_lang:
            try:
                from tree_sitter import Parser
                parser = Parser()
                parser.set_language(ts_lang)
                tree = parser.parse(bytes(content, "utf8"))
                
                imports = set()
                # Simple query for imports
                # (import_statement (dotted_name) @import)
                # (import_from_statement (dotted_name) @from)
                
                # Manual traversal for now as query syntax varies by version
                
                def visit(node):
                    if node.type == 'import_statement':
                         # import X
                         for child in node.children:
                             if child.type == 'dotted_name':
                                 imports.add(content[child.start_byte:child.end_byte])
                             elif child.type == 'aliased_import':
                                 # import X as Y
                                 for sub in child.children:
                                     if sub.type == 'dotted_name':
                                         imports.add(content[sub.start_byte:sub.end_byte])
                                         break
                    elif node.type == 'import_from_statement':
                        # from X import Y
                        module_name = None
                        for child in node.children:
                            if child.type == 'dotted_name':
                                module_name = content[child.start_byte:child.end_byte]
                                break
                        if module_name:
                            imports.add(module_name)
                    
                    for child in node.children:
                        visit(child)
                        
                visit(tree.root_node)
                if imports:
                    return imports
            except Exception:
                # Fallback to regex
                # print(f"Tree-sitter error: {e}")
                pass

    spec = _LANG_SPECS.get(lang_name)
    if not spec:
        return set()
        
    imports = set()
    
    # Python
    if lang_name == "python":
        # from X import Y
        for m in re.finditer(r'^\s*from\s+([\w\.]+)', content, re.MULTILINE):
            imports.add(m.group(1))
        # import X
        for m in re.finditer(r'^\s*import\s+([\w\.]+)', content, re.MULTILINE):
            imports.add(m.group(1))
            
    # JavaScript / TypeScript
    elif lang_name in ("javascript", "typescript"):
        # import ... from "X"
        for m in re.finditer(r'import\s+.*?from\s+[\'"](.*?)[\'"]', content, re.MULTILINE):
            imports.add(m.group(1))
        # require("X")
        for m in re.finditer(r'require\s*\(\s*[\'"](.*?)[\'"]\s*\)', content, re.MULTILINE):
            imports.add(m.group(1))
            
    # Java
    elif lang_name == "java":
        # import X;
        for m in re.finditer(r'^\s*import\s+([\w\.]+);', content, re.MULTILINE):
            imports.add(m.group(1))
            
    # C#
    elif lang_name == "c_sharp":
        # using X;
        for m in re.finditer(r'^\s*using\s+([\w\.]+);', content, re.MULTILINE):
            imports.add(m.group(1))
            
    # C++
    elif lang_name == "cpp":
        # #include <X> or "X"
        for m in re.finditer(r'^\s*#include\s+[<"](.*?)[\">]', content, re.MULTILINE):
            imports.add(m.group(1))
            
    # Dart
    elif lang_name == "dart":
        # import 'X';
        for m in re.finditer(r"^\s*import\s+['\"](.*?)['\"]", content, re.MULTILINE):
            imports.add(m.group(1))
            
    # Go
    elif lang_name == "go":
        # import "X"
        for m in re.finditer(r'^\s*import\s+"(.*?)"', content, re.MULTILINE):
            imports.add(m.group(1))
        # import ( "X" ... )
        # This is harder with regex, skipping multiline import blocks for now
        
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
            parser = Parser()
            parser.set_language(ts_lang)
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
            
    return defs
