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
Flow: Prompt Generation (AI Thinking Context).
业务流：为 AI 生成思考所需的上下文 Prompt。
"""
import re
from pathlib import Path
from typing import List, Optional

from ..atoms import io, scanner, index
from ..parsing.ast import skeleton
from ..brain.vectordb import VectorDB
from ..models.config import ProjectConfig

# --- Markers ---
RULE_MARKER = "## !RULE"
CTX_START = "<!-- NIKI_CTX_START -->"

def get_context_prompt(file_path: Path, config: ProjectConfig, focus: bool = False, use_skeleton: bool = False) -> str:
    """
    生成针对特定文件的上下文 Prompt。
    支持 Focus Mode: 只返回最相关的 5% 上下文。
    支持 Skeleton Mode: 返回代码骨架而非全文。
    """
    root = config.scan.root_path
    target_path = Path(file_path).resolve()
    
    content = ""
    
    # Skeleton Logic
    if use_skeleton:
        if target_path.exists():
            raw_content = io.read_text(target_path)
            if raw_content:
                skel = skeleton.generate_skeleton(raw_content, str(target_path))
                content += f"### Skeleton of {target_path.name}\n```python\n{skel}\n```\n\n"
        else:
            content += f"### Skeleton of {target_path.name}\n(File not found)\n\n"
    
    # 1. Basic Path Context (Legacy logic)
    # ... (Keep existing logic if focus is False, or merge it)
    
    if not focus:
        # Legacy full context mode
        return content + _get_full_context(target_path, root)
        
    # 2. Focus Mode (Thalamus Routing)
    # Scan all files to build index (In real app, load from cache)
    # For now, we do a quick scan of _AI.md files and _SYNTAX.md
    
    # Try VectorDB First
    vectordb = VectorDB(root)
    relevant_rules = []
    
    if vectordb.collection:
        # If VectorDB is active, use it for semantic retrieval
        # Query using the file content (first 2000 chars as query)
        query_text = ""
        if target_path.exists():
            query_text = io.read_text(target_path)[:2000]
            
        if query_text:
            results = vectordb.query(query_text, n_results=3)
            if results:
                relevant_rules.append(f"### Related Context (Vector Search)")
                for item in results:
                    path = item['metadata'].get('path', 'Unknown')
                    # Convert to relative path
                    try:
                        rel_p = str(Path(path).relative_to(root))
                    except:
                        rel_p = str(path)
                        
                    # Extract document content (It's the _AI.md content)
                    doc_content = item['document']
                    # Maybe truncate?
                    relevant_rules.append(f"#### From {rel_p}\n{doc_content[:1000]}...\n")

    # If VectorDB yielded nothing or not available, fallback to legacy index logic
    # (or combine them)
    
    # Gather all _AI.md files
    ai_files = list(root.rglob("_AI.md"))
    scanned_contexts = []
    
    for f in ai_files:
        # Scan and convert to FileContext
        res = scanner.scan_file(f, root)
        # Use helper from check_flow (duplicated for now, or move to common)
        # We'll just construct a lightweight context object for index
        from ..models.context import FileContext
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)
            
        ctx = FileContext(
            path=f,
            rel_path=rel,
            tags=res.tags,
            memories=res.memories
        )
        scanned_contexts.append(ctx)
        
    # Build Index
    # Try loading from disk first
    cache_dir = root / ".ndoc" / "cache"
    index_file = cache_dir / "index.json"
    if index_file.exists():
        semantic_index = index.SemanticIndex.load(index_file)
    else:
        semantic_index = index.build_index(scanned_contexts)
        semantic_index.save(index_file)
    
    # a. Always include _SYNTAX.md (The Language)
    syntax_path = root / "_SYNTAX.md"
    if syntax_path.exists():
        relevant_rules.append(f"### Project Syntax\n{io.read_text(syntax_path)[:2000]}...") # Truncate
        
    # b. Find nearest _AI.md (Local Context)
    # ... (Keep existing nearest logic as high priority)
    current = target_path.parent if target_path.is_file() else target_path
    while current != root.parent:
        ai_path = current / "_AI.md"
        if ai_path.exists():
            dist = index.calculate_distance(str(target_path), str(ai_path))
            content = io.read_text(ai_path)
            # Simple heuristic: If distance is small, include it
            if dist <= 2: 
                relevant_rules.append(f"### Context (Dist={dist})\n{content}")
            break # Only nearest one for now in focus mode
        current = current.parent
        
    # c. Query Semantic Index (Hippocampus)
    # Find rules related to keywords in the target file
    
    # 3. Vector Search (Semantic Context)
    try:
        from ..brain.vectordb import VectorDB
        vdb = VectorDB(root)
        # Use filename + summary as query
        query = f"{target_path.name} context"
        # Get more candidates, then filter
        results = vdb.query(query, n_results=5)
        
        if results:
            relevant_rules.append("### Semantic Context (Vector Search)")
            # Dedup based on source
            seen_sources = set()
            
            for res in results:
                meta = res.get('metadata', {})
                src = meta.get('source', 'unknown')
                
                # Avoid self-reference
                if str(src) in str(target_path):
                    continue
                    
                if src in seen_sources:
                    continue
                seen_sources.add(src)
                
                doc = res.get('document', '')
                relevant_rules.append(f"#### From {src}\n{doc}")
    except Exception:
        pass
    
    return "\n\n".join(relevant_rules)

def _get_full_context(file_path: Path, root: Path) -> str:
    """
    Legacy full context generation.
    """
    current_dir = file_path.parent if file_path.is_file() else file_path
    
    rules = []
    
    # 1. Global Rules (_RULES.md)
    global_rules_path = root / "_RULES.md"
    if global_rules_path.exists():
        rules.append(f"### Global Rules ({global_rules_path.name})\n{io.read_text(global_rules_path)}")
        
    # 2. _SYNTAX.md
    syntax_path = root / "_SYNTAX.md"
    if syntax_path.exists():
        rules.append(f"### Syntax\n{io.read_text(syntax_path)}")

    # 3. Inherited Rules
    try:
        if file_path.is_absolute() and str(file_path).startswith(str(root)):
            rel_path = file_path.relative_to(root)
            parts = rel_path.parts[:-1] if file_path.is_file() else rel_path.parts
            
            path_cursor = root
            # Root _AI.md
            ai_file = path_cursor / "_AI.md"
            if ai_file.exists():
                 rules.append(f"### Project Context ({path_cursor.name})\n{io.read_text(ai_file)}")
                 
            for part in parts:
                path_cursor = path_cursor / part
                ai_file = path_cursor / "_AI.md"
                if ai_file.exists():
                    rules.append(f"### Module Context ({part})\n{io.read_text(ai_file)}")
    except ValueError:
        pass

    return "\n\n".join(rules)

def run(file_path: str, config: ProjectConfig, focus: bool = False) -> bool:
    """
    打印 Prompt Context 到标准输出。
    """
    path = Path(file_path)
    prompt = get_context_prompt(path, config, focus)
    
    print("-" * 20 + " AI CONTEXT START " + "-" * 20)
    print(prompt)
    print("-" * 20 + " AI CONTEXT END " + "-" * 20)
    return True
