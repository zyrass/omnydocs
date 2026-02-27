---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Ateliers UI #2

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Todo list (version simple)

## Objectif de l’atelier

Créer une Todo list simple mais propre, avec :

* ajout d’une tâche via formulaire
* suppression d’une tâche
* marquer une tâche comme “done”
* compteur total
* structure lisible (pas de logique en vrac dans le HTML)

Important : on fait volontairement une version “simple”, mais avec un niveau qualité **pro**.

---

## 1) Spécification fonctionnelle

### Fonctionnalités attendues

* l’utilisateur tape une tâche
* il clique “Ajouter” (ou Enter)
* la tâche apparaît dans la liste
* il peut :

  * cocher une tâche pour la terminer
  * supprimer une tâche
* un compteur affiche :

  * nombre total
  * nombre terminées

### Règles UX minimales

* empêcher l’ajout d’une tâche vide
* nettoyer le texte (trim)
* reset l’input après ajout
* feedback visuel “terminé”

---

## 2) Livrable complet (Vanilla + CDN) — prêt à coller

Copie-colle dans un fichier `todo.html`.

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Atelier #2 — Todo simple (Alpine)</title>

    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      [x-cloak] {
        display: none !important;
      }

      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 16px;
        background: #fafafa;
      }

      .card {
        max-width: 620px;
        margin: 0 auto;
        background: #fff;
        border: 1px solid #eee;
        border-radius: 14px;
        padding: 16px;
      }

      .title {
        margin: 0;
        font-size: 20px;
      }

      .muted {
        color: #666;
        font-size: 14px;
      }

      .row {
        display: flex;
        gap: 8px;
        align-items: center;
      }

      input[type="text"] {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
      }

      button {
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background: #111;
        color: #fff;
        cursor: pointer;
      }

      button.secondary {
        background: #fff;
        color: #111;
      }

      button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      button:focus-visible,
      input:focus-visible {
        outline: 3px solid #111;
        outline-offset: 2px;
      }

      ul {
        list-style: none;
        padding: 0;
        margin: 16px 0 0;
      }

      li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 10px 12px;
        border: 1px solid #eee;
        border-radius: 12px;
        margin-bottom: 8px;
      }

      .todo-left {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
      }

      .todo-text {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 380px;
      }

      .done {
        text-decoration: line-through;
        opacity: 0.6;
      }

      .badge {
        font-size: 12px;
        padding: 4px 8px;
        border: 1px solid #ddd;
        border-radius: 999px;
        background: #fff;
        color: #111;
      }
    </style>
  </head>

  <body>
    <div class="card" x-data="todoApp()">
      <h1 class="title">Todo list — version simple</h1>
      <p class="muted">
        Objectif : ajouter / supprimer / done + compteur. Code propre, sans bricolage.
      </p>

      <!-- Formulaire d'ajout -->
      <form class="row" style="margin-top: 12px;" @submit.prevent="addTodo()">
        <input
          type="text"
          x-model="newTodo"
          placeholder="Ex: Apprendre x-model"
          aria-label="Nouvelle tâche"
        />

        <button type="submit" :disabled="newTodo.trim().length === 0">
          Ajouter
        </button>
      </form>

      <!-- Stats -->
      <div class="row" style="margin-top: 12px; justify-content: space-between;">
        <div class="row">
          <span class="badge">
            Total : <strong x-text="totalCount"></strong>
          </span>

          <span class="badge">
            Done : <strong x-text="doneCount"></strong>
          </span>
        </div>

        <button
          type="button"
          class="secondary"
          @click="clearDone()"
          :disabled="doneCount === 0"
        >
          Supprimer les terminées
        </button>
      </div>

      <!-- Liste -->
      <ul x-show="totalCount > 0" x-cloak>
        <template x-for="todo in todos" :key="todo.id">
          <li>
            <div class="todo-left">
              <input
                type="checkbox"
                x-model="todo.done"
                :aria-label="`Marquer ${todo.label} comme terminée`"
              />

              <span
                class="todo-text"
                :class="{ 'done': todo.done }"
                x-text="todo.label"
              ></span>
            </div>

            <button type="button" class="secondary" @click="removeTodo(todo.id)">
              Supprimer
            </button>
          </li>
        </template>
      </ul>

      <!-- Empty state -->
      <p x-show="totalCount === 0" x-cloak class="muted" style="margin-top: 16px;">
        Aucune tâche pour le moment. Ajoute ta première tâche.
      </p>
    </div>

    <script>
      /**
       * todoApp()
       * Version simple, mais structurée comme un vrai composant.
       */
      function todoApp() {
        return {
          // Champ input
          newTodo: "",

          // Liste des tâches
          todos: [
            { id: 1, label: "Comprendre x-data", done: true },
            { id: 2, label: "Apprendre x-model", done: false },
          ],

          // Générateur d'ID simple
          nextId: 3,

          // Stats calculées (getters)
          get totalCount() {
            return this.todos.length;
          },

          get doneCount() {
            return this.todos.filter((t) => t.done).length;
          },

          // Actions
          addTodo() {
            const label = this.newTodo.trim();

            // Sécurité UX : empêcher ajout vide
            if (label.length === 0) return;

            this.todos.push({
              id: this.nextId++,
              label,
              done: false,
            });

            // Reset input
            this.newTodo = "";
          },

          removeTodo(id) {
            this.todos = this.todos.filter((t) => t.id !== id);
          },

          clearDone() {
            this.todos = this.todos.filter((t) => !t.done);
          },
        };
      }
    </script>
  </body>
