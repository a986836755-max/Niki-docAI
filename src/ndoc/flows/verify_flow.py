"""
Flow: Verification.
业务流：架构验证 (Architecture Verification).
"""
import sys
from ndoc.models.config import ProjectConfig

def run(config: ProjectConfig) -> bool:
    """
    执行验证 (Execute Verification).
    Checks if documentation artifacts exist and are valid.
    """
    print(f"Verifying Niki-docAI artifacts for {config.name}...")
    
    root = config.scan.root_path
    required_files = [
        "_MAP.md",
        "_TECH.md",
        "_AI.md",
        "_RULES.md",
        "_SYNTAX.md"
    ]
    
    missing = []
    for fname in required_files:
        fpath = root / fname
        if not fpath.exists():
            missing.append(fname)
            
    if missing:
        print("❌ Verification Failed: Missing artifacts:")
        for m in missing:
            print(f"   - {m}")
        print("\nRun 'ndoc all' to generate missing files.")
        return False

    # Check for !RULE compliance (Deeper rule verification)
    if not _verify_rules_content(config):
        print("❌ Rule Verification Failed.")
        return False
    
    # --- Architecture Guard ---
    if not _check_architecture(config):
        print("❌ Architecture Guard: Violation detected.")
        return False

    print("✅ Verification Passed: All core documentation artifacts exist and architecture is sound.")
    return True

def _verify_rules_content(config: ProjectConfig) -> bool:
    """
    Verify that _AI.md files contain meaningful content under ## !RULE.
    """
    from ..atoms import io
    root = config.scan.root_path
    
    ai_files = list(root.glob("**/_AI.md"))
    if not ai_files:
        return True
        
    violations = []
    for ai_file in ai_files:
        content = io.read_text(ai_file)
        if not content:
            continue
            
        # Check for !RULE section
        if "## !RULE" not in content:
            violations.append(f"{ai_file.relative_to(root)}: Missing ## !RULE section")
            continue
            
        # Check if !RULE is empty (only has placeholder)
        rule_part = content.split("## !RULE")[1].split("##")[0].strip()
        placeholder = "<!-- Add local rules here -->"
        
        if not rule_part or rule_part == placeholder:
            # We don't fail for this yet, but we could warn
            # print(f"⚠️  Warning: {ai_file.relative_to(root)} has empty ## !RULE")
            pass
            
    if violations:
        print("❌ Rule Verification Failed: The following files are missing ## !RULE section:")
        for v in violations:
            print(f"   - {v}")
        return False
        
    return True

def _check_architecture(config: ProjectConfig) -> bool:
    """
    Check for architectural dependency violations.
    """
    from ..atoms import fs, scanner
    root = config.scan.root_path
    src_path = root / "src" / "ndoc"
    if not src_path.exists():
        return True # Skip if no src/ndoc
        
    print("Running Architecture Guard...")
    
    violations = []
    
    # Layer definitions
    layers = {
        "atoms": src_path / "atoms",
        "flows": src_path / "flows",
        "models": src_path / "models"
    }
    
    for layer_name, layer_path in layers.items():
        if not layer_path.exists():
            continue
            
        files = fs.walk_files(layer_path, ignore_patterns=config.scan.ignore_patterns, extensions=['.py'])
        for f in files:
            rel_f = f.relative_to(root).as_posix()
            res = scanner.scan_file(f, root)
            
            # Check imports and calls
            all_deps = res.imports + res.calls
            
            for dep in all_deps:
                # Rule 1: atoms should not depend on flows
                if layer_name == "atoms":
                    if "ndoc.flows" in dep or "from ..flows" in dep or "from flows" in dep:
                        violations.append(f"{rel_f} depends on flows: {dep}")
                
                # Rule 2: models should not depend on atoms or flows
                if layer_name == "models":
                    if "ndoc.atoms" in dep or "from ..atoms" in dep or "ndoc.flows" in dep or "from ..flows" in dep:
                        violations.append(f"{rel_f} depends on {dep}")
                        
    if violations:
        print("❌ Architecture Violations found:")
        for v in violations:
            print(f"   - {v}")
        return False
        
    return True
