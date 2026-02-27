---
description: "Maîtriser Animations CSS : transitions, @keyframes, transforms, timing-functions, animations performantes"
icon: lucide/book-open-check
tags: ["CSS", "ANIMATIONS", "TRANSITIONS", "TRANSFORMS", "KEYFRAMES", "PERFORMANCE"]
---

# XIII - Anim' & Transitions

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : Donner Vie au Web

!!! quote "Analogie pédagogique"
    _Imaginez un **livre pop-up** : quand vous tournez la page, des éléments surgissent en 3D, se déplient, tournent, créant une expérience magique. **Les animations CSS**, c'est exactement ça pour le web : transformer un site statique en expérience **vivante et engageante**. **Avant les animations CSS** (pré-2010), on utilisait Flash (lourd, non-mobile, sécurité problématique) ou JavaScript/jQuery (performance médiocre, complexe). **Avec CSS animations**, le navigateur optimise TOUT : GPU acceleration, 60fps fluides, aucun JavaScript nécessaire. Un simple `:hover` peut transformer un bouton fade en expérience tactile satisfaisante. Un `@keyframes` peut créer un loader élégant, une notification qui slide, un menu qui se déploie. **Transitions = changements doux** (A → B sur déclencheur comme :hover). **Animations = séquences complexes** (A → B → C → D en boucle). **Transforms = manipulations visuelles** (rotation, scale, translation) SANS modifier layout (performance GPU). Les animations CSS ne sont pas décoratives : elles **guident l'attention**, indiquent **état du système** (loading), donnent **feedback utilisateur** (bouton cliqué), créent **hiérarchie visuelle**. Mais attention : trop d'animations = site circus amateur. Règle d'or : **animations subtiles, intentionnelles, performantes**. Ce module vous transforme en expert animations : vous créerez des micro-interactions délicieuses, des loaders professionnels, des transitions fluides, tout en maintenant 60fps sur mobile._

**Animations CSS** = Technique pour créer mouvement et changements visuels en CSS pur.

**Pourquoi les Animations CSS sont ESSENTIELLES ?**

✅ **UX améliorée** : Feedback visuel, guidage attention  
✅ **Performance** : GPU-accelerated, 60fps natif  
✅ **Engagement** : Expérience vivante vs site statique  
✅ **Pas de JavaScript** : CSS pur, moins de code  
✅ **Accessibility** : Respect prefers-reduced-motion  
✅ **Mobile-friendly** : Optimisé navigateurs mobiles  

**Statistiques animations :**

- Sites avec micro-interactions : +20% engagement
- Animations bien faites : +15% conversion
- Animations mal faites : -30% crédibilité
- 60fps = impératif (< 60fps = laggy, amateur)

**Les 3 techniques d'animation CSS :**

1. **Transitions** : Changement A → B (hover, focus, class change)
2. **Animations** : Séquences complexes @keyframes (loops, multi-step)
3. **Transforms** : Manipulations visuelles (rotate, scale, translate)

**Ce module couvre TOUTES les animations CSS niveau expert.**

---

## 1. CSS Transitions

### 1.1 Concept et Syntaxe

```css
/* Transition = Animation douce entre 2 états */

/* Syntaxe complète */
.element {
    transition-property: background-color;  /* Quelle propriété animer */
    transition-duration: 0.3s;              /* Durée */
    transition-timing-function: ease-in-out; /* Courbe vitesse */
    transition-delay: 0s;                   /* Délai avant démarrage */
}

/* Raccourci (recommandé) */
.element {
    transition: background-color 0.3s ease-in-out 0s;
    /* property duration timing-function delay */
}

/* Exemple bouton */
.button {
    background-color: blue;
    color: white;
    padding: 15px 30px;
    border: none;
    cursor: pointer;
    
    /* Transition sur background */
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: darkblue;
}

/* Au hover, background change de blue → darkblue en 0.3s
   Sans transition : changement brutal
   Avec transition : changement doux, fluide
*/
```

### 1.2 transition-property

```css
/* Spécifie QUELLE propriété animer */

/* Une propriété */
.element {
    transition-property: opacity;
}

/* Plusieurs propriétés (virgule) */
.element {
    transition-property: opacity, transform;
}

/* Toutes propriétés (attention performance) */
.element {
    transition-property: all;
}

/* ⚠️ Éviter 'all' : performance médiocre */
/* Spécifier propriétés exactes toujours mieux */

/* Propriétés CSS animables (principales) */

/* ✅ PERFORMANT (GPU-accelerated) */
- opacity
- transform (translate, rotate, scale)
- filter (blur, brightness)

/* ⚠️ ACCEPTABLE (moins performant) */
- background-color
- color
- border-color
- box-shadow
- width, height (déclenche reflow)
- top, left, right, bottom (position absolute)
- margin, padding (déclenche reflow)

/* ❌ ÉVITER (très lent, déclenche reflow/repaint) */
- display (pas animable directement)
- font-size (reflow)
- border-width (reflow)

/* Exemple combinaison performante */
.card {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.card:hover {
    opacity: 0.8;
    transform: translateY(-10px);
}
/* Seulement opacity + transform = GPU, très fluide */
```

### 1.3 transition-duration

```css
/* Durée de la transition */

/* Secondes (s) */
.element {
    transition-duration: 0.3s;  /* 300 millisecondes */
}

/* Millisecondes (ms) */
.element {
    transition-duration: 300ms;  /* = 0.3s */
}

/* Durées recommandées selon type */

/* Micro-interactions (hover, focus) */
.button {
    transition-duration: 0.15s;  /* 150ms : rapide, réactif */
}

/* Changements moyens (tooltips, dropdowns) */
.dropdown {
    transition-duration: 0.3s;  /* 300ms : standard, fluide */
}

/* Animations importantes (modals, slides) */
.modal {
    transition-duration: 0.5s;  /* 500ms : plus lent, emphase */
}

/* Animations complexes */
.slide {
    transition-duration: 0.8s;  /* 800ms : très lent, attention */
}

/* ⚠️ Règles durée */
/* < 100ms : trop rapide, imperceptible */
/* 100-300ms : idéal micro-interactions */
/* 300-500ms : idéal changements moyens */
/* 500-1000ms : animations importantes uniquement */
/* > 1000ms : éviter (frustrant utilisateur) */

/* Durées différentes par propriété */
.element {
    transition: opacity 0.2s ease,
                transform 0.3s ease,
                background-color 0.4s ease;
}
/* opacity rapide, transform moyen, background lent */
```

### 1.4 transition-timing-function

