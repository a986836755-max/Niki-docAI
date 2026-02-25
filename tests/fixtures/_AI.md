# Context: fixtures
> @CONTEXT: Local | fixtures | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:56

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[complex_api.py](complex_api.py#L1)** @DEP: typing, dataclasses
    *   `@API`
        *   `PUB:` CLS **User** [🔗328]
            *   `VAL->` VAR **name**`: str` [🔗25070]
            *   `VAL->` VAR **age**`: int = 18` [🔗243]
            *   `VAL->` VAR _internal`: bool = False` [🔗10]
            *   `PRV:` MET __init__`(self, name: str)` [🔗44]
            *   `GET->` PRP **is_adult**`(self) -> bool` [🔗2]
            *   `AWAIT` ASY **fetch_data**`(self) -> dict` [🔗3]
            *   `PUB:` CLM **from_dict**`(cls, data: dict) -> "User"` [🔗6]
        *   `PUB:` CLS **Database** [🔗22]
            *   `VAL->` VAR **connection_string**`: str = "localhost:5432"` [🔗2]
            *   `PUB:` MET **connect**`(self)` [🔗424]
        *   `PUB:` FUN **global_func**`(x: int, y: int) -> int` [🔗4]
        *   `AWAIT` ASY **global_async_func**`()` [🔗3]
<!-- NIKI_AUTO_Context_END -->
