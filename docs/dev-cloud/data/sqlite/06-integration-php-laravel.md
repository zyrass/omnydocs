---
description: "SQLite — Module 6 : Intégration PHP (PDO) et Laravel — configuration, migrations, tests in-memory, bonnes pratiques de production."
icon: lucide/book-open-check
tags: ["SQLITE", "PHP", "PDO", "LARAVEL", "TESTS", "PRODUCTION"]
---

# Intégration PHP & Laravel

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="3.43+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Module Enfichable"
    Un appareil photo numérique accepte différents types de cartes mémoire via le même connecteur standard. PDO est ce connecteur standard pour PHP : peu importe si votre base de données est SQLite, MySQL ou PostgreSQL, l'API est identique. Pour Laravel, SQLite est la carte mémoire de test par excellence — rapide, jetable, sans serveur à démarrer. Chaque test repart d'une base vierge en mémoire, sans état persistant.

<br>

---

## 1. PDO SQLite en PHP

```php title="PHP — Connexion PDO SQLite : fichier et mémoire"
<?php

// ─── Connexion à un fichier .db ───────────────────────────────────────────────
$pdo = new PDO('sqlite:/path/to/database/app.db');

// Options recommandées pour la production
$pdo = new PDO(
    dsn: 'sqlite:/path/to/database/app.db',
    options: [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,  // Lève des exceptions
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,        // Tableaux associatifs
        PDO::ATTR_EMULATE_PREPARES   => false,                   // Requêtes préparées natives
    ]
);

// ─── Connexion en mémoire (tests) ─────────────────────────────────────────────
$pdo = new PDO('sqlite::memory:');  // Base temporaire en RAM, vidée à la fin du script
```

```php title="PHP — CRUD avec PDO SQLite"
<?php

$pdo = new PDO('sqlite:app.db', options: [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);

// Activer les clés étrangères (obligatoire à chaque connexion)
$pdo->exec('PRAGMA foreign_keys = ON');
$pdo->exec('PRAGMA journal_mode = WAL');

// ─── CREATE TABLE ─────────────────────────────────────────────────────────────
$pdo->exec('
    CREATE TABLE IF NOT EXISTS users (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        email      TEXT UNIQUE NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
');

// ─── INSERT avec requête préparée (protection injection SQL) ──────────────────
$stmt = $pdo->prepare('INSERT INTO users (name, email) VALUES (:name, :email)');
$stmt->execute([':name' => 'Alice Dupont', ':email' => 'alice@example.com']);
$newId = (int) $pdo->lastInsertId();

// ─── SELECT ───────────────────────────────────────────────────────────────────
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
$stmt->execute([':id' => $newId]);
$user = $stmt->fetch(); // ['id' => 1, 'name' => 'Alice Dupont', ...]

// SELECT multiples
$stmt = $pdo->query('SELECT * FROM users ORDER BY name');
$users = $stmt->fetchAll(); // Array de tableaux associatifs

// ─── UPDATE ───────────────────────────────────────────────────────────────────
$stmt = $pdo->prepare('UPDATE users SET name = :name WHERE id = :id');
$stmt->execute([':name' => 'Alice Martin', ':id' => 1]);
echo $stmt->rowCount() . ' ligne(s) modifiée(s)';

// ─── DELETE ───────────────────────────────────────────────────────────────────
$stmt = $pdo->prepare('DELETE FROM users WHERE id = :id');
$stmt->execute([':id' => 1]);

// ─── Transaction ──────────────────────────────────────────────────────────────
try {
    $pdo->beginTransaction();

    $pdo->prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?')
        ->execute([100, 1]);
    $pdo->prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?')
        ->execute([100, 2]);

    $pdo->commit();
} catch (PDOException $e) {
    $pdo->rollBack();
    throw $e;
}
```

<br>

---

## 2. SQLite avec Laravel

### Configuration `.env`

```bash title="Bash — .env : configurer SQLite comme base de données Laravel"
# ─── Développement / Tests : SQLite ───────────────────────────────────────────
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database/database.db
# Ou chemin relatif depuis la racine du projet :
# DB_DATABASE=database/database.db

# ─── Alternative : base en mémoire (tests uniquement) ─────────────────────────
# DB_DATABASE=:memory:
```

```php title="PHP — config/database.php : configuration SQLite Laravel"
'connections' => [
    'sqlite' => [
        'driver'                  => 'sqlite',
        'url'                     => env('DATABASE_URL'),
        'database'                => env('DB_DATABASE', database_path('database.sqlite')),
        'prefix'                  => '',
        'foreign_key_constraints' => env('DB_FOREIGN_KEYS', true),
        // foreign_key_constraints active PRAGMA foreign_keys = ON automatiquement
    ],
],
```

### Créer la Base et Migrer

```bash title="Bash — Initialiser SQLite dans Laravel"
# Créer le fichier database.sqlite
touch database/database.sqlite

# Lancer les migrations
php artisan migrate

# Ou tout en un (migrate + seed)
php artisan migrate --seed

# Voir l'état des migrations
php artisan migrate:status
```

