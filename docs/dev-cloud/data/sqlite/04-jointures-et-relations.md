---
description: "SQLite — Module 4 : Jointures relationnelles (INNER, LEFT, CROSS, SELF JOIN), sous-requêtes avancées et CTE (Common Table Expressions)."
icon: lucide/book-open-check
tags: ["SQLITE", "JOIN", "INNER JOIN", "LEFT JOIN", "CTE", "SOUS-REQUETES"]
---

# Jointures & Relations

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="3.43+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Carnet d'Adresses Croisé"
    Un carnet d'adresses contient des noms. Un agenda contient des rendez-vous avec des ID de participants. Pour voir "qui a quel rendez-vous avec quel nom", vous devez **croiser** les deux documents — c'est exactement ce que fait un JOIN. INNER JOIN = seulement ceux qui apparaissent dans les deux. LEFT JOIN = tout le carnet d'adresses, même ceux sans rendez-vous (NULL à la place). La maîtrise du JOIN est la compétence clé qui distingue un développeur SQL intermédiaire d'un avancé.

Ce module couvre toutes les jointures SQLite, les sous-requêtes avancées et les CTE (Common Table Expressions).

<br>

---

## Données d'Exemple

```sql title="SQL — Jeu de données pour tous les exemples de ce module"
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE posts (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER,        -- NULL possible pour tester LEFT JOIN
    title   TEXT NOT NULL,
    views   INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE tags (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER NOT NULL,
    tag_id  INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id)
);

INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO posts VALUES
    (1, 1, 'Premier article',    150),
    (2, 1, 'Deuxième article',   80),
    (3, 2, 'Guide SQL',          320),
    (4, NULL, 'Post sans auteur', 0);   -- Pas de user_id
INSERT INTO tags VALUES (1, 'PHP'), (2, 'SQL'), (3, 'Laravel');
INSERT INTO post_tags VALUES (1, 1), (1, 3), (2, 1), (3, 2), (3, 3);
```

<br>

---

## 1. INNER JOIN — Intersection

**INNER JOIN retourne uniquement les lignes qui ont une correspondance dans les deux tables.**

```sql title="SQL — INNER JOIN : articles avec leurs auteurs"
-- Syntaxe moderne (INNER JOIN ... ON)
SELECT
    p.id    AS post_id,
    p.title,
    u.name  AS author
FROM posts p
INNER JOIN users u ON p.user_id = u.id;

-- Résultat : Le post 4 (user_id NULL) n'apparaît PAS
-- ┌─────────┬────────────────────┬────────┐
-- │ post_id │ title              │ author │
-- ├─────────┼────────────────────┼────────┤
-- │ 1       │ Premier article    │ Alice  │
-- │ 2       │ Deuxième article   │ Alice  │
-- │ 3       │ Guide SQL          │ Bob    │
-- └─────────┴────────────────────┴────────┘

-- Jointure sur 3 tables : posts + auteurs + tags
SELECT
    p.title,
    u.name  AS author,
    t.name  AS tag
FROM posts p
INNER JOIN users    u  ON p.user_id = u.id
INNER JOIN post_tags pt ON p.id      = pt.post_id
INNER JOIN tags     t  ON pt.tag_id  = t.id
ORDER BY p.title, t.name;
```

```sql title="SQL — Agrégations avec INNER JOIN"
-- Nombre de posts par auteur (seulement ceux qui ont au moins un post)
SELECT
    u.name,
    COUNT(p.id) AS nb_posts,
    SUM(p.views) AS total_views,
    MAX(p.views) AS best_post_views
FROM users u
INNER JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
ORDER BY nb_posts DESC;
-- Charlie n'apparaît pas (aucun post)
```

<br>

---

## 2. LEFT JOIN — Toutes les lignes de gauche

**LEFT JOIN retourne toutes les lignes de la table de gauche, avec NULL pour les colonnes de droite quand il n'y a pas de correspondance.**

