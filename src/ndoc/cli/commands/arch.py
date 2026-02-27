"""
Command: Architecture.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="arch", help="Generate Architecture Overview (_ARCH.md)", group="Granular")
def run(config: ProjectConfig) -> bool:
    """
    Execute Arch Flow (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.arch_report import ArchitectureReportPlugin
    
    print("Running Niki-docAI Architecture Overview (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(ArchitectureReportPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Architecture overview failed: {e}")
        import traceback
        traceback.print_exc()
        return False
