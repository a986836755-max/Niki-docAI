"""
Command: Impact Analysis.
"""
from pathlib import Path
from typing import List, Set, Dict, Optional
from datetime import datetime

from ndoc.models.config import ProjectConfig
from ndoc.core.cli import ndoc_command
from ndoc.core.templates import render_document
from ndoc.services.impact_service import ImpactService
from ndoc.kernel.bootstrap import create_kernel, run_analysis_phase

@ndoc_command(name="impact", help="Analyze impact of changed files (Git aware)", group="Analysis")
def run(config: ProjectConfig) -> bool:
    """
    Run Impact Analysis.
    """
    root = config.scan.root_path
    
    # 1. Initialize Kernel (Analysis only)
    # We need to collect files and resolve dependencies to build the graph.
    ctx = create_kernel(include_actions=False)
    
    # Run analysis phase to populate dependency graph
    ctx = run_analysis_phase(ctx, str(root))
    
    # 2. Initialize Service
    service = ImpactService(ctx, root)
    
    # 3. Get Changes
    changed_files = service.get_changed_files()
    
    if not changed_files:
        print("No changes detected via Git.")
        return True
        
    print(f"Changed files ({len(changed_files)}):")
    for f in changed_files[:5]:
        print(f" - {f}")
    if len(changed_files) > 5:
        print(" ...")

    # 4. Analyze Impact
    result = service.analyze_impact(changed_files)
    
    impacted_modules = result.get("impacted_modules", [])
    
    if not impacted_modules:
        print("✅ No downstream impact detected (or dependencies not resolved).")
        return True
        
    print(f"⚠️  Impact Detected: {len(impacted_modules)} modules potentially affected.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    changed_list = "\n".join([f"- `{f}`" for f in sorted(changed_files)])
    impacted_list = "\n".join([f"- `{m}`" for m in sorted(impacted_modules)])
    
    # Render report
    try:
        report = render_document(
            "impact.md.tpl",
            title="Impact Analysis Report",
            context="Impact | Git Changes",
            tags="",
            timestamp=timestamp,
            changed_files_list=changed_list,
            impacted_modules_list=impacted_list
        )
        print("\n" + report)
    except Exception as e:
        print(f"Failed to render report: {e}")
        print("\nImpacted Modules:")
        print(impacted_list)
    
    return True
