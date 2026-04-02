---
description: "Animations CSS : transitions, transforms 2D/3D, @keyframes, performance GPU, accessibilité prefers-reduced-motion."
icon: lucide/book-open-check
tags: ["CSS", "ANIMATIONS", "TRANSITIONS", "TRANSFORMS", "KEYFRAMES", "PERFORMANCE"]
---

# Animations CSS

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="1.1"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Livre Pop-up"
    Pensez à un **livre pop-up artisanal** : lorsque vous tournez la page, des éléments surgissent, se déplient, pivotent — l'expérience est radicalement différente d'une page plate. Le livre ne contient pas plus d'informations qu'un livre ordinaire, mais il les révèle d'une manière qui capte l'attention et rend la lecture mémorable.

    Les **animations CSS** jouent exactement ce rôle sur le web : elles transforment un ensemble de boîtes statiques en expérience vivante, en donnant du sens aux transitions entre les états.

Avant les animations CSS (pré-2010), tout effet visuel nécessitait Flash ou JavaScript/jQuery, avec des coûts de performance significatifs. Les animations modernes CSS sont exécutées directement par le GPU du navigateur : fluides, légères, elles ne bloquent pas le fil d'exécution principal.

Deux mécanismes complémentaires permettent d'animer en CSS :

- **Les transitions** — le passage doux d'un état A vers un état B, déclenché par un événement (`:hover`, `:focus`, ajout de classe).
- **Les animations `@keyframes`** — des séquences multi-étapes qui s'exécutent de manière autonome.

<br>

---

## Transitions CSS

Une transition décrit comment une propriété CSS doit évoluer entre deux valeurs, plutôt que de changer brutalement.

<br>

### Syntaxe

```css title="CSS - Propriétés de transition"
/* Version développée */
.element {
    transition-property: background-color; /* Quelle propriété animer */
    transition-duration: 0.3s;             /* Durée de l'animation */
    transition-timing-function: ease-out;  /* Courbe de vitesse */
    transition-delay: 0s;                  /* Délai avant démarrage */
}

/* Version raccourcie (recommandée) : propriété | durée | timing | délai */
.element {
    transition: background-color 0.3s ease-out 0s;
}
```

*La syntaxe raccourcie est préférée dans les projets réels. L'ordre des valeurs est fixe : propriété → durée → timing → délai.*

```css title="CSS - Bouton avec transitions multiples"
.btn {
    background-color: #667eea;
    color: #ffffff;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;

    /* Plusieurs propriétés animées simultanément, séparées par des virgules */
    transition:
        background-color 0.2s ease-out,
        transform        0.2s ease-out,
        box-shadow       0.2s ease-out;
}

.btn:hover {
    background-color: #5a6fd6;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
```

*Chaque propriété animée peut avoir sa propre durée et courbe de vitesse.*

<br>

### Propriétés animables et performance GPU

Toutes les propriétés CSS ne s'animent pas avec la même efficacité. Le critère déterminant est l'impact sur le moteur de rendu.

```css title="CSS - Classification des propriétés par coût de performance"
/* PERFORMANT — accélérées par le GPU, pas de reflow */
.element { transition: opacity 0.3s ease; }
.element { transition: transform 0.3s ease; }  /* translate, scale, rotate */
.element { transition: filter 0.3s ease; }

/* ACCEPTABLE — légère charge sur le rendu */
.element { transition: background-color 0.3s ease; }
.element { transition: color 0.3s ease; }
.element { transition: border-color 0.3s ease; }
.element { transition: box-shadow 0.3s ease; }

/* A EVITER — déclenchent un reflow complet de la page */
.element { transition: width 0.3s ease; }
.element { transition: height 0.3s ease; }
.element { transition: margin 0.3s ease; }
.element { transition: padding 0.3s ease; }
```

*La règle d'or : pour des animations fluides, n'animez que `opacity` et `transform`. Ces deux propriétés sont composées directement par le GPU, indépendamment du moteur de rendu de la page.*

<br>

### Courbes de timing

