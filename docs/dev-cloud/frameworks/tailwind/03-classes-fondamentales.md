---
description: "Tailwind CSS — Classes fondamentales : spacing, typography, colors, borders, sizing — le vocabulaire essentiel pour styliser n'importe quel élément."
icon: lucide/book-open-check
tags: ["TAILWIND", "SPACING", "TYPOGRAPHY", "COLORS", "SIZING", "BORDERS"]
---

# Classes Fondamentales

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Alphabet du Designer"
    Un typographe maîtrise son alphabet avant d'écrire. En Tailwind, les classes fondamentales sont cet alphabet : `p-4` pour l'espacement intérieur, `text-xl` pour la taille de police, `bg-blue-500` pour la couleur. Une fois cet alphabet intériorisé (ce qui prend 2-3 jours), vous lisez et écrivez du Tailwind aussi naturellement que du français. Ce module vous donne l'alphabet complet.

Tailwind suit une **échelle de valeurs cohérente** basée sur une unité de 4px (`rem`). `p-1` = `0.25rem` = `4px`, `p-4` = `1rem` = `16px`, `p-8` = `2rem` = `32px`. Cette cohérence rend les designs naturellement harmonieux.

<br>

---

## Spacing — Marges & Paddings

Le système d'espacement Tailwind utilise une échelle de 0 à 96 (par pas de 0.5, 1, 2...).

```html title="HTML (Tailwind) — Spacing : padding, margin et leurs variantes directionnelles"
<!-- Padding uniforme -->
<div class="p-4">   <!-- padding: 1rem (16px) tous côtés -->
<div class="p-8">   <!-- padding: 2rem (32px) tous côtés -->

<!-- Padding directionnel -->
<div class="px-4">  <!-- padding-left: 1rem; padding-right: 1rem -->
<div class="py-2">  <!-- padding-top: 0.5rem; padding-bottom: 0.5rem -->
<div class="pt-6">  <!-- padding-top: 1.5rem -->
<div class="pb-4">  <!-- padding-bottom: 1rem -->
<div class="pl-2">  <!-- padding-left: 0.5rem -->
<div class="pr-2">  <!-- padding-right: 0.5rem -->

<!-- Margin uniforme -->
<div class="m-4">   <!-- margin: 1rem tous côtés -->
<div class="mx-auto">  <!-- margin-left: auto; margin-right: auto (centrage) -->
<div class="my-8">  <!-- margin-top: 2rem; margin-bottom: 2rem -->
<div class="mt-4">  <!-- margin-top: 1rem -->
<div class="mb-6">  <!-- margin-bottom: 1.5rem -->
<div class="space-y-4">  <!-- gap vertical entre enfants directs : 1rem -->
```

*`mx-auto` est le pattern classique pour centrer un élément de largeur fixe. `space-y-4` est plus pratique que `mt-4` sur chaque enfant — il applique `margin-top: 1rem` à tous les enfants sauf le premier.*

| Valeur | `rem` | `px` |
|---|---|---|
| `0` | `0` | `0` |
| `0.5` | `0.125rem` | `2px` |
| `1` | `0.25rem` | `4px` |
| `2` | `0.5rem` | `8px` |
| `4` | `1rem` | `16px` |
| `6` | `1.5rem` | `24px` |
| `8` | `2rem` | `32px` |
| `12` | `3rem` | `48px` |
| `16` | `4rem` | `64px` |

<br>

---

## Typography — Texte & Police

