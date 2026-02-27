---
description: "Maîtriser CSS Grid : grid-template, grid-area, layouts bidimensionnels, responsive grids avancés"
icon: lucide/book-open-check
tags: ["CSS", "GRID", "LAYOUT", "RESPONSIVE", "GRID-TEMPLATE", "GRID-AREA", "2D-LAYOUT"]
---

# XI - Grid CSS

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="8-10 heures">
</div>

## Introduction : Layouts Bidimensionnels

!!! quote "Analogie pédagogique"
    _Imaginez un **tableau Excel** ou une **grille de mots croisés**. Chaque case a une position précise définie par **ligne ET colonne**. **CSS Grid**, c'est exactement ça : un système de layout **bidimensionnel** (2D) où vous définissez des lignes ET colonnes, puis placez les éléments dans les cases. **Avant Grid** (pré-2017), créer une galerie photos 3×3 nécessitait des calculs complexes avec float ou Flexbox imbriqués. **Avec Grid**, vous dites : "3 colonnes de 300px, 3 lignes de 200px", et le navigateur crée automatiquement une grille 3×3 parfaite. **Grid vs Flexbox** : Flexbox = **unidimensionnel** (une ligne OU une colonne à la fois), Grid = **bidimensionnel** (lignes ET colonnes simultanément). Flexbox excellent pour navigation, cards en ligne, composants simples. Grid parfait pour layouts complets de page, galeries photos, dashboards complexes, magazines. Grid offre un **contrôle pixel-perfect** : "Cet élément occupe colonnes 2 à 4 et lignes 1 à 3". Vous pouvez même nommer les zones : "header", "sidebar", "content", "footer" et placer les éléments avec `grid-area: header`. Ce module vous transforme en architecte Grid : vous créerez des layouts professionnels impossibles avant Grid._

**CSS Grid (Grid Layout)** = Système de layout bidimensionnel pour créer des grilles complexes.

**Pourquoi CSS Grid est RÉVOLUTIONNAIRE ?**

✅ **Bidimensionnel** : Lignes ET colonnes simultanément  
✅ **Placement précis** : Contrôle exact position items  
✅ **Layouts complexes** : Grilles imbriquées, zones nommées  
✅ **Responsive puissant** : auto-fit, auto-fill, minmax()  
✅ **Moins de markup** : Pas besoin div wrapper partout  
✅ **Ordre indépendant** : HTML ≠ ordre visuel  

**Grid vs Flexbox :**

| Critère | Flexbox | CSS Grid |
|---------|---------|----------|
| Dimensions | 1D (ligne OU colonne) | 2D (lignes ET colonnes) |
| Usage | Navigation, cards ligne | Layouts page, galeries |
| Contrôle | Distribution espace | Placement précis |
| Complexité | Simple | Avancé |
| Quand utiliser | Composants simples | Layouts complexes |

**Exemple comparaison :**

```css
/* FLEXBOX : Navigation (1D horizontal) */
nav {
    display: flex;
    gap: 20px;
}

/* GRID : Galerie photos (2D) */
.gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 200px);
    gap: 20px;
}
/* 3 colonnes × 3 lignes = grille 3×3 automatique */
```

**Ce module couvre TOUT CSS Grid du débutant à l'expert.**

---

## 1. Concepts Fondamentaux

### 1.1 Grid Container vs Grid Items

```html
<!-- Structure Grid -->
<div class="grid-container">     <!-- ← Grid Container -->
    <div class="grid-item">1</div>  <!-- ← Grid Item -->
    <div class="grid-item">2</div>  <!-- ← Grid Item -->
    <div class="grid-item">3</div>  <!-- ← Grid Item -->
    <div class="grid-item">4</div>  <!-- ← Grid Item -->
</div>
```

```css
/* Activation Grid */
.grid-container {
    display: grid;  /* ← Active Grid sur container */
}

/* Les enfants DIRECTS deviennent automatiquement grid items */
/* Petits-enfants ne sont PAS grid items */

/* Exemple */
.grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;  /* 3 colonnes égales */
}

/* HTML :
<div class="grid-container">
    <div>Item 1</div>              ← Grid item ✅
    <div>Item 2</div>              ← Grid item ✅
    <div>
        Item 3                     ← Grid item ✅
        <div>Nested</div>          ← PAS grid item ❌ (petit-enfant)
    </div>
</div>
*/
```

**Propriétés Grid : 2 catégories**

| Container (parent) | Items (enfants) |
|--------------------|-----------------|
| `display: grid` | `grid-column` |
| `grid-template-columns` | `grid-row` |
| `grid-template-rows` | `grid-area` |
| `grid-template-areas` | `justify-self` |
| `gap` / `column-gap` / `row-gap` | `align-self` |
| `justify-items` | `place-self` |
| `align-items` | |
| `place-items` | |
| `justify-content` | |
| `align-content` | |
| `place-content` | |
| `grid-auto-columns` | |
| `grid-auto-rows` | |
| `grid-auto-flow` | |

### 1.2 Terminologie Grid

```
Grid Container
┌─────────────────────────────────────────────────────┐
│  Grid Line 1 (column)                               │
│  ↓                                                   │
│  ┌──────────┬──────────┬──────────┐  ← Grid Line 1  │
│  │          │          │          │    (row)        │
│  │  Cell    │  Cell    │  Cell    │                 │
│  │  (1,1)   │  (1,2)   │  (1,3)   │                 │
│  ├──────────┼──────────┼──────────┤  ← Grid Line 2  │
│  │          │          │          │                 │
│  │  Cell    │  Cell    │  Cell    │                 │
│  │  (2,1)   │  (2,2)   │  (2,3)   │                 │
│  └──────────┴──────────┴──────────┘  ← Grid Line 3  │
│  ↑          ↑          ↑          ↑                  │
│  GL1        GL2        GL3        GL4                │
│  (column)                                            │
└─────────────────────────────────────────────────────┘

GL = Grid Line
Cell = Cellule (intersection ligne/colonne)
Track = Piste (rangée ou colonne complète)
Area = Zone (groupe de cellules)
```

**Vocabulaire Grid :**

- **Grid Line** : Lignes qui divisent la grille (horizontales et verticales)
- **Grid Track** : Espace entre 2 lignes (= rangée ou colonne)
- **Grid Cell** : Intersection ligne/colonne (= case)
- **Grid Area** : Rectangle de plusieurs cellules

```css
/* Exemple avec terminologie */
.grid-container {
    display: grid;
    
    /* 3 tracks colonnes (4 grid lines colonnes : 1, 2, 3, 4) */
    grid-template-columns: 100px 200px 100px;
    
    /* 2 tracks lignes (3 grid lines lignes : 1, 2, 3) */
    grid-template-rows: 150px 150px;
    
    gap: 10px;
}

.item-1 {
    /* Occupe de grid line colonne 1 à 3 (2 tracks) */
    grid-column: 1 / 3;
    
    /* Occupe de grid line ligne 1 à 2 (1 track) */
    grid-row: 1 / 2;
    
    /* = Area de 2 colonnes × 1 ligne */
}
```

