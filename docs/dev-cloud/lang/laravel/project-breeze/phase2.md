---
description: "Création des migrations (users, categories, posts, comments), relations Eloquent et structure base de données complète."
icon: lucide/database
tags: ["ELOQUENT", "MIGRATIONS", "RELATIONS", "BDD"]
---

# Phase 2 : Base de Données & Modèles Eloquent

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h30-2h">
</div>

## Introduction à la Base de Données et aux Modèles Eloquent

### Vue d'Ensemble de la Phase

> Cette deuxième phase constitue le **cœur technique** de votre blog multi-auteurs. Vous allez concevoir et implémenter la **structure de données complète** qui supportera toutes les fonctionnalités de l'application : utilisateurs, articles, catégories et commentaires. Cette phase se décompose en deux volets complémentaires : les **migrations** (structure des tables SQL) et les **modèles Eloquent** (représentation objet en PHP).

!!! note "Les migrations Laravel sont des **fichiers PHP versionnés** qui décrivent la structure de la base de données de manière programmatique. Contrairement aux scripts SQL bruts, elles permettent de **construire**, **modifier** et **supprimer** des tables de façon reproductible sur n'importe quel environnement (**développement**, **staging**, **production**). Chaque migration contient deux méthodes : **`up()`** pour appliquer les changements et **`down()`** pour les annuler."

!!! note "Les modèles Eloquent, quant à eux, sont des **classes PHP** qui représentent les tables de la base de données. Ils permettent d'interagir avec les données via une syntaxe orientée objet intuitive (**`$post->user->name`**) au lieu de requêtes SQL manuelles. Eloquent gère automatiquement les relations entre tables (**1-N**, **N-N**), **la validation**, **les événements** et bien plus."

!!! quote "À l'issue de cette phase, votre base de données disposera de **4 tables métier** (**`users`, `categories`, `posts`, `comments`**) avec **toutes leurs relations** configurées (**clés étrangères**, **cascade delete**), et vous pourrez manipuler ces données via des modèles Eloquent expressifs et puissants."

!!! danger "**Prérequis pour la Phase 2** : La Phase 1 doit être terminée avec succès : **projet Laravel créé**, **Breeze installé**, et **migrations de base exécutées**. Votre serveur de base de données (**MySQL**/**MariaDB**) doit être démarré."

## Étape 2.1 : Enrichir le Modèle User avec bio et avatar

**Contexte de l'étape :**

> Le modèle `User` généré par Breeze contient les colonnes essentielles pour l'authentification (`name`, `email`, `password`), mais notre blog nécessite des informations supplémentaires pour créer des **profils auteurs riches** : une biographie (`bio`) et un avatar (`avatar`). Plutôt que de créer une nouvelle migration, nous allons modifier la migration existante `create_users_table` avant de relancer toutes les migrations.

Cette approche est valide **uniquement en développement local** : si la migration avait déjà été exécutée en production, vous devriez créer une migration `ALTER TABLE` séparée. En développement, modifier la migration originale puis exécuter `migrate:fresh` est plus propre.

**Localiser et modifier la migration :**

Ouvrir le fichier `database/migrations/2014_10_12_000000_create_users_table.php`

```php title="Fichier : 2014_10_12_000000_create_users_table.php"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table users avec colonnes authentification + profil auteur
     * 
     * Breeze fournit les colonnes de base (name, email, password).
     * On ajoute bio et avatar pour les profils publics d'auteurs.
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            // Clé primaire auto-incrémentée
            $table->id();
            
            // Colonnes authentification (fournies par Breeze)
            $table->string('name');                              // Nom complet de l'utilisateur
            $table->string('email')->unique();                   // Email (connexion + unicité)
            $table->timestamp('email_verified_at')->nullable();  // Date vérification email
            $table->string('password');                          // Mot de passe haché (bcrypt)
            
            // ✅ AJOUT : Colonnes profil auteur
            $table->text('bio')->nullable();      // Biographie auteur (max 65,535 caractères)
                                                   // nullable() = optionnel, peut être NULL
            $table->string('avatar')->nullable(); // URL image avatar (ex: Gravatar, Unsplash)
                                                   // string() = VARCHAR(255) par défaut
            
            // Token "Se souvenir de moi" (Breeze)
            $table->rememberToken();  // VARCHAR(100) pour cookie persistant
            
            // Timestamps automatiques (created_at, updated_at)
            $table->timestamps();     // Gérés automatiquement par Laravel
        });

        // Configuration session (Breeze)
        Schema::create('password_reset_tokens', function (Blueprint $table) {
            $table->string('email')->primary();
            $table->string('token');
            $table->timestamp('created_at')->nullable();
        });

        Schema::create('sessions', function (Blueprint $table) {
            $table->string('id')->primary();
            $table->foreignId('user_id')->nullable()->index();
            $table->string('ip_address', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->longText('payload');
            $table->integer('last_activity')->index();
        });
    }

    /**
     * Supprimer les tables créées
     * 
     * Méthode rollback : permet d'annuler la migration via php artisan migrate:rollback
     */
    public function down(): void
    {
        Schema::dropIfExists('sessions');
        Schema::dropIfExists('password_reset_tokens');
        Schema::dropIfExists('users');
    }
};
```

