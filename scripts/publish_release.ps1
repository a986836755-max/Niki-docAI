# Publish Release Script
# Usage: ./scripts/publish_release.ps1 <version>
param(
    [string]$Version = "2.0.0"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Preparing Release v$Version for GitHub..." -ForegroundColor Cyan

# 1. Clean previous builds
Write-Host "cleaning up..."
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "src/*.egg-info") { Remove-Item -Recurse -Force "src/*.egg-info" }

# 2. Build Python Package
Write-Host "📦 Building Python Package..."
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    py -m build --no-isolation
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    python -m build --no-isolation
} else {
    Write-Error "Python not found! Please install Python."
}

# 3. Build VS Code Extension
Write-Host "🧩 Building VS Code Extension..."
Push-Location "editors/vscode"
# Ensure clean build
if (Test-Path "out") { Remove-Item -Recurse -Force "out" }
if (Test-Path "*.vsix") { Remove-Item -Force "*.vsix" }

# Use .cmd on Windows
if ($IsWindows) {
    npm.cmd install
    npm.cmd run compile
    npx.cmd vsce package --out "nk-doc-ai-vscode-$Version.vsix"
} else {
    npm install
    npm run compile
    npx vsce package --out "nk-doc-ai-vscode-$Version.vsix"
}

# Move VSIX to dist for unified release
Move-Item "nk-doc-ai-vscode-$Version.vsix" "../../dist/"
Pop-Location

# 4. Summary
Write-Host "`n✅ Build Complete! Artifacts in dist/:" -ForegroundColor Green
Get-ChildItem "dist" | Select-Object Name, Length

Write-Host "`nTo publish to GitHub:" -ForegroundColor Yellow
Write-Host "1. Create a new Release on: https://github.com/a986836755-max/Niki-docAI/releases/new"
Write-Host "2. Tag version: v$Version"
Write-Host "3. Upload the following files from 'dist/':"
Get-ChildItem "dist" | ForEach-Object { Write-Host "   - $($_.Name)" }
Write-Host "4. (Optional) Publish Python package to PyPI: twine upload dist/*"
Write-Host "5. (Optional) Publish Extension to Marketplace: vsce publish"
