"""
Command: Context.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="context", help="Generate Recursive Context (_AI.md)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Execute Context Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.context_report import ContextReportPlugin
    
    print("Running Niki-docAI Context Update (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin())
    ctx.register_plugin(ContextReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Context update failed: {e}")
        import traceback
        traceback.print_exc()
        return False
