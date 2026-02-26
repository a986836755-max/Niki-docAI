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
Flow: Syntax Manual Sync.
业务流：同步 _SYNTAX.md (Sync Syntax Manual).
"""
from pathlib import Path
from ndoc.models.config import ProjectConfig
from ..core import io
from ..core.templates import get_template

def run(config: ProjectConfig, force: bool = False) -> bool:
    """
    执行 Syntax Flow (Execute Syntax Flow).
    Ensure _SYNTAX.md exists in the project root.
    :param force: If True, overwrite existing file.
    """
    syntax_file = config.scan.root_path / "_SYNTAX.md"
    
    # Simple strategy: Write if missing.
    # We do not overwrite existing files to respect user customizations,
    # unless we implement a smarter merge strategy later.
    if force or not syntax_file.exists():
        if force:
             print(f"Restoring default Syntax Manual at {syntax_file.name}...")
        else:
             print(f"Creating Syntax Manual at {syntax_file.name}...")
        content = get_template("syntax.md.tpl")
        return io.write_text(syntax_file, content)
    else:
        # Optional: Check version and prompt? 
        # For now, just silently skip if exists.
        # print(f"Syntax Manual exists: {syntax_file.name}")
        return True
