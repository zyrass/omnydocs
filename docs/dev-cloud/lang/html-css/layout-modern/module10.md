---
description: "Maîtriser Flexbox : flex-direction, justify-content, align-items, flex-grow, layouts modernes responsives"
icon: lucide/book-open-check
tags: ["CSS", "FLEXBOX", "LAYOUT", "RESPONSIVE", "FLEX-DIRECTION", "JUSTIFY-CONTENT", "ALIGN-ITEMS"]
---

# X - Flexbox CSS

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : La Révolution du Layout

!!! quote "Analogie pédagogique"
    _Imaginez ranger des **livres sur une étagère**. **Avant Flexbox** (méthode float), vous deviez calculer manuellement la largeur de chaque livre, gérer les espacements avec des marges complexes, empiler avec des hacks CSS (clearfix), et tout cassait au moindre changement. **Avec Flexbox**, vous dites à l'étagère : "Arrange ces livres de gauche à droite, avec espace égal entre eux, et s'ils ne rentrent pas, passe à la ligne suivante". L'étagère s'occupe de TOUT automatiquement : espacement, alignement, distribution, wrap. **Flexbox = Chef d'orchestre du layout**. Vous définissez les règles (direction, alignement, distribution), et Flexbox calcule les positions optimales. Plus de calculs de pourcentages, plus de float incompréhensibles, plus de clearfix. Flexbox a révolutionné le CSS en 2015 (support universel) : navigation responsive en 3 lignes, cards auto-espacées, centrage vertical enfin simple, layouts adaptables sans media queries complexes. Ce module vous transforme en maître Flexbox : vous créerez des layouts modernes, responsives, et maintenables en quelques propriétés._

**Flexbox (Flexible Box Layout)** = Système de layout unidimensionnel pour distribuer l'espace et aligner les éléments.

**Pourquoi Flexbox est ESSENTIEL ?**

✅ **Layouts simples** : 3 lignes CSS vs 50 lignes float  
✅ **Responsive naturel** : S'adapte automatiquement  
✅ **Alignement facile** : Vertical, horizontal, centré  
✅ **Distribution espace** : Automatique et intelligente  
✅ **Ordre flexible** : Réorganiser sans toucher HTML  
✅ **Moins de JavaScript** : Layout géré en CSS pur  

**Avant vs Après Flexbox :**

```css
/* ❌ AVANT FLEXBOX : Navigation avec float */
nav ul {
    list-style: none;
    overflow: hidden;  /* Clearfix */
}

nav li {
    float: left;
    width: 25%;        /* Calcul manuel */
    margin-right: 1%;  /* Espacement */
}

nav li:last-child {
    margin-right: 0;   /* Reset dernier */
}

/* ✅ APRÈS FLEXBOX : 3 lignes */
nav ul {
    display: flex;
    gap: 20px;
}

/* C'est TOUT ! */
```

**Flexbox = Layout unidimensionnel**
- Une dimension à la fois (horizontal OU vertical)
- Pour layouts 2D complexes → CSS Grid (Module 11)

**Ce module couvre TOUT Flexbox du débutant à l'expert.**

---

## 1. Concepts Fondamentaux

### 1.1 Container Flex vs Items Flex

```html
<!-- Structure Flexbox -->
<div class="container">        <!-- ← Flex Container -->
    <div class="item">1</div>  <!-- ← Flex Item -->
    <div class="item">2</div>  <!-- ← Flex Item -->
    <div class="item">3</div>  <!-- ← Flex Item -->
</div>
```

```css
/* Activation Flexbox */
.container {
    display: flex;  /* ← Active Flexbox sur container */
}

/* Les enfants DIRECTS deviennent automatiquement flex items */
/* Petits-enfants ne sont PAS flex items */

/* Exemple */
.flex-container {
    display: flex;
}

/* HTML :
<div class="flex-container">
    <div>Item 1</div>              ← Flex item ✅
    <div>Item 2</div>              ← Flex item ✅
    <div>
        Item 3                     ← Flex item ✅
        <div>Nested</div>          ← PAS flex item ❌ (petit-enfant)
    </div>
</div>
*/
```

**Propriétés Flex : 2 catégories**

| Container (parent) | Items (enfants) |
|--------------------|-----------------|
| `display: flex` | `order` |
| `flex-direction` | `flex-grow` |
| `flex-wrap` | `flex-shrink` |
| `flex-flow` | `flex-basis` |
| `justify-content` | `flex` |
| `align-items` | `align-self` |
| `align-content` | |
| `gap` | |

### 1.2 Les Axes Flexbox

```
┌─────────────────────────────────────────────┐
│    FLEX-DIRECTION: ROW (défaut)             │
│                                             │
│    ┌───┐  ┌───┐  ┌───┐                     │
│    │ 1 │  │ 2 │  │ 3 │                     │
│    └───┘  └───┘  └───┘                     │
│    ────────────────────► Main Axis         │
│    │                                        │
│    │                                        │
│    ▼ Cross Axis                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│    FLEX-DIRECTION: COLUMN                   │
│                                             │
│    │   ┌───┐                                │
│    │   │ 1 │                                │
│    │   └───┘                                │
│    │   ┌───┐                                │
│    ▼   │ 2 │                                │
│ Main   └───┘                                │
│ Axis   ┌───┐                                │
│        │ 3 │                                │
│        └───┘                                │
│        ─────► Cross Axis                    │
└─────────────────────────────────────────────┘
```

**Axes Flexbox :**

- **Main Axis (Axe principal)** : Direction du flux (row = horizontal, column = vertical)
- **Cross Axis (Axe perpendiculaire)** : Perpendiculaire au main axis

**CRUCIAL : Les propriétés dépendent de l'axe**
- `justify-content` : Alignement sur **main axis**
- `align-items` : Alignement sur **cross axis**

