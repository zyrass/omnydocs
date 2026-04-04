---
description: "Tailwind CSS — Flexbox & Grid : layouts complexes avec utilitaires flex, grid, gap, justify, items, col-span sans écrire une ligne de CSS."
icon: lucide/book-open-check
tags: ["TAILWIND", "FLEXBOX", "GRID", "LAYOUT", "GAP", "RESPONSIVE"]
---

# Flexbox & Grid avec Tailwind

<div
  class="omny-meta"
  data-level="🟢→🟡 Intermédiaire"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Grille d'un Journal"
    Un journal imprimé organise son contenu en colonnes — certains articles occupent 1 colonne, d'autres 2 ou 3. Le chef de mise en page n'invente pas les règles : il suit une grille définie. Tailwind Flexbox et Grid sont cette grille : des règles précises que vous appliquez directement sur les conteneurs et leurs enfants. Pas de CSS à inventer — juste des classes à composer.

Les utilitaires Tailwind pour Flexbox et CSS Grid couvrent l'intégralité des propriétés CSS correspondantes. Ce module construit des interfaces complètes sans écrire une ligne de CSS personnalisé.

<br>

---

## Flexbox — Les Bases

```html title="HTML (Tailwind) — Flexbox : conteneur et enfants"
<!-- Activer Flexbox -->
<div class="flex">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Direction -->
<div class="flex flex-row">     <!-- flex-direction: row (défaut) -->
<div class="flex flex-col">     <!-- flex-direction: column -->
<div class="flex flex-row-reverse"> <!-- Inversé horizontalement -->
<div class="flex flex-col-reverse"> <!-- Inversé verticalement -->

<!-- Alignement principal (justify-content) -->
<div class="flex justify-start">   <!-- flex-start — défaut -->
<div class="flex justify-center">  <!-- center -->
<div class="flex justify-end">     <!-- flex-end -->
<div class="flex justify-between"> <!-- space-between -->
<div class="flex justify-around">  <!-- space-around -->
<div class="flex justify-evenly">  <!-- space-evenly -->

<!-- Alignement croisé (align-items) -->
<div class="flex items-start">    <!-- align-items: flex-start -->
<div class="flex items-center">   <!-- align-items: center -->
<div class="flex items-end">      <!-- align-items: flex-end -->
<div class="flex items-stretch">  <!-- align-items: stretch — défaut -->
<div class="flex items-baseline"> <!-- align-items: baseline -->

<!-- Gap (espacement entre enfants — meilleur que margin) -->
<div class="flex gap-4">         <!-- gap: 1rem entre tous les items -->
<div class="flex gap-x-4 gap-y-2"> <!-- gap-x horizontal, gap-y vertical -->
```

<br>

---

## Flexbox — Propriétés sur les Enfants

```html title="HTML (Tailwind) — Flex items : grow, shrink, basis, auto"
<div class="flex gap-4">

  <!-- flex-grow : prend tout l'espace disponible -->
  <div class="flex-1">    <!-- flex: 1 1 0% — grandit pour remplir -->
  <div class="flex-auto">  <!-- flex: 1 1 auto -->
  <div class="flex-none">  <!-- flex: none — taille fixe, ne grandit pas -->

  <!-- Alignement individuel (override de items-*) -->
  <div class="self-start">  <!-- align-self: flex-start -->
  <div class="self-center"> <!-- align-self: center -->
  <div class="self-end">    <!-- align-self: flex-end -->

  <!-- Ordre -->
  <div class="order-first"> <!-- order: -9999 — premier visuellement -->
  <div class="order-last">  <!-- order: 9999 — dernier visuellement -->
  <div class="order-2">     <!-- order: 2 -->

</div>
```

### Exemple — Header de Navigation

```html title="HTML (Tailwind) — Header avec Flexbox : logo, nav, actions"
<header class="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200">

  <!-- Logo — taille fixe, ne grandit pas -->
  <div class="flex-none">
    <span class="text-xl font-bold text-blue-600">OmnyDocs</span>
  </div>

  <!-- Navigation centrale — grandit pour prendre l'espace -->
  <nav class="flex-1 flex justify-center gap-8">
    <a href="#" class="text-sm font-medium text-gray-700 hover:text-blue-600">Documentation</a>
    <a href="#" class="text-sm font-medium text-gray-700 hover:text-blue-600">Formations</a>
    <a href="#" class="text-sm font-medium text-gray-700 hover:text-blue-600">À propos</a>
  </nav>

  <!-- Actions — taille fixe, à droite -->
  <div class="flex-none flex items-center gap-3">
    <button class="text-sm text-gray-600">Connexion</button>
    <button class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg">
      Commencer
    </button>
  </div>
</header>
```

<br>

---

## CSS Grid — Les Bases

```html title="HTML (Tailwind) — CSS Grid : colonnes, rangées, gap"
<!-- Grid avec nombre de colonnes fixe -->
<div class="grid grid-cols-2">   <!-- 2 colonnes égales -->
<div class="grid grid-cols-3">   <!-- 3 colonnes égales -->
<div class="grid grid-cols-4">   <!-- 4 colonnes égales -->
<div class="grid grid-cols-6">   <!-- 6 colonnes égales -->
<div class="grid grid-cols-12">  <!-- 12 colonnes (layout classique) -->

<!-- Gap sur la grille -->
<div class="grid grid-cols-3 gap-4">      <!-- gap: 1rem partout -->
<div class="grid grid-cols-3 gap-x-6 gap-y-4"> <!-- horizontal 1.5rem, vertical 1rem -->

<!-- Rangées -->
<div class="grid grid-rows-3">   <!-- 3 rangées -->
<div class="grid grid-rows-none"> <!-- Rangées automatiques -->

<!-- Colonnes en template custom -->
<div class="grid grid-cols-[250px_1fr_1fr]"> <!-- Sidebar + 2 colonnes flex -->
```

