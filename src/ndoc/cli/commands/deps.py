"""
Command: Dependencies.
"""
from typing import Optional
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="deps", help="Generate Dependency Graph (_DEPS.md)", group="Analysis")
def run(config: ProjectConfig, target: Optional[str] = None) -> bool:
    """
    Execute Dependency Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.deps_report import DependencyReportPlugin
    
    print("Running Niki-docAI Dependency Analysis (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for GraphComponent (Imports)
    ctx.register_plugin(DependencyReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Dependency analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
