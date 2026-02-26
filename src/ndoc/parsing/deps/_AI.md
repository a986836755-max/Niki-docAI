# Context: deps
> @CONTEXT: Local | deps | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-26 20:35:05

## !RULE
<!-- Add local rules here. Examples: -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
<!-- !RULE: @FORBID(hardcoded_paths) -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)** @DEP: .
*   **[api_extractor.py](api_extractor.py#L1)**: Parsing: Dependency API Extractor. @DEP: ...core, ...models.config, ...parsing, .builder, pathlib, ...
    *   `@API`
        *   `PUB:` FUN **extract_related_apis**`(file_path: Path, config: ProjectConfig) -> str`
*   **[builder.py](builder.py#L1)**: Parsing: Dependency Graph Builder. @DEP: ...core, ...models.config, ...parsing, collections, pathlib, ...
    *   `@API`
        *   `PUB:` FUN **collect_imports**`(root_path: Path, config: ProjectConfig = None) -> Dict[str, List[str]]`
        *   `PUB:` FUN **build_dependency_graph**`(import_map: Dict[str, List[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **get_module_name**`(path: str) -> str`
        *   `PUB:` FUN **aggregate_graph**`(file_graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]`
        *   `PUB:` FUN **is_core_module**`(name: str) -> bool`
*   **[core.py](core.py#L1)**: Core parsing logic for dependency manifests. @DEP: ...core, json, pathlib, re, typing
    *   `@API`
        *   `PUB:` FUN **parse_requirements_txt**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pyproject_toml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_package_json**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_pubspec_yaml**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_csproj**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_go_mod**`(file_path: Path) -> List[str]`
        *   `PUB:` FUN **parse_cargo_toml**`(file_path: Path) -> List[str]`
*   **[stats.py](stats.py#L1)**: Language Statistics. @DEP: ...core, ..langs, pathlib, typing
    *   `@API`
        *   `PUB:` FUN **detect_languages**`(root: Path, ignore_patterns: Set[str]) -> Dict[str, float]`
*   **[test_mapper.py](test_mapper.py#L1)**: Deps: Test Usage Mapper. @DEP: ...core.fs, ...core.io, ...models.config, ...parsing.ast, ...parsing.ast.discovery, ...
    *   `@API`
        *   `PUB:` CLS **TestUsageMapper**
            *   `PRV:` MET __init__`(self, config: ProjectConfig)`
            *   `PUB:` MET **scan**`(self)`
            *   `PRV:` MET _extract_import_aliases`(self, content: str) -> Dict[str, str]`
            *   `PRV:` MET _process_python_file`(self, file_path: Path)`
            *   `PRV:` MET _resolve_with_aliases`(self, call_name: str, import_map: Dict[str, str]) -> List[str]`
        *   `PUB:` FUN **run_test_mapping**`(config: ProjectConfig) -> TestUsageMapper`
<!-- NIKI_AUTO_Context_END -->