```html title="HTML (Tailwind) — Typography : taille, graisse, alignement, couleur"
<!-- Taille de police -->
<p class="text-xs">   Extra small — 0.75rem (12px) </p>
<p class="text-sm">   Small — 0.875rem (14px) </p>
<p class="text-base"> Base — 1rem (16px) — défaut </p>
<p class="text-lg">   Large — 1.125rem (18px) </p>
<p class="text-xl">   XL — 1.25rem (20px) </p>
<p class="text-2xl">  2XL — 1.5rem (24px) </p>
<p class="text-3xl">  3XL — 1.875rem (30px) </p>
<p class="text-4xl">  4XL — 2.25rem (36px) </p>

<!-- Graisse (font-weight) -->
<p class="font-thin">     font-weight: 100 </p>
<p class="font-light">    font-weight: 300 </p>
<p class="font-normal">   font-weight: 400 — défaut </p>
<p class="font-medium">   font-weight: 500 </p>
<p class="font-semibold"> font-weight: 600 </p>
<p class="font-bold">     font-weight: 700 </p>
<p class="font-black">    font-weight: 900 </p>

<!-- Alignement -->
<p class="text-left">   Aligné à gauche </p>
<p class="text-center"> Centré </p>
<p class="text-right">  Aligné à droite </p>

<!-- Hauteur de ligne (line-height) -->
<p class="leading-tight">   line-height: 1.25 </p>
<p class="leading-normal">  line-height: 1.5 — défaut </p>
<p class="leading-relaxed"> line-height: 1.625 </p>
<p class="leading-loose">   line-height: 2 </p>

<!-- Décoration -->
<p class="underline">         text-decoration: underline </p>
<p class="line-through">      text-decoration: line-through </p>
<p class="no-underline">      text-decoration: none </p>
<p class="uppercase">         text-transform: uppercase </p>
<p class="lowercase">         text-transform: lowercase </p>
<p class="capitalize">        text-transform: capitalize </p>
<p class="truncate">          overflow: hidden; text-overflow: ellipsis </p>
```

<br>

---

## Colors — Palette de Couleurs

Tailwind fournit une palette complète avec 22 couleurs × 11 nuances chacune (50 à 950).

```html title="HTML (Tailwind) — Colors : background, text, border"
<!-- Background colors -->
<div class="bg-white">       Background blanc </div>
<div class="bg-gray-50">     Gris très clair </div>
<div class="bg-gray-100">    Gris clair </div>
<div class="bg-gray-900">    Gris très foncé </div>
<div class="bg-blue-500">    Bleu medium </div>
<div class="bg-blue-600">    Bleu foncé </div>
<div class="bg-emerald-500"> Vert / success </div>
<div class="bg-red-500">     Rouge / danger </div>
<div class="bg-amber-500">   Jaune / warning </div>
<div class="bg-slate-800">   Gris bleuté foncé </div>

<!-- Text colors -->
<p class="text-gray-900">   Texte noir (principal) </p>
<p class="text-gray-700">   Texte foncé (corps) </p>
<p class="text-gray-500">   Texte secondaire </p>
<p class="text-gray-400">   Texte désactivé </p>
<p class="text-blue-600">   Texte bleu (liens) </p>
<p class="text-white">      Texte blanc </p>

<!-- Opacité de couleur -->
<div class="bg-blue-500/50">  Background bleu à 50% d'opacité </div>
<div class="bg-black/10">     Overlay noir léger </div>
<p class="text-gray-900/75">  Texte à 75% d'opacité </p>
```

*La notation `/50` pour l'opacité est une fonctionnalité moderne de Tailwind v3. `bg-blue-500/50` est équivalent à `background-color: rgb(59 130 246 / 0.5)` — pas besoin de variables CSS ou de HSLA.*

**Palette Tailwind complète (extrait) :**

| Couleur | 100 | 300 | 500 | 700 | 900 |
|---|---|---|---|---|---|
| `slate` | #f1f5f9 | #cbd5e1 | #64748b | #334155 | #0f172a |
| `blue` | #dbeafe | #93c5fd | #3b82f6 | #1d4ed8 | #1e3a8a |
| `emerald` | #d1fae5 | #6ee7b7 | #10b981 | #047857 | #064e3b |
| `rose` | #ffe4e6 | #fda4af | #f43f5e | #be123c | #881337 |

<br>

---

## Sizing — Largeurs & Hauteurs

