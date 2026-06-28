---
description: "Tailwind CSS v4 — Intégration dans Laravel 13 : configuration avancée du plugin Vite, gestion des assets via la directive @vite, compilation de production, et déploiement."
icon: lucide/book-open-check
tags: ["TAILWIND V4", "LARAVEL 13", "VITE", "ASSETS", "DEPLOYMENT"]
---

# Intégration dans Laravel 13

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire à 🔴 Avancé"
  data-version="4.x"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chef d'Orchestre et les Musiciens"
    Dans une salle de concert, le chef d'orchestre (Vite) doit coordonner plusieurs musiciens (PHP/Blade, JavaScript, CSS/Tailwind) pour jouer une symphonie harmonieuse (votre application Web). Dans l'écosystème Laravel 13, cette coordination s'effectue sans aucune friction. Grâce au plugin `@tailwindcss/vite`, le chef d'orchestre surveille chaque note jouée dans vos fichiers Blade, ordonne au compilateur Rust de compiler les styles instantanément, et sert le résultat final au public (le navigateur) sans aucun temps mort.

Ce module détaille la structure et l'optimisation de Tailwind CSS v4.x au sein d'une application **Laravel 13** en environnement de production.

<br>

---

## 1. Structure des Fichiers et Assets

Dans une installation Laravel 13 typique, les assets se situent dans le dossier `resources/`, tandis que les fichiers compilés pour le navigateur sont stockés dans le dossier public `public/build/`.

### Organisation recommandée

```
mon-projet-laravel/
├── resources/
│   ├── css/
│   │   └── app.css          # Point d'entrée CSS principal
│   ├── js/
│   │   └── app.js           # Script JavaScript principal
│   └── views/
│       ├── layouts/
│       │   └── app.blade.php # Layout HTML principal
│       └── welcome.blade.php # Page d'accueil standard
├── vite.config.js           # Configuration du bundler Vite
└── package.json             # Dépendances Node.js et scripts de build
```
_Arborescence standard des fichiers sources d'assets dans un projet Laravel 13._

Le compilateur de Tailwind v4 lit le fichier `resources/css/app.css` qui contient la directive `@import "tailwindcss";`. Il scanne ensuite tous les fichiers se trouvant sous `resources/views/` (les templates Blade) et sous `resources/js/` (les scripts) pour en extraire les classes CSS utilisées.

<br>

---

## 2. Configuration Optimisée de Vite

Le fichier `vite.config.js` est le cœur du système de build. Voici la configuration optimale pour intégrer Tailwind v4 de manière performante.

### `vite.config.js`

```js title="JavaScript - configuration complète de vite.config.js pour Laravel 13 + Tailwind v4"
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [
        // Le plugin Tailwind doit TOUJOURS être appelé avant le plugin Laravel
        tailwindcss(),
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            // Active le rechargement automatique en développement à chaque sauvegarde Blade/CSS/JS
            refresh: true,
        }),
    ],
    // Configuration réseau optionnelle pour écouter sur toutes les interfaces (ex: Docker)
    server: {
        host: '0.0.0.0',
        port: 5173,
    }
});
```
_Déclaration du plugin Vite Tailwind aux côtés du middleware Laravel pour orchestrer la compilation à chaud._

*Grâce au moteur Rust de Tailwind v4, les modifications CSS sont appliquées via le Hot Module Replacement (HMR) presque instantanément (généralement en moins de 10 millisecondes), sans recharger la page entière.*

<br>

---

## 3. Chargement des Assets dans les Vues Blade

Laravel 13 utilise la directive `@vite` pour injecter automatiquement les balises HTML `<link>` et `<script>` appropriées dans vos layouts.

### Exemple de Layout Blade principal

```html title="Blade - resources/views/layouts/app.blade.php : structure HTML"
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title ?? config('app.name', 'Laravel') }}</title>

    <!-- Injection automatique des styles et scripts compilés -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-slate-100 text-slate-900 antialiased min-h-screen">
    <main class="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {{ $slot }}
    </main>
</body>
</html>
```
_Template de base utilisant la directive @vite pour orchestrer l'inclusion dynamique des fichiers de style et de logique._

<br>

---

## 4. Compilation et Déploiement en Production

Avant de déployer votre application sur un serveur de production (VPS, Heroku, Laravel Forge, etc.), vous devez générer les assets minifiés et purgés pour garantir des performances optimales.

### Commandes de production

```bash title="Terminal - Compilation des assets pour la production"
# 1. Installer toutes les dépendances Node.js du projet
npm install

# 2. Exécuter le script de compilation pour la production
npm run build
```
_Séquence de commandes pour compiler, purger et minifier le CSS final dans le dossier public._

À l'issue de la commande `npm run build`, Vite génère les fichiers finaux dans le dossier `public/build/assets/` avec des identifiants uniques (hachages) pour éviter les problèmes de mise en cache du navigateur (ex : `app-Bw9lBwJV.css`). Le fichier CSS final est débarrassé de tout code inutile et ne pèse généralement que quelques dizaines de kilo-octets.

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Tester le Hot Module Replacement (HMR)**

1. Lancez le serveur de développement Laravel (`php artisan serve`) et le serveur de développement Vite (`npm run dev`) en parallèle.
2. Ouvrez la page d'accueil dans votre navigateur.
3. Modifiez une classe CSS dans `welcome.blade.php` (par exemple, passez de `bg-slate-100` à `bg-amber-100`).
4. Constatez l'application immédiate du style dans votre navigateur sans aucun rechargement manuel de la page.

**Exercice 2 — Valider le Build de Production**

1. Exécutez la commande `npm run build`.
2. Inspectez le dossier `public/build/assets/` et localisez le fichier CSS généré.
3. Ouvrez-le et recherchez les classes utilitaires que vous n'avez pas utilisées dans votre projet (ex: `bg-purple-500`). Vérifiez qu'elles ont été correctement purgées.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    L'intégration de Tailwind v4 dans Laravel 13 repose sur l'association transparente du plugin `@tailwindcss/vite` et de la directive Blade `@vite`. Le serveur de développement assure un retour visuel instantané grâce au HMR, tandis que le build de production génère des bundles minimes hautement optimisés grâce au purging automatique géré au niveau du compilateur Rust de Tailwind.

> **Félicitations !** Vous avez terminé la formation complète sur Tailwind CSS v4. La prochaine étape naturelle est de dynamiser vos interfaces utilisateur en explorant la **[formation Livewire v4](../livewire/index.md)**.
