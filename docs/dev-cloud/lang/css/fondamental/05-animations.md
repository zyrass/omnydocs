---
description: "Animations CSS : transitions, transforms 2D/3D, @keyframes, performance GPU, accessibilité prefers-reduced-motion"
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

!!! quote "Analogie pédagogique"
    _Pensez à un **livre pop-up artisanal** : lorsque vous tournez la page, des éléments surgissent, se déplient, pivotent — l'expérience est radicalement différente d'une page plate. Le livre ne contient pas plus d'informations qu'un livre ordinaire, mais il les révèle d'une manière qui capte l'attention et rend la lecture mémorable. **Les animations CSS** jouent exactement ce rôle sur le web : elles transforment un ensemble de boîtes statiques en expérience vivante, en donnant du sens aux transitions entre les états._

Avant les animations CSS (pré-2010), tout effet visuel nécessitait Flash ou JavaScript/jQuery, avec des coûts de performance significatifs. Les animations modernes CSS sont exécutées directement par le GPU du navigateur : elles sont fluides, légères, et ne bloquent pas le fil d'exécution principal.

Deux mécanismes complémentaires permettent d'animer en CSS :

- **Les transitions** — le passage doux d'un état A vers un état B, déclenché par un événement (`:hover`, `:focus`, ajout de classe)
- **Les animations `@keyframes`** — des séquences multi-étapes qui s'exécutent de manière autonome

<br>

---

## Transitions CSS

Une transition décrit comment une propriété CSS doit évoluer entre deux valeurs, plutôt que de changer brutalement.

### Syntaxe

```css title="CSS — Propriétés de transition"
/* Version développée */
.element {
    transition-property: background-color; /* Quelle propriété animer */
    transition-duration: 0.3s;            /* Durée de l'animation */
    transition-timing-function: ease-out; /* Courbe de vitesse */
    transition-delay: 0s;                 /* Délai avant démarrage */
}

/* Version raccourcie (recommandée) */
.element {
    transition: background-color 0.3s ease-out 0s;
    /* propriété  durée    timing  délai */
}
```

_La syntaxe raccourcie est préférée dans les projets réels car plus lisible. L'ordre des valeurs est fixe : propriété → durée → timing → délai._

```css title="CSS — Exemple concret : bouton avec transition"
.btn {
    background-color: #667eea;
    color: #ffffff;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;

    /* Transition sur 3 propriétés simultanément */
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

_Plusieurs propriétés peuvent être animées simultanément en les séparant par des virgules. Chacune peut avoir sa propre durée et courbe de vitesse._

### Propriétés animables et performance GPU

Toutes les propriétés CSS ne sont pas animables avec la même efficacité.

```css title="CSS — Propriétés et leur coût de performance"
/* ==== PERFORMANT — Accélérées par le GPU ============== */
.element {
    /* Ces propriétés n'affectent pas le layout (pas de reflow) */
    transition: opacity 0.3s ease;
    transition: transform 0.3s ease; /* translate, scale, rotate */
    transition: filter 0.3s ease;
}

/* ==== ACCEPTABLE — Légère charge sur le rendu ========= */
.element {
    transition: background-color 0.3s ease;
    transition: color 0.3s ease;
    transition: border-color 0.3s ease;
    transition: box-shadow 0.3s ease;
}

/* ==== À ÉVITER — Déclenchent un reflow complet ======== */
.element {
    /* Modifier ces propriétés recalcule toute la mise en page */
    transition: width 0.3s ease;
    transition: height 0.3s ease;
    transition: margin 0.3s ease;
    transition: padding 0.3s ease;
}
```

_La règle d'or : pour les animations fluides, n'animez que `opacity` et `transform`. Ces deux propriétés sont composées directement par le GPU, indépendamment du moteur de rendu de la page._

### Courbes de timing

```css title="CSS — Fonctions de timing disponibles"
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

_Pour générer et visualiser des courbes `cubic-bezier`, utilisez l'outil en ligne [cubic-bezier.com](https://cubic-bezier.com)._

### Durées recommandées

| Type d'interaction | Durée | Contexte |
|--------------------|-------|----------|
| Micro-interaction (`:hover`, `:focus`) | 100–200 ms | Boutons, liens, icônes |
| Changement d'état moyen | 200–350 ms | Dropdowns, tooltips |
| Apparition / disparition | 300–500 ms | Modales, drawers |
| Animation structurante | 500–800 ms | Transitions de page |

!!! warning "Au-delà de 1 seconde"
    Une animation de plus d'une seconde est perçue comme lente et frustrante dans la majorité des interactions quotidiennes. Réservez ce rythme aux introductions ou aux éléments de storytelling.

### Transitions avec délai — effet cascade

```css title="CSS — Animation en cascade avec transition-delay"
/* Les éléments apparaissent les uns après les autres */
.item { opacity: 0; transform: translateY(20px); }

.item:nth-child(1) { transition: opacity 0.4s ease 0s,    transform 0.4s ease 0s; }
.item:nth-child(2) { transition: opacity 0.4s ease 0.1s,  transform 0.4s ease 0.1s; }
.item:nth-child(3) { transition: opacity 0.4s ease 0.2s,  transform 0.4s ease 0.2s; }
.item:nth-child(4) { transition: opacity 0.4s ease 0.3s,  transform 0.4s ease 0.3s; }

/* Quand une classe est ajoutée (via JS ou :checked) */
.is-visible .item {
    opacity: 1;
    transform: translateY(0);
}
```

