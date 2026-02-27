---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 8

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Installation en Vanilla JavaScript (CDN) + premier vrai composant Alpine

### Objectif de la leçon

À la fin de cette leçon, tu vas :

* installer Alpine.js **en 30 secondes** via CDN
* créer ton premier **Playground Alpine**
* comprendre exactement **ce qui se passe**
* apprendre les **pièges classiques** (et comment les éviter)

Ici on ne parle plus, on fait.

---

## 1) C’est quoi une installation “CDN” ?

CDN = Content Delivery Network.
C’est un réseau de serveurs qui te fournit un fichier rapidement.

Quand tu utilises un CDN, tu dis simplement au navigateur :

> “Télécharge Alpine.js depuis internet, et exécute-le dans ma page.”

Avantages :

* zéro configuration
* parfait pour apprendre
* parfait pour prototyper
* idéal pour tester des composants

Inconvénients (on le verra plus tard) :

* dépendance au réseau
* moins adapté à un projet “production moderne” avec build

Mais pour commencer une formation sérieuse, c’est exactement ce qu’on veut.

---

## 2) Création du Playground Alpine (base de travail)

Tu vas créer un fichier :

* `index.html`

Et dedans tu vas mettre une structure propre et professionnelle.

### Code complet (Playground de base)

Copie-colle ce fichier exactement :

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>Alpine.js Playground</title>

    <!-- Alpine.js (CDN) -->
    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      body {
        font-family: Arial, sans-serif;
        padding: 16px;
        line-height: 1.4;
      }

      .card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        max-width: 520px;
      }

      button {
        padding: 8px 12px;
        cursor: pointer;
      }

      .row {
        display: flex;
        gap: 8px;
        align-items: center;
      }
    </style>
  </head>

  <body>
    <h1>Alpine.js Playground</h1>

    <div class="card" x-data="{ count: 0 }">
      <p>
        Compteur :
        <strong x-text="count"></strong>
      </p>

      <div class="row">
        <button @click="count++">+1</button>
        <button @click="count = 0">Reset</button>
      </div>
    </div>
  </body>
</html>
```

---

## 3) Explication pédagogique : pourquoi ça marche ?

On va décortiquer les points importants.

### 3.1 `defer` (très important)

Tu vois :

```html
<script defer src="https://unpkg.com/alpinejs"></script>
```

`defer` signifie :

* le navigateur télécharge Alpine pendant qu’il lit le HTML
* mais il exécute Alpine **après** avoir fini de lire le HTML

Sans ça, tu peux avoir des comportements instables.

C’est une bonne habitude.

---

### 3.2 `x-data` = le début du composant

Tu vois :

```html
<div x-data="{ count: 0 }">
```

Ça veut dire :

* “Cette zone devient un composant Alpine”
* “Elle a un état interne”
* “Cet état contient `count` qui vaut 0 au départ”

C’est le cœur d’Alpine.

---

### 3.3 `x-text` = affichage dynamique

Tu vois :

```html
<strong x-text="count"></strong>
```

Alpine va mettre la valeur de `count` dans cet élément.

---

### 3.4 `@click` = événement

Tu vois :

```html
<button @click="count++">+1</button>
```

Au clic, Alpine exécute `count++`
Donc `count` augmente, et l’UI se met à jour.

---

## 4) Ton premier “vrai composant” : toggle panel

Maintenant on va ajouter un second composant, un peu plus réaliste.

### Objectif

Créer un panneau qu’on peut ouvrir/fermer.

Ajoute ça sous ton compteur :

```html
<hr style="margin: 16px 0" />

<div class="card" x-data="{ open: false }">
  <div class="row">
    <button @click="open = !open">
      Toggle
    </button>

    <span x-text="open ? 'Ouvert' : 'Fermé'"></span>
  </div>

  <p x-show="open" style="margin-top: 12px;">
    Ce contenu est visible uniquement quand <strong>open</strong> est à true.
  </p>
</div>
```

---

## 5) Les pièges classiques (et comment les corriger)

### Piège 1 — Alpine ne marche pas du tout

Tu cliques, rien ne se passe.

Check-list rapide :

1. Est-ce que ton script Alpine est bien chargé ?
2. Est-ce que tu as une erreur dans la console ?
3. Est-ce que tu as bien mis `defer` ?
4. Est-ce que tu as bien écrit `x-data` ?

La console est ton juge.

---

### Piège 2 — “open is not defined”

Ça arrive quand tu utilises une variable qui n’existe pas dans le composant.

Exemple :

```html
<div x-data="{ open: false }">
  <button @click="opened = !opened">Toggle</button>
</div>
```

Ici, `opened` n’existe pas.

Solution : être strict sur le nommage.

---

### Piège 3 — “x-show” affiche bizarrement

Rappel :

* `x-show` ne supprime pas l’élément
* il le cache avec du CSS (`display: none`)

Donc si ton layout est étrange, inspecte dans DevTools.

---

### Piège 4 — Tu vois le contenu avant qu’Alpine démarre

C’est le fameux “flash” où l’UI s’affiche 0.2 seconde avant d’être cachée.

Solution : `x-cloak` (on le verra dans Chapitre 2), mais je te le montre déjà.

Exemple :

```html
<p x-show="open" x-cloak>
  Contenu caché proprement dès le chargement.
</p>
```

---

## 6) Mini exercice (important)

### Exercice A — compteur pro

Améliore le compteur :

* ajoute un bouton “-1”
* empêche le compteur d’aller en dessous de 0
* ajoute un message “Bravo” quand `count >= 10`

Indice : tu vas utiliser une condition.

---

### Exercice B — toggle panel

Améliore ton toggle :

* quand tu ouvres le panel, le bouton doit afficher “Fermer”
* quand tu fermes, le bouton affiche “Ouvrir”

Indice : tu vas utiliser un ternaire dans `x-text`.

---

## Résumé de la leçon

Tu sais maintenant :

* installer Alpine via CDN
* créer un Playground propre
* créer des composants avec `x-data`
* afficher avec `x-text`
* écouter des événements avec `@click`
* comprendre les pièges de base

Ce Playground, c’est ton laboratoire officiel pour les chapitres suivants.

---

Prochaine leçon : **Leçon 9 — Installation via ViteJS (projet moderne)**
Là, on passe dans le monde “pro” : structure de projet, build, imports, et base prête pour Tailwind + component library.
