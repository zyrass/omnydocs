---
description: "CSS Avancé : variables CSS, filtres, clip-path, blend modes, masques, gradients, container queries, sélecteurs modernes"
icon: lucide/book-open-check
tags: ["CSS", "VARIABLES", "FILTERS", "CLIP-PATH", "BLEND-MODES", "GRADIENTS", "CONTAINER-QUERIES"]
---

# CSS Avancé

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="1.1"
  data-time="5-6 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    _Imaginez un **studio de photographie professionnel** équipé de Photoshop. Le photographe a livré ses clichés bruts : bons techniquement, mais sans vie. En post-production, il applique des filtres de couleur, découpe des silhouettes sur fond transparent, superpose des calques avec des modes de fusion, joue avec des dégradés pour créer une ambiance. L'image finale n'a plus rien à voir avec la photo d'origine — et pourtant aucun pixel réel n'a changé, seulement la façon de les présenter. **CSS Avancé**, c'est ce studio de post-production pour le web : des propriétés qui transforment l'apparence visuelle en temps réel, directement dans le navigateur, sans modifier le HTML ni recourir à des images pré-générées._

Avant 2015, obtenir ces effets en CSS était impossible : on utilisait des images PNG ou JPEG pour les formes, des images avec calque pour les effets de transparence, et un renouvellement complet des assets à chaque changement de couleur. Les propriétés couvertes dans ce module ont changé radicalement le travail frontend :

- **Variables CSS** — un seul endroit pour piloter l'ensemble d'un design system
- **Filtres** — effets Photoshop appliqués à n'importe quel élément HTML
- **Clip-path** — découpes vectorielles sans images
- **Blend modes** — fusion de calques
- **Gradients** — dégradés complexes et dynamiques
- **Container queries** — responsive par composant (CSS 2023)

---

## Variables CSS (Custom Properties)

Les variables CSS sont des propriétés personnalisées réutilisables dans toute la feuille de style. Elles permettent de centraliser les valeurs d'un design system et de créer des thèmes dynamiques.

### Déclaration et utilisation

```css title="CSS — Syntaxe des variables CSS"
/* Déclaration dans :root (portée globale) */
:root {
    --color-primary: #667eea;
    --spacing-base: 1rem;
    --radius-card: 8px;
}

/* Utilisation avec var() */
.button {
    background-color: var(--color-primary);
    padding: var(--spacing-base) calc(var(--spacing-base) * 2);
    border-radius: var(--radius-card);
}
```

_`var()` lit la valeur de la variable au moment du rendu. Si la variable est modifiée (en CSS ou via un attribut data), tous les éléments qui l'utilisent se mettent à jour instantanément._

```css title="CSS — Valeur de repli (fallback)"
.element {
    /* Si --undefined-var n'existe pas, utilise #333333 */
    color: var(--undefined-var, #333333);
}

/* Fallback chaîné */
.element {
    color: var(--primary, var(--brand-color, #667eea));
    /* Essaie --primary, sinon --brand-color, sinon #667eea */
}
```

### Portée et héritage

```css title="CSS — Portée locale d'une variable"
/* Portée globale */
:root {
    --text-color: #1a1a2e;
}

/* Portée locale : la variable n'est accessible qu'au sein de .card */
.card {
    --card-gap: 1.5rem;
    gap: var(--card-gap);
}

/* Héritage : les enfants accèdent aux variables du parent */
.section {
    --section-padding: 4rem;
}

.section .inner {
    padding: var(--section-padding); /* Hérite de .section */
}
```

_Les variables CSS suivent la cascade et l'héritage CSS : elles peuvent être redéfinies localement pour un composant sans affecter les autres._

### Design system complet

