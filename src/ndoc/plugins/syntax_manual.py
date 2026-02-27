"""
Syntax Manual Plugin (Action).
Generates _SYNTAX.md (Syntax Manual) if missing.
Ported from syntax_flow.
"""
from pathlib import Path
from ndoc.sdk.interfaces import ActionPlugin
from ndoc.kernel.context import KernelContext
from ndoc.core.templates import render_document
from datetime import datetime
from ndoc.core import io

class SyntaxManualPlugin(ActionPlugin):
    """
    Action plugin to ensure _SYNTAX.md exists.
    """
    
    def ndoc_generate_docs(self, context: KernelContext):
        # We need to know where the root is.
        # Assuming we can find it from entities or CWD
        try:
            root = Path.cwd()
        except Exception:
            return

        syntax_file = root / "_SYNTAX.md"
        
        # Simple strategy: Write if missing.
        if not syntax_file.exists():
            print(f"[SyntaxManual] Creating Syntax Manual at {syntax_file.name}...")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = render_document(
                "syntax.md.tpl",
                title="PROJECT SYNTAX",
                context="DSL 定义 | @TAGS: @SYNTAX @OP",
                tags="",
                timestamp=timestamp
            )
            io.write_text(syntax_file, content)
            print(f"[SyntaxManual] Created: {syntax_file}")
        else:
            # print(f"[SyntaxManual] Exists: {syntax_file}")
            pass
