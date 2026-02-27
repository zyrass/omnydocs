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

## `x-ref` et `$refs` : contrôler le DOM proprement (focus, scroll, sélection)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait `x-ref`
* comment utiliser `$refs` sans bricolage
* gérer des besoins UI réels :

  * focus automatique
  * scroll vers un élément
  * sélectionner le texte d’un input
  * déclencher une action sur un élément DOM
* éviter les erreurs classiques : `document.querySelector`, dépendances fragiles, DOM non prêt

Ici on passe d’un Alpine “sympa” à un Alpine “pro”.

---

## 1) Définition simple

### `x-ref`

`x-ref` sert à donner un nom à un élément HTML pour le retrouver facilement.

Exemple :

```html
<input x-ref="email" type="email" />
```

### `$refs`

`$refs` est un objet fourni par Alpine qui contient tous les refs du composant.

Exemple :

```js
$refs.email.focus()
```

---

## 2) Analogie simple

`x-ref` c’est comme mettre une étiquette sur une boîte.

* tu écris “email” dessus
* plus tard tu peux dire : “donne-moi la boîte email”
* sans chercher partout dans la maison

Sans `x-ref`, tu fais :

* `document.querySelector(...)`
* fragile, lent, dépendant de classes/IDs

---

# 3) Exemple #1 — Focus sur un champ (cas réel)

Objectif : quand tu ouvres un formulaire, le curseur est déjà prêt.

```html
<div x-data="{ open: false }">
  <button @click="open = true">Ouvrir formulaire</button>

  <div x-show="open" x-cloak style="margin-top: 10px; border: 1px solid #ddd; padding: 12px; border-radius: 12px;">
    <label style="display:block;">
      Email
      <input x-ref="email" type="email" placeholder="ex: mail@site.com"
        style="width:100%; margin-top:6px; padding:10px; border:1px solid #ddd; border-radius:10px;" />
    </label>

    <div style="margin-top: 10px;">
      <button @click="open = false">Fermer</button>
    </div>
  </div>

  <div x-effect="
    if (open) {
      $refs.email.focus();
    }
  "></div>
</div>
```

### Pourquoi c’est “pro”

* tu améliores l’UX immédiatement
* pas besoin de cliquer dans le champ
* c’est un comportement attendu dans une vraie app

---

## 4) Exemple #2 — Sélectionner le texte automatiquement

Cas réel :

* un champ contient une URL
* tu veux que l’utilisateur puisse copier direct

```html
<div x-data="{ link: 'https://example.com/token/abc123' }">
  <input
    x-ref="link"
    type="text"
    x-model="link"
    style="width:100%; padding:10px; border:1px solid #ddd; border-radius:10px;"
  />

  <button style="margin-top:10px;" @click="
    $refs.link.focus();
    $refs.link.select();
  ">
    Sélectionner le texte
  </button>
</div>
```

### Explication

* `.focus()` met le curseur
* `.select()` sélectionne tout le texte

Très utile dans des outils (DevOps, sécurité, admin).

---

# 5) Exemple #3 — Scroll vers un élément (UI propre)

Cas réel :

* tu ajoutes une todo
* tu veux scroller vers le bas

```html
<div x-data="{
  items: [],
  add() {
    this.items.push('Item ' + (this.items.length + 1));
    // On fera $nextTick dans la leçon suivante pour garantir le DOM
  }
}">
  <button @click="add()">Ajouter</button>

  <div x-ref="list" style="margin-top:10px; height:120px; overflow:auto; border:1px solid #ddd; border-radius:10px; padding:10px;">
    <template x-for="(item, index) in items" :key="index">
      <p x-text="item" style="margin:0 0 6px;"></p>
    </template>
  </div>

  <button style="margin-top:10px;" @click="
    $refs.list.scrollTop = $refs.list.scrollHeight;
  ">
    Scroll en bas
  </button>
</div>
```

Ici on modifie directement une propriété DOM :

* `scrollTop`
* `scrollHeight`

---

## 6) Pièges fréquents avec `x-ref`

### Piège A — `x-ref` n’existe que dans le composant

Tu ne peux pas faire `$refs` depuis un autre composant.

Chaque `x-data` a son scope.

Donc :

* refs = local
* store = global (plus tard)

---

### Piège B — `x-ref` dans un `x-if`

Si l’élément est conditionnel et n’existe pas dans le DOM, `$refs.xxx` sera `undefined`.

Exemple :

* modal fermée
* input n’existe pas
* donc `$refs.email` n’existe pas

Solution :

* ne pas appeler `$refs` quand c’est fermé
* ou utiliser `$nextTick` après ouverture (Leçon 4)

---

### Piège C — mauvais nom de ref

Tu écris `x-ref="Email"` et tu appelles `$refs.email`.

Ça ne match pas.

Règle :

* utilise des noms simples et cohérents : `email`, `search`, `modal`, `list`

---

# 7) Bonnes pratiques (niveau pro)

## Bonne pratique 1 — refs pour DOM, pas pour data

`x-ref` n’est pas fait pour stocker des valeurs.

C’est uniquement pour accéder à un élément DOM.

## Bonne pratique 2 — éviter `querySelector`

En Alpine, `x-ref` est la méthode propre.

Tu ne veux pas de :

```js
document.querySelector('.my-input')
```

Parce que :

* fragile
* dépend de classes
* casse dès que tu refactors

## Bonne pratique 3 — ref + méthode dédiée

Tu peux faire une méthode claire :

```js
focusEmail() {
  this.$refs.email.focus();
}
```

Lisible et réutilisable.

---

## 8) Résumé de la leçon

* `x-ref="name"` crée un repère DOM
* `$refs.name` permet d’accéder à l’élément
* utile pour :

  * focus
  * select
  * scroll
* attention :

  * scope local
  * refs inexistants si `x-if` fermé

---

## Mini exercice (obligatoire)

### Exercice A — Focus automatique

* bouton “Ouvrir”
* input focus automatiquement

### Exercice B — Copy helper

* input avec un texte
* bouton “Sélectionner” qui focus + select

### Exercice C — Scroll list

* liste scrollable
* bouton “Bas” qui scroll en bas

---

### Étape suivante logique

**Leçon 4 — `$nextTick` : attendre le DOM (modals, listes, transitions)**
Parce que parfois tu veux agir sur un ref… mais le DOM n’est pas encore prêt.
