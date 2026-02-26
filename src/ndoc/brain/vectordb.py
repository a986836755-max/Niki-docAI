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
        Uses a simple hash check to avoid re-embedding existing documents.
        """
        if not self.collection:
            return
            
        try:
            import hashlib
            
            # 1. Get existing records
            existing = self.collection.get(ids=ids, include=['metadatas', 'documents'])
            existing_map = {}
            if existing['ids']:
                for id, doc, meta in zip(existing['ids'], existing['documents'], existing['metadatas']):
                    existing_map[id] = (doc, meta)
            
            new_docs = []
            new_metas = []
            new_ids = []
            
            for doc, meta, doc_id in zip(documents, metadatas, ids):
                # Calculate hash of content
                content_hash = hashlib.md5(doc.encode('utf-8')).hexdigest()
                meta['hash'] = content_hash
                
                # Check if exists and hash matches
                if doc_id in existing_map:
                    ex_doc, ex_meta = existing_map[doc_id]
                    # If hash in metadata matches, skip
                    if ex_meta and ex_meta.get('hash') == content_hash:
                        continue
                        
                new_docs.append(doc)
                new_metas.append(meta)
                new_ids.append(doc_id)
            
            if new_docs:
                # print(f"🧠 VectorDB: Upserting {len(new_docs)} new/changed documents...")
                self.collection.upsert(
                    documents=new_docs,
                    metadatas=new_metas,
                    ids=new_ids
                )
            else:
                # print(f"🧠 VectorDB: All {len(documents)} documents up-to-date.")
                pass
                
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
