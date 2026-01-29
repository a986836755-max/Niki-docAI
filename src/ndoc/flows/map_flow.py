"""
Flow: Map Generation.
业务流：生成项目结构图 (_MAP.md)。
"""
from pathlib import Path
from typing import List

from ndoc.atoms import fs, io
from ndoc.models.config import ProjectConfig

def generate_tree(root: Path, config: ProjectConfig) -> str:
    """
    生成目录树字符串 (Generate directory tree string).
    
    Args:
        root: 根目录
        config: 项目配置
        
    Returns:
        str: Markdown 格式的目录树
    """
    lines = []
    
    # 1. 获取所有文件 (Get all files)
    # 我们需要先遍历得到结构，然后构建树
    # 为了简单起见，这里我们再次使用 fs.walk_files，但为了构建树状结构，
    # 我们可能需要自定义的遍历逻辑，或者对路径列表进行后处理。
    # 这里我们采用“先获取路径，再构建树”的策略，这样可以复用 fs.walk_files 的过滤逻辑。
    
    # 注意：fs.walk_files 返回的是文件路径。我们需要目录结构。
    # 所以我们需要一个能返回目录的遍历器，或者修改 fs.walk_files。
    # 让我们直接使用 fs.walk_files 并推导目录结构。
    
    all_paths = sorted(list(fs.walk_files(root, config.scan.ignore_patterns, config.scan.extensions)))
    
    if not all_paths:
        return "* (No files found)"

    # 构建树结构 (Build tree structure)
    # 这是一个简化版的树生成，仅展示文件和目录
    
    # 使用 set 存储所有需要显示的目录，包括中间目录
    dirs_to_show = set()
    files_to_show = []
    
    for p in all_paths:
        rel = p.relative_to(root)
        files_to_show.append(rel)
        # 添加所有父目录
        for parent in rel.parents:
            if parent != Path('.'):
                dirs_to_show.add(parent)
                
    # 排序目录
    sorted_dirs = sorted(list(dirs_to_show))
    
    # 简单的一层一层输出可能比较乱，我们尝试直接按行输出
    # 更好的方法是递归打印，但我们需要复用 fs 的忽略逻辑。
    # 让我们换一种方式：递归遍历，但使用 fs.should_ignore 检查。
    
    return _recursive_tree(root, root, config.scan.ignore_patterns)

def _recursive_tree(current_path: Path, root: Path, ignore_patterns: List[str], level: int = 0) -> str:
    """
    递归生成树 (Recursive tree generation).
    """
    indent = "    " * level
    lines = []
    
    # 获取当前目录下的条目
    try:
        entries = sorted(list(current_path.iterdir()), key=lambda x: (x.is_file(), x.name))
    except PermissionError:
        return ""

    for entry in entries:
        if fs.should_ignore(entry.name, ignore_patterns):
            continue
            
        rel_path = fs.get_relative_path(entry, root)
        
        if entry.is_dir():
            # 目录
            lines.append(f"{indent}*   **{entry.name}/**")
            # 递归
            lines.append(_recursive_tree(entry, root, ignore_patterns, level + 1))
        else:
            # 文件
            # 检查扩展名（如果配置了）- 这里暂时跳过，假设 ignore_patterns 已经够了，
            # 或者我们需要传入 extensions。
            # 为了保持一致性，我们应该在这里也检查 extensions，但在 map 中通常显示所有非忽略文件。
            lines.append(f"{indent}*   `{entry.name}`")
            
    return "\n".join(filter(None, lines))

def update_map_doc(config: ProjectConfig) -> bool:
    """
    更新 _MAP.md 文件 (Update _MAP.md file).
    
    Args:
        config: 项目配置
        
    Returns:
        bool: 是否成功
    """
    map_file = config.scan.root_path / "_MAP.md"
    if not map_file.exists():
        print(f"_MAP.md not found at {map_file}")
        return False
        
    print(f"Generating project tree for {config.name}...")
    tree_content = generate_tree(config.scan.root_path, config)
    
    # 标记定义
    start_marker = "<!-- NIKI_MAP_START -->"
    end_marker = "<!-- NIKI_MAP_END -->"
    
    return io.update_section(map_file, start_marker, end_marker, tree_content)
