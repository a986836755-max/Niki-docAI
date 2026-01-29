import re
import sys
import json
import tomli
from pathlib import Path
from datetime import datetime
from ndoc.core import console
from ndoc.core import config
from ndoc.features import tech

class RuleViolation:
    def __init__(self, rule_id, file_path, line_num, content, message):
        self.rule_id = rule_id
        self.file_path = str(file_path) # Store as string for serialization
        self.line_num = line_num
        self.content = content
        self.message = message

    def __str__(self):
        return f"[{self.rule_id}] {self.file_path}:{self.line_num} - {self.message}\n    > {self.content.strip()}"

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "file_path": self.file_path,
            "line_num": self.line_num,
            "content": self.content.strip(),
            "message": self.message
        }

# --- Rule Repository ---

class RuleRepository:
    """Holds default rules for different languages."""
    
    # Format: "Language": { 
    #   "extensions": [".ext", ...], 
    #   "rules": [ ("ID", RegexPattern, "Message") ] 
    # }
    DEFAULTS = {
        "C++": {
            "extensions": [".cpp", ".h", ".hpp", ".cc", ".cxx"],
            "rules": [
                ("!RULE:NO_EXCEPTIONS", re.compile(r'\b(try|catch|throw)\b'), "Exceptions are forbidden in Engine core."),
                ("!RULE:NO_RAW_NEW", re.compile(r'\b(new\s+|delete\s+)\b'), "Raw new/delete forbidden. Use smart pointers or EnTT."),
                ("!RULE:NO_OOP", re.compile(r'\bvirtual\b'), "Virtual functions (Runtime Polymorphism) forbidden. Use ECS.")
            ]
        },
        "Python": {
            "extensions": [".py"],
            "rules": [
                ("!RULE:NO_PRINT", re.compile(r'\bprint\('), "Avoid 'print' in production code. Use 'logger'."),
                ("!RULE:NO_WILD_IMPORT", re.compile(r'from\s+\S+\s+import\s+\*'), "Wildcard imports are forbidden."),
                ("!RULE:TODO_FORMAT", re.compile(r'#\s*TODO(?!:)'), "TODOs must be followed by a colon (TODO:).")
            ]
        },
        "Dart": {
            "extensions": [".dart"],
            "rules": [
                ("!RULE:NO_PRINT", re.compile(r'\bprint\('), "Avoid 'print' in Flutter apps. Use 'debugPrint' or logger.")
            ]
        }
    }
    
    # Stores custom user configuration
    # Format: { "Language": { "extensions": [...], "rules": [...] } }
    _custom_config = {}
    _isolation_config = []

    @classmethod
    def load_config(cls, root: Path):
        """
        Loads configuration from global config (populated by core/config.py).
        Deprecated: The internal loading logic is moved to core/config.py, 
        but we keep this method signature to sync with global state if needed.
        """
        # Sync rules from config
        if config.PROJECT_RULES:
            for lang, rules_list in config.PROJECT_RULES.items():
                lang_key = lang.title()
                if lang_key == "Cpp": lang_key = "C++"
                
                if lang_key not in cls.DEFAULTS:
                    cls.DEFAULTS[lang_key] = {"extensions": [], "rules": []}

                for r in rules_list:
                    rule_id = r.get("id")
                    pattern_str = r.get("pattern")
                    msg = r.get("message", "Rule violation")
                    
                    if rule_id and pattern_str:
                        cls.DEFAULTS[lang_key]["rules"].append(
                            (rule_id, re.compile(pattern_str), msg)
                        )
        
        # Sync layers from config
        if config.PROJECT_LAYERS:
            cls._isolation_config = config.PROJECT_LAYERS

    @classmethod
    def get_rules_for_file(cls, file_path, active_languages=None):
        """Returns list of rules applicable to the given file based on extension."""
        ext = file_path.suffix.lower()
        applicable_rules = []
        
        # If active_languages is provided, only check those languages
        # Otherwise check all known defaults
        candidates = active_languages if active_languages else cls.DEFAULTS.keys()
        
        for lang in candidates:
            # Handle case mismatch (e.g. 'Python' vs 'python')
            # tech.py returns title case, our keys are title case.
            if lang not in cls.DEFAULTS:
                continue
                
            lang_def = cls.DEFAULTS[lang]
            # Some languages in DEFAULTS might not have extensions if created purely from config without extensions
            # So we check if extensions exist
            if "extensions" in lang_def and ext in lang_def["extensions"]:
                applicable_rules.extend(lang_def["rules"])
                
        return applicable_rules

    @classmethod
    def get_isolation_rules(cls):
        return cls._isolation_config

