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

## 3. The Solution (Five Core Domains)

Niki-docAI categorizes its capabilities into five strategic domains to automate "Context Ops":

### 3.1 🗺️ Panoramic Navigation (全景导航)
*Give AI a complete map of your project without overwhelming its context window.*

*   **Context Map (`ndoc map`)**:
    Generates a high-level navigational map of your project structure with **Precise Line References** (e.g., `file.py#L1`), helping AI find the right files instantly.
*   **AI Context (`ndoc context`)**:
    Produces a recursive, token-optimized summary of your codebase, including file descriptions, symbols, and relationships.
*   **Skeleton Extraction (`ndoc skeleton`)**:
    Extracts high-density code skeletons (interfaces/signatures only) from source files, reducing token usage by up to 70% while retaining structural information.
*   **LSP Query (`ndoc lsp`)**:
    Provides a CLI interface to query the Language Server Protocol for symbols and definitions, enabling precise code navigation.

### 3.2 🏗️ Architecture Governance (架构治理)
*Ensure your project structure remains clean and adheres to defined rules.*

*   **Architecture View (`ndoc arch`)**:
    Visualizes the high-level architecture, technology stack, and module boundaries.
*   **Dependency Analysis (`ndoc deps`)**:
    Detects and reports circular dependencies using Tarjan's algorithm and generates Mermaid diagrams for visualization.
*   **Constraint Checking (`ndoc check`)**:
    Enforces architectural rules (e.g., Layering) defined in `_RULES.md` using `!RULE` syntax. Prevents "Architecture Drift".
*   **Impact Analysis (`ndoc impact`)**:
    Analyzes Git changes to predict which downstream modules and tests might be affected by current modifications.
*   **Quality Gates (`ndoc lint`)**:
    Integrated wrapper for project-specific linting commands, ensuring code quality standards are met before commit.

### 3.3 🧠 Knowledge Management (知识管理)
*Capture and recall project knowledge, decisions, and lessons learned.*

*   **Memory Archive (`ndoc archive`)**:
    Stores and retrieves long-term project memories using Vector Database embeddings.
*   **Short-term Memory (Hippocampus)**:
    Manages active context and recent interactions to maintain continuity during a coding session.
*   **Architecture Decision Records (`ndoc adr`)**:
    Automatically extracts `@DECISION` tags from comments into `_ADR.md`, creating a living history of architectural choices.
*   **Data Dictionary (`ndoc data`)**:
    Auto-extracts data schemas (`dataclass`, `TypedDict`, `Enum`) into `_DATA.md`, creating a centralized data registry.
*   **Project Stats (`ndoc stats`)**:
    Tracks code metrics (lines of code, complexity) and scans for `TODO` items to monitor project health.
*   **Smart Prompt (`ndoc prompt`)**:
    Generates optimized prompts for AI, combining rules, context summaries, and relevant API references.

### 3.4 ⚡ Environment & Efficiency (环境效能)
*Keep the development environment healthy and tools ready.*

*   **System Doctor (`ndoc doctor`)**:
    Comprehensive environment check including OS, Python version, dependencies, and Tree-sitter language bindings.
*   **Project Init (`ndoc init`)**:
    Initializes a new Niki-docAI project with standard configuration files (`_RULES.md`, `.ndoc.toml`).
*   **Context Injection (`ndoc inject`)**:
    Injects context markers and headers into source files to aid AI understanding.
*   **Capability Check (`ndoc caps`)**:
    Verifies installed capabilities and dynamic language support (e.g., checking if Rust parser is loaded).
*   **Cleanup (`ndoc clean`)**:
    Removes generated temporary files and caches to keep the workspace tidy.

### 3.5 🚀 Advanced Extensions (高级扩展)
*Extend Niki-docAI with powerful integrations and automation.*

*   **Watch Mode (`ndoc watch`)**:
    A daemon that monitors file changes and automatically updates documentation and indexes in real-time.
*   **IDE Server (`ndoc server`)**:
    A Language Server Protocol (LSP) implementation that powers IDE extensions with Niki-docAI capabilities.
*   **Plugin SDK**:
    A robust SDK (`ndoc.sdk.interfaces`) allowing developers to create custom plugins for specific languages or frameworks.
*   **Full Pilot (`ndoc all` / `ndoc pilot`)**:
    Runs the complete analysis pipeline to generate all documentation and reports in one go.

---

## 4. Usage Guide (Command Line Interface)

Niki-docAI provides a rich set of commands. Here are the most common operations:

### 🚀 Core Workflow
```bash
# Initialize a new project
ndoc init

# Run full analysis (Generate all docs)
ndoc all
# Alias: ndoc pilot

# Start watch mode (Auto-update on file change)
ndoc watch
```

### 🗺️ Navigation & Context
```bash
# Update just the structure map (_MAP.md)
ndoc map

# Update detailed AI context (_AI.md)
ndoc context

# Generate a skeleton for a specific file (to paste to AI)
ndoc skeleton src/main.py

# Query LSP for symbol definition
ndoc lsp MyClass
```

### 🏗️ Architecture & Quality
```bash
# Check for architecture rule violations (!RULE)
ndoc check

# Visualize dependencies and detect cycles
ndoc deps

# Generate high-level architecture view
ndoc arch

# Analyze impact of current Git changes
ndoc impact
```

### 🧠 Knowledge & Prompting
```bash
# Generate an optimized prompt for a specific file
ndoc prompt src/core/logic.py --focus

# Search codebase semantically (requires vector db)
ndoc search "how does authentication work?"

# Update project statistics and TODO tracking
ndoc stats
```

### ⚡ Maintenance
```bash
# Check environment health
ndoc doctor

# Clean generated artifacts
ndoc clean

# Self-update (git pull)
ndoc update
```

---

## 5. Integration Guide (How to Use in Your Project)

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

(Coming Soon)
