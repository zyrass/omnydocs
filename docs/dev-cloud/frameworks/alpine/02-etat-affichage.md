---
description: "Affichage conditionnel et l'itération des données dans le DOM avec Alpine.js."
icon: lucide/book-open-check
tags: ["THEORIE", "ALPINE", "JAVASCRIPT", "DOM"]
---

# État et Affichage

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Alpine 3.x"
  data-time="2 Heures">
</div>

!!! quote "Les Marionnettes de l'HTML"
    Imaginez que le DOM (Document Object Model) de votre page est une scène de théâtre, et vos données Javascript sont le metteur en scène. Si le metteur en scène dit "Affichez ceci !", la pièce apparait. S'il dit "Répétez cette scène trois fois", l'acteur le fait. Alpine utilise des **directives** (qui commencent toutes par un `x-`) pour relier vos données invisibles au texte visuel de vos balises.

<br>

---

## 1. Injecter du Texte HTML : x-text et x-html

La base de tout framework est de pouvoir écrire une variable déclarée dans `x-data` au centre d'une balise HTML propre (h1, p, span...).

```html title="Manipulation de l'innerHTML de façon réactive"
<div x-data="{ user: 'Zensical', warning: '<b>Attention</b>' }">
    <!-- Remplace le contenu textuel interne -->
    <h1 x-text="user"></h1>
    
    <!-- Injection stricte HTML : Dangereux si XSS -->
    <p x-html="warning"></p>
</div>
```

_La propriété `x-text` évacue tous les risques d'injection de script (XSS). À l'inverse, n'utilisez **jamais** `x-html` avec des données fournies par les utilisateurs, au risque de corrompre votre système web._

<br>

---

## 2. Affichage Conditionnel : x-show et x-if

L'une des tâches les plus fréquentes est de masquer/afficher des éléments (menus déroulants, failles de sécurité résolues, modales).

```html title="Les deux façons de conditionner le rendu"
<div x-data="{ isVisible: true, isPremium: false }">
    <button @click="isVisible = !isVisible">Basculer le Rendu</button>
    <button @click="isPremium = true">Activer Premium</button>

    <!-- Cache visuellement (CSS display: none) mais EXISTE toujours dans le code -->
    <div x-show="isVisible">
        Je suis un contenu rapide à basculer !
    </div>

    <!-- N'existe PAS dans le DOM, la balise <template> est obligatoire ! -->
    <template x-if="isPremium">
        <div>
            Contenu secret qui n'es pas télé-chargé par l'analyseur SEO initial tant que c'est faux !
        </div>
    </template>
</div>
```

_Le `x-show` est pensé pour les menus fréquents nécessitant de la fluidité, alors que le `x-if` est structurel et économise l'arbre du navigateur. La directive `x-if` requiert impérativement un `<template>` parent._

<br>

---

## 3. Les Boucles : x-for

Traiter un tableau massif d'informations depuis Laravel ou une API Rest pour construire des li de liste. 

```html title="Itération avec template"
<div x-data="{ fruits: ['Pomme', 'Banane', 'Cerise'] }">
    <ul>
        <template x-for="(fruit, index) in fruits" :key="index">
            <li>
                <span x-text="index + 1"></span>. 
                <strong x-text="fruit"></strong>
            </li>
        </template>
    </ul>
</div>
```

_Tout comme avec le `x-if`, the `x-for` doit absolument être encadré avec un tag `template`. L'attribut `:key` est un élément technique indispensable qui permet à Alpine d'optimiser le repositionnement des éléments sans tout recalculer (le fameux Virtual DOM tracking)._

<br>

---

## Conclusion

!!! quote "Visualisation terminée"
    Avec ces 5 premières directives (`x-data`, `x-text`, `x-html`, `x-show`, `x-if`, `x-for`), vous savez désormais récupérer une structure Javascript en mémoire et la forcer à s'afficher dans tous les espaces que vous lui dictez.

> Une page web n'est pas uniquement un affichage passif. Elle reçoit des clics, des déplacements de souris et les utilisateurs écrivent dans des formulaires. Découvrez ces flux d'entrées dans le [chapitre 3 : Interactions et Événements](./03-interactions-evenements.md) !
