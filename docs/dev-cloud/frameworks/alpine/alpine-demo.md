---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Présentation

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Introduction à la formation

!!! quote "Vue d'ensemble du projet de formation"
    Cette formation représente **la première ressource pédagogique française offrant une couverture intégrale d'Alpine.js**, atteignant **100% des fonctionnalités** du framework. Elle s'articule autour d'environ 25 chapitres progressifs, répartis en deux grandes parties : 
    
    - **15 chapitres fondamentaux** 
    - **10 chapitres avancés**.

L'approche pédagogique se distingue par **une double stratégie d'apprentissage**.
    
> D'une part, un projet fil rouge appelé "**Clicker Hero RPG**" traverse l'intégralité de la formation, permettant de voir comment chaque concept s'intègre dans une application réelle et complète. Ce projet évolue chapitre après chapitre, incorporant progressivement toutes les fonctionnalités Alpine.js jusqu'à devenir une application web moderne et pleinement fonctionnelle.

> D'autre part, et c'est là un élément pédagogique crucial, chaque concept est d'abord expliqué à travers des exemples variés et indépendants du projet fil rouge. Cette approche garantit que l'apprenant comprend le concept lui-même, dans sa généralité, plutôt que simplement son application spécifique dans notre jeu.

Cette formation doit permettre à un développeur de pouvoir transférer ses connaissances à n'importe quel type d'application, qu'il s'agisse d'un _dashboard d'administration_, d'_un site e-commerce_, d'_une application de gestion de tâches_, ou de tout autre projet web.

### Le principe de la double démonstration

!!! example "Exemple théorique"

    _Prenons un exemple concret pour illustrer cette méthodologie. Lorsque nous enseignons la directive `x-show`, nous commençons par des exemples simples et universels. Nous montrons comment **afficher** ou **masquer un message d'alerte**, comment **créer un menu déroulant qui s'ouvre au clic**, comment **gérer l'affichage d'une section de FAQ**. _Ces exemples sont volontairement déconnectés de notre jeu de rôle et représentent des cas d'usage que tout développeur rencontrera dans sa carrière._

> Ce n'est qu'après avoir maîtrisé `x-show` à travers ces exemples variés que nous l'appliquons à notre projet fil rouge.
    
Dans "**Clicker Hero**", nous utiliserons `x-show` pour **afficher conditionnellement** le message de victoire après avoir vaincu un monstre, pour **masquer** ou **révéler des sections d'interface** selon l'écran actif, ou pour **montrer des tooltips d'information**. L'apprenant comprend alors comment le même concept, déjà maîtrisé dans sa généralité, s'applique naturellement à notre contexte spécifique.

!!! info "Cette **double démonstration force la pratique et l'assimilation profonde**"
    Vous ne vous contenterez pas de copier du code pour faire fonctionner le jeu, vous comprendrez réellement pourquoi `x-show` fonctionne ainsi, quand l'utiliser, et comment l'adapter à n'importe quelle situation.
    
    Cette compréhension conceptuelle est ce qui différencie un développeur capable de suivre un tutoriel d'un développeur capable de construire ses propres solutions, vous en l'occurence à l'issue de cette formation.


---
---
---
---
---


## Sommaire (chapitrage logique Alpine.js)

1. Socle Alpine : initialisation, périmètre, structure
2. Affichage dynamique : texte, HTML, conditions
3. Événements : interactions, modificateurs, dispatch
4. Données & formulaires : binding, model, validation simple
5. Collections : boucles, templates, performance
6. Animations & UX : transitions, collapse, focus, trap
7. Architecture : composants, stores, persistance
8. Intégrations & extensions : plugins, patterns avancés

---

## Chapitre 1 — Socle Alpine : initialisation, périmètre, structure

### Leçon (concept fondamental)

Alpine c’est du JavaScript réactif “collé” à ton HTML.
Le cœur du système : tu déclares un **scope** (`x-data`), tu l’initialises (`x-init`), et tu contrôles le DOM à partir de là.

### Checklist (Core)

