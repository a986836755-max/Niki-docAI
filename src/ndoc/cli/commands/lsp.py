"""
Command: LSP Query.
"""
from pathlib import Path
from ndoc.core.cli import ndoc_command
from ndoc.core.logger import logger
from ndoc.models.config import ProjectConfig
from ndoc.interfaces import lsp
from ndoc.core import fs

@ndoc_command(name="lsp", help="Query symbol definitions and references", group="Diagnostics")
def run(config: ProjectConfig, target: str) -> bool:
    """
    Run LSP query locally.
    """
    if not target:
        print("Error: Missing symbol name. Usage: ndoc lsp <symbol_name>")
        return False
        
    logger.info(f"Searching for symbol: {target}")
    root_path = config.scan.root_path
    
    try:
        lsp_service = lsp.get_service(root_path)
        files = list(fs.walk_files(root_path, config.scan.ignore_patterns))
        lsp_service.index_project(files, config=config)
        
        # Find Definitions
        defs = lsp_service.find_definitions(target)
        print(f"\n📍 Definitions ({len(defs)}):")
        for d in defs:
            # d is a Symbol object
            rel = Path(d.path).relative_to(root_path)
            print(f"  - {rel}:{d.line}  -> {d.signature or d.name}")
            
        # Find References
        refs = lsp_service.find_references(target)
        print(f"\n🔗 References ({len(refs)}):")
        for r in refs:
            rel = Path(r['path']).relative_to(root_path)
            print(f"  - {rel}:{r['line']}  -> {r['content']}")
            
        return True
    except Exception as e:
        logger.error(f"LSP command failed: {e}")
        return False
