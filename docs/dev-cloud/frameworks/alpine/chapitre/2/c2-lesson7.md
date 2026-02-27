---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 7

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Mini-pattern “State + UI” : toggle, compteur, panneau repliable (les 3 réflexes pro)

### Objectif de la leçon

À la fin, tu sauras construire les 3 patterns Alpine les plus importants :

1. **Toggle** (ouvrir/fermer)
2. **Compteur** (incrémenter/décrémenter)
3. **Panneau repliable** (section dynamique + UX propre)

Ces patterns, tu vas les réutiliser partout :

* menu responsive
* dropdown
* modal
* tabs
* accordéon
* todo list
* notifications
* UI filtrée

C’est une leçon “muscle mémoire” : tu dois être capable de les refaire sans réfléchir.

---

## 1) Le concept : “State + UI”

Dans Alpine, tout repose sur une idée très simple :

* **State** = tes variables (données)
* **UI** = ton HTML (ce que l’utilisateur voit)
* **Binding** = le lien entre les deux (`x-text`, `x-show`, `x-model`, etc.)

Quand le state change, l’UI se met à jour automatiquement.

### Analogie simple

Le state, c’est ton tableau de bord interne.
L’UI, c’est ce que le conducteur voit.

Tu ne modifies pas l’UI directement, tu modifies le state, et Alpine met à jour l’UI.

---

# Pattern 1 — Toggle (le plus utilisé)

## Objectif

Ouvrir / fermer un élément (menu, dropdown, panneau, modal).

### Version minimale

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <p x-show="open">
    Contenu visible si open = true
  </p>
</div>
```

### Ce que tu dois retenir

* `open` est un booléen (`true/false`)
* `open = !open` inverse l’état
* `x-show="open"` affiche/masque

---

## Version pro (avec méthode + lisibilité)

```html
<div x-data="{
  open: false,

  toggle() {
    this.open = !this.open;
  }
}">
  <button @click="toggle()">
    <span x-text="open ? 'Fermer' : 'Ouvrir'"></span>
  </button>

  <p x-show="open" x-cloak>
    Contenu visible uniquement quand c’est ouvert.
  </p>
</div>
```

### Pourquoi c’est mieux ?

* le bouton est clair (“Ouvrir / Fermer”)
* `x-cloak` évite le flash
* la logique est centralisée (`toggle()`)

---

## Pièges à éviter (toggle)

### Piège 1 — utiliser un nom de variable flou

Mauvais :

* `state`
* `toggle`
* `click`

Bon :

* `open`
* `isOpen`
* `menuOpen`

### Piège 2 — oublier `x-cloak`

Sur un menu ou une modal, c’est visible et moche.

---

# Pattern 2 — Compteur (state numérique + actions)

## Objectif

Manipuler une valeur numérique avec des actions.

### Version simple

```html
<div x-data="{ count: 0 }">
  <p>Compteur : <strong x-text="count"></strong></p>

  <button @click="count++">+1</button>
  <button @click="count--">-1</button>
</div>
```

Ça marche, mais ce n’est pas propre.

---

## Version pro (avec garde-fou)

Ici on empêche `count` d’aller en dessous de 0.

```html
<div x-data="{
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
  }
}">
  <p>Compteur : <strong x-text="count"></strong></p>

  <button @click="decrement()">-1</button>
  <button @click="increment()">+1</button>
  <button @click="reset()">Reset</button>
</div>
```

### Pourquoi c’est important ?

Parce que dans un vrai projet, tu ne laisses pas l’utilisateur casser ton state.

Exemple réel :

* quantité panier (ne doit pas être négative)
* stock
* niveau RPG
* pages pagination

---

## Pièges à éviter (compteur)

### Piège 1 — logique dans le HTML

Évite :

```html
<button @click="count = count + 1">+1</button>
```

Ça marche, mais ça se multiplie et devient illisible.

Préférence pro : méthodes.

### Piège 2 — oublier le reset

Une UI pro a souvent un bouton “reset” ou “clear”.

---

# Pattern 3 — Panneau repliable (collapsible panel)

## Objectif

Créer une section qu’on peut ouvrir/fermer proprement.

C’est la base des :

* FAQ
* accordéons
* sections de paramètres
* blocs “plus de détails”

---

## Version simple

```html
<section x-data="{ open: false }">
  <button @click="open = !open">
    Détails
  </button>

  <div x-show="open">
    <p>Voici le contenu du panneau.</p>
  </div>
