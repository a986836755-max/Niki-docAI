import * as path from 'path';
import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('NDoc AI');
    outputChannel.appendLine('NDoc AI Extension is now active!');

    const config = vscode.workspace.getConfiguration('ndoc');
    const pythonPath = config.get<string>('pythonPath') || 'python';
    
    // 获取项目根目录
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        outputChannel.appendLine('No workspace folder found. LSP server will not start.');
        return;
    }
    const projectRoot = workspaceFolders[0].uri.fsPath;
    
    // 假设 ndoc 源码就在当前插件所在的项目中，或者在工作区中
    // 这里的逻辑可以根据实际部署方式调整
    const ndocSrcPath = path.join(projectRoot, 'src');
    outputChannel.appendLine(`Using PYTHONPATH: ${ndocSrcPath}`);

    const serverOptions: ServerOptions = {
        command: pythonPath,
        args: ['-m', 'ndoc.lsp_server'],
        options: {
            env: {
                ...process.env,
                "PYTHONPATH": ndocSrcPath,
                "PYTHONUNBUFFERED": "1"
            }
        }
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'python' },
            { scheme: 'file', language: 'dart' },
            { scheme: 'file', language: 'javascript' },
            { scheme: 'file', language: 'typescript' }
        ],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*')
        },
        outputChannel: outputChannel
    };

    client = new LanguageClient(
        'ndocAI',
        'NDoc AI Language Server',
        serverOptions,
        clientOptions
    );

    outputChannel.appendLine('Starting NDoc AI Language Server...');
    client.start().then(() => {
        outputChannel.appendLine('LSP Server started successfully.');
    }).catch(err => {
        outputChannel.appendLine(`Failed to start LSP Server: ${err}`);
    });
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
