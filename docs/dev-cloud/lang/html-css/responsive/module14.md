---
description: "Maîtriser CSS Avancé : variables CSS, filters, clip-path, blend modes, masks, gradients complexes, shapes"
icon: lucide/book-open-check
tags: ["CSS", "ADVANCED", "VARIABLES", "FILTERS", "CLIP-PATH", "BLEND-MODES", "MASKS", "GRADIENTS"]
---

# XIV - CSS Avancé

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : CSS comme Langage de Design

!!! quote "Analogie pédagogique"
    _Imaginez un **studio de post-production photo/vidéo professionnel** : filtres couleurs (Photoshop), masques de découpe (InDesign), modes de fusion (calques), dégradés complexes, effets visuels avancés. **Avant CSS avancé** (pré-2015), ces effets nécessitaient images PNG/SVG pré-générées ou JavaScript lourd. Modifier une couleur = régénérer 50 images. **Avec CSS moderne**, tout est dynamique en temps réel : `filter: blur(5px)` floute élément instantanément, `clip-path: polygon()` découpe formes complexes, `mix-blend-mode: multiply` fusionne calques comme Photoshop, `--color-primary: #3498db` centralise variables réutilisables partout. **CSS Variables (Custom Properties)** = révolution maintenabilité : un thème complet modifiable en changeant 5 variables. **Filters CSS** = Photoshop dans navigateur : brightness, contrast, saturate, blur, drop-shadow en temps réel GPU-accelerated. **Clip-path** = découpes vectorielles sans images : cercles, polygones, SVG path. **Blend modes** = fusion calques professionnelle : multiply, screen, overlay identiques Photoshop. **Masks** = masques alpha complexes. **Gradients** = dégradés multi-couleurs, radiaux, coniques, motifs. Ce module transforme CSS de "langage styling basique" en **outil design professionnel puissant**. Vous créerez effets visuels impossibles avant, thèmes dynamiques, UI glassmorphism, neumorphism, effets holographiques, tout en CSS pur performant._

**CSS Avancé** = Fonctionnalités CSS modernes pour effets visuels et design complexes.

**Pourquoi CSS Avancé est ESSENTIEL ?**

✅ **Maintenabilité** : Variables CSS = thèmes dynamiques faciles  
✅ **Performance** : Filtres GPU vs images lourdes  
✅ **Flexibilité** : Modifications temps réel sans régénérer assets  
✅ **Créativité** : Effets impossibles avant sans JavaScript  
✅ **Responsive** : Effets s'adaptent automatiquement  
✅ **Accessibilité** : Respect prefers-color-scheme, high-contrast  

**Évolution CSS :**

- 2011 : CSS3 (border-radius, box-shadow, transitions)
- 2015 : Variables CSS (custom properties)
- 2016 : Filters, blend modes
- 2018 : clip-path, masks
- 2020 : conic-gradient, aspect-ratio
- 2023+ : CSS moderne (container queries, :has(), layers)

**Ce module couvre TOUT CSS avancé niveau expert.**

---

## 1. Variables CSS (Custom Properties)

### 1.1 Syntaxe et Déclaration

```css
/* Variables CSS = Propriétés personnalisées réutilisables */

/* Déclaration dans :root (global) */
:root {
    --color-primary: #3498db;
    --color-secondary: #2ecc71;
    --spacing-base: 16px;
    --font-size-large: 2rem;
}

/* Utilisation avec var() */
.button {
    background-color: var(--color-primary);
    padding: var(--spacing-base);
    font-size: var(--font-size-large);
}

/* Résultat :
   background-color: #3498db;
   padding: 16px;
   font-size: 2rem;
*/

/* Scope des variables */

/* Global (:root) */
:root {
    --primary: blue;
}

/* Tout élément peut utiliser */
.element {
    color: var(--primary);
}

/* Local (élément spécifique) */
.card {
    --card-padding: 20px;
    padding: var(--card-padding);
}

/* Uniquement .card et descendants peuvent utiliser --card-padding */

/* Héritage CSS variables */
.parent {
    --text-color: red;
}

.child {
    color: var(--text-color);  /* Hérite de parent = red */
}

/* Valeur par défaut (fallback) */
.element {
    color: var(--undefined-var, blue);
    /* Si --undefined-var n'existe pas, utilise blue */
}

/* Fallback chaîné */
.element {
    color: var(--primary, var(--secondary, black));
    /* --primary → --secondary → black (cascade) */
}
```

### 1.2 Conventions de Nommage

```css
/* Conventions best practices */

:root {
    /* Couleurs : --color-* */
    --color-primary: #3498db;
    --color-secondary: #2ecc71;
    --color-danger: #e74c3c;
    --color-warning: #f39c12;
    --color-success: #2ecc71;
    --color-info: #3498db;
    
    /* Couleurs texte : --text-* */
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --text-muted: #95a5a6;
    --text-inverse: #ffffff;
    
    /* Couleurs fond : --bg-* */
    --bg-primary: #ffffff;
    --bg-secondary: #ecf0f1;
    --bg-dark: #2c3e50;
    
    /* Spacing : --space-* */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-2xl: 48px;
    
    /* Typography : --font-* */
    --font-family-base: 'Segoe UI', sans-serif;
    --font-family-heading: 'Georgia', serif;
    --font-family-mono: 'Courier New', monospace;
    
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 2rem;
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    
    --line-height-tight: 1.2;
    --line-height-base: 1.6;
    --line-height-loose: 1.8;
    
    /* Borders : --border-* */
    --border-width-thin: 1px;
    --border-width-medium: 2px;
    --border-width-thick: 4px;
    
    --border-radius-sm: 4px;
    --border-radius-md: 8px;
    --border-radius-lg: 12px;
    --border-radius-xl: 16px;
    --border-radius-full: 9999px;
    
    /* Shadows : --shadow-* */
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.15);
    --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.2);
    
    /* Transitions : --transition-* */
    --transition-fast: 150ms;
    --transition-base: 300ms;
    --transition-slow: 500ms;
    
    --ease-in: cubic-bezier(0.4, 0, 1, 1);
    --ease-out: cubic-bezier(0, 0, 0.2, 1);
    --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Z-index : --z-* */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-popover: 1060;
    --z-tooltip: 1070;
}

/* Utilisation */
.button {
    background-color: var(--color-primary);
    color: var(--text-inverse);
    padding: var(--space-md) var(--space-lg);
    border-radius: var(--border-radius-md);
    font-weight: var(--font-weight-semibold);
    transition: all var(--transition-base) var(--ease-out);
    box-shadow: var(--shadow-md);
}

.button:hover {
    box-shadow: var(--shadow-lg);
}
```

### 1.3 Thèmes Dynamiques (Dark Mode)

