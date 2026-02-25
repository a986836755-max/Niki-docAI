# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Dynamic Capability Loading**: `capabilities.py` implements the "Kernel + Plugins" architecture. Do not hardcode...
# *   **Decoupled Text Processing**: 所有纯文本级别的清洗和标签提取逻辑必须放在 `text_utils.py` 中，禁止在 `scanner.py` 中直接操作原始正则，以避免循环引用和逻辑冗余。
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Constraint Checking (Static Assertion).
业务流：执行静态约束检查。
"""

from pathlib import Path
from typing import Optional
from ..models.config import ProjectConfig
from ..models.context import FileContext
from ..brain import checker, index
from ..core import fs, io
from ..parsing import scanner

def _to_context(scan_result: scanner.ScanResult, path: Path, root: Path) -> FileContext:
    """Convert ScanResult to FileContext"""
    try:
        rel = str(path.relative_to(root))
    except ValueError:
        rel = str(path)
        
    return FileContext(
        path=path,
        rel_path=rel,
        tags=scan_result.tags,
        sections=scan_result.sections,
        symbols=scan_result.symbols,
        docstring=scan_result.docstring,
        memories=scan_result.memories
    )

def run(config: ProjectConfig, target: Optional[str] = None) -> bool:
    """
    Run the constraint checker.
    """
    root = config.scan.root_path
    
    # 1. Determine scope
    if target:
        scan_target = Path(target).resolve()
    else:
        scan_target = root
        
    print(f"🔍 Scanning for violations in {scan_target}...")
    
    # 2. Scan files to build context and index
    # Note: Ideally we should use a persistent index, but for now we rebuild.
    # This might be slow for large projects, but ensures freshness.
    
    # We need to scan ALL _AI.md files first to build the RULE index
    # Use rglob but filter manually
    ai_files = []
    for f in root.rglob("_AI.md"):
        # Basic exclusion
        parts = f.parts
        if "node_modules" in parts or ".git" in parts or "__pycache__" in parts:
            continue
        ai_files.append(f)
        
    rule_contexts = []
    for f in ai_files:
        ctx = scanner.scan_file(f, root)
        if ctx:
            rule_contexts.append(_to_context(ctx, f, root))
        
    cache_dir = root / ".ndoc" / "cache"
    index_file = cache_dir / "index.json"
    
    # Try load
    if index_file.exists():
         semantic_index = index.SemanticIndex.load(index_file)
    else:
         semantic_index = index.build_index(rule_contexts)
         semantic_index.save(index_file)

    print(f"ℹ️  Loaded {len(semantic_index.rules)} rules from {len(ai_files)} context files.")
    
    # 3. Scan target files for checking
    # We only check source files (not _AI.md)
    # Filter based on config ignore patterns? Yes, scanner handles it.
    
    files_to_check = []
    
    if scan_target.is_file():
        ctx = scanner.scan_file(scan_target, root)
        if ctx:
            files_to_check.append(_to_context(ctx, scan_target, root))
    else:
        # Use new public API for project scanning
        # Use config's ignore patterns if scanning project root or subdir
        ignore = config.scan.ignore_patterns if scan_target == root else []
        
        # If target is a subdir, we might want to respect project ignore patterns too
        # But fs.walk_files called by scan_project handles basic filtering if provided
        
        scan_results = scanner.scan_project(scan_target, ignore_patterns=ignore)
        
        for p, ctx in scan_results.items():
             if ctx:
                 files_to_check.append(_to_context(ctx, p, root))
                    
    print(f"ℹ️  Checking {len(files_to_check)} files against constraints...")
    
    # 4. Check Rules
    violations = checker.check_all(files_to_check, semantic_index)
    
    if not violations:
        print("✅ No violations found.")
        return True
    
    # 5. Report
    print(f"❌ Found {len(violations)} violations.")
    for v in violations:
        print(f"  {v.severity}: {v.file_path}")
        print(f"    Rule: {v.rule_name}")
        print(f"    Message: {v.message}")
        
    return False