```html title="HTML (Tailwind) — Sizing : width, height, min/max"
<!-- Largeurs fixes (même échelle que spacing) -->
<div class="w-4">   width: 1rem </div>
<div class="w-16">  width: 4rem (64px) </div>
<div class="w-32">  width: 8rem (128px) </div>
<div class="w-64">  width: 16rem (256px) </div>

<!-- Largeurs relatives -->
<div class="w-full">     width: 100% </div>
<div class="w-1/2">      width: 50% </div>
<div class="w-1/3">      width: 33.333% </div>
<div class="w-2/3">      width: 66.667% </div>
<div class="w-screen">   width: 100vw </div>
<div class="w-auto">     width: auto </div>

<!-- Hauteurs -->
<div class="h-4">      height: 1rem </div>
<div class="h-16">     height: 4rem </div>
<div class="h-full">   height: 100% </div>
<div class="h-screen"> height: 100vh </div>

<!-- Min/Max -->
<div class="min-w-0">       min-width: 0 (évite l'overflow flex) </div>
<div class="max-w-xs">      max-width: 20rem (320px) </div>
<div class="max-w-sm">      max-width: 24rem (384px) </div>
<div class="max-w-md">      max-width: 28rem (448px) </div>
<div class="max-w-lg">      max-width: 32rem (512px) </div>
<div class="max-w-xl">      max-width: 36rem (576px) </div>
<div class="max-w-2xl">     max-width: 42rem (672px) </div>
<div class="max-w-7xl">     max-width: 80rem (1280px) </div>
<div class="max-w-prose">   max-width: 65ch (lisibilité optimale) </div>
```

<br>

---

## Borders — Bordures & Coins Arrondis

```html title="HTML (Tailwind) — Borders : épaisseur, couleur, coins arrondis"
<!-- Épaisseur de bordure -->
<div class="border">     border-width: 1px (défaut) </div>
<div class="border-2">   border-width: 2px </div>
<div class="border-4">   border-width: 4px </div>
<div class="border-t">   border-top-width: 1px seulement </div>
<div class="border-b">   border-bottom-width: 1px seulement </div>
<div class="border-l-4"> border-left-width: 4px </div>

<!-- Couleur de bordure -->
<div class="border border-gray-200">    Bordure grise légère </div>
<div class="border-2 border-blue-500">  Bordure bleue 2px </div>
<div class="border border-red-300">     Bordure rouge légère </div>

<!-- Coins arrondis (border-radius) -->
<div class="rounded-sm">    border-radius: 0.125rem (2px) </div>
<div class="rounded">       border-radius: 0.25rem (4px) — défaut </div>
<div class="rounded-md">    border-radius: 0.375rem (6px) </div>
<div class="rounded-lg">    border-radius: 0.5rem (8px) </div>
<div class="rounded-xl">    border-radius: 0.75rem (12px) </div>
<div class="rounded-2xl">   border-radius: 1rem (16px) </div>
<div class="rounded-3xl">   border-radius: 1.5rem (24px) </div>
<div class="rounded-full">  border-radius: 9999px (cercle/pilule) </div>

<!-- Ring (focus outline) -->
<button class="ring-2 ring-blue-500 ring-offset-2">
  <!-- Anneau bleu avec espace (commun pour les focus) -->
</button>
```

<br>

---

## Shadows & Display

```html title="HTML (Tailwind) — Shadow, Display et autres utilitaires fréquents"
<!-- Box Shadow -->
<div class="shadow-sm">   Ombre subtile </div>
<div class="shadow">      Ombre légère </div>
<div class="shadow-md">   Ombre medium </div>
<div class="shadow-lg">   Ombre prononcée </div>
<div class="shadow-xl">   Ombre très prononcée </div>
<div class="shadow-none"> Aucune ombre </div>

<!-- Display -->
<div class="block">         display: block </div>
<div class="inline">        display: inline </div>
<div class="inline-block">  display: inline-block </div>
<div class="hidden">        display: none </div>

<!-- Position -->
<div class="static">    position: static (défaut) </div>
<div class="relative">  position: relative </div>
<div class="absolute">  position: absolute </div>
<div class="fixed">     position: fixed </div>
<div class="sticky">    position: sticky </div>
<div class="top-4">     top: 1rem </div>
<div class="right-0">   right: 0 </div>
<div class="inset-0">   top/right/bottom/left: 0 (overlay fullscreen) </div>

<!-- Opacity -->
<div class="opacity-0">   opacity: 0 </div>
<div class="opacity-50">  opacity: 0.5 </div>
<div class="opacity-100"> opacity: 1 </div>

<!-- Overflow -->
<div class="overflow-hidden">  overflow: hidden </div>
<div class="overflow-auto">    overflow: auto </div>
<div class="overflow-scroll">  overflow: scroll </div>
```

