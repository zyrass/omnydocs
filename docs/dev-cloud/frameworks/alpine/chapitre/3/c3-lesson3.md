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

## `x-model` : synchroniser les inputs (text, checkbox, radio, select)

### Objectif de la leçon

À la fin, tu sauras :

* utiliser `x-model` pour lier un champ à ton state
* comprendre la différence entre `x-model` et `@input`
* gérer les types d’inputs les plus importants :

  * texte
  * checkbox
  * radio
  * select
* éviter les pièges : valeurs incohérentes, types mal compris, state “sale”
* construire un formulaire propre et stable

`x-model` est une des directives les plus rentables d’Alpine : elle te fait gagner du temps immédiatement.

---

## 1) `x-model` : définition simple

`x-model` relie la valeur d’un champ HTML à une variable dans ton state.

Ça veut dire :

* quand l’utilisateur tape → la variable se met à jour
* quand tu modifies la variable → le champ se met à jour

C’est une synchronisation dans les deux sens.

### Analogie simple

`x-model` c’est comme un câble entre ton input et ton state :

* tu changes un côté → l’autre suit automatiquement

---

## 2) Exemple minimal : input texte

```html
<div x-data="{ name: '' }">
  <input type="text" x-model="name" placeholder="Ton prénom" />

  <p>Bonjour <strong x-text="name"></strong></p>
</div>
```

Ici, tu as :

* state : `name`
* UI : input + affichage
* synchronisation automatique

---

## 3) `x-model` vs `@input` : quand utiliser quoi ?

### Avec `@input`

Tu fais toi-même le boulot :

```html
<input @input="name = $event.target.value" />
```

### Avec `x-model`

Alpine le fait pour toi :

```html
<input x-model="name" />
```

Règle simple :

* `x-model` = standard, propre, rapide
* `@input` = utile quand tu veux intercepter et faire une logique spéciale

Exemple de logique spéciale :

* forcer en majuscules
* filtrer certains caractères
* debounce manuel (on verra plus tard)

---

# 4) Input texte (avec nettoyage pro)

Le piège classique : accepter des espaces inutiles.

Tu peux gérer ça au submit, mais tu peux aussi normaliser.

### Exemple : trim au moment de l’affichage

```html
<div x-data="{ name: '' }">
  <input x-model="name" placeholder="Ton prénom" />

  <p x-text="`Bonjour ${name.trim()}`"></p>
</div>
```

Tu gardes le state brut, mais tu affiches propre.

---

# 5) Checkbox (booléen)

Une checkbox est parfaite pour un booléen.

### Exemple

```html
<div x-data="{ accepted: false }">
  <label>
    <input type="checkbox" x-model="accepted" />
    J’accepte les conditions
  </label>

  <p>
    Statut :
    <strong x-text="accepted ? 'Accepté' : 'Refusé'"></strong>
  </p>

  <button :disabled="!accepted">
    Continuer
  </button>
</div>
```

### Ce que tu dois comprendre

* `accepted` vaut `true` ou `false`
* tu peux utiliser `:disabled` directement

C’est un pattern très pro.

---

# 6) Radio (choix unique)

Les radios servent à choisir une seule option.

### Exemple

```html
<div x-data="{ plan: 'basic' }">
  <p>Choisis ton plan :</p>

  <label>
    <input type="radio" value="basic" x-model="plan" />
    Basic
  </label>

  <label>
    <input type="radio" value="pro" x-model="plan" />
    Pro
  </label>

  <label>
    <input type="radio" value="enterprise" x-model="plan" />
    Enterprise
  </label>

  <p>
    Plan choisi :
    <strong x-text="plan"></strong>
  </p>
</div>
```

### Piège classique

Les valeurs des radios sont des strings.

Même si tu mets `value="1"`, tu récupères `"1"` (string), pas `1` (number).

Tu dois en être conscient quand tu fais des comparaisons.

---

