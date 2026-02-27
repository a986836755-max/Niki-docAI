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
Flow: Prompt Generation (AI Thinking Context).
业务流：为 AI 生成思考所需的上下文 Prompt。
"""
from pathlib import Path

from ..core import io
from ..parsing import rules as parsing_rules
from ..parsing.ast import skeleton
from ..parsing.deps import api_extractor
from ..models.config import ProjectConfig
from ..core.cli import ndoc_command
from ..core.templates import get_template

def get_context_prompt(file_path: str, config: ProjectConfig, focus: bool = False, use_skeleton: bool = False) -> str:
    """
    生成针对特定文件的上下文 Prompt。
    支持 Focus Mode: 只返回最相关的 5% 上下文。
    """
    root = config.scan.root_path
    target = root / file_path
    
    if not target.exists():
        return f"Error: File not found: {file_path}"

    target_path = target.resolve()
    
    # 1. Target Code (Skeleton or Full)
    target_code = ""
    if target_path.exists():
        raw_content = io.read_text(target_path)
        if raw_content:
            if use_skeleton:
                target_code = skeleton.generate_skeleton(raw_content, str(target_path))
            else:
                target_code = raw_content
    else:
        target_code = "(File not found)"

    # 2. Global Rules (Condensed)
    global_rules = parsing_rules.extract_global_rules(root)
    
    # 3. Syntax (Condensed)
    syntax_summary = parsing_rules.extract_syntax_summary(root)
    
    # 4. Domain Context (Nearest _AI.md)
    domain_context = parsing_rules.extract_domain_context(target_path, root)
    
    # 5. Related APIs (Imports)
    related_apis = api_extractor.extract_related_apis(target_path, config)
    
    # 6. Semantic Context (VectorDB)
    semantic_context = ""
    if focus:
        # Use Vector DB to find relevant snippets
        from ..brain.vectordb import VectorDB
        db = VectorDB(root)
        
        related_snippets = []
        if db.collection:
            # Query using file content or name
            query = target_path.name
            if target_path.exists() and io.read_text(target_path):
                query = io.read_text(target_path)[:500] # Use first 500 chars
                
            results = db.search(query, n_results=5)
            if results:
                related_snippets.append("## Related Context (Semantic Search)")
                for res in results:
                    path = res.get('id', 'unknown')
                    content = res.get('document', '')
                    # Truncate content
                    preview = content[:300] + "..." if len(content) > 300 else content
                    related_snippets.append(f"### {path}\n```\n{preview}\n```")
        
        if related_snippets:
            semantic_context = "\n".join(related_snippets)

    # Render Template
    template = get_template("prompt.md.tpl")
    return template.format(
        target_file=str(target_path.relative_to(root)),
        global_rules=global_rules,
        domain_context=domain_context,
        syntax_summary=syntax_summary,
        related_apis=related_apis,
        semantic_context=semantic_context,
        target_code=target_code
    )

@ndoc_command(name="prompt", help="Generate semantic context prompt for AI (Vector Search)", group="Analysis")
def run(file_path: str, config: ProjectConfig, focus: bool = False) -> bool:
    """
    打印 Prompt Context 到标准输出。
    """
    path = Path(file_path)
    prompt = get_context_prompt(path, config, focus)
    
    print("-" * 20 + " AI CONTEXT START " + "-" * 20)
    print(prompt)
    print("-" * 20 + " AI CONTEXT END " + "-" * 20)
    return True
