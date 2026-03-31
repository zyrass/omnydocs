---
description: "Le cours exhaustif sur CSS Grid Layout : grille formelle, grid-template-areas, placement absolu, subgrid et auto-fit/minmax."
icon: lucide/book-open-check
tags: ["CSS", "GRID", "LAYOUT", "2D", "SUBGRID", "TEMPLATE-AREAS"]
---

# CSS Grid Layout

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2.1"
  data-time="5-7 heures">
</div>

## Introduction

Jusqu'à l'arrivée de Grid en 2017, la structuration globale d'une page Web (en-tête, sidebar, contenu, pied de page) reposait sur des détournements de `float` ou des imbrications complexes de Flexbox.

**CSS Grid** est le premier système natif de mise en page **bidimensionnel** du web. Il permet de définir simultanément des lignes et des colonnes, créant une grille formelle invisible sur laquelle les éléments se placent avec une précision absolue.

Grid est l'outil du design **macroscopique** — la structure globale de la page. Flexbox excelle dans le design **microscopique** — l'alignement des éléments à l'intérieur de ces zones.

!!! quote "Analogie pédagogique - Le Plan d'Architecte"
    Si Flexbox ressemble à un élastique unidimensionnel où les éléments s'alignent en chaîne, CSS Grid ressemble davantage à un **plan d'architecte**. Vous dessinez virtuellement les pièces de la maison (la grille formelle), puis vous assignez chaque meuble (vos éléments HTML) à une pièce précise. La structure globale prime sur le contenu individuel.

<br>

---

## Flexbox vs Grid : les deux sont complémentaires

Ces deux systèmes ne sont pas en compétition — ils sont conçus pour fonctionner ensemble.

![Concept de base 2D du CSS Grid](../../../../assets/images/dev/layout-modern/css_grid_2d_concept.png)

*Flexbox gère l'alignement sur un seul axe (ligne ou colonne). Grid structure l'espace sur deux axes simultanés (lignes et colonnes croisées).*

!!! tip "La règle d'or de l'intégrateur"
    Utilisez **Grid** sur le conteneur principal pour définir les grandes zones fixes de la page (en-tête, sidebar, contenu, footer). Utilisez **Flexbox** à l'intérieur de ces zones pour fluidifier et aligner les éléments de détail (navigation, icônes, boutons).

<br>

---

## L'anatomie du système Grid

Une grille repose sur un vocabulaire technique précis.

![Anatomie complète des composants CSS Grid](../../../../assets/images/dev/layout-modern/css_grid_anatomy.png)

*Architecture visuelle d'un système Grid : ligne, piste, cellule et zone.*

| Terme | Explication |
| :--- | :--- |
| **Grid Container** | L'élément parent sur lequel s'écrit `display: grid` |
| **Grid Item** | Les enfants **directs** du Grid Container |
| **Grid Line** | Les traits de découpe invisibles. Une grille de 3 colonnes possède 4 lignes verticales |
| **Grid Track** | L'espace entre deux Grid Lines (une colonne ou une rangée) |
| **Grid Cell** | L'intersection d'une colonne et d'une rangée (la plus petite unité) |
| **Grid Area** | Un regroupement rectangulaire de plusieurs cellules adjacentes |

<br>

---

## Déclaration et structure

<br>

### Initialisation

```css title="CSS - Activation du contexte Grid"
.plan-de-travail {
    /* Active le contexte Grid sur ce conteneur */
    display: grid;
}
```

*Sans instructions supplémentaires, Grid empile les enfants dans une colonne unique par défaut.*

<br>

### `grid-template-columns` et `grid-template-rows`

Ces deux propriétés découpent l'espace du conteneur en colonnes et en rangées.

L'unité `fr` (fraction) représente une part de l'espace restant après déduction des tailles fixes.

![Découpage en lignes et colonnes avec fr](../../../../assets/images/dev/layout-modern/css_grid_template_columns_rows.png)

*L'association de pixels fixes (pour les sidebars) et de fractions `fr` (pour le contenu fluide) permet un contrôle architectural absolu.*

```css title="CSS - Découpe des colonnes et rangées"
.architecture-container {
    display: grid;

    /*
        3 colonnes :
        - Colonne 1 : 100px fixes
        - Colonne 2 : 1 fraction du vide restant
        - Colonne 3 : 2 fractions du vide restant (le double de la 2)
    */
    grid-template-columns: 100px 1fr 2fr;

    /*
        3 rangées :
        - Rangée 1 : 80px fixes (en-tête)
        - Rangée 2 : s'adapte à son contenu
        - Rangée 3 : prend l'espace restant
    */
    grid-template-rows: 80px auto 1fr;

    /* Gouttière entre toutes les cellules */
    gap: 16px;
}
```

