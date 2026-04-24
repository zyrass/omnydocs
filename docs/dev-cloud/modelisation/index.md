---
description: "Modélisation — Hub de navigation : UML pour l'architecture objet et Merise pour la conception de bases de données relationnelles."
tags: ["MODELISATION", "UML", "MERISE", "ARCHITECTURE"]
---

# Modélisation

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-version="2024"
  data-time="Hub">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le plan avant les briques"
    Commencer à coder ou à créer des tables SQL sans modéliser, c'est comme commencer à construire une maison en posant des briques au hasard. La modélisation est le **plan de l'architecte**. Elle permet de valider la faisabilité, d'aligner la compréhension de toute l'équipe (métier, développeurs, testeurs) et d'identifier les problèmes de conception *avant* d'écrire la moindre ligne de code, là où les changements ne coûtent encore rien.

La modélisation est une étape fondamentale du génie logiciel. Cette section couvre les deux standards de l'industrie, chacun ayant son domaine d'excellence :
- **UML** (Unified Modeling Language) pour l'architecture orientée objet et les comportements.
- **Merise** pour la conception structurée et optimale des bases de données relationnelles.

<br>

---

## Les deux piliers de la modélisation

<div class="grid cards" markdown>

-   :lucide-boxes:{ .lg .middle } **UML — Modélisation Objet**

    ---
    12 diagrammes essentiels (statiques et dynamiques). Use cases, diagrammes de classes, de séquence, d'activités, d'états. Le standard international pour documenter et concevoir les architectures logicielles.

    **Niveau** : 🟡 Intermédiaire | **Durée** : 4-6 semaines

    [:lucide-book-open-check: Accéder à la section UML](./uml/index.md)

-   :lucide-database:{ .lg .middle } **Merise — Modélisation des Données**

    ---
    Le standard français de conception de bases de données. Cycle complet : des règles métier (MCD) à l'architecture relationnelle (MLD) jusqu'à la génération du schéma SQL physique (MPD).

    **Niveau** : 🟢 Débutant → 🟡 Intermédiaire | **Durée** : ~15-20h

    [:lucide-book-open-check: Accéder à la section Merise](./merise/index.md)

</div>

<br>

---

## Lequel choisir ?

| Besoin de conception | Outil recommandé | Pourquoi ? |
|---|---|---|
| **Comprendre les parcours utilisateurs** | UML (Use Cases, Activités) | Modélise le flux d'interactions entre acteurs et système. |
| **Concevoir la base de données** | Merise (MCD, MLD) | Spécialement conçu pour l'intégrité relationnelle et les cardinalités. |
| **Structurer le code (POO)** | UML (Classes) | Mappe directement vers les classes, interfaces et héritages. |
| **Documenter un workflow API** | UML (Séquence) | Montre parfaitement l'ordre des requêtes et réponses entre systèmes. |

!!! tip "La synergie dans la vraie vie"
    Dans un projet réel, ces méthodes sont complémentaires. Vous utiliserez **UML (Use Cases)** pour comprendre ce que veut le client, **Merise (MCD)** pour structurer sa base de données, et **UML (Séquence)** pour concevoir le backend qui lie les deux.

<br>