# --- Check Logic ---

def check_file_content(file_path, rules):
    """
    Scans a single file against a list of regex rules.
    rules: list of (rule_id, regex_pattern, failure_message)
    """
    violations = []
    if not rules:
        return violations
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Skip comments (basic heuristic, language agnostic-ish)
                sline = line.strip()
                # C++/Java/Dart/JS style
                if sline.startswith("//") or sline.startswith("/*") or sline.startswith("*"):
                    continue
                # Python/Shell style
                if sline.startswith("#"):
                    continue

                for rule_id, pattern, msg in rules:
                    if pattern.search(line):
                        violations.append(RuleViolation(
                            rule_id, file_path.name, i + 1, line, msg
                        ))
    except UnicodeDecodeError:
        pass # Skip binary files
    except Exception as e:
        # console.debug(f"Error reading {file_path}: {e}")
        pass
    return violations

def check_isolation(root):
    """
    Checks isolation rules defined in configuration or default hardcoded rules.
    """
    violations = []
    
    # 1. Load Dynamic Topology Config
    layers = RuleRepository.get_isolation_rules()
    
    # If no config, fall back to hardcoded Legacy behavior for backward compatibility
    if not layers:
        engine_dir = root / "engine"
        if not engine_dir.exists():
            return violations
            
        # Legacy Pattern
        include_client_pattern = re.compile(r'#include\s+["<](.*client.*)[">]')
        cpp_files = list(engine_dir.rglob("*.cpp")) + list(engine_dir.rglob("*.h")) + list(engine_dir.rglob("*.hpp"))
        
        for file_path in cpp_files:
            if any(part in file_path.parts for part in ['build', 'generated', 'third_party', '_deps']): continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if include_client_pattern.search(line):
                            violations.append(RuleViolation(
                                "!RULE:ISOLATION", file_path.relative_to(root), i + 1, line, 
                                "Engine code must NOT include Client headers."
                            ))
            except Exception: pass
        return violations

    # 2. Dynamic Topology Check
    for layer in layers:
        name = layer.get("name")
        path_str = layer.get("path")
        deny_list = layer.get("deny", [])
        
        if not path_str or not deny_list:
            continue
            
        layer_root = root / path_str
        if not layer_root.exists():
            continue
            
        # Build patterns for denied layers
        # Simple heuristic: look for imports/includes that match denied layer names
        # This is tricky across languages. 
        # C++: #include "denied/..."
        # Python: from denied import ... or import denied
        # Dart: import 'package:denied/...'
        
        # For now, we use a generic string search for the denied path segments
        # e.g. if deny="client", we look for "client/" or "client." in import lines
        
        files = [p for p in layer_root.rglob('*') if p.is_file()]
        
        for file_path in files:
            if any(part in file_path.parts for part in ['build', 'generated', 'third_party', '_deps', '__pycache__', '.git']):
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        sline = line.strip()
                        # Very basic import detection
                        is_import = sline.startswith("#include") or sline.startswith("import") or sline.startswith("from") or sline.startswith("using")
                        
                        if is_import:
                            for denied in deny_list:
                                # Regex to find denied token in import string
                                # e.g. "client" -> matching "client/" or "client." or "client"
                                if denied in sline:
                                    violations.append(RuleViolation(
                                        f"!RULE:ISOLATION:{name}->{denied}", 
                                        file_path.relative_to(root), 
                                        i + 1, 
                                        line, 
                                        f"Layer '{name}' must NOT depend on '{denied}'."
                                    ))
            except Exception:
                pass

    return violations

