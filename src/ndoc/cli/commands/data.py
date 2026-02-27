"""
Command: Data Schema Registry.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="data", help="Generate Data Schema Registry (_DATA.md)", group="Knowledge")
def run(config: ProjectConfig) -> bool:
    """
    Execute Data Schema Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.data_schema import DataSchemaPlugin
    
    print("Running Niki-docAI Data Registry Generation (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for SymbolComponent
    ctx.register_plugin(DataSchemaPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Data registry generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
