---
description: "PostgreSQL — SGBDR avancé : types riches, JSONB, Full-Text Search, partitionnement, index spécialisés et intégration Laravel."
icon: lucide/database
tags: ["POSTGRESQL", "DATABASE", "SQL", "JSONB", "LARAVEL"]
---

# PostgreSQL

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire à 🔴 Avancé"
  data-version="16.x"
  data-time="20-25 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothèque Académique"
    Si MySQL est la bibliothèque municipale standard, PostgreSQL est la médiathèque universitaire : beaucoup plus de types de ressources (cartes, partitions musicales, données géospatiales, JSON natif), des règles d'accès très granulaires, et des capacités d'analyse que les bibliothèques ordinaires ne proposent pas. Plus exigeant à prendre en main, mais infiniment plus puissant pour les applications complexes.

**PostgreSQL** (surnommé **Postgres**) est le SGBDR open-source le plus avancé. Il se distingue par ses types de données riches, son JSON natif performant (JSONB), sa conformité stricte aux standards SQL, et sa fiabilité légendaire. C'est le choix de référence pour les applications critiques, les APIs modernes et les projets nécessitant des capacités analytiques.

> PostgreSQL est utilisé par Instagram, GitHub, Shopify, Heroku, et est le moteur recommandé par l'équipe Laravel pour les applications en production.

<br>

---

## 1. Installation & Configuration

```bash title="Bash — Installer PostgreSQL"
# ─── Ubuntu / Debian ──────────────────────────────────────────────────────────
sudo apt update
sudo apt install postgresql postgresql-contrib

# Démarrer le service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# ─── macOS (Homebrew) ─────────────────────────────────────────────────────────
brew install postgresql@16
brew services start postgresql@16

# ─── Docker (développement) ───────────────────────────────────────────────────
docker run -d \
  --name postgres-dev \
  -e POSTGRES_USER=laravel \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  postgres:16-alpine
```

```sql title="SQL — Connexion et setup initial PostgreSQL"
-- Connexion CLI : psql -U postgres
-- ou : psql -U laravel -d myapp -h 127.0.0.1

-- Créer une base
CREATE DATABASE myapp
    WITH ENCODING 'UTF8'
    LC_COLLATE 'fr_FR.UTF-8'
    LC_CTYPE   'fr_FR.UTF-8';

-- Créer un utilisateur
CREATE USER laravel WITH PASSWORD 'secret_password';

-- Donner les droits
GRANT ALL PRIVILEGES ON DATABASE myapp TO laravel;

-- Depuis PostgreSQL 15 : droits sur le schéma public aussi
\c myapp
GRANT ALL ON SCHEMA public TO laravel;

-- Commandes psql utiles
\l          -- Lister les bases
\c myapp    -- Se connecter à myapp
\dt         -- Lister les tables
\d users    -- Décrire la table users
\di         -- Lister les index
\timing on  -- Afficher le temps d'exécution
\q          -- Quitter
```

<br>

---

## 2. Types de Données Riches

PostgreSQL dispose de types que MySQL n'offre pas nativement :

```sql title="SQL — Types PostgreSQL avancés"
CREATE TABLE articles (
    -- ─── Identifiants ─────────────────────────────────────────────────────────
    id         BIGSERIAL PRIMARY KEY,           -- Auto-increment 64 bits
    -- Ou avec UUID :
    uuid       UUID DEFAULT gen_random_uuid(),  -- UUID v4 natif

    -- ─── Texte ────────────────────────────────────────────────────────────────
    title      VARCHAR(500) NOT NULL,
    content    TEXT,
    slug       VARCHAR(255) UNIQUE NOT NULL,

    -- ─── Nombres ──────────────────────────────────────────────────────────────
    price      NUMERIC(10, 2),         -- Précision exacte (≠ REAL/FLOAT)
    rating     REAL,                   -- Flottant simple précision

    -- ─── Booléen natif ────────────────────────────────────────────────────────
    published  BOOLEAN NOT NULL DEFAULT FALSE,

    -- ─── Dates & Fuseaux horaires ─────────────────────────────────────────────
    published_at  TIMESTAMPTZ,         -- Timestamp AVEC fuseau (RECOMMANDÉ)
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_date    DATE,
    duration      INTERVAL,            -- '2 hours 30 minutes', '1 day'

    -- ─── JSON & JSONB ─────────────────────────────────────────────────────────
    metadata   JSONB,                  -- JSON binaire : indexable et queryable
    raw_json   JSON,                   -- JSON texte : ordre préservé

    -- ─── Tableaux natifs ──────────────────────────────────────────────────────
    tags       TEXT[],                 -- Tableau de textes
    scores     INTEGER[],              -- Tableau d'entiers

    -- ─── Énumération typée ────────────────────────────────────────────────────
    status     VARCHAR(20) CHECK (status IN ('draft', 'published', 'archived'))
                           DEFAULT 'draft',

    -- ─── Données géospatiales (extension PostGIS) ──────────────────────────────
    -- location   GEOGRAPHY(POINT, 4326),

    -- ─── Full-Text Search ─────────────────────────────────────────────────────
    search_vector TSVECTOR             -- Vecteur de recherche plein texte
);
```

