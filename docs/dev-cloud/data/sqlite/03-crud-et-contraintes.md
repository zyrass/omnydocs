---
description: "SQLite — Module 3 : CRUD complet (INSERT, SELECT, UPDATE, DELETE) et contraintes d'intégrité (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL)."
icon: lucide/book-open-check
tags: ["SQLITE", "CRUD", "INSERT", "SELECT", "UPDATE", "DELETE", "CONTRAINTES"]
---

# CRUD & Contraintes

<div
  class="omny-meta"
  data-level="🟢→🟡 Intermédiaire"
  data-version="3.43+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Guichet de Mairie"
    Un guichet de mairie traite des actes : création de dossier (INSERT), consultation de registre (SELECT), modification d'état civil (UPDATE), suppression d'archive (DELETE). Mais il a des règles : un numéro de dossier est unique (PRIMARY KEY), une pièce jointe doit référencer un dossier existant (FOREIGN KEY), un âge ne peut pas être négatif (CHECK). Ces règles — les contraintes — garantissent l'intégrité des données. Sans elles, n'importe qui pourrait insérer des absurdités.

Ce module couvre l'intégralité du CRUD SQLite avec ses variantes, et toutes les contraintes d'intégrité disponibles.

<br>

---

## 1. INSERT — Insérer des Données

```sql title="SQL — INSERT : syntaxes standard et avancées"
-- ─── Basique ──────────────────────────────────────────────────────────────────
INSERT INTO users (name, email, age)
VALUES ('Alice Dupont', 'alice@example.com', 28);

-- Toutes les colonnes (dans l'ordre du schéma, NULL pour l'auto-incrémenté)
INSERT INTO users VALUES (NULL, 'Bob Martin', 'bob@example.com', 35, CURRENT_TIMESTAMP);

-- ─── Multi-lignes ─────────────────────────────────────────────────────────────
INSERT INTO users (name, email, age) VALUES
    ('Carol White', 'carol@example.com', 22),
    ('David Brown', 'david@example.com', 41),
    ('Eve Wilson',  'eve@example.com',   19);

-- ─── Ignorer les conflits de contrainte ───────────────────────────────────────
INSERT OR IGNORE INTO users (name, email, age)
VALUES ('Alice Dupont', 'alice@example.com', 28);
-- Si email existe déjà (UNIQUE), l'insertion est ignorée silencieusement

-- ─── Remplacer en cas de conflit ──────────────────────────────────────────────
INSERT OR REPLACE INTO users (id, name, email, age)
VALUES (1, 'Alice Updated', 'alice@example.com', 29);
-- Si id=1 existe : DELETE + INSERT. Sinon : INSERT direct.

-- ─── UPSERT (SQLite 3.24+) — recommandé ──────────────────────────────────────
INSERT INTO users (name, email, age)
VALUES ('Alice Dupont', 'alice@example.com', 28)
ON CONFLICT(email) DO UPDATE SET
    name = excluded.name,
    age  = excluded.age;
-- Si l'email existe déjà, met à jour name et age sans toucher aux autres colonnes

-- ─── Insérer depuis une requête SELECT ────────────────────────────────────────
INSERT INTO archived_users
SELECT * FROM users WHERE created_at < date('now', '-1 year');

-- ─── Récupérer l'ID de la dernière insertion ──────────────────────────────────
SELECT last_insert_rowid();
```

<br>

---

## 2. SELECT — Lire des Données

