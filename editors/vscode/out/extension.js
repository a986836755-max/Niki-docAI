"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const path = require("path");
const vscode_1 = require("vscode");
const node_1 = require("vscode-languageclient/node");
let client;
function activate(context) {
    const config = vscode_1.workspace.getConfiguration('ndoc');
    // Default to 'py' on Windows if not configured, as 'python' might not be in PATH
    const defaultPython = process.platform === 'win32' ? 'py' : 'python3';
    const pythonPath = config.get('pythonPath') || defaultPython;
    // Server implementation (using ndoc CLI 'server' command)
    // We assume the user has 'ndoc' installed or available in the project.
    let serverExecutable = pythonPath;
    let serverArgs = ['-m', 'ndoc', 'server'];
    let env = { ...process.env };
    // Check for 'ndoc.server.localPath' override (Dogfooding Mode)
    const localPath = config.get('server.localPath');
    if (localPath && localPath.trim() !== '') {
        const devRoot = path.resolve(localPath);
        const devEntry = path.join(devRoot, 'src', 'ndoc', 'entry.py');
        // Simple synchronous check
        const fs = require('fs');
        if (fs.existsSync(devEntry)) {
            serverArgs = [devEntry, 'server'];
            // Set PYTHONPATH so it finds the 'ndoc' package
            env['PYTHONPATH'] = path.join(devRoot, 'src');
            vscode_1.window.showInformationMessage(`🐶 Niki-docAI Dogfooding: Using local source at ${devRoot}`);
        }
        else {
            vscode_1.window.showWarningMessage(`⚠️ Niki-docAI: Local path configured but entry.py not found at ${devEntry}. Falling back to installed package.`);
        }
    }
    else if (context.extensionMode === 2) { // ExtensionMode.Development fallback
        // ... (existing dev logic, but now superseded by explicit config)
        const devRoot = "e:\\work\\appcodes\\nk_doc_ai";
        const devEntry = path.join(devRoot, 'src', 'ndoc', 'entry.py');
        serverArgs = [devEntry, 'server'];
        env['PYTHONPATH'] = path.join(devRoot, 'src');
        vscode_1.window.showInformationMessage(`🔧 Niki-docAI Dev Mode: Using local server at ${devEntry}`);
    }
    else {
        // Production mode: try to find if workspace has local ndoc source
        const workspaceRoot = vscode_1.workspace.workspaceFolders?.[0].uri.fsPath;
        if (workspaceRoot) {
            const localEntry = path.join(workspaceRoot, 'src', 'ndoc', 'entry.py');
            // Check if file exists (sync check for simplicity)
            const fs = require('fs');
            if (fs.existsSync(localEntry)) {
                serverArgs = [localEntry, 'server'];
                // If we found local source, we likely need PYTHONPATH too if not installed
                // But let's assume if it's in workspace, user configured environment.
            }
            else {
                // Try to check if 'ndoc' is installed
                // We rely on the LanguageClient startup failure to detect missing ndoc.
                // However, we can proactively check here to offer a better UX.
                const cp = require('child_process');
                try {
                    // Try to run 'python -m ndoc --help' to see if it's installed
                    cp.execSync(`${serverExecutable} -m ndoc --help`, { env: env });
                }
                catch (e) {
                    // Not installed! Prompt user to install.
                    vscode_1.window.showWarningMessage("Niki-docAI Core (ndoc) is not installed. Install now?", "Install").then(selection => {
                        if (selection === "Install") {
                            const term = vscode_1.window.createTerminal("Niki-docAI Installer");
                            term.show();
                            // Install from PyPI (future) or Git
                            term.sendText(`${serverExecutable} -m pip install git+https://github.com/niki/nk_doc_ai.git`);
                            // After install, we should restart client? 
                            // Or just tell user to reload window.
                            vscode_1.window.showInformationMessage("Installing Niki-docAI... Please reload window after completion.", "Reload").then(s => {
                                if (s === "Reload") {
                                    vscode_1.commands.executeCommand('workbench.action.reloadWindow');
                                }
                            });
                        }
                    });
                }
            }
        }
    }
    const serverOptions = {
        command: serverExecutable,
        args: [...serverArgs, '--stdio'], // Explicitly add --stdio for clarity
        options: { env: env }, // Pass the environment with PYTHONPATH
        transport: node_1.TransportKind.stdio,
    };
    const clientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'csharp' },
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'cpp' },
            { scheme: 'file', language: 'c' }
        ],
        synchronize: {
            fileEvents: vscode_1.workspace.createFileSystemWatcher('**/.clientrc')
        },
        // Handle server start failure
        errorHandler: {
            error: (error, message, count) => {
                return { action: 2 }; // Shutdown
            },
            closed: () => {
                // If server crashes or fails to start
                vscode_1.window.showErrorMessage("Niki-docAI Core (ndoc) not found or crashed.", "Install ndoc").then(selection => {
                    if (selection === "Install ndoc") {
                        const term = vscode_1.window.createTerminal("Niki-docAI Installer");
                        term.show();
                        term.sendText(`${serverExecutable} -m pip install niki-doc-ai`); // Future: pip install niki-doc-ai
                        // For now, guide them to repo? Or use local install if we are in the repo?
                        // Assuming pip install . if in repo, but extension doesn't know context.
                    }
                });
                return { action: 1 }; // Do not restart
            }
        }
    };
    client = new node_1.LanguageClient('ndocLSP', 'Niki-docAI LSP', serverOptions, clientOptions);
    client.start().catch(e => {
        vscode_1.window.showErrorMessage(`Niki-docAI Failed to Start: ${e}. Is 'ndoc' installed?`, "Install Guide").then(s => {
            if (s === "Install Guide") {
                // Open URL
                vscode_1.commands.executeCommand('vscode.open', vscode_1.Uri.parse('https://github.com/niki/nk_doc_ai#installation'));
            }
        });
    });
    vscode_1.window.showInformationMessage('🧠 Niki-docAI Thinking Interface Active');
    // Register custom commands
    context.subscriptions.push(vscode_1.commands.registerCommand('ndoc.showContext', async (uri) => {
        let editor = vscode_1.window.activeTextEditor;
        // If URI is passed (e.g. from CodeLens), try to find that document
        if (uri) {
            const doc = vscode_1.workspace.textDocuments.find(d => d.uri.toString() === uri);
            if (doc) {
                // If the document is not active, we might need to show it, 
                // but usually CodeLens is clicked on an active editor.
            }
        }
        if (!editor) {
            vscode_1.window.showErrorMessage('No active editor');
            return;
        }
        // We can reuse the hover logic or fetch context via a new request
        // For simplicity, let's just trigger the Hover manually or show a QuickPick with info
        // BUT, since we want to show the full context, let's execute a command on the server
        // Actually, we can't easily "trigger hover" programmatically at a specific position from here without more work.
        // Let's just show an Information Message for now, or an Output Channel
        const outputChannel = vscode_1.window.createOutputChannel("Niki-docAI Context");
        outputChannel.show(true);
        outputChannel.appendLine("Fetching context...");
        try {
            // Call the custom command on the server
            // Note: client.sendRequest('workspace/executeCommand', ...) is the standard way
            const result = await client.sendRequest('workspace/executeCommand', {
                command: 'ndoc.getThinkingContext',
                arguments: [editor.document.uri.toString()]
            });
            outputChannel.clear();
            if (result) {
                outputChannel.appendLine("🧠 Niki-docAI Context Rules:");
                outputChannel.appendLine(`File: ${editor.document.uri.fsPath}`);
                outputChannel.appendLine("========================================");
                outputChannel.appendLine(result);
                outputChannel.appendLine("========================================");
                outputChannel.appendLine("(You can copy this context to your AI Assistant)");
            }
            else {
                outputChannel.appendLine("No context found or error occurred.");
            }
        }
        catch (e) {
            outputChannel.appendLine(`Error fetching context: ${e}`);
        }
    }));
    context.subscriptions.push(vscode_1.commands.registerCommand('ndoc.restartServer', async () => {
        if (!client) {
            vscode_1.window.showErrorMessage('Niki-docAI LSP is not running');
            return;
        }
        await client.stop();
        client.start();
        vscode_1.window.showInformationMessage('Niki-docAI LSP restarted');
    }));
}
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
//# sourceMappingURL=extension.js.map