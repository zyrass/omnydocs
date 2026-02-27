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

## `x-data` : créer un composant Alpine (toutes les variantes, proprement)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait exactement `x-data` et pourquoi c’est la base d’Alpine
* définir un composant Alpine avec **un objet inline**
* définir un composant Alpine avec **des fonctions inline**
* créer un composant “pro” **déclaré dans un fichier JavaScript** (mode Vite)
* comprendre le **scope** (périmètre), les erreurs typiques, et les bonnes pratiques

---

## 1) `x-data` : la définition simple (sans blabla)

`x-data` transforme un élément HTML en **composant Alpine**.

Un composant Alpine, c’est :

* un **état** (state) : des données (variables)
* des **actions** : des fonctions qui modifient ces données
* un **périmètre** : tout ce qui est à l’intérieur de l’élément peut utiliser cet état

Tu peux le voir comme une “mini application” locale.

### Analogie simple

`x-data` c’est comme créer un petit cerveau pour un morceau de ta page.

Tout ce qui est dans ce cerveau (variables + fonctions) est accessible aux éléments HTML à l’intérieur.

---

## 2) Variante A — `x-data` avec un objet inline (le plus simple)

### Exemple : compteur minimal

```html
<div x-data="{ count: 0 }">
  <p>Compteur : <span x-text="count"></span></p>
  <button @click="count++">+1</button>
</div>
```

### Ce que ça veut dire

* `count: 0` est une variable dans l’état du composant
* `@click="count++"` modifie l’état
* `x-text="count"` affiche l’état

Cette variante est parfaite pour :

* demos
* prototypes
* composants ultra simples

### Piège courant

Si tu écris :

```html
<button @click="count++">+1</button>
<div x-data="{ count: 0 }"></div>
```

Le bouton est **hors scope**, donc `count` n’existe pas pour lui.

---

## 3) Variante B — `x-data` avec fonctions inline (niveau intermédiaire)

Dès que tu as un peu de logique, tu dois arrêter de faire des expressions partout.

### Exemple : compteur propre (avec méthodes)

```html
<div x-data="{
  count: 0,

  increment() {
    this.count++;
  },

  reset() {
    this.count = 0;
  }
}">
  <p>Compteur : <span x-text="count"></span></p>

  <button @click="increment()">+1</button>
  <button @click="reset()">Reset</button>
</div>
```

### Pourquoi `this.count` ?

Dans Alpine, `this` fait référence au composant courant (l’objet de `x-data`).

Donc `this.count` = “le count de ce composant”.

### Piège courant

Utiliser une arrow function :

```js
increment: () => {
  this.count++;
}
```

Ça peut casser la logique de `this` dans certains contextes, et c’est une mauvaise habitude.

Règle pro : privilégie les méthodes “classiques” :

```js
increment() { ... }
```

---

## 4) Variante C — `x-data` qui appelle une fonction (pattern propre, réutilisable)

Quand tu veux une meilleure lisibilité, tu peux déléguer l’objet à une fonction.

### Exemple : même compteur, plus lisible

```html
<div x-data="counter()">
  <p>Compteur : <span x-text="count"></span></p>

  <button @click="increment()">+1</button>
  <button @click="reset()">Reset</button>
</div>

<script>
  function counter() {
    return {
      count: 0,
      increment() { this.count++; },
      reset() { this.count = 0; }
    };
  }
</script>
```

### Intérêt

* HTML plus clair
* logique regroupée
* plus facile à maintenir

### Limite

Dans une page simple, ok.
Dans un vrai projet, tu veux éviter d’écrire trop de JS dans le HTML, donc on passe à la variante suivante.

---

## 5) Variante D — Composant “pro” dans un fichier JavaScript (mode Vite / projet réel)

Ici on reproduit exactement l’approche professionnelle évoquée dans la partie Vite.

L’idée :

* tu déclares tes composants Alpine dans des fichiers JS
* tu les enregistres via `Alpine.data(...)`
* ton HTML reste propre et lisible

---

### Étape 1 — Créer le composant dans `src/components/counter.js`

```js
// src/components/counter.js
export function counterComponent() {
  return {
    count: 0,

    increment() {
      this.count++;
    },

    decrement() {
      if (this.count > 0) {
        this.count--;
      }
    },

    reset() {
      this.count = 0;
    },
  };
}
```

Ici, tu as :

* un état (`count`)
* des actions (`increment`, `decrement`, `reset`)
* une logique pro (on bloque le compteur sous 0)

