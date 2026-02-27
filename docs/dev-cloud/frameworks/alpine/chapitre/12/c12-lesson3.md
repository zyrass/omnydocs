---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 3

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Performance sur gros `x-for` : tri, filtre, `key`, rendu

### Objectif de la leçon

À la fin, tu sauras :

* pourquoi un `x-for` peut devenir lent
* comment éviter les ralentissements invisibles
* structurer un tri/filtre/recherche sans recalcul inutile
* utiliser `:key` correctement (obligatoire)
* écrire un rendu “pro” même sur des listes longues

C’est une leçon ultra importante parce qu’Alpine est léger…
mais si tu fais n’importe quoi dans un `x-for`, tu peux tuer ton UI.

---

## 1) Le problème : “ça marche” ≠ “ça scale”

Quand tu as 10 items, tout va bien.

Quand tu as :

* 500 items
* 2 000 items
* 10 000 items

Tu peux avoir :

* input lag (retard quand tu tapes)
* scroll qui saccade
* freeze au tri
* CPU qui chauffe

Et là tu te dis “Alpine c’est nul”.

Non.

C’est ton rendu qui est mal pensé.

---

# 2) Comment Alpine rend une liste

Quand tu fais :

```html
<template x-for="item in items">
  ...
</template>
```

Alpine doit :

* parcourir `items`
* créer du DOM pour chaque item
* mettre à jour le DOM quand `items` change

Donc si tu modifies souvent `items` :

* Alpine réagit souvent
* le DOM bouge souvent
* le navigateur travaille beaucoup

---

# 3) Le point critique : `:key` est obligatoire

### Pourquoi ?

Sans `:key`, Alpine ne sait pas identifier correctement les éléments.

Résultat :

* bugs invisibles
* mauvais item mis à jour
* checkboxes qui changent de ligne
* transitions cassées

Exemple correct :

```html
<template x-for="item in items" :key="item.id">
  <div x-text="item.label"></div>
</template>
```

Règle pro :

> La clé doit être stable et unique.

Pas `index` si la liste peut bouger.

---

# 4) Les 3 gros pièges de performance

## Piège A — filtrer directement dans le template

Tu fais :

```html
<template x-for="item in items.filter(i => i.done)">
```

Ça marche…
mais ce filtre est recalculé à chaque re-render.

Sur grosse liste :

* c’est violent.

---

## Piège B — trier en place (`sort`) sur le tableau original

`sort()` modifie le tableau original.

Donc tu fais :

```js
items.sort(...)
```

Tu modifies ton state directement.
Et ça peut casser :

* cohérence
* persistance
* logique de l’app

Solution :

* clone avant de trier.

---

## Piège C — recalculer tout à chaque frappe

Si tu as une recherche live :

* tu tapes 10 caractères
* tu déclenches 10 rendus
* sur 2000 items

Ça lag.

Solution :

* debounce
* optimisation du calcul
* pagination simple

---

# 5) Pattern pro : `items` (source) + `viewItems` (calculé)

Tu gardes :

* `items` = source de vérité
* `viewItems` = résultat filtré/trié

Exemple :

```js
get viewItems() {
  return this.items;
}
```

Puis tu enrichis.

---

# 6) Exemple complet : Liste avec filtre + tri + recherche

## Objectif

* recherche
* filtre done/active
* tri asc/desc
* rendu stable

---

## Code (CDN simple)

