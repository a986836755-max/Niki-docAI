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
Flow: Semantic Search.
业务流：自然语言代码搜索 (Semantic Search).
"""
from typing import List, Dict, Any
from pathlib import Path
from ..models.config import ProjectConfig
from ..brain.vectordb import VectorDB
from ..core.logger import logger
from ..core.cli import ndoc_command

@ndoc_command(name="search", help="Search codebase using natural language", group="Analysis")
def run(config: ProjectConfig, query: str, limit: int = 5) -> bool:
    """
    Search codebase using natural language.
    """
    if not query:
        logger.error("Search query cannot be empty.")
        return False

    db = VectorDB(config.scan.root_path)
    
    # Check if DB exists
    if not db.collection:
        logger.warning("Vector database not found. Please run 'ndoc context' first to index the codebase.")
        return False

    logger.info(f"Searching for: '{query}'...")
    
    try:
        results = db.search(query, n_results=limit)
        
        if not results:
            logger.info("No relevant results found.")
            return True
            
        print(f"\n🔍 Top {len(results)} Results for '{query}':")
        print("=" * 60)
        
        for i, res in enumerate(results):
            # res is a dict with 'id', 'document', 'metadata', 'distance'
            path = res.get('id', 'unknown')
            score = 1.0 - res.get('distance', 1.0) # Convert distance to similarity score
            content = res.get('document', '')
            
            # Truncate content for display
            preview = content[:200].replace('\n', ' ') + "..." if len(content) > 200 else content
            
            print(f"{i+1}. [{score:.2f}] {path}")
            print(f"   {preview}")
            print("-" * 60)
            
        return True
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return False
