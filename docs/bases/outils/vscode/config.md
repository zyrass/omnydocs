---
description: "Visual Studio Code — Configuration professionnelle de l'éditeur de référence. Paramétrage, workspace settings, formatage automatique et bonnes pratiques par langage."
icon: lucide/book-open-check
tags: ["VSCODE", "ÉDITEUR", "CONFIGURATION", "PRODUCTIVITÉ", "SETTINGS"]
---

# VS Code — Configuration Professionnelle

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2024.x"
  data-time="~15 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Bureau du Développeur"
    Un développeur qui utilise VS Code avec les paramètres par défaut, c'est comme un chirurgien qui opère avec les outils rangés dans le désordre. Les instruments sont là, mais chaque seconde perdue à chercher coûte cher.

    La configuration de VS Code est votre **rituel d'installation du bureau de travail** : vous ne le faites qu'une fois, mais vous en bénéficiez chaque jour. Les 20 minutes investies ici se transforment en heures récupérées sur l'année.

VS Code stocke sa configuration dans un fichier JSON (`settings.json`). Celui-ci peut exister à deux niveaux : **Global** (User Settings, s'applique à tous les projets) et **Workspace** (`.vscode/settings.json`, prioritaire sur le global pour le projet en cours).

<br>

---

## Accéder aux Paramètres

```
Raccourci : Ctrl + , (virgule)
→ Mode UI  : Cliquer "Open Settings (UI)"
→ Mode JSON : Cliquer l'icône {} en haut à droite
```

Pour éditer le JSON directement :
```
Ctrl + Shift + P → "Open User Settings (JSON)"
```

<br>

---

## `settings.json` — Configuration Recommandée

```json title="settings.json — Configuration PHP/Laravel/Python"
{
    // ── Éditeur ────────────────────────────────────────────────
    "editor.fontSize": 14,
    "editor.tabSize": 4,
    "editor.insertSpaces": true,       // Espaces au lieu de tabulations
    "editor.wordWrap": "on",           // Retour à la ligne automatique
    "editor.formatOnSave": true,       // Formater à chaque sauvegarde
    "editor.formatOnPaste": true,
    "editor.minimap.enabled": false,   // Désactiver la minimap (gain d'espace)
    "editor.renderWhitespace": "boundary",
    "editor.rulers": [80, 120],        // Règles verticales à 80 et 120 caractères
    "editor.bracketPairColorization.enabled": true,
    "editor.inlineSuggest.enabled": true,

    // ── Fichiers ───────────────────────────────────────────────
    "files.trimTrailingWhitespace": true,  // Supprimer les espaces en fin de ligne
    "files.insertFinalNewline": true,      // Toujours finir par une ligne vide
    "files.encoding": "utf8",
    "files.autoSave": "onFocusChange",     // Sauvegarde automatique

    // ── Terminal intégré ───────────────────────────────────────
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.defaultProfile.windows": "Git Bash",

    // ── Git ────────────────────────────────────────────────────
    "git.autofetch": true,
    "git.confirmSync": false,

    // ── PHP / Laravel ──────────────────────────────────────────
    "[php]": {
        "editor.tabSize": 4,
        "editor.defaultFormatter": "bmewburn.vscode-intelephense-client"
    },

    // ── Python ────────────────────────────────────────────────
    "[python]": {
        "editor.tabSize": 4,
        "editor.defaultFormatter": "ms-python.black-formatter"
    },

    // ── JavaScript / TypeScript ────────────────────────────────
    "[javascript]": {
        "editor.tabSize": 2,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
        "editor.tabSize": 2,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },

    // ── Markdown ───────────────────────────────────────────────
    "[markdown]": {
        "editor.wordWrap": "on",
        "editor.quickSuggestions": { "other": false }
    },

    // ── Explorateur ────────────────────────────────────────────
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false,
    "workbench.startupEditor": "none"
}
```

<br>

---

## `.vscode/settings.json` — Config par Projet

Pour overrider les settings globaux **uniquement pour un projet**, créez un fichier `.vscode/settings.json` à la racine du projet et commitez-le dans Git.

```json title=".vscode/settings.json — Projet Laravel"
{
    // Format PHP uniquement avec PSR-12 pour ce projet
    "[php]": {
        "editor.defaultFormatter": "bmewburn.vscode-intelephense-client"
    },
    // Exclure les dossiers lourds de l'explorateur et de la recherche
    "files.exclude": {
        "vendor/": true,
        "node_modules/": true,
        ".git/": true,
        "storage/logs/": true
    },
    "search.exclude": {
        "vendor/": true,
        "node_modules/": true,
        "*.lock": true
    }
}
```

!!! tip "Bonne pratique équipe"
    Commitez `.vscode/settings.json` dans votre repository. Tous les développeurs de l'équipe auront automatiquement la même configuration d'éditeur sans avoir à la configurer manuellement.

<br>

---

## Raccourcis Clavier Indispensables

| Raccourci | Action |
|---|---|
| `Ctrl + P` | Ouvrir un fichier rapidement (fuzzy search) |
| `Ctrl + Shift + P` | Palette de commandes |
| `Ctrl + \`` | Ouvrir/fermer le terminal |
| `Ctrl + B` | Afficher/masquer la barre latérale |
| `Alt + Clic` | Multi-curseurs |
| `Ctrl + D` | Sélectionner la prochaine occurrence |
| `Ctrl + Shift + L` | Sélectionner toutes les occurrences |
| `F2` | Renommer un symbole dans tout le projet |
| `Ctrl + K, Ctrl + 0` | Replier tout le code |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La configuration de VS Code est un investissement ponctuel à fort retour. Le `formatOnSave`, le `trimTrailingWhitespace` et les règles de formatage par langage éliminent silencieusement des dizaines de micro-décisions par jour. Le `.vscode/settings.json` commité dans Git garantit que toute l'équipe travaille avec les mêmes standards — la cohérence du code commence par la cohérence de l'environnement.

> [Extensions VS Code recommandées →](./liste-extensions.md)
