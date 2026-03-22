---
description: "Responsive Design : viewport, media queries mobile-first, breakpoints, images adaptatives, typographie fluide, navigation CSS"
icon: lucide/book-open-check
tags: ["CSS", "RESPONSIVE", "MEDIA-QUERIES", "MOBILE-FIRST", "BREAKPOINTS", "CLAMP"]
---

# Responsive Design

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="1.1"
  data-time="5-6 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique"
    _Imaginez un **journal papier professionnel** conçu pour exister en trois formats simultanément : l'édition de poche pour le métro, le format standard pour la table du petit-déjeuner, et l'affiche murale pour les espaces publics. Le même contenu, la même maquette éditoriale, mais des proportions, des colonnes et des typographies qui s'ajustent intelligemment selon le support. **Le Responsive Design**, c'est exactement ce principe appliqué au web : un seul code HTML, un seul site, qui s'adapte automatiquement à tous les écrans — du smartphone au moniteur 4K._

Avant l'ère du Responsive (pré-2010 environ), la norme était de maintenir deux sites distincts : une version mobile (`m.site.com`) et une version desktop (`site.com`). Cela signifiait deux bases de code, deux fois les bugs, deux fois la maintenance.

Le Responsive Design met fin à cette dualité avec trois mécanismes fondamentaux :

- **La grille fluide** — les largeurs exprimées en pourcentages plutôt qu'en pixels fixes
- **Les images flexibles** — les médias qui s'étirent ou se contractent dans leur contenant
- **Les media queries** — les règles CSS conditionnelles qui s'appliquent selon le contexte d'affichage

!!! info "Pourquoi c'est incontournable aujourd'hui"
    La majorité du trafic web mondial provient aujourd'hui des appareils mobiles. Google applique depuis 2019 une politique de **Mobile-First Indexing** : c'est la version mobile d'un site qui est indexée et référencée en priorité. Un site non responsive est pénalisé dans les résultats de recherche.

<br>

---

## Le viewport

!!! note "Rappel — CSS Fondamentaux"
    Le viewport a été introduit dans le module CSS Fondamentaux. Ce rappel est volontairement court. Si vous avez besoin de revenir sur les bases, consultez le module [Introduction CSS](../css-fondamental/01-introduction-css.md).

### Qu'est-ce que le viewport ?

Le **viewport** est la zone visible du navigateur sur l'écran de l'utilisateur. Sa largeur est différente selon l'appareil : environ 390 px sur un iPhone récent, 768 px sur une tablette, 1440 px sur un laptop.

Sans instruction particulière, un navigateur mobile affiche les pages web comme si l'écran mesurait 980 px de large, puis réduit l'ensemble pour le faire tenir dans la surface physique de l'écran. Le résultat : une page miniaturisée, illisible sans zoom.

La balise `<meta name="viewport">` corrige ce comportement.

```html title="HTML — Déclaration obligatoire du viewport"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">

    <!-- Indique au navigateur d'utiliser la largeur réelle de l'écran -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Mon site responsive</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Contenu -->
</body>
</html>
```

_`width=device-width` force le viewport à correspondre à la largeur physique de l'appareil. `initial-scale=1.0` définit le zoom initial à 100 %, sans agrandissement ni réduction._

!!! warning "Ne jamais bloquer le zoom utilisateur"
    Certains développeurs ajoutent `user-scalable=no` ou `maximum-scale=1` pour empêcher le zoom. C'est une mauvaise pratique sévère : elle rend le contenu inaccessible aux personnes malvoyantes. Ne l'utilisez jamais.

---

## Media queries

Les **media queries** sont des conditions CSS : elles permettent d'appliquer des règles uniquement lorsque certaines caractéristiques de l'appareil sont vérifiées.

### Syntaxe fondamentale

```css title="CSS — Structure d'une media query"
/* Règles qui s'appliquent toujours */
.container {
    padding: 1rem;
}

/* Règles qui s'appliquent uniquement si la largeur de fenêtre
   est supérieure ou égale à 768 px */
@media (min-width: 768px) {
    .container {
        padding: 2rem;
    }
}
```

