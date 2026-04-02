---
description: "Démystifier les unités de mesures CSS : absolues (px), relatives (rem, em, %), viewport (vw, vh, dvh) et fonctions de comparaison (clamp, min, max)."
icon: lucide/book-open-check
tags: ["CSS", "UNITÉS", "RESPONSIVE", "REM", "VIEWPORT", "CLAMP"]
---

# Les Unités de Mesures

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.1"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Mètre Ruban contre la Loupe Magique"
    Imaginez construire une maison. Vous utilisez un décamètre en laiton : 1 mètre vaudra toujours 1 mètre, que vous regardiez la maison à l'œil nu ou à travers des jumelles. Ce sont les unités **absolues** comme le pixel `px`.

    Imaginez maintenant que vous êtes dans Alice au Pays des Merveilles. Vous possédez une loupe magique de croissance. Si vous l'appliquez sur une chaise, sa taille dépendra désormais de la pièce qui la contient. Si la pièce grandit de 20%, la chaise grossit automatiquement de 20%. Ce sont les unités **relatives** comme `rem` ou `%`.

    En développement web moderne, construire un site uniquement avec des pixels rigides est une faute professionnelle. Votre visiteur consulte votre travail sur un écran de 42 pouces, sur le minuscule écran d'un téléphone, ou sur une montre connectée.

Si vous ne maîtrisez pas la différence entre `px`, `rem`, `em` et `vw` **avant** Flexbox ou Grid, votre design finira toujours par déborder ou se casser sur mobile.

<br>

---

## L'Unité Absolue : `px`

Le pixel est l'unité historique du CSS. Il est statique et ne s'adapte à aucun contexte.

```css title="CSS - Unité absolue px"
.boite-rigide {
    width: 300px;  /* Largeur fixe, identique sur tous les écrans */
    font-size: 16px; /* Taille de texte figée */
}
```

!!! danger "Ne jamais utiliser `px` pour la taille des textes"
    Les utilisateurs malvoyants configurent leur navigateur pour agrandir les textes à 150% ou 200%. Si votre texte est codé en `px`, il reste figé à cette valeur et **ignore les paramètres d'accessibilité** de l'utilisateur. Le score d'accessibilité de votre site tombe à zéro.

    Réservez le pixel exclusivement aux éléments qui ne doivent **jamais** varier : bordures (`border: 1px solid`), ombres (`box-shadow`), marges microscopiques décoratives.

![Concept des unités absolues versus relatives en CSS](../../../../assets/images/dev/css-fondamental/css_units_absolute_relative.png)

*Cette illustration schématise l'opposition entre une unité physique rigide comme le pixel, face aux unités relatives qui gonflent et se rétractent élastiquement selon leur environnement.*

<br>

---

## Les Unités Relatives

<br>

### Le Pourcentage (`%`)

Le pourcentage se base toujours sur la **taille de l'élément parent direct**.

```css title="CSS - Comportement du pourcentage"
.conteneur {
    width: 1000px; /* Le parent fait 1000px */
}

.enfant {
    /* 50% de 1000px = 500px */
    /* Si le parent rétrécit à 400px sur mobile, l'enfant passe automatiquement à 200px */
    width: 50%;
}
```

*Le pourcentage crée une liaison mathématique directe avec le parent. C'est l'unité idéale pour les mises en page fluides où les éléments doivent occuper une fraction de leur conteneur.*

<br>

### Le `rem` — l'unité universelle de l'accessibilité

`rem` signifie **Root EM** — il est relatif à la taille de police de l'élément racine `<html>`.

Par convention, tous les navigateurs fixent `<html>` à **16px** par défaut — sauf si l'utilisateur a modifié ce paramètre dans ses réglages d'accessibilité.

!!! info "La connexion entre `:root` et `rem`"
    Dans le module précédent, vous avez utilisé `:root` pour stocker vos variables CSS. En CSS, `:root` cible précisément l'élément `<html>`. L'unité `rem` s'appuie donc sur la même source. Ce sont deux faces de la même pièce.

```css title="CSS - Calcul avec rem"
h1 {
    /* 2 × 16px (racine par défaut) = 32px pour un œil valide */
    /* Si l'utilisateur a réglé son navigateur à 24px : 2 × 24 = 48px automatiquement */
    font-size: 2rem;
}

p {
    /* 1.125 × 16px = 18px */
    font-size: 1.125rem;
}

.carte {
    /* Le padding s'adapte aussi à la racine */
    padding: 1.5rem;
}
```

*Si un utilisateur malvoyant a configuré son navigateur à 24px, `2rem` donnera 48px sans que vous n'ayez modifié une seule ligne de code. C'est l'accessibilité automatique.*

<br>

### Le `em` — relatif au parent local

