# Context: models
> @CONTEXT: Local | models | @TAGS: @LOCAL

## !RULE
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[__init__.py](__init__.py)**: Models: Data Definitions.
*   **[config.py](config.py)**: Models: Configuration definitions.
    *   `PUB:` CLS **ProjectConfig**
    *   `PUB:` CLS **ScanConfig**
*   **[context.py](context.py)**: Models: Context Models.
    *   `PUB:` CLS **DirectoryContext**
    *   `PUB:` CLS **FileContext**
    *   `PUB:` CLS **Section**
    *   `PUB:` CLS **Symbol**
    *   `PUB:` CLS **Tag**
    *   `GET->` VAR **has_content**`(self) -> bool`
    *   `GET->` VAR **is_public**`(self) -> bool`
    *   `GET->` VAR **name**`(self) -> str`
<!-- NIKI_AUTO_Context_END -->
