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

## `x-html` : afficher du HTML (et comprendre le danger XSS)

### Objectif de la leçon

À la fin, tu sauras :

* à quoi sert `x-html`
* quand c’est légitime de l’utiliser
* pourquoi c’est **dangereux**
* ce qu’est une attaque **XSS**
* comment éviter de créer une vulnérabilité en production

Je vais être très clair :
`x-html` est une fonctionnalité utile, mais c’est aussi une des plus risquées si tu l’utilises sans discipline.

---

## 1) `x-html` : définition simple

`x-html` permet d’injecter du **HTML** dans un élément.

Exemple :

```html
<div x-data="{ content: '<strong>Texte en gras</strong>' }">
  <div x-html="content"></div>
</div>
```

Ici, Alpine ne met pas “du texte”, il met du **HTML interprété**.

Donc le résultat visuel sera :

Texte en gras (en gras réel)

---

## 2) Différence entre `x-text` et `x-html` (très important)

### `x-text` (sécurisé par défaut)

Affiche du texte brut.

Si tu fais :

```html
<div x-data="{ content: '<strong>Salut</strong>' }">
  <div x-text="content"></div>
</div>
```

Tu verras littéralement :

`<strong>Salut</strong>`

Le navigateur n’exécute rien.

---

### `x-html` (puissant, mais dangereux)

Interprète le HTML.

Donc :

```html
<div x-data="{ content: '<strong>Salut</strong>' }">
  <div x-html="content"></div>
</div>
```

Tu verras :

Salut (en gras)

---

## 3) Quand est-ce que `x-html` est légitime ?

Tu utilises `x-html` uniquement si tu as une vraie raison.

Exemples légitimes :

* afficher un contenu HTML provenant d’un CMS **de confiance**
* afficher un template HTML que toi-même tu contrôles
* afficher des fragments HTML générés côté serveur, validés
* rendre un contenu “rich text” (texte enrichi) déjà nettoyé

### Exemple typique “safe”

Tu as une liste de messages prédéfinis dans ton code :

```html
<div x-data="{
  templates: {
    ok: '<strong>Succès :</strong> opération terminée.',
    warn: '<strong>Attention :</strong> vérifie tes données.'
  },
  current: 'ok'
}">
  <div x-html="templates[current]"></div>
</div>
```

Ici, tu contrôles tout.
Donc le risque est faible.

---

## 4) Maintenant le point critique : le danger XSS

### 4.1 Définition de XSS

XSS = Cross-Site Scripting.

C’est une attaque où un attaquant arrive à injecter du code dans ton site, généralement via :

* un champ de formulaire
* une URL
* un commentaire
* une donnée stockée en base
* un contenu récupéré via API

Et ce code s’exécute ensuite dans le navigateur des utilisateurs.

### Ce que ça signifie concrètement

Une faille XSS peut permettre :

* voler des cookies de session
* voler des tokens (JWT, session ID)
* modifier la page affichée
* rediriger l’utilisateur
* exécuter des actions à la place de l’utilisateur

Et dans un contexte pro, ça peut être une compromission totale de comptes.

---

## 5) Exemple simple d’attaque XSS via `x-html` (très parlant)

Imagine un formulaire “bio” où l’utilisateur écrit une description.

Tu fais ça :

```html
<div x-data="{ bio: '' }">
  <textarea x-model="bio"></textarea>

  <h3>Prévisualisation</h3>
  <div x-html="bio"></div>
</div>
```

Un étudiant va dire : “Cool, ça prévisualise en HTML.”

Mais maintenant, un attaquant peut écrire dans le textarea :

```html
<img src="x" onerror="alert('XSS')">
```

Résultat :

* l’image échoue
* `onerror` s’exécute
* le JS se lance dans ta page

Donc oui : ton site vient d’exécuter du code injecté par un utilisateur.

Ce n’est pas un “petit bug”.
C’est une faille de sécurité.

---

## 6) Pourquoi c’est grave (version entreprise)

En entreprise, une faille XSS, c’est souvent :

* un incident de sécurité
* un risque légal (données utilisateurs)
* une perte de confiance
* un audit de conformité raté

Si ton application a :

* des cookies de session
* un token d’auth
* des données personnelles

Une XSS peut être utilisée pour :

* prendre le contrôle d’un compte
* récupérer des infos sensibles
* faire du phishing dans l’interface elle-même

Et surtout : une XSS n’a pas besoin d’être “spectaculaire”.
Même sans `alert()`, un script peut exfiltrer des données en silence.

---

## 7) La règle pro : `x-html` ne doit jamais afficher du contenu utilisateur brut

