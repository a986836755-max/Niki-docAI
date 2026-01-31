"""
Flow: Symbol Index Generation.
业务流：生成全局符号索引 (_SYMBOLS.md)。
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

from ..atoms import fs, io, scanner, ast
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
    files = fs.walk_files(root, config.scan.ignore_patterns)
    
    # 2. Extract symbols from each file
    # Map: relative_dir -> { relative_file_path -> List[Symbol] }
    all_symbols = defaultdict(lambda: defaultdict(list))
    
    total_symbols = 0
    for file_path in files:
        # Use cached scanner to get symbols
        scan_result = scanner.scan_file(file_path, root)
        symbols = scan_result.symbols
        if not symbols:
            continue
            
        # Filter for public symbols only
        public_symbols = [s for s in symbols if s.is_public]
        if not public_symbols:
            continue
            
        rel_path = file_path.relative_to(root)
        parent_dir = rel_path.parent
        all_symbols[parent_dir][rel_path] = public_symbols
        total_symbols += len(public_symbols)

    if total_symbols == 0:
        print("No public symbols found.")
        # If file exists, we might want to clear it or leave it. 
        # For now, just return.
        return True

    # 3. Generate Markdown content
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
                lines.append(f"    *   {kind_icon} **{sym.name}**{sig}")
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
        'property': 'PRP',
        'variable': 'VAR',
        'classmethod': 'CLM',
        'staticmethod': 'STA'
    }
    return kind_map.get(kind, 'SYM')
