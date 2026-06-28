---
description: "Tailwind CSS v4 — Plugins et theming avancé : personnalisation du design system en CSS-first via @theme, création d'utilitaires via @utility, importation de plugins via @plugin, et DaisyUI v5."
icon: lucide/book-open-check
tags: ["TAILWIND V4", "THEMING", "PLUGINS", "DAISYUI", "CSS-FIRST"]
---

# Plugins & Theming Avancé (Tailwind v4)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="4.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Architecte et la Charte de Chantier"
    Concevoir une application sans design system, c'est comme laisser chaque ouvrier choisir la couleur des briques et la hauteur des fenêtres au feeling. Dans Tailwind v3, la charte était un script JavaScript externe (`tailwind.config.js`). Avec Tailwind v4, la charte est directement écrite dans le ciment de votre feuille de style : vous rédigez vos règles de thème en CSS natif via `@theme`, vous greffez des extensions de machines via la directive `@plugin`, et vous créez des outils sur mesure via `@utility`. C'est le modèle CSS-first, unifié et instantané.

Ce module présente les mécanismes avancés pour étendre, personnaliser et enrichir Tailwind CSS v4.

<br>

---

## 1. Le Thème CSS-first avec `@theme`

Dans Tailwind v4, vous n'avez plus besoin d'un fichier de configuration JavaScript. La personnalisation du design system se fait directement au sein du fichier CSS principal, dans la directive `@theme`.

### Configurer le thème dans `resources/css/app.css`

```css title="CSS - resources/css/app.css : surcharge et extension du thème"
@import "tailwindcss";

@theme {
  /* Extension et surcharge des couleurs */
  --color-primary-50: #f0fdf4;
  --color-primary-500: #22c55e;
  --color-primary-950: #052e16;

  /* Ajout d'une police display personnalisée */
  --font-display: "Outfit", sans-serif;

  /* Définition d'une animation personnalisée */
  --animate-fade-in-slow: fade-in 1.5s ease-out;

  /* Configuration d'ombres personnalisées */
  --shadow-brand-glow: 0 4px 20px -2px rgba(34, 197, 94, 0.4);
}
```
_Déclaration des variables CSS globales de niveau 4 au sein de la directive @theme pour configurer les couleurs, les polices, les animations et les ombres du design system._

*En déclarant `--color-primary-500`, Tailwind génère automatiquement toutes les classes utilitaires correspondantes : `bg-primary-500`, `text-primary-500`, `border-primary-500`, etc. Les clés CSS-first s'intègrent nativement avec les DevTools du navigateur.*

<br>

---

## 2. Créer des Utilitaires Personnalisés avec `@utility`

Tailwind v4 introduit la directive `@utility` qui permet de déclarer de nouvelles classes utilitaires en écrivant du CSS natif, tout en bénéficiant du moteur de build.

### Déclaration d'utilitaires dans le CSS

```css title="CSS - Définition de classes utilitaires personnalisées"
/* Utilitaire pour tronquer le texte sur plusieurs lignes */
@utility line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Utilitaire de mise en page réutilisable avec media queries */
@utility container-app {
  width: 100%;
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1rem;
  
  @media (min-width: 640px) {
    padding: 0 1.5rem;
  }
  @media (min-width: 1024px) {
    padding: 0 2rem;
  }
}
```
_Enregistrement de nouvelles classes utilitaires réutilisables dans le compilateur Tailwind via la directive CSS @utility._

```html title="HTML - Utilisation des utilitaires personnalisés"
<div class="container-app py-8">
  <p class="line-clamp-2 text-slate-700">
    Ce texte particulièrement long sera limité à deux lignes et automatiquement
    tronqué par des points de suspension, tout en restant responsive grâce au conteneur.
  </p>
</div>
```
_Code HTML tirant parti des classes utilitaires personnalisées définies dans la feuille de style principale._

<br>

---

## 3. Ajout de Plugins Officiels avec `@plugin`

Pour charger des extensions JavaScript complexes (comme le plugin de typographie pour formater le Markdown ou le reset des formulaires), Tailwind v4 utilise la directive `@plugin`.

### Importation de plugins officiels

