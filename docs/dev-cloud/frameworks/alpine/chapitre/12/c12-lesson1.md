---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 1

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Structure projet Vite + Alpine : organisation fichiers, imports

### Objectif de la leçon

À la fin, tu sauras :

* créer une structure de projet propre avec Vite + Alpine
* organiser ton code pour éviter le “main.js de 900 lignes”
* séparer :

  * stores
  * composants
  * utilitaires
* importer Alpine et ses plugins proprement
* préparer un starter clonable “pro”

Ici, on ne fait pas un tuto “copie-colle”.
On explique la logique d’architecture, et on te donne une structure stable.

---

## 1) Pourquoi passer sur Vite ?

Avec le CDN, tu es rapide, mais tu es limité :

* pas de découpage propre en fichiers
* pas de bundling
* pas de pipeline moderne
* pas de build optimisé
* pas de versionnage propre de tes composants

Avec Vite :

* imports propres
* build rapide
* organisation par modules
* meilleure maintenabilité

Bref : tu passes de “démo” à “projet”.

---

# 2) Architecture recommandée (simple, mais sérieuse)

Objectif :

* lisible
* scalable
* accessible à un débutant (sans complexité inutile)

Structure :

```
my-alpine-app/
  index.html
  package.json
  vite.config.js
  src/
    main.js
    styles.css
    alpine/
      index.js
      plugins.js
      stores/
        ui.store.js
        grocery.store.js
      components/
        dropdown.js
        modal.js
        tabs.js
        form.js
      utils/
        storage.js
```

### Pourquoi cette structure marche

* `src/main.js` est le point d’entrée Vite
* `src/alpine/index.js` centralise Alpine (init, start)
* `plugins.js` centralise les plugins
* `stores/` et `components/` sont séparés
* `utils/` évite la duplication (validation, storage, helpers)

Tu peux l’adapter, mais cette base est clean.

---

# 3) Installation : Vite + Tailwind + Alpine (commande)

En local :

```bash
npm create vite@latest my-alpine-app -- --template vanilla
cd my-alpine-app
npm install
```

Puis on installe Alpine + plugins :

```bash
npm install alpinejs
npm install @alpinejs/persist @alpinejs/focus @alpinejs/intersect @alpinejs/collapse @alpinejs/mask
```

Tailwind (optionnel ici, mais dans ton chapitre 12 c’est prévu) :

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

# 4) Les fichiers clés à écrire (starter clean)

## A) `src/main.js` — point d’entrée

```js
import './styles.css';
import { initAlpine } from './alpine/index.js';

initAlpine();
```

Simple. Pas de logique dedans.

---

## B) `src/alpine/index.js` — bootstrap Alpine

```js
import Alpine from 'alpinejs';
import { registerPlugins } from './plugins.js';
import { registerStores } from './stores/index.js';
import { registerComponents } from './components/index.js';

export function initAlpine() {
  // Plugins
  registerPlugins(Alpine);

  // Stores
  registerStores(Alpine);

  // Components (x-data factories)
  registerComponents();

  // Expose for debug (optionnel)
  window.Alpine = Alpine;

  // Start
  Alpine.start();
}
```

Ici tu as un vrai bootstrap.
C’est la colonne vertébrale.

---

## C) `src/alpine/plugins.js` — enregistrement des plugins

```js
import persist from '@alpinejs/persist';
import focus from '@alpinejs/focus';
import intersect from '@alpinejs/intersect';
import collapse from '@alpinejs/collapse';
import mask from '@alpinejs/mask';

/**
 * Enregistre les plugins Alpine.
 * On centralise ici pour éviter les imports dispersés.
 */
export function registerPlugins(Alpine) {
  Alpine.plugin(persist);
  Alpine.plugin(focus);
  Alpine.plugin(intersect);
  Alpine.plugin(collapse);
  Alpine.plugin(mask);
}
```

---

## D) `src/alpine/stores/index.js`

```js
import { uiStore } from './ui.store.js';
import { groceryStore } from './grocery.store.js';

export function registerStores(Alpine) {
  Alpine.store('ui', uiStore(Alpine));
  Alpine.store('grocery', groceryStore(Alpine));
}
```

Remarque :

* je passe `Alpine` au store si tu veux utiliser `$persist` dedans via `Alpine.$persist`.

---

## E) `src/alpine/stores/ui.store.js`

```js
/**
 * Store UI : global minimal.
 * On persiste uniquement ce qui doit survivre au refresh.
 */
export function uiStore(Alpine) {
  return {
    theme: Alpine.$persist('light').as('alpine:starter:ui:theme:v1'),

    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
    },
  };
}
```

---

## F) `src/alpine/stores/grocery.store.js`