---

## 2. Propriétés du Grid Container

### 2.1 display: grid

```css
/* Active Grid */
.container {
    display: grid;         /* Block-level grid container */
}

/* Ou inline-grid */
.container-inline {
    display: inline-grid;  /* Inline-level grid container */
}

/* Différence grid vs inline-grid */

/* display: grid */
.grid {
    display: grid;
    /* Container prend 100% largeur (block) */
}

/* display: inline-grid */
.inline-grid {
    display: inline-grid;
    /* Container prend uniquement largeur contenu (inline) */
}
```

### 2.2 grid-template-columns

```css
/* Définit le nombre et taille des colonnes */

/* Pixels fixes */
.grid {
    display: grid;
    grid-template-columns: 100px 200px 100px;
    /* 3 colonnes : 100px, 200px, 100px */
}

/* Fractions (fr) - Distribue espace disponible */
.grid {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    /* 3 colonnes : 25%, 50%, 25% de l'espace */
}

/* Mix unités */
.grid {
    display: grid;
    grid-template-columns: 200px 1fr 200px;
    /* Colonnes 1 et 3 fixes 200px, colonne 2 prend espace restant */
}

/* repeat() - Répétition */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    /* = 1fr 1fr 1fr (3 colonnes égales) */
}

.grid {
    display: grid;
    grid-template-columns: repeat(4, 100px);
    /* = 100px 100px 100px 100px (4 colonnes 100px) */
}

/* repeat() avec pattern */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 100px 200px);
    /* = 100px 200px 100px 200px 100px 200px (6 colonnes alternées) */
}

/* minmax() - Min et Max */
.grid {
    display: grid;
    grid-template-columns: minmax(100px, 300px) 1fr 1fr;
    /* Colonne 1 : min 100px, max 300px */
}

.grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(200px, 1fr));
    /* 3 colonnes : min 200px chacune, se partagent espace */
}

/* auto - Taille du contenu */
.grid {
    display: grid;
    grid-template-columns: auto 1fr auto;
    /* Colonnes 1 et 3 = taille contenu, 2 = espace restant */
}

/* auto-fill - Crée autant de colonnes que possible */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, 200px);
    /* Crée autant de colonnes 200px que container peut contenir */
    /* Container 1000px : 5 colonnes */
    /* Container 500px : 2 colonnes */
}

/* auto-fit - Comme auto-fill mais collapse colonnes vides */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    /* Responsive grid magique : min 200px, étire pour remplir */
}

/* Exemple responsive sans media query */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}
/* Desktop (1200px) : 4 colonnes
   Tablet (800px) : 3 colonnes
   Mobile (400px) : 1 colonne
   → AUTOMATIQUE !
*/
```

### 2.3 grid-template-rows

```css
/* Définit le nombre et taille des lignes */

/* Syntaxe identique à grid-template-columns */

/* Pixels fixes */
.grid {
    display: grid;
    grid-template-rows: 100px 200px 100px;
    /* 3 lignes : 100px, 200px, 100px */
}

/* Fractions */
.grid {
    display: grid;
    grid-template-rows: 1fr 2fr 1fr;
    height: 600px;  /* Hauteur container nécessaire pour fr */
    /* 3 lignes : 150px, 300px, 150px */
}

/* repeat() */
.grid {
    display: grid;
    grid-template-rows: repeat(3, 200px);
    /* 3 lignes de 200px */
}

/* minmax() */
.grid {
    display: grid;
    grid-template-rows: minmax(100px, auto) 1fr;
    /* Ligne 1 : min 100px, grandit selon contenu
       Ligne 2 : espace restant */
}

/* auto - Hauteur du contenu */
.grid {
    display: grid;
    grid-template-rows: auto auto auto;
    /* 3 lignes, hauteur selon contenu */
}

/* Exemple layout page */
.page {
    display: grid;
    grid-template-rows: 80px 1fr 60px;
    min-height: 100vh;
}
/* Header : 80px fixe
   Content : espace restant
   Footer : 60px fixe
*/
```

### 2.4 grid-template-areas

```css
/* Nommer les zones de la grille (très puissant) */

.grid {
    display: grid;
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: 80px 1fr 60px;
    grid-template-areas:
        "header  header  header"
        "sidebar content aside"
        "footer  footer  footer";
}

/* Placer items dans zones nommées */
.header {
    grid-area: header;
}

.sidebar {
    grid-area: sidebar;
}

.content {
    grid-area: content;
}

.aside {
    grid-area: aside;
}

.footer {
    grid-area: footer;
}

/* Résultat :
┌─────────────────────────────────┐
│         header                  │  ← 80px
├──────┬──────────────┬──────────┤
│      │              │          │
│ side │   content    │  aside   │  ← 1fr
│ bar  │              │          │
├──────┴──────────────┴──────────┤
│         footer                  │  ← 60px
└─────────────────────────────────┘
  200px      1fr        200px
*/

/* Point (.) pour cellule vide */
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 100px 100px 100px;
    grid-template-areas:
        "header header header"
        "sidebar content ."
        "footer footer footer";
}
/* Cellule (2,3) vide */

/* Responsive avec areas */
.layout {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-areas:
        "header"
        "content"
        "sidebar"
        "footer";
}

@media (min-width: 768px) {
    .layout {
        grid-template-columns: 200px 1fr;
        grid-template-areas:
            "header  header"
            "sidebar content"
            "footer  footer";
    }
}

@media (min-width: 1024px) {
    .layout {
        grid-template-columns: 200px 1fr 200px;
        grid-template-areas:
            "header header  header"
            "sidebar content aside"
            "footer footer  footer";
    }
}
/* Mobile : colonne unique
   Tablet : sidebar + content
   Desktop : sidebar + content + aside
*/
```

### 2.5 gap (espacement)

```css
/* gap : Espace entre cellules */

/* gap uniforme */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;  /* 20px entre lignes ET colonnes */
}

/* row-gap et column-gap séparés */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    row-gap: 30px;     /* Espace vertical (entre lignes) */
    column-gap: 20px;  /* Espace horizontal (entre colonnes) */
}

/* Raccourci gap (row-gap column-gap) */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px 20px;  /* 30px vertical, 20px horizontal */
}

/* Anciens noms (compatibilité) */
.grid {
    grid-row-gap: 30px;     /* Ancien nom */
    grid-column-gap: 20px;  /* Ancien nom */
    grid-gap: 30px 20px;    /* Ancien nom */
}
/* Préférer gap, row-gap, column-gap (modernes) */

/* gap avec fr */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
/* fr distribue l'espace APRÈS gap
   Container 1000px, gap 20px :
   Espace colonnes : 1000 - 40 (2 gaps) = 960px
   Par colonne : 960 / 3 = 320px
*/
```

