#!/usr/bin/env python3
from pathlib import Path

PARTS = [
    "config/toml/00-project-core.toml",
    "config/toml/navigation/00-nav-accueil.toml",
    "config/toml/navigation/01-nav-bases-fondamentaux.toml",
    "config/toml/navigation/02-nav-sys-reseau.toml",
    "config/toml/navigation/03-nav-dev-cloud.toml",
    "config/toml/navigation/04-nav-devsecops.toml",
    "config/toml/navigation/05-nav-cyber-governance.toml",
    "config/toml/navigation/06-nav-cyber-operations.toml",
    "config/toml/navigation/07-nav-cyber-tools.toml",
    "config/toml/navigation/08-nav-glossaire.toml",
    "config/toml/10-project-theme-and-markdown.toml",
]

OUT_FILE = Path("zensical.toml")


def main() -> None:
    pieces: list[str] = []

    for rel in PARTS:
        p = Path(rel)
        if not p.is_file():
            raise SystemExit(f"Fichier introuvable : {p}")
        text = p.read_text(encoding="utf-8")
        # on normalise et on sépare les blocs par deux sauts de ligne
        pieces.append(text.rstrip() + "\n\n")

    OUT_FILE.write_text("".join(pieces), encoding="utf-8")
    print(f"[OK] Fichier {OUT_FILE} généré à partir des fragments TOML.")


if __name__ == "__main__":
    main()
