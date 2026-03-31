---
description: "CSS Avancé : variables CSS, filtres, clip-path, blend modes, gradients, container queries, @layer et nesting natif."
icon: lucide/book-open-check
tags: ["CSS", "VARIABLES", "FILTERS", "CLIP-PATH", "BLEND-MODES", "GRADIENTS", "NESTING", "LAYERS"]
---

# CSS Avancé

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="1.1"
  data-time="5-6 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Studio de Post-Production"
    Imaginez un **studio de photographie professionnel** équipé de Photoshop. Le photographe a livré ses clichés bruts : bons techniquement, mais sans vie. En post-production, il applique des filtres de couleur, découpe des silhouettes sur fond transparent, superpose des calques avec des modes de fusion, joue avec des dégradés pour créer une ambiance. L'image finale n'a plus rien à voir avec la photo d'origine — sans qu'un seul pixel réel n'ait changé, seulement la façon de les présenter.

    **CSS Avancé**, c'est ce studio de post-production pour le web : des propriétés qui transforment l'apparence visuelle en temps réel, directement dans le navigateur, sans modifier le HTML ni recourir à des images pré-générées.

Avant 2015, obtenir ces effets exigeait des images PNG ou JPEG statiques, et chaque changement de couleur nécessitait de régénérer les assets. Les propriétés couvertes dans ce module ont changé radicalement le travail frontend.

<br>

---

## Variables CSS (Custom Properties)

Les variables CSS permettent de centraliser les valeurs d'un design system et de créer des thèmes dynamiques.

!!! note "Référence croisée"
    La déclaration dans `:root` et l'utilisation de `var()` ont été introduites dans le [module 02 — Sélecteurs CSS](./02-selecteurs-css.md). Ce module approfondit leur usage dans un design system complet et la gestion du dark mode.

<br>

### Portée et héritage

```css title="CSS - Portée locale et héritage des variables"
/* Portée globale : accessible partout dans le document */
:root {
    --text-color: #1a1a2e;
}

/* Portée locale : la variable n'est accessible qu'au sein de .card */
.card {
    --card-gap: 1.5rem;
    gap: var(--card-gap);
}

/* Valeur de repli (fallback) : utilisée si la variable n'existe pas */
.element {
    color: var(--undefined-var, #333333);
}

/* Fallback chaîné : essaie --primary, sinon --brand-color, sinon #667eea */
.element {
    color: var(--primary, var(--brand-color, #667eea));
}
```

<br>

### Design system complet

```css title="CSS - Jeu de variables pour un design system"
:root {
    /* Couleurs */
    --color-primary:    #667eea;
    --color-secondary:  #764ba2;
    --color-accent:     #f093fb;
    --color-success:    #2ecc71;
    --color-warning:    #f39c12;
    --color-danger:     #e74c3c;

    /* Texte */
    --text-primary:   #1a1a2e;
    --text-secondary: #6b7280;
    --text-muted:     #9ca3af;
    --text-inverse:   #ffffff;

    /* Fonds */
    --bg-page:   #ffffff;
    --bg-card:   #f8fafc;
    --bg-dark:   #1a1a2e;

    /* Espacement */
    --space-xs:  0.25rem;  /*  4 px */
    --space-sm:  0.5rem;   /*  8 px */
    --space-md:  1rem;     /* 16 px */
    --space-lg:  1.5rem;   /* 24 px */
    --space-xl:  2rem;     /* 32 px */
    --space-2xl: 3rem;     /* 48 px */
    --space-3xl: 4rem;     /* 64 px */

    /* Typographie */
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;

    --fs-xs:   0.75rem;
    --fs-sm:   0.875rem;
    --fs-base: 1rem;
    --fs-lg:   1.125rem;
    --fs-xl:   1.25rem;
    --fs-2xl:  1.5rem;
    --fs-3xl:  2rem;
    --fs-4xl:  2.5rem;

    /* Bordures */
    --radius-sm:   4px;
    --radius-md:   8px;
    --radius-lg:   12px;
    --radius-xl:   16px;
    --radius-full: 9999px;

    /* Ombres */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.10);
    --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.12);
    --shadow-xl: 0 20px 48px rgba(0, 0, 0, 0.16);

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --transition-slow: 400ms ease;

    /* Z-index */
    --z-base:    1;
    --z-menu:    100;
    --z-sticky:  200;
    --z-modal:   500;
    --z-tooltip: 700;
}
```

