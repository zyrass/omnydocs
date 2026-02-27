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

## Convention de composants Alpine : nommage, découpage, lisibilité

### Objectif de la leçon

À la fin, tu sauras :

* définir une convention claire (lisible et scalable)
* structurer tes composants Alpine comme une mini “component library”
* éviter les anti-patterns :

  * gros objets `x-data` illisibles
  * logique dispersée
  * states incohérents
* écrire des composants “vendables” :

  * API explicite
  * options
  * events
  * accessibilité intégrée

Tu veux construire une formation vendable : ça implique une convention stable, répétable.

---

## 1) Le problème : Alpine encourage le “petit code dans le HTML”…

Alpine est HTML-first, donc naturellement tu peux écrire :

```html
<div x-data="{ open:false, items:[], ... 50 lignes ... }">
```

Ça marche… jusqu’au jour où tu veux :

* réutiliser le composant
* le tester
* le maintenir
* le documenter

Le code devient illisible.

Donc : on met une convention.

---

# 2) La convention “pro” que je recommande

On s’aligne sur 4 principes :

### Principe A — un composant = une responsabilité

Exemples :

* dropdown
* modal
* tabs
* toast
* datatable

Pas :

* “componentDashboardQuiFaitTout”

### Principe B — API explicite

Ton composant doit exposer :

* state (minimal)
* actions (méthodes)
* options (config)
* events (`$dispatch`) si utile

### Principe C — pas de logique métier dans le template

Le template doit rester lisible.

Si tu as un calcul :

* tu le mets dans une méthode/getter.

### Principe D — accessibilité par défaut

Chaque composant a :

* focus visible
* clavier
* aria quand nécessaire

---

# 3) Nommage strict

### Dossier

`src/alpine/components/<component-name>/`

Exemple :

```
components/
  dropdown/
    dropdown.js
    dropdown.html (optionnel si tu externalises)
    README.md (doc interne)
```

Mais en Alpine simple, on fera juste `dropdown.js`.

### Nom Alpine.data

* en kebab-case : `dropdown-menu`
* en préfixant si tu veux éviter conflits : `ov-dropdown`

Exemple :

```js
Alpine.data('ov-dropdown', dropdown);
```

---

# 4) Structure interne d’un composant (pattern stable)

Chaque composant suit ce pattern :

* `options` (par défaut + override)
* `state` minimal
* `init()` optionnel
* `actions`
* `getters` (computed simples)

### Exemple de squelette

```js
export function componentName(userOptions = {}) {
  return {
    // --- Options ---
    options: {
      closeOnEscape: true,
      closeOnOutside: true,
      ...userOptions,
    },

    // --- State ---
    open: false,

    // --- Lifecycle ---
    init() {
      // optional
    },

    // --- Actions ---
    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    // --- Getters ---
    get isOpen() {
      return this.open === true;
    },
  };
}
```

Propre, répétable, documentable.

---

# 5) Exemple complet : Dropdown “pro” (API + a11y + outside + escape)

## A) `src/alpine/components/dropdown.js`

```js
/**
 * Dropdown réutilisable.
 * - UX : outside click, Escape
 * - A11Y : aria-expanded, aria-controls
 * - API : options configurables
 */
export function dropdown(userOptions = {}) {
  return {
    options: {
      id: 'dropdown-panel',
      closeOnEscape: true,
      closeOnOutside: true,
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

## B) Enregistrement : `src/alpine/components/index.js`

```js
import Alpine from 'alpinejs';
import { dropdown } from './dropdown.js';

export function registerComponents() {
  Alpine.data('ov-dropdown', dropdown);
}
```

## C) Utilisation : HTML

```html
<div x-data="ov-dropdown({ id: 'main-menu' })" style="position:relative;">
  <button
    type="button"
    @click="toggle()"
    :aria-expanded="open"
    :aria-controls="options.id"
  >
    Menu
  </button>

  <div
    :id="options.id"
    x-show="open"
    x-cloak
    @click.outside="onOutside()"
    @keydown.escape.window="onEscape()"
    style="position:absolute; top: 40px; left:0;"
  >
    <button type="button" @click="close()">Item 1</button>
    <button type="button" @click="close()">Item 2</button>
  </div>
</div>
```

Là tu as :

* API claire
* options
* accessibilité
* comportement pro

---

# 6) Pattern “Events” pour library vendable

Quand tu fais une library, tu ne veux pas que ton composant “connaisse” le reste.

Donc tu utilises `$dispatch`.

Exemple dropdown :

* quand on clique item 1, dispatch un event :

```js
select(value) {
  this.$dispatch('dropdown:select', { value });
  this.close();
}
```

Dans l’app :

```html
<div @dropdown:select.window="console.log($event.detail.value)">
```

Ce pattern rend tes composants découplés.

---

# 7) Anti-patterns (à éviter explicitement)

## Anti-pattern A — “state énorme”

Un composant n’est pas une application.

Si tu as 25 variables :

* tu dois découper.

## Anti-pattern B — “fonctions inline partout”

Ça :

```html
@click="items = items.filter(...)"
```

C’est illisible.

Préférer :

```js
remove(id) { ... }
```

## Anti-pattern C — “DOM hack”

Si tu manipules trop le DOM :

* tu perds le bénéfice d’Alpine

Utilise :

* `x-ref`
* `$refs`
* `$nextTick`

---

# 8) Checklist standard d’un composant “vendable”

Pour chaque composant livré dans ton pack final, tu dois avoir :

* Nom clair
* API (options)
* Méthodes (actions)
* Événements dispatch (si composant réutilisable)
* Accessibilité minimale :

  * `button` pas `div`
  * focus visible
  * aria si nécessaire
* Exemple d’utilisation complet
* Notes pièges

C’est exactement ce que ton chapitre final “Component Library” va contenir.

---

# 9) Mini exercice (obligatoire)

### Exercice A — Appliquer la convention à Modal

Crée `modal.js` :

* `open()`
* `close()`
* `confirm()`
* `options: { closeOnOutside, closeOnEscape }`

### Exercice B — Tabs propre

Crée `tabs.js` :

* `active`
* `set(tab)`
* `is(tab)`

### Exercice C — Documenter un composant

Écris 10 lignes de doc (README) pour ton dropdown :

* but
* API
* events
* a11y

---

## Résumé de la leçon

* Alpine est simple, mais ça ne dispense pas de discipline
* convention = cohérence + maintenabilité
* un composant = responsabilité unique
* API + options = vendable et réutilisable
* accessibilité par défaut = non négociable

---

### Étape suivante logique

Chapitre 12 — Production Ready
**Leçon 3 — Performance sur gros `x-for` : tri, filtre, `key`, rendu**
On va apprendre à ne pas se tirer une balle dans le pied avec des listes de 5 000 items.