```css title="CSS - Fonctions de timing et courbes cubic-bezier"
/* Mots-clés prédéfinis */
.element { transition-timing-function: ease; }         /* Lent → Rapide → Lent (défaut) */
.element { transition-timing-function: ease-in; }      /* Démarre lentement */
.element { transition-timing-function: ease-out; }     /* Finit lentement */
.element { transition-timing-function: ease-in-out; }  /* Lent aux deux extrêmes */
.element { transition-timing-function: linear; }       /* Vitesse constante */

/* Courbes personnalisées avec cubic-bezier */
/* Material Design 3 (Google) */
.element { transition-timing-function: cubic-bezier(0.2, 0, 0, 1); }

/* iOS / SpringBoard (Apple) */
.element { transition-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }

/* Rebond léger */
.element { transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); }
```

*Pour générer et visualiser des courbes `cubic-bezier`, utilisez l'outil [cubic-bezier.com](https://cubic-bezier.com).*

**Durées recommandées selon le type d'interaction :**

| Type d'interaction | Durée | Contexte |
| --- | --- | --- |
| Micro-interaction (`:hover`, `:focus`) | 100–200 ms | Boutons, liens, icônes |
| Changement d'état moyen | 200–350 ms | Dropdowns, tooltips |
| Apparition / disparition | 300–500 ms | Modales, drawers |
| Animation structurante | 500–800 ms | Transitions de page |

!!! warning "Au-delà de 1 seconde"
    Une animation de plus d'une seconde est perçue comme lente et frustrante dans la majorité des interactions quotidiennes. Réservez ce rythme aux introductions ou aux éléments de storytelling.

<br>

### Transitions en cascade avec `transition-delay`

```css title="CSS - Effet de vague avec délais progressifs"
/* État initial : éléments invisibles, décalés vers le bas */
.item {
    opacity: 0;
    transform: translateY(20px);
}

/* Chaque élément démarre sa transition avec un délai croissant */
.item:nth-child(1) { transition: opacity 0.4s ease 0s,   transform 0.4s ease 0s; }
.item:nth-child(2) { transition: opacity 0.4s ease 0.1s, transform 0.4s ease 0.1s; }
.item:nth-child(3) { transition: opacity 0.4s ease 0.2s, transform 0.4s ease 0.2s; }
.item:nth-child(4) { transition: opacity 0.4s ease 0.3s, transform 0.4s ease 0.3s; }

/* Déclenchement : une classe est ajoutée par JavaScript */
.is-visible .item {
    opacity: 1;
    transform: translateY(0);
}
```

*Chaque élément attend un peu plus longtemps avant de démarrer sa transition. Le résultat est un effet de vague naturel.*

<br>

---

## CSS Transforms

Les transforms manipulent visuellement un élément **sans modifier le flux du document**. Ils sont GPU-accélérés et n'ont aucun impact sur les éléments voisins.

<br>

### Transforms 2D

```css title="CSS - Fonctions de transform 2D"
/* TRANSLATE : déplacement */
.element { transform: translateX(100px); }     /* Vers la droite */
.element { transform: translateY(-50px); }     /* Vers le haut */
.element { transform: translate(20px, 30px); } /* X et Y ensemble */

/* Technique classique de centrage absolu */
.centered {
    position: absolute;
    top: 50%;
    left: 50%;
    /* Décale l'élément de la moitié de sa propre taille */
    transform: translate(-50%, -50%);
}

/* SCALE : redimensionnement */
.element { transform: scale(1.5); }   /* 150 % */
.element { transform: scale(0.8); }   /* 80 % */
.element { transform: scaleX(2); }    /* Largeur seule × 2 */
.element { transform: scaleY(0.5); }  /* Hauteur seule ÷ 2 */

/* ROTATE : rotation */
.element { transform: rotate(45deg); }    /* Sens horaire */
.element { transform: rotate(-90deg); }   /* Sens anti-horaire */
.element { transform: rotate(0.25turn); } /* Quart de tour */

/* SKEW : inclinaison */
.element { transform: skewX(20deg); }
.element { transform: skewY(10deg); }

/* COMBINAISON : ordre important, de droite à gauche */
.card:hover {
    /* 1. Scale 1.02 s'applique, 2. puis translateY(-8px) */
    transform: translateY(-8px) scale(1.02);
}
```

