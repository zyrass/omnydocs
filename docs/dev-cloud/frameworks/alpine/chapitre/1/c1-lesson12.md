---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Leçon n° 12

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Présentation des projets fil rouge (A/B/C) : apprendre Alpine comme un pro

### Objectif de la leçon

À la fin de cette leçon, tu vas comprendre :

* pourquoi on fait des **projets fil rouge** (et pas juste des exercices)
* ce que chaque projet t’apprend réellement
* comment ils sont découpés en parties pour rester progressifs
* comment éviter le piège “je code tout d’un coup et je me perds”

Un projet fil rouge, ce n’est pas un bonus.
C’est la colonne vertébrale qui transforme une formation en compétence réelle.

---

## 1) C’est quoi un “projet fil rouge” exactement ?

Un projet fil rouge, c’est une application qui évolue au fil des chapitres.

Au lieu de faire 50 petits exemples isolés, tu construis une vraie application en ajoutant :

* une feature à la fois
* au bon moment
* avec la bonne directive Alpine
* avec une progression logique

### Analogie simple

C’est comme apprendre à conduire :

* tu ne fais pas “le volant” un jour, “les pédales” un autre, “les panneaux” à part
* tu apprends tout ensemble, mais étape par étape, dans un contexte réel

---

## 2) Pourquoi on en fait 3 (et pas un seul)

Avoir 3 projets, c’est intelligent parce que tu couvres 3 univers différents :

* un projet fun (motivation + UX)
* un projet réel (business + refactor)
* un projet data/logique (tableaux + calculs)

Ça évite un gros problème pédagogique :

> “Je sais faire une Todo, mais je suis perdu dès que ce n’est plus une Todo.”

Avec A/B/C, tu apprends Alpine dans plusieurs contextes.

---

# Projet A — Clicker Hero RPG (fun + UX + progression naturelle)

## Objectif du projet

Construire une application “jeu” qui évolue et devient de plus en plus riche.

Ce projet est parfait parce qu’il est :

* motivant
* progressif
* naturellement orienté “state management”
* excellent pour apprendre les transitions et les modals

### Pourquoi c’est pédagogique

Dans un RPG, tout est “state-driven” :

* tes stats changent
* ton inventaire change
* ton shop change
* tes upgrades changent

Donc Alpine devient logique.

---

## Ce que tu vas apprendre avec ce projet

Tu vas pratiquer :

* `x-data` pour gérer l’état du joueur
* `x-text` pour afficher stats / gold / niveau
* `x-show` et `x-if` pour afficher des panneaux selon le contexte
* `x-for` + `:key` pour inventaire, shop, upgrades
* `x-transition` pour rendre le jeu agréable
* `$dispatch` pour des événements UI (toast, modals)
* `Alpine.store()` pour gérer un état global propre
* persistance localStorage / Persist plugin pour sauvegarder la partie

---

## Découpage (progression par parties)

### Partie 1 — Clicker + state + affichage

Le cœur du jeu :

* bouton “Attaquer”
* compteur de dégâts
* or gagné
* progression simple

### Partie 2 — Upgrades + conditions + UI panels

Tu ajoutes :

* upgrades achetables
* conditions d’achat (disabled)
* UI plus structurée

### Partie 3 — Inventaire + shop (x-for + key)

Tu gères des listes :

* items
* quantités
* achats
* affichage dynamique propre

### Partie 4 — Animations + transitions + modals

Tu passes en mode “UI produit” :

* modals pour shop
* transitions
* feedback visuel

### Partie 5 — Store global + persistance

Tu professionnalises :

* store central
* sauvegarde automatique
* reset

### Partie 6 — Équilibrage + refactor + componentisation

Tu fais le niveau pro :

* nettoyage code
* extraction composants
* lisibilité et maintenabilité

---

# Projet B — Tracker de paris sportifs (projet réel + clean code)

## Objectif du projet

Construire un tracker de tickets de paris sportifs, avec :

* affichage clair
* filtres
* stats
* persistance
* UX propre

Ce projet est extrêmement intéressant parce qu’il ressemble à un vrai besoin business :

> “Je veux suivre mes tickets, comprendre mes résultats, et analyser.”

---

## Pourquoi c’est le projet “pro” de la formation

Parce qu’il te force à travailler :

* comme sur un outil interne
* avec des données structurées
* avec des vues filtrées
* avec des calculs

Et surtout, tu vas apprendre un skill rare :

> refactor un projet existant sans tout casser

---

## Ce que tu vas apprendre avec ce projet

Tu vas pratiquer :