<small>*La colonne `bio` utilise le type `text` (jusqu'à 65 Ko) car une biographie peut contenir plusieurs paragraphes. La colonne `avatar` stocke une **URL** (pas le fichier binaire) : vous pouvez utiliser des services externes comme Gravatar, Unsplash, ou stocker l'image dans `storage/` et y pointer. Le modificateur `nullable()` signifie que ces champs peuvent rester vides : un utilisateur peut s'inscrire sans remplir sa bio ou choisir d'avatar.*</small>

!!! tip "Pourquoi pas une table `profiles` séparée ?"
    On pourrait créer une table `profiles` (1-1 avec `users`) pour séparer les données d'authentification des données de profil. C'est une bonne pratique pour des profils très volumineux (>10 colonnes), mais ici 2 colonnes supplémentaires ne justifient pas la complexité d'une jointure systématique.

## Étape 2.2 : Créer la Migration de la Table Categories

**Contexte de l'étape :**

Les catégories permettent d'**organiser les articles** par thématique (Technologie, Voyage, Cuisine, etc.). Chaque article appartiendra à exactement **une catégorie** (relation 1-N : une catégorie contient plusieurs articles). Cette table est volontairement simple : seulement un nom et un slug.

Le **slug** est une version URL-friendly du nom de la catégorie (`Technologie` → `technologie`), utilisé pour créer des URLs propres (`/category/technologie` au lieu de `/category/1`). Eloquent générera automatiquement les slugs via un événement `creating` dans le modèle.

**Générer le fichier de migration :**

```bash
# Créer une nouvelle migration pour la table categories
php artisan make:migration create_categories_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_categories_table
```

<small>*Artisan génère automatiquement le nom de classe `CreateCategoriesTable` et crée un fichier horodaté dans `database/migrations/`. Le timestamp garantit l'ordre d'exécution des migrations.*</small>

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_categories_table.php` :

```php title="Fichier : 202X_XX_XX_XXXXXX_create_categories_table.php"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table categories
     * 
     * Structure minimaliste : chaque catégorie a un nom (affiché) 
     * et un slug (utilisé dans les URLs).
     * 
     * Exemple de données :
     * | id | name         | slug         | created_at | updated_at |
     * |----|--------------|--------------|------------|------------|
     * | 1  | Technologie  | technologie  | ...        | ...        |
     * | 2  | Voyage       | voyage       | ...        | ...        |
     */
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            // Clé primaire auto-incrémentée
            $table->id();
            
            // Nom de la catégorie (affiché dans l'interface)
            $table->string('name');  // VARCHAR(255) - Ex: "Technologie"
            
            // Slug URL-friendly (utilisé dans les routes)
            $table->string('slug')   // VARCHAR(255) - Ex: "technologie"
                  ->unique();        // INDEX UNIQUE : empêche doublons
                                     // Évite /category/technologie-1, technologie-2
            
            // Timestamps automatiques
            $table->timestamps();    // created_at, updated_at
        });
    }

    /**
     * Supprimer la table categories
     * 
     * ⚠️ CASCADE : Si on supprime cette table, les posts qui référencent 
     * ces catégories seront automatiquement supprimés (défini dans posts migration).
     */
    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
```

<small>*La contrainte `unique()` sur le slug est **critique** : elle empêche deux catégories d'avoir le même slug, ce qui causerait des conflits de routing (`/category/voyage` ne pourrait pas savoir quelle catégorie afficher). Laravel génère automatiquement un index unique en SQL : `UNIQUE KEY categories_slug_unique (slug)`.*</small>

**Tableau des types de colonnes utilisés :**

| Colonne | Type PHP | Type SQL | Taille Max | Indexation | Contrainte |
|---------|----------|----------|------------|------------|------------|
| `id` | `id()` | `BIGINT UNSIGNED` | 18 446 744 073 709 551 615 | PRIMARY KEY | AUTO_INCREMENT |
| `name` | `string()` | `VARCHAR(255)` | 255 caractères | Aucune | NOT NULL |
| `slug` | `string()` | `VARCHAR(255)` | 255 caractères | UNIQUE INDEX | NOT NULL, UNIQUE |
| `created_at` | `timestamps()` | `TIMESTAMP` | Date/heure | Aucune | NULLABLE |
| `updated_at` | `timestamps()` | `TIMESTAMP` | Date/heure | Aucune | NULLABLE |

## Étape 2.3 : Créer la Migration de la Table Posts

**Contexte de l'étape :**

La table `posts` est le **cœur du blog**. Elle stocke tous les articles avec leur contenu, métadonnées et relations vers `users` (auteur) et `categories`. Cette migration est plus complexe car elle introduit :

1. **Deux clés étrangères** : `user_id` (auteur) et `category_id` (thématique)
2. **Suppression en cascade** : si un user/catégorie est supprimé, ses posts le sont aussi
3. **Un système de statut** : `draft` (brouillon) ou `published` (publié)
4. **Des index de performance** : pour accélérer les requêtes fréquentes

**Générer la migration :**

```bash
# Créer la migration posts
php artisan make:migration create_posts_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_posts_table
```

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_posts_table.php` :

