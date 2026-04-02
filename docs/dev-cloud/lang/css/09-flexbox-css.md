---
description: "Le cours exhaustif sur CSS Flexbox : axes croisés, distribution spatiale, élasticité des enfants et cas pratiques."
icon: lucide/book-open-check
tags: ["CSS", "FLEXBOX", "LAYOUT", "RESPONSIVE", "ALIGNEMENT"]
---

# CSS Flexbox

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.1"
  data-time="4-6 heures">
</div>

## Introduction

Pendant les premières années du Web, positionner des blocs nécessitait des propriétés instables (`float`, `inline-block`) et des calculs manuels complexes. En 2015, le W3C[^1] a standardisé **Flexbox** (The Flexible Box Module).

Flexbox est un système **unidimensionnel**[^3] : il traite les éléments sur un seul rail à la fois — soit en ligne, soit en colonne. C'est la fondation du design responsive moderne.

!!! quote "Analogie pédagogique - L'Orchestre d'Élastiques"
    Imaginez un conteneur comme une scène d'orchestre dont le sol serait un élastique géant. Plutôt que de fixer la position rigide de chaque musicien (vos éléments HTML), vous définissez les règles de tension de l'élastique[^2]. Les musiciens s'adaptent alors d'eux-mêmes : ils se serrent si l'espace manque, s'étirent pour combler le vide, ou sautent à la ligne si la scène devient trop étroite.

<br>

---

## Le Concept des Deux Axes

Pour maîtriser Flexbox, il est impératif d'abandonner les notions de "Gauche/Droite" ou "Haut/Bas". La logique repose sur deux vecteurs invisibles pilotés par le parent.

<br>

### L'Axe Principal (Main Axis) et l'Axe Secondaire (Cross Axis)

Lorsque vous activez le contexte Flexbox, un rail traverse votre conteneur : c'est l'**Axe Principal**. Perpendiculairement à celui-ci se trouve l'**Axe Secondaire**.

La puissance de Flexbox réside dans sa capacité à faire pivoter l'Axe Principal à 90 degrés.

- Si l'Axe Principal est **horizontal**, les enfants s'alignent en **ligne** (`row`).
- Si l'Axe Principal est **vertical**, les enfants s'alignent en **colonne** (`column`).

![Concept des Axes Flexbox : Axe Principal et Axe Secondaire](../../../../assets/images/dev/layout-modern/flexbox_axes_concept.png)

*Cette illustration schématise la bascule entre le mode ligne (axe principal horizontal) et le mode colonne (axe principal vertical). L'axe secondaire suit toujours perpendiculairement.*

!!! warning "Le secret de la terminologie Flexbox"
    - `justify-content` gère l'**Axe Principal** — pas "l'horizontal". Si `flex-direction: column`, `justify-content` gère l'espace **vertical**.
    - `align-items` gère l'**Axe Secondaire** — pas "le vertical". Si `flex-direction: column`, `align-items` gère l'espace **horizontal**.

<br>

---

## Cibler la direction : `flex-direction`

Flexbox repose toujours sur la relation **Parent / Enfants directs**. La propriété `display: flex` s'applique **au conteneur**, jamais directement aux enfants.

```html title="HTML - Structure Parent / Enfants Flexbox"
<!-- LE PARENT : reçoit display: flex -->
<nav class="menu-parent">
    <!-- LES ENFANTS DIRECTS : deviennent des flex items -->
    <a href="#" class="lien-nav">Accueil</a>
    <a href="#" class="lien-nav">Produits</a>
    <a href="#" class="lien-nav">Contact</a>
</nav>
```

```css title="CSS - Activation du contexte Flexbox"
.menu-parent {
    /* Active le contexte Flexbox sur ce conteneur */
    display: flex;

    /*
        flex-direction définit le sens de l'Axe Principal.
        row (défaut)     : horizontal, gauche vers droite
        column           : vertical, haut vers bas
        row-reverse      : horizontal, droite vers gauche
        column-reverse   : vertical, bas vers haut
    */
    flex-direction: row;
}
```

!!! note "La valeur `row` est la valeur par défaut"
    Écrire `flex-direction: row` est techniquement redondant. Cependant, pour la lisibilité du code, beaucoup de développeurs préfèrent l'écrire explicitement dans les projets d'équipe.

<br>

---

## Positionnement spatial : `justify-content`

`justify-content` définit la manière dont l'espace vide restant est réparti le long de l'**Axe Principal**.

![Distribution spatiale avec justify-content en mode row](../../../../assets/images/dev/layout-modern/flexbox_justify_content.png)

*Représentation de la distribution mathématique du vide sur l'Axe Principal, en mode `flex-direction: row`.*

```css title="CSS - Répartition de l'espace sur l'axe principal"
.menu {
    display: flex;
    flex-direction: row;
    /*
        flex-start  : éléments collés au début de l'axe
        flex-end    : éléments poussés à la fin
        center      : éléments regroupés au centre
        space-between: premier et dernier aux bords, vide réparti entre les autres
        space-around : espace égal partagé autour de chaque élément
        space-evenly : espace strictement identique entre chaque bord et élément
    */
    justify-content: space-between;
}
```

