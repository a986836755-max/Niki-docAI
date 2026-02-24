import * as path from 'path';
import { workspace, ExtensionContext, window, commands, Uri } from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
    const config = workspace.getConfiguration('ndoc');
    // Default to 'py' on Windows if not configured, as 'python' might not be in PATH
    const defaultPython = process.platform === 'win32' ? 'py' : 'python3';
    const pythonPath = config.get<string>('pythonPath') || defaultPython;
    
    // Server implementation (using ndoc CLI 'server' command)
    // We assume the user has 'ndoc' installed or available in the project.
    // For development, we can point to the local src/ndoc/entry.py if we detect it.
    
    let serverExecutable = pythonPath;
    let serverArgs = ['-m', 'ndoc', 'server'];

    // Auto-detect local development setup (Debugging mode)
    // In dev mode, we want to point to the actual entry.py in nk_doc_ai
    // We can use a hardcoded path for dev, or check environment variables.
    // For simplicity in this dev environment, let's check a known path.
    
    // Check if we are running in extension development host
    if (context.extensionMode === 2) { // ExtensionMode.Development
        const devRoot = "e:\\work\\appcodes\\nk_doc_ai";
        const devEntry = path.join(devRoot, 'src', 'ndoc', 'entry.py');
        serverArgs = [devEntry, 'server'];
        
        // Also set PYTHONPATH for the child process so it can find 'ndoc' module
        process.env.PYTHONPATH = path.join(devRoot, 'src');
        window.showInformationMessage(`🔧 Niki-docAI Dev Mode: Using local server at ${devEntry}`);
    } else {
        // Production mode: try to find if workspace has local ndoc source
        const workspaceRoot = workspace.workspaceFolders?.[0].uri.fsPath;
        if (workspaceRoot) {
            const localEntry = path.join(workspaceRoot, 'src', 'ndoc', 'entry.py');
            // Check if file exists (sync check for simplicity)
            const fs = require('fs');
            if (fs.existsSync(localEntry)) {
                 serverArgs = [localEntry, 'server'];
                 // If we found local source, we likely need PYTHONPATH too if not installed
                 // But let's assume if it's in workspace, user configured environment.
            }
        }
    }

    const serverOptions: ServerOptions = {
        command: serverExecutable,
        args: serverArgs,
        transport: TransportKind.stdio,
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'csharp' },
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'cpp' },
            { scheme: 'file', language: 'c' }
        ],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/.clientrc')
        }
    };

    client = new LanguageClient(
        'ndocLSP',
        'Niki-docAI LSP',
        serverOptions,
        clientOptions
    );

    client.start();
    
    window.showInformationMessage('🧠 Niki-docAI Thinking Interface Active');

    // Register custom commands
    context.subscriptions.push(commands.registerCommand('ndoc.showContext', async () => {
        const editor = window.activeTextEditor;
        if (!editor) {
            window.showErrorMessage('No active editor');
            return;
        }
        
        const uri = editor.document.uri.toString();
        try {
            // Call the custom command on the server
            const result = await client.sendRequest('workspace/executeCommand', {
                command: 'ndoc.getThinkingContext',
                arguments: [uri]
            });
            
            if (result) {
                // Show in a new output channel or virtual document
                const channel = window.createOutputChannel("Niki Context");
                channel.clear();
                channel.append(result as string);
                channel.show(true);
            } else {
                window.showInformationMessage('No context found for this file.');
            }
        } catch (e) {
            window.showErrorMessage(`Error fetching context: ${e}`);
        }
    }));
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
