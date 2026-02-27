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

## Sécurité : pièges `x-html` (cas réel, prévention)

### Objectif de la leçon

À la fin, tu vas comprendre :

* ce qu’est une attaque **XSS** (Cross-Site Scripting)
* pourquoi `x-html` est une zone rouge
* comment une donnée “innocente” peut devenir du code exécuté
* les règles pro à appliquer pour ne pas livrer une faille
* comment sécuriser proprement (sans paniquer)

Cette leçon est non négociable.
Parce que la plupart des failles web ne viennent pas d’un “hack génial”.
Elles viennent d’un dev qui a fait `x-html` sur une string utilisateur.

---

# 1) Définition simple : XSS

XSS signifie **Cross-Site Scripting**.

Traduction simple :

> Un attaquant arrive à injecter du JavaScript dans ton site, et ton site l’exécute.

Donc ce n’est pas “un bug d’affichage”.
C’est un bug de sécurité.

---

## 2) Analogie simple (pour comprendre vite)

Imagine ton site comme un restaurant.

* toi = le chef
* l’utilisateur = un client

Normalement :

* le client te donne une commande (texte)
* toi tu cuisines (tu affiches)

Avec XSS :

* le client glisse un “petit papier” dans la commande
* et ce papier dit au serveur :
  “Donne-moi les clés de la cuisine et les recettes.”

Et toi, tu obéis, parce que tu n’as pas vérifié.

---

# 3) Pourquoi `x-html` est dangereux

`x-text` affiche du texte.
Donc même si l’utilisateur écrit :

```html
<script>alert(1)</script>
```

ça s’affiche comme du texte, sans exécuter.

Mais `x-html` injecte du HTML dans le DOM.

Donc si tu fais :

```html
<div x-html="content"></div>
```

Et que `content` contient du code malveillant…
tu viens d’ouvrir la porte.

---

# 4) Exemple : démonstration d’une faille (à ne jamais faire)

## Code vulnérable

```html
<div x-data="{ message: '' }" style="max-width:920px; margin:0 auto; padding:16px;">
  <h2>Démo XSS (vulnérable)</h2>

  <input
    type="text"
    x-model="message"
    placeholder="Tape un message..."
    style="padding:10px; border:1px solid #ddd; border-radius:10px; width:100%;"
  />

  <p style="color:#666; margin-top:10px;">Rendu :</p>

  <div style="border:1px solid #eee; border-radius:12px; padding:12px;">
    <div x-html="message"></div>
  </div>
</div>
```

---

## Payload d’attaque simple

L’attaquant tape :

```html
<img src="x" onerror="alert('XSS')">
```

Résultat :

* le navigateur tente de charger l’image
* ça échoue
* `onerror` s’exécute
* tu as du JavaScript exécuté

Ce n’est pas “juste une alerte”.
Dans la vraie vie ça peut être :

* vol de session (selon contexte)
* actions en ton nom
* extraction de données visibles
* redirections
* phishing interne

---

# 5) Règle pro numéro 1 : `x-html` doit être rare

Si tu peux faire avec `x-text`, fais avec `x-text`.

### Exemple safe

```html
<div x-text="message"></div>
```

Là, le HTML est neutralisé.

---

# 6) Cas légitime : quand `x-html` est acceptable

Oui, il y a des cas où `x-html` est utile :

* afficher un contenu HTML venant d’un CMS
* afficher une description formatée (markdown rendu)
* afficher un template de contenu contrôlé

Mais dans ces cas :

1. le contenu doit être **de confiance**
2. ou il doit être **sanitisé** (nettoyé)

---

# 7) Termes importants expliqués

## “Sanitiser” (sanitize)

Ça veut dire :

> nettoyer une entrée HTML pour retirer les balises dangereuses et les attributs dangereux

Exemple :

* enlever `<script>`
* enlever `onerror=...`
* enlever `onclick=...`
* enlever `javascript:...`

---

## “Échapper” (escape)

Ça veut dire :

> transformer les caractères HTML en texte

Exemple :

* `<` devient `&lt;`
* `>` devient `&gt;`