| Feature    | Type      | À maîtriser                          | Statut    |
| ---------- | --------- | ------------------------------------ | --------- |
| `x-data`   | Directive | Scope local, état initial, fonctions | À couvrir |
| `x-init`   | Directive | Init de données, watchers, appels    | À couvrir |
| `x-ignore` | Directive | Exclure une zone Alpine              | À couvrir |
| `$data`    | Magic     | Accès brut aux données du scope      | À couvrir |
| `$el`      | Magic     | Référence vers l’élément courant     | À couvrir |
| `$root`    | Magic     | Racine du composant                  | À couvrir |

### Résultat attendu (ce que l’élève doit savoir faire)

Créer un composant isolé, comprendre où vit l’état, éviter les effets de bord.

---

## Chapitre 2 — Affichage dynamique : texte, HTML, conditions

### Leçon (concept fondamental)

Tu affiches des données avec des directives simples.
Tu dois comprendre la différence entre :

* “je cache/affiche” (`x-show`)
* “je crée/supprime du DOM” (`x-if`)

### Checklist (Core)

| Feature   | Type      | À maîtriser                       | Statut    |
| --------- | --------- | --------------------------------- | --------- |
| `x-text`  | Directive | Afficher du texte                 | À couvrir |
| `x-html`  | Directive | Injecter du HTML (attention XSS)  | À couvrir |
| `x-show`  | Directive | Toggle CSS display (DOM conservé) | À couvrir |
| `x-if`    | Directive | DOM conditionnel via `<template>` | À couvrir |
| `x-cloak` | Directive | Anti “flash” avant init           | À couvrir |

### Résultat attendu

Créer une UI conditionnelle propre (loading, empty state, erreurs, etc.).

---

## Chapitre 3 — Événements : interactions, modificateurs, dispatch

### Leçon (concept fondamental)

Alpine brille dans l’interaction.
Tu relies des actions utilisateur à ton état via `x-on` / `@event`.

### Checklist (Core)

| Feature      | Type      | À maîtriser                   | Statut    |
| ------------ | --------- | ----------------------------- | --------- |
| `x-on` / `@` | Directive | Click, input, keydown, submit | À couvrir |
| `$dispatch`  | Magic     | Émettre des événements custom | À couvrir |
| `$nextTick`  | Magic     | Attendre le DOM “post update” | À couvrir |

### Modificateurs essentiels (à documenter)

Ici, tu peux faire un tableau à part parce que c’est une énorme “feature zone”.

| Modificateur            | S’applique à     | But                                |
| ----------------------- | ---------------- | ---------------------------------- |
| `.prevent`              | submit/click     | Bloquer le comportement par défaut |
| `.stop`                 | events           | Stop propagation                   |
| `.debounce`             | input            | Lisser les saisies                 |
| `.throttle`             | scroll/mousemove | Limiter fréquence                  |
| `.once`                 | click            | Une seule exécution                |
| `.window`               | events           | Écouter au niveau window           |
| `.document`             | events           | Écouter au niveau document         |
| `.outside`              | click            | Détecter clic extérieur            |
| `.self`                 | events           | Seulement si target = element      |
| `.enter` `.escape` etc. | keyboard         | Raccourcis clavier                 |

### Résultat attendu

Gérer une modal, un dropdown, un menu mobile, un formulaire sans framework lourd.

---

## Chapitre 4 — Données & formulaires : binding, model, synchronisation

### Leçon (concept fondamental)

Les formulaires sont la guerre. Alpine simplifie ça avec `x-model`.

### Checklist (Core)

| Feature       | Type      | À maîtriser                  | Statut    |
| ------------- | --------- | ---------------------------- | --------- |
| `x-model`     | Directive | Liaison input ↔ state        | À couvrir |
| `x-modelable` | Directive | Exposer une valeur modelable | À couvrir |

### Modificateurs clés de `x-model`

| Modificateur | Exemple           | But                   |
| ------------ | ----------------- | --------------------- |
| `.lazy`      | input             | Update au blur/change |
| `.number`    | input type number | Convertir en number   |
| `.debounce`  | text input        | Lisser la saisie      |

### Résultat attendu

Construire un mini formulaire (login, filtre, recherche) propre et stable.

