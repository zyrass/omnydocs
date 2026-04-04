---
description: "Tailwind CSS — Responsive Design & Dark Mode : breakpoints mobile-first sm: md: lg: xl:, variante dark:, stratégies d'adaptation sans media queries manuelles."
icon: lucide/book-open-check
tags: ["TAILWIND", "RESPONSIVE", "DARK MODE", "BREAKPOINTS", "MOBILE-FIRST"]
---

# Responsive & Dark Mode

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Tenue Adaptable"
    Un caméléon ne change pas de couleur de façon aléatoire — il s'adapte à son environnement de manière prévisible. Le responsive Tailwind fonctionne pareil : `sm:flex` signifie "applique `flex` quand l'écran est `sm` ou plus grand". Pas de media queries à écrire, pas de fichiers séparés — chaque classe peut être préfixée avec `sm:`, `md:`, `lg:` pour devenir conditionnellement adaptative.

Tailwind suit une approche **mobile-first** : les classes sans préfixe s'appliquent à toutes les tailles d'écran. Les préfixes `sm:`, `md:`, `lg:` s'appliquent à partir d'une certaine largeur.

<br>

---

## Les Breakpoints Tailwind

| Préfixe | Min-width | Description |
|---|---|---|
| *(aucun)* | `0px` | Tous les écrans (mobile en premier) |
| `sm:` | `640px` | Petits écrans (lanscape mobile, tablette) |
| `md:` | `768px` | Tablettes |
| `lg:` | `1024px` | Desktops |
| `xl:` | `1280px` | Grands écrans |
| `2xl:` | `1536px` | Très grands écrans |

```html title="HTML (Tailwind) — Breakpoints : lecture de gauche à droite = mobile vers desktop"
<!-- Lecture : "1 colonne sur mobile, 2 sur tablet, 3 sur desktop" -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  ...
</div>

<!-- Lecture : "texte xl sur mobile, 2xl sur tablet, 4xl sur desktop" -->
<h1 class="text-xl sm:text-2xl lg:text-4xl font-bold">
  Bienvenue sur OmnyDocs
</h1>

<!-- Lecture : "caché sur mobile, visible à partir de md" -->
<aside class="hidden md:block">
  Navigation latérale
</aside>

<!-- Lecture : "pleine largeur sur mobile, auto sur desktop" -->
<button class="w-full md:w-auto px-6 py-2 bg-blue-600 text-white rounded-lg">
  Commencer
</button>
```

*Le préfixe `sm:` ne signifie pas "seulement sur small" — il signifie "à partir de `640px` et au-delà". C'est le principe mobile-first : on part du petit, on enrichit vers le grand.*

<br>

---

## Patterns Responsive Fréquents

### Grid Adaptatif

```html title="HTML (Tailwind) — Grille qui s'adapte du mobile au desktop"
<!-- Cartes : 1 col mobile → 2 col sm → 3 col lg → 4 col xl -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  <div class="bg-white rounded-lg p-4 shadow">Carte 1</div>
  <div class="bg-white rounded-lg p-4 shadow">Carte 2</div>
  <div class="bg-white rounded-lg p-4 shadow">Carte 3</div>
  <div class="bg-white rounded-lg p-4 shadow">Carte 4</div>
</div>
```

### Menu Hamburger vs Navigation Desktop

```html title="HTML (Tailwind) — Navigation : hamburger mobile, liens desktop"
<header class="bg-white border-b border-gray-200 px-6 py-4">
  <div class="flex items-center justify-between">
    <span class="font-bold text-lg">OmnyDocs</span>

    <!-- Menu hamburger : visible seulement sur mobile -->
    <button class="md:hidden p-2 text-gray-600" aria-label="Menu">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>

    <!-- Navigation : cachée sur mobile, visible à partir de md -->
    <nav class="hidden md:flex items-center gap-6">
      <a href="#" class="text-sm text-gray-600 hover:text-gray-900">Documentation</a>
      <a href="#" class="text-sm text-gray-600 hover:text-gray-900">Formations</a>
      <a href="#" class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg">
        Commencer
      </a>
    </nav>
  </div>
</header>
```

### Layout Sidebar

```html title="HTML (Tailwind) — Layout stacked mobile, sidebar desktop"
<div class="max-w-7xl mx-auto px-4 py-8">
  <!-- Sur mobile : colonne unique. Sur lg : sidebar + contenu -->
  <div class="flex flex-col lg:flex-row gap-8">

    <!-- Sidebar : pleine largeur mobile, 256px fixe sur desktop -->
    <aside class="w-full lg:w-64 lg:flex-none">
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        Sidebar de navigation
      </div>
    </aside>

    <!-- Contenu : pleine largeur, grandit sur desktop -->
    <main class="flex-1 min-w-0">
      <div class="bg-white rounded-lg border border-gray-200 p-6">
        Contenu principal
      </div>
    </main>
  </div>
</div>
```

<br>

---

## Dark Mode

Tailwind gère le dark mode avec la variante `dark:`. Deux modes de déclenchement :

```js title="JavaScript — tailwind.config.js : choisir la stratégie dark mode"
module.exports = {
  // 'media' : suit la préférence système (prefers-color-scheme)
  // 'class' : contrôlé par la classe 'dark' sur <html>
  darkMode: 'class',  // Recommandé pour permettre le toggle manuel
  // ...
}
```

