"""
Brain: Context Ingestion.
智能层：将生成的上下文摄入向量数据库。
"""
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .vectordb import VectorDB
from ..core import io
from ..models.config import ProjectConfig
from ..models.symbol import Tag

def ingest_context_file(
    file_path: Path, 
    root_path: Path, 
    vectordb: VectorDB,
    tags: List[Tag] = None
) -> None:
    """
    Ingest a generated _AI.md context file into VectorDB.
    Chunks content by sections.
    """
    if not file_path.exists():
        return
        
    try:
        base_id = str(file_path.parent.relative_to(root_path)).replace('\\', '/')
    except ValueError:
        base_id = "root"
    
    if base_id == ".":
        base_id = "root"
        
    tag_names = ",".join([t.name for t in tags]) if tags else ""
        
    base_metadata = {
        "type": "context",
        "path": str(file_path.parent),
        "tags": tag_names,
        "timestamp": datetime.now().isoformat()
    }
    
    full_content = io.read_text(file_path)
    if not full_content:
        return

    # 1. Store Full Document
    vectordb.add_documents(
        documents=[full_content],
        metadatas=[base_metadata],
        ids=[base_id]
    )
    
    # 2. Store Chunks (Split by H2 headers)
    # Simple splitter: split by "\n## "
    chunks = re.split(r'\n## ', full_content)
    chunk_docs = []
    chunk_metas = []
    chunk_ids = []
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
            
        # Re-add header marker if it's not the first preamble
        chunk_text = f"## {chunk}" if i > 0 else chunk
        
        # Extract title for metadata
        title_line = chunk.split('\n')[0].strip()
        section_title = title_line
        
        # Construct ID: path/section_title
        safe_title = re.sub(r'[^a-zA-Z0-9]', '_', section_title)[:30]
        c_id = f"{base_id}#{safe_title}_{i}"
        
        meta = base_metadata.copy()
        meta["section"] = section_title
        meta["is_chunk"] = True
        
        chunk_docs.append(chunk_text)
        chunk_metas.append(meta)
        chunk_ids.append(c_id)
        
    if chunk_docs:
        vectordb.add_documents(
            documents=chunk_docs,
            metadatas=chunk_metas,
            ids=chunk_ids
        )