```php title="Fichier : 202X_XX_XX_XXXXXX_create_posts_table.php"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table posts (articles du blog)
     * 
     * Cette table centralise tout le contenu du blog : titre, texte, image,
     * statut publication, compteurs de vues. Elle est reliée aux tables
     * users (auteur) et categories (thématique).
     * 
     * Structure relationnelle :
     * - Chaque post appartient à 1 user (relation N-1)
     * - Chaque post appartient à 1 category (relation N-1)
     * - Chaque post peut avoir N comments (relation 1-N)
     */
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            // Clé primaire
            $table->id();
            
            /*
            |--------------------------------------------------------------------------
            | RELATIONS (Clés étrangères)
            |--------------------------------------------------------------------------
            */
            
            // Relation vers users : qui a écrit cet article ?
            $table->foreignId('user_id')         // BIGINT UNSIGNED (même type que users.id)
                  ->constrained()                // Crée la contrainte FK vers users.id
                  ->onDelete('cascade');         // Si user supprimé → ses posts supprimés
                                                 // SQL: ON DELETE CASCADE
            
            // Relation vers categories : quelle est la thématique ?
            $table->foreignId('category_id')     // BIGINT UNSIGNED (même type que categories.id)
                  ->constrained()                // Crée la contrainte FK vers categories.id
                  ->onDelete('cascade');         // Si catégorie supprimée → posts supprimés
                                                 // SQL: ON DELETE CASCADE
            
            /*
            |--------------------------------------------------------------------------
            | CONTENU DE L'ARTICLE
            |--------------------------------------------------------------------------
            */
            
            // Titre de l'article
            $table->string('title');             // VARCHAR(255) - Ex: "Introduction à Laravel 11"
            
            // Slug URL-friendly (généré auto depuis le titre dans le modèle)
            $table->string('slug')               // VARCHAR(255) - Ex: "introduction-a-laravel-11"
                  ->unique();                    // INDEX UNIQUE - URLs uniques
            
            // Résumé court (affiché dans les listes d'articles)
            $table->text('excerpt');             // TEXT (max 65 Ko) - 2-3 phrases
                                                 // Ex: "Découvrez les nouveautés de Laravel 11..."
            
            // Contenu complet de l'article
            $table->longText('content');         // LONGTEXT (max 4 Go) - Article complet
                                                 // Peut contenir plusieurs milliers de mots
            
            /*
            |--------------------------------------------------------------------------
            | MÉTADONNÉES
            |--------------------------------------------------------------------------
            */
            
            // URL de l'image de couverture (optionnelle)
            $table->string('image')              // VARCHAR(255) - URL vers Unsplash, storage/...
                  ->nullable();                  // Peut être NULL si pas d'image
            
            // Statut de publication
            $table->enum('status', ['draft', 'published'])  // ENUM('draft','published')
                  ->default('draft');                       // Par défaut = brouillon
                                                            // draft = invisible public
                                                            // published = visible public
            
            // Date de publication effective (NULL si brouillon)
            $table->timestamp('published_at')    // TIMESTAMP - Quand l'article a été publié
                  ->nullable();                  // NULL si status = draft
                                                 // Rempli auto quand status passe à published
            
            // Compteur de vues (incrémenté à chaque visite)
            $table->unsignedInteger('views_count')  // INT UNSIGNED (max 4,294,967,295)
                  ->default(0);                     // Démarre à 0
            
            // Timestamps automatiques
            $table->timestamps();                // created_at, updated_at
            
            /*
            |--------------------------------------------------------------------------
            | INDEX DE PERFORMANCE
            |--------------------------------------------------------------------------
            | Ces index accélèrent les requêtes fréquentes. Sans eux, MySQL doit
            | parcourir TOUTE la table (FULL TABLE SCAN = lent sur >10k lignes).
            */
            
            // Index composite : requêtes "posts de cet auteur avec ce statut"
            $table->index(['user_id', 'status']);
            // Exemple SQL rapide : SELECT * FROM posts WHERE user_id=1 AND status='published'
            
            // Index simple : tri par date de publication (page d'accueil)
            $table->index('published_at');
            // Exemple SQL rapide : SELECT * FROM posts WHERE status='published' ORDER BY published_at DESC
        });
    }

    /**
     * Supprimer la table posts
     * 
     * ⚠️ Ordre important : cette table doit être supprimée AVANT users et categories
     * car elle contient des clés étrangères qui les référencent.
     * Laravel gère l'ordre automatiquement grâce aux timestamps des migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

<small>*Le choix de `longText` pour `content` permet de stocker des articles très longs (plusieurs dizaines de milliers de mots). Le type `text` (65 Ko) serait insuffisant pour des tutoriels détaillés. Le compteur `views_count` utilise `unsignedInteger` (jamais négatif) : avec 4 milliards de valeurs possibles, même un article viral ne débordera pas.*</small>

**Pourquoi ces index spécifiques ?**

| Index | Requête Accélérée | Gain de Performance |
|-------|-------------------|---------------------|
| `['user_id', 'status']` | "Afficher les articles publiés de cet auteur" (dashboard) | x10 à x100 sur 10k+ articles |
| `published_at` | "Lister les derniers articles publiés" (page d'accueil) | x5 à x50 avec ORDER BY |

!!! warning "Cascade Delete : Attention aux Suppressions"
    `onDelete('cascade')` signifie que **supprimer un utilisateur supprime automatiquement tous ses articles**. C'est voulu pour maintenir la cohérence des données (pas d'articles orphelins), mais il faut en informer l'utilisateur avant de supprimer son compte. Alternative : `onDelete('set null')` pour conserver les articles en les marquant "Auteur supprimé".

## Étape 2.4 : Créer la Migration de la Table Comments

**Contexte de l'étape :**

> La table `comments` gère les **commentaires publics** sur les articles. Particularité : les commentaires peuvent être laissés par des **visiteurs non inscrits** (pas de relation vers `users`), d'où les colonnes `author_name` et `author_email` au lieu d'une clé étrangère `user_id`.

!!! quote "Le système de **modération** (`approved`) permet aux auteurs d'articles de valider les commentaires avant qu'ils n'apparaissent publiquement, évitant ainsi le spam."

**Générer la migration :**

```bash
# Créer la migration comments
php artisan make:migration create_comments_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_comments_table
```

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_comments_table.php` :

