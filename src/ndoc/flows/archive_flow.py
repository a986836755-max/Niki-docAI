"""
Flow: Project Archiving & Memory.
业务流：项目归档与记忆提取。将已完成任务移入历史并提取关键决策。
"""
import re
from datetime import datetime
from pathlib import Path
from ..atoms import io, llm
from ..models.config import ProjectConfig

def run(config: ProjectConfig) -> bool:
    """
    Execute Archive Flow.
    """
    next_file = config.scan.root_path / "_NEXT.md"
    memory_file = config.scan.root_path / "_MEMORY.md"
    
    if not next_file.exists():
        return False

    content = io.read_text(next_file)
    if not content:
        return False

    # 1. Identify completed tasks/sections
    # For simplicity, we look for level 3 headers (###) where all items are [x]
    # Use a more robust split that captures the header
    sections = re.split(r'\n(###\s+.*)', content)
    
    header = sections[0]
    remaining_sections = []
    archived_content = []
    
    for i in range(1, len(sections), 2):
        section_title = sections[i]
        # Body is the next element, but might contain subsequent ### if split was weird
        section_body = sections[i+1] if i+1 < len(sections) else ""
        
        # Check if all tasks in this section are completed
        # Find all checkboxes: [ ] or [x]
        tasks = re.findall(r'\[( |x)\]', section_body)
        
        if tasks and all(t == 'x' for t in tasks):
            print(f"📦 Archiving completed section: {section_title.strip()}")
            archived_content.append(f"{section_title}{section_body}")
        else:
            remaining_sections.append(f"{section_title}{section_body}")

    if not archived_content:
        print("ℹ️ No fully completed sections to archive.")
        return True

    # 2. Update _NEXT.md
    new_next_content = header + "\n" + "\n".join(remaining_sections)
    
    # Add to @HISTORY section in _NEXT.md
    history_marker = "## @HISTORY"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    archive_block = f"\n#### Archived on {timestamp}\n" + "\n".join(archived_content)
    
    if history_marker in new_next_content:
        parts = new_next_content.split(history_marker, 1)
        new_next_content = parts[0] + history_marker + "\n" + archive_block + parts[1]
    else:
        new_next_content += f"\n\n{history_marker}\n" + archive_block

    io.write_text(next_file, new_next_content)
    io.update_header_timestamp(next_file)

    # 3. Memory Extraction (Optional LLM Step)
    _extract_memory(config, archived_content, memory_file)

    return True

def _extract_memory(config: ProjectConfig, archived_content: list, memory_file: Path):
    """
    Extract key decisions and learnings from archived content using LLM.
    """
    if not archived_content:
        return

    print("🧠 Extracting memory from archived tasks...")
    
    prompt = f"""
Below are recently completed and archived tasks from the project roadmap.
Please extract key technical decisions, architectural changes, or "lessons learned" into a concise summary.
Format the output as Markdown bullets.

Archived Content:
{"".join(archived_content)}
"""
    
    system_prompt = "You are a project historian. Focus on 'Why' and 'How' certain things were built, not just 'What'."
    
    summary = llm.call_llm(prompt, system_prompt=system_prompt)
    if not summary:
        return

    # Update _MEMORY.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n### Memory Update ({timestamp})\n{summary}\n"
    
    if not memory_file.exists():
        header = "# PROJECT MEMORY\n> @CONTEXT: Architectural Decisions & Learnings\n"
        io.write_text(memory_file, header + entry)
    else:
        current_memory = io.read_text(memory_file)
        io.write_text(memory_file, current_memory + "\n" + entry)
    
    print(f"✅ Memory updated in {memory_file.name}")
