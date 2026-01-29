"""
Entry Point: CLI Execution.
入口：CLI 执行。
"""
import argparse
import sys
from pathlib import Path

# 添加 src 到 sys.path 以便直接运行
sys.path.insert(0, str(Path(__file__).parent.parent))

from ndoc.models.config import ProjectConfig, ScanConfig
from ndoc.flows import map_flow, context_flow, tech_flow, todo_flow
from ndoc.daemon import start_watch_mode

def main():
    """
    CLI 主入口 (CLI Main Entry).
    """
    parser = argparse.ArgumentParser(description="Niki-docAI 2.0 (Rebirth)")
    parser.add_argument("command", choices=["map", "context", "tech", "todo", "all", "watch"], help="Command to execute")
    parser.add_argument("--root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    root_path = Path(args.root).resolve()
    
    # 构建配置 (Build Config)
    # 暂时使用硬编码的默认配置，后续可以从 ndoc.toml 加载
    config = ProjectConfig(
        scan=ScanConfig(root_path=root_path),
        name=root_path.name
    )
    
    print(f"Starting Niki-docAI 2.0 in {root_path}")
    
    success = True
    
    if args.command in ["map", "all"]:
        print("Running Map Flow...")
        # Update: Use 'run' instead of 'update_map_doc' to match DOD convention
        if map_flow.run(config):
            print("✅ Map updated successfully.")
        else:
            print("❌ Map update failed.")
            success = False

    if args.command in ["context", "all"]:
        print("Running Context Flow...")
        if context_flow.run(config):
            print("✅ Context updated successfully.")
        else:
            print("❌ Context update failed.")
            success = False

    if args.command in ["tech", "all"]:
        print("Running Tech Flow...")
        if tech_flow.run(config):
            print("✅ Tech Stack updated successfully.")
        else:
            print("❌ Tech Stack update failed.")
            success = False

    if args.command in ["todo", "all"]:
        print("Running Todo Flow...")
        if todo_flow.run(config):
            print("✅ Todo updated successfully.")
        else:
            print("❌ Todo update failed.")
            success = False
            
    if args.command == "watch":
        start_watch_mode(config)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
