from pathlib import Path

def add_marker():
    root = Path("src/ndoc")
    count = 0
    for path in root.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
            if "# <AI Context>" not in content:
                # Check for shebang
                lines = content.splitlines()
                if lines and lines[0].startswith("#!"):
                    # Insert after shebang
                    lines.insert(1, "# <AI Context>")
                    new_content = "\n".join(lines) + "\n"
                else:
                    new_content = "# <AI Context>\n" + content
                
                path.write_text(new_content, encoding="utf-8")
                count += 1
                print(f"Updated: {path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")
    
    print(f"Total updated: {count}")

if __name__ == "__main__":
    add_marker()