### Appliquer les Classes Dark Mode

```html title="HTML (Tailwind) — Dark mode : variante dark: sur chaque classe concernée"
<!-- Le principe : dark:classe s'applique quand 'dark' est sur <html> -->
<div class="bg-white dark:bg-gray-900">

  <!-- Texte -->
  <h1 class="text-gray-900 dark:text-white">Titre</h1>
  <p class="text-gray-600 dark:text-gray-400">Corps du texte</p>
  <span class="text-gray-500 dark:text-gray-500">Secondaire</span>

  <!-- Backgrounds -->
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    Carte
  </div>

  <!-- Bordures -->
  <div class="border border-gray-200 dark:border-gray-700 rounded">
    Zone bordée
  </div>

  <!-- Boutons -->
  <button class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white px-4 py-2 rounded">
    Action
  </button>

</div>
```

### Toggle Dark Mode avec Alpine.js

```html title="HTML (Blade + Tailwind + Alpine.js) — Toggle dark mode"
{{-- Layout principal : x-data pour gérer le dark mode --}}
<html x-data="{ dark: localStorage.getItem('theme') === 'dark' }"
      x-bind:class="{ 'dark': dark }"
      x-init="$watch('dark', v => localStorage.setItem('theme', v ? 'dark' : 'light'))">
<head>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-white dark:bg-gray-900 transition-colors duration-300">

  {{-- Bouton toggle --}}
  <button
    @click="dark = !dark"
    class="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">

    {{-- Icône soleil (mode clair) --}}
    <svg x-show="dark" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path d="M10 2a1 1 0 011 1v1a1 1 0 01-2 0V3a1 1 0 011-1zm..."/>
    </svg>

    {{-- Icône lune (mode sombre) --}}
    <svg x-show="!dark" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
    </svg>
  </button>

  {{ $slot }}
</body>
</html>
```

*`localStorage` conserve la préférence de l'utilisateur entre les sessions. `transition-colors duration-300` crée une transition fluide lors du basculement.*

<br>

---

## Stratégie de Palette Dark Mode

```html title="HTML (Tailwind) — Palette complète : design system clair/sombre"
<!--
  Stratégie recommandée pour un design system cohérent :
  
  FOND PRINCIPAL :   bg-white          dark:bg-gray-950
  FOND SECONDAIRE :  bg-gray-50        dark:bg-gray-900
  FOND CARDS :       bg-white          dark:bg-gray-800
  
  TEXTE PRIMAIRE :   text-gray-900     dark:text-gray-50
  TEXTE SECONDAIRE : text-gray-600     dark:text-gray-400
  TEXTE TERTIRE :    text-gray-400     dark:text-gray-600
  
  BORDURES :         border-gray-200   dark:border-gray-700
  SÉPARATEURS :      border-gray-100   dark:border-gray-800
  
  ACCENT BLEU :      bg-blue-600       dark:bg-blue-500
  ACCENT TEXTE :     text-blue-600     dark:text-blue-400
-->

<!-- Exemple appliqué -->
<div class="min-h-screen bg-white dark:bg-gray-950 transition-colors">
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-50 mb-4">
      Documentation Tailwind
    </h1>
    <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-6">
      <p class="text-gray-700 dark:text-gray-300 leading-relaxed">
        Cette carte s'adapte automatiquement au mode sombre.
      </p>
    </div>
  </div>
</div>
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Page Hero Responsive**

```html title="HTML — Exercice 1 : hero section adaptative"
<!-- Créez une section Hero avec :
     - Texte centré sur mobile (text-center), aligné à gauche sur lg (lg:text-left)
     - Layout flex-col sur mobile, flex-row sur lg
     - Titre : text-3xl mobile → text-5xl lg
     - Description : text-base mobile → text-lg lg
     - 2 boutons côte à côte sur mobile, séparés sur lg
     - Image : cachée sur mobile (hidden), visible sur lg (lg:block) -->
```

**Exercice 2 — Carte Dark Mode Ready**

```html title="HTML — Exercice 2 : composant card avec dark mode complet"
<!-- Créez une carte "article" complète avec dark mode :
     Fond : bg-white dark:bg-gray-800
     Titre : text-gray-900 dark:text-gray-100
     Description : text-gray-600 dark:text-gray-400
     Date : text-gray-400 dark:text-gray-500
     Bordure : border-gray-200 dark:border-gray-700
     Tag : bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 -->
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    L'approche **mobile-first** de Tailwind signifie que las classes sans préfixe ciblent tous les écrans, et les préfixes `sm:`, `md:`, `lg:`, `xl:` s'activent progressivement. `hidden md:block` est le pattern pour masquer un élément sur mobile et l'afficher sur desktop. Le dark mode avec `darkMode: 'class'` permet un toggle Manuel contrôlé : `dark:bg-gray-900` s'active quand la classe `dark` est présente sur `<html>`. La combinaison Tailwind + Alpine.js pour le toggle dark mode est la solution standard dans la Stack TALL.

> Dans le module suivant, nous couvrons les **états et interactions** — `hover:`, `focus:`, `active:`, `group-hover:`, `peer:`, transitions et animations — pour des interfaces réactives sans une ligne de JavaScript.

<br>
