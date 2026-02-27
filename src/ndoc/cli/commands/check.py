"""
Command: Check Constraints.
"""
from typing import Optional
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="check", help="Check code for constraint violations (!RULE)", group="Diagnostics")
def run(config: ProjectConfig, target: Optional[str] = None) -> bool:
    """
    Run the constraint checker (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.scanner import SyntaxAnalysisPlugin
    from ndoc.plugins.checker import ConstraintCheckerPlugin
    
    print("Running Niki-docAI Constraint Checker (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(SyntaxAnalysisPlugin()) # Required for Symbols/Imports/Memories
    ctx.register_plugin(ConstraintCheckerPlugin())
    
    # Note: 'target' parameter is not easily passed to run_pipeline yet.
    # run_pipeline takes 'root_path'.
    # If target is a specific file/dir, we should set it as root_path or filter in collector?
    # FileCollectorPlugin takes root_path.
    # So if target is provided, we use it as root_path for the pipeline.
    
    scan_root = target if target else str(config.scan.root_path)
    
    try:
        run_pipeline(ctx, scan_root)
        return True
    except Exception as e:
        print(f"❌ Check failed: {e}")
        import traceback
        traceback.print_exc()
        return False