### Migrations Standard

```php title="PHP — database/migrations/create_users_table.php : migration SQLite compatible"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();                              // INTEGER PRIMARY KEY AUTOINCREMENT
            $table->foreignId('user_id')              // INTEGER NOT NULL
                  ->constrained()                      // FK → users.id ON DELETE RESTRICT
                  ->cascadeOnDelete();                 // ON DELETE CASCADE

            $table->string('title');                   // TEXT NOT NULL
            $table->text('content')->nullable();       // TEXT NULL
            $table->string('status', 20)
                  ->default('draft');                  // TEXT DEFAULT 'draft'
            $table->boolean('published')->default(false); // INTEGER DEFAULT 0
            $table->unsignedInteger('views')->default(0);

            $table->timestamps();                      // created_at, updated_at TEXT

            // Index
            $table->index(['user_id', 'status']);      // Index composite
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

<br>

---

## 3. Tests Laravel avec SQLite In-Memory

SQLite en mémoire (`:memory:`) est la configuration standard pour les tests Laravel — ultra-rapide car tout est en RAM.

```php title="PHP — phpunit.xml : configurer SQLite in-memory pour les tests"
<?xml version="1.0" encoding="UTF-8"?>
<phpunit>
    <php>
        <env name="APP_ENV"       value="testing"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE"   value=":memory:"/>
        <!-- Chaque test repart d'une base vide et fraîche -->
    </php>
</phpunit>
```

```php title="PHP — Tests Feature Laravel : RefreshDatabase avec SQLite"
<?php

namespace Tests\Feature;

use App\Models\Post;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostTest extends TestCase
{
    use RefreshDatabase;
    // RefreshDatabase recrée toutes les tables avant chaque test
    // Avec SQLite :memory:, c'est instantané (~5ms vs ~500ms avec MySQL)

    public function test_user_can_create_post(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->postJson('/api/posts', [
                'title'   => 'Mon Premier Article',
                'content' => 'Contenu de l\'article.',
                'status'  => 'draft',
            ]);

        $response->assertStatus(201);
        $this->assertDatabaseHas('posts', [
            'title'   => 'Mon Premier Article',
            'user_id' => $user->id,
        ]);
    }

    public function test_published_post_is_visible(): void
    {
        Post::factory()->count(3)->create(['status' => 'published']);
        Post::factory()->count(2)->create(['status' => 'draft']);

        $response = $this->getJson('/api/posts');

        $response->assertStatus(200)
                 ->assertJsonCount(3, 'data');
    }
}
```

```php title="PHP — Tests unitaires avec SQLite in-memory directement"
<?php

namespace Tests\Unit;

use PDO;
use PHPUnit\Framework\TestCase;

class SqliteRepositoryTest extends TestCase
{
    private PDO $pdo;

