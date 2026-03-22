import os
import re
from pathlib import Path

def main():
    docs_dir = Path(r"g:\Omnyvia\omnydocs\docs")
    config_dir = Path(r"g:\Omnyvia\omnydocs\config\toml\navigation")
    
    path_regex = re.compile(r'"([^"]+\.md)"')
    missing_files = []
    
    for toml_file in config_dir.glob("*.toml"):
        with open(toml_file, "r", encoding="utf-8") as f:
            content = f.read()
            matches = path_regex.findall(content)
            for file_path in matches:
                full_path = docs_dir / file_path
                if not full_path.exists():
                    missing_files.append((toml_file.name, file_path))
                    
    if missing_files:
        print("MISSING FILES FOUND:")
        for toml, file in missing_files:
            print(f"- {file} (in {toml})")
    else:
        print("ALL LINKS OK.")

if __name__ == "__main__":
    main()
