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

## Utiliser le store dans plusieurs composants : patterns propres (multi-composants)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser un store proprement dans plusieurs composants Alpine
* appliquer des patterns “pro” :

  * composants spécialisés
  * actions claires
  * affichage dérivé (computed simple)
* éviter les erreurs fréquentes :

  * logique métier dispersée
  * calculs dupliqués partout
  * mutations directes non contrôlées
* construire une mini app “liste de courses” vraiment solide

On va faire un vrai cas réel : **multi-composants + store**.

---

## 1) Le problème classique : “j’ai un store… mais mon code reste bordélique”

Beaucoup de gens créent un store, puis :

* ils modifient `items` directement partout
* ils font des `filter()` dans tous les composants
* ils recodent la logique “done / remaining” 4 fois

Résultat :

* store inutile
* code redondant
* maintenance pénible

Donc ici on va faire les patterns propres.

---

# 2) Pattern #1 — Store = API claire

Ton store doit se lire comme une mini API.

Exemple :

* `$store.grocery.addItem(label)`
* `$store.grocery.removeItem(id)`
* `$store.grocery.toggleDone(id)`
* `$store.grocery.clearDone()`

Tu évites :

* `$store.grocery.items.push(...)`
* `$store.grocery.items = ...` depuis un composant

Pourquoi ?
Parce que sinon n’importe qui peut casser ton état.

---

# 3) Pattern #2 — Le store peut exposer des “dérivés” (computed simple)

Alpine n’a pas de computed comme Vue, mais tu peux créer des getters.

Exemple :

```js
get doneCount() {
  return this.items.filter(i => i.done).length;
}
```

C’est propre, et tu ne répètes pas les calculs dans le HTML.

---

# 4) Pattern #3 — Chaque composant a une responsabilité claire

Exemple “courses” :

* `GroceryAdd` : ajout
* `GroceryList` : affichage + actions
* `GroceryStats` : stats
* `GroceryToolbar` : filtre / reset

Tu peux les mettre dans la même page, mais ils restent conceptuellement séparés.

---

# 5) Implémentation complète : Grocery App multi-composants (pro)

### Fonctionnalités

* ajout
* suppression
* toggle done
* filtre All / Active / Done
* clear done
* stats centralisées dans le store
* un seul store = une seule source de vérité

Copie-colle :

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Grocery App — Multi-composants + Store</h2>
  <p style="color:#666;">
    Exemple propre : UI locale pour les filtres, data globale dans le store.
  </p>

  <!-- Composant : Ajout -->
  <div x-data="GroceryAdd()" style="border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Ajouter un item</h3>

    <form @submit.prevent="submit()" style="display:flex; gap:10px; margin-top:10px;">
      <input
        type="text"
        x-model="label"
        placeholder="Ex: Pommes"
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

  <!-- Composant : Toolbar (UI locale) -->
  <div x-data="GroceryToolbar()" style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Filtres</h3>

    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">
      <button
        type="button"
        @click="filter = 'all'"
        :style="filter === 'all' ? activeStyle : baseStyle"
      >
        Tous
      </button>

      <button
        type="button"
        @click="filter = 'active'"
        :style="filter === 'active' ? activeStyle : baseStyle"
      >
        Restants
      </button>

      <button
        type="button"
        @click="filter = 'done'"
        :style="filter === 'done' ? activeStyle : baseStyle"
      >
        Terminés
      </button>

      <button
        type="button"
        @click="$store.grocery.clearDone()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Supprimer terminés
      </button>

      <button
        type="button"
        @click="$store.grocery.clearAll()"
        style="padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;"
      >
        Tout supprimer
      </button>
    </div>

    <!-- Liste filtrée -->
    <div style="margin-top:12px;">
      <template x-for="item in filteredItems()" :key="item.id">
        <div
          style="border:1px solid #eee; border-radius:12px; padding:12px; display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:10px;"
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

      <p x-show="filteredItems().length === 0" x-cloak style="color:#666; margin:0;">
        Aucun item dans ce filtre.
      </p>
    </div>
  </div>

  <!-- Composant : Stats -->
  <div x-data style="margin-top: 14px; border:1px solid #eee; padding:14px; border-radius:14px; background:#fff;">
    <h3 style="margin:0;">Stats</h3>

    <p style="margin-top:10px; color:#666;">
      Total : <strong x-text="$store.grocery.totalCount"></strong>
    </p>

    <p style="margin-top:6px; color:#666;">
      Terminés : <strong x-text="$store.grocery.doneCount"></strong>
    </p>

    <p style="margin-top:6px; color:#666;">
      Restants : <strong x-text="$store.grocery.activeCount"></strong>
    </p>
  </div>