`em` est relatif à la taille de police de **l'élément parent direct**, pas de la racine. C'est sa différence fondamentale avec `rem`.

![Concept en arbre généalogique REM vs EM](../../../../assets/images/dev/css-fondamental/css_units_rem_vs_em.png)

*Le `rem` puise directement à la racine `<html>` comme source unique. Le `em` se base sur son parent direct, ce qui peut créer des cascades de multiplication incontrôlables sur des éléments imbriqués.*

```html title="HTML - Conteneurs imbriqués pour la démonstration"
<div class="boite-grand-pere">
    <div class="boite-parent">
        <p class="texte-enfant">Je suis un texte cassé</p>
    </div>
</div>
```

```css title="CSS - L'effet boule de neige du em"
.boite-grand-pere {
    font-size: 20px;
}

.boite-parent {
    /* 2em × 20px (grand-père) = 40px */
    font-size: 2em;
}

.texte-enfant {
    /* 2em × 40px (parent direct) = 80px — le texte explose l'écran */
    font-size: 2em;
}
```

!!! warning "Règle d'or : `rem` pour les textes, `em` pour les composants isolés"
    N'utilisez **jamais** `em` pour les `font-size` dans une hiérarchie d'éléments imbriqués. L'effet multiplicatif est imprévisible. Utilisez `rem` pour toutes les tailles de texte. L'`em` reste utile dans un composant **isolé et autonome** (un bouton, une étiquette) pour que son padding s'adapte proportionnellement à sa propre taille de texte.

**L'unité `ch` — largeur d'un caractère**

```css title="CSS - Unité ch pour la typographie"
/*
    1ch = largeur du caractère "0" dans la police actuelle.
    Idéale pour limiter la largeur des paragraphes à un nombre optimal de caractères
    (65-75ch est la plage de lisibilité recommandée par la typographie).
*/
p {
    max-width: 70ch; /* Le texte ne dépassera jamais 70 caractères de large */
}

/* Utile aussi pour les champs de saisie de codes */
input[type="text"].code-postal {
    width: 5ch; /* Exactement 5 caractères */
}
```

<br>

---

## Le Viewport : s'aligner sur l'écran

Les unités Viewport ne dépendent pas du parent — elles se calent sur **les dimensions physiques de la fenêtre du navigateur**.

- `vw` = 1% de la **largeur** de la fenêtre
- `vh` = 1% de la **hauteur** de la fenêtre

```css title="CSS - Section plein écran avec vw et vh"
.hero-accueil {
    /* Prend exactement 100% de la largeur visible du navigateur */
    width: 100vw;

    /* Prend exactement 100% de la hauteur visible du navigateur */
    height: 100vh;

    /* Centrer le contenu dans ce bloc */
    display: flex;
    align-items: center;
    justify-content: center;
}
```

![Concept des unités viewport vw et vh](../../../../assets/images/dev/css-fondamental/css_units_viewport.png)

*Les unités viewport mesurent directement la fenêtre du navigateur, indépendamment de tout parent. 100vw = largeur complète de la vitre, 100vh = hauteur complète.*

!!! warning "Le piège de `100vh` sur mobile (et son correctif `dvh`)"
    Sur iOS et Android, la barre d'URL du navigateur se superpose au contenu. `100vh` inclut la zone masquée par cette barre, provoquant un débordement visible. Les unités dynamiques corrigent ce comportement.

**Tableau des variantes viewport modernes :**

| Unité | Signification | Usage recommandé |
| --- | --- | --- |
| `vw` / `vh` | Viewport statique | Mise en page desktop |
| `svh` | Small Viewport Height — viewport **avec** les barres UI | Interface mobile avec barres visibles |
| `lvh` | Large Viewport Height — viewport **sans** les barres UI | Interface mobile sans barres |
| `dvh` | Dynamic Viewport Height — s'ajuste dynamiquement | **Standard recommandé en production mobile** |

```css title="CSS - dvh pour les interfaces mobiles"
.page-mobile {
    /* dvh s'ajuste quand la barre d'URL apparaît ou disparaît */
    min-height: 100dvh;
}
```

<br>

---

## Les Fonctions de Comparaison : `min()`, `max()`, `clamp()`

Ces trois fonctions CSS permettent de créer des valeurs **fluides qui s'adaptent automatiquement** entre des bornes définies — sans media queries.

<br>

### `min()` et `max()`

```css title="CSS - Fonctions min et max"
.conteneur {
    /*
        min() retourne la valeur la plus petite.
        Ici : la largeur sera 100% SAUF si 800px est plus petit — alors 800px s'applique.
        Effet : le conteneur ne dépasse jamais 800px mais peut se réduire en dessous.
    */
    width: min(100%, 800px);
}

.texte-adaptatif {
    /*
        max() retourne la valeur la plus grande.
        Ici : la taille est 4vw SAUF si 1rem est plus grand — alors 1rem s'applique.
        Effet : le texte ne descend jamais en dessous de 1rem même sur petit écran.
    */
    font-size: max(1rem, 4vw);
}
```

