"""
Entry Point: CLI Execution.
入口：CLI 执行。
"""
import argparse
import sys
import logging
from pathlib import Path
from ndoc.core.logger import logger, set_log_level
from ndoc.core.bootstrap import ensure_cli_environment
from ndoc.core.cli import CommandRegistry

# Ensure environment is set up BEFORE importing flows that might depend on it
ensure_cli_environment()

# 添加 src 到 sys.path 以便直接运行
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- LOGGING SUPPRESSION ---
# Prevent pygls and other libraries from spamming stdout/stderr during CLI execution
# unless we are explicitly running the server.
logging.getLogger("pygls").setLevel(logging.WARNING)
logging.getLogger("lsprotocol").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)
# ---------------------------

from ndoc.models.config import ProjectConfig, ScanConfig
from ndoc import lsp_server
from ndoc.flows import (
    context_flow, 
    map_flow,
    config_flow, 
    syntax_flow, 
    doctor_flow, 
    init_flow, 
    verify_flow, 
    clean_flow, 
    update_flow, 
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
    search_flow,
    quality_flow,
)
from ndoc.daemon import start_watch_mode
from ndoc.core import io
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
  
  prompt    : Generate semantic context prompt for AI (Vector Search).
              Usage: ndoc prompt <file> [--focus] [--skeleton]
              
  search    : Search codebase using natural language.
              Usage: ndoc search "query string"

Diagnostics (诊断与维护):
  check     : Check code for constraint violations (!RULE).
              Usage: ndoc check [target]
  verify    : Verify documentation artifacts.
  doctor    : Diagnose environment and configuration health.
  stats     : Update project statistics (_STATS.md).
  lint      : Run lint commands defined in _RULES.md.
  typecheck : Run typecheck commands defined in _RULES.md.
  
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
    
    # Dynamically build choices from registry
    commands = CommandRegistry.get_commands()
    command_names = [cmd.name for cmd in commands]
    # Add special commands that might not be flows or need custom handling
    special_commands = ["all", "watch", "server", "skeleton", "lsp", "stats"] 
    all_choices = list(set(command_names + special_commands))
    all_choices.sort()

    parser.add_argument("command", choices=all_choices, help="Command to execute")
    parser.add_argument("target", nargs="?", help="Target file or directory (for clean command)")
    parser.add_argument("--root", default=".", help="Project root directory (Default: current dir)")
    parser.add_argument("--file", "-f", help="Specific file for prompt context generation")
    parser.add_argument("--force", action="store_true", help="⚠️ Force execution (DANGER: Overwrite configs in init, Delete without confirm in clean)")
    parser.add_argument("--focus", action="store_true", help="Enable Focus Mode (Vector Search) for prompt command")
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
        # Set log level based on args
        # set_log_level(logging.DEBUG if getattr(args, 'verbose', False) else logging.INFO)
        logger.info(f"Starting Niki-docAI 2.0 in {root_path}")
    
    # 0. Special Handlers (Pre-Config)
    if args.command == "server":
        sys.stderr.write("Starting Niki-docAI LSP Server...\n")
        lsp_server.run()
        sys.exit(0)

    if args.command == "skeleton":
        if not args.target:
            print("❌ Error: 'skeleton' command requires a file path.")
            sys.exit(1)
        path = Path(args.target)
        if not path.exists():
            print(f"❌ Error: File not found: {path}")
            sys.exit(1)
        from ndoc.core import io
        content = io.read_text(path)
        if content:
            print(skeleton.generate_skeleton(content, str(path)))
        sys.exit(0)

    if args.command == "lsp":
        if not args.target:
            print("❌ Error: Missing symbol name. Usage: ndoc lsp <symbol_name>")
            sys.exit(1)
        
        from ndoc.interfaces import lsp
        from ndoc.core import fs
        print(f"🔍 Searching for symbol: {args.target}")
        
        # Load config for LSP
        # 1. Ensure Configuration Files Exist (Documentation as Configuration)
        if args.command not in ["doctor", "init"]:
            config_flow.ensure_rules_file(root_path)
            syntax_flow.run(ProjectConfig(scan=ScanConfig(root_path=root_path))) # Ensure syntax manual
        config = config_flow.load_project_config(root_path)

        lsp_service = lsp.get_service(root_path)
        files = list(fs.walk_files(root_path, config.scan.ignore_patterns))
        lsp_service.index_project(files, config=config)
        
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

    # 1. Ensure Configuration Files Exist (Documentation as Configuration)
    if args.command not in ["doctor", "init", "server"]:
        config_flow.ensure_rules_file(root_path)
        syntax_flow.run(ProjectConfig(scan=ScanConfig(root_path=root_path))) # Ensure syntax manual

    # 2. Load Configuration
    config = config_flow.load_project_config(root_path)
    
    # 3. Dynamic Dispatch
    handler = CommandRegistry.get_handler(args.command)
    if handler:
        # Check signature to pass arguments correctly
        import inspect
        sig = inspect.signature(handler)
        kwargs = {}
        
        if "config" in sig.parameters:
            kwargs["config"] = config
        if "target" in sig.parameters and args.target:
            kwargs["target"] = args.target
        if "query" in sig.parameters and args.target: # Search uses target as query
            kwargs["query"] = args.target
        if "file_path" in sig.parameters and args.target: # Prompt uses target as file_path
            kwargs["file_path"] = args.target
        if "force" in sig.parameters:
            kwargs["force"] = args.force
        if "auto_install" in sig.parameters:
            # For init/caps, usually true or passed via args? 
            # Let's assume True for init context if not specified
            kwargs["auto_install"] = True
        if "focus" in sig.parameters:
            kwargs["focus"] = args.focus
            
        try:
            success = handler(**kwargs)
            if not success:
                sys.exit(1)
            sys.exit(0)
        except TypeError as e:
            logger.error(f"Command signature mismatch: {e}")
            sys.exit(1)

    # 4. Handle Special/Composite Commands
    success = True
    
    if args.command == "all":
        # Sequence of commands to run
        sequence = ["map", "arch", "context", "status", "data", "deps", "archive"]
        
        for cmd_name in sequence:
            handler = CommandRegistry.get_handler(cmd_name)
            if handler:
                print(f"Running {cmd_name.title()} Flow...")
                try:
                    if not handler(config=config):
                        print(f"❌ {cmd_name.title()} failed.")
                        success = False
                    else:
                        print(f"✅ {cmd_name.title()} updated successfully.")
                except Exception as e:
                    print(f"❌ {cmd_name.title()} crashed: {e}")
                    success = False
    
    elif args.command == "stats":
        # Re-use status flow logic but with force=True
        # We can call status_flow.update_stats_file directly if exposed, 
        # or just run status flow.
        # But status flow main entry point updates both TODOs and Stats.
        # Let's keep it simple and just run status flow.
        handler = CommandRegistry.get_handler("status")
        if handler:
            success = handler(config=config)

    elif args.command == "watch":
        start_watch_mode(config)
            
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