```css
/* Courbe de vitesse (accélération/décélération) */

/* ========================================
   FONCTIONS PRÉDÉFINIES
   ======================================== */

/* linear : Vitesse constante */
.element {
    transition-timing-function: linear;
}
/* Vitesse : ━━━━━━━━━ (uniforme) */

/* ease : Lent → Rapide → Lent (défaut) */
.element {
    transition-timing-function: ease;
}
/* Vitesse : ╱━━━━╲ (naturel) */

/* ease-in : Lent → Rapide (accélération) */
.element {
    transition-timing-function: ease-in;
}
/* Vitesse : ╱━━━━ (démarre lent) */

/* ease-out : Rapide → Lent (décélération) */
.element {
    transition-timing-function: ease-out;
}
/* Vitesse : ━━━━╲ (finit lent) */

/* ease-in-out : Lent → Rapide → Lent (symétrique) */
.element {
    transition-timing-function: ease-in-out;
}
/* Vitesse : ╱━━╲ (smooth entrée/sortie) */

/* ========================================
   CUBIC-BEZIER (Courbes custom)
   ======================================== */

/* Syntaxe : cubic-bezier(x1, y1, x2, y2) */

/* Équivalences prédéfinies */
ease          = cubic-bezier(0.25, 0.1, 0.25, 1.0)
linear        = cubic-bezier(0, 0, 1, 1)
ease-in       = cubic-bezier(0.42, 0, 1.0, 1.0)
ease-out      = cubic-bezier(0, 0, 0.58, 1.0)
ease-in-out   = cubic-bezier(0.42, 0, 0.58, 1.0)

/* Courbes custom populaires */

/* Material Design (Google) */
.element {
    transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
}

/* iOS (Apple) */
.element {
    transition-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Bounce (rebond) */
.element {
    transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Générateur : https://cubic-bezier.com */

/* ========================================
   STEPS (Animations par étapes)
   ======================================== */

/* steps(n) : n étapes discrètes (pas fluide) */

.element {
    transition-timing-function: steps(5);
}
/* Animation en 5 sauts (sprite animation) */

/* steps(n, start/end) */
.element {
    transition-timing-function: steps(4, end);
}
/* 4 étapes, changement à la fin de chaque step */

/* step-start / step-end */
.element {
    transition-timing-function: step-start;
    /* = steps(1, start) : changement immédiat au début */
}

.element {
    transition-timing-function: step-end;
    /* = steps(1, end) : changement immédiat à la fin */
}

/* ========================================
   USAGE RECOMMANDÉ
   ======================================== */

/* Hover/Focus : ease-out (réactif) */
.button:hover {
    transition-timing-function: ease-out;
}

/* Entrée éléments : ease-out (apparition douce) */
.modal {
    transition-timing-function: ease-out;
}

/* Sortie éléments : ease-in (disparition rapide) */
.modal.closing {
    transition-timing-function: ease-in;
}

/* Mouvement physique : ease-in-out (naturel) */
.slider {
    transition-timing-function: ease-in-out;
}
```

### 1.5 transition-delay

```css
/* Délai AVANT démarrage transition */

/* Secondes */
.element {
    transition-delay: 0.2s;  /* Attends 200ms avant démarrer */
}

/* Millisecondes */
.element {
    transition-delay: 200ms;
}

/* Délai négatif (démarre au milieu) */
.element {
    transition-delay: -0.1s;  /* Démarre 100ms "dans le passé" */
}

/* Exemple : Animation cascade */

.item-1 {
    transition: opacity 0.5s ease 0s;    /* Immédiat */
}

.item-2 {
    transition: opacity 0.5s ease 0.1s;  /* +100ms */
}

.item-3 {
    transition: opacity 0.5s ease 0.2s;  /* +200ms */
}

.item-4 {
    transition: opacity 0.5s ease 0.3s;  /* +300ms */
}

/* Items apparaissent en cascade (effet vague) */

/* Générer avec boucle (Sass/SCSS) */
@for $i from 1 through 10 {
    .item-#{$i} {
        transition-delay: #{$i * 0.05}s;
    }
}
/* item-1: 0.05s, item-2: 0.1s, ..., item-10: 0.5s */
```

### 1.6 Transitions Multiples

```css
/* Animer plusieurs propriétés simultanément */

/* Même durée/timing */
.button {
    transition: background-color 0.3s ease,
                color 0.3s ease,
                transform 0.3s ease;
}

/* Durées/timings différents */
.card {
    transition: opacity 0.2s ease-out,
                transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1),
                box-shadow 0.3s ease;
}

.card:hover {
    opacity: 0.9;
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Propriétés avec délais différents */
.menu {
    transition: opacity 0.3s ease 0s,
                transform 0.3s ease 0.1s;
}
/* opacity démarre immédiatement, transform après 100ms */

/* ⚠️ Éviter 'all' pour performance */

/* ❌ MAL (toutes propriétés, même non utilisées) */
.element {
    transition: all 0.3s ease;
}

/* ✅ BIEN (propriétés spécifiques) */
.element {
    transition: opacity 0.3s ease,
                transform 0.3s ease;
}
```

---

## 2. CSS Transforms

### 2.1 Transform 2D

