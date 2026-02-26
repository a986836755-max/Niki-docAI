set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
dart_dll="$root/src/ndoc/parsing/langs/bin/tree_sitter_dart.dll"
venv="$root/.ndoc/packaging_venv"
python="$venv/bin/python"

if [ ! -f "$python" ]; then
  python3 -m venv "$venv"
fi
"$python" -m pip install -U pip
"$python" -m pip install -r "$root/tools/packaging/requirements-packaging.txt"
"$python" -m pip install "$root"

add_data=()
if [ -f "$dart_dll" ]; then
  add_data+=(--add-data "$dart_dll:ndoc/parsing/langs/bin")
fi

"$python" -m PyInstaller \
  --noconfirm \
  --clean \
  --onefile \
  --name ndoc \
  --distpath "$root/dist" \
  --workpath "$root/build" \
  --specpath "$root/build_spec" \
  --collect-submodules ndoc \
  --collect-all tree_sitter \
  --collect-all tree_sitter_python \
  --collect-all tree_sitter_javascript \
  --collect-all tree_sitter_typescript \
  --collect-all tree_sitter_go \
  --collect-all tree_sitter_rust \
  --collect-all tree_sitter_cpp \
  --collect-all tree_sitter_c_sharp \
  --collect-all tree_sitter_java \
  --collect-all tree_sitter_json \
  "${add_data[@]}" \
  "$root/tools/packaging/ndoc_entry.py"
