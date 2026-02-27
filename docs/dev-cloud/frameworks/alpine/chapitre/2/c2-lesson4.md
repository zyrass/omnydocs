---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 4

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `x-show` : afficher / masquer un bloc (cas UI + limites + bonnes pratiques)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `x-show` correctement
* comprendre ce que `x-show` fait réellement dans le DOM
* éviter les bugs classiques (flash, logique inversée, conflits CSS)
* appliquer `x-show` sur des cas UI réalistes : menu, dropdown, modal
* connaître les limites et quand utiliser `x-if` à la place (on détaillera `x-if` au chapitre 5)

---

## 1) `x-show` : définition simple

`x-show` affiche ou masque un élément en fonction d’une condition.

Exemple :

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>

  <p x-show="open">
    Je suis visible uniquement si open = true
  </p>
</div>
```

Si `open` est `true`, le paragraphe s’affiche.
Si `open` est `false`, il disparaît.

---

## 2) Ce que fait vraiment `x-show` (important pour comprendre les bugs)

`x-show` ne supprime pas l’élément du DOM.

Il applique simplement un style :

* `display: none`

Donc l’élément :

* existe toujours
* mais il est caché visuellement

### Pourquoi c’est important ?

Parce que :

* les éléments cachés sont toujours dans la page
* ils peuvent être inspectés
* et parfois ils peuvent poser des problèmes UX (focus clavier, accessibilité)

---

## 3) `x-show` : quand l’utiliser (cas d’usage parfaits)

`x-show` est idéal pour :

* menus
* dropdowns
* panneaux repliables
* accordéons
* modals simples (avec une gestion propre)

En général :

> Si tu veux juste afficher/masquer rapidement sans recréer l’élément, `x-show` est parfait.

---

## 4) Exemple concret #1 : Menu mobile simple

```html
<nav x-data="{ open: false }">
  <button @click="open = !open">
    Menu
  </button>

  <div x-show="open">
    <a href="#">Accueil</a>
    <a href="#">Services</a>
    <a href="#">Contact</a>
  </div>
</nav>
```

Ça marche, mais ce n’est pas encore “pro”.

On va l’améliorer.

---

## 5) Exemple concret #2 : Menu “pro” (fermeture + clavier + outside)

Tu veux un comportement naturel :

* ouverture au clic
* fermeture si clic en dehors
* fermeture avec Escape

```html
<nav x-data="{ open: false }">
  <button
    @click="open = !open"
    :aria-expanded="open.toString()"
    aria-controls="mobile-menu"
  >
    Menu
  </button>

  <div
    id="mobile-menu"
    x-show="open"
    @click.outside="open = false"
    @keydown.escape.window="open = false"
    style="margin-top: 8px;"
  >
    <a href="#">Accueil</a>
    <a href="#">Services</a>
    <a href="#">Contact</a>
  </div>
</nav>
```

### Explications importantes

* `@click.outside` : ferme si tu cliques ailleurs
* `@keydown.escape.window` : ferme si tu appuies sur Escape
* `aria-expanded` : indique l’état ouvert/fermé pour l’accessibilité
* `aria-controls` : lie le bouton au menu

Tu vois la différence ?

Ce n’est plus “un menu qui marche”.
C’est un menu qui se comporte comme un vrai composant UI.

---

## 6) Le piège numéro 1 : le “flash” au chargement (FOUC)

FOUC = Flash Of Unstyled Content
Ici, c’est surtout le flash d’un élément visible avant qu’Alpine ne le masque.

### Problème

Si `open` est `false`, tu veux que le menu soit caché immédiatement.

Mais parfois, le navigateur affiche le menu 0.1 seconde avant Alpine.

### Solution : `x-cloak`

Tu fais :

```html
<div x-show="open" x-cloak>
  Menu caché proprement dès le départ
</div>
```

Et tu ajoutes dans ton CSS global :

```css
[x-cloak] {
  display: none !important;
}
```

Ça, c’est une bonne pratique de base.

---

## 7) Le piège numéro 2 : logique inversée

Très classique.

Tu veux afficher si `open = true`, mais tu écris :

```html
<div x-show="!open">
```

Résultat : tu crois que ça bug.

Solution : nommer proprement tes variables.

Bon nom :

* `open`
* `isOpen`
* `isMenuOpen`

Mauvais nom :

* `toggle`
* `click`
* `state1`

Un bon nom réduit les bugs.

---

## 8) Le piège numéro 3 : conflit CSS

Si tu as un CSS qui force l’affichage, tu peux casser `x-show`.

Exemple :

```css
.menu {
  display: block !important;
}
```

Même si Alpine met `display: none`, ton CSS gagne.

Résultat : `x-show` semble “ne pas marcher”.

Solution :

* éviter les `!important` inutiles
* inspecter les styles dans DevTools
* laisser Alpine contrôler le `display`

---

## 9) `x-show` et accessibilité (point sérieux)

Un élément caché avec `display: none` n’est pas visible, donc en général :

* il n’est pas focusable
* il n’est pas lu par les lecteurs d’écran

C’est plutôt correct.

Mais attention aux cas plus complexes :

* modals
* menus navigables au clavier
* éléments interactifs dans des zones cachées

Une UI pro ne doit pas piéger l’utilisateur clavier.

On traitera ça en profondeur dans :

* Chapitre 7 (modals)
* Chapitre 11 (Focus plugin + accessibilité)

---

## 10) `x-show` vs `x-if` (introduction rapide)

Même si `x-if` est au Chapitre 5, tu dois comprendre la différence dès maintenant.

| Directive | Comportement               | Effet                       |
| --------- | -------------------------- | --------------------------- |
| `x-show`  | cache/affiche via CSS      | l’élément reste dans le DOM |
| `x-if`    | ajoute/supprime réellement | l’élément est créé/détruit  |

En général :

* `x-show` = rapide et simple
* `x-if` = plus strict (meilleur quand tu veux supprimer complètement)

On détaillera avec des cas de performance et de logique.

---

## 11) Mini exemple : dropdown menu (cas réel)

```html
<div x-data="{ open: false }" style="position: relative; display: inline-block;">
  <button @click="open = !open" :aria-expanded="open.toString()">
    Options
  </button>

  <div
    x-show="open"
    x-cloak
    @click.outside="open = false"
    style="position: absolute; top: 100%; left: 0; border: 1px solid #ddd; padding: 8px; background: white;"
  >
    <button @click="open = false">Profil</button>
    <button @click="open = false">Paramètres</button>
    <button @click="open = false">Déconnexion</button>
  </div>
</div>
```

Ici tu vois un pattern standard :

* état `open`
* affichage conditionnel
* fermeture outside
* `x-cloak` pour éviter le flash

---

## Résumé de la leçon

* `x-show` affiche/masque un élément via `display: none`
* l’élément reste dans le DOM
* c’est parfait pour menus, dropdowns, panels, UI simple
* attention au flash → `x-cloak`
* attention aux conflits CSS
* accessibilité : penser clavier + aria
* `x-if` est une alternative quand tu veux créer/détruire réellement

---

## Mini exercice (important)

1. Crée un composant `x-data="{ open: false }"`
2. Fais un bouton “Ouvrir/Fermer”
3. Ajoute un bloc `x-show="open"`
4. Ajoute `x-cloak` + CSS global
5. Bonus :

   * fermeture au clic dehors
   * fermeture Escape

---

Prochaine leçon : **Leçon 5 — `x-cloak` : éviter le flash avant init**
On va le traiter proprement, avec une explication claire, une implémentation propre, et les erreurs classiques (et oui, beaucoup le font mal).