<br>

### `clamp()` — la typographie fluide

`clamp(minimum, valeur-idéale, maximum)` est la fonction la plus puissante du trio. Elle définit une **valeur qui grandit entre deux bornes** sans jamais dépasser les limites.

```css title="CSS - clamp pour une typographie parfaitement fluide"
h1 {
    /*
        clamp(valeur-min, valeur-fluide, valeur-max)

        - Ne descend jamais sous 1.5rem (24px)
        - Grandit proportionnellement à 5% de la largeur du viewport
        - Ne dépasse jamais 3rem (48px)

        Sur mobile (375px) : 5vw = 18.75px → plancher à 24px
        Sur tablette (768px) : 5vw = 38.4px → 38.4px
        Sur desktop (1440px) : 5vw = 72px → plafonné à 48px
    */
    font-size: clamp(1.5rem, 5vw, 3rem);
}

.texte-corps {
    /* Taille de texte fluide entre 1rem et 1.25rem */
    font-size: clamp(1rem, 2.5vw, 1.25rem);
}

.carte {
    /* Padding qui s'adapte entre 1rem et 2.5rem */
    padding: clamp(1rem, 3vw, 2.5rem);
}
```

*`clamp()` remplace des dizaines de media queries pour la typographie et les espacements fluides. C'est la technique de référence pour un design véritablement adaptatif.*

<br>

---

## Les Container Queries (`cqw`, `cqh`)

Les unités viewport se basent sur la fenêtre du navigateur. Mais dans une architecture par composants, un même composant peut être utilisé dans une colonne étroite ou dans un conteneur large. C'est le problème que les Container Queries résolvent.

```css title="CSS - Container queries pour les composants adaptatifs"
/*
    Étape 1 : Déclarer un contexte de conteneur sur l'élément parent.
    Le navigateur mesurera maintenant ce conteneur comme référence pour ses enfants.
*/
.wrapper-carte {
    container-type: inline-size;
    container-name: carte; /* Optionnel : nommer le conteneur */
}

/*
    Étape 2 : Dans l'enfant, utiliser cqw au lieu de vw.
    1cqw = 1% de la largeur du conteneur déclaré, pas de la fenêtre.
*/
.titre-carte {
    /* Le titre s'adapte à la largeur du conteneur, pas de l'écran */
    font-size: clamp(1rem, 5cqw, 1.75rem);
}
```

!!! note "Container Queries et architecture de composants"
    Les Container Queries sont particulièrement puissantes dans l'écosystème TALL Stack (Livewire, Alpine.js). Un composant Livewire réutilisable dans différentes zones de mise en page s'adapte automatiquement à son contexte. Le support navigateur atteint 93% en 2025 — utilisables en production.

<br>

---

## Tableau récapitulatif des unités

| Unité | Base de référence | Cas d'usage prioritaire |
| --- | --- | --- |
| `px` | Absolue (fixe) | Bordures, ombres, micro-détails décoratifs |
| `%` | Parent direct | Largeurs fluides, mise en page en colonnes |
| `rem` | Racine `<html>` | **Tailles de texte, espacements** — unité principale |
| `em` | Parent direct | Composants isolés autonomes (bouton, badge) |
| `ch` | Largeur du caractère `0` | Largeur de colonnes de texte, champs de saisie |
| `vw` / `vh` | Fenêtre du navigateur | Sections plein écran |
| `dvh` | Fenêtre dynamique | Interfaces mobiles (correctif iOS/Android) |
| `cqw` / `cqh` | Conteneur déclaré | Composants adaptatifs réutilisables |
| `clamp()` | Fonction fluide | Typographie et espacements adaptatifs |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Utilisez `rem` pour toute taille de texte et espacement — c'est l'unité de l'accessibilité. Utilisez `%` et `vw`/`dvh` pour les grandes zones de mise en page. Utilisez `clamp()` pour des tailles fluides entre deux bornes sans media queries. Évitez `px` pour les textes — cela brise les réglages d'accessibilité des utilisateurs. Réservez `em` aux composants isolés et autonomes.

> Maintenant que vous savez dimensionner vos éléments, il est temps de comprendre comment un élément HTML occupe l'espace autour de lui : **le Box Model** — margin, padding, border et la propriété `box-sizing`.

<br>

[^1]: L'**accessibilité web** (a11y) désigne l'ensemble des pratiques visant à rendre les services numériques accessibles à tous, notamment aux personnes handicapées. En France, la conformité au **RGAA** (Référentiel Général d'Amélioration de l'Accessibilité) est obligatoire pour les services publics et fortement recommandée pour le secteur privé.