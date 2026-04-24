---
description: "Python — Hub de navigation : présentation du langage, parcours de formation et frameworks disponibles (Django, Flask, Tkinter)."
tags: ["PYTHON", "DJANGO", "FLASK", "TKINTER", "HUB"]
---

# Python

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-version="Python 3.12+"
  data-time="Hub">
</div>

## Présentation

!!! quote "Analogie pédagogique — Le Couteau Suisse"
    Python est le couteau suisse du développeur : scripts d'automatisation, développement web (Django, Flask), interfaces graphiques (Tkinter), data science, intelligence artificielle. Un seul langage, des dizaines de domaines. Sa syntaxe lisible et sa bibliothèque standard exhaustive en font le premier langage recommandé pour apprendre la programmation.

**Python** est un langage interprété, à typage dynamique, multi-paradigme (procédural, orienté objet, fonctionnel). Créé par Guido van Rossum en 1991, il est aujourd'hui le langage le plus utilisé au monde.

| Caractéristique | Valeur |
|---|---|
| **Créé par** | Guido van Rossum (1991) |
| **Paradigmes** | Procédural, OOP, Fonctionnel |
| **Typage** | Dynamique, fort |
| **Interpréteur** | CPython (référence), PyPy, Jython |
| **Gestionnaire de paquets** | `pip` / `uv` |

<br>

---

## Parcours de Formation

!!! quote "**Notre recommandation**"

    1. Maîtriser les fondamentaux Python (variables, fonctions, OOP, erreurs)

    2. Choisir un framework selon votre objectif :

        - Web backend → Django (complet) ou Flask (micro)
        - Interfaces graphiques → Tkinter
        - Data / IA → NumPy, Pandas, PyTorch (hors périmètre)

<br>

---

## Modules Disponibles

| Section | Contenu | Niveau |
|---|---|---|
| [Rapport de formation](./00-rapport-formation-python.md) | Bilan, couverture, recommandations | 📋 |
| [**Django**](./django/index.md) | MVT, ORM, Admin, auth, REST | 🟡 Intermédiaire |
| [**Flask**](./flask/index.md) | App Factory, Blueprints, SQLAlchemy | 🟡 Intermédiaire |
| [**Tkinter**](./tkinter/index.md) | Widgets, layouts, événements, Canvas | 🟢 Débutant |

<br>

---

## Prérequis

- Bases de programmation (variables, boucles, fonctions)
- Python installé (`python --version` ≥ 3.10)
- Éditeur : VS Code + extension Pylance recommandé

<br>

---

## Installation Rapide

```bash title="Bash — Installer Python et créer un environnement virtuel"
# Vérifier la version installée
python --version   # ou python3 --version

# Créer un environnement virtuel (isoler les dépendances)
python -m venv .venv

# Activer l'environnement
# macOS/Linux :
source .venv/bin/activate
# Windows :
.venv\Scripts\activate

# Installer des dépendances
pip install django flask

# Générer le fichier de dépendances
pip freeze > requirements.txt

# Réinstaller depuis requirements.txt
pip install -r requirements.txt
```

!!! tip "Utilisez `uv` pour la rapidité"
    `uv` (à la place de `pip`) est 50× plus rapide et résout les conflits de dépendances automatiquement.
    ```bash
    pip install uv
    uv pip install django
    ```

<br>