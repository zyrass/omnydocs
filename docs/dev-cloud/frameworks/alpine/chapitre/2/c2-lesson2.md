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

## `x-text` : afficher du texte proprement (et éviter les affichages “sales”)

### Objectif de la leçon

À la fin, tu sauras :

* afficher une donnée dans l’UI avec `x-text` proprement
* comprendre pourquoi `x-text` est préférable à certaines interpolations “à la main”
* éviter les erreurs classiques (undefined, flash, concat foireuse)
* structurer un affichage professionnel (formatage, fallback, lisibilité)

---

## 1) `x-text` : définition simple

`x-text` sert à **injecter du texte** dans un élément HTML.

C’est l’équivalent de dire :

> “Le contenu de cette balise dépend d’une variable.”

Exemple :

```html
<div x-data="{ name: 'Alain' }">
  <p>Bonjour <span x-text="name"></span></p>
</div>
```

Ici, Alpine met automatiquement `"Alain"` dans le `span`.

---

## 2) Pourquoi `x-text` est important (même si ça paraît basique)

Beaucoup d’étudiants pensent :

“Ok c’est juste afficher une variable, je vois pas l’intérêt.”

Mais en vrai, `x-text` te donne 3 garanties essentielles :

1. **Sécurité de rendu** : Alpine insère du texte, pas du HTML
2. **Réactivité** : si la valeur change, l’UI se met à jour automatiquement
3. **Lisibilité** : tu sais immédiatement ce qui est affiché

### Point sécurité (très important)

`x-text` affiche du texte brut.
Donc si quelqu’un essaie d’injecter du HTML, il sera affiché comme texte, pas exécuté.

C’est exactement ce qu’on veut dans 90% des cas.

---

## 3) `x-text` vs interpolation “brute” : pourquoi Alpine recommande `x-text`

Tu pourrais être tenté de faire :

```html
<p>Bonjour {{ name }}</p>
```

Mais ça, c’est une syntaxe de templating (Blade, Vue, Angular…), pas Alpine.

Alpine n’utilise pas `{{ }}` comme moteur de template.

Donc si tu écris ça dans une page Alpine, ça va juste afficher :

`Bonjour {{ name }}`

Le bon réflexe, c’est `x-text`.

---

## 4) Exemple simple mais réaliste : afficher une carte utilisateur

```html
<div x-data="{ user: { name: 'Alain', role: 'Développeur' } }">
  <h2 x-text="user.name"></h2>
  <p x-text="user.role"></p>
</div>
```

Tu affiches ici des propriétés d’objet.

---

## 5) Les erreurs classiques avec `x-text`

### Erreur 1 — Afficher une variable qui n’existe pas

Exemple :

```html
<div x-data="{ username: 'Alain' }">
  <span x-text="name"></span>
</div>
```

Ici `name` n’existe pas.
Tu risques d’avoir :

* rien affiché
* ou une erreur console selon le contexte

Solution pro : être strict sur le nommage.

---

### Erreur 2 — Afficher `undefined` (le rendu “moche”)

Exemple typique :

```html
<div x-data="{ user: {} }">
  <span x-text="user.name"></span>
</div>
```

`user.name` vaut `undefined`.

Donc l’utilisateur voit un vide, ou pire un affichage incohérent.

#### Solution 1 : fallback simple

```html
<span x-text="user.name ?? 'Inconnu'"></span>
```

`??` = opérateur “nullish coalescing”
Ça signifie : si la valeur est `null` ou `undefined`, alors utilise le fallback.

---

### Erreur 3 — Concaténer n’importe comment

Exemple pas propre :

```html
<span x-text="'Bonjour ' + name + ' !'"></span>
```

Ça marche, mais ça devient vite illisible si tu fais ça partout.

#### Version plus propre (template string)

```html
<span x-text="`Bonjour ${name} !`"></span>
```

C’est plus lisible.

---

## 6) `x-text` et formatage (niveau pro)

Très vite tu vas vouloir afficher des valeurs formatées :

* prix
* pourcentages
* dates
* stats

### Exemple : afficher un montant proprement

```html
<div x-data="{ amount: 1234.5 }">
  <p>
    Total :
    <strong x-text="amount.toFixed(2) + ' €'"></strong>
  </p>
</div>
```

Ici tu forces 2 décimales.

---

### Exemple : formatage monnaie “pro” (Intl.NumberFormat)

C’est une vraie bonne pratique.

```html
<div x-data="{
  amount: 1234.5,
  formatEUR(value) {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR'
    }).format(value);
  }
}">
  <p>Total : <strong x-text="formatEUR(amount)"></strong></p>
</div>
```

Pourquoi c’est mieux ?

Parce que ça gère :

* espaces
* virgules
* symboles
* conventions locales

C’est propre.

---

## 7) `x-text` et accessibilité (oui, même ici)

Une UI pro ne doit pas être “juste jolie”, elle doit être compréhensible.

Exemple :

```html
<div x-data="{ count: 3 }">
  <p>
    Articles dans le panier :
    <span x-text="count"></span>
  </p>
</div>
```

C’est correct.

Mais si tu veux être plus clair :

```html
<div x-data="{ count: 3 }">
  <p x-text="`Articles dans le panier : ${count}`"></p>
</div>
```

Tu évites un découpage inutile, et ton texte est complet.

---

## 8) Piège UX : texte visible avant Alpine (flash)

Si Alpine n’a pas encore démarré, tu peux avoir un moment où le texte est vide ou pas prêt.

Solution : `x-cloak` (on le détaillera plus loin, mais tu dois connaître l’idée).

Exemple :

```html
<p x-cloak x-text="name"></p>
```

Et dans ton CSS global :

```css
[x-cloak] { display: none !important; }
```

---

## 9) Mini exemple complet (propre + réaliste)

Objectif : afficher un profil utilisateur avec fallback.

```html
<div x-data="{
  user: {
    name: 'Alain',
    job: 'Fullstack',
    score: 92
  }
}">
  <h2 x-text="user.name ?? 'Utilisateur'"></h2>

  <p>
    Métier :
    <strong x-text="user.job ?? 'Non renseigné'"></strong>
  </p>

  <p>
    Score :
    <strong x-text="`${user.score}/100`"></strong>
  </p>
</div>
```

---

## Résumé de la leçon

`x-text` sert à afficher du texte dynamiquement.

C’est une directive simple, mais fondamentale car elle apporte :

* réactivité
* lisibilité
* sécurité (texte brut)
* rendu propre avec fallback et formatage

Et surtout : c’est le standard Alpine pour afficher une valeur.

---

## Mini exercice (rapide)

1. Crée un composant `x-data` avec :

   * `user: { name: 'Jean', age: 20 }`
2. Affiche :

   * “Nom : Jean”
   * “Âge : 20”
3. Ajoute un fallback si `user.name` est vide :

   * afficher “Inconnu”
4. Bonus : affiche un message :

   * “Majeur” si âge >= 18
   * sinon “Mineur”

---

Prochaine leçon : **Leçon 3 — `x-html` : afficher du HTML (et comprendre le danger XSS)**
Là on va rentrer dans un sujet sérieux : pourquoi c’est utile, mais pourquoi c’est dangereux si tu ne sais pas ce que tu fais.