```php title="Fichier : 202X_XX_XX_XXXXXX_create_comments_table.php"
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table comments
     * 
     * Commentaires publics sur les articles du blog. Peuvent être laissés
     * par des visiteurs anonymes (pas besoin de compte). L'auteur de l'article
     * peut modérer (approuver/rejeter) chaque commentaire.
     * 
     * Relation : N comments appartiennent à 1 post (relation N-1)
     * Pas de relation vers users : les commentateurs ne sont pas inscrits
     */
    public function up(): void
    {
        Schema::create('comments', function (Blueprint $table) {
            // Clé primaire
            $table->id();
            
            /*
            |--------------------------------------------------------------------------
            | RELATION vers posts
            |--------------------------------------------------------------------------
            */
            
            // Sur quel article ce commentaire est-il posté ?
            $table->foreignId('post_id')         // BIGINT UNSIGNED (même type que posts.id)
                  ->constrained()                // Crée FK vers posts.id
                  ->onDelete('cascade');         // Si post supprimé → commentaires supprimés
                                                 // Logique : pas de commentaires orphelins
            
            /*
            |--------------------------------------------------------------------------
            | INFORMATIONS DU COMMENTATEUR (visiteur non inscrit)
            |--------------------------------------------------------------------------
            | Pas de user_id : les visiteurs peuvent commenter sans compte.
            | On stocke juste leur nom et email pour affichage et contact éventuel.
            */
            
            // Nom affiché publiquement
            $table->string('author_name');       // VARCHAR(255) - Ex: "Jean Durand"
                                                 // Saisi manuellement par le visiteur
            
            // Email (non affiché, sert pour gravatar ou contact)
            $table->string('author_email');      // VARCHAR(255) - Ex: "jean@example.com"
                                                 // Validé côté formulaire (format email)
            
            // Contenu du commentaire
            $table->text('content');             // TEXT (max 65 Ko) - Quelques paragraphes max
                                                 // Suffisant pour un commentaire classique
            
            /*
            |--------------------------------------------------------------------------
            | SYSTÈME DE MODÉRATION
            |--------------------------------------------------------------------------
            */
            
            // Statut d'approbation par l'auteur de l'article
            $table->boolean('approved')          // TINYINT(1) - 0 = en attente, 1 = approuvé
                  ->default(false);              // Par défaut = NON approuvé
                                                 // L'auteur doit manuellement approuver
            
            // Timestamps automatiques
            $table->timestamps();                // created_at (pour tri chronologique)
                                                 // updated_at (si commentaire édité)
            
            /*
            |--------------------------------------------------------------------------
            | INDEX DE PERFORMANCE
            |--------------------------------------------------------------------------
            */
            
            // Index composite : requête "commentaires approuvés de cet article"
            $table->index(['post_id', 'approved']);
            // Exemple SQL rapide : SELECT * FROM comments WHERE post_id=5 AND approved=1
            // Utilisé sur la page publique de l'article
        });
    }

    /**
     * Supprimer la table comments
     * 
     * Doit être supprimée AVANT posts car elle référence posts.id
     * (l'ordre des migrations garantit cela automatiquement).
     */
    public function down(): void
    {
        Schema::dropIfExists('comments');
    }
};
```

<small>*Le choix de `text` (65 Ko) pour `content` est suffisant : un commentaire de blog dépassant rarement 1000 mots. Le type `boolean` pour `approved` est stocké en SQL comme `TINYINT(1)` (0 ou 1) : plus compact qu'un `VARCHAR` et permet des index optimisés. L'index composite `['post_id', 'approved']` est crucial : sur un article avec 1000 commentaires, récupérer seulement les commentaires approuvés sans index nécessiterait de parcourir les 1000 lignes.*</small>

**Workflow de modération :**

1. **Visiteur poste un commentaire** → `approved = false` (invisible)
2. **Auteur de l'article reçoit une notification** (optionnel, à implémenter)
3. **Auteur modère** :
   - Approuver → `approved = true` (visible publiquement)
   - Rejeter/Supprimer → ligne supprimée de la BDD

!!! tip "Alternative : Modération automatique avec scoring"
    Pour éviter la modération manuelle, vous pourriez implémenter un système de **scoring anti-spam** : analyse des liens suspects, mots-clés spam, patterns (ex: Akismet API). Les commentaires avec score < seuil seraient auto-approuvés, les autres envoyés en modération.

## Étape 2.5 : Exécuter les Migrations

**Contexte de l'étape :**

> À ce stade, vous avez créé **4 fichiers de migration** (users modifié, categories, posts, comments), mais ils ne sont pas encore appliqués à la base de données MySQL. La commande `migrate:fresh` va :  
> 
> 1. **Supprimer toutes les tables existantes** (y compris celles de Breeze)
> 2. **Recréer toutes les tables** dans l'ordre chronologique des migrations
> 3. **Appliquer les contraintes** (clés étrangères, index, valeurs par défaut)

!!! danger "migrate:fresh DÉTRUIT les données"
    **Ne JAMAIS utiliser `migrate:fresh` en production** ! Cette commande supprime toutes les données. En production, utilisez `php artisan migrate` (applique uniquement les nouvelles migrations) ou créez des migrations `ALTER TABLE` pour modifier les tables existantes sans perte de données.

**Exécuter les migrations :**

```bash
# Supprimer toutes les tables et réappliquer toutes les migrations
php artisan migrate:fresh

# Alternative si migrate:fresh échoue (problème de permissions) :
# php artisan db:wipe  # Supprime tout
# php artisan migrate  # Recrée tout
```

**Sortie console attendue :**

```bash
Dropping all tables ...............................................DONE
Migration table created successfully.

Migrating: 2014_10_12_000000_create_users_table
Migrated:  2014_10_12_000000_create_users_table (45.67ms)

Migrating: 2014_10_12_100000_create_password_reset_tokens_table
Migrated:  2014_10_12_100000_create_password_reset_tokens_table (32.14ms)

Migrating: 2019_08_19_000000_create_failed_jobs_table
Migrated:  2019_08_19_000000_create_failed_jobs_table (28.91ms)

Migrating: 2019_12_14_000001_create_personal_access_tokens_table
Migrated:  2019_12_14_000001_create_personal_access_tokens_table (35.42ms)

Migrating: 0001_01_01_000001_create_cache_table
Migrated:  0001_01_01_000001_create_cache_table (22.78ms)

Migrating: 0001_01_01_000002_create_jobs_table
Migrated:  0001_01_01_000002_create_jobs_table (30.56ms)

Migrating: 2024_xx_xx_xxxxxx_create_categories_table
Migrated:  2024_xx_xx_xxxxxx_create_categories_table (18.23ms)

Migrating: 2024_xx_xx_xxxxxx_create_posts_table
Migrated:  2024_xx_xx_xxxxxx_create_posts_table (42.89ms)

Migrating: 2024_xx_xx_xxxxxx_create_comments_table
Migrated:  2024_xx_xx_xxxxxx_create_comments_table (25.34ms)
```

