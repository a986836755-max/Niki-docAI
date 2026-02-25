# Niki-docAI 2.0 (Rebirth)

> **Context Ops & Architecture Guard for AI-Assisted Development**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
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
    **[NEW in 2.0]** Detects and reports circular dependencies in your codebase using Tarjan's algorithm.

*   **Intelligent Retrieval (`ndoc prompt --focus`)**:
    **[NEW in 2.0]** Uses **Vector Database (ChromaDB)** to semantic search related context, enabling AI to "recall" relevant code even if it's not open.

*   **Impact Analysis (`ndoc impact`)**:
    **[NEW in 2.0]** Analyzes Git changes to predict which modules and tests are affected.

*   **Semantic Skeleton (`ndoc skeleton`)**:
    **[NEW in 2.0]** Generates high-density code skeletons (interfaces only), reducing token usage by 70%.

---

## 4. Installation & Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/nk_doc_ai.git
cd nk_doc_ai

# Install
pip install .
```

### Quick Start

**1. Initialize**

```bash
# Initialize Niki-docAI (Create _RULES.md, _SYNTAX.md)
ndoc init
```

**2. Generate Context**

```bash
# Generate/Update ALL documentation (Arch + Context + Status + Deps)
ndoc all
```

**3. AI Assistance**

```bash
# Generate context prompt for a specific file (Smart Retrieval)
ndoc prompt src/main.py --focus

# View high-density skeleton of a file
ndoc skeleton src/utils.py
```

**4. Architecture Governance**

```bash
# Check for architecture violations
ndoc check

# Detect circular dependencies
ndoc deps

# Analyze impact of current changes
ndoc impact
```

---

## 5. Configuration

Configure your project via `_RULES.md`:

```markdown
## Scanning Rules
- `!IGNORE`: node_modules, dist, build, .git

## Architecture Rules
- `!RULE`: @LAYER(core) CANNOT_IMPORT @LAYER(ui)
- `!RULE`: @FORBID(hardcoded_paths)
```

---

## 6. Supported Languages

Built-in Tree-sitter integration for polyglot codebases:
*   **Python** (`.py`)
*   **JavaScript/TypeScript** (`.js`, `.ts`, `.jsx`, `.tsx`)
*   **Java** (`.java`)
*   **Go** (`.go`)
*   **C/C++** (`.cpp`, `.h`)
*   **C#** (`.cs`)
*   **Rust** (`.rs`)
*   **Dart** (`.dart`)

---

*Powered by Niki-docAI Team*
