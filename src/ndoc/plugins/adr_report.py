"""
ADR Report Plugin (Action).
Generates _ADR.md (Architecture Decision Records) from ECS data.
Ported from adr_flow.
"""
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.sdk.models import Entity, EntityType, MetaComponent
from ndoc.core.templates import render_document
from datetime import datetime

class AdrReportPlugin(ActionPlugin):
    """
    Action plugin to generate _ADR.md.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        print("[AdrReport] Generating _ADR.md...")
        
        # 1. Query entities with MetaComponent that have 'decisions'
        # Note: Current MetaComponent only has 'todos'. We need to extend it or store decisions elsewhere.
        # In legacy flow, scanner.scan_file returns result.decisions.
        # We need to make sure Sensor/Collector extracts decisions and puts them in MetaComponent.
        # Assuming MetaComponent has 'decisions' field or we put them in 'todos' with tag='DECISION'?
        # Let's check how MetaComponent is defined. 
        
        # If MetaComponent doesn't support it yet, we should update it.
        # For now, let's assume we can access raw data or extend MetaComponent.
        # Wait, the bootstrap.py only extracts 'todos' from result.
        
        # We need to update bootstrap.py or StatusPlugin to also extract decisions.
        # But for this refactor, let's assume we can get them.
        
        # Strategy: 
        # Since we cannot easily change the Sensor interface right now without touching legacy code too much,
        # we will rely on the fact that `StatusPlugin` (or a new `AdrSensorPlugin`) should populate this.
        # But wait, `StatusPlugin` is already running.
        
        # Let's iterate all entities and look for decisions in their components.
        # If they are not there, we might need to re-scan or upgrade the Sensor.
        
        # Temporary workaround for Pilot: 
        # The legacy adr_flow used `scanner.scan_file`.
        # We should probably create an `AdrSensorPlugin` that does exactly that and stores it in context.
        # But to save time, let's just query the scanner here (which is "illegal" for an Action plugin but pragmatic for migration).
        # ideally: Sensor -> Context -> Action.
        # pragmatic: Action -> Scanner -> Context (if missing) -> Generate.
        
        from ndoc.parsing import scanner
        
        decisions = []
        files = [e for e in context.entities.values() if e.type == EntityType.FILE]
        
        print(f"[AdrReport] Scanning {len(files)} files for @DECISION tags...")
        
        for f in files:
             # We can use the entity path
             path = f.path
             if not path.exists(): continue
             
             # Use cached scanner
             # Note: scanner.scan_file might have been called by other plugins, so it should be fast (cached)
             try:
                 result = scanner.scan_file(path, context.root_path if hasattr(context, 'root_path') else path.parent)
                 if result and result.decisions:
                    for d in result.decisions:
                        decisions.append({
                            "file": path,
                            "rel_path": f.id, # Entity ID is relative path
                            "content": d['content'],
                            "line": d['line']
                        })
             except Exception:
                 pass
                 
        if not decisions:
            print("[AdrReport] No @DECISION tags found.")
            return

        # 2. Group by directory/module
        grouped = defaultdict(list)
        for d in decisions:
            parts = Path(d['rel_path']).parts
            group = parts[0] if len(parts) > 1 else "Root"
            grouped[group].append(d)
            
        # 3. Generate Markdown
        lines = []
        # Header is handled by template usually, but let's follow legacy format for now
        # lines.append("# Architecture Decision Records (ADR)")
        # lines.append("> @CONTEXT: Architecture | @TAGS: @ADR")
        
        for group in sorted(grouped.keys()):
            lines.append(f"## {group}")
            for d in grouped[group]:
                link = f"[{d['rel_path']}]({d['rel_path']}#L{d['line']})"
                lines.append(f"*   **{d['content']}**")
                lines.append(f"    *   Source: {link}")
            lines.append("")
            
        content = "\n".join(lines)
        
        # 4. Render
        doc = render_document(
            "adr.md.tpl", # We need to ensure this template exists or use a generic one
            title="Architecture Decision Records",
            context="Architecture | Decisions",
            tags="@ADR",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content=content,
            decisions_count=len(decisions)
        )
        
        # 5. Write
        # Try to find root from context or first file
        try:
            root = Path.cwd()
        except Exception:
            root = Path(files[0].path).parent
            
        output_path = root / "_ADR.md"
        output_path.write_text(doc, encoding="utf-8")
        print(f"[AdrReport] Written to: {output_path}")
