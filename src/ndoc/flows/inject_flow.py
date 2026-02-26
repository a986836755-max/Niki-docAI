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
Flow: Inject Context Header (Header Injection).
业务流：将上下文规则注入到源代码头部。
"""
from pathlib import Path

from ..core import fs
from ..core.logger import logger
from ..core import transforms
from ..parsing import rules as parsing_rules
from ..views import header as header_view
from ..models.config import ProjectConfig
from ..core.cli import ndoc_command

def process_file(file_path: Path, root: Path) -> bool:
    """
    Process a single file for injection.
    """
    current_dir = file_path.parent
    
    # 1. Parse Rules (Parsing)
    ai_path = current_dir / "_AI.md"
    local_rules = parsing_rules.extract_summary_rules(ai_path)
    
    # 2. Generate Header (View)
    header_content = header_view.generate_header(file_path, local_rules)
    
    # 3. Inject (Transform)
    return transforms.inject_header_to_file(file_path, header_content)

@ndoc_command(name="inject", help="Inject context headers into source files", group="Granular")
def run(config: ProjectConfig, target: str = None):
    """
    Execute injection flow.
    """
    root = config.scan.root_path
    
    if target:
        path = Path(target)
        if not path.is_absolute():
            path = root / path
        
        if path.is_file():
            if process_file(path, root):
                logger.info(f"Injected: {path.relative_to(root)}")
            else:
                logger.debug(f"Skipped: {path.relative_to(root)} (No rules or not supported)")
        else:
            # Dir
             files = fs.walk_files(path, config.scan.ignore_patterns)
             for f in files:
                 if process_file(f, root):
                     logger.info(f"Injected: {f.relative_to(root)}")
    else:
        # All
        files = fs.walk_files(root, config.scan.ignore_patterns)
        count = 0
        for f in files:
             if process_file(f, root):
                 logger.info(f"Injected: {f.relative_to(root)}")
                 count += 1
        logger.info(f"Injection complete. Updated {count} files.")