```css
/* Transform = Manipulation visuelle SANS changer layout */
/* GPU-accelerated = très performant */

/* ========================================
   TRANSLATE (Déplacement)
   ======================================== */

/* translateX : Déplacement horizontal */
.element {
    transform: translateX(100px);  /* 100px à droite */
    transform: translateX(-50px);  /* 50px à gauche */
    transform: translateX(50%);    /* 50% largeur élément */
}

/* translateY : Déplacement vertical */
.element {
    transform: translateY(100px);  /* 100px vers bas */
    transform: translateY(-50px);  /* 50px vers haut */
}

/* translate : X et Y ensemble */
.element {
    transform: translate(100px, 50px);  /* X: 100px, Y: 50px */
    transform: translate(50%, -20px);   /* X: 50%, Y: -20px */
}

/* Centrage parfait avec translate */
.centered {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
/* Décale de 50% sa propre taille = centrage pixel-perfect */

/* ========================================
   SCALE (Redimensionnement)
   ======================================== */

/* scale : Agrandir/Rétrécir */
.element {
    transform: scale(1.5);    /* 150% taille (1.5×) */
    transform: scale(0.8);    /* 80% taille (0.8×) */
    transform: scale(2);      /* 200% taille (2×) */
}

/* scaleX : Largeur uniquement */
.element {
    transform: scaleX(2);     /* Largeur ×2, hauteur normale */
}

/* scaleY : Hauteur uniquement */
.element {
    transform: scaleY(0.5);   /* Hauteur ÷2, largeur normale */
}

/* scale(x, y) : Séparé X et Y */
.element {
    transform: scale(1.5, 0.8);  /* Largeur ×1.5, hauteur ×0.8 */
}

/* Hover effect classique */
.card {
    transition: transform 0.3s ease;
}

.card:hover {
    transform: scale(1.05);  /* Agrandit 5% au hover */
}

/* ========================================
   ROTATE (Rotation)
   ======================================== */

/* rotate : Rotation en degrés (deg) */
.element {
    transform: rotate(45deg);    /* 45° sens horaire */
    transform: rotate(-90deg);   /* 90° sens anti-horaire */
    transform: rotate(180deg);   /* 180° (retourné) */
}

/* Rotation complète */
.element {
    transform: rotate(360deg);   /* Tour complet */
}

/* Unités rotation */
.element {
    transform: rotate(45deg);    /* Degrés (0-360) */
    transform: rotate(0.25turn); /* Tours (1turn = 360deg) */
    transform: rotate(50grad);   /* Gradians (400grad = 360deg) */
    transform: rotate(0.785rad); /* Radians (2π rad = 360deg) */
}

/* Loader spinning */
.loader {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ========================================
   SKEW (Inclinaison)
   ======================================== */

/* skewX : Inclinaison horizontale */
.element {
    transform: skewX(20deg);   /* Incline vers droite */
    transform: skewX(-20deg);  /* Incline vers gauche */
}

/* skewY : Inclinaison verticale */
.element {
    transform: skewY(15deg);
}

/* skew : X et Y ensemble */
.element {
    transform: skew(10deg, 5deg);  /* skewX: 10deg, skewY: 5deg */
}

/* Effet parallax/vitesse */
.speed-lines {
    transform: skewX(-15deg);
}

/* ========================================
   COMBINAISON TRANSFORMS
   ======================================== */

/* Ordre IMPORTANT : translate → rotate → scale */

/* ✅ BON ORDRE */
.element {
    transform: translate(50px, 50px) rotate(45deg) scale(1.2);
}
/* 1. Déplace 50px/50px
   2. Rotation 45°
   3. Agrandit 1.2×
*/

/* ❌ ORDRE DIFFÉRENT = RÉSULTAT DIFFÉRENT */
.element {
    transform: rotate(45deg) translate(50px, 50px) scale(1.2);
}
/* Translate APRÈS rotate = direction différente */

/* Exemple hover complexe */
.card {
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-10px) scale(1.05) rotate(2deg);
}
/* Lève, agrandit légèrement, incline 2° */

/* ========================================
   TRANSFORM-ORIGIN (Point pivot)
   ======================================== */

/* Par défaut : center (50% 50%) */
.element {
    transform-origin: center;  /* Défaut */
    transform: rotate(45deg);  /* Rotation autour centre */
}

/* Origine custom */
.element {
    transform-origin: top left;  /* Rotation autour coin haut-gauche */
    transform: rotate(45deg);
}

/* Valeurs possibles */
.element {
    transform-origin: center;           /* 50% 50% */
    transform-origin: top;              /* 50% 0% */
    transform-origin: top right;        /* 100% 0% */
    transform-origin: right;            /* 100% 50% */
    transform-origin: bottom right;     /* 100% 100% */
    transform-origin: bottom;           /* 50% 100% */
    transform-origin: bottom left;      /* 0% 100% */
    transform-origin: left;             /* 0% 50% */
    transform-origin: 20px 40px;        /* Position exacte */
    transform-origin: 30% 70%;          /* Pourcentages */
}

/* Exemple : Porte qui s'ouvre */
.door {
    transform-origin: left center;  /* Pivot côté gauche */
    transition: transform 0.5s ease;
}

.door.open {
    transform: rotateY(90deg);  /* S'ouvre comme vraie porte */
}
```

### 2.2 Transform 3D

```css
/* Transforms 3D = Manipulation dans espace 3D */

/* ========================================
   PERSPECTIVE (Profondeur 3D)
   ======================================== */

/* Perspective sur parent = active 3D pour enfants */
.container {
    perspective: 1000px;  /* Distance "caméra" (px) */
}

/* Plus perspective grande = effet 3D subtil */
/* Plus perspective petite = effet 3D prononcé */

.container {
    perspective: 2000px;  /* Effet 3D léger */
}

.container {
    perspective: 500px;   /* Effet 3D fort */
}

/* perspective-origin : Point de vue */
.container {
    perspective: 1000px;
    perspective-origin: center;      /* Vue de face (défaut) */
    perspective-origin: top;         /* Vue du dessus */
    perspective-origin: 50% 50%;     /* Custom */
}

/* ========================================
   TRANSLATE 3D
   ======================================== */

/* translateZ : Profondeur (avant/arrière) */
.element {
    transform: translateZ(100px);   /* 100px vers avant */
    transform: translateZ(-100px);  /* 100px vers arrière */
}

/* translate3d : X, Y, Z ensemble */
.element {
    transform: translate3d(50px, 30px, 100px);
    /* X: 50px, Y: 30px, Z: 100px */
}

/* Parallax effect */
.layer-1 {
    transform: translateZ(0px);     /* Fond (loin) */
}

.layer-2 {
    transform: translateZ(50px);    /* Milieu */
}

.layer-3 {
    transform: translateZ(100px);   /* Avant (proche) */
}

/* ========================================
   ROTATE 3D
   ======================================== */

/* rotateX : Rotation axe horizontal */
.element {
    transform: rotateX(45deg);   /* Bascule avant/arrière */
}

/* rotateY : Rotation axe vertical */
.element {
    transform: rotateY(45deg);   /* Tourne gauche/droite */
}

/* rotateZ : Rotation axe profondeur (= rotate 2D) */
.element {
    transform: rotateZ(45deg);   /* = rotate(45deg) */
}

/* rotate3d : Rotation axe custom */
.element {
    transform: rotate3d(1, 1, 0, 45deg);
    /* Axe (1,1,0), angle 45deg */
}

/* Card flip effet */
.card-container {
    perspective: 1000px;
}

.card {
    transition: transform 0.6s;
    transform-style: preserve-3d;  /* Enfants en 3D */
}

.card:hover {
    transform: rotateY(180deg);  /* Flip horizontal */
}

.card-front,
.card-back {
    backface-visibility: hidden;  /* Cache face arrière */
}

.card-back {
    transform: rotateY(180deg);  /* Face arrière retournée */
}

/* ========================================
   SCALE 3D
   ======================================== */

/* scaleZ : Profondeur (rare) */
.element {
    transform: scaleZ(2);  /* Profondeur ×2 */
}

/* scale3d : X, Y, Z */
.element {
    transform: scale3d(1.5, 1.5, 2);
    /* Largeur ×1.5, hauteur ×1.5, profondeur ×2 */
}

/* ========================================
   TRANSFORM-STYLE
   ======================================== */

/* preserve-3d : Enfants en 3D (pas aplatis) */
.parent {
    transform-style: preserve-3d;
}

/* flat : Enfants aplatis 2D (défaut) */
.parent {
    transform-style: flat;
}

/* ========================================
   BACKFACE-VISIBILITY
   ======================================== */

/* visible : Face arrière visible (défaut) */
.element {
    backface-visibility: visible;
}

/* hidden : Face arrière cachée */
.element {
    backface-visibility: hidden;
}

/* Essentiel pour card flip */
.card-face {
    backface-visibility: hidden;
}
```

---

## 3. CSS Animations (@keyframes)

### 3.1 Syntaxe @keyframes