_La condition `(min-width: 768px)` est vraie dès que la fenêtre atteint 768 px. En dessous, la première règle s'applique ; au-dessus, la seconde prend le relais._

### Mobile-first vs Desktop-first

Il existe deux approches opposées pour organiser les media queries.

=== "Mobile-First (recommandé)"

    !!! info "On écrit **d'abord le CSS pour les petits écrans**, puis on ajoute des règles pour les écrans plus larges avec `min-width`."

    ```css title="CSS — Approche mobile-first"
    /* Base : mobile (aucune media query) */
    .nav {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    /* À partir de 768 px : tablette et plus */
    @media (min-width: 768px) {
        .nav {
            flex-direction: row;
            gap: 2rem;
        }
    }

    /* À partir de 1024 px : desktop */
    @media (min-width: 1024px) {
        .nav {
            gap: 3rem;
        }
    }
    ```

    _Le CSS de base est minimal et s'applique à tous les appareils. Les variations pour les grands écrans s'accumulent progressivement._

=== "Desktop-First (à éviter)"

    !!! info "On écrit d'abord pour les grands écrans, puis on réduit avec `max-width`."

    ```css title="CSS — Approche desktop-first"
    /* Base : desktop */
    .nav {
        display: flex;
        flex-direction: row;
        gap: 3rem;
    }

    /* En dessous de 1024 px : tablette */
    @media (max-width: 1023px) {
        .nav {
            gap: 2rem;
        }
    }

    /* En dessous de 768 px : mobile */
    @media (max-width: 767px) {
        .nav {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
    ```

    _Cette approche oblige à "défaire" les styles desktop pour le mobile. Elle produit un CSS plus lourd et moins maintenable._

!!! tip "Pourquoi mobile-first est la norme"
    Le mobile-first est recommandé par Google, MDN et l'ensemble de la communauté frontend depuis 2012. Il correspond à la réalité du trafic (_majorité mobile_) et produit un CSS plus léger pour les petits écrans — précisément là où la performance est la plus critique.

### Media features courantes

```css title="CSS — Conditions media query autres que la largeur"
/* Hauteur de la fenêtre */
@media (min-height: 600px) { }

/* Orientation */
@media (orientation: landscape) { }
@media (orientation: portrait) { }

/* Résolution (écrans Retina) */
@media (min-resolution: 2dppx) { }

/* Préférences système */
/* pour les personnes qui préfèrent le mode sombre */
@media (prefers-color-scheme: dark) { }
/* pour les personnes qui ne supportent pas les animations */
@media (prefers-reduced-motion: reduce) { } 

/* Combiner plusieurs conditions */
@media (min-width: 768px) and (orientation: landscape) { }
```

_Les préférences système (`prefers-color-scheme`, `prefers-reduced-motion`) permettent de respecter les choix d'accessibilité de l'utilisateur directement en CSS, sans JavaScript._

<br>

---

## Breakpoints

Les **breakpoints** sont les largeurs seuils auxquelles le design change. **Il n'existe pas de breakpoints universels et immuables** : ils doivent idéalement s'adapter au contenu.

!!! quote "_En pratique, la communauté frontend s'est alignée sur des valeurs de référence._"

### Tableau de référence 2026

| Nom | Valeur | Appareils ciblés |
|-----|--------|-----------------|
| `xs` | < 480 px | Très petits mobiles, anciens Android |
| `sm` | ≥ 480 px | Mobiles standard (iPhone, Android récents) |
| `md` | ≥ 768 px | Tablettes portrait |
| `lg` | ≥ 1024 px | Tablettes paysage, petits laptops |
| `xl` | ≥ 1280 px | Laptops et desktops standard |
| `2xl` | ≥ 1536 px | Grands moniteurs |
| `3xl` | ≥ 1920 px | Très grands écrans, TV |

!!! note "Origine de ces valeurs"
    Ces breakpoints sont ceux de **Tailwind[^1] CSS v3/v4**, la référence utility-first la plus utilisée en 2024-2026. Bootstrap 5[^2] utilise des valeurs proches (**576** / **768** / **992** / **1200** / **1400** px). **MDN**[^3] recommande de choisir les breakpoints **là où votre contenu se casse**, pas en fonction des appareils.

