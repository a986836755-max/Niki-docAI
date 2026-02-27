"""
Syntax Analysis Plugin (Sensor).
Extracts Symbols, Metadata, and Imports from source files.
"""
from typing import Dict, Any
from ndoc.sdk.interfaces import SensorPlugin, hookimpl
from ndoc.sdk.models import Entity, SymbolComponent, MetaComponent, GraphComponent, MemoryComponent
from ndoc.parsing import scanner
from ndoc.core.logger import logger

class SyntaxAnalysisPlugin(SensorPlugin):
    """
    Standard plugin to parse file content and extract syntax information.
    Populates SymbolComponent, MetaComponent, GraphComponent, and MemoryComponent.
    """
    
    @hookimpl
    def ndoc_process_syntax(self, entity: Entity) -> Dict[str, Any]:
        """
        Process a single file entity to extract syntax data.
        """
        if not entity.path or not entity.path.exists() or not entity.path.is_file():
            return {}

        try:
            # Hack: We use entity.path.parent as root to satisfy the signature
            root = entity.path.parent
            
            result = scanner.scan_file(entity.path, root)
            
            if not result:
                return {}
                
            components = {}
            
            # 1. SymbolComponent
            if result.symbols:
                # print(f"[Scanner] Found {len(result.symbols)} symbols in {entity.name}")
                components[SymbolComponent.__name__] = SymbolComponent(symbols=result.symbols)
            else:
                # print(f"[Scanner] No symbols found in {entity.name} (Parser: {result.docstring[:20] if result.docstring else 'None'})")
                pass
                
            # 2. MetaComponent
            # Merge tags, docstring, todos
            meta = MetaComponent(
                tags={t.name for t in result.tags},
                docstring=result.docstring,
                todos=result.todos or []
            )
            components[MetaComponent.__name__] = meta
            
            # 3. GraphComponent
            if result.imports:
                components[GraphComponent.__name__] = GraphComponent(imports=list(result.imports))
                
            # 4. MemoryComponent
            if result.memories or result.decisions or result.lessons or result.intents:
                mem_comp = MemoryComponent(
                    memories=result.memories or [],
                    decisions=result.decisions or [],
                    lessons=result.lessons or [],
                    intents=result.intents or []
                )
                components[MemoryComponent.__name__] = mem_comp
                
            return components
            
        except Exception as e:
            logger.error(f"[Scanner] Failed to parse {entity.name}: {e}")
            return {}
