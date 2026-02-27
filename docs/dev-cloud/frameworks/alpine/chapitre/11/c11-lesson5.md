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

## Mask : inputs contrôlés (téléphone, date, formats)

### Objectif de la leçon

À la fin, tu sauras :

* comprendre ce qu’est un **input mask** (masque de saisie)
* utiliser le plugin **Mask** d’Alpine
* créer des champs “pro” :

  * téléphone
  * date
  * code postal
  * carte (format)
* éviter les pièges :

  * faux sentiment de validation
  * masques trop stricts
  * accessibilité oubliée
  * données incohérentes côté backend

Cette leçon est essentielle car dans la vraie vie…
les formulaires sont une source infinie de bugs.

---

## 1) C’est quoi un masque de saisie ?

Un masque de saisie, c’est une règle qui guide l’utilisateur pendant qu’il tape.

Exemple téléphone FR :

```
06 12 34 56 78
```

Donc le masque impose :

* espaces
* longueur
* format

Mais attention :

> un masque n’est pas une validation complète

C’est juste une aide de saisie.

---

## 2) Analogie simple

Imagine que tu remplis un formulaire papier.

Si la case “téléphone” est pré-imprimée comme ça :

```
__ __ __ __ __
```

Tu comprends immédiatement :

* combien de chiffres tu dois écrire
* comment les séparer

Mask fait pareil en numérique.

---

# 3) Pourquoi c’est utile ?

Sans masque :

* l’utilisateur tape n’importe comment
* tu reçois des données incohérentes
* tu passes ton temps à nettoyer côté backend

Avec masque :

* saisie guidée
* meilleure UX
* moins d’erreurs

Mais il faut le faire intelligemment.

---

# 4) Installation du plugin Mask (CDN)

Tu charges :

1. Alpine core
2. Mask plugin

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/mask@3.x.x/dist/cdn.min.js"></script>
```

---

# 5) Exemple 1 : Téléphone FR (simple)

### Objectif

Saisie formatée en direct.

---

## Code complet (copie-colle)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Plugin Mask — Téléphone FR</h2>

  <div x-data="{ phone: '' }" style="margin-top:12px; border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <label style="display:flex; flex-direction:column; gap:8px;">
      <strong>Téléphone</strong>

      <input
        type="text"
        x-model="phone"
        x-mask="99 99 99 99 99"
        placeholder="06 12 34 56 78"
        inputmode="numeric"
        style="padding:10px; border:1px solid #ddd; border-radius:10px;"
      />

      <span style="color:#666;">
        Valeur : <strong x-text="phone"></strong>
      </span>
    </label>
  </div>
</div>
```

---

# 6) Explication : ce que signifie `x-mask="99 99 99 99 99"`

Le masque utilise des symboles :

* `9` = chiffre obligatoire
* les espaces sont des séparateurs

Donc :

* tu ne peux pas taper de lettre
* tu es guidé sur 10 chiffres

---

# 7) Exemple 2 : Date (JJ/MM/AAAA)

### Objectif

Une date lisible.

---

## Code complet

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Mask — Date (JJ/MM/AAAA)</h2>

  <div x-data="{ date: '' }" style="margin-top:12px; border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <label style="display:flex; flex-direction:column; gap:8px;">
      <strong>Date</strong>

      <input
        type="text"
        x-model="date"
        x-mask="99/99/9999"
        placeholder="31/12/2026"
        inputmode="numeric"
        style="padding:10px; border:1px solid #ddd; border-radius:10px;"
      />

      <span style="color:#666;">
        Valeur : <strong x-text="date"></strong>
      </span>
    </label>
  </div>
</div>
```

---

# 8) Exemple 3 : Code postal (France)

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Mask — Code postal</h2>

  <div x-data="{ zip: '' }" style="margin-top:12px; border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <label style="display:flex; flex-direction:column; gap:8px;">
      <strong>Code postal</strong>

      <input
        type="text"
        x-model="zip"
        x-mask="99999"
        placeholder="69000"
        inputmode="numeric"
        style="padding:10px; border:1px solid #ddd; border-radius:10px;"
      />

      <span style="color:#666;">
        Valeur : <strong x-text="zip"></strong>
      </span>
    </label>
  </div>
</div>
```

