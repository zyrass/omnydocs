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

## Transition sur listes : ajout/suppression, timing (sans glitch)

### Objectif de la leçon

À la fin, tu sauras :

* animer une liste quand elle change (ajout / suppression)
* comprendre pourquoi c’est plus compliqué qu’un simple `x-show`
* éviter les bugs visuels :

  * éléments qui sautent
  * animation sur le mauvais item
  * disparition brutale
* appliquer une méthode propre et réutilisable pour :

  * Todo list
  * Blog mock
  * notifications
  * panier / liste de courses

---

## 1) Pourquoi animer une liste est différent d’un bloc simple

Un `x-show` anime un élément unique.

Une liste, c’est autre chose :

* tu ajoutes un item → il apparaît
* tu supprimes un item → il disparaît
* mais surtout :

  * les autres items changent de position
  * le DOM est “réorganisé”
  * et là tu peux avoir des glitchs

Donc la base absolue pour une liste animée, c’est :

> `:key` stable, sinon tu vas animer le mauvais élément.

---

# 2) Première règle : une liste dynamique sérieuse = `:key`

Tu dois faire :

```html
<template x-for="item in items" :key="item.id">
  ...
</template>
```

Si tu mets `:key="index"` :

* Alpine peut réutiliser un DOM d’un item pour un autre
* et l’animation va sembler “buggée”

---

## 3) Problème technique : “suppression” = disparition instantanée

Quand tu fais :

```js
items = items.filter(...)
```

L’élément disparaît immédiatement du DOM.

Donc tu ne peux pas “animer sa sortie” si tu le supprimes trop tôt.

Tu dois faire un pattern “pro” :

1. marquer l’item comme “deleting”
2. lancer la transition visuelle
3. supprimer réellement après un délai

C’est exactement ce que font les apps sérieuses.

---

# 4) Exemple complet : Todo list animée (ajout + suppression douce)

### Fonctionnalités

* ajout item
* suppression animée
* animation d’apparition
* pas de glitch grâce à `:key`

Copie-colle :

```html
<div x-data="todoAnimated()" style="max-width: 720px; margin: 0 auto;">
  <h2>Todo list animée</h2>

  <form @submit.prevent="add()" style="display:flex; gap:10px; margin-top:10px;">
    <input
      type="text"
      x-model="label"
      placeholder="Nouvelle tâche..."
      style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
    />
    <button type="submit" style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;">
      Ajouter
    </button>
  </form>

  <p style="margin-top:10px; color:#666;">
    Total : <strong x-text="todos.length"></strong>
  </p>

  <ul style="list-style:none; padding:0; display:flex; flex-direction:column; gap:10px; margin-top:10px;">
    <template x-for="todo in todos" :key="todo.id">
      <li
        x-show="!todo.isDeleting"
        x-transition.opacity.scale
        style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; align-items:center; gap:10px;"
      >
        <span x-text="todo.label"></span>

        <button
          type="button"
          @click="remove(todo.id)"
          style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
        >
          Supprimer
        </button>
      </li>
    </template>
  </ul>
</div>

<script>
  function todoAnimated() {
    return {
      label: '',
      nextId: 1,
      todos: [],

      add() {
        const value = this.label.trim();
        if (!value) return;

        this.todos.unshift({
          id: this.nextId++,
          label: value,
          isDeleting: false,
        });

        this.label = '';
      },

      remove(id) {
        const todo = this.todos.find(t => t.id === id);
        if (!todo) return;

        // 1) déclenche l'animation de sortie
        todo.isDeleting = true;

        // 2) supprime après la durée de transition
        // x-transition default ≈ 150ms/200ms, on laisse un peu de marge
        setTimeout(() => {
          this.todos = this.todos.filter(t => t.id !== id);
        }, 220);
      },
    };
  }
</script>
```

---

## 5) Pourquoi ce pattern est propre ?

### 1) `x-show` gère l’animation

* entrée/sortie propre
* aucune brutalité

### 2) on ne supprime pas immédiatement

On marque l’item `isDeleting = true` pour laisser la transition se faire.

### 3) `:key` évite les bugs invisibles

Sans key stable :

* mauvais item animé
* état qui saute
* UI incohérente

---

# 6) Timing : comment choisir le délai ?

Tu dois aligner le délai `setTimeout` avec la durée de transition.

Si tu utilises une transition custom de 300ms, tu mets 300ms.

Ici on a mis 220ms :

* assez pour laisser la sortie visible
* pas trop long

### Règle pro

> La durée de l’animation doit être la même que la durée du “delete réel”.

---

## 7) Pièges fréquents

### Piège A — supprimer directement

Mauvais :

```js
this.todos = this.todos.filter(...)
```

Tu tues l’animation.

---

### Piège B — utiliser `x-if` pour la liste

`x-if` détruit l’élément immédiatement.
Tu perds la transition de sortie.

Règle débutant :

* liste animée → `x-show` + transition

---

### Piège C — key instable

On l’a déjà dit, mais je le répète parce que c’est critique :

> une liste animée sans key stable est une liste qui buggera.

---

# 8) Variante : animation d’ajout plus visible

Tu peux faire un style plus “app moderne” :

* entrée : opacity 0 + translateY
* sortie : inverse

Avec Tailwind c’est simple, mais ici on reste compréhensible.

Tu verras ça en mode Vite + Tailwind dans les chapitres suivants.

---

## 9) Mini exercice (obligatoire)

### Exercice A — Ajout en bas

Au lieu de `unshift`, fais `push` et observe l’UX.

### Exercice B — Confirmation suppression

Ajoute un `confirm()` avant suppression.

### Exercice C — Done + animation

Ajoute un champ `done` et une checkbox.
Quand `done` passe true :

* l’item devient gris
* et remonte en bas (bonus : tri dynamique)

---

## Résumé de la leçon

* animer une liste, c’est plus complexe qu’un bloc
* `:key` stable est obligatoire
* suppression propre = 2 étapes :

  1. animation visuelle
  2. suppression réelle après délai

---

### Étape suivante logique

**Leçon 3 — Modal production-ready (UX)**
Overlay, fermeture outside/Escape, focus, et surtout le concept de scroll lock.
