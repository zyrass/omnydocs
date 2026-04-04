---
description: "SQLite — Module 2 : Types de données (storage classes, type affinity), DDL complet (CREATE, ALTER, DROP), gestion des dates et heures."
icon: lucide/book-open-check
tags: ["SQLITE", "TYPES", "DDL", "CREATE", "ALTER", "DATES"]
---

# Types & Structure

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="3.43+"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Casier Multiformat"
    Un casier dans une librairie peut accueillir des livres de formats différents — poche, grand format, atlas. SQLite fonctionne de la même façon : ses colonnes ont une **affinité** (une préférence), pas une contrainte stricte. Une colonne `INTEGER` préfère les entiers mais peut accepter du texte si nécessaire. C'est ce qu'on appelle le **typing dynamique** — à l'opposé de MySQL où un `INT` refusera absolument du texte. Cette flexibilité est une caractéristique unique et puissante de SQLite.

<br>

---

## 1. Les 5 Storage Classes

SQLite ne stocke pas les données selon leur type déclaré mais selon leur **storage class** — la représentation réelle en mémoire.

```
Storage Class │ Description                          │ Exemples
──────────────┼──────────────────────────────────────┼─────────────────────
NULL          │ Valeur NULL (absence de valeur)      │ NULL
INTEGER       │ Entier signé (1 à 8 bytes)           │ 42, -100, 0
REAL          │ Nombre flottant IEEE 754 (8 bytes)   │ 3.14, -0.001, 2.5e10
TEXT          │ Chaîne de caractères (UTF-8/16)      │ 'Hello', "World"
BLOB          │ Données binaires brutes              │ x'0123456789ABCDEF'
```

```sql title="SQL — Vérifier le type réellement stocké avec typeof()"
CREATE TABLE test (col_int INTEGER, col_text TEXT, col_real REAL);

INSERT INTO test VALUES ('100', 123, '2.5');
-- SQLite applique les conversions d'affinité :
-- col_int  : STRING '100' → INTEGER 100 (conversion réussie)
-- col_text : INTEGER 123  → TEXT '123'  (tout devient texte)
-- col_real : STRING '2.5' → REAL 2.5   (conversion réussie)

SELECT
    typeof(col_int),   -- 'integer'
    typeof(col_text),  -- 'text'
    typeof(col_real)   -- 'real'
FROM test;
```

_`typeof()` révèle le type réellement stocké — pas le type déclaré dans le schéma._

<br>

---

## 2. Type Affinity (Affinité de Type)

Quand vous déclarez un type de colonne, SQLite détermine son **affinité** selon des règles simples :

| Type déclaré (exemples) | Affinité | Comportement |
|---|---|---|
| `INT`, `INTEGER`, `BIGINT`, `TINYINT` | **INTEGER** | Convertit en entier si possible |
| `TEXT`, `VARCHAR`, `CHAR`, `CLOB` | **TEXT** | Stocke comme texte |
| `REAL`, `FLOAT`, `DOUBLE` | **REAL** | Convertit en flottant si possible |
| `BLOB`, *(pas de type)* | **BLOB** | Stocke sans conversion |
| `DECIMAL`, `NUMERIC` | **NUMERIC** | Integer ou Real selon la valeur |

```sql title="SQL — Différence MySQL (strict) vs SQLite (flexible)"
-- MySQL/PostgreSQL : typage strict
CREATE TABLE strict_table (
    id   INT,          -- DOIT être un entier (erreur sinon)
    name VARCHAR(50)   -- DOIT être texte ≤ 50 chars
);

-- SQLite : type = affinité (préférence, pas contrainte)
CREATE TABLE flexible_table (
    id   INTEGER,  -- Préfère INTEGER, accepte d'autres types
    name TEXT      -- Préfère TEXT, accepte d'autres types
);

-- SQLite accepte sans erreur :
INSERT INTO flexible_table VALUES (1, 'Alice');     -- ✅ Types attendus
INSERT INTO flexible_table VALUES ('2', 'Bob');     -- ✅ '2' stocké comme 2 (INTEGER)
INSERT INTO flexible_table VALUES (3.5, 'Charlie'); -- ✅ 3.5 stocké comme 3 (INTEGER)
```

!!! warning "Piège : DECIMAL et la précision monétaire"
    `DECIMAL(10,2)` dans SQLite est traité comme `REAL` (flottant IEEE 754). Cela peut causer des erreurs de précision pour les montants financiers. **Solution : stocker les montants en centimes (INTEGER)** ou utiliser la fonction `ROUND()` pour les affichages.

<br>

---

## 3. Types Courants — Référence Pratique