<br>

### La fonction `repeat()`

```css title="CSS - repeat() pour les grilles régulières"
/* 12 colonnes égales (grille Bootstrap-style) */
.grille-12 {
    grid-template-columns: repeat(12, 1fr);
}

/* Alternance : 100px fixe, 2fr fluide, répétée 3 fois */
.grille-alternee {
    grid-template-columns: repeat(3, 100px 2fr);
    /* Génère : 100px 2fr 100px 2fr 100px 2fr */
}
```

<br>

### `grid-auto-rows` et `grid-auto-columns`

Ces propriétés définissent la taille des rangées ou colonnes créées **implicitement** — celles que Grid génère automatiquement quand les éléments dépassent la grille déclarée.

```css title="CSS - Lignes et colonnes implicites"
.galerie {
    display: grid;
    grid-template-columns: repeat(3, 1fr);

    /*
        Toute rangée créée automatiquement (au-delà des grid-template-rows déclarées)
        aura une hauteur minimale de 200px et s'étendra si le contenu est plus grand.
    */
    grid-auto-rows: minmax(200px, auto);

    gap: 1rem;
}
```

*`grid-auto-rows` est particulièrement utile pour les galeries dynamiques dont le nombre d'éléments n'est pas connu à l'avance.*

<br>

### `grid-auto-flow` — contrôler le remplissage automatique

```css title="CSS - Ordre de placement automatique des éléments"
.layout {
    display: grid;
    grid-template-columns: repeat(3, 1fr);

    /*
        row (défaut) : remplit de gauche à droite, ligne par ligne
        column       : remplit de haut en bas, colonne par colonne
        dense        : algorithme de remplissage compact (comble les trous)
    */
    grid-auto-flow: row dense;
}
```

*`grid-auto-flow: row dense` est utile pour les mosaïques d'éléments de tailles variées — Grid tentera de combler les espaces vides laissés par des éléments plus grands.*

<br>

---

## Le placement absolu : `grid-column` et `grid-row`

Par défaut, Grid place les éléments séquentiellement. Ces propriétés forcent la position d'un enfant en l'ancrant sur des **Grid Lines** numérotées.

```css title="CSS - Placement par numéros de lignes"
.banniere {
    /*
        L'élément démarre à la Grid Line verticale 1
        et s'étend jusqu'à la Grid Line 4 (couvre 3 colonnes)
    */
    grid-column: 1 / 4;

    /* L'élément occupe la première rangée */
    grid-row: 1 / 2;
}

.footer {
    /*
        -1 cible toujours la toute dernière ligne de la grille déclarée
        Utile pour s'étirer jusqu'au bord sans connaître le nombre exact de colonnes
    */
    grid-column: 1 / -1;
}

.element-large {
    /* span : s'étale sur 2 colonnes à partir de sa position courante */
    grid-column: span 2;
    grid-row: span 3;
}
```

<br>

---

## Les zones nommées : `grid-template-areas`

S'appuyer sur des numéros de lignes invisibles devient difficile à maintenir sur des mises en page complexes. `grid-template-areas` permet de dessiner une représentation visuelle de l'architecture.

![Explication visuelle de grid-template-areas](../../../../assets/images/dev/layout-modern/css_grid_template_areas.png)

*La définition par mots-clés permet aux enfants de s'encastrer automatiquement sur leurs zones désignées.*

```css title="CSS - Architecture complète avec grid-template-areas"
/* LE CONTENEUR PARENT */
.layout-page {
    display: grid;
    grid-template-columns: 240px 1fr 180px;
    grid-template-rows: 64px 1fr 56px;
    min-height: 100dvh;
    gap: 0;

    /*
        Chaque chaîne de caractères représente une rangée.
        Chaque mot représente une zone nommée.
        Un point "." représente une cellule vide.
    */
    grid-template-areas:
        "en-tete    en-tete     en-tete"
        "navigation zone-centre pub-droite"
        "pied-page  pied-page   pied-page";
}

/* LES ENFANTS : s'assignent à leur zone par nom */
.header        { grid-area: en-tete; }
.sidebar-nav   { grid-area: navigation; }
.contenu       { grid-area: zone-centre; }
.sidebar-pub   { grid-area: pub-droite; }
.footer        { grid-area: pied-page; }
```

*Les enfants peuvent être déclarés dans n'importe quel ordre dans le HTML — Grid les place selon les zones, indépendamment de l'ordre source.*

**Responsive avec `grid-template-areas` :**

```css title="CSS - Réorganisation du layout sur mobile"
/*
    Sur mobile, on redessine simplement l'ASCII art.
    Aucune modification du HTML nécessaire.
*/
@media (max-width: 768px) {
    .layout-page {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas:
            "en-tete"
            "zone-centre"
            "navigation"
            "pub-droite"
            "pied-page";
    }
}
```