<small>*Chaque ligne `Migrated:` indique qu'une table a été créée avec succès. Le temps d'exécution (en millisecondes) est informatif : si une migration prend >5 secondes, c'est qu'elle contient beaucoup d'index ou de données initiales (seeders). L'ordre d'exécution respecte les timestamps des fichiers de migration (d'où l'importance de ne pas les renommer).*</small>

**Vérifier la structure créée dans MySQL :**

```bash
# Se connecter à MySQL
mysql -u root -p blog_breeze

# Lister toutes les tables
SHOW TABLES;
```

**Résultat attendu :**

```sql
+------------------------+
| Tables_in_blog_breeze  |
+------------------------+
| cache                  |  -- Breeze: cache applicatif
| cache_locks            |  -- Breeze: verrous cache distribué
| categories             |  ✅ Notre table
| comments               |  ✅ Notre table
| failed_jobs            |  -- Breeze: jobs en erreur
| jobs                   |  -- Breeze: file d'attente jobs
| migrations             |  -- Suivi des migrations exécutées
| password_reset_tokens  |  -- Breeze: reset password
| personal_access_tokens |  -- Sanctum API tokens (si utilisé)
| posts                  |  ✅ Notre table
| sessions               |  -- Breeze: sessions utilisateur
| users                  |  ✅ Notre table (enrichie)
+------------------------+
12 rows in set (0.00 sec)
```

**Inspecter la structure détaillée d'une table :**

```sql
-- Voir la structure complète de la table posts
DESCRIBE posts;

-- Résultat attendu :
+---------------+--------------------------------------------+------+-----+---------+----------------+
| Field         | Type                                       | Null | Key | Default | Extra          |
+---------------+--------------------------------------------+------+-----+---------+----------------+
| id            | bigint unsigned                            | NO   | PRI | NULL    | auto_increment |
| user_id       | bigint unsigned                            | NO   | MUL | NULL    |                |
| category_id   | bigint unsigned                            | NO   | MUL | NULL    |                |
| title         | varchar(255)                               | NO   |     | NULL    |                |
| slug          | varchar(255)                               | NO   | UNI | NULL    |                |
| excerpt       | text                                       | NO   |     | NULL    |                |
| content       | longtext                                   | NO   |     | NULL    |                |
| image         | varchar(255)                               | YES  |     | NULL    |                |
| status        | enum('draft','published')                  | NO   |     | draft   |                |
| published_at  | timestamp                                  | YES  | MUL | NULL    |                |
| views_count   | int unsigned                               | NO   |     | 0       |                |
| created_at    | timestamp                                  | YES  |     | NULL    |                |
| updated_at    | timestamp                                  | YES  |     | NULL    |                |
+---------------+--------------------------------------------+------+-----+---------+----------------+

-- Voir les clés étrangères et index
SHOW CREATE TABLE posts\G

-- Quitter MySQL
EXIT;
```

<small>*La colonne `Key` indique les index : `PRI` (clé primaire), `MUL` (index multiple/clé étrangère), `UNI` (index unique). Les contraintes `FOREIGN KEY` apparaissent dans `SHOW CREATE TABLE` avec leurs clauses `ON DELETE CASCADE`. Vérifiez que les types correspondent bien à vos attentes (notamment `enum` pour status et `longtext` pour content).*</small>

!!! success "Checkpoint Phase 2.5"
    À ce stade, votre base de données MySQL contient 12 tables dont 4 personnalisées (users, categories, posts, comments) avec toutes leurs relations et index. Vous pouvez passer aux modèles Eloquent.

## Étape 2.6 : Créer les Modèles Eloquent

**Contexte de l'étape :**

> Les migrations ont créé la **structure des tables en SQL**, mais pour **manipuler les données en PHP**, nous avons besoin de **modèles Eloquent**. Un modèle est une classe PHP qui représente une table et définit :

> 1. **Les colonnes modifiables** (`$fillable`) pour la protection contre mass-assignment
2. **Les relations** entre modèles (hasMany, belongsTo, etc.)
3. **Les scopes** : méthodes réutilisables pour filtrer les requêtes
4. **Les événements** : actions automatiques (ex: générer un slug à la création)
5. **Les casts** : conversion automatique de types (ex: `published_at` en objet Carbon)

!!! note "Laravel suit la convention "**nom de table pluriel = nom de modèle singulier**" : table `posts` ↔ modèle `Post`. Eloquent déduit automatiquement le nom de table, mais vous pouvez le forcer avec `protected $table = 'nom_table'`."