---

## Chapitre 5 — Collections : boucles, templates, performance

### Leçon (concept fondamental)

Tu rends des listes avec `x-for`.
C’est ici que tu commences à faire une “vraie app”.

### Checklist (Core)

| Feature | Type      | À maîtriser                | Statut    |
| ------- | --------- | -------------------------- | --------- |
| `x-for` | Directive | Itération sur array/object | À couvrir |
| `x-id`  | Directive | IDs uniques, accessibles   | À couvrir |
| `$id`   | Magic     | Générer des IDs cohérents  | À couvrir |

### Résultat attendu

Todo-list, rendu de cartes, liste filtrée + tri + compteur.

---

## Chapitre 6 — Animations & UX : transitions, collapse, focus, trap

### Leçon (concept fondamental)

C’est le chapitre “interface moderne”.
Sans ça, ton app fait “cheap” même si elle marche.

### Checklist (Core + Plugins)

| Feature           | Type      | À maîtriser                | Statut    |
| ----------------- | --------- | -------------------------- | --------- |
| `x-transition`    | Directive | Animations d’entrée/sortie | À couvrir |
| `Collapse` plugin | Plugin    | Accordéons, menus fluides  | À couvrir |
| `Focus` plugin    | Plugin    | `x-trap`, gestion focus    | À couvrir |

### Résultat attendu

Une modal accessible + un accordion propre + un dropdown fluide.

---

## Chapitre 7 — Architecture : composants, stores, persistance

### Leçon (concept fondamental)

C’est ici que tu passes du “script dans une page” à “mini application”.

### Checklist (Core + API)

| Feature          | Type   | À maîtriser                       | Statut    |
| ---------------- | ------ | --------------------------------- | --------- |
| `Alpine.data()`  | API    | Définir composants réutilisables  | À couvrir |
| `Alpine.store()` | API    | État global partagé               | À couvrir |
| `$store`         | Magic  | Accéder au store dans le template | À couvrir |
| `$watch`         | Magic  | Observer un état                  | À couvrir |
| `Persist` plugin | Plugin | Sauvegarde localStorage           | À couvrir |

### Résultat attendu

Un store global “auth”, “panier”, “thème dark/light”, avec persistance.

---

## Chapitre 8 — Intégrations & extensions : plugins officiels & patterns avancés

### Leçon (concept fondamental)

Ici tu complètes “100% features” avec les plugins officiels et les patterns utiles.

### Checklist (Plugins officiels)

| Plugin    | Feature       | Utilité                             |
| --------- | ------------- | ----------------------------------- |
| Intersect | `x-intersect` | Lazy loading, animations on-scroll  |
| Resize    | `x-resize`    | UI responsive, calcul dynamique     |
| Mask      | `x-mask`      | Input masking (téléphone, date)     |
| Anchor    | `x-anchor`    | Positionnement contextuel           |
| Morph     | morphing DOM  | Update partiel sans re-render total |
| Sort      | drag & drop   | Tri interactif                      |

### Checklist (Core complémentaire souvent oublié)

| Feature         | Type      | À maîtriser                        | Pourquoi c’est important |
| --------------- | --------- | ---------------------------------- | ------------------------ |
| `x-bind` / `:`  | Directive | Bind classes, attrs, styles        | Base du templating       |
| `Alpine.bind()` | API       | Bind réutilisable (pattern avancé) | DRY sur attributs        |
| `x-ref`         | Directive | Références DOM                     | Essentiel en UI complexe |
| `$refs`         | Magic     | Utiliser les refs                  | Focus, scroll, etc.      |
| `x-effect`      | Directive | Effets automatiques                | Réactions implicites     |
| `x-teleport`    | Directive | Déporter DOM (modals)              | Modals propres           |

### Résultat attendu

Une UI moderne et propre : modals via teleport, scroll-to, inputs masqués, lazy-loading.

---

## Vue globale : combien de “features” au total ?

Voici une estimation propre (sans bullshit) :