```sql title="SQL — SELECT : filtres, tri, agrégations, sous-requêtes"
-- ─── Basique ──────────────────────────────────────────────────────────────────
SELECT * FROM users;
SELECT id, name, email FROM users;
SELECT id AS user_id, name AS full_name FROM users;  -- Alias

-- ─── WHERE : filtrer ──────────────────────────────────────────────────────────
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE name = 'Alice Dupont';
SELECT * FROM users WHERE email LIKE '%@gmail.com';   -- Pattern
SELECT * FROM users WHERE email LIKE 'a%';            -- Commence par 'a'
SELECT * FROM users WHERE email GLOB 'a*';            -- Sensible à la casse
SELECT * FROM users WHERE age BETWEEN 18 AND 65;      -- Intervalle inclusif
SELECT * FROM users WHERE age IN (18, 25, 30, 35);   -- Liste de valeurs
SELECT * FROM users WHERE email IS NULL;              -- Valeur NULL
SELECT * FROM users WHERE email IS NOT NULL;          -- Valeur non-NULL

-- ─── Combinaisons logiques ────────────────────────────────────────────────────
SELECT * FROM users WHERE age >= 18 AND age <= 65;    -- ET
SELECT * FROM users WHERE age < 18 OR age > 65;       -- OU
SELECT * FROM users WHERE NOT (age < 18);             -- NON

-- ─── ORDER BY ─────────────────────────────────────────────────────────────────
SELECT * FROM users ORDER BY age;                     -- Ascendant (défaut)
SELECT * FROM users ORDER BY age DESC;                -- Descendant
SELECT * FROM users ORDER BY name ASC, age DESC;      -- Multi-colonnes
SELECT * FROM users ORDER BY created_at DESC;         -- Plus récent en premier

-- ─── LIMIT & OFFSET (pagination) ─────────────────────────────────────────────
SELECT * FROM users LIMIT 10;                         -- 10 premiers
SELECT * FROM users LIMIT 10 OFFSET 20;              -- Page 3 (items 21-30)
SELECT * FROM users ORDER BY id DESC LIMIT 5;         -- 5 plus récents

-- ─── DISTINCT ─────────────────────────────────────────────────────────────────
SELECT DISTINCT country FROM users;                   -- Pays uniques

-- ─── Fonctions d'agrégation ───────────────────────────────────────────────────
SELECT COUNT(*)       FROM users;                     -- Nombre total de lignes
SELECT COUNT(email)   FROM users;                     -- Nombre de non-NULL
SELECT AVG(age)       FROM users;                     -- Âge moyen
SELECT SUM(price)     FROM products;                  -- Somme des prix
SELECT MIN(age)       FROM users;                     -- Âge minimum
SELECT MAX(age)       FROM users;                     -- Âge maximum

-- ─── GROUP BY + HAVING ────────────────────────────────────────────────────────
SELECT country, COUNT(*) AS nb_users
FROM users
GROUP BY country
ORDER BY nb_users DESC;

SELECT country, COUNT(*) AS nb_users
FROM users
GROUP BY country
HAVING nb_users > 5;         -- Filtrer APRÈS le GROUP BY (≠ WHERE)

-- ─── Sous-requêtes ────────────────────────────────────────────────────────────
-- Plus âgé que la moyenne
SELECT * FROM users WHERE age > (SELECT AVG(age) FROM users);

-- Users ayant au moins un post publié
SELECT name, email FROM users
WHERE id IN (SELECT DISTINCT user_id FROM posts WHERE published = 1);

-- Compter les posts par user via sous-requête corrélée
SELECT name,
       (SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) AS nb_posts
FROM users;
```

<br>

---

## 3. UPDATE — Modifier des Données

```sql title="SQL — UPDATE : modifications simples, calculées, conditionnelles"
-- ─── Basique (TOUJOURS préciser WHERE) ────────────────────────────────────────
UPDATE users SET age = 29 WHERE id = 1;

-- Multi-colonnes
UPDATE users
SET name  = 'Alice Updated',
    email = 'alice.new@example.com',
    age   = 29
WHERE id = 1;

-- ─── Calculs ──────────────────────────────────────────────────────────────────
UPDATE products SET price = price * 1.10 WHERE category = 'electronics';
-- Augmenter tous les prix électronique de 10%

UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = 1;

-- ─── Conditions multiples ─────────────────────────────────────────────────────
UPDATE users
SET active = 0
WHERE last_login < date('now', '-6 months') AND active = 1;

-- ─── UPDATE conditionnel avec CASE ────────────────────────────────────────────
UPDATE users
SET category = CASE
    WHEN age < 18         THEN 'junior'
    WHEN age BETWEEN 18 AND 64 THEN 'adult'
    ELSE                       'senior'
END;

-- ─── Update depuis une autre table (sous-requête) ─────────────────────────────
UPDATE posts
SET author_name = (
    SELECT name FROM users WHERE users.id = posts.user_id
)
WHERE user_id IS NOT NULL;
```

!!! warning "Danger : UPDATE sans WHERE"
    `UPDATE users SET active = 0;` — sans `WHERE`, **toutes les lignes** sont modifiées. Toujours tester votre `WHERE` avec un `SELECT` avant d'exécuter un `UPDATE`.

<br>

---

## 4. DELETE — Supprimer des Données

```sql title="SQL — DELETE : suppressions ciblées et cascades"
-- ─── Basique ──────────────────────────────────────────────────────────────────
DELETE FROM users WHERE id = 1;

-- ─── Conditions multiples ─────────────────────────────────────────────────────
DELETE FROM users WHERE age < 18;
DELETE FROM users WHERE created_at < date('now', '-1 year');
DELETE FROM logs WHERE level = 'debug' AND created_at < date('now', '-7 days');

-- ─── Sous-requête ─────────────────────────────────────────────────────────────
DELETE FROM posts
WHERE user_id IN (
    SELECT id FROM users WHERE active = 0
);
-- Supprimer les posts des utilisateurs inactifs

-- ─── Vider une table sans supprimer sa structure ──────────────────────────────
DELETE FROM session_data;        -- Vide toutes les lignes

-- ─── Reset de l'AUTOINCREMENT après vidage ────────────────────────────────────
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name = 'users';
-- La prochaine insertion aura id=1 à nouveau
```

<br>

---

## 5. Contraintes d'Intégrité

Les contraintes définissent les règles que les données doivent respecter. Elles sont vérifiées à chaque `INSERT`, `UPDATE`, ou `DELETE`.

### PRIMARY KEY

