---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 3

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Événements clavier : Enter, Escape, raccourcis (UX “pro”)

### Objectif de la leçon

À la fin, tu sauras :

* écouter des événements clavier avec Alpine
* gérer correctement :

  * Enter
  * Escape
  * combinaisons de touches (raccourcis)
* écouter au bon endroit (`.window`, `.document`)
* éviter les pièges : déclenchement involontaire, UI instable, conflits

Une UI qui marche uniquement à la souris, c’est une UI incomplète.
Le clavier, c’est la base d’une interface professionnelle.

---

## 1) Rappel : comment on écoute un événement clavier ?

En Alpine, tu peux faire :

```html
<div x-data="{ }" @keydown="console.log('touche pressée')">
  ...
</div>
```

Mais ça écoute toutes les touches, ce qui est rarement ce qu’on veut.

---

## 2) Écouter une touche spécifique : `.enter`, `.escape`, etc.

Alpine propose des modificateurs clavier.

### Exemple : Enter

```html
<input
  type="text"
  x-data="{ value: '' }"
  x-model="value"
  @keydown.enter="console.log('Enter pressé', value)"
/>
```

### Exemple : Escape

```html
<div x-data="{ open: true }" @keydown.escape="open = false">
  <p x-show="open">Appuie sur Escape pour fermer</p>
</div>
```

---

## 3) Le point clé : où placer l’écoute clavier ?

Si tu mets `@keydown.escape` sur un élément, ça ne marche que si :

* l’élément est focus
* ou un enfant est focus

Dans une vraie UI, tu veux souvent écouter Escape “partout”.

Donc tu utilises `.window`.

---

# 4) Pattern pro : Escape global avec `.window`

### Exemple : fermer une modal

```html
<div x-data="{ open: false }" @keydown.escape.window="open = false">
  <button @click="open = true">Ouvrir</button>

  <div x-show="open" x-cloak style="margin-top: 10px; border: 1px solid #ddd; padding: 12px;">
    <p>Modal simulée</p>
    <button @click="open = false">Fermer</button>
  </div>
</div>
```

Ici :

* peu importe où tu es sur la page
* Escape ferme la modal

C’est exactement le comportement attendu en prod.

---

## 5) Pattern pro : priorité des fermetures (dropdown avant menu)

Dans une UI complexe, Escape doit fermer dans cet ordre :

1. fermer le sous-menu / dropdown
2. sinon fermer le menu principal
3. sinon ne rien faire

### Exemple

```html
<div
  x-data="{
    menuOpen: false,
    dropdownOpen: false,

    onEscape() {
      if (this.dropdownOpen) {
        this.dropdownOpen = false;
        return;
      }

      if (this.menuOpen) {
        this.menuOpen = false;
      }
    }
  }"
  @keydown.escape.window="onEscape()"
>
  <button @click="menuOpen = !menuOpen">Menu</button>

  <div x-show="menuOpen" x-cloak style="margin-top: 8px;">
    <button @click="dropdownOpen = !dropdownOpen">Produits</button>

    <div x-show="dropdownOpen" x-cloak style="margin-top: 6px; border: 1px solid #ddd; padding: 8px;">
      Dropdown
    </div>
  </div>
</div>
```

Ça évite les comportements “bizarres” où Escape ferme tout d’un coup.

---

# 6) Enter : améliorer l’UX sur les formulaires

### Cas réel : Todo list

Tu veux que Enter ajoute la tâche.

La bonne solution : un `<form>` avec `@submit.prevent`.

Mais parfois tu veux gérer Enter sur un champ spécifique.

### Exemple : Enter déclenche une action

```html
<div x-data="{
  value: '',
  add() {
    if (this.value.trim().length === 0) return;
    console.log('Ajout :', this.value);
    this.value = '';
  }
}">
  <input
    type="text"
    x-model="value"
    placeholder="Tape puis Enter"
    @keydown.enter="add()"
  />

  <button @click="add()">Ajouter</button>
</div>
```

---

## Piège important : Enter dans un formulaire

Si tu es dans un `<form>`, Enter déclenche un submit.

Donc :

* soit tu veux ce comportement (souvent oui)
* soit tu veux l’empêcher (rare)

Dans la plupart des cas : `@submit.prevent` est la solution propre.

---

# 7) Raccourcis clavier (Ctrl+K, Ctrl+S, etc.)

Une UI pro propose souvent un raccourci.

Exemples classiques :

* Ctrl+K : ouvrir recherche
* Ctrl+S : sauvegarder
* ? : ouvrir aide

### Exemple : Ctrl+K ouvre une barre de recherche

```html
<div x-data="{
  open: false,

  toggle() {
    this.open = !this.open;
  }
}" @keydown.window="
  if ($event.ctrlKey && $event.key === 'k') {
    $event.preventDefault();
    toggle();
  }
">
  <button @click="toggle()">Recherche</button>

  <div x-show="open" x-cloak style="margin-top: 10px;">
    <input type="text" placeholder="Rechercher..." />
  </div>
</div>
```

### Explication

* `$event.ctrlKey` : touche Ctrl pressée
* `$event.key === 'k'` : touche K
* `preventDefault()` : empêche le navigateur de faire autre chose (souvent il focus la barre d’adresse ou autre)

---

## Piège : raccourcis qui cassent le navigateur

Certains raccourcis sont déjà pris :

* Ctrl+S
* Ctrl+P
* Ctrl+R
* Ctrl+L

Tu peux les utiliser dans une web app, mais c’est à faire avec prudence.

---

# 8) `.document` vs `.window` (différence utile)

Dans Alpine tu peux écouter :

* `.window` : global navigateur
* `.document` : document DOM

Dans la plupart des cas UI : `.window` est suffisant.

---

# 9) Résumé de la leçon

Tu sais maintenant :

* écouter des touches spécifiques (`.enter`, `.escape`)
* écouter globalement (`.window`)
* gérer des priorités (dropdown → menu)
* améliorer les formulaires avec Enter
* ajouter des raccourcis clavier (Ctrl+K)
* éviter les conflits avec le comportement natif

---

## Mini exercice (obligatoire)

### Exercice A — Modal clavier

* bouton ouvre modal
* Escape ferme modal (global)
* clic outside ferme modal (bonus)

### Exercice B — Dropdown clavier

* dropdown s’ouvre au clic
* Escape ferme dropdown sans fermer le reste

### Exercice C — Raccourci Ctrl+K

* Ctrl+K ouvre un champ recherche
* Escape ferme le champ

---

Prochaine leçon : **Leçon 4 — `.window` / `.document` : écoute globale, pièges et bonnes pratiques**
On va clarifier proprement ce que ça change et quand l’utiliser.
