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

## `x-bind` (alias `:`) : rendre les attributs dynamiques (classes, disabled, aria, data-*)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `x-bind` (et sa version courte `:`)
* rendre dynamiques des attributs HTML (class, disabled, value, aria-*, data-*)
* éviter les erreurs classiques (mauvais types, concat illisible, UI incohérente)
* appliquer `x-bind` sur des cas réels : boutons, états, accessibilité

`x-bind`, c’est ce qui te permet de faire une UI “vivante” sans bricolage.

---

## 1) `x-bind` : définition simple

`x-bind` sert à lier un attribut HTML à une expression JavaScript.

Exemple :

```html
<div x-data="{ isDisabled: true }">
  <button x-bind:disabled="isDisabled">
    Valider
  </button>
</div>
```

Ici, si `isDisabled = true`, le bouton est désactivé.

---

## 2) Version courte : `:` (le standard pro)

Alpine te permet d’écrire :

```html
<button :disabled="isDisabled">Valider</button>
```

C’est exactement la même chose, juste plus court.

Dans la pratique, tu verras presque toujours `:` plutôt que `x-bind:`.

---

## 3) Pourquoi `x-bind` est essentiel en UI

Sans `x-bind`, tu es obligé de :

* dupliquer du HTML
* mettre des conditions partout
* faire du JS manuel qui modifie le DOM

Avec `x-bind`, tu relies directement :

* l’état (`state`)
* aux attributs HTML

Donc l’UI reflète toujours la réalité du state.

---

# Cas 1 — `:class` (le plus utilisé)

## 4) `:class` simple : activer une classe selon un état

```html
<div x-data="{ active: false }">
  <button
    class="btn"
    :class="active ? 'active' : ''"
    @click="active = !active"
  >
    Toggle
  </button>
</div>

<style>
  .btn {
    border: 1px solid #ddd;
    padding: 8px 12px;
    border-radius: 8px;
  }
  .active {
    border-color: #111;
    font-weight: bold;
  }
</style>
```

Quand `active = true`, la classe `active` s’ajoute.

---

## 5) `:class` version pro : objet de classes

Quand tu veux gérer plusieurs classes, fais propre.

```html
<div x-data="{ isOpen: false, isDanger: false }">
  <button
    class="btn"
    :class="{
      'btn-open': isOpen,
      'btn-danger': isDanger
    }"
    @click="isOpen = !isOpen"
  >
    Bouton dynamique
  </button>
</div>

<style>
  .btn-open { border-color: green; }
  .btn-danger { border-color: red; }
</style>
```

### Pourquoi c’est mieux ?

Parce que tu lis ça comme une règle :

* si `isOpen` → classe `btn-open`
* si `isDanger` → classe `btn-danger`

Lisible, maintenable, pro.

---

# Cas 2 — `:disabled` (UX et validation)

## 6) Exemple : désactiver un bouton si input vide

```html
<div x-data="{ name: '' }">
  <input type="text" x-model="name" placeholder="Ton prénom" />

  <button :disabled="name.trim().length === 0">
    Envoyer
  </button>
</div>
```

Ici, tant que l’utilisateur n’a pas saisi de prénom, le bouton reste désactivé.

### Piège classique

Oublier `.trim()`.

Sans trim, `"   "` compte comme une valeur, alors que c’est vide.

---

# Cas 3 — `:aria-*` (accessibilité sérieuse)

## 7) Exemple : menu avec `aria-expanded`

```html
<div x-data="{ open: false }">
  <button
    @click="open = !open"
    :aria-expanded="open.toString()"
  >
    Menu
  </button>

  <nav x-show="open" x-cloak>
    ...
  </nav>
</div>
```

### Pourquoi `.toString()` ?

Parce que certains attributs ARIA attendent des chaînes `"true"` / `"false"`.

Si tu mets un booléen directement, ça marche souvent… mais c’est moins propre.

En UI pro, on est strict.

---

# Cas 4 — `:data-*` (data attributes)

Les `data-*` sont très utiles pour :

* tests automatisés
* tracking analytics
* debug UI

Exemple :

```html
<div x-data="{ status: 'draft' }">
  <span :data-status="status" x-text="status"></span>
</div>
```

Tu peux ensuite inspecter ton HTML et voir :

```html
<span data-status="draft">draft</span>
```

---

# Cas 5 — `:style` (à utiliser avec discipline)

Tu peux aussi binder du style inline :

```html
<div x-data="{ progress: 30 }">
  <div style="border: 1px solid #ddd; width: 300px;">
    <div
      :style="`width: ${progress}%`"
      style="height: 10px; background: black;"
    ></div>
  </div>

  <button @click="progress = Math.min(progress + 10, 100)">+10%</button>
</div>
```

### Bonne pratique

`style` inline est OK pour une démo.

Mais en production, tu préfères :

* classes CSS
* ou Tailwind plus tard

---

## 8) Les pièges classiques avec `x-bind`

### Piège 1 — concat illisible

Évite :

```html
:class="isOpen ? 'a b c' : 'd e f'"
```

Tu vas te perdre.

Préférence pro : objet de classes.

---

### Piège 2 — attributs incohérents

Exemple :

* bouton disabled mais visuellement actif
* menu fermé mais aria-expanded reste true

Solution :

> 1 état = 1 vérité

Ton state pilote tout : classes, disabled, aria.

---

### Piège 3 — sur-utiliser `:style`

Si tu mets tout en `:style`, tu vas créer une UI impossible à maintenir.

---

## 9) Mini exemple complet (pro, réaliste)

Objectif : un bouton de validation avec UX propre.

```html
<div x-data="{ email: '' }">
  <label>
    Email
    <input type="email" x-model="email" placeholder="test@mail.com" />
  </label>

  <button
    :disabled="email.trim().length === 0"
    :class="{
      'btn-disabled': email.trim().length === 0,
      'btn-ready': email.trim().length > 0
    }"
  >
    Valider
  </button>
</div>

<style>
  .btn-disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .btn-ready {
    font-weight: bold;
  }
</style>
```

---

## Résumé de la leçon

* `x-bind` lie un attribut HTML à ton state
* `:` est le raccourci standard
* `:class` est central pour le design dynamique
* `:disabled` améliore l’UX
* `:aria-*` rend ton UI accessible
* `:data-*` est utile pour tests/debug
* le state doit être la seule source de vérité

---

## Mini exercice (obligatoire)

1. Crée un composant avec :

   * `isValid: false`
2. Fais un bouton qui :

   * est disabled si `isValid = false`
   * a une classe “valid” si `isValid = true`
3. Ajoute un checkbox “Valider”

   * quand on coche → `isValid = true`
4. Bonus :

   * ajoute `aria-disabled`

---

Prochaine leçon : **Leçon 2 — `x-on` (alias `@`) : écouter des événements (click, input, change, submit)**
On va rentrer dans le cœur des interactions : gérer des actions propres, et éviter le code spaghetti dans le HTML.