### Mise en pratique

```css title="CSS — Grille responsive avec les breakpoints de référence (Mobile-first)"
/* Mobile (base) : 1 colonne */
.grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

/* Tablette (md ≥ 768 px) : 2 colonnes */
@media (min-width: 768px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }
}

/* Desktop (xl ≥ 1280 px) : 4 colonnes */
@media (min-width: 1280px) {
    .grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;
    }
}
```

_On part d'une colonne (mobile), on passe à deux (tablette), puis à quatre (desktop). Chaque étape est déclenché par un breakpoint `min-width`._

<br>

---

## Typographie fluide

### rem et vw — rappel

!!! note "Rappel — CSS Fondamentaux"
    `rem` (root em) et `vw` (viewport width) ont été couverts dans le module [Introduction CSS](../css-fondamental/01-introduction-css.md). Bref rappel ici.

- `1rem` = taille de police racine (par défaut 16 px dans la plupart des navigateurs)
- `1vw` = 1 % de la largeur du viewport

```css title="CSS — rem et vw en responsive"
/* Taille de base définie en rem : scalable */
h1 { font-size: 2rem; }      /* 32 px par défaut */
p  { font-size: 1rem; }      /* 16 px par défaut */

/* vw : texte qui grandit avec la fenêtre */
.hero-title { font-size: 5vw; }  /* 5 % de 1280 px = 64 px sur desktop */
```

_En revanche, `vw` seul est problématique : sur mobile 320 px, `5vw` donne 16 px (acceptable), mais sur très grand écran 2560 px, il donne 128 px (excessif). C'est là qu'intervient `clamp()`._

### clamp() — typographie vraiment fluide

`clamp()` est une fonction CSS qui contraint une valeur entre un **minimum**, une **valeur idéale**, et un **maximum**. Elle évite les extrêmes trop petits ou trop grands.

```css title="CSS — Syntaxe de clamp()"
/* clamp(minimum, valeur-idéale, maximum) */
font-size: clamp(1rem, 2.5vw, 2rem);

/*
  → sur mobile 320 px  : 2.5vw = 8 px → forcé à 1rem (16 px)
  → sur laptop 1280 px : 2.5vw = 32 px → trop grand, forcé à 2rem (32 px)
  → sur écran 800 px   : 2.5vw = 20 px → dans la plage, appliqué tel quel
*/
```

_`clamp()` est la méthode moderne pour créer une typographie fluide sans `@media` : la taille s'adapte en continu entre le minimum garanti et le maximum autorisé._

```css title="CSS — Système typographique complet avec clamp()"
:root {
    /* Titres : grandissent de manière fluide entre mobile et desktop */
    --fs-h1: clamp(2rem, 5vw, 3.5rem);    /* 32 px → 56 px */
    --fs-h2: clamp(1.5rem, 3.5vw, 2.5rem); /* 24 px → 40 px */
    --fs-h3: clamp(1.25rem, 2.5vw, 2rem);  /* 20 px → 32 px */

    /* Corps : stable sur tous les écrans */
    --fs-body: clamp(1rem, 1.25vw, 1.125rem); /* 16 px → 18 px */

    /* Petits textes */
    --fs-small: clamp(0.875rem, 1vw, 1rem); /* 14 px → 16 px */
}

h1 { font-size: var(--fs-h1); }
h2 { font-size: var(--fs-h2); }
h3 { font-size: var(--fs-h3); }
p  { font-size: var(--fs-body); }
```

_Ce système garantit que la typographie reste lisible sur mobile (minimum garanti) et élégante sur grand écran (maximum maîtrisé), sans une seule media query._

