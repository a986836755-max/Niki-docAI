"""
Parsing: Dependency API Extractor.
感知层：提取依赖模块的 API 签名。
"""
from pathlib import Path
from typing import List, Dict, Set

from ...core import io
from ...parsing import scanner
from ...models.config import ProjectConfig
from .builder import collect_imports, build_dependency_graph, is_core_module

def extract_related_apis(file_path: Path, config: ProjectConfig) -> str:
    """
    Extract API signatures from modules that the target file imports.
    """
    root = config.scan.root_path
    
    # 1. Resolve imports
    # We use builder's logic but scoped to single file for performance
    try:
        rel_path = file_path.relative_to(root).as_posix()
    except ValueError:
        return ""
        
    # We need a mini-build of dependency graph
    # Optim: Just scan the target file first
    file_scan = scanner.scan_file(file_path, root)
    if not file_scan.imports:
        return ""
        
    # Build a mini import map
    import_map = {rel_path: file_scan.imports}
    
    # Use builder to resolve these imports to actual files
    # Note: build_dependency_graph needs a full file map to resolve paths correctly.
    # So we might need to scan project structure (lightweight) or trust builder cache.
    # For accuracy, let's do a quick walk to get file list, but not content.
    
    # Ideally builder.build_dependency_graph should be refactored to take file_list
    # But for now, we can try to resolve common patterns.
    
    # Let's rely on builder.build_dependency_graph logic which re-scans everything if we pass it all.
    # That's too slow for 'ndoc prompt'.
    
    # Faster approach:
    # 1. Look for _AI.md files in imported packages (if Python).
    # 2. Or just try to match filenames.
    
    # Let's use a simplified resolver here for prompt context
    resolved_files = set()
    
    # Naive resolver for Python
    if file_path.suffix == '.py':
        for imp in file_scan.imports:
            # import ndoc.core.io -> ndoc/core/io.py
            # import .utils -> sibling utils.py
            
            # Absolute
            parts = imp.split('.')
            candidate = root.joinpath(*parts).with_suffix('.py')
            if candidate.exists():
                resolved_files.add(candidate)
                continue
                
            # Src layout? src/ndoc/...
            candidate_src = root / "src" / Path(*parts).with_suffix('.py')
            if candidate_src.exists():
                resolved_files.add(candidate_src)
                continue
                
            # Package init?
            candidate_init = root.joinpath(*parts) / "__init__.py"
            if candidate_init.exists():
                resolved_files.add(candidate_init)
                continue
    
    if not resolved_files:
        return ""
        
    # 2. Extract APIs from resolved files
    api_lines = []
    api_lines.append("## 5. Related APIs (Dependencies)")
    
    for dep_path in sorted(list(resolved_files)):
        try:
            # Check if it has an _AI.md context
            ai_path = dep_path.parent / "_AI.md"
            if ai_path.exists():
                # Extract @API section from _AI.md (faster and pre-summarized)
                content = io.read_text(ai_path)
                in_api = False
                file_apis = []
                
                # Look for file entry
                # Structure:
                # * **[file.py](...)**
                #     * `@API`
                #         * `PUB:` ...
                
                lines = content.splitlines()
                target_file_marker = f"**[{dep_path.name}]"
                found_file = False
                
                for line in lines:
                    if target_file_marker in line:
                        found_file = True
                        continue
                    
                    if found_file:
                        if line.strip().startswith("* **["): # Next file
                            break
                        if "`@API`" in line:
                            in_api = True
                            continue
                        
                        if in_api:
                            # Check indentation to ensure we are still inside @API
                            if not line.startswith("    "): # Dedent
                                # Wait, markdown lists are tricky.
                                # But standard format uses 4 spaces.
                                pass
                            
                            if "PUB:" in line or "VAL->" in line or "FUN" in line:
                                # Clean up formatting
                                clean_line = line.strip().replace("* `", "").replace("`", "")
                                file_apis.append(clean_line)
                                
                if file_apis:
                    api_lines.append(f"### {dep_path.relative_to(root)}")
                    for api in file_apis[:10]: # Limit to 10 APIs per file
                        api_lines.append(f"- {api}")
                    if len(file_apis) > 10:
                        api_lines.append(f"- ... ({len(file_apis)-10} more)")
            else:
                # Fallback: Scan file directly if no _AI.md
                res = scanner.scan_file(dep_path, root)
                if res.symbols:
                    public_syms = [s for s in res.symbols if s.is_public]
                    if public_syms:
                        api_lines.append(f"### {dep_path.relative_to(root)}")
                        for sym in public_syms[:10]:
                            api_lines.append(f"- {sym.kind} {sym.name}{sym.signature}")
                            
        except Exception:
            pass
            
    if len(api_lines) == 1: # Only header
        return ""
        
    return "\n".join(api_lines)
