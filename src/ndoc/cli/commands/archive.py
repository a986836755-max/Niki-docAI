"""
Command: Archive.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="archive", help="Archive completed tasks and extract memory", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """
    Execute Archive Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.memory_report import MemoryReportPlugin
    
    print("Running Niki-docAI Memory Archive (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for MemoryComponent
    ctx.register_plugin(MemoryReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Archive failed: {e}")
        import traceback
        traceback.print_exc()
        return False
