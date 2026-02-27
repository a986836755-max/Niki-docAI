"""
Command: Search.
"""
from typing import List, Dict, Any
from pathlib import Path
from ndoc.models.config import ProjectConfig
from ndoc.core.cli import ndoc_command
from ndoc.services.search_service import SearchService
from ndoc.kernel.bootstrap import create_kernel, run_analysis_phase

@ndoc_command(name="search", help="Search codebase using natural language", group="Analysis")
def run(config: ProjectConfig, query: str, limit: int = 5) -> bool:
    """
    Search codebase using natural language.
    """
    if not query:
        print("Search query cannot be empty.")
        return False

    # Initialize Kernel (Lightweight - no actions)
    # We only need sensors to establish context if we want "live" search,
    # but currently search relies on VectorDB which is persisted by "ndoc all".
    # So we might not even need to run analysis phase if we just query DB.
    # However, to be "KaaS", we should load the kernel.
    
    ctx = create_kernel(include_actions=False)
    # For pure search, we don't necessarily need to re-scan files if we trust the DB.
    # But let's assume we want to be safe and just load the service.
    
    service = SearchService(ctx)
    # Inject root path manually since context doesn't have it yet
    service.root_path = config.scan.root_path
    
    print(f"Searching for: '{query}'...")
    results = service.search(query, limit)
    
    if not results:
        print("No relevant results found.")
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