```sql title="SQL — PRIMARY KEY : clé primaire simple et composite"
-- Clé primaire simple (entier auto-incrémenté — le plus courant)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrémenté, jamais réutilisé
    name TEXT NOT NULL
);

-- Clé primaire simple sans AUTOINCREMENT (rowid recyclé)
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,  -- Plus rapide qu'AUTOINCREMENT pour les bulks
    name TEXT
);

-- Clé primaire composite (sur plusieurs colonnes)
CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, role_id)  -- La combinaison doit être unique
);
```

### UNIQUE

```sql title="SQL — Contrainte UNIQUE"
-- Sur une colonne
CREATE TABLE users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,    -- Chaque email doit être unique
    name  TEXT NOT NULL
);

-- UNIQUE composite (la combinaison doit être unique)
CREATE TABLE event_registrations (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    UNIQUE (user_id, event_id)     -- Un user ne peut s'inscrire qu'une fois par event
);
```

### NOT NULL

```sql title="SQL — Contrainte NOT NULL"
CREATE TABLE articles (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,             -- Obligatoire
    content    TEXT NOT NULL,             -- Obligatoire
    summary    TEXT,                      -- Optionnel (NULL autorisé)
    author_id  INTEGER NOT NULL           -- Obligatoire
);
```

### CHECK

```sql title="SQL — Contrainte CHECK : règles métier sur les valeurs"
CREATE TABLE products (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    price    REAL NOT NULL CHECK(price > 0),           -- Prix strictement positif
    stock    INTEGER DEFAULT 0 CHECK(stock >= 0),       -- Stock non négatif
    rating   REAL CHECK(rating BETWEEN 0.0 AND 5.0),   -- Note entre 0 et 5
    status   TEXT DEFAULT 'draft'
                  CHECK(status IN ('draft', 'published', 'archived'))
    -- Status limité à 3 valeurs possibles (pseudo-enum)
);

-- CHECK composite (plusieurs colonnes)
CREATE TABLE events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date   TEXT NOT NULL,
    CHECK(end_date >= start_date)    -- La fin doit être après le début
);
```

### FOREIGN KEY

```sql title="SQL — FOREIGN KEY : intégrité référentielle"
-- Important : les clés étrangères sont DÉSACTIVÉES par défaut dans SQLite !
-- À activer à chaque connexion :
PRAGMA foreign_keys = ON;

-- Table parent
CREATE TABLE users (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table enfant avec référence
CREATE TABLE posts (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title   TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    --                                             ↑ Action si user supprimé
);

-- Actions ON DELETE / ON UPDATE disponibles :
-- CASCADE   : Supprime/met à jour les lignes enfants automatiquement
-- SET NULL  : Met la colonne à NULL (nécessite que la colonne accepte NULL)
-- RESTRICT  : Refuse la suppression si des enfants existent (défaut)
-- NO ACTION : Identique à RESTRICT pour SQLite
-- SET DEFAULT : Met la valeur DEFAULT (rarement utilisé)

CREATE TABLE comments (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
    -- Si un post est supprimé, ses commentaires le sont aussi
);

-- Vérifier si les FK sont activées
PRAGMA foreign_keys;  -- 0 = désactivé, 1 = activé

-- Vérifier les violations existantes
PRAGMA foreign_key_check;
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Schéma de blog complet**

```sql title="SQL — Exercice 1 : créer et peupler un schéma de blog"
-- Créez les tables avec toutes les contraintes appropriées :
-- users : id, username (unique), email (unique), created_at
-- posts : id, user_id (FK), title, content, status (draft/published), created_at
-- tags  : id, name (unique)
-- post_tags : post_id, tag_id (PK composite, FK vers posts et tags)

-- Insérez 3 users, 5 posts (3 publiés, 2 drafts), 4 tags
-- Associez des tags aux posts

-- Requêtes :
-- 1. Tous les posts publiés avec le nom de leur auteur
-- 2. Nombre de posts par user
-- 3. Users sans aucun post (sous-requête NOT IN)
-- 4. Insérer un post avec un user_id inexistant → erreur FK attendue
```

**Exercice 2 — UPSERT pratique**

```sql title="SQL — Exercice 2 : synchronisation de données avec UPSERT"
-- Vous recevez une liste de produits (id, name, price, stock)
-- Si le produit existe (même id) : mettez à jour price et stock
-- Sinon : insérez-le

-- Utilisez INSERT ... ON CONFLICT DO UPDATE
-- Vérifiez avec SELECT avant et après chaque UPSERT
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Le CRUD SQLite suit la syntaxe SQL standard avec des extensions pratiques : `INSERT OR IGNORE`, `INSERT OR REPLACE`, et le moderne `UPSERT` via `ON CONFLICT DO UPDATE`. **Toujours préciser `WHERE`** pour les `UPDATE` et `DELETE` — sans ça, toutes les lignes sont affectées. Les contraintes (`PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `FOREIGN KEY`) sont les gardiens de l'intégrité des données. Les **clés étrangères doivent être activées explicitement** (`PRAGMA foreign_keys = ON`) — elles sont désactivées par défaut dans SQLite.

> Dans le module suivant, nous construisons des **jointures et relations** — INNER JOIN, LEFT JOIN, sous-requêtes avancées, CTE (Common Table Expressions) et multi-tables.

<br>
