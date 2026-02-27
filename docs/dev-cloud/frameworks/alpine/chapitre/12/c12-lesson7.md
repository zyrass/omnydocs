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

# Component Library (pack réutilisable)

## Objectif : livrer une librairie de composants Alpine + Tailwind “vendable”

### Pourquoi ce chapitre est le plus important de la formation

Jusqu’ici, tu as appris Alpine.

Maintenant tu vas **industrialiser** Alpine.

Une librairie de composants, c’est ce qui te permet :

* d’aller vite sur tous tes futurs projets
* de garder une cohérence UI/UX
* de ne pas réécrire 20 fois les mêmes modals
* de vendre une formation “pro” avec un livrable final concret

Tu passes du niveau “je connais Alpine” au niveau :

> “Je peux ship une UI propre et cohérente en 2 heures.”

---

# 1) Ce que tu vas livrer (pack final)

Composants inclus :

* Navbar responsive
* Dropdown menu
* Modal accessible
* Tabs (H/V)
* Accordéon (Collapse)
* Toast notifications
* Tooltip
* Search bar debounce
* DataTable (tri + filtre)
* Theme switcher AAA

Chaque composant inclut :

* une API (options dans `x-data`)
* un exemple complet
* une checklist accessibilité
* un exemple d’intégration dans un projet réel

---

# 2) Structure du pack (propre et clonable)

Structure recommandée :

```
src/alpine/
  components/
    navbar/
      navbar.js
    dropdown/
      dropdown.js
    modal/
      modal.js
    tabs/
      tabs.js
    accordion/
      accordion.js
    toast/
      toast.store.js
      toast.component.js
    tooltip/
      tooltip.js
    search/
      search.js
    datatable/
      datatable.js
    theme/
      theme.store.js
```

Pourquoi c’est propre :

* chaque composant a son fichier
* les stores sont séparés
* tu peux documenter chaque module

---

# 3) Convention de documentation (format vendable)

Pour chaque composant, tu dois avoir :

## A) Résumé

* à quoi ça sert
* quand l’utiliser

## B) API

Options disponibles (avec défauts)

## C) Exemple complet

Copie-colle utilisable

## D) Accessibilité

Checklist courte

## E) Pièges

Ce qu’il ne faut pas faire

---

# 4) Composant 1 — Theme Switcher AAA (store global)

Ce composant est la base du pack.
Parce que tous les composants doivent être cohérents avec le thème.

---

## A) Store `theme.store.js`

```js
export function themeStore(Alpine) {
  return {
    theme: Alpine.$persist('light').as('ov:theme:v1'),

    toggle() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
    },

    set(value) {
      if (value !== 'light' && value !== 'dark') return;
      this.theme = value;
    },
  };
}
```

---

## B) Utilisation

```html
<body x-data x-bind:data-theme="$store.theme.theme">
  <button type="button" @click="$store.theme.toggle()">
    Thème : <span x-text="$store.theme.theme"></span>
  </button>
</body>
```

### Checklist accessibilité

* bouton réel
* texte visible
* focus visible

---

# 5) Composant 2 — Navbar responsive (production-ready)

### Objectif

* menu burger
* fermeture outside
* fermeture Escape
* navigation clavier simple

---

## A) `navbar.js`

```js
export function navbar(userOptions = {}) {
  return {
    options: {
      closeOnOutside: true,
      closeOnEscape: true,
      ...userOptions,
    },

    open: false,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    onEscape() {
      if (!this.options.closeOnEscape) return;
      this.close();
    },

    onOutside() {
      if (!this.options.closeOnOutside) return;
      this.close();
    },
  };
}
```

---

## B) Exemple HTML