| Valeur | Description |
| :--- | :--- |
| `flex-start` | Éléments collés au début de l'axe principal |
| `flex-end` | Éléments poussés à la fin de l'axe principal |
| `center` | Éléments regroupés au centre |
| `space-between` | Premier et dernier aux bords, vide réparti entre les autres |
| `space-around` | Espace égal partagé autour de chaque élément |
| `space-evenly` | Espace strictement identique entre chaque bord et élément |

!!! warning "Le piège de `justify-content` en mode colonne"
    Si le conteneur est en `flex-direction: column`, `justify-content` gère l'espace **vertical** — pas horizontal. L'axe principal a pivoté. C'est le point où la majorité des débutants se perdent.

<br>

---

## Alignement transversal : `align-items`

`align-items` gère l'alignement des enfants sur l'**Axe Secondaire** — perpendiculaire à l'axe principal.

En mode `row`, si votre menu fait 120px de hauteur mais que les textes ne font que 20px : où "flottent" vos enfants dans les 100px restants ?

![Alignement sur l'Axe Secondaire avec align-items](../../../../assets/images/dev/layout-modern/flexbox_align_items.png)

*L'alignement transversal permet de centrer ou d'étirer les éléments sur l'épaisseur du conteneur.*

```css title="CSS - Centrage vertical parfait avec align-items"
.header {
    display: flex;
    flex-direction: row;
    height: 120px;

    /* Poussé vers la droite sur l'axe principal (horizontal) */
    justify-content: flex-end;

    /* Centré verticalement sur l'axe secondaire */
    align-items: center;
}
```

*Ce pattern `justify-content` + `align-items` est l'une des combinaisons les plus utilisées en production pour centrer un contenu dans une barre de navigation.*

| Valeur | Description |
| :--- | :--- |
| `stretch` | *(Défaut)* Étire les enfants pour remplir l'axe secondaire |
| `flex-start` | Enfants collés au début de l'axe secondaire |
| `flex-end` | Enfants collés à la fin de l'axe secondaire |
| `center` | Enfants centrés sur l'axe secondaire |
| `baseline` | Aligne sur la ligne de base typographique du texte |

<br>

### Shorthand : `place-items` et `place-content`

Ces deux raccourcis combinent les propriétés d'alignement en une seule déclaration.

```css title="CSS - Shorthands place-items et place-content"
/*
    place-items: align-items justify-items
    Utile pour centrer un élément unique dans son conteneur flex ou grid.
*/
.carte-centree {
    display: flex;
    place-items: center; /* Équivalent à align-items: center + justify-content: center */
}

/*
    place-content: align-content justify-content
    Utile pour les conteneurs multi-lignes (flex-wrap).
*/
.galerie {
    display: flex;
    flex-wrap: wrap;
    place-content: center space-between;
    /* align-content: center + justify-content: space-between */
}
```

<br>

---

## Gérer les lignes multiples : `flex-wrap` et `align-content`

Par défaut, Flexbox tente de faire tenir tous les éléments sur une seule ligne (`nowrap`), quitte à les écraser.

```css title="CSS - Autoriser le retour à la ligne"
.galerie {
    display: flex;
    /* Autorise le passage à la ligne quand les enfants dépassent le conteneur */
    flex-wrap: wrap;
    gap: 1rem;
}
```

![Retour à la ligne avec flex-wrap](../../../../assets/images/dev/layout-modern/flexbox_wrap.png)

*Le passage à la ligne évite l'écrasement des éléments et permet de construire des grilles fluides simples.*

<br>

### Shorthand `flex-flow`

```css title="CSS - Shorthand flex-flow combinant direction et wrap"
.navigation {
    display: flex;
    /* flex-direction: row + flex-wrap: wrap en une seule déclaration */
    flex-flow: row wrap;
}
```

<br>

### `align-content` — espacer les rangées multiples

`align-content` n'a d'effet **que si** `flex-wrap: wrap` est actif et qu'il existe plusieurs lignes. Il répartit l'espace entre les rangées elles-mêmes.

```css title="CSS - Répartition des lignes multiples"
.grille {
    display: flex;
    flex-wrap: wrap;
    height: 500px; /* Une hauteur définie est nécessaire pour voir l'effet */
    align-content: space-around;
}
```

<br>

---

## Gérer l'espacement : `gap`

```css title="CSS - Gap uniforme et indépendant"
.groupe-boutons {
    display: flex;
    /* Espace uniforme de 16px entre tous les enfants */
    gap: 16px;
}

/* Valeurs distinctes : row-gap et column-gap */
.grille-flex {
    display: flex;
    flex-wrap: wrap;
    /* gap: vertical horizontal */
    gap: 24px 16px; /* 24px entre les lignes, 16px entre les colonnes */
}
```

*`gap` injecte un espace uniquement **entre** les enfants, sans affecter les bords extérieurs du conteneur — contrairement aux marges.*

<br>

### L'astuce du "Push" avec `margin: auto`

En Flexbox, une marge réglée sur `auto` absorbe tout l'espace disponible dans sa direction.

```css title="CSS - Pousser un élément à l'opposé"
.navbar {
    display: flex;
    align-items: center;
}

.btn-deconnexion {
    /* Absorbe tout l'espace horizontal disponible à gauche */
    /* Résultat : le bouton se retrouve poussé à l'extrémité droite */
    margin-left: auto;
}
```

<br>

---

## Propriétés des Enfants

<br>

### Élasticité : `flex-grow`, `flex-shrink`, `flex-basis`

Ces trois propriétés s'appliquent aux **enfants**, pas au conteneur.

- `flex-grow` — capacité à grandir pour occuper le vide disponible (défaut : `0`)
- `flex-shrink` — capacité à rétrécir pour éviter le débordement (défaut : `1`)
- `flex-basis` — taille idéale avant redimensionnement (défaut : `auto`)

```css title="CSS - Élasticité avec le shorthand flex"
/*
    Shorthand flex : grow | shrink | basis
    flex: 1         → équivalent à flex: 1 1 0% (grandit, rétrécit, base zéro)
    flex: 0 0 250px → taille fixe à 250px (ne grandit pas, ne rétrécit pas)
    flex: auto      → équivalent à flex: 1 1 auto
*/
.contenu-principal {
    flex: 1; /* Prend tout l'espace disponible */
}

.sidebar {
    flex: 0 0 260px; /* Largeur fixe, ne bouge pas */
}
```

!!! tip "Toujours utiliser le shorthand `flex`"
    La propriété raccourcie `flex` est recommandée par les spécifications W3C. Elle initialise correctement les valeurs par défaut de `flex-grow`, `flex-shrink` et `flex-basis` selon des comportements standard. Déclarer les trois propriétés séparément peut produire des résultats inattendus.

<br>

### `align-self` — alignement individuel

Un enfant peut outrepasser l'ordre général du parent (`align-items`) pour s'aligner seul.

```css title="CSS - Alignement propre à un enfant"
.notification-badge {
    /* S'aligne en haut tandis que les autres enfants sont centrés */
    align-self: flex-start;
}
```

<br>

### `order` — réorganisation visuelle

`order` permet de réorganiser visuellement les éléments sans toucher au HTML d'origine.

```css title="CSS - Réorganisation visuelle avec order"
.logo     { order: 1; }
.nav      { order: 2; }
.btn-cta  { order: 3; }

/* Sur mobile : mettre le CTA en premier */
@media (max-width: 768px) {
    .btn-cta { order: -1; } /* -1 place l'élément avant order: 0 (défaut) */
}
```

!!! danger "Accessibilité et `order`"
    La propriété `order` change l'ordre **visuel** mais pas l'ordre du **DOM**. Un utilisateur naviguant au clavier (touche Tab) suivra toujours l'ordre du code HTML original, créant une confusion majeure. Utilisez `order` avec parcimonie et toujours en testant la navigation clavier.

<br>

---

## Cas Pratique : Le Flex Imbriqué

Dans les projets réels, on utilise souvent un conteneur Flex à l'intérieur d'un autre pour structurer des composants complexes.

```html title="HTML - Barre de navigation avec sous-liste"
<nav class="nav">
    <div class="logo">OmnyDocs</div>
    <ul class="nav-liens">
        <li><a href="#">Cours</a></li>
        <li><a href="#">Lab</a></li>
        <li><a href="#">Contact</a></li>
    </ul>
</nav>
```

```css title="CSS - Flex imbriqué pour une navbar"
/* Niveau 1 : conteneur principal — logo à gauche, liens à droite */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    height: 64px;
}

/* Niveau 2 : les liens s'alignent horizontalement entre eux */
.nav-liens {
    display: flex;
    gap: 2rem;
    list-style: none;
    margin: 0;
    padding: 0;
}
```

*Le parent `.nav` gère la structure macro (logo vs liens), tandis que `.nav-liens` gère l'alignement micro de ses éléments propres.*

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Flexbox est l'outil indispensable pour les interfaces unidimensionnelles. `justify-content` gère l'**Axe Principal**, `align-items` gère l'**Axe Secondaire** — leur direction dépend de `flex-direction`. `gap` remplace les marges pour les espacements internes. `flex: 1` permet à un enfant de prendre tout l'espace disponible. `margin: auto` pousse un élément vers l'opposé. Ne jamais utiliser `order` sans tester la navigation clavier.

> Dans le prochain module, nous aborderons **CSS Grid** — l'outil conçu pour structurer les architectures globales sur deux dimensions simultanées (lignes et colonnes).

<br>

[^1]: **W3C** (World Wide Web Consortium) : organisme international de standardisation du Web.
[^2]: **Règles de tension** : manière dont les éléments se partagent l'espace libre ou se compressent selon les propriétés Flexbox définies.
[^3]: **Unidimensionnel** : système ne traitant qu'une seule direction à la fois — ligne OU colonne, jamais les deux simultanément.