---
description: "SQLite — Module 1 : Architecture serverless, cas d'usage, installation CLI sur Windows/macOS/Linux, premiers pas shell interactif."
icon: lucide/book-open-check
tags: ["SQLITE", "INSTALLATION", "SERVERLESS", "CLI"]
---

# Introduction & Installation

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="3.43+"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothèque Personnelle vs la Bibliothèque Municipale"
    MySQL et PostgreSQL sont des bibliothèques municipales : bâtiment dédié, personnel, horaires d'ouverture, système de réservation complexe. SQLite, c'est votre classeur personnel — un seul fichier `.db` que vous emportez partout. Vous l'ouvrez directement depuis votre application, sans serveur intermédiaire, sans installation d'administrateur, sans port réseau. C'est pourquoi SQLite est le moteur de base de données le plus déployé au monde : milliards de smartphones (iOS/Android), navigateurs (Chrome, Firefox stockent leur historique), applications desktop (Skype, Photoshop), systèmes IoT.

Ce module couvre l'architecture SQLite, les cas d'usage, l'installation et votre première session shell.

<br>

---

## 1. Qu'est-ce que SQLite ?

**SQLite = Moteur SQL embarqué, serverless, zero-configuration**

```
Architecture Traditionnelle (MySQL/PostgreSQL) :
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│ Application │ ←─TCP──→ │ Serveur DB   │ ←────→ │ Fichiers DB  │
│  (PHP/Laravel) │      │ (mysqld)     │         │ (.frm, .ibd) │
└─────────────┘         └──────────────┘         └──────────────┘
  Client                  Serveur                  Stockage

Architecture SQLite :
┌─────────────────────────────┐         ┌──────────────┐
│ Application + Bibliothèque  │ ←────→ │ Fichier DB   │
│   SQLite intégrée           │         │ (app.db)     │
└─────────────────────────────┘         └──────────────┘
  Tout dans le process                    Stockage direct
```

_Avec SQLite, il n'y a pas de serveur à démarrer, pas de daemon à administrer. La bibliothèque SQLite est liée directement à votre application — elle lit et écrit dans le fichier `.db` via le système de fichiers._

| Critère | SQLite | MySQL / PostgreSQL |
|---|---|---|
| **Architecture** | Bibliothèque intégrée | Serveur client-serveur |
| **Configuration** | Aucune (zero-config) | Fichiers config, users, permissions |
| **Fichiers** | 1 fichier `.db` | Multiples fichiers, logs, config |
| **Réseau** | Accès local uniquement | TCP/IP, remote connections |
| **Concurrence** | Lecture multiple, écriture unique | Lecture/écriture simultanées |
| **Utilisateurs** | Aucun (filesystem permissions) | Users, roles, grants SQL |
| **Taille max** | 281 TB théorique, ~1 TB pratique | Quasi-illimitée |
| **Use case idéal** | Mobile, desktop, IoT, tests, prototypes | Web apps multi-users, haute concurrence |

<br>

---

## 2. Quand Utiliser SQLite ?

!!! note "Utilisez SQLite pour..."
    - Applications mobiles (iOS, Android)
    - Applications desktop (Electron, Qt)
    - Prototypes et POCs (Proof of Concept)
    - Systèmes embarqués et IoT
    - Applications single-user
    - **Tests unitaires avec base in-memory** ← usage Laravel très courant
    - Cache local de données
    - Analyse de données locale (data science)
    - Configuration application

!!! warning "N'utilisez PAS SQLite pour..."
    - Applications web à haute concurrence (> 100 req écriture/seconde)
    - Bases de données très volumineuses (> 100 Go avec écritures fréquentes)
    - Applications nécessitant accès réseau distant
    - Systèmes distribués multi-serveurs
    - Applications nécessitant permissions granulaires par utilisateur

<br>

---

## 3. Installation

### Vérifier si SQLite est déjà installé

```bash title="Bash — Vérifier l'installation SQLite"
# SQLite est préinstallé sur macOS et la plupart des distributions Linux
sqlite3 --version
# → 3.43.2 2023-10-10 13:08:14 (exemple)
```

### Installation par OS

```bash title="Bash — Installation SQLite selon l'OS"
# ─── Ubuntu / Debian ──────────────────────────────────────────────────────────
sudo apt update && sudo apt install sqlite3

# ─── macOS (Homebrew) ─────────────────────────────────────────────────────────
brew install sqlite3

# ─── Windows ──────────────────────────────────────────────────────────────────
# 1. Télécharger depuis https://www.sqlite.org/download.html
# 2. Télécharger "sqlite-tools-win32-x86-*.zip"
# 3. Extraire sqlite3.exe dans un répertoire dans votre PATH
# 4. Vérifier : sqlite3 --version
```

### SQLite dans les langages de programmation

