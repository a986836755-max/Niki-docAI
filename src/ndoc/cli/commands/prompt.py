"""
Command: AI Prompt.
"""
from pathlib import Path
from ndoc.models.config import ProjectConfig
from ndoc.core.cli import ndoc_command
from ndoc.services.prompt_service import PromptService
from ndoc.kernel.bootstrap import create_kernel, run_analysis_phase

@ndoc_command(name="prompt", help="Generate semantic context prompt for AI (Vector Search)", group="Analysis")
def run(config: ProjectConfig, target: str, focus: bool = False) -> bool:
    """
    Generate context prompt for a file.
    """
    root = config.scan.root_path
    target_path = Path(target).resolve()
    
    if not target_path.exists():
        print(f"Error: File not found: {target}")
        return False
        
    # 1. Initialize Kernel (Analysis only)
    # We need to resolve dependencies to find related APIs.
    ctx = create_kernel(include_actions=False)
    
    # Run analysis phase to populate dependency graph
    ctx = run_analysis_phase(ctx, str(root))
    
    # 2. Initialize Service
    service = PromptService(ctx, root)
    
    # 3. Generate Prompt
    prompt = service.generate_prompt(target_path, focus)
    
    print("-" * 20 + " AI CONTEXT START " + "-" * 20)
    print(prompt)
    print("-" * 20 + " AI CONTEXT END " + "-" * 20)
    return True