```html
<div style="max-width: 920px; margin:0 auto; padding:16px;" x-data="BigListDemo()">
  <h2>Performance x-for</h2>

  <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">
    <input
      type="text"
      x-model="query"
      @input.debounce.250ms="onSearch()"
      placeholder="Recherche..."
      style="padding:10px; border:1px solid #ddd; border-radius:10px; flex:1;"
    />

    <select x-model="filter" style="padding:10px; border:1px solid #ddd; border-radius:10px;">
      <option value="all">Tous</option>
      <option value="active">Actifs</option>
      <option value="done">Done</option>
    </select>

    <select x-model="sort" style="padding:10px; border:1px solid #ddd; border-radius:10px;">
      <option value="asc">Tri A→Z</option>
      <option value="desc">Tri Z→A</option>
    </select>
  </div>

  <p style="color:#666; margin-top:10px;">
    Total : <strong x-text="items.length"></strong> |
    Affichés : <strong x-text="viewItems.length"></strong>
  </p>

  <div style="margin-top:12px; display:flex; flex-direction:column; gap:8px;">
    <template x-for="item in viewItems" :key="item.id">
      <div style="display:flex; gap:10px; align-items:center; border:1px solid #eee; border-radius:12px; padding:10px;">
        <input type="checkbox" :checked="item.done" @change="toggle(item.id)" />
        <span x-text="item.label"></span>
      </div>
    </template>
  </div>
</div>

<script>
  function BigListDemo() {
    return {
      // Source de vérité
      items: Array.from({ length: 200 }, (_, i) => ({
        id: i + 1,
        label: 'Item #' + (i + 1),
        done: Math.random() > 0.7,
      })),

      // UI state
      query: '',
      filter: 'all',
      sort: 'asc',

      // Optionnel : cache de recherche (évite recalcul sur chaque frappe)
      normalizedQuery: '',

      onSearch() {
        this.normalizedQuery = this.query.trim().toLowerCase();
      },

      toggle(id) {
        const item = this.items.find(i => i.id === id);
        if (!item) return;
        item.done = !item.done;
      },

      get viewItems() {
        let result = this.items;

        // Filtre done/active
        if (this.filter === 'done') {
          result = result.filter(i => i.done);
        } else if (this.filter === 'active') {
          result = result.filter(i => !i.done);
        }

        // Recherche (sur cache)
        if (this.normalizedQuery) {
          const q = this.normalizedQuery;
          result = result.filter(i => i.label.toLowerCase().includes(q));
        }

        // Tri (clone avant sort pour ne pas muter la source)
        const sorted = [...result].sort((a, b) => {
          if (a.label < b.label) return this.sort === 'asc' ? -1 : 1;
          if (a.label > b.label) return this.sort === 'asc' ? 1 : -1;
          return 0;
        });

        return sorted;
      },
    };
  }
</script>
```

---

# 7) Pourquoi ce code est “pro”

### A) `items` n’est jamais muté par `sort`

On clone :

```js
const sorted = [...result].sort(...)
```

### B) la recherche est debounced

Donc pas de recalcul violent à chaque frappe.

### C) `:key` est stable

On utilise `id`.

---

# 8) Optimisation supplémentaire : pagination simple

Si tu as 10 000 items, même avec un tri propre,
rendre 10 000 divs = lourd.

Solution simple :

* pagination ou “afficher 50 par 50”.

Exemple :

```js
page: 1,
perPage: 50,

get paginatedItems() {
  const start = (this.page - 1) * this.perPage;
  return this.viewItems.slice(start, start + this.perPage);
}
```

Puis dans le template :

```html
<template x-for="item in paginatedItems" :key="item.id">
```

Tu viens de diviser le coût DOM.

---

# 9) Pièges invisibles qui font mal

## Piège A — `index` comme key

Si tu supprimes un item :

* les index changent
* le DOM se mélange

Donc non.

## Piège B — `x-effect` qui touche `items`

Tu peux créer une boucle de render.

## Piège C — trop de watchers

Si tu mets `$watch` sur 5 variables et que chacune déclenche un recalcul complet :

* tu crées un mini chaos

---

# 10) Règle “performance” à retenir (simple)

Tu veux être rapide ?

1. `:key` stable
2. clone avant tri
3. debounced search
4. limite le DOM (pagination)
5. évite les calculs inline dans `x-for`

---

# 11) Mini exercice (obligatoire)

### Exercice A — Ajoute un filtre “done + query”

* recherche + done
* vérifie que ça reste fluide

### Exercice B — Ajoute pagination

* 20 par page
* boutons précédent/suivant

### Exercice C — Ajoute un tri “done first”

* items done en haut
* puis tri alpha

---

## Résumé de la leçon

* `x-for` peut être lent si tu recalcules trop
* `:key` est obligatoire
* filtre/recherche/tri doivent être structurés
* pagination = arme simple et efficace

---

### Étape suivante logique

Chapitre 12 — Production Ready
**Leçon 4 — Sécurité : pièges `x-html` (cas réel, prévention)**
On va parler de XSS sérieusement, et je vais te montrer comment un composant Alpine peut devenir une faille si tu fais le malin.