Donc ça s’affiche sans être interprété.

---

# 8) Protection réaliste dans Alpine (ce que tu dois faire)

## Solution 1 — Ne jamais utiliser `x-html` sur une donnée utilisateur

C’est la meilleure.

Tu affiches avec `x-text`.

---

## Solution 2 — Whitelist stricte (contenu contrôlé)

Si tu as un set de contenus “internes” (non user input) :

```js
const templates = {
  welcome: "<strong>Bienvenue</strong> sur le dashboard",
  info: "<em>Info</em> : maintenance à 22h",
};
```

Là tu peux faire `x-html="templates.welcome"` car tu contrôles la source.

---

## Solution 3 — Sanitizer (si contenu externe)

Dans un projet réel, tu utilises une lib comme DOMPurify.

Mais dans une formation Alpine “pure”, tu dois au moins comprendre le principe.

Tu peux faire une version “pédagogique” :

### Exemple pédagogique (non parfait)

```js
function naiveSanitize(html) {
  return html
    .replaceAll(/<script.*?>.*?<\/script>/gi, '')
    .replaceAll(/on\w+=".*?"/gi, '');
}
```

Mais je te le dis clairement :

* ce n’est pas suffisant en prod
* c’est juste pour expliquer le concept

---

# 9) Le piège moderne : “c’est du front, donc c’est safe”

Non.

Un front peut être une faille grave.

Pourquoi ?
Parce que le front :

* manipule le DOM
* affiche des données
* gère parfois des actions sensibles

Donc une injection peut :

* détourner ton UI
* tromper l’utilisateur
* voler des infos visibles

---

# 10) Ce qu’il ne faut JAMAIS faire (liste courte, mais brutale)

* stocker un token en localStorage “par facilité”
* afficher du contenu utilisateur via `x-html`
* faire confiance à un champ “readonly”
* croire que “ça vient de mon API donc c’est safe”
  (si l’API stocke des données utilisateur, c’est potentiellement infecté)

---

# 11) Exemple “pro” : Blog mock avec rendu safe

Tu as un blog avec :

* title (texte)
* excerpt (texte)
* content (html contrôlé)

### Exemple :

```html
<div x-data="BlogSafe()">
  <template x-for="post in posts" :key="post.id">
    <article style="border:1px solid #eee; border-radius:12px; padding:12px; margin-top:10px;">
      <h3 style="margin:0;" x-text="post.title"></h3>

      <p style="color:#666;" x-text="post.excerpt"></p>

      <!-- OK uniquement si post.content est contrôlé/sanitisé -->
      <div x-html="post.content"></div>
    </article>
  </template>
</div>

<script>
  function BlogSafe() {
    return {
      posts: [
        {
          id: 1,
          title: "Article 1",
          excerpt: "Intro simple en texte.",
          content: "<p><strong>Contenu HTML</strong> contrôlé.</p>",
        },
      ],
    };
  }
</script>
```

Règle :

* `title` et `excerpt` => `x-text`
* `content` => `x-html` uniquement si contrôlé

---

# 12) Mini exercice (obligatoire)

### Exercice A — Transformer un rendu vulnérable en rendu safe

Tu as :

```html
<div x-html="comment"></div>
```

Tu dois le remplacer par :

* `x-text`
  ou
* sanitize + `x-html`

### Exercice B — Liste de commentaires

* tu ajoutes 5 commentaires
* tu affiches en `x-text`
* tu testes un payload `<img onerror=...>`

Tu dois constater que ça ne s’exécute pas.

---

# Résumé de la leçon (à mémoriser)

* XSS = injection de JavaScript exécuté dans ton site
* `x-html` est dangereux
* `x-text` est safe par défaut
* `x-html` uniquement sur contenu contrôlé ou sanitisé
* backend validation et nettoyage restent essentiels

---

### Étape suivante logique

Chapitre 12 — Production Ready
**Leçon 5 — Accessibilité finale : modals/tabs/menu (ARIA, focus, navigation clavier)**
On fait la checklist finale “composants prêts pour la prod”.
