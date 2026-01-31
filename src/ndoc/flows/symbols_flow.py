"""
Flow: Symbol Index Generation.
业务流：生成全局符号索引 (_SYMBOLS.md)。
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

from ..atoms import fs, io, scanner, ast, lsp
from ..models.config import ProjectConfig
from ..models.context import Symbol

def run(config: ProjectConfig) -> bool:
    """
    执行符号索引生成 (Execute Symbol Index Generation).
    """
    root = config.scan.root_path
    symbols_file = root / "_SYMBOLS.md"
    
    print(f"Scanning symbols for {config.name}...")
    
    # 1. Collect all source files
    files = list(fs.walk_files(root, config.scan.ignore_patterns))
    
    # 2. Initialize LSP for cross-reference stats
    lsp_service = lsp.get_service(root)
    lsp_service.index_project(files)
    
    # 3. Extract symbols from each file
    # Map: relative_dir -> { relative_file_path -> List[Symbol] }
    all_symbols = defaultdict(lambda: defaultdict(list))
    
    total_symbols = 0
    file_count = len(files)
    for i, file_path in enumerate(files):
        rel_path = file_path.relative_to(root)
        # print(f"[{i+1}/{file_count}] Scanning {rel_path}...")
        # Use cached scanner to get symbols
        scan_result = scanner.scan_file(file_path, root)
        symbols = scan_result.symbols
        if not symbols:
            continue
            
        # Filter for public symbols only
        public_symbols = [s for s in symbols if s.is_public]
        if not public_symbols:
            continue
            
        parent_dir = rel_path.parent
        all_symbols[parent_dir][rel_path] = public_symbols
        total_symbols += len(public_symbols)

    if total_symbols == 0:
        print("No public symbols found.")
        return True

    print(f"Generating Symbol Index for {total_symbols} symbols...")
    # 4. Generate Markdown content
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("# Symbol Index")
    lines.append(f"> 最后更新 (Last Updated): {timestamp}")
    lines.append("")
    lines.append("## @OVERVIEW")
    lines.append(f"*   **Total Public Symbols**: {total_symbols}")
    lines.append("")

    # Sort directories
    sorted_dirs = sorted(all_symbols.keys())
    for d in sorted_dirs:
        dir_display = str(d).replace('\\', '/') if str(d) != "." else "Root"
        lines.append(f"## {dir_display}")
        
        # Sort files in directory
        sorted_files = sorted(all_symbols[d].keys())
        for f in sorted_files:
            symbols = all_symbols[d][f]
            # Link to file
            rel_f = f.as_posix()
            lines.append(f"*   **[{f.name}]({rel_f}#L1)**")
            
            # Sort symbols by line
            for sym in sorted(symbols, key=lambda s: s.line):
                kind_icon = _get_kind_icon(sym.kind)
                sig = f" `{sym.signature}`" if sym.signature else ""
                
                # Use LSP to get reference count
                ref_count = lsp_service.get_reference_count(sym.name)
                ref_text = f" [🔗{ref_count}]" if ref_count > 0 else ""
                
                lines.append(f"    *   {kind_icon} **{sym.name}**{sig}{ref_text}")
        lines.append("")

    content = "\n".join(lines)
    
    # 4. Write to file
    success = io.write_text(symbols_file, content)
    if success:
        print(f"✅ Generated {symbols_file} ({total_symbols} symbols)")
    return success

def _get_kind_icon(kind: str) -> str:
    kind_map = {
        'class': 'CLS',
        'struct': 'STC',
        'function': 'FUN',
        'method': 'MET',
        'async_function': 'ASY',
        'async_method': 'ASY',
        'enum': 'ENM',
        'record': 'REC',
        'property': 'PRP',
        'namespace': 'NSP',
        'variable': 'VAR',
        'classmethod': 'CLM',
        'staticmethod': 'STA'
    }
    return kind_map.get(kind, 'SYM')
