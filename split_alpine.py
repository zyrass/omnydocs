import os

filepath = "g:/Omnyvia/omnydocs/docs/dev-cloud/frameworks/alpine/alpinejs-fondamentaux.md"
out_dir = "g:/Omnyvia/omnydocs/docs/projets/alpine-lab/"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

out_files = {
    1: "03-pentest-tool-p1.md",
    2: "04-pentest-tool-p2.md",
    3: "05-pentest-tool-p3.md",
    4: "06-pentest-tool-p4.md"
}

file_contents = {i: [] for i in range(1, 5)}
current_idx = 1

for line in lines:
    if line.startswith("## Phase 2"):
        current_idx = 2
    elif line.startswith("## Phase 4"):
        current_idx = 3
    elif line.startswith("## Phase 6"):
        current_idx = 4
        
    file_contents[current_idx].append(line)

frontmatters = {
    2: "---\ndescription: \"Projet 3 - Phase 2 : CRUD, Formulaires et Filtres avec Alpine.js\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"CRUD\"]\n---\n\n",
    3: "---\ndescription: \"Projet 3 - Phase 3 : Calculateurs complexes (CVSS) et Persistance LocalStorage\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"CVSS\", \"PERSISTENCE\"]\n---\n\n",
    4: "---\ndescription: \"Projet 3 - Phase 4 : Export Multi-Format (PDF, Markdown), UX et Librairie\"\nicon: lucide/mountain\ntags: [\"PROJET\", \"ALPINE\", \"EXPORT\", \"UX\"]\n---\n\n"
}

for i in range(2, 5):
    if len(file_contents[i]) > 0 and file_contents[i][0].startswith("## Phase"):
        file_contents[i][0] = file_contents[i][0].replace("## Phase", "# Phase", 1)

for i in range(1, 5):
    path = os.path.join(out_dir, out_files[i])
    with open(path, "w", encoding="utf-8") as f:
        if i == 1:
            f.writelines(file_contents[i])
        else:
            f.write(frontmatters[i])
            f.writelines(file_contents[i])

print("Split completed successfully!")