---

### Étape 2 — Enregistrer le composant dans `src/main.js`

```js
// src/main.js
import Alpine from "alpinejs";
import { counterComponent } from "./components/counter.js";

window.Alpine = Alpine;

// On déclare un "nom" de composant : counter
Alpine.data("counter", counterComponent);

Alpine.start();
```

### Explication

`Alpine.data("counter", counterComponent)` dit :

> “Quand tu vois `x-data="counter"`, tu utilises l’objet retourné par `counterComponent()`.”

C’est une déclaration propre, maintenable, testable.

---

### Étape 3 — Utiliser le composant dans le HTML

```html
<div x-data="counter">
  <p>Compteur : <span x-text="count"></span></p>

  <button @click="decrement()">-1</button>
  <button @click="increment()">+1</button>
  <button @click="reset()">Reset</button>
</div>
```

Ton HTML est maintenant :

* lisible
* concentré sur l’UI
* sans logique lourde

---

## 6) Comprendre le scope (périmètre) avec un exemple réel

### Exemple : deux compteurs séparés

```html
<div class="row">
  <div x-data="{ count: 0 }">
    <button @click="count++">A +1</button>
    <span x-text="count"></span>
  </div>

  <div x-data="{ count: 0 }">
    <button @click="count++">B +1</button>
    <span x-text="count"></span>
  </div>
</div>
```

Chaque bloc a son propre `count`.

Donc :

* A ne modifie pas B
* B ne modifie pas A

C’est normal : chaque composant est isolé.

---

## 7) Erreurs fréquentes (et diagnostic rapide)

### Erreur 1 — “count is not defined”

Causes :

* variable hors scope
* faute de frappe
* `x-data` pas chargé (Alpine pas démarré)

Réflexe :

* console navigateur
* vérifier `x-data` parent
* vérifier script Alpine / `Alpine.start()`

---

### Erreur 2 — “ça marche mais c’est illisible”

Cause :

* logique dans `@click` trop longue

Solution :

* créer une méthode dans `x-data`
* ou externaliser le composant dans un fichier JS

---

### Erreur 3 — mauvaise gestion de `this`

Cause :

* fonctions fléchées utilisées comme méthodes

Solution :

* méthodes classiques `increment() { ... }`

---

## 8) Bonnes pratiques pro (règles simples)

### Règle 1 — Inline uniquement si c’est trivial

Si c’est plus de 2-3 lignes, tu sors la logique.

### Règle 2 — Un composant = une responsabilité

Exemple :

* un composant “menu”
* un composant “modal”
* un composant “tabs”

Pas un composant “menu+modal+search+toast” dans le même `x-data`.

### Règle 3 — Nommage cohérent

* `x-data="menu"`
* `x-data="modal"`
* `x-data="counter"`

Et côté fichiers :

* `menu.js`
* `modal.js`
* `counter.js`

---

## 9) Mini exercice (obligatoire si tu veux progresser vite)

### Exercice A — Variante inline

1. Crée un composant `x-data` inline avec :

   * `open: false`
   * `toggle()`
2. Affiche “Ouvert / Fermé” avec `x-text`
3. Ajoute un bouton qui appelle `toggle()`

### Exercice B — Variante fichier JS (style Vite)

1. Crée `src/components/toggle.js` :

```js
export function toggleComponent() {
  return {
    open: false,
    toggle() {
      this.open = !this.open;
    },
  };
}
```

2. Déclare le composant dans `src/main.js` :

```js
import { toggleComponent } from "./components/toggle.js";
Alpine.data("toggle", toggleComponent);
```

3. Utilise-le :

```html
<div x-data="toggle">
  <button @click="toggle()">Toggle</button>
  <span x-text="open ? 'Ouvert' : 'Fermé'"></span>
</div>
```

---

## Résumé de la leçon

Tu connais maintenant les 4 variantes importantes :

1. `x-data="{...}"` simple
2. `x-data="{..., method(){...}}"` avec méthodes
3. `x-data="factory()"` via fonction
4. `Alpine.data("name", factory)` dans un fichier JS (pro / Vite)

Et tu comprends le point crucial : **le scope**.

---

Prochaine leçon : **Leçon 2 — `x-text` : afficher du texte proprement**
On va expliquer pourquoi Alpine évite l’interpolation “hasardeuse”, comment afficher des données sans glitch, et comment structurer un affichage propre (et accessible).
