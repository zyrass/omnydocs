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

## `x-transition` : bases (enter/leave, opacité, translate)

### Objectif de la leçon

À la fin, tu sauras :

* à quoi sert `x-transition`
* comment fonctionnent les transitions Alpine (enter / leave)
* appliquer une transition propre sur :

  * un menu
  * un dropdown
  * une modal
* éviter les pièges classiques :

  * animations qui glitch
  * éléments qui “clignotent”
  * transitions impossibles sur `display: none`
* construire un composant UI qui fait “produit fini”

---

## 1) Pourquoi les transitions comptent vraiment

Une UI sans transitions, c’est fonctionnel… mais souvent “sec”.

Une UI avec transitions bien dosées, c’est :

* plus lisible
* plus agréable
* plus compréhensible (tu vois ce qui apparaît/disparaît)
* plus “premium”

Et surtout : tu n’as pas besoin d’un gros framework pour ça.

---

## 2) Définition simple

`x-transition` permet d’animer l’apparition et la disparition d’un élément quand tu utilises `x-show`.

Donc le duo classique c’est :

* `x-show="open"`
* `x-transition`

---

# 3) Exemple minimal (le plus simple possible)

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <div
    x-show="open"
    x-transition
    style="margin-top:10px; padding:12px; border:1px solid #ddd; border-radius:12px;"
  >
    Hello, je suis animé.
  </div>
</div>
```

### Ce que ça fait

* quand `open` passe à true → animation d’entrée
* quand `open` repasse à false → animation de sortie

---

## 4) Comprendre enter / leave (la mécanique)

Une transition se décompose en 4 étapes :

### Entrée

* `enter` : préparation
* `enter-start` : état de départ
* `enter-end` : état final

### Sortie

* `leave` : préparation
* `leave-start` : état de départ
* `leave-end` : état final

Tu peux les définir en classes (style Tailwind), ou en styles.

En “vanilla”, Alpine te permet aussi une version simple via `x-transition.opacity` etc.

---

# 5) Variante simple : `x-transition.opacity`

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <div
    x-show="open"
    x-transition.opacity
    style="margin-top:10px; padding:12px; border:1px solid #ddd; border-radius:12px;"
  >
    Fade in / fade out
  </div>
</div>
```

Résultat :

* fondu doux
* ultra propre
* pas de complexité

---

## 6) Variante simple : `x-transition.scale`

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <div
    x-show="open"
    x-transition.scale
    style="margin-top:10px; padding:12px; border:1px solid #ddd; border-radius:12px;"
  >
    Petit zoom léger
  </div>
</div>
```

Très utile pour :

* dropdown
* popover
* menu

---

# 7) Exemple “pro” : Dropdown menu animé + fermeture outside

On combine :

* `x-show`
* `x-transition`
* `@click.outside`

```html
<div x-data="{ open: false }" style="position:relative; display:inline-block;">
  <button @click="open = !open">
    Actions
  </button>

  <div
    x-show="open"
    x-transition.opacity.scale
    @click.outside="open = false"
    x-cloak
    style="
      position:absolute;
      top: 44px;
      right: 0;
      width: 220px;
      background:#fff;
      border:1px solid #ddd;
      border-radius:12px;
      padding:10px;
      box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    "
  >
    <button style="width:100%; margin-bottom:6px;" @click="alert('Edit')">Edit</button>
    <button style="width:100%; margin-bottom:6px;" @click="alert('Duplicate')">Duplicate</button>
    <button style="width:100%;" @click="alert('Delete')">Delete</button>
  </div>
</div>
```

### Pourquoi c’est “production-ready”

* transition douce
* fermeture au clic extérieur
* pas de flash grâce à `x-cloak`

---

# 8) Pièges fréquents avec `x-transition`

## Piège A — oublier `x-cloak`

Si tu as une transition sur un élément caché au départ, tu peux avoir un flash avant Alpine init.

Solution :

* `x-cloak`
* et CSS :

```css
[x-cloak] { display: none !important; }
```

---

## Piège B — utiliser `x-if` au lieu de `x-show` (sans comprendre)

`x-transition` marche naturellement avec `x-show`.

Avec `x-if`, c’est plus délicat car l’élément est créé/détruit.
Tu peux le faire, mais ce n’est pas la voie “simple”.

Règle débutant :

> transitions = `x-show`

---

## Piège C — transitions trop longues

Une transition trop lente donne une impression de lag.

Bon repère :

* rapide
* discret
* 150ms à 250ms environ

Tu n’es pas en train de faire une cinématique Netflix.

---

## Piège D — enchaîner 5 transitions dans tous les sens

Trop d’animations tue l’UX.
Tu veux une UI calme, lisible.

---

# 9) Exemple “pro” : panneau latéral (slide)

Ici on simule un panneau qui arrive de la droite.

```html
<div x-data="{ open: false }">
  <button @click="open = true">Ouvrir panneau</button>

  <div
    x-show="open"
    x-cloak
    style="position:fixed; inset:0; background:rgba(0,0,0,0.4);"
    @click.self="open = false"
  >
    <div
      x-show="open"
      x-transition:enter="transition ease-out duration-200"
      x-transition:enter-start="opacity-0 translate-x-4"
      x-transition:enter-end="opacity-100 translate-x-0"
      x-transition:leave="transition ease-in duration-150"
      x-transition:leave-start="opacity-100 translate-x-0"
      x-transition:leave-end="opacity-0 translate-x-4"
      style="
        position:absolute;
        right: 0;
        top: 0;
        height: 100%;
        width: 320px;
        background:#fff;
        padding:16px;
      "
    >
      <h3>Panneau</h3>
      <p style="color:#666;">Ici tu mets ton contenu.</p>
      <button @click="open = false">Fermer</button>
    </div>
  </div>
</div>
```

### Note importante

Les classes `transition ease-out duration-200` etc ressemblent à Tailwind.
Si tu n’as pas Tailwind, tu peux le faire en CSS classique.

Dans la suite de la formation (Bloc 2), on bascule sur Vite + Tailwind donc ça devient naturel.

---

## 10) Mini exercice (obligatoire)

### Exercice A — Dropdown animé

* bouton “Menu”
* menu en dessous
* `x-transition.opacity.scale`
* fermeture outside

### Exercice B — Panneau slide

* bouton “Ouvrir”
* overlay
* panneau qui glisse

### Exercice C — Timing

Teste 100ms, 200ms, 500ms
Observe quand ça devient “lent”.

---

## Résumé de la leçon

* `x-transition` rend l’UI plus claire et agréable
* fonctionne parfaitement avec `x-show`
* patterns pro :

  * dropdown
  * panneau
  * modal
* pièges :

  * flash sans `x-cloak`
  * trop long
  * trop d’animations

---

### Étape suivante logique

**Leçon 2 — Transition sur listes : ajout/suppression, timing**
Là on va faire un truc qui fait très “app moderne” : animer une liste qui change sans glitch.