### 2.6 Alignement Grid

```css
/* justify-items : Alignement horizontal items DANS cellules */

.grid {
    display: grid;
    grid-template-columns: repeat(3, 200px);
    justify-items: start;    /* Début cellule (défaut : stretch) */
}

.grid {
    justify-items: start;    /* Début */
    justify-items: end;      /* Fin */
    justify-items: center;   /* Centré */
    justify-items: stretch;  /* Étiré (défaut) */
}

/* align-items : Alignement vertical items DANS cellules */

.grid {
    display: grid;
    grid-template-rows: repeat(3, 200px);
    align-items: start;      /* Haut cellule */
}

.grid {
    align-items: start;      /* Haut */
    align-items: end;        /* Bas */
    align-items: center;     /* Centré */
    align-items: stretch;    /* Étiré (défaut) */
}

/* place-items : Raccourci align-items + justify-items */

.grid {
    place-items: center;     /* Centré vertical ET horizontal */
    /* = align-items: center; justify-items: center; */
}

.grid {
    place-items: start end;  /* Haut + Droite */
    /* = align-items: start; justify-items: end; */
}

/* justify-content : Alignement GRILLE dans container (si taille fixe) */

.grid {
    display: grid;
    grid-template-columns: repeat(3, 200px);  /* Grille 600px */
    width: 1000px;           /* Container 1000px */
    justify-content: start;  /* Grille au début (défaut) */
}

.grid {
    justify-content: start;        /* Début */
    justify-content: end;          /* Fin */
    justify-content: center;       /* Centré */
    justify-content: space-between; /* Espace entre colonnes */
    justify-content: space-around;  /* Espace autour colonnes */
    justify-content: space-evenly;  /* Espace égal partout */
}

/* align-content : Alignement GRILLE verticalement */

.grid {
    display: grid;
    grid-template-rows: repeat(3, 100px);  /* Grille 300px */
    height: 600px;           /* Container 600px */
    align-content: start;    /* Grille en haut */
}

.grid {
    align-content: start;        /* Haut */
    align-content: end;          /* Bas */
    align-content: center;       /* Centré */
    align-content: space-between;
    align-content: space-around;
    align-content: space-evenly;
}

/* place-content : Raccourci align-content + justify-content */

.grid {
    place-content: center;   /* Grille centrée vertical ET horizontal */
}

.grid {
    place-content: start end;
    /* = align-content: start; justify-content: end; */
}
```

### 2.7 grid-auto-rows et grid-auto-columns

```css
/* Taille des lignes/colonnes créées automatiquement (implicites) */

/* Sans grid-auto-rows */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 200px;  /* Seulement 1ère ligne définie */
}
/* Items 4, 5, 6 créent ligne 2 automatiquement
   Hauteur ligne 2 = auto (hauteur contenu) */

/* Avec grid-auto-rows */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 200px;
    grid-auto-rows: 150px;  /* Lignes implicites = 150px */
}
/* Ligne 2+ = 150px automatiquement */

/* minmax() pour auto-rows */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-auto-rows: minmax(100px, auto);
    /* Lignes implicites : min 100px, grandit selon contenu */
}

/* grid-auto-columns (rare, sauf grid-auto-flow: column) */
.grid {
    display: grid;
    grid-template-rows: repeat(3, 100px);
    grid-auto-flow: column;      /* Items créent colonnes (pas lignes) */
    grid-auto-columns: 200px;    /* Colonnes implicites = 200px */
}
```

### 2.8 grid-auto-flow

```css
/* Contrôle le placement automatique des items */

/* row (défaut) : Remplit lignes de gauche à droite */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-auto-flow: row;  /* Défaut */
}
/* Items 1, 2, 3 → ligne 1
   Items 4, 5, 6 → ligne 2
*/

/* column : Remplit colonnes de haut en bas */
.grid {
    display: grid;
    grid-template-rows: repeat(3, 100px);
    grid-auto-flow: column;
}
/* Items 1, 2, 3 → colonne 1
   Items 4, 5, 6 → colonne 2
*/

/* dense : Remplit trous (items peuvent passer avant d'autres) */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-auto-flow: row dense;
}
/* Si item occupe 2 colonnes et laisse trou,
   item suivant remplit le trou même s'il passe avant visuellement
*/

/* Exemple dense */
.grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-flow: dense;
}

.item-large {
    grid-column: span 2;  /* Occupe 2 colonnes */
}

/* Sans dense :
   [1][2 large ][  ]
   [3][4][5][6]

   Avec dense :
   [1][2 large ][3]
   [4][5][6][7]
   
   Item 3 remplit le trou
*/
```

---

## 3. Propriétés des Grid Items

### 3.1 grid-column

```css
/* Position item sur colonnes (grid lines) */

/* Syntaxe longue */
.item {
    grid-column-start: 1;
    grid-column-end: 3;
    /* Commence colonne line 1, finit line 3 (occupe 2 colonnes) */
}

/* Syntaxe courte (recommandée) */
.item {
    grid-column: 1 / 3;
    /* start / end */
}

/* span - Nombre de colonnes à occuper */
.item {
    grid-column: 1 / span 2;
    /* Démarre ligne 1, occupe 2 colonnes (finit ligne 3) */
}

.item {
    grid-column: span 2;
    /* Occupe 2 colonnes (position auto) */
}

/* Lignes négatives (depuis la fin) */
.item {
    grid-column: 1 / -1;
    /* Ligne 1 à dernière ligne (toute la largeur) */
}

.item {
    grid-column: 2 / -2;
    /* Ligne 2 à avant-dernière ligne */
}

/* Exemples pratiques */

/* Item occupe colonnes 1-2 */
.item-1 {
    grid-column: 1 / 3;
}

/* Item occupe colonnes 2-4 */
.item-2 {
    grid-column: 2 / 5;
}

/* Item occupe toutes les colonnes */
.full-width {
    grid-column: 1 / -1;
}

/* Item occupe 3 colonnes (position auto) */
.wide {
    grid-column: span 3;
}
```

### 3.2 grid-row

