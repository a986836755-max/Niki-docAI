"""
Command: Project Statistics.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="stats", help="Update project statistics (_STATS.md)", group="Diagnostics")
def run(config: ProjectConfig) -> bool:
    """
    Run stats update using ECS Kernel.
    Runs FileCollector, StatusPlugin, and StatsReportPlugin.
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.status import StatusPlugin
    from ndoc.plugins.stats_report import StatsReportPlugin
    
    print("Running Niki-docAI Statistics Update...")
    
    # Create a minimal kernel for stats
    ctx = KernelContext()
    
    # Register necessary plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(StatusPlugin())
    ctx.register_plugin(StatsReportPlugin())
    
    try:
        # Run pipeline
        # config.scan.root_path should be resolved
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Stats update failed: {e}")
        import traceback
        traceback.print_exc()
        return False