```css title="CSS — Variables d'un design system"
:root {
    /* ── Couleurs ─────────────────────────────────── */
    --color-primary:    #667eea;
    --color-secondary:  #764ba2;
    --color-accent:     #f093fb;
    --color-success:    #2ecc71;
    --color-warning:    #f39c12;
    --color-danger:     #e74c3c;

    /* ── Texte ───────────────────────────────────── */
    --text-primary:   #1a1a2e;
    --text-secondary: #6b7280;
    --text-muted:     #9ca3af;
    --text-inverse:   #ffffff;

    /* ── Fonds ───────────────────────────────────── */
    --bg-page:   #ffffff;
    --bg-card:   #f8fafc;
    --bg-dark:   #1a1a2e;

    /* ── Espacement ──────────────────────────────── */
    --space-xs:  0.25rem;  /*  4 px */
    --space-sm:  0.5rem;   /*  8 px */
    --space-md:  1rem;     /* 16 px */
    --space-lg:  1.5rem;   /* 24 px */
    --space-xl:  2rem;     /* 32 px */
    --space-2xl: 3rem;     /* 48 px */
    --space-3xl: 4rem;     /* 64 px */

    /* ── Typographie ─────────────────────────────── */
    --font-sans:  'Inter', system-ui, sans-serif;
    --font-mono:  'JetBrains Mono', monospace;

    --fs-xs:   0.75rem;
    --fs-sm:   0.875rem;
    --fs-base: 1rem;
    --fs-lg:   1.125rem;
    --fs-xl:   1.25rem;
    --fs-2xl:  1.5rem;
    --fs-3xl:  2rem;
    --fs-4xl:  2.5rem;

    /* ── Bordures ────────────────────────────────── */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-full: 9999px;

    /* ── Ombres ──────────────────────────────────── */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.10);
    --shadow-lg: 0 10px 24px rgba(0, 0, 0, 0.12);
    --shadow-xl: 0 20px 48px rgba(0, 0, 0, 0.16);

    /* ── Transitions ─────────────────────────────── */
    --transition-fast: 150ms ease;
    --transition-base: 250ms ease;
    --transition-slow: 400ms ease;

    /* ── Z-index ─────────────────────────────────── */
    --z-base:    1;
    --z-menu:    100;
    --z-sticky:  200;
    --z-modal:   500;
    --z-tooltip: 700;
}
```

_Ce jeu de variables fait office de **token system** : changer `--color-primary` répercute la modification sur tous les boutons, liens, badges et éléments d'accent du site en une seule ligne._

### Thème sombre avec prefers-color-scheme

```css title="CSS — Dark mode automatique sans JavaScript"
/* Thème clair (défaut) */
:root {
    --bg-page:    #ffffff;
    --bg-card:    #f8fafc;
    --text-main:  #1a1a2e;
    --text-muted: #6b7280;
    --border:     #e5e7eb;
}

/* Thème sombre : activé par la préférence système */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-page:    #0f0f1a;
        --bg-card:    #1a1a2e;
        --text-main:  #e2e8f0;
        --text-muted: #94a3b8;
        --border:     #2d3748;
    }
}

/* L'attribut data-theme permet un basculement manuel */
[data-theme="dark"] {
    --bg-page:    #0f0f1a;
    --bg-card:    #1a1a2e;
    --text-main:  #e2e8f0;
    --text-muted: #94a3b8;
    --border:     #2d3748;
}

/* Application */
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

_Le basculement de thème via `prefers-color-scheme` est entièrement automatique : le navigateur lit la préférence système et active les bonnes variables. Aucun JavaScript n'est nécessaire pour le comportement de base._

### Variables avec calc()

```css title="CSS — Calculs dynamiques avec variables"
:root {
    --space-unit: 8px;   /* Unité de base */
    --scale: 1.5;        /* Facteur d'échelle typographique */
    --fs-base: 1rem;
}

/* Espacement systématique */
.mb-1 { margin-bottom: calc(var(--space-unit) * 1); }   /*  8 px */
.mb-2 { margin-bottom: calc(var(--space-unit) * 2); }   /* 16 px */
.mb-3 { margin-bottom: calc(var(--space-unit) * 3); }   /* 24 px */
.mb-4 { margin-bottom: calc(var(--space-unit) * 4); }   /* 32 px */

/* Échelle typographique */
.text-sm  { font-size: calc(var(--fs-base) / var(--scale)); }       /* 0.67 rem */
.text-lg  { font-size: calc(var(--fs-base) * var(--scale)); }        /* 1.5 rem */
.text-xl  { font-size: calc(var(--fs-base) * var(--scale) * var(--scale)); } /* 2.25 rem */
```

---

## CSS Filters

Les filtres CSS appliquent des traitements visuels à un élément et à son contenu, comme Photoshop mais dans le navigateur.

### Filtres disponibles

```css title="CSS — Les 9 filtres CSS avec leurs valeurs"
/* blur() : flou gaussien */
.element { filter: blur(5px); }  /* 0 = pas de flou */

/* brightness() : luminosité */
.element { filter: brightness(0.5); } /* 50 % : sombre */
.element { filter: brightness(1.5); } /* 150 % : clair */

/* contrast() : contraste */
.element { filter: contrast(0.5); } /* Contraste réduit */
.element { filter: contrast(2); }   /* Contraste élevé */