!!! tip "Outil de calcul clamp()"
    Le site [utopia.fyi](https://utopia.fyi) permet de générer des valeurs `clamp()` optimales en définissant simplement vos tailles de police idéales sur mobile et desktop.

<br>

---

## Images responsives

### Largeur fluide

La règle minimale pour rendre une image responsive :

```css title="CSS — Image fluide de base"
img {
    max-width: 100%;  /* L'image ne déborde jamais de son conteneur */
    height: auto;     /* Le ratio est préservé automatiquement */
    display: block;   /* Élimine l'espace blanc sous l'image (inline par défaut) */
}
```

_Cette règle s'applique globalement à toutes les images dans la plupart des feuilles de style modernes._

### L'attribut srcset

`srcset` permet de fournir plusieurs versions d'une image. Le navigateur choisit automatiquement la plus adaptée selon la taille d'affichage et la densité de pixels.

```html title="HTML — srcset avec descripteurs de largeur (w)"
<img
    src="photo-800.jpg"
    srcset="
        photo-400.jpg  400w,
        photo-800.jpg  800w,
        photo-1200.jpg 1200w
    "
    sizes="
        (max-width: 600px) 100vw,
        (max-width: 1024px) 50vw,
        800px
    "
    alt="Paysage montagneux au lever du soleil"
    loading="lazy"
    width="800"
    height="533"
>
```

_`srcset` liste les fichiers disponibles avec leur largeur réelle. `sizes` indique au navigateur la taille d'affichage prévue selon le contexte. Le navigateur fait le calcul et télécharge uniquement le fichier dont il a besoin — ni plus grand, ni plus petit._

!!! note "Attributs width et height obligatoires"
    Toujours spécifier `width` et `height` en HTML. Cela permet au navigateur de **réserver l'espace** avant que l'image soit chargée, évitant les sauts de mise en page (CLS — Cumulative Layout Shift).

!!! warning "loading="lazy" — quand l'utiliser"
    `loading="lazy"` reporte le chargement d'une image jusqu'à ce qu'elle soit proche du viewport. Ne l'utilisez **jamais** sur les images au-dessus de la ligne de flottaison (hero, logo) : cela ralentirait leur affichage, ce qui nuit aux performances Lighthouse[^4].

### L'élément `<picture>`

`<picture>` va plus loin : il permet de fournir des **images différentes** selon le contexte (format, orientation, taille) et non seulement des résolutions différentes.

```html title="HTML — picture avec formats modernes et fallback"
<picture>
    <!-- Format AVIF : meilleure compression, support limité -->
    <source
        type="image/avif"
        srcset="photo-400.avif 400w, photo-800.avif 800w"
        sizes="(max-width: 600px) 100vw, 50vw"
    >

    <!-- Format WebP : bonne compression, support large -->
    <source
        type="image/webp"
        srcset="photo-400.webp 400w, photo-800.webp 800w"
        sizes="(max-width: 600px) 100vw, 50vw"
    >

    <!-- Fallback JPEG pour navigateurs anciens (toujours présent) -->
    <img
        src="photo-800.jpg"
        alt="Paysage montagneux au lever du soleil"
        width="800"
        height="533"
        loading="lazy"
    >
</picture>
```

_Le navigateur parcourt les `<source>` dans l'ordre et utilise le premier format qu'il supporte. Si aucun n'est supporté, il utilise le `<img>` de fallback. Cette stratégie permet de servir des formats modernes (AVIF, WebP) sans rompre la compatibilité._

### object-fit

```css title="CSS — object-fit pour contrôler le remplissage d'un conteneur"
.card-image {
    width: 100%;
    height: 240px;           /* Hauteur fixe */
    object-fit: cover;       /* L'image remplit le conteneur sans se déformer */
    object-position: center; /* Centrage du point focal */
}
```

_`object-fit: cover` fonctionne comme `background-size: cover` mais pour les éléments `<img>`. L'image est rognée pour remplir le conteneur, en préservant son ratio._

| Valeur | Comportement |
|--------|-------------|
| `fill` | Étire l'image pour remplir (déforme le ratio) |
| `contain` | Affiche l'image entière avec des bandes vides |
| `cover` | Remplit le conteneur en rognant (recommandé pour les cartes) |
| `none` | Taille originale, sans mise à l'échelle |
| `scale-down` | Applique `contain` ou `none`, selon ce qui est le plus petit |

<br>

---

## Flexbox et Grid en responsive

!!! note "Ces techniques ont été couvertes dans les modules précédents"
    Flexbox et CSS Grid ont été étudiés en profondeur dans [Layout Modern — Flexbox](../layout-modern/01-flexbox-css.md) et [Layout Modern — CSS Grid](../layout-modern/02-grid-css.md).<br>**Ce module n'y revient pas.**

    En responsive, la règle pratique est simple :

    - **Flexbox** → navigation, en-têtes, cartes en ligne, composants 1D
    - **Grid** → mises en page 2D, sections, galeries

    La combinaison des deux avec des media queries ou `auto-fit` / `auto-fill` couvre la quasi-totalité des besoins adaptatifs.

<br>

---

## Navigation responsive — CSS uniquement

La navigation hamburger est un pattern universel sur mobile. Il est possible de l'implémenter en **CSS pur**, sans JavaScript, grâce à l'état `:checked` d'une case à cocher invisible.

### Le principe checkbox hack

```html title="HTML — Structure de la navigation hamburger"
<header class="site-header">

    <!-- Case à cocher cachée : l'interrupteur CSS -->
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">

    <!-- Label cliquable : le bouton hamburger visible -->
    <label for="nav-toggle" class="hamburger" aria-label="Ouvrir le menu">
        <span></span>
        <span></span>
        <span></span>
    </label>

    <!-- Logo -->
    <a href="/" class="logo">MonSite</a>

    <!-- Menu de navigation -->
    <nav class="nav" aria-label="Navigation principale">
        <ul class="nav-list">
            <li><a href="/">Accueil</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/portfolio">Portfolio</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
    </nav>

</header>
```

```css title="CSS — Navigation hamburger complète sans JavaScript"
/* =======================================================
 * Réinitialisation de la case à cocher
 * ======================================================= */
.nav-toggle {
    display: none; /* Invisible mais fonctionnelle */
}

/* =======================================================
 * Structure header
 * ======================================================= */
.site-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background-color: #1a1a2e;
    position: relative;
}

/* =======================================================
 * Bouton hamburger (3 barres)
 * ======================================================= */
.hamburger {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 0.5rem;

    /* Zone de clic suffisante (accessibilité) */
    min-width: 44px;
    min-height: 44px;
    justify-content: center;
}

.hamburger span {
    display: block;
    width: 24px;
    height: 2px;
    background-color: #ffffff;

    /* Transition pour l'animation croix */
    transition: transform 0.3s ease, opacity 0.3s ease;
}

/* =======================================================
 * Navigation — fermée sur mobile (base)
 * ======================================================= */
.nav {
    display: none;           /* Cachée par défaut */
    position: absolute;
    top: 100%;               /* Juste sous le header */
    left: 0;
    right: 0;
    background-color: #1a1a2e;
    padding: 1rem 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.nav-list a {
    color: #ffffff;
    text-decoration: none;
    font-size: 1rem;
    padding: 0.5rem 0;
    display: block;
    transition: color 0.2s ease;
}

.nav-list a:hover {
    color: #667eea;
}

/* =======================================================
 * Navigation ouverte : quand la checkbox est cochée
 * ======================================================= */
.nav-toggle:checked ~ .nav {
    display: block;
}

/* Animation croix sur les barres du hamburger */
.nav-toggle:checked ~ .hamburger span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
}

.nav-toggle:checked ~ .hamburger span:nth-child(2) {
    opacity: 0;
}

.nav-toggle:checked ~ .hamburger span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
}

/* =======================================================
 * Desktop (≥ 1024 px) : navigation horizontale
 * ======================================================= */
@media (min-width: 1024px) {

    /* Hamburger caché sur desktop */
    .hamburger {
        display: none;
    }

    /* Navigation toujours visible */
    .nav {
        display: block;
        position: static;    /* Sort du positionnement absolu */
        background: none;
        padding: 0;
        border: none;
    }

    /* Liens en ligne */
    .nav-list {
        flex-direction: row;
        gap: 2rem;
        align-items: center;
    }
}
```

_Le sélecteur `~` (sélecteur de frères généraux) est la clé du mécanisme : il cible tous les éléments frères qui suivent la checkbox dans le DOM. Quand la checkbox passe à l'état `:checked`, le sélecteur `.nav-toggle:checked ~ .nav` devient actif et affiche le menu._

!!! warning "Limite de cette approche"
    Le checkbox hack fonctionne parfaitement pour la majorité des cas. Il présente une limitation : il ne permet pas de fermer le menu en cliquant en dehors de lui. Cette fonctionnalité nécessite JavaScript, qui sera abordé dans le module dédié.

<br>

---

## Performance mobile

??? abstract "Bonnes pratiques de performance responsive"

    **Éviter les ressources inutiles sur mobile**

    ```css title="CSS — Masquer les assets non nécessaires sur mobile"
    /* L'image décorative de fond n'est chargée que sur desktop */
    .hero {
        /* Pas de background sur mobile */
    }

    @media (min-width: 1024px) {
        .hero {
            background-image: url('decoration.jpg');
        }
    }
    ```

    **Tailles de cibles tactiles**

    Les boutons et liens doivent mesurer au moins **44 × 44 px** pour être utilisables au doigt (recommandation Apple, Google, WCAG 2.5.5).

    ```css title="CSS — Taille minimale des cibles tactiles"
    .btn,
    nav a,
    .icon-button {
        min-width: 44px;
        min-height: 44px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    ```

    **Container queries — responsive par composant**

    CSS moderne (2023+) permet de conditionner les styles à la taille du *conteneur*, et non du viewport.

    ```css title="CSS — Container queries"
    /* Déclarer un conteneur */
    .card-wrapper {
        container-type: inline-size;
        container-name: card;
    }

    /* Styles conditionnels selon la taille du conteneur */
    @container card (min-width: 400px) {
        .card {
            display: grid;
            grid-template-columns: 1fr 2fr;
        }
    }
    ```

    _Les container queries permettent de créer des composants véritablement indépendants qui s'adaptent à leur contexte d'insertion, pas à la taille globale de la fenêtre._

<br>

---

## Tester le responsive

!!! tip "DevTools navigateur"
    Dans Chrome ou Firefox, appuyez sur **F12** → icône de téléphone (mode responsive). Vous pouvez :

    - Simuler les résolutions des appareils courants (iPhone, Pixel, iPad)
    - Tester en mode portrait et paysage
    - Réduire ou agrandir manuellement la fenêtre pour observer les breakpoints
    - Activer la limitation de bande passante pour simuler une connexion mobile

!!! tip "Extensions utiles"
    - **Responsive Viewer** (Chrome) : affiche simultanément plusieurs tailles d'écran
    - **BrowserStack** (payant) : tests sur appareils réels à distance

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le Responsive Design repose sur trois piliers indissociables : **la balise `<meta name="viewport">`** (sans elle, rien ne fonctionne), **les media queries mobile-first** (on part du petit pour aller vers le grand), et **les unités fluides** — `%`, `rem`, `vw`, et surtout `clamp()` — qui permettent à la mise en page de s'adapter en continu sans multiplier les breakpoints.

> Ce module pose les fondations de la mise en page adaptative. La prochaine étape pour mettre en pratique l'ensemble de ces techniques — HTML, CSS Fondamentaux, Flexbox, Grid et Responsive — est le [Projet Final HTML/CSS](../../../projets/html-css-vitrine/index.md).

[^1]: Tailwind CSS est un framework CSS utility-first qui fournit une collection de classes prédéfinies pour le développement web. Vous pouvez le consulter à l'adresse suivante : https://tailwindcss.com/

[^2]: Bootstrap est un framework CSS open-source qui fournit une collection de styles et de composants prédéfinis pour le développement web. Vous pouvez le consulter à l'adresse suivante : https://getbootstrap.com/

[^3]: MDN est une excellente ressource gratuite pour apprendre le développement web. Vous pouvez la consulter à l'adresse suivante : https://developer.mozilla.org/fr/docs/Web/CSS

[^4]: Lighthouse est un outil open-source développé par Google pour améliorer la qualité des pages web. Vous pouvez le consulter à l'adresse suivante : https://developer.chrome.com/docs/lighthouse
