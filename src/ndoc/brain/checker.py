# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
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
    severity: str = "ERROR" # ERROR, WARNING

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
        
        # Avoid checking same rule multiple times
        if rule_key in checked_rules:
            continue
        checked_rules.add(rule_key)
        
        # 1. Check FORBID
        if "FORBID" in rule_tag.attributes:
            forbidden_tag = rule_tag.attributes["FORBID"]
            # Check if file has this tag
            for ft in file.tags:
                if ft.name == forbidden_tag or (ft.name.startswith("@") and ft.name[1:] == forbidden_tag):
                    violations.append(Violation(
                        file_path=str(file.path),
                        rule_name=rule_tag.name,
                        message=f"Rule '{rule_key}' forbids tag '{forbidden_tag}'",
                        severity="ERROR" if "CRITICAL" in rule_tag.attributes else "WARNING"
                    ))
                    
        # 2. Check REQUIRE
        if "REQUIRE" in rule_tag.attributes:
            required_tag = rule_tag.attributes["REQUIRE"]
            has_tag = False
            for ft in file.tags:
                if ft.name == required_tag or (ft.name.startswith("@") and ft.name[1:] == required_tag):
                    has_tag = True
                    break
            
            if not has_tag:
                violations.append(Violation(
                    file_path=str(file.path),
                    rule_name=rule_tag.name,
                    message=f"Rule '{rule_key}' requires tag '{required_tag}'",
                    severity="ERROR" if "CRITICAL" in rule_tag.attributes else "WARNING"
                ))

        # 3. Check LAYER (Architecture Guard)
        # Format: !RULE: @LAYER(source) CANNOT_IMPORT @LAYER(target)
        if rule_tag.name == "!RULE" and rule_tag.args and "CANNOT_IMPORT" in rule_tag.args:
            # Parse args: ['@LAYER(brain)', 'CANNOT_IMPORT', '@LAYER(interfaces)']
            try:
                idx = rule_tag.args.index("CANNOT_IMPORT")
                source_layer = rule_tag.args[idx-1]
                target_layer = rule_tag.args[idx+1]
                
                # Check if current file belongs to source_layer
                # Assuming layer is defined by directory name or @LAYER tag
                if _file_in_layer(file, source_layer):
                    # Check imports
                    for imp in file.imports:
                        # Convert import to layer (heuristic)
                        if _import_in_layer(imp, target_layer):
                            violations.append(Violation(
                                file_path=str(file.path),
                                rule_name=rule_tag.name,
                                message=f"Layer violation: '{source_layer}' cannot import '{target_layer}' (found '{imp}')",
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