---

# 9) Exemple 4 : Carte bancaire (format visuel)

Attention : ce n’est pas une validation de carte.
C’est juste un format de saisie.

```html
<div style="max-width: 920px; margin: 0 auto; padding: 16px;">
  <h2>Mask — Carte (format)</h2>

  <div x-data="{ card: '' }" style="margin-top:12px; border:1px solid #eee; border-radius:16px; padding:16px; background:#fff;">
    <label style="display:flex; flex-direction:column; gap:8px;">
      <strong>Numéro de carte</strong>

      <input
        type="text"
        x-model="card"
        x-mask="9999 9999 9999 9999"
        placeholder="1234 5678 9012 3456"
        inputmode="numeric"
        style="padding:10px; border:1px solid #ddd; border-radius:10px;"
      />

      <span style="color:#666;">
        Valeur : <strong x-text="card"></strong>
      </span>
    </label>
  </div>
</div>
```

---

# 10) Point ultra important : Mask ≠ Validation

C’est LE piège numéro 1.

Exemple :

* `31/99/0000` respecte le masque
* mais ce n’est pas une date valide

Donc tu dois toujours valider :

* côté front (minimum)
* côté backend (obligatoire)

---

## Validation simple (exemple date)

Tu peux faire :

```html
<div x-data="DateCheck()">
  <input x-model="date" x-mask="99/99/9999" />
  <p x-show="date && !isValid" style="color:#b00;">
    Date invalide
  </p>
</div>

<script>
  function DateCheck() {
    return {
      date: '',
      get isValid() {
        // Validation simplifiée (exemple pédagogique)
        const m = this.date.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
        if (!m) return false;

        const day = Number(m[1]);
        const month = Number(m[2]);
        const year = Number(m[3]);

        if (month < 1 || month > 12) return false;
        if (day < 1 || day > 31) return false;
        if (year < 1900 || year > 2100) return false;

        return true;
      },
    };
  }
</script>
```

C’est une validation simple, pas parfaite, mais elle montre l’idée.

---

# 11) Accessibilité et UX (ce qu’on doit faire)

## A) Toujours un label

Ne fais pas un input sans label.

## B) `inputmode="numeric"`

Sur mobile, ça affiche le clavier numérique.

## C) Placeholder = exemple, pas vérité

Le placeholder est un guide.
Mais la vraie règle doit être claire.

---

# 12) Pièges fréquents

## Piège A — masque trop strict

Si tu imposes un format ultra précis, tu bloques des utilisateurs.

Exemple téléphone :

* certains vont écrire `+33`
* d’autres `0033`

Donc parfois tu dois accepter plusieurs formats côté backend.

---

## Piège B — données incohérentes envoyées au backend

Même si c’est masqué, tu dois nettoyer.

Exemple téléphone :

* tu peux retirer les espaces avant d’envoyer.

---

## Piège C — croire que Mask “sécurise”

Mask n’empêche pas :

* un user malveillant
* un script
* une requête API

Donc backend validation obligatoire.

---

# 13) Mini exercice (obligatoire)

### Exercice A — Nettoyage avant submit

Avant d’envoyer le téléphone, retire les espaces.

Indice :

```js
phone.replaceAll(' ', '')
```

### Exercice B — Masque + persistance

Persiste un champ “téléphone” avec `$persist`.

### Exercice C — Formulaire complet

Crée un mini formulaire :

* prénom
* téléphone (mask)
* date (mask)
  Et un bouton submit qui affiche un objet JSON.

---

## Résumé de la leçon

* Mask guide la saisie et améliore l’UX
* mais ne remplace jamais une validation réelle
* parfait pour téléphone, date, formats
* pense accessibilité (label + inputmode)

---

### Étape suivante logique

Chapitre 11 — Plugins officiels & Accessibilité
**Atelier UI #9 — Page “AAA Theme Test”**
On assemble tout : modal, tabs, menu, formulaire, checklist AAA, et on teste comme un produit.
