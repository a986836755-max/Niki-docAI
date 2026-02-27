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
Flow: Status Dashboard & Statistics.
业务流：生成项目状态看板 (_STATUS.md) 和统计报告 (_STATS.md)。
"""
from datetime import datetime
from typing import List

from ..core import io
from ..core.logger import logger
from ..core import stats as core_stats
from ..core import task_manager
from ..views import status as status_view
from ..models.config import ProjectConfig
from ..core.cli import ndoc_command
from ..core.templates import render_document

@ndoc_command(name="status", help="Update Status Dashboard (_STATUS.md)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Execute Status Flow.
    Generates _STATUS.md (TODOs) and _STATS.md (Metrics).
    """
    logger.info("Updating Status Dashboard & Stats...")
    root = config.scan.root_path
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Collect TODOs (Core Logic)
    todos = task_manager.collect_todos(root, config.scan.ignore_patterns)
    
    # 2. Sync Task Checkboxes (Core Logic)
    # Sync with existing _STATUS.md or other tracking files if needed
    status_file = root / "_STATUS.md"
    if status_file.exists():
        task_manager.sync_task_checkboxes(status_file, todos, log_prefix="Auto-completing task: ")
        
        # Cleanup legacy stats section if present
        task_manager.remove_stats_section(status_file)

    # 3. Generate _STATUS.md (View)
    todo_content = status_view.format_todo_lines(todos, root)
    
    status_content = render_document(
        "status.md.tpl",
        title="Project Status",
        context="Project Status",
        tags="@STATUS @AUTO",
        timestamp=timestamp,
        todo_content=todo_content
    )
    io.write_text(status_file, status_content)
    logger.info(f"✅ Status Dashboard updated: {status_file.name}")

    # 4. Statistics (Core Logic)
    # Check if we should update stats (e.g. throttle to avoid heavy IO)
    force_stats = True # For now, always force or use config flag?
    # Let's assume we want fresh stats if user explicitly ran this flow.
    # But if called via 'ndoc all', maybe check cache?
    # For now, let's just run it.
    
    if core_stats.should_update_stats(root, force=True):
        logger.info("Collecting project statistics (this may take a moment)...")
        stats_data = core_stats.collect_full_stats(config)
        
        # 5. Generate _STATS.md (View)
        stats_report = status_view.format_stats_report(stats_data)
        
        stats_file = root / "_STATS.md"
        io.write_text(stats_file, stats_report)
        logger.info(f"✅ Project Statistics updated: {stats_file.name}")
        
    return True