### Propriétés sur les Enfants Grid

```html title="HTML (Tailwind) — Grid items : col-span, row-span, placement"
<div class="grid grid-cols-3 gap-4">

  <!-- Étendre sur plusieurs colonnes -->
  <div class="col-span-1"> <!-- Occupe 1 colonne (défaut) -->
  <div class="col-span-2"> <!-- Occupe 2 colonnes -->
  <div class="col-span-3"> <!-- Occupe toute la largeur -->
  <div class="col-span-full"> <!-- Identique à col-span-3 ici -->

  <!-- Étendre sur plusieurs rangées -->
  <div class="row-span-2"> <!-- Occupe 2 rangées de hauteur -->

  <!-- Placement explicite -->
  <div class="col-start-2 col-end-4"> <!-- Commence col 2, finit col 4 -->

</div>
```

<br>

---

## Exemple Complet — Layout de Page

```html title="HTML (Tailwind) — Layout complet : sidebar + content + aside"
<!-- Layout trois colonnes : sidebar fixe, contenu flexible, aside fixe -->
<div class="min-h-screen bg-gray-50">

  <!-- Header sticky -->
  <header class="sticky top-0 z-10 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
    <span class="font-bold text-lg text-gray-900">OmnyDocs</span>
    <nav class="flex gap-6">
      <a href="#" class="text-sm text-gray-600 hover:text-gray-900">Docs</a>
      <a href="#" class="text-sm text-gray-600 hover:text-gray-900">Blog</a>
    </nav>
  </header>

  <!-- Corps : 3 colonnes sur desktop -->
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="grid grid-cols-1 md:grid-cols-[240px_1fr_200px] gap-8">

      <!-- Sidebar de navigation -->
      <aside class="hidden md:block">
        <nav class="space-y-1">
          <a href="#" class="flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg">
            Introduction
          </a>
          <a href="#" class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
            Installation
          </a>
          <a href="#" class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
            Classes de base
          </a>
        </nav>
      </aside>

      <!-- Contenu principal -->
      <main class="min-w-0">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">Flexbox & Grid</h1>
        <p class="text-gray-600 leading-relaxed mb-6">
          Les utilitaires layout de Tailwind couvrent l'intégralité de Flexbox et CSS Grid.
        </p>

        <!-- Grille de cartes dans le contenu -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h3 class="font-semibold text-gray-900 mb-1">Flexbox</h3>
            <p class="text-sm text-gray-600">Layouts monodimensionnels</p>
          </div>
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h3 class="font-semibold text-gray-900 mb-1">Grid</h3>
            <p class="text-sm text-gray-600">Layouts bidimensionnels</p>
          </div>
        </div>
      </main>

      <!-- Aside droite (table des matières) -->
      <aside class="hidden md:block">
        <div class="sticky top-24">
          <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Sur cette page
          </p>
          <nav class="space-y-2">
            <a href="#flexbox" class="block text-sm text-gray-600 hover:text-blue-600">Flexbox</a>
            <a href="#grid" class="block text-sm text-gray-600 hover:text-blue-600">CSS Grid</a>
          </nav>
        </div>
      </aside>

    </div>
  </div>
</div>
```

*Ce layout complet — header sticky, sidebar, contenu, aside — utilise uniquement `flex` et `grid`. La colonne `grid-cols-[240px_1fr_200px]` définit des valeurs arbitraires avec la syntaxe `[]` de Tailwind v3.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Grille de cards**

```html title="HTML — Exercice 1 : grille responsive de produits"
<!-- Créez une grille de 6 cartes produits :
     - 1 colonne sur mobile
     - 2 colonnes sur sm
     - 3 colonnes sur lg
     - gap de 6 entre les cartes
     Chaque carte : image (div bg-gray-200, h-48), titre, prix en bleu, bouton -->
<div class="grid ...">
  <!-- 6 cartes -->
</div>
```

**Exercice 2 — Dashboard statistics**

```html title="HTML — Exercice 2 : bandeau de statistiques avec Flexbox"
<!-- Créez un bandeau de 4 statistiques côte à côte :
     - justify-between
     - Chaque stat : chiffre en text-3xl font-bold, label en text-sm text-gray-500
     - Bordure droite entre les stats (sauf la dernière)
     - Fond blanc, padding, ombre légère (shadow-sm) -->
<div class="flex ...">
  <div class="...">
    <p class="text-3xl font-bold">4,821</p>
    <p class="text-sm text-gray-500">Utilisateurs</p>
  </div>
  <!-- × 3 -->
</div>
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Tailwind expose l'intégralité de Flexbox (`flex`, `flex-col`, `justify-*`, `items-*`, `gap-*`, `flex-1`) et CSS Grid (`grid`, `grid-cols-*`, `col-span-*`, `gap-*`) via des utilitaires prévisibles. `flex items-center justify-between` remplace 3 lignes de CSS. `grid grid-cols-3 gap-6` crée une grille en 2 mots. La syntaxe arbitraire `grid-cols-[240px_1fr_200px]` permet des layouts sur-mesure sans quitter le HTML. `max-w-7xl mx-auto` est le pattern canonique pour centrer et contraindre la largeur d'un layout.

> Dans le module suivant, nous abordons le **Responsive Design et le Dark Mode** — les préfixes `sm:`, `md:`, `lg:`, `xl:` et `dark:` pour des interfaces adaptatives zéro configuration.

<br>
