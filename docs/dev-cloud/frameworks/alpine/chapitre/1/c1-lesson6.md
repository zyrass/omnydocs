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

## Prérequis nécessaires (et comment éviter de te saboter)

### Objectif de la leçon

À la fin, tu sauras exactement :

* ce que tu dois maîtriser en **HTML / CSS / JavaScript**
* ce qui est **obligatoire** vs ce qui est juste “utile”
* les **erreurs classiques** des étudiants
* comment être à l’aise pour suivre la formation sans galérer

Alpine est simple, mais il ne pardonne pas un truc :
si tes bases sont bancales, tu vas faire du code “qui marche” mais impossible à maintenir.

---

## 1) Prérequis HTML (obligatoires)

Tu n’as pas besoin d’être un expert HTML, mais tu dois comprendre la structure d’une page.

### Ce que tu dois savoir faire

Tu dois être à l’aise avec :

* les balises de base : `div`, `button`, `a`, `p`, `span`, `input`, `form`
* les attributs HTML : `class`, `id`, `type`, `name`, `value`, `disabled`
* la différence entre un élément “bloc” et “inline”
* la structure d’un formulaire

### Pourquoi c’est important avec Alpine

Alpine est “HTML-first”, donc ton HTML est ton terrain de jeu.

Si tu ne comprends pas bien la structure, tu vas :

* mettre un `x-data` au mauvais endroit
* casser le scope (périmètre) de ton composant
* créer des bugs de comportement

#### Exemple de piège classique

Tu veux que 2 boutons partagent le même état, mais tu as mis `x-data` trop bas.

Mauvais placement :

```html
<button @click="open = !open">Toggle</button>

<div x-data="{ open: false }">
  <p x-show="open">Menu</p>
</div>
```

Ici, le bouton ne “voit” pas `open`.
Pourquoi ? Parce que `open` existe uniquement dans le composant `x-data`.

Bonne approche :

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <p x-show="open">Menu</p>
</div>
```

---

## 2) Prérequis CSS (obligatoires, mais simples)

Tu n’as pas besoin d’être un designer.
Mais tu dois savoir gérer :

* `display`, `flex`, `grid`
* `padding`, `margin`
* `gap`
* `position` (relative/absolute)
* `z-index`
* la gestion d’un overlay (modal)

### Pourquoi c’est important avec Alpine

Beaucoup de composants Alpine sont des composants UI :

* menus
* dropdowns
* modals
* accordéons

Et ces composants sont autant du CSS que du JS.

Si tu ne maîtrises pas un minimum le CSS, tu vas croire que “Alpine bug”…
alors que c’est ton layout qui est mauvais.

---

## 3) Prérequis JavaScript (obligatoires)

Ici, on va être précis : Alpine utilise du JavaScript moderne dans ses attributs.

Tu dois comprendre au minimum :

### 3.1 Variables et types

Tu dois savoir ce que c’est :

* une variable (`let`, `const`)
* un nombre, une string, un booléen
* `true / false`

Exemple :

```js
const open = false;
let count = 0;
```

### 3.2 Objets et propriétés

Tu dois être à l’aise avec :

* les objets `{ ... }`
* accéder à une propriété `obj.key`

Exemple :

```js
const user = { name: "Alain", age: 32 };
console.log(user.name);
```

Dans Alpine, `x-data` est souvent un objet.

---

### 3.3 Fonctions

Tu dois comprendre :

* créer une fonction
* l’appeler
* comprendre `this` (au moins en surface)

Exemple :

```js
function increment() {
  count++;
}
```

Dans Alpine, tu vas souvent faire :

```html
<div x-data="{
  count: 0,
  increment() {
    this.count++;
  }
}">
</div>
```

Ici, `this.count` veut dire : “le count de CE composant”.

---

### 3.4 Conditions (if / else)

Tu dois savoir faire :

* `if`
* opérateurs `===`, `!==`
* ternaires `condition ? A : B`

Exemple :

```js
if (count > 0) {
  console.log("positif");
}
```

Dans Alpine, ça sert pour :

* afficher un bouton seulement si une condition est vraie
* changer un texte selon l’état

---

### 3.5 Tableaux (arrays) et boucles

Tu dois comprendre :

* un tableau `[]`
* `push`, `filter`, `map`
* une boucle simple

Exemple :

```js
const tasks = [];
tasks.push({ title: "Apprendre Alpine", done: false });
```

C’est obligatoire parce qu’on va faire :

* Todo list
* Blog mock
* DataTable
* Liste de courses
* Tracker de paris

Tout ça, c’est des tableaux.

---

### 3.6 Événements (event handling)

Tu dois comprendre ce que veut dire :

* “au clic”
* “à la saisie”
* “au submit”

Même sans connaître `addEventListener`, tu dois comprendre la logique.

Dans Alpine, c’est simplifié avec :

* `@click`
* `@input`
* `@submit.prevent`

---

## 4) Prérequis utiles (mais pas obligatoires au départ)

Ces notions sont très utiles, mais tu peux les apprendre pendant la formation :

### JSON

JSON = format de données (texte structuré).

Utile pour :

* export/import
* persistance
* stockage local

### localStorage

Stockage dans le navigateur.

Utile pour :

* garder une todo list
* sauvegarder des préférences UI

### Accessibilité (A11Y)

Tu n’as pas besoin d’être expert, mais tu dois accepter une règle :

> une UI pro doit fonctionner au clavier.

On va t’apprendre ça dans les ateliers.

---

## 5) Les erreurs les plus fréquentes (et comment les corriger)

### Erreur 1 — Confondre “ça marche” avec “c’est propre”

Beaucoup d’étudiants sont contents quand ça marche.

Mais en production, tu veux :

* lisible
* stable
* maintenable

Alpine te donne de la vitesse, mais toi tu dois apporter la discipline.

---

### Erreur 2 — Ne pas comprendre le scope

Scope = zone où une variable existe.

Si tu ne comprends pas ça, tu vas avoir :

* `open is not defined`
* des comportements incohérents

Règle simple :

> Tout ce qui est dans `x-data` est visible uniquement dans ses enfants HTML.

---

### Erreur 3 — Mettre trop de logique dans les attributs

Exemple typique :

```html
<button @click="a = a + 1; b = b + 2; c = computeSomething(); if (...) ...">
```

Ça devient illisible.

Solution pro : mettre une fonction dans `x-data` :

```html
<div x-data="menuComponent()">
  <button @click="toggle()">Menu</button>
