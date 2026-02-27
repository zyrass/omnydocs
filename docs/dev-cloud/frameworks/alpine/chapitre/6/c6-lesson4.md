---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 4

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `:key` : éviter les bugs invisibles (obligatoire en rendu dynamique sérieux)

### Objectif de la leçon

À la fin, tu sauras :

* comprendre ce que fait réellement `:key`
* pourquoi c’est **obligatoire** dès que tu manipules des listes dynamiques
* reconnaître les symptômes d’un rendu sans key (bugs “fantômes”)
* choisir une key correcte (stable, unique)
* éviter les mauvaises keys (index, random)

Si tu retiens une seule chose de cette leçon :

> Une liste sans `:key` peut fonctionner… jusqu’au jour où elle te détruit la logique de ton UI.

---

## 1) C’est quoi `:key` exactement ?

Quand Alpine rend une liste avec `x-for`, il doit décider :

* est-ce que cet élément DOM correspond encore au même item ?
* ou est-ce qu’il faut le remplacer ?

La key est l’identité unique d’un item.

### Analogie simple

Imagine une classe d’élèves.

* Sans carte d’identité : tu peux confondre les élèves quand ils changent de place.
* Avec carte d’identité : tu sais qui est qui, même si tu réorganises la classe.

`key` = carte d’identité de chaque item.

---

## 2) Pourquoi ça existe ? (le vrai problème)

Quand tu ajoutes/supprimes des éléments dans une liste, Alpine doit “réconcilier” le DOM.

Réconcilier = faire correspondre :

* les anciens éléments
* avec les nouveaux éléments

Si Alpine n’a pas de key stable, il peut faire une optimisation :

> “Je réutilise le DOM existant et je remplace juste les textes.”

Et c’est là que tu te fais piéger.

---

# 3) Le bug typique : checkbox qui se coche sur la mauvaise ligne

### Exemple de Todo list

Tu as :

* une checkbox (done)
* un label

Si tu supprimes le premier élément sans key stable, Alpine peut réutiliser le DOM du premier pour le second.

Résultat :

* tu supprimes “Tâche A”
* mais la checkbox de “Tâche B” garde l’état de “Tâche A”
* donc “Tâche B” apparaît cochée alors que ce n’est pas vrai

Tu as l’impression que ton state est cassé… alors que c’est ton DOM qui est mal “matché”.

---

## 4) Comment utiliser `:key` correctement

### Règle obligatoire

Tu mets `:key` sur le `<template>` qui contient le `x-for`.

Exemple :

```html
<template x-for="todo in todos" :key="todo.id">
  <li>
    <input type="checkbox" x-model="todo.done" />
    <span x-text="todo.label"></span>
  </li>
</template>
```

Ici, Alpine sait que :

* l’item est identifié par `todo.id`

---

# 5) Qu’est-ce qu’une bonne key ?

Une bonne key est :

* unique (pas de doublon)
* stable (ne change pas)
* prévisible

### Exemple parfait

* `todo.id`
* `user.id`
* `product.sku`

---

## 6) Les mauvaises keys (et pourquoi c’est mauvais)

### Mauvais choix #1 — l’index

```html
<template x-for="(todo, index) in todos" :key="index">
```

Pourquoi c’est mauvais ?
Parce que l’index change quand tu supprimes ou ajoutes un élément.

Donc l’identité n’est pas stable.

Exemple :

* tu supprimes l’élément 0
* l’élément 1 devient 0
* Alpine croit que c’est le même item, alors que non

---

### Mauvais choix #2 — `Math.random()`

```html
<template x-for="todo in todos" :key="Math.random()">
```

C’est encore pire.

Pourquoi ?
Parce que la key change à chaque rendu.

Donc Alpine va :

* détruire et recréer tout le DOM
* perdre les états
* faire ramer ton UI

---

### Mauvais choix #3 — une propriété non unique

Exemple :

```html
:key="todo.label"
```

Si tu as deux tâches “Acheter du lait”, tu as un conflit.

Et tu vas créer des comportements incohérents.

---

# 7) Exemple complet (mini démo pédagogique)

Voici une liste avec `id` stable.

```html
<div x-data="{
  todos: [
    { id: 10, label: 'Tâche A', done: false },
    { id: 20, label: 'Tâche B', done: true },
    { id: 30, label: 'Tâche C', done: false }
  ],

  removeFirst() {
    this.todos.shift();
  }
}">
  <button @click="removeFirst()">Supprimer la première</button>

  <ul style="margin-top: 10px;">
    <template x-for="todo in todos" :key="todo.id">
      <li style="display:flex; gap:10px; align-items:center;">
        <input type="checkbox" x-model="todo.done" />
        <span x-text="todo.label"></span>
      </li>
    </template>
  </ul>
</div>
```

Tu peux tester :

* coche/décoche
* supprime le premier
* tu verras que l’état reste correct

Parce que Alpine sait exactement qui est qui.

---

# 8) Impact sur les transitions (important)

Quand tu fais des transitions sur une liste (comme dans l’atelier #3), sans key stable :

* Alpine peut animer le mauvais élément
* l’animation peut glitch
* tu vois des effets “fantômes”

Donc si tu veux une UI propre :

> `:key` est non négociable.

---

# 9) Résumé clair (table)

| Choix de key    | Qualité        | Pourquoi              |
| --------------- | -------------- | --------------------- |
| `item.id`       | Excellent      | stable + unique       |
| `item.slug`     | Très bon       | stable + unique       |
| `index`         | Mauvais        | change selon l’ordre  |
| `Math.random()` | Catastrophique | change à chaque rendu |
| `item.label`    | Risqué         | pas toujours unique   |

---

## Mini exercice (obligatoire)

### Exercice A — Liste d’utilisateurs

Crée une liste :

```js
users: [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
]
```

Affiche avec `x-for` + `:key="user.id"`.

### Exercice B — Test suppression

Ajoute un bouton “Supprimer le premier” et vérifie que l’affichage reste cohérent.

### Exercice C — Cas piège

Teste `:key="index"` et observe si tu peux provoquer un bug avec checkbox + suppression.

---

## Conclusion de la leçon

`x-for` sans `:key`, c’est comme :

* gérer une base de données sans identifiant unique
* tu peux faire semblant que ça marche
* jusqu’au jour où tu perds la cohérence

---

Prochaine leçon : **Leçon 4 — Tri / filtre / recherche : patterns réutilisables**
On va faire ce que tu feras dans 100% des apps : transformer une liste en UI dynamique, propre et maintenable.
