"""
Command: Architecture Decision Records (ADR).
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="adr", help="Generate ADR Report (_ADR.md)", group="Knowledge")
def run(config: ProjectConfig) -> bool:
    """
    Execute ADR Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.adr_report import AdrReportPlugin
    
    print("Running Niki-docAI ADR Generation (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for MetaComponent (Tags)
    ctx.register_plugin(AdrReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ ADR generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
