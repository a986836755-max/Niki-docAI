"""
Command: Init.
"""
from pathlib import Path
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig
from ndoc.core import io
from ndoc.flows import config_flow

@ndoc_command(name="init", help="Initialize project structure", group="Core")
def run(config: ProjectConfig, force: bool = False) -> bool:
    """
    执行 Init Flow (Execute Init Flow).
    :param force: If True, overwrite existing files.
    """
    root = config.scan.root_path
    print(f"Initializing Niki-docAI in {root}...")
    
    # 1. Create _RULES.md
    config_flow.ensure_rules_file(root, force=force)
    
    # 2. Create _SYNTAX.md
    # Replaced by manual invocation of SyntaxManualPlugin logic or similar
    _ensure_syntax_file(root, force=force)
    
    # 3. Create .ndocignore (Optional, if we want default ignore)
    
    print("ℹ️  Language capabilities will be checked when you run 'ndoc all'.")

    print("\nInitialization complete. You can now run 'ndoc all' to generate documentation.")
    return True

def _ensure_syntax_file(root: Path, force: bool = False):
    from ndoc.core.templates import render_document
    from datetime import datetime
    
    syntax_file = root / "_SYNTAX.md"
    if force or not syntax_file.exists():
        if force:
             print(f"Restoring default Syntax Manual at {syntax_file.name}...")
        else:
             print(f"Creating Syntax Manual at {syntax_file.name}...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = render_document(
            "syntax.md.tpl",
            title="PROJECT SYNTAX",
            context="DSL 定义 | @TAGS: @SYNTAX @OP",
            tags="",
            timestamp=timestamp
        )
        io.write_text(syntax_file, content)
