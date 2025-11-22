#!/usr/bin/env python3
from pathlib import Path
import shutil
import argparse

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

# -------------------------------------------------------------------
# AJUSTEMENT : racine du projet
# Le script est placé dans scripts/, on remonte donc d'un niveau
# pour cibler la racine du repo : .../omnydocs
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUT_FILE = PROJECT_ROOT / "zensical.toml"


# -------------------------------------------------------------------
# Nettoyage des artefacts de build à la racine du projet
# (.cache/, site/, zensical.md)
# -------------------------------------------------------------------
def cleanup() -> None:
    """
    Supprime les artefacts de build (.cache/, site/, zensical.md)
    à partir de PROJECT_ROOT. Ne lève pas d'exception bloquante.
    """
    targets = [
        PROJECT_ROOT / ".cache",
        PROJECT_ROOT / "site",
        PROJECT_ROOT / "zensical.md",
    ]

    print(f"[INFO] Nettoyage dans : {PROJECT_ROOT}")

    for target in targets:
        try:
            if target.is_dir():
                shutil.rmtree(target)
                print(f"[CLEAN] Dossier supprimé : {target}")
            elif target.is_file():
                target.unlink()
                print(f"[CLEAN] Fichier supprimé : {target}")
            else:
                print(f"[SKIP] Rien à supprimer : {target}")
        except Exception as e:
            # Le nettoyage ne doit jamais interrompre la construction.
            print(f"[WARN] Impossible de supprimer {target} : {e}")


# -------------------------------------------------------------------
# Parser d’arguments pour contrôler le comportement :
# --clean-only : effectue uniquement le nettoyage
# --no-clean   : saute totalement le nettoyage
# -------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assembleur TOML + nettoyage des artefacts."
    )

    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Exécute uniquement le nettoyage puis s’arrête."
    )

    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Désactive entièrement le nettoyage automatique."
    )

    return parser.parse_args()


# -------------------------------------------------------------------
# Fonction principale : nettoyage (optionnel) + assemblage TOML
# -------------------------------------------------------------------
def main() -> None:
    args = parse_args()

    # Gestion des modes de nettoyage
    if args.clean_only:
        cleanup()
        print("[INFO] Nettoyage effectué. Aucun fichier TOML généré (mode --clean-only).")
        return

    if not args.no_clean:
        cleanup()

    # Assemblage des fragments TOML à partir de la racine projet
    pieces: list[str] = []

    for rel in PARTS:
        p = PROJECT_ROOT / rel
        if not p.is_file():
            raise SystemExit(f"Fichier introuvable : {p}")
        text = p.read_text(encoding="utf-8")
        pieces.append(text.rstrip() + "\n\n")

    OUT_FILE.write_text("".join(pieces), encoding="utf-8")
    print(f"[OK] Fichier {OUT_FILE} généré à partir des fragments TOML.")


if __name__ == "__main__":
    main()
