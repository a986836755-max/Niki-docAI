# Context: models
> @CONTEXT: Local | models | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-01-29 19:27:32

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py#L1)**: Models: Data Definitions.
*   **[config.py](config.py#L1)**: Models: Configuration definitions.
    *   `PUB:` CLS **ProjectConfig**
    *   `PUB:` CLS **ScanConfig**
    *   `@DEP` dataclasses, pathlib, typing
*   **[context.py](context.py#L1)**: Models: Context Models.
    *   `PUB:` CLS **DirectoryContext**
    *   `PUB:` CLS **FileContext**
    *   `PUB:` CLS **Section**
    *   `PUB:` CLS **Symbol**
    *   `PUB:` CLS **Tag**
    *   `GET->` VAR **has_content**`(self) -> bool`
    *   `GET->` VAR **is_public**`(self) -> bool`
    *   `GET->` VAR **name**`(self) -> str`
    *   `@DEP` dataclasses, pathlib, typing
<!-- NIKI_AUTO_Context_END -->
