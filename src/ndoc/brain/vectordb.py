# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Atoms: Vector Database (ChromaDB Wrapper).
原子能力：向量数据库。
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..core.capabilities import CapabilityManager

class VectorDB:
    """
    Wrapper for ChromaDB to provide semantic search capabilities.
    """
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.db_path = root_path / ".ndoc" / "vectordb"
        self.client = None
        self.collection = None
        self._init_db()

    def _init_db(self):
        # Auto-install chromadb if missing
        if not CapabilityManager.ensure_package("chromadb", auto_install=True):
            print("⚠️ ChromaDB not available. Vector search disabled.")
            return
            
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.client = chromadb.PersistentClient(path=str(self.db_path))
            self.collection = self.client.get_or_create_collection(name="ndoc_context")
        except ImportError:
            print("⚠️ ChromaDB import failed even after installation check.")
        except Exception as e:
            print(f"⚠️ Failed to initialize VectorDB: {e}")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Add or update documents in the vector store.
        """
        if not self.collection:
            return
            
        try:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            print(f"⚠️ VectorDB upsert failed: {e}")

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic search.
        """
        if not self.collection:
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Format results
            # Chroma returns: {'ids': [['id1']], 'distances': [[0.1]], 'metadatas': [[{'source': '...'}]]}
            formatted = []
            if results['ids']:
                for i, doc_id in enumerate(results['ids'][0]):
                    item = {
                        "id": doc_id,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "document": results['documents'][0][i] if results['documents'] else "",
                        "distance": results['distances'][0][i] if results['distances'] else 0.0
                    }
                    formatted.append(item)
            return formatted
        except Exception as e:
            print(f"⚠️ VectorDB query failed: {e}")
            return []

    def search(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Alias for query to match expected interface.
        """
        return self.query(query_text, n_results)

    def delete(self, ids: List[str]):
        if not self.collection:
            return
        try:
            self.collection.delete(ids=ids)
        except Exception:
            pass
