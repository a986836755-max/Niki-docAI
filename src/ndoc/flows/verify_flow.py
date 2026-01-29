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

    # Check for !RULE compliance (Basic check: Are there any rules defined?)
    # TODO: Implement deeper rule verification
    
    print("✅ Verification Passed: All core documentation artifacts exist.")
    return True
