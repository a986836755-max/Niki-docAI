import re
import sys
from pathlib import Path
from ndoc.core import console
from ndoc.core import config

class RuleViolation:
    def __init__(self, rule_id, file_path, line_num, content, message):
        self.rule_id = rule_id
        self.file_path = file_path
        self.line_num = line_num
        self.content = content
        self.message = message

    def __str__(self):
        return f"[{self.rule_id}] {self.file_path}:{self.line_num} - {self.message}\n    > {self.content.strip()}"

def check_file_content(file_path, rules):
    """
    Scans a single file against a list of regex rules.
    rules: list of (rule_id, regex_pattern, failure_message)
    """
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Skip comments (basic heuristic)
                if line.strip().startswith("//") or line.strip().startswith("*"):
                    continue

                for rule_id, pattern, msg in rules:
                    if pattern.search(line):
                        violations.append(RuleViolation(
                            rule_id, file_path.name, i + 1, line, msg
                        ))
    except UnicodeDecodeError:
        pass # Skip binary files
    return violations

def check_isolation(root):
    """
    !RULE:ISOLATION
    Engine must NOT include Client headers.
    """
    violations = []
    engine_dir = root / "engine"
    
    # Pattern: #include "client/..." or <client/...>
    # or even relative paths that go up to client
    include_client_pattern = re.compile(r'#include\s+["<](.*client.*)[">]')
    
    cpp_files = list(engine_dir.rglob("*.cpp")) + list(engine_dir.rglob("*.h")) + list(engine_dir.rglob("*.hpp"))
    
    for file_path in cpp_files:
        # Skip build, generated, and third-party files
        if any(part in file_path.parts for part in ['build', 'generated', 'third_party', '_deps']):
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if include_client_pattern.search(line):
                        violations.append(RuleViolation(
                            "!RULE:ISOLATION", 
                            file_path.relative_to(root), 
                            i + 1, 
                            line, 
                            "Engine code must NOT include Client headers."
                        ))
        except Exception:
            pass
            
    return violations

def check_coding_standards(root):
    """
    !RULE:NO_EXCEPTIONS
    !RULE:NO_RAW_NEW
    !RULE:NO_OOP (No virtual)
    """
    violations = []
    engine_dir = root / "engine"
    
    # Rules definition: (ID, Regex, Message)
    rules = [
        ("!RULE:NO_EXCEPTIONS", re.compile(r'\b(try|catch|throw)\b'), "Exceptions are forbidden in Engine core."),
        ("!RULE:NO_RAW_NEW", re.compile(r'\b(new\s+|delete\s+)\b'), "Raw new/delete forbidden. Use smart pointers or EnTT."),
        ("!RULE:NO_OOP", re.compile(r'\bvirtual\b'), "Virtual functions (Runtime Polymorphism) forbidden. Use ECS.")
    ]
    
    cpp_files = list(engine_dir.rglob("*.cpp")) + list(engine_dir.rglob("*.h")) + list(engine_dir.rglob("*.hpp"))
    
    for file_path in cpp_files:
        # Skip build, generated, and third-party files
        if any(part in file_path.parts for part in ['build', 'generated', 'third_party', '_deps']):
            continue
            
        # Skip generated files by suffix
        if file_path.name.endswith("_generated.h") or file_path.name.endswith("_generated.cpp"):
            continue

        file_violations = check_file_content(file_path, rules)
        # Update relative path for display
        for v in file_violations:
            v.file_path = file_path.relative_to(root)
            violations.append(v)
            
    return violations

def cmd_verify(root):
    console.step("Verifying Project Rules...")
    
    all_violations = []
    
    # 1. Check Isolation
    console.info("Checking !RULE:ISOLATION (Engine -> Client dependency)...")
    v_iso = check_isolation(root)
    all_violations.extend(v_iso)
    
    # 2. Check Coding Standards
    console.info("Checking C++ Coding Standards (!RULE:NO_EXCEPTIONS, !RULE:NO_RAW_NEW, !RULE:NO_OOP)...")
    v_code = check_coding_standards(root)
    all_violations.extend(v_code)
    
    if not all_violations:
        console.success("All rules passed. Project is clean.")
    else:
        # Use simple print to ensure visibility
        print(f"\n[!] Found {len(all_violations)} rule violations:")
        for v in all_violations:
            print(f"  {v}")
            
        # We might want to exit with error code if this is run in CI
        # but for tool usage, just showing errors is enough.