*Lorsqu'on combine plusieurs fonctions de transform, elles s'appliquent de droite à gauche. L'ordre conditionne le résultat final.*

<br>

### `transform-origin` — le point de pivot

```css title="CSS - Modifier le point autour duquel la transformation s'applique"
/* Par défaut : centre de l'élément (50% 50%) */
.element {
    transform-origin: center;
    transform: rotate(45deg); /* Rotation autour du centre */
}

/* Effet de porte qui s'ouvre */
.door {
    transform-origin: left center; /* Pivot sur le bord gauche */
    transition: transform 0.5s ease;
}

.door:hover {
    transform: rotateY(80deg);
}

/* Valeurs disponibles */
.element { transform-origin: top left; }     /* Coin supérieur gauche */
.element { transform-origin: bottom right; } /* Coin inférieur droit */
.element { transform-origin: 30% 70%; }      /* Position en pourcentages */
.element { transform-origin: 20px 40px; }    /* Position en pixels */
```

<br>

### Transforms 3D

```css title="CSS - Perspective et card flip en 3D"
/* La perspective s'applique sur le PARENT pour activer l'espace 3D */
.scene {
    perspective: 1000px; /* Distance caméra : plus grand = effet 3D subtil */
}

/* Rotations 3D */
.element { transform: rotateX(45deg); }  /* Bascule avant/arrière */
.element { transform: rotateY(45deg); }  /* Tourne gauche/droite */
.element { transform: rotateZ(45deg); }  /* Identique à rotate() 2D */

/* Exemple complet : card flip au survol */
.card-scene {
    perspective: 1000px;
    width: 300px;
    height: 200px;
}

.card {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d; /* Les enfants vivent en 3D */
    transition: transform 0.6s ease;
}

.card:hover {
    transform: rotateY(180deg);
}

.card-face,
.card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden; /* Cache la face quand elle est tournée au-delà de 90° */
}

.card-back {
    transform: rotateY(180deg); /* Pré-retournée, invisible au repos */
}
```

*`transform-style: preserve-3d` est indispensable : sans lui, les enfants sont aplatis en 2D avant l'application de leur transform. `backface-visibility: hidden` masque une face quand elle est orientée à l'opposé du regard.*

<br>

---

## Animations @keyframes

Les `@keyframes` définissent une séquence d'états par lesquels un élément doit passer. Contrairement aux transitions, elles ne nécessitent pas de déclencheur externe.

<br>

### Syntaxe fondamentale

```css title="CSS - Définition et application d'une animation"
/* 1. Définir la séquence */
@keyframes slide-in {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Avec étapes multiples en pourcentages */
@keyframes pulse {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.08); }
    100% { transform: scale(1); }
}

/* 2. Appliquer l'animation (version développée) */
.hero-title {
    animation-name: slide-in;
    animation-duration: 0.6s;
    animation-timing-function: ease-out;
    animation-delay: 0.1s;
    animation-iteration-count: 1;         /* Nombre de répétitions (ou infinite) */
    animation-direction: normal;          /* normal | reverse | alternate */
    animation-fill-mode: forwards;        /* État final conservé après l'animation */
    animation-play-state: running;        /* running | paused */
}

/* Raccourci : nom | durée | timing | délai | répétitions | direction | fill-mode */
.hero-title {
    animation: slide-in 0.6s ease-out 0.1s 1 normal forwards;
}
```

*`animation-fill-mode: forwards` conserve l'état final une fois l'animation terminée. Sans lui, l'élément revient instantanément à son état initial.*

<br>

### Exemples pratiques

```css title="CSS - Loader spinner"
@keyframes spin {
    to { transform: rotate(360deg); }
}

.loader {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(102, 126, 234, 0.2);
    border-top-color: #667eea;
    border-radius: 50%;

    /* linear pour une vitesse constante, infinite pour la boucle */
    animation: spin 0.8s linear infinite;
}
```