```sql title="SQL — LEFT JOIN : tous les auteurs, même sans post"
SELECT
    u.name,
    p.title,
    p.views
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;

-- Résultat : Charlie apparaît avec NULL dans title et views
-- ┌─────────┬────────────────────┬───────┐
-- │ name    │ title              │ views │
-- ├─────────┼────────────────────┼───────┤
-- │ Alice   │ Premier article    │ 150   │
-- │ Alice   │ Deuxième article   │ 80    │
-- │ Bob     │ Guide SQL          │ 320   │
-- │ Charlie │ NULL               │ NULL  │  ← Pas de post
-- └─────────┴────────────────────┴───────┘
```

```sql title="SQL — LEFT JOIN avec COUNT : afficher 0 au lieu de NULL"
-- Nombre de posts par auteur (inclut ceux sans post avec 0)
SELECT
    u.name,
    COUNT(p.id) AS nb_posts     -- COUNT ignore les NULL → 0 pour Charlie
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
ORDER BY nb_posts DESC;
-- ┌─────────┬──────────┐
-- │ name    │ nb_posts │
-- ├─────────┼──────────┤
-- │ Bob     │ 1        │
-- │ Alice   │ 2        │
-- │ Charlie │ 0        │
-- └─────────┴──────────┘

-- Pattern : trouver les users SANS aucun post
SELECT u.id, u.name
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE p.id IS NULL;             -- NULL = pas de correspondance = pas de post
-- Résultat : Charlie seulement
```

<br>

---

## 3. CROSS JOIN — Produit Cartésien

**CROSS JOIN combine chaque ligne de la table A avec chaque ligne de la table B (toutes les combinaisons possibles).**

```sql title="SQL — CROSS JOIN : générer toutes les combinaisons"
-- Générer toutes les combinaisons couleur × taille
CREATE TABLE colors (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE sizes  (id INTEGER PRIMARY KEY, name TEXT);

INSERT INTO colors VALUES (1, 'Rouge'), (2, 'Bleu'), (3, 'Vert');
INSERT INTO sizes  VALUES (1, 'S'), (2, 'M'), (3, 'L');

SELECT c.name AS color, s.name AS size
FROM colors c
CROSS JOIN sizes s
ORDER BY c.name, s.name;
-- Résultat : 3 × 3 = 9 combinaisons
-- Rouge-S, Rouge-M, Rouge-L, Bleu-S, Bleu-M, ...
```

_Le CROSS JOIN est utile pour générer des grilles de test, des matrices de configuration, ou des calendriers._

<br>

---

## 4. SELF JOIN — Auto-Jointure (Hiérarchies)

**Un SELF JOIN joint une table avec elle-même — utile pour les structures hiérarchiques.**

```sql title="SQL — SELF JOIN : hiérarchie employés-managers"
CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    manager_id INTEGER,  -- Référence employees.id (NULL = CEO)
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

INSERT INTO employees VALUES
    (1, 'Alice CEO',    NULL),
    (2, 'Bob Manager',     1),
    (3, 'Carol Manager',   1),
    (4, 'David Dev',       2),
    (5, 'Eve Dev',         2),
    (6, 'Frank Dev',       3);

-- Chaque employé avec le nom de son manager
SELECT
    e.name   AS employee,
    m.name   AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY m.name NULLS FIRST;

-- Compter les subordonnés directs par manager
SELECT
    m.name AS manager,
    COUNT(e.id) AS direct_reports
FROM employees m
LEFT JOIN employees e ON m.id = e.manager_id
GROUP BY m.id, m.name
ORDER BY direct_reports DESC;
```

<br>

---

## 5. CTE — Common Table Expressions

Les **CTE** (clause `WITH`) permettent d'écrire des sous-requêtes nommées et réutilisables, rendant les requêtes complexes lisibles.