<br>

---

## 3. JSONB — JSON Performant et Indexable

```sql title="SQL — JSONB : requêtes, opérateurs et index"
-- ─── Créer les données ────────────────────────────────────────────────────────
CREATE TABLE users (
    id       BIGSERIAL PRIMARY KEY,
    name     TEXT NOT NULL,
    settings JSONB DEFAULT '{}'::jsonb
);

INSERT INTO users (name, settings) VALUES
    ('Alice', '{"theme": "dark", "lang": "fr", "notifications": {"email": true, "sms": false}}'),
    ('Bob',   '{"theme": "light", "lang": "en", "notifications": {"email": false, "sms": true}}');

-- ─── Opérateurs JSONB ─────────────────────────────────────────────────────────
-- Accéder à une clé (retourne JSONB)
SELECT settings -> 'theme' FROM users;             -- "dark", "light"

-- Accéder à une clé (retourne TEXT)
SELECT settings ->> 'theme' FROM users;            -- dark, light

-- Accéder en profondeur
SELECT settings -> 'notifications' ->> 'email' FROM users;

-- Filtrer par valeur JSONB
SELECT name FROM users
WHERE settings ->> 'theme' = 'dark';

WHERE settings @> '{"notifications": {"email": true}}'::jsonb;  -- Containment

-- ─── Modifier JSONB ───────────────────────────────────────────────────────────
-- Mettre à jour une clé
UPDATE users
SET settings = settings || '{"theme": "auto"}'::jsonb
WHERE id = 1;

-- Supprimer une clé
UPDATE users
SET settings = settings - 'theme'
WHERE id = 1;

-- Mettre à jour une clé imbriquée
UPDATE users
SET settings = jsonb_set(settings, '{notifications, email}', 'false'::jsonb)
WHERE id = 2;

-- ─── Index GIN sur JSONB (recherche ultra-rapide) ─────────────────────────────
CREATE INDEX idx_users_settings ON users USING GIN (settings);

-- Après cet index, les requêtes @> (containment) sont accélérées :
EXPLAIN ANALYZE
SELECT * FROM users WHERE settings @> '{"theme": "dark"}'::jsonb;
-- Output : Bitmap Index Scan on idx_users_settings (rapide)
```

<br>

---

## 4. Full-Text Search

```sql title="SQL — Recherche plein texte PostgreSQL"
-- ─── Créer un index de recherche ──────────────────────────────────────────────
ALTER TABLE articles
    ADD COLUMN search_vector TSVECTOR
    GENERATED ALWAYS AS (
        setweight(to_tsvector('french', COALESCE(title, '')), 'A')   -- Titre = poids A
        || setweight(to_tsvector('french', COALESCE(content, '')), 'B') -- Corps = poids B
    ) STORED;

CREATE INDEX idx_articles_fts ON articles USING GIN (search_vector);

-- ─── Rechercher ───────────────────────────────────────────────────────────────
SELECT title,
       ts_rank(search_vector, query) AS relevance
FROM articles,
     to_tsquery('french', 'laravel & eloquent') AS query
WHERE search_vector @@ query
ORDER BY relevance DESC
LIMIT 10;

-- ─── Avec surbrillance des termes trouvés ─────────────────────────────────────
SELECT
    title,
    ts_headline('french', content,
                to_tsquery('french', 'laravel'),
                'MaxWords=50, MinWords=20, StartSel=<mark>, StopSel=</mark>') AS excerpt
FROM articles
WHERE search_vector @@ to_tsquery('french', 'laravel');
```

<br>

---

## 5. Index Spécialisés

```sql title="SQL — Types d'index PostgreSQL"
-- ─── B-Tree (défaut) — pour les égalités et les intervalles ──────────────────
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_date ON orders(created_at DESC);

-- ─── GIN — pour les tableaux, JSONB, Full-Text Search ─────────────────────────
CREATE INDEX idx_tags    ON articles USING GIN (tags);       -- Tableau
CREATE INDEX idx_meta    ON articles USING GIN (metadata);   -- JSONB
CREATE INDEX idx_fts     ON articles USING GIN (search_vector); -- FTS

-- ─── GiST — pour la géospatialité et les intervalles ─────────────────────────
-- CREATE INDEX idx_location ON places USING GIST (location);  -- PostGIS

-- ─── Index partiel (uniquement une partie des lignes) ─────────────────────────
CREATE INDEX idx_published_posts ON articles(created_at)
WHERE published = TRUE;          -- Seulement les articles publiés

-- ─── Index sur expression ─────────────────────────────────────────────────────
CREATE INDEX idx_lower_email ON users(LOWER(email));
-- Accélère : WHERE LOWER(email) = LOWER('Alice@Example.Com')

-- ─── Index composite ──────────────────────────────────────────────────────────
CREATE INDEX idx_user_status_date ON orders(user_id, status, created_at DESC);
-- Optimise : WHERE user_id = ? AND status = 'pending' ORDER BY created_at DESC

-- ─── Analyser l'utilisation des index ─────────────────────────────────────────
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
-- idx_scan = 0 → index jamais utilisé → candidat à la suppression
```

