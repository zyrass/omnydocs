---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 5

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `$el`, `$root`, `$data` : comprendre ce que tu manipules vraiment

### Objectif de la leçon

À la fin, tu sauras :

* ce que représente `$el` (l’élément actuel)
* ce que représente `$root` (la racine du composant)
* ce que contient `$data` (les données du composant)
* comment ces outils t’aident à :

  * debugger proprement
  * éviter le “querySelector sauvage”
  * manipuler le DOM sans casser la structure
* les pièges : abus, couplage fort, logique trop magique

Cette leçon, c’est du “mental model”.
Quand tu comprends ça, Alpine devient simple et prévisible.

---

## 1) `$el` : l’élément sur lequel tu es en train de travailler

### Définition simple

`$el` représente **l’élément DOM actuel**, celui sur lequel l’expression Alpine est exécutée.

Si tu écris :

```html
<button @click="console.log($el)">Clique</button>
```

Alors `$el` = ce bouton.

### Exemple concret

```html
<div x-data="{ count: 0 }">
  <button
    @click="
      count++;
      console.log('Je suis :', $el);
    "
  >
    +1
  </button>
</div>
```

Tu verras dans la console :

* l’élément `<button>...</button>`

---

## 2) `$root` : la racine du composant Alpine

### Définition simple

`$root` = l’élément qui porte `x-data`.

C’est **le conteneur principal** du composant.

Exemple :

```html
<div x-data="{ name: 'Alain' }">
  <button @click="console.log($root)">Log root</button>
</div>
```

Ici :

* `$root` = le `<div x-data="...">`

### Pourquoi c’est utile ?

Parce que dans une UI complexe, tu peux être dans un bouton à l’intérieur, mais tu veux accéder à la racine du composant.

---

## 3) `$data` : l’objet de données Alpine (ton state)

### Définition simple

`$data` = l’objet qui contient toutes les variables et fonctions définies dans `x-data`.

Exemple :

```html
<div x-data="{ count: 0, inc() { this.count++ } }">
  <button @click="console.log($data)">Voir data</button>
</div>
```

Dans la console, tu verras un objet avec :

* `count`
* `inc()`

### Très important

`$data` n’est pas le DOM.
C’est ton “cerveau” (state + actions).

---

# 4) Exemple complet : comprendre les 3 en une seule fois

```html
<div x-data="{
  title: 'Blog mock',
  count: 0,
  inc() { this.count++ }
}" style="border:1px solid #ddd; padding:12px; border-radius:12px;">

  <h3 x-text="title"></h3>
  <p>Count: <strong x-text="count"></strong></p>

  <button @click="
    inc();

    console.log('--- DEBUG ---');
    console.log('$el:', $el);
    console.log('$root:', $root);
    console.log('$data:', $data);
  ">
    Debug +1
  </button>
</div>
```

Ce que tu dois observer :

* `$el` = le bouton
* `$root` = le div racine du composant
* `$data` = l’objet `{ title, count, inc }`

---

# 5) Cas d’usage réel : faire du debug sans se perdre

Quand tu as une UI complexe, tu peux faire :

```html
<button @click="console.log($data)">Debug state</button>
```

Ça te permet de vérifier :

* si ta variable change bien
* si ton state est correct
* si une fonction existe vraiment

Ça évite :

* “je crois que ça marche”
* alors que non

---

## 6) Cas d’usage réel : manipuler un élément DOM proche sans querySelector global

### Exemple : ajouter une classe au root

```html
<div x-data="{ active: false }"
     :class="{ 'active': active }"
     style="padding:12px; border:1px solid #ddd; border-radius:12px;">
  <button @click="
    active = !active;
    console.log('root classes:', $root.className);
  ">
    Toggle active
  </button>
</div>
```

Ici tu manipules proprement le composant sans sortir de son scope.

---

# 7) Attention : pièges et abus

## Piège A — trop utiliser `$el` pour faire du “jQuery style”

Exemple mauvais :

```js
$el.parentElement.parentElement.querySelector(...)
```

Tu vas créer :

* du code fragile
* dépendant du HTML exact
* qui casse au moindre refactor

Si tu as besoin de cibler un élément :

* utilise `x-ref`
* ou restructure ton composant

---

## Piège B — `$root` utilisé comme un “global”

`$root` est utile, mais si tu fais tout avec `$root.querySelector(...)` :

* tu recrées les problèmes de `document.querySelector`
* juste à une échelle locale

Règle :

> `$root` est un outil de debug et d’accès ponctuel, pas une architecture.

---

## Piège C — modifier `$data` de manière obscure

Tu peux faire :

```js
$data.count = 999
```

Mais si tu fais ça partout, tu perds la clarté.

Préférer :

* des méthodes : `inc()`, `reset()`
* une logique explicite

---

# 8) Petit bonus : `$data` dans un composant “factory” (pattern pro)

Quand tu fais :

```html
<div x-data="blogMock()"></div>
```

Ton `$data` est le retour de `blogMock()`.

Donc tu peux debug comme ça :

```html
<button @click="console.log($data)">Voir tout le composant</button>
```

C’est très utile pour vérifier :

* `filteredPosts`
* `toggleFavorite`
* `searchQuery`

---

## 9) Résumé clair

| Outil   | Ce que c’est        | Usage principal                   |
| ------- | ------------------- | --------------------------------- |
| `$el`   | élément actuel      | debug, actions locales            |
| `$root` | racine du composant | debug, accès racine               |
| `$data` | state + fonctions   | debug, compréhension du composant |

---

## Mini exercice (obligatoire)

### Exercice A — Debug state

Dans ton Blog mock, ajoute un bouton :

* “Debug state”
* au clic : `console.log($data)`

### Exercice B — Root marker

Ajoute un bouton :

* au clic, ajoute une classe au `$root` (ou log ses classes)

### Exercice C — Element log

Sur un bouton favori :

* log `$el` au clic
* observe que `$el` change selon le bouton cliqué

---

# Conclusion du Chapitre 6

Tu maîtrises maintenant :

* `x-effect` (réactivité automatique)
* `$watch` (observer proprement une variable)
* `x-ref / $refs` (contrôle du DOM)
* `$nextTick` (attendre le rendu)
* `$el / $root / $data` (mental model + debug)

Tu as littéralement les outils pour faire des interfaces propres sans framework lourd.

---

## Étape suivante logique

On attaque **Chapitre 7 — Transitions & UI “pro”**
Leçon 1 : `x-transition` (enter/leave) : rendre une UI agréable sans bricolage.
