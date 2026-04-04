---
description: "SQLite — Module 5 : Index (création, stratégie, EXPLAIN QUERY PLAN) et transactions ACID."
icon: lucide/book-open-check
tags: ["SQLITE", "INDEX", "TRANSACTIONS", "ACID", "WAL", "PERFORMANCE"]
---

# Index & Transactions

<div
  class="omny-meta"
  data-level="🟡→🔴 Avancé"
  data-version="3.43+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Index de Livre vs le Virement Bancaire"
    Un index de livre permet de trouver "Bitcoin" à la page 247 sans lire les 800 pages. Un index SQLite fonctionne pareil : une structure B-Tree qui localise une ligne directement sans full scan. Les transactions fonctionnent comme un virement bancaire : débit et crédit réussissent ensemble ou échouent ensemble — jamais un sans l'autre. Ce sont les deux piliers de performance et de fiabilité SQLite.

<br>

---

## 1. Comprendre les Index

```
Sans index (1 000 000 lignes) :
SELECT * FROM users WHERE email = 'alice@example.com';
→ Scan de toutes les lignes (~500ms)

Avec index B-Tree sur email :
SELECT * FROM users WHERE email = 'alice@example.com';
→ Lookup O(log n) sur ~20 niveaux (~1ms)
```

```sql title="SQL — Créer et gérer les index"
-- Index simple sur une colonne fréquemment filtrée
CREATE INDEX idx_users_email ON users(email);

-- Index composite (ordre important : mettre le filtre le plus sélectif en premier)
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at);

-- Index UNIQUE (unicité + performance)
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Index partiel (partial index) — indexe seulement un sous-ensemble
CREATE INDEX idx_active_users ON users(email) WHERE active = 1;

-- Index sur expression (pour les recherches insensibles à la casse)
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Voir les index existants
SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'index';

-- Supprimer un index
DROP INDEX IF EXISTS idx_users_email;
```

_Les clés primaires et contraintes UNIQUE créent automatiquement un index._

<br>

---

## 2. Stratégie d'Indexation

```sql title="SQL — Quand créer (ou non) un index"
-- ✅ Colonnes dans WHERE fréquent
CREATE INDEX idx_posts_status ON posts(status);

-- ✅ Colonnes de JOIN (clés étrangères)
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- ✅ Colonnes dans ORDER BY
CREATE INDEX idx_posts_created ON posts(created_at DESC);

-- ✅ Index composite pour requêtes courantes
CREATE INDEX idx_posts_user_status_date ON posts(user_id, status, created_at);
-- Optimise : WHERE user_id = ? AND status = 'published' ORDER BY created_at DESC

-- ❌ Tables petites (< 1000 lignes) — overhead > bénéfice
-- ❌ Colonnes à faible cardinalité (boolean, gender) — full scan souvent plus rapide
-- ❌ Colonnes rarement utilisées en WHERE — espace disque inutile
```

<br>

---

## 3. EXPLAIN QUERY PLAN

```sql title="SQL — Analyser le plan d'exécution"
-- Sans index → SCAN (mauvais)
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'alice@example.com';
-- Output : SCAN users

-- Après création de l'index → SEARCH (optimal)
CREATE INDEX idx_users_email ON users(email);

EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'alice@example.com';
-- Output : SEARCH users USING INDEX idx_users_email (email=?)
```

| Signal EXPLAIN | Signification | Performance |
|---|---|---|
| `SCAN table` | Full table scan | 🔴 Problème sur grandes tables |
| `SEARCH ... USING INDEX` | Utilise index B-Tree | ✅ Bon |
| `SEARCH ... USING INTEGER PRIMARY KEY` | Lookup via rowid | ✅ Très bon |
| `USE TEMP B-TREE FOR ORDER BY` | Tri en mémoire | ⚠️ À optimiser |

<br>

---

## 4. Transactions ACID

```
A — Atomicity : tout réussit OU tout échoue
C — Consistency : contraintes respectées après transaction
I — Isolation : transactions concurrentes s'exécutent isolément
D — Durability : données persistantes après commit (même crash)
```

```sql title="SQL — BEGIN, COMMIT, ROLLBACK"
-- Transaction explicite
BEGIN TRANSACTION;

    UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Débiter
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Créditer

COMMIT;   -- Les deux opérations sont validées ensemble

-- ROLLBACK si problème
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    -- Vérification : solde devenu négatif ?
ROLLBACK;  -- Annule tout, état initial restauré
```

