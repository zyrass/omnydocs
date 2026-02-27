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

## Checklist “avant prod” : qualité, debug, cohérence

### Objectif de la leçon

À la fin, tu vas avoir une checklist claire et applicable pour livrer un projet Alpine :

* propre
* stable
* maintenable
* cohérent
* accessible
* sans faille évidente

Ce n’est pas une leçon “théorique”.
C’est une procédure pro, exactement comme en entreprise avant une release.

---

# 1) Le principe : “avant prod” = tu réduis les risques

Mettons les choses au clair :

* en dev, tu peux accepter du bricolage
* en prod, tu dois accepter seulement :

  * ce que tu comprends
  * ce que tu peux maintenir
  * ce que tu peux justifier

L’objectif de cette checklist :

* éviter les bugs stupides
* éviter les comportements incohérents
* éviter les failles faciles
* éviter le “ça marche chez moi”

---

# 2) Checklist Qualité Code (Alpine)

## A) Structure du projet

Tu dois pouvoir répondre à ces questions en 10 secondes :

* où sont les stores ?
* où sont les composants ?
* où sont les plugins ?
* où est le point d’entrée ?

Exemple attendu :

* `src/alpine/index.js` = bootstrap
* `src/alpine/stores/` = stores
* `src/alpine/components/` = composants

Si tu ne sais pas où chercher :

* ton futur toi va souffrir.

---

## B) Composants lisibles

Chaque composant doit :

* être court
* avoir une API claire
* ne pas mélanger 50 responsabilités

### Règle simple

Si un `x-data` dépasse 80 lignes :

* tu dois te poser la question du découpage.

---

## C) `x-for` et performance

Avant prod, vérifie :

* `:key` partout
* pas de `filter()` inline dans le template
* tri sans muter la source (`[...arr].sort()`)

Si liste énorme :

* pagination simple
* debounce sur recherche

---

# 3) Checklist UX (comportements attendus)

## Menus / dropdown

* se ferme au clic extérieur
* se ferme avec Escape
* focus visible
* pas de menu “bloqué ouvert”

## Modals

* Escape ferme
* click outside ferme (souvent)
* focus trap
* focus restore
* pas de scroll derrière (bonus)

## Formulaires

* submit prevent
* validation minimale
* reset propre
* messages d’erreur lisibles

---

# 4) Checklist Accessibilité (minimum pro)

Tu dois tester au clavier uniquement :

* Tab
* Shift+Tab
* Enter
* Escape

Et tu dois vérifier :

* focus visible partout
* pas de `div @click` en bouton
* aria-expanded sur dropdown
* role dialog + aria-modal sur modal
* tabs cohérentes (aria-selected)

Si tu fais ça, tu es déjà au-dessus de 80% des sites.

---

# 5) Checklist Sécurité (anti catastrophes)

## A) Interdit : `x-html` sur input utilisateur

C’est le classique.

Si tu vois :

```html
<div x-html="comment"></div>
```

et `comment` vient d’un utilisateur :

* c’est une faille.

## B) localStorage : pas de secrets

Tu peux persister :

* thème
* préférences UI
* favoris

Tu ne dois jamais persister :

* token
* password
* info sensible

## C) Pas de confiance dans le front

Même si tu valides côté front :

* backend validation obligatoire

---

# 6) Checklist Debug (propre et efficace)

## A) `x-cloak`

Tous les éléments `x-show` importants doivent être couverts par :

```css
[x-cloak] { display:none !important; }
```

Sinon tu as un flash moche au chargement.

## B) Logs temporaires

En prod :

* pas de `console.log()` partout

Tu nettoies.

## C) Vérifier les erreurs console

Avant prod, tu ouvres DevTools et tu vérifies :

* aucun warning
* aucune erreur

C’est bête mais 50% des bugs se voient là.

---

# 7) Checklist Build (Vite)

Tu dois faire :

```bash
npm run build
npm run preview
```

Pourquoi ?
Parce que parfois :

* en dev ça marche
* en build ça casse (imports, chemins, assets)

Donc tu testes le build.

---

# 8) Checklist “Cohérence UI” (le détail qui fait pro)

Tu vérifies :

* mêmes espacements
* mêmes styles de boutons
* mêmes bordures
* mêmes transitions
* mêmes comportements

Tu ne veux pas :

* un modal qui se ferme avec Escape
* un autre modal qui ne se ferme pas

Cohérence = sensation de produit fini.

---

# 9) Tableau “Avant prod” (résumé visuel)

| Catégorie | À vérifier                             | Pourquoi c’est critique |
| --------- | -------------------------------------- | ----------------------- |
| Code      | structure fichiers + composants courts | maintenance             |
| Rendu     | `x-for` + `:key` + tri propre          | bugs invisibles         |
| UX        | dropdown/modal cohérents               | confiance utilisateur   |
| A11Y      | clavier + focus visible                | utilisabilité réelle    |
| Sécurité  | pas de `x-html` user input             | XSS                     |
| Persist   | pas de secrets                         | fuite possible          |
| Build     | `npm run build`                        | éviter crash en prod    |
| Debug     | console clean                          | qualité                 |

---

# 10) Mini exercice (obligatoire)

### Exercice A — Audit ton projet “AAA Theme Test”

Tu prends ta page, et tu coches :

* focus visible OK
* modal trap OK
* dropdown close OK
* `x-cloak` OK
* aucun `x-html` dangereux

### Exercice B — Ajoute une “Release checklist” dans ton repo

Crée un fichier :

`CHECKLIST_RELEASE.md`

Et tu colles cette checklist dedans.

Ça te donne une discipline pro.

---

# Résumé de la leçon

* “avant prod” = réduire les risques
* la checklist évite les erreurs idiotes
* accessibilité + sécurité + cohérence = produit vendable

---

# Livrable final du Chapitre 12

Tu dois maintenant avoir :

* un starter Alpine + Vite + Tailwind propre
* des composants structurés
* une page de test AAA
* une checklist release

Tu es officiellement en mode “production-ready”.

---

## Étape suivante logique (et là c’est le vrai boss final)

**Chapitre final — Component Library (pack réutilisable)**
On va extraire tes composants (navbar, dropdown, modal, tabs, accordéon, toast, datatable, theme switcher AAA) en version pack vendable avec API + exemples + checklist accessibilité.

On passe du “projet” à la “lib”.