</div>
```

Et `menuComponent()` contient la logique.

---

### Erreur 4 — Oublier que `x-html` est dangereux

On le répète volontairement.

`x-html` injecte du HTML.
Si tu mets du contenu utilisateur dedans : risque XSS.

En entreprise, une faille XSS, c’est une vraie vulnérabilité.

---

## 6) Mini exemple complet (prérequis en action)

Objectif : montrer les bases JS nécessaires avec Alpine.

On veut :

* un champ texte
* un compteur de caractères
* un message si c’est trop long

```html
<div x-data="{ message: '' }">
  <label>
    Message :
    <input type="text" x-model="message" />
  </label>

  <p>
    Longueur :
    <span x-text="message.length"></span>
  </p>

  <p x-show="message.length > 10">
    Attention : message trop long (max 10 caractères).
  </p>
</div>
```

### Ce que ça utilise comme prérequis

* string (`message`)
* binding (`x-model`)
* propriété (`message.length`)
* condition (`> 10`)
* affichage dynamique (`x-text`, `x-show`)

Donc oui : Alpine est simple… mais il demande des bases propres.

---

## Résumé de la leçon

Pour apprendre Alpine confortablement, tu dois maîtriser :

* HTML : structure + formulaires
* CSS : layout de base (flex/grid)
* JS : variables, objets, fonctions, conditions, tableaux, événements

Et surtout : comprendre le scope et éviter de faire du code illisible dans les attributs.

---

## Mini exercice (rapide)

1. Fais un composant Alpine avec `x-data` contenant :

   * `count: 0`
   * une fonction `increment()`
2. Affiche `count` avec `x-text`
3. Ajoute un bouton “+1” qui appelle `increment()`
4. Ajoute une condition : si `count >= 5`, affiche “Stop”.

---

Prochaine leçon : **Leçon 7 — Préparer l’environnement**
Là on va faire un setup propre : navigateur, DevTools, VSCode, extensions, et surtout les habitudes de debug “pro” qui évitent 80% des galères.
