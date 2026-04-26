---
description: "Les Snippets VS Code — Créez vos propres templates de code pour automatiser les patterns répétitifs et accélérer votre productivité quotidienne."
icon: lucide/book-open-check
tags: ["VSCODE", "SNIPPETS", "PRODUCTIVITÉ", "TEMPLATES", "AUTOMATISATION"]
---

# Snippets VS Code — Vos Raccourcis Personnels

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2024.x"
  data-time="~15 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Tampon Encreurs du Développeur"
    Un clerc d'huissier des années 50 utilisait des tampons encreurs pour reproduire instantanément les formules juridiques standard sans les retaper à chaque fois. **Les Snippets VS Code** sont vos tampons encreurs numériques : vous tapez un préfixe court (`php-class`, `laravel-route`), appuyez sur `Tab`, et la structure complète apparaît avec le curseur positionné au bon endroit pour saisir votre logique.

Les Snippets VS Code sont des **templates de code associés à un préfixe court**. Ils supportent les **tabstops** (`$1`, `$2`) pour naviguer entre les zones à remplir, les **placeholders** (`${1:nomDeClasse}`) pour afficher une valeur par défaut, et les **variables** (`$TM_FILENAME_BASE`) pour injecter des informations contextuelles.

<br>

---

## Accéder à l'Éditeur de Snippets

```
Ctrl + Shift + P → "Configure User Snippets"
→ Choisir le langage : "php", "javascript", "python", etc.
→ Ou "New Global Snippets File" pour des snippets multi-langages
```

<br>

---

## Snippets PHP / Laravel

```json title="php.json — Snippets PHP/Laravel"
{
    // ── Classe PHP Standard ────────────────────────────────────
    "PHP Class": {
        "prefix": "php-class",
        "description": "Classe PHP avec namespace",
        "body": [
            "<?php",
            "",
            "declare(strict_types=1);",
            "",
            "namespace ${1:App\\\\Domain};",
            "",
            "class ${2:NomDeLaClasse}",
            "{",
            "    public function __construct(",
            "        $0",
            "    ) {}",
            "}"
        ]
    },

    // ── Controller Laravel Resource ────────────────────────────
    "Laravel Controller": {
        "prefix": "laravel-controller",
        "description": "Controller Resource Laravel",
        "body": [
            "<?php",
            "",
            "namespace App\\Http\\Controllers;",
            "",
            "use App\\Models\\${1:Model};",
            "use Illuminate\\Http\\Request;",
            "",
            "class ${1}Controller extends Controller",
            "{",
            "    public function index()",
            "    {",
            "        return view('${2:view}.index', [",
            "            '${3:items}' => ${1}::latest()->paginate(20),",
            "        ]);",
            "    }",
            "",
            "    public function store(Request \\$request)",
            "    {",
            "        \\$validated = \\$request->validate([",
            "            $0",
            "        ]);",
            "",
            "        ${1}::create(\\$validated);",
            "",
            "        return redirect()->route('${2}.index')",
            "            ->with('success', '${1} créé avec succès.');",
            "    }",
            "}"
        ]
    },

    // ── Route Laravel ──────────────────────────────────────────
    "Laravel Route Resource": {
        "prefix": "laravel-route",
        "description": "Route Resource Laravel",
        "body": [
            "Route::resource('${1:resource}', ${2:Controller}::class);"
        ]
    },

    // ── dd() de debug ──────────────────────────────────────────
    "Laravel DD": {
        "prefix": "dd",
        "description": "Dump and Die Laravel",
        "body": ["dd(${1:\\$variable});"]
    }
}
```

<br>

---

## Snippets JavaScript

```json title="javascript.json — Snippets JS/TS"
{
    // ── Fetch API ──────────────────────────────────────────────
    "Fetch API": {
        "prefix": "js-fetch",
        "description": "Appel API avec fetch + async/await",
        "body": [
            "const response = await fetch('${1:/api/endpoint}', {",
            "    method: '${2:GET}',",
            "    headers: {",
            "        'Content-Type': 'application/json',",
            "        'Authorization': `Bearer ${3:\\${token\\}}`",
            "    },",
            "    ${4:body: JSON.stringify(data),}",
            "});",
            "",
            "if (!response.ok) {",
            "    throw new Error(`HTTP error! status: ${3:\\${response.status\\}}`);",
            "}",
            "",
            "const data = await response.json();",
            "$0"
        ]
    },

    // ── Console.log avec label ─────────────────────────────────
    "Console Log": {
        "prefix": "cl",
        "description": "console.log avec label",
        "body": ["console.log('${1:label}:', ${2:value});"]
    }
}
```

<br>

---

## Les Variables de Contexte

VS Code injecte automatiquement ces variables dans vos snippets :

| Variable | Valeur injectée |
|---|---|
| `$TM_FILENAME` | Nom du fichier courant (`UserController.php`) |
| `$TM_FILENAME_BASE` | Nom sans extension (`UserController`) |
| `$TM_DIRECTORY` | Chemin du dossier du fichier |
| `$CURRENT_DATE` | Date du jour (`25`) |
| `$CURRENT_YEAR` | Année courante (`2026`) |
| `$CLIPBOARD` | Contenu du presse-papiers |

```json title="Exemple : Header de fichier avec date automatique"
"File Header PHP": {
    "prefix": "php-header",
    "body": [
        "<?php",
        "/**",
        " * ${TM_FILENAME_BASE}",
        " *",
        " * @created ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}",
        " * @author  ${1:Auteur}",
        " */"
    ]
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les Snippets sont le dernier niveau d'automatisation de l'éditeur : là où les extensions automatisent le formatage et la détection d'erreurs, les Snippets automatisent **votre façon personnelle d'écrire**. Commencez par identifier les 5 structures que vous tapez le plus souvent dans votre langage principal, créez-les en Snippets, et mesurez le temps gagné sur une semaine. La résultat est invariablement supérieur aux attentes.

> [Retour à l'index des outils VS Code →](./)
