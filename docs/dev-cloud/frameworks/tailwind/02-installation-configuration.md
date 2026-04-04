---
description: "Tailwind CSS — Installation et configuration : intégration Vite + Laravel, tailwind.config.js, purge CSS, IntelliSense VS Code et premier build."
icon: lucide/book-open-check
tags: ["TAILWIND", "INSTALLATION", "VITE", "LARAVEL", "CONFIGURATION"]
---

# Installation & Configuration

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="3.x"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Atelier du Menuisier"
    Avant de construire quoi que ce soit, le menuisier installe son atelier : plan de travail, outils rangés par taille, machine configurée pour le bon matériau. Mal configuré, chaque coupe est imprécise. Bien configuré, le travail suit sans friction. La configuration Tailwind, c'est cet atelier : `tailwind.config.js` définit les matériaux disponibles (couleurs, espacements, typographie), le plugin Vite automatise la compilation, IntelliSense VS Code vous guide en temps réel.

Ce module couvre l'installation complète de Tailwind CSS dans un projet **Laravel + Vite** — l'environnement standard de la Stack TALL.

<br>

---

## Installation dans un Projet Laravel

### Prérequis

```bash title="Terminal — Vérifier les prérequis"
# Node.js 18+ requis
node --version
# → v20.x.x

# npm 9+ (ou pnpm, bun)
npm --version
# → 10.x.x

# Laravel avec Vite (Laravel 10+ par défaut)
php artisan --version
# → Laravel Framework 11.x.x
```

### Installation de Tailwind

```bash title="Terminal — Installer Tailwind CSS dans Laravel"
# Depuis la racine du projet Laravel
npm install -D tailwindcss postcss autoprefixer

# Générer tailwind.config.js et postcss.config.js
npx tailwindcss init -p
```

*`-D` installe en devDependency — Tailwind n'est pas embarqué dans le bundle final, uniquement le CSS généré. `-p` crée également `postcss.config.js` requis par Vite.*

<br>

---

## Configuration — `tailwind.config.js`

### Fichier généré par défaut

```js title="JavaScript — tailwind.config.js : configuration de base générée"
/** @type {import('tailwindcss').Config} */
module.exports = {
  // content : les fichiers à scanner pour trouver les classes Tailwind
  // Sans cette option, Tailwind génère TOUT le CSS (~3 Mo)
  // Avec cette option, il génère uniquement les classes utilisées (~5-20 Ko)
  content: [],

  theme: {
    extend: {
      // Vos personnalisations ici (ne remplace pas, étend le thème)
    },
  },

  plugins: [],
}
```

### Configuration pour Laravel

```js title="JavaScript — tailwind.config.js : configuration pour Laravel + Blade + Alpine"
/** @type {import('tailwindcss').Config} */
module.exports = {
  // Tailwind scanne ces fichiers à la recherche des classes utilisées
  content: [
    // Vues Blade : toutes les templates Laravel
    './resources/views/**/*.blade.php',

    // Fichiers JavaScript : classes utilisées via Alpine.js (:class, x-bind)
    './resources/js/**/*.js',
    './resources/js/**/*.vue',      // Si vous utilisez Vue

    // Composants Livewire : classes dans les vues des composants
    './app/Livewire/**/*.php',      // Livewire dynamique (PHP)
    './app/Http/Livewire/**/*.php', // Livewire v2 (ancienne structure)
  ],

  // darkMode : 'media' (préférence système) ou 'class' (contrôlé manuellement)
  darkMode: 'class',

  theme: {
    extend: {
      // Exemple : ajouter une couleur custom
      colors: {
        'brand': {
          50:  '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a5f',
        },
      },

      // Exemple : ajouter une taille de police custom
      fontSize: {
        'xxs': '0.65rem',
      },
    },
  },

  plugins: [
    // Plugins officiels Tailwind (voir module 8)
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
  ],
}
```

*La section `content` est **critique** — c'est le "purging". Si vous oubliez un chemin, les classes utilisées dans ces fichiers seront absentes du CSS final en production.*

<br>

---

## Intégration dans le CSS

### Fichier `resources/css/app.css`

```css title="CSS — resources/css/app.css : directives Tailwind obligatoires"
/* Directive base : reset CSS + styles base (html, body, titres...) */
@tailwind base;

/* Directive components : classes générées par les plugins (@layer components) */
@tailwind components;

/* Directive utilities : toutes les classes utilitaires Tailwind */
@tailwind utilities;

/* Vos styles personnalisés viennent ICI, après les directives */
/* Ils peuvent utiliser @apply pour composer des classes Tailwind */
```