```css
/* Position item sur lignes (syntaxe identique à grid-column) */

/* Syntaxe longue */
.item {
    grid-row-start: 1;
    grid-row-end: 3;
}

/* Syntaxe courte */
.item {
    grid-row: 1 / 3;
    /* Lignes 1 à 3 (occupe 2 lignes) */
}

/* span */
.item {
    grid-row: span 2;
    /* Occupe 2 lignes */
}

/* Lignes négatives */
.item {
    grid-row: 1 / -1;
    /* Toute la hauteur */
}

/* Placement précis colonnes ET lignes */
.item {
    grid-column: 2 / 4;  /* Colonnes 2-4 */
    grid-row: 1 / 3;     /* Lignes 1-3 */
    /* Rectangle précis dans grille */
}

/* Exemple galerie avec featured image */
.gallery {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 200px);
    gap: 10px;
}

.featured {
    grid-column: 1 / 3;  /* 2 colonnes */
    grid-row: 1 / 3;     /* 2 lignes */
    /* Image 2× plus grande */
}
```

### 3.3 grid-area

```css
/* 3 usages différents de grid-area */

/* Usage 1 : Raccourci grid-row + grid-column */
.item {
    grid-area: 1 / 2 / 3 / 4;
    /* row-start / column-start / row-end / column-end */
    /* = grid-row: 1 / 3; grid-column: 2 / 4; */
}

/* Usage 2 : Nom de zone (avec grid-template-areas) */
.header {
    grid-area: header;  /* Référence zone nommée "header" */
}

/* Usage 3 : Nom custom pour réutilisation */
.item {
    grid-area: myitem;
}

.container {
    grid-template-areas:
        "myitem myitem sidebar"
        "content content sidebar";
}

/* Exemple layout complet */
.layout {
    display: grid;
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: 80px 1fr 60px;
    grid-template-areas:
        "header  header  header"
        "sidebar content aside"
        "footer  footer  footer";
    min-height: 100vh;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.aside   { grid-area: aside; }
.footer  { grid-area: footer; }
```

### 3.4 Alignement Individuel

```css
/* justify-self : Alignement horizontal item DANS sa cellule */

.item {
    justify-self: start;    /* Début cellule */
    justify-self: end;      /* Fin cellule */
    justify-self: center;   /* Centré cellule */
    justify-self: stretch;  /* Étiré (défaut) */
}

/* align-self : Alignement vertical item DANS sa cellule */

.item {
    align-self: start;      /* Haut cellule */
    align-self: end;        /* Bas cellule */
    align-self: center;     /* Centré cellule */
    align-self: stretch;    /* Étiré (défaut) */
}

/* place-self : Raccourci align-self + justify-self */

.item {
    place-self: center;     /* Centré vertical ET horizontal */
    /* = align-self: center; justify-self: center; */
}

.item {
    place-self: start end;
    /* = align-self: start; justify-self: end; */
}

/* Override alignement global */
.grid {
    display: grid;
    align-items: start;      /* Tous items en haut */
}

.item-special {
    align-self: center;      /* Cet item centré */
}
```

---

## 4. Techniques Avancées Grid

### 4.1 Grille Responsive Automatique

```css
/* Grille qui s'adapte SANS media queries */

/* Technique 1 : auto-fit + minmax */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

/* Comportement :
   1600px : 6 colonnes (6 × 250 = 1500)
   1200px : 4 colonnes
   800px  : 3 colonnes
   600px  : 2 colonnes
   400px  : 1 colonne
   → AUTOMATIQUE selon largeur container
*/

/* Technique 2 : auto-fill (garde colonnes vides) */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

/* auto-fit vs auto-fill :
   
   auto-fit : 3 items dans container 1200px
   [Item1][Item2][Item3]           ← Items s'étirent
   
   auto-fill : 3 items dans container 1200px
   [Item1][Item2][Item3][vide]     ← Colonnes vides gardées
*/

/* Recommandation : Utiliser auto-fit généralement */

/* Technique 3 : minmax avec clamp() */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(clamp(200px, 30vw, 400px), 1fr));
    gap: 20px;
}
/* Taille colonnes : min 200px, idéal 30vw, max 400px */
```

### 4.2 Grilles Imbriquées

```css
/* Grid dans Grid (subgrid serait idéal mais support limité) */

/* Container principal */
.main-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

/* Item qui contient une grille */
.card {
    display: grid;
    grid-template-rows: auto 1fr auto;
    gap: 15px;
}

/* HTML :
<div class="main-grid">
    <div class="card">          ← Grid item + Grid container
        <header>Header</header>
        <div>Content</div>
        <footer>Footer</footer>
    </div>
</div>
*/

/* Exemple galerie avec cards complexes */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.product-card {
    display: grid;
    grid-template-rows: 250px auto auto 1fr auto;
    gap: 15px;
    background: white;
    padding: 20px;
    border-radius: 10px;
}

/* HTML :
<div class="gallery">
    <div class="product-card">
        <img class="product-image">
        <h3 class="product-title">
        <p class="product-price">
        <p class="product-description">
        <button class="product-cta">
    </div>
</div>
*/
```

### 4.3 Overlapping Items (Superposition)

```css
/* Grid permet superposition items facilement */

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 200px);
}

.item-1 {
    grid-column: 1 / 3;
    grid-row: 1 / 3;
    background-color: rgba(52, 152, 219, 0.8);
}

.item-2 {
    grid-column: 2 / 4;
    grid-row: 2 / 4;
    background-color: rgba(231, 76, 60, 0.8);
}

/* Items se superposent dans zone 2,2
   z-index contrôle ordre empilement
*/

.item-1 {
    z-index: 1;
}

.item-2 {
    z-index: 2;  /* Au-dessus de item-1 */
}

/* Exemple : Image avec overlay texte */
.hero {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
}

.hero-image {
    grid-column: 1;
    grid-row: 1;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    grid-column: 1;
    grid-row: 1;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1;
}

.hero-content {
    grid-column: 1;
    grid-row: 1;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

/* Résultat : Image + Overlay noir + Texte blanc superposés */
```

### 4.4 Grid avec Named Lines

```css
/* Nommer les grid lines pour référence facile */

.grid {
    display: grid;
    grid-template-columns:
        [sidebar-start] 200px
        [sidebar-end content-start] 1fr
        [content-end aside-start] 200px
        [aside-end];
    grid-template-rows:
        [header-start] 80px
        [header-end main-start] 1fr
        [main-end footer-start] 60px
        [footer-end];
}

/* Utiliser noms au lieu de numéros */
.header {
    grid-column: sidebar-start / aside-end;
    grid-row: header-start / header-end;
}

.sidebar {
    grid-column: sidebar-start / sidebar-end;
    grid-row: main-start / main-end;
}

.content {
    grid-column: content-start / content-end;
    grid-row: main-start / main-end;
}

/* Plus lisible que grid-column: 1 / 4 */

/* Noms multiples pour même ligne */
.grid {
    display: grid;
    grid-template-columns:
        [left-start sidebar-start] 200px
        [sidebar-end main-start content-start] 1fr
        [content-end main-end right-end];
}

.full-width {
    grid-column: left-start / right-end;
}
```

---

## 5. Layouts Courants Grid

