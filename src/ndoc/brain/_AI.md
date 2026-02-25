# Context: brain
> @CONTEXT: Local | brain | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:48

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: """ @DEP: cache, hippocampus, index, llm, checker
*   **[cache.py](cache.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: hashlib, typing, sqlite3, pathlib, json
    *   `@API`
        *   `PUB:` CLS **FileCache** [🔗8]
            *   `PRV:` MET __init__`(self, cache_dir: Path)` [🔗44]
            *   `PRV:` MET _connect`(self)` [🔗2]
            *   `PRV:` MET _init_db`(self)` [🔗4]
            *   `PUB:` MET **load**`(self)` [🔗460]
            *   `PUB:` MET **save**`(self)` [🔗475]
            *   `PUB:` MET **close**`(self)` [🔗1441]
            *   `PUB:` MET **get_file_hash**`(self, file_path: Path) -> str` [🔗4]
            *   `PUB:` MET **is_changed**`(self, file_path: Path) -> bool` [🔗4]
            *   `PUB:` MET **update**`(self, file_path: Path, result: Any)` [🔗1860]
            *   `PUB:` MET **get**`(self, file_path: Path) -> Optional[Any]` [🔗6630]
*   **[checker.py](checker.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: models.symbol, typing, models.context, index, pathlib, dataclasses
    *   `@API`
        *   `PUB:` CLS **Violation** [🔗14]
            *   `VAL->` VAR **file_path**`: str` [🔗236]
            *   `VAL->` VAR **rule_name**`: str` [🔗9]
            *   `VAL->` VAR **message**`: str` [🔗6788]
            *   `VAL->` VAR **severity**`: str = "ERROR"` [🔗253]
        *   `PUB:` FUN **check_file**`(file: FileContext, index: SemanticIndex) -> List[Violation]` [🔗5]
        *   `PRV:` FUN _file_in_layer`(file: FileContext, layer_def: str) -> bool` [🔗2]
        *   `PRV:` FUN _import_in_layer`(import_name: str, layer_def: str) -> bool` [🔗2]
        *   `PUB:` FUN **check_all**`(files: List[FileContext], index: SemanticIndex) -> List[Violation]` [🔗4]
*   **[hippocampus.py](hippocampus.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: collections, time, typing, enum, pathlib, dataclasses
    *   `@API`
        *   `PUB:` CLS **ActionType** [🔗13]
            *   `VAL->` VAR **OPEN**` = 1` [🔗44]
            *   `VAL->` VAR **EDIT**` = 5` [🔗69]
            *   `VAL->` VAR **SAVE**` = 2` [🔗4]
            *   `VAL->` VAR **CLOSE**` = 0` [🔗11]
        *   `PUB:` CLS **Observation** [🔗11]
            *   `VAL->` VAR **file_path**`: str` [🔗236]
            *   `VAL->` VAR **action**`: ActionType` [🔗1178]
            *   `VAL->` VAR **timestamp**`: float = field(default_factory=time.time)` [🔗651]
        *   `PUB:` CLS **Hippocampus** [🔗10]
            *   `VAL->` VAR **buffer**`: Deque[Observation] = field(default_factory=lambda: deque(maxlen=100))` [🔗3300]
            *   `VAL->` VAR **decay_rate**`: float = 0.95` [🔗2]
            *   `PUB:` MET **record**`(self, file_path: str, action: ActionType)` [🔗944]
            *   `PUB:` MET **get_file_heat**`(self, now: float = None) -> Dict[str, float]` [🔗4]
            *   `PUB:` MET **get_tag_heat**`(self, file_tags_map: Dict[str, List[str]], now: float = None) -> Dict[str, float]` [🔗2]
*   **[index.py](index.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: models.symbol, typing, os, models.context, pathlib, dataclasses, json
    *   `@API`
        *   `PUB:` CLS **IndexEntry** [🔗9]
            *   `VAL->` VAR **tag**`: Tag` [🔗2690]
            *   `VAL->` VAR **source_file**`: str` [🔗4]
            *   `VAL->` VAR **weight**`: int = 1` [🔗68]
        *   `PUB:` CLS **SemanticIndex** [🔗15]
            *   `VAL->` VAR **rules**`: Dict[str, List[IndexEntry]] = field(default_factory=dict)` [🔗1575]
            *   `VAL->` VAR **keywords**`: Dict[str, Set[str]] = field(default_factory=dict)` [🔗440]
            *   `PUB:` MET **save**`(self, path: Path)` [🔗475]
            *   `PUB:` CLM **load**`(cls, path: Path) -> 'SemanticIndex'` [🔗460]
        *   `PUB:` FUN **build_index**`(files: List[FileContext]) -> SemanticIndex` [🔗6]
        *   `PUB:` FUN **calculate_distance**`(source_path: str, target_path: str) -> int` [🔗4]
*   **[llm.py](llm.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: urllib.request, typing, json, os
    *   `@API`
        *   `PUB:` CLS **LLMClient** [🔗3]
            *   `PUB:` STA **call**`(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]` [🔗3444]
        *   `PUB:` FUN **call_llm**`(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]` [🔗4]
        *   `PRV:` FUN _call_openai_compatible`(api_key: str, base_url: str, model: str, prompt: str, system_prompt: str) -> Optional[str]` [🔗4]
        *   `PRV:` FUN _call_gemini`(api_key: str, prompt: str, system_prompt: str) -> Optional[str]` [🔗3]
*   **[vectordb.py](vectordb.py#L1)**: <NIKI_AUTO_HEADER_START> @DEP: chromadb.config, typing, core.capabilities, os, pathlib, chromadb
    *   `@API`
        *   `PUB:` CLS **VectorDB** [🔗26]
            *   `PRV:` MET __init__`(self, root_path: Path)` [🔗44]
            *   `PRV:` MET _init_db`(self)` [🔗4]
            *   `PUB:` MET **add_documents**`(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str])` [🔗4]
            *   `PUB:` MET **query**`(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]` [🔗1776]
            *   `PUB:` MET **delete**`(self, ids: List[str])` [🔗1487]
<!-- NIKI_AUTO_Context_END -->
