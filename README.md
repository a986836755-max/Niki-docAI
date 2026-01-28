# Niki-docAI

> **Context Ops & Architecture Guard for NikiDice**

**Niki-docAI** is an intelligent toolchain designed to enforce **Data-Oriented Design (DOD)** principles and maintain "Living Documentation" for the NikiDice engine. It bridges the gap between Code (Reality) and Documentation (Knowledge), ensuring that architecture constraints are not just written, but verified.

## Core Philosophy

*   **Single Source of Truth**: Documentation should be generated from or verified against code.
*   **Architecture as Code**: Project rules (Isolation, FFI barriers) are checked via static analysis.
*   **Context Aware**: Auto-detects tech stack, generates dependency graphs, and maps project structure.

## Key Features

*   **`ndoc doctor`**: Diagnoses environment health and toolchain dependencies.
*   **`ndoc map`**: Auto-generates the project navigation map (`_MAP.md`) and tech stack inventory (`_TECH.md`).
*   **`ndoc graph`**: Visualizes module dependencies and highlights architecture violations.
*   **`ndoc verify`**: Enforces strict DOD rules (e.g., "No Exceptions in Core", "Engine/Client Isolation").

## Installation

```bash
# Install in editable mode
pip install -e packages/Niki_docAI
```

## Usage

```bash
ndoc doctor       # Check environment
ndoc map          # Update project map & tech stack
ndoc verify       # Verify architecture rules
```
