"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
const node_1 = require("vscode-languageclient/node");
let client;
let outputChannel;
function activate(context) {
    outputChannel = vscode.window.createOutputChannel('NDoc AI');
    outputChannel.appendLine('NDoc AI Extension is now active!');
    const config = vscode.workspace.getConfiguration('ndoc');
    const pythonPath = config.get('pythonPath') || 'python';
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
    const serverOptions = {
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
    const clientOptions = {
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
    client = new node_1.LanguageClient('ndocAI', 'NDoc AI Language Server', serverOptions, clientOptions);
    outputChannel.appendLine('Starting NDoc AI Language Server...');
    client.start().then(() => {
        outputChannel.appendLine('LSP Server started successfully.');
    }).catch(err => {
        outputChannel.appendLine(`Failed to start LSP Server: ${err}`);
    });
}
exports.activate = activate;
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map