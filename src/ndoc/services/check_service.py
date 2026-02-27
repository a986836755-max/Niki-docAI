"""
Check Service (Kernel-as-a-Service).
Executes constraint checks (Static Analysis) using ECS Kernel data.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, Component
from ndoc.parsing import scanner
from ndoc.brain import checker, index

# Note: The legacy check_flow used `ndoc.brain.checker` and `ndoc.brain.index`.
# These modules likely rely on `FileContext` objects which are distinct from ECS `Entity`.
# To migrate properly, we should adapt the ECS Entities to what the checker expects, 
# OR refactor the checker to use ECS Entities.
# Given the "Refactor" scope, we should try to reuse existing logic but feed it from ECS.

class CheckService:
    def __init__(self, context: KernelContext, root_path: Path):
        self.context = context
        self.root_path = root_path
        
    def _entity_to_legacy_context(self, entity: Entity):
        """
        Convert ECS Entity to legacy FileContext for compatibility with checker.
        This is a temporary bridge.
        """
        # We need content, tags, sections, etc.
        # Currently, ECS FileCollector doesn't store full content in Entity (it's in file).
        # And scanner results are not fully persisted in Entity yet (only some components).
        # But wait! ndoc_process_syntax hook in legacy flows was used to populate components.
        # In the new ECS, we might need to re-scan if the data isn't in components.
        
        # However, for `check` command, we want it to be fast.
        # If we already have the kernel loaded, we might not have content in memory.
        
        # Strategy: Re-scan the file using `scanner` just like legacy flow, 
        # but iterate over ECS entities to know WHICH files to check.
        # This respects .ndocignore because FileCollector respects it.
        
        path = entity.path
        if not path.exists(): return None
        
        try:
            # Re-use scanner to get full details (AST, tags, etc)
            # This duplicates work if Kernel already did it, but currently Kernel 
            # only extracts 'todos' and 'dependencies'. It doesn't store full AST.
            scan_result = scanner.scan_file(path, self.root_path)
            if not scan_result: return None
            
            # Convert to FileContext
            # We need to import FileContext. It was in ndoc.models.context
            from ndoc.models.context import FileContext
            from ndoc.core import io
            
            # Read content again? Scanner usually reads it.
            # ScanResult has docstring but maybe not full content?
            # Let's check ScanResult definition... It doesn't seem to have 'content'.
            # Legacy flow read it manually.
            content = io.read_text(path)
            
            rel = entity.id # ECS ID is relative path
            
            return FileContext(
                path=path,
                rel_path=rel,
                content=content,
                tags=scan_result.tags,
                sections=scan_result.sections,
                symbols=scan_result.symbols,
                imports=scan_result.imports,
                docstring=scan_result.docstring,
                memories=scan_result.memories
            )
        except Exception:
            return None

    def check_constraints(self, target_path: Optional[Path] = None) -> List[Any]:
        """
        Run checks.
        """
        # 1. Collect Rules (from _AI.md files)
        # We can find them in ECS entities!
        ai_files = [e for e in self.context.entities.values() 
                   if e.type == EntityType.FILE and e.path.name == "_AI.md"]
        
        print(f"ℹ️  Found {len(ai_files)} rule files in context.")
        
        rule_contexts = []
        for e in ai_files:
            ctx = self._entity_to_legacy_context(e)
            if ctx:
                rule_contexts.append(ctx)
                
        # Build Index
        # We can probably cache this in the service or context
        semantic_index = index.build_index(rule_contexts)
        
        # 2. Collect Target Files
        files_to_check = []
        
        if target_path:
            # Filter entities by target path
            # target_path can be file or dir
            abs_target = target_path.resolve()
            
            for e in self.context.entities.values():
                if e.type != EntityType.FILE: continue
                
                # Check if e.path is within target
                # If target is file, match exact
                if abs_target.is_file():
                    if e.path.resolve() == abs_target:
                        ctx = self._entity_to_legacy_context(e)
                        if ctx: files_to_check.append(ctx)
                else:
                    # Dir
                    if str(e.path.resolve()).startswith(str(abs_target)):
                        ctx = self._entity_to_legacy_context(e)
                        if ctx: files_to_check.append(ctx)
        else:
            # All files
            # But we should skip _AI.md and other docs from checking?
            # Legacy flow didn't explicitly skip them in `files_to_check` list 
            # unless scanner.scan_project did.
            # Let's exclude markdown files from checking for now?
            # Actually, sometimes we want to check markdown. 
            # But usually we check code.
            
            print(f"ℹ️  Scanning project files...")
            count = 0
            for e in self.context.entities.values():
                if e.type != EntityType.FILE: continue
                # Skip _AI.md itself from being checked for code violations?
                if e.path.name == "_AI.md": continue
                
                ctx = self._entity_to_legacy_context(e)
                if ctx: 
                    files_to_check.append(ctx)
                    count += 1
                    if count % 100 == 0:
                        print(f"    ... scanned {count} files")
                        
        print(f"ℹ️  Checking {len(files_to_check)} files against {len(semantic_index.rules)} rules...")
        
        # 3. Check
        violations = checker.check_all(files_to_check, semantic_index)
        return violations
