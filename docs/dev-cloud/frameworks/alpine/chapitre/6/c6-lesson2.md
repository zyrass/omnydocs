---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 2

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `$watch` : observer une variable (réagir proprement à un changement)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait `$watch`
* pourquoi `$watch` est parfois meilleur que `x-effect`
* comment observer une variable et déclencher une action proprement
* les cas d’usage réels :

  * recherche
  * filtre
  * persistance (plus tard)
  * logs / debug contrôlé
* éviter les pièges : watchers multiples, actions trop lourdes, comportements inattendus

---

## 1) Définition simple

`$watch` permet d’écouter une variable Alpine.

Quand cette variable change, Alpine exécute une fonction.

### Traduction humaine

“Quand `X` change, fais `Y`.”

---

## 2) Différence avec `x-effect` (très important)

### `x-effect`

* se relance quand **n’importe quelle dépendance utilisée** change
* pratique, mais parfois trop large

### `$watch`

* tu surveilles **explicitement une variable**
* tu déclenches une fonction claire

Règle pro :

> Si tu veux réagir à une seule variable : `$watch` est souvent plus lisible.

---

# 3) Comment utiliser `$watch` ?

Tu l’utilises généralement dans `x-init`.

### Exemple minimal

```html
<div x-data="{ count: 0 }"
     x-init="$watch('count', value => console.log('count:', value))">
  <button @click="count++">+1</button>
  <p x-text="count"></p>
</div>
```

Ici :

* Alpine observe `count`
* à chaque changement, la fonction s’exécute

---

## 4) `$watch` : signature (explication claire)

La fonction watch reçoit souvent :

* la nouvelle valeur (value)
* parfois l’ancienne valeur (selon version / usage)

Mais le plus important : tu as au moins la nouvelle valeur.

Exemple :

```js
$watch('query', (value) => {
  console.log(value);
});
```

---

# 5) Cas réel #1 — appliquer une recherche automatiquement

Tu as :

* un input `search`
* une liste
* tu veux déclencher un “applySearch” quand `search` change

### Exemple

```html
<div x-data="{
  search: '',
  applied: '',
  apply() { this.applied = this.search.trim(); }
}" x-init="$watch('search', () => apply())">

  <input x-model="search" placeholder="Tape..." />
  <p>Recherche appliquée : <strong x-text="applied"></strong></p>
</div>
```

Ce pattern est utile si tu veux :

* une logique centralisée dans `apply()`
* et ne pas mettre `@input` partout

---

## 6) Cas réel #2 — reset automatique quand un filtre change

Tu as :

* `category`
* `searchQuery`

Quand la catégorie change, tu veux reset la recherche.

### Exemple

```html
<div x-data="{
  category: 'all',
  search: ''
}" x-init="
  $watch('category', () => {
    search = '';
  })
">
  <select x-model="category">
    <option value="all">All</option>
    <option value="frontend">Frontend</option>
    <option value="backend">Backend</option>
  </select>

  <input x-model="search" placeholder="Recherche..." />
</div>
```

Ici, `$watch` te permet d’imposer une cohérence UX.

---

# 7) Cas réel #3 — préparer la persistance (teaser Chapitre 10)

Plus tard, tu vas faire :

* watch sur `todos`
* sauvegarde dans localStorage

Concept :

```js
$watch('todos', value => {
  localStorage.setItem('todos', JSON.stringify(value));
})
```

On ne le fait pas encore proprement ici (parce que ça dépend du format et du plugin Persist), mais tu vois l’idée.

---

# 8) Les pièges fréquents avec `$watch`

## Piège A — watchers en cascade

Tu watch `A` et dans le watch tu modifies `B`
Puis tu watch `B` et ça modifie `A`

Tu crées une boucle logique.

Règle :

> Un watcher doit être simple et prévisible.

---

## Piège B — watchers trop lourds

Si tu fais :

* tri lourd
* traitement lourd
* requêtes réseau
  à chaque changement de variable…

Tu vas créer une app lente.

Solution :

* debounce côté input
* ou throttle
* ou limiter le watch

---

## Piège C — multiplier les watchers partout

Si tu as 10 watchers dans un composant, ça devient difficile à maintenir.

Dans ce cas :

* restructure ton state
* regroupe les actions

---

# 9) Pattern pro : watcher + méthode claire

Tu écris :

* une méthode `sync()`
* un watcher qui appelle `sync()`

Exemple :

```html
<div x-data="{
  query: '',
  sync() {
    console.log('sync query:', this.query);
  }
}" x-init="
  $watch('query', () => sync())
">
  <input x-model="query" placeholder="Tape..." />
</div>
```

Avantage :

* ton watcher reste simple
* la logique est testable / lisible

---

## 10) Résumé de la leçon

* `$watch` observe une variable précise
* il déclenche une fonction quand elle change
* plus lisible que `x-effect` quand tu veux être explicite
* utile pour :

  * recherche
  * filtres
  * cohérence d’état
  * persistance

---

## Mini exercice (obligatoire)

### Exercice A — Watch search

* variable `search`
* watcher qui met à jour `appliedSearch`

### Exercice B — Watch category

* variable `category`
* watcher qui reset `search`

### Exercice C — Debug

* variable `count`
* watcher qui log la valeur

---

### Étape suivante logique

**Leçon 3 — `x-ref` et `$refs` : DOM contrôlé (focus, scroll, sélection)**
Là on passe au niveau supérieur : manipuler le DOM proprement sans “querySelector partout”.
