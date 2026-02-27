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

## `x-on` (alias `@`) : écouter des événements proprement (click, input, change, submit)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `x-on` et son raccourci `@`
* écouter les événements les plus importants : `click`, `input`, `change`, `submit`, `keydown`
* utiliser les modificateurs d’événements (intro, on approfondira au Chapitre 4)
* structurer ton code pour éviter le “spaghetti” dans le HTML
* gérer des interactions UI réalistes et propres

Dans Alpine, `x-on` c’est le nerf de la guerre : c’est ce qui transforme ton HTML en interface interactive.

---

## 1) `x-on` : définition simple

`x-on` permet d’écouter un événement et d’exécuter du JavaScript.

Exemple :

```html
<div x-data="{ count: 0 }">
  <button x-on:click="count++">+1</button>
  <span x-text="count"></span>
</div>
```

---

## 2) Raccourci standard : `@`

La version courte est :

```html
<button @click="count++">+1</button>
```

C’est exactement pareil.

Dans un projet pro, on utilise quasiment toujours `@`.

---

## 3) Les événements essentiels à connaître

Voici les événements les plus utilisés en UI :

| Événement        | Déclenché quand…                             | Exemple concret      |
| ---------------- | -------------------------------------------- | -------------------- |
| `click`          | clic souris / tap mobile                     | ouvrir menu, valider |
| `input`          | valeur d’un champ change (pendant la saisie) | recherche live       |
| `change`         | valeur validée (souvent sur select/checkbox) | filtres              |
| `submit`         | formulaire envoyé                            | login, todo          |
| `keydown`        | touche clavier pressée                       | Escape, Enter        |
| `focus` / `blur` | entrée/sortie focus                          | validation UX        |

Tu n’as pas besoin d’en apprendre 50. Ceux-là couvrent 95% des cas.

---

# Cas 1 — `@click` (le classique)

## 4) Exemple simple : toggle

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <p x-show="open" x-cloak>Contenu visible</p>
</div>
```

---

## 5) Version pro : logique dans une méthode

Dès que ton `@click` devient plus long que 1 ligne, tu dois le sortir.

```html
<div x-data="{
  open: false,

  toggle() {
    this.open = !this.open;
  }
}">
  <button @click="toggle()">Toggle</button>
  <p x-show="open" x-cloak>Contenu visible</p>
</div>
```

Pourquoi ?
Parce que tu veux garder ton HTML lisible.

---

# Cas 2 — `@input` (réactivité pendant la saisie)

## 6) Exemple : recherche live (sans x-model)

```html
<div x-data="{ query: '' }">
  <input
    type="text"
    placeholder="Rechercher..."
    @input="query = $event.target.value"
  />

  <p>Recherche : <strong x-text="query"></strong></p>
</div>
```

### Explication importante : `$event`

`$event` représente l’événement JS natif.

`$event.target.value` = la valeur du champ.

---

## Pourquoi ce pattern existe alors qu’on a `x-model` ?

Parce que parfois tu veux :

* capturer la valeur
* et déclencher une logique (ex: filtrer, logger, normaliser)

Mais dans la majorité des cas, tu utiliseras `x-model` (Leçon 3).

---

# Cas 3 — `@change` (validation / filtres)

## 7) Exemple : filtre via select

```html
<div x-data="{ filter: 'all' }">
  <select @change="filter = $event.target.value">
    <option value="all">Tous</option>
    <option value="active">Actifs</option>
    <option value="done">Terminés</option>
  </select>

  <p>Filtre actuel : <strong x-text="filter"></strong></p>
</div>
```

---

# Cas 4 — `@submit` (formulaires)

## 8) Exemple : formulaire basique (mauvaise UX)

```html
<form x-data="{ name: '' }" @submit="console.log(name)">
  <input type="text" @input="name = $event.target.value" />
  <button type="submit">Envoyer</button>
</form>
```

Problème : le formulaire va recharger la page.

Dans une UI moderne, tu veux empêcher ça.

---

## 9) Solution pro : `@submit.prevent`

```html
<form x-data="{ name: '' }" @submit.prevent="console.log(name)">
  <input type="text" @input="name = $event.target.value" />
  <button type="submit">Envoyer</button>
</form>
```

`.prevent` = `event.preventDefault()`
Donc pas de reload.

On détaillera plus tard les modificateurs, mais celui-ci est indispensable.

---

# Cas 5 — `@keydown` (clavier)

## 10) Exemple : fermer avec Escape

```html
<div x-data="{ open: true }" @keydown.escape.window="open = false">
  <p x-show="open">Appuie sur Escape pour fermer</p>
</div>
```

Ici tu vois déjà deux modificateurs :

* `.escape` : touche Escape
* `.window` : écoute globale (pas seulement dans l’élément)

On approfondira au Chapitre 4, mais c’est important de l’avoir en tête.

---

## 11) Éviter le code spaghetti : règle de base

Mauvais exemple :

```html
<button @click="open = !open; if(open){count++; console.log(count)}">
  Action
</button>
```

Ça marche, mais c’est illisible.

Version pro :

```html
<div x-data="{
  open: false,
  count: 0,

  handleClick() {
    this.open = !this.open;

    if (this.open) {
      this.count++;
      console.log('count =', this.count);
    }
  }
}">
  <button @click="handleClick()">Action</button>
  <p x-text="count"></p>
</div>
```

Tu peux lire, maintenir, et évoluer.

---

## 12) Mini exemple complet (pro, utile)

Objectif : bouton “Sauvegarder” qui se désactive après clic.

```html
<div x-data="{
  saved: false,

  save() {
    // simulation d'une action
    this.saved = true;

    // reset après 2 secondes (simulation UX)
    setTimeout(() => {
      this.saved = false;
    }, 2000);
  }
}">
  <button
    @click="save()"
    :disabled="saved"
  >
    <span x-text="saved ? 'Sauvegardé' : 'Sauvegarder'"></span>
  </button>
</div>
```

Tu combines ici :

* `@click`
* `:disabled`
* `x-text`

C’est exactement le genre de mini pattern que tu vas réutiliser dans tes projets.

---

## 13) Pièges fréquents avec `x-on`

### Piège 1 — oublier `type="button"`

Dans un formulaire, un bouton sans type est un submit par défaut.

Exemple dangereux :

```html
<form>
  <button @click="doSomething()">Clique</button>
</form>
```

Ça peut soumettre le formulaire.

Solution :

```html
<button type="button" @click="doSomething()">Clique</button>
```

---

### Piège 2 — écouter trop haut dans le DOM

Si tu mets un `@click` sur un parent, tu peux déclencher des actions involontaires.

Solution :

* placer l’événement au bon niveau
* utiliser `.stop` si nécessaire (Chapitre 4)

---

### Piège 3 — trop de logique dans le HTML

Même règle que toujours :

* si c’est complexe → méthode

---

## Résumé de la leçon

* `x-on` écoute des événements
* `@` est le raccourci standard
* événements clés : click, input, change, submit, keydown
* `@submit.prevent` est indispensable
* `$event` donne accès à l’événement natif
* propreté : logique dans des méthodes, pas dans l’attribut

---

## Mini exercice (obligatoire)

1. Crée un composant avec :

   * `count: 0`
2. Ajoute :

   * bouton `+1`
   * bouton `Reset`
3. Ajoute un input :

   * quand on tape, affiche la valeur en dessous
4. Ajoute un formulaire :

   * empêcher le reload avec `@submit.prevent`

---

Prochaine leçon : **Leçon 3 — `x-model` : synchroniser les inputs (text, checkbox, radio, select)**
C’est la directive qui te fait gagner du temps sur tous les formulaires.
