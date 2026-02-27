"""
Dependency Report Plugin (Action).
Generates _DEPS.md using data from GraphComponents in ECS.
"""
from collections import defaultdict
from typing import Dict, Set
from ndoc.sdk.interfaces import ActionPlugin, hookimpl
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import GraphComponent
from ndoc.core.templates import render_document
from ndoc.core import graph as graph_algo
from ndoc.views import reports, mermaid
from datetime import datetime
from pathlib import Path

class DependencyReportPlugin(ActionPlugin):
    """
    Action plugin to generate _DEPS.md.
    """
    
    @hookimpl
    def ndoc_generate_docs(self, context: KernelContext):
        print("[DependencyReport] Generating _DEPS.md...")
        
        # 1. Reconstruct Graph from ECS
        # We need a dict format: { 'source': {'target1', 'target2'} }
        graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Query all entities with GraphComponent
        entities_with_deps = context.query(GraphComponent)
        
        for eid in entities_with_deps:
            comp = context.get_component(eid, GraphComponent)
            if comp and comp.imports:
                graph[eid] = set(comp.imports)
                
        if not graph:
            print("[DependencyReport] No dependencies found in Kernel.")
            return

        # 2. Calculate Metrics (Reuse existing logic)
        # Note: aggregation logic might need adjustment if Entity IDs are just file paths
        # builder.aggregate_graph expects paths like "src/ndoc/core/..."
        
        # Hack: Reuse builder's aggregate function if possible, or simple aggregation
        from ndoc.parsing.deps import builder
        agg_graph = builder.aggregate_graph(graph)
        metrics = graph_algo.calculate_metrics(agg_graph)
        
        # 3. Generate Views
        table = reports.generate_instability_table(metrics, is_core_func=builder.is_core_module)
        sorted_modules = sorted(metrics.keys())
        
        matrix = ""
        if len(sorted_modules) < 50:
            matrix = reports.generate_dependency_matrix(agg_graph, sorted_modules, is_core_func=builder.is_core_module)
        else:
            matrix = "*Matrix omitted due to size (> 50 modules).*"
            
        # Check cycles
        file_cycles = graph_algo.find_circular_dependencies(graph)
        
        cycle_report = ""
        if file_cycles:
            cycle_report += f"\n## ⚠️ Circular Dependencies (File Level)\n"
            cycle_report += f"**Found {len(file_cycles)} file-level circular dependencies**:\n"
            for cycle in file_cycles[:5]: 
                 cycle_report += f"   - `{' -> '.join(cycle)} -> {cycle[0]}`\n"
        
        # 4. Render Document
        # We need a core graph view too
        core_graph = mermaid.generate_mermaid_graph(agg_graph, metrics)
        
        # Calculate file metrics for full graph
        file_metrics = graph_algo.calculate_metrics(graph)
        full_graph = mermaid.generate_mermaid_graph(graph, file_metrics)
        
        doc = render_document(
            "deps.md.tpl",
            title="Dependency Analysis",
            context="Architecture & Dependencies",
            tags="@DEPS",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metrics_table=table,
            cycle_report=cycle_report,
            core_graph=core_graph,
            dependency_matrix=matrix,
            full_graph="*Full graph omitted in Pilot*" 
        )
        
        # 5. Write Output
        # Assume root is CWD for Pilot
        output_path = Path.cwd() / "_DEPS.md"
        output_path.write_text(doc, encoding="utf-8")
        print(f"[DependencyReport] Written to: {output_path}")
