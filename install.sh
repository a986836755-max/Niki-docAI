#!/bin/bash
# Niki-docAI Unified Installer (Unix/Linux/macOS)

echo "🐶 Niki-docAI: Starting One-Click Installation..."

# 1. Check Python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Error: Python not found. Please install Python 3.9+."
        exit 1
    fi
fi

echo "✅ Found Python: $PYTHON_CMD"

# 2. Install Core Package (ndoc)
echo "📦 Installing ndoc core..."
$PYTHON_CMD -m pip install . --quiet
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install ndoc package."
    exit 1
fi

# 3. Ensure CLI Shim
echo "🔗 Configuring CLI shim..."
# Run ndoc module to trigger bootstrap logic (creates shim in ~/.ndoc/bin)
$PYTHON_CMD -m ndoc --help > /dev/null 2>&1

# 4. Check/Install VS Code Extension
echo "🧩 Configuring VS Code Extension..."
if command -v code &> /dev/null; then
    VSIX_PATH=$(find editors/vscode -name "*.vsix" | head -n 1)
    if [ -n "$VSIX_PATH" ]; then
        echo "   Found extension: $(basename $VSIX_PATH)"
        code --install-extension "$VSIX_PATH" --force
        if [ $? -eq 0 ]; then
            echo "✅ VS Code extension installed."
        else
            echo "⚠️ Warning: Failed to install VS Code extension."
        fi
    else
        # Try to build if npm available
        if command -v npm &> /dev/null; then
            echo "   Building extension from source..."
            cd editors/vscode
            npm install --silent
            npx vsce package
            VSIX_PATH=$(find . -name "*.vsix" | head -n 1)
            if [ -n "$VSIX_PATH" ]; then
                code --install-extension "$VSIX_PATH" --force
                echo "✅ VS Code extension built and installed."
            fi
            cd ../..
        else
            echo "⚠️ Warning: No .vsix found and npm not available. Skipping extension install."
        fi
    fi
else
    echo "⚠️ Warning: 'code' command not found. Skipping VS Code extension install."
fi

echo ""
echo "🎉 Niki-docAI installed successfully!"
echo "   Run 'ndoc init' in your project to get started."
