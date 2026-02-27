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
Flow: Map Generation.
业务流：生成项目结构图 (_MAP.md)。
"""
from datetime import datetime

from ..core import io
from ..core import map_builder
from ..core.templates import get_template, render_document
from ..models.config import ProjectConfig
from ..core.cli import ndoc_command

@ndoc_command(name="map", help="Generate Project Structure Map (_MAP.md)", group="Core")
def run(config: ProjectConfig) -> bool:
    """
    执行 Map 生成流 (Execute Map Flow).
    Pipeline: Config -> Generate -> Update IO.
    """
    map_file = config.scan.root_path / "_MAP.md"
    
    # 1. Generate Content (Pure)
    tree_content = map_builder.generate_tree_content(config)
    
    # 2. Define Markers (Data)
    start_marker = "<!-- NIKI_MAP_START -->"
    end_marker = "<!-- NIKI_MAP_END -->"
    
    # 3. Execute IO (Side Effect)
    print(f"Updating MAP at {map_file}...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not map_file.exists():
        content = render_document(
            "map.md.tpl",
            title="Project Map",
            context="Map | Project Structure",
            tags="",
            timestamp=timestamp,
            tree_content=tree_content
        )
        return io.write_text(map_file, content)
    else:
        # Update body
        success = io.update_section(map_file, start_marker, end_marker, tree_content)
        
        if not success:
            print(f"⚠️  Markers not found in {map_file.name}. Overwriting file to ensure structure...")
            # Fallback: Overwrite entire file if markers are missing
            content = render_document(
                "map.md.tpl",
                title="Project Map",
                context="Map | Project Structure",
                tags="",
                timestamp=timestamp,
                tree_content=tree_content
            )
            return io.write_text(map_file, content)

        # Update header timestamp
        if success:
            io.update_header_timestamp(map_file)
        return success
