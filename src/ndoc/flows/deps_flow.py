# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **RULE**: @LAYER(core) CANNOT_IMPORT @LAYER(ui) --> [context_flow.py:198](context_flow.py#L198)
# *   **RULE**: @FORBID(hardcoded_paths) --> [context_flow.py:199](context_flow.py#L199)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Dependency Graph Generation.
业务流：生成模块依赖图 (_DEPS.md)。
"""
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from ..core import io
from ..core.logger import logger
from ..models.config import ProjectConfig

# --- Imports from new Refactored Modules ---
from ..parsing.deps import builder
from ..core import graph as graph_algo
from ..views import mermaid, reports
from ..core.cli import ndoc_command
from ..core.templates import render_document

@ndoc_command(name="deps", help="Generate Dependency Graph (_DEPS.md)", group="Analysis")
def run(config: ProjectConfig, target: str = None) -> bool:
    """
    Execute Dependency Flow.
    :param target: Optional target directory to filter the dependency graph.
    """
    logger.info("Generating Dependency Graph...")
    root_path = config.scan.root_path
    
    # 1. Collect Imports & Build Graph
    import_map = builder.collect_imports(root_path, config)
    graph = builder.build_dependency_graph(import_map)
    
    # 3. Filter Graph (if target is provided)
    if target:
        target_path = Path(target).resolve()
        try:
            rel_target = target_path.relative_to(root_path).as_posix()
            logger.info(f"Filtering graph for target: {rel_target}")
            
            filtered_graph = defaultdict(set)
            nodes_in_scope = {n for n in graph.keys() if n.startswith(rel_target)}
            
            if not nodes_in_scope:
                logger.warning(f"No files found in target scope: {rel_target}")
                return False
                
            for source in nodes_in_scope:
                targets = graph.get(source, set())
                filtered_graph[source] = targets
            
            graph = filtered_graph
            target_file = target_path / "_DEPS.md"
            logger.info(f"Dependency Graph (Scoped) updated: {target_file}")
            
        except ValueError:
            logger.error(f"Error: Target {target} is not inside project root.")
            return False
    else:
        target_file = root_path / "_DEPS.md"
        logger.info(f"Dependency Graph updated: {target_file.name}")

    # Calculate Metrics
    agg_graph = builder.aggregate_graph(graph)
    metrics = graph_algo.calculate_metrics(agg_graph)
    
    # Generate Views
    table = reports.generate_instability_table(metrics, is_core_func=builder.is_core_module)
    sorted_modules = sorted(metrics.keys())
    
    matrix = ""
    if len(sorted_modules) < 50:
        matrix = reports.generate_dependency_matrix(agg_graph, sorted_modules, is_core_func=builder.is_core_module)
    else:
        matrix = "*Matrix omitted due to size (> 50 modules).*"

    # Check for circular dependencies
    file_cycles = graph_algo.find_circular_dependencies(graph)
    mod_cycles = graph_algo.find_circular_dependencies(agg_graph)
    
    cycle_report = ""
    if file_cycles:
        cycle_report += f"\n## ⚠️ Circular Dependencies (File Level)\n"
        cycle_report += f"**Found {len(file_cycles)} file-level circular dependencies** (Potential Deadlocks):\n"
        for cycle in file_cycles[:5]: 
            path_cycle = [Path(c).name for c in cycle]
            cycle_report += f"   - `{' -> '.join(path_cycle)} -> {path_cycle[0]}`\n"
        if len(file_cycles) > 5:
            cycle_report += "   - ... (see logs for full list)\n"
            
    if mod_cycles:
        cycle_report += f"\n## ⚠️ Circular Dependencies (Module Level)\n"
        cycle_report += f"**Found {len(mod_cycles)} module-level circular dependencies** (Architectural Issues):\n"
        for cycle in mod_cycles[:5]:
            cycle_report += f"   - `{' -> '.join(cycle)} -> {cycle[0]}`\n"
        if len(mod_cycles) > 5:
            cycle_report += "   - ... (see logs for full list)\n"

    # Generate Two Mermaid Graphs
    mermaid_core = mermaid.generate_mermaid_graph(agg_graph, metrics, core_only=True, is_core_func=builder.is_core_module)
    mermaid_full = mermaid.generate_mermaid_graph(agg_graph, metrics, core_only=False)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = render_document(
        "deps.md.tpl",
        title="Dependency Graph",
        context="Dependencies | Graph",
        tags="",
        timestamp=timestamp,
        metrics_table=table,
        cycle_report=cycle_report,
        core_graph=mermaid_core,
        dependency_matrix=matrix,
        full_graph=mermaid_full
    )
    
    io.write_text(target_file, content)
    return True
