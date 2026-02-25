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
Flow: Recursive Context Generation.
业务流：递归生成局部上下文 (_AI.md)。
"""
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from ..core import fs, io
from ..parsing import scanner, ast, deps
from ..parsing.ast import skeleton
from ..interfaces import lsp
from ..brain.vectordb import VectorDB
from ..models.config import ProjectConfig
from ..models.context import FileContext, DirectoryContext
from .test_map_flow import run_test_mapping, TestUsageMapper

# --- Data Structures ---


# --- Transformations (Pure) ---

def format_file_summary(ctx: FileContext, root: Optional[Path] = None) -> str:
    """
    格式化文件摘要 (Format file summary).
    Args:
        root: Root directory for relative path calculation.
    """
    # Calculate display path
    display_name = ctx.path.name
    link_target = ctx.path.name
    
    if root:
        try:
            # Use forward slashes for Markdown links
            rel = ctx.path.relative_to(root)
            display_name = str(rel).replace('\\', '/')
            link_target = display_name
        except ValueError:
            pass
            
    # Link to file with Line 1 reference
    summary = f"*   **[{display_name}]({link_target}#L1)**"
    
    # Add docstring first line if available
    if ctx.docstring:
        first_line = ctx.docstring.strip().split('\n')[0]
        summary += f": {first_line}"
    elif ctx.description:
        summary += f": {ctx.description}"
        
    return summary

def format_symbol_list(ctx: FileContext, use_skeleton: bool = False) -> str:
    """
    格式化符号列表 (Format symbol list).
    Supports hierarchical display (Classes -> Members) or Semantic Skeleton.
    """
    if not ctx.symbols:
        return ""
        
    # Option 1: Semantic Skeleton (New High-Density Mode)
    # Only if use_skeleton is True (Currently experimental/optional)
    # For now, let's inject a small skeleton preview for core files?
    # Or maybe keep the list format but improve content?
    
    # Let's keep the structured list for _AI.md as it's easier to scan for humans than a code block.
    # But we can enhance the description.
    
    # Build hierarchy map: parent_name -> list[Symbol]
    children_map = {}
    roots = []
    
    # Pre-sort to ensure deterministic order
    # Sort by line number to keep definition order
    sorted_symbols = sorted(ctx.symbols, key=lambda s: s.line)
    
    symbol_by_name = {s.name: s for s in sorted_symbols}

    for sym in sorted_symbols:
        if sym.parent:
            if sym.parent not in children_map:
                children_map[sym.parent] = []
            children_map[sym.parent].append(sym)
        else:
            roots.append(sym)
            
    lines = []
    # Add API identifier wrapper
    lines.append("    *   `@API`")
    
    def _format_single_symbol(sym, level: int):
        # Base indent is 2 levels (File -> @API -> Symbol)
        indent = "    " * (level + 2)
        
        # Kind icon/prefix
        kind_map = {
            'class': 'CLS',
            'struct': 'STC',
            'mixin': 'STC',
            'enum': 'STC',
            'table': 'CLS',
            'function': 'FUN',
            'method': 'MET',
            'async_function': 'ASY',
            'async_method': 'ASY',
            'property': 'PRP',
            'variable': 'VAR',
            'classmethod': 'CLM',
            'staticmethod': 'STA'
        }
        kind_char = kind_map.get(sym.kind, '???')
        
        # Label-Op Protocol
        label = "PUB:" if sym.is_public else "PRV:"
        
        if sym.kind == 'property':
            label = "GET->"
        elif sym.kind == 'variable':
            label = "VAL->"
        elif 'async' in sym.kind:
            label = "AWAIT"
        
        # Bold for public
        name_display = f"**{sym.name}**" if sym.is_public else f"{sym.name}"
        
        # Highlight Labels (PUB:, PRV:) but keep Kind (CLS, FUN) plain
        display = f"`{label}` {kind_char} {name_display}"
        
        if sym.signature:
            display += f"`{sym.signature}`"

        # Add Reference Count if available
        # Need to access LSP Service somehow. It's a singleton.
        # But root path? We can assume _INSTANCE is initialized if run() was called.
        # If not, we skip.
        lsp_service = lsp.get_service(Path(".")) # Root doesn't matter for get_service singleton access
        if lsp_service and lsp_service._is_indexed:
            count = lsp_service.get_reference_count(sym.name)
            if count > 0:
                display += f" [🔗{count}]"
            
        # Add Test Usages
        if hasattr(sym, 'test_usages') and sym.test_usages:
            usage_links = []
            for usage in sym.test_usages[:3]:
                path = usage['path']
                line = usage['line']
                # Create a link relative to project root (assume user is in IDE)
                usage_links.append(f"[{path}#L{line}]")
            
            if usage_links:
                display += f" ↳ Usage: {', '.join(usage_links)}"

        lines.append(f"{indent}*   {display}")
        
        # Recurse for children
        if sym.name in children_map:
            for child in children_map[sym.name]:
                _format_single_symbol(child, level + 1)

    for root in roots:
        _format_single_symbol(root, 0)
        
    # Handle orphans (symbols with parent that wasn't found in roots/hierarchy? 
    # e.g. if parent class is not in top-level for some reason, though tree-sitter should find it)
    # With current logic, if parent is not a symbol (e.g. dynamic class?), they won't be printed via recursion.
    # But extract_symbols returns ALL definitions.
    # If `class A` is defined, it is a root.
    # If `def foo` is defined, it is a root.
    # So this should cover everything.
    
    return "\n".join(lines)

def format_dependencies(ctx: FileContext) -> str:
    """
    Format dependencies list (if any).
    Uses indentation and keyword markers for visibility.
    """
    try:
        content = io.read_text(ctx.path)
        imports = deps.extract_dependencies(content, ctx.path)
        if not imports:
            return ""
            
        # Use simple indent line
        # Limit the number of dependencies shown to keep it concise
        MAX_DEPS = 8
        if len(imports) > MAX_DEPS:
            deps_str = ", ".join(list(imports)[:MAX_DEPS]) + " ..."
        else:
            deps_str = ", ".join(imports)
        
        return f" @DEP: {deps_str}"
    except:
        return ""

def generate_dir_content(context: DirectoryContext) -> str:
    """
    生成目录上下文内容 (Generate directory context content).
    Merged FILES and SUBDIRS into STRUCTURE for unified view.
    """
    lines = []
    
    lines.append("## @STRUCTURE")
    
    has_content = False
    
    # 1. Subdirectories (Navigation first)
    if context.subdirs:
        has_content = True
        for d_path in context.subdirs:
            # Add trailing slash to indicate directory clearly
            # Link to _AI.md inside subdirectory, with #L1
            lines.append(f"*   **[{d_path.name}/]({d_path.name}/_AI.md#L1)**")

    # 2. Files (Content second)
    if context.files:
        has_content = True
        for f_ctx in context.files:
            # Add dependencies
            dep_info = format_dependencies(f_ctx)
            
            summary = format_file_summary(f_ctx, root=context.path)
            if dep_info:
                summary += dep_info
            
            lines.append(summary)
            # Add symbols as sub-list
            sym_list = format_symbol_list(f_ctx)
            if sym_list:
                lines.append(sym_list)
            
            # Dep info already added to summary
            
    if not has_content:
        lines.append("*   *No structural content.*")
            
    return "\n".join(lines)

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

def _inject_test_usages(f_ctx: FileContext, test_mapper: TestUsageMapper, config: ProjectConfig):
    """
    Inject test usage information into symbols.
    """
    try:
        # Rel path relative to root: src/ndoc/...
        rel_path = Path(f_ctx.rel_path)
        parts = list(rel_path.parts)
        # Simple heuristic for python projects in src layout
        if parts and parts[0] == "src":
            parts = parts[1:]
        
        module_path = ".".join(parts)
        if module_path.endswith(".py"):
            module_path = module_path[:-3]
        
        module_name = module_path
        
        for sym in f_ctx.symbols:
            full_name = f"{module_name}.{sym.name}"
            usages = test_mapper.get_usages(full_name)
            if usages:
                sym.test_usages = usages
                
            # Check parent for methods (Class.method)
            if sym.parent:
                parent_full_name = f"{module_name}.{sym.parent}.{sym.name}"
                usages_p = test_mapper.get_usages(parent_full_name)
                if usages_p:
                    if sym.test_usages:
                        # Merge without duplicates
                        existing_paths = {f"{u['path']}:{u['line']}" for u in sym.test_usages}
                        for u in usages_p:
                            key = f"{u['path']}:{u['line']}"
                            if key not in existing_paths:
                                sym.test_usages.append(u)
                    else:
                        sym.test_usages = usages_p
                        
    except Exception:
        pass

def process_directory(path: Path, config: ProjectConfig, recursive: bool = True, parent_aggregate: bool = False, test_mapper: Optional[TestUsageMapper] = None, vectordb: Optional[VectorDB] = None) -> Optional[DirectoryContext]:
    """
    处理单个目录 (Process single directory).
    Args:
        path: Target directory path.
        config: Project configuration.
        recursive: Whether to process subdirectories recursively.
        parent_aggregate: Whether the parent directory is aggregating this one.
        test_mapper: Optional TestUsageMapper for linking tests.
        vectordb: Optional VectorDB for indexing.
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
                docstring=scan_result.docstring,
                memories=scan_result.memories,
                description=scan_result.summary
            )
            
            if test_mapper:
                _inject_test_usages(f_ctx, test_mapper, config)

            files.append(f_ctx)
    
    # 3. Generate Content (Transform)
    # Even if we don't write, we return context for parent
    ctx = DirectoryContext(path=path, files=files, subdirs=subdirs)
    
    if should_write_ai:
        if files or subdirs:
            content = generate_dir_content(ctx)
            
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
                template = f"""# Context: {path.name}
> @CONTEXT: Local | {path.name} | @TAGS: @LOCAL
> 最后更新 (Last Updated): {timestamp}

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

{mem_start}
{memory_content}
{mem_end}

{start_marker}
{content}
{end_marker}
"""
                io.write_text(ai_file, template)
            else:
                # Update Context
                if io.update_section(ai_file, start_marker, end_marker, content):
                    io.update_header_timestamp(ai_file)
                else:
                    print(f"Injecting missing Context markers into {ai_file}")
                    wrapped_content = f"\n\n{start_marker}\n{content}\n{end_marker}\n"
                    io.append_text(ai_file, wrapped_content)
                    io.update_header_timestamp(ai_file)
                
                # Update Memories
                if io.update_section(ai_file, mem_start, mem_end, memory_content):
                    pass
                else:
                    # Inject memories section if missing (e.g. legacy files)
                    # Try to insert after ## !RULE
                    file_content = io.read_text(ai_file)
                    rule_marker = "## !RULE"
                    if rule_marker in file_content and mem_start not in file_content:
                        # Insert after ## !RULE section
                        # We look for the next section (starting with ## or #) or end of file
                        # But simpler is to just append it to ## !RULE if we can locate it
                        # For now, let's just append it before Context Start if possible, or after !RULE
                        
                        # Regex replace to insert after !RULE line
                        pattern = r"(## !RULE.*?\n)"
                        replacement = f"\\1\n{mem_start}\n{memory_content}\n{mem_end}\n"
                        new_content = re.sub(pattern, replacement, file_content, flags=re.DOTALL)
                        if new_content != file_content:
                            io.write_text(ai_file, new_content)
                        else:
                            # Fallback: append before context start
                            wrapped_mem = f"\n{mem_start}\n{memory_content}\n{mem_end}\n"
                            io.update_section(ai_file, start_marker, end_marker, content) # Ensure content is updated
                            # We need to insert mem block.
                            # Let's just rewrite the file if structure is simple enough? No, user edits.
                            # Just append it at the end of !RULE section manually by user?
                            # No, automation.
                            pass # For now, only new files or files with marker get updates.
                            # To support migration, we could force inject.
                            pass
    else:
        # Cleanup: If we shouldn't write, ensure file doesn't exist
        if ai_file.exists():
            # print(f"Removing redundant context: {ai_file}")
            io.delete_file(ai_file)

    if vectordb and should_write_ai and (files or subdirs):
        base_id = str(path.relative_to(config.scan.root_path)).replace('\\', '/')
        if base_id == ".":
            base_id = "root"
            
        base_metadata = {
            "type": "context",
            "path": str(path),
            "tags": ",".join([t.name for t in local_tags]),
            "timestamp": datetime.now().isoformat()
        }
        
        if ai_file.exists():
            full_content = io.read_text(ai_file)
            if full_content:
                # 1. Store Full Document
                vectordb.add_documents(
                    documents=[full_content],
                    metadatas=[base_metadata],
                    ids=[base_id]
                )
                
                # 2. Store Chunks (Split by H2 headers)
                # Simple splitter: split by "\n## "
                # This helps retrieve specific sections like "## !RULE" or "## @FILES"
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

    return ctx

# --- Entry Point ---

def run(config: ProjectConfig) -> bool:
    """
    执行 Context 生成流 (Execute Context Flow).
    """
    print(f"Generating Recursive Context starting from {config.scan.root_path}...")
    
    # 0. Initialize LSP Index for reference counting
    lsp_service = lsp.get_service(config.scan.root_path)
    if not lsp_service._is_indexed:
        files = list(fs.walk_files(config.scan.root_path, config.scan.ignore_patterns))
        lsp_service.index_project(files)
        
    # 0.1 Initialize VectorDB for context ingestion
    # Only if chromadb is available (checked inside VectorDB)
    vectordb = VectorDB(config.scan.root_path)
    
    test_mapper = None
    try:
        test_mapper = run_test_mapping(config)
    except Exception as e:
        print(f"Warning: Test mapping failed: {e}")
        
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
        print(f"Failed to update directory {path}: {e}")
        return False
