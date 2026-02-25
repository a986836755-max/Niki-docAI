# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
#
# [Local Rules] (_AI.md)
# *   **Proactive Capability Check**: `entry.py` serves as the primary gatekeeper. It must invoke `capability_flow` to ...
# *   **Dynamic Watchdog**: `daemon.py` monitors file system events. When a new file type is detected (e.g., a `.rs` fi...
# *   **CLI Robustness**: All CLI commands (including `lsp`) must handle missing capabilities gracefully, either by att...
# *   **LSP Protocol Integrity**: `entry.py`'s `server` command MUST NOT print anything to `stdout` other than JSON-RPC...
# *   **Context Awareness**: `lsp_server.py` implements "Thinking Context" via `textDocument/hover`, aggregating rules ...
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
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
from ndoc import lsp_server
from ndoc.flows import (
    context_flow, 
    config_flow, 
    syntax_flow, 
    doctor_flow, 
    init_flow, 
    verify_flow, 
    clean_flow, 
    stats_flow, 
    update_flow, 
    plan_flow, 
    archive_flow, 
    data_flow, 
    capability_flow, 
    prompt_flow, 
    inject_flow, 
    check_flow, 
    arch_flow, 
    status_flow, 
    adr_flow, 
    mind_flow, 
    lesson_flow,
    deps_flow,
    impact_flow,
)
from ndoc.daemon import start_watch_mode
from ndoc.atoms import io
from ndoc.parsing.ast import skeleton

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
              (Arch + Context + Status + Data + Deps)
              
  watch     : Start DAEMON mode to auto-update docs on file changes.
  
  update    : Self-update the tool (git pull).
  
  clean     : Clean/Reset generated documentation artifacts.
              ⚠️  DELETES all _AI.md, _ARCH.md, etc.
              Usage: ndoc clean [target] (e.g. ndoc clean src/)

Analysis & Insights (分析与洞察):
  deps      : Generate Dependency Graph (_DEPS.md) and check for circular dependencies.
  impact    : Analyze impact of changed files (Git aware).
  skeleton  : Generate semantic skeleton of a file.
              Usage: ndoc skeleton <file_path>

Diagnostics (诊断与维护):
  check     : Check code for constraint violations (!RULE).
              Usage: ndoc check [target]
  verify    : Verify documentation artifacts.
  doctor    : Diagnose environment and configuration health.
  stats     : Show project statistics (Merged into status).
  
  plan      : Plan and split an objective into tasks (LLM required).
              Usage: ndoc plan "Your Objective"
  
  archive   : Archive completed tasks and extract memory.

Granular Updates (单独更新):
  arch      : Update Architecture Overview (_ARCH.md).
  context   : Update Recursive Context (_AI.md).
  status    : Update Status Board (_STATUS.md).
  data      : Generate Data Registry (_DATA.md).
  inject    : Inject context headers into source files.
              Usage: ndoc inject [file/dir]
  
  lsp       : Query symbol definitions and references.
              Usage: ndoc lsp <symbol_name>
