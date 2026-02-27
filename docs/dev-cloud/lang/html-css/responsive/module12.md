---
description: "Maîtriser le Responsive Design : media queries, mobile-first, breakpoints, images responsive, layouts adaptatifs"
icon: lucide/book-open-check
tags: ["CSS", "RESPONSIVE", "MEDIA-QUERIES", "MOBILE-FIRST", "BREAKPOINTS", "ADAPTIVE-DESIGN"]
---

# XII - Responsive Design

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : Un Site pour Tous les Écrans

!!! quote "Analogie pédagogique"
    _Imaginez un **journal papier** qui s'adapte magiquement selon qu'on le lit dans le métro (format poche), sur la table du petit-déjeuner (format standard), ou affiché sur un mur (affiche géante). Les articles se réorganisent, les colonnes changent, les images s'ajustent, tout reste lisible et agréable. **Le Responsive Design**, c'est exactement ça pour le web : un site qui s'adapte **intelligemment** à TOUS les écrans (smartphone 320px, tablette 768px, laptop 1366px, écran 4K 3840px). **Avant le Responsive** (pré-2010), on créait 3 sites séparés : mobile.site.com, site.com, desktop.site.com. **Maintenance cauchemar** : 3× le code, 3× les bugs, 3× le temps. **Avec Responsive**, UN SEUL site qui s'adapte automatiquement. Les **media queries CSS** détectent la largeur écran et appliquent styles appropriés : "Si écran < 768px, navigation devient menu hamburger, 1 colonne, images pleine largeur". Plus de 60% du trafic web vient du mobile aujourd'hui : **le Responsive n'est plus une option, c'est OBLIGATOIRE**. Google pénalise sites non-responsive dans résultats recherche mobile. Ce module vous transforme en expert Responsive : vous créerez des sites qui fonctionnent parfaitement sur smartwatch, smartphone, tablette, laptop, desktop, TV, et tout ce qui existe entre les deux._

**Responsive Design** = Approche de conception web où un site s'adapte automatiquement à la taille de l'écran.

**Pourquoi le Responsive est ESSENTIEL ?**

✅ **Multi-devices** : 60%+ trafic mobile (smartphones, tablettes)  
✅ **SEO** : Google privilégie sites mobile-friendly  
✅ **UX** : Expérience optimale sur tous écrans  
✅ **Maintenance** : Un seul code pour tous devices  
✅ **Coût** : Pas besoin versions séparées  
✅ **Futur-proof** : S'adapte aux nouveaux devices  

**Statistiques 2024 :**

