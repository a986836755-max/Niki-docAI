# Context: samples
> @CONTEXT: Local | samples | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-25 12:15:46

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->

<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[sample_csharp.cs](sample_csharp.cs#L1)** @DEP: System
    *   `@API`
        *   `PUB:` ??? **MyProject.Core**
        *   `PUB:` CLS **SampleService** [🔗4]
            *   `GET->` PRP **Name**` -> string` [🔗933]
            *   `PUB:` MET **SampleService()**`(string id)`
            *   `PUB:` MET **DoWork**`(int count, string message = "default") -> void` [🔗2]
            *   `PRV:` MET Dispose`(bool disposing) -> void` [🔗28]
            *   `PUB:` MET **Dispose**`() -> void` [🔗28]
        *   `PUB:` STC **ServiceStatus** [🔗21]
<!-- NIKI_AUTO_Context_END -->
