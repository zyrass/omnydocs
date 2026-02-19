---
description: "Guide exhaustif SQLite : concepts, syntaxe, optimisation, best practices production"
icon: lucide/book-open-check
tags: ["SQLITE", "DATABASE", "SQL", "FUNDAMENTALS"]
---

# SQLite — Fondamentaux

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🔴 Avancé"
  data-duration="6-8 heures"
  data-sections="12">
</div>

## Vue d'ensemble

!!! quote "Analogie pédagogique"
    _Imaginez une **bibliothèque personnelle ultra-organisée dans un seul classeur compact** : SQLite fonctionne comme un **système de classement autonome** où TOUTES vos données (livres = tables) sont stockées dans UN SEUL fichier `.db` transportable. **Contrairement bibliothèque municipale** (MySQL/PostgreSQL) nécessitant bâtiment dédié, personnel gardiens, système réservations complexe, horaires ouverture, **votre bibliothèque SQLite** = classeur portable ouvrable N'IMPORTE OÙ, N'IMPORTE QUAND, sans installation serveur, sans configuration réseau, sans authentification. **Fiches bibliothèque** = tables SQL (auteurs, livres, emprunts), **système classement Dewey** = index (recherche ultra-rapide), **règles emprunt** = contraintes (UNIQUE, FOREIGN KEY, CHECK), **transactions** = emprunter plusieurs livres simultanément (tout ou rien, jamais état incohérent). **SQLite = moteur base données le PLUS déployé monde** (milliards appareils) : navigateurs (Chrome, Firefox stockent historique), smartphones (iOS/Android apps natives), applications desktop (Skype, iTunes, Adobe), IoT devices, systèmes embarqués. **Zero-configuration, zero-administration, ultra-fiable** (tests exhaustifs 100% coverage, format stable 20+ ans), **performances excellentes** (<100Ko RAM, millions transactions/seconde NVMe), **ACID complet** (Atomicity, Consistency, Isolation, Durability garantis). C'est le **couteau suisse bases données** : simple débutants, puissant experts, production-ready immédiatement._

**SQLite en résumé :**

- ✅ **Serverless** = Pas de serveur séparé, bibliothèque intégrée application
- ✅ **Zero-configuration** = Pas de setup, pas d'admin, fonctionne immédiatement
- ✅ **Single-file** = Base données complète = 1 fichier `.db` portable
- ✅ **Cross-platform** = Windows, macOS, Linux, iOS, Android, embarqué
- ✅ **ACID** = Transactions atomiques, cohérentes, isolées, durables
- ✅ **SQL standard** = Syntaxe SQL classique (avec extensions pratiques)
- ✅ **Performant** = Millions requêtes/seconde, faible latence
- ✅ **Fiable** = Tests exhaustifs, stable depuis 20+ ans
- ✅ **Gratuit** = Public domain, aucune licence, usage commercial libre

**Guide structure :**

1. Introduction et concepts
2. Installation et premiers pas
3. Types de données SQLite
4. Opérations CRUD (Create, Read, Update, Delete)
5. Contraintes et intégrité données
6. Index et optimisation requêtes
7. Jointures et relations
8. Transactions et concurrence
9. Fonctions et expressions
10. Pragma et configuration
11. Best practices production
12. Cas d'usage et patterns

---

## Section 1 : Introduction et Concepts

### 1.1 Qu'est-ce que SQLite ?

**SQLite = Moteur base données SQL embarqué, serverless, zero-configuration**

```
Architecture Traditionnelle (MySQL/PostgreSQL) :
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│ Application │ ←─TCP──→ │ Serveur DB   │ ←────→ │ Fichiers DB  │
│  (Python)   │         │ (mysqld)     │         │ (.frm, .ibd) │
└─────────────┘         └──────────────┘         └──────────────┘
  Client                  Serveur                  Stockage

Architecture SQLite :
┌─────────────┐         ┌──────────────┐
│ Application │ ←────→ │ Fichier DB   │
│  (Python)   │         │ (app.db)     │
└─────────────┘         └──────────────┘
  Bibliothèque SQLite     Stockage direct
    intégrée app
```

**Différences fondamentales :**

| Critère | SQLite | MySQL/PostgreSQL |
|---------|--------|------------------|
| **Architecture** | Bibliothèque intégrée | Serveur client-serveur |
| **Configuration** | Aucune (zero-config) | Fichiers config, users, permissions |
| **Fichiers** | 1 fichier `.db` | Multiples fichiers, logs, config |
| **Réseau** | Accès local uniquement | TCP/IP, remote connections |
| **Concurrence** | Lecture multiple, écriture unique | Lecture/écriture simultanées |
| **Utilisateurs** | Aucun (filesystem permissions) | Users, roles, grants SQL |
| **Taille max** | 281 TB (théorique), 1 TB pratique | Quasi-illimitée |
| **Use case idéal** | Apps mobiles, desktop, IoT, prototypes | Web apps multi-users, haute concurrence |

### 1.2 Quand utiliser SQLite ?

**✅ Utilisez SQLite pour :**

- Applications mobiles (iOS, Android)
- Applications desktop (Electron, Qt, GTK)
- Prototypes et POCs (Proof of Concept)
- Embedded systems et IoT devices
- Applications single-user
- Cache local de données
- Stockage configuration app
- Testing et développement
- Analyse données locales (data science, ML)
- Static site generators (générateurs sites statiques)

**❌ N'utilisez PAS SQLite pour :**

- Applications web haute concurrence (>100 req écriture/seconde)
- Bases données très volumineuses (>100GB avec écritures fréquentes)
- Applications nécessitant accès réseau distant
- Systèmes distribués multi-serveurs
- Applications nécessitant permissions granulaires par utilisateur

### 1.3 Concepts fondamentaux

**Base de données = Fichier `.db` contenant tables**

```
myapp.db (fichier unique)
├── Table: users
│   ├── Colonnes: id, name, email, created_at
│   └── Lignes: 1000 users
├── Table: posts
│   ├── Colonnes: id, user_id, title, content
│   └── Lignes: 5000 posts
└── Table: comments
    ├── Colonnes: id, post_id, user_id, content
    └── Lignes: 15000 comments
```

**Table = Collection données structurées (lignes + colonnes)**

```
Table: users
┌────┬────────────┬─────────────────────┬─────────────────────┐
│ id │ name       │ email               │ created_at          │
├────┼────────────┼─────────────────────┼─────────────────────┤
│ 1  │ John Doe   │ john@example.com    │ 2024-01-15 10:30:00 │
│ 2  │ Jane Smith │ jane@example.com    │ 2024-01-16 14:20:00 │
│ 3  │ Bob Martin │ bob@example.com     │ 2024-01-17 09:15:00 │
└────┴────────────┴─────────────────────┴─────────────────────┘
```

**Colonne = Attribut données (type défini)**

```sql
-- Définition colonnes table users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,        -- Colonne entier, clé primaire
    name TEXT NOT NULL,            -- Colonne texte, obligatoire
    email TEXT UNIQUE,             -- Colonne texte, unique
    age INTEGER CHECK(age >= 18),  -- Colonne entier, contrainte >= 18
    created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- Colonne texte, valeur défaut
);
```

**Ligne = Enregistrement données (une entrée table)**

```sql
-- Insérer ligne (enregistrement)
INSERT INTO users (name, email, age) VALUES ('John Doe', 'john@example.com', 25);
-- Résultat : 1 ligne ajoutée avec id auto-incrémenté
```

---

## Section 2 : Installation et Premiers Pas

### 2.1 Installation SQLite

**SQLite est déjà installé sur la plupart systèmes :**

```bash
# Vérifier installation
sqlite3 --version
# Output : 3.43.2 2023-10-10 13:08:14 (exemple)

# Si absent, installer :

# Ubuntu/Debian
sudo apt update
sudo apt install sqlite3

# macOS (Homebrew)
brew install sqlite3

# Windows (télécharger depuis sqlite.org)
# https://www.sqlite.org/download.html
# Télécharger "sqlite-tools-win32-x86-*.zip"
# Extraire sqlite3.exe dans PATH
```

**Vérifier langages programmation :**

```python
# Python (intégré par défaut)
import sqlite3
print(sqlite3.version)  # Version bibliothèque Python
print(sqlite3.sqlite_version)  # Version SQLite

# Node.js (installer better-sqlite3)
npm install better-sqlite3

# PHP (extension pdo_sqlite généralement incluse)
php -m | grep sqlite  # Vérifier extension chargée
```

### 2.2 Créer première base données

**Via ligne de commande :**

```bash
# Créer/ouvrir base données (fichier créé si absent)
sqlite3 myapp.db

# Shell interactif SQLite ouvert :
# sqlite>
```

**Via Python :**

```python
import sqlite3

# Créer connexion (fichier créé si absent)
conn = sqlite3.connect('myapp.db')

# Créer curseur (exécuter requêtes)
cursor = conn.cursor()

# Exécuter requête
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
''')

# Commit changements
conn.commit()

# Fermer connexion
conn.close()

print("✅ Base données créée : myapp.db")
```

### 2.3 Commandes Shell SQLite

**Commandes utiles (préfixées `.`) :**

```sql
-- Afficher toutes tables
.tables

-- Afficher schéma table
.schema users

-- Afficher structure ALL tables
.schema

-- Afficher mode sortie (colonnes, liste, etc.)
.mode column  -- Affichage colonnes alignées
.mode csv     -- Output CSV
.mode json    -- Output JSON

-- Activer headers colonnes
.headers on

-- Importer CSV
.mode csv
.import data.csv users

-- Exporter table en CSV
.mode csv
.headers on
.output users.csv
SELECT * FROM users;
.output stdout  -- Revenir à sortie standard

-- Afficher infos base données
.databases

-- Exécuter script SQL externe
.read script.sql

-- Afficher temps exécution requêtes
.timer on

-- Quitter shell
.exit
-- ou
.quit
```

**Exemple session complète :**

```bash
$ sqlite3 myapp.db
SQLite version 3.43.2 2023-10-10 13:08:14
sqlite> .mode column
sqlite> .headers on
sqlite> 
sqlite> CREATE TABLE users (
   ...>     id INTEGER PRIMARY KEY,
   ...>     name TEXT,
   ...>     email TEXT
   ...> );
sqlite> 
sqlite> INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
sqlite> INSERT INTO users (name, email) VALUES ('Jane', 'jane@example.com');
sqlite> 
sqlite> SELECT * FROM users;
id  name  email
--  ----  ----------------
1   John  john@example.com
2   Jane  jane@example.com
sqlite> 
sqlite> .exit
```

