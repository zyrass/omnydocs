---
description: "Astuces CSS modernes : drop-shadow, compteurs, tooltips, scroll animations, scroll-snap, aspect-ratio, object-fit et typographie avancée."
icon: lucide/book-open-check
tags: ["CSS", "BONUS", "DROP-SHADOW", "COUNTERS", "SCROLL", "TYPOGRAPHY", "OBJECT-FIT"]
---

# Pour aller plus loin

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.1"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Art de la Finition"
    Un menuisier crée une bonne table avec du bois massif, des clous et de la colle. Un **maître ébéniste**, lui, ajoute les finitions invisibles qui transforment un meuble fonctionnel en chef-d'œuvre : un ponçage au millimètre, un vernis qui reflète la lumière selon sa courbure, des tiroirs qui coulissent avec un frein de butée.

    Cette section regroupe les "finitions de l'ébéniste" du Web moderne — des fonctionnalités subtiles, souvent méconnues, qui font dire à un utilisateur : "Ce site est vraiment haut de gamme."

Ces techniques natives permettent d'accomplir en pur CSS des effets qui nécessitaient des dizaines de lignes de JavaScript il y a encore quelques années.

<br>

---

## La battle des ombres : `box-shadow` vs `drop-shadow()`

Il existe une confusion fréquente entre ces deux approches. Leur différence fondamentale tient au contour qu'elles analysent.

`box-shadow` projette une ombre depuis les **limites rectangulaires** de la boîte CSS — le Box Model. Peu importe si l'image à l'intérieur est un PNG avec fond transparent : l'ombre sera toujours un rectangle.

`filter: drop-shadow()` analyse les **pixels optiquement opaques** de l'élément et dessine l'ombre exactement sur leur contour. C'est la solution pour les images PNG détourées, les SVG et les formes découpées au `clip-path`.

```css title="CSS - box-shadow vs drop-shadow"
/* Produit un carré d'ombre derrière le PNG, ignorant sa transparence */
.avatar-png-boite {
    box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.5);
}

/* Produit une ombre épousant exactement la silhouette opaque du PNG */
.avatar-png-silhouette {
    filter: drop-shadow(0px 10px 15px rgba(0, 0, 0, 0.5));
}
```

*`drop-shadow()` est également l'ombre correcte pour les éléments découpés avec `clip-path` : `box-shadow` est découpé avec le clip, `drop-shadow()` s'applique après.*

<br>

---

## Contenu généré dynamiquement

Les pseudo-éléments `::before` et `::after` avec la propriété `content` permettent au CSS de créer du texte ou des formes absents du HTML d'origine.

<br>

### Tooltip 100% CSS avec `attr()`

En lisant la valeur d'un attribut HTML via `attr()`, le CSS peut afficher une bulle d'information au survol sans aucun JavaScript ni `<div>` cachée.

```html title="HTML - Attribut de données pour le tooltip"
<button class="btn-tooltip" data-message="Ce dossier sera supprimé définitivement.">
    Supprimer
</button>
```

```css title="CSS - Tooltip via attr() et ::after"
.btn-tooltip {
    position: relative;
}

/* Bulle invisible par défaut, positionnée au-dessus du bouton */
.btn-tooltip::after {
    /* Lit dynamiquement la valeur de l'attribut data-message */
    content: attr(data-message);

    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;

    background: #1a1a2e;
    color: white;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 4px;

    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none; /* Le tooltip ne bloque pas les clics */
}

/* Au survol, la bulle devient visible */
.btn-tooltip:hover::after {
    opacity: 1;
}
```

<br>

### Les Compteurs CSS

Les compteurs CSS permettent de numéroter automatiquement des éléments répétitifs sans écrire manuellement "1.", "2.", "3." dans le HTML.

```css title="CSS - Compteurs automatiques pour les chapitres"
/* 1. Initialiser le compteur à 0 sur le conteneur parent */
body {
    counter-reset: chapitre;
}

/* 2. Incrémenter le compteur à chaque h2 rencontré */
h2 {
    counter-increment: chapitre;
}

/* 3. Afficher la valeur courante avant chaque titre */
h2::before {
    content: "Chapitre " counter(chapitre) " — ";
    color: var(--color-primary);
    font-weight: 500;
}
```

