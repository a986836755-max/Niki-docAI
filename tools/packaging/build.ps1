$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$dartDll = Join-Path $root "src\ndoc\parsing\langs\bin\tree_sitter_dart.dll"
$venv = Join-Path $root ".ndoc\packaging_venv"
$python = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path $python)) {
  py -m venv $venv
}
& $python -m pip install -U pip
& $python -m pip install -r (Join-Path $PSScriptRoot "requirements-packaging.txt")
& $python -m pip install $root

$addDataArgs = @()
if (Test-Path $dartDll) {
  $addDataArgs = @("--add-data", "$dartDll;ndoc/parsing/langs/bin")
}

& $python -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --name ndoc `
  --distpath (Join-Path $root "dist") `
  --workpath (Join-Path $root "build") `
  --specpath (Join-Path $root "build_spec") `
  --collect-submodules ndoc `
  --collect-all tree_sitter `
  --collect-all tree_sitter_python `
  --collect-all tree_sitter_javascript `
  --collect-all tree_sitter_typescript `
  --collect-all tree_sitter_go `
  --collect-all tree_sitter_rust `
  --collect-all tree_sitter_cpp `
  --collect-all tree_sitter_c_sharp `
  --collect-all tree_sitter_java `
  --collect-all tree_sitter_json `
  @addDataArgs `
  (Join-Path $PSScriptRoot "ndoc_entry.py")
