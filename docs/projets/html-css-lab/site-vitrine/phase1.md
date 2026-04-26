---
description: "Phase 1 : Mise en place de l'environnement, architecture des fichiers et fondations du Design System avec les CSS Custom Properties."
icon: lucide/folder-tree
tags: ["CSS", "VARIABLES", "RESET", "ARCHITECTURE"]
status: stable
---

# Phase 1 : Architecture & Design System

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="1 Heure">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le but d'un développeur professionnel n'est pas de coder immédiatement des animations, c'est de bâtir des fondations résilientes. Dans cette première étape, vous allez configurer l'espace de travail, lier vos fichiers et créer la "palette" de votre application web : le **Design System**.

## 1. Structure Physique des Fichiers

Ne sous-estimez jamais l'importance d'une bonne hiérarchie. Dans votre éditeur (ex: VS Code), créez un dossier racine nommé `defi-vitrine-htmlcss`. À l'intérieur, instanciez l'arbre suivant :

```text
defi-vitrine-htmlcss/
├── index.html        (Page d'accueil)
├── services.html     (Page de l'offre)
├── portfolio.html    (Page de la galerie)
├── css/
│   └── style.css     (Feuille de style unique)
└── assets/
    ├── images/       (Vos .jpg, .png, .webp)
    └── icons/        (Vos .svg si applicables)
```

!!! tip "Gagner du temps avec Emmet"
    Ouvrez `index.html`. Tapez `!` (point d'exclamation) sur la première ligne et appuyez sur la touche `Tab`. Votre éditeur va générer instantanément l'en-tête HTML5 parfait (Doctype, Lang, Meta viewport). Cela prouve que vous travaillez _avec_ l'outil, pas _contre_ lui.

N'oubliez pas d'importer votre fichier CSS. Placez la ligne `<link rel="stylesheet" href="./css/style.css">` **avant** la fermeture de la balise `</head>` sur vos 3 pages HTML.

## 2. Le "Reset" CSS Fondamental

Par défaut, tous les navigateurs injectent leurs propres styles (marges autour des titres, marges sur le `<body>`). Un ingénieur Front-End remet toujours les compteurs à zéro pour éviter les "casses" inexpliquées.

Ouvrez votre fichier `css/style.css` et déclarez la règle absolue :

```css
/* 1. Reset Global - Destruction de l'héritage navigateur */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  /* Changement le mode de calcul de l'épaisseur des blocs */
  box-sizing: border-box; 
}

/* 2. Suppression de la marge du corps */
body {
  min-height: 100vh;
  line-height: 1.6;
}

/* 3. Normes pour les éléments textuels et de listes */
ul, ol {
  list-style-type: none; /* Retire les puces des listes */
}

a {
  text-decoration: none; /* Retire le soulignement bleu des liens */
  color: inherit;        /* Le lien prend la couleur de son parent */
}
```

!!! note "L'importance de `box-sizing: border-box`"
    C'est la règle d'Or du CSS moderne. Par défaut, si vous donnez à une `div` une largeur de `200px` et un padding de `20px`, le navigateur va l'afficher à `240px` de large (200 + 20g + 20d). Avec `border-box`, le padding est "absorbé" à l'intérieur de la boîte visuelle : la largeur externe reste bloquée à `200px`. Vous venez d'éviter `90%` des problèmes de débordement d'interface.

## 3. Paramétrer le Design System (CSS Variables)

Une charte graphique bien codée permet une maintenance aisée. Nous allons utiliser la pseudo-classe `:root` du DOM pour stocker nos **Variables CSS natives** (aussi appelées Custom Properties).

Insérez ce bloc tout en haut de votre `style.css` (avant le Reset) :

```css
/* DESIGN SYSTEM DIGITALCRAFT
 * Utilisation des couleurs HSL (Hue, Saturation, Lightness) 
 * Maintien du contraste maximal pour l'accessibilité
 */
:root {
  /* -- Palette de couleurs -- */
  --color-primary: hsl(220, 90%, 56%);    /* Un bleu électrique moderne */
  --color-dark: hsl(220, 20%, 15%);       /* Presque noir, doux pour les yeux */
  --color-light: hsl(0, 0%, 98%);         /* Presque blanc, gris cassé subtil */
  --color-border: hsl(220, 10%, 85%);     /* Gris bordure classique */

  /* -- Typographie (Google Fonts au choix) -- */
  --font-family: 'Inter', system-ui, sans-serif;
  --font-size-base: 16px;

  /* -- Espacements (Spacings proportionnels) -- */
  --spacing-sm: 0.5rem;   /* 8px */
  --spacing-md: 1rem;     /* 16px */
  --spacing-lg: 2rem;     /* 32px */
  --spacing-xl: 4rem;     /* 64px */

  /* -- Décorations (Radiuses, Ombres) -- */
  --radius-md: 8px;
  --shadow-sm: 0 4px 6px rgba(0,0,0,0.05);
}

/* --- Application de l'ADN Visuel au Body --- */
body {
  font-family: var(--font-family);
  background-color: var(--color-light);
  color: var(--color-dark);
}
```

## Checklist de la Phase 1

- [ ] L'arbre de vos fichiers est correct.
- [ ] Le `<link rel="stylesheet">` est bien inséré dans vos 3 entêtes.
- [ ] Le `:root` et le `box-sizing: border-box` sont positionnés dans le CSS.
- [ ] Lorsque vous double-cliquez sur `index.html`, la page est bien vierge, mais l'arrière-plan n'est pas totalement blanc (merci au `hsl(0, 0%, 98%)`).

**Vous venez de construire le ciment de l'application.** C'est dans ce cadre rigide que nous allons désormais bâtir le composant le plus complexe du projet : la Navigation.

[Passer à la Phase 2 : Navbar & Mobile Menu →](phase2.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