*Modifier `--color-primary` dans `:root` répercute le changement sur tous les boutons, liens, badges et éléments d'accent du site en une seule ligne — c'est la puissance d'un token system.*

<br>

### Thème sombre avec `prefers-color-scheme`

```css title="CSS - Dark mode automatique sans JavaScript"
/* Thème clair par défaut */
:root {
    --bg-page:    #ffffff;
    --bg-card:    #f8fafc;
    --text-main:  #1a1a2e;
    --text-muted: #6b7280;
    --border:     #e5e7eb;
}

/* Thème sombre : activé automatiquement par la préférence système */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-page:    #0f0f1a;
        --bg-card:    #1a1a2e;
        --text-main:  #e2e8f0;
        --text-muted: #94a3b8;
        --border:     #2d3748;
    }
}

/* L'attribut data-theme permet un basculement manuel via JavaScript */
[data-theme="dark"] {
    --bg-page:    #0f0f1a;
    --bg-card:    #1a1a2e;
    --text-main:  #e2e8f0;
    --text-muted: #94a3b8;
    --border:     #2d3748;
}

/* Application : tous les éléments lisent automatiquement la bonne variable */
body {
    background-color: var(--bg-page);
    color: var(--text-main);
    font-family: var(--font-sans);
}

.card {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
}
```

*Le basculement de thème via `prefers-color-scheme` est entièrement automatique — le navigateur lit la préférence système et active les bonnes variables. Aucun JavaScript n'est nécessaire pour le comportement de base.*

<br>

### Variables et `calc()`

```css title="CSS - Calculs dynamiques avec variables CSS"
:root {
    --space-unit: 8px;   /* Unité de base */
    --scale: 1.5;        /* Facteur d'échelle typographique */
    --fs-base: 1rem;
}

/* Espacement systématique */
.mb-1 { margin-bottom: calc(var(--space-unit) * 1); }   /*  8 px */
.mb-2 { margin-bottom: calc(var(--space-unit) * 2); }   /* 16 px */
.mb-3 { margin-bottom: calc(var(--space-unit) * 3); }   /* 24 px */

/* Échelle typographique */
.text-sm { font-size: calc(var(--fs-base) / var(--scale)); }
.text-lg { font-size: calc(var(--fs-base) * var(--scale)); }
.text-xl { font-size: calc(var(--fs-base) * var(--scale) * var(--scale)); }
```

<br>

---

## CSS Filters

Les filtres CSS appliquent des traitements visuels à un élément et à son contenu — comme Photoshop, mais dans le navigateur en temps réel.

<br>

### Les filtres disponibles

```css title="CSS - Les neuf filtres CSS avec leurs valeurs"
/* blur() : flou gaussien */
.element { filter: blur(5px); }

/* brightness() : luminosité */
.element { filter: brightness(0.5); }  /* 50 % : assombri */
.element { filter: brightness(1.5); }  /* 150 % : éclairci */

/* contrast() : contraste */
.element { filter: contrast(0.5); }
.element { filter: contrast(2); }

/* grayscale() : niveau de gris */
.element { filter: grayscale(0); }   /* Couleur normale */
.element { filter: grayscale(1); }   /* Noir et blanc */

/* saturate() : saturation */
.element { filter: saturate(0); }   /* Désaturé */
.element { filter: saturate(3); }   /* Très saturé */

/* hue-rotate() : rotation de teinte sur la roue chromatique */
.element { filter: hue-rotate(90deg); }

/* invert() : inversion des couleurs (effet négatif photo) */
.element { filter: invert(1); }

/* sepia() : effet vintage */
.element { filter: sepia(1); }

/* opacity() : transparence */
.element { filter: opacity(0.5); }
```

<br>

### Composer les filtres

