"""
Deps: Test Usage Mapper.
感知层：建立测试用例反向索引。
"""
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast as py_ast
from ...core.fs import walk_files
from ...core.io import read_text
from ...parsing.ast import parse_code
from ...parsing.ast.discovery import find_calls_with_loc
from ...models.config import ProjectConfig

class TestUsageMapper:
    """
    Maps symbol usages in test files to their definitions.
    """
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.usage_map: Dict[str, List[Dict[str, Any]]] = {} # full_name -> [{"path": str, "line": int}]

    def scan(self):
        """
        Scan tests directory and build usage map.
        """
        test_dir = self.config.scan.root_path / "tests"
        if not test_dir.exists():
            # Try src/tests or other common locations?
            # For now stick to strict convention
            return
            
        # Walk all python files in tests/
        for file_path in walk_files(test_dir, self.config.scan.ignore_patterns):
            if file_path.suffix == ".py":
                self._process_python_file(file_path)

    def _extract_import_aliases(self, content: str) -> Dict[str, str]:
        """
        Extract imports mapping: alias -> full_name
        """
        mapping = {}
        try:
            tree = py_ast.parse(content)
            for node in py_ast.walk(tree):
                if isinstance(node, py_ast.Import):
                    for alias in node.names:
                        name = alias.name
                        asname = alias.asname or name
                        mapping[asname] = name
                elif isinstance(node, py_ast.ImportFrom):
                    if node.module:
                        module = node.module
                        for alias in node.names:
                            name = alias.name
                            asname = alias.asname or name
                            full_name = f"{module}.{name}"
                            mapping[asname] = full_name
        except:
            pass
        return mapping

    def _process_python_file(self, file_path: Path):
        content = read_text(file_path)
        if not content:
            return
            
        import_map = self._extract_import_aliases(content)
        
        # Use our robust AST parser
        tree = parse_code(content, file_path)
        if not tree:
            return
            
        calls = find_calls_with_loc(tree, 'python')
        try:
            rel_path = str(file_path.relative_to(self.config.scan.root_path)).replace("\\", "/")
        except ValueError:
            rel_path = file_path.name
        
        for call in calls:
            name = call['name'] # e.g. "context_flow.run" or "run"
            line = call['line']
            
            resolved_names = self._resolve_with_aliases(name, import_map)
            
            for full_name in resolved_names:
                if full_name not in self.usage_map:
                    self.usage_map[full_name] = []
                
                # Avoid duplicates
                entry = {"path": rel_path, "line": line}
                if entry not in self.usage_map[full_name]:
                    self.usage_map[full_name].append(entry)

    def _resolve_with_aliases(self, call_name: str, import_map: Dict[str, str]) -> List[str]:
        """
        Resolve call name using import aliases.
        """
        candidates = []
        parts = call_name.split('.')
        head = parts[0]
        
        # Case 1: Direct alias match (e.g. "run" -> "context_flow.run")
        if head in import_map:
            resolved_head = import_map[head]
            if len(parts) > 1:
                candidates.append(f"{resolved_head}.{'.'.join(parts[1:])}")
            else:
                candidates.append(resolved_head)
        else:
            # Case 2: No alias, assume it's a direct reference (less likely to be correct without full analysis)
            candidates.append(call_name)
            
        return candidates

def run_test_mapping(config: ProjectConfig) -> TestUsageMapper:
    """Helper to run the mapping process."""
    mapper = TestUsageMapper(config)
    mapper.scan()
    return mapper