---

## Section 3 : Types de Données SQLite

### 3.1 Storage Classes (Classes Stockage)

**SQLite utilise système typage dynamique avec 5 storage classes :**

```
Storage Class │ Description                        │ Exemples
──────────────┼────────────────────────────────────┼─────────────────────
NULL          │ Valeur NULL (absence valeur)       │ NULL
INTEGER       │ Entier signé (1-8 bytes)           │ 42, -100, 0
REAL          │ Nombre flottant (8 bytes)          │ 3.14, -0.001, 2.5e10
TEXT          │ Chaîne caractères (UTF-8/16)       │ 'Hello', "World"
BLOB          │ Données binaires brutes            │ x'0123456789ABCDEF'
```

**Différence avec SQL classique :**

```sql
-- MySQL/PostgreSQL : typage strict
CREATE TABLE users (
    id INT,           -- DOIT être entier
    name VARCHAR(50), -- DOIT être texte ≤ 50 chars
    age TINYINT       -- DOIT être petit entier
);

-- SQLite : typage flexible (type affinité, pas contrainte)
CREATE TABLE users (
    id INTEGER,   -- Affinity INTEGER (mais accepte autres types)
    name TEXT,    -- Affinity TEXT (mais accepte autres types)
    age INTEGER   -- Affinity INTEGER (mais accepte autres types)
);

-- SQLite accepte ça (flexible) :
INSERT INTO users VALUES (1, 'John', 25);      -- Types corrects
INSERT INTO users VALUES ('2', 'Jane', '30');  -- TEXT stocké comme INTEGER si possible
INSERT INTO users VALUES (3.5, 123, 'old');    -- REAL id, INTEGER name, TEXT age
```

### 3.2 Type Affinity (Affinité Type)

**SQLite convertit types selon "type affinity" colonne :**

```
Declared Type      │ Affinity   │ Comportement
───────────────────┼────────────┼────────────────────────────────────────
INT, INTEGER       │ INTEGER    │ Convertit en INTEGER si possible
VARCHAR, TEXT      │ TEXT       │ Stocke comme TEXT
REAL, FLOAT        │ REAL       │ Convertit en REAL si possible
BLOB               │ BLOB       │ Stocke données brutes
(aucun type)       │ BLOB       │ Pas de conversion
```

**Exemples conversions :**

```sql
CREATE TABLE test (
    col_int INTEGER,
    col_text TEXT,
    col_real REAL,
    col_blob BLOB
);

-- Insérer différentes valeurs
INSERT INTO test VALUES (42, 'hello', 3.14, x'DEADBEEF');
-- Résultat : types corrects stockés

INSERT INTO test VALUES ('100', 123, '2.5', 'binary');
-- Résultat après conversions affinité :
-- col_int   : 100 (TEXT→INTEGER)
-- col_text  : "123" (INTEGER→TEXT)
-- col_real  : 2.5 (TEXT→REAL)
-- col_blob  : "binary" (TEXT→BLOB)

-- Vérifier types réels stockés
SELECT 
    typeof(col_int),   -- "integer"
    typeof(col_text),  -- "text"
    typeof(col_real),  -- "real"
    typeof(col_blob)   -- "text" (car "binary" reste texte)
FROM test;
```

### 3.3 Types Déclarés Courants

**Types recommandés (compatibilité SQL standard) :**

```sql
CREATE TABLE products (
    -- Entiers
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrémenté
    stock INT NOT NULL DEFAULT 0,          -- Alias INTEGER
    quantity SMALLINT,                     -- Alias INTEGER
    big_number BIGINT,                     -- Alias INTEGER
    
    -- Texte
    name TEXT NOT NULL,                    -- Texte variable
    description VARCHAR(500),              -- Alias TEXT (limite ignorée SQLite)
    code CHAR(10),                         -- Alias TEXT
    
    -- Nombres décimaux
    price REAL NOT NULL,                   -- Flottant
    weight FLOAT,                          -- Alias REAL
    precision_value DOUBLE,                -- Alias REAL
    monetary DECIMAL(10,2),                -- Alias REAL (précision ignorée)
    
    -- Binaire
    image BLOB,                            -- Données binaires
    
    -- Booléen (pas natif SQLite, utilise INTEGER 0/1)
    active BOOLEAN DEFAULT 1,              -- Alias INTEGER
    
    -- Date/Heure (stocké comme TEXT ou INTEGER)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- TEXT ISO8601
    updated_timestamp INTEGER,             -- Unix timestamp (secondes depuis 1970)
    
    -- JSON (TEXT avec validation via CHECK)
    metadata JSON CHECK(json_valid(metadata))
);
```

### 3.4 Gestion Dates et Heures

**SQLite n'a PAS de type DATE/TIME natif. Utilise TEXT, REAL ou INTEGER :**

```sql
-- Option 1 : TEXT (ISO8601 format) - RECOMMANDÉ
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT,
    start_date TEXT,  -- Format : '2024-01-15'
    start_time TEXT,  -- Format : '14:30:00'
    start_datetime TEXT  -- Format : '2024-01-15 14:30:00' ou '2024-01-15T14:30:00Z'
);

-- Insérer dates courantes
INSERT INTO events (name, start_datetime) VALUES 
    ('Meeting', CURRENT_TIMESTAMP),     -- '2024-01-15 14:30:00'
    ('Conference', datetime('now')),    -- Fonction datetime()
    ('Workshop', datetime('now', '+7 days'));  -- Dans 7 jours

-- Option 2 : INTEGER (Unix timestamp)
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    message TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now'))  -- Timestamp Unix
);

-- Option 3 : REAL (Julian Day Numbers) - RARE
CREATE TABLE rare_case (
    id INTEGER PRIMARY KEY,
    date_julian REAL DEFAULT (julianday('now'))
);
```

**Fonctions date/heure SQLite :**

```sql
-- Obtenir date/heure actuelle
SELECT date('now');               -- '2024-01-15'
SELECT time('now');               -- '14:30:00'
SELECT datetime('now');           -- '2024-01-15 14:30:00'
SELECT julianday('now');          -- 2460326.104166667
SELECT strftime('%s', 'now');     -- 1705328400 (Unix timestamp)

-- Formater dates
SELECT strftime('%Y-%m-%d', 'now');           -- '2024-01-15'
SELECT strftime('%d/%m/%Y', 'now');           -- '15/01/2024'
SELECT strftime('%Y-%m-%d %H:%M:%S', 'now');  -- '2024-01-15 14:30:00'
SELECT strftime('%A, %B %d, %Y', 'now');      -- 'Monday, January 15, 2024'

-- Arithmétique dates
SELECT datetime('now', '+1 day');       -- Demain même heure
SELECT datetime('now', '-1 month');     -- Il y a 1 mois
SELECT datetime('now', '+3 hours');     -- Dans 3 heures
SELECT datetime('now', 'start of month');  -- Premier jour mois
SELECT datetime('now', 'start of year');   -- 1er janvier

-- Extraire composants
SELECT strftime('%Y', 'now') AS year;    -- 2024
SELECT strftime('%m', 'now') AS month;   -- 01
SELECT strftime('%d', 'now') AS day;     -- 15
SELECT strftime('%H', 'now') AS hour;    -- 14
SELECT strftime('%M', 'now') AS minute;  -- 30

-- Comparaisons dates
SELECT * FROM events 
WHERE start_datetime > datetime('now', '-7 days');  -- Derniers 7 jours

SELECT * FROM logs
WHERE created_at > strftime('%s', 'now', '-1 hour');  -- Dernière heure
```

---

## Section 4 : Opérations CRUD

### 4.1 CREATE - Créer Table

```sql
-- Syntaxe basique
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER CHECK(age >= 0),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- CREATE IF NOT EXISTS (évite erreur si table existe)
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    -- Contrainte clé étrangère
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table temporaire (supprimée fin connexion)
CREATE TEMP TABLE temp_results (
    id INTEGER,
    value TEXT
);

-- Créer table depuis requête existante
CREATE TABLE active_users AS
SELECT * FROM users WHERE active = 1;
```

### 4.2 INSERT - Insérer Données

```sql
-- Syntaxe basique
INSERT INTO users (name, email, age) VALUES ('John Doe', 'john@example.com', 25);

-- Insérer toutes colonnes (ordre schéma)
INSERT INTO users VALUES (NULL, 'Jane Smith', 'jane@example.com', 30, CURRENT_TIMESTAMP);

-- Insérer multiples lignes
INSERT INTO users (name, email, age) VALUES 
    ('Bob Martin', 'bob@example.com', 28),
    ('Alice Johnson', 'alice@example.com', 32),
    ('Charlie Brown', 'charlie@example.com', 45);

-- INSERT OR IGNORE (ignore si contrainte violée)
INSERT OR IGNORE INTO users (name, email, age) 
VALUES ('John Doe', 'john@example.com', 25);
-- Si email existe déjà (UNIQUE), ignore silencieusement

-- INSERT OR REPLACE (remplace si contrainte violée)
INSERT OR REPLACE INTO users (id, name, email, age) 
VALUES (1, 'John Updated', 'john@example.com', 26);
-- Si id=1 existe, update. Sinon insert.

-- UPSERT (SQLite 3.24+)
INSERT INTO users (name, email, age) 
VALUES ('John Doe', 'john@example.com', 25)
ON CONFLICT(email) DO UPDATE SET 
    name = excluded.name,
    age = excluded.age;
-- Si email existe, update name et age. Sinon insert.

-- Insérer depuis SELECT
INSERT INTO archived_users 
SELECT * FROM users WHERE created_at < date('now', '-1 year');

-- Obtenir ID dernière insertion
-- Python :
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('John', 'john@example.com'))
last_id = cursor.lastrowid
print(f"ID inséré : {last_id}")

-- SQL :
SELECT last_insert_rowid();
```

### 4.3 SELECT - Lire Données

