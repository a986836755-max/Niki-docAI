import argparse
import sys
from niki.core import console, config, utils
from niki.features import tech, docs, map, graph, link, log, verify, fix, test, module, build, doctor

def cmd_init(args):
    """Initialize toolchain meta files."""
    root = utils.get_project_root()
    meta_files = {
        "_RULES.md": getattr(config, "RULES_TEMPLATE", ""),
        "_TECH.md": getattr(config, "TECH_TEMPLATE", ""), 
        "_GLOSSARY.md": getattr(config, "GLOSSARY_TEMPLATE", ""),
        "_SYNTAX.md": getattr(config, "SYNTAX_TEMPLATE", ""),
    }
    
    for filename, template in meta_files.items():
        if not template: continue
        path = root / filename
        if not path.exists():
            console.info(f"Creating {filename}...")
            content = template.format(version=config.TOOLCHAIN_VERSION)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
    console.success("Initialization Complete.")

def main():
    parser = argparse.ArgumentParser(prog="niki", description="NikiDice Toolchain CLI")
    parser.add_argument("--version", action="version", version=f"niki-toolchain v{config.TOOLCHAIN_VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init
    parser_init = subparsers.add_parser("init", help="Initialize toolchain meta files")
    parser_init.set_defaults(func=cmd_init)
    
    # Tech
    parser_tech = subparsers.add_parser("tech", help="Manage technology stack")
    tech_subs = parser_tech.add_subparsers(dest="subcommand", help="Tech subcommands")
    tech_update = tech_subs.add_parser("update", help="Update _TECH.md from dependencies")
    tech_update.set_defaults(func=lambda args: tech.update(utils.get_project_root()))
    
    # Docs
    parser_docs = subparsers.add_parser("docs", help="Manage documentation")
    docs_subs = parser_docs.add_subparsers(dest="subcommand", help="Docs subcommands")
    
    docs_audit = docs_subs.add_parser("audit", help="Audit _AI.md sync status")
    docs_audit.add_argument("--hook", action="store_true", help="Run as pre-commit hook")
    docs_audit.add_argument("files", nargs="*", help="Files changed (for hook)")
    docs_audit.set_defaults(func=lambda args: docs.audit_hook(args.files) if args.hook else docs.audit_scan())
    
    docs_update = docs_subs.add_parser("update", help="Update _AI.md with Doxygen summaries")
    docs_update.set_defaults(func=lambda args: docs.update(utils.get_project_root()))

    # Map
    parser_map = subparsers.add_parser("map", help="Manage project map")
    map_subs = parser_map.add_subparsers(dest="subcommand", help="Map subcommands")
    map_update = map_subs.add_parser("update", help="Update _MAP.md and Contexts")
    map_update.set_defaults(func=lambda args: map.update_map(utils.get_project_root()))

    # Module
    parser_module = subparsers.add_parser("module", help="Manage modules")
    module_subs = parser_module.add_subparsers(dest="subcommand", help="Module subcommands")
    module_create = module_subs.add_parser("create", help="Create a new engine module")
    module_create.add_argument("name", help="Module name")
    module_create.set_defaults(func=lambda args: module.cmd_create(utils.get_project_root(), args.name))

    # Graph
    parser_graph = subparsers.add_parser("graph", help="Generate dependency graph")
    parser_graph.set_defaults(func=lambda args: graph.cmd_graph(utils.get_project_root()))

    # Link
    parser_link = subparsers.add_parser("link", help="Link glossary terms in docs")
    parser_link.set_defaults(func=lambda args: link.cmd_link(utils.get_project_root()))

    # Log
    parser_log = subparsers.add_parser("log", help="Log entry to _MEMORY.md")
    parser_log.add_argument("title", help="Log entry title")
    parser_log.add_argument("content", nargs="*", help="Log content words")
    parser_log.add_argument("--tag", default="Decision", help="Log tag (default: Decision)")
    parser_log.set_defaults(func=lambda args: log.cmd_log(utils.get_project_root(), args.title, " ".join(args.content), args.tag))

    # Verify
    parser_verify = subparsers.add_parser("verify", help="Verify project rules")
    parser_verify.set_defaults(func=lambda args: verify.cmd_verify(utils.get_project_root()))

    # Fix
    parser_fix = subparsers.add_parser("fix", help="Auto-fix documentation")
    parser_fix.set_defaults(func=lambda args: fix.cmd_fix(utils.get_project_root()))

    # Test
    parser_test = subparsers.add_parser("test", help="Run tests and update docs")
    parser_test.set_defaults(func=lambda args: test.cmd_test(utils.get_project_root(), args))

    # Build
    parser_build = subparsers.add_parser("build", help="Build project")
    parser_build.set_defaults(func=lambda args: build.cmd_build(utils.get_project_root()))

    # Doctor
    parser_doctor = subparsers.add_parser("doctor", help="Check toolchain health")
    parser_doctor.set_defaults(func=lambda args: doctor.cmd_doctor(utils.get_project_root()))

    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
