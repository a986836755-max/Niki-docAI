"""
Simple test client to verify LSP Server initialization.
简单的测试脚本，验证 LSP Server 的启动和初始化。
"""
import subprocess
import json
import sys
import time

def test_lsp_init():
    # 启动服务器进程
    process = subprocess.Popen(
        [sys.executable, "-m", "ndoc.lsp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="src"
    )

    # 构造 LSP Initialize 请求
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": None,
            "rootPath": ".",
            "rootUri": "file:///.",
            "capabilities": {}
        }
    }

    request_str = json.dumps(init_request)
    message = f"Content-Length: {len(request_str)}\r\n\r\n{request_str}"
    
    print("Sending initialize request...")
    process.stdin.write(message)
    process.stdin.flush()

    # 读取响应
    time.sleep(2)  # 等待索引完成
    
    # 读取 Content-Length
    line = process.stdout.readline()
    print(f"Server response header: {line.strip()}")
    
    if "Content-Length" in line:
        length = int(line.split(":")[1].strip())
        process.stdout.readline() # 跳过空行
        response = process.stdout.read(length)
        print("Server response body:")
        print(json.dumps(json.loads(response), indent=2))

    process.terminate()

if __name__ == "__main__":
    test_lsp_init()