```sql
-- Sélectionner toutes colonnes
SELECT * FROM users;

-- Sélectionner colonnes spécifiques
SELECT id, name, email FROM users;

-- Avec alias colonnes
SELECT 
    id AS user_id,
    name AS full_name,
    email AS contact_email
FROM users;

-- WHERE : filtrer lignes
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE name = 'John Doe';
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- Opérateurs WHERE
SELECT * FROM users WHERE age > 18;              -- Supérieur
SELECT * FROM users WHERE age >= 18;             -- Supérieur ou égal
SELECT * FROM users WHERE age < 65;              -- Inférieur
SELECT * FROM users WHERE age <= 65;             -- Inférieur ou égal
SELECT * FROM users WHERE age = 25;              -- Égal
SELECT * FROM users WHERE age != 25;             -- Différent
SELECT * FROM users WHERE age <> 25;             -- Différent (alias)
SELECT * FROM users WHERE age BETWEEN 18 AND 65; -- Entre valeurs
SELECT * FROM users WHERE age IN (18, 25, 30);   -- Dans liste
SELECT * FROM users WHERE name LIKE 'J%';        -- Pattern (commence J)
SELECT * FROM users WHERE email IS NULL;         -- NULL
SELECT * FROM users WHERE email IS NOT NULL;     -- NOT NULL

-- Combinaisons logiques
SELECT * FROM users WHERE age >= 18 AND age <= 65;  -- ET
SELECT * FROM users WHERE age < 18 OR age > 65;     -- OU
SELECT * FROM users WHERE NOT (age < 18);           -- NON

-- ORDER BY : trier résultats
SELECT * FROM users ORDER BY age ASC;         -- Ascendant (défaut)
SELECT * FROM users ORDER BY age DESC;        -- Descendant
SELECT * FROM users ORDER BY age, name;       -- Multi-colonnes
SELECT * FROM users ORDER BY created_at DESC; -- Plus récent d'abord

-- LIMIT : limiter résultats
SELECT * FROM users LIMIT 10;                 -- 10 premiers
SELECT * FROM users LIMIT 10 OFFSET 20;       -- 10 résultats, skip 20
SELECT * FROM users ORDER BY id DESC LIMIT 5; -- 5 plus récents

-- DISTINCT : valeurs uniques
SELECT DISTINCT age FROM users;               -- Ages uniques
SELECT DISTINCT country FROM users;           -- Pays uniques

-- Agrégations
SELECT COUNT(*) FROM users;                   -- Nombre total
SELECT COUNT(*) FROM users WHERE age >= 18;   -- Nombre adultes
SELECT AVG(age) FROM users;                   -- Âge moyen
SELECT SUM(age) FROM users;                   -- Somme âges
SELECT MIN(age) FROM users;                   -- Âge minimum
SELECT MAX(age) FROM users;                   -- Âge maximum

-- GROUP BY : grouper résultats
SELECT age, COUNT(*) FROM users GROUP BY age; -- Compte par âge
SELECT country, AVG(age) FROM users GROUP BY country; -- Âge moyen par pays

-- HAVING : filtrer groupes (après GROUP BY)
SELECT age, COUNT(*) as count 
FROM users 
GROUP BY age 
HAVING count > 5;  -- Groupes avec >5 personnes

-- Sous-requêtes
SELECT * FROM users 
WHERE age > (SELECT AVG(age) FROM users);  -- Plus vieux que moyenne

SELECT name, email FROM users 
WHERE id IN (SELECT user_id FROM posts WHERE published = 1);  -- Users avec posts publiés
```

### 4.4 UPDATE - Mettre à Jour Données

```sql
-- Syntaxe basique (ATTENTION : sans WHERE, update TOUTES lignes)
UPDATE users SET age = 26 WHERE id = 1;

-- Update multiples colonnes
UPDATE users 
SET 
    name = 'John Updated',
    age = 26,
    email = 'john.new@example.com'
WHERE id = 1;

-- Update avec conditions multiples
UPDATE users 
SET age = age + 1 
WHERE age < 65 AND active = 1;

-- Update avec calculs
UPDATE products 
SET price = price * 1.1  -- Augmenter prix 10%
WHERE category = 'electronics';

UPDATE users 
SET updated_at = CURRENT_TIMESTAMP 
WHERE id = 1;

-- Update depuis autre table (JOIN)
UPDATE posts 
SET author_name = (
    SELECT name FROM users WHERE users.id = posts.user_id
)
WHERE user_id IS NOT NULL;

-- Update conditionnel (CASE)
UPDATE users 
SET status = CASE
    WHEN age < 18 THEN 'minor'
    WHEN age >= 18 AND age < 65 THEN 'adult'
    ELSE 'senior'
END;

-- Obtenir nombre lignes affectées
-- Python :
cursor.execute("UPDATE users SET age = 26 WHERE id = 1")
rows_affected = cursor.rowcount
print(f"Lignes modifiées : {rows_affected}")
```

### 4.5 DELETE - Supprimer Données

```sql
-- Syntaxe basique (ATTENTION : sans WHERE, supprime TOUTES lignes)
DELETE FROM users WHERE id = 1;

-- Delete avec conditions
DELETE FROM users WHERE age < 18;
DELETE FROM users WHERE created_at < date('now', '-1 year');

-- Delete avec sous-requête
DELETE FROM posts 
WHERE user_id IN (
    SELECT id FROM users WHERE active = 0
);

-- Delete toutes lignes (garde structure table)
DELETE FROM temp_table;

-- Obtenir nombre lignes supprimées
-- Python :
cursor.execute("DELETE FROM users WHERE age < 18")
rows_deleted = cursor.rowcount
print(f"Lignes supprimées : {rows_deleted}")

-- TRUNCATE (pas standard SQLite, utiliser DELETE)
-- Pour vider table complètement et reset AUTOINCREMENT :
DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name='users';  -- Reset auto-increment
```

### 4.6 ALTER TABLE - Modifier Structure

```sql
-- Ajouter colonne
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN country TEXT DEFAULT 'France';

-- Renommer table
ALTER TABLE users RENAME TO customers;

-- Renommer colonne (SQLite 3.25+)
ALTER TABLE users RENAME COLUMN name TO full_name;

-- SQLite NE SUPPORTE PAS (limitations) :
-- ALTER TABLE users DROP COLUMN phone;        -- ❌ Pas possible
-- ALTER TABLE users MODIFY COLUMN age REAL;   -- ❌ Pas possible
-- ALTER TABLE users ADD CONSTRAINT ...;       -- ❌ Pas possible directement

-- Workaround pour modifications complexes :
-- 1. Créer nouvelle table avec structure voulue
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,  -- Renommée
    email TEXT UNIQUE NOT NULL,
    -- phone supprimée
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 2. Copier données
INSERT INTO users_new (id, full_name, email, created_at)
SELECT id, name, email, created_at FROM users;

-- 3. Supprimer ancienne table
DROP TABLE users;

-- 4. Renommer nouvelle table
ALTER TABLE users_new RENAME TO users;
```

### 4.7 DROP TABLE - Supprimer Table

```sql
-- Supprimer table (définitif)
DROP TABLE users;

-- DROP IF EXISTS (évite erreur si table absente)
DROP TABLE IF EXISTS temp_results;
```

---

## Section 5 : Contraintes et Intégrité Données

### 5.1 PRIMARY KEY (Clé Primaire)

**PRIMARY KEY = Identifiant unique chaque ligne (NOT NULL + UNIQUE automatique)**

```sql
-- Syntaxe basique
CREATE TABLE users (
    id INTEGER PRIMARY KEY,  -- Clé primaire simple
    name TEXT
);

-- AUTOINCREMENT (recommandé pour id auto-généré)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrémenté
    name TEXT
);

-- Différence avec/sans AUTOINCREMENT :
-- SANS : Réutilise IDs supprimés (1,2,3 → delete 2 → insert → 2)
-- AVEC : Ne réutilise JAMAIS IDs (1,2,3 → delete 2 → insert → 4)

-- Clé primaire composite (multiple colonnes)
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date TEXT,
    PRIMARY KEY (student_id, course_id)  -- Combinaison unique
);

-- Clé primaire sur autre type (TEXT, rare mais possible)
CREATE TABLE countries (
    code TEXT PRIMARY KEY,  -- 'FR', 'US', 'UK'
    name TEXT
);
```

**Règles PRIMARY KEY :**

```sql
-- ✅ AUTORISÉ
INSERT INTO users (name) VALUES ('John');  -- id auto-généré

-- ❌ INTERDIT : Violer unicité PRIMARY KEY
INSERT INTO users (id, name) VALUES (1, 'Jane');  -- Si id=1 existe déjà
-- Error: UNIQUE constraint failed: users.id

-- ❌ INTERDIT : NULL sur PRIMARY KEY
INSERT INTO users (id, name) VALUES (NULL, 'Bob');  -- NULL impossible
-- Mais AUTOINCREMENT génère automatiquement
```

### 5.2 NOT NULL (Non Null)

**NOT NULL = Colonne DOIT avoir valeur (NULL interdit)**

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,           -- Obligatoire
    description TEXT,             -- Optionnel (NULL autorisé)
    price REAL NOT NULL,          -- Obligatoire
    stock INTEGER NOT NULL DEFAULT 0  -- Obligatoire avec défaut
);

-- ✅ AUTORISÉ
INSERT INTO products (name, price) VALUES ('Laptop', 999.99);
-- stock=0 (défaut), description=NULL (autorisé)

-- ❌ INTERDIT : NULL sur colonne NOT NULL
INSERT INTO products (name, description) VALUES ('Mouse', 'USB mouse');
-- Error: NOT NULL constraint failed: products.price
```

### 5.3 UNIQUE (Unicité)

**UNIQUE = Valeur unique dans table (NULL autorisé sauf PRIMARY KEY)**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,   -- Email unique obligatoire
    username TEXT UNIQUE,         -- Username unique optionnel
    phone TEXT                    -- Phone non-unique optionnel
);

-- ✅ AUTORISÉ
INSERT INTO users (email, username) VALUES ('john@example.com', 'john_doe');
INSERT INTO users (email, username) VALUES ('jane@example.com', NULL);  -- username NULL OK
INSERT INTO users (email, username) VALUES ('bob@example.com', NULL);   -- Multiple NULL OK

-- ❌ INTERDIT : Violer UNIQUE
INSERT INTO users (email) VALUES ('john@example.com');
-- Error: UNIQUE constraint failed: users.email

-- UNIQUE sur multiples colonnes (combinaison unique)
CREATE TABLE user_courses (
    user_id INTEGER,
    course_id INTEGER,
    UNIQUE(user_id, course_id)  -- Paire unique
);
```

### 5.4 CHECK (Contrainte Vérification)

