---
description: "Tailwind CSS v4 — Installation et configuration : intégration native avec Vite via @tailwindcss/vite, configuration CSS-first sans tailwind.config.js, directives v4 et premier build."
icon: lucide/book-open-check
tags: ["TAILWIND V4", "INSTALLATION", "VITE", "LARAVEL", "CONFIGURATION CSS-FIRST"]
---

# Installation & Configuration (Tailwind v4)

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="4.x"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Atelier d'Usine Automatisé"
    Dans sa version 3, configurer Tailwind demandait d'installer de nombreuses dépendances distinctes (PostCSS, Autoprefixer, tailwindcss) et de maintenir un fichier de configuration JavaScript (`tailwind.config.js`) qui dupliquait vos chemins et vos styles. Tailwind v4 est un atelier d'usine automatisé en Rust : vous installez un seul outil natif pour Vite (`@tailwindcss/vite`), vous importez Tailwind dans votre CSS, et le compilateur détecte automatiquement tous vos fichiers sources sans configuration manuelle.

Ce module couvre l'installation de Tailwind CSS v4 dans un projet **Laravel 13 + Vite** — l'environnement standardisé moderne.

<br>

---

## Installation dans un Projet Laravel

### Prérequis

```bash title="Terminal - Vérifier les prérequis système"
# Node.js 20+ requis pour les outils récents
node --version
# Output attendu : v20.x.x ou supérieur

# npm 10+
npm --version
# Output attendu : 10.x.x ou supérieur

# Laravel 13 avec configuration Vite par défaut
php artisan --version
# Output attendu : Laravel Framework 13.x.x
```
_Vérification préalable des versions de Node.js, de npm et de Laravel pour assurer la compatibilité des outils de build._

### Installation de Tailwind v4 et du plugin Vite

Contrairement à la v3, plus besoin d'installer `postcss` ou `autoprefixer` séparément de manière obligatoire. Nous installons directement le cœur de Tailwind et son plugin d'intégration Vite natif.

```bash title="Terminal - Installer Tailwind CSS v4 dans Laravel"
# Depuis la racine de votre projet Laravel 13
npm install tailwindcss @tailwindcss/vite
```
_Commande d'installation locale de la dépendance principale de Tailwind v4 et de son plugin dédié pour le serveur de développement Vite._

<br>

---

## Configuration Vite — `@tailwindcss/vite`

Dans Tailwind v4, l'intégration se fait au plus près du compilateur d'assets. Nous devons déclarer le plugin dans `vite.config.js`.

### `vite.config.js` avec Tailwind v4

```js title="JavaScript - configuration de vite.config.js pour Tailwind v4"
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite'; // Import du plugin natif Rust

export default defineConfig({
    plugins: [
        tailwindcss(), // Doit être déclaré AVANT le plugin Laravel
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            refresh: true, // Auto-refresh en développement
        }),
    ],
});
```
_Fichier de configuration de Vite déclarant l'utilisation du compilateur Rust de Tailwind avant le middleware de gestion des assets de Laravel._

*Le plugin `@tailwindcss/vite` s'occupe de tout : il scanne automatiquement toutes les extensions de fichiers courantes de votre projet (`.blade.php`, `.js`, `.vue`, `.php`) pour détecter les classes utilisées. Il n'y a **aucun fichier `tailwind.config.js`** à créer ni à configurer.*

<br>

---

## Intégration dans le CSS (CSS-first)

Toute la personnalisation de votre design system s'effectue désormais directement dans votre fichier CSS principal en utilisant les variables CSS standard de niveau 4.

### Fichier `resources/css/app.css`

```css title="CSS - resources/css/app.css : importation et thème custom v4"
/* 1. Importation unique de Tailwind v4 */
@import "tailwindcss";

/* 2. Déclaration du thème (remplace le extend de tailwind.config.js) */
@theme {
  /* Déclaration de couleurs personnalisées */
  --color-brand-50: #eff6ff;
  --color-brand-500: #3b82f6;
  --color-brand-900: #1e3a5f;

  /* Déclaration de typographie personnalisée */
  --font-xxs: 0.65rem;
}

/* Vos styles personnalisés viennent ici */
.mon-bouton-custom {
  @apply bg-brand-500 text-white p-4 rounded-lg hover:bg-brand-900;
}
```
_Déclaration CSS-first où la directive @import charge Tailwind, et la directive @theme permet de surcharger les variables du système de design directement dans le CSS._

*Avec Tailwind v4, l'instruction `@import "tailwindcss";` remplace les anciennes directives `@tailwind base;`, `@tailwind components;` et `@tailwind utilities;`. La directive `@theme` définit les variables CSS globales que vous pouvez utiliser directement (par exemple, la couleur `--color-brand-500` génère automatiquement la classe `bg-brand-500`).*

<br>

---

## Inclusion dans le Layout Blade

```html title="Blade - layouts/app.blade.php : inclusion standard"
<!DOCTYPE html>
<html lang="fr" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? 'OmnyApp' }}</title>

    {{-- @vite injecte les balises d'importation --}}
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="h-full bg-slate-50 text-slate-900">
    {{ $slot }}
</body>
</html>
```
_Layout de base Laravel Blade incluant l'injecteur @vite qui résout et importe les fichiers CSS et JS compilés ou servis par le HMR._

<br>

---

## Workflow de Développement

Les commandes restent standardisées au niveau du gestionnaire de paquet de l'application, mais bénéficient de la compilation instantanée en Rust :

```bash title="Terminal - Commandes de développement et build"
# --- Mode Développement ---
# Lance le serveur Vite en tâche de fond. Le CSS se compile à la volée en quelques millisecondes.
npm run dev

# --- Mode Production ---
# Compile et minifie les assets pour la production en purgeant le CSS inutile.
npm run build
```
_Commandes système pour exécuter le serveur d'actualisation à chaud en local ou générer le bundle optimisé pour la mise en ligne._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Migration v3 vers v4**

Si vous reprenez un projet Laravel 11/12 existant utilisant Tailwind v3, réalisez les étapes de migration suivantes :
1. Désinstallez les anciens packages : `npm uninstall tailwindcss postcss autoprefixer`.
2. Installez les dépendances v4 : `npm install tailwindcss @tailwindcss/vite`.
3. Supprimez les fichiers de configuration devenus obsolètes : `rm tailwind.config.js postcss.config.js`.
4. Ajoutez le plugin `tailwindcss()` dans `vite.config.js`.
5. Modifiez `app.css` en remplaçant les directives `@tailwind` par `@import "tailwindcss";`.

**Exercice 2 — Personnaliser un thème en CSS-first**

1. Ajoutez une variable de police personnalisée `--font-primary` pointant vers une police système dans `@theme` (dans `resources/css/app.css`).
2. Appliquez-la à la balise `body` via la classe `font-primary`.
3. Vérifiez dans votre inspecteur de navigateur que la variable CSS est correctement générée et appliquée.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Tailwind v4 simplifie drastiquement le setup dans Laravel 13 en éliminant la configuration JavaScript et PostCSS. Tout s'articule autour du plugin Vite `@tailwindcss/vite` et d'une déclaration CSS unique `@import "tailwindcss";`. Le design system s'étend directement en écrivant des variables CSS au sein de la directive `@theme`. Le moteur de build Rust gère nativement le scan de fichiers pour le purging, garantissant des bundles de production minimes.

> Dans le module suivant, nous découvrons les **classes fondamentales de Tailwind** — spacing, typography, colors, borders, sizing — pour commencer à manipuler l'interface.
