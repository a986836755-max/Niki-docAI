# <NIKI_AUTO_HEADER_START>
# ------------------------------------------------------------------------------
# 🧠 Niki-docAI Context (Auto-Generated)
# ------------------------------------------------------------------------------
# <NIKI_AUTO_HEADER_END>
"""
Flow: Test Usage Mapper.
扫描测试文件，建立 API -> 测试用例的反向索引。
"""
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast as py_ast
from ndoc.core.fs import walk_files
from ndoc.core.io import read_text
from ndoc.parsing.ast import parse_code
from ndoc.parsing.ast.discovery import find_calls_with_loc
from ndoc.models.config import ProjectConfig

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
        
        tree = parse_code(content, file_path)
        if not tree:
            return
            
        calls = find_calls_with_loc(tree, 'python')
        rel_path = str(file_path.relative_to(self.config.scan.root_path)).replace("\\", "/")
        
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
        
        if head in import_map:
            full_prefix = import_map[head]
            if len(parts) > 1:
                # e.g. call="context_flow.run", head="context_flow" -> "ndoc.flows.context_flow"
                # result = "ndoc.flows.context_flow.run"
                candidates.append(f"{full_prefix}.{'.'.join(parts[1:])}")
            else:
                # e.g. call="run", head="run" -> "ndoc.flows.context_flow.run"
                candidates.append(full_prefix)
                
        # Also support fully qualified names if they start with ndoc
        if call_name.startswith("ndoc."):
            candidates.append(call_name)
            
        return candidates

    def get_usages(self, symbol_full_name: str) -> List[Dict[str, Any]]:
        """
        Get usages for a symbol.
        """
        return self.usage_map.get(symbol_full_name, [])

def run_test_mapping(config: ProjectConfig) -> TestUsageMapper:
    mapper = TestUsageMapper(config)
    mapper.scan()
    return mapper
