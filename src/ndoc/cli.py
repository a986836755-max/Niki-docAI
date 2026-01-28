import argparse
import sys
from ndoc.core import console, config, utils, initializer
from ndoc.features import tech, docs, map, graph, link, log, verify, fix, test, module, build, doctor

def cmd_init(args):
    """Initialize toolchain meta files."""
    root = utils.get_project_root()
    
    if args.reset_all:
        initializer.init_meta_files(root, reset=True)
        docs.init_all_recursive(".", reset=True)
    elif args.reset_path:
        docs.init_ai_md(args.reset_path, reset=True)
    elif args.reset_meta:
        initializer.init_meta_files(root, reset=True)
    else:
        # Default behavior (no reset)
        initializer.init_meta_files(root, reset=False)

def run_auto(func, args=None, use_root=True):
    """Run a function with auto-initialization."""
    root = utils.get_project_root()
    initializer.check_and_auto_init(root)
    if use_root:
        func(root)
    else:
        func()

def cmd_dashboard():
    """Show project status dashboard."""
    console.header("Niki-docAI Dashboard")
    root = utils.get_project_root()
    
    # Check meta files
    meta_files = ["_RULES.md", "_TECH.md", "_GLOSSARY.md", "_MAP.md"]
    missing = [f for f in meta_files if not (root / f).exists()]
    
    if missing:
        console.warning(f"Missing meta files: {', '.join(missing)}")
        console.info("Run 'ndoc init' or any command to auto-initialize.")
    else:
        console.success("Project Context: Initialized")
        
    # Simple stats
    console.info(f"Root: {root}")
    console.info(f"Version: {config.TOOLCHAIN_VERSION}")
    console.info("\nAvailable Commands:")
    console.info("  ndoc map update   - Update project map")
    console.info("  ndoc verify       - Verify architecture")
    console.info("  ndoc doctor       - Check environment")

def main():
    parser = argparse.ArgumentParser(prog="ndoc", description="NikiDice Toolchain CLI (Niki_docAI)")
    parser.add_argument("--version", action="version", version=f"Niki_docAI v{config.TOOLCHAIN_VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init
    parser_init = subparsers.add_parser("init", help="Initialize toolchain meta files")
    
    group = parser_init.add_mutually_exclusive_group()
    group.add_argument("--reset-meta", action="store_true", help="Reset global meta files")
    group.add_argument("--reset-all", action="store_true", help="Reset all files (recursive)")
    group.add_argument("--reset-path", metavar="PATH", help="Reset _AI.md in specific path")
    
    parser_init.set_defaults(func=cmd_init)
    
    # Tech
    parser_tech = subparsers.add_parser("tech", help="Manage technology stack")
    tech_subs = parser_tech.add_subparsers(dest="subcommand", help="Tech subcommands")
    tech_update = tech_subs.add_parser("update", help="Update _TECH.md from dependencies")
    tech_update.set_defaults(func=lambda args: run_auto(tech.update))
    
    # Docs
    parser_docs = subparsers.add_parser("docs", help="Manage documentation")
    docs_subs = parser_docs.add_subparsers(dest="subcommand", help="Docs subcommands")
    
    docs_init = docs_subs.add_parser("init", help="Create _AI.md in a directory")
    docs_init.add_argument("path", nargs="?", default=".", help="Directory path to initialize (default: current root)")
    docs_init.add_argument("--all", action="store_true", help="Recursively initialize all subdirectories")
    
    def handle_docs_init(args):
        if args.all:
            # If path is provided with --all, use it as start path
            start_path = args.path if args.path else "."
            run_auto(lambda root: docs.init_all_recursive(start_path))
        else:
            # If no path provided and no --all, maybe we should ask for path or default to current?
            # Argument parser default="." handles it, but let's be explicit if needed.
            run_auto(lambda root: docs.init_ai_md(args.path))

    docs_init.set_defaults(func=handle_docs_init)
    
    docs_audit = docs_subs.add_parser("audit", help="Audit _AI.md sync status")
    docs_audit.add_argument("--hook", action="store_true", help="Run as pre-commit hook")
    docs_audit.add_argument("files", nargs="*", help="Files changed (for hook)")
    docs_audit.set_defaults(func=lambda args: docs.audit_hook(args.files) if args.hook else run_auto(docs.audit_scan, use_root=False))
    
    docs_update = docs_subs.add_parser("update", help="Update _AI.md with Doxygen summaries")
    docs_update.set_defaults(func=lambda args: run_auto(docs.update))

    # Map
    parser_map = subparsers.add_parser("map", help="Manage project map")
    map_subs = parser_map.add_subparsers(dest="subcommand", help="Map subcommands")
    map_update = map_subs.add_parser("update", help="Update _MAP.md and Contexts")
    map_update.set_defaults(func=lambda args: run_auto(map.update_map))

    # Module
    parser_module = subparsers.add_parser("module", help="Manage modules")
    module_subs = parser_module.add_subparsers(dest="subcommand", help="Module subcommands")
    module_create = module_subs.add_parser("create", help="Create a new engine module")
    module_create.add_argument("name", help="Module name")
    module_create.set_defaults(func=lambda args: run_auto(lambda root: module.cmd_create(root, args.name)))

    # Graph
    parser_graph = subparsers.add_parser("graph", help="Generate dependency graph")
    parser_graph.set_defaults(func=lambda args: run_auto(graph.cmd_graph))

    # Link
    parser_link = subparsers.add_parser("link", help="Link glossary terms in docs")
    parser_link.set_defaults(func=lambda args: run_auto(link.cmd_link))

    # Log
    parser_log = subparsers.add_parser("log", help="Log entry to _MEMORY.md")
    parser_log.add_argument("title", help="Log entry title")
    parser_log.add_argument("content", nargs="*", help="Log content words")
    parser_log.add_argument("--tag", default="Decision", help="Log tag (default: Decision)")
    parser_log.set_defaults(func=lambda args: run_auto(lambda root: log.cmd_log(root, args.title, " ".join(args.content), args.tag)))

    # Verify
    parser_verify = subparsers.add_parser("verify", help="Verify project rules")
    parser_verify.set_defaults(func=lambda args: run_auto(verify.cmd_verify))

    # Fix
    parser_fix = subparsers.add_parser("fix", help="Auto-fix documentation")
    parser_fix.set_defaults(func=lambda args: run_auto(fix.cmd_fix))

    # Test
    parser_test = subparsers.add_parser("test", help="Run tests and update docs")
    parser_test.set_defaults(func=lambda args: run_auto(lambda root: test.cmd_test(root, args)))

    # Build
    parser_build = subparsers.add_parser("build", help="Build project")
    parser_build.set_defaults(func=lambda args: run_auto(build.cmd_build))

    # Doctor
    parser_doctor = subparsers.add_parser("doctor", help="Check toolchain health")
    parser_doctor.set_defaults(func=lambda args: doctor.cmd_doctor(utils.get_project_root()))

    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        cmd_dashboard()

if __name__ == "__main__":
    main()
