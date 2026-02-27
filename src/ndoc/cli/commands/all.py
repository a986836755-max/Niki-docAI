"""
Command: Run All Analysis (ECS Pipeline).
"""
from pathlib import Path
from ndoc.core.cli import ndoc_command
from ndoc.models.config import ProjectConfig

@ndoc_command(name="all", help="Generate/Update ALL documentation (Recommended)", group="Core")
def run(config: ProjectConfig) -> bool:
    """
    Run the full ECS pipeline.
    """
    from ndoc.kernel.bootstrap import create_kernel, run_pipeline
    
    print("Running Niki-docAI Full Analysis (ECS Kernel)...")
    
    try:
        ctx = create_kernel()
        # Resolve path to absolute
        # config.scan.root_path should be already resolved by config loader
        run_pipeline(ctx, str(config.scan.root_path))
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