    protected function setUp(): void
    {
        parent::setUp();

        // Base in-memory fraîche pour chaque test
        $this->pdo = new PDO('sqlite::memory:', options: [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);

        $this->pdo->exec('PRAGMA foreign_keys = ON');

        // Créer le schéma de test
        $this->pdo->exec('
            CREATE TABLE users (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ');
    }

    public function test_can_insert_and_retrieve_user(): void
    {
        $stmt = $this->pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
        $stmt->execute(['Alice', 'alice@example.com']);

        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE email = ?');
        $stmt->execute(['alice@example.com']);
        $user = $stmt->fetch();

        $this->assertEquals('Alice', $user['name']);
        $this->assertEquals('alice@example.com', $user['email']);
    }

    public function test_unique_email_constraint(): void
    {
        $this->expectException(\PDOException::class);

        $stmt = $this->pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
        $stmt->execute(['Alice', 'alice@example.com']);
        $stmt->execute(['Bob',   'alice@example.com']); // Dupliqué → exception
    }
}
```

<br>

---

## 4. Bonnes Pratiques Production

```php title="PHP — Classe SQLiteConnection : wrapper production-ready"
<?php

class SQLiteConnection
{
    private PDO $pdo;

    public function __construct(string $path)
    {
        // Validation du chemin
        if ($path !== ':memory:' && !is_writable(dirname($path))) {
            throw new \RuntimeException("Répertoire non accessible en écriture : " . dirname($path));
        }

        $this->pdo = new PDO("sqlite:$path", options: [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);

        $this->configure();
    }

    private function configure(): void
    {
        // Configuration recommandée pour la production
        $this->pdo->exec('PRAGMA foreign_keys = ON');   // Intégrité référentielle
        $this->pdo->exec('PRAGMA journal_mode = WAL');  // Meilleure concurrence
        $this->pdo->exec('PRAGMA synchronous = NORMAL'); // Balance vitesse/sécurité
        $this->pdo->exec('PRAGMA cache_size = -64000'); // Cache 64 Mo en RAM
        $this->pdo->exec('PRAGMA temp_store = MEMORY'); // Tables temporaires en RAM
        $this->pdo->exec('PRAGMA mmap_size = 268435456'); // Memory-mapped I/O 256 Mo
    }

    public function getPdo(): PDO
    {
        return $this->pdo;
    }
}
```

```php title="PHP — config/database.php : SQLite production avec PRAGMA via hook"
// Laravel 10+ : configurer les PRAGMAs via l'événement de connexion
// Dans AppServiceProvider::boot() :
use Illuminate\Support\Facades\DB;

DB::listen(function ($query) {
    // Monitoring des requêtes lentes en production
});

// Configurer SQLite à chaque connexion
config(['database.connections.sqlite.options' => [
    // SQLite specific pragmas via PDO after connect
]]);

// Alternative : Utiliser l'événement Illuminate\Database\Events\ConnectionEstablished
// dans un ServiceProvider pour exécuter les PRAGMAs immédiatement après connexion
```

<br>

---

## 5. Checklist Production SQLite

```sql title="SQL — Vérifications avant mise en production SQLite"
-- ─── Sécurité ─────────────────────────────────────────────────────────────────
PRAGMA foreign_keys;          -- Doit retourner 1 (activé)
PRAGMA integrity_check;       -- Doit retourner 'ok'
PRAGMA foreign_key_check;     -- Ne doit rien retourner (pas de violations)

-- ─── Performance ──────────────────────────────────────────────────────────────
PRAGMA journal_mode;          -- Recommandé : wal
PRAGMA cache_size;            -- Recommandé : valeur négative (Ko) ex: -64000 = 64 Mo
PRAGMA page_size;             -- Défaut : 4096, OK pour la plupart des cas
PRAGMA optimize;              -- Analyse les statistiques des tables pour l'optimiseur

-- ─── Analyse et nettoyage ─────────────────────────────────────────────────────
ANALYZE;                      -- Met à jour les statistiques pour l'optimiseur de requêtes
VACUUM;                       -- Compacte le fichier .db (récupère l'espace des suppressions)

-- ─── Informations de la base ──────────────────────────────────────────────────
PRAGMA database_list;         -- Liste les bases attachées
SELECT page_count * page_size AS size_bytes FROM pragma_page_count(), pragma_page_size();
-- Taille actuelle du fichier .db
```

**Checklist déploiement :**

| Item | Vérification |
|---|---|
| Répertoire `database/` | Accessible en écriture par le process PHP |
| `foreign_keys = ON` | Configuré à chaque connexion |
| `journal_mode = WAL` | Activé pour la concurrence |
| Backups | Script de sauvegarde quotidien du fichier `.db` |
| Permissions fichier | `chmod 644 database.db` ou `660` selon le setup |
| `.gitignore` | `database/*.sqlite` ajouté |
| Tests | `RefreshDatabase` + SQLite `:memory:` dans phpunit.xml |

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Repository Pattern avec PDO SQLite**

```php title="PHP — Exercice 1 : implémenter un UserRepository"
// Créez une classe UserRepository avec :
// - __construct(PDO $pdo)
// - find(int $id): ?array
// - findByEmail(string $email): ?array
// - findAll(int $limit = 20, int $offset = 0): array
// - create(string $name, string $email): int (retourne l'id)
// - update(int $id, array $data): bool
// - delete(int $id): bool
// Utilisez uniquement des requêtes préparées (protection injection SQL).
```

**Exercice 2 — Suite de tests Feature Laravel**

```php title="PHP — Exercice 2 : tester une API CRUD avec SQLite in-memory"
// Configurez phpunit.xml pour DB_DATABASE=:memory:
// Écrivez des tests Feature pour un PostController avec :
// - test_can_list_published_posts
// - test_authenticated_user_can_create_post
// - test_unauthenticated_user_cannot_create_post
// - test_user_can_only_delete_own_posts
// - test_post_validation_requires_title
// Utilisez RefreshDatabase + User::factory() + actingAs()
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    **PDO SQLite** fournit une interface PHP standard identique à MySQL/PostgreSQL — seul le DSN change (`'sqlite:path.db'`). Les **requêtes préparées** sont obligatoires contre les injections SQL. Dans Laravel, `DB_DATABASE=:memory:` avec `RefreshDatabase` donne des tests ultra-rapides (~5ms par test vs ~500ms avec MySQL). En production, configurer `PRAGMA foreign_keys = ON` et `PRAGMA journal_mode = WAL` à chaque connexion. `VACUUM` et `ANALYZE` sont les outils de maintenance périodique. SQLite est excellent en production pour les applications single-tenant, les outils en ligne de commande, les APIs à faible concurrence, et les applications desktop.

> **Formation SQLite terminée.** Vous maîtrisez maintenant SQLite du shell interactif jusqu'à l'intégration Laravel avec tests in-memory. Pour aller plus loin : [SQL avancé →](../sql.md) ou [PostgreSQL →](../postgresql.md).

<br>
