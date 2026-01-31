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
from ndoc.flows import map_flow, context_flow, tech_flow, todo_flow, deps_flow, config_flow, syntax_flow, doctor_flow, init_flow, verify_flow, clean_flow, stats_flow, update_flow, symbols_flow, plan_flow, archive_flow, data_flow
from ndoc.daemon import start_watch_mode
from ndoc.atoms import io

def main():
    """
    CLI 主入口 (CLI Main Entry).
    """
    description = """
Niki-docAI 2.0 (Rebirth) - AI Context Ops Toolchain

Core Commands (核心指令):
  init      : Initialize project structure (Create _RULES.md, _SYNTAX.md).
              ⚠️  Use --force to RESET configuration files (Overwrite existing).
  
  all       : Generate/Update ALL documentation (Recommended).
              (Map + Context + Tech + Todo + Deps)
              
  watch     : Start DAEMON mode to auto-update docs on file changes.
  
  update    : Self-update the tool (git pull).
  
  clean     : Clean/Reset generated documentation artifacts.
              ⚠️  DELETES all _AI.md, _MAP.md, etc.
              Usage: ndoc clean [target] (e.g. ndoc clean src/)

Diagnostics (诊断与维护):
  verify    : Verify documentation artifacts.
  doctor    : Diagnose environment and configuration health.
  stats     : Show project statistics.
  
  plan      : Plan and split an objective into tasks (LLM required).
              Usage: ndoc plan "Your Objective"
  
  archive   : Archive completed tasks and extract memory.

Granular Updates (单独更新):
  map       : Update Project Structure Map (_MAP.md).
  context   : Update Recursive Context (_AI.md).
  tech      : Update Tech Stack Snapshot (_TECH.md).
  todo      : Scan and aggregate Todos (_NEXT.md).
  deps      : Update Dependency Graph (_DEPS.md).
  symbols   : Generate Global Symbol Index (_SYMBOLS.md).
  data      : Generate Data Registry (_DATA.md).
  
  lsp       : Query symbol definitions and references.
              Usage: ndoc lsp <symbol_name>
"""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("command", choices=["map", "context", "tech", "todo", "deps", "symbols", "data", "all", "watch", "doctor", "init", "verify", "clean", "stats", "update", "plan", "archive", "lsp", "help"], help="Command to execute")
    parser.add_argument("target", nargs="?", help="Target file or directory (for clean command)")
    parser.add_argument("--root", default=".", help="Project root directory (Default: current dir)")
    parser.add_argument("--force", action="store_true", help="⚠️ Force execution (DANGER: Overwrite configs in init, Delete without confirm in clean)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing to disk")
    
    args = parser.parse_args()
    
    if args.command == "help":
        parser.print_help()
        sys.exit(0)
    
    root_path = Path(args.root).resolve()

    # Set Global Dry Run Mode
    if args.dry_run:
        io.set_dry_run(True)
        print("⚠️  DRY RUN MODE: No changes will be written to disk.")
    
    print(f"Starting Niki-docAI 2.0 in {root_path}")
    
    # 0. Handle Self-Update (No Config Needed)
    if args.command == "update":
        if update_flow.run():
            sys.exit(0)
        else:
            sys.exit(1)

    # 1. Ensure Configuration Files Exist (Documentation as Configuration)
    # Skip ensures for doctor command to diagnose raw state
    # Also skip for init, as init handles it explicitly
    if args.command not in ["doctor", "init"]:
        config_flow.ensure_rules_file(root_path)
        syntax_flow.run(ProjectConfig(scan=ScanConfig(root_path=root_path))) # Ensure syntax manual

    # 2. Load Configuration
    config = config_flow.load_project_config(root_path)
    
    success = True
    
    if args.command == "init":
        if init_flow.run(config, force=args.force):
            sys.exit(0)
        else:
            sys.exit(1)

    if args.command == "plan":
        if not args.target:
            print("❌ Error: 'plan' command requires an objective. Usage: ndoc plan \"Objective\"")
            sys.exit(1)
        if plan_flow.run(config, args.target):
            sys.exit(0)
        else:
            sys.exit(1)
            
    if args.command == "clean":
        if clean_flow.run(config, target=args.target, force=args.force):
            sys.exit(0)
        else:
            sys.exit(1)

    if args.command == "doctor":
        if doctor_flow.run(config):
            sys.exit(0)
        else:
            sys.exit(1)

    if args.command == "stats":
        if stats_flow.run(config, force=True):
            sys.exit(0)
        else:
            sys.exit(1)
            
    if args.command == "verify":
        if verify_flow.run(config):
            sys.exit(0)
        else:
            sys.exit(1)

    if args.command == "lsp":
        if not args.target:
            print("❌ Error: Missing symbol name. Usage: ndoc lsp <symbol_name>")
            sys.exit(1)
        
        from ndoc.atoms import lsp, fs
        print(f"🔍 Searching for symbol: {args.target}")
        lsp_service = lsp.get_service(root_path)
        files = fs.walk_files(root_path, config.scan.ignore_patterns)
        lsp_service.index_project(files)
        
        # Find Definitions
        defs = lsp_service.find_definitions(args.target)
        print(f"\n📍 Definitions ({len(defs)}):")
        for d in defs:
            # d is a Symbol object
            rel = Path(d.path).relative_to(root_path)
            print(f"  - {rel}:{d.line}  -> {d.signature or d.name}")
            
        # Find References
        refs = lsp_service.find_references(args.target)
        print(f"\n🔗 References ({len(refs)}):")
        for r in refs:
            rel = Path(r['path']).relative_to(root_path)
            print(f"  - {rel}:{r['line']}  -> {r['content']}")
        sys.exit(0)
    
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

    if args.command in ["archive", "all"]:
        # Archive is part of 'all' to maintain _MEMORY.md automatically
        print("Running Archive Flow...")
        if archive_flow.run(config):
            print("✅ Archive completed successfully.")
        else:
            if args.command == "archive": # Only fail if explicitly requested
                print("❌ Archive failed.")
                success = False
            else:
                print("ℹ️ Archive skipped or failed (non-critical for 'all').")

    if args.command in ["deps", "all"]:
        print("Running Deps Flow...")
        if deps_flow.run(config):
            print("✅ Dependency Graph updated successfully.")
        else:
            print("❌ Dependency Graph update failed.")
            success = False

    if args.command in ["symbols", "all"]:
        print("Running Symbols Flow...")
        if symbols_flow.run(config):
            print("✅ Symbol Index updated successfully.")
        else:
            print("❌ Symbol Index update failed.")
            success = False

    if args.command in ["data", "all"]:
        print("Running Data Flow...")
        if data_flow.run(config):
            print("✅ Data Registry updated successfully.")
        else:
            print("❌ Data Registry update failed.")
            success = False

    if args.command in ["stats", "all"]:
        # Stats is low priority, run last. Check interval internally.
        if stats_flow.run(config, force=False):
            pass # Stats failures shouldn't fail the build usually
        else:
            print("❌ Stats update failed.")
            
    if args.command == "watch":
        start_watch_mode(config)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