```css
/* @keyframes = Définir séquence animation */

/* Syntaxe de base */
@keyframes nom-animation {
    from {
        /* État initial (0%) */
        opacity: 0;
    }
    
    to {
        /* État final (100%) */
        opacity: 1;
    }
}

/* Avec pourcentages (plus flexible) */
@keyframes fade-slide {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Multi-étapes */
@keyframes bounce {
    0% {
        transform: translateY(0);
    }
    
    50% {
        transform: translateY(-20px);
    }
    
    100% {
        transform: translateY(0);
    }
}

/* Étapes multiples complexes */
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    
    50% {
        transform: scale(1.1);
        opacity: 0.8;
    }
}

/* Appliquer animation */
.element {
    animation-name: fade-slide;
    animation-duration: 1s;
}

/* Ou raccourci */
.element {
    animation: fade-slide 1s;
}
```

### 3.2 animation-name et animation-duration

```css
/* animation-name : Nom @keyframes à utiliser */
.element {
    animation-name: fade-in;
}

/* animation-duration : Durée */
.element {
    animation-duration: 2s;    /* 2 secondes */
    animation-duration: 500ms; /* 500 millisecondes */
}

/* Exemple complet */
@keyframes slide-in {
    from {
        transform: translateX(-100%);
    }
    
    to {
        transform: translateX(0);
    }
}

.notification {
    animation-name: slide-in;
    animation-duration: 0.5s;
}
```

### 3.3 animation-timing-function

```css
/* Timing function (identique transitions) */

.element {
    animation-timing-function: ease;         /* Défaut */
    animation-timing-function: linear;
    animation-timing-function: ease-in;
    animation-timing-function: ease-out;
    animation-timing-function: ease-in-out;
    animation-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
    animation-timing-function: steps(5);
}

/* Différent timing par étape */
@keyframes complex {
    0% {
        opacity: 0;
        animation-timing-function: ease-in;
    }
    
    50% {
        opacity: 1;
        animation-timing-function: ease-out;
    }
    
    100% {
        opacity: 0;
    }
}
```

### 3.4 animation-delay

```css
/* Délai avant démarrage */

.element {
    animation-delay: 1s;     /* Démarre après 1 seconde */
    animation-delay: 500ms;  /* Démarre après 500ms */
}

/* Délai négatif (démarre "au milieu") */
.element {
    animation-delay: -0.5s;  /* Démarre 0.5s dans animation */
}

/* Cascade animations */
.item-1 { animation-delay: 0s; }
.item-2 { animation-delay: 0.1s; }
.item-3 { animation-delay: 0.2s; }
.item-4 { animation-delay: 0.3s; }
```

### 3.5 animation-iteration-count

```css
/* Nombre de répétitions */

.element {
    animation-iteration-count: 1;        /* 1 fois (défaut) */
    animation-iteration-count: 3;        /* 3 fois */
    animation-iteration-count: infinite; /* Infini (boucle) */
}

/* Exemple loader infini */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.loader {
    animation: spin 1s linear infinite;
}
```

### 3.6 animation-direction

```css
/* Direction lecture animation */

.element {
    /* normal : 0% → 100% (défaut) */
    animation-direction: normal;
}

.element {
    /* reverse : 100% → 0% (inverse) */
    animation-direction: reverse;
}

.element {
    /* alternate : 0% → 100%, 100% → 0%, 0% → 100%... */
    animation-direction: alternate;
}

.element {
    /* alternate-reverse : 100% → 0%, 0% → 100%, 100% → 0%... */
    animation-direction: alternate-reverse;
}

/* Exemple pendule */
@keyframes swing {
    from { transform: rotate(-10deg); }
    to { transform: rotate(10deg); }
}

.pendulum {
    animation: swing 1s ease-in-out infinite alternate;
}
/* Oscille -10° ↔ 10° en boucle */
```

### 3.7 animation-fill-mode

```css
/* État avant/après animation */

.element {
    /* none : Pas d'effet avant/après (défaut) */
    animation-fill-mode: none;
}

.element {
    /* forwards : Garde état final (100%) après fin */
    animation-fill-mode: forwards;
}

.element {
    /* backwards : Applique état initial (0%) avant démarrage */
    animation-fill-mode: backwards;
}

.element {
    /* both : forwards + backwards */
    animation-fill-mode: both;
}

/* Exemple fade-in qui reste */
@keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}

.element {
    opacity: 0;  /* Initial */
    animation: fade-in 1s ease forwards;
    /* Reste opacity: 1 après animation */
}

/* Sans forwards, reviendrait à opacity: 0 */
```

### 3.8 animation-play-state

```css
/* Pause/Reprendre animation */

.element {
    animation-play-state: running;  /* En cours (défaut) */
    animation-play-state: paused;   /* Pause */
}

/* Pause au hover */
.loader {
    animation: spin 2s linear infinite;
}

.loader:hover {
    animation-play-state: paused;
}

/* Contrôle JavaScript */
.element.paused {
    animation-play-state: paused;
}
```

### 3.9 Animation Raccourci

```css
/* Syntaxe complète raccourci */
animation: name duration timing-function delay iteration-count direction fill-mode play-state;

/* Exemples */

/* Simple */
.element {
    animation: fade-in 1s;
}

/* Complet */
.element {
    animation: slide-in 0.5s ease-out 0.2s 1 normal forwards running;
}

/* Infini */
.element {
    animation: spin 2s linear infinite;
}

/* Multiple animations */
.element {
    animation: fade-in 1s ease-out,
               slide-up 1s ease-out,
               scale-up 1s ease-out;
}

/* Paramètres différents */
.element {
    animation: fade-in 0.5s ease-out forwards,
               rotate 2s linear infinite;
}
```

---

## 4. Animations Avancées

### 4.1 Loaders et Spinners

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Loaders CSS</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            gap: 60px;
            background-color: #f5f5f5;
            flex-wrap: wrap;
        }
        
        /* Spinner classique */
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Dots pulsing */
        .dots {
            display: flex;
            gap: 10px;
        }
        
        .dot {
            width: 15px;
            height: 15px;
            background-color: #3498db;
            border-radius: 50%;
            animation: pulse 1.4s ease-in-out infinite;
        }
        
        .dot:nth-child(1) { animation-delay: 0s; }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            50% {
                transform: scale(1.2);
                opacity: 1;
            }
        }
        
        /* Bars bouncing */
        .bars {
            display: flex;
            gap: 5px;
            align-items: flex-end;
            height: 50px;
        }
        
        .bar {
            width: 8px;
            background-color: #3498db;
            animation: bounce 1.2s ease-in-out infinite;
        }
        
        .bar:nth-child(1) { animation-delay: 0s; }
        .bar:nth-child(2) { animation-delay: 0.1s; }
        .bar:nth-child(3) { animation-delay: 0.2s; }
        .bar:nth-child(4) { animation-delay: 0.3s; }
        .bar:nth-child(5) { animation-delay: 0.4s; }
        
        @keyframes bounce {
            0%, 100% { height: 10px; }
            50% { height: 50px; }
        }
    </style>
</head>
<body>
    <div class="spinner"></div>
    
    <div class="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    
    <div class="bars">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</body>
