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
Flow: Recursive Context Generation.
业务流：递归生成局部上下文 (_AI.md)。
"""
import re
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from ..core import io, fs
from ..core.logger import logger
from ..core import transforms
from ..parsing import scanner
from ..interfaces import lsp
from ..brain.vectordb import VectorDB
from ..brain import ingest
from ..models.config import ProjectConfig
from ..models.context import FileContext, DirectoryContext
from ..parsing.deps.test_mapper import run_test_mapping, TestUsageMapper
from ..views import context as context_view
from ..core.cli import ndoc_command
from ..core.templates import render_document

# --- Engine (Pipeline) ---

def cleanup_legacy_map(file_path: Path) -> None:
    """
    清理旧的 @MAP 部分 (Cleanup legacy @MAP section).
    Removes ## @MAP block and its markers to avoid conflict with ## @FILES.
    """
    if not file_path.exists():
        return
        
    content = io.read_text(file_path)
    if not content:
        return
        
    has_changes = False
    
    # Remove ## @MAP ... <!-- NIKI_MAP_END -->
    pattern = r"## @MAP\s*<!-- NIKI_MAP_START -->.*?<!-- NIKI_MAP_END -->\s*"
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, "", content, flags=re.DOTALL)
        has_changes = True
        
    if "## @MAP" in content:
        content = re.sub(r"^## @MAP\s*$", "", content, flags=re.MULTILINE)
        has_changes = True
        
    if has_changes:
        io.write_text(file_path, content.strip() + "\n")

def process_directory(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False, test_mapper: Optional[TestUsageMapper] = None, vectordb: Optional[VectorDB] = None) -> Optional[DirectoryContext]:
    """
    处理单个目录 (Process single directory).
    """
    # 0. Read Local Context & Tags to determine behavior
    ai_file = path / "_AI.md"
    local_tags = []
    if ai_file.exists():
        content = io.read_text(ai_file) or ""
        local_tags = scanner.parse_tags(content)

    is_aggregate = any(t.name == "@AGGREGATE" for t in local_tags)
    is_check_ignore = any(t.name == "@CHECK_IGNORE" for t in local_tags)
    
    # Logic:
    # 1. If parent is aggregating, we do NOT write _AI.md (parent_aggregate=True)
    # 2. If @CHECK_IGNORE, we do NOT write _AI.md (treated as ignored for doc gen)
    should_write_ai = not parent_aggregate and not is_check_ignore
    
    # 1. List Contents (Atom: fs)
    # We iterate manually to handle !IGNORE cleanup properly
    filter_config = fs.FileFilter(
        ignore_patterns=set(config.scan.ignore_patterns),
    )
    
    try:
        all_entries = sorted(list(path.iterdir()), key=lambda x: (x.is_file(), x.name))
    except (PermissionError, FileNotFoundError):
        return None
    
    files: List[FileContext] = []
    subdirs: List[Path] = []
    
    # 2. Classify & Scan
    for entry in all_entries:
        # Check Ignore Rules
        if fs.should_ignore(entry, filter_config, root=config.scan.root_path):
            # CLEANUP: If it's a directory, ensure no _AI.md exists
            if entry.is_dir():
                ignored_ai = entry / "_AI.md"
                if ignored_ai.exists():
                    # print(f"Cleaning up ignored context: {ignored_ai}")
                    io.delete_file(ignored_ai)
            continue
            
        if entry.is_dir():
            if recursive:
                # Recurse
                # If we are aggregating, tell child to NOT write (parent_aggregate=True)
                # If we are @CHECK_IGNORE, also tell child to NOT write (cleanup only)
                pass_aggregate = is_aggregate or is_check_ignore
                
                child_ctx = process_directory(entry, config, recursive=True, parent_aggregate=pass_aggregate, test_mapper=test_mapper, vectordb=vectordb)
                
                if child_ctx:
                    if is_aggregate and not is_check_ignore:
                        # @AGGREGATE: Merge child content (files & subdirs)
                        files.extend(child_ctx.files)
                        subdirs.extend(child_ctx.subdirs)
                    elif not is_check_ignore:
                        # Normal: Link to subdir
                        subdirs.append(entry)
            else:
                if not is_check_ignore:
                    subdirs.append(entry)
                    
        else: # File
            if entry.name == "_AI.md":
                continue
                
            if is_check_ignore:
                continue

            # Use cached scanner
            scan_result = scanner.scan_file(entry, config.scan.root_path)
            
            f_ctx = FileContext(
                path=entry,
                rel_path=str(entry.relative_to(config.scan.root_path)),
                tags=scan_result.tags,
                sections=scan_result.sections,
                symbols=scan_result.symbols,
                imports=scan_result.imports, # Pass imports
                docstring=scan_result.docstring,
                memories=scan_result.memories,
                description=scan_result.summary
            )
            
            # Transform: Inject Test Usages
            if test_mapper:
                transforms.inject_test_usages(f_ctx, test_mapper, config)

            files.append(f_ctx)
    
    # 3. Generate Content (Transform)
    # Even if we don't write, we return context for parent
    ctx = DirectoryContext(path=path, files=files, subdirs=subdirs)
    
    if should_write_ai:
        if files or subdirs:
            # View: Generate Markdown Content
            content = context_view.generate_dir_content(ctx, root_path=config.scan.root_path)
            
            # 4. Write Output (Atom: io)
            cleanup_legacy_map(ai_file)
            
            start_marker = "<!-- NIKI_AUTO_Context_START -->"
            end_marker = "<!-- NIKI_AUTO_Context_END -->"
            
            mem_start = "<!-- NIKI_AUTO_MEMORIES_START -->"
            mem_end = "<!-- NIKI_AUTO_MEMORIES_END -->"
            
            # Format memories
            memory_lines = []
            for f in files:
                if not hasattr(f, 'memories') or not f.memories:
                    continue
                for m in f.memories:
                    # Format: *   **TYPE**: Content [File:L123]
                    link = f"[{f.path.name}:{m['line']}]({f.path.name}#L{m['line']})"
                    memory_lines.append(f"*   **{m['type']}**: {m['content']} {link}")
            
            memory_content = "\n".join(memory_lines)
            if memory_content:
                memory_content = f"### Auto-Detected Rules\n{memory_content}"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if file exists to initialize it with markers if needed
            if not ai_file.exists():
                content = render_document(
                    "ai.md.tpl",
                    title=f"Context: {path.name}",
                    context=f"Local | {path.name}",
                    tags="@LOCAL",
                    timestamp=timestamp,
                    name=path.name,
                    memory_content=memory_content,
                    file_table=content # Initial content
                )
                io.write_text(ai_file, content)
            else:
                # Update body
                success = io.update_section(ai_file, start_marker, end_marker, content)
                
                # Update memories if present (NEW feature: memory section update)
                # We need to implement update_section for memories too if we want it dynamic
                # For now, let's stick to files update which is critical.
                
                if not success:
                    # Fallback
                    # If markers missing, we might want to append or overwrite. 
                    # Overwriting is safer for _AI.md consistency if it's auto-generated.
                    full_content = render_document(
                        "ai.md.tpl",
                        title=f"Context: {path.name}",
                        context=f"Local | {path.name}",
                        tags="@LOCAL",
                        timestamp=timestamp,
                        name=path.name,
                        memory_content=memory_content,
                        file_table=content
                    )
                    io.write_text(ai_file, full_content)
                
                # Update header timestamp
                if success:
                    io.update_header_timestamp(ai_file)
    
    # Brain: Ingest into VectorDB
    if vectordb and should_write_ai and (files or subdirs):
        ingest.ingest_context_file(ai_file, config.scan.root_path, vectordb, tags=local_tags)
    
    # Cleanup: If we shouldn't write, ensure file doesn't exist
    if not should_write_ai and ai_file.exists():
        io.delete_file(ai_file)

    return ctx

# --- Entry Point ---

@ndoc_command(name="context", help="Generate Recursive Context (_AI.md)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    执行 Context 生成流 (Execute Context Flow).
    """
    logger.info(f"Generating Recursive Context starting from {config.scan.root_path}...")
    
    # 0. Initialize LSP Index for reference counting
    lsp_service = lsp.get_service(config.scan.root_path)
    if not lsp_service._is_indexed:
        files = list(fs.walk_files(config.scan.root_path, config.scan.ignore_patterns))
        lsp_service.index_project(files, config=config)
        
    # 0.1 Initialize VectorDB for context ingestion
    # Only if chromadb is available (checked inside VectorDB)
    vectordb = VectorDB(config.scan.root_path)
    
    test_mapper = None
    try:
        test_mapper = run_test_mapping(config)
    except Exception as e:
        logger.warning(f"Test mapping failed: {e}")
        
    process_directory(config.scan.root_path, config, recursive=True, test_mapper=test_mapper, vectordb=vectordb)
    return True

def update_directory(path: Path, config: ProjectConfig) -> bool:
    """
    更新单个目录的 Context (Update single directory context).
    Non-recursive.
    """
    try:
        # Also pass vectordb to update index incrementally
        vectordb = VectorDB(config.scan.root_path)
        process_directory(path, config, recursive=False, vectordb=vectordb)
        return True
    except Exception as e:
        logger.error(f"Failed to update directory {path}: {e}")
        return False
