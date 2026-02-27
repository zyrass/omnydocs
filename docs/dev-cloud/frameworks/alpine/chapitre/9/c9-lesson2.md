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

## Créer un store Alpine : state + actions (propre, réutilisable)

### Objectif de la leçon

À la fin, tu sauras :

* créer un store global avec `Alpine.store()`
* structurer un store proprement :

  * state
  * actions
* utiliser `$store` dans plusieurs composants
* éviter les erreurs classiques (mutation sauvage, fonctions mal placées)
* poser une base solide pour l’atelier “liste de courses multi-composants”

---

## 1) Ce qu’on va construire (simple mais réaliste)

On va créer un store “courses” :

* `items[]` = liste des courses
* actions :

  * `addItem(label)`
  * `removeItem(id)`
  * `toggleDone(id)`
  * `clearAll()`

Puis on fera 3 composants :

1. Ajout
2. Liste
3. Stats

Tous synchronisés sans events.

---

# 2) Rappel important : un store Alpine se crée au bon moment

Un store doit être initialisé quand Alpine démarre.

On utilise :

```js
document.addEventListener('alpine:init', () => {
  Alpine.store('name', { ... })
})
```

Pourquoi ?
Parce que Alpine doit être prêt, sinon tu peux avoir :

* store non disponible
* `$store` undefined

---

# 3) Code complet : Store “grocery” (courses)

Copie-colle tel quel (CDN ou Vite, même logique).

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Store Alpine — Liste de courses</h2>
  <p style="color:#666;">
    3 composants séparés, 1 seul store global. Zéro duplication.
  </p>

  <!-- Composant 1 : ajout -->
  <div x-data="groceryAdd()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Ajouter</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Lait"
        style="flex:1; padding:10px; border:1px solid #ddd; border-radius:10px;"
      />
      <button
        type="submit"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;"
      >
        Ajouter
      </button>
    </form>

    <p style="margin-top:10px; color:#666;">
      Dernier ajout : <strong x-text="lastAdded || '—'"></strong>
    </p>
  </div>

  <!-- Composant 2 : liste -->
  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Liste</h3>

    <p style="margin-top:10px; color:#666;">
      Items : <strong x-text="$store.grocery.items.length"></strong>
    </p>

    <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px;">
      <template x-for="item in $store.grocery.items" :key="item.id">
        <div
          style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; gap:10px; align-items:center;"
        >
          <label style="display:flex; gap:10px; align-items:center; flex:1; min-width:0;">
            <input type="checkbox" :checked="item.done" @change="$store.grocery.toggleDone(item.id)" />
            <span
              x-text="item.label"
              :style="item.done ? 'text-decoration: line-through; color:#999;' : 'color:#111;'"
              style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"
            ></span>
          </label>

          <button
            type="button"
            @click="$store.grocery.removeItem(item.id)"
            style="padding:8px 10px; border-radius:10px; border:1px solid #ddd; background:#fff;"
          >
            Supprimer
          </button>
        </div>
      </template>
    </div>

    <div style="display:flex; justify-content:flex-end; margin-top: 12px;">
      <button
        type="button"
        @click="$store.grocery.clearAll()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Tout supprimer
      </button>
    </div>
  </div>

  <!-- Composant 3 : stats -->
  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Stats</h3>

    <p style="margin-top:10px; color:#666;">
      Total : <strong x-text="$store.grocery.items.length"></strong>
    </p>

    <p style="margin-top:6px; color:#666;">
      Terminés :
      <strong x-text="$store.grocery.items.filter(i => i.done).length"></strong>
    </p>

    <p style="margin-top:6px; color:#666;">
      Restants :
      <strong x-text="$store.grocery.items.filter(i => !i.done).length"></strong>
    </p>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    Alpine.store('grocery', {
      // STATE
      items: [],

      // ACTIONS
      addItem(label) {
        const value = String(label ?? '').trim();
        if (!value) return;

        this.items.unshift({
          id: Date.now() + Math.random(),
          label: value,
          done: false,
        });
      },

      removeItem(id) {
        this.items = this.items.filter(i => i.id !== id);
      },

      toggleDone(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;
        item.done = !item.done;
      },

      clearAll() {
        this.items = [];
      },
    });
  });

  function groceryAdd() {
    return {
      label: '',
      lastAdded: '',

      submit() {
        const value = this.label.trim();
        if (!value) return;

        this.$store.grocery.addItem(value);
        this.lastAdded = value;
        this.label = '';
      },
    };
  }
</script>
```

---

# 4) Explication formateur : pourquoi ce store est bien structuré

## A) Le store contient la “source de vérité”

La liste `items` est unique.

Donc :

* pas de duplication
* pas de synchronisation manuelle
* pas de “state incohérent”

---

## B) Les composants sont simples

Chaque composant fait un job :

* Add : collecter input + appeler action
* List : afficher + appeler actions
* Stats : calculer depuis le store

Ils ne gèrent pas eux-mêmes les données.

---

## C) Actions = logique centralisée

La logique “métier” (ajout, suppression, toggle) est dans le store.

Donc si demain tu changes une règle :

* tu modifies 1 endroit
* pas 6 composants

---

# 5) Pièges fréquents avec les stores (et comment les éviter)

## Piège A — mettre de l’UI dans le store

Exemple mauvais :

* `openModal = true` dans le store
* `activeDropdown = ...` dans le store

Ça dépend.

Règle simple :

* UI locale → `x-data`
* data partagée → store

---

## Piège B — modifier le store “en direct” partout

Exemple :

```js
$store.grocery.items.push(...)
```

Ça marche… mais c’est du bricolage.

En pro, tu veux :

```js
$store.grocery.addItem(...)
```

Pourquoi ?
Parce que tu gardes une API claire.
C’est comme une mini librairie.

---

## Piège C — IDs non stables

Ici on utilise :

```js
Date.now() + Math.random()
```

C’est suffisant pour un atelier.

En prod tu utiliserais :

* UUID
* ou un compteur incrémental stable

Mais l’idée est là : `:key` doit être stable.

---

## Piège D — store trop gros

Ne fais pas “un store pour tout”.

Meilleure pratique :

* un store “grocery”
* un store “theme”
* un store “auth”
* etc.

Ça reste lisible.

---

# 6) Mini exercice (obligatoire)

### Exercice A — Empêcher les doublons

Si un item existe déjà (même label), refuse l’ajout.

Indice : dans `addItem` :

```js
const exists = this.items.some(i => i.label.toLowerCase() === value.toLowerCase());
```

---

### Exercice B — Ajouter une action `clearDone()`

Supprime uniquement les items terminés.

---

### Exercice C — Ajouter une action `renameItem(id, label)`

Tu prépares le terrain pour une UI d’édition.

---

## Résumé de la leçon

* `Alpine.store()` te donne un état global partagé
* `$store` te permet de l’utiliser dans n’importe quel composant
* une bonne architecture = state central + actions claires
* les composants restent simples et maintenables

---

### Étape suivante logique

**Leçon 3 — Séparer UI store / Data store (lisibilité & maintenance)**
Là on va apprendre à structurer plusieurs stores et éviter de transformer ton store en “gros monolithe”.
