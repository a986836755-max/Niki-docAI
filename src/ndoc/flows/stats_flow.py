# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: New flows (like `capability_flow.py`) must be registered in `entry.py` to ensure ...
# *   **Auto-Provisioning**: `capability_flow` acts as the project's "immune system", proactively detecting and install...
# *   **Doctor Integration**: `doctor_flow` should reuse the `CapabilityManager` logic to verify system health, rather ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Statistics.
业务流：项目统计 (Project Statistics).
"""
from pathlib import Path
from ndoc.models.config import ProjectConfig
from . import status_flow

check_should_update = status_flow.should_update_stats

def run(config: ProjectConfig, force: bool = False) -> bool:
    return status_flow.update_stats_file(config, force=force)