```css title="CSS - Apparition en cascade (stagger)"
@keyframes fade-up {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card {
    opacity: 0; /* Invisible avant l'animation */
    animation: fade-up 0.5s ease-out forwards;
}

/* Décalage progressif : chaque carte démarre 100ms après la précédente */
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
```

```css title="CSS - Badge de notification pulsant"
@keyframes ring {
    0%   { transform: scale(1); opacity: 1; }
    50%  { transform: scale(1.2); opacity: 0.6; }
    100% { transform: scale(1); opacity: 1; }
}

.notification-badge {
    animation: ring 2s ease-in-out infinite;
}
```

<br>

### `animation-fill-mode`

```css title="CSS - Comportement avant et après l'animation"
/* none (défaut) : revient à l'état initial après l'animation */
.element { animation-fill-mode: none; }

/* forwards : conserve l'état de la dernière @keyframes */
.element { animation-fill-mode: forwards; }

/* backwards : applique l'état initial pendant le délai (animation-delay) */
.element { animation-fill-mode: backwards; }

/* both : combine forwards et backwards */
.element { animation-fill-mode: both; }
```

<br>

---

## Performance des animations

<br>

### `will-change` — préparer la couche GPU

```css title="CSS - Déclarer les propriétés qui seront animées"
/* Prépare le navigateur à créer une couche GPU pour cet élément */
.menu-panel {
    will-change: transform;
}

.fade-element {
    will-change: opacity;
}
```

!!! warning "Ne pas abuser de `will-change`"
    `will-change` est une promesse faite au navigateur : il alloue de la mémoire GPU en anticipation. Appliqué à trop d'éléments, il dégrade les performances au lieu de les améliorer. Réservez-le aux éléments animés de manière répétée — menus, overlays, panels.

<br>

---

## Accessibilité — `prefers-reduced-motion`

!!! danger "Obligation d'accessibilité"
    Certains utilisateurs souffrent de troubles vestibulaires, d'épilepsie photosensible ou de migraines. Pour eux, les animations peuvent provoquer des malaises physiques réels. Le système d'exploitation expose une préférence `prefers-reduced-motion` que CSS peut lire et respecter.

```css title="CSS - Respect de prefers-reduced-motion"
/* Animations par défaut */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Désactivation pour les utilisateurs qui ont activé la réduction de mouvement */
@media (prefers-reduced-motion: reduce) {
    .card {
        transition: none;
    }

    .card:hover {
        transform: none;
        /* Les changements de couleur restent acceptables */
        box-shadow: 0 0 0 2px #667eea;
    }

    /*
        Règle globale de sécurité : réduit toutes les animations à 0.01ms.
        Elles ne sont pas supprimées — les états finaux restent atteignables —
        mais elles deviennent imperceptibles.
    */
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

<br>

---

## Micro-interactions — collection de patterns courants

```css title="CSS - Bouton avec effet de pression au clic"
.btn {
    transition: transform 0.1s ease-out, box-shadow 0.1s ease-out;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* :active simule l'enfoncement physique du bouton */
.btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

```css title="CSS - Lien avec soulignement animé"
.nav-link {
    position: relative;
    text-decoration: none;
}

/* ::after génère un trait invisible sous le lien */
.nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;             /* Démarre à zéro */
    height: 2px;
    background-color: #667eea;
    transition: width 0.3s ease-out;
}

/* Au survol, le trait s'étend de gauche à droite */
.nav-link:hover::after {
    width: 100%;
}
```

```css title="CSS - Carte avec élévation au survol"
.card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition:
        transform  0.25s ease-out,
        box-shadow 0.25s ease-out;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les **transitions** assurent le passage doux entre deux états — déclenchées par `:hover`, `:focus` ou l'ajout d'une classe. Les **transforms** manipulent visuellement un élément sans impact sur le flux du document. Les **`@keyframes`** orchestrent des séquences multi-étapes autonomes. Pour des animations performantes, n'animez que `opacity` et `transform`. Respectez toujours `prefers-reduced-motion` — c'est une obligation d'accessibilité, pas une option.

> Dans le module suivant, nous aborderons les techniques **CSS Avancées** : Variables CSS, filtres, clip-path, blend modes, gradients et nesting natif.

<br>