```css
/* Row : Main axis = horizontal, Cross axis = vertical */
.container-row {
    display: flex;
    flex-direction: row;
    justify-content: center;  /* Centrage horizontal */
    align-items: center;      /* Centrage vertical */
}

/* Column : Main axis = vertical, Cross axis = horizontal */
.container-column {
    display: flex;
    flex-direction: column;
    justify-content: center;  /* Centrage vertical */
    align-items: center;      /* Centrage horizontal */
}

/* Les axes INVERSENT selon flex-direction ! */
```

---

## 2. Propriétés du Container Flex

### 2.1 display: flex

```css
/* Active Flexbox */
.container {
    display: flex;         /* Block-level flex container */
}

/* Ou inline-flex */
.container-inline {
    display: inline-flex;  /* Inline-level flex container */
}

/* Différence flex vs inline-flex */

/* display: flex */
.flex {
    display: flex;
    /* Container prend 100% largeur (block) */
}

/* display: inline-flex */
.inline-flex {
    display: inline-flex;
    /* Container prend uniquement largeur contenu (inline) */
}

/* Exemple visuel */
<div style="display: flex; background: lightblue;">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
<!-- Fond bleu = toute la largeur -->

<div style="display: inline-flex; background: lightgreen;">
    <div>Item 1</div>
    <div>Item 2</div>
</div>
<!-- Fond vert = largeur items uniquement -->
```

### 2.2 flex-direction

```css
/* Définit la direction du main axis */

/* row (défaut) : Horizontal, gauche → droite */
.container {
    display: flex;
    flex-direction: row;
}
/* ┌───┐ ┌───┐ ┌───┐ */

/* row-reverse : Horizontal, droite → gauche */
.container {
    display: flex;
    flex-direction: row-reverse;
}
/* ┌───┐ ┌───┐ ┌───┐ */
/*   3     2     1   */

/* column : Vertical, haut → bas */
.container {
    display: flex;
    flex-direction: column;
}
/* ┌───┐
   │ 1 │
   └───┘
   ┌───┐
   │ 2 │
   └───┘
   ┌───┐
   │ 3 │
   └───┘ */

/* column-reverse : Vertical, bas → haut */
.container {
    display: flex;
    flex-direction: column-reverse;
}
/* ┌───┐
   │ 3 │
   └───┘
   ┌───┐
   │ 2 │
   └───┘
   ┌───┐
   │ 1 │
   └───┘ */

/* Cas d'usage */

/* Navigation horizontale */
nav {
    display: flex;
    flex-direction: row;
}

/* Sidebar verticale */
aside {
    display: flex;
    flex-direction: column;
}

/* Mobile : inverser ordre */
@media (max-width: 768px) {
    .container {
        flex-direction: column-reverse;
        /* Dernier élément en premier visuellement */
    }
}
```

### 2.3 flex-wrap

```css
/* Contrôle le passage à la ligne (wrap) */

/* nowrap (défaut) : Items sur UNE ligne (peuvent déborder) */
.container {
    display: flex;
    flex-wrap: nowrap;
}
/* ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐ → Dépasse si trop d'items */

/* wrap : Passe à la ligne si nécessaire */
.container {
    display: flex;
    flex-wrap: wrap;
}
/* ┌───┐┌───┐┌───┐
   ┌───┐┌───┐┌───┐ ← Nouvelle ligne */

/* wrap-reverse : Wrap avec lignes inversées */
.container {
    display: flex;
    flex-wrap: wrap-reverse;
}
/* ┌───┐┌───┐┌───┐ ← Ligne 2 (dessus)
   ┌───┐┌───┐┌───┐ ← Ligne 1 (dessous) */

/* Exemple pratique : Grille responsive */
.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.card {
    width: 300px;
}

/* Résultat :
   Desktop (1200px) : 3 cartes par ligne
   Tablet (800px)   : 2 cartes par ligne
   Mobile (400px)   : 1 carte par ligne
   → Automatique sans media queries !
*/
```

### 2.4 flex-flow (Raccourci)

```css
/* flex-flow : Raccourci flex-direction + flex-wrap */

/* Syntaxe : flex-flow: <flex-direction> <flex-wrap>; */

/* Équivalences */
.container {
    flex-direction: row;
    flex-wrap: wrap;
}
/* = */
.container {
    flex-flow: row wrap;
}

/* Autres exemples */
.container {
    flex-flow: column nowrap;
    /* = flex-direction: column; + flex-wrap: nowrap; */
}

.container {
    flex-flow: row-reverse wrap;
}

.container {
    flex-flow: column-reverse wrap-reverse;
}

/* Valeur unique (direction seulement) */
.container {
    flex-flow: column;
    /* = flex-direction: column; wrap reste défaut (nowrap) */
}
```

### 2.5 justify-content

```css
/* Aligne items sur MAIN AXIS (axe principal) */

/* flex-start (défaut) : Début du main axis */
.container {
    display: flex;
    justify-content: flex-start;
}
/* ┌───┐┌───┐┌───┐                    */

/* flex-end : Fin du main axis */
.container {
    display: flex;
    justify-content: flex-end;
}
/*                    ┌───┐┌───┐┌───┐ */

/* center : Centré sur main axis */
.container {
    display: flex;
    justify-content: center;
}
/*          ┌───┐┌───┐┌───┐          */

/* space-between : Espace entre items (pas sur bords) */
.container {
    display: flex;
    justify-content: space-between;
}
/* ┌───┐      ┌───┐      ┌───┐ */

/* space-around : Espace autour items (demi-espace bords) */
.container {
    display: flex;
    justify-content: space-around;
}
/*   ┌───┐    ┌───┐    ┌───┐   */

/* space-evenly : Espace égal partout (inclus bords) */
.container {
    display: flex;
    justify-content: space-evenly;
}
/*    ┌───┐    ┌───┐    ┌───┐    */

/* Visualisation différences space-* */

/* space-between : |Item   Item   Item| */
/*                   ↑ 0    ↑ X    ↑ X    ↑ 0 */

/* space-around :   | Item  Item  Item | */
/*                   ↑ X/2  ↑ X    ↑ X    ↑ X/2 */

/* space-evenly :   | Item  Item  Item | */
/*                   ↑ X    ↑ X    ↑ X    ↑ X */

/* Cas d'usage */

/* Navigation centrée */
nav {
    display: flex;
    justify-content: center;
}

/* Navigation spacée */
nav {
    display: flex;
    justify-content: space-between;
}

/* Boutons alignés droite */
.button-group {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
```