<br>

---

## Composition — Exemple Complet

```html title="HTML (Tailwind) — Carte de profil composée avec les fondamentaux"
<!-- Carte de profil complète : uniquement avec les classes de ce module -->
<div class="bg-white rounded-xl shadow-md p-6 max-w-sm">

  <!-- Avatar -->
  <div class="flex items-center mb-4">
    <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center mr-3">
      <span class="text-white font-bold text-lg">AG</span>
    </div>
    <div>
      <p class="font-semibold text-gray-900">Alain Guillon</p>
      <p class="text-sm text-gray-500">Développeur Full-Stack</p>
    </div>
  </div>

  <!-- Description -->
  <p class="text-gray-700 text-sm leading-relaxed mb-4">
    Passionné par Laravel, Tailwind et la documentation technique.  
    Créateur d'OmnyDocs.
  </p>

  <!-- Tags -->
  <div class="flex space-x-2 mb-4">
    <span class="bg-blue-100 text-blue-700 text-xs font-medium px-2.5 py-0.5 rounded-full">
      Laravel
    </span>
    <span class="bg-emerald-100 text-emerald-700 text-xs font-medium px-2.5 py-0.5 rounded-full">
      Tailwind
    </span>
  </div>

  <!-- Bouton -->
  <button class="w-full bg-blue-600 text-white font-medium py-2 rounded-lg text-sm">
    Voir le profil
  </button>
</div>
```

*Cette carte est entièrement stylisée sans une ligne de CSS personnalisé — uniquement avec les classes fondamentales de ce module.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Badge coloré**

```html title="HTML — Exercice 1 : créer des badges de statut"
<!-- Créez 3 badges de statut avec des classes Tailwind :
     - "Actif" → vert (bg-emerald-100, text-emerald-700)
     - "En attente" → jaune (bg-amber-100, text-amber-700)
     - "Inactif" → rouge (bg-red-100, text-red-700)
     Chaque badge doit être arrondi (rounded-full), avoir du padding (px-3 py-1)
     et une police petite (text-xs) et medium (font-medium) -->
<span class="...">Actif</span>
<span class="...">En attente</span>
<span class="...">Inactif</span>
```

**Exercice 2 — Carte d'article**

```html title="HTML — Exercice 2 : carte d'article de blog"
<!-- Reproduisez une carte d'article avec :
     - Fond blanc, coins arrondis (rounded-xl), ombre (shadow-md)
     - Image de placeholder : div de 200px de haut, bg-gray-200, rounded-t-xl
     - Catégorie en badge bleu en haut de l'image (position absolute)
     - Titre en text-xl, font-semibold
     - Description en text-gray-600, text-sm, 2 lignes max (line-clamp-2)
     - Lien "Lire l'article" en bleu avec underline -->
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les classes fondamentales Tailwind suivent des **conventions prévisibles** : préfixe (`p-`, `m-`, `w-`, `h-`, `text-`, `bg-`, `border-`) + valeur (chiffre ou nom). L'échelle de spacing utilise des pas de `0.25rem` (4px). La palette de couleurs propose 22 teintes × 11 nuances. Les coins arrondis vont de `rounded-sm` (2px) à `rounded-full`. Une fois cet alphabet maîtrisé, vous construisez n'importe quelle interface sans ouvrir un fichier CSS. La notation `/50` permet de contrôler l'opacité directement sur la classe couleur.

> Dans le module suivant, nous construisons des **layouts complexes** avec les utilitaires Flexbox et Grid de Tailwind — `flex`, `grid`, `gap`, `justify-*`, `items-*`, `col-span-*`.

<br>