```html
<nav x-data="ov-navbar()" style="border:1px solid #eee; border-radius:16px; padding:12px;">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <strong>OmnyUI</strong>

    <button
      type="button"
      @click="toggle()"
      :aria-expanded="open"
      aria-controls="nav-panel"
    >
      ☰
    </button>
  </div>

  <div
    id="nav-panel"
    x-show="open"
    x-cloak
    @click.outside="onOutside()"
    @keydown.escape.window="onEscape()"
    style="margin-top:10px;"
  >
    <a href="#" style="display:block; padding:8px 0;">Accueil</a>
    <a href="#" style="display:block; padding:8px 0;">Docs</a>
    <a href="#" style="display:block; padding:8px 0;">Contact</a>
  </div>
</nav>
```

### Checklist accessibilité

* bouton burger réel
* aria-expanded
* Escape/outside

---

# 6) Composant 3 — Dropdown Menu

Tu l’as déjà, on le formalise en pack.

API :

* `closeOnOutside`
* `closeOnEscape`
* `id`

Event :

* `dropdown:select`

---

## `dropdown.js`

```js
export function dropdown(userOptions = {}) {
  return {
    options: {
      id: 'dropdown-panel',
      closeOnOutside: true,
      closeOnEscape: true,
      ...userOptions,
    },

    open: false,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    onOutside() {
      if (!this.options.closeOnOutside) return;
      this.close();
    },

    onEscape() {
      if (!this.options.closeOnEscape) return;
      this.close();
    },

    select(value) {
      this.$dispatch('dropdown:select', { value });
      this.close();
    },
  };
}
```

---

# 7) Composant 4 — Modal accessible (Focus plugin)

API :

* `closeOnOutside`
* `closeOnEscape`

Events :

* `modal:confirm`
* `modal:cancel`

---

## `modal.js`

```js
export function modal(userOptions = {}) {
  return {
    options: {
      closeOnOutside: true,
      closeOnEscape: true,
      ...userOptions,
    },

    open: false,

    openModal() {
      this.open = true;
    },

    closeModal() {
      this.open = false;
    },

    onEscape() {
      if (!this.options.closeOnEscape) return;
      this.closeModal();
      this.$dispatch('modal:cancel');
    },

    onOutside() {
      if (!this.options.closeOnOutside) return;
      this.closeModal();
      this.$dispatch('modal:cancel');
    },

    confirm() {
      this.$dispatch('modal:confirm');
      this.closeModal();
    },
  };
}
```

---

# 8) Composant 5 — Tabs H/V (horizontal/vertical)

API :

* `defaultTab`
* `tabs[]`

---

## `tabs.js`

```js
export function tabs(userOptions = {}) {
  return {
    options: {
      defaultTab: 'overview',
      ...userOptions,
    },

    active: null,

    init() {
      this.active = this.options.defaultTab;
    },

    set(tab) {
      this.active = tab;
    },

    is(tab) {
      return this.active === tab;
    },
  };
}
```

---

# 9) Composant 6 — Accordéon (Collapse)

API :

* `singleOpen` (true/false)

---

## `accordion.js`

```js
export function accordion(userOptions = {}) {
  return {
    options: {
      singleOpen: true,
      ...userOptions,
    },

    openIds: [],

    toggle(id) {
      if (this.options.singleOpen) {
        this.openIds = this.openIds.includes(id) ? [] : [id];
        return;
      }

      if (this.openIds.includes(id)) {
        this.openIds = this.openIds.filter(x => x !== id);
      } else {
        this.openIds = [...this.openIds, id];
      }
    },

    isOpen(id) {
      return this.openIds.includes(id);
    },
  };
}
```

---

# 10) Composant 7 — Toast notifications (store + dispatch)

Un toast est un message temporaire.

Exemple :

* “Sauvegardé”
* “Erreur réseau”
* “Ajouté au panier”

Pattern propre :

* store global `toast`
* composant affichage

---

## A) `toast.store.js`

```js
export function toastStore() {
  return {
    items: [],

    push(message, type = 'info', duration = 2500) {
      const id = Date.now() + Math.random();

      this.items.push({ id, message, type });

      setTimeout(() => {
        this.items = this.items.filter(t => t.id !== id);
      }, duration);
    },

    remove(id) {
      this.items = this.items.filter(t => t.id !== id);
    },
  };
}
```

