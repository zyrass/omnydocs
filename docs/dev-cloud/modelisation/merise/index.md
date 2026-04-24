---
description: "Merise — Hub de navigation : de l'introduction à la génération SQL, en passant par MCD, MLD et MPD. La méthode française de modélisation des données."
tags: ["MERISE", "MCD", "MLD", "MPD", "MODELISATION", "BASE DE DONNÉES"]
---

# Merise

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="Merise 2"
  data-time="~15-20 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Plan d'Architecte"
    Construire une base de données sans Merise, c'est bâtir un immeuble sans plan : chaque pièce est ajoutée au fur et à mesure, sans cohérence globale. Merise impose une progression logique — du **vocabulaire métier** (MCD) à la **structure technique** (MLD) jusqu'au **schéma SQL physique** (MPD) — comme un architecte qui dessine d'abord les fondations avant d'élever les murs.

**Merise** est une méthode française de modélisation des systèmes d'information. Elle reste une référence robuste pour concevoir proprement les bases de données relationnelles et structurer les échanges entre métier et équipe technique.

> L'idée centrale : on ne part **pas directement dans le SQL**. On clarifie d'abord les règles métier, on les traduit en structures logiques, puis on arrive au schéma physique implémentable.

<br>

---

## Le cycle Merise

```mermaid
graph LR
    A["Besoins métier<br/>(règles, vocabulaire)"] --> B["MCD<br/>Conceptuel"]
    B --> C["MLD<br/>Logique"]
    C --> D["MPD<br/>Physique"]
    D --> E["Schéma SQL<br/>CREATE TABLE…"]

    style A fill:#f0f4ff,stroke:#4a6cf7
    style E fill:#f0fdf4,stroke:#22c55e
```

<br>

---

## Modules de la formation

<div class="grid cards" markdown>

-   :lucide-book-open:{ .lg .middle } **Introduction à Merise**

    ---
    Pourquoi Merise ? Vue d'ensemble du cycle MCD → MLD → MPD → SQL. Pour qui, quand l'utiliser. Exemples métier concrets (boutique, bibliothèque, tickets support).

    **Durée** : ~20-30 min | **Niveau** : 🟢 Débutant

    [:lucide-book-open-check: Accéder à l'introduction](./intro.md)

-   :lucide-shapes:{ .lg .middle } **MCD — Modèle Conceptuel de Données**

    ---
    Entités, associations, cardinalités, attributs, identifiants. Le langage commun métier / technique — sans SQL. Exemples complets avec notation Merise.

    **Durée** : ~3-4h | **Niveau** : 🟢 Débutant

    [:lucide-book-open-check: Accéder au MCD](./mcd.md)

-   :lucide-table:{ .lg .middle } **MLD — Modèle Logique de Données**

    ---
    Transformation du MCD en tables relationnelles. Clés primaires, clés étrangères, tables associatives. Normalisation (1FN, 2FN, 3FN) et dépendances fonctionnelles.

    **Durée** : ~4-5h | **Niveau** : 🟡 Intermédiaire

    [:lucide-book-open-check: Accéder au MLD](./mld.md)

-   :lucide-server:{ .lg .middle } **MPD — Modèle Physique de Données**

    ---
    Adaptation du MLD à un SGBD cible (PostgreSQL, MySQL). Choix des types SQL, contraintes (`NOT NULL`, `UNIQUE`, `CHECK`), index et paramètres propres au moteur.

    **Durée** : ~4-5h | **Niveau** : 🟡 Intermédiaire

    [:lucide-book-open-check: Accéder au MPD](./mpd.md)

-   :lucide-code-2:{ .lg .middle } **MPD → SQL — Génération du Schéma**

    ---
    Transformer le MPD en instructions SQL concrètes : `CREATE TABLE`, `ALTER TABLE`, `CREATE INDEX`, contraintes `FOREIGN KEY`. Cas complets de A à Z avec bonnes pratiques.

    **Durée** : ~5-6h | **Niveau** : 🟡 Intermédiaire

    [:lucide-book-open-check: Accéder à MPD → SQL](./mpd-to-sql.md)

</div>

<br>

---

## Progression recommandée

| Étape | Module | Rôle |
|---|---|---|
| 1 | [Introduction](./intro.md) | Comprendre la philosophie et le cycle complet |
| 2 | [MCD](./mcd.md) | Modéliser les règles métier |
| 3 | [MLD](./mld.md) | Traduire en structure relationnelle |
| 4 | [MPD](./mpd.md) | Adapter au SGBD cible |
| 5 | [MPD → SQL](./mpd-to-sql.md) | Générer le schéma SQL final |

!!! note "Prérequis"
    Une connaissance basique de SQL (SELECT, CREATE TABLE) est suffisante pour commencer. Merise s'apprend **avant** de créer des tables, pas après.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Merise n'est pas obsolète — c'est une discipline de pensée. Modéliser avant de coder évite les restructurations douloureuses de base de données en production. Un MCD propre produit un MLD cohérent, qui produit un MPD performant, qui génère un SQL maintenable. Chaque heure investie en modélisation économise des semaines de migrations correctives.

> Vous pouvez ensuite explorer [UML →](../uml/index.md) pour la modélisation objet et les diagrammes comportementaux.

<br>