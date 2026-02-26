"""
View: Context Rendering.
视图层：负责 _AI.md 的内容渲染 (Markdown)。
"""
from typing import Optional, List
from pathlib import Path

from ..models.context import FileContext, DirectoryContext
from ..interfaces import lsp
from ..core import io

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
        
    # Inject Local Dependencies (@DEP)
    if hasattr(ctx, 'imports') and ctx.imports:
        # Limit to 5 imports to avoid clutter
        deps_list = sorted(list(set(ctx.imports)))
        if deps_list:
            deps_str = ", ".join(deps_list[:5])
            if len(deps_list) > 5:
                deps_str += ", ..."
            summary += f" @DEP: {deps_str}"

    return summary

def format_symbol_list(ctx: FileContext, root_path: Path = None) -> str:
    """
    格式化符号列表 (Format symbol list).
    Supports hierarchical display (Classes -> Members).
    """
    if not ctx.symbols:
        return ""
        
    # Build hierarchy map: parent_name -> list[Symbol]
    children_map = {}
    roots = []
    
    # Pre-sort to ensure deterministic order
    # Sort by line number to keep definition order
    sorted_symbols = sorted(ctx.symbols, key=lambda s: s.line)
    
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
    
    # Try to get LSP service (Singleton)
    lsp_service = None
    if root_path:
        lsp_service = lsp.get_service(root_path)

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
    
    return "\n".join(lines)

def format_dependencies(ctx: FileContext) -> str:
    """
    Format dependencies list (if any).
    Uses indentation and keyword markers for visibility.
    """
    # Note: ctx.imports is already populated by scanner/FileContext
    if hasattr(ctx, 'imports') and ctx.imports:
        imports = ctx.imports
        # Limit the number of dependencies shown to keep it concise
        MAX_DEPS = 8
        if len(imports) > MAX_DEPS:
            deps_str = ", ".join(list(imports)[:MAX_DEPS]) + " ..."
        else:
            deps_str = ", ".join(imports)
        
        return f" @DEP: {deps_str}"
    return ""

def generate_dir_content(context: DirectoryContext, root_path: Path = None) -> str:
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
            # Avoid duplicating dep info if format_file_summary adds it too?
            # format_file_summary adds @DEP tags.
            # format_dependencies returns string starting with " @DEP: ..."
            # So we don't need to call format_dependencies separately if format_file_summary does it.
            # But let's check format_file_summary implementation above.
            # Yes, it does. So we can remove duplicate call or keep it consistent.
            # Let's trust format_file_summary.
            
            lines.append(summary)
            # Add symbols as sub-list
            sym_list = format_symbol_list(f_ctx, root_path=root_path)
            if sym_list:
                lines.append(sym_list)
            
    if not has_content:
        lines.append("*   *No structural content.*")
            
    return "\n".join(lines)
