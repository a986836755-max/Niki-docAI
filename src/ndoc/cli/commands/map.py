"""
Command: Map.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="map", help="Generate Project Structure Map (_MAP.md)", group="Core")
def run(config: ProjectConfig) -> bool:
    """
    Execute Map Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.map_report import MapReportPlugin
    
    print("Running Niki-docAI Map Update (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for MetaComponent (Summaries)
    ctx.register_plugin(MapReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Map update failed: {e}")
        import traceback
        traceback.print_exc()
        return False