```js
/**
 * Store data : liste de courses.
 * Démonstration Persist plugin sur un tableau.
 */
export function groceryStore(Alpine) {
  return {
    items: Alpine.$persist([]).as('alpine:starter:grocery:items:v1'),

    addItem(label) {
      const value = String(label ?? '').trim();
      if (!value) return;

      this.items.unshift({
        id: Date.now() + Math.random(),
        label: value,
        done: false,
      });
    },

    toggleDone(id) {
      const item = this.items.find(i => i.id === id);
      if (!item) return;
      item.done = !item.done;
    },

    removeItem(id) {
      this.items = this.items.filter(i => i.id !== id);
    },

    clearDone() {
      this.items = this.items.filter(i => !i.done);
    },
  };
}
```

---

## G) `src/alpine/components/index.js` — factories x-data

Ici tu as deux options :

1. Déclarer les factories globales (`window.*`)
2. Utiliser `Alpine.data(...)` (propre)

En Vite, le pattern propre est `Alpine.data`.

### Exemple :

```js
import Alpine from 'alpinejs';
import { dropdown } from './dropdown.js';
import { modal } from './modal.js';
import { groceryAdd } from './groceryAdd.js';

export function registerComponents() {
  Alpine.data('dropdown', dropdown);
  Alpine.data('modal', modal);
  Alpine.data('groceryAdd', groceryAdd);
}
```

---

## H) `src/alpine/components/groceryAdd.js`

```js
export function groceryAdd() {
  return {
    label: '',

    submit() {
      const value = this.label.trim();
      if (!value) return;

      this.$store.grocery.addItem(value);
      this.label = '';
    },
  };
}
```

---

# 5) `index.html` : comment utiliser les composants

Exemple minimal :

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Alpine + Vite Starter</title>
  </head>

  <body x-data x-bind:data-theme="$store.ui.theme">
    <div style="max-width: 920px; margin: 0 auto; padding: 16px;">
      <h1>Starter Alpine + Vite</h1>

      <button type="button" @click="$store.ui.toggleTheme()">
        Thème : <span x-text="$store.ui.theme"></span>
      </button>

      <div style="margin-top: 16px;" x-data="groceryAdd">
        <form @submit.prevent="submit()" style="display:flex; gap:10px;">
          <input type="text" x-model="label" placeholder="Ajouter..." />
          <button type="submit">OK</button>
        </form>
      </div>

      <div style="margin-top: 16px;">
        <template x-for="item in $store.grocery.items" :key="item.id">
          <div style="display:flex; gap:10px; align-items:center;">
            <input type="checkbox" :checked="item.done" @change="$store.grocery.toggleDone(item.id)" />
            <span x-text="item.label"></span>
            <button type="button" @click="$store.grocery.removeItem(item.id)">
              Supprimer
            </button>
          </div>
        </template>
      </div>
    </div>

    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

Note :

* c’est Vite, donc `type="module"` obligatoire

---

# 6) Tailwind : intégration minimale (sans t’embrouiller)

## A) `tailwind.config.js`

```js
export default {
  content: ['./index.html', './src/**/*.{js,ts}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

## B) `src/styles.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Optionnel : base focus visible (bonne habitude) */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,0,0,0.18);
}
```

---

# 7) Pièges fréquents (important)

## Piège A — mettre Alpine dans 15 fichiers sans point d’entrée

Tu perds la vision d’ensemble.

Solution :

* un bootstrap (`src/alpine/index.js`)

## Piège B — factories globales via `window.*`

Ça marche, mais ça pollue.

Solution :

* `Alpine.data('name', factory)`

## Piège C — persister n’importe quoi

Rappel :

* pas de token
* pas de secrets
* pas de données perso

## Piège D — `x-data="{...}"` partout en dur

Pour un composant réutilisable :

* préfère une factory `Alpine.data(...)`

---

# 8) Mini exercice (obligatoire)

### Exercice A — Ajouter un composant Dropdown

Crée `src/alpine/components/dropdown.js`
Puis enregistre-le dans `registerComponents()`
Puis utilise-le dans `index.html`.

### Exercice B — Ajouter un store `blog`

Persiste `favoriteIds` comme on l’a fait.

### Exercice C — Ajouter un plugin Focus + modal

Import `@alpinejs/focus`, puis fais une modal accessible.

---

## Résumé de la leçon

* Vite = passage au niveau projet
* un bootstrap Alpine central = lisibilité
* plugins/stores/components séparés = maintenabilité
* `Alpine.data(...)` = composants propres
* Tailwind s’ajoute sans casser l’architecture

---

### Étape suivante logique

Chapitre 12 — Production Ready
**Leçon 2 — Convention de composants Alpine : nommage, découpage, lisibilité**
On va définir une convention stricte pour que tout ton pack final soit homogène et vendable.