| Catégorie                    | Nombre | Commentaire        |
| ---------------------------- | -----: | ------------------ |
| Directives core              |     18 | Liste officielle   |
| Magic properties             |      9 | Liste officielle   |
| API globales                 |      3 | `data/store/bind`  |
| Plugins officiels            |      9 | Liste officielle   |
| Total “features principales” | **39** | Référentiel stable |

Le chiffre “106” arrive quand tu comptes aussi :
les modificateurs d’événements, les variantes de `x-model`, les patterns de store, les options de transitions, etc.

---

## Ce qu’il te manque probablement sur ta page (à fort impact)

Sans te faire une liste interminable, les “gros manquants” typiques sont :

* `x-teleport` (modals clean)
* `x-cloak` (anti flash)
* `x-ref` + `$refs` (DOM control propre)
* `x-effect` (effets réactifs)
* `x-html` (avec sécurité expliquée)
* `x-id` + `$id` (accessibilité et unicité)
* Plugins : Mask / Resize / Intersect / Anchor / Morph / Sort

---

## Plan pédagogique recommandé (progression logique)

Tu peux organiser ton site comme ça :

1. **Fondations** (x-data, x-init, x-text)
2. **UI dynamique** (x-show, x-if, x-transition)
3. **Interactivité** (x-on + modificateurs)
4. **Formulaires** (x-model)
5. **Listes** (x-for)
6. **Accessibilité/UX** (x-trap, focus, teleport)
7. **Architecture** (Alpine.data, store, persist)
8. **Plugins avancés** (Intersect, Mask, Resize, Morph…)

---

## Prochaine étape (et je m’arrête là pour attendre ta réponse)

Je peux te générer un **template MDX “Chapitre Alpine”** réutilisable (comme tu fais sur OmnyDocs) avec :

* Objectifs pédagogiques
* Pré-requis
* Démo + code
* Erreurs fréquentes
* Exercices
* Mini-quizz
* Checklist “features validées”

Tu veux que je te le fasse au format **MDX Docusaurus** avec tes blocs `:::info / :::warning / :::danger` ?


---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---

Très bien. Je te fais une version **chapitrée uniquement**, logique, exhaustive, et orientée “formation pro” (pas juste une liste de features).

Principe :
Chaque **chapitre = 1 concept fondamental** + une **leçon structurée** + une **checklist de validation**.
Et surtout : on couvre **100% du core Alpine.js** + **100% des plugins officiels** + une couche “production” (qui n’est pas Alpine mais indispensable).

---

# Alpine.js — Formation exhaustive (Chapitrage final)

Tu as totalement raison. Sans la genèse, tu as une formation “qui marche”, mais pas une formation “qui convainc”.
La genèse, c’est ce qui donne du sens : pourquoi Alpine existe, quel problème il résout, et pourquoi on le choisit en 2026.

Je te propose d’ajouter **3 chapitres au tout début**, avant l’installation. Ils servent de socle narratif + technique.

---

# Chapitre 0 — Genèse : pourquoi Alpine.js existe

## Leçon : le besoin réel derrière Alpine

Alpine.js est né d’un constat simple : beaucoup de projets veulent du **comportement dynamique** dans une page, mais sans embarquer un framework complet (React/Vue/Angular).
Tu veux souvent juste gérer une modal, un menu, un filtre, une validation de formulaire… et tu veux que ce soit **rapide, lisible, et proche du HTML**.

**À couvrir**

* Le problème historique : jQuery (impératif, spaghetti, difficile à maintenir)
* Le problème des frameworks lourds : build, boilerplate, complexité
* Alpine : “le minimum réactif” directement dans le DOM
* Les cas d’usage naturels : landing pages, back-office, CMS, apps hybrides

**Objectif**
Comprendre “pourquoi Alpine” avant de voir “comment Alpine”.

---

# Chapitre 0.1 — Philosophie : le modèle mental Alpine

## Leçon : Alpine = état local + directives + expressions

Alpine, c’est un modèle mental simple :

* Tu as un état (`x-data`)
* Tu affiches cet état (directives comme `x-text`, `x-show`)
* Tu modifies cet état (événements `@click`, `@input`)
* Alpine synchronise le DOM automatiquement