def check_coding_standards(root, active_languages):
    """
    Scans project files against rules for active languages.
    """
    violations = []
    
    # 1. Collect all files to scan
    # We scan src, engine, client, scripts
    dirs_to_scan = [
        root / 'engine',
        root / 'client',
        root / 'src',
        root / 'scripts',
    ]
    
    files_to_scan = []
    for d in dirs_to_scan:
        if d.exists():
            files_to_scan.extend([p for p in d.rglob('*') if p.is_file()])
            
    # 2. Iterate and check
    for file_path in files_to_scan:
        # Skip common ignore patterns
        if any(part in file_path.parts for part in ['build', 'generated', 'third_party', '_deps', '__pycache__', '.git', 'node_modules']):
            continue
            
        # Skip generated files by suffix
        if file_path.name.endswith("_generated.h") or file_path.name.endswith("_generated.cpp"):
            continue

        # Get rules for this file
        rules = RuleRepository.get_rules_for_file(file_path, active_languages)
        
        if rules:
            file_violations = check_file_content(file_path, rules)
            # Update relative path for display
            for v in file_violations:
                try:
                    v.file_path = str(file_path.relative_to(root))
                except ValueError:
                    v.file_path = str(file_path) # Fallback if not relative
                violations.append(v)
            
    return violations

def cmd_verify(root, output_format="text"):
    if output_format == "text":
        console.step("Verifying Project Rules...")
    
    # 0. Load Configuration
    RuleRepository.load_config(root)
    
    # 1. Auto-detect languages
    details = tech.get_project_details(root)
    detected_langs = list(details['languages'].keys())
    # Map detected names to RuleRepository keys (case sensitive match)
    # RuleRepository uses Title Case keys (C++, Python) matching tech.py output
    
    if output_format == "text":
        console.info(f"Detected Context: {', '.join(detected_langs)}")
    
    all_violations = []
    
    # 2. Check Isolation (Dynamic or Legacy)
    if output_format == "text":
        console.info("Checking Architecture Isolation...")
    v_iso = check_isolation(root)
    all_violations.extend(v_iso)
    
    # 3. Check Coding Standards (Adaptive + Configured)
    if output_format == "text":
        console.info(f"Checking Coding Standards for: {', '.join(detected_langs)}...")
    v_code = check_coding_standards(root, detected_langs)
    all_violations.extend(v_code)
    
    # 4. Report
    exit_code = 0
    if all_violations:
        exit_code = 1

    if output_format == "json":
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_violations": len(all_violations),
                "languages": detected_langs
            },
            "violations": [v.to_dict() for v in all_violations]
        }
        print(json.dumps(report, indent=2))
        
    elif output_format == "junit":
        # Simple JUnit XML generation
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print(f'<testsuites name="ndoc-verify" time="0">')
        print(f'  <testsuite name="ndoc-verify" tests="{len(all_violations)}" failures="{len(all_violations)}">')
        for v in all_violations:
            # Escape XML special chars
            msg = v.message.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            content = v.content.strip().replace('<', '&lt;').replace('>', '&gt;')
            print(f'    <testcase name="{v.file_path}:{v.line_num}" classname="{v.rule_id}">')
            print(f'      <failure message="{msg}">{content}</failure>')
            print(f'    </testcase>')
        print('  </testsuite>')
        print('</testsuites>')
        
    else: # text
        if not all_violations:
            console.success("All rules passed. Project is clean.")
        else:
            # Use simple print to ensure visibility
            print(f"\n[!] Found {len(all_violations)} rule violations:")
            for v in all_violations:
                print(f"  {v}")
            
    if exit_code != 0:
        sys.exit(exit_code)
