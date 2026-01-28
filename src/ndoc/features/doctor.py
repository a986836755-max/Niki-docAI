import shutil
from ndoc.core import console, config

def check_tool(name):
    path = shutil.which(name)
    if path:
        console.success(f"Found {name}: {path}")
    else:
        console.error(f"Missing {name}")

def cmd_doctor(root=None):
    console.header("Niki Toolchain Doctor")
    
    console.step("Checking Dependencies...")
    check_tool("cmake")
    check_tool("flatc")
    check_tool("git")
    check_tool("python")
    check_tool("doxygen")
    
    console.step("Checking Configuration...")
    console.info(f"XML Output Dir: {config.XML_OUTPUT_DIR}")
    console.info(f"Doxyfile: {config.DOXYFILE_PATH}")
    
    console.success("Doctor check complete.")