```sql title="SQL — Types recommandés pour les cas d'usage courants"
CREATE TABLE products (
    -- ─── Entiers ─────────────────────────────────────────────────────────────
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto-incrémenté
    stock       INTEGER NOT NULL DEFAULT 0,         -- Stock (jamais négatif idéalement)
    category_id INTEGER,                            -- Clé étrangère

    -- ─── Texte ───────────────────────────────────────────────────────────────
    name        TEXT NOT NULL,                      -- Texte variable (pas de limite SQLite)
    description TEXT,                               -- Texte long
    code        TEXT UNIQUE,                        -- Code unique produit
    -- Note : VARCHAR(255) et CHAR(10) sont aussi TEXT en SQLite

    -- ─── Nombres décimaux ────────────────────────────────────────────────────
    price       REAL NOT NULL,                      -- Flottant 8 bytes
    -- Alternative pour monnaie : INTEGER (en centimes, 1999 = 19.99€)
    price_cents INTEGER,

    -- ─── Booléen (pas natif — convention 0/1) ────────────────────────────────
    active      INTEGER NOT NULL DEFAULT 1,         -- 0 = inactif, 1 = actif
    published   INTEGER NOT NULL DEFAULT 0,

    -- ─── Données binaires ────────────────────────────────────────────────────
    thumbnail   BLOB,                               -- Image binaire (petit fichier)

    -- ─── Dates (TEXT recommandé — format ISO8601) ─────────────────────────────
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- '2024-01-15 14:30:00'
    updated_at  TEXT,

    -- ─── JSON (TEXT avec validation optionnelle) ─────────────────────────────
    metadata    TEXT CHECK(metadata IS NULL OR json_valid(metadata))
);
```

<br>

---

## 4. Gestion des Dates et Heures

SQLite n'a **pas** de type DATE/TIME natif. Trois conventions coexistent :

```sql title="SQL — Trois façons de stocker les dates en SQLite"
-- ─── Option 1 : TEXT ISO8601 (RECOMMANDÉ) ─────────────────────────────────
-- Format : 'YYYY-MM-DD HH:MM:SS'  ou  'YYYY-MM-DDTHH:MM:SSZ'
CREATE TABLE events (
    id             INTEGER PRIMARY KEY,
    name           TEXT,
    event_date     TEXT,   -- '2024-06-15'
    event_datetime TEXT    -- '2024-06-15 14:30:00'
);

-- ─── Option 2 : INTEGER (Unix timestamp) ──────────────────────────────────
-- Nombre de secondes depuis le 1er janvier 1970
CREATE TABLE logs (
    id         INTEGER PRIMARY KEY,
    message    TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))
    -- strftime('%s', 'now') = timestamp Unix actuel
);

-- ─── Option 3 : REAL (Julian Day) — RARE ──────────────────────────────────
-- Nombre de jours depuis le 24 novembre 4714 av. J.-C.
CREATE TABLE rare_case (
    id          INTEGER PRIMARY KEY,
    date_julian REAL DEFAULT (julianday('now'))
);
```

### Fonctions de Date SQLite

```sql title="SQL — Fonctions date/heure SQLite : datetime(), strftime(), julianday()"
-- ─── Obtenir la date/heure actuelle ───────────────────────────────────────
SELECT date('now');               -- '2024-01-15'
SELECT time('now');               -- '14:30:00'
SELECT datetime('now');           -- '2024-01-15 14:30:00' (UTC)
SELECT strftime('%s', 'now');     -- '1705328400' (Unix timestamp)

-- ─── Formater les dates ───────────────────────────────────────────────────
SELECT strftime('%d/%m/%Y', 'now');           -- '15/01/2024'
SELECT strftime('%Y-%m-%d %H:%M', 'now');    -- '2024-01-15 14:30'
SELECT strftime('%A', 'now');                 -- 'Monday' (jour de la semaine)

-- ─── Arithmétique sur les dates ───────────────────────────────────────────
SELECT datetime('now', '+7 days');      -- Dans 7 jours
SELECT datetime('now', '-1 month');     -- Il y a 1 mois
SELECT datetime('now', '+3 hours');     -- Dans 3 heures
SELECT datetime('now', 'start of month'); -- Premier jour du mois courant
SELECT datetime('now', 'start of year');  -- 1er janvier de l'année courante

-- ─── Comparer des dates ───────────────────────────────────────────────────
-- Les dates TEXT ISO8601 sont comparables lexicographiquement
SELECT * FROM events
WHERE event_date > date('now')            -- Événements futurs
  AND event_date < date('now', '+30 days'); -- Dans les 30 prochains jours

-- ─── Extraire des composants ──────────────────────────────────────────────
SELECT strftime('%Y', created_at) AS year,
       strftime('%m', created_at) AS month,
       strftime('%d', created_at) AS day
FROM events;
```

