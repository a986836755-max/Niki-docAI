# Context: samples
> @CONTEXT: Local | samples | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:53

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->
<!-- NIKI_AUTO_MEMORIES_END -->
<!-- Add local rules here -->

<!-- NIKI_AUTO_Context_START -->
## @STRUCTURE
*   **[sample_csharp.cs](sample_csharp.cs#L1)** @DEP: System
    *   `@API`
        *   `PUB:` ??? **MyProject.Core**
        *   `PUB:` CLS **SampleService**
            *   `GET->` PRP **Name**` -> string`
            *   `PUB:` MET **SampleService()**`(string id)`
            *   `PUB:` MET **DoWork**`(int count, string message = "default") -> void`
            *   `PRV:` MET Dispose`(bool disposing) -> void`
            *   `PUB:` MET **Dispose**`() -> void`
        *   `PUB:` STC **ServiceStatus**
<!-- NIKI_AUTO_Context_END -->