Tu dois faire comprendre que ce n’est pas “du JS magique”, c’est une **réactivité contrôlée**.

**À couvrir**

* Scope local vs global
* HTML comme “template”
* Le DOM comme source de vérité visuelle
* Ce que Alpine ne fait pas (routing complet, state management complexe par défaut)

**Objectif**
Savoir raisonner en composants Alpine sans se perdre.

---

# Chapitre 0.2 — Positionnement : Alpine vs React/Vue/Angular vs HTMX

## Leçon : choisir Alpine pour de bonnes raisons

Tu donnes une grille de décision professionnelle.

### Tableau de décision rapide

| Besoin                                            |      Alpine |           Vue/React |     Angular |      HTMX |
| ------------------------------------------------- | ----------: | ------------------: | ----------: | --------: |
| Ajouter de l’interactivité sur une page existante |         Oui | Possible mais lourd |  Non adapté |       Oui |
| Composants UI simples (dropdown, modal, tabs)     |         Oui |                 Oui |         Oui |       Oui |
| Grosse SPA avec routing, état massif              |      Limité |                 Oui |         Oui |       Non |
| Projet backend HTML-first (Laravel, Symfony)      |   Excellent |            Possible | Peu logique | Excellent |
| Courbe d’apprentissage                            | Très faible |             Moyenne |       Forte |    Faible |

**À couvrir**

* Quand Alpine est le meilleur choix
* Quand Alpine est un mauvais choix (et pourquoi)
* Alpine + Laravel / Livewire : combo naturel
* Alpine + API Node/Go : possible mais attention architecture

**Objectif**
Éviter les choix “par hype” et rester pro.

---

# Où ça s’insère dans ton plan validé ?

Tu places ces chapitres avant tout le reste :

* Chapitre 0 — Genèse : pourquoi Alpine.js existe
* Chapitre 0.1 — Philosophie : modèle mental Alpine
* Chapitre 0.2 — Positionnement : Alpine vs autres solutions
* Chapitre 1 — Installation & démarrage propre
* … puis ton plan complet jusqu’au Chapitre 37

---

Si tu veux, je peux aussi te rédiger ces 3 chapitres directement en **Markdown Zensical** (avec un schéma Mermaid “évolution jQuery → framework → Alpine → plugins”), dans ton style OmnyDocs.


## Chapitre 1 — Installation & démarrage propre (CDN, Vite, NPM)

### Leçon : comment Alpine “prend la main” sur le DOM

Tu dois expliquer comment Alpine démarre, scanne le DOM et instancie les composants.

**À couvrir**

* Installation via CDN (script defer)
* Installation via Vite + import
* `Alpine.start()` (démarrage contrôlé)
* Organisation minimale du projet (assets, scripts, plugins)

**Objectif**
Savoir lancer Alpine proprement dans un vrai projet (pas juste une démo).

---

## Chapitre 2 — `x-data` : état local, scope et méthodes

### Leçon : Alpine = état + HTML réactif

Le cœur : l’état vit dans `x-data`, chaque composant est un scope isolé.

**À couvrir**

* `x-data="{ ... }"` objet simple
* `x-data="factory()"` (préparation à Alpine.data)
* méthodes (`increment()`, `toggle()`)
* `this` dans Alpine

**Objectif**
Créer un composant autonome sans se mélanger les scopes.

---

## Chapitre 3 — `x-init` : initialisation et lifecycle minimal

### Leçon : ce qui se passe “au montage”

Tu montres comment initialiser des valeurs, lancer des actions, brancher des watchers.

**À couvrir**

* `x-init="..."` dans le HTML
* `init()` dans Alpine.data()
* `$watch` (preview)
* `$nextTick` (preview)

**Objectif**
Initialiser proprement un composant (sans hacks).

---

## Chapitre 4 — Affichage simple : `x-text` et expressions

### Leçon : afficher des données sans danger

Le chapitre “safe par défaut”.

**À couvrir**

* `x-text="variable"`
* expressions simples (ternaires, concat)
* bonnes pratiques (logique hors template)

**Objectif**
Affichage propre et lisible.

---