```css
/* Thème clair (défaut) */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --border-color: #e0e0e0;
}

/* Thème sombre */
[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2c2c2c;
    --text-primary: #ffffff;
    --text-secondary: #b0b0b0;
    --border-color: #404040;
}

/* Ou avec prefers-color-scheme */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2c2c2c;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --border-color: #404040;
    }
}

/* Application */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
}

/* Toggle dark mode avec JavaScript */
/*
const toggleDarkMode = () => {
    document.documentElement.setAttribute(
        'data-theme',
        document.documentElement.getAttribute('data-theme') === 'dark' 
            ? 'light' 
            : 'dark'
    );
};
*/

/* Exemple complet thème */
:root {
    /* Colors */
    --primary: #3498db;
    --secondary: #2ecc71;
    
    /* Light theme */
    --bg-page: #ffffff;
    --bg-card: #f8f9fa;
    --text-main: #2c3e50;
    --text-muted: #7f8c8d;
    --border: #dee2e6;
}

[data-theme="dark"] {
    --bg-page: #0d1117;
    --bg-card: #161b22;
    --text-main: #c9d1d9;
    --text-muted: #8b949e;
    --border: #30363d;
}

/* Utilisation */
body {
    background: var(--bg-page);
    color: var(--text-main);
}

.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
}

.button-primary {
    background: var(--primary);
    /* Primary garde même couleur light/dark */
}
```

### 1.4 Variables avec calc()

```css
/* Variables dans calculs */

:root {
    --base-size: 16px;
    --scale: 1.5;
}

.heading-1 {
    font-size: calc(var(--base-size) * var(--scale) * var(--scale) * var(--scale));
    /* 16px × 1.5 × 1.5 × 1.5 = 54px */
}

.heading-2 {
    font-size: calc(var(--base-size) * var(--scale) * var(--scale));
    /* 16px × 1.5 × 1.5 = 36px */
}

/* Spacing system */
:root {
    --space-unit: 8px;
}

.margin-1 { margin: calc(var(--space-unit) * 1); }  /* 8px */
.margin-2 { margin: calc(var(--space-unit) * 2); }  /* 16px */
.margin-3 { margin: calc(var(--space-unit) * 3); }  /* 24px */
.margin-4 { margin: calc(var(--space-unit) * 4); }  /* 32px */

/* Responsive avec variables */
:root {
    --container-width: 90%;
    --container-max: 1200px;
    --gutter: 20px;
}

@media (min-width: 768px) {
    :root {
        --gutter: 40px;
    }
}

.container {
    width: var(--container-width);
    max-width: var(--container-max);
    padding: 0 var(--gutter);
    margin: 0 auto;
}
```

### 1.5 Variables et JavaScript

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Variables CSS + JS</title>
    <style>
        :root {
            --theme-color: #3498db;
        }
        
        .box {
            width: 200px;
            height: 200px;
            background-color: var(--theme-color);
            transition: background-color 0.3s;
        }
    </style>
</head>
<body>
    <div class="box"></div>
    
    <button onclick="changeColor('#e74c3c')">Rouge</button>
    <button onclick="changeColor('#2ecc71')">Vert</button>
    <button onclick="changeColor('#f39c12')">Orange</button>
    
    <script>
        function changeColor(color) {
            // Modifier variable CSS depuis JavaScript
            document.documentElement.style.setProperty('--theme-color', color);
        }
        
        // Lire variable CSS
        const root = document.documentElement;
        const themeColor = getComputedStyle(root).getPropertyValue('--theme-color');
        console.log(themeColor); // "#3498db"
    </script>
</body>
</html>
```

---

## 2. CSS Filters

### 2.1 Filters de Base

```css
/* Filters = Effets visuels Photoshop-like */

/* blur() : Flou gaussien */
.element {
    filter: blur(5px);      /* Flou 5px */
    filter: blur(0);        /* Pas de flou (défaut) */
    filter: blur(10px);     /* Flou fort */
}

/* brightness() : Luminosité */
.element {
    filter: brightness(1);    /* Normal (défaut) */
    filter: brightness(0.5);  /* 50% luminosité (sombre) */
    filter: brightness(1.5);  /* 150% luminosité (clair) */
    filter: brightness(0);    /* Noir complet */
    filter: brightness(2);    /* Très clair */
}

/* contrast() : Contraste */
.element {
    filter: contrast(1);      /* Normal (défaut) */
    filter: contrast(0.5);    /* Faible contraste */
    filter: contrast(2);      /* Contraste élevé */
    filter: contrast(0);      /* Gris uniforme */
}

/* grayscale() : Noir et blanc */
.element {
    filter: grayscale(0);     /* Couleur normale (défaut) */
    filter: grayscale(0.5);   /* 50% désaturé */
    filter: grayscale(1);     /* 100% noir et blanc */
    filter: grayscale(100%);  /* = grayscale(1) */
}

/* saturate() : Saturation couleurs */
.element {
    filter: saturate(1);      /* Normal (défaut) */
    filter: saturate(0);      /* Désaturé complet (= grayscale) */
    filter: saturate(0.5);    /* Couleurs fades */
    filter: saturate(2);      /* Couleurs vibrantes */
    filter: saturate(3);      /* Sursaturé */
}

/* hue-rotate() : Rotation teinte */
.element {
    filter: hue-rotate(0deg);     /* Normal (défaut) */
    filter: hue-rotate(90deg);    /* Rotation 90° roue couleurs */
    filter: hue-rotate(180deg);   /* Couleurs inversées */
    filter: hue-rotate(360deg);   /* Tour complet = normal */
}

/* invert() : Inversion couleurs */
.element {
    filter: invert(0);        /* Normal (défaut) */
    filter: invert(0.5);      /* 50% inversé */
    filter: invert(1);        /* 100% inversé (négatif photo) */
}

/* opacity() : Transparence (= propriété opacity) */
.element {
    filter: opacity(1);       /* Opaque (défaut) */
    filter: opacity(0.5);     /* 50% transparent */
    filter: opacity(0);       /* Invisible */
}

/* sepia() : Effet sépia (photo ancienne) */
.element {
    filter: sepia(0);         /* Normal (défaut) */
    filter: sepia(0.5);       /* 50% sépia */
    filter: sepia(1);         /* 100% sépia (vintage) */
}

/* drop-shadow() : Ombre portée */
.element {
    filter: drop-shadow(5px 5px 10px rgba(0, 0, 0, 0.5));
    /* offset-x offset-y blur-radius color */
}

/* Différence drop-shadow vs box-shadow :
   drop-shadow suit contours élément (PNG transparents)
   box-shadow = boîte rectangulaire
*/
```

### 2.2 Combinaison de Filters

```css
/* Combiner plusieurs filters (espace séparé) */

.element {
    filter: brightness(1.2) contrast(1.1) saturate(1.3);
}

/* Ordre important (appliqué gauche → droite) */

/* Photo vintage */
.vintage {
    filter: sepia(0.5) contrast(1.2) brightness(1.1);
}

/* Image floue désaturée */
.blur-grayscale {
    filter: blur(3px) grayscale(1);
}

/* Glow effect */
.glow {
    filter: brightness(1.5) blur(2px) contrast(1.2);
}

/* Exemple hover effects */

.image {
    filter: grayscale(1) brightness(0.8);
    transition: filter 0.3s ease;
}

.image:hover {
    filter: grayscale(0) brightness(1);
}

/* Dark mode image adjustment */
@media (prefers-color-scheme: dark) {
    img {
        filter: brightness(0.8) contrast(1.2);
    }
}
```

### 2.3 backdrop-filter

```css
/* backdrop-filter = Filtre sur FOND derrière élément */
/* Effet "glassmorphism" moderne */