```python title="Python — Context manager pour les transactions"
import sqlite3

def transfer_funds(conn: sqlite3.Connection, from_id: int, to_id: int, amount: float) -> bool:
    """Transfert atomique : commit si OK, rollback si exception."""
    try:
        with conn:  # Context manager Python pour SQLite
            cursor = conn.cursor()

            row = cursor.execute(
                'SELECT balance FROM accounts WHERE id = ?', (from_id,)
            ).fetchone()

            if row is None or row[0] < amount:
                raise ValueError(f"Solde insuffisant ou compte inexistant")

            cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_id))
            cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_id))

        return True   # COMMIT automatique à la sortie du with

    except (ValueError, sqlite3.Error) as e:
        print(f"Erreur : {e}")
        return False  # ROLLBACK automatique
```

_`with conn:` gère automatiquement le `BEGIN`/`COMMIT`/`ROLLBACK` — c'est le pattern recommandé en Python._

<br>

---

## 5. Performance — Insertion en Lot

```sql title="SQL — 1000 inserts : autocommit vs transaction unique"
-- ❌ Lent : 1000 transactions automatiques (~5 secondes)
INSERT INTO logs VALUES (1, 'Log 1');
INSERT INTO logs VALUES (2, 'Log 2');
-- × 1000 = 1000 BEGIN + COMMIT

-- ✅ Rapide : 1 transaction pour 1000 inserts (~50ms = 100x plus rapide)
BEGIN TRANSACTION;
    INSERT INTO logs VALUES (1, 'Log 1');
    INSERT INTO logs VALUES (2, 'Log 2');
    -- × 1000
COMMIT;
```

<br>

---

## 6. WAL Mode

```sql title="SQL — Activer WAL pour la concurrence en lecture"
-- Mode par défaut : DELETE (lecteurs bloqués pendant l'écriture)
-- Mode WAL : lecteurs non bloqués pendant l'écriture
PRAGMA journal_mode = WAL;
-- → Retourne 'wal' pour confirmer

-- Vérifier le mode actuel
PRAGMA journal_mode;

-- Recommandé pour Laravel : meilleure concurrence SELECT/INSERT simultanés
```

| Mode | Lecteurs | Écrivains | Recommandé pour |
|---|---|---|---|
| DELETE (défaut) | Bloqués lors des écritures | 1 à la fois | Usage simple, CLI |
| WAL | Non bloqués | 1 à la fois | Laravel, APIs, concurrence |

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Audit de performance**

```sql title="SQL — Exercice 1 : identifier les scans et créer les bons index"
-- Table orders (id, user_id, status, amount, created_at) — 100 000 lignes
-- 1. EXPLAIN QUERY PLAN sur ces requêtes :
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'pending';
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42 ORDER BY created_at DESC;
-- 2. Créer les index appropriés
-- 3. Vérifier que SCAN est remplacé par SEARCH USING INDEX
```

**Exercice 2 — Transaction critique**

```python title="Python — Exercice 2 : processus de commande atomique"
# process_order(conn, user_id, product_id, quantity) doit :
# 1. Vérifier que le stock >= quantity (ValueError si insuffisant)
# 2. Décrémenter le stock : UPDATE products SET stock = stock - quantity
# 3. Créer la commande : INSERT INTO orders ...
# 4. Logger l'opération : INSERT INTO order_logs ...
# Rollback automatique si n'importe quelle étape échoue.
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les **index** transforment O(n) en O(log n) — indispensables sur les colonnes de `WHERE`, `JOIN`, `ORDER BY`. `EXPLAIN QUERY PLAN` révèle si SQLite utilise vos index : `SCAN` = problème, `SEARCH USING INDEX` = optimal. Les **transactions ACID** garantissent l'atomicité — critiques pour toute opération multi-tables. Une transaction unique pour 1000 insertions est 100x plus rapide que 1000 autocommits. Le **mode WAL** est recommandé pour Laravel : les lecteurs ne bloquent pas les écrivains.

> Dans le dernier module, nous intégrons SQLite dans **PHP et Laravel** — PDO, configuration, migrations, tests in-memory et checklist production.

<br>