### 2.6 align-items

```css
/* Aligne items sur CROSS AXIS (axe perpendiculaire) */

/* stretch (défaut) : Items s'étirent sur cross axis */
.container {
    display: flex;
    align-items: stretch;
    height: 200px;
}
/* Items prennent 200px hauteur (si flex-direction: row) */

/* flex-start : Début du cross axis */
.container {
    display: flex;
    align-items: flex-start;
    height: 200px;
}
/* Items en haut du container */

/* flex-end : Fin du cross axis */
.container {
    display: flex;
    align-items: flex-end;
    height: 200px;
}
/* Items en bas du container */

/* center : Centré sur cross axis */
.container {
    display: flex;
    align-items: center;
    height: 200px;
}
/* Items centrés verticalement */

/* baseline : Aligné sur ligne de base du texte */
.container {
    display: flex;
    align-items: baseline;
}
/* Items alignés sur baseline texte (utile si tailles polices différentes) */

/* Centrage parfait (horizontal + vertical) */
.center-perfect {
    display: flex;
    justify-content: center;  /* Horizontal (main axis) */
    align-items: center;      /* Vertical (cross axis) */
    height: 100vh;
}

/* Hero section centrée */
.hero {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    text-align: center;
}
```

### 2.7 align-content

```css
/* Aligne LIGNES sur cross axis (multi-lignes uniquement) */
/* ⚠️ Fonctionne SEULEMENT si flex-wrap: wrap ET plusieurs lignes */

/* stretch (défaut) : Lignes s'étirent */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: stretch;
    height: 400px;
}

/* flex-start : Lignes au début */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    height: 400px;
}

/* flex-end : Lignes à la fin */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: flex-end;
    height: 400px;
}

/* center : Lignes centrées */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    height: 400px;
}

/* space-between : Espace entre lignes */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: space-between;
    height: 400px;
}

/* space-around : Espace autour lignes */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: space-around;
    height: 400px;
}

/* space-evenly : Espace égal lignes */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: space-evenly;
    height: 400px;
}

/* Différence align-items vs align-content */

/* align-items : Aligne items DANS leur ligne */
.container {
    display: flex;
    align-items: center;  /* Chaque item centré dans sa ligne */
}

/* align-content : Aligne les LIGNES elles-mêmes */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: center;  /* Les lignes centrées dans container */
}
```

### 2.8 gap (Espacement)

```css
/* gap : Espace entre items (moderne, très pratique) */

/* gap : Espacement uniforme */
.container {
    display: flex;
    gap: 20px;  /* 20px entre items (horizontal ET vertical si wrap) */
}

/* row-gap et column-gap séparés */
.container {
    display: flex;
    flex-wrap: wrap;
    row-gap: 30px;     /* Espace vertical (entre lignes) */
    column-gap: 20px;  /* Espace horizontal (entre colonnes) */
}

/* Raccourci gap (row-gap column-gap) */
.container {
    display: flex;
    flex-wrap: wrap;
    gap: 30px 20px;  /* 30px vertical, 20px horizontal */
}

/* Avant gap : margin sur items */

/* ❌ ANCIEN : Margin avec reset dernier */
.container {
    display: flex;
}

.item {
    margin-right: 20px;
}

.item:last-child {
    margin-right: 0;  /* Reset dernier */
}

/* ✅ MODERNE : gap */
.container {
    display: flex;
    gap: 20px;
}
/* Plus simple, pas de reset nécessaire */

/* gap fonctionne avec flex-wrap */
.cards {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;  /* Espace horizontal ET vertical entre cartes */
}

.card {
    width: 300px;
}
/* Grille responsive automatique avec espacement parfait */
```

---

## 3. Propriétés des Items Flex

### 3.1 order

```css
/* Contrôle l'ORDRE VISUEL des items (sans changer HTML) */

/* Par défaut, order: 0 pour tous items */

.item {
    order: 0;  /* Défaut */
}

/* Ordre croissant : -∞ ... -1, 0, 1 ... +∞ */

/* HTML : <div>A</div><div>B</div><div>C</div> */

.item-a {
    order: 2;
}

.item-b {
    order: 1;
}

.item-c {
    order: 3;
}

/* Ordre visuel : B (1), A (2), C (3) */

/* Valeurs négatives */
.item-first {
    order: -1;  /* Avant tous les autres (qui ont 0) */
}

/* Cas d'usage : Responsive */

/* Desktop : Logo | Nav | Search */
/* Mobile : Nav | Logo | Search */

@media (max-width: 768px) {
    .logo {
        order: 2;  /* Logo au milieu */
    }
    
    .nav {
        order: 1;  /* Nav en premier */
    }
    
    .search {
        order: 3;  /* Search en dernier */
    }
}

/* ⚠️ order change SEULEMENT l'ordre VISUEL */
/* Ordre DOM reste identique (important pour accessibilité) */
/* Tab order (clavier) suit l'ordre HTML, pas order CSS */
```

### 3.2 flex-grow