**CHECK = Condition validation personnalisée**

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),              -- Prix positif
    discount_percent INTEGER CHECK(discount_percent BETWEEN 0 AND 100),  -- 0-100%
    stock INTEGER NOT NULL CHECK(stock >= 0),          -- Stock non-négatif
    status TEXT CHECK(status IN ('active', 'inactive', 'discontinued'))  -- Valeurs fixes
);

-- ✅ AUTORISÉ
INSERT INTO products (name, price, discount_percent, stock, status) 
VALUES ('Laptop', 999.99, 10, 50, 'active');

-- ❌ INTERDIT : Violer CHECK
INSERT INTO products (name, price, discount_percent, stock, status) 
VALUES ('Mouse', -10, 150, -5, 'unknown');
-- Error: CHECK constraint failed: price > 0

-- CHECK avec multiples conditions
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    age INTEGER CHECK(age >= 18 AND age <= 120),  -- Adultes seulement
    email TEXT CHECK(email LIKE '%@%')            -- Email basique validation
);

-- CHECK au niveau table (référence multiples colonnes)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    subtotal REAL,
    tax REAL,
    total REAL,
    CHECK(total = subtotal + tax)  -- Total cohérent
);
```

### 5.5 DEFAULT (Valeur Par Défaut)

**DEFAULT = Valeur automatique si non fournie**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    active BOOLEAN DEFAULT 1,                    -- Actif par défaut
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,   -- Date actuelle
    country TEXT DEFAULT 'France',               -- Pays défaut
    attempts INTEGER DEFAULT 0                   -- Compteur zéro
);

-- ✅ INSERT sans spécifier colonnes DEFAULT
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
-- Résultat : active=1, created_at=maintenant, country='France', attempts=0

-- DEFAULT avec expressions
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),  -- Unix timestamp
    random_id TEXT DEFAULT (hex(randomblob(16)))         -- ID aléatoire
);
```

### 5.6 FOREIGN KEY (Clé Étrangère)

**FOREIGN KEY = Référence autre table (intégrité référentielle)**

```sql
-- IMPORTANT : Activer foreign keys (désactivées par défaut SQLite)
PRAGMA foreign_keys = ON;

-- Définir foreign key
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Référence users.id
);

-- ✅ AUTORISÉ : user_id existant
INSERT INTO users (name) VALUES ('John');  -- id=1
INSERT INTO posts (user_id, title, content) VALUES (1, 'First Post', 'Content...');

-- ❌ INTERDIT : user_id inexistant
INSERT INTO posts (user_id, title, content) VALUES (999, 'Invalid Post', 'Content...');
-- Error: FOREIGN KEY constraint failed

-- Actions ON DELETE / ON UPDATE
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT,
    
    -- CASCADE : supprime posts si user supprimé
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    content TEXT,
    
    -- SET NULL : met NULL si post supprimé
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE SET NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    total REAL,
    
    -- RESTRICT : empêche suppression si orders existent (défaut)
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT
);

-- NO ACTION : similaire RESTRICT (défaut SQLite)
-- SET DEFAULT : met valeur DEFAULT si parent supprimé (rare)
```

**Vérifier contraintes foreign key :**

```sql
-- Activer enforcement
PRAGMA foreign_keys = ON;

-- Vérifier si activé
PRAGMA foreign_keys;  -- Retourne 1 si ON, 0 si OFF

-- Vérifier violations existantes (avant activer)
PRAGMA foreign_key_check;

-- Vérifier violations table spécifique
PRAGMA foreign_key_check(posts);
```

---

## Section 6 : Index et Optimisation Requêtes

### 6.1 Index Concept

**Index = Structure données accélère recherches (comme index livre)**

```
Sans index (Full Table Scan) :
Table users (1,000,000 lignes)
SELECT * FROM users WHERE email = 'john@example.com';
→ Scan 1,000,000 lignes (lent, ~500ms)

Avec index sur email (Binary Tree Search) :
SELECT * FROM users WHERE email = 'john@example.com';
→ Lookup index, jump directement ligne (rapide, ~1ms)
```

**Structure index (B-Tree simplifié) :**

```
Index sur colonne 'age' :
        [30]
       /    \
    [20]    [40]
    / \     / \
  [10][25][35][50]
   |  |   |   |
  lignes table
```

### 6.2 Créer Index

```sql
-- Index simple (colonne unique)
CREATE INDEX idx_users_email ON users(email);

-- Index composite (multiples colonnes)
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);

-- Index UNIQUE (garantit unicité + accélère)
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Index conditionnel (partial index)
CREATE INDEX idx_active_users ON users(email) WHERE active = 1;
-- Indexe seulement users actifs (plus petit, plus rapide)

-- Index expression
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Accélère recherches insensibles casse

-- Vérifier index existants
SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'index';

-- Supprimer index
DROP INDEX idx_users_email;

-- IF EXISTS
DROP INDEX IF EXISTS idx_users_email;
```

### 6.3 Quand Créer Index

**✅ Créez index quand :**

```sql
-- Colonnes dans WHERE fréquemment
SELECT * FROM users WHERE email = ?;  -- Index sur email
SELECT * FROM posts WHERE user_id = ?;  -- Index sur user_id

-- Colonnes dans JOIN
SELECT * FROM posts 
JOIN users ON posts.user_id = users.id;  -- Index sur user_id

-- Colonnes dans ORDER BY
SELECT * FROM users ORDER BY created_at DESC;  -- Index sur created_at

-- Colonnes avec UNIQUE constraint (index auto-créé)
-- PRIMARY KEY (index auto-créé)

-- Colonnes FOREIGN KEY (recommandé)
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

**❌ N'indexez PAS quand :**

```sql
-- Tables très petites (<1000 lignes)
-- Overhead index > bénéfice

-- Colonnes modifiées fréquemment
-- Chaque UPDATE/INSERT/DELETE doit mettre à jour index (coût)

-- Colonnes avec peu valeurs distinctes (low cardinality)
-- Exemple : genre (M/F), boolean (0/1)
-- Index inefficace, full scan souvent plus rapide

-- Colonnes rarement utilisées dans requêtes
-- Index consomme espace disque inutilement
```

### 6.4 EXPLAIN QUERY PLAN

**Analyser comment SQLite exécute requête :**

```sql
-- Sans index
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'john@example.com';

-- Output :
-- SCAN users  (full table scan, lent)

-- Créer index
CREATE INDEX idx_users_email ON users(email);

-- Avec index
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'john@example.com';

-- Output :
-- SEARCH users USING INDEX idx_users_email (email=?)  (rapide)
```

**Exemples analysis :**

```sql
-- Example 1 : JOIN sans index
EXPLAIN QUERY PLAN
SELECT * FROM posts JOIN users ON posts.user_id = users.id;
-- Output :
-- SCAN posts
-- SEARCH users USING INTEGER PRIMARY KEY (rowid=?)

-- Example 2 : ORDER BY sans index
EXPLAIN QUERY PLAN
SELECT * FROM users ORDER BY created_at DESC;
-- Output :
-- SCAN users
-- USE TEMP B-TREE FOR ORDER BY  (nécessite tri, lent)

-- Créer index
CREATE INDEX idx_users_created ON users(created_at);

EXPLAIN QUERY PLAN
SELECT * FROM users ORDER BY created_at DESC;
-- Output :
-- SCAN users USING INDEX idx_users_created  (déjà trié, rapide)
```

### 6.5 Optimisation Requêtes

**Techniques optimisation :**

```sql
-- 1. Utiliser index covering (toutes colonnes dans index)
CREATE INDEX idx_users_email_name ON users(email, name);
SELECT name FROM users WHERE email = ?;  -- Query entière dans index

-- 2. Éviter SELECT *
-- ❌ Lent
SELECT * FROM users WHERE email = ?;

-- ✅ Rapide
SELECT id, name, email FROM users WHERE email = ?;

-- 3. Utiliser LIMIT
-- ❌ Charge toutes lignes
SELECT * FROM users ORDER BY created_at DESC;

-- ✅ Limite résultats
SELECT * FROM users ORDER BY created_at DESC LIMIT 20;

-- 4. Éviter OR dans WHERE (utiliser IN ou UNION)
-- ❌ Lent (index non utilisé)
SELECT * FROM users WHERE age = 25 OR age = 30 OR age = 35;

-- ✅ Rapide (index utilisé)
SELECT * FROM users WHERE age IN (25, 30, 35);

-- 5. Éviter fonctions dans WHERE (empêche index)
-- ❌ Index non utilisé
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- ✅ Index utilisé (si email déjà lowercase DB)
SELECT * FROM users WHERE email = 'john@example.com';

-- Ou créer index expression
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';  -- OK

-- 6. Utiliser EXISTS au lieu COUNT
-- ❌ Lent (compte tout)
SELECT CASE WHEN (SELECT COUNT(*) FROM posts WHERE user_id = 1) > 0 THEN 1 ELSE 0 END;

-- ✅ Rapide (stop dès première trouvée)
SELECT EXISTS(SELECT 1 FROM posts WHERE user_id = 1);

-- 7. Dénormaliser si nécessaire (copier données éviter JOIN)
-- Au lieu JOIN systématique :
SELECT posts.*, users.name FROM posts JOIN users ON posts.user_id = users.id;

-- Ajouter colonne author_name dans posts (dénormalisé)
ALTER TABLE posts ADD COLUMN author_name TEXT;
UPDATE posts SET author_name = (SELECT name FROM users WHERE id = posts.user_id);

-- Query plus simple :
SELECT * FROM posts;  -- Pas de JOIN
```

---

## Section 7 : Jointures et Relations

### 7.1 Types de Jointures

**Diagramme Venn jointures :**

```
INNER JOIN       LEFT JOIN        RIGHT JOIN       FULL OUTER JOIN
(intersection)   (gauche + inter) (droite + inter) (tout)

   A    B           A    B           A    B           A    B
  ┌─┐  ┌─┐         ┌─┐  ┌─┐         ┌─┐  ┌─┐         ┌─┐  ┌─┐
  │ └──┘ │         │████│ │         │ │████│         │████████│
  └──────┘         └────┘ │         │ └────┘         │████████│
                          └─┘       └─┘              └────────┘
```

### 7.2 INNER JOIN

**INNER JOIN = Lignes présentes dans LES DEUX tables**

```sql
-- Syntaxe explicite (recommandée)
SELECT 
    users.id,
    users.name,
    posts.title,
    posts.content
