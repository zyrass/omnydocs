---
description: "Maîtriser le Box Model CSS : margin, padding, border, outline, overflow, box-sizing et les modes d'affichage block/inline."
icon: lucide/book-open-check
tags: ["CSS", "BOX-MODEL", "MARGIN", "PADDING", "BORDER", "OVERFLOW", "DISPLAY"]
---

# Modèle de Boîte

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.1"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Œuvre d'Art au Musée"
    Imaginez une œuvre d'art inestimable accrochée au mur blanc d'un musée parisien. Le Box Model CSS, c'est l'analyse de cet espace vital autour d'elle :

    1. La toile elle-même — c'est le **Contenu** (`width` / `height`).
    2. Le passe-partout blanc entre la toile et le cadre — c'est le **Padding** (espace intérieur).
    3. Le cadre doré qui encadre l'ensemble — c'est la **Border** (bordure).
    4. La distance de sécurité qui éloigne cette œuvre du tableau voisin — c'est la **Margin** (marge extérieure).

    Avant de maîtriser Flexbox ou Grid, vous **devez** comprendre comment une simple balise HTML occupe et envahit l'espace sur votre page. Sinon, vous passerez des heures à ne pas comprendre pourquoi "ça sort de l'écran".

<br>

---

## Les quatre zones du Box Model

Chaque élément HTML est représenté par le navigateur comme une boîte rectangulaire constituée de quatre zones concentriques.

![Le Modèle de Boîte CSS](../../../../assets/images/dev/css-fondamental/css_box_model.png)

*Chaque élément HTML est une boîte avec quatre zones : contenu au centre, entouré du padding, puis de la border, puis de la margin à l'extérieur.*

<br>

### Padding — l'espace intérieur

Le padding est l'espace entre le **contenu** et la **bordure**. Il fait partie de la zone colorée de l'élément : il hérite du `background-color`.

```css title="CSS - Padding intérieur"
.carte {
    background-color: #f0f4f8;

    /*
        padding: valeur-uniforme
        Repousse le contenu de 24px par rapport aux quatre bords de la carte.
        La zone colorée inclut le padding.
    */
    padding: 24px;
}
```

<br>

### Border — la bordure visible

La bordure est la ligne physique qui encadre le padding et le contenu. Elle se définit avec trois valeurs : épaisseur, style, couleur.

```css title="CSS - Border avec les styles disponibles"
.carte {
    /* Epaisseur | Style | Couleur */
    border: 2px solid #2c3e50;

    /* Arrondir les angles */
    border-radius: 8px;
}

/* Styler chaque côté indépendamment */
.separateur {
    border-top: 1px solid #e2e8f0;  /* Seulement le bord supérieur */
    border-bottom: none;             /* Supprimer un bord */
}
```

**Les styles de bordure disponibles :**

| Valeur | Rendu |
| --- | --- |
| `solid` | Ligne pleine continue |
| `dashed` | Tirets |
| `dotted` | Points |
| `double` | Double ligne |
| `none` | Aucune bordure |

<br>

### Margin — la marge extérieure

La marge s'applique **à l'extérieur** de la bordure. Elle repousse les éléments voisins. Contrairement au padding, la margin est **totalement transparente** — elle révèle l'arrière-plan de la page.

```css title="CSS - Margin extérieure"
.carte {
    /*
        La marge repousse les éléments adjacents de 32px dans toutes les directions.
        Cette zone est transparente : pas de background-color.
    */
    margin: 32px;
}
```

<br>

---

## Les valeurs raccourcies (shorthand)

Padding et margin acceptent de 1 à 4 valeurs selon la règle de l'horloge : **Haut, Droite, Bas, Gauche** (sens des aiguilles, en partant de midi).

```css title="CSS - Syntaxes raccourcies padding et margin"
/* 1 valeur : uniforme sur les quatre côtés */
.box { padding: 20px; }
/* → Haut: 20px  Droite: 20px  Bas: 20px  Gauche: 20px */

/* 2 valeurs : vertical | horizontal */
.box { margin: 10px 40px; }
/* → Haut/Bas: 10px  Droite/Gauche: 40px */

/* 3 valeurs : haut | horizontal | bas */
.box { padding: 10px 20px 30px; }
/* → Haut: 10px  Droite/Gauche: 20px  Bas: 30px */

/* 4 valeurs : haut | droite | bas | gauche (sens horaire depuis midi) */
.box { margin: 10px 20px 30px 40px; }
/* → Haut: 10px  Droite: 20px  Bas: 30px  Gauche: 40px */
```