```php title="PHP — Extension PDO SQLite (incluse dans PHP)"
<?php
// Vérifier que l'extension PDO SQLite est activée
var_dump(extension_loaded('pdo_sqlite')); // bool(true)
var_dump(extension_loaded('sqlite3'));    // bool(true)

// php.ini : décommenter si nécessaire
// extension=pdo_sqlite
// extension=sqlite3
```

```python title="Python — sqlite3 (module standard)"
import sqlite3

# Module intégré à Python, aucune installation nécessaire
print(sqlite3.version)         # 2.6.0 (version du module Python)
print(sqlite3.sqlite_version)  # 3.43.2 (version SQLite sous-jacente)
```

```bash title="Bash — Node.js (better-sqlite3)"
# Node.js nécessite une librairie externe
npm install better-sqlite3
# Synchrone et performant — recommandé sur sqlite3 (async)
```

<br>

---

## 4. Premiers Pas — CLI SQLite

Le shell SQLite interactif (`sqlite3`) est l'outil de développement principal.

```bash title="Bash — Ouvrir et créer une base de données"
# Créer ou ouvrir une base de données (fichier créé si absent)
sqlite3 myapp.db

# Base en mémoire (temporaire, parfaite pour les tests)
sqlite3 :memory:

# Shell interactif ouvert :
# SQLite version 3.43.2
# sqlite>
```

### Commandes Shell (métacommandes)

```sql title="SQLite Shell — Métacommandes essentielles (prefixées par .)"
-- Afficher toutes les tables
.tables

-- Afficher le schéma d'une table
.schema users

-- Afficher tous les schémas
.schema

-- Mode d'affichage (par défaut : list)
.mode column   -- Colonnes alignées
.mode table    -- Format tableau
.mode csv      -- Format CSV
.mode json     -- Format JSON

-- Activer les en-têtes de colonnes
.headers on

-- Importer un CSV
.mode csv
.import data.csv users

-- Exporter une table en CSV
.mode csv
.headers on
.output users.csv
SELECT * FROM users;
.output stdout

-- Afficher le temps d'exécution des requêtes
.timer on

-- Afficher les informations de la base
.databases

-- Exécuter un fichier SQL externe
.read script.sql

-- Quitter le shell
.exit
```

### Session Complète — Exemple

```bash title="Bash — Session SQLite complète : création, insertion, requête"
$ sqlite3 myapp.db
SQLite version 3.43.2
sqlite> .mode column
sqlite> .headers on

sqlite> CREATE TABLE users (
   ...>     id INTEGER PRIMARY KEY AUTOINCREMENT,
   ...>     name TEXT NOT NULL,
   ...>     email TEXT UNIQUE NOT NULL
   ...> );

sqlite> INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
sqlite> INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');

sqlite> SELECT * FROM users;
id  name   email
--  -----  -----------------
1   Alice  alice@example.com
2   Bob    bob@example.com

sqlite> .schema users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

sqlite> .exit
```

<br>

---

## 5. Structure d'une Base SQLite

```sql title="SQL — Structure typique d'une base SQLite"
-- Un fichier .db contient des tables
-- myapp.db
-- ├── Table: users         → id, name, email, created_at
-- ├── Table: posts         → id, user_id, title, content
-- └── Table: comments      → id, post_id, user_id, content

-- Exemple de structure relationnelle complète
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    published INTEGER DEFAULT 0,  -- Booléen : 0/1
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

_Cette structure à 3 tables est suffisante pour un blog complet. SQLite gère les relations via les clés étrangères (à activer avec `PRAGMA foreign_keys = ON`)._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Installation et première base**

```bash title="Bash — Exercice 1 : créer votre première base SQLite"
# 1. Ouvrir SQLite
sqlite3 blog.db

# 2. Créer la table users (id, name, email, created_at)
# 3. Insérer 3 utilisateurs
# 4. Afficher tous les utilisateurs avec .headers on et .mode column
# 5. Vérifier le schéma avec .schema
# 6. Exporter en CSV avec .output et SELECT
# 7. Quitter avec .exit
```

**Exercice 2 — Comparaison architectures**

Listez 3 applications installées sur votre ordinateur ou smartphone qui utilisent SQLite (navigateurs, apps mobiles, apps desktop). Cherchez des fichiers `.db` dans les répertoires de données utilisateur de ces applications.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    SQLite est une **bibliothèque SQL intégrée** — pas un serveur. Un fichier `.db` contient toute la base de données. Zéro configuration, zéro administration. Le shell `sqlite3` permet de créer des tables, exécuter des requêtes et exporter des données directement depuis le terminal. SQLite est le choix naturel pour les tests Laravel (base in-memory), les prototypes, les applications mobile/desktop, et tout environnement où un serveur de base de données est impossible ou superflu.

> Dans le module suivant, nous découvrons le **système de types SQLite** — storage classes, type affinity, DDL (CREATE, ALTER, DROP) et gestion des dates.

<br>