FROM users
INNER JOIN posts ON users.id = posts.user_id;

-- Alias tables (raccourci)
SELECT 
    u.id,
    u.name,
    p.title,
    p.content
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

-- INNER JOIN multiple tables
SELECT 
    u.name AS author,
    p.title AS post_title,
    c.content AS comment_content
FROM users u
INNER JOIN posts p ON u.id = p.user_id
INNER JOIN comments c ON p.id = c.post_id;

-- WHERE avec JOIN
SELECT 
    u.name,
    p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE p.published = 1 AND u.active = 1;

-- Jointure implicite (ancienne syntaxe, éviter)
SELECT users.name, posts.title
FROM users, posts
WHERE users.id = posts.user_id;  -- Condition WHERE au lieu ON
```

**Exemple données :**

```
Table users :
┌────┬───────┐
│ id │ name  │
├────┼───────┤
│ 1  │ John  │
│ 2  │ Jane  │
│ 3  │ Bob   │
└────┴───────┘

Table posts :
┌────┬─────────┬───────────┐
│ id │ user_id │ title     │
├────┼─────────┼───────────┤
│ 1  │ 1       │ Post A    │
│ 2  │ 1       │ Post B    │
│ 3  │ 2       │ Post C    │
└────┴─────────┴───────────┘

INNER JOIN résultat :
┌─────┬───────────┐
│ name│ title     │
├─────┼───────────┤
│ John│ Post A    │
│ John│ Post B    │
│ Jane│ Post C    │
└─────┴───────────┘
(Bob absent : pas de posts)
```

### 7.3 LEFT JOIN

**LEFT JOIN = TOUTES lignes table gauche + matching droite (NULL si pas match)**

```sql
-- Syntaxe
SELECT 
    u.id,
    u.name,
    p.title
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;

-- Résultat (reprend exemple précédent) :
┌────┬──────┬────────┐
│ id │ name │ title  │
├────┼──────┼────────┤
│ 1  │ John │ Post A │
│ 1  │ John │ Post B │
│ 2  │ Jane │ Post C │
│ 3  │ Bob  │ NULL   │  ← Bob inclus (pas de posts)
└────┴──────┴────────┘

-- Trouver users SANS posts (LEFT JOIN + WHERE NULL)
SELECT 
    u.id,
    u.name
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE p.id IS NULL;  -- Pas de post associé

-- Résultat :
┌────┬──────┐
│ id │ name │
├────┼──────┤
│ 3  │ Bob  │
└────┴──────┘

-- LEFT JOIN avec COUNT
SELECT 
    u.name,
    COUNT(p.id) AS posts_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name;

-- Résultat :
┌──────┬──────────────┐
│ name │ posts_count  │
├──────┼──────────────┤
│ John │ 2            │
│ Jane │ 1            │
│ Bob  │ 0            │  ← 0 posts (pas NULL)
└──────┴──────────────┘
```

### 7.4 CROSS JOIN

**CROSS JOIN = Produit cartésien (toutes combinaisons possibles)**

```sql
-- Syntaxe explicite
SELECT 
    colors.name AS color,
    sizes.name AS size
FROM colors
CROSS JOIN sizes;

-- Syntaxe implicite (comma join)
SELECT 
    colors.name AS color,
    sizes.name AS size
FROM colors, sizes;

-- Exemple :
Table colors :
┌────┬───────┐
│ id │ name  │
├────┼───────┤
│ 1  │ Red   │
│ 2  │ Blue  │
└────┴───────┘

Table sizes :
┌────┬───────┐
│ id │ name  │
├────┼───────┤
│ 1  │ Small │
│ 2  │ Large │
└────┴───────┘

CROSS JOIN résultat (2 × 2 = 4 lignes) :
┌──────┬───────┐
│ color│ size  │
├──────┼───────┤
│ Red  │ Small │
│ Red  │ Large │
│ Blue │ Small │
│ Blue │ Large │
└──────┴───────┘

-- Use case : générer combinaisons
-- Exemple : produits × couleurs × tailles
```

### 7.5 SELF JOIN

**SELF JOIN = Table jointe à elle-même (relations hiérarchiques)**

```sql
-- Exemple : Employés + Managers (même table)
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    manager_id INTEGER,  -- Référence employees.id
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

INSERT INTO employees VALUES 
    (1, 'Alice', NULL),    -- CEO (pas de manager)
    (2, 'Bob', 1),         -- Manager : Alice
    (3, 'Charlie', 1),     -- Manager : Alice
    (4, 'David', 2),       -- Manager : Bob
    (5, 'Eve', 2);         -- Manager : Bob

-- SELF JOIN : Employé + son manager
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Résultat :
┌──────────┬─────────┐
│ employee │ manager │
├──────────┼─────────┤
│ Alice    │ NULL    │  ← CEO
│ Bob      │ Alice   │
│ Charlie  │ Alice   │
│ David    │ Bob     │
│ Eve      │ Bob     │
└──────────┴─────────┘

-- Compter subordonnés par manager
SELECT 
    m.name AS manager,
    COUNT(e.id) AS direct_reports
FROM employees m
LEFT JOIN employees e ON m.id = e.manager_id
GROUP BY m.id, m.name;

-- Hiérarchie complète (CTE récursif, voir section avancée)
```

---

## Section 8 : Transactions et Concurrence

### 8.1 Concept Transactions

**Transaction = Séquence opérations exécutées comme UNITÉ ATOMIQUE (tout ou rien)**

**Propriétés ACID :**

```
A - Atomicity (Atomicité)
    Tout réussit OU tout échoue (jamais état partiel)
    
C - Consistency (Cohérence)
    DB passe d'état cohérent à état cohérent
    
I - Isolation (Isolation)
    Transactions concurrentes s'exécutent isolément
    
D - Durability (Durabilité)
    Changements committés persistants (même crash)
```

### 8.2 Syntaxe Transactions

```sql
-- Démarrer transaction explicite
BEGIN TRANSACTION;

-- Opérations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Valider transaction (persistant)
COMMIT;

-- OU annuler transaction (rollback)
-- ROLLBACK;
```

**Transaction complète exemple (transfert bancaire) :**

```sql
-- Transfert 100€ : Account 1 → Account 2
BEGIN TRANSACTION;

-- Vérifier solde suffisant
SELECT balance FROM accounts WHERE id = 1;
-- Si balance >= 100 :

-- Débiter compte source
UPDATE accounts SET balance = balance - 100 WHERE id = 1;

-- Créditer compte destination
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Vérifier cohérence
SELECT SUM(balance) FROM accounts;  -- Total doit être identique

-- Si tout OK
COMMIT;

-- Si erreur quelconque
-- ROLLBACK;  -- Annule TOUTES modifications
```

### 8.3 Transaction Automatiques

**SQLite mode autocommit par défaut :**

```sql
-- Chaque statement = transaction automatique
INSERT INTO users (name) VALUES ('John');  -- BEGIN + COMMIT automatique
UPDATE users SET name = 'Jane' WHERE id = 1;  -- BEGIN + COMMIT automatique

-- Équivalent explicite :
BEGIN TRANSACTION;
INSERT INTO users (name) VALUES ('John');
COMMIT;
```

**Désactiver autocommit (Python) :**

```python
import sqlite3

# Connection par défaut : autocommit OFF (transaction manuelle)
conn = sqlite3.connect('myapp.db')

# Insérer données (pas committed automatiquement)
cursor = conn.cursor()
cursor.execute("INSERT INTO users (name) VALUES ('John')")

# DOIT commit manuellement
conn.commit()

# OU rollback
# conn.rollback()
```

### 8.4 Modes Transaction SQLite

**SQLite 3 modes transaction (journal_mode) :**

```sql
-- Vérifier mode actuel
PRAGMA journal_mode;

-- Mode DELETE (défaut, compatible)
PRAGMA journal_mode = DELETE;
-- Journal supprimé après commit

-- Mode WAL (Write-Ahead Logging, recommandé production)
PRAGMA journal_mode = WAL;
-- Meilleure concurrence lecture/écriture
-- Lecteurs ne bloquent PAS écrivain
-- Écrivain ne bloque PAS lecteurs

-- Mode MEMORY (rapide, dangereux)
PRAGMA journal_mode = MEMORY;
-- Journal en RAM (perdu si crash)
```

**Avantages WAL mode :**

```
Mode DELETE (défaut) :
- Écrivain : LOCK exclusif (lecteurs bloqués)
- Lecteurs : LOCK partagé (écrivain bloqué)

Mode WAL (recommandé) :
- Écrivain : Écrit dans WAL file (lecteurs continuent)
- Lecteurs : Lisent dernière version committée
- Concurrence : Meilleure performance multi-threads
```

### 8.5 Niveaux Isolation (Locking)

**SQLite utilise locking database-level (pas row-level) :**

```
Lock Types :
┌──────────┬────────────────────────────────────────┐
│ UNLOCKED │ Pas de lock, DB fermée                 │
├──────────┼────────────────────────────────────────┤
│ SHARED   │ Lecture OK, écriture bloquée           │
├──────────┼────────────────────────────────────────┤
│ RESERVED │ 1 écrivain prépare, lecteurs continuent│
├──────────┼────────────────────────────────────────┤
│ PENDING  │ Attend lecteurs finir                  │
├──────────┼────────────────────────────────────────┤
│ EXCLUSIVE│ Écrit, tout bloqué                     │
└──────────┴────────────────────────────────────────┘
```

**Timeout lock (Python) :**

```python
import sqlite3

# Timeout 5 secondes si DB locked
conn = sqlite3.connect('myapp.db', timeout=5.0)

try:
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = 'John' WHERE id = 1")
    conn.commit()
except sqlite3.OperationalError as e:
    print(f"Database locked: {e}")
    conn.rollback()
```

### 8.6 Savepoints (Points Sauvegarde)

**SAVEPOINT = Point intermédiaire transaction (rollback partiel possible)**

```sql
BEGIN TRANSACTION;

INSERT INTO users (name) VALUES ('John');
SAVEPOINT sp1;  -- Point sauvegarde 1

INSERT INTO users (name) VALUES ('Jane');
SAVEPOINT sp2;  -- Point sauvegarde 2

INSERT INTO users (name) VALUES ('Bob');

-- Erreur sur Bob, rollback à sp2
ROLLBACK TO sp2;  -- Annule seulement Bob
-- John et Jane toujours là

-- Continuer transaction
INSERT INTO users (name) VALUES ('Alice');

