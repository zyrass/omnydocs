---
description: "Bases de données — Hub de navigation : SQL, NoSQL, GraphQL et solutions embarquées pour les applications web modernes."
tags: ["DATABASE", "SQL", "NOSQL", "GRAPHQL", "SQLITE", "POSTGRESQL", "MYSQL"]
---

# Bases de Données

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-version="2024"
  data-time="Hub">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'entrepôt et ses rayons"
    Une base de données est l'entrepôt de votre application : c'est là que vivent toutes ses données. Comme un entrepôt physique, il en existe différents types selon ce qu'on stocke. Un entrepôt de documents (NoSQL document) ressemble à une bibliothèque — chaque livre est autonome. Un entrepôt relationnel (SQL) ressemble à un tableur géant où chaque ligne est liée aux autres par des clés. Choisir le bon entrepôt, c'est choisir la bonne architecture avant de poser la première brique.

Cette section couvre les principales solutions de persistance des données, du SQL relationnel classique aux bases NoSQL modernes, en passant par GraphQL comme couche d'accès.

<br>

---

## Solutions disponibles

<div class="grid cards" markdown>

-   :lucide-hard-drive:{ .lg .middle } **SQLite**

    ---
    Base de données embarquée — aucun serveur requis. Idéale pour les prototypes, tests, applications desktop et environnements de développement Laravel.

    **Niveau** : 🟢 Débutant | **Durée** : ~10h | **6 modules**

    [:lucide-book-open-check: Accéder à SQLite](./sqlite/index.md)

-   :lucide-server:{ .lg .middle } **MariaDB & MySQL**

    ---
    SGBDR open-source de référence pour les applications web. Driver natif Laravel, stacks LAMP/LEMP, hébergements partagés. DDL, DML, index, fenêtrage, CTE.

    **Niveau** : 🟢 Débutant → 🔴 Avancé | **Durée** : ~25-30h

    [:lucide-book-open-check: Accéder à SQL & MariaDB](./sql.md)

-   :lucide-elephant:{ .lg .middle } **PostgreSQL**

    ---
    SGBDR avancé : types riches (JSONB, arrays, ranges), extensions PostGIS, performances sur gros volumes, full-text search natif. Référence enterprise.

    **Niveau** : 🟡 Intermédiaire → 🔴 Avancé | **Durée** : ~20-25h

    [:lucide-book-open-check: Accéder à PostgreSQL](./postgresql.md)

-   :lucide-layers:{ .lg .middle } **NoSQL**

    ---
    Panorama des bases non-relationnelles : Document (MongoDB), Clé-Valeur (Redis), Colonne (Cassandra), Graphe (Neo4j). Cas d'usage, forces et limites.

    **Niveau** : 🟡 Intermédiaire | **Durée** : ~15h

    [:lucide-book-open-check: Accéder à NoSQL](./nosql.md)

-   :lucide-git-branch:{ .lg .middle } **GraphQL**

    ---
    API orientée schéma : requêtes typées, résolution flexible, subscriptions temps réel. Alternatives REST, intégration Laravel avec Lighthouse.

    **Niveau** : 🟡 Intermédiaire → 🔴 Avancé | **Durée** : ~15h

    [:lucide-book-open-check: Accéder à GraphQL](./graphql.md)

</div>

<br>

---

## Choisir sa base de données

| Besoin | Solution recommandée |
|---|---|
| **Prototype / tests locaux** | SQLite |
| **Application web Laravel classique** | MariaDB / MySQL |
| **Données complexes / fonctions avancées** | PostgreSQL |
| **Cache / sessions / temps réel** | Redis (NoSQL clé-valeur) |
| **Documents flexibles / schéma variable** | MongoDB (NoSQL document) |
| **API flexible / plusieurs clients** | GraphQL + Lighthouse |

!!! tip "Conseil Laravel"
    Dans l'écosystème Laravel, **MariaDB/MySQL** est le choix par défaut. Utilisez **SQLite** pour les tests automatisés (`RefreshDatabase`). Adoptez **PostgreSQL** si votre infrastructure ou vos données l'exigent — Eloquent est 100% compatible.

<br>