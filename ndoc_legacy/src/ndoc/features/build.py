import sys
from pathlib import Path
from ndoc.core import console
from ndoc.core import utils
from ndoc.features import docs

def cmd_build(root):
    console.step("[Phase 1] Generating FBS...")
    flatc = utils.find_flatc()

    if not flatc:
        console.error("'flatc' not found in PATH. Please install FlatBuffers compiler (v23.5.26+).")
        console.info("    You can download it from https://github.com/google/flatbuffers/releases")
        sys.exit(1)

    schema_dir = root / "schemas"
    engine_gen_dir = root / "engine" / "generated"
    client_gen_dir = root / "client" / "lib" / "schemas"

    utils.ensure_directory(engine_gen_dir)
    utils.ensure_directory(client_gen_dir)

    fbs_files = list(schema_dir.glob("*.fbs"))
    if not fbs_files:
        console.warning(f"No .fbs files found in {schema_dir}")
    else:
        for fbs in fbs_files:
            console.log(f"    Processing {fbs.name}...")
            # C++
            utils.run_command(f'"{flatc}" --cpp --gen-object-api -o "{engine_gen_dir}" "{fbs}"', cwd=root)
            # Dart
            utils.run_command(f'"{flatc}" --dart -o "{client_gen_dir}" "{fbs}"', cwd=root)

    console.step("[Phase 2] Validate DNA (Docs Sync Scan)...")
    # We use internal call now, but catch exception to avoid blocking build if it's just a warning?
    # Original code: run_command(..., fail_exit=False) inside cmd_doc, but cmd_build didn't have fail_exit=False in the original script?
    # Let's check original cmd_build:
    # utils.run_command(f'"{sys.executable}" "{check_script}" --scan', cwd=root)
    # This implies it would fail exit if scan failed.
    # But in cmd_doc it had try-except.
    # Let's assume strict build for now.
    docs.audit_scan()

    console.step("[Phase 3] Compiling Code...")
    engine_dir = root / "engine"
    build_dir = engine_dir / "build"

    # Configure
    utils.run_command(f'cmake -B "{build_dir}" -S "{engine_dir}" -DCMAKE_BUILD_TYPE=Release', cwd=root)

    # Build
    utils.run_command(f'cmake --build "{build_dir}" --config Release', cwd=root)

    console.success("Build Complete.")