"""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("command", choices=["map", "context", "todo", "deps", "symbols", "data", "inject", "all", "watch", "doctor", "init", "verify", "clean", "stats", "update", "plan", "archive", "lsp", "prompt", "server", "check", "arch", "status", "help", "adr", "mind", "lesson", "impact", "skeleton"], help="Command to execute")
    parser.add_argument("target", nargs="?", help="Target file or directory (for clean command)")
    parser.add_argument("--root", default=".", help="Project root directory (Default: current dir)")
    parser.add_argument("--file", "-f", help="Specific file for prompt context generation")
    parser.add_argument("--force", action="store_true", help="⚠️ Force execution (DANGER: Overwrite configs in init, Delete without confirm in clean)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing to disk")
    # Add --stdio argument to satisfy VS Code LSP client
    parser.add_argument("--stdio", action="store_true", help="Run in stdio mode (LSP Server)")

    args = parser.parse_args()
    
    if args.command == "help":
        parser.print_help()
        sys.exit(0)
    
    root_path = Path(args.root).resolve()

    # Set Global Dry Run Mode
    if args.dry_run:
        io.set_dry_run(True)
        print("⚠️  DRY RUN MODE: No changes will be written to disk.")
    
    if args.command != "server":
        print(f"Starting Niki-docAI 2.0 in {root_path}")
    
    # 0. Handle Self-Update (No Config Needed)
    if args.command == "update":
        if update_flow.run():
            sys.exit(0)
        else:
            sys.exit(1)

    if args.command == "server":
        # Do not print to stdout as it breaks LSP protocol
        # We also need to ignore --stdio flag if present
        sys.stderr.write("Starting Niki-docAI LSP Server...\n")
        lsp_server.run()
        sys.exit(0)


    # 1. Ensure Configuration Files Exist (Documentation as Configuration)
    # Skip ensures for doctor command to diagnose raw state
    # Also skip for init, as init handles it explicitly
    if args.command not in ["doctor", "init", "server"]:
        config_flow.ensure_rules_file(root_path)
        syntax_flow.run(ProjectConfig(scan=ScanConfig(root_path=root_path))) # Ensure syntax manual


    # 2. Load Configuration
    config = config_flow.load_project_config(root_path)
    
    success = True
    
    if args.command == "init":
        if init_flow.run(config, force=args.force):
            # Check capabilities on init as well
            capability_flow.run(config, auto_install=True)
            sys.exit(0)
        else:
            sys.exit(1)
            
    if args.command == "check":
        if check_flow.run(config, target=args.target):
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

    if args.command == "prompt":
        # target can be the second argument
        target_file = args.target
        if not target_file:
            print("❌ Error: Please specify a target file for prompt generation.")
            print("Usage: ndoc prompt <file_path> [--skeleton] [--focus]")
            sys.exit(1)
            
        use_skeleton = "--skeleton" in sys.argv
        use_focus = "--focus" in sys.argv
        print(prompt_flow.get_context_prompt(target_file, config, focus=use_focus, use_skeleton=use_skeleton))
        sys.exit(0)

    # For 'server' command, we handle it early to avoid any stdout pollution
    # if args.command == "server":
    #    # Do not print to stdout as it breaks LSP protocol
    #    # We also need to ignore --stdio flag if present
    #    sys.stderr.write("Starting Niki-docAI LSP Server...\n")
    #    lsp_server.run()
    #    sys.exit(0)

    if args.command == "lsp":
        if not args.target:
            print("❌ Error: Missing symbol name. Usage: ndoc lsp <symbol_name>")
            sys.exit(1)
        
        from ndoc.atoms import lsp, fs
        print(f"🔍 Searching for symbol: {args.target}")
        lsp_service = lsp.get_service(root_path)
        files = list(fs.walk_files(root_path, config.scan.ignore_patterns))
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

    if args.command == "inject":
        inject_flow.run(config, args.target)
        sys.exit(0)
    
    if args.command in ["arch", "all"]:
        print("Running Arch Flow...")
        if arch_flow.run(config):
            print("✅ Architecture Overview updated successfully.")
        else:
            print("❌ Architecture Overview update failed.")
            success = False

    if args.command in ["context", "all"]:
        print("Running Context Flow...")
        if context_flow.run(config):
            print("✅ Context updated successfully.")
        else:
            print("❌ Context update failed.")
            success = False

    if args.command in ["status", "all"]:
        print("Running Status Flow...")
        if status_flow.run(config):
            print("✅ Status Board updated successfully.")
        else:
            print("❌ Status Board update failed.")
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

    if args.command in ["data", "all"]:
        print("Running Data Flow...")
        if data_flow.run(config):
            print("✅ Data Registry updated successfully.")
        else:
            print("❌ Data Registry update failed.")
            success = False

    elif args.command == "adr":
        adr_flow.run(config)
    elif args.command == "mind":
        mind_flow.run(config)
    elif args.command == "lesson":
        lesson_flow.run(config)
    elif args.command == "deps":
        deps_flow.run(config)
    elif args.command == "impact":
        impact_flow.run(config)
    elif args.command == "skeleton":
        if not args.target:
            print("❌ Error: 'skeleton' command requires a file path.")
            sys.exit(1)
        path = Path(args.target)
        if not path.exists():
            print(f"❌ Error: File not found: {path}")
            sys.exit(1)
        from ndoc.atoms import io
        content = io.read_text(path)
        if content:
            print(skeleton.generate_skeleton(content, str(path)))
        sys.exit(0)

    # Legacy Commands (Redirect or Deprecated)
    if args.command == "map":
        print("⚠️  'map' command is deprecated. Using 'arch' instead.")
        arch_flow.run(config)
    # if args.command == "deps": # Now a first-class command
    #     print("⚠️  'deps' command is deprecated. Using 'arch' instead.")
    #     arch_flow.run(config)
    if args.command == "tech":
        print("⚠️  'tech' command is deprecated. Using 'arch' instead.")
        arch_flow.run(config)
    if args.command == "todo":
        print("⚠️  'todo' command is deprecated. Using 'status' instead.")
        status_flow.run(config)
    if args.command == "symbols":
        print("⚠️  'symbols' command is deprecated. Using 'arch' instead.")
        arch_flow.run(config)

    if not success:
        sys.exit(1)
            
    if args.command == "watch":
        start_watch_mode(config)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
