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

## `x-effect` : réaction automatique (quand l’utiliser, quand éviter)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait `x-effect` exactement
* comment Alpine détecte les dépendances (ce qui déclenche l’effet)
* quand `x-effect` est un excellent outil
* quand c’est une mauvaise idée (boucles, effets cachés, complexité)
* comment structurer un effet proprement, avec un exemple concret

---

## 1) Définition simple

`x-effect` exécute automatiquement une expression **à chaque fois qu’une donnée utilisée dans cette expression change**.

C’est de la “réactivité”.

### Traduction en langage humain

Tu écris :
“Si cette donnée change, je veux refaire ça.”

---

## 2) Analogie simple

Imagine un tableau blanc dans une salle de classe :

* dès que tu changes un chiffre dans la formule
* le résultat sur le tableau se met à jour automatiquement

`x-effect`, c’est ce mécanisme “mise à jour auto”.

---

## 3) Exemple minimal (pour comprendre)

```html
<div x-data="{ count: 0 }">
  <button @click="count++">+1</button>
  <p x-text="count"></p>

  <p x-effect="console.log('count a changé :', count)"></p>
</div>
```

Ici :

* Alpine voit que l’expression utilise `count`
* donc à chaque changement de `count`, l’effet se relance

---

# 4) À quoi sert `x-effect` en vrai projet ?

## Cas réel A — synchroniser une UI avec un side effect

Exemple : changer le titre de la page selon l’état.

```html
<div x-data="{ query: '' }">
  <input x-model="query" placeholder="Recherche..." />

  <p x-effect="document.title = query ? `Recherche: ${query}` : 'Blog mock'"></p>
</div>
```

Résultat :

* tu tapes
* le titre change automatiquement

---

## Cas réel B — recalculer quelque chose de “non trivial” (avec prudence)

Exemple : log, métrique, trace debug, tracking (dans un environnement contrôlé).

---

# 5) Différence avec un getter (très important)

### Getter

Un getter sert à **calculer une valeur** à afficher.

Il doit être “pur” :

* pas de modification du monde extérieur
* pas de side effects

### `x-effect`

`x-effect` sert plutôt à faire un **side effect** (effet de bord) :

* modifier un élément DOM externe
* déclencher un log
* synchroniser quelque chose

Règle pro :

> Calcul = getter. Effet de bord = x-effect.

---

# 6) Pièges dangereux avec `x-effect`

## Danger 1 — créer une boucle infinie

Si ton `x-effect` modifie une donnée qui déclenche le `x-effect`, tu peux créer une boucle.

Exemple (mauvais) :

```html
<div x-data="{ count: 0 }">
  <p x-effect="count++"></p>
</div>
```

Pourquoi c’est un problème ?

* `count` change
* l’effet se relance
* `count` change encore
* etc.

Résultat : ça part en boucle.

---

## Danger 2 — mettre trop de logique dans un effet

Si ton effet fait 10 choses :

* tu perds la lisibilité
* tu crées des dépendances implicites
* tu rends le debug plus compliqué

Un effet doit être :

* court
* explicite
* justifié

---

## Danger 3 — effet déclenché trop souvent

Si tu utilises `x-effect` sur une donnée qui change en continu (ex: scroll), tu peux plomber les performances.

Pour scroll :

* throttle
* ou plugin Intersect (plus tard)

---

# 7) Exemple “pro” : focus automatique sur un champ quand une modal s’ouvre

Objectif :

* quand `open` devient true
* on focus un input

### Code

```html
<div x-data="{ open: false }" style="max-width: 520px;">
  <button @click="open = true">Ouvrir</button>

  <div
    x-show="open"
    x-cloak
    style="margin-top: 10px; border: 1px solid #ddd; padding: 12px; border-radius: 12px;"
  >
    <h3>Recherche</h3>
    <input type="text" x-ref="search" placeholder="Tape ici..." style="width:100%; padding:10px; border:1px solid #ddd; border-radius:10px;" />

    <div style="margin-top: 10px;">
      <button @click="open = false">Fermer</button>
    </div>
  </div>

  <!-- Effet -->
  <div x-effect="
    if (open) {
      $refs.search.focus();
    }
  "></div>
</div>
```

### Ce que tu dois comprendre

* l’effet dépend de `open`
* quand `open` passe à true → focus

Ce pattern est valide parce que :

* l’effet est court
* il a un but UX clair
* il n’entraîne pas de boucle

---

## 8) Résumé de la leçon

* `x-effect` relance une expression dès que ses dépendances changent
* c’est utile pour des effets de bord (focus, title, sync externe)
* éviter :

  * boucle infinie
  * logique trop lourde
  * effets inutiles
* règle pro : getter pour calcul, `x-effect` pour side effects

---

## Mini exercice (obligatoire)

### Exercice A — Document title

* input `query`
* `x-effect` met à jour `document.title`

### Exercice B — Auto-focus

* toggle `open`
* focus automatique sur input quand open = true

### Exercice C — Anti-boucle

* tente un `x-effect="count++"` et observe
* explique pourquoi c’est dangereux

---

### Étape suivante logique

**Leçon 2 — `$watch` : observer une variable (filtre/recherche/persist)**
`$watch` est souvent préférable à `x-effect` quand tu veux réagir proprement à une seule variable, avec une fonction claire.