_Chaque élément attend un peu plus longtemps avant de démarrer sa transition. Le résultat est un effet de vague naturel._

<br>

---

## CSS Transforms

Les transforms manipulent visuellement un élément **sans modifier le flux du document**. Ils sont GPU-accélérés et n'ont aucun impact sur les éléments voisins.

### Transforms 2D

```css title="CSS — Fonctions de transform 2D"
/* ==== TRANSLATE : Déplacement ============= */

.element { transform: translateX(100px); }  /* 100 px vers la droite */
.element { transform: translateY(-50px); }  /* 50 px vers le haut */
.element { transform: translate(20px, 30px); } /* X et Y ensemble */

/* Centrage absolu avec translate */
.centered {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); /* Décale de sa propre moitié */
}


/* ==== SCALE : Redimensionnement =========== */

.element { transform: scale(1.5); }    /* 150 % de la taille d'origine */
.element { transform: scale(0.8); }    /* 80 % */
.element { transform: scaleX(2); }     /* Largeur seule × 2 */
.element { transform: scaleY(0.5); }   /* Hauteur seule ÷ 2 */


/* ==== ROTATE : Rotation =================== */

.element { transform: rotate(45deg); }    /* 45° sens horaire */
.element { transform: rotate(-90deg); }   /* 90° sens anti-horaire */
.element { transform: rotate(0.25turn); } /* Quart de tour */


/* ==== SKEW : Inclinaison ================== */

.element { transform: skewX(20deg); }  /* Inclinaison horizontale */
.element { transform: skewY(10deg); }  /* Inclinaison verticale */


/* ==== COMBINAISON ========================= */

/* L'ordre est important : les transformations s'appliquent de droite à gauche */
.card:hover {
    transform: translateY(-8px) scale(1.02);
    /* 1. Scale 1.02  →  2. Translate -8px vers le haut */
}
```

_Lorsqu'on combine plusieurs fonctions de transform, elles s'appliquent de droite à gauche dans la propriété. L'ordre conditionne le résultat final._

### transform-origin — point de pivot

```css title="CSS — Modifier le point de pivot"
/* Par défaut : centre de l'élément (50% 50%) */
.element {
    transform-origin: center;
    transform: rotate(45deg);   /* Rotation autour du centre */
}

/* Rotation autour du coin supérieur gauche */
.door {
    transform-origin: left center;
    transition: transform 0.5s ease;
}

.door:hover {
    transform: rotateY(80deg);  /* S'ouvre comme une vraie porte */
}

/* Valeurs possibles */
.element { transform-origin: top left; }     /* Coin supérieur gauche */
.element { transform-origin: bottom right; } /* Coin inférieur droit */
.element { transform-origin: 30% 70%; }      /* Position en pourcentages */
.element { transform-origin: 20px 40px; }    /* Position en pixels */
```

### Transforms 3D

```css title="CSS — Perspective et transforms 3D"
/* La perspective s'applique sur le PARENT pour activer la 3D */
.scene {
    perspective: 1000px; /* Distance "caméra" : plus grand = effet 3D subtil */
}

/* ==== ROTATE 3D =============================== */
.element { transform: rotateX(45deg); }  /* Bascule avant/arrière */
.element { transform: rotateY(45deg); }  /* Tourne gauche/droite */
.element { transform: rotateZ(45deg); }  /* Équivalent à rotate() 2D */


/* ==== CARD FLIP (exemple complet) ============ */
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
    backface-visibility: hidden; /* Cache la face arrière quand elle est derrière */
}

.card-back {
    transform: rotateY(180deg); /* Pré-retournée, invisible au repos */
}
```

_`transform-style: preserve-3d` est essentiel : sans lui, les éléments enfants sont aplatis en 2D avant l'application de leur transform. `backface-visibility: hidden` masque une face quand elle est tournée au-delà de 90°._

<br>

---

## Animations @keyframes

Les `@keyframes` définissent une séquence d'états par lesquels un élément doit passer. Contrairement aux transitions, elles ne nécessitent pas de déclencheur externe.

### Syntaxe fondamentale

```css title="CSS — Définition et utilisation d'une animation"
/* ==== 1. Définir la séquence =============== */

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

/* Avec étapes multiples (pourcentages) */
@keyframes pulse {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.08); }
    100% { transform: scale(1); }
}


/* ==== 2. Appliquer l'animation ============= */

.hero-title {
    animation-name: slide-in;      /* Nom de la @keyframes */
    animation-duration: 0.6s;      /* Durée */
    animation-timing-function: ease-out;
    animation-delay: 0.1s;         /* Délai avant démarrage */
    animation-iteration-count: 1;  /* Nombre de répétitions (ou infinite) */
    animation-direction: normal;   /* normal | reverse | alternate */
    animation-fill-mode: forwards; /* État final conservé après l'animation */
    animation-play-state: running; /* running | paused */
}

/* Raccourci : name duration timing delay iterations direction fill-mode */
.hero-title {
    animation: slide-in 0.6s ease-out 0.1s 1 normal forwards;
}
```

