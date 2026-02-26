# Niki-docAI 2.0 (Rebirth)

> **Context Ops & Architecture Guard for AI-Assisted Development**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)]()

[**中文文档**](README_zh.md) | [**English**](README.md)

---

## 1. What is Niki-docAI?

**Niki-docAI** is an intelligent toolchain designed to bridge the gap between **Human Engineers** and **AI Coding Assistants** (like Copilot, Cursor, Trae).

It treats documentation not as static text, but as a **"Context Database"** that is:
1.  **Auto-generated** from code (Single Source of Truth).
2.  **Structurally Optimized** for AI context windows (Token efficient).
3.  **Strictly Verified** against architectural rules (Hallucination reduction).

---

## 2. The Problem

In the era of AI-assisted coding, we face three major pain points:

*   **Context Loss**:
    AI assistants often fail to understand the "Big Picture" of a large codebase because they can only see a few open files.

*   **Hallucination**:
    When documentation is outdated, AI generates code based on wrong assumptions.

*   **Maintenance Burden**:
    Humans hate writing docs. Keeping architecture diagrams and dependency lists up-to-date manually is painful and error-prone.

---

## 3. The Solution

Niki-docAI provides a suite of tools to automate "Context Ops":

### Core Features

*   **Automated Context Map (`_MAP.md`)**:
    Automatically generates a navigational map of your project structure with **Precise Line References** (e.g., `file.py#L1`), helping AI find the right files instantly.

*   **Architecture Guard (`ndoc check`)**:
    **[NEW in 2.0]** Enforce architecture rules (e.g., Layering) defined in `_RULES.md` using `!RULE`. Prevents "Architecture Drift" before it happens.

*   **Circular Dependency Detection (`ndoc deps`)**:
    **[NEW in 2.0]** Detects and reports circular dependencies in your codebase using Tarjan's algorithm. Supports scoped dependency analysis for specific modules.

*   **Intelligent Retrieval (`ndoc prompt --focus`)**:
    **[NEW in 2.0]** Uses **Vector Database (ChromaDB)** to semantic search related context, enabling AI to "recall" relevant code even if it's not open.

*   **Impact Analysis (`ndoc impact`)**:
    **[NEW in 2.0]** Analyzes Git changes to predict which modules and tests are affected.

*   **Semantic Skeleton (`ndoc skeleton`)**:
    **[NEW in 2.0]** Generates high-density code skeletons (interfaces only), reducing token usage by 70%.

*   **Data Registry (`ndoc data`)**:
    **[NEW in 2.0]** Auto-extracts `dataclass`, `TypedDict`, `Enum`, `struct`, and `model` definitions into `_DATA.md`, creating a centralized data dictionary.

*   **Quality Gates (`ndoc lint` / `ndoc typecheck`)**:
    **[NEW in 2.0]** Integrated quality checks defined in `_RULES.md`, allowing you to run project-specific linting and type checking commands via a unified interface.

*   **Memory Consolidation (`ndoc lesson`)**:
    **[NEW in 2.0]** Extracts `@LESSON` tags from code comments into `_LESSONS.md`, serving as a project knowledge base and preventing repeat mistakes.

*   **System Diagnostics (`ndoc doctor`)**:
    **[NEW in 2.0]** Comprehensive environment check including OS, Python version, dependencies, Tree-sitter language bindings, and project configuration health.

---

## 4. Integration Guide (How to Use in Your Project)

Niki-docAI consists of two parts: the **Core Tool (Python CLI)** and the **IDE Extension**.

### Step 1: Install Core Tool (Python CLI)

The `ndoc` CLI is the brain of the operation. It must be installed in your environment.

**Option A: Install from Source (Recommended for Beta)**
```bash
# Clone the repository
git clone https://github.com/niki/nk_doc_ai.git
cd nk_doc_ai

# Install package
pip install .
```

**Option B: Install via Pip (Future)**
```bash
pip install niki-doc-ai
```

### Step 2: Install IDE Extension (VS Code)

The VS Code extension provides real-time integration (LSP) and context visualization.

1.  Navigate to `editors/vscode`.
2.  Package the extension:
    ```bash
    npm install
    npx vsce package
    ```
3.  Install the generated `.vsix` file in VS Code:
    *   Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac).
    *   Type `Extensions: Install from VSIX...`.
    *   Select `nk-doc-ai-vscode-x.x.x.vsix`.

*Note: The extension will automatically find the `ndoc` command if it's in your PATH or configured via `ndoc.pythonPath`.*

### Step 3: Initialize Your Project

1.  Open your target project in VS Code.
2.  Open the terminal and run:
    ```bash
    ndoc init
    ```
    This creates the `.ndoc` configuration directory and essential files:
    *   `_RULES.md`: Architecture rules and lint commands.
    *   `_SYNTAX.md`: Documentation syntax guide.

### Step 4: Generate Context

Run the full generation command to index your codebase:

```bash
ndoc all
```

You will see new files generated in your project root:
*   `_MAP.md`: Project structure map.
*   `_ARCH.md`: Architecture overview.
*   `_DEPS.md`: Dependency graph.
*   `_AI.md`: Recursive context files in each directory.

### Step 5: Configure Rules (Optional)

Edit `_RULES.md` to define your project's specific constraints:

```markdown
## !RULE
<!-- Example: Enforce Layering -->
<!-- !RULE: @LAYER(core) CANNOT_IMPORT @LAYER(ui) -->
```

Then run `ndoc check` to validate your code against these rules.

---

## 5. Development (Dogfooding)

To develop Niki-docAI itself:

1.  Open this repository in VS Code.
2.  Run `ndoc init` (we eat our own dogfood!).
3.  Use the "Launch Extension" debug configuration to test the VS Code extension.

---

## License

MIT
