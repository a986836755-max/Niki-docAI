# Context: fixtures
> @CONTEXT: Local | fixtures | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-30 19:25:16

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[complex_api.py](complex_api.py#L1)** @DEP: dataclasses, typing
    *   `@API`
        *   `PUB:` CLS **User**
            *   `VAL->` VAR **name**`: str`
            *   `VAL->` VAR **age**`: int = 18`
            *   `VAL->` VAR _internal`: bool = False`
            *   `PRV:` MET __init__`(self, name: str)`
            *   `GET->` PRP **is_adult**`(self) -> bool`
            *   `AWAIT` ASY **fetch_data**`(self) -> dict`
            *   `PUB:` CLM **from_dict**`(cls, data: dict) -> "User"`
        *   `PUB:` CLS **Database**
            *   `VAL->` VAR **connection_string**`: str = "localhost:5432"`
            *   `PUB:` MET **connect**`(self)`
        *   `PUB:` FUN **global_func**`(x: int, y: int) -> int`
        *   `AWAIT` ASY **global_async_func**`()`
<!-- NIKI_AUTO_Context_END -->
