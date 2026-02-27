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

## `x-if` vs `x-show` : choix stratégique (DOM, perf, accessibilité)

### Objectif de la leçon

À la fin, tu sauras :

* ce que font exactement `x-if` et `x-show`
* pourquoi ce n’est pas “la même chose”
* quand utiliser l’un plutôt que l’autre
* les impacts concrets sur :

  * le DOM
  * la performance
  * l’accessibilité
  * les transitions
* éviter les bugs invisibles (ceux qui te ruinent une UI sans que tu comprennes)

Cette leçon est ultra importante parce que le rendu conditionnel, c’est le cœur de toutes les interfaces modernes.

---

## 1) Définition simple

### `x-show`

`x-show` affiche ou masque un élément **sans le retirer du DOM**.

Techniquement, Alpine applique un style `display: none;` quand c’est false.

Exemple :

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <p x-show="open">
    Je suis caché/affiché mais je reste dans le DOM.
  </p>
</div>
```

---

### `x-if`

`x-if` ajoute ou retire l’élément **du DOM**.

Mais attention :

> `x-if` doit obligatoirement être utilisé sur un `<template>`.

Exemple :

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <template x-if="open">
    <p>Je suis créé/détruit dans le DOM.</p>
  </template>
</div>
```

---

## 2) Analogie simple (pour bien comprendre)

### `x-show`

C’est comme une porte avec un rideau.

* tu peux ouvrir/fermer le rideau
* mais la pièce existe toujours

### `x-if`

C’est comme une pièce qui apparaît/disparaît.

* quand c’est fermé → la pièce n’existe même pas
* quand c’est ouvert → la pièce est construite

---

## 3) Différence concrète : DOM

### Avec `x-show`

L’élément est là, mais caché.

Conséquence :

* les listeners existent déjà
* les inputs gardent leur valeur
* le composant reste “vivant”

### Avec `x-if`

L’élément est détruit puis recréé.

Conséquence :

* état interne perdu (si tu n’as pas persisté)
* input reset automatiquement
* events réinitialisés
* c’est plus “propre” mais plus coûteux

---

# 4) Exemple réel : champ de formulaire conditionnel

## Version `x-show` (le champ garde sa valeur)

```html
<div x-data="{ enabled: false, note: '' }">
  <label style="display:block;">
    <input type="checkbox" x-model="enabled" />
    Activer la note
  </label>

  <div x-show="enabled" style="margin-top: 8px;">
    <input type="text" x-model="note" placeholder="Tape une note..." />
  </div>

  <p style="margin-top: 8px;">
    Valeur note : <strong x-text="note"></strong>
  </p>
</div>
```

Tu coches → tu tapes → tu décoches → tu recoches → la valeur est encore là.

C’est logique : l’input n’a jamais été détruit.

---

## Version `x-if` (le champ est recréé, donc reset)

```html
<div x-data="{ enabled: false, note: '' }">
  <label style="display:block;">
    <input type="checkbox" x-model="enabled" />
    Activer la note
  </label>

  <template x-if="enabled">
    <div style="margin-top: 8px;">
      <input type="text" x-model="note" placeholder="Tape une note..." />
    </div>
  </template>

  <p style="margin-top: 8px;">
    Valeur note : <strong x-text="note"></strong>
  </p>
</div>
```

Ici, selon comment tu gères ton state, tu peux avoir un reset perçu.

---

# 5) Performance : lequel est le plus “rapide” ?

Réponse courte :

* `x-show` est souvent plus rapide pour du toggle fréquent
* `x-if` est plus propre pour du contenu lourd affiché rarement

### Pourquoi ?

* `x-show` = juste un style CSS qui change
* `x-if` = création / destruction DOM (plus lourd)

---

# 6) Accessibilité : le point que les gens oublient

### `x-show`

Quand c’est caché (display none), l’élément n’est pas visible et n’est pas focusable.

Donc c’est OK dans la plupart des cas.

Mais attention :

* si tu caches une zone importante, il faut que l’utilisateur comprenne ce qui se passe
* et surtout, ton UI ne doit pas “piéger” le focus

### `x-if`

Comme l’élément est retiré du DOM, il ne peut pas être focusable.

C’est souvent plus “safe” pour éviter des éléments invisibles mais présents.

---

# 7) Transitions : qui marche mieux ?

### `x-show` + `x-transition`

C’est le combo le plus classique.

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <div x-show="open" x-transition style="margin-top: 8px;">
    Bloc animé
  </div>
</div>
```

`x-show` est parfait pour faire des animations d’apparition/disparition.

### `x-if`

Tu peux aussi, mais c’est plus délicat car l’élément est créé/détruit.
Souvent on préfère `x-show` pour les transitions UI.

---

# 8) Quand utiliser quoi ? (règle pro)

## Utilise `x-show` si :

* tu fais un toggle fréquent (menu, panneau, dropdown)
* tu veux garder l’état interne (input, scroll, etc.)
* tu veux des transitions simples

## Utilise `x-if` si :

* le bloc est lourd (beaucoup d’éléments)
* tu veux libérer le DOM quand c’est fermé
* tu veux reset automatiquement un contenu
* tu veux éviter que du code tourne “en arrière-plan”

---

## 9) Erreurs fréquentes (et comment les éviter)

### Erreur 1 — utiliser `x-if` sans `<template>`

C’est interdit.

Toujours :

```html
<template x-if="condition">
  ...
</template>
```

### Erreur 2 — utiliser `x-if` partout “par habitude”

Mauvais réflexe.

Si tu fais un menu qui s’ouvre 50 fois, `x-if` peut être plus coûteux.

### Erreur 3 — perdre l’état d’un input

Tu utilises `x-if` sur un formulaire et tu te demandes pourquoi ça reset.

C’est normal : le DOM est détruit.

---

## 10) Mini exercice (obligatoire)

### Exercice A — Comparaison

* fais un toggle
* affiche un input avec `x-show`
* affiche le même input avec `x-if`
* observe la différence de comportement

### Exercice B — Modal

* version 1 : modal en `x-show` + `x-transition`
* version 2 : modal en `x-if` (template)
* note laquelle te semble plus naturelle

---

## Résumé de la leçon

* `x-show` cache/affiche sans détruire → rapide, transitions faciles
* `x-if` crée/détruit → plus propre, reset naturel, plus lourd
* le bon choix dépend de l’usage (fréquence, état, poids DOM)

---

Prochaine leçon : **Leçon 2 — `x-for` : afficher des listes (syntaxe, arrays, objets)**
Là on passe au niveau “app” : générer de l’UI à partir de données.