---

## B) Exemple HTML

```html
<div style="position:fixed; top:12px; right:12px; display:flex; flex-direction:column; gap:10px;">
  <template x-for="t in $store.toast.items" :key="t.id">
    <div style="border:1px solid #eee; border-radius:12px; padding:12px; background:#fff;">
      <strong x-text="t.type.toUpperCase()"></strong>
      <div style="color:#666;" x-text="t.message"></div>
      <button type="button" @click="$store.toast.remove(t.id)">Fermer</button>
    </div>
  </template>
</div>
```

---

# 11) Composant 8 — Tooltip (simple mais propre)

Un tooltip doit :

* apparaître au hover
* apparaître au focus (clavier)

Donc tu utilises :

* `mouseenter`
* `mouseleave`
* `focus`
* `blur`

---

## `tooltip.js`

```js
export function tooltip(userOptions = {}) {
  return {
    options: {
      text: 'Tooltip',
      ...userOptions,
    },

    open: false,

    show() {
      this.open = true;
    },

    hide() {
      this.open = false;
    },
  };
}
```

---

# 12) Composant 9 — Search bar debounce

API :

* `delay`
* `onSearch` (callback via event)

---

## `search.js`

```js
export function searchBar(userOptions = {}) {
  return {
    options: {
      delay: 250,
      ...userOptions,
    },

    query: '',

    emit() {
      this.$dispatch('search:change', { query: this.query.trim() });
    },
  };
}
```

HTML :

```html
<div x-data="ov-searchBar()">
  <input
    type="text"
    x-model="query"
    @input.debounce.250ms="emit()"
    placeholder="Rechercher..."
  />
</div>
```

---

# 13) Composant 10 — DataTable (tri + filtre)

C’est le composant le plus “boss final”.

Fonctionnalités :

* tri colonne
* recherche
* affichage stable
* `:key` correct
* pagination simple (bonus)

On le fait en version “simple mais propre”.

---

## `datatable.js`

```js
export function dataTable(userOptions = {}) {
  return {
    options: {
      rows: [],
      columns: [],
      ...userOptions,
    },

    query: '',
    sortKey: null,
    sortDir: 'asc',

    setSort(key) {
      if (this.sortKey === key) {
        this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortKey = key;
        this.sortDir = 'asc';
      }
    },

    get viewRows() {
      let rows = this.options.rows;

      const q = this.query.trim().toLowerCase();
      if (q) {
        rows = rows.filter(r => JSON.stringify(r).toLowerCase().includes(q));
      }

      if (this.sortKey) {
        rows = [...rows].sort((a, b) => {
          const va = a[this.sortKey];
          const vb = b[this.sortKey];

          if (va < vb) return this.sortDir === 'asc' ? -1 : 1;
          if (va > vb) return this.sortDir === 'asc' ? 1 : -1;
          return 0;
        });
      }

      return rows;
    },
  };
}
```

---

# 14) Résumé du pack final

Tu as maintenant :

* des composants cohérents
* une architecture réutilisable
* une base vendable

Et surtout :

* tu as un livrable final concret qui prouve ta maîtrise.

---

# 15) Dernier livrable attendu (fin de formation)

Tu dois fournir :

1. un repo starter `alpine-vite-tailwind-starter`
2. une page `AAA Theme Test`
3. un dossier `components/` complet
4. une doc par composant (API + exemple + a11y)
5. une checklist release

Tu peux vendre ça.

---

## Prochaine étape logique (si on continue la production)

On peut maintenant faire un truc très propre :

* générer un **template MDX standard** pour chaque composant
  (comme tu le fais déjà dans OmnyDocs)
* et ensuite on rédige un par un :

  * Navbar
  * Dropdown
  * Modal
  * Tabs
  * Accordéon
  * Toast
  * Tooltip
  * Search
  * DataTable

Mais là, objectivement, ton plan est complet et solide.