/* grayscale() : niveau de gris */
.element { filter: grayscale(0); }    /* Couleur normale */
.element { filter: grayscale(1); }    /* Noir et blanc complet */

/* saturate() : saturation */
.element { filter: saturate(0); }  /* Désaturé = grayscale */
.element { filter: saturate(3); }  /* Couleurs très vives */

/* hue-rotate() : rotation de teinte */
.element { filter: hue-rotate(90deg); }  /* Décalage de la roue chromatique */

/* invert() : inversion des couleurs */
.element { filter: invert(1); }  /* Négatif photo */

/* sepia() : effet sépia (vintage) */
.element { filter: sepia(1); }  /* 100 % sépia */

/* opacity() : transparence (= propriété opacity) */
.element { filter: opacity(0.5); }
```

### Combiner les filtres

```css title="CSS — Composition de filtres"
/* Plusieurs filtres s'enchaînent (de gauche à droite) */

/* Photo vintage */
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

/* Ajustement dark mode pour les images */
@media (prefers-color-scheme: dark) {
    img:not([role="icon"]) {
        filter: brightness(0.85) contrast(1.1);
    }
}
```

### backdrop-filter — effet glassmorphism

`backdrop-filter` applique un filtre **au fond visible derrière l'élément**, pas à l'élément lui-même. C'est la propriété clé du glassmorphism.

```css title="CSS — Glassmorphism avec backdrop-filter"
/* Carte de verre */
.glass-card {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-lg);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Navigation fixe avec effet de verre */
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

    .site-header {
        background: rgba(15, 15, 26, 0.75);
    }
}
```

!!! note "Support navigateurs"
    `backdrop-filter` est supporté par Chrome 76+, Safari 9+, Firefox 103+, Edge 79+. Pour les navigateurs qui ne le supportent pas, utilisez `@supports` :

    ```css
    @supports not (backdrop-filter: blur(10px)) {
        .glass-card {
            background: rgba(255, 255, 255, 0.95); /* Fond opaque en fallback */
        }
    }
    ```

---

## Clip-path

`clip-path` découpe un élément selon une forme géométrique. Tout ce qui est hors de la forme est invisible.

### Formes disponibles

```css title="CSS — Clip-path : les quatre fonctions de base"
/* circle() : cercle */
.avatar {
    clip-path: circle(50%);        /* Cercle parfait */
    clip-path: circle(40% at 50% 50%); /* Rayon 40 %, centré */
}

/* ellipse() : ellipse */
.element {
    clip-path: ellipse(60% 40%); /* Rayon X: 60 %, Y: 40 % */
}

/* inset() : rectangle avec coins optionnellement arrondis */
.element {
    clip-path: inset(10px 20px);          /* Rognage haut/bas: 10px, gauche/droite: 20px */
    clip-path: inset(10px round 8px);     /* Rognage + coins arrondis */
}

/* polygon() : forme libre par coordonnées X Y */
.triangle {
    clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
    /* Sommet haut-centre, bas-droite, bas-gauche */
}