*Ces trois directives sont le point d'entrée de Tailwind. Ne changez pas leur ordre — `base` doit précéder `utilities` pour que la cascade CSS fonctionne correctement.*

<br>

---

## Configuration Vite

### `vite.config.js`

```js title="JavaScript — vite.config.js : plugin Laravel avec Tailwind"
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // Point d'entrée : votre CSS incluant les directives Tailwind
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            // Hot Module Replacement : rechargement auto en développement
            refresh: true,
        }),
    ],
});
```

### Inclusion dans le Layout Blade

```html title="Blade — layouts/app.blade.php : inclure les assets compilés"
<!DOCTYPE html>
<html lang="fr" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? 'OmnyApp' }}</title>

    {{-- @vite inclut le CSS compilé par Tailwind + le JS --}}
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="h-full bg-gray-50 text-gray-900">
    {{ $slot }}
</body>
</html>
```

*`@vite()` est la directive Laravel qui injecte les assets avec les bons chemins — en dev avec HMR, en prod avec les chemins hashés du build.*

<br>

---

## Workflow de Développement

```bash title="Terminal — Commandes de développement et production"
# ─── Développement ────────────────────────────────────────────
# Lance Vite avec HMR : Tailwind regénère le CSS à chaque sauvegarde
npm run dev
# → VITE v5.x.x  ready in 300ms
# → ➜  Local:   http://localhost:5173/

# ─── Production ───────────────────────────────────────────────
# Build optimisé : Tailwind purge, minifie (~5-20 Ko)
npm run build
# → vite v5.x.x building for production...
# → dist/assets/app-Bw9lBwJV.css (12.34 kB gzipped: 3.21 kB)

# ─── Vérification du CSS généré ───────────────────────────────
# Voir les classes incluses dans le build
npm run build && cat public/build/assets/app-*.css | wc -c
```

<br>

---

## IntelliSense VS Code

L'extension **Tailwind CSS IntelliSense** est indispensable. Elle active :

```json title="JSON — .vscode/settings.json : configuration de l'extension"
{
    // Autocomplétion Tailwind dans les fichiers Blade
    "tailwindCSS.includeLanguages": {
        "blade": "html",
        "html": "html"
    },

    // Activer le folding des longues listes de classes
    "editor.quickSuggestions": {
        "strings": true
    },

    // Afficher les valeurs CSS réelles au survol d'une classe
    "tailwindCSS.experimental.classRegex": [
        ["class=[\"']([^\"']*)[\"']", "[\"']([^\"']*)[\"']"]
    ]
}
```

*Avec IntelliSense, tapez `bg-` et VS Code vous liste toutes les couleurs disponibles avec leur prévisualisation. Tapez `p-` pour voir toutes les valeurs d'espacement. La mémorisation devient secondaire.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Installation complète**

```bash title="Terminal — Exercice 1 : créer un projet Laravel avec Tailwind"
# 1. Créer un nouveau projet Laravel
composer create-project laravel/laravel tailwind-lab

# 2. Installer Tailwind
cd tailwind-lab
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 3. Configurer tailwind.config.js avec le bon chemin content
# (voir ci-dessus)

# 4. Ajouter les directives dans resources/css/app.css

# 5. Lancer le serveur de développement
php artisan serve &
npm run dev

# 6. Vérifier : ouvrir http://localhost:8000
# Le CSS Tailwind doit être chargé dans les DevTools
```

**Exercice 2 — Vérifier le purging**

```bash title="Terminal — Exercice 2 : mesurer l'impact du purging"
# 1. Ajouter quelques classes dans une vue Blade (bg-blue-500, text-xl, p-4)
# 2. Lancer npm run build
# 3. Mesurer la taille du CSS généré
cat public/build/assets/app-*.css | wc -c

# Les classes non utilisées ne doivent pas apparaître dans le CSS final
# grep "bg-red-900" public/build/assets/app-*.css → doit retourner vide
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    L'installation Tailwind dans Laravel se fait en 4 étapes : `npm install`, `npx tailwindcss init -p`, configuration de `content` dans `tailwind.config.js`, et ajout des directives `@tailwind` dans `app.css`. La section **`content`** est critique — elle contrôle le purging. Sans elle, le CSS fait 3 Mo ; avec elle, 5-20 Ko. Vite intègre nativement Tailwind via PostCSS — `npm run dev` lance le HMR, `npm run build` produit le bundle optimisé. Installez l'extension IntelliSense VS Code dès maintenant : elle multiplie votre vitesse de développement.

> Dans le module suivant, nous découvrons les **classes fondamentales de Tailwind** — spacing, typography, colors, borders, sizing — le vocabulaire que vous utiliserez dans 90% de votre code.

<br>
