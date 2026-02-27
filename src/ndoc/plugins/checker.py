"""
Constraint Checker Plugin (Action).
Validates project against constraints defined in _RULES.md.
"""
from pathlib import Path
from typing import Dict, Any, List
from ndoc.sdk.interfaces import ActionPlugin, hookimpl
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, MetaComponent, SymbolComponent, GraphComponent
from ndoc.brain import checker, index
from ndoc.models.context import FileContext

class ConstraintCheckerPlugin(ActionPlugin):
    """
    Action plugin to run static assertions (!RULE).
    """
    
    @hookimpl
    def ndoc_generate_docs(self, context: KernelContext):
        print("[Checker] Checking constraints...")
        
        # 1. Build Index from ECS Data
        # We need to reconstruct FileContext-like objects for the checker
        # or adapt the checker to work with Components.
        # Since checker logic is complex (regex/ast matching), 
        # let's adapt ECS data to FileContext for compatibility.
        
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        root = context.root_path if hasattr(context, 'root_path') else Path.cwd()
        
        file_contexts = []
        
        for f in files:
            # Reconstruct FileContext
            fc = FileContext(
                path=f.path,
                rel_path=f.id,
                tags=[],
                sections={},
                symbols=[],
                imports=[],
                docstring="",
                memories=[],
                content="" # Checker might need raw content?
            )
            
            # Fill from Components
            try:
                meta = context.get_component(f.id, MetaComponent)
                if meta:
                    fc.docstring = meta.docstring
                    # Tags conversion
                    # fc.tags = ...
            except KeyError: pass
            
            try:
                sym = context.get_component(f.id, SymbolComponent)
                if sym:
                    fc.symbols = sym.symbols
            except KeyError: pass
            
            try:
                graph = context.get_component(f.id, GraphComponent)
                if graph:
                    fc.imports = graph.imports
            except KeyError: pass
            
            # Note: Checker relies heavily on scanner.scan_file which provides full context including 'content'
            # If SyntaxAnalysisPlugin didn't store content, we might need to read it again or cache it.
            # Current checker implementation (ndoc.brain.checker) works on FileContext.
            # But FileContext in models.context has 'content' field.
            # SyntaxAnalysisPlugin didn't populate 'content' in any component.
            # So we might need to read file content here if checker needs it (e.g. for regex rules).
            
            try:
                # Read content for checking
                # Performance hit? Yes, but checking is heavy anyway.
                # Or we can skip content if rules only use AST.
                # Most rules use symbols or imports. Regex rules need content.
                fc.content = f.path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                pass
                
            file_contexts.append(fc)
            
        # 2. Build Rule Index
        # We need to find rules from _AI.md files (which are not in 'files' list usually?)
        # Wait, _AI.md files are files too.
        # But we need to extract rules from them.
        # The scanner extracts rules into 'memories'.
        # We need MemoryComponent!
        
        from ndoc.sdk.models import MemoryComponent
        
        rule_contexts = []
        for f in files:
            if f.path.name == "_AI.md" or f.path.name == "_RULES.md":
                # Convert to context for index builder
                # We need to pass memories
                try:
                    mem = context.get_component(f.id, MemoryComponent)
                    if mem:
                        # Construct a dummy ScanResult-like object or just use FileContext with memories
                        # index.build_index expects list of FileContext
                        fc = FileContext(
                            path=f.path,
                            rel_path=f.id,
                            memories=mem.memories # These are raw dicts from scanner
                        )
                        rule_contexts.append(fc)
                except KeyError: pass
        
        cache_dir = root / ".ndoc" / "cache"
        index_file = cache_dir / "index.json"
        
        if index_file.exists():
             semantic_index = index.SemanticIndex.load(index_file)
        else:
             semantic_index = index.build_index(rule_contexts)
             semantic_index.save(index_file)
             
        print(f"[Checker] Active Rules: {len(semantic_index.rules)}")
        
        # 3. Check
        violations = checker.check_all(file_contexts, semantic_index)
        
        if not violations:
            print("✅ No violations found.")
        else:
            print(f"❌ Found {len(violations)} violations.")
            for v in violations:
                print(f"  {v.severity}: {v.file_path}")
                print(f"    Rule: {v.rule_name}")
                print(f"    Message: {v.message}")