</div>

<script>
  document.addEventListener('alpine:init', () => {
    Alpine.store('grocery', {
      // DATA STATE
      items: [],

      // GETTERS (computed simple)
      get totalCount() {
        return this.items.length;
      },

      get doneCount() {
        return this.items.filter(i => i.done).length;
      },

      get activeCount() {
        return this.items.filter(i => !i.done).length;
      },

      // ACTIONS
      addItem(label) {
        const value = String(label ?? '').trim();
        if (!value) return;

        // Optionnel : empêcher doublons
        const exists = this.items.some(i => i.label.toLowerCase() === value.toLowerCase());
        if (exists) return;

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

      clearDone() {
        this.items = this.items.filter(i => !i.done);
      },

      clearAll() {
        this.items = [];
      },
    });
  });

  function GroceryAdd() {
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

  function GroceryToolbar() {
    return {
      filter: 'all',

      baseStyle: "padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#fff;",
      activeStyle: "padding:10px 12px; border-radius:10px; border:1px solid #ddd; background:#111; color:#fff;",

      filteredItems() {
        const items = this.$store.grocery.items;

        if (this.filter === 'active') {
          return items.filter(i => !i.done);
        }

        if (this.filter === 'done') {
          return items.filter(i => i.done);
        }

        return items;
      },
    };
  }
</script>
```

---

# 6) Explication : ce qui est “pro” dans ce code

## A) Les stats sont dans le store (getters)

Tu ne recalcules pas partout.

Tu peux afficher :

```html
x-text="$store.grocery.doneCount"
```

C’est propre et centralisé.

---

## B) Le filtre est UI local

Le filtre ne modifie pas les données.
Il modifie juste l’affichage.

Donc il reste dans `GroceryToolbar()`.

---

## C) Les actions sont centralisées

Même si 5 composants modifient la liste, ils utilisent tous :

* `addItem`
* `removeItem`
* `toggleDone`

Tu as un comportement cohérent.

---

# 7) Pièges fréquents

## Piège A — mettre le filtre dans le store

Tu peux, mais tu vas polluer ton store.

Sauf si :

* tu veux que le filtre soit global sur toute l’app

Sinon :

* local = mieux

---

## Piège B — filtrer directement dans le HTML avec 3 filter()

Tu peux faire :

```html
x-for="item in $store.grocery.items.filter(...).filter(...)"
```

Mais tu vas obtenir :

* un HTML illisible
* des calculs dupliqués
* un code dur à maintenir

Le mieux :

* méthode `filteredItems()` dans le composant UI

---

## Piège C — pas de key stable

Toujours :

```html
:key="item.id"
```

Sinon bug invisible assuré.

---

# 8) Résumé de la leçon

* un store doit être utilisé comme une API
* centralise les actions dans le store
* expose des getters pour éviter les calculs dupliqués
* garde l’UI state local quand c’est juste un filtre / une vue

---

## Mini exercice (obligatoire)

### Exercice A — Ajout d’une recherche

Ajoute dans `GroceryToolbar` :

* `query: ''`
* filtre par texte en plus du filtre done/active

### Exercice B — Ajout d’une priorité

Dans `items`, ajoute :

* `priority: 'low' | 'medium' | 'high'`
  Puis filtre par priorité.

### Exercice C — Event + store

Quand tu ajoutes un item :

* dispatch `ui:toast` “Item ajouté”
  (ça te fait combiner Chapitre 8 + 9)

---

### Étape suivante logique

Chapitre 10 — Persistance (localStorage + Persist)
Leçon 1 : localStorage : sauvegarder/restaurer proprement.
