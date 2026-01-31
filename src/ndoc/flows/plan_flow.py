"""
Flow: Project Planning.
业务流：项目规划。根据目标自动拆解任务并更新 _NEXT.md。
"""
from pathlib import Path
from datetime import datetime
from ..atoms import io, llm, fs
from ..models.config import ProjectConfig

PLAN_SYSTEM_PROMPT = """
You are a senior software architect and project manager. 
Your task is to take a high-level "Objective" and break it down into actionable tasks for a developer.
These tasks will be added to the project's `_NEXT.md` roadmap.

Rules:
1. Keep tasks specific and actionable.
2. Group tasks logically into a new section.
3. Use Markdown format with checkboxes: * [ ] #task-id: description.
4. Each task MUST have a unique `#task-id` (e.g., #refactor-auth, #ui-login).
5. Output ONLY the new section content in Markdown, starting with a level 3 header `###`.

Current context:
You are working on Niki-docAI, a tool that generates documentation context for AI assistants.
"""

def run(config: ProjectConfig, objective: str) -> bool:
    """
    Execute Plan Flow.
    """
    if not objective:
        print("❌ Error: No objective provided for planning.")
        return False

    next_file = config.scan.root_path / "_NEXT.md"
    map_file = config.scan.root_path / "_MAP.md"
    
    # 1. Gather Context (Map + Next)
    project_map = ""
    if map_file.exists():
        project_map = io.read_text(map_file)[:2000] # Limit context
    
    current_next = ""
    if next_file.exists():
        current_next = io.read_text(next_file)
    
    # 2. Build Prompt
    prompt = f"""
Objective: {objective}

Project Structure Summary:
{project_map}

Current Roadmap (_NEXT.md):
{current_next}

Please provide a new section of tasks to achieve the Objective. 
Make sure the Task IDs are new and do not conflict with existing ones in _NEXT.md.
"""

    print(f"🤔 Planning for objective: '{objective}'...")
    
    # 3. Call LLM
    result = llm.call_llm(prompt, system_prompt=PLAN_SYSTEM_PROMPT)
    
    if not result:
        print("❌ Planning failed: LLM returned no result.")
        return False
    
    # 4. Update _NEXT.md
    # We'll append the new section before the @HISTORY or at the end of @CURRENT
    if not next_file.exists():
        # Create a basic structure if missing
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"# PROJECT ROADMAP\n> Last Updated: {timestamp}\n\n## @CURRENT\n\n{result}\n"
        return io.write_text(next_file, content)
    
    # Logic to insert before @PLAN or @HISTORY or just append to @CURRENT
    content = io.read_text(next_file)
    
    # Simple insertion: after ## @CURRENT
    marker = "## @CURRENT"
    if marker in content:
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n\n" + result + "\n" + parts[1]
    else:
        # Just append
        new_content = content + "\n\n" + result + "\n"
    
    success = io.write_text(next_file, new_content)
    if success:
        io.update_header_timestamp(next_file)
        print(f"✅ Project Roadmap updated with new plan for: {objective}")
    
    return success
