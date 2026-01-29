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
from ndoc.flows import map_flow

def main():
    """
    CLI 主入口 (CLI Main Entry).
    """
    parser = argparse.ArgumentParser(description="Niki-docAI 2.0 (Rebirth)")
    parser.add_argument("command", choices=["map", "all"], help="Command to execute")
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
        if map_flow.update_map_doc(config):
            print("✅ Map updated successfully.")
        else:
            print("❌ Map update failed.")
            success = False
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