_`animation-fill-mode: forwards` conserve l'état final de l'animation une fois terminée. Sans lui, l'élément revient instantanément à son état initial._

### Exemples pratiques

```css title="CSS — Loader spinner"
@keyframes spin {
    to { transform: rotate(360deg); }
}

.loader {
    width: 32px;
    height: 32px;
    border: 3px solid rgba(102, 126, 234, 0.2);
    border-top-color: #667eea;
    border-radius: 50%;

    animation: spin 0.8s linear infinite;
}
```

```css title="CSS — Apparition en fondu avec décalage (stagger)"
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
    /* Chaque carte est invisible au départ */
    opacity: 0;
    animation: fade-up 0.5s ease-out forwards;
}

/* Décalage progressif par élément */
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
```

```css title="CSS — Animation pulsante pour une notification"
@keyframes ring {
    0%   { transform: scale(1); opacity: 1; }
    50%  { transform: scale(1.2); opacity: 0.6; }
    100% { transform: scale(1); opacity: 1; }
}

.notification-badge {
    animation: ring 2s ease-in-out infinite;
}
```

### animation-fill-mode

```css title="CSS — Comportement avant et après l'animation"
/* none (défaut) : l'élément revient à son état initial */
.element { animation-fill-mode: none; }

/* forwards : conserve l'état de la dernière @keyframes */
.element { animation-fill-mode: forwards; }

/* backwards : applique l'état de la première @keyframes pendant le délai */
.element { animation-fill-mode: backwards; }

/* both : forwards + backwards */
.element { animation-fill-mode: both; }
```

<br>

---

## Performance des animations

### will-change — préparer la couche GPU

```css title="CSS — Déclarer les propriétés qui seront animées"
/* Prépare le navigateur à créer une couche GPU pour cet élément */
.menu-panel {
    will-change: transform;
}

.fade-element {
    will-change: opacity;
}
```

!!! warning "Ne pas abuser de will-change"
    `will-change` est une promesse faite au navigateur : il va allouer de la mémoire GPU en anticipation. Si vous l'appliquez à trop d'éléments, vous consommez de la mémoire pour rien et pouvez dégrader les performances. Ne l'utilisez que sur les éléments animés **de manière répétée** (menus, overlays).

<br>

---

## Accessibilité — prefers-reduced-motion

!!! important "Obligation d'accessibilité"
    Certains utilisateurs souffrent de troubles vestibulaires, d'épilepsie photosensible ou de migraines. Pour eux, les animations peuvent provoquer des malaises physiques. Le système d'exploitation expose une préférence `prefers-reduced-motion` que CSS peut lire.

```css title="CSS — Respect de prefers-reduced-motion"
/* Animations par défaut */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Désactivation pour les utilisateurs sensibles */
@media (prefers-reduced-motion: reduce) {
    .card {
        transition: none;
    }

    .card:hover {
        transform: none;
        /* On peut conserver les changements de couleur, moins problématiques */
        box-shadow: 0 0 0 2px #667eea;
    }

    /* Stopper toutes les animations en boucle */
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

_La règle globale sur `*` dans `prefers-reduced-motion: reduce` stoppe toutes les animations sans les supprimer entièrement — elles durent 0,01 ms, ce qui les rend imperceptibles tout en permettant aux états finaux d'être atteints._

<br>

---

## Micro-interactions — exemples concrets

```css title="CSS — Collection de micro-interactions courantes"
/* ==== Bouton avec effet de pression ================== */
.btn {
    transition: transform 0.1s ease-out, box-shadow 0.1s ease-out;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


/* ==== Lien avec soulignement animé ====================== */
.nav-link {
    position: relative;
    text-decoration: none;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;          /* Commence à 0 */
    height: 2px;
    background-color: #667eea;
    transition: width 0.3s ease-out;
}

.nav-link:hover::after {
    width: 100%;       /* S'étend vers la droite */
}


/* ==== Carte avec élévation au survol ==================== */
.card {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition:
        transform        0.25s ease-out,
        box-shadow       0.25s ease-out;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}


/* ==== Icône qui tourne au survol ======================== */
.icon-btn {
    transition: transform 0.3s ease;
}

.icon-btn:hover {
    transform: rotate(15deg) scale(1.1);
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les **transitions** assurent le passage doux entre deux états (déclenché par `:hover`, `:focus` ou une classe). Les **transforms** manipulent visuellement un élément sans impact sur le flux. Les **`@keyframes`** orchestrent des séquences multi-étapes autonomes. Pour des animations performantes, animez uniquement `opacity` et `transform` — ils sont exécutés par le GPU. Et toujours, respectez `prefers-reduced-motion`.

> Pour appliquer l'ensemble de ces techniques dans un projet concret, rendez-vous directement dans [CSS Avancé](./06-css-avance.md), puis dans le [Projet Final HTML/CSS](../../../projets/html-css-vitrine/index.md).

<br>
