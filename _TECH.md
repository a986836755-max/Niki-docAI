# PROJECT STACK
> @CONTEXT: 技术栈 | 依赖 | @TAGS: @TECH @STACK

<!-- NIKI_VERSION: 2.0.0 -->

## @STACK
*   **Language**: Python 3.10+
*   **Paradigm**: 函数式 (Data Pipeline)。
*   **Type System**: 严格类型提示 (Strict Type Hints)。

## @DEPENDENCIES
> 我们致力于 **Zero External Dependencies** (零外部依赖)，以确保可移植性和安装便捷性。

### Core (Runtime)
*   `stdlib`:
    *   `dataclasses`: 用于数据模型 (Data Models)。
    *   `pathlib`: 用于文件系统操作。
    *   `typing`: 用于类型提示。
    *   `argparse`: 用于 CLI 解析。
    *   `re`: 用于文本处理。
    *   `subprocess`: 用于运行外部工具 (git, doxygen)。

### Dev (Development)
*   `pytest`: 用于测试。
*   `mypy`: 用于静态类型检查 (可选)。

## @TOOLS
*   **Doxygen**: 用于 C++/C# 代码分析 (可选的 Fallback)。
*   **Git**: 版本控制集成。