=== "Créer le Modèle Category"

    ```bash
    # Générer le modèle Category
    php artisan make:model Category

    # Résultat attendu :
    # Model created successfully.
    ```

    <small>*Cette commande crée le fichier `app/Models/Category.php`. Le flag `--migration` aurait créé automatiquement la migration associée, mais nous l'avons déjà faite manuellement.*</small>

    **Éditer `app/Models/Category.php` :**

    ```php title="Fichier : app/Models/Category.php"
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Support\Str;

    class Category extends Model
    {
        use HasFactory;  // Active les factories (génération données test)

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Les colonnes autorisées pour mass-assignment
         * 
         * Mass-assignment = remplir plusieurs colonnes d'un coup :
         * Category::create(['name' => 'Technologie', 'slug' => 'technologie']);
         * 
         * Sans $fillable, Laravel refuse par sécurité (protection contre injection).
         * Seules les colonnes listées ici peuvent être remplies massivement.
         * 
         * @var array<string>
         */
        protected $fillable = [
            'name',  // Nom de la catégorie
            'slug',  // Slug URL (généré auto, mais autorisé en cas d'override)
        ];

        /*
        |--------------------------------------------------------------------------
        | ÉVÉNEMENTS DU MODÈLE (Auto-génération du slug)
        |--------------------------------------------------------------------------
        */

        /**
         * Actions automatiques lors de la création/mise à jour
         * 
         * La méthode boot() s'exécute au chargement du modèle.
         * On y enregistre des événements (creating, updating, deleting, etc.)
         */
        protected static function boot()
        {
            parent::boot();  // Important : toujours appeler le boot parent

            /**
             * Événement creating : juste AVANT l'insertion en BDD
             * 
             * Si le slug est vide, on le génère automatiquement depuis le nom.
             * Exemple : "Technologie Web" → "technologie-web"
             */
            static::creating(function ($category) {
                // Si le slug n'est pas fourni manuellement
                if (empty($category->slug)) {
                    // Str::slug() convertit en URL-friendly :
                    // - Minuscules
                    // - Espaces → tirets
                    // - Accents supprimés (é → e)
                    // - Caractères spéciaux supprimés
                    $category->slug = Str::slug($category->name);
                }
            });

            /**
             * Alternative : gérer les doublons de slug
             * 
             * Si "Technologie" existe déjà, créer "technologie-1", "technologie-2", etc.
             * (Non implémenté ici pour rester simple, mais possible avec :)
             * 
             * $count = static::where('slug', 'LIKE', "{$category->slug}%")->count();
             * if ($count > 0) {
             *     $category->slug = "{$category->slug}-" . ($count + 1);
             * }
             */
        }

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Une catégorie a plusieurs posts (1-N)
         * 
         * Permet d'écrire : $category->posts (retourne Collection de Post)
         * 
         * Eloquent génère automatiquement la requête SQL :
         * SELECT * FROM posts WHERE category_id = ?
         * 
         * @return \Illuminate\Database\Eloquent\Relations\HasMany
         */
        public function posts()
        {
            return $this->hasMany(Post::class);
            // Équivaut à : return $this->hasMany(Post::class, 'category_id', 'id');
            // Laravel déduit automatiquement les clés (category_id, id)
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Nombre d'articles dans cette catégorie
         * 
         * Utilisation : $category->postsCount()
         * Alternative avec attribut : protected $appends = ['posts_count'];
         */
        public function postsCount()
        {
            return $this->posts()->count();
        }
    }
    ```

    <small>*La génération automatique du slug dans `boot()` est une **excellente pratique** : elle évite d'avoir à appeler manuellement `Str::slug()` partout dans le code. L'événement `creating` garantit que le slug est généré **avant** l'insertion en base, donc la contrainte `unique()` de la migration peut valider l'unicité immédiatement.*</small>