*C'est l'avantage majeur de `grid-template-areas` : réorganiser complètement une mise en page complexe en quelques lignes, sans toucher au HTML.*

<br>

---

## L'élasticité intelligente : `minmax()`, `auto-fit`, `auto-fill`

<br>

### `minmax()` — sécuriser les dimensions

```css title="CSS - Colonnes avec plancher et plafond"
.galerie {
    display: grid;
    /*
        Chaque colonne a un minimum de 250px et peut s'étirer sur l'espace restant.
        Si la fenêtre est trop étroite pour 3 colonnes de 250px, Grid passe à 2, puis 1.
    */
    grid-template-columns: repeat(3, minmax(250px, 1fr));
    gap: 1rem;
}
```

<br>

### `auto-fit` — grille responsive sans media query

```css title="CSS - Grille fluide algorithmique avec auto-fit"
.catalogue {
    display: grid;
    gap: 1.5rem;

    /*
        auto-fit crée autant de colonnes élastiques (1fr, minimum 300px)
        qu'il est physiquement possible d'en faire tenir dans le conteneur.
        Si l'écran rétrécit, les colonnes passent à 2, puis à 1 automatiquement.
        Aucune media query n'est nécessaire.
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}
```

**Différence entre `auto-fit` et `auto-fill` :**

```css title="CSS - auto-fit vs auto-fill"
/*
    auto-fill : crée autant de pistes que possible, même vides.
    Sur un écran de 900px avec minmax(300px, 1fr) :
    → crée 3 colonnes (300px chacune), même si seulement 1 élément existe.
    → les colonnes vides sont visibles comme de l'espace blanc.
*/
.avec-auto-fill {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

/*
    auto-fit : crée les pistes, puis réduit les vides à zéro.
    Sur le même écran avec 1 seul élément :
    → l'élément s'étire pour remplir les 900px.
    → pas de colonnes vides visibles.
*/
.avec-auto-fit {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}
```

*`auto-fit` est généralement préféré pour les galeries d'articles. `auto-fill` est utile quand on veut réserver visuellement des emplacements pour de futurs éléments.*

<br>

---

## Subgrid — hériter de la grille parente

`subgrid` est l'une des fonctionnalités CSS les plus attendues depuis des années. Disponible nativement depuis 2023.

Le problème qu'il résout : dans une grille de cards, les éléments internes (titre, contenu, bouton) ne s'alignent pas entre les cards si elles ont des hauteurs de contenu différentes.

```css title="CSS - Subgrid pour l'alignement interne des cards"
/* La grille principale : 3 colonnes de cards */
.grille-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: auto;
    gap: 1.5rem;
}

/* Chaque card hérite des rangées de la grille parente */
.card {
    display: grid;
    /*
        subgrid sur grid-row indique que cet enfant utilise
        les rangées de son parent Grid comme référence.
        Les éléments internes de chaque card s'aligneront
        automatiquement avec leurs équivalents dans les autres cards.
    */
    grid-row: span 3;
    grid-template-rows: subgrid;
    gap: 0;
}

/* Les éléments internes s'alignent sur les mêmes lignes dans toutes les cards */
.card-header  { /* Rangée 1 de la grille parente */ }
.card-content { /* Rangée 2 de la grille parente */ }
.card-footer  { /* Rangée 3 de la grille parente */ }
```

*Sans `subgrid`, les boutons de chaque card étaient à des hauteurs différentes selon la longueur du texte. Avec `subgrid`, toutes les cards partagent les mêmes lignes de grille — les boutons sont parfaitement alignés horizontalement.*

!!! info "Support navigateurs"
    `subgrid` est disponible dans Chrome 117+, Firefox 71+, Safari 16+, Edge 117+. En 2025, le support dépasse 91% des utilisateurs. C'est la solution définitive au problème classique d'alignement interne des cards.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    CSS Grid est la fondation inébranlable de la macro-architecture front-end moderne. `grid-template-columns` et `grid-template-rows` découpent l'espace avec l'unité `fr`. `grid-template-areas` dessine l'architecture en ASCII lisible et maintenable. `minmax()` avec `auto-fit` crée des grilles responsive sans media query. `grid-auto-rows` gère les rangées implicites. `subgrid` aligne les éléments internes des cards avec précision. Utilisez Grid pour le macro, Flexbox pour le micro.

> Dans le module suivant, nous aborderons le **Responsive Design** — Media Queries, méthode mobile-first et adaptation complète à tous les écrans.

<br>

[^1]: **W3C** (World Wide Web Consortium) : organisme international responsable de la standardisation des technologies web (HTML, CSS, SVG, etc.).