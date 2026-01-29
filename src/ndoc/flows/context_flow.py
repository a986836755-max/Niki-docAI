"""
Flow: Recursive Context Generation.
业务流：递归生成局部上下文 (_AI.md)。
"""
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from ..atoms import fs, io, scanner, ast, deps
from ..models.config import ProjectConfig
from ..models.context import FileContext, DirectoryContext

# --- Data Structures ---


# --- Transformations (Pure) ---

def format_file_summary(ctx: FileContext) -> str:
    """
    格式化文件摘要 (Format file summary).
    """
    # Link to file with Line 1 reference
    summary = f"*   **[{ctx.path.name}]({ctx.path.name}#L1)**"
    
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

def format_dependencies(ctx: FileContext) -> str:
    """
    Format dependencies list (if any).
    Uses indentation and keyword markers for visibility.
    """
    try:
        content = io.read_text(ctx.path)
        imports = deps.extract_imports(content)
        if not imports:
            return ""
            
        # Use simple indent line
        deps_str = ", ".join(imports)
        
        # No truncation, allow full visibility
        return f"    *   `@DEP` {deps_str}"
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
            lines.append(format_file_summary(f_ctx))
            # Add symbols as sub-list
            sym_list = format_symbol_list(f_ctx)
            if sym_list:
                lines.append(sym_list)
            
            # Add dependencies
            dep_info = format_dependencies(f_ctx)
            if dep_info:
                lines.append(dep_info)

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

def process_directory(path: Path, config: ProjectConfig, recursive: bool = True) -> None:
    """
    处理单个目录 (Process single directory).
    Args:
        path: Target directory path.
        config: Project configuration.
        recursive: Whether to process subdirectories recursively.
    """
    # 1. List Contents (Atom: fs)
    filter_config = fs.FileFilter(
        ignore_patterns=set(config.scan.ignore_patterns),
    )
    
    entries = fs.list_dir(path, filter_config)
    
    files: List[FileContext] = []
    subdirs: List[Path] = []
    
    # 2. Classify & Scan (Atom: scanner, ast)
    for entry in entries:
        if entry.is_dir():
            subdirs.append(entry)
            if recursive:
                process_directory(entry, config, recursive=True)
        else:
            if entry.name == "_AI.md":
                continue

            content = io.read_text(entry)
            if content is None:
                continue
                
            scan_result = scanner.scan_file_content(content, entry)
            
            f_ctx = FileContext(
                path=entry,
                rel_path=str(entry.relative_to(config.scan.root_path)),
                tags=scan_result.tags,
                sections=scan_result.sections,
                symbols=scan_result.symbols,
                docstring=scan_result.docstring
            )
            files.append(f_ctx)
    
    # 3. Generate Content (Transform)
    if not files and not subdirs:
        return

    dir_context = DirectoryContext(path=path, files=files, subdirs=subdirs)
    content = generate_dir_content(dir_context)
    
    # 4. Write Output (Atom: io)
    ai_file = path / "_AI.md"
    
    cleanup_legacy_map(ai_file)
    
    start_marker = "<!-- NIKI_AUTO_Context_START -->"
    end_marker = "<!-- NIKI_AUTO_Context_END -->"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file exists to initialize it with markers if needed
    if not ai_file.exists():
        template = f"""# Context: {path.name}
> @CONTEXT: Local | {path.name} | @TAGS: @LOCAL
> 最后更新 (Last Updated): {timestamp}

## !RULE
<!-- Add local rules here -->

{start_marker}
{content}
{end_marker}
"""
        io.write_text(ai_file, template)
    else:
        if io.update_section(ai_file, start_marker, end_marker, content):
            io.update_header_timestamp(ai_file)
        else:
            print(f"Injecting missing Context markers into {ai_file}")
            wrapped_content = f"\n\n{start_marker}\n{content}\n{end_marker}\n"
            io.append_text(ai_file, wrapped_content)
            io.update_header_timestamp(ai_file)

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
