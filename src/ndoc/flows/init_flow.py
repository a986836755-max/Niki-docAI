"""
Flow: Initialization.
业务流：初始化项目结构 (Initialize Project).
"""
from ndoc.models.config import ProjectConfig
from ndoc.flows import config_flow, syntax_flow

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
        
    print("\nInitialization complete. You can now run 'ndoc all' to generate documentation.")
    return True