- 📱 63% du trafic web = mobile
- 💻 32% = desktop
- 📲 5% = tablette
- 🔍 Google = "Mobile-First Indexing" (index version mobile d'abord)

**Les 3 piliers du Responsive :**

1. **Fluid Grids** : Layouts flexibles (%, fr, auto-fit)
2. **Flexible Images** : Images qui s'adaptent (max-width: 100%)
3. **Media Queries** : Styles conditionnels selon écran

**Ce module couvre TOUT le Responsive Design moderne.**

---

## 1. Viewport et Meta Tag

### 1.1 Comprendre le Viewport

```
┌─────────────────────────────────────────────┐
│  DEVICE (Écran physique)                    │
│  iPhone 12 : 390×844 pixels                 │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │  VIEWPORT (Zone visible navigateur)   │  │
│  │  Sans meta viewport : 980px (défaut)  │  │
│  │                                       │  │
│  │  Page desktop "zoomée" pour rentrer   │  │
│  │  → Texte illisible, besoin zoom       │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  AVEC META VIEWPORT                         │
│  iPhone 12 : 390×844 pixels                 │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │  VIEWPORT : 390px (largeur device)    │  │
│  │                                       │  │
│  │  Page optimisée pour mobile           │  │
│  │  → Texte lisible, pas besoin zoom     │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

**Viewport** = Zone visible du navigateur (≠ taille physique écran).

Sans meta viewport, mobile affiche version desktop zoomée (980px de large).

### 1.2 Meta Viewport Tag

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    
    <!-- ⚠️ OBLIGATOIRE pour Responsive -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Mon Site Responsive</title>
</head>
<body>
    <!-- Contenu -->
</body>
</html>
```

**Décortication meta viewport :**

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

- `name="viewport"` : Configure le viewport
- `width=device-width` : Largeur viewport = largeur device
- `initial-scale=1.0` : Zoom initial 100% (pas de zoom)

**Autres propriétés viewport (rarement utilisées) :**

```html
<!-- Minimum zoom -->
<meta name="viewport" content="width=device-width, minimum-scale=0.5">

<!-- Maximum zoom -->
<meta name="viewport" content="width=device-width, maximum-scale=2.0">

<!-- ❌ ÉVITER : Désactive zoom utilisateur (accessibilité) -->
<meta name="viewport" content="width=device-width, user-scalable=no">

<!-- Largeur fixe (rare) -->
<meta name="viewport" content="width=600">

<!-- Combinaison (courante) -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

**viewport-fit=cover** : Pour iPhone X+ (encoche notch).

**Règle d'or : TOUJOURS inclure meta viewport en responsive.**

```html
<!-- ✅ Configuration recommandée (99% des cas) -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## 2. Media Queries

### 2.1 Syntaxe de Base

```css
/* Syntaxe générale */
@media media-type and (media-feature) {
    /* Styles appliqués si condition vraie */
}

/* Exemple simple */
@media screen and (max-width: 768px) {
    body {
        background-color: lightblue;
    }
}
/* Si écran ≤ 768px : fond bleu clair */

/* Exemple pratique : Navigation responsive */
.nav {
    display: flex;
    gap: 20px;
}

@media (max-width: 768px) {
    .nav {
        flex-direction: column;
        gap: 10px;
    }
}
/* Desktop : horizontal, Mobile : vertical */
```

### 2.2 Media Types

```css
/* screen : Écrans (desktop, mobile, tablette) */
@media screen {
    /* Styles pour écrans */
}

/* print : Impression */
@media print {
    .no-print {
        display: none;
    }
}

/* all : Tous types (défaut) */
@media all {
    /* Tous devices */
}

/* speech : Lecteurs d'écran (rare) */
@media speech {
    /* Styles pour synthèse vocale */
}

/* ⚠️ Types dépréciés (ne plus utiliser) */
/* handheld, projection, tv, etc. */

/* Omission type = all implicite */
@media (max-width: 768px) {
    /* = @media all and (max-width: 768px) */
}
```

### 2.3 Media Features (Caractéristiques)

```css
/* ========================================
   WIDTH (Largeur viewport)
   ======================================== */

/* max-width : Largeur MAXIMALE */
@media (max-width: 768px) {
    /* Appliqué si largeur ≤ 768px */
}

/* min-width : Largeur MINIMALE */
@media (min-width: 1024px) {
    /* Appliqué si largeur ≥ 1024px */
}

/* width : Largeur EXACTE (rare) */
@media (width: 768px) {
    /* Appliqué si largeur = exactement 768px */
}

/* ========================================
   HEIGHT (Hauteur viewport)
   ======================================== */

/* max-height : Hauteur MAXIMALE */
@media (max-height: 600px) {
    /* Écrans petits en hauteur */
    .header {
        height: 60px;  /* Header plus petit */
    }
}

/* min-height : Hauteur MINIMALE */
@media (min-height: 900px) {
    /* Écrans grands en hauteur */
}

/* ========================================
   ORIENTATION
   ======================================== */

/* portrait : Hauteur > Largeur */
@media (orientation: portrait) {
    /* Smartphone vertical, tablette verticale */
}

/* landscape : Largeur > Hauteur */
@media (orientation: landscape) {
    /* Smartphone horizontal, desktop */
}

/* ========================================
   ASPECT-RATIO (Ratio d'affichage)
   ======================================== */

@media (aspect-ratio: 16/9) {
    /* Écran 16:9 (TV, beaucoup de laptops) */
}

@media (min-aspect-ratio: 16/9) {
    /* Écran au moins 16:9 (ultra-wide) */
}

/* ========================================
   RESOLUTION (Densité pixels)
   ======================================== */

/* Écrans Retina/HiDPI (2× densité) */
@media (min-resolution: 2dppx) {
    /* Charger images haute résolution */
    .logo {
        background-image: url('logo@2x.png');
    }
}

/* ========================================
   PREFERS (Préférences utilisateur)
   ======================================== */

/* Dark mode */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: white;
    }
}

/* Light mode */
@media (prefers-color-scheme: light) {
    body {
        background-color: white;
        color: black;
    }
}

/* Réduction mouvement (accessibilité) */
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

/* Contraste élevé */
@media (prefers-contrast: high) {
    /* Augmenter contrastes */
}

/* ========================================
   HOVER (Capacité survol)
   ======================================== */

/* Peut survoler (souris) */
@media (hover: hover) {
    .button:hover {
        background-color: blue;
    }
}

/* Ne peut pas survoler (tactile) */
@media (hover: none) {
    .button:active {
        background-color: blue;
    }
}

/* ========================================
   POINTER (Précision pointeur)
   ======================================== */

/* Pointeur précis (souris) */
@media (pointer: fine) {
    /* Petits boutons OK */
}

/* Pointeur imprécis (doigt) */
@media (pointer: coarse) {
    .button {
        min-height: 44px;  /* Apple recommande 44×44px tactile */
    }
}
```

### 2.4 Opérateurs Logiques

```css
/* AND : Combine conditions (toutes vraies) */
@media screen and (min-width: 768px) and (max-width: 1024px) {
    /* Écran entre 768px et 1024px (tablette) */
}

/* OR : Virgule = OU (une condition vraie suffit) */
@media (max-width: 768px), (orientation: portrait) {
    /* Mobile OU orientation portrait */
}

/* NOT : Inverse condition */
@media not screen and (min-width: 768px) {
    /* PAS écran ≥ 768px */
}

/* ONLY : Masque pour anciens navigateurs (obsolète) */
@media only screen and (min-width: 768px) {
    /* Anciens navigateurs ignorent cette règle */
}

/* Combinaisons complexes */
@media screen and (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
    /* Tablette horizontale entre 768-1024px */
}

@media (min-width: 768px) and (prefers-color-scheme: dark), (max-width: 480px) {
    /* (Desktop ET dark mode) OU Mobile */
}
```

### 2.5 Breakpoints Courants

```css
/* ========================================
   BREAKPOINTS STANDARDS
   ======================================== */

/* Mobile (smartphones) */
@media (max-width: 480px) {
    /* Très petits écrans (iPhone SE, etc.) */
}

@media (max-width: 767px) {
    /* Tous mobiles */
}

/* Tablette */
@media (min-width: 768px) and (max-width: 1023px) {
    /* Tablettes (iPad, etc.) */
}

/* Desktop */
@media (min-width: 1024px) {
    /* Laptops, desktops */
}

@media (min-width: 1280px) {
    /* Grands écrans */
}

@media (min-width: 1920px) {
    /* Full HD et plus */
}

/* ========================================
   APPROCHE MOBILE-FIRST (Recommandée)
   ======================================== */

/* Styles de base = Mobile (pas de media query) */
body {
    font-size: 16px;
    padding: 15px;
}

/* Tablette et plus */
@media (min-width: 768px) {
    body {
        font-size: 18px;
        padding: 30px;
    }
}

/* Desktop et plus */
@media (min-width: 1024px) {
    body {
        font-size: 20px;
        padding: 40px;
    }
}

/* ========================================
   BREAKPOINTS FRAMEWORKS POPULAIRES
   ======================================== */

/* Bootstrap 5 */
/* xs: < 576px (défaut, pas de media query) */
/* sm: ≥ 576px */
/* md: ≥ 768px */
/* lg: ≥ 992px */
/* xl: ≥ 1200px */
/* xxl: ≥ 1400px */

/* Tailwind CSS */
/* sm: 640px */
/* md: 768px */
/* lg: 1024px */
/* xl: 1280px */
/* 2xl: 1536px */

/* ========================================
   BREAKPOINTS CUSTOM (Selon projet)
   ======================================== */

/* Variables CSS pour breakpoints */
:root {
    --breakpoint-mobile: 480px;
    --breakpoint-tablet: 768px;
    --breakpoint-desktop: 1024px;
    --breakpoint-large: 1440px;
}

/* Utilisation avec @custom-media (future spec) */
@custom-media --mobile (max-width: 480px);
@custom-media --tablet (min-width: 481px) and (max-width: 1023px);
@custom-media --desktop (min-width: 1024px);

/* ⚠️ @custom-media pas encore supporté universellement */
/* Utiliser préprocesseur CSS (Sass, PostCSS) pour l'instant */
```

---

## 3. Mobile-First vs Desktop-First

### 3.1 Approche Desktop-First (Ancienne)

```css
/* ❌ DESKTOP-FIRST (partir du desktop, adapter mobile) */

/* Styles de base = Desktop */
.container {
    max-width: 1200px;
    padding: 40px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
}

/* Puis adapter pour plus petit */
@media (max-width: 1024px) {
    .container {
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
}

@media (max-width: 768px) {
    .container {
        grid-template-columns: repeat(2, 1fr);
        padding: 30px;
    }
}

@media (max-width: 480px) {
    .container {
        grid-template-columns: 1fr;
        padding: 15px;
        gap: 15px;
    }
}

/* Problèmes :
   1. Mobile charge styles desktop inutiles
   2. Plus de code (reset styles)
   3. Max-width = logique inversée
   4. Performance mobile dégradée
*/
```

### 3.2 Approche Mobile-First (Moderne, Recommandée)

```css
/* ✅ MOBILE-FIRST (partir du mobile, enrichir desktop) */

/* Styles de base = Mobile (pas de media query) */
.container {
    padding: 15px;
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
}

/* Puis enrichir pour plus grand */
@media (min-width: 481px) {
    .container {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}

@media (min-width: 769px) {
    .container {
        padding: 30px;
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (min-width: 1025px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 40px;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
    }
}

/* Avantages :
   1. Mobile charge UNIQUEMENT styles mobile
   2. Moins de code (ajout progressif)
   3. Min-width = logique progressive
   4. Performance mobile optimale
   5. Priorise majorité trafic (mobile 60%+)
*/
```

### 3.3 Comparaison Détaillée

```css
/* ========================================
   EXEMPLE COMPLET : NAVIGATION
   ======================================== */

/* DESKTOP-FIRST */
/* ❌ */
.nav {
    display: flex;
    justify-content: space-between;
    padding: 0 40px;
}

.nav-links {
    display: flex;
    gap: 30px;
}

.menu-toggle {
    display: none;  /* Burger caché par défaut */
}

@media (max-width: 768px) {
    .nav {
        padding: 0 20px;
    }
    
    .nav-links {
        display: none;  /* Cache liens */
        flex-direction: column;
    }
    
    .menu-toggle {
        display: block;  /* Affiche burger */
    }
    
    .nav-links.open {
        display: flex;  /* Affiche menu si ouvert */
    }
}

/* MOBILE-FIRST */
/* ✅ */
.nav {
    padding: 0 20px;
}

.nav-links {
    display: none;
    flex-direction: column;
}

.nav-links.open {
    display: flex;
}

.menu-toggle {
    display: block;
}

@media (min-width: 769px) {
    .nav {
        display: flex;
        justify-content: space-between;
        padding: 0 40px;
    }
    
    .nav-links {
        display: flex !important;  /* Toujours visible */
        flex-direction: row;
        gap: 30px;
    }
    
    .menu-toggle {
        display: none;  /* Cache burger */
    }
}

/* Mobile-First = Moins de reset, plus clair */
```

**Règle d'or : TOUJOURS utiliser Mobile-First en 2024.**

---

## 4. Images Responsives

### 4.1 Images Fluides de Base

```css
/* Image responsive simple */
img {
    max-width: 100%;  /* Jamais plus large que container */
    height: auto;     /* Garde ratio */
    display: block;   /* Évite espace bas (inline) */
}

/* Exemple dans container */
.image-container {
    width: 100%;
    max-width: 800px;
}

.image-container img {
    max-width: 100%;
    height: auto;
}

/* Image avec contraintes */
.thumbnail {
    max-width: 100%;
    height: auto;
    min-width: 200px;   /* Minimum 200px */
    max-height: 400px;  /* Maximum 400px hauteur */
    object-fit: cover;  /* Couvre zone sans déformation */
}

/* Image background responsive */
.hero {
    background-image: url('hero.jpg');
    background-size: cover;      /* Couvre tout */
    background-position: center; /* Centré */
    background-repeat: no-repeat;
    min-height: 400px;
}

@media (min-width: 768px) {
    .hero {
        min-height: 600px;
    }
}
```

### 4.2 srcset et sizes (Résolutions Multiples)

```html
<!-- srcset : Images différentes résolutions -->
<img 
    src="image-800.jpg" 
    srcset="
        image-400.jpg 400w,
        image-800.jpg 800w,
        image-1200.jpg 1200w,
        image-1600.jpg 1600w
    "
    sizes="
        (max-width: 480px) 100vw,
        (max-width: 1024px) 50vw,
        800px
    "
    alt="Description"
>

<!-- Explication :
     srcset : Liste images avec largeur (400w = 400px de large)
     sizes : 
       - Mobile (≤480px) : image prend 100% largeur viewport (100vw)
       - Tablette (≤1024px) : image prend 50% largeur viewport (50vw)
       - Desktop : image fixe 800px
     
     Navigateur choisit image optimale selon :
     1. Taille écran
     2. Densité pixels (Retina = 2×)
     3. Conditions réseau
-->

<!-- Exemple concret : Galerie photos -->
<div class="gallery">
    <img 
        src="photo-medium.jpg"
        srcset="
            photo-small.jpg 400w,
            photo-medium.jpg 800w,
            photo-large.jpg 1200w
        "
        sizes="
            (max-width: 768px) 100vw,
            (max-width: 1200px) 50vw,
            33vw
        "
        alt="Photo galerie"
    >
</div>

<!-- Mobile : 100vw (pleine largeur)
     Tablette : 50vw (2 colonnes)
     Desktop : 33vw (3 colonnes)
-->

<!-- Images Retina/HiDPI avec densité pixels -->
<img 
    src="logo.png"
    srcset="
        logo.png 1x,
        logo@2x.png 2x,
        logo@3x.png 3x
    "
    alt="Logo"
>
<!-- 1x = écran normal
     2x = Retina (iPhone, MacBook)
     3x = Retina HD (iPhone Plus)
-->
```

### 4.3 Element `<picture>` (Art Direction)

```html
<!-- Art direction : Images DIFFÉRENTES selon écran -->

<!-- Cas 1 : Recadrage différent -->
<picture>
    <!-- Mobile : image verticale (portrait) -->
    <source 
        media="(max-width: 768px)" 
        srcset="hero-portrait.jpg"
    >
    
    <!-- Desktop : image horizontale (paysage) -->
    <source 
        media="(min-width: 769px)" 
        srcset="hero-landscape.jpg"
    >
    
    <!-- Fallback (navigateurs anciens) -->
    <img src="hero-landscape.jpg" alt="Hero">
</picture>

<!-- Cas 2 : Formats modernes (WebP, AVIF) -->
<picture>
    <!-- Format AVIF (meilleur compression, navigateurs modernes) -->
    <source 
        srcset="image.avif" 
        type="image/avif"
    >
    
    <!-- Format WebP (bon compromis) -->
    <source 
        srcset="image.webp" 
        type="image/webp"
    >
    
    <!-- Fallback JPEG (tous navigateurs) -->
    <img src="image.jpg" alt="Image">
</picture>

<!-- Cas 3 : Combinaison art direction + résolution -->
<picture>
    <!-- Mobile -->
    <source 
        media="(max-width: 768px)"
        srcset="
            mobile-small.jpg 400w,
            mobile-large.jpg 800w
        "
        sizes="100vw"
    >
    
    <!-- Tablette -->
    <source 
        media="(min-width: 769px) and (max-width: 1024px)"
        srcset="
            tablet-small.jpg 600w,
            tablet-large.jpg 1200w
        "
        sizes="100vw"
    >
    
    <!-- Desktop -->
    <source 
        media="(min-width: 1025px)"
        srcset="
            desktop-small.jpg 1000w,
            desktop-large.jpg 2000w
        "
        sizes="80vw"
    >
    
    <img src="desktop-small.jpg" alt="Hero">
</picture>

<!-- Exemple pratique : Hero banner -->
<picture>
    <!-- Mobile : image carrée centrée sur visage -->
    <source 
        media="(max-width: 768px)" 
        srcset="hero-mobile-square.jpg"
    >
    
    <!-- Desktop : image large avec paysage -->
    <source 
        media="(min-width: 769px)" 
        srcset="hero-desktop-wide.jpg"
    >
    
    <img 
        src="hero-desktop-wide.jpg" 
        alt="Hero banner"
        style="width: 100%; height: auto;"
    >
</picture>
```

### 4.4 Lazy Loading

```html
<!-- Loading lazy : Charge image quand visible (économie bande passante) -->

<img 
    src="image.jpg" 
    alt="Description"
    loading="lazy"
>

<!-- Valeurs loading :
     - lazy : Charge quand proche viewport (défaut recommandé)
     - eager : Charge immédiatement (images above-fold)
     - auto : Navigateur décide
-->

<!-- Exemple galerie avec lazy loading -->
<div class="gallery">
    <!-- Première image : eager (immédiatement visible) -->
    <img src="photo-1.jpg" alt="Photo 1" loading="eager">
    
    <!-- Images suivantes : lazy (scroll nécessaire) -->
    <img src="photo-2.jpg" alt="Photo 2" loading="lazy">
    <img src="photo-3.jpg" alt="Photo 3" loading="lazy">
    <img src="photo-4.jpg" alt="Photo 4" loading="lazy">
    <!-- ... -->
</div>

<!-- Combinaison srcset + lazy -->
<img 
    src="image-800.jpg"
    srcset="
        image-400.jpg 400w,
        image-800.jpg 800w,
        image-1200.jpg 1200w
    "
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="Description"
    loading="lazy"
>
```

---

## 5. Typographie Responsive

### 5.1 Tailles Relatives (rem, em)

```css
/* ========================================
   REM (Recommandé pour responsive)
   ======================================== */

html {
    font-size: 16px;  /* Base (1rem = 16px) */
}

body {
    font-size: 1rem;  /* = 16px */
}

h1 {
    font-size: 2.5rem;  /* = 40px */
}

h2 {
    font-size: 2rem;    /* = 32px */
}

p {
    font-size: 1rem;    /* = 16px */
    line-height: 1.6;   /* Relatif à font-size */
}

/* Adapter taille base selon écran */
@media (min-width: 768px) {
    html {
        font-size: 18px;  /* 1rem = 18px sur tablette+ */
    }
    /* Tous les rem s'ajustent automatiquement */
}

@media (min-width: 1024px) {
    html {
        font-size: 20px;  /* 1rem = 20px sur desktop */
    }
}

/* Résultat :
   Mobile  : h1 = 2.5 × 16 = 40px
   Tablette: h1 = 2.5 × 18 = 45px
   Desktop : h1 = 2.5 × 20 = 50px
   → Échelle automatique
*/
```

### 5.2 Fluid Typography avec clamp()

```css
/* clamp() : Typographie fluide (s'adapte automatiquement) */

/* Syntaxe : clamp(min, idéal, max) */

h1 {
    font-size: clamp(2rem, 5vw, 4rem);
    /* Min 2rem (32px), Idéal 5% viewport, Max 4rem (64px) */
}

/* Comportement :
   Mobile (320px)  : 5vw = 16px → clamp à 2rem = 32px (min)
   Tablette (768px): 5vw = 38px → 38px (entre min/max)
   Desktop (1920px): 5vw = 96px → clamp à 4rem = 64px (max)
   → Grandit progressivement sans media queries
*/

/* Exemple complet typographie fluide */
:root {
    /* Taille base fluide */
    font-size: clamp(14px, 1.5vw, 20px);
}

h1 {
    font-size: clamp(2rem, 5vw + 1rem, 4rem);
    line-height: 1.2;
}

h2 {
    font-size: clamp(1.5rem, 3vw + 1rem, 3rem);
}

h3 {
    font-size: clamp(1.25rem, 2vw + 1rem, 2rem);
}

p {
    font-size: clamp(1rem, 1vw + 0.5rem, 1.25rem);
    line-height: clamp(1.5, 1vw + 1.2, 1.8);
}

/* Formule magique typographie fluide */
/* font-size: clamp(MIN_rem, VW_value + BASE_rem, MAX_rem) */

/* Calculateur en ligne : 
   https://modern-fluid-typography.vercel.app/
*/
```

### 5.3 Échelle Typographique Responsive

```css
/* Échelle modulaire (ratio 1.25 - Major Third) */

/* Mobile (base 16px) */
:root {
    --ratio: 1.25;
    
    --text-xs: 0.8rem;      /* 12.8px */
    --text-sm: 0.889rem;    /* 14.2px */
    --text-base: 1rem;      /* 16px */
    --text-lg: 1.25rem;     /* 20px */
    --text-xl: 1.563rem;    /* 25px */
    --text-2xl: 1.953rem;   /* 31.2px */
    --text-3xl: 2.441rem;   /* 39px */
    --text-4xl: 3.052rem;   /* 48.8px */
}

/* Desktop (ratio plus grand - 1.333 - Perfect Fourth) */
@media (min-width: 1024px) {
    :root {
        --ratio: 1.333;
        
        --text-xl: 1.777rem;   /* 28.4px */
        --text-2xl: 2.369rem;  /* 37.9px */
        --text-3xl: 3.157rem;  /* 50.5px */
        --text-4xl: 4.209rem;  /* 67.3px */
    }
}

/* Utilisation */
h1 {
    font-size: var(--text-4xl);
}

h2 {
    font-size: var(--text-3xl);
}

p {
    font-size: var(--text-base);
}

.caption {
    font-size: var(--text-sm);
}
```

### 5.4 Line-height et Spacing Responsifs

```css
/* Line-height adaptatif */
p {
    font-size: 1rem;
    line-height: 1.6;  /* Mobile : Plus serré */
}

@media (min-width: 768px) {
    p {
        line-height: 1.75;  /* Desktop : Plus aéré */
    }
}

/* Ou avec clamp */
p {
    line-height: clamp(1.5, 0.5vw + 1.3, 1.8);
}

/* Espacement paragraphes responsive */
p {
    margin-bottom: clamp(1rem, 2vw, 2rem);
}

/* Mesure optimale (caractères par ligne) */
.content {
    max-width: 65ch;  /* Idéal : 45-75 caractères */
    margin: 0 auto;
}

/* Responsive avec clamp */
.content {
    max-width: clamp(45ch, 50vw, 75ch);
}
```

---

## 6. Layouts Responsive Avancés

### 6.1 Container Queries (Moderne)

```css
/* Container queries : Media queries sur CONTAINER (pas viewport) */

/* Définir container */
.card-container {
    container-type: inline-size;  /* Active container queries */
    container-name: card;          /* Nom optionnel */
}

/* Query sur taille container (pas viewport) */
@container card (min-width: 400px) {
    .card {
        display: grid;
        grid-template-columns: 200px 1fr;
    }
}

@container card (min-width: 600px) {
    .card {
        grid-template-columns: 300px 1fr;
    }
}

/* Avantage : Composant s'adapte selon SON container
   Pas selon viewport global
   Idéal pour composants réutilisables
*/

/* Exemple pratique : Card responsive */
.sidebar-container {
    container-type: inline-size;
    width: 300px;
}

.main-container {
    container-type: inline-size;
    width: 1000px;
}

/* Même carte, comportement différent selon container */
@container (max-width: 400px) {
    .product-card {
        /* Layout vertical si container étroit */
        grid-template-columns: 1fr;
    }
}

@container (min-width: 401px) {
    .product-card {
        /* Layout horizontal si container large */
        grid-template-columns: 200px 1fr;
    }
}

/* Card dans sidebar (300px) : vertical
   Card dans main (1000px) : horizontal
   → S'adapte au contexte, pas au viewport global
*/

/* ⚠️ Support navigateurs : Chrome 105+, Safari 16+, Firefox 110+ */
```

### 6.2 Grid Responsive Sans Media Queries

```css
/* Grille auto-responsive (vue Module 11) */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

/* Comportement automatique :
   Mobile (400px) : 1 colonne (400 < 2×250)
   Tablette (800px) : 3 colonnes (800 / 250 ≈ 3)
   Desktop (1600px) : 6 colonnes
   → ZÉRO media query
*/

/* Variantes */

/* Min 200px, préféré 300px */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr));
}

/* Avec contraintes */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(clamp(200px, 30vw, 400px), 1fr));
}

/* Layout RAM (Repeat, Auto, Minmax) */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: clamp(1rem, 3vw, 3rem);
}
```

### 6.3 Flexbox Responsive

```css
/* Flexbox wrap automatique */
.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.card {
    flex: 1 1 300px;  /* Grandit, rétrécit, base 300px */
}

/* Comportement :
   Mobile (400px) : 1 carte par ligne
   Tablette (800px) : 2 cartes par ligne
   Desktop (1200px) : 3-4 cartes
   → Automatique selon espace disponible
*/

/* Navigation responsive */
.nav {
    display: flex;
    gap: 20px;
}

@media (max-width: 768px) {
    .nav {
        flex-direction: column;
    }
}

/* Layout Flexbox classique */
.layout {
    display: flex;
    gap: 20px;
}

.sidebar {
    flex: 0 0 250px;  /* Fixe 250px */
}

.content {
    flex: 1;  /* Prend espace restant */
}

@media (max-width: 768px) {
    .layout {
        flex-direction: column;
    }
    
    .sidebar {
        flex: 0 0 auto;  /* Hauteur auto */
    }
}
```

---

## 7. Touch et Interactions Mobiles

### 7.1 Tailles Cibles Tactiles

```css
/* Apple Human Interface Guidelines : 44×44px minimum */
/* Material Design : 48×48px minimum */

/* Boutons tactiles */
.button {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 24px;
    
    /* Espacement entre boutons */
    margin: 8px;
}

/* Liens dans texte */
a {
    /* Augmenter zone cliquable sans changer visuel */
    position: relative;
    padding: 8px 4px;
}

/* Inputs formulaire */
input,
textarea,
select {
    min-height: 44px;
    padding: 12px;
    font-size: 16px;  /* Évite zoom auto iOS (≥16px) */
}

/* Checkbox et radio */
input[type="checkbox"],
input[type="radio"] {
    width: 24px;
    height: 24px;
    /* Ajouter padding label pour zone plus grande */
}

label {
    padding: 12px;
    cursor: pointer;
}

/* Navigation mobile */
.mobile-nav a {
    display: block;
    padding: 16px 20px;  /* Zone tactile confortable */
    min-height: 48px;
}
```

### 7.2 Hover vs Touch

```css
/* Détecter capacité hover */

/* Desktop (souris) : hover activé */
@media (hover: hover) {
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
}

/* Mobile (tactile) : pas de hover, utiliser :active */
@media (hover: none) {
    .card:active {
        transform: scale(0.98);
        opacity: 0.8;
    }
}

/* Combo hover + touch */
.button {
    transition: all 0.3s ease;
}

/* Hover souris */
@media (hover: hover) {
    .button:hover {
        background-color: blue;
    }
}

/* Touch feedback */
.button:active {
    transform: scale(0.95);
}

/* Désactiver effets hover sur touch */
@media (hover: none) {
    .card:hover {
        /* Annuler hover sur tactile */
        transform: none;
    }
}
```

### 7.3 Optimisations Touch

```css
/* Désactiver sélection texte (UI éléments) */
.button,
.nav-item {
    user-select: none;
    -webkit-user-select: none;
    -webkit-tap-highlight-color: transparent;  /* Retire highlight iOS */
}

/* Touch-action : Contrôle gestes navigateur */
.swipeable {
    touch-action: pan-y;  /* Uniquement scroll vertical */
}

.map {
    touch-action: none;  /* Désactive gestes (carte interactive) */
}

.carousel {
    touch-action: pan-x;  /* Uniquement swipe horizontal */
}

/* Scroll comportement */
.scroll-container {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;  /* Momentum scroll iOS */
}

/* Zoom image désactivé */
img {
    touch-action: manipulation;  /* Désactive double-tap zoom */
}

/* Formulaires iOS */
input,
textarea {
    font-size: 16px;  /* ≥16px évite zoom auto iOS */
}

/* Supprime arrondis iOS */
input,
button {
    -webkit-appearance: none;
    border-radius: 0;
}
```

---

## 8. Exercices Pratiques

### Exercice 1 : Navigation Responsive

**Objectif :** Créer navigation qui devient menu hamburger mobile.

**Consigne :**
- Desktop : liens horizontaux
- Mobile : menu hamburger + menu vertical

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Responsive</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
        }
        
        /* Mobile-first */
        .nav {
            background-color: #2c3e50;
            padding: 15px 20px;
        }
        
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        /* Menu hamburger (mobile) */
        .menu-toggle {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 10px;
        }
        
        .nav-links {
            display: none;
            flex-direction: column;
            width: 100%;
            margin-top: 15px;
        }
        
        .nav-links.open {
            display: flex;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .nav-links a:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Desktop (≥768px) */
        @media (min-width: 768px) {
            .nav-container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .menu-toggle {
                display: none;
            }
            
            .nav-links {
                display: flex !important;
                flex-direction: row;
                width: auto;
                margin-top: 0;
            }
            
            .nav-links a {
                border-top: none;
                padding: 10px 20px;
            }
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-container">
            <div class="logo">MonSite</div>
            
            <button class="menu-toggle" aria-label="Toggle menu">
                ☰
            </button>
            
            <div class="nav-links">
                <a href="#home">Accueil</a>
                <a href="#about">À propos</a>
                <a href="#services">Services</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
    </nav>
    
    <script>
        const menuToggle = document.querySelector('.menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
    </script>
</body>
</html>
```

</details>

### Exercice 2 : Galerie Responsive

**Objectif :** Galerie photos adaptive sans media queries.

**Consigne :**
- Grid auto-responsive
- Cards min 250px
- Images srcset

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie Responsive</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: clamp(20px, 5vw, 60px);
        }
        
        h1 {
            text-align: center;
            margin-bottom: clamp(30px, 5vw, 60px);
            font-size: clamp(2rem, 5vw, 3rem);
            color: #2c3e50;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: clamp(15px, 3vw, 30px);
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .gallery-item {
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        @media (hover: hover) {
            .gallery-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
        }
        
        .gallery-item img {
            width: 100%;
            height: 250px;
            object-fit: cover;
            display: block;
        }
        
        .gallery-item-content {
            padding: 20px;
        }
        
        .gallery-item h3 {
            margin-bottom: 10px;
            color: #2c3e50;
            font-size: clamp(1.1rem, 2vw, 1.3rem);
        }
        
        .gallery-item p {
            color: #7f8c8d;
            line-height: 1.6;
            font-size: clamp(0.9rem, 1.5vw, 1rem);
        }
    </style>
</head>
<body>
    <h1>Galerie Photos Responsive</h1>
    
    <div class="gallery">
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/3498db/ffffff?text=Photo+1"
                srcset="
                    https://via.placeholder.com/400/3498db/ffffff?text=Photo+1 400w,
                    https://via.placeholder.com/800/3498db/ffffff?text=Photo+1 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 1"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Paysage Montagne</h3>
                <p>Belle vue panoramique des Alpes.</p>
            </div>
        </div>
        
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/2ecc71/ffffff?text=Photo+2"
                srcset="
                    https://via.placeholder.com/400/2ecc71/ffffff?text=Photo+2 400w,
                    https://via.placeholder.com/800/2ecc71/ffffff?text=Photo+2 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 2"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Forêt Tropicale</h3>
                <p>Végétation luxuriante en Amazonie.</p>
            </div>
        </div>
        
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/e74c3c/ffffff?text=Photo+3"
                srcset="
                    https://via.placeholder.com/400/e74c3c/ffffff?text=Photo+3 400w,
                    https://via.placeholder.com/800/e74c3c/ffffff?text=Photo+3 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 3"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Coucher de Soleil</h3>
                <p>Magnifique coucher de soleil sur l'océan.</p>
            </div>
        </div>
        
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/f39c12/ffffff?text=Photo+4"
                srcset="
                    https://via.placeholder.com/400/f39c12/ffffff?text=Photo+4 400w,
                    https://via.placeholder.com/800/f39c12/ffffff?text=Photo+4 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 4"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Désert Sahara</h3>
                <p>Dunes de sable à perte de vue.</p>
            </div>
        </div>
        
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/9b59b6/ffffff?text=Photo+5"
                srcset="
                    https://via.placeholder.com/400/9b59b6/ffffff?text=Photo+5 400w,
                    https://via.placeholder.com/800/9b59b6/ffffff?text=Photo+5 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 5"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Aurore Boréale</h3>
                <p>Spectacle lumineux en Norvège.</p>
            </div>
        </div>
        
        <div class="gallery-item">
            <img 
                src="https://via.placeholder.com/400/1abc9c/ffffff?text=Photo+6"
                srcset="
                    https://via.placeholder.com/400/1abc9c/ffffff?text=Photo+6 400w,
                    https://via.placeholder.com/800/1abc9c/ffffff?text=Photo+6 800w
                "
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                alt="Photo 6"
                loading="lazy"
            >
            <div class="gallery-item-content">
                <h3>Cascade</h3>
                <p>Chute d'eau impressionnante en Islande.</p>
            </div>
        </div>
    </div>
</body>
</html>
```

</details>

### Exercice 3 : Layout Responsive Complet

**Objectif :** Page avec header, sidebar, content, footer responsive.

**Consigne :**
- Mobile : colonne unique
- Desktop : sidebar + content

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layout Responsive</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        
        /* Mobile-first */
        .page-layout {
            display: grid;
            grid-template-areas:
                "header"
                "main"
                "sidebar"
                "footer";
            min-height: 100vh;
        }
        
        .header {
            grid-area: header;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
        }
        
        .header h1 {
            font-size: clamp(1.5rem, 4vw, 2rem);
        }
        
        .main {
            grid-area: main;
            padding: clamp(20px, 5vw, 40px);
        }
        
        .sidebar {
            grid-area: sidebar;
            background-color: #ecf0f1;
            padding: clamp(20px, 5vw, 30px);
        }
        
        .footer {
            grid-area: footer;
            background-color: #34495e;
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        .content-section {
            margin-bottom: 30px;
        }
        
        .content-section h2 {
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: clamp(1.3rem, 3vw, 1.8rem);
        }
        
        .content-section p {
            color: #555;
            margin-bottom: 15px;
        }
        
        .sidebar h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .sidebar ul {
            list-style: none;
        }
        
        .sidebar li {
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
        }
        
        .sidebar a {
            color: #3498db;
            text-decoration: none;
        }
        
        /* Tablette (≥768px) */
        @media (min-width: 768px) {
            .page-layout {
                grid-template-areas:
                    "header header"
                    "main sidebar"
                    "footer footer";
                grid-template-columns: 1fr 300px;
                grid-template-rows: auto 1fr auto;
            }
        }
        
        /* Desktop (≥1024px) */
        @media (min-width: 1024px) {
            .page-layout {
                grid-template-columns: 1fr 350px;
            }
            
            .header,
            .main,
            .sidebar,
            .footer {
                padding-left: max(20px, calc((100vw - 1200px) / 2));
                padding-right: max(20px, calc((100vw - 1200px) / 2));
            }
        }
    </style>
</head>
<body>
    <div class="page-layout">
        <header class="header">
            <h1>Mon Site Responsive</h1>
            <p>Un layout qui s'adapte à tous les écrans</p>
        </header>
        
        <main class="main">
            <article class="content-section">
                <h2>Article Principal</h2>
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
                <p>
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco 
                    laboris nisi ut aliquip ex ea commodo consequat.
                </p>
            </article>
            
            <article class="content-section">
                <h2>Deuxième Section</h2>
                <p>
                    Duis aute irure dolor in reprehenderit in voluptate velit 
                    esse cillum dolore eu fugiat nulla pariatur.
                </p>
                <p>
                    Excepteur sint occaecat cupidatat non proident, sunt in 
                    culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </article>
        </main>
        
        <aside class="sidebar">
            <h3>Navigation</h3>
            <ul>
                <li><a href="#section1">Section 1</a></li>
                <li><a href="#section2">Section 2</a></li>
                <li><a href="#section3">Section 3</a></li>
                <li><a href="#section4">Section 4</a></li>
            </ul>
            
            <h3 style="margin-top: 30px;">À propos</h3>
            <p style="font-size: 0.9rem; color: #555;">
                Cette sidebar s'affiche en bas sur mobile, 
                à droite sur desktop.
            </p>
        </aside>
        
        <footer class="footer">
            <p>&copy; 2024 Mon Site. Tous droits réservés.</p>
        </footer>
    </div>
</body>
</html>
```

</details>

---

## 9. Projet du Module : Portfolio Responsive Complet

### 9.1 Cahier des Charges

**Créer un portfolio professionnel fully responsive :**

**Spécifications techniques :**
- Meta viewport configuré
- Mobile-first approach
- Navigation responsive (hamburger mobile)
- Hero section fluid typography
- About section (image + texte responsive)
- Portfolio gallery (auto-responsive grid)
- Contact form (inputs tactiles)
- Footer
- Images srcset
- Dark mode support
- 3 breakpoints minimum (mobile, tablet, desktop)
- Code CSS externe validé

### 9.2 Solution Complète

<details>
<summary>Voir la solution complète du projet (HTML)</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Portfolio responsive de Sophie Martin, développeuse web frontend">
    <title>Sophie Martin - Portfolio Responsive</title>
    <link rel="stylesheet" href="portfolio-responsive.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="#home" class="logo">Sophie Martin</a>
            
            <button class="menu-toggle" aria-label="Toggle navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            
            <ul class="nav-links">
                <li><a href="#about">À propos</a></li>
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>
    
    <!-- Hero -->
    <section class="hero" id="home">
        <div class="hero-content">
            <h1>Développeuse Web Frontend</h1>
            <p>Je crée des expériences web modernes, responsives et performantes</p>
            <a href="#contact" class="cta-button">Me contacter</a>
        </div>
    </section>
    
    <!-- About -->
    <section class="about" id="about">
        <div class="container">
            <div class="about-grid">
                <div class="about-image">
                    <picture>
                        <source 
                            media="(max-width: 768px)"
                            srcset="https://via.placeholder.com/400x400/3498db/ffffff?text=Sophie"
                        >
                        <img 
                            src="https://via.placeholder.com/500x500/3498db/ffffff?text=Sophie"
                            alt="Sophie Martin"
                            loading="lazy"
                        >
                    </picture>
                </div>
                
                <div class="about-text">
                    <h2>À propos de moi</h2>
                    <p>
                        Développeuse web frontend passionnée avec 5 ans d'expérience 
                        dans la création d'interfaces utilisateur modernes et responsives.
                    </p>
                    <p>
                        Spécialisée en HTML5, CSS3, JavaScript et frameworks modernes 
                        (React, Vue.js), je m'assure que chaque projet fonctionne 
                        parfaitement sur tous les devices.
                    </p>
                    
                    <div class="skills">
                        <span class="skill-tag">HTML5/CSS3</span>
                        <span class="skill-tag">JavaScript</span>
                        <span class="skill-tag">React</span>
                        <span class="skill-tag">Vue.js</span>
                        <span class="skill-tag">Responsive Design</span>
                        <span class="skill-tag">Accessibilité</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Portfolio -->
    <section class="portfolio" id="portfolio">
        <div class="container">
            <h2 class="section-title">Mon Portfolio</h2>
            
            <div class="portfolio-grid">
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/3498db/ffffff?text=Projet+1"
                        srcset="
                            https://via.placeholder.com/400x300/3498db/ffffff?text=Projet+1 400w,
                            https://via.placeholder.com/800x600/3498db/ffffff?text=Projet+1 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="E-commerce Platform"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>E-commerce Platform</h3>
                        <p>Plateforme de vente en ligne responsive avec React et API REST.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
                
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/2ecc71/ffffff?text=Projet+2"
                        srcset="
                            https://via.placeholder.com/400x300/2ecc71/ffffff?text=Projet+2 400w,
                            https://via.placeholder.com/800x600/2ecc71/ffffff?text=Projet+2 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="Dashboard Analytics"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>Dashboard Analytics</h3>
                        <p>Dashboard de visualisation de données avec graphiques interactifs.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
                
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/e74c3c/ffffff?text=Projet+3"
                        srcset="
                            https://via.placeholder.com/400x300/e74c3c/ffffff?text=Projet+3 400w,
                            https://via.placeholder.com/800x600/e74c3c/ffffff?text=Projet+3 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="Blog CMS"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>Blog CMS</h3>
                        <p>Système de gestion de contenu avec éditeur WYSIWYG.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
                
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/f39c12/ffffff?text=Projet+4"
                        srcset="
                            https://via.placeholder.com/400x300/f39c12/ffffff?text=Projet+4 400w,
                            https://via.placeholder.com/800x600/f39c12/ffffff?text=Projet+4 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="Portfolio Designer"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>Portfolio Designer</h3>
                        <p>Site portfolio pour designer graphique avec galerie photos.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
                
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/9b59b6/ffffff?text=Projet+5"
                        srcset="
                            https://via.placeholder.com/400x300/9b59b6/ffffff?text=Projet+5 400w,
                            https://via.placeholder.com/800x600/9b59b6/ffffff?text=Projet+5 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="App Mobile"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>Progressive Web App</h3>
                        <p>Application web progressive installable offline-first.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
                
                <article class="portfolio-item">
                    <img 
                        src="https://via.placeholder.com/400x300/1abc9c/ffffff?text=Projet+6"
                        srcset="
                            https://via.placeholder.com/400x300/1abc9c/ffffff?text=Projet+6 400w,
                            https://via.placeholder.com/800x600/1abc9c/ffffff?text=Projet+6 800w
                        "
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        alt="Landing Page"
                        loading="lazy"
                    >
                    <div class="portfolio-content">
                        <h3>Landing Page SaaS</h3>
                        <p>Page de destination optimisée conversion pour produit SaaS.</p>
                        <a href="#" class="project-link">Voir le projet →</a>
                    </div>
                </article>
            </div>
        </div>
    </section>
    
    <!-- Contact -->
    <section class="contact" id="contact">
        <div class="container">
            <h2 class="section-title">Me Contacter</h2>
            
            <form class="contact-form">
                <div class="form-group">
                    <label for="name">Nom</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" rows="5" required></textarea>
                </div>
                
                <button type="submit" class="submit-button">Envoyer le message</button>
            </form>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Sophie Martin. Tous droits réservés.</p>
            <div class="social-links">
                <a href="#" aria-label="LinkedIn">LinkedIn</a>
                <a href="#" aria-label="GitHub">GitHub</a>
                <a href="#" aria-label="Twitter">Twitter</a>
            </div>
        </div>
    </footer>
    
    <script src="portfolio-responsive.js"></script>
</body>
</html>
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 1/2)</summary>

```css
/* portfolio-responsive.css */

/* ========================================
   RESET & VARIABLES
   ======================================== */

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    /* Colors */
    --color-primary: #3498db;
    --color-secondary: #2ecc71;
    --color-dark: #2c3e50;
    --color-light: #ecf0f1;
    --color-white: #ffffff;
    --color-text: #555555;
    
    /* Spacing */
    --spacing-xs: clamp(0.5rem, 1vw, 1rem);
    --spacing-sm: clamp(1rem, 2vw, 1.5rem);
    --spacing-md: clamp(1.5rem, 3vw, 2.5rem);
    --spacing-lg: clamp(2rem, 5vw, 4rem);
    --spacing-xl: clamp(3rem, 7vw, 6rem);
    
    /* Typography */
    --font-base: 16px;
    --font-heading: clamp(2rem, 5vw + 1rem, 4rem);
    --font-subheading: clamp(1.5rem, 3vw + 1rem, 2.5rem);
    
    /* Container */
    --container-max: 1200px;
    --container-padding: clamp(20px, 5vw, 60px);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    :root {
        --color-dark: #ecf0f1;
        --color-light: #2c3e50;
        --color-white: #1a1a1a;
        --color-text: #cccccc;
    }
}

html {
    font-size: var(--font-base);
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--color-text);
    background-color: var(--color-white);
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

/* ========================================
   UTILITIES
   ======================================== */

.container {
    max-width: var(--container-max);
    margin: 0 auto;
    padding: 0 var(--container-padding);
}

.section-title {
    font-size: var(--font-subheading);
    text-align: center;
    margin-bottom: var(--spacing-lg);
    color: var(--color-dark);
}

/* ========================================
   NAVIGATION
   ======================================== */

.nav {
    background-color: var(--color-dark);
    color: var(--color-white);
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-container {
    max-width: var(--container-max);
    margin: 0 auto;
    padding: 0 var(--container-padding);
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 70px;
}

.logo {
    color: var(--color-white);
    text-decoration: none;
    font-size: clamp(1.2rem, 3vw, 1.5rem);
    font-weight: bold;
}

/* Menu toggle (mobile) */
.menu-toggle {
    display: flex;
    flex-direction: column;
    gap: 5px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 10px;
}

.menu-toggle span {
    width: 25px;
    height: 3px;
    background-color: var(--color-white);
    transition: all 0.3s ease;
}

.menu-toggle.open span:nth-child(1) {
    transform: rotate(45deg) translateY(8px);
}

.menu-toggle.open span:nth-child(2) {
    opacity: 0;
}

.menu-toggle.open span:nth-child(3) {
    transform: rotate(-45deg) translateY(-8px);
}

/* Navigation links (mobile) */
.nav-links {
    display: none;
    position: fixed;
    top: 70px;
    left: 0;
    width: 100%;
    background-color: var(--color-dark);
    flex-direction: column;
    list-style: none;
}

.nav-links.open {
    display: flex;
}

.nav-links li {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-links a {
    display: block;
    color: var(--color-white);
    text-decoration: none;
    padding: 20px var(--container-padding);
    transition: background-color 0.3s ease;
}

.nav-links a:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Desktop navigation (≥768px) */
@media (min-width: 768px) {
    .menu-toggle {
        display: none;
    }
    
    .nav-links {
        display: flex !important;
        position: static;
        flex-direction: row;
        width: auto;
        background-color: transparent;
    }
    
    .nav-links li {
        border-top: none;
    }
    
    .nav-links a {
        padding: 10px 20px;
    }
}

/* ========================================
   HERO
   ======================================== */

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: var(--color-white);
    padding: var(--spacing-xl) var(--container-padding);
    text-align: center;
    min-height: clamp(400px, 60vh, 600px);
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-content h1 {
    font-size: var(--font-heading);
    margin-bottom: var(--spacing-md);
    line-height: 1.2;
}

.hero-content p {
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    margin-bottom: var(--spacing-lg);
    opacity: 0.95;
}

.cta-button {
    display: inline-block;
    padding: clamp(12px, 2vw, 18px) clamp(30px, 5vw, 50px);
    background-color: var(--color-white);
    color: #667eea;
    text-decoration: none;
    border-radius: 50px;
    font-weight: bold;
    font-size: clamp(1rem, 1.5vw, 1.2rem);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

@media (hover: hover) {
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
}

.cta-button:active {
    transform: scale(0.98);
}

/* ========================================
   ABOUT
   ======================================== */

.about {
    padding: var(--spacing-xl) 0;
    background-color: var(--color-light);
}

.about-grid {
    display: grid;
    gap: var(--spacing-lg);
    align-items: center;
}

.about-image img {
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.about-text h2 {
    font-size: var(--font-subheading);
    margin-bottom: var(--spacing-md);
    color: var(--color-dark);
}

.about-text p {
    margin-bottom: var(--spacing-sm);
    line-height: 1.8;
}

.skills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: var(--spacing-md);
}

.skill-tag {
    padding: 8px 16px;
    background-color: var(--color-primary);
    color: var(--color-white);
    border-radius: 20px;
    font-size: 0.9rem;
}

/* Desktop about (≥768px) */
@media (min-width: 768px) {
    .about-grid {
        grid-template-columns: 400px 1fr;
        gap: var(--spacing-xl);
    }
}
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 2/2)</summary>

```css
/* ========================================
   PORTFOLIO
   ======================================== */

.portfolio {
    padding: var(--spacing-xl) 0;
}

.portfolio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-md);
}

.portfolio-item {
    background-color: var(--color-white);
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

@media (hover: hover) {
    .portfolio-item:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
}

.portfolio-item img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.portfolio-content {
    padding: var(--spacing-md);
}

.portfolio-content h3 {
    margin-bottom: var(--spacing-sm);
    color: var(--color-dark);
    font-size: clamp(1.2rem, 2vw, 1.4rem);
}

.portfolio-content p {
    margin-bottom: var(--spacing-sm);
    line-height: 1.6;
}

.project-link {
    color: var(--color-primary);
    text-decoration: none;
    font-weight: bold;
    transition: color 0.3s ease;
}

.project-link:hover {
    color: var(--color-secondary);
}

/* ========================================
   CONTACT
   ======================================== */

.contact {
    padding: var(--spacing-xl) 0;
    background-color: var(--color-light);
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
    background-color: var(--color-white);
    padding: var(--spacing-lg);
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: var(--spacing-md);
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--color-dark);
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: clamp(12px, 2vw, 16px);
    border: 2px solid #ddd;
    border-radius: 8px;
    font-family: inherit;
    font-size: 16px;  /* Évite zoom iOS */
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--color-primary);
}

.form-group textarea {
    resize: vertical;
    min-height: 120px;
}

.submit-button {
    width: 100%;
    padding: clamp(14px, 2.5vw, 18px);
    background-color: var(--color-primary);
    color: var(--color-white);
    border: none;
    border-radius: 8px;
    font-size: clamp(1rem, 1.5vw, 1.1rem);
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    
    /* Touch-friendly */
    min-height: 48px;
    -webkit-tap-highlight-color: transparent;
}

@media (hover: hover) {
    .submit-button:hover {
        background-color: var(--color-secondary);
    }
}

.submit-button:active {
    transform: scale(0.98);
}

/* ========================================
   FOOTER
   ======================================== */

.footer {
    background-color: var(--color-dark);
    color: var(--color-white);
    padding: var(--spacing-lg) 0;
    text-align: center;
}

.footer .container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: center;
}

.social-links {
    display: flex;
    gap: var(--spacing-md);
}

.social-links a {
    color: var(--color-white);
    text-decoration: none;
    transition: color 0.3s ease;
}

.social-links a:hover {
    color: var(--color-primary);
}

/* Desktop footer (≥768px) */
@media (min-width: 768px) {
    .footer .container {
        flex-direction: row;
        justify-content: space-between;
    }
}

/* ========================================
   RESPONSIVE REFINEMENTS
   ======================================== */

/* Reduce motion (accessibility) */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* Print styles */
@media print {
    .nav,
    .cta-button,
    .contact-form,
    .footer {
        display: none;
    }
    
    body {
        font-size: 12pt;
        color: black;
        background: white;
    }
}

/* High contrast mode */
@media (prefers-contrast: high) {
    :root {
        --color-primary: #0000ff;
        --color-secondary: #008000;
    }
}
```

</details>

<details>
<summary>Voir la solution complète du projet (JavaScript)</summary>

```javascript
// portfolio-responsive.js

// Menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('open');
    navLinks.classList.toggle('open');
});

// Fermer menu au clic sur lien
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('open');
        navLinks.classList.remove('open');
    });
});

// Smooth scroll (fallback pour anciens navigateurs)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
const contactForm = document.querySelector('.contact-form');

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    
    if (name && email && message) {
        alert('Message envoyé avec succès ! (Démo)');
        contactForm.reset();
    }
});

// Lazy loading images (polyfill pour anciens navigateurs)
if ('loading' in HTMLImageElement.prototype) {
    // Natif lazy loading supporté
} else {
    // Polyfill ou librairie (exemple : lazysizes)
    console.log('Lazy loading not supported, consider polyfill');
}

// Détection viewport pour analytics (optionnel)
const reportViewport = () => {
    const width = window.innerWidth;
    let device;
    
    if (width < 768) {
        device = 'mobile';
    } else if (width < 1024) {
        device = 'tablet';
    } else {
        device = 'desktop';
    }
    
    console.log(`Viewport: ${width}px - Device: ${device}`);
    // Envoyer à analytics si nécessaire
};

window.addEventListener('resize', reportViewport);
reportViewport();
```

</details>

### 9.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Meta viewport correctement configuré
- [ ] Mobile-first approach utilisée
- [ ] Navigation hamburger fonctionnelle mobile
- [ ] Hero avec typographie fluide (clamp)
- [ ] About section responsive (grid adaptatif)
- [ ] Portfolio grid auto-responsive (auto-fit minmax)
- [ ] Images avec srcset/sizes
- [ ] Picture element pour art direction
- [ ] Lazy loading images
- [ ] Formulaire inputs ≥48px (touch-friendly)
- [ ] Font-size inputs ≥16px (évite zoom iOS)
- [ ] Hover detection (@media hover)
- [ ] Touch-action sur éléments interactifs
- [ ] Dark mode support (prefers-color-scheme)
- [ ] Reduced motion support
- [ ] 3+ breakpoints testés (320px, 768px, 1024px+)
- [ ] Code CSS externe validé W3C
- [ ] Performance mobile testée (Lighthouse)

---

## 10. Best Practices Responsive

### 10.1 Règles d'Or

```css
/* 1. TOUJOURS meta viewport */
<meta name="viewport" content="width=device-width, initial-scale=1.0">

/* 2. Mobile-first TOUJOURS */
/* Base = mobile, enrichir pour desktop */

/* 3. clamp() pour typographie fluide */
h1 {
    font-size: clamp(2rem, 5vw, 4rem);
}

/* 4. auto-fit + minmax pour grids */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* 5. rem pour tout sauf borders (px) */
.container {
    padding: 2rem;  /* rem */
    border: 1px solid;  /* px OK pour borders */
}

/* 6. Images max-width: 100% */
img {
    max-width: 100%;
    height: auto;
}

/* 7. Touch targets ≥48×48px */
.button {
    min-height: 48px;
    min-width: 48px;
}

/* 8. Tester VRAIMENT sur devices */
/* Émulateur Chrome ≠ vraie tablette/smartphone */

/* 9. Performance mobile prioritaire */
/* Images optimisées, lazy loading */

/* 10. Accessibilité */
/* Prefers-reduced-motion, contraste, focus visible */
```

### 10.2 Breakpoints Recommandés 2024

```css
/* Approche simplifiée (3 breakpoints) */

/* Mobile (défaut, pas de media query) */
/* 320px - 767px */

/* Tablette */
@media (min-width: 768px) {
    /* 768px - 1023px */
}

/* Desktop */
@media (min-width: 1024px) {
    /* 1024px+ */
}

/* Approche détaillée (5 breakpoints) */

/* Mobile portrait (défaut) */
/* 320px - 479px */

/* Mobile landscape */
@media (min-width: 480px) {
    /* 480px - 767px */
}

/* Tablette portrait */
@media (min-width: 768px) {
    /* 768px - 1023px */
}

/* Desktop / Tablette landscape */
@media (min-width: 1024px) {
    /* 1024px - 1439px */
}

/* Large desktop */
@media (min-width: 1440px) {
    /* 1440px+ */
}

/* Custom selon projet */
/* Analyser analytics : quelles résolutions visiteurs ? */
/* Adapter breakpoints aux besoins réels */
```

### 10.3 Testing Responsive

```
OUTILS TESTING :

1. Chrome DevTools
   - F12 → Device Toolbar (Ctrl+Shift+M)
   - Tester toutes résolutions
   - Throttling réseau (3G, 4G)

2. Firefox Responsive Design Mode
   - F12 → Responsive Design Mode
   - Toucher simulation

3. Devices Réels (OBLIGATOIRE)
   - iPhone (Safari iOS ≠ Chrome)
   - Android (Chrome, Samsung Internet)
   - iPad
   - Vieux devices (performance)

4. Lighthouse (Chrome)
   - Performance mobile
   - Accessibility
   - Best practices

5. BrowserStack / Sauce Labs
   - Tests cross-browser cloud
   - Vrais devices virtuels

6. Can I Use
   - Support features CSS/HTML
   - https://caniuse.com

CHECKLIST TESTING :

[ ] 320px (iPhone SE)
[ ] 375px (iPhone standard)
[ ] 390px (iPhone 12+)
[ ] 768px (iPad portrait)
[ ] 1024px (iPad landscape)
[ ] 1366px (Laptop standard)
[ ] 1920px (Full HD)
[ ] 2560px (2K)
[ ] 3840px (4K)

[ ] Orientation portrait
[ ] Orientation landscape
[ ] Zoom 200% (accessibilité)
[ ] Touch interactions
[ ] Keyboard navigation
```

---

## 11. Checkpoint de Progression

### À la fin de ce Module 12, vous maîtrisez :

**Fondamentaux Responsive :**

- [x] Viewport et meta tag
- [x] Mobile-first vs Desktop-first
- [x] Breakpoints standards

**Media Queries :**

- [x] Syntaxe complète
- [x] Media types (screen, print)
- [x] Media features (width, height, orientation, etc.)
- [x] Opérateurs logiques (and, or, not)
- [x] Prefers (color-scheme, reduced-motion, contrast)

**Images Responsives :**

- [x] Images fluides (max-width: 100%)
- [x] srcset et sizes
- [x] Picture element (art direction)
- [x] Lazy loading

**Typographie Responsive :**

- [x] rem et em
- [x] clamp() fluid typography
- [x] Échelle modulaire
- [x] Line-height adaptatif

**Layouts Responsifs :**

- [x] Grid auto-responsive
- [x] Flexbox responsive
- [x] Container queries (moderne)

**Touch et Mobile :**

- [x] Tailles cibles tactiles
- [x] Hover vs touch
- [x] Touch optimisations

**Best practices :**

- [x] Règles d'or
- [x] Breakpoints recommandés
- [x] Testing checklist

### Félicitations Formation HTML+CSS

**Vous avez terminé la formation complète HTML+CSS (12 modules) !**

**Modules HTML (1-6) :**

- ✅ Introduction, texte, liens, images, listes, tableaux, formulaires, sémantique

**Modules CSS (7-12) :**

- ✅ Introduction CSS, sélecteurs, box model, Flexbox, Grid, Responsive

**Compétences acquises :**

- 🎯 HTML5 sémantique professionnel
- 🎨 CSS moderne (Flexbox, Grid)
- 📱 Sites fully responsive multi-devices
- ♿ Accessibilité web
- ⚡ Performance optimisée
- 🎭 UX/UI best practices

**Prochaines étapes possibles :**

- Module 13 : Animations & Transitions CSS
- Module 14 : CSS Avancé (variables, transforms, filters)
- Module 15 : Projet Final Intégral
- JavaScript (ES6+, DOM, Events)
- Frameworks (React, Vue.js)
- Backend (Node.js, PHP)

---

**Module 12 Terminé - Bravo ! 🎉 📱**

**Statistiques Module 12 :**

- 1 projet complet (Portfolio responsive professionnel)
- 3 exercices progressifs avec solutions
- Media queries maîtrisées
- Mobile-first approach appliquée
- Images responsives (srcset, picture)
- Typographie fluide (clamp)
- Touch optimisations
- Testing checklist complète

**Félicitations pour cette maîtrise complète du Responsive Design ! 🚀📱**
