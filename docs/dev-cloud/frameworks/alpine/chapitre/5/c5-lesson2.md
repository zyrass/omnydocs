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

## `x-for` : afficher des listes (syntaxe, arrays, objets)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `x-for` pour générer une UI à partir d’un tableau
* comprendre la syntaxe correcte (et les erreurs classiques)
* afficher :

  * une liste simple (array de strings)
  * une liste d’objets (cas réel)
  * l’index (position)
* faire un rendu lisible et maintenable
* préparer le terrain pour le tri / filtre / recherche (Leçon 4)

`x-for` est un outil central : dès que tu as des données, tu dois pouvoir les afficher proprement.

---

## 1) Définition simple

`x-for` répète un morceau de HTML pour chaque élément d’une liste.

Tu lui donnes :

* une variable (ex: `item`)
* une collection (ex: `items`)

Et Alpine génère le DOM.

---

## 2) Règle obligatoire : `x-for` se met sur un `<template>`

Tu dois écrire :

```html
<template x-for="item in items">
  <li x-text="item"></li>
</template>
```

Pas :

```html
<li x-for="item in items">...</li>
```

Ce dernier est incorrect.

Pourquoi ?
Parce que `template` est une balise spéciale qui sert de “moule”.
Alpine utilise ce moule pour créer plusieurs éléments.

---

# 3) Exemple #1 — Array simple (strings)

```html
<div x-data="{ skills: ['HTML', 'CSS', 'JavaScript', 'Alpine.js'] }">
  <h3>Compétences</h3>

  <ul>
    <template x-for="skill in skills">
      <li x-text="skill"></li>
    </template>
  </ul>
</div>
```

### Ce que ça fait

* Alpine lit le tableau `skills`
* crée un `<li>` par élément
* affiche la valeur

---

## 4) Exemple #2 — Avec index

Tu peux récupérer la position dans la liste :

```html
<div x-data="{ skills: ['HTML', 'CSS', 'JavaScript', 'Alpine.js'] }">
  <ul>
    <template x-for="(skill, index) in skills">
      <li>
        <strong x-text="index + 1"></strong>
        —
        <span x-text="skill"></span>
      </li>
    </template>
  </ul>
</div>
```

Ici :

* `index` commence à 0
* on affiche `index + 1` pour une numérotation humaine

---

# 5) Exemple #3 — Liste d’objets (cas réel)

En vrai projet, tu n’affiches presque jamais des strings.
Tu affiches des objets.

Exemple : utilisateurs.

```html
<div x-data="{
  users: [
    { id: 1, name: 'Alain', role: 'admin' },
    { id: 2, name: 'Sarah', role: 'user' },
    { id: 3, name: 'Mehdi', role: 'moderator' }
  ]
}">
  <h3>Utilisateurs</h3>

  <ul>
    <template x-for="user in users" :key="user.id">
      <li>
        <strong x-text="user.name"></strong>
        —
        <span x-text="user.role"></span>
      </li>
    </template>
  </ul>
</div>
```

### Point clé

Tu vois ici un truc nouveau :

* `:key="user.id"`

C’est obligatoire dès que tu veux un rendu sérieux.

On le détaille dans la Leçon 3, mais retiens déjà :

> sans key stable, tu peux avoir des bugs invisibles.

---

# 6) Exemple #4 — `x-for` + `x-show` (pattern très courant)

Tu veux afficher une liste seulement si elle a du contenu.

```html
<div x-data="{ items: ['A', 'B', 'C'] }">
  <p x-show="items.length === 0">
    Liste vide.
  </p>

  <ul x-show="items.length > 0">
    <template x-for="item in items">
      <li x-text="item"></li>
    </template>
  </ul>
</div>
```

C’est un pattern propre :

* état vide clair
* liste affichée seulement si utile

---

# 7) `x-for` sur objets (clé/valeur)

Tu peux aussi boucler sur un objet.

Exemple :

```html
<div x-data="{ config: { theme: 'dark', lang: 'fr', version: '1.0.0' } }">
  <ul>
    <template x-for="(value, key) in config" :key="key">
      <li>
        <strong x-text="key"></strong> :
        <span x-text="value"></span>
      </li>
    </template>
  </ul>
</div>
```

Très utile pour debug ou affichage de settings.

---

# 8) Pièges fréquents avec `x-for`

## Piège A — oublier le `template`

Ça ne marche pas ou ça donne un rendu bizarre.

Toujours :

```html
<template x-for="...">...</template>
```

---

## Piège B — modifier la liste sans `:key`

Sans key stable, Alpine peut “réutiliser” des éléments DOM de manière inattendue.

Résultat :

* checkbox qui change de ligne
* input qui garde une mauvaise valeur
* transitions qui glitch

Conclusion :

> Dès que tu as des objets, mets une key stable.

---

## Piège C — faire du rendu lourd dans la boucle

Si tu fais des calculs lourds dans chaque item, tu vas ralentir ton UI.

Solution :

* préparer les données avant
* utiliser getters ou méthodes

---

# 9) Bon pattern pro : séparer “data” et “UI”

Au lieu d’écrire des conditions compliquées dans le HTML, fais une structure claire.

Exemple :

```html
<div x-data="{
  users: [
    { id: 1, name: 'Alain', active: true },
    { id: 2, name: 'Sarah', active: false }
  ],

  get activeUsers() {
    return this.users.filter(u => u.active);
  }
}">
  <ul>
    <template x-for="user in activeUsers" :key="user.id">
      <li x-text="user.name"></li>
    </template>
  </ul>
</div>
```

Ton HTML devient “bête” (et c’est une bonne chose).

---

## 10) Mini exercice (obligatoire)

### Exercice A — Liste de tâches

Crée une liste :

```js
todos: [
  { id: 1, label: 'Lire la doc Alpine', done: false },
  { id: 2, label: 'Faire un atelier', done: true }
]
```

Affiche :

* label
* done (texte “oui/non”)

### Exercice B — Affichage conditionnel

Si done = true :

* texte barré
  Sinon :
* normal

Indice : `:class="{ 'done': todo.done }"`

### Exercice C — Index

Affiche le numéro de la tâche (index + 1).

---

## Résumé de la leçon

* `x-for` sert à répéter une UI à partir d’une liste
* il se met sur un `<template>`
* tu peux boucler sur arrays et objets
* tu peux récupérer l’index
* dès que tu fais du rendu sérieux, tu dois penser à `:key`

---

Prochaine leçon : **Leçon 3 — `:key` : éviter les bugs invisibles (obligatoire en rendu dynamique sérieux)**
On va expliquer pourquoi la key est non négociable en production.