* `x-for` pour afficher des tickets
* tri / filtre / recherche
* `x-model` pour des filtres UI
* `x-effect` / `$watch` pour recalculer stats automatiquement
* persistance pour garder les tickets
* export/import JSON
* accessibilité (navigation clavier, focus visible)
* UI stable (pas de glitch)

---

## Découpage en parties

### Partie 1 — Audit du code + structure Vite

Tu poses une base propre :

* structure fichiers
* conventions
* composants

### Partie 2 — Affichage tickets + filtres + tri

Tu construis la vue principale :

* liste
* recherche
* filtres
* tags

### Partie 3 — Stats + persistance + UX

Tu ajoutes la valeur :

* gains/pertes
* historique
* stats globales
* sauvegarde

### Partie 4 — Accessibilité + AAA theme

Tu passes au niveau produit :

* focus visible
* clavier
* UI lisible
* cohérence

### Partie 5 — Extraction component library

Tu récupères ce que tu as créé pour le réutiliser ailleurs.

---

# Projet C — Classement Ligue 1 dynamique (data + logique + tableaux)

## Objectif du projet

Construire un mini système de classement :

* équipes
* matchs
* points
* calcul automatique
* tri dynamique

Ce projet est parfait pour apprendre Alpine sur un cas très structuré.

---

## Pourquoi c’est pédagogique

Parce que tu travailles avec :

* des tableaux de données
* des calculs
* des règles de tri
* des affichages conditionnels

C’est excellent pour apprendre à ne pas faire du code “approximatif”.

---

## Ce que tu vas apprendre avec ce projet

Tu vas pratiquer :

* CRUD local (ajout/suppression équipes)
* `x-for` pour les tableaux
* `:key` pour éviter les bugs invisibles
* calcul du classement
* tri automatique
* filtres
* persistance
* export/import
* DataTable réutilisable

---

## Découpage en parties

### Partie 1 — CRUD équipes + points

Tu crées :

* liste équipes
* ajout/suppression
* modification

### Partie 2 — Saisie matchs dynamique

Tu ajoutes :

* formulaire de match
* sélection équipes
* score
* validation

### Partie 3 — Calcul classement auto + tri + filtres

Tu fais la partie logique :

* calcul points
* tri
* affichage final

### Partie 4 — Persistance + export/import

Tu rends ça solide :

* sauvegarde
* récupération
* import/export JSON

### Partie 5 — UI DataTable réutilisable (bonus pagination)

Tu professionnalises :

* table générique
* réutilisable dans d’autres projets

---

## 3) Comment choisir ton projet principal (si tu dois en prioriser un)

Même si tu feras les trois dans la formation, il y a une logique :

| Projet      | Idéal si tu veux…              | Ce que ça développe       |
| ----------- | ------------------------------ | ------------------------- |
| A (RPG)     | apprendre en t’amusant         | UX + state + composants   |
| B (Tracker) | faire du concret business      | architecture + clean code |
| C (Ligue 1) | devenir solide en logique data | tableaux + calculs + tri  |

---

## 4) Le piège à éviter absolument : “je code tout d’un coup”

Le pire comportement étudiant :

* “j’ai compris, je fais tout le projet en 1 nuit”

Résultat :

* bugs partout
* code illisible
* état incohérent
* refactor impossible

La règle pro :

> une feature = une étape = un livrable stable

Tu avances comme un vrai développeur produit.

---

## 5) Mini exemple : comment un fil rouge s’aligne avec un chapitre

Exemple : Chapitre 5 (x-for + key)

Tu peux l’utiliser dans :

* Projet A : inventaire / shop
* Projet B : liste de tickets
* Projet C : tableau de classement

Donc un chapitre te sert 3 fois.
C’est exactement ce qui crée la mémorisation.

---

## Résumé de la leçon

Les projets fil rouge sont là pour transformer la formation en vraie compétence.

* Projet A = motivation + UI fun + progression
* Projet B = projet réel + refactor + architecture
* Projet C = data + logique + tableaux

Chaque projet est découpé en parties pour rester progressif, stable, et maintenable.

---

## Mini exercice (rapide)

Tu choisis ton projet “principal” (celui que tu veux pousser le plus loin), et tu écris :

1. Pourquoi tu le choisis
2. Ce que tu veux apprendre en priorité (UX, data, architecture)
3. Le résultat final que tu veux obtenir

---

On a terminé le Chapitre 1 (présentation/installation) de façon complète et cohérente.

Prochaine étape logique : on attaque **Chapitre 2 — État & Affichage (les fondations)**
et on démarre avec la Leçon 1 :

**x-data : créer un composant Alpine (scope, données, fonctions, bonnes pratiques)**

Quand tu me dis “go”, je démarre Chapitre 2, Leçon 1, au même niveau de qualité.