### 5.1 Galerie Photos Responsive

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie Grid</title>
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
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .gallery-item {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            aspect-ratio: 1;
        }
        
        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .gallery-item:hover img {
            transform: scale(1.1);
        }
        
        /* Featured items (plus grands) */
        .gallery-item:nth-child(1) {
            grid-column: span 2;
            grid-row: span 2;
        }
        
        .gallery-item:nth-child(5) {
            grid-column: span 2;
        }
    </style>
</head>
<body>
    <div class="gallery">
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/3498db/ffffff?text=1" alt="Photo 1">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/2ecc71/ffffff?text=2" alt="Photo 2">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/e74c3c/ffffff?text=3" alt="Photo 3">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/f39c12/ffffff?text=4" alt="Photo 4">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/9b59b6/ffffff?text=5" alt="Photo 5">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/1abc9c/ffffff?text=6" alt="Photo 6">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/34495e/ffffff?text=7" alt="Photo 7">
        </div>
        <div class="gallery-item">
            <img src="https://via.placeholder.com/400/95a5a6/ffffff?text=8" alt="Photo 8">
        </div>
    </div>
</body>
</html>
```

### 5.2 Dashboard Layout

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Grid</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
        }
        
        .dashboard {
            display: grid;
            grid-template-areas:
                "header header header"
                "sidebar main main"
                "sidebar main main";
            grid-template-columns: 250px 1fr 1fr;
            grid-template-rows: 80px 1fr 1fr;
            min-height: 100vh;
            gap: 0;
        }
        
        .header {
            grid-area: header;
            background-color: #2c3e50;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 30px;
        }
        
        .sidebar {
            grid-area: sidebar;
            background-color: #34495e;
            color: white;
            padding: 30px 0;
        }
        
        .main {
            grid-area: main;
            padding: 30px;
            background-color: #ecf0f1;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            align-content: start;
        }
        
        .card {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .card-large {
            grid-column: span 2;
        }
        
        @media (max-width: 768px) {
            .dashboard {
                grid-template-areas:
                    "header"
                    "main"
                    "sidebar";
                grid-template-columns: 1fr;
                grid-template-rows: 80px 1fr auto;
            }
            
            .main {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>Dashboard</h1>
        </header>
        
        <aside class="sidebar">
            <nav>
                <p style="padding: 15px 30px;">Menu</p>
            </nav>
        </aside>
        
        <main class="main">
            <div class="card">
                <h3>Stats 1</h3>
                <p>Contenu...</p>
            </div>
            <div class="card">
                <h3>Stats 2</h3>
                <p>Contenu...</p>
            </div>
            <div class="card card-large">
                <h3>Graphique</h3>
                <p>Contenu large...</p>
            </div>
            <div class="card">
                <h3>Stats 3</h3>
                <p>Contenu...</p>
            </div>
            <div class="card">
                <h3>Stats 4</h3>
                <p>Contenu...</p>
            </div>
        </main>
    </div>
</body>
</html>
```

### 5.3 Magazine Layout

```css
/* Layout magazine complexe avec Grid */

.magazine {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(4, 250px);
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

/* Article principal (grande image) */
.featured {
    grid-column: 1 / 5;
    grid-row: 1 / 3;
}

/* Articles secondaires */
.secondary-1 {
    grid-column: 5 / 7;
    grid-row: 1 / 2;
}

.secondary-2 {
    grid-column: 5 / 7;
    grid-row: 2 / 3;
}

/* Bande articles */
.tertiary-1 {
    grid-column: 1 / 3;
    grid-row: 3 / 4;
}

.tertiary-2 {
    grid-column: 3 / 5;
    grid-row: 3 / 4;
}

.tertiary-3 {
    grid-column: 5 / 7;
    grid-row: 3 / 4;
}

/* Publicité */
.ad {
    grid-column: 1 / 7;
    grid-row: 4 / 5;
}

/* Responsive */
@media (max-width: 1024px) {
    .magazine {
        grid-template-columns: repeat(4, 1fr);
    }
    
    .featured {
        grid-column: 1 / 5;
    }
    
    .secondary-1,
    .secondary-2 {
        grid-column: span 2;
    }
}

@media (max-width: 768px) {
    .magazine {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
    }
    
    .featured,
    .secondary-1,
    .secondary-2,
    .tertiary-1,
    .tertiary-2,
    .tertiary-3,
    .ad {
        grid-column: 1;
        grid-row: auto;
    }
}
```

---

## 6. Exercices Pratiques

### Exercice 1 : Grille Photos 3×3

**Objectif :** Créer une galerie 3×3 avec image centrale plus grande.

**Consigne :** 
- 9 images totales
- Image centrale (5) occupe 2×2 cases
- Gap 10px

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie 3×3</title>
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
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(4, 200px);
            gap: 10px;
            max-width: 840px;
            margin: 0 auto;
        }
        
        .photo {
            background-color: #3498db;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
            border-radius: 5px;
        }
        
        .photo:nth-child(1) { grid-column: 1; grid-row: 1; }
        .photo:nth-child(2) { grid-column: 2; grid-row: 1; }
        .photo:nth-child(3) { grid-column: 3; grid-row: 1; }
        .photo:nth-child(4) { grid-column: 4; grid-row: 1; }
        
        .photo:nth-child(5) { grid-column: 1; grid-row: 2; }
        
        /* Image centrale 2×2 */
        .photo:nth-child(6) {
            grid-column: 2 / 4;
            grid-row: 2 / 4;
            background-color: #e74c3c;
            font-size: 3rem;
        }
        
        .photo:nth-child(7) { grid-column: 4; grid-row: 2; }
        .photo:nth-child(8) { grid-column: 1; grid-row: 3; }
        .photo:nth-child(9) { grid-column: 4; grid-row: 3; }
        
        .photo:nth-child(10) { grid-column: 1; grid-row: 4; }
        .photo:nth-child(11) { grid-column: 2; grid-row: 4; }
        .photo:nth-child(12) { grid-column: 3; grid-row: 4; }
        .photo:nth-child(13) { grid-column: 4; grid-row: 4; }
    </style>
</head>
<body>
    <div class="gallery">
        <div class="photo">1</div>
        <div class="photo">2</div>
        <div class="photo">3</div>
        <div class="photo">4</div>
        <div class="photo">5</div>
        <div class="photo">6</div>
        <div class="photo">7</div>
        <div class="photo">8</div>
        <div class="photo">9</div>
        <div class="photo">10</div>
        <div class="photo">11</div>
        <div class="photo">12</div>
        <div class="photo">13</div>
    </div>
