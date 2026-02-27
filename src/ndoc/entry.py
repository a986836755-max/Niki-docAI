"""
Entry Point: CLI Execution.
入口：CLI 执行。
"""
import argparse
import sys
import logging
import inspect
from pathlib import Path

# 1. Environment Setup
from ndoc.core.bootstrap import ensure_cli_environment
ensure_cli_environment()

# Add src to sys.path for direct execution if needed
sys.path.insert(0, str(Path(__file__).parent.parent))

# 2. Logging Configuration
from ndoc.core.logger import logger

# Prevent pygls and other libraries from spamming stdout/stderr during CLI execution
logging.getLogger("pygls").setLevel(logging.WARNING)
logging.getLogger("lsprotocol").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)

# 3. Import Dependencies
from ndoc.models.config import ProjectConfig, ScanConfig
from ndoc.core.cli import CommandRegistry
from ndoc.core import io, templates
from ndoc.flows import config_flow

# 4. Import Commands to Register them
# This ensures all @ndoc_command decorators are executed
import ndoc.cli.commands
# Also import legacy flows that expose commands
# (Assuming they are still needed and use @ndoc_command)
from ndoc.flows import (
    verify_flow, 
    clean_flow, 
    update_flow, 
    inject_flow, 
    quality_flow,
)


def main():
    """
    CLI Main Entry.
    """
    description = """
Niki-docAI 2.0 (Rebirth) - AI Context Ops Toolchain

Run 'ndoc <command> --help' for more information on a command.
"""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Dynamically build choices from registry
    commands = CommandRegistry.get_commands()
    # Sort commands by group then name for better help display?
    # For now just list names
    command_names = sorted([cmd.name for cmd in commands])
    command_names.append("help")
    
    if not command_names:
        print("Error: No commands registered.")
        sys.exit(1)

    parser.add_argument("command", choices=command_names, help="Command to execute")
    parser.add_argument("target", nargs="?", help="Target file or directory (context dependent)")
    parser.add_argument("--root", default=".", help="Project root directory (Default: current dir)")
    parser.add_argument("--file", "-f", help="Specific file for prompt/context generation")
    parser.add_argument("--force", action="store_true", help="Force execution (Overwrite configs, Delete without confirm)")
    parser.add_argument("--focus", action="store_true", help="Enable Focus Mode (Vector Search)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing to disk")
    parser.add_argument("--stdio", action="store_true", help="Run in stdio mode (LSP Server)")

    # Parse arguments
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
        logger.info(f"Starting Niki-docAI 2.0 in {root_path}")
    
    # 5. Load Configuration (Documentation as Configuration)
    # Some commands don't need full config, but loading it is generally safe
    # Exception: 'init' might run before config exists, but load_project_config handles missing file gracefully
    config = None
    try:
        # Ensure _RULES.md exists only for commands that likely need it
        # Skip for 'init', 'doctor', 'server', 'help'
        if args.command not in ["doctor", "init", "server", "help"]:
            try:
                config_flow.ensure_rules_file(root_path)
            except Exception as e:
                logger.debug(f"Config ensure failed (non-critical): {e}")

        # Load Project Config
        config = config_flow.load_project_config(root_path)
        
        # Configure Templates System
        if config and config.template:
            templates.configure(config.template)
            
    except Exception as e:
        logger.error(f"Failed to load project configuration: {e}")
        # We don't exit here because some commands might not need config
        # But if they do, they will fail later or use defaults

    # 6. Dynamic Dispatch
    handler = CommandRegistry.get_handler(args.command)
    
    if not handler:
        print(f"Error: Command '{args.command}' not found.")
        sys.exit(1)

    # Inspect signature to inject dependencies
    sig = inspect.signature(handler)
    kwargs = {}
    
    # Map CLI args to handler arguments
    if "config" in sig.parameters:
        if config is None:
             # Create default config if loading failed but handler needs it
             config = ProjectConfig(scan=ScanConfig(root_path=root_path))
        kwargs["config"] = config
        
    if "target" in sig.parameters:
        kwargs["target"] = args.target
        
    # Legacy mappings (some handlers use different names for target)
    if "query" in sig.parameters and args.target: 
        kwargs["query"] = args.target
    if "file_path" in sig.parameters and args.target: 
        kwargs["file_path"] = args.target
        
    if "force" in sig.parameters:
        kwargs["force"] = args.force
        
    if "auto_install" in sig.parameters:
        kwargs["auto_install"] = True
        
    if "focus" in sig.parameters:
        kwargs["focus"] = args.focus
        
    if "stdio" in sig.parameters:
        kwargs["stdio"] = args.stdio

    # Execute Handler
    try:
        success = handler(**kwargs)
        if not success:
            sys.exit(1)
        sys.exit(0)
    except TypeError as e:
        logger.error(f"Command signature mismatch for '{args.command}': {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        logger.error(f"Command '{args.command}' failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