COMMIT;  -- John, Jane, Alice committés (Bob annulé)
```

---

## Section 9 : Fonctions et Expressions

### 9.1 Fonctions Agrégation

```sql
-- COUNT : Compter lignes
SELECT COUNT(*) FROM users;                -- Total lignes
SELECT COUNT(email) FROM users;            -- Compte non-NULL
SELECT COUNT(DISTINCT country) FROM users; -- Pays uniques

-- SUM : Somme valeurs
SELECT SUM(price) FROM orders;             -- Total prix
SELECT SUM(quantity * price) FROM orders;  -- Total montant

-- AVG : Moyenne
SELECT AVG(age) FROM users;                -- Âge moyen
SELECT AVG(price) FROM products WHERE category = 'electronics';

-- MIN / MAX : Minimum / Maximum
SELECT MIN(price) FROM products;           -- Prix minimum
SELECT MAX(created_at) FROM posts;         -- Post plus récent

-- GROUP_CONCAT : Concaténer valeurs
SELECT GROUP_CONCAT(name, ', ') FROM users;  -- "John, Jane, Bob"
SELECT GROUP_CONCAT(DISTINCT country) FROM users;  -- Pays uniques

-- Combinaisons
SELECT 
    category,
    COUNT(*) AS total_products,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM products
GROUP BY category;
```

### 9.2 Fonctions String

```sql
-- LENGTH : Longueur chaîne
SELECT LENGTH('Hello');  -- 5
SELECT name FROM users WHERE LENGTH(name) > 10;

-- SUBSTR : Sous-chaîne
SELECT SUBSTR('Hello World', 1, 5);  -- 'Hello' (index 1-based)
SELECT SUBSTR(email, 1, INSTR(email, '@') - 1) FROM users;  -- Username email

-- UPPER / LOWER : Casse
SELECT UPPER('hello');  -- 'HELLO'
SELECT LOWER('WORLD');  -- 'world'
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- TRIM : Supprimer espaces
SELECT TRIM('  hello  ');       -- 'hello'
SELECT LTRIM('  hello');        -- 'hello'
SELECT RTRIM('hello  ');        -- 'hello'
SELECT TRIM('x', 'xxxhelloxxx'); -- 'hello'

-- REPLACE : Remplacer sous-chaîne
SELECT REPLACE('Hello World', 'World', 'SQLite');  -- 'Hello SQLite'
SELECT REPLACE(phone, '-', '') FROM users;  -- Supprimer tirets

-- INSTR : Position sous-chaîne
SELECT INSTR('Hello World', 'World');  -- 7 (index 1-based)
SELECT * FROM users WHERE INSTR(email, '@gmail.com') > 0;

-- || : Concaténation
SELECT 'Hello' || ' ' || 'World';  -- 'Hello World'
SELECT first_name || ' ' || last_name AS full_name FROM users;

-- LIKE : Pattern matching
SELECT * FROM users WHERE email LIKE '%@gmail.com';     -- Termine @gmail.com
SELECT * FROM users WHERE name LIKE 'J%';               -- Commence J
SELECT * FROM users WHERE name LIKE '%son';             -- Termine son
SELECT * FROM users WHERE name LIKE '%o%';              -- Contient o
SELECT * FROM users WHERE phone LIKE '06________';      -- 10 chiffres (06...)

-- GLOB : Pattern matching (case-sensitive)
SELECT * FROM files WHERE name GLOB '*.txt';            -- Extension .txt
SELECT * FROM files WHERE name GLOB '[0-9]*';           -- Commence chiffre
```

### 9.3 Fonctions Mathématiques

```sql
-- ABS : Valeur absolue
SELECT ABS(-10);  -- 10

-- ROUND : Arrondir
SELECT ROUND(3.14159, 2);  -- 3.14
SELECT ROUND(price) FROM products;

-- CAST : Conversion type
SELECT CAST(3.14 AS INTEGER);  -- 3
SELECT CAST('123' AS INTEGER); -- 123
SELECT CAST(price AS TEXT) FROM products;

-- RANDOM : Nombre aléatoire
SELECT RANDOM();              -- Entier aléatoire
SELECT ABS(RANDOM() % 100);   -- 0-99

-- MIN / MAX : Plus petit / grand (non agrégation)
SELECT MIN(10, 20, 5);  -- 5
SELECT MAX(10, 20, 5);  -- 20

-- Opérateurs arithmétiques
SELECT 10 + 5;   -- 15
SELECT 10 - 5;   -- 5
SELECT 10 * 5;   -- 50
SELECT 10 / 5;   -- 2
SELECT 10 % 3;   -- 1 (modulo)
```

### 9.4 Fonctions Date/Heure

```sql
-- Obtenir date/heure actuelle
SELECT date('now');                -- '2024-01-15'
SELECT time('now');                -- '14:30:00'
SELECT datetime('now');            -- '2024-01-15 14:30:00'
SELECT julianday('now');           -- 2460326.104166667
SELECT strftime('%s', 'now');      -- 1705328400 (Unix timestamp)

-- Arithmétique dates
SELECT date('now', '+1 day');      -- Demain
SELECT date('now', '-7 days');     -- Il y a 7 jours
SELECT date('now', '+1 month');    -- Dans 1 mois
SELECT date('now', '-1 year');     -- Il y a 1 an
SELECT date('now', 'start of month');  -- Premier jour mois
SELECT date('now', 'start of year');   -- 1er janvier

-- Formater dates (strftime)
SELECT strftime('%Y-%m-%d', 'now');          -- '2024-01-15'
SELECT strftime('%d/%m/%Y', 'now');          -- '15/01/2024'
SELECT strftime('%Y-%m-%d %H:%M:%S', 'now'); -- '2024-01-15 14:30:00'
SELECT strftime('%w', 'now');                -- 1 (jour semaine 0=dimanche)
SELECT strftime('%j', 'now');                -- 15 (jour année)
SELECT strftime('%W', 'now');                -- 03 (semaine année)

-- Extraire composants
SELECT strftime('%Y', 'now') AS year;    -- 2024
SELECT strftime('%m', 'now') AS month;   -- 01
SELECT strftime('%d', 'now') AS day;     -- 15
SELECT strftime('%H', 'now') AS hour;    -- 14

-- Différence dates
SELECT julianday('2024-12-31') - julianday('2024-01-01');  -- 365.0 jours
SELECT (julianday('now') - julianday(created_at)) AS days_old FROM posts;

-- Comparer dates
SELECT * FROM events WHERE date(start_date) = date('now');  -- Aujourd'hui
SELECT * FROM events WHERE date(start_date) > date('now');  -- Futurs
```

### 9.5 Fonctions Conditionnelles

```sql
-- CASE : Condition switch
SELECT 
    name,
    age,
    CASE
        WHEN age < 18 THEN 'Minor'
        WHEN age >= 18 AND age < 65 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group
FROM users;

-- IIF : If inline (SQLite 3.32+)
SELECT 
    name,
    IIF(age >= 18, 'Adult', 'Minor') AS status
FROM users;

-- IFNULL : Valeur si NULL
SELECT IFNULL(phone, 'No phone') FROM users;
SELECT IFNULL(email, 'no-email@example.com') FROM users;

-- COALESCE : Première valeur non-NULL
SELECT COALESCE(phone, mobile, email, 'No contact') FROM users;

-- NULLIF : NULL si égal
SELECT NULLIF(discount, 0) FROM products;  -- NULL si discount=0
```

### 9.6 Fonctions Système

```sql
-- LAST_INSERT_ROWID : Dernier ID inséré
INSERT INTO users (name) VALUES ('John');
SELECT last_insert_rowid();  -- ID nouvellement inséré

-- CHANGES : Lignes affectées dernière requête
UPDATE users SET active = 1;
SELECT changes();  -- Nombre lignes modifiées

-- TOTAL_CHANGES : Lignes affectées depuis connexion
SELECT total_changes();

-- SQLITE_VERSION : Version SQLite
SELECT sqlite_version();  -- '3.43.2'

-- TYPEOF : Type valeur
SELECT typeof(42);         -- 'integer'
SELECT typeof(3.14);       -- 'real'
SELECT typeof('hello');    -- 'text'
SELECT typeof(NULL);       -- 'null'
SELECT typeof(x'FF');      -- 'blob'
```

---

## Section 10 : Pragma et Configuration

### 10.1 Pragma Essentiels

**PRAGMA = Commandes configuration/interrogation SQLite**

```sql
-- Afficher toutes PRAGMAs
PRAGMA;

-- Foreign keys (désactivées par défaut, IMPORTANT activer)
PRAGMA foreign_keys = ON;   -- Activer
PRAGMA foreign_keys;         -- Vérifier (retourne 1 si ON)

-- Journal mode (WAL recommandé production)
PRAGMA journal_mode = WAL;   -- Activer WAL
PRAGMA journal_mode;         -- Vérifier mode actuel

-- Synchronous (compromise performance/sécurité)
PRAGMA synchronous = FULL;   -- Sécurité maximale (défaut)
PRAGMA synchronous = NORMAL; -- Compromise (recommandé WAL)
PRAGMA synchronous = OFF;    -- Rapide, dangereux (tests uniquement)

-- Cache size (mémoire utilisée)
PRAGMA cache_size = -64000;  -- 64MB cache (négatif = kibibytes)
PRAGMA cache_size;           -- Vérifier taille

-- Page size (taille page DB)
PRAGMA page_size = 4096;     -- 4KB par page (défaut, optimal)
-- DOIT être défini AVANT création tables

-- Auto vacuum (récupération espace)
PRAGMA auto_vacuum = FULL;   -- Compactage automatique
PRAGMA auto_vacuum = INCREMENTAL; -- Manuel via PRAGMA incremental_vacuum
PRAGMA auto_vacuum = NONE;   -- Désactivé (défaut)

-- Temp store (stockage données temporaires)
PRAGMA temp_store = MEMORY;  -- RAM (rapide)
PRAGMA temp_store = FILE;    -- Disque (économise RAM)

-- Integrity check (vérifier corruption)
PRAGMA integrity_check;      -- Vérifier intégrité complète
PRAGMA quick_check;          -- Vérification rapide
```

### 10.2 Informations Base Données

```sql
-- Liste tables
SELECT name FROM sqlite_master WHERE type='table';

-- Schéma table
SELECT sql FROM sqlite_master WHERE name='users';

-- Liste index
SELECT name FROM sqlite_master WHERE type='index';