</section>
```

Correct, mais pas encore “pro”.

---

## Version pro (accessibilité + UX)

```html
<section x-data="{
  open: false,

  toggle() {
    this.open = !this.open;
  }
}">
  <button
    @click="toggle()"
    :aria-expanded="open.toString()"
    aria-controls="panel-details"
  >
    <span x-text="open ? 'Masquer les détails' : 'Afficher les détails'"></span>
  </button>

  <div
    id="panel-details"
    x-show="open"
    x-cloak
    style="margin-top: 8px;"
  >
    <p>
      Ce panneau contient des informations complémentaires.
      Il est visible uniquement si <strong>open</strong> est à true.
    </p>
  </div>
</section>
```

### Pourquoi c’est pro ?

* `aria-expanded` indique l’état (important accessibilité)
* `aria-controls` lie le bouton au panneau
* `x-cloak` évite le flash
* texte dynamique clair

---

## Variante “bonus” : panneau auto-ouvert au démarrage (`x-init`)

```html
<section x-data="{ open: false }" x-init="open = true">
  <button @click="open = !open">Toggle</button>

  <div x-show="open" x-cloak>
    <p>Panneau ouvert au chargement.</p>
  </div>
</section>
```

Utile dans un cas réel :

* afficher une section “Important”
* ouvrir automatiquement une aide utilisateur

---

# 4) Version “projet Vite” : patterns en composants réutilisables

Tu m’as demandé un truc très important : le passage vers le composant JS externe.

Voici un exemple concret.

## Étape 1 — `src/components/collapsible.js`

```js
// src/components/collapsible.js
export function collapsibleComponent(defaultOpen = false) {
  return {
    open: defaultOpen,

    toggle() {
      this.open = !this.open;
    },

    close() {
      this.open = false;
    },

    openPanel() {
      this.open = true;
    },
  };
}
```

## Étape 2 — `src/main.js`

```js
import Alpine from "alpinejs";
import { collapsibleComponent } from "./components/collapsible.js";

window.Alpine = Alpine;

Alpine.data("collapsible", () => collapsibleComponent(false));

Alpine.start();
```

## Étape 3 — HTML

```html
<section x-data="collapsible">
  <button @click="toggle()">
    <span x-text="open ? 'Masquer' : 'Afficher'"></span>
  </button>

  <div x-show="open" x-cloak>
    Contenu du panneau
  </div>
</section>
```

### Pourquoi c’est puissant ?

Parce que tu peux réutiliser `collapsible` dans 15 pages différentes sans recopier du code.

---

# 5) Les erreurs “niveau débutant” à corriger immédiatement

### Erreur 1 — tout mettre dans un seul composant

Tu fais :

```html
<div x-data="{ menuOpen:false, modalOpen:false, tab:1, search:'', ... }">
```

Ça devient ingérable.

Règle :

> 1 composant = 1 responsabilité

---

### Erreur 2 — state incohérent

Exemple :

* tu fermes le menu, mais tu oublies de reset un sous-menu
* tu changes un tab, mais tu gardes l’ancien état visible

Solution :

* méthodes
* reset contrôlé

---

### Erreur 3 — UI qui ne reflète pas l’état

Si `open = true`, ton bouton doit le montrer.

Exemple :

* label “Fermer”
* icône qui tourne
* aria-expanded mis à jour

---

# Résumé de la leçon

Tu maîtrises les 3 patterns fondamentaux Alpine :

* Toggle (booléen)
* Compteur (numérique + actions)
* Panneau repliable (toggle + UX + accessibilité)

Et tu as vu la version “pro” :

* méthodes au lieu d’expressions partout
* `x-cloak` systématique sur éléments conditionnels
* extraction possible en composants JS (Vite)

---

## Mini exercice (obligatoire)

Tu dois coder 3 blocs :

1. Un toggle “Afficher/Masquer”
2. Un compteur qui ne descend pas sous 0
3. Un panneau repliable avec :

   * aria-expanded
   * aria-controls
   * x-cloak

Bonus : refais le panneau repliable en composant JS (mode Vite).

---

On a terminé le Chapitre 2 (Leçons 1 → 7).

Prochaine étape logique : **Atelier UI #1 — Menu responsive complet (production-ready)**
Et là, on va tout assembler : `x-data`, `x-show`, events, outside, Escape, accessibilité, structure propre.

Quand tu me dis “go”, je l’écris complet comme un livrable de formation.
