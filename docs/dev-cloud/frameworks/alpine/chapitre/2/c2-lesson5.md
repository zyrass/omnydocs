---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 5

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `x-cloak` : éviter le flash avant l’initialisation (proprement)

### Objectif de la leçon

À la fin, tu sauras :

* pourquoi le “flash” arrive sur une page Alpine
* à quoi sert `x-cloak`
* comment l’utiliser correctement (avec le CSS obligatoire)
* où le placer dans une UI réelle (menus, modals, dropdowns)
* les erreurs fréquentes qui rendent `x-cloak` inutile

Cette leçon paraît simple, mais elle fait la différence entre :

* une UI “amateur” qui clignote
* une UI “propre” et stable

---

## 1) Le problème : le flash avant Alpine (et pourquoi il existe)

Quand une page se charge, il se passe toujours un ordre d’exécution :

1. le navigateur lit le HTML
2. il affiche ce qu’il peut afficher immédiatement
3. puis il charge le JavaScript
4. puis Alpine démarre et applique les comportements (`x-show`, `x-text`, etc.)

Pendant le petit délai entre l’étape 2 et 4, ton HTML peut apparaître dans un état “brut”.

### Exemple typique

Tu as :

```html
<div x-data="{ open: false }">
  <div x-show="open">
    Menu
  </div>
</div>
```

Tu veux que le menu soit caché au départ.
Mais parfois tu vois “Menu” apparaître une fraction de seconde.

Ce phénomène est normal : Alpine n’a pas encore eu le temps de masquer l’élément.

---

## 2) `x-cloak` : définition simple

`x-cloak` est un attribut Alpine qui sert à dire :

> “Cache cet élément tant qu’Alpine n’est pas prêt.”

Mais attention : `x-cloak` ne fonctionne pas tout seul.
Il a besoin d’un CSS associé.

---

## 3) La règle obligatoire : `x-cloak` + CSS global

### Étape 1 — Ajouter le CSS global

Tu dois ajouter ceci dans ton CSS :

```css
[x-cloak] {
  display: none !important;
}
```

Pourquoi `!important` ?

Parce que tu veux être sûr que rien ne force l’affichage de l’élément.

### Étape 2 — Ajouter `x-cloak` sur l’élément à protéger

```html
<div x-show="open" x-cloak>
  Menu
</div>
```

Résultat :

* au chargement : le CSS cache l’élément
* quand Alpine démarre : Alpine retire automatiquement `x-cloak`
* et ensuite `x-show` contrôle l’affichage

---

## 4) Exemple complet : menu sans flash

### Code

```html
<style>
  [x-cloak] {
    display: none !important;
  }
</style>

<nav x-data="{ open: false }">
  <button @click="open = !open">
    Menu
  </button>

  <div x-show="open" x-cloak>
    <a href="#">Accueil</a>
    <a href="#">Services</a>
    <a href="#">Contact</a>
  </div>
</nav>
```

Tu peux recharger la page 50 fois :
tu ne verras plus le menu apparaître au chargement.

---

## 5) Où utiliser `x-cloak` (cas concrets)

`x-cloak` doit être utilisé sur tout élément qui :

* ne doit jamais être visible “par défaut”
* dépend d’un état Alpine
* risque de clignoter au chargement

### Exemples typiques

* dropdown menu
* menu mobile
* modal
* panneau repliable
* onglets (tabs)
* accordéon

En gros : tout ce qui est contrôlé par `x-show` ou `x-if`.

---

## 6) Erreurs fréquentes (et comment les corriger)

### Erreur 1 — Mettre `x-cloak` sans CSS

Très fréquent.

Tu écris :

```html
<div x-cloak x-show="open">Menu</div>
```

Mais tu oublies le CSS `[x-cloak] { display:none }`

Résultat : `x-cloak` ne sert à rien.

**Règle : sans CSS, x-cloak = inutile.**

---

### Erreur 2 — Mettre `x-cloak` au mauvais endroit

Tu mets `x-cloak` sur le parent, mais c’est l’enfant qui flash.

Exemple :

```html
<div x-data="{ open: false }" x-cloak>
  <div x-show="open">Menu</div>
</div>
```

Ça peut fonctionner dans certains cas, mais ce n’est pas toujours optimal.

Bonne pratique :

* mettre `x-cloak` sur l’élément réellement conditionnel

```html
<div x-data="{ open: false }">
  <div x-show="open" x-cloak>Menu</div>
</div>
```

---

### Erreur 3 — Utiliser `x-cloak` pour masquer des bugs

`x-cloak` ne doit pas servir à cacher une UI cassée.

Il sert uniquement à éviter le flash avant init.

Si ton composant bug après init, `x-cloak` ne résout rien.

---

## 7) `x-cloak` dans un projet Vite (organisation propre)

Dans un projet moderne (Vite + CSS), tu ne mets pas ton CSS dans le HTML.

Tu mets le style global dans ton fichier CSS principal, par exemple :

* `src/styles/app.css`
  ou
* `resources/css/app.css` (Laravel)

Et tu ajoutes :

```css
[x-cloak] {
  display: none !important;
}
```

C’est propre, centralisé, maintenable.

---

## 8) Mini exemple : modal (cas ultra important)

Une modal qui flash au chargement, c’est une catastrophe UX.

Voici le pattern :

```html
<style>
  [x-cloak] { display: none !important; }
</style>

<div x-data="{ open: false }">
  <button @click="open = true">Ouvrir modal</button>

  <div x-show="open" x-cloak>
    <div style="border: 1px solid #ddd; padding: 12px; margin-top: 8px;">
      <p>Modal content</p>
      <button @click="open = false">Fermer</button>
    </div>
  </div>
</div>
```

Sans `x-cloak`, tu peux voir la modal au chargement.
Avec `x-cloak`, c’est clean.

---

## 9) Résumé de la leçon

* Le flash existe parce que le navigateur affiche le HTML avant Alpine.
* `x-cloak` sert à cacher les éléments avant l’initialisation.
* `x-cloak` fonctionne uniquement avec le CSS :

```css
[x-cloak] { display: none !important; }
```

* Utilise-le sur tout composant conditionnel important (menu, modal, dropdown).
* Ne l’utilise pas comme cache-misère.

---

## Mini exercice (rapide)

1. Ajoute le CSS `[x-cloak]` dans ton projet
2. Fais un composant avec :

   * `open: false`
   * un menu `x-show="open"`
3. Recharge la page plusieurs fois
4. Vérifie qu’il n’y a aucun flash
5. Bonus : ajoute un dropdown + `@click.outside`

---

Prochaine leçon : **Leçon 6 — `x-init` : initialiser un composant proprement**
Et là on va entrer dans un point clé : comment initialiser un state, précharger des données, et lancer une logique au bon moment sans faire n’importe quoi.