```css
/* Facteur de croissance (redistribution espace LIBRE) */

/* flex-grow: 0 (défaut) : Ne grandit pas */
.item {
    flex-grow: 0;
}

/* flex-grow: 1 : Grandit pour remplir espace */
.item {
    flex-grow: 1;
}

/* Exemple : 3 items, container 600px */

.container {
    display: flex;
    width: 600px;
}

.item {
    width: 100px;  /* Chaque item : 100px */
    flex-grow: 1;
}

/* Calcul :
   Espace total : 600px
   Espace utilisé : 3 × 100px = 300px
   Espace libre : 600 - 300 = 300px
   
   flex-grow total : 1 + 1 + 1 = 3
   Espace par item : 300 ÷ 3 = 100px
   
   Largeur finale : 100 + 100 = 200px chacun
*/

/* flex-grow différents */

.item-1 {
    width: 100px;
    flex-grow: 1;
}

.item-2 {
    width: 100px;
    flex-grow: 2;  /* Grandit 2× plus */
}

.item-3 {
    width: 100px;
    flex-grow: 1;
}

/* Calcul :
   Espace libre : 300px
   flex-grow total : 1 + 2 + 1 = 4
   
   Item 1 : 100 + (300 × 1/4) = 175px
   Item 2 : 100 + (300 × 2/4) = 250px
   Item 3 : 100 + (300 × 1/4) = 175px
*/

/* Cas d'usage : Layout responsive */

/* Sidebar fixe + Content flexible */
.sidebar {
    width: 250px;
    flex-grow: 0;  /* Ne grandit pas */
}

.content {
    flex-grow: 1;  /* Prend espace restant */
}

/* Navigation avec logo fixe */
.logo {
    width: 150px;
}

.nav {
    flex-grow: 1;  /* Nav prend espace disponible */
}

.search {
    width: 200px;
}
```

### 3.3 flex-shrink

```css
/* Facteur de rétrécissement (si items dépassent) */

/* flex-shrink: 1 (défaut) : Peut rétrécir */
.item {
    flex-shrink: 1;
}

/* flex-shrink: 0 : Ne rétrécit JAMAIS */
.item {
    flex-shrink: 0;
}

/* Exemple : 3 items trop larges */

.container {
    display: flex;
    width: 600px;
}

.item {
    width: 300px;      /* Total : 900px > 600px */
    flex-shrink: 1;
}

/* Calcul :
   Espace total : 600px
   Espace nécessaire : 900px
   Dépassement : 900 - 600 = 300px
   
   flex-shrink total : 1 + 1 + 1 = 3
   Réduction par item : 300 ÷ 3 = 100px
   
   Largeur finale : 300 - 100 = 200px chacun
*/

/* flex-shrink différents */

.item-1 {
    width: 300px;
    flex-shrink: 1;
}

.item-2 {
    width: 300px;
    flex-shrink: 0;  /* Ne rétrécit PAS */
}

.item-3 {
    width: 300px;
    flex-shrink: 2;  /* Rétrécit 2× plus */
}

/* Calcul :
   Dépassement : 300px
   flex-shrink actifs : 1 + 2 = 3 (item-2 ignoré)
   
   Item 1 : 300 - (300 × 1/3) = 200px
   Item 2 : 300 - 0 = 300px (reste fixe)
   Item 3 : 300 - (300 × 2/3) = 100px
*/

/* Cas d'usage : Éléments fixes */

/* Logo ne rétrécit jamais */
.logo {
    width: 150px;
    flex-shrink: 0;
}

/* Nav peut rétrécir */
.nav {
    flex-shrink: 1;
}

/* Image responsive mais pas en dessous de min */
.image {
    min-width: 200px;
    flex-shrink: 1;
}
```

### 3.4 flex-basis

```css
/* Taille de BASE avant distribution espace */

/* flex-basis : Définit taille initiale (priorité sur width) */

.item {
    flex-basis: 200px;  /* Taille de base 200px */
}

/* flex-basis vs width */

.item {
    width: 200px;       /* Taille fixe (peut être override par flex) */
    flex-basis: 300px;  /* ← Gagne (priorité sur width) */
}
/* Résultat : item démarre à 300px */

/* Valeurs flex-basis */

.item {
    flex-basis: auto;       /* Défaut : utilise width/height ou taille contenu */
    flex-basis: 200px;      /* Pixels */
    flex-basis: 20%;        /* Pourcentage du container */
    flex-basis: 10em;       /* Em */
    flex-basis: content;    /* Taille du contenu (moderne) */
}

/* Exemple : Cards égales */

.cards {
    display: flex;
    gap: 20px;
}

.card {
    flex-basis: 300px;  /* Chaque carte démarre à 300px */
    flex-grow: 1;       /* Grandit si espace disponible */
}

/* Responsive avec flex-basis */

.card {
    flex-basis: 100%;   /* Mobile : 100% largeur */
}

@media (min-width: 768px) {
    .card {
        flex-basis: calc(50% - 10px);  /* Tablet : 2 colonnes */
    }
}

@media (min-width: 1024px) {
    .card {
        flex-basis: calc(33.33% - 14px);  /* Desktop : 3 colonnes */
    }
}
```

### 3.5 flex (Raccourci)

```css
/* flex : Raccourci flex-grow + flex-shrink + flex-basis */

/* Syntaxe : flex: <flex-grow> <flex-shrink> <flex-basis>; */

/* Valeurs courantes */

/* flex: 1 */
.item {
    flex: 1;
    /* = flex-grow: 1; flex-shrink: 1; flex-basis: 0%; */
    /* Item prend part égale espace disponible */
}

/* flex: auto */
.item {
    flex: auto;
    /* = flex-grow: 1; flex-shrink: 1; flex-basis: auto; */
    /* Item grandit/rétrécit, base = taille contenu */
}

/* flex: none */
.item {
    flex: none;
    /* = flex-grow: 0; flex-shrink: 0; flex-basis: auto; */
    /* Item fixe, ne grandit ni rétrécit */
}

/* flex: 0 1 auto (défaut) */
.item {
    flex: 0 1 auto;
    /* Ne grandit pas, peut rétrécir, base = auto */
}

/* Exemples pratiques */

/* Colonnes égales */
.column {
    flex: 1;  /* Chaque colonne prend part égale */
}

/* Sidebar fixe + Content flexible */
.sidebar {
    flex: none;
    width: 250px;
}

.content {
    flex: 1;  /* Prend espace restant */
}

/* Cards avec taille minimale */
.card {
    flex: 1 1 300px;
    /* Grandit, rétrécit, base 300px */
}

/* Header : Logo fixe, Nav flexible, Search fixe */
.logo {
    flex: none;
    width: 150px;
}

.nav {
    flex: 1;  /* Prend espace disponible */
}

.search {
    flex: none;
    width: 200px;
}
```

