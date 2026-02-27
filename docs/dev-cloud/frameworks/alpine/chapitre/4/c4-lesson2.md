---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 2

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## `.outside` : fermeture intelligente (menus, dropdowns, modals)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `@click.outside` correctement
* comprendre pourquoi ça évite des tonnes de bugs
* fermer proprement :

  * un dropdown
  * un menu
  * une modal
* éviter les pièges classiques (fermeture immédiate, conflit avec `.stop`, état incohérent)

`.outside` est une feature qui fait très “framework moderne” alors qu’on est en Alpine : c’est exactement ce qu’on veut.

---

## 1) Définition simple

`@click.outside="..."` exécute une action **quand l’utilisateur clique en dehors de l’élément**.

Donc :

* clic dedans → rien
* clic dehors → action (souvent “fermer”)

### Analogie simple

Imagine que ton composant est une pièce.

* si tu cliques dans la pièce, tu continues ton action
* si tu cliques dehors, tu sors → donc on ferme

---

## 2) Pourquoi `.outside` est indispensable en UI “pro”

Sans `.outside`, tu vois souvent du JS manuel :

* écouter `document.addEventListener('click', ...)`
* comparer `event.target`
* gérer les cas bizarres
* nettoyer les listeners

C’est lourd, fragile, et souvent mal fait.

Avec Alpine :

* tu poses `@click.outside`
* c’est clair, lisible, maintenable

---

# 3) Exemple #1 — Dropdown basique (le cas d’école)

### Objectif UX

* clic bouton → ouvre
* clic ailleurs → ferme

```html
<div x-data="{ open: false }" style="position: relative; display: inline-block;">
  <button @click="open = !open">
    Actions
  </button>

  <div
    x-show="open"
    x-cloak
    @click.outside="open = false"
    style="position: absolute; top: calc(100% + 8px); left: 0; border: 1px solid #ddd; background: #fff; padding: 8px; border-radius: 10px; min-width: 180px;"
  >
    <a href="#" @click.prevent="open = false">Modifier</a><br />
    <a href="#" @click.prevent="open = false">Supprimer</a>
  </div>
</div>
```

### Ce qu’il faut retenir

Le `@click.outside` doit être placé sur **le bloc à fermer** (le dropdown panel).

---

# 4) Exemple #2 — Menu mobile (comme en prod)

Tu veux :

* ouvrir menu
* clic dehors ferme

```html
<nav x-data="{ open: false }">
  <button @click="open = !open" :aria-expanded="open.toString()">
    Menu
  </button>

  <div
    x-show="open"
    x-cloak
    @click.outside="open = false"
    style="margin-top: 8px; border: 1px solid #ddd; padding: 10px; border-radius: 12px;"
  >
    <a href="#home" @click="open = false">Accueil</a><br />
    <a href="#services" @click="open = false">Services</a><br />
    <a href="#contact" @click="open = false">Contact</a>
  </div>
</nav>
```

---

# 5) Exemple #3 — Modal (fermeture outside + overlay)

Pour une modal, il y a deux façons :

## Option A (simple) : `@click.self` sur l’overlay

C’est souvent la meilleure option pour une modal.

```html
<div x-data="{ open: false }">
  <button @click="open = true">Ouvrir modal</button>

  <div
    x-show="open"
    x-cloak
    @click.self="open = false"
    style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); padding: 40px;"
  >
    <div style="background: #fff; padding: 16px; border-radius: 12px;">
      <h2>Modal</h2>
      <p>Cliquer sur l’overlay ferme la modal.</p>
      <button @click="open = false">Fermer</button>
    </div>
  </div>
</div>
```

## Option B : `@click.outside` sur le panel

Possible aussi, mais moins “modal standard” selon structure.

---

# 6) Pièges fréquents avec `.outside`

### Piège 1 — fermeture immédiate à l’ouverture

Tu cliques sur le bouton pour ouvrir… et ça se ferme instantanément.

Pourquoi ?
Parce que tu as placé `@click.outside` sur un parent trop large ou mal structuré.

Règle :

> `@click.outside` doit être sur le bloc qui représente “la zone ouverte”.

---

### Piège 2 — conflit avec `.stop`

Si tu mets `.stop` partout, tu peux empêcher `.outside` de détecter le clic.

Exemple :

* clic sur un bouton dans le dropdown
* tu veux fermer
* mais `.stop` bloque des comportements attendus

Règle :

> Utilise `.stop` uniquement si tu as un vrai bug de propagation.

---

### Piège 3 — état incohérent (menu fermé mais dropdown ouvert)

Dans un menu complexe :

* menu principal se ferme
* dropdown reste “open” dans le state

Résultat : quand tu réouvres, tu te retrouves avec un sous-menu ouvert sans logique.

Solution :

* quand tu fermes le parent → tu fermes les enfants

Exemple pro :

```js
closeMenu() {
  this.open = false;
  this.dropdownOpen = false;
}
```

---

# 7) Bon pattern : `toggle()` + `close()` (propre et maintenable)

Quand tu fais des UI “pro”, tu dois éviter les `open = false` dispersés partout.

Exemple propre :

```html
<div x-data="{
  open: false,

  toggle() {
    this.open = !this.open;
  },

  close() {
    this.open = false;
  }
}">
  <button @click="toggle()">Toggle</button>

  <div x-show="open" x-cloak @click.outside="close()">
    Contenu
  </div>
</div>
```

Lisible, propre, réutilisable.

---

# 8) Résumé (ce que tu dois maîtriser)

* `@click.outside` ferme un bloc quand clic en dehors
* parfait pour dropdowns, menus, panneaux
* attention au placement (sur le bon élément)
* éviter les conflits `.stop`
* toujours garder un state cohérent (parent/child)

---

## Mini exercice (obligatoire)

### Exercice A — Dropdown “Profil”

* bouton “Profil”
* dropdown : “Mon compte”, “Déconnexion”
* clic dehors ferme
* clic sur un lien ferme aussi

### Exercice B — Menu mobile

* bouton Menu
* nav visible
* clic dehors ferme
* Escape ferme (bonus : utilise `@keydown.escape.window`)

---

Prochaine leçon : **Leçon 3 — Événements clavier (Enter, Escape, raccourcis)**
On va rendre ton UI utilisable au clavier, comme un vrai produit.