```css title="CSS - Composition de filtres pour des effets photo"
/* Photo vintage : sépia léger + contraste + luminosité */
.vintage {
    filter: sepia(0.4) contrast(1.1) brightness(1.1) saturate(0.9);
}

/* Image désaturée qui reprend ses couleurs au survol */
.portfolio-img {
    filter: grayscale(0.8) brightness(0.9);
    transition: filter 0.4s ease;
}

.portfolio-img:hover {
    filter: grayscale(0) brightness(1);
}

/* Adaptation des images en dark mode */
@media (prefers-color-scheme: dark) {
    img:not([role="icon"]) {
        filter: brightness(0.85) contrast(1.1);
    }
}
```

<br>

### `backdrop-filter` — le glassmorphism

`backdrop-filter` applique un filtre au **fond visible derrière l'élément**, pas à l'élément lui-même. C'est la propriété clé du glassmorphism.

```css title="CSS - Glassmorphism avec backdrop-filter"
/* Carte de verre */
.glass-card {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-lg);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Navigation fixe translucide */
.site-header {
    position: sticky;
    top: 0;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px) saturate(200%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

/* Version dark mode */
@media (prefers-color-scheme: dark) {
    .glass-card {
        background: rgba(15, 15, 26, 0.6);
        border-color: rgba(255, 255, 255, 0.08);
    }
}
```

!!! info "Support navigateurs et fallback"
    `backdrop-filter` est supporté par Chrome 76+, Safari 9+, Firefox 103+, Edge 79+. Pour les navigateurs sans support, utilisez `@supports` :

    ```css title="CSS - Fallback avec @supports"
    @supports not (backdrop-filter: blur(10px)) {
        .glass-card {
            background: rgba(255, 255, 255, 0.95); /* Fond opaque en repli */
        }
    }
    ```

<br>

---

## Clip-path

`clip-path` découpe un élément selon une forme géométrique. Tout ce qui est hors de la forme est invisible.

<br>

### Les formes disponibles

```css title="CSS - Les quatre fonctions clip-path"
/* circle() : cercle */
.avatar      { clip-path: circle(50%); }
.avatar-sm   { clip-path: circle(40% at 50% 50%); }

/* ellipse() : ellipse */
.element { clip-path: ellipse(60% 40%); }

/* inset() : rectangle avec rognage et coins optionnels */
.element { clip-path: inset(10px 20px); }
.element { clip-path: inset(10px round 8px); }

/* polygon() : forme libre par coordonnées X Y */
.triangle {
    clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
}

.hexagon {
    clip-path: polygon(
        25% 0%,  75% 0%,
        100% 50%,
        75% 100%, 25% 100%,
        0% 50%
    );
}

.chevron {
    clip-path: polygon(
        0 0, 75% 0, 100% 50%,
        75% 100%, 0 100%, 25% 50%
    );
}
```

