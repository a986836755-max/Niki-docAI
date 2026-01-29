# PROJECT MAP
> @CONTEXT: 导航 | 结构 | @TAGS: @MAP @TREE

<!-- NIKI_VERSION: 2.0.0 -->

## @OVERVIEW
本地图定义了 **Niki-docAI 2.0** 系统的物理结构。

## @META_FILES (Root)
*   `_AI.md`: [Context] 递归上下文入口 (Recursive Context Entry)。
*   `_ARCH.md`: [Architecture] 系统设计与数据流。
*   `_MAP.md`: [Map] 项目结构 (本文件)。
*   `_RULES.md`: [Rules] 约束与开发规范。
*   `_SYNTAX.md`: [Syntax] 标签与标记定义。
*   `_TECH.md`: [Stack] 技术栈与依赖。

## @TREE (Directory Structure)
<!-- NIKI_MAP_START -->
- **[ndoc_legacy](ndoc_legacy)**
  - **[src](ndoc_legacy/src)**: Source Code Root (源代码根目录)
    - **[ndoc](ndoc_legacy/src/ndoc)**
      - **[base](ndoc_legacy/src/ndoc/base)**
      - **[core](ndoc_legacy/src/ndoc/core)**: Core Logic (核心逻辑)
      - **[features](ndoc_legacy/src/ndoc/features)**: Feature Modules (功能模块)
      - **[resources](ndoc_legacy/src/ndoc/resources)**
    - **[niki_docai.egg-info](ndoc_legacy/src/niki_docai.egg-info)**
    - **[niki_toolchain.egg-info](ndoc_legacy/src/niki_toolchain.egg-info)**
  - **[test](ndoc_legacy/test)**: Test Suites (测试套件)
    - **[playground](ndoc_legacy/test/playground)**
      - **[subdir](ndoc_legacy/test/playground/subdir)**
- **[src](src)**: Source Code Root (源代码根目录)
  - **[ndoc](src/ndoc)**
    - **[atoms](src/ndoc/atoms)**
    - **[flows](src/ndoc/flows)**
    - **[models](src/ndoc/models)**
- **[tools](tools)**: Dev Tools & Scripts (开发工具与脚本)
<!-- NIKI_MAP_END -->