=== "Créer le Modèle Post"

    ```bash
    # Générer le modèle Post
    php artisan make:model Post

    # Résultat attendu :
    # Model created successfully.
    ```

    **Éditer `app/Models/Post.php` :**

    ```php title="Fichier : app/Models/Post.php"
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Support\Str;

    class Post extends Model
    {
        use HasFactory;

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * @var array<string>
         */
        protected $fillable = [
            'user_id',       // Auteur de l'article
            'category_id',   // Catégorie de l'article
            'title',         // Titre
            'slug',          // Slug URL (généré auto mais peut être overridé)
            'excerpt',       // Résumé court
            'content',       // Contenu complet
            'image',         // URL image couverture
            'status',        // draft ou published
            'published_at',  // Date publication (rempli auto si status=published)
        ];

        /**
         * Casts automatiques de types
         * 
         * Laravel convertit automatiquement ces colonnes :
         * - published_at (string en BDD) → objet Carbon (manipulation dates)
         * 
         * Exemple : $post->published_at->format('d/m/Y') fonctionne directement
         * 
         * @var array<string, string>
         */
        protected $casts = [
            'published_at' => 'datetime',  // TIMESTAMP → Carbon\Carbon
        ];

        /*
        |--------------------------------------------------------------------------
        | ÉVÉNEMENTS DU MODÈLE (Auto-slug et auto-publish_at)
        |--------------------------------------------------------------------------
        */

        protected static function boot()
        {
            parent::boot();

            /**
             * Événement creating : à la création d'un nouveau post
             */
            static::creating(function ($post) {
                // 1. Générer le slug si vide
                if (empty($post->slug)) {
                    $post->slug = Str::slug($post->title);
                    
                    // Gestion des doublons de slug
                    // Si "introduction-laravel" existe, créer "introduction-laravel-2"
                    $count = static::where('slug', 'LIKE', "{$post->slug}%")->count();
                    if ($count > 0) {
                        $post->slug = "{$post->slug}-" . ($count + 1);
                    }
                }
                
                // 2. Si status=published, définir published_at automatiquement
                if ($post->status === 'published' && empty($post->published_at)) {
                    $post->published_at = now();  // now() = Carbon::now()
                }
            });

            /**
             * Événement updating : lors d'une modification
             * 
             * Exemple : Un auteur passe son brouillon en publié
             */
            static::updating(function ($post) {
                // Si le status passe de draft à published
                if ($post->isDirty('status') &&           // La colonne status a changé
                    $post->status === 'published' &&      // Nouvelle valeur = published
                    empty($post->published_at)) {         // Et pas encore de date publication
                    
                    $post->published_at = now();          // On timestamp la publication
                }
            });

            /**
             * Note : On ne regénère PAS le slug lors de l'update du titre
             * Raison : changement d'URL casserait les liens existants (SEO)
             * Alternative : garder l'ancien slug ou créer une redirection 301
             */
        }

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un post appartient à un utilisateur (N-1)
         * 
         * Permet : $post->user (retourne instance de User)
         * SQL généré : SELECT * FROM users WHERE id = ?
         */
        public function user()
        {
            return $this->belongsTo(User::class);
        }
        
        /**
         * Alias de user() pour plus de clarté sémantique
         * 
         * Permet d'écrire : $post->author->name au lieu de $post->user->name
         */
        public function author()
        {
            return $this->user();
        }

        /**
         * Relation : Un post appartient à une catégorie (N-1)
         * 
         * Permet : $post->category (retourne instance de Category)
         */
        public function category()
        {
            return $this->belongsTo(Category::class);
        }

        /**
         * Relation : Un post a plusieurs commentaires (1-N)
         * 
         * Permet : $post->comments (retourne Collection de Comment)
         */
        public function comments()
        {
            return $this->hasMany(Comment::class);
        }

        /*
        |--------------------------------------------------------------------------
        | QUERY SCOPES (Filtres réutilisables)
        |--------------------------------------------------------------------------
        | Les scopes sont des méthodes de filtrage qu'on peut chaîner.
        | Convention : prefixe "scope" + nom en PascalCase
        | Utilisation : Post::published()->get()
        */

        /**
         * Scope : Récupérer seulement les posts publiés
         * 
         * Utilisation : Post::published()->get()
         * SQL : WHERE status='published' AND published_at IS NOT NULL AND published_at <= NOW()
         * 
         * @param \Illuminate\Database\Eloquent\Builder $query
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopePublished($query)
        {
            return $query->where('status', 'published')
                        ->whereNotNull('published_at')      // published_at doit être rempli
                        ->where('published_at', '<=', now()); // Date publication passée/actuelle
                                                              // (permet de programmer publication future)
        }

        /**
         * Scope : Récupérer seulement les brouillons
         * 
         * Utilisation : Post::draft()->get()
         */
        public function scopeDraft($query)
        {
            return $query->where('status', 'draft');
        }

        /**
         * Exemple de scope chaîné :
         * Post::published()->where('category_id', 1)->latest()->get()
         * = Articles publiés de la catégorie 1, triés par date DESC
         */

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Incrémenter le compteur de vues
         * 
         * Utilisation : $post->incrementViews()
         * SQL généré : UPDATE posts SET views_count = views_count + 1 WHERE id = ?
         * 
         * @return void
         */
        public function incrementViews()
        {
            $this->increment('views_count');
            // Équivaut à : $this->views_count++; $this->save();
            // Mais increment() génère un UPDATE optimisé en 1 seule requête
        }

        /**
         * Vérifier si le post est publié
         * 
         * @return bool
         */
        public function isPublished()
        {
            return $this->status === 'published' && $this->published_at !== null;
        }

        /**
         * Obtenir l'URL complète du post
         * 
         * @return string
         */
        public function getUrl()
        {
            return route('posts.show', $this->slug);
        }
    }
    ```

    <small>*Le scope `published()` est **crucial** : il évite d'écrire `where('status', 'published')` partout dans le code. Si demain vous ajoutez une condition supplémentaire (ex: `is_featured`), vous la modifiez une seule fois dans le scope, et tout le code en bénéficie automatiquement. La méthode `incrementViews()` utilise `increment()` plutôt que `$post->views_count++; $post->save();` pour éviter les conditions de concurrence (race conditions) si deux utilisateurs visitent l'article simultanément.*</small>

=== "Créer le Modèle Comment"

    ```bash
    # Générer le modèle Comment
    php artisan make:model Comment

    # Résultat attendu :
    # Model created successfully.
    ```

    **Éditer `app/Models/Comment.php` :**

    ```php title="Fichier : app/Models/Comment.php"
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;

    class Comment extends Model
    {
        use HasFactory;

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * @var array<string>
         */
        protected $fillable = [
            'post_id',       // Article commenté
            'author_name',   // Nom du commentateur (visiteur non inscrit)
            'author_email',  // Email du commentateur
            'content',       // Contenu du commentaire
            'approved',      // Statut modération (0=en attente, 1=approuvé)
        ];

        /**
         * Casts automatiques de types
         * 
         * approved (tinyint en BDD) → boolean en PHP
         * Permet d'écrire : if ($comment->approved) au lieu de if ($comment->approved == 1)
         * 
         * @var array<string, string>
         */
        protected $casts = [
            'approved' => 'boolean',
        ];

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un commentaire appartient à un post (N-1)
         * 
         * Permet : $comment->post (retourne instance de Post)
         */
        public function post()
        {
            return $this->belongsTo(Post::class);
        }

        /**
         * Note : Pas de relation vers User
         * 
         * Les commentateurs ne sont pas des utilisateurs inscrits.
         * On stocke juste leur nom/email fournis dans le formulaire.
         * 
         * Alternative future : Permettre aux users connectés de commenter
         * avec auto-remplissage nom/email depuis leur profil.
         * → Ajouter colonne nullable('user_id') + relation belongsTo(User)
         */

        /*
        |--------------------------------------------------------------------------
        | QUERY SCOPES
        |--------------------------------------------------------------------------
        */

        /**
         * Scope : Récupérer seulement les commentaires approuvés
         * 
         * Utilisation : Comment::approved()->get()
         * Ou chaîné : $post->comments()->approved()->get()
         * 
         * @param \Illuminate\Database\Eloquent\Builder $query
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopeApproved($query)
        {
            return $query->where('approved', true);
        }

        /**
         * Scope : Commentaires en attente de modération
         * 
         * Utilisation : Comment::pending()->get()
         */
        public function scopePending($query)
        {
            return $query->where('approved', false);
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Approuver le commentaire
         * 
         * @return bool
         */
        public function approve()
        {
            $this->approved = true;
            return $this->save();
        }

        /**
         * Rejeter le commentaire (le marquer comme non approuvé)
         * 
         * @return bool
         */
        public function reject()
        {
            $this->approved = false;
            return $this->save();
        }

        /**
         * Obtenir l'avatar Gravatar du commentateur
         * 
         * @param int $size Taille de l'image en pixels
         * @return string URL de l'avatar
         */
        public function getGravatarUrl($size = 80)
        {
            $hash = md5(strtolower(trim($this->author_email)));
            return "https://www.gravatar.com/avatar/{$hash}?s={$size}&d=mp";
        }
    }
    ```

    <small>*Le scope `approved()` est essentiel pour afficher **uniquement les commentaires modérés** sur la page publique de l'article. La méthode `getGravatarUrl()` est une astuce pratique : elle génère automatiquement l'avatar du commentateur via son email en utilisant le service Gravatar (avatars universels associés aux emails). Si l'email n'a pas de Gravatar, Gravatar retourne un avatar par défaut (`d=mp` = mystère person).*</small>