# 7) Select (liste déroulante)

### Exemple simple

```html
<div x-data="{ country: 'FR' }">
  <select x-model="country">
    <option value="FR">France</option>
    <option value="BE">Belgique</option>
    <option value="CH">Suisse</option>
  </select>

  <p>Pays : <strong x-text="country"></strong></p>
</div>
```

---

# 8) Formulaire complet (propre + réaliste)

Objectif : formulaire utilisateur simple avec validation front.

* prénom obligatoire
* email obligatoire
* conditions acceptées
* plan choisi

```html
<form x-data="{
  name: '',
  email: '',
  accepted: false,
  plan: 'basic',

  get isValid() {
    return this.name.trim().length > 0
      && this.email.trim().length > 0
      && this.accepted === true;
  },

  submit() {
    if (!this.isValid) return;

    console.log('Formulaire envoyé :', {
      name: this.name.trim(),
      email: this.email.trim(),
      plan: this.plan,
      accepted: this.accepted
    });

    // reset propre
    this.name = '';
    this.email = '';
    this.accepted = false;
    this.plan = 'basic';
  }
}" @submit.prevent="submit()">

  <div>
    <label>
      Prénom
      <input type="text" x-model="name" placeholder="Jean" />
    </label>
  </div>

  <div style="margin-top: 8px;">
    <label>
      Email
      <input type="email" x-model="email" placeholder="jean@mail.com" />
    </label>
  </div>

  <div style="margin-top: 8px;">
    <label>
      <input type="checkbox" x-model="accepted" />
      J’accepte les conditions
    </label>
  </div>

  <div style="margin-top: 8px;">
    <p>Plan :</p>

    <label>
      <input type="radio" value="basic" x-model="plan" />
      Basic
    </label>

    <label>
      <input type="radio" value="pro" x-model="plan" />
      Pro
    </label>
  </div>

  <button
    type="submit"
    :disabled="!isValid"
    style="margin-top: 12px;"
  >
    Envoyer
  </button>

  <p style="margin-top: 8px;">
    Statut :
    <strong x-text="isValid ? 'Formulaire valide' : 'Formulaire incomplet'"></strong>
  </p>
</form>
```

### Points importants (niveau pro)

* on utilise `@submit.prevent`
* on centralise la validation dans `isValid`
* on reset proprement
* on trim avant d’envoyer

Et surtout : ton HTML reste lisible.

---

## 9) Pièges fréquents avec `x-model`

### Piège 1 — state incohérent

Exemple : tu reset `name` mais tu oublies `accepted`.

Résultat : le formulaire reste “valide” alors qu’il ne devrait pas.

Solution : reset complet et cohérent.

---

### Piège 2 — validation dispersée partout

Éviter :

* `:disabled="name !== '' && email !== '' && accepted"`
* répétée 4 fois dans le HTML

Solution : centraliser dans un getter `isValid`.

---

### Piège 3 — types non maîtrisés

* radio = string
* select = string
* checkbox = bool

Donc attention aux comparaisons strictes.

---

## Résumé de la leçon

* `x-model` synchronise un input avec ton state (dans les deux sens)
* c’est plus simple et plus propre que `@input`
* tu sais gérer :

  * texte
  * checkbox
  * radio
  * select
* bonne pratique : validation centralisée, reset cohérent, trim

---

## Mini exercice (obligatoire)

1. Crée un formulaire avec :

   * `username` (text)
   * `newsletter` (checkbox)
   * `role` (select : user/admin)
2. Affiche en live un résumé :

   * “Nom : …”
   * “Newsletter : oui/non”
   * “Rôle : …”
3. Désactive le bouton Envoyer si username vide

---

Prochaine leçon : **Leçon 4 — Formulaires : submit propre et UX (validation simple côté front)**
On va apprendre à faire un vrai submit propre, avec erreurs affichées, messages utilisateur, et patterns pro pour éviter les formulaires “fragiles”.