.glass {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Glassmorphism complet */
.glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px) saturate(180%);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Navigation glassmorphism */
.nav-glass {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

/* Dark mode glass */
.glass-dark {
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(15px) brightness(1.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Modal glassmorphism */
.modal-glass {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    padding: 40px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Support navigateurs : Chrome 76+, Safari 9+ */
/* Fallback pour anciens navigateurs */
@supports not (backdrop-filter: blur(10px)) {
    .glass {
        background: rgba(255, 255, 255, 0.9);
    }
}
```

---

## 3. Clip-path

### 3.1 Formes de Base

```css
/* clip-path = Découper élément selon forme */

/* circle() : Cercle */
.element {
    clip-path: circle(50%);
    /* Rayon 50% = cercle parfait */
}

.element {
    clip-path: circle(100px);
    /* Rayon 100px */
}

.element {
    clip-path: circle(40% at 50% 50%);
    /* Rayon 40%, centre à 50% 50% (défaut) */
}

.element {
    clip-path: circle(50% at 0 0);
    /* Centre coin haut-gauche */
}

/* ellipse() : Ellipse */
.element {
    clip-path: ellipse(50% 30%);
    /* Rayon X: 50%, rayon Y: 30% */
}

.element {
    clip-path: ellipse(100px 50px at 50% 50%);
    /* Rayon X: 100px, Y: 50px, centre milieu */
}

/* inset() : Rectangle avec coins arrondis */
.element {
    clip-path: inset(10px);
    /* Coupe 10px de chaque côté */
}

.element {
    clip-path: inset(10px 20px);
    /* Top/bottom: 10px, left/right: 20px */
}

.element {
    clip-path: inset(10px 20px 30px 40px);
    /* Top, right, bottom, left (comme margin) */
}

.element {
    clip-path: inset(10px round 20px);
    /* Coupe 10px + coins arrondis 20px */
}

/* polygon() : Polygone custom */
.element {
    clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
    /* Triangle : haut-milieu, bas-droite, bas-gauche */
}

/* Coordonnées en % (x y, x y, x y...) */

/* Triangle pointant droite */
.triangle-right {
    clip-path: polygon(0 0, 100% 50%, 0 100%);
}

/* Hexagone */
.hexagon {
    clip-path: polygon(
        25% 0%,
        75% 0%,
        100% 50%,
        75% 100%,
        25% 100%,
        0% 50%
    );
}

/* Étoile 5 branches */
.star {
    clip-path: polygon(
        50% 0%,
        61% 35%,
        98% 35%,
        68% 57%,
        79% 91%,
        50% 70%,
        21% 91%,
        32% 57%,
        2% 35%,
        39% 35%
    );
}

/* Message bubble */
.bubble {
    clip-path: polygon(
        0% 0%,
        100% 0%,
        100% 75%,
        75% 75%,
        75% 100%,
        50% 75%,
        0% 75%
    );
}

/* Chevron */
.chevron {
    clip-path: polygon(
        0 0,
        80% 0,
        100% 50%,
        80% 100%,
        0 100%,
        20% 50%
    );
}
```

### 3.2 Clip-path avec SVG

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Clip-path SVG</title>
    <style>
        .image-custom {
            width: 400px;
            height: 400px;
            clip-path: url(#custom-shape);
        }
    </style>
</head>
<body>
    <!-- Définir SVG path -->
    <svg width="0" height="0">
        <defs>
            <clipPath id="custom-shape">
                <path d="M0,200 Q200,0 400,200 T400,400 Q200,600 0,400 T0,200 Z" />
            </clipPath>
        </defs>
    </svg>
    
    <img src="image.jpg" class="image-custom" alt="Image">
</body>
</html>
```

### 3.3 Animations Clip-path

```css
/* Animer clip-path pour transitions */

@keyframes reveal {
    from {
        clip-path: circle(0% at 50% 50%);
    }
    to {
        clip-path: circle(100% at 50% 50%);
    }
}

.reveal-circle {
    animation: reveal 1s ease-out forwards;
}

/* Slide reveal */
@keyframes slide-reveal {
    from {
        clip-path: inset(0 100% 0 0);
    }
    to {
        clip-path: inset(0 0% 0 0);
    }
}

.slide-in {
    animation: slide-reveal 0.8s ease-out;
}

/* Morphing shapes */
@keyframes morph {
    0% {
        clip-path: circle(50% at 50% 50%);
    }
    50% {
        clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
    }
    100% {
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    }
}

.morphing {
    animation: morph 3s ease-in-out infinite;
}

/* Hover effect reveal */
.image-reveal {
    clip-path: circle(30% at 50% 50%);
    transition: clip-path 0.5s ease;
}

.image-reveal:hover {
    clip-path: circle(100% at 50% 50%);
}
```

---

## 4. Blend Modes

### 4.1 mix-blend-mode

```css
/* mix-blend-mode = Fusion élément avec fond (comme Photoshop) */

.element {
    mix-blend-mode: normal;        /* Défaut, pas de fusion */
    mix-blend-mode: multiply;      /* Multiplier (assombrir) */
    mix-blend-mode: screen;        /* Superposer (éclaircir) */
    mix-blend-mode: overlay;       /* Incrustation (contraste) */
    mix-blend-mode: darken;        /* Obscurcir */
    mix-blend-mode: lighten;       /* Éclaircir */
    mix-blend-mode: color-dodge;   /* Densité couleur - */
    mix-blend-mode: color-burn;    /* Densité couleur + */
    mix-blend-mode: hard-light;    /* Lumière crue */
    mix-blend-mode: soft-light;    /* Lumière tamisée */
    mix-blend-mode: difference;    /* Différence */
    mix-blend-mode: exclusion;     /* Exclusion */
    mix-blend-mode: hue;           /* Teinte */
    mix-blend-mode: saturation;    /* Saturation */
    mix-blend-mode: color;         /* Couleur */
    mix-blend-mode: luminosity;    /* Luminosité */
}

/* Exemples pratiques */

/* Texte sur image avec multiply */
.text-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 4rem;
    font-weight: bold;
    mix-blend-mode: multiply;
}

/* Effet duotone */
.duotone {
    background: linear-gradient(to bottom, #3498db, #e74c3c);
    mix-blend-mode: multiply;
}

/* Overlay coloré */
.color-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #3498db;
    mix-blend-mode: screen;
    opacity: 0.5;
}

/* Texte lumineux sur fond sombre */
.glow-text {
    color: white;
    background-color: black;
    mix-blend-mode: screen;
}

/* Exemple complet effet image */
.image-container {
    position: relative;
}

.image-container img {
    width: 100%;
    display: block;
}

.image-container::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    mix-blend-mode: overlay;
    opacity: 0;
    transition: opacity 0.3s;
}

.image-container:hover::after {
    opacity: 1;
}
```

### 4.2 background-blend-mode

```css
/* background-blend-mode = Fusion backgrounds multiples */

.element {
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url('image.jpg');
    background-blend-mode: multiply;
}

/* Effet duotone */
.duotone {
    background-image:
        linear-gradient(to right, #3498db, #e74c3c),
        url('photo.jpg');
    background-blend-mode: screen;
    background-size: cover;
}

/* Pattern overlay */
.pattern-overlay {
    background-image:
        url('pattern.png'),
        linear-gradient(135deg, #667eea, #764ba2);
    background-blend-mode: multiply;
}

/* Multiple blend modes */
.element {
    background-image: url('layer1.jpg'), url('layer2.jpg'), url('layer3.jpg');
    background-blend-mode: multiply, screen, overlay;
    /* Chaque layer avec blend mode différent */
}

/* Effet vintage */
.vintage {
    background-image:
        linear-gradient(rgba(255, 200, 150, 0.3), rgba(255, 200, 150, 0.3)),
        url('photo.jpg');
    background-blend-mode: multiply;
    filter: sepia(0.3) contrast(1.2);
}
```

---

## 5. Gradients Avancés

### 5.1 Linear Gradients Complexes

```css
/* Gradients linéaires multi-couleurs */

.element {
    background: linear-gradient(
        to right,
        #3498db 0%,
        #2ecc71 50%,
        #e74c3c 100%
    );
}

/* Angles précis */
.element {
    background: linear-gradient(45deg, red, blue);
    background: linear-gradient(135deg, red, blue);
    background: linear-gradient(90deg, red, blue);  /* to right */
}

/* Multiples stops */
.element {
    background: linear-gradient(
        to right,
        #667eea 0%,
        #764ba2 25%,
        #f093fb 50%,
        #4facfe 75%,
        #00f2fe 100%
    );
}

/* Hard stops (pas de transition) */
.element {
    background: linear-gradient(
        to right,
        red 0%, red 50%,
        blue 50%, blue 100%
    );
    /* Moitié rouge, moitié bleue (ligne nette) */
}

/* Repeating gradients */
.element {
    background: repeating-linear-gradient(
        45deg,
        #3498db 0px,
        #3498db 10px,
        #2ecc71 10px,
        #2ecc71 20px
    );
    /* Rayures diagonales 10px */
}

/* Pattern rayures */
.stripes {
    background: repeating-linear-gradient(
        90deg,
        #f0f0f0 0px,
        #f0f0f0 50px,
        white 50px,
        white 100px
    );
}
```

### 5.2 Radial Gradients

```css
/* Radial gradient = Dégradé circulaire/elliptique */

.element {
    background: radial-gradient(circle, red, blue);
}

/* Position */
.element {
    background: radial-gradient(circle at center, red, blue);
    background: radial-gradient(circle at top left, red, blue);
    background: radial-gradient(circle at 70% 30%, red, blue);
}

/* Taille */
.element {
    background: radial-gradient(
        circle closest-side at center,
        red,
        blue
    );
    /* closest-side, farthest-side, closest-corner, farthest-corner */
}

/* Ellipse */
.element {
    background: radial-gradient(ellipse, red, blue);
    background: radial-gradient(ellipse at center, red, blue);
}

/* Taille explicite */
.element {
    background: radial-gradient(
        circle 200px at center,
        red,
        blue
    );
}

.element {
    background: radial-gradient(
        ellipse 200px 100px at center,
        red,
        blue
    );
}

/* Repeating radial */
.element {
    background: repeating-radial-gradient(
        circle at center,
        #3498db 0px,
        #3498db 20px,
        #2ecc71 20px,
        #2ecc71 40px
    );
    /* Cercles concentriques */
}

/* Effet spotlight */
.spotlight {
    background: radial-gradient(
        circle at 50% 50%,
        rgba(255, 255, 255, 0.3) 0%,
        transparent 70%
    );
}
```

### 5.3 Conic Gradients

```css
/* Conic gradient = Dégradé conique (roue couleur) */

.element {
    background: conic-gradient(red, yellow, lime, aqua, blue, magenta, red);
    /* Roue couleur complète */
}

/* Angle départ */
.element {
    background: conic-gradient(from 90deg, red, blue);
}

/* Position centre */
.element {
    background: conic-gradient(at 30% 40%, red, blue);
}

/* Stops précis */
.element {
    background: conic-gradient(
        from 0deg at 50% 50%,
        red 0deg,
        yellow 90deg,
        lime 180deg,
        blue 270deg,
        red 360deg
    );
}

/* Pie chart CSS */
.pie-chart {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: conic-gradient(
        #3498db 0deg 120deg,
        #2ecc71 120deg 240deg,
        #e74c3c 240deg 360deg
    );
}

/* Repeating conic */
.element {
    background: repeating-conic-gradient(
        from 0deg,
        #3498db 0deg 30deg,
        #2ecc71 30deg 60deg
    );
    /* Motif rayons */
}

/* Loading spinner */
.spinner {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(
        transparent 0deg 270deg,
        #3498db 270deg 360deg
    );
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

### 5.4 Gradients Combinés

```css
/* Superposer plusieurs gradients */

.element {
    background:
        linear-gradient(45deg, rgba(255, 0, 0, 0.5), transparent),
        linear-gradient(-45deg, rgba(0, 0, 255, 0.5), transparent),
        white;
}

/* Mesh gradient */
.mesh {
    background:
        radial-gradient(circle at 20% 30%, rgba(255, 0, 0, 0.3), transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(0, 0, 255, 0.3), transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(0, 255, 0, 0.3), transparent 50%),
        linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Pattern complexe */
.pattern {
    background:
        repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,255,255,.1) 35px, rgba(255,255,255,.1) 70px),
        linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 6. Masks CSS

### 6.1 mask-image

```css
/* Mask = Masque alpha sur élément */

/* Gradient mask */
.element {
    mask-image: linear-gradient(to bottom, black, transparent);
    /* Fade out vers bas */
}

/* Radial mask */
.element {
    mask-image: radial-gradient(circle, black 50%, transparent 100%);
    /* Vignette circulaire */
}

/* Image mask */
.element {
    mask-image: url('mask.png');
    /* Utilise alpha channel image */
}

/* SVG mask */
.element {
    mask-image: url('mask.svg');
}

/* Exemples pratiques */

/* Text gradient avec mask */
.gradient-text {
    background: linear-gradient(45deg, #3498db, #e74c3c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Image fade bottom */
.fade-bottom {
    mask-image: linear-gradient(
        to bottom,
        black 0%,
        black 70%,
        transparent 100%
    );
}

/* Spotlight effect */
.spotlight {
    mask-image: radial-gradient(
        circle at var(--mouse-x) var(--mouse-y),
        black 20%,
        transparent 80%
    );
}
```

### 6.2 mask Properties

```css
/* mask-size */
.element {
    mask-image: url('mask.png');
    mask-size: cover;
    mask-size: contain;
    mask-size: 100% 100%;
    mask-size: 200px 300px;
}

/* mask-position */
.element {
    mask-image: url('mask.png');
    mask-position: center;
    mask-position: top left;
    mask-position: 50% 50%;
}

/* mask-repeat */
.element {
    mask-image: url('pattern-mask.png');
    mask-repeat: repeat;
    mask-repeat: no-repeat;
    mask-repeat: repeat-x;
    mask-repeat: repeat-y;
}

/* mask-mode */
.element {
    mask-image: url('mask.svg');
    mask-mode: alpha;          /* Utilise canal alpha */
    mask-mode: luminance;      /* Utilise luminosité */
}

/* mask-composite */
.element {
    mask-image: url('mask1.png'), url('mask2.png');
    mask-composite: add;       /* Addition */
    mask-composite: subtract;  /* Soustraction */
    mask-composite: intersect; /* Intersection */
    mask-composite: exclude;   /* Exclusion */
}

/* Raccourci mask */
.element {
    mask: url('mask.png') center / cover no-repeat;
    /* image position / size repeat */
}
```

---

## 7. Autres Propriétés Avancées

### 7.1 object-fit et object-position

```css
/* object-fit = Ajustement image/vidéo dans container */

.image {
    width: 400px;
    height: 300px;
    object-fit: fill;       /* Déforme pour remplir (défaut) */
    object-fit: contain;    /* Contient entier (peut avoir espace) */
    object-fit: cover;      /* Couvre zone (peut rogner) */
    object-fit: none;       /* Taille originale */
    object-fit: scale-down; /* contain OU none (plus petit) */
}

/* object-position */
.image {
    object-fit: cover;
    object-position: center;        /* Défaut */
    object-position: top;
    object-position: top right;
    object-position: 50% 50%;
    object-position: 10px 20px;
}

/* Exemple hero image */
.hero-image {
    width: 100%;
    height: 500px;
    object-fit: cover;
    object-position: center 30%;  /* Focus partie haute */
}
```

### 7.2 shape-outside

```css
/* shape-outside = Texte entoure forme */

.float-image {
    float: left;
    width: 200px;
    height: 200px;
    shape-outside: circle(50%);
    margin: 20px;
}
/* Texte entoure image en cercle */

/* Polygon */
.float-shape {
    float: right;
    width: 300px;
    height: 300px;
    shape-outside: polygon(0 0, 100% 0, 100% 100%);
    clip-path: polygon(0 0, 100% 0, 100% 100%);
}
/* Triangle avec texte qui entoure */

/* Image alpha */
.float-transparent {
    float: left;
    shape-outside: url('shape.png');
    shape-image-threshold: 0.5;  /* Seuil alpha */
}
```

### 7.3 aspect-ratio

```css
/* aspect-ratio = Maintenir ratio largeur/hauteur */

.video-container {
    aspect-ratio: 16 / 9;
    width: 100%;
}
/* Hauteur automatique pour ratio 16:9 */

.square {
    aspect-ratio: 1 / 1;
    width: 300px;
}
/* Carré parfait 300×300 */

.portrait {
    aspect-ratio: 3 / 4;
}

/* Remplace padding-hack ancien */

/* ❌ Ancien (padding hack) */
.video-wrapper {
    position: relative;
    padding-bottom: 56.25%;  /* 16:9 ratio */
    height: 0;
}

.video-wrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

/* ✅ Moderne (aspect-ratio) */
.video-wrapper {
    aspect-ratio: 16 / 9;
    width: 100%;
}

.video-wrapper iframe {
    width: 100%;
    height: 100%;
}
```

---

## 8. Exercices Pratiques

### Exercice 1 : Système de Thème avec Variables

**Objectif :** Créer thème light/dark avec variables CSS.

**Consignes :**
- Variables couleurs, spacing, typography
- Toggle light/dark
- Smooth transitions

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thème Light/Dark</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            /* Light theme (défaut) */
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --border-color: #dee2e6;
            --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            
            /* Brand colors (identiques light/dark) */
            --color-primary: #3498db;
            --color-secondary: #2ecc71;
            --color-danger: #e74c3c;
            
            /* Spacing */
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            
            /* Typography */
            --font-size-base: 16px;
            --font-size-lg: 1.25rem;
            --font-size-xl: 1.5rem;
        }
        
        [data-theme="dark"] {
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-tertiary: #404040;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --border-color: #404040;
            --shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }
        
        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Segoe UI', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
            padding: var(--space-xl);
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: var(--font-size-xl);
            margin-bottom: var(--space-lg);
        }
        
        .card {
            background-color: var(--bg-secondary);
            padding: var(--space-lg);
            border-radius: 12px;
            margin-bottom: var(--space-md);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }
        
        .card h2 {
            color: var(--color-primary);
            margin-bottom: var(--space-sm);
        }
        
        .card p {
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: var(--bg-secondary);
            border: 2px solid var(--border-color);
            padding: 12px 24px;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .theme-toggle:hover {
            background-color: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
        }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">
        Changer thème
    </button>
    
    <div class="container">
        <h1>Système de Thème avec Variables CSS</h1>
        
        <div class="card">
            <h2>Card 1</h2>
            <p>
                Ce système utilise des variables CSS pour gérer le thème.
                Cliquez sur le bouton pour basculer entre light et dark.
            </p>
        </div>
        
        <div class="card">
            <h2>Card 2</h2>
            <p>
                Toutes les couleurs, espacements et styles sont définis
                via des variables CSS réutilisables.
            </p>
        </div>
        
        <div class="card">
            <h2>Card 3</h2>
            <p>
                Les transitions rendent le changement de thème smooth
                et agréable pour l'utilisateur.
            </p>
        </div>
    </div>
    
    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            
            // Sauvegarder préférence
            localStorage.setItem('theme', newTheme);
        }
        
        // Charger thème sauvegardé
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
        
        // Respecter préférence système
        if (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    </script>
</body>
</html>
```

</details>

### Exercice 2 : Glassmorphism Card

**Objectif :** Créer carte avec effet glassmorphism.

**Consignes :**
- backdrop-filter blur
- Background semi-transparent
- Border subtle

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glassmorphism Card</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
        }
        
        /* Éléments décoratifs fond */
        body::before,
        body::after {
            content: '';
            position: absolute;
            border-radius: 50%;
        }
        
        body::before {
            width: 400px;
            height: 400px;
            background: rgba(255, 255, 255, 0.1);
            top: -100px;
            left: -100px;
        }
        
        body::after {
            width: 300px;
            height: 300px;
            background: rgba(255, 255, 255, 0.1);
            bottom: -50px;
            right: -50px;
        }
        
        .glass-card {
            position: relative;
            z-index: 1;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }
        
        .glass-card h2 {
            color: white;
            font-size: 2rem;
            margin-bottom: 20px;
        }
        
        .glass-card p {
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.8;
            margin-bottom: 15px;
        }
        
        .glass-button {
            display: inline-block;
            padding: 12px 30px;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 50px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            margin-top: 20px;
        }
        
        .glass-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        /* Fallback pour navigateurs sans backdrop-filter */
        @supports not (backdrop-filter: blur(20px)) {
            .glass-card {
                background: rgba(255, 255, 255, 0.9);
            }
            
            .glass-button {
                background: rgba(255, 255, 255, 0.8);
            }
        }
    </style>
</head>
<body>
    <div class="glass-card">
        <h2>Glassmorphism</h2>
        <p>
            Effet verre dépoli moderne utilisant backdrop-filter 
            pour flouter le fond derrière la carte.
        </p>
        <p>
            La transparence et le flou créent un effet élégant
            et contemporain très populaire en UI/UX design.
        </p>
        <a href="#" class="glass-button">En savoir plus</a>
    </div>
</body>
</html>
```

</details>

### Exercice 3 : Image Effects Gallery

**Objectif :** Galerie avec filtres hover variés.

**Consignes :**
- 6 images avec filters différents
- Transitions smooth
- clip-path ou blend-mode bonus

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Effects Gallery</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #1a1a1a;
            padding: 60px 20px;
        }
        
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 60px;
            font-size: 3rem;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .image-box {
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            aspect-ratio: 1;
            cursor: pointer;
        }
        
        .image-box img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: all 0.5s ease;
        }
        
        .image-label {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            color: white;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 600;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        }
        
        .image-box:hover .image-label {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Effect 1 : Grayscale */
        .effect-1 img {
            filter: grayscale(1);
        }
        
        .effect-1:hover img {
            filter: grayscale(0);
            transform: scale(1.1);
        }
        
        /* Effect 2 : Blur */
        .effect-2 img {
            filter: blur(3px) brightness(0.8);
        }
        
        .effect-2:hover img {
            filter: blur(0) brightness(1);
        }
        
        /* Effect 3 : Sepia + Contrast */
        .effect-3 img {
            filter: sepia(0.8) contrast(1.3);
        }
        
        .effect-3:hover img {
            filter: sepia(0) contrast(1);
            transform: scale(1.05);
        }
        
        /* Effect 4 : Saturate */
        .effect-4 img {
            filter: saturate(0.3);
        }
        
        .effect-4:hover img {
            filter: saturate(2);
            transform: rotate(2deg) scale(1.05);
        }
        
        /* Effect 5 : Hue Rotate */
        .effect-5 img {
            filter: hue-rotate(0deg);
        }
        
        .effect-5:hover img {
            filter: hue-rotate(180deg);
        }
        
        /* Effect 6 : Blend Mode */
        .effect-6 {
            background: linear-gradient(45deg, #3498db, #e74c3c);
        }
        
        .effect-6 img {
            mix-blend-mode: multiply;
            opacity: 0.8;
        }
        
        .effect-6:hover img {
            mix-blend-mode: normal;
            opacity: 1;
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <h1>Image Effects Gallery</h1>
    
    <div class="gallery">
        <div class="image-box effect-1">
            <img src="https://via.placeholder.com/400/3498db/ffffff?text=Image+1" alt="Image 1">
            <div class="image-label">Grayscale</div>
        </div>
        
        <div class="image-box effect-2">
            <img src="https://via.placeholder.com/400/2ecc71/ffffff?text=Image+2" alt="Image 2">
            <div class="image-label">Blur</div>
        </div>
        
        <div class="image-box effect-3">
            <img src="https://via.placeholder.com/400/e74c3c/ffffff?text=Image+3" alt="Image 3">
            <div class="image-label">Sepia</div>
        </div>
        
        <div class="image-box effect-4">
            <img src="https://via.placeholder.com/400/f39c12/ffffff?text=Image+4" alt="Image 4">
            <div class="image-label">Saturate</div>
        </div>
        
        <div class="image-box effect-5">
            <img src="https://via.placeholder.com/400/9b59b6/ffffff?text=Image+5" alt="Image 5">
            <div class="image-label">Hue Rotate</div>
        </div>
        
        <div class="image-box effect-6">
            <img src="https://via.placeholder.com/400/1abc9c/ffffff?text=Image+6" alt="Image 6">
            <div class="image-label">Blend Mode</div>
        </div>
    </div>
</body>
</html>
```

</details>

---

## 9. Projet du Module : Portfolio Moderne avec CSS Avancé

### 9.1 Cahier des Charges

**Créer un portfolio utilisant toutes les techniques CSS avancées :**

**Spécifications techniques :**
- Variables CSS (thème complet)
- Glassmorphism sections
- Filters sur images
- clip-path formes custom
- Gradients complexes
- mix-blend-mode texte
- backdrop-filter navigation
- Animations smooth
- Dark mode toggle
- Code CSS validé

### 9.2 Solution Complète

<details>
<summary>Voir la solution complète du projet (HTML)</summary>

```html
<!DOCTYPE html>
<html lang="fr" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Moderne - CSS Avancé</title>
    <link rel="stylesheet" href="portfolio-advanced.css">
</head>
<body>
    <!-- Navigation Glassmorphism -->
    <nav class="nav-glass">
        <div class="container nav-container">
            <a href="#" class="logo">Portfolio</a>
            
            <ul class="nav-links">
                <li><a href="#about">À propos</a></li>
                <li><a href="#work">Travaux</a></li>
                <li><a href="#skills">Compétences</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
            
            <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
                <span class="theme-icon"></span>
            </button>
        </div>
    </nav>
    
    <!-- Hero Section avec Gradient -->
    <section class="hero">
        <div class="hero-bg"></div>
        <div class="container hero-content">
            <h1 class="hero-title">
                <span class="gradient-text">Designer</span> &
                <span class="gradient-text">Developer</span>
            </h1>
            <p class="hero-subtitle">
                Créateur d'expériences digitales modernes et performantes
            </p>
            <a href="#work" class="btn-primary">Voir mes travaux</a>
        </div>
    </section>
    
    <!-- About Section Glass -->
    <section class="about" id="about">
        <div class="container">
            <div class="about-grid">
                <div class="about-image">
                    <div class="image-shape"></div>
                </div>
                
                <div class="about-content glass-card">
                    <h2>À propos</h2>
                    <p>
                        Passionné par le design et le développement web,
                        je crée des interfaces modernes utilisant les dernières
                        technologies CSS et JavaScript.
                    </p>
                    <p>
                        Spécialisé en animations performantes, glassmorphism,
                        et design systems scalables.
                    </p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Work Section -->
    <section class="work" id="work">
        <div class="container">
            <h2 class="section-title">
                <span class="gradient-text">Mes Travaux</span>
            </h2>
            
            <div class="work-grid">
                <div class="work-item">
                    <div class="work-image">
                        <img src="https://via.placeholder.com/600x400/3498db/ffffff?text=Projet+1" alt="Projet 1">
                        <div class="work-overlay">
                            <h3>E-commerce Platform</h3>
                            <p>React, Node.js, MongoDB</p>
                        </div>
                    </div>
                </div>
                
                <div class="work-item">
                    <div class="work-image">
                        <img src="https://via.placeholder.com/600x400/2ecc71/ffffff?text=Projet+2" alt="Projet 2">
                        <div class="work-overlay">
                            <h3>Dashboard Analytics</h3>
                            <p>Vue.js, D3.js, Firebase</p>
                        </div>
                    </div>
                </div>
                
                <div class="work-item">
                    <div class="work-image">
                        <img src="https://via.placeholder.com/600x400/e74c3c/ffffff?text=Projet+3" alt="Projet 3">
                        <div class="work-overlay">
                            <h3>Mobile App Design</h3>
                            <p>Figma, React Native</p>
                        </div>
                    </div>
                </div>
                
                <div class="work-item">
                    <div class="work-image">
                        <img src="https://via.placeholder.com/600x400/f39c12/ffffff?text=Projet+4" alt="Projet 4">
                        <div class="work-overlay">
                            <h3>SaaS Landing Page</h3>
                            <p>HTML, CSS, Animations</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Skills Section -->
    <section class="skills" id="skills">
        <div class="container">
            <h2 class="section-title gradient-text">Compétences</h2>
            
            <div class="skills-grid">
                <div class="skill-card glass-card">
                    <div class="skill-icon">🎨</div>
                    <h3>Design</h3>
                    <p>UI/UX, Figma, Adobe XD</p>
                </div>
                
                <div class="skill-card glass-card">
                    <div class="skill-icon">💻</div>
                    <h3>Frontend</h3>
                    <p>HTML, CSS, JavaScript, React</p>
                </div>
                
                <div class="skill-card glass-card">
                    <div class="skill-icon">⚙️</div>
                    <h3>Backend</h3>
                    <p>Node.js, Python, MongoDB</p>
                </div>
                
                <div class="skill-card glass-card">
                    <div class="skill-icon">📱</div>
                    <h3>Mobile</h3>
                    <p>React Native, Flutter</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Contact Section -->
    <section class="contact" id="contact">
        <div class="container">
            <div class="contact-content glass-card">
                <h2>Travaillons ensemble</h2>
                <p>Un projet en tête ? N'hésitez pas à me contacter.</p>
                <a href="mailto:contact@example.com" class="btn-contact">
                    Me contacter
                </a>
            </div>
        </div>
    </section>
    
    <script src="portfolio-advanced.js"></script>
</body>
</html>
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 1/2)</summary>

```css
/* portfolio-advanced.css */

/* ========================================
   VARIABLES CSS
   ======================================== */

:root {
    /* Colors Light */
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #2c3e50;
    --text-secondary: #7f8c8d;
    --border-color: rgba(0, 0, 0, 0.1);
    
    /* Glass effect */
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    /* Gradients */
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --gradient-mesh: 
        radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.3), transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(118, 75, 162, 0.3), transparent 50%);
    
    /* Spacing */
    --space-xs: 8px;
    --space-sm: 16px;
    --space-md: 24px;
    --space-lg: 40px;
    --space-xl: 60px;
    
    /* Typography */
    --font-base: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 1rem;
    --font-size-lg: 1.25rem;
    --font-size-xl: 2rem;
    --font-size-2xl: 3rem;
    
    /* Transitions */
    --transition-fast: 0.2s ease;
    --transition-normal: 0.3s ease;
    --transition-slow: 0.6s ease;
}

[data-theme="dark"] {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --border-color: rgba(255, 255, 255, 0.1);
    
    --glass-bg: rgba(0, 0, 0, 0.3);
    --glass-border: rgba(255, 255, 255, 0.1);
    --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

/* ========================================
   RESET
   ======================================== */

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: var(--font-base);
    font-size: var(--font-size-base);
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--bg-primary);
    transition: background-color var(--transition-normal), color var(--transition-normal);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--space-md);
}

/* ========================================
   NAVIGATION GLASSMORPHISM
   ======================================== */

.nav-glass {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: var(--glass-bg);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid var(--glass-border);
    z-index: 1000;
    transition: all var(--transition-normal);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 80px;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-decoration: none;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: var(--space-lg);
}

.nav-links a {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color var(--transition-fast);
    position: relative;
}

.nav-links a::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--gradient-primary);
    transition: width var(--transition-normal);
}

.nav-links a:hover::after {
    width: 100%;
}

.theme-toggle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    cursor: pointer;
    transition: all var(--transition-normal);
    display: flex;
    align-items: center;
    justify-content: center;
}

.theme-toggle:hover {
    transform: rotate(180deg);
}

.theme-icon::before {
    content: '☀️';
    font-size: 1.5rem;
}

[data-theme="dark"] .theme-icon::before {
    content: '🌙';
}

/* ========================================
   HERO SECTION
   ======================================== */

.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    padding-top: 80px;
}

.hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--gradient-primary);
    z-index: -2;
}

.hero-bg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--gradient-mesh);
    z-index: -1;
}

.hero-content {
    text-align: center;
    z-index: 1;
}

.hero-title {
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 800;
    margin-bottom: var(--space-md);
    color: white;
}

.gradient-text {
    background: linear-gradient(45deg, #ffffff, rgba(255, 255, 255, 0.5));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: clamp(1.1rem, 3vw, 1.5rem);
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: var(--space-lg);
}

.btn-primary {
    display: inline-block;
    padding: 18px 40px;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all var(--transition-normal);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

/* ========================================
   GLASS CARD COMPONENT
   ======================================== */

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px) saturate(180%);
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    padding: var(--space-lg);
    box-shadow: var(--glass-shadow);
    transition: all var(--transition-normal);
}

.glass-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

/* ========================================
   ABOUT SECTION
   ======================================== */

.about {
    padding: var(--space-xl) 0;
    background-color: var(--bg-secondary);
}

.about-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-xl);
    align-items: center;
}

.about-image {
    position: relative;
    height: 500px;
}

.image-shape {
    width: 100%;
    height: 100%;
    background: var(--gradient-secondary);
    clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
    animation: morph 8s ease-in-out infinite;
}

@keyframes morph {
    0%, 100% {
        clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
    }
    50% {
        clip-path: polygon(20% 10%, 80% 10%, 90% 30%, 90% 70%, 80% 90%, 20% 90%, 10% 70%, 10% 30%);
    }
}

.about-content h2 {
    font-size: var(--font-size-xl);
    margin-bottom: var(--space-md);
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.about-content p {
    margin-bottom: var(--space-sm);
    color: var(--text-secondary);
    line-height: 1.8;
}
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 2/2)</summary>

```css
/* ========================================
   WORK SECTION
   ======================================== */

.work {
    padding: var(--space-xl) 0;
}

.section-title {
    text-align: center;
    font-size: var(--font-size-2xl);
    margin-bottom: var(--space-xl);
}

.work-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-lg);
}

.work-item {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    aspect-ratio: 3 / 2;
}

.work-image {
    width: 100%;
    height: 100%;
    position: relative;
}

.work-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all var(--transition-slow);
}