-- Taille base données
SELECT page_count * page_size AS size FROM pragma_page_count(), pragma_page_size();

-- Statistiques table
PRAGMA table_info(users);     -- Colonnes + types
PRAGMA index_list(users);     -- Index sur table
PRAGMA foreign_key_list(posts); -- Foreign keys table

-- Nombre pages libres
PRAGMA freelist_count;

-- Compacter base données (récupérer espace)
VACUUM;  -- Compacte TOUTE DB (peut être long)
```

### 10.3 Optimisation Performance

```sql
-- Analyser statistiques tables (améliore query planner)
ANALYZE;                     -- Toutes tables
ANALYZE users;               -- Table spécifique

-- Optimiser base données
PRAGMA optimize;             -- Lance optimisations recommandées

-- Vider caches
PRAGMA shrink_memory;        -- Libère mémoire inutilisée

-- WAL checkpoint (flush WAL → DB principale)
PRAGMA wal_checkpoint(FULL); -- Flush complet WAL

-- Mesurer performance query
.timer on                    -- Activer timer (shell SQLite)
SELECT * FROM users;
.timer off
```

### 10.4 Configuration Recommandée Production

```sql
-- Configuration optimale production (WAL mode)
PRAGMA journal_mode = WAL;        -- Meilleure concurrence
PRAGMA synchronous = NORMAL;      -- Bon compromise (WAL safe)
PRAGMA cache_size = -64000;       -- 64MB cache
PRAGMA foreign_keys = ON;         -- Intégrité référentielle
PRAGMA temp_store = MEMORY;       -- Temp en RAM
PRAGMA mmap_size = 268435456;     -- 256MB memory-mapped I/O

-- Vérifier config active
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA cache_size;
PRAGMA foreign_keys;

-- Maintenance régulière (cron job)
-- PRAGMA optimize;    -- Quotidien
-- VACUUM;             -- Mensuel
-- PRAGMA wal_checkpoint(TRUNCATE);  -- Hebdomadaire
```

---

## Section 11 : Best Practices Production

### 11.1 Sécurité : SQL Injection Prevention

**❌ DANGER : Concaténation SQL (JAMAIS faire ça)**

```python
# ❌ VULNÉRABLE SQL Injection
user_input = "admin' OR '1'='1"
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# SQL exécuté : SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Retourne TOUS users (bypass authentification)

cursor.execute(query)  # ❌ DANGER
```

**✅ SÉCURISÉ : Parameterized Queries**

```python
# ✅ SAFE : Parameterized query
user_input = "admin' OR '1'='1"
cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
# SQL exécuté : SELECT * FROM users WHERE username = 'admin'' OR ''1''=''1'
# Cherche littéralement username "admin' OR '1'='1" (pas trouvé)

# Multiple paramètres
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ('John Doe', 'john@example.com', 25)
)

# Named parameters
cursor.execute(
    "SELECT * FROM users WHERE name = :name AND age > :age",
    {'name': 'John', 'age': 18}
)
```

### 11.2 Backup et Restore

**Backup base données :**

```bash
# Backup complet (ligne commande)
sqlite3 myapp.db ".backup myapp_backup.db"

# Backup avec compression
sqlite3 myapp.db ".backup myapp_backup.db" && gzip myapp_backup.db

# Dump SQL (texte lisible)
sqlite3 myapp.db .dump > myapp_dump.sql

# Restore depuis dump
sqlite3 myapp_new.db < myapp_dump.sql

# Backup programmatique (Python)
import sqlite3
import shutil

# Simple copy
shutil.copy2('myapp.db', 'myapp_backup.db')

# Backup avec vacuum
source = sqlite3.connect('myapp.db')
backup = sqlite3.connect('myapp_backup.db')
source.backup(backup)
backup.close()
source.close()
```

**Stratégie backup production :**

```bash
#!/bin/bash
# backup_sqlite.sh

DB_PATH="/var/www/myapp/database.db"
BACKUP_DIR="/backups/sqlite"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/myapp_$DATE.db"

# Créer backup
sqlite3 $DB_PATH ".backup $BACKUP_FILE"

# Compresser
gzip $BACKUP_FILE

# Garder seulement 30 derniers jours
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

# Log
echo "Backup created: $BACKUP_FILE.gz"

# Cron job (quotidien 2h du matin) :
# 0 2 * * * /path/to/backup_sqlite.sh
```

### 11.3 Gestion Erreurs

```python
import sqlite3

def safe_execute(conn, query, params=None):
    """Execute query avec gestion erreurs robuste"""
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
        
    except sqlite3.IntegrityError as e:
        # Contrainte violée (UNIQUE, FOREIGN KEY, etc.)
        conn.rollback()
        print(f"Integrity error: {e}")
        raise
        
    except sqlite3.OperationalError as e:
        # DB locked, syntax error, etc.
        conn.rollback()
        print(f"Operational error: {e}")
        raise
        
    except sqlite3.DatabaseError as e:
        # Erreur générique database
        conn.rollback()
        print(f"Database error: {e}")
        raise
        
    except Exception as e:
        # Catch-all
        conn.rollback()
        print(f"Unexpected error: {e}")
        raise

# Usage
try:
    conn = sqlite3.connect('myapp.db', timeout=10)
    safe_execute(conn, "INSERT INTO users (email) VALUES (?)", ('john@example.com',))
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
finally:
    conn.close()
```

### 11.4 Connection Pool (Multi-threading)

```python
import sqlite3
from queue import Queue
from threading import Thread

class SQLiteConnectionPool:
    """Pool connexions SQLite thread-safe"""
    
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.pool = Queue(maxsize=max_connections)
        
        # Pré-créer connexions
        for _ in range(max_connections):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            self.pool.put(conn)
    
    def get_connection(self):
        """Obtenir connexion depuis pool"""
        return self.pool.get()
    
    def return_connection(self, conn):
        """Retourner connexion au pool"""
        self.pool.put(conn)
    
    def close_all(self):
        """Fermer toutes connexions"""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

# Usage
pool = SQLiteConnectionPool('myapp.db', max_connections=10)

def worker(pool, user_data):
    """Thread worker"""
    conn = pool.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (user_data,))
        conn.commit()
    finally:
        pool.return_connection(conn)

# Créer multiples threads
threads = []
for i in range(100):
    t = Thread(target=worker, args=(pool, f'User {i}'))
    threads.append(t)
    t.start()

# Attendre fin
for t in threads:
    t.join()

pool.close_all()
```

### 11.5 Monitoring Performance

```python
import sqlite3
import time

def monitor_query(conn, query, params=None):
    """Monitor performance query"""
    start = time.time()
    
    cursor = conn.cursor()
    
    # EXPLAIN QUERY PLAN
    explain_query = f"EXPLAIN QUERY PLAN {query}"
    cursor.execute(explain_query, params or ())
    plan = cursor.fetchall()
    
    # Execute query
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    
    duration = (time.time() - start) * 1000  # ms
    
    print(f"Query: {query}")
    print(f"Duration: {duration:.2f}ms")
    print(f"Rows: {len(results)}")
    print(f"Plan: {plan}")
    
    if duration > 100:  # Slow query threshold
        print("⚠️  SLOW QUERY DETECTED")
    
    return results

# Usage
conn = sqlite3.connect('myapp.db')
monitor_query(conn, "SELECT * FROM users WHERE age > ?", (18,))
```

---

## Section 12 : Cas d'Usage et Patterns

### 12.1 Application Mobile (iOS/Android)

```python
# Configuration optimale mobile app
import sqlite3

def setup_mobile_db(db_path):
    """Configure SQLite pour app mobile"""
    conn = sqlite3.connect(db_path)
    
    # Configuration optimale mobile
    conn.execute("PRAGMA journal_mode=WAL")      # Meilleure concurrence
    conn.execute("PRAGMA synchronous=NORMAL")    # Compromise
    conn.execute("PRAGMA cache_size=-8000")      # 8MB cache (économie batterie)
    conn.execute("PRAGMA temp_store=MEMORY")     # Temp en RAM
    conn.execute("PRAGMA foreign_keys=ON")       # Intégrité
    
    return conn

# Schema exemple app mobile
schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    sync_status INTEGER DEFAULT 0,  -- 0=local, 1=synced
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    read INTEGER DEFAULT 0,
    sync_status INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_messages_user ON messages(user_id);
CREATE INDEX idx_messages_unread ON messages(user_id, read) WHERE read = 0;
"""

conn = setup_mobile_db('mobile_app.db')
conn.executescript(schema)
conn.close()
```

### 12.2 Cache Local Web Application

```python
# Cache SQLite pour web app
class SQLiteCache:
    """Cache local avec expiration"""
    
    def __init__(self, db_path='cache.db'):
        self.conn = sqlite3.connect(db_path)
        self.setup()
    
    def setup(self):
        """Créer table cache"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                expires_at INTEGER NOT NULL
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_expires ON cache(expires_at)")
        self.conn.commit()
    
    def set(self, key, value, ttl=3600):
        """Store value avec TTL (secondes)"""
        import time
        expires_at = int(time.time()) + ttl
        
        self.conn.execute(
            "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
            (key, value, expires_at)
        )
        self.conn.commit()
    
    def get(self, key):
        """Retrieve value (None si expiré)"""
        import time
        
        cursor = self.conn.execute(
            "SELECT value FROM cache WHERE key = ? AND expires_at > ?",
            (key, int(time.time()))
        )
        result = cursor.fetchone()
        return result[0] if result else None
    
    def cleanup(self):
        """Supprimer entrées expirées"""
        import time
        self.conn.execute("DELETE FROM cache WHERE expires_at < ?", (int(time.time()),))
        self.conn.commit()

# Usage
cache = SQLiteCache()
cache.set('user:123', '{"name": "John", "email": "john@example.com"}', ttl=3600)
user_data = cache.get('user:123')
print(user_data)
```

### 12.3 Data Analysis (Pandas Integration)

```python
import sqlite3
import pandas as pd

# Connexion
conn = sqlite3.connect('analytics.db')

# Pandas → SQLite
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob'],
    'age': [25, 30, 35],
    'city': ['Paris', 'Lyon', 'Marseille']
})

df.to_sql('users', conn, if_exists='replace', index=False)

# SQLite → Pandas
query = "SELECT * FROM users WHERE age > 25"
df_result = pd.read_sql_query(query, conn)
print(df_result)

