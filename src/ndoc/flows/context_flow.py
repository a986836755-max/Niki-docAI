"""
Flow: Recursive Context Generation.
业务流：递归生成局部上下文 (_AI.md)。
"""
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

from ..atoms import fs, io, scanner, ast
from ..models.config import ProjectConfig
from ..models.context import FileContext, DirectoryContext

# --- Data Structures ---


# --- Transformations (Pure) ---

def format_file_summary(ctx: FileContext) -> str:
    """
    格式化文件摘要 (Format file summary).
    """
    summary = f"*   **[{ctx.path.name}]({ctx.path.name})**"
    
    # Add docstring first line if available
    if ctx.docstring:
        first_line = ctx.docstring.strip().split('\n')[0]
        summary += f": {first_line}"
    elif ctx.description:
        summary += f": {ctx.description}"
        
    return summary

def format_symbol_list(ctx: FileContext) -> str:
    """
    格式化符号列表 (Format symbol list).
    """
    if not ctx.symbols:
        return ""
        
    lines = []
    
    # Sort: Public first, then Private (alphabetical within groups)
    sorted_symbols = sorted(ctx.symbols, key=lambda s: (not s.is_public, s.name))
    
    for sym in sorted_symbols:
        # Kind icon/prefix
        kind_map = {
            'class': 'CLS',
            'function': 'FUN',
            'method': 'FUN',
            'property': 'VAR'
        }
        kind_char = kind_map.get(sym.kind, '???')
        
        # Label-Op Protocol
        if sym.kind == 'property':
            label = "GET->"
        elif sym.is_public:
            label = "PUB:"
        else:
            label = "PRV:"
        
        # Bold for public
        name_display = f"**{sym.name}**" if sym.is_public else f"{sym.name}"
        
        # Highlight Labels (PUB:, PRV:) but keep Kind (CLS, FUN) plain
        display = f"`{label}` {kind_char} {name_display}"
        
        if sym.signature:
            display += f"`{sym.signature}`"
            
        lines.append(f"    *   {display}")
    return "\n".join(lines)

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
            lines.append(f"*   **[{d_path.name}/]({d_path.name}/_AI.md)**")

    # 2. Files (Content second)
    if context.files:
        has_content = True
        for f_ctx in context.files:
            lines.append(format_file_summary(f_ctx))
            # Add symbols as sub-list
            sym_list = format_symbol_list(f_ctx)
            if sym_list:
                lines.append(sym_list)
                
    if not has_content:
        lines.append("*   *(Empty directory)*")
            
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
    # Pattern handles:
    # ## @MAP
    # <!-- NIKI_MAP_START -->
    # ...
    # <!-- NIKI_MAP_END -->
    pattern = r"## @MAP\s*<!-- NIKI_MAP_START -->.*?<!-- NIKI_MAP_END -->\s*"
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, "", content, flags=re.DOTALL)
        has_changes = True
        
    # Also clean up standalone ## @MAP if it remains (e.g. if markers were missing)
    # Be careful not to delete user content if they used ## @MAP without markers
    # But ## @MAP is a reserved system keyword in our design, so it should be safe.
    if "## @MAP" in content:
        # Simple removal of the header line
        content = re.sub(r"^## @MAP\s*$", "", content, flags=re.MULTILINE)
        has_changes = True
        
    if has_changes:
        io.write_text(file_path, content.strip() + "\n")

def process_directory(path: Path, config: ProjectConfig, recursive: bool = True) -> None:
    """
    处理单个目录 (Process single directory).
    Args:
        path: Target directory path.
        config: Project configuration.
        recursive: Whether to process subdirectories recursively.
    """
    # 1. List Contents (Atom: fs)
    # We use a localized filter config based on the project config
    filter_config = fs.FileFilter(
        ignore_patterns=set(config.scan.ignore_patterns),
        # We can add extension filters here if needed, but for context we might want to see more
    )
    
    # fs.list_dir returns sorted paths
    entries = fs.list_dir(path, filter_config)
    
    files: List[FileContext] = []
    subdirs: List[Path] = []
    
    # 2. Classify & Scan (Atom: scanner, ast)
    for entry in entries:
        if entry.is_dir():
            subdirs.append(entry)
            # Recurse immediately (Depth-first)
            if recursive:
                process_directory(entry, config, recursive=True)
        else:
            # Check if it's a source file we care about (e.g., .py)
            # For now, let's process all files that pass the filter, 
            # but detailed AST only for Python.
            
            # Skip meta files (start with _) to avoid infinite loops or noise, 
            # except maybe for referencing? 
            # Rule: Don't document the documentation files themselves in the code context?
            # Let's include them but maybe treat differently.
            # For now, simple rule: Skip _AI.md to avoid self-reference loop in content generation
            if entry.name == "_AI.md":
                continue

            # Read content
            content = io.read_text(entry)
            if content is None:
                continue
                
            # Scan
            scan_result = scanner.scan_file_content(content, entry)
            
            f_ctx = FileContext(
                path=entry,
                rel_path=str(entry.relative_to(config.scan.root_path)),
                tags=scan_result.tags,
                sections=scan_result.sections,
                symbols=scan_result.symbols,
                docstring=scan_result.docstring
            )
            
            # AST Extraction is already done in scan_file_content if applicable
                
            files.append(f_ctx)
    
    # 3. Generate Content (Transform)
    # Only generate _AI.md if there is something relevant (files or subdirs)
    if not files and not subdirs:
        return

    dir_context = DirectoryContext(path=path, files=files, subdirs=subdirs)
    content = generate_dir_content(dir_context)
    
    # 4. Write Output (Atom: io)
    ai_file = path / "_AI.md"
    
    # Pre-cleanup: Remove legacy MAP section to avoid conflicts
    cleanup_legacy_map(ai_file)
    
    # We want to preserve manual sections if they exist, or just overwrite?
    # The requirement is "Recursive Local Context". Usually these are auto-generated.
    # But adhering to "Zero Overwrite", we should use markers if we want to allow user edits.
    # However, for pure context files, maybe full generation is better?
    # Let's stick to the Project Pattern: Use Markers.
    
    start_marker = "<!-- NIKI_AUTO_Context_START -->"
    end_marker = "<!-- NIKI_AUTO_Context_END -->"
    
    # Check if file exists to initialize it with markers if needed
    if not ai_file.exists():
        # Initialize with standard template (Header + Rules + Auto Body)
        template = f"""# Context: {path.name}
> @CONTEXT: Local | {path.name} | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

{start_marker}
{content}
{end_marker}
"""
        io.write_text(ai_file, template)
    else:
        # Update dynamic section only
        if not io.update_section(ai_file, start_marker, end_marker, content):
            # Markers missing, append them (fallback)
            print(f"Injecting missing Context markers into {ai_file}")
            wrapped_content = f"\n\n{start_marker}\n{content}\n{end_marker}\n"
            io.append_text(ai_file, wrapped_content)

# --- Entry Point ---

def run(config: ProjectConfig) -> bool:
    """
    执行 Context 生成流 (Execute Context Flow).
    """
    print(f"Generating Recursive Context starting from {config.scan.root_path}...")
    process_directory(config.scan.root_path, config, recursive=True)
    return True

def update_directory(path: Path, config: ProjectConfig) -> bool:
    """
    更新单个目录的 Context (Update single directory context).
    Non-recursive.
    """
    try:
        process_directory(path, config, recursive=False)
        return True
    except Exception as e:
        print(f"Failed to update directory {path}: {e}")
        return False
