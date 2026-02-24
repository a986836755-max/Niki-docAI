# Context: samples
> @CONTEXT: Local | samples | @TAGS: @LOCAL
> 最后更新 (Last Updated): 2026-02-24 14:59:53

## !RULE

<!-- NIKI_AUTO_MEMORIES_START -->
### Auto-Detected Rules
*   **RULE**: All metrics must be normalized to [0, 1] range. [memory_test.py:4](memory_test.py#L4)
*   **WARN**: Large lists may cause memory overflow, use generator if len > 1M. [memory_test.py:5](memory_test.py#L5)
*   **INTENT**: We chose float64 for precision. [memory_test.py:6](memory_test.py#L6)
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