## Chapitre 5 — `x-html` : injection HTML + sécurité XSS

### Leçon : puissance dangereuse

Tu fais une vraie leçon sécurité (sanitization).

**À couvrir**

* différence `x-text` vs `x-html`
* pourquoi XSS est critique
* DOMPurify (concept, exemple)

**Objectif**
Savoir quand l’utiliser et quand l’interdire.

---

## Chapitre 6 — `x-show` : afficher/cacher (DOM conservé)

### Leçon : visibilité ≠ existence

Tu expliques que `x-show` garde le DOM et joue sur le CSS.

**À couvrir**

* `x-show="condition"`
* `x-show` + transitions
* impacts UX et perf

**Objectif**
Créer dropdown/menu/modal simple.

---

## Chapitre 7 — `x-if` : rendu conditionnel (DOM créé/supprimé)

### Leçon : le DOM disparaît vraiment

Différence clé avec `x-show`.

**À couvrir**

* `<template x-if="...">`
* effets sur focus / performance
* quand préférer `x-if`

**Objectif**
Comprendre le “vrai conditionnel”.

---

## Chapitre 8 — `x-cloak` : anti flash de contenu (FOUC)

### Leçon : rendre une app propre au chargement

Petit chapitre mais indispensable en production.

**À couvrir**

* `x-cloak` + CSS associé
* cas concret : menu affiché 0.2s avant init

**Objectif**
UI propre dès la première frame.

---

## Chapitre 9 — Événements : `x-on` et `@click`

### Leçon : interaction utilisateur

Tu montres l’essentiel + discipline.

**À couvrir**

* `x-on:click="..."` et `@click`
* events clavier, submit
* `@keydown.enter`, `@keyup.escape`

**Objectif**
Tout ce qui est action utilisateur devient simple.

---

## Chapitre 10 — Modificateurs d’événements (indispensables)

### Leçon : contrôler le comportement sans JS lourd

C’est une feature énorme, donc chapitre dédié.

**À couvrir**

* `.prevent`, `.stop`, `.once`, `.self`
* `.outside`, `.window`, `.document`
* `.debounce`, `.throttle`
* erreurs fréquentes

**Objectif**
Maîtriser les patterns modernes (dropdown auto-close, etc.).

---

## Chapitre 11 — Communication : `$dispatch` (events custom)

### Leçon : composants qui parlent entre eux

Sans store global, sans spaghetti.

**À couvrir**

* `$dispatch('event-name', payload)`
* écoute avec `@event-name.window`
* cas : modal ouverte depuis un bouton distant

**Objectif**
Créer une communication simple et maintenable.

---

## Chapitre 12 — `x-bind` et `:` : attributs dynamiques

### Leçon : templating sérieux

C’est là que tu fais du “vrai front”.

**À couvrir**

* `:class`, `:style`, `:disabled`, `:aria-*`
* objets conditionnels pour classes
* pattern “computed” via getters

**Objectif**
Créer des composants stylés, accessibles, dynamiques.

---

## Chapitre 13 — Formulaires : `x-model` (liaison bidirectionnelle)

### Leçon : input ↔ état

Base de toutes les apps.

**À couvrir**

* `x-model="value"`
* `.lazy`, `.number`, `.debounce`
* checkbox, radio, select
* validations simples

**Objectif**
Formulaires fluides, sans rechargement.

---

## Chapitre 14 — `x-modelable` : composants custom compatibles `x-model`

### Leçon : composants “pro”

Tu passes du natif au custom.

**À couvrir**

* rôle de `x-modelable`
* créer un composant slider / dropdown
* synchronisation propre

**Objectif**
Avoir des composants réutilisables “first-class”.

---

## Chapitre 15 — Boucles : `x-for` et performance

### Leçon : rendre des listes proprement

Tout ce qui est table, cards, listes.

**À couvrir**

* `<template x-for="item in items">`
* `:key` obligatoire (et pourquoi)
* patterns (index, destructuring)

**Objectif**
Rendre des collections sans bugs visuels.

---

## Chapitre 16 — `x-transition` : animations natives Alpine