### 3.6 align-self

```css
/* Override align-items pour UN item spécifique */

.container {
    display: flex;
    align-items: center;  /* Tous items centrés */
    height: 200px;
}

.item-special {
    align-self: flex-start;  /* Cet item au début */
}

/* Valeurs identiques à align-items */

.item {
    align-self: auto;        /* Défaut : hérite align-items */
    align-self: flex-start;  /* Début cross axis */
    align-self: flex-end;    /* Fin cross axis */
    align-self: center;      /* Centré cross axis */
    align-self: baseline;    /* Baseline texte */
    align-self: stretch;     /* Étiré cross axis */
}

/* Exemple : Navigation avec logo centré, items alignés différemment */

nav {
    display: flex;
    align-items: center;
    height: 80px;
}

.logo {
    align-self: center;  /* Logo centré (défaut) */
}

.nav-link {
    align-self: flex-start;  /* Liens en haut */
}

.search {
    align-self: flex-end;  /* Search en bas */
}
```

---

## 4. Layouts Courants Flexbox

### 4.1 Navigation Horizontale

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Navigation Flexbox</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #2c3e50;
            padding: 20px 40px;
        }
        
        .logo {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 30px;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .nav-links a:hover {
            color: #3498db;
        }
        
        .nav-cta {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">MonSite</div>
        
        <ul class="nav-links">
            <li><a href="#home">Accueil</a></li>
            <li><a href="#about">À propos</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
        
        <a href="#signup" class="nav-cta">S'inscrire</a>
    </nav>
</body>
</html>
```

### 4.2 Cards Grid Responsive

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Cards Grid Flexbox</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .cards-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
        }
        
        .card {
            flex: 1 1 300px;  /* Grandit, rétrécit, base 300px */
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .card h3 {
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .card p {
            color: #7f8c8d;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Services</h1>
        
        <div class="cards-grid">
            <div class="card">
                <h3>Design</h3>
                <p>Création de designs modernes et responsive pour tous supports.</p>
            </div>
            
            <div class="card">
                <h3>Développement</h3>
                <p>Développement web avec les technologies les plus récentes.</p>
            </div>
            
            <div class="card">
                <h3>SEO</h3>
                <p>Optimisation pour moteurs de recherche et performance.</p>
            </div>
            
            <div class="card">
                <h3>Marketing</h3>
                <p>Stratégie marketing digital et réseaux sociaux.</p>
            </div>
            
            <div class="card">
                <h3>Support</h3>
                <p>Support technique 24/7 pour tous vos projets.</p>
            </div>
        </div>
    </div>
</body>
</html>
```

### 4.3 Holy Grail Layout

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Holy Grail Layout</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            font-family: Arial, sans-serif;
        }
        
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .main-container {
            display: flex;
            flex: 1;  /* Prend espace restant */
        }
        
        aside {
            background-color: #ecf0f1;
            padding: 20px;
            width: 200px;
            flex-shrink: 0;  /* Ne rétrécit pas */
        }
        
        main {
            flex: 1;  /* Prend espace restant */
            padding: 20px;
        }
        
        footer {
            background-color: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .main-container {
                flex-direction: column;
            }
            
            aside {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Holy Grail Layout</h1>
    </header>
    
    <div class="main-container">
        <aside>
            <h2>Sidebar Gauche</h2>
            <ul>
                <li>Lien 1</li>
                <li>Lien 2</li>
                <li>Lien 3</li>
            </ul>
        </aside>
        
        <main>
            <h2>Contenu Principal</h2>
            <p>Lorem ipsum dolor sit amet...</p>
        </main>
        
        <aside>
            <h2>Sidebar Droite</h2>
            <p>Publicités...</p>
        </aside>
    </div>
    
    <footer>
        <p>&copy; 2024 Mon Site</p>
    </footer>
</body>
</html>
```

### 4.4 Centrage Parfait

```css
/* Centrage horizontal + vertical (très courant) */

.center-container {
    display: flex;
    justify-content: center;  /* Horizontal */
    align-items: center;      /* Vertical */
    min-height: 100vh;
}

/* Hero section centrée */
.hero {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
}

/* Modal centrée */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    max-width: 500px;
}
```

---

## 5. Exercices Pratiques

### Exercice 1 : Navigation Responsive

**Objectif :** Créer une navigation qui s'adapte au mobile.

**Consigne :** 
- Desktop : Logo à gauche, liens au centre, bouton à droite
- Mobile : Colonne verticale

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
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #2c3e50;
            padding: 20px 40px;
            gap: 20px;
        }
        
        .logo {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 30px;
            flex: 1;
            justify-content: center;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
        }
        
        .nav-cta {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            flex-shrink: 0;
        }
        
        @media (max-width: 768px) {
            nav {
                flex-direction: column;
                padding: 20px;
            }
            
            .nav-links {
                flex-direction: column;
                align-items: center;
                width: 100%;
            }
            
            .nav-cta {
                width: 100%;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <nav>
        <div class="logo">MonSite</div>
        
        <ul class="nav-links">
            <li><a href="#">Accueil</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Portfolio</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
        
        <a href="#" class="nav-cta">S'inscrire</a>
    </nav>
</body>
</html>
```

</details>

### Exercice 2 : Grille de Cartes Auto-Adaptable

**Objectif :** Créer une grille qui s'adapte automatiquement.

**Consigne :** Cartes de 250px minimum, s'adaptant au nombre par ligne selon largeur écran.

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grille Auto-Adaptable</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            margin-bottom: 40px;
            text-align: center;
            color: #2c3e50;
        }
        
        .cards {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .card {
            flex: 1 1 250px;  /* Clé : base 250px, grandit pour remplir */
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            margin-bottom: 15px;
            color: #3498db;
        }
        
        .card p {
            color: #7f8c8d;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Galerie Auto-Adaptable</h1>
        
        <div class="cards">
            <div class="card">
                <h3>Card 1</h3>
                <p>Description de la carte numéro 1.</p>
            </div>
            
            <div class="card">
                <h3>Card 2</h3>
                <p>Description de la carte numéro 2.</p>
            </div>
            
            <div class="card">
                <h3>Card 3</h3>
                <p>Description de la carte numéro 3.</p>
            </div>
            
            <div class="card">
                <h3>Card 4</h3>
                <p>Description de la carte numéro 4.</p>
            </div>
            
            <div class="card">
                <h3>Card 5</h3>
                <p>Description de la carte numéro 5.</p>
            </div>
            
            <div class="card">
                <h3>Card 6</h3>
                <p>Description de la carte numéro 6.</p>
            </div>
        </div>
    </div>
</body>
</html>
```

**Résultat :**
- 1600px+ : 5 cartes par ligne
- 1200px : 4 cartes par ligne
- 800px : 3 cartes par ligne
- 600px : 2 cartes par ligne
- 400px : 1 carte par ligne

**Tout automatique avec `flex: 1 1 250px` !**

</details>

### Exercice 3 : Layout Sidebar + Content

**Objectif :** Sidebar fixe 250px + Content flexible.

**Consigne :** Sidebar qui passe en haut sur mobile.

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sidebar Layout</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
        }
        
        .layout {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            flex: none;
            width: 250px;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
        }
        
        .sidebar h2 {
            margin-bottom: 20px;
        }
        
        .sidebar ul {
            list-style: none;
        }
        
        .sidebar li {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .sidebar a {
            color: white;
            text-decoration: none;
        }
        
        .content {
            flex: 1;
            padding: 40px;
            background-color: #f5f5f5;
        }
        
        .content h1 {
            margin-bottom: 20px;
            color: #2c3e50;
        }
        
        .content p {
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        @media (max-width: 768px) {
            .layout {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="layout">
        <aside class="sidebar">
            <h2>Menu</h2>
            <ul>
                <li><a href="#">Dashboard</a></li>
                <li><a href="#">Profil</a></li>
                <li><a href="#">Messages</a></li>
                <li><a href="#">Paramètres</a></li>
                <li><a href="#">Déconnexion</a></li>
            </ul>
        </aside>
        
        <main class="content">
            <h1>Dashboard</h1>
            <p>
                Bienvenue sur votre tableau de bord. Voici les statistiques 
                de votre compte et les dernières activités.
            </p>
            <p>
                Sidebar fixe à 250px sur desktop, passe en haut sur mobile 
                grâce à flex-direction: column.
            </p>
            <p>
                Le contenu principal utilise flex: 1 pour prendre tout 
                l'espace restant.
            </p>
        </main>
    </div>
</body>
</html>
```

</details>

---

## 6. Projet du Module : Dashboard Complet

### 6.1 Cahier des Charges

**Créer un dashboard professionnel avec Flexbox :**

**Spécifications techniques :**
- ✅ Header avec logo, nav, profil
- ✅ Sidebar fixe 250px (pliable mobile)
- ✅ Content principal flexible
- ✅ Grid de stats (4 cartes)
- ✅ Section graphiques (2 colonnes)
- ✅ Footer
- ✅ Responsive complet
- ✅ Code CSS externe validé

### 6.2 Solution Complète

<details>
<summary>Voir la solution complète du projet</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Flexbox</title>
    <link rel="stylesheet" href="dashboard.css">
</head>
<body>
    <div class="dashboard">
        <!-- Header -->
        <header class="header">
            <div class="header-left">
                <h1 class="logo">Dashboard</h1>
            </div>
            
            <nav class="header-nav">
                <a href="#">Accueil</a>
                <a href="#">Projets</a>
                <a href="#">Analytics</a>
                <a href="#">Rapports</a>
            </nav>
            
            <div class="header-right">
                <div class="user-profile">
                    <span>Alice Dupont</span>
                    <div class="avatar">AD</div>
                </div>
            </div>
        </header>
        
        <!-- Main Layout -->
        <div class="main-layout">
            <!-- Sidebar -->
            <aside class="sidebar">
                <nav class="sidebar-nav">
                    <a href="#" class="nav-item active">
                        📊 Dashboard
                    </a>
                    <a href="#" class="nav-item">
                        📈 Statistiques
                    </a>
                    <a href="#" class="nav-item">
                        👥 Utilisateurs
                    </a>
                    <a href="#" class="nav-item">
                        ⚙️ Paramètres
                    </a>
                </nav>
            </aside>
            
            <!-- Content -->
            <main class="content">
                <h2 class="page-title">Vue d'ensemble</h2>
                
                <!-- Stats Grid -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon" style="background-color: #3498db;">👥</div>
                        <div class="stat-info">
                            <h3>1,234</h3>
                            <p>Utilisateurs</p>
                        </div>
                        <div class="stat-change positive">+12%</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon" style="background-color: #2ecc71;">💰</div>
                        <div class="stat-info">
                            <h3>45,678 €</h3>
                            <p>Revenus</p>
                        </div>
                        <div class="stat-change positive">+23%</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon" style="background-color: #e74c3c;">📦</div>
                        <div class="stat-info">
                            <h3>567</h3>
                            <p>Commandes</p>
                        </div>
                        <div class="stat-change negative">-3%</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon" style="background-color: #f39c12;">⭐</div>
                        <div class="stat-info">
                            <h3>4.8/5</h3>
                            <p>Satisfaction</p>
                        </div>
                        <div class="stat-change positive">+0.2</div>
                    </div>
                </div>
                
                <!-- Charts Section -->
                <div class="charts-section">
                    <div class="chart-card">
                        <h3>Ventes Mensuelles</h3>
                        <div class="chart-placeholder">
                            📈 Graphique ici
                        </div>
                    </div>
                    
                    <div class="chart-card">
                        <h3>Répartition par Catégorie</h3>
                        <div class="chart-placeholder">
                            🥧 Graphique ici
                        </div>
                    </div>
                </div>
                
                <!-- Recent Activity -->
                <div class="activity-section">
                    <h3>Activité Récente</h3>
                    <div class="activity-list">
                        <div class="activity-item">
                            <div class="activity-icon">✓</div>
                            <div class="activity-content">
                                <p><strong>Commande #1234</strong> complétée</p>
                                <span class="activity-time">Il y a 5 minutes</span>
                            </div>
                        </div>
                        
                        <div class="activity-item">
                            <div class="activity-icon">👤</div>
                            <div class="activity-content">
                                <p><strong>Nouvel utilisateur</strong> inscrit</p>
                                <span class="activity-time">Il y a 12 minutes</span>
                            </div>
                        </div>
                        
                        <div class="activity-item">
                            <div class="activity-icon">💳</div>
                            <div class="activity-content">
                                <p><strong>Paiement reçu</strong> 234,50 €</p>
                                <span class="activity-time">Il y a 1 heure</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
        
        <!-- Footer -->
        <footer class="footer">
            <p>&copy; 2024 Dashboard. Tous droits réservés.</p>
        </footer>
    </div>
</body>
</html>
```

```css
/* dashboard.css */

/* ========================================
   RESET & BASE
   ======================================== */

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f7fa;
    color: #2c3e50;
}

/* ========================================
   DASHBOARD LAYOUT
   ======================================== */

.dashboard {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* ========================================
   HEADER
   ======================================== */

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: white;
    padding: 0 30px;
    height: 70px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.header-left {
    flex-shrink: 0;
}

.logo {
    font-size: 1.5rem;
    color: #3498db;
}

.header-nav {
    display: flex;
    gap: 30px;
    flex: 1;
    justify-content: center;
}

.header-nav a {
    color: #7f8c8d;
    text-decoration: none;
    transition: color 0.3s ease;
}

.header-nav a:hover {
    color: #3498db;
}

.header-right {
    flex-shrink: 0;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 15px;
}

.avatar {
    width: 40px;
    height: 40px;
    background-color: #3498db;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

/* ========================================
   MAIN LAYOUT (Sidebar + Content)
   ======================================== */

.main-layout {
    display: flex;
    flex: 1;
}

/* ========================================
   SIDEBAR
   ======================================== */

.sidebar {
    flex: none;
    width: 250px;
    background-color: #2c3e50;
    padding: 30px 0;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
}

.nav-item {
    padding: 15px 30px;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: all 0.3s ease;
}

.nav-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
}

.nav-item.active {
    background-color: #3498db;
    color: white;
    border-left: 4px solid white;
}

/* ========================================
   CONTENT
   ======================================== */

.content {
    flex: 1;
    padding: 40px;
    overflow-y: auto;
}

.page-title {
    font-size: 2rem;
    margin-bottom: 30px;
    color: #2c3e50;
}

/* ========================================
   STATS GRID
   ======================================== */

.stats-grid {
    display: flex;
    gap: 20px;
    margin-bottom: 40px;
    flex-wrap: wrap;
}

.stat-card {
    flex: 1 1 240px;
    background-color: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;
    gap: 20px;
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    flex-shrink: 0;
}

.stat-info {
    flex: 1;
}

.stat-info h3 {
    font-size: 2rem;
    margin-bottom: 5px;
}

.stat-info p {
    color: #7f8c8d;
    font-size: 0.9rem;
}

.stat-change {
    font-weight: bold;
    font-size: 1.1rem;
    padding: 5px 10px;
    border-radius: 5px;
}

.stat-change.positive {
    color: #2ecc71;
    background-color: rgba(46, 204, 113, 0.1);
}

.stat-change.negative {
    color: #e74c3c;
    background-color: rgba(231, 76, 60, 0.1);
}

/* ========================================
   CHARTS SECTION
   ======================================== */

.charts-section {
    display: flex;
    gap: 20px;
    margin-bottom: 40px;
    flex-wrap: wrap;
}

.chart-card {
    flex: 1 1 400px;
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.chart-card h3 {
    margin-bottom: 20px;
    color: #2c3e50;
}

.chart-placeholder {
    height: 300px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
}

/* ========================================
   ACTIVITY SECTION
   ======================================== */

.activity-section {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.activity-section h3 {
    margin-bottom: 20px;
    color: #2c3e50;
}

.activity-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.activity-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    border-radius: 8px;
    background-color: #f8f9fa;
}

.activity-icon {
    width: 40px;
    height: 40px;
    background-color: #3498db;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.activity-content {
    flex: 1;
}

.activity-content p {
    margin-bottom: 5px;
}

.activity-time {
    color: #95a5a6;
    font-size: 0.85rem;
}

/* ========================================
   FOOTER
   ======================================== */

.footer {
    background-color: white;
    padding: 20px;
    text-align: center;
    border-top: 1px solid #e0e6ed;
}

.footer p {
    color: #7f8c8d;
    font-size: 0.9rem;
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 1024px) {
    .stats-grid {
        flex-wrap: wrap;
    }
    
    .stat-card {
        flex: 1 1 calc(50% - 10px);
    }
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        height: auto;
        padding: 20px;
        gap: 15px;
    }
    
    .header-nav {
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    
    .main-layout {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        order: 2;
    }
    
    .content {
        padding: 20px;
        order: 1;
    }
    
    .stat-card {
        flex: 1 1 100%;
    }
    
    .charts-section {
        flex-direction: column;
    }
}
```

</details>

### 6.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Header avec logo, nav, profil (flex space-between)
- [ ] Sidebar fixe 250px (flex: none)
- [ ] Content flexible (flex: 1)
- [ ] 4 stats cards (flex-wrap)
- [ ] 2 graphiques (flex 2 colonnes)
- [ ] Liste activités (flex-direction: column)
- [ ] Footer
- [ ] Mobile : header column, sidebar en haut
- [ ] Tablet : stats 2 colonnes
- [ ] Desktop : stats 4 colonnes
- [ ] Code CSS externe validé W3C
- [ ] Pas de dépassement (overflow)

---

## 7. Best Practices Flexbox

### 7.1 Règles d'Or

```css
/* 1. Toujours box-sizing: border-box */
*,
*::before,
*::after {
    box-sizing: border-box;
}

/* 2. Préférer gap à margin pour espacement */

/* ❌ ANCIEN */
.item {
    margin-right: 20px;
}

.item:last-child {
    margin-right: 0;
}

/* ✅ MODERNE */
.container {
    display: flex;
    gap: 20px;
}

/* 3. Utiliser flex raccourci */

/* ❌ VERBEUX */
.item {
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 0%;
}

/* ✅ CONCIS */
.item {
    flex: 1;
}

/* 4. flex: 1 vs flex: auto */

.equal-width {
    flex: 1;  /* Largeurs égales (ignores contenu) */
}

.content-based {
    flex: auto;  /* Largeurs basées sur contenu */
}

/* 5. Éviter hauteurs fixes avec flex */

/* ❌ PROBLÈME */
.container {
    display: flex;
    height: 200px;  /* Fixe, peut couper contenu */
}

/* ✅ SOLUTION */
.container {
    display: flex;
    min-height: 200px;  /* Grandit si nécessaire */
}

/* 6. Flex pour layouts, Grid pour grilles complexes */

/* Flex : Une dimension (ligne ou colonne) */
.navigation {
    display: flex;  /* Bon choix */
}

/* Grid : Deux dimensions (lignes ET colonnes) */
.photo-gallery {
    display: grid;  /* Meilleur choix que flex */
}
```

### 7.2 Pièges à Éviter

```css
/* PIÈGE 1 : Oublier flex-wrap */

/* ❌ Items débordent */
.container {
    display: flex;
    /* flex-wrap: nowrap par défaut */
}

/* ✅ Items wrappent */
.container {
    display: flex;
    flex-wrap: wrap;
}

/* PIÈGE 2 : Mauvais axe justify/align */

/* ❌ Confusion axes */
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;  /* Vertical en column */
    align-items: center;      /* Horizontal en column */
}

/* Les axes changent selon flex-direction ! */

/* PIÈGE 3 : align-content sans wrap */

/* ❌ Ne fonctionne pas */
.container {
    display: flex;
    align-content: center;  /* Ignoré sans wrap + multi-lignes */
}

/* ✅ Fonctionne */
.container {
    display: flex;
    flex-wrap: wrap;
    align-content: center;  /* OK si plusieurs lignes */
}

/* PIÈGE 4 : Width avec flex-grow */

/* ❌ Width écrasé */
.item {
    width: 300px;
    flex-grow: 1;  /* width ignoré si espace disponible */
}

/* ✅ Utiliser flex-basis */
.item {
    flex: 1 1 300px;  /* Base 300px, grandit */
}

/* PIÈGE 5 : Marges auto étranges */

/* Margin auto dans flex = espace restant */
.item {
    margin-left: auto;  /* Pousse à droite */
}

/* Utile pour layouts : */
.nav {
    display: flex;
}

.nav-right {
    margin-left: auto;  /* Aligne à droite */
}
```

### 7.3 Performance

```css
/* ✅ Flex est performant par défaut */
/* Navigateurs modernes optimisent bien Flexbox */

/* Éviter changements fréquents flex-basis en JS */
/* Préférer transform pour animations */

/* ❌ LENT (recalcule layout) */
.item {
    animation: grow 1s infinite;
}

@keyframes grow {
    to { flex-basis: 500px; }
}

/* ✅ RAPIDE (GPU) */
.item {
    animation: grow 1s infinite;
}

@keyframes grow {
    to { transform: scaleX(1.5); }
}
```

---

## 8. Checkpoint de Progression

### À la fin de ce Module 10, vous maîtrisez :

**Concepts Flexbox :**

- [x] Container vs Items
- [x] Main axis vs Cross axis
- [x] display: flex vs inline-flex

**Propriétés Container :**

- [x] flex-direction (row, column, reverse)
- [x] flex-wrap (nowrap, wrap, wrap-reverse)
- [x] flex-flow (raccourci)
- [x] justify-content (alignement main axis)
- [x] align-items (alignement cross axis)
- [x] align-content (lignes multi)
- [x] gap (espacement moderne)

**Propriétés Items :**

- [x] order (ordre visuel)
- [x] flex-grow (croissance)
- [x] flex-shrink (rétrécissement)
- [x] flex-basis (base)
- [x] flex (raccourci magique)
- [x] align-self (override individuel)

**Layouts courants :**

- [x] Navigation responsive
- [x] Cards grid auto-adaptable
- [x] Holy Grail layout
- [x] Sidebar + Content
- [x] Centrage parfait

**Best practices :**

- [x] Règles d'or
- [x] Pièges à éviter
- [x] Performance

### Prochaine Étape

**Direction le Module 11** où vous allez :

- Maîtriser CSS Grid (display: grid)
- Layouts bidimensionnels complexes
- grid-template-columns et rows
- grid-area et placement
- Responsive sans media queries
- Grilles imbriquées
- Layouts modernes professionnels

---

**Module 10 Terminé - Bravo ! 🎉 📐**

**Vous avez appris :**

- ✅ Flexbox complet maîtrisé (container + items)
- ✅ Tous les alignements (justify-content, align-items, align-content)
- ✅ Distribution espace intelligente (flex-grow, flex-shrink)
- ✅ Layouts responsives sans media queries complexes
- ✅ gap pour espacement moderne
- ✅ Layouts courants professionnels
- ✅ Best practices Flexbox

**Statistiques Module 10 :**

- 1 projet complet (Dashboard professionnel)
- 3 exercices progressifs avec solutions
- 8 propriétés container maîtrisées
- 6 propriétés items maîtrisées
- 4 layouts courants créés
- Flexbox révolution comprise

**Prochain objectif : Maîtriser CSS Grid (Module 11)**

**Félicitations pour cette maîtrise de Flexbox ! 🚀📐**
