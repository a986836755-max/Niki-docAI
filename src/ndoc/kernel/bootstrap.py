"""
Bootstrap new ECS Kernel and load default plugins.
"""
from typing import List, Any
from ndoc.kernel.context import KernelContext

def create_kernel(include_actions: bool = True) -> KernelContext:
    """
    Initialize Kernel and register plugins.
    
    :param include_actions: If False, only load sensors (for query services).
    """
    # Lazy import plugins to avoid circular imports and tree-sitter version conflicts
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.status import StatusPlugin
    from ndoc.plugins.deps_sensor import DependencySensorPlugin
    from ndoc.plugins.deps_report import DependencyReportPlugin
    from ndoc.plugins.arch_report import ArchitectureReportPlugin
    from ndoc.plugins.stats_report import StatsReportPlugin
    from ndoc.plugins.map_report import MapReportPlugin
    from ndoc.plugins.context_report import ContextReportPlugin
    from ndoc.plugins.adr_report import AdrReportPlugin
    from ndoc.plugins.data_schema import DataSchemaPlugin
    from ndoc.plugins.syntax_manual import SyntaxManualPlugin
    from ndoc.plugins.capability_map import CapabilityMapPlugin
    from ndoc.plugins.lesson_report import LessonReportPlugin
    from ndoc.plugins.mind_map import MindMapPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin

    ctx = KernelContext()
    
    # Core Sensors (Always loaded)
    sensors = [
        FileCollectorPlugin(),
        StatusPlugin(), # Status acts as syntax sensor too
        DependencySensorPlugin(),
        SyntaxAnalysisPlugin(),
    ]
    
    # Action Plugins (Only for 'ndoc all')
    actions = [
        DependencyReportPlugin(),
        ArchitectureReportPlugin(),
        StatsReportPlugin(),
        MapReportPlugin(),
        ContextReportPlugin(),
        AdrReportPlugin(),
        DataSchemaPlugin(),
        SyntaxManualPlugin(),
        CapabilityMapPlugin(),
        LessonReportPlugin(),
        MindMapPlugin(),
    ]
    
    for p in sensors:
        ctx.register_plugin(p)
        
    if include_actions:
        for p in actions:
            ctx.register_plugin(p)
        
    return ctx

def run_analysis_phase(ctx: KernelContext, root_path: str):
    """
    Run only the analysis phase (Collect -> Syntax -> Dependencies).
    Does NOT generate docs.
    Returns populated Context.
    """
    print("🚀 [ECS Kernel] Starting Analysis...")
    
    # 1. Collect
    print(f"  [Kernel] Collecting entities from: {root_path}")
    
    # Legacy manual call for robustness
    # Lazy import for type checking if needed
    from ndoc.plugins.collector import FileCollectorPlugin
    
    entities = []
    for p in ctx.pm.get_plugins():
        if isinstance(p, FileCollectorPlugin):
            entities = p.ndoc_collect_entities(str(root_path))
            break
            
    # Also try hook if needed, but manual call is safe for now
    
    if not entities:
        print("  [Kernel] No entities found.")
        return ctx
        
    print(f"  [Kernel] Registered {len(entities)} entities.")
    for e in entities:
        ctx.add_entity(e)
        
    # 2. Process Syntax
    print("  [Kernel] Processing Syntax...")
    count = 0
    # Manual loop because hooks don't auto-iterate entities
    from ndoc.sdk.models import Component, MetaComponent
    
    for eid, entity in ctx.entities.items():
        results = ctx.pm.hook.ndoc_process_syntax(entity=entity)
        # Results are List[Dict] from multiple plugins
        for res in results:
            if not res: continue
            
            # 1. Handle direct Component objects (Preferred)
            for key, value in res.items():
                if isinstance(value, Component):
                    ctx.add_component(eid, value)
            
            # 2. Handle legacy dict output (e.g. StatusPlugin returns {"todos": ...})
            # Only if MetaComponent wasn't already added by the same plugin
            if "todos" in res and MetaComponent.__name__ not in res:
                # Merge into existing MetaComponent if possible, or create new
                existing_meta = ctx.get_component(eid, MetaComponent)
                if existing_meta:
                    existing_meta.todos.extend(res["todos"])
                else:
                    comp = MetaComponent(todos=res["todos"])
                    ctx.add_component(eid, comp)
        
        count += 1
        if count % 2000 == 0:
            print(f"    ... processed {count} entities")
            
    print(f"  [Kernel] Syntax processing complete.")
    
    # 3. Resolve Dependencies
    print("  [Kernel] Resolving Dependencies...")
    ctx.pm.hook.ndoc_process_dependencies(context=ctx)
    
    print("✅ [ECS Kernel] Analysis Complete.")
    return ctx

def run_pipeline(ctx: KernelContext, root_path: str):
    """
    Run the full standard analysis pipeline including Doc Generation.
    """
    # Run Analysis Phase
    run_analysis_phase(ctx, root_path)
    
    # 4. Generate Docs
    print("  [Kernel] Generating Docs...")
    
    # Debug: Check which plugins are loaded
    for p in ctx.pm.get_plugins():
        print(f"    Plugin Loaded: {p.__class__.__name__}")
        
    try:
        ctx.pm.hook.ndoc_generate_docs(context=ctx)
    except Exception as e:
        print(f"  [Kernel] Error generating docs: {e}")
        import traceback
        traceback.print_exc()
    
    print("✅ [ECS Kernel] Pipeline Complete.")
