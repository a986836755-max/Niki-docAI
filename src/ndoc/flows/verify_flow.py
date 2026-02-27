# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **RULE**: @LAYER(core) CANNOT_IMPORT @LAYER(ui) --> [context_flow.py:198](context_flow.py#L198)
# *   **RULE**: @FORBID(hardcoded_paths) --> [context_flow.py:199](context_flow.py#L199)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Verification.
业务流：架构验证 (Architecture Verification).
"""
import sys
from ndoc.models.config import ProjectConfig
from ..core import fs, io
from ..parsing import scanner
from ..core.logger import logger
from ..core.cli import ndoc_command

def run(config: ProjectConfig, 
        fs_module=fs, 
        io_module=io, 
        scanner_module=scanner,
        logger_instance=logger) -> bool:
    """
    执行验证 (Execute Verification).
    Checks if documentation artifacts exist and are valid.
    Supports Dependency Injection for testing.
    """
    logger_instance.info(f"Verifying Niki-docAI artifacts for {config.name}...")
    
    root = config.scan.root_path
    required_files = [
        "_MAP.md",
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
        logger_instance.error("Verification Failed: Missing artifacts:")
        for m in missing:
            logger_instance.error(f"   - {m}")
        logger_instance.info("\nRun 'ndoc all' to generate missing files.")
        return False

    # Check for !RULE compliance (Deeper rule verification)
    if not _verify_rules_content(config, io_module, logger_instance):
        logger_instance.error("Rule Verification Failed.")
        return False
    
    # --- Architecture Guard ---
    if not _check_architecture(config, fs_module, io_module, scanner_module, logger_instance):
        logger_instance.error("Architecture Guard: Violation detected.")
        return False

    logger_instance.info("✅ Verification Passed: All core documentation artifacts exist and architecture is sound.")
    return True

def _verify_rules_content(config: ProjectConfig, io_module, logger_instance) -> bool:
    """
    Verify that _AI.md files contain meaningful content under ## !RULE.
    """
    root = config.scan.root_path
    
    ai_files = list(root.glob("**/_AI.md"))
    if not ai_files:
        return True
        
    violations = []
    for ai_file in ai_files:
        content = io_module.read_text(ai_file)
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
            # logger_instance.warning(f"⚠️  Warning: {ai_file.relative_to(root)} has empty ## !RULE")
            pass
            
    if violations:
        logger_instance.error("Rule Verification Failed: The following files are missing ## !RULE section:")
        for v in violations:
            logger_instance.error(f"   - {v}")
        return False
        
    return True

def _check_architecture(config: ProjectConfig, fs_module, io_module, scanner_module, logger_instance) -> bool:
    """
    Check for architectural dependency violations.
    """
    root = config.scan.root_path
    src_path = root / "src" / "ndoc"
    if not src_path.exists():
        return True # Skip if no src/ndoc
        
    logger_instance.info("Running Architecture Guard...")
    
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
            
        files = fs_module.walk_files(layer_path, ignore_patterns=config.scan.ignore_patterns, extensions=['.py'])
        for f in files:
            rel_f = f.relative_to(root).as_posix()
            res = scanner_module.scan_file(f, root)
            
            # Check imports and calls
            all_deps = res.imports + res.calls
            
            for dep in all_deps:
                # Rule 1: atoms should not depend on flows
                # atoms is deprecated, but check if any legacy code remains
                if layer_name == "atoms":
                    if "ndoc.flows" in dep or "from ..flows" in dep or "from flows" in dep:
                        violations.append(f"{rel_f} depends on flows: {dep}")
                
                # Rule 2: models should not depend on atoms or flows
                if layer_name == "models":
                    # ndoc.atoms deprecated
                    if "from ..atoms" in dep or "ndoc.flows" in dep or "from ..flows" in dep:
                        violations.append(f"{rel_f} depends on {dep}")
                        
    if violations:
        logger_instance.error("Architecture Violations found:")
        for v in violations:
            logger_instance.error(f"   - {v}")
        return False
        
    return True
