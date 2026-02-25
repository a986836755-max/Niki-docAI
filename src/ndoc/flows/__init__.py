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
Flows: Business Logic Pipelines.
"""
from . import map_flow
from . import context_flow
# from . import tech_flow # Deleted or renamed?
from . import todo_flow
from . import deps_flow
from . import config_flow
from . import syntax_flow
from . import doctor_flow
from . import init_flow
from . import verify_flow