=== "Enrichir le Modèle User"

    Le modèle `User` existe déjà (généré par Breeze), mais nous devons lui ajouter la relation vers `posts` et les colonnes `bio`/`avatar` dans `$fillable`.

    **Ouvrir `app/Models/User.php` et modifier :**

    ```php title="Fichier : app/Models/User.php"
    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable
    {
        use Notifiable;

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * ✅ AJOUTER bio et avatar à la liste existante
         * 
         * @var array<int, string>
         */
        protected $fillable = [
            'name',
            'email',
            'password',
            'bio',        // ✅ Ajouté : biographie auteur
            'avatar',     // ✅ Ajouté : URL avatar
        ];

        /**
         * Colonnes cachées lors de la sérialisation JSON
         * 
         * Important pour sécurité : empêche l'exposition du password hashé
         * dans les réponses API ou les logs.
         * 
         * @var array<int, string>
         */
        protected $hidden = [
            'password',
            'remember_token',
        ];

        /**
         * Casts automatiques
         * 
         * @return array<string, string>
         */
        protected function casts(): array
        {
            return [
                'email_verified_at' => 'datetime',
                'password' => 'hashed',  // Hash automatique du password à l'assignation
            ];
        }

        /*
        |--------------------------------------------------------------------------
        | ✅ AJOUTER : RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un utilisateur a plusieurs posts (1-N)
         * 
         * Permet : $user->posts (retourne Collection de Post)
         * Permet aussi : $user->posts()->published()->get() (chaîner scopes)
         * 
         * @return \Illuminate\Database\Eloquent\Relations\HasMany
         */
        public function posts()
        {
            return $this->hasMany(Post::class);
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Obtenir l'initiale du nom (pour affichage avatar)
         * 
         * Exemple : "Alice Dupont" → "A"
         * Utilisé quand l'utilisateur n'a pas uploadé d'avatar
         * 
         * @return string
         */
        public function getInitial()
        {
            return strtoupper(substr($this->name, 0, 1));
        }

        /**
         * Vérifier si l'utilisateur a des articles publiés
         * 
         * @return bool
         */
        public function hasPublishedPosts()
        {
            return $this->posts()->published()->exists();
        }

        /**
         * Nombre total de vues sur tous les articles de l'auteur
         * 
         * @return int
         */
        public function totalViews()
        {
            return $this->posts()->sum('views_count');
        }
    }
    ```

    <small>*Les méthodes utilitaires `getInitial()`, `hasPublishedPosts()` et `totalViews()` ne sont pas obligatoires mais rendent le code des contrôleurs/vues plus lisible. Plutôt que d'écrire `strtoupper(substr($user->name, 0, 1))` partout, on écrit simplement `$user->getInitial()`. Ces méthodes sont appelées **accessors** ou **helper methods**.*</small>

## Récapitulatif Phase 2 : Ce que vous avez construit

=== "Migrations (Structure SQL)"

    - `users` enrichi avec `bio` et `avatar`
    - `categories` avec génération auto de slug
    - `posts` avec relations vers users/categories, statuts, compteur vues, index optimisés
    - `comments` avec modération, sans lien vers users (visiteurs anonymes)

=== "Modèles Eloquent (Représentation PHP)"

    - `Category` : génération auto slug, relation hasMany posts
    - `Post` : génération auto slug avec gestion doublons, auto-remplissage published_at, relations vers User/Category/Comment, scopes published/draft, méthode incrementViews
    - `Comment` : cast boolean pour approved, scopes approved/pending, méthodes approve/reject, génération Gravatar
    - `User` : relation hasMany posts, méthodes utilitaires (initial, total vues)

=== "Concepts Laravel maîtrisés"

    - Migrations avec clés étrangères, index, cascade delete
    - Eloquent relations (hasMany, belongsTo)
    - Mass assignment protection ($fillable)
    - Type casting ($casts)
    - Model events (boot, creating, updating)
    - Query scopes (filtres réutilisables)
    - Helper methods (méthodes utilitaires)

!!! success "Phase 2 Terminée - Votre architecture de données est maintenant **complète et opérationnelle**. Vous êtes prêt à passer à la **Phase 3 : Seeders** pour remplir la base avec des données de test réalistes, puis à la **Phase 4 : Contrôleurs** pour implémenter la logique métier du blog."

<br />