# ndoc Module AI Context

@DOMAIN: Core Toolchain
@AGGREGATE
@STATUS: Stable

## 1. Overview
The `ndoc` package is the heart of the Niki-docAI toolchain. It implements the "Architecture as Code" philosophy, providing a suite of CLI tools to manage documentation, enforce architectural rules, and visualize system structure.

Key capabilities:
- **Context Ops**: Auto-maintenance of `_AI.md` and meta-files.
- **Architecture Guard**: Dependency analysis and rule verification.
- **Smart Init**: Zero-config project initialization.

## 2. Architecture
<!-- NIKI_AUTO_DOC_START -->
### Files
<!-- (Aggregated View) -->
- [__init__.py](__init__.py): Niki Toolchain
- [cli.py](cli.py)
- [core/__init__.py](core/__init__.py): Core modules
- [core/config.py](core/config.py): Core Configuration for Niki Context Ops
- [core/console.py](core/console.py)
- [core/initializer.py](core/initializer.py)
- [core/utils.py](core/utils.py)
- [features/__init__.py](features/__init__.py): Feature modules
- [features/build.py](features/build.py)
- [features/docs.py](features/docs.py)
- [features/doctor.py](features/doctor.py)
- [features/fix.py](features/fix.py)
- [features/graph.py](features/graph.py)
- [features/link.py](features/link.py)
- [features/log.py](features/log.py)
- [features/map.py](features/map.py)
- [features/module.py](features/module.py)
- [features/tech.py](features/tech.py)
- [features/test.py](features/test.py)
- [features/verify.py](features/verify.py)
<!-- NIKI_AUTO_DOC_END -->

## 3. Constraints (!RULE)
- !RULE: (Add constraint here)

## 4. Map
- [README.md](README.md)

## 5. Tool Config
<!-- Files/Folders exempted from document synchronization audit -->
<!-- @CHECK_IGNORE: generated/ -->