# Analyse complexe
analysis_query = """
SELECT 
    city,
    COUNT(*) as count,
    AVG(age) as avg_age,
    MIN(age) as min_age,
    MAX(age) as max_age
FROM users
GROUP BY city
"""
df_stats = pd.read_sql_query(analysis_query, conn)
print(df_stats)

conn.close()
```

### 12.4 Configuration Storage

```python
# Configuration app avec SQLite
class ConfigStore:
    """Store configuration key-value"""
    
    def __init__(self, db_path='config.db'):
        self.conn = sqlite3.connect(db_path)
        self.setup()
    
    def setup(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                type TEXT NOT NULL,  -- 'string', 'int', 'float', 'bool', 'json'
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def set(self, key, value):
        """Store config value (auto-detect type)"""
        import json
        
        if isinstance(value, bool):
            type_str, value_str = 'bool', str(int(value))
        elif isinstance(value, int):
            type_str, value_str = 'int', str(value)
        elif isinstance(value, float):
            type_str, value_str = 'float', str(value)
        elif isinstance(value, (dict, list)):
            type_str, value_str = 'json', json.dumps(value)
        else:
            type_str, value_str = 'string', str(value)
        
        self.conn.execute(
            "INSERT OR REPLACE INTO config (key, value, type) VALUES (?, ?, ?)",
            (key, value_str, type_str)
        )
        self.conn.commit()
    
    def get(self, key, default=None):
        """Retrieve config value"""
        import json
        
        cursor = self.conn.execute(
            "SELECT value, type FROM config WHERE key = ?", (key,)
        )
        result = cursor.fetchone()
        
        if not result:
            return default
        
        value_str, type_str = result
        
        if type_str == 'bool':
            return bool(int(value_str))
        elif type_str == 'int':
            return int(value_str)
        elif type_str == 'float':
            return float(value_str)
        elif type_str == 'json':
            return json.loads(value_str)
        else:
            return value_str

# Usage
config = ConfigStore()
config.set('app_name', 'MyApp')
config.set('debug', True)
config.set('max_connections', 100)
config.set('features', ['feature_a', 'feature_b'])

print(config.get('app_name'))        # 'MyApp'
print(config.get('debug'))           # True
print(config.get('max_connections')) # 100
print(config.get('features'))        # ['feature_a', 'feature_b']
```

### 12.5 Full-Text Search

```sql
-- Créer table FTS5 (Full-Text Search)
CREATE VIRTUAL TABLE articles_fts USING fts5(
    title,
    content,
    author
);

-- Insérer données
INSERT INTO articles_fts (title, content, author) VALUES 
    ('SQLite Tutorial', 'Learn SQLite fundamentals and advanced concepts', 'John Doe'),
    ('Python Guide', 'Comprehensive Python programming guide', 'Jane Smith'),
    ('SQLite Performance', 'Optimize SQLite queries for production', 'Bob Martin');

-- Recherche full-text
SELECT * FROM articles_fts WHERE articles_fts MATCH 'sqlite';
-- Retourne articles contenant "sqlite" (case-insensitive)

-- Recherche phrase exacte
SELECT * FROM articles_fts WHERE articles_fts MATCH '"sqlite fundamentals"';

-- Recherche multiple mots (AND)
SELECT * FROM articles_fts WHERE articles_fts MATCH 'sqlite performance';

-- Recherche OR
SELECT * FROM articles_fts WHERE articles_fts MATCH 'sqlite OR python';

-- Recherche NOT
SELECT * FROM articles_fts WHERE articles_fts MATCH 'sqlite NOT performance';

-- Recherche colonne spécifique
SELECT * FROM articles_fts WHERE articles_fts MATCH 'title:sqlite';

-- Ranking (pertinence)
SELECT *, rank FROM articles_fts 
WHERE articles_fts MATCH 'sqlite' 
ORDER BY rank;

-- Highlight résultats
SELECT highlight(articles_fts, 1, '<b>', '</b>') AS highlighted_content
FROM articles_fts 
WHERE articles_fts MATCH 'sqlite';
```

---

## Checklist Complète SQLite

### Concepts Fondamentaux
- [ ] Comprendre architecture serverless SQLite
- [ ] Connaître différences SQL traditionnel vs SQLite
- [ ] Maîtriser quand utiliser/ne pas utiliser SQLite
- [ ] Comprendre propriétés ACID

### Installation et Configuration
- [ ] SQLite installé et fonctionnel
- [ ] Shell sqlite3 maîtrisé
- [ ] Commandes `.` shell connues
- [ ] Connexion depuis langage programmation

### Types de Données
- [ ] 5 storage classes maîtrisées
- [ ] Type affinity comprise
- [ ] Gestion dates/heures (TEXT/INTEGER/REAL)
- [ ] Fonctions date/heure utilisées

### Opérations CRUD
- [ ] CREATE TABLE avec contraintes
- [ ] INSERT (simple, multiple, UPSERT)
- [ ] SELECT avec WHERE, ORDER BY, LIMIT
- [ ] UPDATE avec conditions
- [ ] DELETE sécurisé
- [ ] ALTER TABLE (limitations connues)

### Contraintes
- [ ] PRIMARY KEY (AUTOINCREMENT)
- [ ] NOT NULL appliqué
- [ ] UNIQUE configuré
- [ ] CHECK contraintes validées
- [ ] DEFAULT valeurs définies
- [ ] FOREIGN KEY avec ON DELETE/UPDATE

### Index et Performance
- [ ] Index créés colonnes fréquentes
- [ ] EXPLAIN QUERY PLAN utilisé
- [ ] Index composite compris
- [ ] Techniques optimisation appliquées
- [ ] Quand indexer/ne pas indexer connu

### Jointures
- [ ] INNER JOIN maîtrisé
- [ ] LEFT JOIN utilisé correctement
- [ ] CROSS JOIN compris
- [ ] SELF JOIN pour hiérarchies

### Transactions
- [ ] BEGIN/COMMIT/ROLLBACK maîtrisés
- [ ] ACID properties comprises
- [ ] WAL mode activé production
- [ ] SAVEPOINT utilisé si nécessaire
- [ ] Gestion locks/timeout

### Fonctions
- [ ] Agrégations (COUNT, SUM, AVG, etc.)
- [ ] String fonctions (SUBSTR, REPLACE, etc.)
- [ ] Math fonctions (ROUND, ABS, etc.)
- [ ] Date/heure fonctions
- [ ] Conditionnelles (CASE, COALESCE)

### Configuration
- [ ] PRAGMA foreign_keys ON
- [ ] PRAGMA journal_mode WAL
- [ ] PRAGMA synchronous optimisé
- [ ] PRAGMA cache_size configuré
- [ ] ANALYZE exécuté régulièrement

### Sécurité
- [ ] SQL injection prévenue (parameterized queries)
- [ ] Transactions utilisées modifications multiples
- [ ] Backup stratégie définie
- [ ] Gestion erreurs robuste

### Production
- [ ] WAL mode production
- [ ] Backup automatiques quotidiens
- [ ] Monitoring performance queries
- [ ] Connection pool si multi-thread
- [ ] VACUUM maintenance mensuelle

---

## Ressources Officielles

**Documentation :**
- Site officiel : https://www.sqlite.org/
- Documentation complète : https://www.sqlite.org/docs.html
- FAQ : https://www.sqlite.org/faq.html
- Optimisation : https://www.sqlite.org/optoverview.html

**Téléchargements :**
- Binaires SQLite : https://www.sqlite.org/download.html
- Source code : https://www.sqlite.org/src/doc/trunk/README.md

**Tutoriels :**
- SQLite Tutorial : https://www.sqlitetutorial.net/
- W3Schools SQLite : https://www.w3schools.com/sql/sql_ref_sqlite.asp

**Livres recommandés :**
- "The Definitive Guide to SQLite" par Grant Allen & Mike Owens
- "Using SQLite" par Jay A. Kreibich

---

## Conclusion

**SQLite = Outil ESSENTIEL développeur moderne**

**Points clés à retenir :**

✅ **Serverless** = Pas de setup, fonctionne immédiatement
✅ **Portable** = 1 fichier `.db`, copier/coller suffit
✅ **Performant** = Millions queries/seconde, faible latence
✅ **Fiable** = ACID complet, tests exhaustifs, stable 20+ ans
✅ **Versatile** = Mobile, desktop, embedded, prototypes, production
✅ **Gratuit** = Public domain, aucune restriction usage

**Utilisation optimale :**

```sql
-- Configuration production recommandée
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;
PRAGMA cache_size = -64000;

-- Toujours utiliser parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

-- Index colonnes fréquentes
CREATE INDEX idx_users_email ON users(email);

-- Transactions modifications multiples
BEGIN TRANSACTION;
-- ... opérations ...
COMMIT;

-- Backup réguliers
sqlite3 myapp.db ".backup myapp_backup.db"

-- Maintenance périodique
ANALYZE;
PRAGMA optimize;
```

**SQLite est parfait pour :**

- 90% applications (mobile, desktop, IoT, prototypes)
- Bases données <100GB avec écritures modérées
- Applications single-user ou faible concurrence écriture
- Stockage local, cache, configuration
- Testing et développement

**Tu maîtrises maintenant SQLite des fondamentaux à la production !** 🚀

---

**Guide SQLite Complet terminé !** 🎉

Ce guide couvre exhaustivement SQLite du niveau débutant au niveau production. Tu as maintenant toutes les connaissances nécessaires pour utiliser SQLite efficacement dans tes projets professionnels !

---

✅ **Guide SQLite complet créé en un seul fichier !**

**Contenu exhaustif :**
- ✅ 12 sections complètes (analogies pédagogiques)
- ✅ Installation et configuration
- ✅ Types de données et conversions
- ✅ Opérations CRUD détaillées
- ✅ Contraintes et intégrité
- ✅ Index et optimisation
- ✅ Jointures (INNER, LEFT, CROSS, SELF)
- ✅ Transactions ACID
- ✅ Fonctions (agrégation, string, math, date/heure)
- ✅ PRAGMA configuration production
- ✅ Best practices (sécurité, backup, monitoring)
- ✅ Cas d'usage pratiques (mobile, cache, analytics, FTS)
- ✅ Code commenté ligne par ligne
- ✅ Exemples progressifs
- ✅ Checklist complète
- ✅ Même rigueur que modules Livewire

**Format Markdown structuré, prêt à être utilisé comme documentation ou cours !** 💪