</body>
</html>
```

</details>

### Exercice 2 : Layout avec Named Areas

**Objectif :** Créer un layout classique avec grid-template-areas.

**Consigne :** Header, Sidebar, Content, Aside, Footer responsive.

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layout Named Areas</title>
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
            display: grid;
            grid-template-areas:
                "header  header  header"
                "sidebar content aside"
                "footer  footer  footer";
            grid-template-columns: 200px 1fr 200px;
            grid-template-rows: 80px 1fr 60px;
            min-height: 100vh;
            gap: 0;
        }
        
        .header {
            grid-area: header;
            background-color: #2c3e50;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .sidebar {
            grid-area: sidebar;
            background-color: #34495e;
            color: white;
            padding: 20px;
        }
        
        .content {
            grid-area: content;
            background-color: white;
            padding: 40px;
        }
        
        .aside {
            grid-area: aside;
            background-color: #ecf0f1;
            padding: 20px;
        }
        
        .footer {
            grid-area: footer;
            background-color: #2c3e50;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        @media (max-width: 1024px) {
            .layout {
                grid-template-areas:
                    "header header"
                    "sidebar content"
                    "footer footer";
                grid-template-columns: 200px 1fr;
                grid-template-rows: 80px 1fr 60px;
            }
            
            .aside {
                display: none;
            }
        }
        
        @media (max-width: 768px) {
            .layout {
                grid-template-areas:
                    "header"
                    "content"
                    "sidebar"
                    "footer";
                grid-template-columns: 1fr;
                grid-template-rows: 80px 1fr auto 60px;
            }
        }
    </style>
</head>
<body>
    <div class="layout">
        <header class="header">
            <h1>Header</h1>
        </header>
        
        <aside class="sidebar">
            <h2>Sidebar</h2>
            <ul>
                <li>Menu 1</li>
                <li>Menu 2</li>
                <li>Menu 3</li>
            </ul>
        </aside>
        
        <main class="content">
            <h2>Contenu Principal</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </main>
        
        <aside class="aside">
            <h2>Aside</h2>
            <p>Contenu secondaire...</p>
        </aside>
        
        <footer class="footer">
            <p>&copy; 2024 Mon Site</p>
        </footer>
    </div>
</body>
</html>
```

</details>

### Exercice 3 : Grille Auto-Responsive

**Objectif :** Grille qui s'adapte automatiquement sans media queries.