*La même syntaxe s'applique identiquement à `padding` et à `margin`.*

<br>

---

## `box-sizing` : contrôler le calcul de la largeur

C'est le piège le plus fréquent du CSS débutant. Par défaut, `width` ne définit que le **contenu** — padding et border s'ajoutent par-dessus.

```css title="CSS - Le piège de content-box par défaut"
/*
    Par défaut (content-box) :
    width: 300px + padding: 20px (×2) + border: 2px (×2) = 344px réels

    La boîte dépasse sa largeur déclarée de 44px.
    Résultat sur l'écran : débordement.
*/
.boite-cassee {
    width: 300px;
    padding: 20px;
    border: 2px solid black;
    /* Largeur réelle : 344px — pas 300px */
}
```

### La solution : `border-box`

`box-sizing: border-box` force le navigateur à inclure padding et border **dans** la largeur déclarée. Le contenu se compresse au centre, mais la boîte respecte exactement `width`.

```css title="CSS - Reset universel avec border-box"
/*
    À placer en tout début de fichier CSS, avant toute autre règle.
    Cette déclaration sauve des centaines d'heures de débogage.
*/
*,
*::before,
*::after {
    /*
        Toutes les balises + leurs pseudo-éléments before/after
        respecteront la même convention de calcul.
        width: 300px restera visuellement 300px, quels que soient
        le padding et la border ajoutés.
    */
    box-sizing: border-box;
}
```

*Notez l'inclusion de `*::before` et `*::after` — les pseudo-éléments ont leurs propres boîtes et doivent aussi être couverts par le reset.*

<br>

---

## `outline` — la bordure fantôme

`outline` ressemble à `border` mais a un comportement fondamentalement différent : **il ne modifie pas le box model**. Il se dessine **autour** de la boîte sans en modifier les dimensions ni déplacer les éléments voisins.

```css title="CSS - Différence border et outline"
.bouton {
    border: 2px solid #3498db;    /* Fait partie du box model : occupe de l'espace */
    padding: 12px 24px;
}

/*
    :focus-visible cible les éléments focalisés via le clavier (pas la souris).
    C'est la pseudo-classe recommandée pour styliser le focus sans affecter
    les utilisateurs de souris.
*/
.bouton:focus-visible {
    outline: 3px solid #f39c12;   /* NE modifie pas le box model */
    outline-offset: 2px;          /* Espace entre la border et l'outline */
}

/*
    NE PAS supprimer outline sans alternative !
    outline: none sur :focus est une erreur d'accessibilité grave.
    Les utilisateurs naviguant au clavier perdent tout repère visuel.
*/
```

!!! warning "Ne jamais supprimer `outline` sans le remplacer"
    `outline: none` sur `:focus` (ou `:focus-visible`) est une violation d'accessibilité WCAG 2.1 Critère 2.4.7. Les utilisateurs naviguant uniquement au clavier ne peuvent plus voir quel élément est actif. Si le style par défaut ne vous convient pas, remplacez-le par un outline personnalisé — ne le supprimez pas.

<br>

---

## `overflow` — gérer le dépassement de contenu

Quand le contenu d'une boîte dépasse ses dimensions définies, `overflow` contrôle le comportement.

```css title="CSS - Les valeurs d'overflow"
.carte {
    width: 300px;
    height: 200px;

    /*
        overflow: visible (défaut) — le contenu dépasse visuellement la boîte.
        overflow: hidden  — le contenu dépassant est coupé et invisible.
        overflow: scroll  — ajoute une barre de défilement permanente.
        overflow: auto    — ajoute une barre de défilement seulement si nécessaire.
        overflow: clip    — coupe sans créer de contexte de formatage de bloc.
    */
    overflow: hidden;
}

/* Contrôler les axes indépendamment */
.tableau-defilant {
    overflow-x: auto;   /* Défilement horizontal si nécessaire */
    overflow-y: hidden; /* Pas de défilement vertical */
}

/* Cas classique : rogner les images qui débordent */
.avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    overflow: hidden; /* L'image carrée est rognée dans le cercle */
}
```

*`overflow: hidden` est aussi couramment utilisé pour créer un **Block Formatting Context** — un contexte d'isolation qui empêche les marges de fusionner et force un parent à englober ses enfants flottants.*

<br>

---

## Modes d'affichage : `block`, `inline`, `inline-block`

La propriété `display` détermine comment un élément occupe l'espace et interagit avec ses voisins. C'est essentiel pour comprendre pourquoi `margin` et `padding` se comportent différemment selon les éléments.