.hexagon {
    clip-path: polygon(
        25% 0%, 75% 0%,
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

!!! tip "Générateur clip-path"
    Le site [bennettfeely.com/clippy](https://bennettfeely.com/clippy) permet de créer visuellement des polygones et de copier le code CSS généré.

### Animations de clip-path

```css title="CSS — Transitions entre formes clip-path"
/* Révélation circulaire */
@keyframes reveal-circle {
    from { clip-path: circle(0% at 50% 50%); }
    to   { clip-path: circle(100% at 50% 50%); }
}

.reveal {
    animation: reveal-circle 0.8s ease-out forwards;
}

/* Slide depuis la gauche */
@keyframes slide-reveal {
    from { clip-path: inset(0 100% 0 0); }
    to   { clip-path: inset(0 0% 0 0); }
}

.slide-in {
    animation: slide-reveal 0.6s ease-out forwards;
}

/* Important : les deux clip-path doivent utiliser la même fonction pour être animables */
```

---

## Blend Modes

Les blend modes définissent comment un élément se fond visuellement avec ce qui est derrière lui, à l'image des modes de fusion de Photoshop.

```css title="CSS — mix-blend-mode et background-blend-mode"
/* mix-blend-mode : fusion entre l'élément et son arrière-plan */
.element {
    mix-blend-mode: multiply;  /* Multiplication des channels couleur */
    mix-blend-mode: screen;    /* Inverse du multiply, éclaircit */
    mix-blend-mode: overlay;   /* Combine multiply et screen */
    mix-blend-mode: darken;    /* Conserve les pixels les plus sombres */
    mix-blend-mode: lighten;   /* Conserve les pixels les plus clairs */
    mix-blend-mode: difference;/* Soustraction absolue (effet négatif partiel) */
    mix-blend-mode: color;     /* Applique la teinte de l'élément */
    mix-blend-mode: luminosity;/* Applique la luminosité de l'élément */
}

/* Exemple : texte qui se fusionne avec une image de fond */
.hero-title {
    color: #ffffff;
    mix-blend-mode: overlay;
    /* Le texte blanc s'intègre visuellement au gradient de fond */
}

/* background-blend-mode : fusion entre background-image et background-color */
.section {
    background-image: url('texture.jpg');
    background-color: #667eea;
    background-blend-mode: multiply;
    /* La texture est teintée par la couleur primaire */
}
```

---

## Gradients

### linear-gradient

```css title="CSS — Gradients linéaires"
/* Dégradé simple : de gauche à droite (défaut) */
.element {
    background: linear-gradient(#667eea, #764ba2);
}

/* Direction en degrés ou mots-clés */
.element {
    background: linear-gradient(to right, #667eea, #764ba2);
    background: linear-gradient(45deg, #667eea, #764ba2);
    background: linear-gradient(135deg, #667eea, #764ba2);
}

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

### radial-gradient et conic-gradient

```css title="CSS — Gradients radiaux et coniques"
/* Dégradé radial : du centre vers l'extérieur */
.element {
    background: radial-gradient(circle, #667eea 0%, #764ba2 100%);
    background: radial-gradient(ellipse at top left, #667eea, #764ba2);
}

/* Dégradé conique (roue chromatique, graphiques en secteurs) */
.element {
    background: conic-gradient(#667eea, #764ba2, #f093fb, #667eea);
}

/* Graphique en secteurs CSS */
.pie-chart {
    border-radius: 50%;
    background: conic-gradient(
        #667eea  0%   35%,   /* 35 % : Premier secteur */
        #764ba2  35%  60%,   /* 25 % : Deuxième secteur */
        #f093fb  60%  100%   /* 40 % : Troisième secteur */
    );
}
```

### Mesh gradient (tendance 2024-2026)

```css title="CSS — Mesh gradient avec radial-gradient superposés"
.hero {
    background-color: #0f0f1a;
    background-image:
        radial-gradient(ellipse 80% 80% at 20% 20%, rgba(102, 126, 234, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse 80% 80% at 80% 80%, rgba(118, 75, 162, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse 60% 60% at 60% 20%, rgba(240, 147, 251, 0.3) 0%, transparent 50%);
}
```

_Plusieurs `radial-gradient` superposés créent un effet de "taches de couleur" (mesh gradient) très tendance depuis 2023. Ils sont légers et 100 % CSS._

---

## Container Queries

!!! info "CSS 2023 — support navigateurs"
    Les container queries sont disponibles dans Chrome 105+, Firefox 110+, Safari 16+, Edge 105+. Ils remplacent avantageusement les media queries pour les composants réutilisables.

Les container queries permettent de conditionner les styles à la taille du **conteneur direct** de l'élément, plutôt qu'à celle du viewport.

```css title="CSS — Container queries : composant auto-adaptatif"
/* 1. Déclarer un conteneur */
.card-wrapper {
    container-type: inline-size; /* Active le container query sur la largeur */
    container-name: card;        /* Nom optionnel mais pratique */
}

/* 2. Styles conditionnels selon la largeur du conteneur */

/* Par défaut : layout vertical (petite taille) */
.card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Quand le conteneur fait au moins 400 px de large */
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

_Le même composant `.card` s'affichera différemment selon qu'il est dans une sidebar de 300 px ou une zone principale de 800 px — sans media query sur le viewport._

---

## Sélecteurs CSS modernes

### :is(), :where() et :has()

```css title="CSS — Sélecteurs de niveau 4"
/* :is() : groupe de sélecteurs avec poids CSS normal */
:is(h1, h2, h3, h4) {
    line-height: 1.2;
    font-weight: 700;
}

/* Equivalent à h1, h2, h3, h4 { … } mais plus lisible */

/* :where() : identique à :is() mais avec spécificité 0  */
:where(h1, h2, h3) {
    margin-bottom: 1rem;
}

/* :has() : sélectionne un parent selon son contenu */
/* Sélectionne .card qui CONTIENT un élément img */
.card:has(img) {
    padding: 0;
}

/* Sélectionne .form-group dont l'input est invalide */
.form-group:has(input:invalid) {
    color: var(--color-danger);
}
```

!!! note "Compatibilité :has()"
    `:has()` est supporté dans Chrome 105+, Safari 15.4+, Firefox 121+. C'est le sélecteur le plus puissant jamais ajouté à CSS — il permet des logiques qui nécessitaient auparavant JavaScript.

### @layer — couches de cascade

```css title="CSS — Gestion des couches de cascade"
/* Déclarer les couches dans l'ordre de priorité voulue */
@layer reset, base, components, utilities;

@layer reset {
    * { margin: 0; padding: 0; box-sizing: border-box; }
}

@layer base {
    body { font-family: var(--font-sans); color: var(--text-primary); }
}

@layer components {
    .btn { /* styles du bouton */ }
}

@layer utilities {
    .text-center { text-align: center; }
    .hidden { display: none; }
}

/* Les utility classes surclassent les composants, les composants surclassent la base */
```

_`@layer` résout les conflits de spécificité par ordre de déclaration des couches. Les styles dans une couche de priorité supérieure gagnent, quelle que soit leur spécificité CSS._

---

## CSS Nesting (Imbrication native)

L'imbrication (Nesting) permet d'écrire des règles CSS de manière hiérarchique. Historiquement, cette fonctionnalité extrêmement plébiscitée nécessitait l'installation d'un préprocesseur comme **SCSS** (Sass) ou **Less**. Depuis fin 2023, c'est **une fonctionnalité complètement native dans le langage CSS3** !

### Syntaxe de base

```css title="CSS — Imbrication basique"
/* Avant : la répétition constante du sélecteur parent était obligatoire */
.card { background: white; padding: 1rem; }
.card .title { font-size: 1.5rem; }
.card .title span { color: var(--color-primary); }

/* Aujourd'hui, on imbrique logiquement la cascade : Le Nesting natif ! */
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

### Le sélecteur parent référent `&`

Le symbole `&` référence le parent de la portée d'imbrication actuelle. Il est vital pour enchaîner les fameuses pseudo-classes (`:hover`), concaténer des modificateurs d'état ou pointer la fraterie.

```css title="CSS — Nesting avancé avec le symbole &"
.btn {
    background: var(--color-primary);
    color: white;
    
    /* Vise le hover DIRECTEMENT rattaché au parent ".btn:hover" */
    &:hover {
        background: var(--color-secondary);
        transform: translateY(-2px);
    }
    
    /* Fusionne une classe pour marquer un état ".btn.is-active" */
    &.is-active {
        box-shadow: 0 0 0 2px var(--color-accent);
    }
    
    /* Vise la fraterie directe : "Si un bouton vient juste après un autre bouton" */
    & + & {
        margin-left: 1rem;
    }
}
```

!!! tip "L'ère moderne"
    Le Nesting permet au code CSS de calquer exactement la structure arborescente visuelle de la page HTML. Il supprime la charge cognitive de lecture et réduit considérablement le besoin d'outils de compilation tiers sur des projets Frontend modernes.

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les **variables CSS** centralisent votre design system et permettent le dark mode sans JavaScript. Les **filtres** (`blur`, `grayscale`, `brightness` et `backdrop-filter`) ouvrent la porte au glassmorphism et aux traitements d'images dynamiques. **Clip-path**, **blend modes** et **gradients** donnent au CSS un pouvoir graphique que l'on réservait autrefois à Photoshop. Les **container queries** et les sélecteurs `:is()`, `:has()`, `@layer` sont la génération suivante du CSS — largement supportés en 2025.

| Propriété | Usage principal |
|-----------|----------------|
| `--var` / `var()` | Design system, thèmes, dark mode |
| `filter` | Effets photo, hover desaturation |
| `backdrop-filter` | Glassmorphism, navigation translucide |
| `clip-path` | Formes décoratives, révélations animées |
| `mix-blend-mode` | Fusion calques, effets créatifs |
| `linear-gradient` | Fonds, overlays, boutons |
| `conic-gradient` | Graphiques, effets coniques |
| `@container` | Composants auto-adaptatifs |
| `:has()` | Logique parent-enfant en CSS pur |
| `Nesting (&)` | Structurer l'arborescence proprement sans SCSS |

> Vous maîtrisez maintenant l'ensemble de la chaîne CSS — des fondamentaux aux propriétés avancées. L'étape suivante est de mettre en pratique toutes ces compétences dans un projet concret : le [Projet Final HTML/CSS](../../../projets/html-css-vitrine/index.md), où vous construirez un site vitrine professionnel multi-pages en HTML et CSS uniquement.

<br>