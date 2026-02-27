# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#

# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Command: Capabilities.
"""
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="caps", help="Manage project capabilities", group="Core")
def run(config: ProjectConfig, auto_install: bool = True) -> bool:
    """
    Manage project capabilities (ECS Architecture).
    """
    from ndoc.kernel.context import KernelContext
    from ndoc.kernel.bootstrap import run_pipeline
    from ndoc.plugins.collector import FileCollectorPlugin
    from ndoc.plugins.capability_map import CapabilityMapPlugin
    
    print("Running Niki-docAI Capability Check (ECS)...")
    
    ctx = KernelContext()
    
    # Register Plugins
    ctx.register_plugin(FileCollectorPlugin())
    ctx.register_plugin(CapabilityMapPlugin())
    
    try:
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Capability check failed: {e}")
        import traceback
        traceback.print_exc()
        return False