</html>
```

### 4.2 Animations Entrée/Sortie

```css
/* Fade animations */

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes fadeOut {
    from {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}

/* Slide animations */

@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideInUp {
    from {
        transform: translateY(100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@keyframes slideInDown {
    from {
        transform: translateY(-100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Zoom animations */

@keyframes zoomIn {
    from {
        transform: scale(0);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

@keyframes zoomOut {
    from {
        transform: scale(1);
        opacity: 1;
    }
    to {
        transform: scale(0);
        opacity: 0;
    }
}

/* Bounce entrée */

@keyframes bounceIn {
    0% {
        transform: scale(0.3);
        opacity: 0;
    }
    50% {
        transform: scale(1.05);
        opacity: 1;
    }
    70% {
        transform: scale(0.9);
    }
    100% {
        transform: scale(1);
    }
}

/* Utilisation */

.modal {
    animation: fadeIn 0.3s ease-out;
}

.notification {
    animation: slideInRight 0.5s ease-out;
}

.card {
    animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### 4.3 Animations Continues

```css
/* Floating effect */

@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-20px);
    }
}

.floating-element {
    animation: float 3s ease-in-out infinite;
}

/* Breathing/Pulsing */

@keyframes breathe {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

.pulse-button {
    animation: breathe 2s ease-in-out infinite;
}

/* Shimmer loading */

@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

.skeleton {
    background: linear-gradient(
        90deg,
        #f0f0f0 25%,
        #e0e0e0 50%,
        #f0f0f0 75%
    );
    background-size: 1000px 100%;
    animation: shimmer 2s infinite;
}

/* Gradient animé */

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.animated-gradient {
    background: linear-gradient(
        45deg,
        #667eea,
        #764ba2,
        #f093fb,
        #4facfe
    );
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}
```

---

## 5. Performance Animations

### 5.1 Propriétés Performantes

```css
/* ========================================
   GPU-ACCELERATED (60fps garanti)
   ======================================== */

/* ✅ TOUJOURS UTILISER */

/* Transform */
.element {
    transform: translateX(100px);
    transform: translateY(50px);
    transform: translate(100px, 50px);
    transform: scale(1.5);
    transform: rotate(45deg);
    transform: translate3d(50px, 30px, 0);  /* Force GPU */
}

/* Opacity */
.element {
    opacity: 0.5;
}

/* Filter */
.element {
    filter: blur(5px);
    filter: brightness(1.2);
}

/* ========================================
   ÉVITER (Déclenchent reflow/repaint)
   ======================================== */

/* ❌ PAS PERFORMANT */

/* Width/Height */
.element {
    width: 200px;      /* Déclenche reflow */
    height: 300px;     /* Déclenche reflow */
}

/* Position (top, left, right, bottom) */
.element {
    top: 100px;        /* Déclenche reflow */
    left: 50px;        /* Déclenche reflow */
}

/* Margin/Padding */
.element {
    margin-left: 20px; /* Déclenche reflow */
    padding: 10px;     /* Déclenche reflow */
}

/* ========================================
   OPTIMISATION : REMPLACEMENTS
   ======================================== */

/* Déplacer élément */

/* ❌ Lent (reflow) */
.element {
    transition: left 0.3s;
}
.element:hover {
    left: 100px;
}

/* ✅ Rapide (GPU) */
.element {
    transition: transform 0.3s;
}
.element:hover {
    transform: translateX(100px);
}

/* Agrandir élément */

/* ❌ Lent (reflow) */
.element {
    transition: width 0.3s, height 0.3s;
}
.element:hover {
    width: 300px;
    height: 300px;
}

/* ✅ Rapide (GPU) */
.element {
    transition: transform 0.3s;
}
.element:hover {
    transform: scale(1.5);
}

/* Disparaître élément */

/* ❌ Lent (reflow) */
.element {
    transition: height 0.3s;
}
.element.hidden {
    height: 0;
}

/* ✅ Rapide (GPU) */
.element {
    transition: opacity 0.3s, transform 0.3s;
}
.element.hidden {
    opacity: 0;
    transform: scale(0);
}
```

### 5.2 will-change Property

```css
/* will-change : Prévient navigateur qu'animation arrive */

/* ✅ UTILISER */

.element {
    will-change: transform, opacity;
}

/* Navigateur prépare GPU, optimise */

/* ⚠️ RÈGLES will-change */

/* 1. Utiliser AVANT animation (pas pendant) */

/* Bon */
.button {
    will-change: transform;
    transition: transform 0.3s;
}

.button:hover {
    transform: scale(1.1);
}

/* 2. Retirer APRÈS animation */

.element {
    will-change: transform;
    animation: slide 1s;
}

.element.animation-complete {
    will-change: auto;  /* Libère ressources */
}

/* 3. NE PAS utiliser sur trop d'éléments */

/* ❌ Mauvais (tout le document) */
* {
    will-change: transform;
}

/* ✅ Bon (éléments spécifiques qui animent) */
.animated-card {
    will-change: transform;
}

/* 4. Propriétés supportées */

.element {
    will-change: auto;                    /* Défaut, aucune optimisation */
    will-change: scroll-position;         /* Scroll */
    will-change: contents;                /* Contenu change */
    will-change: transform;               /* Transform */
    will-change: opacity;                 /* Opacity */
    will-change: transform, opacity;      /* Multiple */
}

/* Exemple avec JavaScript */

/*
element.addEventListener('mouseenter', function() {
    this.style.willChange = 'transform';
});

element.addEventListener('animationend', function() {
    this.style.willChange = 'auto';
});
*/
```

### 5.3 Hardware Acceleration

```css
/* Forcer GPU acceleration */

/* translate3d avec Z=0 */
.element {
    transform: translate3d(100px, 50px, 0);
}
/* Z=0 mais force GPU quand même */

/* translateZ(0) hack */
.element {
    transform: translateZ(0);
}
/* Ne fait rien visuellement mais active GPU */

/* Exemple performance */

/* ❌ Pas GPU */
.slow {
    transition: margin-left 0.5s;
}

.slow:hover {
    margin-left: 100px;
}

/* ✅ GPU-accelerated */
.fast {
    transform: translateZ(0);  /* Force GPU */
    transition: transform 0.5s;
}

.fast:hover {
    transform: translate3d(100px, 0, 0);
}

/* Backface-visibility hidden */
.element {
    backface-visibility: hidden;
}
/* Optimisation GPU (cache face arrière) */
```

### 5.4 Performance Best Practices

```css
/* ========================================
   RÈGLES D'OR PERFORMANCE
   ======================================== */

/* 1. Animer UNIQUEMENT transform + opacity */

/* ✅ Performant */
.element {
    transition: transform 0.3s, opacity 0.3s;
}

/* ❌ Lent */
.element {
    transition: width 0.3s, margin 0.3s, top 0.3s;
}

/* 2. Utiliser translate au lieu position */

/* ❌ */
.element {
    position: absolute;
    left: 0;
    transition: left 0.3s;
}

.element:hover {
    left: 100px;
}

/* ✅ */
.element {
    position: absolute;
    left: 0;
    transition: transform 0.3s;
}

.element:hover {
    transform: translateX(100px);
}

/* 3. Durées courtes (< 500ms généralement) */

.element {
    transition: transform 0.3s;  /* ✅ Bon */
}

.element {
    transition: transform 2s;    /* ⚠️ Trop long, frustrant */
}

/* 4. Réduire animations sur mobile */

@media (max-width: 768px) {
    .element {
        transition-duration: 0.2s;  /* Plus rapide mobile */
    }
}

/* 5. Respecter prefers-reduced-motion */

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* 6. Tester avec DevTools Performance */

/* Chrome DevTools → Performance Tab
   Enregistrer animation, analyser FPS
   Objectif : 60fps constant
*/

/* 7. Limiter animations simultanées */

/* ❌ Trop d'animations */
.element {
    animation: spin 1s, pulse 1s, float 1s, shimmer 1s;
}

/* ✅ Animations ciblées */
.element {
    animation: fadeIn 0.5s;
}
```

---

## 6. Exercices Pratiques

### Exercice 1 : Boutons Animés

**Objectif :** Créer 3 boutons avec hover effects différents.

**Consignes :**
- Bouton 1 : Scale + shadow
- Bouton 2 : Slide background
- Bouton 3 : Rotate + scale

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boutons Animés</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            gap: 30px;
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
            flex-wrap: wrap;
        }
        
        .button {
            padding: 15px 40px;
            font-size: 1rem;
            font-weight: bold;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Bouton 1 : Scale + Shadow */
        .button-1 {
            background-color: #3498db;
            color: white;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .button-1:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 10px 30px rgba(52, 152, 219, 0.4);
        }
        
        .button-1:active {
            transform: translateY(-2px) scale(1.02);
        }
        
        /* Bouton 2 : Slide Background */
        .button-2 {
            background: linear-gradient(to right, #2ecc71 50%, #27ae60 50%);
            background-size: 200% 100%;
            background-position: right bottom;
            color: white;
            transition: background-position 0.4s ease;
        }
        
        .button-2:hover {
            background-position: left bottom;
        }
        
        /* Bouton 3 : Rotate + Scale */
        .button-3 {
            background-color: #e74c3c;
            color: white;
            transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        .button-3:hover {
            transform: rotate(5deg) scale(1.1);
        }
        
        .button-3:active {
            transform: rotate(2deg) scale(1.05);
        }
    </style>
</head>
<body>
    <button class="button button-1">Scale + Shadow</button>
    <button class="button button-2">Slide Background</button>
    <button class="button button-3">Rotate + Scale</button>
</body>
</html>
```

</details>

### Exercice 2 : Loading Spinner

**Objectif :** Créer un spinner de chargement professionnel.

**Consignes :**
- Animation rotation infinie
- Smooth et fluide
- Optionnel : ajouter texte "Loading..."

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loading Spinner</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #2c3e50;
            font-family: Arial, sans-serif;
        }
        
        .loader-container {
            text-align: center;
        }
        
        .spinner {
            width: 60px;
            height: 60px;
            border: 6px solid rgba(255, 255, 255, 0.1);
            border-top-color: #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }
        
        .loading-text {
            color: white;
            font-size: 1.2rem;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 0.5;
            }
            50% {
                opacity: 1;
            }
        }
        
        /* Dots animés */
        .dots {
            display: inline-block;
        }
        
        .dots::after {
            content: '';
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% {
                content: '';
            }
            40% {
                content: '.';
            }
            60% {
                content: '..';
            }
            80%, 100% {
                content: '...';
            }
        }
    </style>
</head>
<body>
    <div class="loader-container">
        <div class="spinner"></div>
        <p class="loading-text">Loading<span class="dots"></span></p>
    </div>
</body>
</html>
```

</details>

### Exercice 3 : Card Flip

**Objectif :** Carte qui se retourne au hover (recto/verso).

**Consignes :**
- Perspective 3D
- Rotation smooth
- Backface-visibility hidden

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Flip</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
        }
        
        .card-container {
            perspective: 1000px;
            width: 300px;
            height: 400px;
        }
        
        .card {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
        }
        
        .card-container:hover .card {
            transform: rotateY(180deg);
        }
        
        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }
        
        .card-front {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .card-back {
            background: white;
            color: #2c3e50;
            transform: rotateY(180deg);
        }
        
        .card-front h2 {
            font-size: 2rem;
            margin-bottom: 20px;
        }
        
        .card-front p {
            text-align: center;
            opacity: 0.9;
        }
        
        .card-back h2 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: #667eea;
        }
        
        .card-back p {
            text-align: center;
            line-height: 1.6;
        }
        
        .flip-hint {
            position: absolute;
            bottom: 20px;
            font-size: 0.9rem;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="card-container">
        <div class="card">
            <div class="card-face card-front">
                <h2>Front Side</h2>
                <p>Hover to flip the card and reveal the hidden content on the back.</p>
                <span class="flip-hint">Hover me ➜</span>
            </div>
            
            <div class="card-face card-back">
                <h2>Back Side</h2>
                <p>This is the back of the card with additional information. CSS 3D transforms make this smooth flip effect possible without JavaScript!</p>
            </div>
        </div>
    </div>
</body>
</html>
```

</details>

---

## 7. Projet du Module : Landing Page Animée

### 7.1 Cahier des Charges

**Créer une landing page avec animations professionnelles :**

**Spécifications techniques :**
- Hero avec texte animé (fade + slide)
- Bouton CTA avec hover effects
- Features section (cards avec stagger animation)
- Stats counters (nombre qui monte)
- Testimonials carousel (slide animation)
- Scroll reveal animations
- Loading screen au chargement
- Toutes animations performantes (60fps)
- prefers-reduced-motion support
- Code CSS externe validé

### 7.2 Solution Complète

<details>
<summary>Voir la solution complète du projet (HTML)</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page Animée</title>
    <link rel="stylesheet" href="landing-animated.css">
</head>
<body>
    <!-- Loading Screen -->
    <div class="loading-screen">
        <div class="spinner"></div>
        <p>Chargement<span class="dots"></span></p>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Hero Section -->
        <section class="hero">
            <div class="container">
                <div class="hero-content">
                    <h1 class="hero-title">
                        <span class="line">Créez des expériences</span>
                        <span class="line">web extraordinaires</span>
                    </h1>
                    <p class="hero-subtitle">
                        Design moderne, animations fluides, performance optimale
                    </p>
                    <div class="hero-buttons">
                        <a href="#features" class="btn btn-primary">Découvrir</a>
                        <a href="#contact" class="btn btn-secondary">Commencer</a>
                    </div>
                </div>
            </div>
            
            <div class="scroll-indicator">
                <span>Scroll</span>
                <div class="scroll-arrow"></div>
            </div>
        </section>
        
        <!-- Features Section -->
        <section class="features" id="features">
            <div class="container">
                <h2 class="section-title">Fonctionnalités</h2>
                
                <div class="features-grid">
                    <div class="feature-card" data-delay="0">
                        <div class="feature-icon">🚀</div>
                        <h3>Performance</h3>
                        <p>Animations GPU-accelerated pour une fluidité 60fps garantie.</p>
                    </div>
                    
                    <div class="feature-card" data-delay="1">
                        <div class="feature-icon">🎨</div>
                        <h3>Design Moderne</h3>
                        <p>Interface élégante avec micro-interactions délicieuses.</p>
                    </div>
                    
                    <div class="feature-card" data-delay="2">
                        <div class="feature-icon">📱</div>
                        <h3>Responsive</h3>
                        <p>Parfaitement adapté à tous les écrans et devices.</p>
                    </div>
                    
                    <div class="feature-card" data-delay="3">
                        <div class="feature-icon">⚡</div>
                        <h3>Rapide</h3>
                        <p>Chargement ultra-rapide et optimisations avancées.</p>
                    </div>
                    
                    <div class="feature-card" data-delay="4">
                        <div class="feature-icon">🔒</div>
                        <h3>Sécurisé</h3>
                        <p>Protection des données et sécurité renforcée.</p>
                    </div>
                    
                    <div class="feature-card" data-delay="5">
                        <div class="feature-icon">♿</div>
                        <h3>Accessible</h3>
                        <p>Conforme WCAG 2.1 AA pour tous les utilisateurs.</p>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Stats Section -->
        <section class="stats">
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number" data-target="1000">0</div>
                        <div class="stat-label">Projets</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-number" data-target="500">0</div>
                        <div class="stat-label">Clients</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-number" data-target="99">0</div>
                        <div class="stat-label">Satisfaction %</div>
                    </div>
                    
                    <div class="stat-item">
                        <div class="stat-number" data-target="24">0</div>
                        <div class="stat-label">Support 24/7</div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- CTA Section -->
        <section class="cta">
            <div class="container">
                <h2>Prêt à commencer ?</h2>
                <p>Rejoignez des milliers d'utilisateurs satisfaits</p>
                <a href="#" class="btn btn-large">Démarrer gratuitement</a>
            </div>
        </section>
    </div>
    
    <script src="landing-animated.js"></script>
</body>
</html>
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 1/2)</summary>

```css
/* landing-animated.css */

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
    --color-primary: #667eea;
    --color-secondary: #764ba2;
    --color-dark: #2c3e50;
    --color-light: #ecf0f1;
    --color-white: #ffffff;
    
    --transition-fast: 0.2s;
    --transition-normal: 0.3s;
    --transition-slow: 0.6s;
    
    --ease-out: cubic-bezier(0.4, 0.0, 0.2, 1);
    --ease-in-out: cubic-bezier(0.4, 0.0, 0.6, 1);
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--color-dark);
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* ========================================
   LOADING SCREEN
   ======================================== */

.loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    animation: fadeOut 0.5s ease-out 2s forwards;
}

@keyframes fadeOut {
    to {
        opacity: 0;
        visibility: hidden;
    }
}

.spinner {
    width: 60px;
    height: 60px;
    border: 6px solid rgba(255, 255, 255, 0.2);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.loading-screen p {
    color: white;
    font-size: 1.2rem;
}

.dots::after {
    content: '';
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: ''; }
    40% { content: '.'; }
    60% { content: '..'; }
    80%, 100% { content: '...'; }
}

.main-content {
    opacity: 0;
    animation: fadeIn 0.5s ease-out 2.5s forwards;
}

@keyframes fadeIn {
    to { opacity: 1; }
}

/* ========================================
   HERO SECTION
   ======================================== */

.hero {
    min-height: 100vh;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 80%;
    height: 150%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: float 20s ease-in-out infinite;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0) rotate(0deg);
    }
    50% {
        transform: translateY(-30px) rotate(5deg);
    }
}

.hero-content {
    text-align: center;
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 800;
    margin-bottom: 30px;
    line-height: 1.2;
}

.hero-title .line {
    display: block;
    opacity: 0;
    transform: translateY(30px);
    animation: slideUp 0.8s var(--ease-out) forwards;
}

.hero-title .line:nth-child(1) {
    animation-delay: 2.7s;
}

.hero-title .line:nth-child(2) {
    animation-delay: 2.9s;
}

@keyframes slideUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-subtitle {
    font-size: clamp(1.1rem, 3vw, 1.5rem);
    opacity: 0;
    animation: fadeInUp 0.8s var(--ease-out) 3.1s forwards;
    margin-bottom: 40px;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeInUp 0.8s var(--ease-out) 3.3s forwards;
}

/* ========================================
   BUTTONS
   ======================================== */

.btn {
    display: inline-block;
    padding: 15px 40px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 1rem;
    transition: all var(--transition-normal) var(--ease-out);
    position: relative;
    overflow: hidden;
}

.btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
    width: 300px;
    height: 300px;
}

.btn-primary {
    background: white;
    color: var(--color-primary);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
}

.btn-secondary:hover {
    background: white;
    color: var(--color-primary);
    transform: translateY(-3px);
}

.btn-large {
    padding: 20px 60px;
    font-size: 1.2rem;
}

/* ========================================
   SCROLL INDICATOR
   ======================================== */

.scroll-indicator {
    position: absolute;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 100% {
        transform: translateX(-50%) translateY(0);
    }
    50% {
        transform: translateX(-50%) translateY(-10px);
    }
}

.scroll-indicator span {
    display: block;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
    opacity: 0.8;
}

.scroll-arrow {
    width: 30px;
    height: 30px;
    border-left: 2px solid white;
    border-bottom: 2px solid white;
    transform: rotate(-45deg);
    margin: 0 auto;
}

/* ========================================
   FEATURES SECTION
   ======================================== */

.features {
    padding: 100px 0;
    background-color: var(--color-light);
}

.section-title {
    text-align: center;
    font-size: clamp(2rem, 5vw, 3rem);
    margin-bottom: 60px;
    color: var(--color-dark);
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 40px;
}

.feature-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all var(--transition-normal) var(--ease-out);
    opacity: 0;
    transform: translateY(30px);
}

.feature-card.visible {
    animation: slideInUp 0.6s var(--ease-out) forwards;
}

@keyframes slideInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.feature-card[data-delay="0"].visible { animation-delay: 0s; }
.feature-card[data-delay="1"].visible { animation-delay: 0.1s; }
.feature-card[data-delay="2"].visible { animation-delay: 0.2s; }
.feature-card[data-delay="3"].visible { animation-delay: 0.3s; }
.feature-card[data-delay="4"].visible { animation-delay: 0.4s; }
.feature-card[data-delay="5"].visible { animation-delay: 0.5s; }

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
    font-size: 4rem;
    margin-bottom: 20px;
    animation: float 3s ease-in-out infinite;
}

.feature-card:nth-child(even) .feature-icon {
    animation-delay: 1.5s;
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    color: var(--color-primary);
}

.feature-card p {
    color: #666;
    line-height: 1.8;
}
```

</details>

<details>
<summary>Voir la solution complète du projet (CSS - partie 2/2)</summary>

```css
/* ========================================
   STATS SECTION
   ======================================== */

.stats {
    padding: 80px 0;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 40px;
    text-align: center;
}

.stat-item {
    opacity: 0;
    transform: scale(0.8);
}

.stat-item.visible {
    animation: zoomIn 0.6s var(--ease-out) forwards;
}

@keyframes zoomIn {
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.stat-number {
    font-size: clamp(3rem, 8vw, 5rem);
    font-weight: 800;
    margin-bottom: 10px;
}

.stat-label {
    font-size: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.9;
}

/* ========================================
   CTA SECTION
   ======================================== */

.cta {
    padding: 100px 0;
    text-align: center;
    background-color: white;
}

.cta h2 {
    font-size: clamp(2rem, 5vw, 3rem);
    margin-bottom: 20px;
    color: var(--color-dark);
}

.cta p {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 40px;
}

.cta .btn {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    border: none;
}

.cta .btn:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
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
    
    .scroll-indicator {
        animation: none;
    }
    
    .feature-icon {
        animation: none;
    }
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 768px) {
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .btn {
        width: 100%;
        max-width: 300px;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}
```

</details>

<details>
<summary>Voir la solution complète du projet (JavaScript)</summary>

```javascript
// landing-animated.js

// ========================================
// INTERSECTION OBSERVER (Scroll Reveal)
// ========================================

const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observer feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    observer.observe(card);
});

// Observer stats
document.querySelectorAll('.stat-item').forEach(stat => {
    observer.observe(stat);
});

// ========================================
// STATS COUNTER ANIMATION
// ========================================

function animateCounter(element) {
    const target = parseInt(element.dataset.target);
    const duration = 2000; // 2 secondes
    const step = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Observer stats pour counter
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const number = entry.target.querySelector('.stat-number');
            if (number && !number.classList.contains('counted')) {
                number.classList.add('counted');
                animateCounter(number);
            }
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-item').forEach(stat => {
    statsObserver.observe(stat);
});

// ========================================
// SMOOTH SCROLL
// ========================================

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

// ========================================
// HIDE LOADING SCREEN
// ========================================

window.addEventListener('load', () => {
    setTimeout(() => {
        document.querySelector('.loading-screen').style.display = 'none';
    }, 2500);
});
```

</details>

### 7.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Loading screen avec spinner animé
- [ ] Hero avec texte staggered animation
- [ ] Boutons avec hover effects (ripple, scale, shadow)
- [ ] Feature cards scroll reveal (IntersectionObserver)
- [ ] Feature cards stagger delay (0s, 0.1s, 0.2s...)
- [ ] Stats counters qui montent
- [ ] Scroll indicator bounce
- [ ] Background gradient animé (optional)
- [ ] Toutes animations GPU-accelerated (transform, opacity)
- [ ] 60fps maintenu (test Chrome DevTools Performance)
- [ ] prefers-reduced-motion support
- [ ] Responsive mobile
- [ ] Code CSS/JS validé
- [ ] Pas de janky animations

---

## 8. Best Practices Animations

### 8.1 Règles d'Or

```css
/* 1. Animer UNIQUEMENT transform + opacity */

/* ✅ Performant */
.element {
    transition: transform 0.3s, opacity 0.3s;
}

/* ❌ Lent */
.element {
    transition: width 0.3s, height 0.3s, margin 0.3s;
}

/* 2. Durées courtes (< 500ms) */

.button {
    transition: transform 0.2s;  /* ✅ Rapide, réactif */
}

.modal {
    transition: transform 1.5s;  /* ❌ Trop lent, frustrant */
}

/* 3. Subtilité > Spectacle */

/* ✅ Subtil, professionnel */
.card:hover {
    transform: translateY(-5px);
}

/* ❌ Trop voyant, amateur */
.card:hover {
    transform: rotate(360deg) scale(2);
}

/* 4. Intentionnalité */

/* Chaque animation doit avoir but :
   - Guider attention utilisateur
   - Feedback interaction
   - Montrer état système (loading)
   - Hiérarchie visuelle
*/

/* 5. Respecter accessibilité */

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

### 8.2 Animations à Éviter

```css
/* ❌ ÉVITER */

/* Animations automatiques qui boucle indéfiniment (distrayant) */
.annoying {
    animation: bounce 1s infinite;
}

/* Animations trop longues (> 1s généralement) */
.too-slow {
    transition: all 3s;
}

/* Animer toutes propriétés (performance) */
.slow {
    transition: all 0.5s;
}

/* Animations sur scroll (motion sickness) */
.parallax {
    transform: translateY(calc(var(--scroll) * 0.5px));
}

/* Trop d'animations simultanées (circus) */
.chaos {
    animation: spin 1s, bounce 1s, pulse 1s, shimmer 1s, float 1s;
}
```

---

## 9. Checkpoint de Progression

### À la fin de ce Module 13, vous maîtrisez :

**Transitions CSS :**

- [x] transition-property, duration, timing-function, delay
- [x] Propriétés animables (performantes vs lentes)
- [x] Timing functions (ease, cubic-bezier, steps)
- [x] Transitions multiples

**Transforms 2D :**

- [x] translate, scale, rotate, skew
- [x] transform-origin
- [x] Combinaisons transforms

**Transforms 3D :**

- [x] perspective
- [x] rotateX, rotateY, rotateZ
- [x] translate3d, scale3d
- [x] transform-style, backface-visibility

**Animations @keyframes :**

- [x] Syntaxe @keyframes
- [x] animation-name, duration, timing-function
- [x] animation-delay, iteration-count, direction
- [x] animation-fill-mode, play-state
- [x] Raccourci animation

**Animations Avancées :**

- [x] Loaders et spinners
- [x] Animations entrée/sortie
- [x] Animations continues (float, pulse, shimmer)

**Performance :**

- [x] Propriétés GPU-accelerated
- [x] will-change
- [x] Hardware acceleration tricks
- [x] Best practices 60fps

**Best practices :**

- [x] Règles d'or animations
- [x] Animations à éviter
- [x] Accessibilité (prefers-reduced-motion)

### Félicitations Formation HTML+CSS+Animations

**Vous avez maintenant terminé 13 modules complets !**

**Compétences acquises :**

- 🎯 HTML5 sémantique professionnel
- 🎨 CSS moderne (Flexbox, Grid, Responsive)
- ✨ Animations CSS performantes et délicieuses
- 📱 Sites fully responsive multi-devices
- ♿ Accessibilité web complète
- ⚡ Performance 60fps optimisée

**Prochaines étapes :**

- Module 14 : CSS Avancé (variables, filters, clip-path, blend modes)
- Module 15 : Projet Final Intégral
- JavaScript avancé
- Frameworks CSS (Tailwind, Bootstrap)
- Preprocessors (Sass, Less)

---

**Module 13 Terminé - Bravo ! 🎉 ✨**

**Statistiques Module 13 :**

- 1 projet complet (Landing page animée professionnelle)
- 3 exercices progressifs avec solutions
- Transitions CSS maîtrisées
- Transforms 2D/3D maîtrisés
- @keyframes animations complètes
- Performance 60fps garantie
- Loaders, spinners, scroll reveals
- Best practices animations professionnelles

**Félicitations pour cette maîtrise des Animations CSS ! 🚀✨**
