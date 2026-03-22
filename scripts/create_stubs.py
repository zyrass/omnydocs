import os
from pathlib import Path

docs_dir = Path(r"g:\Omnyvia\omnydocs\docs")

missing_files = [
    "bases/outils/terminaux-shell.md",
    "bases/outils/vscode/config.md",
    "bases/outils/vscode/liste-extensions.md",
    "bases/outils/vscode/snippet.md",
    "sys-reseau/linux/security/linux_malware_detect.md",
    "dev-cloud/frameworks/laravel/breeze.md",
    "dev-cloud/frameworks/laravel/jetstream.md",
    "dev-cloud/frameworks/laravel/sanctum.md",
    "bases/devsecops/gestion-projet/index.md",
    "bases/devsecops/gestion-projet/gantt.md",
    "cyber/tools/osint/subfinder.md",
    "cyber/tools/osint/assetfinder.md",
    "cyber/tools/osint/httpx.md",
    "cyber/tools/web/feroxbuster.md",
    "cyber/tools/web/nuclei.md",
    "cyber/tools/web/sqlmap.md",
    "cyber/tools/network/rustscan.md",
    "cyber/tools/network/dns/dnsenum.md",
    "cyber/tools/network/bettercap.md",
    "cyber/tools/crack/crunch.md",
    "cyber/tools/crack/seclists.md",
    "cyber/tools/methodology/opsec.md",
    "cyber/tools/reporting/index.md",
    "cyber/tools/reporting/rapport-structure.md",
    "cyber/tools/reporting/preuves.md",
    "cyber/tools/reporting/cvss.md",
    "cyber/tools/reporting/remediation.md",
    "dev-cloud/lang/laravel/projects/project-breeze/index.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase1.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase2.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase3.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase4.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase5.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase6.md",
    "dev-cloud/lang/laravel/projects/project-breeze/phase7.md",
    "dev-cloud/lang/laravel/projects/project-breeze/conclusion.md",
    "dev-cloud/lang/laravel/projects/project-jetstream/index.md",
    "dev-cloud/lang/laravel/projects/project-sanctum/index.md",
]

stub_template = """---
description: "Document en cours de rédaction"
icon: lucide/file-text
---

# {title}

<div
  class="omny-meta"
  data-level="🟢 En construction"
  data-version="1.0"
  data-time="Bientôt disponible">
</div>

!!! info "Article en cours de rédaction"
    Le contenu détaillé de cette page est actuellement en cours de rédaction. Il sera publié lors des prochaines mises à jour d'OmnyDocs.

<br />
"""

for file_path in missing_files:
    full_path = docs_dir / file_path
    
    # Création des dossiers parents s'ils n'existent pas
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Création du fichier avec injection du titre
    if not full_path.exists():
        name = full_path.stem
        # Si c'est un fichier d'index, on utilise le nom du dossier parent comme titre
        if name == "index":
            title = full_path.parent.name.replace("-", " ").title()
        else:
            title = name.replace("-", " ").replace("_", " ").title()
            
        content = stub_template.format(title=title)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created stub for: {file_path}")

print("All stubs created successfully!")
