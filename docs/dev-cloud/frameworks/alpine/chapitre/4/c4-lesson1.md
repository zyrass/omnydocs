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

## Modificateurs d’événements : `.prevent`, `.stop`, `.once`, `.self` (et pourquoi ça change tout)

### Objectif de la leçon

À la fin, tu sauras :

* ce que sont les **modificateurs d’événements** dans Alpine
* utiliser correctement :

  * `.prevent`
  * `.stop`
  * `.once`
  * `.self`
* éviter les bugs classiques liés aux clics “qui remontent”
* structurer tes interactions UI comme un dev sérieux

Cette leçon est importante parce que les événements, c’est le point où beaucoup de gens font n’importe quoi… et ça se voit.

---

## 1) Définition simple : un modificateur d’événement, c’est quoi ?

Un modificateur, c’est une option ajoutée à ton événement pour changer son comportement.

Exemple :

```html
<button @click.prevent="doSomething()">
  Clique
</button>
```

Ici, `.prevent` modifie le comportement du clic.

### Analogie simple

L’événement, c’est une action (ex: “clic”).
Le modificateur, c’est une règle de comportement (ex: “ne fais pas l’action par défaut”).

---

# 2) `.prevent` — empêcher le comportement par défaut

## Quand l’utiliser ?

Quand un événement déclenche une action “native” du navigateur que tu ne veux pas.

Cas le plus classique : **formulaire**.

### Exemple : formulaire qui reload (mauvais)

```html
<form @submit="console.log('submit')">
  <button type="submit">Envoyer</button>
</form>
```

Ça reload la page → UX catastrophique.

### Version propre

```html
<form @submit.prevent="console.log('submit propre')">
  <button type="submit">Envoyer</button>
</form>
```

`.prevent` = `event.preventDefault()`.

---

## Autre cas réel : lien `<a href="#">` qui remonte en haut

Tu vois souvent ça :

```html
<a href="#" @click="open = true">Ouvrir</a>
```

Ça ouvre ET ça remonte en haut.

Solution :

```html
<a href="#" @click.prevent="open = true">Ouvrir</a>
```

---

# 3) `.stop` — arrêter la propagation (éviter les clics “fantômes”)

## Le problème : propagation d’événements

Dans le DOM, quand tu cliques sur un élément, l’événement “remonte” vers ses parents.

Ça s’appelle la **propagation** (ou “bubbling”).

### Exemple de bug classique

Tu as un parent qui écoute un clic :

```html
<div x-data="{ open: true }" @click="open = false">
  <div style="padding: 12px; border: 1px solid #ddd;">
    <button @click="console.log('clic bouton')">Clique</button>
  </div>
</div>
```

Quand tu cliques sur le bouton :

* ça log “clic bouton”
* MAIS le clic remonte et ferme le parent

Résultat : UI qui se ferme alors que tu voulais juste cliquer dedans.

---

## Solution : `.stop`

```html
<div x-data="{ open: true }" @click="open = false">
  <div style="padding: 12px; border: 1px solid #ddd;">
    <button @click.stop="console.log('clic bouton')">
      Clique sans fermer
    </button>
  </div>
</div>
```

`.stop` = `event.stopPropagation()`.

---

## Cas réel : dropdown

Tu veux :

* clic sur le bouton → ouvre
* clic ailleurs → ferme
* clic dans le menu → ne ferme pas

`.stop` est souvent indispensable.

---

# 4) `.once` — exécuter une seule fois

## Quand l’utiliser ?

Quand tu veux une action qui ne doit arriver qu’une fois.

Exemples :

* message d’accueil
* init d’une animation
* tutoriel “première fois”
* bouton “Activer” (activation unique)

### Exemple

```html
<div x-data="{ count: 0 }">
  <button @click.once="count++">
    Clique (une seule fois)
  </button>

  <p x-text="count"></p>
</div>
```

Même si tu recliques, `count` ne bouge plus.

---

## Piège à éviter

`.once` ne remplace pas une vraie logique métier.

Si ton action doit être “bloquée” selon un état, fais-le dans ton code.

---

# 5) `.self` — déclencher uniquement si on clique sur l’élément lui-même

`.self` veut dire :

> “Déclenche l’action seulement si l’événement vient de cet élément, pas d’un enfant.”

### Exemple concret

Tu as une zone (overlay) qui ferme une modal au clic.

Tu veux :

* clic sur l’overlay → ferme
* clic sur la modal → ne ferme pas

Sans `.self`, cliquer dans la modal peut déclencher le clic sur le parent (selon structure).

### Version propre avec `.self`

```html
<div x-data="{ open: true }">
  <!-- Overlay -->
  <div
    x-show="open"
    x-cloak
    @click.self="open = false"
    style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); padding: 40px;"
  >
    <!-- Modal -->
    <div style="background: #fff; padding: 16px; border-radius: 12px;">
      <h2>Modal</h2>
      <p>Clique en dehors pour fermer.</p>

      <button @click="open = false">Fermer</button>
    </div>
  </div>
</div>
```

Ici :

* clic sur l’overlay (zone grise) → ferme
* clic dans la modal (zone blanche) → ne ferme pas

C’est exactement ce qu’on veut.

---

# 6) Résumé des 4 modificateurs (table clair)

| Modificateur | Effet                                      | Utilisation typique    |
| ------------ | ------------------------------------------ | ---------------------- |
| `.prevent`   | empêche l’action par défaut                | submit, liens          |
| `.stop`      | stop propagation                           | dropdown, menu, modals |
| `.once`      | exécute une seule fois                     | activation unique      |
| `.self`      | déclenche uniquement si clic sur l’élément | overlay modal          |

---

## 7) Les erreurs fréquentes (vraies erreurs terrain)

### Erreur 1 — mettre `.stop` partout

Si tu mets `.stop` partout, tu risques de casser :

* des fermetures outside
* des comportements globaux
* des logiques de parent

Règle :

> `.stop` se met uniquement quand tu as un vrai problème de propagation.

---

### Erreur 2 — confondre `.self` et `.stop`

* `.stop` empêche la propagation
* `.self` filtre l’origine de l’événement

Tu utilises `.self` quand tu veux :

* clic sur le conteneur → OK
* clic sur un enfant → ignore

---

### Erreur 3 — oublier `.prevent` sur submit

Ça, c’est l’erreur la plus visible chez les débutants.

---

## 8) Mini exercice (obligatoire)

### Exercice A — Lien “ouvrir modal”

1. Fais un `<a href="#">Ouvrir</a>`
2. Quand tu cliques → ouvre une modal
3. Le lien ne doit pas remonter en haut

Indice : `@click.prevent`

---

### Exercice B — Dropdown

1. Un bouton ouvre un dropdown
2. Cliquer dans le dropdown ne doit pas le fermer
3. Cliquer sur la page ferme le dropdown

Indice : tu vas avoir besoin de `.stop`

---

### Exercice C — Modal overlay

1. Clique sur overlay → ferme
2. Clique dans modal → ne ferme pas

Indice : `@click.self`

---

## Conclusion de la leçon

Tu viens d’apprendre 4 outils qui rendent ton UX stable :

* `.prevent` évite les comportements parasites
* `.stop` évite les clics “fantômes”
* `.once` évite les actions répétées
* `.self` gère proprement les overlays et zones cliquables

---

Prochaine leçon : **Leçon 2 — `.outside` : fermeture intelligente (menus, dropdowns, modals)**
Et là on va faire un truc vraiment concret : gérer la fermeture au clic extérieur sans bricolage.