*Les compteurs CSS sont utiles pour les documentations techniques, les tables des matières, les étapes de formulaire et les listes de références bibliographiques.*

<br>

---

## Animations au Scroll

Disponible nativement depuis 2024, `animation-timeline: scroll()` lie une animation `@keyframes` à l'avancement du défilement de la page, sans une ligne de JavaScript.

```css title="CSS - Barre de progression de lecture"
@keyframes avancement-lecture {
    0%   { transform: scaleX(0); }
    100% { transform: scaleX(1); }
}

.scroll-watcher {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background-color: var(--color-primary);
    transform-origin: left;

    /*
        L'animation n'est plus pilotée par une durée (3s),
        mais par la position du défilement vertical de la page.
        scroll() sans argument cible le défilement de la fenêtre.
    */
    animation: avancement-lecture linear;
    animation-timeline: scroll();
}
```

*`animation-timeline` supporte aussi `view()` pour déclencher une animation quand un élément entre dans le viewport — alternative native aux bibliothèques comme AOS.*

!!! info "Support navigateurs"
    `animation-timeline` est disponible dans Chrome 115+, Firefox 110+, Safari 17.2+. En 2025, le support dépasse 88% des utilisateurs. Un polyfill JavaScript reste disponible pour les projets nécessitant une couverture plus large.

<br>

---

## Scroll Snap — défilement magnétique

`scroll-snap` force le défilement à s'aligner sur des points définis, créant un effet "magnétique" entre les sections — sans JavaScript.

```css title="CSS - Galerie avec scroll snap horizontal"
/* Conteneur : déclarer le contexte de snapping */
.galerie-scroll {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    /*
        x         : défilement horizontal
        mandatory : le snapping est forcé après chaque interaction
        proximity : snapping déclenché seulement si l'élément est "proche"
    */
    gap: 1rem;
    padding: 1rem;
    -webkit-overflow-scrolling: touch; /* Fluidité iOS */
}

/* Enfants : définir le point d'accrochage */
.galerie-scroll .diapo {
    scroll-snap-align: start; /* start | center | end */
    flex-shrink: 0;
    width: 80%;
    border-radius: 8px;
}
```

```css title="CSS - Sections plein écran avec scroll snap vertical"
/* Défilement "full-page scroll" sans JavaScript */
.site-wrapper {
    height: 100dvh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
}

.section-plein-ecran {
    height: 100dvh;
    scroll-snap-align: start;
    scroll-snap-stop: always; /* Empêche de sauter plusieurs sections d'un coup */
}
```

<br>

---

## `aspect-ratio` — conserver les proportions

`aspect-ratio` force un élément à maintenir un ratio largeur/hauteur défini, quelle que soit la taille de son conteneur.

```css title="CSS - Aspect ratio pour les médias et composants"
/* Ratio 16/9 pour les vidéos et images embarquées */
.video-wrapper {
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    border-radius: 8px;
}

/* Ratio 1/1 pour les avatars et vignettes carrées */
.avatar {
    width: 48px;
    aspect-ratio: 1;      /* Équivalent à 1 / 1 */
    border-radius: 50%;
    overflow: hidden;
}

/* Ratio pour les cartes produit */
.carte-produit-image {
    width: 100%;
    aspect-ratio: 4 / 3;
    background-color: #f0f4f8; /* Fond pendant le chargement */
}
```

*Avant `aspect-ratio`, la technique du "padding-top hack" (`padding-top: 56.25%` pour le 16/9) était la seule solution. `aspect-ratio` remplace entièrement ce hack.*

<br>

---

## `object-fit` et `object-position` — contrôler les médias

`object-fit` définit comment un média (`<img>`, `<video>`) remplit son conteneur quand leurs proportions diffèrent.

