"""
LSP Server Test Client (Refined)
"""
import subprocess
import json
import sys
import time
import threading
import os

def log(msg):
    print(f"[*] {msg}")

def read_stream(stream, name):
    while True:
        line = stream.readline()
        if not line:
            break
        clean_line = line.strip()
        if clean_line:
            print(f"[{name}] {clean_line}")
            if "Content-Length" in clean_line:
                length = int(clean_line.split(":")[1].strip())
                stream.readline() # skip \r\n
                body = stream.read(length)
                print(f"[{name}] BODY: {body}")

def test_lsp():
    cmd = [sys.executable, "-m", "ndoc.lsp_server"]
    log(f"Starting LSP Server: {' '.join(cmd)}")
    
    # 设置 PYTHONPATH 确保能找到 ndoc 模块
    env = os.environ.copy()
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    env["PYTHONPATH"] = src_dir + os.path.pathsep + env.get("PYTHONPATH", "")

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(src_dir), # 在项目根目录运行
        env=env
    )

    # 启动监听线程
    threading.Thread(target=read_stream, args=(process.stdout, "STDOUT"), daemon=True).start()
    threading.Thread(target=read_stream, args=(process.stderr, "STDERR"), daemon=True).start()

    # 发送 Initialize
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "rootPath": os.getcwd(),
            "capabilities": {}
        }
    }
    
    body = json.dumps(init_msg)
    # 显式使用 \r\n 换行符
    msg = f"Content-Length: {len(body)}\r\n\r\n{body}"
    
    log(f"Sending 'initialize' request (Length: {len(body)})...")
    process.stdin.write(msg)
    process.stdin.flush()
    log("Write and flush completed.")

    # 发送 DID_SAVE 模拟
    save_msg = {
        "jsonrpc": "2.0",
        "method": "textDocument/didSave",
        "params": {
            "textDocument": {
                "uri": f"file:///{os.path.abspath('src/ndoc/lsp_server.py').replace(os.sep, '/')}"
            }
        }
    }
    body = json.dumps(save_msg)
    msg = f"Content-Length: {len(body)}\r\n\r\n{body}"
    log("Sending 'didSave' request to trigger re-indexing and diagnostics...")
    process.stdin.write(msg)
    process.stdin.flush()

    # 等待诊断输出
    time.sleep(3)
    
    log("Terminating test.")
    process.terminate()

if __name__ == "__main__":
    test_lsp()