### Leçon : UX fluide sans CSS complexe

C’est le vrai chapitre “wow”.

**À couvrir**

* `x-transition`
* transition enter/leave
* couplage avec `x-show`

**Objectif**
Menus, modals, panneaux animés propres.

---

## Chapitre 17 — Plugin Collapse : `x-collapse`

### Leçon : animations de hauteur naturelles

Accordions/FAQ, panneaux.

**À couvrir**

* installation plugin
* `x-collapse`
* erreurs fréquentes (x-show obligatoire)

**Objectif**
Accordions propres sans calcul manuel.

---

## Chapitre 18 — Plugin Focus : `x-trap`, inert, noscroll

### Leçon : accessibilité et modals “correctes”

Chapitre ultra important en entreprise.

**À couvrir**

* installation focus plugin
* `x-trap`
* `.inert`, `.noscroll`
* gestion clavier (escape, tab)

**Objectif**
Modals accessibles niveau pro.

---

## Chapitre 19 — `x-teleport` : modals propres et overlays

### Leçon : déplacer le DOM au bon endroit

C’est une directive officielle trop souvent oubliée.

**À couvrir**

* `x-teleport="body"`
* modals, tooltips, overlays
* interaction avec focus trap

**Objectif**
UI propre sans problèmes de z-index.

---

## Chapitre 20 — Références DOM : `x-ref` + `$refs`

### Leçon : manipuler le DOM sans jQuery

Quand tu dois scroll, focus, mesurer.

**À couvrir**

* `x-ref="messages"`
* `$refs.messages.scrollTop = ...`
* cas : auto-scroll chat

**Objectif**
Contrôle DOM propre et ciblé.

---

## Chapitre 21 — `x-effect` : effets réactifs maîtrisés

### Leçon : “quand X change, fais Y”

C’est un outil officiel puissant.

**À couvrir**

* `x-effect="..."` (effet automatique)
* comparaison avec `$watch`
* éviter les effets infinis

**Objectif**
Réactivité automatique sans code spaghetti.

---

## Chapitre 22 — `x-ignore` : zones ignorées par Alpine

### Leçon : intégrer d’autres libs / afficher du code Alpine

Chapitre “intégration”.

**À couvrir**

* `x-ignore` pour doc/code samples
* cas : intégration d’un éditeur externe

**Objectif**
Éviter les conflits de frameworks.

---

## Chapitre 23 — `x-id` + `$id` : unicité et accessibilité

### Leçon : composants instanciés 100 fois sans collision

Très utile pour formulaires et ARIA.

**À couvrir**

* `x-id="['email']"`
* `:id="$id('email')"`
* `:for="$id('email')"`

**Objectif**
Accessibilité + HTML valide.

---

## Chapitre 24 — Stores : `Alpine.store()` et `$store`

### Leçon : état global partagé

Auth, thème, panier, config.

**À couvrir**

* `Alpine.store('app', {...})`
* `$store.app.*`
* patterns de séparation (stores par fichier)

**Objectif**
Construire une app multi-écrans sans chaos.

---

## Chapitre 25 — Persist : plugin `@alpinejs/persist`

### Leçon : persistance automatique

Tu veux du “state survivant”.

**À couvrir**

* installation persist
* `$persist(...)`
* cas : thème, settings, préférences

**Objectif**
Expérience utilisateur stable.

---

## Chapitre 26 — Composants réutilisables : `Alpine.data()`

### Leçon : architecture maintenable

Ton chapitre 17 actuel est excellent, tu le gardes ici.

**À couvrir**

* `Alpine.data('name', (params)=>({...}))`
* composition (réutilisation de logique)
* conventions de nommage

**Objectif**
Zéro duplication, logique centralisée.

---

## Chapitre 27 — Bindings réutilisables : `Alpine.bind()`

### Leçon : DRY sur attributs/handlers

Très utile pour design system.

**À couvrir**

* `Alpine.bind('ButtonPrimary', ()=>({...}))`
* usage `x-bind="ButtonPrimary"`
* bindings dynamiques

**Objectif**
UI cohérente + maintenance simple.

---

