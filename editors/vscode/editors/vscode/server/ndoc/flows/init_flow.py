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
Flow: Initialization.
业务流：初始化项目结构 (Initialize Project).
"""
from ndoc.models.config import ProjectConfig
from ndoc.flows import config_flow, syntax_flow
from ..core.cli import ndoc_command

@ndoc_command(name="init", help="Initialize project structure (Create _RULES.md, _SYNTAX.md)", group="Core")
def run(config: ProjectConfig, force: bool = False) -> bool:
    """
    执行初始化 (Execute Init).
    :param force: If True, overwrite existing configuration files.
    """
    print(f"Initializing Niki-docAI for {config.name}...")
    
    # 1. Ensure _RULES.md
    if config_flow.ensure_rules_file(config.scan.root_path, force=force):
        print("✅ Created _RULES.md")
    else:
        print("ℹ️  _RULES.md already exists")
        
    # 2. Ensure _SYNTAX.md
    if syntax_flow.run(config, force=force):
        print("✅ Checked _SYNTAX.md")
        
    # 3. Ensure _GUIDE.md (Instructions for AI)
    if config_flow.ensure_guide_file(config.scan.root_path, force=force):
        print("✅ Created _GUIDE.md (Instructions for AI)")
    else:
        print("ℹ️  _GUIDE.md already exists")
        
    print("\nInitialization complete. You can now run 'ndoc all' to generate documentation.")
    return True
