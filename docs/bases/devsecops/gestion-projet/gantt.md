---
description: "Diagramme de Gantt — Comprendre, créer et lire un planning de projet sous forme de Gantt. Outil de planification temporelle indispensable pour la gestion de projet."
icon: lucide/book-open-check
tags: ["GESTION PROJET", "GANTT", "PLANIFICATION", "MERMAID", "PLANNING"]
---

# Diagramme de Gantt — La Carte Temporelle du Projet

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="2024"
  data-time="~15 minutes">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Plan de Vol"
    Quand un avion décolle de Paris pour New York, le pilote ne consulte pas sa carte toutes les 5 minutes. Il a planifié le vol au sol : route, durée, altitude, carburant, escales d'urgence. Le **Gantt**, c'est le plan de vol de votre projet : qui fait quoi, quand, pour combien de temps, et quelles tâches bloquent les autres.

    Développé par Henry Gantt en 1910, ce diagramme reste, plus d'un siècle plus tard, l'outil de planification le plus lisible qui existe pour un projet à plusieurs phases et plusieurs acteurs.

Un diagramme de Gantt représente les tâches d'un projet sur un **axe temporel horizontal**. La durée d'une barre = la durée de la tâche. Les dépendances (une tâche qui ne peut commencer qu'après une autre) sont représentées par des flèches ou par l'enchaînement des barres.

<br>

---

## Créer un Gantt avec Mermaid

```mermaid
gantt
    title Projet de Développement — Application Web
    dateFormat YYYY-MM-DD
    excludes weekends

    section Phase 1 : Cadrage
        Analyse des besoins       :done,    p1t1, 2026-04-01, 3d
        Maquettes et wireframes   :done,    p1t2, after p1t1, 4d
        Validation client         :active,  p1t3, after p1t2, 2d

    section Phase 2 : Développement Backend
        Installation Laravel      :         p2t1, after p1t3, 1d
        Base de données           :         p2t2, after p2t1, 5d
        API REST + Auth           :         p2t3, after p2t2, 8d

    section Phase 3 : Frontend
        Intégration HTML/CSS      :         p3t1, after p1t3, 6d
        Composants Angular        :         p3t2, after p3t1, 7d
        Connexion API → Frontend  :         p3t3, after p2t3, 4d

    section Phase 4 : Déploiement
        Tests et QA               :crit,    p4t1, after p3t3, 5d
        Déploiement production    :crit,    p4t2, after p4t1, 2d
```

_Le chemin critique (:crit) identifie les tâches qui, si elles prennent du retard, **retardent l'ensemble du projet**. C'est la priorité absolue du chef de projet._

<br>

---

## Syntaxe Mermaid pour les Gantt

```mermaid
gantt
    dateFormat YYYY-MM-DD
    title Syntaxe de référence

    section Section 1
        Tâche terminée       :done,   t1, 2026-01-01, 5d
        Tâche active         :active, t2, after t1, 3d
        Tâche critique       :crit,   t3, after t2, 4d
        Tâche standard       :        t4, after t3, 2d
        Milestone (jalon)    :milestone, m1, 2026-01-20, 0d
```

| Marqueur | Signification | Couleur |
|---|---|---|
| `:done,` | Tâche terminée | Vert foncé |
| `:active,` | En cours | Bleu |
| `:crit,` | Chemin critique | Rouge |
| `:milestone,` | Jalon (point de contrôle) | Losange |
| _(sans marqueur)_ | Planifiée | Bleu clair |

<br>

---

## Gantt vs Kanban — Quand Utiliser Quoi ?

| Critère | Gantt | Kanban |
|---|---|---|
| **Idéal pour** | Projets avec dates fixes, jalons contractuels | Flux de travail continu, maintenance |
| **Visibilité** | Temporelle (qui fait quoi quand) | État du travail (ce qui est en cours) |
| **Flexibilité** | Faible (le planning est figé) | Haute (priorités changeantes) |
| **Taille d'équipe** | 5+ personnes, phases distinctes | 1 à 10 personnes |
| **Usage typique** | Projet client, refonte complète | Développement produit continu |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le Gantt n'est pas un outil de contrôle — c'est un outil de **communication**. Il aligne en un seul visuel le client, le chef de projet et l'équipe sur les priorités, les dépendances et les dates clés. Sur les projets complexes avec des dépendances entre équipes (frontend qui attend le backend, QA qui attend le développement), le Gantt est irremplaçable pour identifier les blocages avant qu'ils surviennent.

> [Retour à la Gestion de Projet →](./index.md)
