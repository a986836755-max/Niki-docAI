
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
    
    // Server implementation
    let command = pythonPath;
    let args = ['-m', 'ndoc', 'server'];
    let env = { ...process.env };

    // 1. Check for 'ndoc.server.localPath' override (Dogfooding/Dev Mode)
    const localPath = config.get<string>('server.localPath');
    if (localPath && localPath.trim() !== '') {
        const devRoot = path.resolve(localPath);
        const devEntry = path.join(devRoot, 'src', 'ndoc', 'entry.py');
        
        const fs = require('fs');
        if (fs.existsSync(devEntry)) {
            // Run from source: python src/ndoc/entry.py server
            command = pythonPath;
            args = [devEntry, 'server'];
            // Set PYTHONPATH so it finds the 'ndoc' package
            env['PYTHONPATH'] = path.join(devRoot, 'src');
            window.showInformationMessage(`🐶 Niki-docAI Dogfooding: Using local source at ${devRoot}`);
        } else {
            window.showWarningMessage(`⚠️ Niki-docAI: Local path configured but entry.py not found at ${devEntry}. Falling back to installed package.`);
        }
    } 

    // 2. Configure Server Options
    const serverOptions: ServerOptions = {
        command: command,
        args: args,
        options: { env: env },
        transport: TransportKind.stdio,
    };

    // 3. Configure Client Options
    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'csharp' },
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' },
            { scheme: 'file', language: 'cpp' },
            { scheme: 'file', language: 'c' },
            { scheme: 'file', language: 'go' },
            { scheme: 'file', language: 'rust' },
            { scheme: 'file', language: 'java' }
        ],
        synchronize: {
            fileEvents: workspace.createFileSystemWatcher('**/.clientrc')
        },
    };

    // 4. Create and Start Client
    client = new LanguageClient(
        'ndocLSP',
        'Niki-docAI LSP',
        serverOptions,
        clientOptions
    );

    client.start().catch(e => {
         window.showErrorMessage(`Niki-docAI Failed to Start: ${e}. Is 'ndoc' installed? Try 'pip install niki-doc-ai'`, "Install Guide").then(s => {
             if (s === "Install Guide") {
                 commands.executeCommand('vscode.open', Uri.parse('https://github.com/a986836755-max/Niki-docAI#installation'));
             }
         });
    });
    
    // 5. Register Commands
    const registerCmd = (cmd: string, cliArg: string) => {
        context.subscriptions.push(commands.registerCommand(cmd, () => {
            const term = window.createTerminal(`Niki-docAI: ${cliArg}`);
            term.show();
            // Construct command string based on current mode
            let cmdStr = '';
            if (args[0] && args[0].endsWith('entry.py')) {
                 // Source mode
                 const envPath = env['PYTHONPATH'] || '';
                 if (process.platform === 'win32') {
                    cmdStr = `$env:PYTHONPATH="${envPath}"; & "${command}" "${args[0]}" ${cliArg}`;
                 } else {
                    cmdStr = `PYTHONPATH="${envPath}" "${command}" "${args[0]}" ${cliArg}`;
                 }
            } else {
                // Installed mode: python -m ndoc <cmd>
                cmdStr = `"${command}" -m ndoc ${cliArg}`;
            }
            term.sendText(cmdStr);
        }));
    };

    registerCmd('ndoc.init', 'init');
    registerCmd('ndoc.generate', 'all');
    registerCmd('ndoc.check', 'check');
    registerCmd('ndoc.doctor', 'doctor');
    registerCmd('ndoc.watch', 'watch');
    
    // Special command: Show Context
    context.subscriptions.push(commands.registerCommand('ndoc.showContext', (uri: Uri) => {
        if (!uri) {
            if (window.activeTextEditor) {
                uri = window.activeTextEditor.document.uri;
            } else {
                window.showErrorMessage("No active file to show context for.");
                return;
            }
        }
        const term = window.createTerminal("Niki-docAI: Context");
        term.show();
        // Use 'ndoc prompt <file> --focus'
        let cmdStr = '';
        if (args[0] && args[0].endsWith('entry.py')) {
             const envPath = env['PYTHONPATH'] || '';
             if (process.platform === 'win32') {
                cmdStr = `$env:PYTHONPATH="${envPath}"; & "${command}" "${args[0]}" prompt "${uri.fsPath}" --focus`;
             } else {
                cmdStr = `PYTHONPATH="${envPath}" "${command}" "${args[0]}" prompt "${uri.fsPath}" --focus`;
             }
        } else {
            cmdStr = `"${command}" -m ndoc prompt "${uri.fsPath}" --focus`;
        }
        term.sendText(cmdStr);
    }));

    window.showInformationMessage('🧠 Niki-docAI Active');
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
