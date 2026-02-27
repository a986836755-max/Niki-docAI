"""
Search Service (Kernel-as-a-Service).
Executes semantic search queries against the ECS Kernel.
"""
from typing import List, Dict, Any
from ndoc.kernel.context import KernelContext
# from ndoc.brain.vectordb import VectorDB # Legacy VectorDB?
# In ECS, we might want to use the Plugin's data or a shared VectorDB.
# For now, let's assume we still use the VectorDB, but initialized via Kernel context or config.

class SearchService:
    def __init__(self, context: KernelContext):
        self.context = context
        # We need root path. Context doesn't store it explicitly yet (only in entities).
        # We should probably pass root_path to service or store in context.
        # Let's assume context has a way to get root, or we pass it.
        # For now, we'll try to deduce it from entities.
        self.root_path = self._deduce_root()

    def _deduce_root(self):
        # Fallback logic
        from pathlib import Path
        try:
            # Try to find common root of files
            files = [e.path for e in self.context.entities.values() if e.path]
            if files:
                return Path(files[0]).parent # Rough approximation
            return Path.cwd()
        except Exception:
            return Path.cwd()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Execute search.
        """
        # For Phase 2, we reuse the existing VectorDB logic but wrapped in this service.
        # In future, this service should interact with a more integrated Embedding Component in ECS.
        
        from ndoc.brain.vectordb import VectorDB
        
        # Note: VectorDB relies on disk persistence. 
        # "ndoc all" (ContextReportPlugin) should have updated the DB.
        
        db = VectorDB(self.root_path)
        if not db.collection:
            print("⚠️  Vector database not found. Please run 'ndoc all' to index the codebase.")
            return []
            
        try:
            results = db.search(query, n_results=limit)
            return results
        except Exception as e:
            print(f"Search failed: {e}")
            return []
