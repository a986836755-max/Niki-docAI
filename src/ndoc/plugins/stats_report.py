"""
Stats Report Plugin (Action).
Generates _STATS.md from ECS data.
"""
from pathlib import Path
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import EntityType, MetaComponent
from ndoc.core.templates import render_document
from datetime import datetime

class StatsReportPlugin(ActionPlugin):
    """
    Action plugin to generate _STATS.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[StatsReport] Generating _STATS.md...")
        
        # 1. Calculate Metrics
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        total_files = len(files)
        
        # Mock lines count (In real app, we should store line count in SyntaxComponent)
        total_lines = 0
        total_size = 0
        
        src_files = 0
        doc_files = 0
        
        for f in files:
            try:
                # This is slow, ideally cached in Component
                stat = f.path.stat()
                total_size += stat.st_size
                
                # Check extension
                if f.path.suffix in ['.py', '.js', '.ts', '.rs', '.go', '.java', '.c', '.cpp']:
                    src_files += 1
                elif f.path.suffix in ['.md', '.txt', '.rst']:
                    doc_files += 1
                    
            except Exception:
                pass
                
        # 2. Render
        # We need to match stats.md.tpl variables
        # {total_files}, {total_lines}, {total_size_kb}, {estimated_tokens}
        # {ai_doc_files}, {ai_doc_lines}, {ai_estimated_tokens}, {ai_coverage}
        # {dirs_with_ai}, {total_dirs_scanned}
        # {src_files}, {src_lines}, {total_doc_files}, {total_doc_lines}, {ratio}
        # {health_ai_coverage}, {health_doc_ratio}
        
        doc = render_document(
            "stats.md.tpl",
            title="Project Statistics",
            context="Metrics",
            tags="@STATS",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_files=total_files,
            total_lines=total_lines, # Mocked
            total_size_kb=total_size / 1024,
            estimated_tokens=int(total_size / 4),
            ai_doc_files=0, # Mocked
            ai_doc_lines=0,
            ai_estimated_tokens=0,
            ai_coverage=0.0,
            dirs_with_ai=0,
            total_dirs_scanned=1,
            src_files=src_files,
            src_lines=0,
            total_doc_files=doc_files,
            total_doc_lines=0,
            ratio=0.0,
            health_ai_coverage="N/A",
            health_doc_ratio="N/A"
        )
        
        # 3. Write
        try:
            output_path = Path.cwd() / "_STATS.md"
        except Exception:
             if files:
                output_path = Path(files[0].path).parent / "_STATS.md"
             else:
                return

        output_path.write_text(doc, encoding="utf-8")
        print(f"[StatsReport] Written to: {output_path}")
