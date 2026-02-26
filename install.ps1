# Niki-docAI Unified Installer (Windows)

Write-Host "🐶 Niki-docAI: Starting One-Click Installation..." -ForegroundColor Cyan

# 1. Check Python
$pythonCmd = "python"
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Python not found. Please install Python 3.9+." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found Python: $pythonCmd" -ForegroundColor Green

# 2. Install Core Package (ndoc)
Write-Host "📦 Installing ndoc core..." -ForegroundColor Yellow
& $pythonCmd -m pip install . --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Failed to install ndoc package." -ForegroundColor Red
    exit 1
}

# 3. Ensure CLI Shim
Write-Host "🔗 Configuring CLI shim..." -ForegroundColor Yellow
# Run ndoc module to trigger bootstrap logic (creates shim in ~/.ndoc/bin)
& $pythonCmd -m ndoc --help > $null 2>&1

# 4. Check/Install VS Code Extension
Write-Host "🧩 Configuring VS Code Extension..." -ForegroundColor Yellow
if (Get-Command code -ErrorAction SilentlyContinue) {
    $vsixPath = Get-ChildItem "editors/vscode/*.vsix" | Select-Object -First 1
    if ($vsixPath) {
        Write-Host "   Found extension: $($vsixPath.Name)" -ForegroundColor Cyan
        code --install-extension $vsixPath.FullName --force
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ VS Code extension installed." -ForegroundColor Green
        } else {
            Write-Host "⚠️ Warning: Failed to install VS Code extension." -ForegroundColor Yellow
        }
    } else {
        # Try to build if npm available
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            Write-Host "   Building extension from source..." -ForegroundColor Cyan
            Push-Location "editors/vscode"
            npm install --silent
            npx vsce package
            $vsixPath = Get-ChildItem "*.vsix" | Select-Object -First 1
            if ($vsixPath) {
                code --install-extension $vsixPath.FullName --force
                Write-Host "✅ VS Code extension built and installed." -ForegroundColor Green
            }
            Pop-Location
        } else {
            Write-Host "⚠️ Warning: No .vsix found and npm not available. Skipping extension install." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "⚠️ Warning: 'code' command not found. Skipping VS Code extension install." -ForegroundColor Yellow
}

Write-Host "`n🎉 Niki-docAI installed successfully!" -ForegroundColor Green
Write-Host "   Run 'ndoc init' in your project to get started." -ForegroundColor Cyan