.work-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--gradient-primary);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: var(--space-md);
    opacity: 0;
    transition: opacity var(--transition-normal);
}

.work-item:hover .work-overlay {
    opacity: 1;
}

.work-item:hover .work-image img {
    filter: blur(5px) brightness(0.5);
    transform: scale(1.1);
}

.work-overlay h3 {
    color: white;
    font-size: 1.8rem;
    margin-bottom: var(--space-sm);
}

.work-overlay p {
    color: rgba(255, 255, 255, 0.9);
}

/* ========================================
   SKILLS SECTION
   ======================================== */

.skills {
    padding: var(--space-xl) 0;
    background-color: var(--bg-secondary);
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-lg);
}

.skill-card {
    text-align: center;
}

.skill-icon {
    font-size: 4rem;
    margin-bottom: var(--space-md);
    filter: grayscale(0.3);
    transition: all var(--transition-normal);
}

.skill-card:hover .skill-icon {
    filter: grayscale(0);
    transform: scale(1.2) rotate(5deg);
}

.skill-card h3 {
    font-size: 1.5rem;
    margin-bottom: var(--space-sm);
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.skill-card p {
    color: var(--text-secondary);
}

/* ========================================
   CONTACT SECTION
   ======================================== */

.contact {
    padding: var(--space-xl) 0;
}

.contact-content {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.contact-content h2 {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--space-md);
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.contact-content p {
    color: var(--text-secondary);
    margin-bottom: var(--space-lg);
    font-size: var(--font-size-lg);
}

.btn-contact {
    display: inline-block;
    padding: 18px 50px;
    background: var(--gradient-primary);
    color: white;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all var(--transition-normal);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.btn-contact:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 768px) {
    .nav-links {
        display: none;
    }
    
    .about-image {
        height: 300px;
    }
    
    .work-grid {
        grid-template-columns: 1fr;
    }
}

/* ========================================
   ACCESSIBILITY
   ======================================== */

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

@media (prefers-contrast: high) {
    :root {
        --glass-bg: rgba(255, 255, 255, 0.95);
        --glass-border: rgba(0, 0, 0, 0.3);
    }
    
    [data-theme="dark"] {
        --glass-bg: rgba(0, 0, 0, 0.95);
        --glass-border: rgba(255, 255, 255, 0.3);
    }
}
```

</details>

<details>
<summary>Voir la solution complète du projet (JavaScript)</summary>

```javascript
// portfolio-advanced.js

// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Charger thème sauvegardé
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
}

// Smooth scroll
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

// Intersection Observer pour animations scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observer tous éléments avec classe 'fade-in'
document.querySelectorAll('.glass-card, .work-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
```

</details>

### 9.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Variables CSS complètes (couleurs, spacing, typography)
- [ ] Thème light/dark fonctionnel
- [ ] Navigation glassmorphism (backdrop-filter)
- [ ] Hero avec gradient complexe
- [ ] Texte gradient (background-clip: text)
- [ ] Glass cards avec backdrop-filter
- [ ] clip-path animation (morph)
- [ ] Images avec filters hover
- [ ] mix-blend-mode sur overlay
- [ ] Gradients multi-couleurs (linear, radial)
- [ ] Transitions smooth partout
- [ ] Responsive complet
- [ ] prefers-color-scheme support
- [ ] prefers-reduced-motion support
- [ ] Code CSS validé W3C
- [ ] Performance optimale (GPU-accelerated)

---

## 10. Best Practices CSS Avancé

### 10.1 Règles d'Or

```css
/* 1. Utiliser variables CSS pour maintenabilité */

/* ✅ BIEN */
:root {
    --color-primary: #3498db;
}

.button {
    background-color: var(--color-primary);
}

/* ❌ ÉVITER */
.button {
    background-color: #3498db;
}
/* Répété 50 fois = cauchemar changement couleur */

/* 2. Glassmorphism nécessite fond */

/* ✅ BIEN (fond derrière) */
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

.glass {
    backdrop-filter: blur(10px);
}

/* ❌ MAL (fond blanc uni) */
body {
    background: white;
}

.glass {
    backdrop-filter: blur(10px);  /* Aucun effet visible */
}

/* 3. Filters performance */

/* ✅ Performant */
.element {
    filter: blur(5px);  /* GPU-accelerated */
}

/* ⚠️ Attention mobile */
.element {
    filter: blur(20px) saturate(2) contrast(1.5);
    /* Trop de filters = lag mobile */
}

/* 4. clip-path pas de fallback */

/* Toujours border-radius fallback */
.element {
    border-radius: 20px;
    clip-path: polygon(...);
}

/* 5. Gradients readability */

/* ✅ Lisible */
.element {
    background: linear-gradient(
        to right,
        #3498db 0%,
        #2ecc71 50%,
        #e74c3c 100%
    );
}

/* ❌ Illisible */
.element {
    background: linear-gradient(to right,#3498db 0%,#2ecc71 50%,#e74c3c 100%);
}
```

### 10.2 Support Navigateurs

```css
/* Toujours vérifier support */

/* backdrop-filter : Chrome 76+, Safari 9+ */
@supports (backdrop-filter: blur(10px)) {
    .glass {
        backdrop-filter: blur(10px);
    }
}

@supports not (backdrop-filter: blur(10px)) {
    .glass {
        background: rgba(255, 255, 255, 0.9);
    }
}

/* clip-path : Chrome 55+, Firefox 54+, Safari 9.1+ */
@supports (clip-path: circle(50%)) {
    .element {
        clip-path: circle(50%);
    }
}

/* aspect-ratio : Chrome 88+, Firefox 89+, Safari 15+ */
@supports (aspect-ratio: 1 / 1) {
    .element {
        aspect-ratio: 16 / 9;
    }
}

@supports not (aspect-ratio: 1 / 1) {
    .element {
        /* Padding hack fallback */
        position: relative;
        padding-bottom: 56.25%;
    }
}
```

---

## 11. Checkpoint de Progression

### À la fin de ce Module 14, vous maîtrisez :

**Variables CSS :**

- [x] Déclaration et utilisation (var())
- [x] Scope (:root, local)
- [x] Conventions nommage
- [x] Thèmes dynamiques (light/dark)
- [x] calc() avec variables
- [x] JavaScript interaction

**Filters CSS :**

- [x] 10+ filters (blur, brightness, contrast, etc.)
- [x] Combinaison filters
- [x] backdrop-filter (glassmorphism)
- [x] Performance GPU

**Clip-path :**

- [x] Formes de base (circle, ellipse, inset, polygon)
- [x] Formes complexes (hexagone, étoile)
- [x] SVG paths
- [x] Animations clip-path

**Blend Modes :**

- [x] mix-blend-mode (multiply, screen, overlay, etc.)
- [x] background-blend-mode
- [x] Effets créatifs

**Gradients :**

- [x] Linear gradients complexes
- [x] Radial gradients
- [x] Conic gradients
- [x] Repeating gradients
- [x] Gradients combinés

**Masks :**

- [x] mask-image
- [x] mask properties (size, position, repeat)
- [x] Gradient masks

**Autres :**

- [x] object-fit, object-position
- [x] shape-outside
- [x] aspect-ratio

**Best practices :**

- [x] Règles d'or CSS avancé
- [x] Support navigateurs
- [x] Fallbacks

### Félicitations Formation HTML+CSS Complète

**Vous avez maintenant terminé 14 modules exhaustifs !**

**Maîtrise complète :**

- HTML5 sémantique professionnel
- CSS fondamental (Box Model, Sélecteurs)
- Layouts modernes (Flexbox, Grid)
- Responsive Design complet
- Animations CSS performantes
- CSS Avancé (Variables, Filters, Clip-path, Blend modes, Gradients)

**Niveau atteint : Expert CSS Moderne**

**Prochaine étape :**

- Module 15 : Projet Final Intégral (site complet professionnel)

---

**Module 14 Terminé - Bravo ! 🎉**

**Statistiques Module 14 :**

- 1 projet complet (Portfolio moderne avec tout CSS avancé)
- 3 exercices progressifs avec solutions
- Variables CSS maîtrisées
- Filters et backdrop-filter glassmorphism
- Clip-path formes complexes
- Blend modes professionnels
- Gradients avancés (linear, radial, conic)
- Masks CSS
- Best practices CSS avancé

**Félicitations pour cette maîtrise complète de CSS Avancé ! 🚀**