```css title="CSS - Les trois modes d'affichage fondamentaux"
/*
    display: block
    - Prend toute la largeur disponible (même si le contenu est plus court).
    - Force un retour à la ligne avant et après lui.
    - Accepte width, height, margin et padding sur les quatre côtés.
    - Éléments block natifs : div, p, h1-h6, section, article, ul, li...
*/
.bloc {
    display: block;
    width: 500px;     /* Respecté */
    margin: 20px 0;   /* Respecté sur tous les côtés */
}

/*
    display: inline
    - S'insère dans le flux du texte, comme un mot dans une phrase.
    - Ne force PAS de retour à la ligne.
    - Ignore width et height.
    - margin et padding gauche/droite fonctionnent, mais haut/bas n'affectent PAS
      l'espacement avec les lignes adjacentes (ils débordent visuellement).
    - Éléments inline natifs : span, a, strong, em, code, img...
*/
.inline {
    display: inline;
    width: 500px;     /* Ignoré */
    margin-top: 20px; /* Ignoré — n'affecte pas l'espacement vertical */
}

/*
    display: inline-block
    - S'insère dans le flux du texte comme un inline.
    - Mais accepte width, height, margin et padding sur TOUS les côtés.
    - Utile pour les badges, boutons inline, icônes avec dimensions.
*/
.badge {
    display: inline-block;
    width: 80px;      /* Respecté */
    padding: 4px 8px; /* Respecté sur tous les côtés */
    margin: 0 4px;    /* Respecté sur tous les côtés */
}
```

**Tableau comparatif des modes d'affichage :**

| Propriété | `block` | `inline` | `inline-block` |
| --- | --- | --- | --- |
| Retour à la ligne | Oui | Non | Non |
| `width` / `height` | Respectés | Ignorés | Respectés |
| `margin` vertical | Respecté | Non appliqué | Respecté |
| `padding` vertical | Respecté | Déborde | Respecté |

<br>

---

## La fusion des marges (Margin Collapsing)

C'est le comportement le plus contre-intuitif du Box Model. Deux marges verticales adjacentes ne s'**additionnent pas** — elles **fusionnent** : seule la plus grande s'applique.

```css title="CSS - Fusion des marges verticales"
.titre {
    margin-bottom: 30px;
}

.paragraphe {
    margin-top: 20px;
}

/*
    Distance réelle entre .titre et .paragraphe : 30px (pas 50px).
    La plus grande marge l'emporte. C'est la fusion des marges.

    La fusion se produit :
    - Entre frères et sœurs adjacents (verticalement)
    - Entre un parent et son premier/dernier enfant (si pas de border/padding entre eux)

    La fusion NE se produit PAS :
    - Pour les marges horizontales
    - Sur les éléments flex ou grid
    - Si un overflow autre que visible est défini
*/
```

<br>

## Le centrage horizontal avec `margin: auto`

Avant l'arrivée de Flexbox, la technique canonique pour centrer un bloc dans sa page était de combiner `max-width` avec `margin: auto`.

```css title="CSS - Centrage horizontal classique avec margin auto"
.contenu-principal {
    /*
        max-width limite la largeur maximale.
        Sans cette limite, l'élément s'étirerait à 100% de la page.
    */
    max-width: 900px;

    /*
        margin: 0 auto
        → Marge verticale (haut/bas) : 0
        → Marge horizontale (gauche/droite) : auto

        Le navigateur divise l'espace horizontal restant en deux parts égales,
        suspendant ainsi le bloc exactement au centre.
    */
    margin: 0 auto;

    /* Padding interne pour que le contenu ne touche pas les bords */
    padding: 0 1.5rem;
}
```

*`margin: auto` ne fonctionne que sur les éléments `display: block` avec une `width` ou `max-width` définie. Sans limite de largeur, l'élément occupant déjà 100% de la largeur, il n'y a pas d'espace vide à distribuer.*

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Le Box Model est le battement de cœur de toute intégration Web. Chaque élément est une boîte avec quatre zones : contenu, padding (intérieur coloré), border (contour visible) et margin (espace extérieur transparent). `box-sizing: border-box` dans le reset universel garantit que `width` reste la largeur réelle. `outline` se dessine autour de la boîte sans affecter le layout — ne jamais le supprimer sans alternative accessible. `overflow` contrôle ce qui dépasse. Les éléments `block` respectent toutes les dimensions, les éléments `inline` ignorent `width`/`height` et les marges verticales.

> Dans le module suivant, nous apprendrons à faire bouger nos éléments avec **les Transitions et Animations CSS** — transformer des interfaces statiques en expériences visuelles dynamiques.

<br>