**Consigne :** Cards minimum 300px, s'adaptant au nombre par ligne.

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grille Auto-Responsive</title>
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
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .card {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
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
        <h1>Grille Auto-Responsive</h1>
        
        <div class="grid">
            <div class="card">
                <h3>Card 1</h3>
                <p>Cette grille s'adapte automatiquement selon la largeur de l'écran, sans media queries.</p>
            </div>
            
            <div class="card">
                <h3>Card 2</h3>
                <p>Minimum 300px par carte, maximum colonnes possibles.</p>
            </div>
            
            <div class="card">
                <h3>Card 3</h3>
                <p>Les cartes s'étirent pour remplir l'espace disponible.</p>
            </div>
            
            <div class="card">
                <h3>Card 4</h3>
                <p>Redimensionnez la fenêtre pour voir la magie opérer.</p>
            </div>
            
            <div class="card">
                <h3>Card 5</h3>
                <p>Desktop : 4 colonnes, Tablet : 2-3, Mobile : 1.</p>
            </div>
            
            <div class="card">
                <h3>Card 6</h3>
                <p>Tout automatique avec auto-fit + minmax().</p>
            </div>
        </div>
    </div>
</body>
</html>
```

</details>

---

## 7. Projet du Module : Portfolio Grid Avancé

### 7.1 Cahier des Charges

**Créer un portfolio professionnel avec Grid :**

**Spécifications techniques :**
- Header avec navigation
- Hero section full-width
- Section About (2 colonnes : image + texte)
- Portfolio gallery (grid auto-responsive)
- Services (3 colonnes égales)
- Contact (formulaire + info)
- Footer
- Responsive complet (grid-template-areas)
- Code CSS externe validé

### 7.2 Solution Complète

<details>
<summary>Voir la solution complète du projet (partie 1/2)</summary>

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Grid Avancé</title>
    <link rel="stylesheet" href="portfolio-grid.css">
</head>
<body>
    <div class="page-layout">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1 class="logo">Alice Dupont</h1>
                <nav class="nav">
                    <a href="#about">À propos</a>
                    <a href="#portfolio">Portfolio</a>
                    <a href="#services">Services</a>
                    <a href="#contact">Contact</a>
                </nav>
            </div>
        </header>
        
        <!-- Hero -->
        <section class="hero">
            <div class="hero-content">
                <h2>Développeuse Web Frontend</h2>
                <p>Création d'expériences web modernes et performantes</p>
                <a href="#contact" class="cta-button">Me contacter</a>
            </div>
        </section>
        
        <!-- About -->
        <section class="about" id="about">
            <div class="about-container">
                <div class="about-image">
                    <div class="placeholder-image">Photo</div>
                </div>
                <div class="about-text">
                    <h2>À propos</h2>
                    <p>
                        Passionnée par le développement web depuis plus de 5 ans, 
                        je crée des interfaces utilisateur intuitives et performantes.
                    </p>
                    <p>
                        Spécialisée en HTML, CSS, JavaScript et frameworks modernes 
                        (React, Vue.js), je transforme vos idées en réalité digitale.
                    </p>
                    <ul class="skills-list">
                        <li>HTML5 & CSS3</li>
                        <li>JavaScript (ES6+)</li>
                        <li>React & Vue.js</li>
                        <li>Responsive Design</li>
                        <li>Performance Web</li>
                        <li>Accessibilité</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- Portfolio -->
        <section class="portfolio" id="portfolio">
            <h2>Portfolio</h2>
            <div class="portfolio-grid">
                <div class="portfolio-item featured">
                    <div class="portfolio-image">Projet 1</div>
                    <h3>E-commerce Platform</h3>
                    <p>Plateforme e-commerce complète avec React</p>
                </div>
                
                <div class="portfolio-item">
                    <div class="portfolio-image">Projet 2</div>
                    <h3>Dashboard Analytics</h3>
                    <p>Dashboard avec visualisations de données</p>
                </div>
                
                <div class="portfolio-item">
                    <div class="portfolio-image">Projet 3</div>
                    <h3>Blog CMS</h3>
                    <p>Système de gestion de contenu personnalisé</p>
                </div>
                
                <div class="portfolio-item">
                    <div class="portfolio-image">Projet 4</div>
                    <h3>Portfolio Designer</h3>
                    <p>Site portfolio pour designer graphique</p>
                </div>
                
                <div class="portfolio-item">
                    <div class="portfolio-image">Projet 5</div>
                    <h3>App Mobile</h3>
                    <p>Application web progressive (PWA)</p>
                </div>
                
                <div class="portfolio-item">
                    <div class="portfolio-image">Projet 6</div>
                    <h3>Landing Page</h3>
                    <p>Page de destination produit SaaS</p>
                </div>
            </div>
        </section>
        
        <!-- Services -->
        <section class="services" id="services">
            <h2>Services</h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3>Développement Web</h3>
                    <p>
                        Création de sites web et applications modernes avec 
                        les dernières technologies.
                    </p>
                </div>
                
                <div class="service-card">
                    <h3>Design Responsive</h3>
                    <p>
                        Interfaces adaptables à tous les écrans : mobile, 
                        tablette, desktop.
                    </p>
                </div>
                
                <div class="service-card">
                    <h3>Optimisation Performance</h3>
                    <p>
                        Amélioration des performances et du référencement 
                        de vos sites existants.
                    </p>
                </div>
            </div>
        </section>
        
        <!-- Contact -->
        <section class="contact" id="contact">
            <h2>Contact</h2>
            <div class="contact-container">
                <div class="contact-form">
                    <form>
                        <div class="form-group">
                            <label for="name">Nom</label>
                            <input type="text" id="name" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input type="email" id="email" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="message">Message</label>
                            <textarea id="message" rows="5" required></textarea>
                        </div>
                        
                        <button type="submit" class="submit-button">Envoyer</button>
                    </form>
                </div>
                
                <div class="contact-info">
                    <h3>Informations</h3>
                    <p><strong>Email:</strong> alice@example.com</p>
                    <p><strong>Téléphone:</strong> 06 12 34 56 78</p>
                    <p><strong>Localisation:</strong> Paris, France</p>
                    
                    <div class="social-links">
                        <a href="#">LinkedIn</a>
                        <a href="#">GitHub</a>
                        <a href="#">Twitter</a>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="footer">
            <p>&copy; 2024 Alice Dupont. Tous droits réservés.</p>
        </footer>
    </div>
</body>
</html>
```

</details>

<details>
<summary>Voir la solution complète du projet (partie 2/2 - CSS)</summary>

```css
/* portfolio-grid.css */

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

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #2c3e50;
}

/* ========================================
   PAGE LAYOUT (Grid principal)
   ======================================== */

.page-layout {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: auto;
}

/* ========================================
   HEADER
   ======================================== */

.header {
    background-color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 40px;
}

.logo {
    font-size: 1.5rem;
    color: #3498db;
}

.nav {
    display: grid;
    grid-auto-flow: column;
    gap: 30px;
    justify-content: end;
}

.nav a {
    color: #7f8c8d;
    text-decoration: none;
    transition: color 0.3s ease;
}

.nav a:hover {
    color: #3498db;
}

/* ========================================
   HERO
   ======================================== */

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 120px 20px;
    text-align: center;
}

.hero-content h2 {
    font-size: 3rem;
    margin-bottom: 20px;
}

.hero-content p {
    font-size: 1.3rem;
    margin-bottom: 30px;
    opacity: 0.9;
}

.cta-button {
    display: inline-block;
    padding: 15px 40px;
    background-color: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 30px;
    font-weight: bold;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* ========================================
   ABOUT (Grid 2 colonnes)
   ======================================== */

.about {
    padding: 80px 20px;
    background-color: white;
}

.about-container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 400px 1fr;
    gap: 60px;
    align-items: center;
}

.about-image {
    aspect-ratio: 1;
}

.placeholder-image {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #3498db, #2ecc71);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2rem;
}

.about-text h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #2c3e50;
}

.about-text p {
    margin-bottom: 15px;
    color: #555;
}

.skills-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 30px;
    list-style: none;
}

.skills-list li {
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 5px;
    color: #3498db;
}

.skills-list li::before {
    content: "✓ ";
    font-weight: bold;
}

/* ========================================
   PORTFOLIO (Grid auto-responsive)
   ======================================== */

.portfolio {
    padding: 80px 20px;
    background-color: #f8f9fa;
}

.portfolio h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 50px;
    color: #2c3e50;
}

.portfolio-grid {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.portfolio-item {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.portfolio-item:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Featured item (plus grand) */
.portfolio-item.featured {
    grid-column: span 2;
}

.portfolio-image {
    height: 250px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2rem;
}

.portfolio-item h3 {
    padding: 20px 20px 10px;
    color: #2c3e50;
}

.portfolio-item p {
    padding: 0 20px 20px;
    color: #7f8c8d;
}

/* ========================================
   SERVICES (Grid 3 colonnes)
   ======================================== */

.services {
    padding: 80px 20px;
    background-color: white;
}

.services h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 50px;
    color: #2c3e50;
}

.services-grid {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px;
}

.service-card {
    padding: 40px 30px;
    background-color: #f8f9fa;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s ease;
}

.service-card:hover {
    transform: translateY(-5px);
}

.service-card h3 {
    margin-bottom: 15px;
    color: #3498db;
}

.service-card p {
    color: #555;
}

/* ========================================
   CONTACT (Grid 2 colonnes)
   ======================================== */

.contact {
    padding: 80px 20px;
    background-color: #f8f9fa;
}

.contact h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 50px;
    color: #2c3e50;
}

.contact-container {
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
}

.contact-form {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    color: #2c3e50;
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
}

.submit-button {
    width: 100%;
    padding: 15px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.submit-button:hover {
    background-color: #2980b9;
}

.contact-info {
    background-color: white;
    padding: 40px;
    border-radius: 10px;
}

.contact-info h3 {
    margin-bottom: 20px;
    color: #2c3e50;
}

.contact-info p {
    margin-bottom: 10px;
    color: #555;
}

.social-links {
    margin-top: 30px;
    display: grid;
    gap: 10px;
}

.social-links a {
    display: block;
    padding: 10px;
    background-color: #3498db;
    color: white;
    text-align: center;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.social-links a:hover {
    background-color: #2980b9;
}

/* ========================================
   FOOTER
   ======================================== */

.footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 30px 20px;
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 1024px) {
    .about-container {
        grid-template-columns: 300px 1fr;
        gap: 40px;
    }
    
    .portfolio-item.featured {
        grid-column: span 1;
    }
    
    .services-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .header-content {
        grid-template-columns: 1fr;
        text-align: center;
    }
    
    .nav {
        justify-content: center;
    }
    
    .hero-content h2 {
        font-size: 2rem;
    }
    
    .about-container {
        grid-template-columns: 1fr;
    }
    
    .portfolio-grid {
        grid-template-columns: 1fr;
    }
    
    .contact-container {
        grid-template-columns: 1fr;
    }
    
    .skills-list {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .hero-content h2 {
        font-size: 1.8rem;
    }
    
    .nav {
        grid-auto-flow: row;
        gap: 15px;
    }
}
```

</details>

### 7.3 Checklist de Validation

Avant de considérer votre projet terminé, vérifiez :

- [ ] Header sticky avec grid (logo + nav)
- [ ] Hero section full-width
- [ ] About en grid 2 colonnes (image + texte)
- [ ] Skills list en grid 2 colonnes
- [ ] Portfolio grid auto-responsive (auto-fit minmax)
- [ ] Featured item (span 2)
- [ ] Services grid 3 colonnes égales
- [ ] Contact grid 2 colonnes (form + info)
- [ ] Social links en grid column
- [ ] Footer
- [ ] Responsive complet (3 breakpoints)
- [ ] Mobile : grids passent en 1 colonne
- [ ] Code CSS externe validé W3C
- [ ] Scroll smooth

---

## 8. Best Practices CSS Grid

### 8.1 Règles d'Or

```css
/* 1. Grid pour layouts 2D, Flexbox pour 1D */

/* Grid : Galerie, dashboard, page layouts */
.gallery {
    display: grid;
}

/* Flexbox : Navigation, cards en ligne */
.nav {
    display: flex;
}

/* 2. Utiliser auto-fit + minmax pour responsive */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
/* Plus simple que media queries multiples */

/* 3. Nommer les zones pour lisibilité */
.layout {
    grid-template-areas:
        "header header"
        "sidebar content"
        "footer footer";
}
/* Plus clair que grid-column: 1 / 3 */

/* 4. gap au lieu de margin */

/* Ancien */
.item {
    margin: 10px;
}

/* Moderne */
.grid {
    gap: 20px;
}

/* 5. fr pour distribution, pas % */

/* Moins flexible */
.grid {
    grid-template-columns: 33.33% 33.33% 33.33%;
}

/* Plus flexible */
.grid {
    grid-template-columns: repeat(3, 1fr);
}

/* 6. minmax() pour contraintes */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
/* Min 200px, max 1fr (flexible) */
```

### 8.2 Pièges à Éviter

```css
/* PIÈGE 1 : Oublier min/max-width avec fr */

/* Problème : colonnes deviennent trop petites */
.grid {
    grid-template-columns: repeat(6, 1fr);
}
/* Mobile : 6 colonnes de 60px = illisible */

/* Solution : minmax */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

/* PIÈGE 2 : Hauteur container pour fr en lignes */

/* Ne fonctionne pas */
.grid {
    grid-template-rows: 1fr 2fr 1fr;
    /* Container sans hauteur définie */
}

/* Solution : définir hauteur */
.grid {
    grid-template-rows: 1fr 2fr 1fr;
    min-height: 100vh;
}

/* PIÈGE 3 : auto-fill vs auto-fit confusion */

/* auto-fill : garde colonnes vides */
.grid {
    grid-template-columns: repeat(auto-fill, 200px);
}

/* auto-fit : collapse colonnes vides */
.grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
/* Généralement auto-fit préféré */

/* PIÈGE 4 : Overlapping non intentionnel */

/* Items peuvent se superposer si placement manuel */
.item-1 {
    grid-column: 1 / 3;
    grid-row: 1 / 2;
}

.item-2 {
    grid-column: 2 / 4;  /* Superpose avec item-1 */
    grid-row: 1 / 2;
}
/* Intentionnel ou bug ? Toujours vérifier */

/* PIÈGE 5 : grid-template-areas mal formatées */

/* Erreur : pas même nombre colonnes */
.grid {
    grid-template-areas:
        "header header"
        "sidebar content aside";  /* 3 colonnes vs 2 */
}
/* Invalide, ne fonctionne pas */

/* Correct : cohérence */
.grid {
    grid-template-columns: 200px 1fr 200px;
    grid-template-areas:
        "header header header"
        "sidebar content aside";
}
```

### 8.3 Performance

```css
/* Grid est performant par défaut */
/* Navigateurs modernes optimisent bien Grid */

/* Éviter grilles trop complexes */
/* Préférer niveaux raisonnables */

/* OK : Grid simple */
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Éviter : Grid dans grid dans grid dans grid */
/* Trop de niveaux = complexité */

/* Animations : transform préféré */
.item {
    transition: transform 0.3s ease;
}

.item:hover {
    transform: scale(1.05);  /* GPU accelerated */
}

/* Éviter animer grid-template */
.grid {
    /* N'animez PAS grid-template-columns/rows */
    /* Recalcule layout complet */
}
```

---

## 9. Checkpoint de Progression

### À la fin de ce Module 11, vous maîtrisez :

**Concepts Grid :**

- [x] Container vs Items
- [x] Grid lines, tracks, cells, areas
- [x] Terminologie complète

**Propriétés Container :**

- [x] grid-template-columns/rows
- [x] grid-template-areas
- [x] gap (row-gap, column-gap)
- [x] Alignement (justify-items, align-items, place-items)
- [x] Alignement contenu (justify-content, align-content, place-content)
- [x] grid-auto-rows/columns
- [x] grid-auto-flow

**Propriétés Items :**

- [x] grid-column/row
- [x] grid-area (3 usages)
- [x] Alignement individuel (justify-self, align-self, place-self)

**Techniques avancées :**

- [x] auto-fit + minmax (responsive magique)
- [x] Named lines
- [x] Grilles imbriquées
- [x] Overlapping items

**Layouts courants :**

- [x] Galerie photos responsive
- [x] Dashboard layout
- [x] Magazine layout
- [x] Portfolio complet

**Best practices :**

- [x] Règles d'or
- [x] Pièges à éviter
- [x] Performance

### Félicitations

**Vous avez terminé les 11 modules de formation HTML+CSS !**

**Modules complétés :**

- ✅ Module 1-6 : HTML complet
- ✅ Module 7 : Introduction CSS
- ✅ Module 8 : Sélecteurs CSS
- ✅ Module 9 : Box Model
- ✅ Module 10 : Flexbox
- ✅ Module 11 : CSS Grid

**Vous maîtrisez maintenant :**

- Structure HTML sémantique professionnelle
- Tous les sélecteurs CSS
- Box Model pixel-perfect
- Layouts Flexbox modernes
- Layouts Grid bidimensionnels
- Responsive design complet

**Prochaines étapes recommandées :**

- Module 12 : Responsive Design (media queries, mobile-first)
- Module 13 : Animations & Transitions CSS
- Module 14 : CSS Avancé (variables, transforms, filters)
- Module 15 : Projet Final (site complet professionnel)

---

**Module 11 Terminé - Bravo ! 🎉**

**Statistiques Module 11 :**

- 1 projet complet (Portfolio Grid avancé)
- 3 exercices progressifs avec solutions
- 15+ propriétés container maîtrisées
- 8+ propriétés items maîtrisées
- Layouts Grid professionnels créés
- Responsive sans media queries maîtrisé

**Félicitations pour cette maîtrise complète de CSS Grid ! 🚀**