</html>
```

---

## 3) Explication formateur (ce qu’il faut comprendre)

### Pourquoi on utilise un `<form>` + `@submit.prevent` ?

Parce que c’est un vrai pattern UI.

* l’utilisateur peut cliquer sur “Ajouter”
* ou appuyer sur Enter
* sans recharger la page

Et tu restes dans une logique web standard.

### Pourquoi `x-model="newTodo"` ?

Parce que c’est la méthode propre pour récupérer la valeur du champ.

Tu ne vas pas t’amuser à faire :

```js
newTodo = $event.target.value
```

à chaque fois.

### Pourquoi un tableau d’objets ?

Parce que c’est la structure minimale réaliste.

Une todo n’est pas juste une string, c’est un objet :

* `id` (clé stable)
* `label` (texte)
* `done` (état)

Tu vas réutiliser exactement ça dans tes projets fil rouge.

---

## 4) Les pièges fréquents (à corriger tout de suite)

### Piège A — utiliser l’index comme clé

Certains font :

```html
<template x-for="(todo, index) in todos" :key="index">
```

Ça marche… jusqu’au jour où tu supprimes un élément.

Et là tu peux avoir des comportements bizarres :

* checkbox qui coche la mauvaise ligne
* UI qui “saute”

Ici on fait propre : `:key="todo.id"`.

---

### Piège B — accepter les tâches vides

Sans trim, tu peux ajouter `"     "`.

Donc on fait :

```js
const label = this.newTodo.trim();
if (label.length === 0) return;
```

C’est une règle UX simple mais essentielle.

---

### Piège C — logique dans le HTML

Tu pourrais faire des trucs compliqués dans le HTML, mais on garde le HTML simple :

* l’UI affiche
* les actions sont dans les méthodes

---

## 5) Ce que tu as appris (sans t’en rendre compte)

Tu viens d’utiliser ensemble :

* `x-data`
* `x-model`
* `@submit.prevent`
* `x-show`
* `x-cloak`
* `x-for`
* `:key`
* `:class`
* getters (calcul dynamique propre)

C’est exactement l’objectif pédagogique : assembler les briques.

---

## 6) Exercices (obligatoires)

### Exercice 1 — Ajoute un compteur “Active”

Active = tâches non terminées.

Indice :

```js
get activeCount() {
  return this.todos.filter(t => !t.done).length;
}
```

---

### Exercice 2 — Empêcher les doublons

Interdire d’ajouter deux fois la même tâche (insensible à la casse).

Exemple :

* “acheter du lait”
* “Acheter du lait”

Doit être considéré comme doublon.

---

### Exercice 3 — Ajouter un bouton “Tout cocher / Tout décocher”

Tu dois ajouter une méthode :

* `markAllDone()`
* `unmarkAllDone()`

---

## 7) Ce qu’on fera dans la Todo avancée (Atelier #3)

Dans la version avancée, on ajoute :

* filtres All / Active / Done
* animations d’ajout/suppression (`x-transition`)
* recherche avec debounce
* fermeture outside sur certains menus (si on ajoute un dropdown)
* meilleure UX

Mais pour l’instant, on reste simple et stable.

---

### Étape suivante logique

On enchaîne avec **Chapitre 4 — Événements avancés & UX** :

* modificateurs (`.prevent`, `.stop`, `.once`, `.self`)
* `.outside`
* clavier (Escape, Enter)
* `.window`, `.document`
* debounce / throttle

Puis **Atelier UI #3 — Todo list avancée (filtres + animation)**

Quand tu me dis “go”, je commence Chapitre 4, Leçon 1.