Je vais le dire clairement :

### Règle absolue

Si une donnée vient de :

* l’utilisateur
* une base de données non maîtrisée
* une API externe
* un CMS où n’importe qui peut écrire

Alors :

> Tu n’affiches pas ça avec `x-html` sans sanitation.

Sanitation = nettoyage / filtrage du HTML pour enlever tout ce qui est dangereux.

---

## 8) “Mais alors comment faire si je veux du HTML enrichi ?”

Très bonne question.
Dans la vraie vie, tu as 3 options sérieuses.

### Option 1 — Tu n’utilises pas `x-html`

Tu affiches en texte brut avec `x-text`.

C’est le choix le plus safe.

---

### Option 2 — Tu utilises un système de rendu contrôlé

Tu autorises uniquement certains tags, par exemple :

* `<strong>`
* `<em>`
* `<p>`
* `<ul><li>`

Et tu supprimes tout le reste.

Mais ça, ça se fait avec un vrai sanitizer (ex: DOMPurify) et une politique stricte.

---

### Option 3 — Tu sanitizes côté serveur

C’est souvent le meilleur choix :

* le serveur nettoie le HTML
* la base stocke du contenu safe
* le front affiche ce contenu safe

Le front ne doit pas être responsable de nettoyer un contenu dangereux.

---

## 9) Mini checklist sécurité avant d’utiliser `x-html`

Avant d’écrire `x-html`, pose-toi ces questions :

| Question                                        | Si la réponse est “oui” | Alors                         |
| ----------------------------------------------- | ----------------------- | ----------------------------- |
| Est-ce que ce contenu vient d’un utilisateur ?  | Oui                     | Danger : pas de `x-html` brut |
| Est-ce que ce contenu vient d’une API externe ? | Oui                     | Danger : pas de `x-html` brut |
| Est-ce que je maîtrise 100% la source ?         | Non                     | Danger                        |
| Est-ce que le HTML est sanitizé ?               | Non                     | Interdit en prod              |
| Est-ce que je peux faire autrement ?            | Oui                     | Fais autrement                |

---

## 10) Exemple “propre” : utiliser `x-html` sans ouvrir la porte à XSS

### Exemple : templates internes uniquement

```html
<div x-data="{
  messageType: 'info',
  messages: {
    info: '<strong>Info :</strong> opération en cours.',
    success: '<strong>OK :</strong> terminé.',
    warning: '<strong>Attention :</strong> vérifie les champs.'
  }
}">
  <select x-model="messageType">
    <option value="info">Info</option>
    <option value="success">Succès</option>
    <option value="warning">Warning</option>
  </select>

  <div x-html="messages[messageType]"></div>
</div>
```

Pourquoi c’est safe ?

* le HTML est codé en dur
* pas d’entrée utilisateur
* pas d’injection

---

## 11) Erreurs fréquentes (et pourquoi elles sont dangereuses)

### Erreur 1 — “C’est juste une preview, c’est pas grave”

Faux.

Même une preview peut :

* voler une session
* injecter une redirection
* tromper l’utilisateur

---

### Erreur 2 — “C’est dans un backoffice interne”

Faux.

Les attaques internes existent :

* comptes compromis
* phishing interne
* utilisateurs malveillants
* droits trop larges

---

### Erreur 3 — “Je filtre juste `<script>`”

Insuffisant.

XSS ne passe pas que par `<script>`.

Exemples :

* `onerror`
* `onclick`
* `onload`
* URLs piégées
* SVG malveillant

Donc un filtre naïf ne suffit pas.

---

## Résumé de la leçon

* `x-html` affiche du HTML interprété.
* C’est utile, mais **risqué**.
* `x-text` est safe par défaut.
* `x-html` + contenu utilisateur brut = **faille XSS**.
* En production, tu dois soit :

  * éviter `x-html`
  * soit sanitiser strictement (idéalement côté serveur)

---

## Mini exercice (pédagogique)

1. Crée un composant avec :

   * `safeContent: "<strong>OK</strong>"`
   * `userContent: ""`
2. Affiche :

   * `safeContent` avec `x-html`
   * `userContent` avec `x-text`
3. Dans `userContent`, tape :

   * `<img src=x onerror=alert('XSS')>`
4. Observe la différence.

But : comprendre pourquoi `x-text` protège et `x-html` ouvre une porte.

---

Prochaine leçon : **Leçon 4 — `x-show` : afficher/masquer un bloc (cas UI + limites)**
On va faire du concret : menus, dropdowns, modals, et surtout les erreurs de logique + accessibilité.