<br>

---

## 5. DDL — Data Definition Language

### CREATE TABLE

```sql title="SQL — CREATE TABLE : options complètes"
-- Table standard
CREATE TABLE users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE IF NOT EXISTS (évite l'erreur si la table existe déjà)
CREATE TABLE IF NOT EXISTS posts (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    title      TEXT NOT NULL,
    content    TEXT,
    published  INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table temporaire (supprimée à la fin de la connexion)
CREATE TEMP TABLE session_data (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- Créer une table depuis une requête SELECT
CREATE TABLE active_users AS
SELECT id, name, email FROM users WHERE active = 1;
```

### ALTER TABLE

```sql title="SQL — ALTER TABLE : ajouter colonne, renommer"
-- ✅ Ajouter une colonne (supporté)
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN country TEXT DEFAULT 'France';

-- ✅ Renommer la table (supporté)
ALTER TABLE users RENAME TO customers;

-- ✅ Renommer une colonne (SQLite 3.25+)
ALTER TABLE users RENAME COLUMN name TO full_name;

-- ❌ Supprimer une colonne — NON SUPPORTÉ directement en SQLite < 3.35
-- ALTER TABLE users DROP COLUMN phone; -- ❌ Erreur < 3.35

-- ✅ Workaround pour modifications complexes (< 3.35)
BEGIN TRANSACTION;
  -- 1. Créer la nouvelle table avec la structure voulue
  CREATE TABLE users_new (
      id    INTEGER PRIMARY KEY AUTOINCREMENT,
      name  TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL
      -- phone supprimée
  );
  -- 2. Copier les données utiles
  INSERT INTO users_new SELECT id, name, email FROM users;
  -- 3. Supprimer l'ancienne
  DROP TABLE users;
  -- 4. Renommer la nouvelle
  ALTER TABLE users_new RENAME TO users;
COMMIT;
```

### DROP TABLE

```sql title="SQL — DROP TABLE"
-- Supprimer une table (définitif)
DROP TABLE users;

-- DROP IF EXISTS (évite l'erreur si la table n'existe pas)
DROP TABLE IF EXISTS temp_results;

-- Vider une table sans supprimer sa structure
DELETE FROM users;

-- Vider et reset de l'AUTOINCREMENT
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name = 'users';
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Typage dynamique**

```sql title="SQL — Exercice 1 : explorer le typage dynamique SQLite"
-- Créez cette table :
CREATE TABLE typing_test (
    col_integer INTEGER,
    col_text    TEXT,
    col_real    REAL,
    col_blob    BLOB
);

-- Insérez ces valeurs :
INSERT INTO typing_test VALUES ('42', 100, '3.14', 'binary data');

-- Utilisez typeof() pour vérifier les types réellement stockés
-- Comparez avec le type déclaré de chaque colonne
SELECT
    typeof(col_integer), -- Attendu : ?
    typeof(col_text),    -- Attendu : ?
    typeof(col_real),    -- Attendu : ?
    typeof(col_blob)     -- Attendu : ?
FROM typing_test;
```

**Exercice 2 — Système de dates**

```sql title="SQL — Exercice 2 : manipuler les dates SQLite"
-- Créez une table d'événements avec :
-- id (PK auto), name (TEXT), start_date (TEXT ISO8601), duration_hours (INTEGER)

-- Insérez 3 événements : un hier, un aujourd'hui, un dans 7 jours
-- Requêtes à écrire :
-- 1. Tous les événements futurs (start_date > aujourd'hui)
-- 2. La date de fin de chaque événement (start_date + duration_hours)
-- 3. Formater start_date en 'DD/MM/YYYY HH:MM'
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    SQLite utilise 5 **storage classes** (NULL, INTEGER, REAL, TEXT, BLOB) et un système d'**affinité de type** — les colonnes ont une préférence, pas une contrainte stricte. Les dates sont stockées en TEXT ISO8601 (`'YYYY-MM-DD HH:MM:SS'`) — c'est la convention recommandée car les comparaisons lexicographiques fonctionnent naturellement. `typeof()` révèle le type réel stocké. Le DDL (CREATE, ALTER, DROP) est standard avec quelques limitations : supprimer une colonne requiert une stratégie copier-renommer en SQLite < 3.35.

> Dans le module suivant, nous couvrons le **CRUD complet** (INSERT, SELECT, UPDATE, DELETE) et toutes les **contraintes d'intégrité** (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL).

<br>