<br>

---

## 6. Configuration Laravel

```bash title="Bash — .env Laravel pour PostgreSQL"
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=myapp
DB_USERNAME=laravel
DB_PASSWORD=secret_password
DB_SEARCH_PATH=public     # Schéma PostgreSQL
```

```php title="PHP — Migration Laravel : types PostgreSQL spécifiques"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('articles', function (Blueprint $table) {
            $table->id();                           // BIGSERIAL PRIMARY KEY
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('content')->nullable();
            $table->string('slug')->unique();
            $table->jsonb('metadata')->nullable();  // JSONB natif
            $table->boolean('published')->default(false);
            $table->timestampsTz();                // TIMESTAMPTZ (avec fuseau)
            $table->softDeletesTz();

            $table->index(['user_id', 'published', 'created_at']);
        });

        // Ajouter la colonne TSVECTOR et son index GIN
        DB::statement("
            ALTER TABLE articles
            ADD COLUMN search_vector TSVECTOR
            GENERATED ALWAYS AS (
                setweight(to_tsvector('french', COALESCE(title, '')), 'A')
                || setweight(to_tsvector('french', COALESCE(content, '')), 'B')
            ) STORED
        ");

        DB::statement('CREATE INDEX idx_articles_fts ON articles USING GIN (search_vector)');
    }

    public function down(): void
    {
        Schema::dropIfExists('articles');
    }
};
```

```php title="PHP — Eloquent : requêtes PostgreSQL avancées"
<?php

use Illuminate\Support\Facades\DB;
use App\Models\Article;

// ─── Recherche Full-Text ──────────────────────────────────────────────────────
$results = Article::whereRaw(
    "search_vector @@ to_tsquery('french', ?)",
    ['laravel & eloquent']
)->orderByRaw(
    "ts_rank(search_vector, to_tsquery('french', ?)) DESC",
    ['laravel & eloquent']
)->get();

// ─── Requête JSONB ────────────────────────────────────────────────────────────
$darkThemeUsers = DB::table('users')
    ->whereRaw("settings @> ?::jsonb", ['{"theme": "dark"}'])
    ->get();

// ─── Arrays PostgreSQL via Laravel ────────────────────────────────────────────
// Avec le package Laravel PostgreSQL : arunazthor/postgresql-for-laravel ou
// directement via whereRaw :
$articles = Article::whereRaw("? = ANY(tags)", ['PHP'])->get();
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — JSONB en pratique**

```sql title="SQL — Exercice 1 : explorer JSONB avec des données réelles"
-- Créez une table products avec un champ JSONB 'specs'
-- Insérez 5 produits avec des specs différentes (CPU, RAM, stockage...)
-- Requêtes :
-- 1. Tous les produits avec RAM >= 16 (specs ->> 'ram')
-- 2. Produits contenant le tag 'gaming' dans un tableau JSONB
-- 3. Mettre à jour dynamiquement une clé imbriquée avec jsonb_set()
-- 4. Créer un index GIN et vérifier avec EXPLAIN ANALYZE
```

**Exercice 2 — Full-Text Search**

```sql title="SQL — Exercice 2 : moteur de recherche sur articles"
-- Sur la table articles (title, content, search_vector) :
-- 1. Créer un index TSVECTOR STORED (généré automatiquement)
-- 2. Rechercher 'laravel AND (eloquent OR query)'
-- 3. Afficher un extrait avec ts_headline (surbrillance)
-- 4. Classer par pertinence (ts_rank)
-- 5. Comparer les temps avec EXPLAIN ANALYZE : avec/sans index GIN
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    PostgreSQL se distingue par **JSONB** (JSON binaire indexable, bien supérieur au JSON MySQL), le **Full-Text Search** natif avec pondération et surbrillance, les **types riches** (UUID, TIMESTAMPTZ, tableaux, intervalles), et les **index spécialisés** (GIN, GiST). `TIMESTAMPTZ` est toujours préféré à `TIMESTAMP` pour gérer correctement les fuseaux horaires. Les **CTE récursives** et les **window functions** sont conformes au standard SQL. Laravel supporte PostgreSQL nativement — changez `DB_CONNECTION=pgsql`, vos migrations fonctionnent sans modification pour les types standard.

> Pour les données non structurées ou à très haute scalabilité horizontale, explorez [NoSQL →](./nosql.md).

<br>