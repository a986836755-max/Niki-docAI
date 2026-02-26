"""
Public API: High-level interfaces for Agents and MCP Servers.
公开接口：供 Agent 和 MCP Server 调用的高层封装。
"""
from typing import List, Dict, Optional, Any
from pathlib import Path

# Import flows
from .flows import (
    context_flow,
    arch_flow,
    check_flow,
    deps_flow,
    impact_flow,
    prompt_flow,
    search_flow
)
from .flows import config_flow
from .models.config import ProjectConfig

class NdocAPI:
    """
    Unified API surface for Niki-docAI.
    """
    
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.config = config_flow.load_project_config(self.root)

    def refresh_context(self) -> bool:
        """
        Refresh all documentation (Architecture + Context).
        Equivalent to: ndoc all
        """
        ok_arch = arch_flow.run(self.config)
        ok_ctx = context_flow.run(self.config)
        return ok_arch and ok_ctx

    def get_semantic_context(self, query_or_file: str, focus: bool = True) -> str:
        """
        Get semantic context for a file or query.
        Equivalent to: ndoc prompt <file> --focus
        """
        # If it looks like a file path, use prompt flow
        if (self.root / query_or_file).exists():
            return prompt_flow.get_context_prompt(query_or_file, self.config, focus=focus)
        
        # Otherwise, treat as search query (future enhancement: return raw search results?)
        # For now, prompt flow handles focus logic best.
        # Fallback to search flow if just getting results
        return f"Search results for: {query_or_file}"

    def validate_architecture(self) -> bool:
        """
        Check for architectural violations.
        Equivalent to: ndoc check
        """
        return check_flow.run(self.config)

    def analyze_impact(self) -> bool:
        """
        Analyze impact of recent changes.
        Equivalent to: ndoc impact
        """
        return impact_flow.run(self.config)

    def get_module_dependencies(self, target: Optional[str] = None) -> bool:
        """
        Generate dependency graph.
        Equivalent to: ndoc deps
        """
        return deps_flow.run(self.config, target=target)

    def search_codebase(self, query: str, limit: int = 5) -> bool:
        """
        Search codebase using natural language.
        Equivalent to: ndoc search
        """
        return search_flow.run(self.config, query, limit)
