---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 6

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `x-init` : initialiser un composant proprement (sans faire du sale)

### Objectif de la leçon

À la fin, tu sauras :

* ce que fait `x-init` et à quel moment il s’exécute
* quand l’utiliser (et quand l’éviter)
* initialiser un state proprement
* lancer une logique d’initialisation (préparation UI, chargement local, timers)
* éviter les pièges : double init, logique lourde, effets secondaires

`x-init` est très utile… mais si tu l’utilises mal, tu peux rendre ton composant instable.

---

## 1) `x-init` : définition simple

`x-init` permet d’exécuter du code **au moment où Alpine initialise le composant**.

En clair :

> “Quand Alpine démarre ce composant, exécute cette instruction.”

Exemple :

```html
<div x-data="{ count: 0 }" x-init="count = 10">
  <p x-text="count"></p>
</div>
```

Au chargement, `count` passe automatiquement à 10.

---

## 2) Quand `x-init` est utile (cas réels)

Tu utilises `x-init` quand tu dois faire une action au démarrage du composant.

Cas typiques :

* définir une valeur initiale selon un contexte
* déclencher une logique de préparation UI
* restaurer une donnée depuis localStorage
* focus automatique sur un champ
* lancer un timer (rare, mais possible)
* lancer un fetch (avec prudence)

Le principe pro :

> `x-init` sert à “préparer” ton composant, pas à le transformer en application complète.

---

## 3) Exemple #1 : initialiser un état selon une condition

```html
<div x-data="{ open: false }" x-init="open = true">
  <p x-show="open">Je suis ouvert au démarrage</p>
</div>
```

C’est simple, mais tu vois le concept.

---

## 4) Exemple #2 : initialisation propre avec une fonction

Si ton init devient un peu plus complexe, tu ne dois pas écrire une usine à gaz dans l’attribut.

Mauvais exemple :

```html
<div x-data="{ count: 0 }" x-init="count = 10; console.log(count); if(count > 5){...}">
```

Ça devient illisible.

Bonne pratique : créer une méthode `init()`.

```html
<div x-data="{
  count: 0,

  init() {
    this.count = 10;
    console.log('Composant initialisé, count =', this.count);
  }
}" x-init="init()">
  <p x-text="count"></p>
</div>
```

### Pourquoi c’est mieux ?

* ton HTML reste lisible
* ta logique est regroupée
* tu peux maintenir facilement

---

## 5) Exemple #3 : restaurer une valeur depuis localStorage (préparation à la persistance)

Même si la persistance complète est au Chapitre 10, tu peux déjà comprendre le principe.

```html
<div x-data="{
  name: '',

  init() {
    const saved = localStorage.getItem('name');
    if (saved) {
      this.name = saved;
    }
  },

  save() {
    localStorage.setItem('name', this.name);
  }
}" x-init="init()">
  <input type="text" x-model="name" placeholder="Ton prénom" />

  <button @click="save()">Sauvegarder</button>

  <p>Bonjour <strong x-text="name"></strong></p>
</div>
```

Ici, `x-init` sert à :

* lire une valeur au démarrage
* restaurer l’état du composant

C’est un cas réel, très fréquent.

---

## 6) Exemple #4 : préparer l’UX (focus automatique)

Tu veux que l’utilisateur puisse taper direct.

```html
<div x-data="{ }" x-init="$refs.input.focus()">
  <input x-ref="input" type="text" placeholder="Tape ici..." />
</div>
```

Tu vois ici un point important :
`x-init` peut interagir avec le DOM via `$refs`.

On détaillera `$refs` au Chapitre 6, mais tu comprends déjà l’intérêt.

---

## 7) Le danger : ce qu’il ne faut pas faire avec `x-init`

### Erreur 1 — Mettre une logique lourde dans `x-init`

Si tu fais des trucs énormes dans `x-init`, tu peux :

* ralentir l’affichage
* créer des bugs de timing
* rendre le composant difficile à debug

Règle pro :

> `x-init` doit rester léger.

---

### Erreur 2 — Déclencher des effets secondaires incontrôlés

Effet secondaire = action qui impacte autre chose que ton composant.

Exemples :

* modifier le DOM global sans contrôle
* lancer des appels réseau multiples
* écrire dans localStorage sans raison
* déclencher des événements globaux

Ça peut casser l’application.

---

### Erreur 3 — Croire que `x-init` remplace une architecture

Non.

`x-init` n’est pas un système de lifecycle complet comme Angular.

C’est un hook simple : “au démarrage”.

---

## 8) `x-init` et ordre d’exécution (point important)

Quand Alpine initialise un composant :

1. il lit `x-data`
2. il crée l’état
3. il exécute `x-init`
4. il applique le rendu (`x-text`, `x-show`, etc.)

Donc `x-init` est parfait pour :

* ajuster l’état juste avant le rendu final

---

## 9) Exemple pro : init + log de debug (bonne pratique dev)

Quand tu développes un composant complexe, tu peux temporairement faire :

```html
<div x-data="{
  open: false,

  init() {
    console.log('Init menu, open =', this.open);
  }
}" x-init="init()">
  <button @click="open = !open">Toggle</button>
</div>
```

Puis tu enlèves le log une fois stable.

---

## 10) Résumé de la leçon

* `x-init` exécute du code au démarrage du composant
* utile pour initialiser un état, restaurer des données, préparer l’UX
* bonne pratique : appeler une méthode `init()` plutôt que mettre 20 instructions inline
* éviter les logiques lourdes et effets secondaires incontrôlés

---

## Mini exercice (rapide)

1. Crée un composant avec :

   * `count: 0`
   * `init()` qui met `count` à 5
2. Affiche `count` avec `x-text`
3. Ajoute un bouton “+1”
4. Bonus : sauvegarde `count` dans localStorage et restaure-le dans `init()`

---

Prochaine leçon : **Leçon 7 — Mini-pattern “state + UI” (toggle, compteur, panneau repliable)**
Là on va faire une leçon très pratique : tu vas apprendre les 3 patterns qui reviennent partout dans les UI modernes, et qui te servent ensuite dans les ateliers (menu responsive, todo, modals, tabs…).