```css title="CSS - Importation des plugins officiels dans app.css"
@import "tailwindcss";

/* Chargement des plugins officiels */
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
```
_Déclaration des extensions JavaScript officielles de Tailwind directement au sein du fichier CSS principal._

### Exemple d'usage avec le plugin Typography

Le plugin de typographie permet de formater automatiquement du contenu brut (par exemple, du Markdown généré par un éditeur ou extrait d'une base de données) à l'aide de la classe globale `prose`.

```html title="Blade - Utilisation de la classe prose pour afficher du Markdown"
<article class="prose dark:prose-invert max-w-none">
    {!! $page->content !!}
</article>
```
_Rendu structuré automatique du HTML brut ou compilé à l'aide des styles par défaut du plugin Typography._

<br>

---

## 4. DaisyUI v5 — Composants et Thèmes

DaisyUI v5 est entièrement compatible avec Tailwind v4. Il s'importe comme plugin au sein de votre fichier CSS principal et utilise les variables CSS globales pour son système de theming.

### Intégration dans le CSS principal

```css title="CSS - resources/css/app.css : intégration de DaisyUI v5"
@import "tailwindcss";

/* Chargement de DaisyUI v5 */
@plugin "daisyui";

/* Personnalisation des thèmes de DaisyUI via les variables CSS */
@theme {
  --color-primary: var(--color-primary-500);
  --color-secondary: #64748b;
}
```
_Enregistrement de DaisyUI v5 comme extension CSS et liaison des couleurs de composants aux variables globales du thème._

### Exemple de composants DaisyUI v5

```html title="Blade - Boutons et cartes sémantiques DaisyUI"
<!-- Boutons sémantiques combinés avec classes utilitaires -->
<div class="flex gap-4">
    <button class="btn btn-primary">Enregistrer</button>
    <button class="btn btn-outline btn-secondary">Annuler</button>
</div>

<!-- Carte sémantique stylisée avec ombrage et bordures -->
<div class="card bg-base-100 shadow-xl border border-slate-200">
    <div class="card-body p-6">
        <h2 class="card-title text-xl font-bold">DaisyUI v5 & Tailwind v4</h2>
        <p class="text-slate-600">Les deux frameworks fonctionnent en harmonie totale.</p>
        <div class="card-actions justify-end mt-4">
            <button class="btn btn-primary btn-sm">En savoir plus</button>
        </div>
    </div>
</div>
```
_Utilisation des classes de composants prédéfinies de DaisyUI combinées avec la flexibilité des classes utilitaires de Tailwind._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Création d'un Thème Sombre Personnalisé**

1. Dans votre fichier `app.css`, ajoutez des variables pour un thème sombre au sein de `@theme` (ex. `--color-dark-bg`, `--color-dark-text`).
2. Créez un composant de carte qui change de couleur de fond et de couleur de texte en utilisant la variante de média ou la classe active `dark:` (ex: `bg-white dark:bg-dark-bg text-slate-900 dark:text-dark-text`).
3. Validez l'affichage en modifiant les préférences système de votre machine.

**Exercice 2 — Enregistrement d'Utilitaires avec `@utility`**

1. Créez un utilitaire `@utility flex-center` qui applique les propriétés `display: flex`, `align-items: center`, et `justify-content: center`.
2. Utilisez cet utilitaire sur une boîte HTML et validez que le contenu est parfaitement centré horizontalement et verticalement.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La directive `@theme` est l'emplacement unique pour étendre et surcharger le design system sous Tailwind v4, éliminant définitivement `tailwind.config.js`. Pour les petits utilitaires spécifiques, utilisez `@utility` en écrivant du CSS natif. Pour greffer des bibliothèques externes et des fonctionnalités avancées complexes, utilisez `@plugin` (ex. Typography ou DaisyUI v5). Ce modèle unifié en CSS accélère le build et simplifie la maintenance globale du projet.

> **Parcours Tailwind CSS complété.** Vous maîtrisez désormais Tailwind CSS de bout en bout. Poursuivez vers le module d'**[Intégration Laravel 13](./09-integration-laravel13.md)** pour structurer et compiler vos interfaces dans le framework PHP.