```css title="CSS - object-fit pour les images dans des conteneurs fixes"
.carte-image {
    width: 100%;
    height: 220px;

    /*
        object-fit contrôle le redimensionnement du média dans le conteneur :
        cover    : remplit le conteneur en coupant si nécessaire (le plus courant)
        contain  : affiche l'image entière en ajoutant des bandes si nécessaire
        fill     : étire l'image pour remplir (distorsion possible)
        none     : conserve la taille originale sans redimensionnement
        scale-down : prend le plus petit entre none et contain
    */
    object-fit: cover;

    /* object-position : définit le point focal de l'image (comme background-position) */
    object-position: center top; /* Privilégie le haut de l'image */
}

/* Galerie de portraits : recadrer sur les visages */
.photo-portrait {
    width: 200px;
    height: 250px;
    object-fit: cover;
    object-position: 50% 20%; /* Focus sur le tiers supérieur */
}
```

*`object-fit: cover` est la propriété la plus utilisée en production pour les images dans des grilles ou des cards — elle garantit que toutes les cartes ont la même hauteur sans déformation.*

<br>

---

## Typographie Avancée

<br>

### Équilibre visuel : `text-wrap: balance`

Un titre long peut se casser sur une deuxième ligne avec un seul mot orphelin. `text-wrap: balance` équilibre mathématiquement les lignes pour éviter ce veuvage typographique.

```css title="CSS - Equilibrage des titres avec text-wrap"
h1,
h2,
.titre-carte {
    /*
        Le navigateur divise le bloc en calculant les espaces
        pour équilibrer les longueurs de ligne.
        Impact sur les performances : réservez aux titres courts,
        pas aux longs blocs de texte.
    */
    text-wrap: balance;
}

/* text-wrap: pretty : pour les corps de texte */
/* Évite les mots orphelins sans recalcul complet du bloc */
p {
    text-wrap: pretty;
}
```

<br>

### Tronquage de texte : `line-clamp`

Pour les cards avec des résumés de longueur variable, `line-clamp` tronque proprement le texte après N lignes et ajoute des points de suspension.

```css title="CSS - Tronquage sur 3 lignes avec line-clamp"
.extrait-article {
    /*
        Ces trois propriétés sont indissociables pour le tronquage multilignes.
        -webkit-line-clamp : nombre de lignes affichées avant tronquage
    */
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
}

/* Version récente : line-clamp sans préfixe (support progressif) */
.extrait-article-moderne {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    line-clamp: 3;          /* Propriété standard (Chrome 125+, Firefox 126+) */
    -webkit-line-clamp: 3;  /* Préfixe maintenu pour compatibilité */
    overflow: hidden;
}
```

*`line-clamp` est le seul mécanisme CSS natif pour les tronquages multilignes. La propriété standard sans préfixe devient progressivement disponible en 2024-2025.*

<br>

---

## Tableau récapitulatif

| Technique | Utilité principale |
| --- | --- |
| `filter: drop-shadow()` | Ombre épousant la silhouette d'un PNG ou SVG |
| `content: attr(data-*)` | Tooltip 100% CSS depuis les attributs HTML |
| `counter-reset` / `counter-increment` | Numérotation automatique sans HTML |
| `animation-timeline: scroll()` | Animations pilotées par le défilement |
| `scroll-snap-type` | Défilement magnétique sans JavaScript |
| `aspect-ratio` | Ratios d'affichage sans hacks padding |
| `object-fit: cover` | Images dans des conteneurs de taille fixe |
| `text-wrap: balance` | Titres sans mots orphelins |
| `-webkit-line-clamp` | Tronquage propre sur N lignes |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Ces techniques sont les finitions qui distinguent un site correct d'un site professionnel. `drop-shadow()` sur les PNGs, `attr()` pour les tooltips, `scroll-snap` pour les galeries, `aspect-ratio` pour les médias, `object-fit: cover` pour les images dans des grilles, `text-wrap: balance` pour les titres — toutes sont 100% CSS natif, sans dépendance externe.

> Vous maîtrisez maintenant l'ensemble de la chaîne CSS fondamentale. L'étape suivante est de structurer des layouts complets avec **Flexbox** — le système d'alignement unidimensionnel du web moderne.

<br>