!!! tip "Générateur visuel"
    [bennettfeely.com/clippy](https://bennettfeely.com/clippy) permet de créer visuellement des polygones et de copier le code CSS généré.

<br>

### Animer `clip-path`

```css title="CSS - Transitions et révélations avec clip-path"
/* Révélation circulaire depuis le centre */
@keyframes reveal-circle {
    from { clip-path: circle(0% at 50% 50%); }
    to   { clip-path: circle(100% at 50% 50%); }
}

.reveal {
    animation: reveal-circle 0.8s ease-out forwards;
}

/* Glissement depuis la gauche */
@keyframes slide-reveal {
    from { clip-path: inset(0 100% 0 0); }
    to   { clip-path: inset(0 0% 0 0); }
}

.slide-in {
    animation: slide-reveal 0.6s ease-out forwards;
}
```

*Les deux clip-path à animer doivent utiliser la même fonction (les deux `circle`, ou les deux `inset`). Les fonctions différentes ne peuvent pas être interpolées.*

<br>

---

## Blend Modes

Les blend modes définissent comment un élément se fond visuellement avec ce qui est derrière lui — à l'image des modes de fusion Photoshop.

```css title="CSS - mix-blend-mode et background-blend-mode"
/* mix-blend-mode : fusion entre l'élément et son arrière-plan */
.element { mix-blend-mode: multiply; }   /* Multiplication des channels */
.element { mix-blend-mode: screen; }     /* Inverse du multiply, éclaircit */
.element { mix-blend-mode: overlay; }    /* Combine multiply et screen */
.element { mix-blend-mode: darken; }     /* Conserve les pixels les plus sombres */
.element { mix-blend-mode: lighten; }    /* Conserve les pixels les plus clairs */
.element { mix-blend-mode: difference; } /* Soustraction absolue */
.element { mix-blend-mode: color; }      /* Applique la teinte de l'élément */
.element { mix-blend-mode: luminosity; } /* Applique la luminosité de l'élément */

/* Texte blanc fusionné avec un fond dégradé */
.hero-title {
    color: #ffffff;
    mix-blend-mode: overlay;
}

/* background-blend-mode : fusion entre background-image et background-color */
.section-teintee {
    background-image: url('texture.jpg');
    background-color: #667eea;
    background-blend-mode: multiply;
    /* La texture est teintée par la couleur primaire */
}
```

<br>

---

## Gradients

<br>

### `linear-gradient`

```css title="CSS - Dégradés linéaires"
/* Dégradé simple */
.element { background: linear-gradient(#667eea, #764ba2); }

/* Direction explicite */
.element { background: linear-gradient(to right, #667eea, #764ba2); }
.element { background: linear-gradient(45deg, #667eea, #764ba2); }

/* Multi-couleurs avec positions */
.element {
    background: linear-gradient(
        135deg,
        #667eea 0%,
        #764ba2 50%,
        #f093fb 100%
    );
}
```

<br>

### `radial-gradient` et `conic-gradient`

```css title="CSS - Dégradés radiaux et coniques"
/* Dégradé radial depuis le centre */
.element { background: radial-gradient(circle, #667eea 0%, #764ba2 100%); }
.element { background: radial-gradient(ellipse at top left, #667eea, #764ba2); }

/* Dégradé conique — roue chromatique */
.element { background: conic-gradient(#667eea, #764ba2, #f093fb, #667eea); }

/* Graphique en secteurs 100% CSS */
.pie-chart {
    border-radius: 50%;
    background: conic-gradient(
        #667eea  0%  35%,   /* 35 % */
        #764ba2 35%  60%,   /* 25 % */
        #f093fb 60% 100%    /* 40 % */
    );
}
```

<br>

### Mesh gradient

```css title="CSS - Mesh gradient avec radial-gradient superposés"
/* Plusieurs radial-gradient empilés créent des taches de couleur lumineuses */
.hero {
    background-color: #0f0f1a;
    background-image:
        radial-gradient(ellipse 80% 80% at 20% 20%, rgba(102, 126, 234, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse 80% 80% at 80% 80%, rgba(118, 75, 162, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse 60% 60% at 60% 20%, rgba(240, 147, 251, 0.3) 0%, transparent 50%);
}
```

*Ce pattern "mesh gradient" est très utilisé depuis 2023 pour les sections hero. Il est léger, 100% CSS, et ne nécessite aucune image externe.*

<br>

---

## Container Queries

!!! note "Référence croisée"
    Les unités `cqw` et `cqh` ont été introduites dans le [module 03 — Unités de Mesures](./03-unites-mesures-css.md). Ce module présente la syntaxe `@container` complète pour les styles conditionnels.

```css title="CSS - Composant auto-adaptatif avec @container"
/* 1. Déclarer le contexte de conteneur sur le parent */
.card-wrapper {
    container-type: inline-size;
    container-name: card;
}

/* 2. Styles par défaut : layout vertical pour les petits conteneurs */
.card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* 3. Styles conditionnels quand le CONTENEUR fait au moins 400px */
@container card (min-width: 400px) {
    .card {
        flex-direction: row;
        align-items: center;
    }

    .card-image {
        width: 120px;
        flex-shrink: 0;
    }
}
```

*Le même composant `.card` s'affiche différemment dans une sidebar de 300px ou une zone principale de 800px — sans media query sur le viewport. C'est la puissance des container queries pour les architectures de composants.*

<br>

---

## `@layer` — Couches de cascade

`@layer` résout les conflits de spécificité en organisant les styles en couches ordonnées. La couche déclarée en dernier est la plus prioritaire.

```css title="CSS - Organisation des styles en couches"
/* Déclaration de l'ordre des couches */
@layer reset, base, components, utilities;

/* Les styles dans une couche plus prioritaire gagnent,
   quelle que soit leur spécificité CSS interne */

@layer reset {
    *,
    *::before,
    *::after {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
}

@layer base {
    body {
        font-family: var(--font-sans);
        color: var(--text-primary);
    }
}

@layer components {
    .btn {
        padding: 0.75rem 1.5rem;
        border-radius: var(--radius-md);
    }
}

/* Les utilities surclassent les composants grâce à l'ordre des couches,
   pas grâce à une spécificité plus élevée */
@layer utilities {
    .text-center { text-align: center; }
    .hidden      { display: none; }
}
```

*`@layer` est particulièrement utile pour intégrer des bibliothèques CSS tierces dans une couche de faible priorité, puis les surcharger facilement depuis votre couche `components` ou `utilities` sans `!important`.*

<br>

---

## CSS Nesting — Imbrication native

Le Nesting permet d'écrire des règles CSS hiérarchiquement. Fonctionnalité phare de SCSS pendant des années, elle est désormais **native dans le langage CSS** depuis fin 2023.

<br>

### Syntaxe de base

```css title="CSS - Nesting natif vs ancienne écriture répétitive"
/* AVANT : répétition constante du sélecteur parent */
.card             { background: white; padding: 1rem; }
.card .title      { font-size: 1.5rem; }
.card .title span { color: var(--color-primary); }

/* AUJOURD'HUI : imbrication logique */
.card {
    background: white;
    padding: 1rem;

    .title {
        font-size: 1.5rem;

        span {
            color: var(--color-primary);
        }
    }
}
```

<br>

### Le sélecteur parent `&`

Le symbole `&` référence le sélecteur parent courant. Il est indispensable pour enchaîner les pseudo-classes, les modificateurs d'état et les sélecteurs frères.

```css title="CSS - Nesting avancé avec le symbole &"
.btn {
    background: var(--color-primary);
    color: white;

    /* .btn:hover */
    &:hover {
        background: var(--color-secondary);
        transform: translateY(-2px);
    }

    /* .btn.is-active */
    &.is-active {
        box-shadow: 0 0 0 2px var(--color-accent);
    }

    /* Bouton immédiatement suivi d'un autre bouton */
    & + & {
        margin-left: 1rem;
    }
}

/* Nesting avec media queries */
.hero {
    font-size: 2rem;
    padding: 2rem;

    @media (max-width: 768px) {
        font-size: 1.5rem;
        padding: 1rem;
    }
}
```

*Le nesting natif permet au CSS de refléter directement la structure hiérarchique du HTML. Il supprime la charge cognitive de lecture des feuilles de style longues et réduit le besoin de préprocesseurs comme SCSS sur les nouveaux projets.*

!!! info "Support navigateurs"
    Le Nesting CSS natif est disponible dans Chrome 112+, Firefox 117+, Safari 17.2+, Edge 112+. En 2025, le support dépasse 92% des utilisateurs mondiaux.

<br>

---

## Tableau récapitulatif

| Propriété / Technique | Usage principal |
| --- | --- |
| `--var` / `var()` | Design system centralisé, thèmes, dark mode |
| `filter` | Effets photo, hover désaturation |
| `backdrop-filter` | Glassmorphism, navigation translucide |
| `clip-path` | Formes décoratives, révélations animées |
| `mix-blend-mode` | Fusion de calques, effets graphiques |
| `linear-gradient` | Fonds, overlays, boutons dégradés |
| `conic-gradient` | Graphiques, effets coniques |
| `@container` | Composants auto-adaptatifs |
| `@layer` | Organisation et priorité de la cascade |
| Nesting (`&`) | Hiérarchie lisible sans SCSS |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les **variables CSS** centralisent votre design system et permettent le dark mode sans JavaScript. Les **filtres** (`blur`, `grayscale`, `brightness`, `backdrop-filter`) ouvrent la porte au glassmorphism et aux traitements d'images dynamiques. **Clip-path**, **blend modes** et **gradients** donnent au CSS un pouvoir graphique autrefois réservé à Photoshop. `@layer` organise la cascade sans guerre de spécificité. Le **Nesting natif** remplace SCSS pour la majorité des projets modernes.

> Dans le module suivant, nous explorerons les ressources et approfondissements pour **aller plus loin** : outils de design, ressources communautaires, et pratiques avancées de l'industrie CSS en 2025.

<br>