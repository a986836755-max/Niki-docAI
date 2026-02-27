"""
Atoms: Constraint Checker (Prefrontal Cortex).
原子能力：约束检查器（前额叶）。
负责执行静态断言，检查代码是否违反了 !RULE 中定义的结构化约束。
此功能默认关闭，需用户显式开启。
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path
from ..models.symbol import Tag
from ..models.context import FileContext
from .index import SemanticIndex

@dataclass
class Violation:
    file_path: str
    rule_name: str
    message: str
    line: int = 0
    character: int = 0
    severity: str = "ERROR"

def _find_import_line(content: Optional[str], import_name: str) -> int:
    if not content or not import_name:
        return 0
    for i, line in enumerate(content.splitlines()):
        if import_name in line:
            return i + 1
    return 0

def check_file(file: FileContext, index: SemanticIndex) -> List[Violation]:
    """
    Check a single file against all active rules in the index.
    Currently supports:
    - FORBID=tagname: If file has tagname, report error.
    - REQUIRE=tagname: If file is missing tagname, report error.
    """
    violations = []
    
    # Iterate over all rules in the index
    # In a real system, we would filter rules relevant to this file context (using distance)
    # For now, we check ALL global rules for simplicity (or we can assume rules are passed in)
    
    # We need to flatten the index structure to get a list of unique rules
    # Index structure: rules: Dict[str, List[IndexEntry]]
    # Key is rule content, Entry has the Tag object with attributes
    
    checked_rules = set()
    
    for rule_key, entries in index.rules.items():
        if not entries:
            continue
            
        # Use the first entry as the definition of the rule
        rule_tag = entries[0].tag
        
        # Helper to access attributes safely (dict or object)
        def get_attr(obj, key):
            if isinstance(obj, dict):
                return obj.get("attributes", {}).get(key)
            return obj.attributes.get(key)
            
        def get_name(obj):
            if isinstance(obj, dict):
                return obj.get("name")
            return obj.name
            
        def get_args(obj):
            if isinstance(obj, dict):
                return obj.get("args", [])
            return obj.args
        
        # Avoid checking same rule multiple times
        if rule_key in checked_rules:
            continue
        checked_rules.add(rule_key)
        
        # 1. Check FORBID
        forbidden_tag = get_attr(rule_tag, "FORBID")
        if forbidden_tag:
            for ft in file.tags:
                if ft.name == forbidden_tag or (ft.name.startswith("@") and ft.name[1:] == forbidden_tag):
                    line_no = ft.line if ft.line > 0 else 0
                    violations.append(Violation(
                        file_path=str(file.path),
                        rule_name=get_name(rule_tag),
                        message=f"Rule '{rule_key}' forbids tag '{forbidden_tag}'",
                        line=line_no,
                        character=0,
                        severity="ERROR" if get_attr(rule_tag, "CRITICAL") else "WARNING"
                    ))
                    
        # 2. Check REQUIRE
        required_tag = get_attr(rule_tag, "REQUIRE")
        if required_tag:
            has_tag = False
            for ft in file.tags:
                if ft.name == required_tag or (ft.name.startswith("@") and ft.name[1:] == required_tag):
                    has_tag = True
                    break
            
            if not has_tag:
                violations.append(Violation(
                    file_path=str(file.path),
                    rule_name=get_name(rule_tag),
                    message=f"Rule '{rule_key}' requires tag '{required_tag}'",
                    line=0,
                    character=0,
                    severity="ERROR" if get_attr(rule_tag, "CRITICAL") else "WARNING"
                ))

        # 3. Check LAYER (Architecture Guard)
        # Format: !RULE: @LAYER(source) CANNOT_IMPORT @LAYER(target)
        if get_name(rule_tag) == "!RULE" and get_args(rule_tag) and "CANNOT_IMPORT" in get_args(rule_tag):
            # Parse args: ['@LAYER(brain)', 'CANNOT_IMPORT', '@LAYER(interfaces)']
            try:
                args = get_args(rule_tag)
                idx = args.index("CANNOT_IMPORT")
                source_layer = args[idx-1]
                target_layer = args[idx+1]
                
                # Check if current file belongs to source_layer
                # Assuming layer is defined by directory name or @LAYER tag
                if _file_in_layer(file, source_layer):
                    # Check imports
                    for imp in file.imports:
                        # Convert import to layer (heuristic)
                        if _import_in_layer(imp, target_layer):
                            line_no = _find_import_line(file.content, imp)
                            violations.append(Violation(
                                file_path=str(file.path),
                                rule_name=get_name(rule_tag),
                                message=f"Layer violation: '{source_layer}' cannot import '{target_layer}' (found '{imp}')",
                                line=line_no,
                                character=0,
                                severity="ERROR"
                            ))
            except (ValueError, IndexError):
                pass

    return violations

def _file_in_layer(file: FileContext, layer_def: str) -> bool:
    """
    Check if file belongs to a layer.
    Layer def: @LAYER(name)
    """
    if not layer_def.startswith("@LAYER("):
        return False
    layer_name = layer_def[7:-1] # extract name
    
    # 1. Check explicit tag
    for t in file.tags:
        if t.name == "@LAYER" and layer_name in t.args:
            return True
            
    # 2. Check directory name (Convention)
    # e.g. src/ndoc/brain/... is in layer 'brain'
    try:
        parts = file.path.parts
        return layer_name in parts
    except AttributeError:
        # file.path might be a string in some contexts? FileContext says Path.
        # But if it's not relative to src root, parts might not contain layer name simply.
        return str(layer_name) in str(file.path)

def _import_in_layer(import_name: str, layer_def: str) -> bool:
    """
    Check if imported module belongs to a layer.
    """
    if not layer_def.startswith("@LAYER("):
        return False
    layer_name = layer_def[7:-1]
    
    # Simple heuristic: check if layer name is part of import path
    # e.g. import ndoc.brain.checker -> layer 'brain'
    # Also handle relative imports if resolved (but imports usually are just strings)
    return f".{layer_name}." in f".{import_name}." or import_name.endswith(f".{layer_name}") or import_name == layer_name or import_name.startswith(f"{layer_name}.")

def check_all(files: List[FileContext], index: SemanticIndex) -> List[Violation]:
    """
    Check all files.
    """
    all_violations = []
    for file in files:
        all_violations.extend(check_file(file, index))
    return all_violations
