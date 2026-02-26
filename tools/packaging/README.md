# Self-Contained Release

## Build (Windows)

```powershell
tools\packaging\build.ps1
```

## Build (macOS/Linux)

```bash
bash tools/packaging/build.sh
```

## Output

- `dist/ndoc` (macOS/Linux)
- `dist/ndoc.exe` (Windows)

## Notes

- Build host must have Python 3.9+ and internet access for dependency download.
- Builds use a local virtualenv in `.ndoc/packaging_venv`.
- The build bundles language parsers present in the build environment.
- Dart DLL is bundled when `src/ndoc/parsing/langs/bin/tree_sitter_dart.dll` exists.