## Chapitre 28 — Plugin Intersect : `x-intersect`

### Leçon : lazy loading, infinite scroll, animations scroll

C’est du “front moderne” propre.

**À couvrir**

* installation
* lazy load image
* sentinel infinite scroll

**Objectif**
Perf + UX moderne.

---

## Chapitre 29 — Plugin Mask : `x-mask`

### Leçon : inputs formatés automatiquement

Téléphone, date, CB.

**À couvrir**

* masques fixes
* masques dynamiques
* pièges UX

**Objectif**
Formulaires fiables.

---

## Chapitre 30 — Plugin Resize : `x-resize`

### Leçon : UI responsive intelligente

Cas tooltip, conteneurs, dashboards.

**À couvrir**

* installation
* callbacks resize
* recalcul layout

**Objectif**
Composants adaptatifs.

---

## Chapitre 31 — Plugin Anchor : `x-anchor`

### Leçon : tooltips/dropdowns positionnés proprement

Le chapitre “popovers pro”.

**À couvrir**

* `x-anchor.bottom-start="$refs.button"`
* fallback auto (évite overflow)
* cas dropdown

**Objectif**
Positionnement fiable sans libs lourdes.

---

## Chapitre 32 — Plugin Morph : `Alpine.morph()`

### Leçon : DOM patch intelligent

Très utile avec backends HTML.

**À couvrir**

* `Alpine.morph(el, html)`
* conserver focus / scroll
* cas refresh serveur

**Objectif**
UI mise à jour sans re-render violent.

---

## Chapitre 33 — Plugin Sort : `x-sort`

### Leçon : drag & drop simple

Listes réordonnables.

**À couvrir**

* `x-sort="callback"`
* `x-sort:item`
* persistance ordre (API)

**Objectif**
UX moderne en quelques lignes.

---

## Chapitre 34 — Performance Alpine : patterns et anti-patterns

### Leçon : rester fluide même à grande échelle

Ton chapitre perf est très bon, mais ici tu le “normalises”.

**À couvrir**

* limiter watchers
* getters vs méthodes
* éviter calculs en template
* virtualisation (pattern)
* lazy init (pattern)

**Objectif**
60 FPS, pas de lag.

---

## Chapitre 35 — TypeScript avec Alpine.js (bonus pro)

### Leçon : typage pour maintenir une grosse app

C’est pas une feature Alpine, mais c’est un bonus pro très crédible.

**À couvrir**

* interfaces stores
* typing `Alpine.data()`
* limites (templates non typés)

**Objectif**
Refactor sans peur.

---

## Chapitre 36 — Temps réel : WebSockets + Alpine (bonus pro)

### Leçon : état temps réel et UI live

Très bon chapitre, mais tu dois préciser : “intégration”, pas “feature Alpine”.

**À couvrir**

* websocket store global
* reconnexion
* auto-scroll messages

**Objectif**
Chat / notifications / dashboard live.

---

## Chapitre 37 — Testing, accessibilité et production

### Leçon : livrer un projet sérieux

Ton chapitre 25 actuel est très bon.

**À couvrir**

* Vitest (unit)
* Playwright (e2e)
* a11y (ARIA, focus, trap)
* build Vite optimisé
* monitoring (Sentry)

**Objectif**
Projet “production-ready”.

---

# Résumé : couverture “100% Alpine.js”

Tu peux affirmer “100%” si tu couvres explicitement :

* **Directives core** : toutes présentes dans les chapitres 2 → 23
* **Magics** : `$refs`, `$watch`, `$dispatch`, `$nextTick`, `$store`, `$el`, `$root`, `$data`, `$id`
* **API** : `Alpine.data`, `Alpine.store`, `Alpine.bind`
* **Plugins officiels** : Persist, Focus, Collapse, Intersect, Mask, Resize, Anchor, Morph, Sort

Avec ce plan, tu as une structure ultra propre et **commercialisable**.

---

Si tu valides ce chapitrage, je te génère ensuite un **tableau global “Feature → Chapitre”** (comme une matrice de conformité), ce qui te permettra de prouver noir sur blanc que ta doc couvre tout.


