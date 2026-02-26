
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("src").resolve()))

def run_command(cmd, cwd=None):
    start = time.time()
    # Run with current python interpreter
    full_cmd = [sys.executable, "-m", "ndoc"] + cmd
    print(f"Running: {' '.join(full_cmd)}")
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    # Use a dedicated cache directory for benchmark to avoid locks
    # Use timestamp to ensure uniqueness if previous runs hang
    bench_cache = cwd / ".ndoc" / f"bench_cache_{int(time.time())}"
    env["NDOC_CACHE_DIR"] = str(bench_cache)
    # Disable parallel execution for benchmark to avoid complexity and hangs on Windows
    env["NDOC_PARALLEL"] = "0"
    
    # Don't capture output, just let it stream to see if it hangs
    # But we want to measure time and check success
    # Let's use Popen
    
    process = subprocess.Popen(
        full_cmd, 
        cwd=cwd, 
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    stdout_lines = []
    stderr_lines = []
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(f"  [STDOUT] {output.strip()}")
            stdout_lines.append(output)
            
    # Read remaining stderr
    for line in process.stderr:
        print(f"  [STDERR] {line.strip()}")
        stderr_lines.append(line)
        
    returncode = process.poll()
    end = time.time()
    
    class Result:
        def __init__(self, rc, out, err):
            self.returncode = rc
            self.stdout = "".join(out)
            self.stderr = "".join(err)
            
    return Result(returncode, stdout_lines, stderr_lines), end - start

def main():
    root = Path(".").resolve()
    print(f"Benchmark Root: {root}")
    
    # 1. Setup / Cleanup
    print("\n--- 1. Cleanup ---")
    artifacts = ["_AI.md", "_ARCH.md", "_DEPS.md", "_STATUS.md", "_MEMORY.md", "_DATA.md"]
    cache_dir = root / ".ndoc" / "cache_v2"
    
    for f in artifacts:
        p = root / f
        if p.exists():
            try:
                p.unlink()
                print(f"Deleted {f}")
            except:
                pass
            
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            print(f"Deleted cache: {cache_dir}")
        except PermissionError:
            print(f"⚠️ Could not delete main cache (Locked): {cache_dir}")
            
    # We use dynamic cache dir, no need to clean old ones explicitly here
    # bench_cache = root / ".ndoc" / "bench_cache"
    # if bench_cache.exists():
    #     try:
    #         shutil.rmtree(bench_cache)
    #         print(f"Deleted benchmark cache: {bench_cache}")
    #     except Exception as e:
    #         print(f"⚠️ Could not delete benchmark cache: {e}")
        
    # 2. Cold Start
    print("\n--- 2. Cold Start (ndoc all) ---")
    res, time_cold = run_command(["all"], cwd=root)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}")
        return
    print(f"Cold Start Time: {time_cold:.2f}s")
    
    # Verify artifacts
    for f in artifacts:
        if not (root / f).exists():
            print(f"ERROR: Artifact {f} missing!")
        else:
            print(f"Verified {f} exists.")

    # 3. Hot Start
    print("\n--- 3. Hot Start (ndoc all) ---")
    res, time_hot = run_command(["all"], cwd=root)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}")
        return
    print(f"Hot Start Time: {time_hot:.2f}s")
    
    # 4. Incremental Update
    print("\n--- 4. Incremental Update (ndoc all) ---")
    # Modify a file
    test_file = root / "temp_benchmark.py"
    test_file.write_text("# @NOTE Benchmark test file\nclass Benchmark:\n    pass")
    
    res, time_inc = run_command(["all"], cwd=root)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}")
        return
    print(f"Incremental Time: {time_inc:.2f}s")
    
    # Cleanup test file
    test_file.unlink()
    
    # 5. LSP Query
    print("\n--- 5. LSP Query (ndoc lsp) ---")
    # Search for a known symbol, e.g. "Scanner" or "ScanResult"
    res, time_lsp = run_command(["lsp", "ScanResult"], cwd=root)
    if res.returncode != 0:
        print(f"FAILED: {res.stderr}")
    else:
        print(f"LSP Query Time: {time_lsp:.2f}s")
        if "Definitions" in res.stdout:
            print("LSP Output Verified.")
        else:
            print("LSP Output suspicious (no Definitions found).")
            
    # 6. Report
    print("\n=== Benchmark Report ===")
    print(f"Cold Start:       {time_cold:.2f}s")
    print(f"Hot Start:        {time_hot:.2f}s")
    print(f"Incremental:      {time_inc:.2f}s")
    print(f"LSP Query:        {time_lsp:.2f}s")
    
    # Verify Hot Start is significantly faster
    if time_hot < time_cold * 0.5:
        print("✅ Cache is working effectively (Hot < 50% Cold)")
    else:
        print("⚠️ Cache might not be optimal")

if __name__ == "__main__":
    main()