```sql title="SQL — CTE : sous-requêtes nommées avec WITH"
-- ─── CTE simple ───────────────────────────────────────────────────────────────
WITH active_users AS (
    -- Définition de la CTE (sous-requête nommée)
    SELECT id, name FROM users
    WHERE active = 1
)
-- Utilisation de la CTE comme une table normale
SELECT au.name, COUNT(p.id) AS nb_posts
FROM active_users au
LEFT JOIN posts p ON au.id = p.user_id
GROUP BY au.id, au.name;

-- ─── CTE multiples (chaînées) ─────────────────────────────────────────────────
WITH
    published_posts AS (
        SELECT * FROM posts WHERE published = 1
    ),
    top_posts AS (
        SELECT * FROM published_posts WHERE views > 100
    )
SELECT tp.title, u.name AS author
FROM top_posts tp
INNER JOIN users u ON tp.user_id = u.id
ORDER BY tp.views DESC;

-- ─── CTE récursive : générer une séquence ─────────────────────────────────────
WITH RECURSIVE sequence(n) AS (
    SELECT 1                          -- Cas de base
    UNION ALL
    SELECT n + 1 FROM sequence WHERE n < 10  -- Cas récursif
)
SELECT n FROM sequence;
-- Résultat : 1, 2, 3, ..., 10

-- ─── CTE récursive : traverser une hiérarchie ─────────────────────────────────
WITH RECURSIVE hierarchy(id, name, manager_id, level) AS (
    -- Cas de base : le CEO (pas de manager)
    SELECT id, name, manager_id, 0
    FROM employees WHERE manager_id IS NULL

    UNION ALL

    -- Cas récursif : les subordonnés
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e
    INNER JOIN hierarchy h ON e.manager_id = h.id
)
SELECT
    level,
    name,
    CASE level
        WHEN 0 THEN 'CEO'
        WHEN 1 THEN 'Manager'
        ELSE 'Développeur'
    END AS role
FROM hierarchy
ORDER BY level, name;
```

<br>

---

## 6. Sous-Requêtes Avancées

```sql title="SQL — Sous-requêtes : EXISTS, NOT EXISTS, ALL, ANY"
-- ─── EXISTS : vrai si la sous-requête retourne au moins une ligne ─────────────
-- Users ayant au moins un post publié
SELECT name FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p
    WHERE p.user_id = u.id AND p.published = 1
);

-- ─── NOT EXISTS : vrai si la sous-requête retourne zéro lignes ────────────────
-- Users sans aucun post
SELECT name FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM posts p WHERE p.user_id = u.id
);

-- ─── Sous-requête dans FROM (inline view) ────────────────────────────────────
SELECT author, total_views
FROM (
    SELECT u.name AS author, SUM(p.views) AS total_views
    FROM users u
    INNER JOIN posts p ON u.id = p.user_id
    GROUP BY u.id, u.name
) AS stats
WHERE total_views > 100
ORDER BY total_views DESC;
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Dashboard auteur**

```sql title="SQL — Exercice 1 : requêtes analytiques sur le schéma blog"
-- Avec le schéma (users, posts, tags, post_tags) :
-- 1. Liste des posts avec auteur ET tous leurs tags (séparés par virgule)
--    Indice : GROUP_CONCAT(t.name, ', ')
-- 2. Top 3 des auteurs par nombre total de vues
-- 3. Tags les plus utilisés (avec leur nombre de posts)
-- 4. Posts sans aucun tag (LEFT JOIN + IS NULL)
-- 5. Auteurs qui ont utilisé le tag 'PHP' (EXISTS ou IN)
```

**Exercice 2 — CTE + hiérarchie**

```sql title="SQL — Exercice 2 : explorer l'organisation avec des CTE récursives"
-- Avec la table employees (exercice ci-dessus) :
-- 1. Écrire une CTE récursive qui retourne la chaîne hiérarchique complète
--    pour chaque employé : "Alice CEO > Bob Manager > David Dev"
-- 2. Compter le nombre total de subordonnés (directs et indirects) par manager
-- 3. Trouver tous les collègues directs d'un employé donné
--    (même manager_id)
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    **INNER JOIN** ne retourne que les lignes avec correspondance des deux côtés. **LEFT JOIN** retourne toutes les lignes de gauche, avec NULL à droite si pas de correspondance — c'est le JOIN le plus courant pour les rapports. Le pattern `LEFT JOIN ... WHERE right.col IS NULL` est la façon standard de trouver les lignes "sans correspondance". Les **CTE** (`WITH`) transforment des requêtes complexes en étapes lisibles. Les **CTE récursives** permettent de traverser des hiérarchies (catégories imbriquées, organigrammes). `EXISTS` est souvent plus performant que `IN` pour les grandes tables.

> Dans le module suivant, nous optimisons les performances avec les **index**, analysons les plans d'exécution (`EXPLAIN QUERY PLAN`), et maîtrisons les **transactions ACID** pour garantir la cohérence des données.

<br>
