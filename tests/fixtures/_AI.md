# Context: fixtures
> @CONTEXT: Local | fixtures | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-29 20:01:46

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[complex_api.py](complex_api.py)**
    *   `PUB:` CLS **Database**
    *   `PUB:` CLS **User**
    *   `PUB:` FUN **connect**`(self)`
    *   `PUB:` FUN **fetch_data**`(self) -> dict`
    *   `PUB:` ??? **from_dict**`(cls, data: dict) -> "User"`
    *   `PUB:` FUN **global_async_func**`()`
    *   `PUB:` FUN **global_func**`(x: int, y: int) -> int`
    *   `GET->` VAR **is_adult**`(self) -> bool`
    *   `PRV:` FUN __init__`(self, name: str)`
<!-- NIKI_AUTO_Context_END -->
