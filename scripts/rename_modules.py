import os
import re
from pathlib import Path
import shutil

def slugify(text):
    text = text.lower()
    # Replace non-alphanumeric with dashes
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    base_dir = Path(r"g:\Omnyvia\omnydocs\docs\dev-cloud\lang\html-css")
    directories = ["html-fondamental", "css-fondamental", "layout-modern", "responsive"]
    toml_path = Path(r"g:\Omnyvia\omnydocs\config\toml\navigation\03-nav-dev-cloud.toml")
    
    mapping = {} # Old relative path -> New relative path
    
    for folder in directories:
        folder_path = base_dir / folder
        if not folder_path.exists():
            continue
            
        # Get all moduleX.md files and sort them by the number X
        module_files = []
        for f in folder_path.glob("module*.md"):
            match = re.search(r'module(\d+)\.md', f.name)
            if match:
                module_files.append((int(match.group(1)), f))
        
        module_files.sort(key=lambda x: x[0])
        
        counter = 1
        for num, file_path in module_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Find the H1 title
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                title = match.group(1)
                # Remove roman numerals like "I - ", "VII - "
                title = re.sub(r'^[IVX]+\s*-\s*', '', title)
                slug = slugify(title)
                new_filename = f"{counter:02d}-{slug}.md"
                
                old_rel = f"dev-cloud/lang/html-css/{folder}/{file_path.name}"
                new_rel = f"dev-cloud/lang/html-css/{folder}/{new_filename}"
                
                mapping[old_rel] = new_rel
                
                # Create the copy file first if it doesn't already exist
                # Actually user wants to keep the ORIGINAL as a "*copy*.md" and use the new one as the working one
                # OR user wants a `copy` file they can easily delete later
                copy_filename = f"{new_filename.replace('.md', '')} copy.md"
                # Let's just create copy of the old file but named with copy
                copy_path = file_path.parent / copy_filename
                if not copy_path.exists():
                    shutil.copy2(file_path, copy_path)
                    
                # Rename original to new
                new_path = file_path.parent / new_filename
                file_path.rename(new_path)
                
                print(f"Renamed {file_path.name} -> {new_filename} and created {copy_filename}.")
                counter += 1

    # Update the TOML
    if toml_path.exists():
        with open(toml_path, "r", encoding="utf-8") as f:
            toml_content = f.read()
            
        for old_rel, new_rel in mapping.items():
            toml_content = toml_content.replace(f'"{old_rel}"', f'"{new_rel}"')
            
        with open(toml_path, "w", encoding="utf-8") as f:
            f.write(toml_content)
            
        print("Updated TOML file.")
        
    # Also handle the monolithic file
    mono_file = base_dir / "html-css.md"
    if mono_file.exists():
        mono_copy = base_dir / "html-css copy.md"
        if not mono_copy.exists():
            mono_file.rename(mono_copy)
            print("Renamed monolithic html-css.md to html-css copy.md.")
            # Let's remove it from any TOML if it's there? It wasn't in TOML initially.

if __name__ == "__main__":
    main()
