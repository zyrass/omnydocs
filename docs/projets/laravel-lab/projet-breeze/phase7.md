---
description: "29 tests automatisés (Feature + Unit), optimisations performance (indexes, cache, Eager Loading), sécurité et déploiement production OVH complet."
icon: lucide/rocket
tags: ["TESTS", "OPTIMIZATION", "DEPLOYMENT", "PRODUCTION", "SECURITY"]
---

# Phase 7 : Tests, Optimisation & Déploiement

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="4h-6h">
</div>


!!! quote "Analogie pédagogique"
    _Créer l'authentification avec Breeze, c'est comme installer des serrures pré-certifiées dans une nouvelle maison. Plutôt que de fondre votre propre métal pour forger une clé, vous utilisez un standard industriel éprouvé, ce qui vous permet de vous concentrer sur la construction des vraies pièces de la maison._

## Introduction aux Tests, Optimisation et Déploiement

**Vue d'ensemble de la phase :**

> La Phase 7 finalise le projet en garantissant **qualité**, **performance** et **sécurité**. C'est la différence entre un projet "qui fonctionne" et un projet **production-ready** déployable en entreprise.

!!! note "**Objectifs de la phase :**"

    1. **Tests automatisés** : Vérifier que le code fonctionne correctement (Feature + Unit)
    2. **Optimisation** : Améliorer performance (caching, indexes, queries)
    3. **Sécurité** : Renforcer protection (rate limiting, validation, headers)
    4. **Configuration production** : Préparer environnement déploiement (.env, optimizations)
    5. **Déploiement** : Guide mise en ligne (serveur, base de données, domaine)

!!! quote "**Structure de la phase :**"

    ```
    Phase 7 : Tests et Déploiement
    │
    ├── Étape 7.1 : Tests Feature (Contrôleurs)
    ├── Étape 7.2 : Tests Unit (Modèles et Helpers)
    ├── Étape 7.3 : Optimisation Performance
    ├── Étape 7.4 : Sécurité et Hardening
    ├── Étape 7.5 : Configuration Production
    └── Étape 7.6 : Guide Déploiement
    ```

### Étape 7.1 : Tests Feature (Contrôleurs et Routes)

**Contexte :**

> Les **Feature Tests** testent l'application **de bout en bout** : requêtes HTTP → contrôleurs → base de données → réponses. Ils simulent le comportement d'un utilisateur réel naviguant sur le site.

!!! note "**Avantages tests automatisés :**"

    - ✅ **Détection bugs** : Trouve erreurs avant production
    - ✅ **Refactoring sûr** : Modifie code sans casser fonctionnalités
    - ✅ **Documentation vivante** : Tests montrent comment utiliser code
    - ✅ **Confiance déploiement** : Vert = safe to deploy

**Framework Laravel : PHPUnit**

Laravel intègre PHPUnit avec helpers spécifiques :

```php
// Simuler requête HTTP
$response = $this->get('/posts/1');

// Vérifier status HTTP
$response->assertStatus(200);

// Vérifier contenu réponse
$response->assertSee('Titre Article');

// Vérifier redirection
$response->assertRedirect('/dashboard');

// Vérifier base de données
$this->assertDatabaseHas('posts', ['title' => 'Mon Article']);
```

??? abstract "7.1.1 : Configuration Base de Données Tests"

    **Créer base de données SQLite pour tests :**

    Laravel utilise par défaut une base SQLite **en mémoire** pour tests (ultra-rapide, isolée).

    **Ouvrir `phpunit.xml`** (racine projet) et **vérifier la configuration** :

    ```xml title="Fichier : phpunit.xml"
    <?xml version="1.0" encoding="UTF-8"?>
    <phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
            bootstrap="vendor/autoload.php"
            colors="true">
        <testsuites>
            <testsuite name="Unit">
                <directory>tests/Unit</directory>
            </testsuite>
            <testsuite name="Feature">
                <directory>tests/Feature</directory>
            </testsuite>
        </testsuites>
        
        <!--
        |--------------------------------------------------------------------------
        | VARIABLES D'ENVIRONNEMENT TESTS
        |--------------------------------------------------------------------------
        | Ces variables écrasent celles du .env lors de l'exécution des tests
        | Garantit isolation complète (pas de pollution base de données dev)
        -->
        <php>
            <!--
            | APP_ENV=testing : Mode test (Laravel ajuste comportements)
            | Exemple : Mails ne sont pas envoyés réellement, files pas créés réellement
            -->
            <env name="APP_ENV" value="testing"/>
            
            <!--
            | DB_CONNECTION=sqlite : Base de données SQLite (fichier unique)
            | Alternative MySQL : Créer base séparée "blog_test"
            -->
            <env name="DB_CONNECTION" value="sqlite"/>
            
            <!--
            | DB_DATABASE=:memory: : Base SQLite en RAM (pas de fichier disque)
            | Ultra-rapide : 100x plus rapide que MySQL/PostgreSQL
            | Détruite après chaque suite de tests (isolation garantie)
            | 
            | Alternative SQLite fichier (persistance) :
            | <env name="DB_DATABASE" value="database/testing.sqlite"/>
            -->
            <env name="DB_DATABASE" value=":memory:"/>
            
            <!--
            | BCRYPT_ROUNDS=4 : Réduit itérations bcrypt (passwords)
            | Défaut : 10 rounds (2^10 = 1024 itérations, ~100ms)
            | Tests : 4 rounds (2^4 = 16 itérations, ~1ms)
            | Accélère tests avec authentification × 100
            -->
            <env name="BCRYPT_ROUNDS" value="4"/>
            
            <!--
            | HASH_DRIVER=bcrypt : Force bcrypt (cohérence production)
            | Alternative : argon2id (plus sécurisé mais plus lent)
            -->
            <env name="HASH_DRIVER" value="bcrypt"/>
            
            <!--
            | CACHE_DRIVER=array : Cache en mémoire (pas Redis/Memcached)
            | Évite dépendance services externes pendant tests
            -->
            <env name="CACHE_DRIVER" value="array"/>
            
            <!--
            | QUEUE_CONNECTION=sync : Exécution synchrone (pas de workers)
            | Jobs exécutés immédiatement pendant tests
            | Évite attendre workers asynchrones
            -->
            <env name="QUEUE_CONNECTION" value="sync"/>
            
            <!--
            | SESSION_DRIVER=array : Sessions en mémoire
            | Pas de fichiers/Redis pendant tests
            -->
            <env name="SESSION_DRIVER" value="array"/>
            
            <!--
            | MAIL_MAILER=array : Mails interceptés (pas envoyés réellement)
            | Testables via Mail::assertSent()
            -->
            <env name="MAIL_MAILER" value="array"/>
        </php>
    </phpunit>
    ```

    **Exécuter les tests :**

    ```bash
    # Exécuter tous les tests
    php artisan test

    # Exécuter seulement tests Feature
    php artisan test --testsuite=Feature

    # Exécuter seulement tests Unit
    php artisan test --testsuite=Unit

    # Exécuter test spécifique
    php artisan test --filter=test_home_page_displays_posts

    # Mode verbose (détails)
    php artisan test -v

    # Coverage (nécessite xdebug)
    php artisan test --coverage
    ```

??? abstract "7.1.2 : Tests Feature - HomeController"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test HomeControllerTest
    ```

    **Éditer `tests/Feature/HomeControllerTest.php` :**

    ```php title="Fichier : tests/Feature/HomeControllerTest.php"
    <?php

    namespace Tests\Feature;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Feature : HomeController
     * 
     * Teste la page d'accueil du blog
     * - Affichage des articles publiés
     * - Pagination fonctionnelle
     * - Sidebar catégories et articles populaires
     */
    class HomeControllerTest extends TestCase
    {
        /**
         * RefreshDatabase : Trait Laravel qui :
         * 1. Exécute toutes les migrations (schéma BDD)
         * 2. Utilise transaction pour chaque test
         * 3. Rollback automatique après chaque test
         * 
         * Résultat : Base de données vierge pour chaque test (isolation)
         * 
         * Alternative :
         * use DatabaseMigrations; // Migrations complètes (plus lent)
         * use DatabaseTransactions; // Rollback seulement (nécessite BDD existante)
         */
        use RefreshDatabase;

        /**
         * Test : Page d'accueil accessible
         * 
         * Vérifie :
         * - Route / retourne status 200 (OK)
         * - Page contient titre "Bienvenue"
         */
        public function test_home_page_is_accessible(): void
        {
            // Simuler requête GET /
            // $this->get() : Helper Laravel, retourne objet TestResponse
            $response = $this->get('/');

            // Assertions : Vérifications
            // assertStatus(200) : Code HTTP 200 (OK)
            // 200 = succès, 404 = non trouvé, 500 = erreur serveur
            $response->assertStatus(200);

            // assertSee('texte') : Vérifie présence texte dans HTML réponse
            // Par défaut : échappe HTML (cherche "Bienvenue" échappé)
            // assertSee('Bienvenue', false) : Désactive échappement (HTML brut)
            $response->assertSee('Bienvenue');
        }

        /**
        * Test : Articles publiés affichés sur page d'accueil
        * 
        * Vérifie :
        * - Articles publiés visibles
        * - Brouillons NON visibles
        * - Articles futurs NON visibles
        */
        public function test_published_posts_are_displayed(): void
        {
            // Arrange : Préparer données test
            // Factory Pattern : Génère données factices réalistes
            
            /**
            * User::factory()->create() : Crée utilisateur en BDD
            * Équivaut à :
            * INSERT INTO users (name, email, password, ...) VALUES (...)
            * 
            * factory() : Appelle UserFactory défini dans database/factories/
            * create() : Insère en BDD (vs make() qui crée instance sans INSERT)
            */
            $user = User::factory()->create();

            /**
            * Category::factory()->create() : Crée catégorie en BDD
            */
            $category = Category::factory()->create();

            /**
            * Post::factory()->create() : Crée article PUBLIÉ
            * 
            * Par défaut PostFactory génère :
            * - status = 'published'
            * - published_at = now()
            * 
            * Associations automatiques :
            * - user_id = $user->id
            * - category_id = $category->id
            */
            $publishedPost = Post::factory()->create([
                'title' => 'Article Publié Visible',
                'status' => 'published',
                'published_at' => now()->subDay(), // Hier
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            /**
            * Créer brouillon (NE DOIT PAS apparaître)
            */
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon Non Visible',
                'status' => 'draft',
                'published_at' => null, // Pas de date publication
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            /**
            * Créer article futur (NE DOIT PAS apparaître)
            */
            $futurePost = Post::factory()->create([
                'title' => 'Article Futur Non Visible',
                'status' => 'published',
                'published_at' => now()->addDay(), // Demain
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Exécuter action testée
            $response = $this->get('/');

            // Assert : Vérifier résultats
            $response->assertStatus(200);
            
            /**
            * assertSee() : Vérifie présence texte
            * Cherche dans HTML réponse (échappé par défaut)
            */
            $response->assertSee('Article Publié Visible');
            
            /**
            * assertDontSee() : Vérifie ABSENCE texte
            * Brouillon et article futur NE DOIVENT PAS être visibles
            */
            $response->assertDontSee('Brouillon Non Visible');
            $response->assertDontSee('Article Futur Non Visible');
        }

        /**
        * Test : Pagination fonctionne (9 articles par page)
        * 
        * Vérifie :
        * - Page 1 affiche 9 articles
        * - Page 2 accessible avec paramètre ?page=2
        * - Articles paginés correctement
        */
        public function test_pagination_works_correctly(): void
        {
            // Arrange : Créer 15 articles publiés
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Post::factory()->count(15)->create() : Crée 15 articles
            * 
            * Boucle équivalente :
            * for ($i = 0; $i < 15; $i++) {
            *     Post::factory()->create([...]);
            * }
            */
            Post::factory()->count(15)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Tester page 1
            $responsePage1 = $this->get('/');

            // Assert : Page 1 contient exactement 9 articles
            /**
            * assertViewHas('posts') : Vérifie variable 'posts' passée à la vue
            * 
            * Équivaut à vérifier dans contrôleur :
            * return view('home', compact('posts')); // $posts doit exister
            */
            $responsePage1->assertViewHas('posts');
            
            /**
            * $responsePage1->viewData('posts') : Récupère variable 'posts' de la vue
            * ->count() : Compte éléments Collection
            */
            $this->assertEquals(9, $responsePage1->viewData('posts')->count());

            // Act : Tester page 2
            $responsePage2 = $this->get('/?page=2');

            // Assert : Page 2 contient 6 articles restants (15 - 9 = 6)
            $responsePage2->assertStatus(200);
            $this->assertEquals(6, $responsePage2->viewData('posts')->count());
        }

        /**
        * Test : Sidebar catégories affichée avec compteurs
        * 
        * Vérifie :
        * - Catégories affichées dans sidebar
        * - Compteurs articles corrects (withCount)
        */
        public function test_sidebar_displays_categories_with_counts(): void
        {
            // Arrange
            $user = User::factory()->create();
            
            /**
            * Créer 2 catégories avec articles
            */
            $categoryTech = Category::factory()->create(['name' => 'Technologie']);
            $categoryVoyage = Category::factory()->create(['name' => 'Voyage']);

            // Catégorie Technologie : 3 articles
            Post::factory()->count(3)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $categoryTech->id,
            ]);

            // Catégorie Voyage : 2 articles
            Post::factory()->count(2)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $categoryVoyage->id,
            ]);

            // Act
            $response = $this->get('/');

            // Assert : Vérifier présence catégories
            $response->assertStatus(200);
            $response->assertSee('Technologie');
            $response->assertSee('Voyage');

            /**
            * Vérifier compteurs
            * assertSee('3') : Cherche "3" dans HTML (compteur catégorie Tech)
            * assertSee('2') : Cherche "2" dans HTML (compteur catégorie Voyage)
            */
            $response->assertSee('3'); // Compteur Technologie
            $response->assertSee('2'); // Compteur Voyage
        }

        /**
        * Test : Articles populaires affichés (top 3 vues)
        * 
        * Vérifie :
        * - 3 articles les plus vus affichés dans sidebar
        * - Ordre décroissant (plus de vues en premier)
        */
        public function test_popular_posts_are_displayed(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Créer articles avec compteurs vues différents
            */
            $post1 = Post::factory()->create([
                'title' => 'Article Populaire #1',
                'views_count' => 500, // Le plus populaire
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post2 = Post::factory()->create([
                'title' => 'Article Populaire #2',
                'views_count' => 300, // Deuxième
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post3 = Post::factory()->create([
                'title' => 'Article Populaire #3',
                'views_count' => 100, // Troisième
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post4 = Post::factory()->create([
                'title' => 'Article Peu Populaire',
                'views_count' => 10, // Pas dans top 3
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act
            $response = $this->get('/');

            // Assert : Vérifier présence top 3
            $response->assertStatus(200);
            $response->assertSee('Article Populaire #1');
            $response->assertSee('Article Populaire #2');
            $response->assertSee('Article Populaire #3');
            
            /**
            * Vérifier absence article peu populaire
            * Ne doit PAS apparaître dans top 3
            */
            $response->assertDontSee('Article Peu Populaire');
        }
    }
    ```

??? abstract "7.1.3 : Tests Feature - PostController"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test PostControllerTest
    ```

    **Éditer `tests/Feature/PostControllerTest.php` :**

    ```php title="Fichier : tests/Feature/PostControllerTest.php"
    <?php

    namespace Tests\Feature;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Feature : PostController
     * 
     * Teste les fonctionnalités CRUD des articles
     */
    class PostControllerTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * Test : Article individuel accessible (page show)
         * 
         * Vérifie :
         * - Route /posts/{slug} retourne 200
         * - Contenu article affiché (titre, contenu, auteur)
         */
        public function test_published_post_is_accessible(): void
        {
            // Arrange
            $user = User::factory()->create(['name' => 'Alice Dupont']);
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'title' => 'Mon Article Test',
                'slug' => 'mon-article-test',
                'content' => 'Contenu complet de mon article test.',
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Accéder via slug
            $response = $this->get('/posts/' . $post->slug);

            // Assert
            $response->assertStatus(200);
            $response->assertSee('Mon Article Test');
            $response->assertSee('Contenu complet de mon article test.');
            $response->assertSee('Alice Dupont'); // Nom auteur
        }

        /**
        * Test : Brouillon non accessible publiquement (404)
        * 
        * Vérifie :
        * - Visiteur anonyme : 404 Not Found
        * - Autre utilisateur : 404 Not Found
        * - Auteur article : 200 OK (accès autorisé)
        */
        public function test_draft_post_not_accessible_to_public(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon Privé',
                'slug' => 'brouillon-prive',
                'status' => 'draft',
                'published_at' => null,
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Visiteur anonyme → 404
            $response = $this->get('/posts/' . $draftPost->slug);
            $response->assertStatus(404);

            // Act & Assert : Autre utilisateur connecté → 404
            /**
            * $this->actingAs($user) : Simule connexion utilisateur
            * 
            * Équivaut à :
            * Auth::login($user);
            * 
            * Tous les appels suivants considèrent $user comme connecté
            */
            $response = $this->actingAs($otherUser)->get('/posts/' . $draftPost->slug);
            $response->assertStatus(404);

            // Act & Assert : Auteur article → 200 (accès autorisé)
            $response = $this->actingAs($author)->get('/posts/' . $draftPost->slug);
            $response->assertStatus(200);
            $response->assertSee('Brouillon Privé');
        }

        /**
        * Test : Incrément compteur vues fonctionne
        * 
        * Vérifie :
        * - views_count incrémenté après visite
        * - Plusieurs visites = plusieurs incréments
        */
        public function test_post_views_count_is_incremented(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'views_count' => 0, // Initialement 0
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier valeur initiale
            $this->assertEquals(0, $post->views_count);

            // Act : Visiter article
            $this->get('/posts/' . $post->slug);

            // Assert : Vérifier incrément (+1)
            /**
            * $post->fresh() : Recharge modèle depuis BDD
            * 
            * Nécessaire car $post en mémoire n'est pas mis à jour automatiquement
            * après modifications en BDD
            */
            $this->assertEquals(1, $post->fresh()->views_count);

            // Act : Visiter à nouveau
            $this->get('/posts/' . $post->slug);

            // Assert : Vérifier nouvel incrément (+1, total = 2)
            $this->assertEquals(2, $post->fresh()->views_count);
        }

        /**
        * Test : Création article nécessite authentification
        * 
        * Vérifie :
        * - Visiteur anonyme redirigé vers /login
        * - Utilisateur connecté accède au formulaire
        */
        public function test_create_post_requires_authentication(): void
        {
            // Act : Visiteur anonyme tente accéder /posts/create
            $response = $this->get('/posts/create');

            // Assert : Redirection vers login
            /**
            * assertRedirect('/login') : Vérifie status 302 + header Location
            */
            $response->assertRedirect('/login');

            // Act : Utilisateur connecté accède formulaire
            $user = User::factory()->create();
            $response = $this->actingAs($user)->get('/posts/create');

            // Assert : Succès
            $response->assertStatus(200);
            $response->assertSee('Créer un Article'); // Titre formulaire
        }

        /**
        * Test : Création article avec données valides
        * 
        * Vérifie :
        * - Article créé en BDD
        * - Redirection vers article créé
        * - Message succès affiché
        * - Slug généré automatiquement
        */
        public function test_authenticated_user_can_create_post(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Données formulaire
            * Tableau associatif = $_POST en PHP
            */
            $postData = [
                'title' => 'Nouvel Article Créé',
                'category_id' => $category->id,
                'excerpt' => 'Résumé de mon nouvel article.',
                'content' => 'Contenu complet de mon nouvel article avec plus de 100 caractères pour passer validation.',
                'image' => 'https://example.com/image.jpg',
                'status' => 'published',
            ];

            // Act : Soumettre formulaire création
            /**
            * $this->actingAs($user)->post($url, $data) : Simule soumission POST
            * 
            * Équivaut à :
            * - Auth::login($user)
            * - Soumettre formulaire avec données $postData
            * - CSRF token ajouté automatiquement par Laravel
            */
            $response = $this->actingAs($user)
                ->post('/posts', $postData);

            // Assert : Vérifier création BDD
            /**
            * assertDatabaseHas('table', ['column' => 'value'])
            * 
            * Vérifie existence enregistrement en BDD
            * Équivaut à :
            * SELECT * FROM posts WHERE title = 'Nouvel Article Créé' LIMIT 1
            * assertTrue(count($result) > 0)
            */
            $this->assertDatabaseHas('posts', [
                'title' => 'Nouvel Article Créé',
                'user_id' => $user->id,
                'category_id' => $category->id,
                'status' => 'published',
            ]);

            // Assert : Vérifier slug auto-généré
            /**
            * Slug doit être généré via événement creating() dans modèle
            * "Nouvel Article Créé" → "nouvel-article-cree"
            */
            $post = Post::where('title', 'Nouvel Article Créé')->first();
            $this->assertEquals('nouvel-article-cree', $post->slug);

            // Assert : Vérifier redirection vers article créé
            $response->assertRedirect('/posts/' . $post->slug);

            // Assert : Vérifier message succès
            /**
            * assertSessionHas('success') : Vérifie variable flash session
            * 
            * Équivaut à vérifier dans contrôleur :
            * return redirect()->with('success', 'Article créé avec succès');
            */
            $response->assertSessionHas('success');
        }

        /**
        * Test : Validation formulaire création
        * 
        * Vérifie :
        * - Champs requis provoquent erreurs validation
        * - Erreurs affichées dans session
        */
        public function test_create_post_validation_fails_with_invalid_data(): void
        {
            // Arrange
            $user = User::factory()->create();

            /**
            * Données invalides :
            * - title : manquant (requis)
            * - category_id : invalide (n'existe pas en BDD)
            * - content : trop court (min 100 chars)
            */
            $invalidData = [
                'title' => '', // Vide (requis)
                'category_id' => 9999, // N'existe pas
                'excerpt' => 'Résumé valide.',
                'content' => 'Court', // < 100 caractères
                'status' => 'published',
            ];

            // Act : Soumettre données invalides
            $response = $this->actingAs($user)
                ->post('/posts', $invalidData);

            // Assert : Vérifier erreurs validation
            /**
            * assertSessionHasErrors(['field1', 'field2'])
            * 
            * Vérifie présence erreurs pour champs spécifiés
            * Équivaut à vérifier :
            * session()->has('errors') && $errors->has('title')
            */
            $response->assertSessionHasErrors(['title', 'category_id', 'content']);

            // Assert : Vérifier article PAS créé en BDD
            /**
            * assertDatabaseMissing('table', ['column' => 'value'])
            * 
            * Vérifie ABSENCE enregistrement en BDD
            */
            $this->assertDatabaseMissing('posts', [
                'excerpt' => 'Résumé valide.',
            ]);
        }

        /**
        * Test : Édition article nécessite être l'auteur
        * 
        * Vérifie :
        * - Auteur article : accès formulaire édition (200)
        * - Autre utilisateur : erreur 403 Forbidden
        * - Visiteur anonyme : redirection login
        */
        public function test_only_author_can_edit_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Visiteur anonyme → Redirection login
            $response = $this->get('/posts/' . $post->slug . '/edit');
            $response->assertRedirect('/login');

            // Act & Assert : Autre utilisateur → 403 Forbidden
            /**
            * assertStatus(403) : Vérifie erreur Forbidden
            * 403 = Authentifié mais pas autorisé (ownership check)
            */
            $response = $this->actingAs($otherUser)
                ->get('/posts/' . $post->slug . '/edit');
            $response->assertStatus(403);

            // Act & Assert : Auteur article → 200 OK
            $response = $this->actingAs($author)
                ->get('/posts/' . $post->slug . '/edit');
            $response->assertStatus(200);
            $response->assertSee('Modifier l\'Article'); // Titre formulaire
        }

        /**
        * Test : Mise à jour article avec données valides
        * 
        * Vérifie :
        * - Article modifié en BDD
        * - Redirection vers article mis à jour
        * - Message succès affiché
        */
        public function test_author_can_update_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'title' => 'Titre Original',
                'content' => 'Contenu original de l\'article avec suffisamment de texte pour validation.',
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Données mise à jour
            $updatedData = [
                'title' => 'Titre Modifié',
                'category_id' => $category->id,
                'excerpt' => 'Résumé modifié.',
                'content' => 'Contenu modifié de l\'article avec suffisamment de texte pour passer validation.',
                'image' => 'https://example.com/new-image.jpg',
                'status' => 'published',
            ];

            // Act : Soumettre mise à jour
            /**
            * $this->put($url, $data) : Simule requête PUT
            * 
            * Équivaut à formulaire HTML :
            * <form method="POST">
            *     @method('PUT')
            *     ...
            * </form>
            */
            $response = $this->actingAs($author)
                ->put('/posts/' . $post->slug, $updatedData);

            // Assert : Vérifier mise à jour BDD
            $this->assertDatabaseHas('posts', [
                'id' => $post->id,
                'title' => 'Titre Modifié',
                'content' => 'Contenu modifié de l\'article avec suffisamment de texte pour passer validation.',
            ]);

            // Assert : Vérifier redirection
            /**
            * $post->fresh()->slug : Recharge post depuis BDD
            * Slug peut avoir changé si titre modifié
            */
            $response->assertRedirect('/posts/' . $post->fresh()->slug);

            // Assert : Vérifier message succès
            $response->assertSessionHas('success');
        }

        /**
        * Test : Suppression article nécessite être l'auteur
        * 
        * Vérifie :
        * - Auteur article : suppression réussie (BDD)
        * - Autre utilisateur : erreur 403
        * - Redirection dashboard après suppression
        */
        public function test_only_author_can_delete_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Autre utilisateur tente supprimer → 403
            $response = $this->actingAs($otherUser)
                ->delete('/posts/' . $post->slug);
            $response->assertStatus(403);

            // Assert : Article toujours en BDD
            $this->assertDatabaseHas('posts', ['id' => $post->id]);

            // Act : Auteur supprime article
            $response = $this->actingAs($author)
                ->delete('/posts/' . $post->slug);

            // Assert : Article supprimé de BDD
            /**
            * assertDatabaseMissing() : Vérifie ABSENCE enregistrement
            */
            $this->assertDatabaseMissing('posts', ['id' => $post->id]);

            // Assert : Redirection dashboard
            $response->assertRedirect('/dashboard');

            // Assert : Message succès
            $response->assertSessionHas('success');
        }
    }
    ```

=== "**Tableau Récapitulatif Tests Feature**"

    | Test | Objectif | Assertions Clés |
    |------|----------|----------------|
    | `test_home_page_is_accessible` | Route / fonctionne | `assertStatus(200)`, `assertSee()` |
    | `test_published_posts_are_displayed` | Articles publiés visibles | `assertSee()`, `assertDontSee()` |
    | `test_pagination_works_correctly` | Pagination 9/page | `assertViewHas()`, `assertEquals()` |
    | `test_sidebar_displays_categories` | Catégories + compteurs | `assertSee()` (noms + nombres) |
    | `test_popular_posts_are_displayed` | Top 3 vues affiché | `assertSee()`, `assertDontSee()` |
    | `test_published_post_is_accessible` | Page article accessible | `assertStatus(200)`, `assertSee()` |
    | `test_draft_post_not_accessible` | Brouillons privés | `assertStatus(404/200)` selon user |
    | `test_post_views_count_incremented` | Compteur vues incrémenté | `assertEquals()`, `fresh()` |
    | `test_create_post_requires_auth` | Création nécessite login | `assertRedirect('/login')` |
    | `test_authenticated_user_can_create` | Création fonctionnelle | `assertDatabaseHas()`, `assertRedirect()` |
    | `test_create_validation_fails` | Validation formulaire | `assertSessionHasErrors()` |
    | `test_only_author_can_edit` | Édition réservée auteur | `assertStatus(403/200)` |
    | `test_author_can_update` | Mise à jour fonctionnelle | `assertDatabaseHas()` (données modifiées) |
    | `test_only_author_can_delete` | Suppression réservée auteur | `assertDatabaseMissing()` |

=== "**Exécuter les tests**"

    ```bash
    # Tous les tests
    php artisan test

    # Seulement HomeControllerTest
    php artisan test --filter=HomeControllerTest

    # Seulement PostControllerTest
    php artisan test --filter=PostControllerTest

    # Avec détails (verbose)
    php artisan test -v

    # Avec temps d'exécution
    php artisan test --profile
    ```

    **Résultat attendu :**

    ```
    PASS  Tests\Feature\HomeControllerTest
    ✓ home page is accessible (0.05s)
    ✓ published posts are displayed (0.08s)
    ✓ pagination works correctly (0.12s)
    ✓ sidebar displays categories with counts (0.09s)
    ✓ popular posts are displayed (0.10s)

    PASS  Tests\Feature\PostControllerTest
    ✓ published post is accessible (0.06s)
    ✓ draft post not accessible to public (0.11s)
    ✓ post views count is incremented (0.07s)
    ✓ create post requires authentication (0.05s)
    ✓ authenticated user can create post (0.13s)
    ✓ create post validation fails with invalid data (0.08s)
    ✓ only author can edit post (0.10s)
    ✓ author can update post (0.14s)
    ✓ only author can delete post (0.12s)

    Tests:    14 passed (19 assertions)
    Duration: 1.10s
    ```

✅ **Étape 7.1 Terminée !**

**Fichiers créés :**

- `tests/Feature/HomeControllerTest.php` : 5 tests page d'accueil
- `tests/Feature/PostControllerTest.php` : 9 tests CRUD articles

**Concepts maîtrisés :**

- RefreshDatabase trait (isolation tests)
- Factory Pattern (génération données tests)
- actingAs() (simulation authentification)
- assertStatus(), assertSee(), assertDontSee()
- assertDatabaseHas(), assertDatabaseMissing()
- assertRedirect(), assertSessionHas()
- assertViewHas(), viewData()
- fresh() (rechargement modèle depuis BDD)

### Étape 7.2 : Tests Unit (Modèles, Scopes et Helpers)

**Contexte :**

> Les **Tests Unit** testent des **unités de code isolées** : méthodes de modèles, scopes Eloquent, helpers personnalisés, calculs métier. Contrairement aux Feature Tests (bout en bout), les Unit Tests se concentrent sur une **fonction spécifique** sans dépendances externes.

!!! note "**Différences Unit vs Feature Tests :**"

    | Aspect | Tests Unit | Tests Feature |
    |--------|-----------|---------------|
    | **Portée** | Fonction isolée | Flux complet (HTTP → BDD) |
    | **Vitesse** | Ultra-rapide (<1ms) | Lent (50-200ms) |
    | **Dépendances** | Aucune (ou mockées) | Base données, routes, vues |
    | **Objectif** | Logique métier pure | Comportement utilisateur |
    | **Exemple** | `Post::generateSlug()` | `POST /posts → création BDD` |

**Avantages Tests Unit :**

- ✅ **Rapidité** : Exécution immédiate (pas de BDD, pas de HTTP)
- ✅ **Précision** : Localise bugs dans méthode spécifique
- ✅ **Refactoring** : Vérifie logique pure indépendamment du reste
- ✅ **Documentation** : Montre usage exact d'une méthode

**Structure Tests Unit Laravel :**

```php
class PostTest extends TestCase
{
    // Pas de RefreshDatabase (pas de BDD nécessaire)
    // Tests méthodes isolées du modèle Post
    
    public function test_slug_is_generated_correctly(): void
    {
        // Tester uniquement la génération de slug
        // Sans créer en BDD
    }
}
```

??? abstract "7.2.1 : Tests Unit - Modèle Post (Méthodes et Scopes)"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test PostTest --unit
    ```

    !!! note "**Flag `--unit` :**"
        Place le fichier dans `tests/Unit/` au lieu de `tests/Feature/`

    **Éditer `tests/Unit/PostTest.php` :**

    ```php title="Fichier : tests/Unit/PostTest.php"
    <?php

    namespace Tests\Unit;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Unit : Modèle Post
     * 
     * Teste les méthodes et scopes du modèle Post
     * - Génération slug automatique
     * - Scope published()
     * - Incrément views
     * - Relations Eloquent
     */
    class PostTest extends TestCase
    {
        /**
         * RefreshDatabase : Nécessaire ici car on teste relations Eloquent
         * 
         * Note : Certains tests unit peuvent se passer de BDD
         * Ici, on teste des méthodes qui interagissent avec BDD (scopes, relations)
         */
        use RefreshDatabase;

        /**
         * Test : Génération automatique du slug lors de la création
         * 
         * Vérifie :
         * - Slug généré à partir du titre
         * - Slug formaté en kebab-case
         * - Événement creating() déclenché correctement
         */
        public function test_slug_is_generated_automatically_on_create(): void
        {
            // Arrange : Créer utilisateur et catégorie
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Act : Créer article SANS spécifier slug
            /**
             * Note : slug n'est PAS fourni dans le tableau
             * Il doit être généré automatiquement par événement creating()
             */
            $post = Post::create([
                'title' => 'Mon Article de Test',
                'excerpt' => 'Résumé du test.',
                'content' => 'Contenu complet de l\'article de test avec suffisamment de caractères pour passer validation.',
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier slug généré correctement
            /**
             * "Mon Article de Test" doit devenir "mon-article-de-test"
             * 
             * Transformations attendues :
             * - Majuscules → minuscules
             * - Espaces → tirets
             * - Accents préservés ou supprimés (selon implémentation)
             */
            $this->assertEquals('mon-article-de-test', $post->slug);

            // Assert : Vérifier unicité du slug
            $this->assertNotNull($post->slug);
            $this->assertIsString($post->slug);
        }

        /**
         * Test : Gestion des slugs dupliqués (unicité)
         * 
         * Vérifie :
         * - Si titre identique, slug doit avoir suffixe numérique
         * - Slug1 : "mon-article"
         * - Slug2 : "mon-article-2"
         */
        public function test_duplicate_slugs_are_handled(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Act : Créer premier article
            $post1 = Post::factory()->create([
                'title' => 'Titre Identique',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Créer deuxième article avec même titre
            $post2 = Post::factory()->create([
                'title' => 'Titre Identique',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier slugs différents
            /**
             * $post1->slug : "titre-identique"
             * $post2->slug : "titre-identique-2" (suffixe ajouté)
             */
            $this->assertNotEquals($post1->slug, $post2->slug);
            
            /**
             * Vérifier format slug2 : doit contenir slug1 + suffixe
             */
            $this->assertStringStartsWith($post1->slug, $post2->slug);
            
            /**
             * Alternative : Vérifier que slug2 matche pattern "titre-identique-N"
             */
            $this->assertMatchesRegularExpression('/^titre-identique-\d+$/', $post2->slug);
        }

        /**
         * Test : Scope published() filtre correctement
         * 
         * Vérifie :
         * - Scope retourne seulement articles publiés
         * - Status 'published' AND published_at <= NOW()
         * - Exclut brouillons et articles futurs
         */
        public function test_published_scope_filters_correctly(): void
        {
            // Arrange : Créer utilisateur et catégorie
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer article publié (DOIT apparaître)
            $publishedPost = Post::factory()->create([
                'title' => 'Article Publié',
                'status' => 'published',
                'published_at' => now()->subDay(), // Hier
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer brouillon (NE DOIT PAS apparaître)
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon',
                'status' => 'draft',
                'published_at' => null,
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer article futur (NE DOIT PAS apparaître)
            $futurePost = Post::factory()->create([
                'title' => 'Article Futur',
                'status' => 'published',
                'published_at' => now()->addDay(), // Demain
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Récupérer articles avec scope published()
            /**
             * Post::published() appelle scopePublished() du modèle
             * 
             * Équivaut à :
             * Post::where('status', 'published')
             *     ->where('published_at', '<=', now())
             *     ->get()
             */
            $publishedPosts = Post::published()->get();

            // Assert : Vérifier filtrage correct
            /**
             * count() : Doit retourner 1 (seulement article publié)
             */
            $this->assertCount(1, $publishedPosts);

            /**
             * contains() : Vérifie présence article publié
             */
            $this->assertTrue($publishedPosts->contains($publishedPost));

            /**
             * Vérifier ABSENCE brouillon et article futur
             */
            $this->assertFalse($publishedPosts->contains($draftPost));
            $this->assertFalse($publishedPosts->contains($futurePost));
        }

        /**
         * Test : Méthode incrementViews() incrémente compteur
         * 
         * Vérifie :
         * - views_count incrémenté de 1
         * - Méthode thread-safe (évite race conditions)
         * - Sauvegarde automatique en BDD
         */
        public function test_increment_views_increases_counter(): void
        {
            // Arrange : Créer article avec 0 vues
            $user = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'views_count' => 0,
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier valeur initiale
            $this->assertEquals(0, $post->views_count);

            // Act : Incrémenter vues
            /**
             * incrementViews() : Méthode personnalisée du modèle Post
             * 
             * Implémentation attendue :
             * public function incrementViews()
             * {
             *     $this->increment('views_count');
             * }
             */
            $post->incrementViews();

            // Assert : Vérifier incrément (+1)
            /**
             * fresh() : Recharge depuis BDD
             * Vérifie que increment() a bien sauvegardé
             */
            $this->assertEquals(1, $post->fresh()->views_count);

            // Act : Incrémenter à nouveau
            $post->incrementViews();

            // Assert : Vérifier nouvel incrément (+1, total = 2)
            $this->assertEquals(2, $post->fresh()->views_count);
        }

        /**
         * Test : Méthode isDraft() détecte brouillons
         * 
         * Vérifie :
         * - isDraft() retourne true si status = 'draft'
         * - isDraft() retourne false si status = 'published'
         */
        public function test_is_draft_method_works_correctly(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer brouillon
            $draftPost = Post::factory()->create([
                'status' => 'draft',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer article publié
            $publishedPost = Post::factory()->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier isDraft()
            /**
             * isDraft() : Méthode personnalisée du modèle Post
             * 
             * Implémentation attendue :
             * public function isDraft(): bool
             * {
             *     return $this->status === 'draft';
             * }
             */
            $this->assertTrue($draftPost->isDraft());
            $this->assertFalse($publishedPost->isDraft());
        }

        /**
         * Test : Relation belongsTo avec User (auteur)
         * 
         * Vérifie :
         * - Relation user chargée correctement
         * - Attribut user_id correspond à user->id
         */
        public function test_belongs_to_user_relationship(): void
        {
            // Arrange
            $user = User::factory()->create(['name' => 'Alice Dupont']);
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation user
            /**
             * $post->user : Appelle méthode user() du modèle Post
             * 
             * public function user()
             * {
             *     return $this->belongsTo(User::class);
             * }
             */
            $postUser = $post->user;

            // Assert : Vérifier relation
            /**
             * assertInstanceOf() : Vérifie type objet
             */
            $this->assertInstanceOf(User::class, $postUser);

            /**
             * Vérifier ID correspondant
             */
            $this->assertEquals($user->id, $postUser->id);

            /**
             * Vérifier attribut name
             */
            $this->assertEquals('Alice Dupont', $postUser->name);
        }

        /**
         * Test : Relation belongsTo avec Category
         * 
         * Vérifie :
         * - Relation category chargée correctement
         * - Attribut category_id correspond à category->id
         */
        public function test_belongs_to_category_relationship(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create(['name' => 'Technologie']);

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation category
            $postCategory = $post->category;

            // Assert : Vérifier relation
            $this->assertInstanceOf(Category::class, $postCategory);
            $this->assertEquals($category->id, $postCategory->id);
            $this->assertEquals('Technologie', $postCategory->name);
        }

        /**
         * Test : Relation hasMany avec Comments
         * 
         * Vérifie :
         * - Relation comments retourne Collection
         * - Commentaires liés à l'article
         */
        public function test_has_many_comments_relationship(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer 3 commentaires pour cet article
            /**
             * Comment::factory()->count(3)->create() nécessite CommentFactory
             * 
             * Alternative manuelle :
             * for ($i = 0; $i < 3; $i++) {
             *     Comment::create([...]);
             * }
             */
            $post->comments()->createMany([
                [
                    'author_name' => 'Visiteur 1',
                    'author_email' => 'visiteur1@example.com',
                    'content' => 'Premier commentaire.',
                    'approved' => true,
                ],
                [
                    'author_name' => 'Visiteur 2',
                    'author_email' => 'visiteur2@example.com',
                    'content' => 'Deuxième commentaire.',
                    'approved' => true,
                ],
                [
                    'author_name' => 'Visiteur 3',
                    'author_email' => 'visiteur3@example.com',
                    'content' => 'Troisième commentaire.',
                    'approved' => false, // Non approuvé
                ],
            ]);

            // Act : Charger tous les commentaires
            $comments = $post->comments;

            // Assert : Vérifier relation
            /**
             * assertCount(3) : Vérifie nombre éléments Collection
             */
            $this->assertCount(3, $comments);

            /**
             * Vérifier type Collection
             */
            $this->assertInstanceOf(\Illuminate\Database\Eloquent\Collection::class, $comments);

            /**
             * Vérifier tous commentaires liés au post
             */
            foreach ($comments as $comment) {
                $this->assertEquals($post->id, $comment->post_id);
            }
        }

        /**
         * Test : Cast attribut published_at en Carbon
         * 
         * Vérifie :
         * - published_at retourné comme instance Carbon
         * - Méthodes Carbon accessibles (format, diffForHumans)
         */
        public function test_published_at_is_cast_to_carbon(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'published_at' => '2024-01-15 10:30:00',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier cast Carbon
            /**
             * assertInstanceOf() : Vérifie type objet
             */
            $this->assertInstanceOf(\Illuminate\Support\Carbon::class, $post->published_at);

            /**
             * Vérifier méthodes Carbon fonctionnent
             */
            $formattedDate = $post->published_at->format('Y-m-d');
            $this->assertEquals('2024-01-15', $formattedDate);

            /**
             * Vérifier diffForHumans() disponible
             */
            $this->assertIsString($post->published_at->diffForHumans());
        }
    }
    ```

??? abstract "7.2.2 : Tests Unit - Modèle User (Méthodes)"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test UserTest --unit
    ```

    **Éditer `tests/Unit/UserTest.php` :**

    ```php title="Fichier : tests/Unit/UserTest.php"
    <?php

    namespace Tests\Unit;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Support\Facades\Hash;
    use Tests\TestCase;

    /**
     * Tests Unit : Modèle User
     * 
     * Teste les méthodes et relations du modèle User
     */
    class UserTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * Test : Relation hasMany avec Posts
         * 
         * Vérifie :
         * - Utilisateur a plusieurs articles
         * - Relation chargée correctement
         */
        public function test_user_has_many_posts(): void
        {
            // Arrange : Créer utilisateur
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer 3 articles pour cet utilisateur
            Post::factory()->count(3)->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation posts
            $userPosts = $user->posts;

            // Assert : Vérifier relation
            $this->assertCount(3, $userPosts);
            $this->assertInstanceOf(\Illuminate\Database\Eloquent\Collection::class, $userPosts);

            /**
             * Vérifier tous articles appartiennent à l'utilisateur
             */
            foreach ($userPosts as $post) {
                $this->assertEquals($user->id, $post->user_id);
            }
        }

        /**
         * Test : Password hashé automatiquement
         * 
         * Vérifie :
         * - Attribut password hashé via mutator
         * - Hash vérifié avec Hash::check()
         */
        public function test_password_is_hashed_automatically(): void
        {
            // Arrange : Créer utilisateur avec password en clair
            /**
             * Factory UserFactory hash automatiquement le password
             * Ici on teste le mutator setPasswordAttribute() du modèle
             */
            $user = User::factory()->create([
                'password' => 'plaintext-password',
            ]);

            // Assert : Vérifier password hashé en BDD
            /**
             * Password ne doit PAS être stocké en clair
             */
            $this->assertNotEquals('plaintext-password', $user->password);

            /**
             * Vérifier hash bcrypt (commence par $2y$)
             */
            $this->assertStringStartsWith('$2y$', $user->password);

            /**
             * Vérifier Hash::check() valide le password
             */
            $this->assertTrue(Hash::check('plaintext-password', $user->password));
        }

        /**
         * Test : Attribut email unique (contrainte BDD)
         * 
         * Vérifie :
         * - Duplication email provoque exception
         */
        public function test_email_must_be_unique(): void
        {
            // Arrange : Créer premier utilisateur
            User::factory()->create([
                'email' => 'alice@example.com',
            ]);

            // Act & Assert : Tenter créer second utilisateur avec même email
            /**
             * expectException() : Attend exception spécifique
             * 
             * QueryException : Exception MySQL/PostgreSQL pour violations contraintes
             */
            $this->expectException(\Illuminate\Database\QueryException::class);

            /**
             * Création doit échouer (email dupliqué)
             */
            User::factory()->create([
                'email' => 'alice@example.com',
            ]);
        }

        /**
         * Test : Cast email_verified_at en Carbon
         * 
         * Vérifie :
         * - email_verified_at retourné comme instance Carbon
         */
        public function test_email_verified_at_is_cast_to_carbon(): void
        {
            // Arrange : Créer utilisateur avec email vérifié
            $user = User::factory()->create([
                'email_verified_at' => now(),
            ]);

            // Assert : Vérifier cast Carbon
            $this->assertInstanceOf(\Illuminate\Support\Carbon::class, $user->email_verified_at);

            /**
             * Vérifier méthodes Carbon disponibles
             */
            $this->assertIsString($user->email_verified_at->format('Y-m-d'));
        }

        /**
         * Test : Attributs fillable protègent mass assignment
         * 
         * Vérifie :
         * - Seuls attributs fillable peuvent être assignés en masse
         * - Attribut password protégé (hors fillable si non défini)
         */
        public function test_fillable_attributes_protect_mass_assignment(): void
        {
            // Arrange : Données utilisateur avec attribut non autorisé
            $userData = [
                'name' => 'Test User',
                'email' => 'test@example.com',
                'password' => bcrypt('password'),
                'is_admin' => true, // Hypothétique attribut non fillable
            ];

            // Act : Créer utilisateur via mass assignment
            /**
             * User::create() utilise $fillable du modèle
             * Attributs non listés dans $fillable sont ignorés
             */
            $user = User::create($userData);

            // Assert : Vérifier attributs fillable assignés
            $this->assertEquals('Test User', $user->name);
            $this->assertEquals('test@example.com', $user->email);

            /**
             * Vérifier attribut non fillable ignoré
             * 
             * Note : is_admin n'existe pas dans User par défaut
             * Cet exemple montre le principe de protection
             */
            // $this->assertNull($user->is_admin);
        }
    }
    ```

??? abstract "7.2.3 : Tests Unit - Helper Str::slug() (Validation)"

    **Test intégré dans PostTest :**

    Ce test vérifie que la génération de slug utilise correctement le helper Laravel `Str::slug()`.

    **Ajouter dans `tests/Unit/PostTest.php` :**

    ```php
    /**
     * Test : Génération slug gère caractères spéciaux
     * 
     * Vérifie :
     * - Accents convertis ou supprimés
     * - Caractères spéciaux supprimés
     * - Espaces multiples réduits à un tiret
     */
    public function test_slug_handles_special_characters(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act : Créer article avec titre complexe
        $post = Post::factory()->create([
            'title' => 'Article avec Accents ÉÈÊ & Symboles @#$ !!!',
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Assert : Vérifier slug nettoyé
        /**
         * Str::slug() Laravel transforme :
         * - Accents → caractères ASCII (É → e)
         * - Espaces → tirets
         * - Symboles → supprimés
         * - Tout en minuscules
         */
        $expectedSlug = 'article-avec-accents-eee-symboles';
        
        /**
         * assertMatchesRegularExpression() : Vérifie pattern regex
         * 
         * Pattern attendu : lettres minuscules + tirets uniquement
         */
        $this->assertMatchesRegularExpression('/^[a-z0-9-]+$/', $post->slug);
        
        /**
         * Vérifier slug ne contient pas caractères spéciaux
         */
        $this->assertStringNotContainsString('&', $post->slug);
        $this->assertStringNotContainsString('@', $post->slug);
        $this->assertStringNotContainsString('!', $post->slug);
    }

    /**
     * Test : Slug vide/null généré depuis titre par défaut
     * 
     * Vérifie :
     * - Si slug non fourni, généré depuis titre
     * - Événement creating() déclenché
     */
    public function test_empty_slug_is_generated_from_title(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act : Créer article SANS slug explicite
        $post = Post::factory()->create([
            'title' => 'Titre Sans Slug Explicite',
            'slug' => null, // Explicitement null
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Assert : Vérifier slug généré automatiquement
        $this->assertNotNull($post->slug);
        $this->assertEquals('titre-sans-slug-explicite', $post->slug);
    }
    ```

=== "**Tableau Récapitulatif Tests Unit**"

    | Test | Modèle | Objectif | Assertions Clés |
    |------|--------|----------|-----------------|
    | `test_slug_is_generated_automatically` | Post | Slug auto depuis titre | `assertEquals()` |
    | `test_duplicate_slugs_are_handled` | Post | Slugs uniques (suffixes) | `assertNotEquals()`, regex |
    | `test_published_scope_filters` | Post | Scope published() filtre | `assertCount()`, `contains()` |
    | `test_increment_views_increases` | Post | Incrément views_count | `assertEquals()`, `fresh()` |
    | `test_is_draft_method_works` | Post | isDraft() détection | `assertTrue()`, `assertFalse()` |
    | `test_belongs_to_user_relationship` | Post | Relation belongsTo User | `assertInstanceOf()` |
    | `test_belongs_to_category` | Post | Relation belongsTo Category | `assertInstanceOf()` |
    | `test_has_many_comments` | Post | Relation hasMany Comments | `assertCount()` |
    | `test_published_at_cast_carbon` | Post | Cast Carbon published_at | `assertInstanceOf()` |
    | `test_slug_handles_special_chars` | Post | Slug caractères spéciaux | `assertMatchesRegularExpression()` |
    | `test_user_has_many_posts` | User | Relation hasMany Posts | `assertCount()` |
    | `test_password_is_hashed` | User | Mutator password hash | `Hash::check()` |
    | `test_email_must_be_unique` | User | Contrainte unique email | `expectException()` |
    | `test_email_verified_at_cast` | User | Cast Carbon email_verified_at | `assertInstanceOf()` |

=== "**Exécuter les tests Unit**"

    ```bash
    # Tous les tests Unit
    php artisan test --testsuite=Unit

    # Test spécifique
    php artisan test --filter=PostTest

    # Test spécifique avec méthode
    php artisan test --filter=PostTest::test_slug_is_generated_automatically

    # Avec détails
    php artisan test --testsuite=Unit -v

    # Avec temps d'exécution
    php artisan test --testsuite=Unit --profile
    ```

    **Résultat attendu :**

    ```
    PASS  Tests\Unit\PostTest
    ✓ slug is generated automatically on create (0.03s)
    ✓ duplicate slugs are handled (0.04s)
    ✓ published scope filters correctly (0.05s)
    ✓ increment views increases counter (0.03s)
    ✓ is draft method works correctly (0.04s)
    ✓ belongs to user relationship (0.03s)
    ✓ belongs to category relationship (0.03s)
    ✓ has many comments relationship (0.05s)
    ✓ published at is cast to carbon (0.02s)
    ✓ slug handles special characters (0.03s)
    ✓ empty slug is generated from title (0.03s)

    PASS  Tests\Unit\UserTest
    ✓ user has many posts (0.04s)
    ✓ password is hashed automatically (0.02s)
    ✓ email must be unique (0.03s)
    ✓ email verified at is cast to carbon (0.02s)

    Tests:    15 passed (32 assertions)
    Duration: 0.38s
    ```

!!! note "**Différence vitesse Unit vs Feature :**"
    - Feature Tests : 1.10s pour 14 tests (HTTP + BDD)
    - Unit Tests : 0.38s pour 15 tests (logique pure)
    - **× 3 plus rapide** malgré plus de tests !

✅ **Étape 7.2 Terminée !**

**Fichiers créés :**

- `tests/Unit/PostTest.php` : 11 tests modèle Post
- `tests/Unit/UserTest.php` : 4 tests modèle User

**Concepts maîtrisés :**

- Tests méthodes modèles (isDraft, incrementViews)
- Tests scopes Eloquent (published)
- Tests relations (belongsTo, hasMany)
- Tests casts (Carbon, Hash)
- Tests génération slug (Str::slug)
- Tests contraintes BDD (unique)
- assertInstanceOf(), assertCount()
- assertMatchesRegularExpression()
- expectException()

### Étape 7.3 : Optimisation Performance

**Contexte :**

> L'optimisation performance transforme une application "fonctionnelle" en application **production-ready**. Un blog avec 1000 articles peut afficher des temps de réponse de **5 secondes** sans optimisation, contre **200ms** après optimisation. La différence entre abandon utilisateur et expérience fluide.

!!! note "**Impact performance sur business :**"

    - ✅ **SEO** : Google pénalise sites lents (-50% trafic si >3s)
    - ✅ **Conversion** : Chaque 100ms perdue = -1% conversion
    - ✅ **UX** : 53% utilisateurs abandonnent si >3s chargement
    - ✅ **Coûts** : Moins de ressources serveur nécessaires

**Les 5 piliers de l'optimisation Laravel :**

1. **Base de données** : Indexes, requêtes optimisées, Eager Loading
2. **Cache** : Views, routes, config, données métier
3. **Assets** : Minification, compression, CDN
4. **Configuration** : Mode production, autoloading optimisé
5. **Monitoring** : Identifier goulots d'étranglement

**Méthodologie d'optimisation :**

```
1. Mesurer (baseline) → 2. Identifier bottlenecks → 3. Optimiser → 4. Re-mesurer → 5. Répéter
```

??? abstract "7.3.1 : Optimisation Base de Données (Indexes)"

    **Contexte :**

    > Les **indexes** sont des structures de données qui accélèrent les requêtes SQL. Sans index, MySQL doit scanner **toute la table** (full table scan). Avec index, recherche devient logarithmique O(log n) au lieu de linéaire O(n).

    !!! note "**Exemple impact index :**"
        Table 100 000 articles sans index : **500ms**  
        Table 100 000 articles avec index : **5ms**  
        **× 100 plus rapide**

    **Règle d'or indexation :**

    > Indexer toutes colonnes utilisées dans `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`

    **Créer une migration d'indexes :**

    ```bash
    php artisan make:migration add_indexes_to_posts_table
    ```

    **Éditer `database/migrations/XXXX_XX_XX_add_indexes_to_posts_table.php` :**

    ```php title="Fichier : database/migrations/XXXX_XX_XX_add_indexes_to_posts_table.php"
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    return new class extends Migration
    {
        /**
         * Ajout des indexes pour optimisation performance
         * 
         * Indexes créés :
         * - posts.status (WHERE status = 'published')
         * - posts.published_at (WHERE published_at <= NOW())
         * - posts.slug (WHERE slug = '...' - Route Model Binding)
         * - posts.user_id (JOIN users ON posts.user_id = users.id)
         * - posts.category_id (JOIN categories ON posts.category_id = categories.id)
         * - posts.views_count (ORDER BY views_count DESC)
         * 
         * Index composite :
         * - (status, published_at) : Optimise scope published()
         */
        public function up(): void
        {
            Schema::table('posts', function (Blueprint $table) {
                /**
                 * INDEX SIMPLE : status
                 * 
                 * Utilisé dans :
                 * - Post::where('status', 'published')->get()
                 * - Scope published() : WHERE status = 'published'
                 * 
                 * Impact : × 50 plus rapide sur table 10k lignes
                 * 
                 * Note : Index ENUM (status) très efficace car peu de valeurs distinctes
                 */
                $table->index('status', 'idx_posts_status');

                /**
                 * INDEX SIMPLE : published_at
                 * 
                 * Utilisé dans :
                 * - WHERE published_at <= NOW()
                 * - ORDER BY published_at DESC
                 * 
                 * Impact : × 30 plus rapide pour tri chronologique
                 */
                $table->index('published_at', 'idx_posts_published_at');

                /**
                 * INDEX UNIQUE : slug
                 * 
                 * Utilisé dans :
                 * - Route Model Binding : WHERE slug = '...'
                 * - Vérification unicité slug
                 * 
                 * UNIQUE : Empêche duplicatas + optimise recherches
                 * 
                 * Impact : × 100 plus rapide (hash index pour égalité stricte)
                 * 
                 * Note : slug déjà indexé par défaut via unique() dans migration
                 * Cette ligne redondante mais explicite (documentation)
                 */
                // $table->unique('slug', 'idx_posts_slug_unique'); // Déjà existant

                /**
                 * INDEX FOREIGN KEY : user_id
                 * 
                 * Utilisé dans :
                 * - JOIN users ON posts.user_id = users.id
                 * - WHERE user_id = X (articles d'un auteur)
                 * 
                 * Impact : × 40 plus rapide pour relations belongsTo
                 * 
                 * Note : Clé étrangère crée automatiquement index dans MySQL/PostgreSQL
                 * Explicite ici pour compatibilité SQLite (pas d'index auto)
                 */
                // $table->index('user_id', 'idx_posts_user_id'); // Déjà via foreignId()

                /**
                 * INDEX FOREIGN KEY : category_id
                 * 
                 * Utilisé dans :
                 * - JOIN categories ON posts.category_id = categories.id
                 * - WHERE category_id = X (articles d'une catégorie)
                 */
                // $table->index('category_id', 'idx_posts_category_id'); // Déjà via foreignId()

                /**
                 * INDEX SIMPLE : views_count
                 * 
                 * Utilisé dans :
                 * - ORDER BY views_count DESC (articles populaires)
                 * - WHERE views_count > X (seuils popularité)
                 * 
                 * Impact : × 20 plus rapide pour tri par popularité
                 */
                $table->index('views_count', 'idx_posts_views_count');

                /**
                 * INDEX COMPOSITE : (status, published_at)
                 * 
                 * Utilisé dans :
                 * - Scope published() : WHERE status = 'published' AND published_at <= NOW()
                 * 
                 * Avantage index composite :
                 * MySQL utilise UN SEUL index au lieu de deux
                 * Condition AND optimisée (index covering query)
                 * 
                 * Impact : × 70 plus rapide que 2 index séparés
                 * 
                 * Ordre colonnes crucial :
                 * (status, published_at) : Optimal (status élimine 50% lignes d'abord)
                 * (published_at, status) : Moins optimal (dates moins sélectives)
                 * 
                 * Règle : Colonne la plus sélective EN PREMIER
                 */
                $table->index(['status', 'published_at'], 'idx_posts_status_published_at');
            });

            /**
             * Indexes pour table comments
             */
            Schema::table('comments', function (Blueprint $table) {
                /**
                 * INDEX : post_id
                 * 
                 * Utilisé dans :
                 * - $post->comments (relation hasMany)
                 * - WHERE post_id = X
                 */
                // $table->index('post_id', 'idx_comments_post_id'); // Déjà via foreignId()

                /**
                 * INDEX : approved
                 * 
                 * Utilisé dans :
                 * - WHERE approved = true (affichage publics)
                 * - Scope approved()
                 * 
                 * Impact : × 15 plus rapide pour filtrage modération
                 */
                $table->index('approved', 'idx_comments_approved');

                /**
                 * INDEX COMPOSITE : (post_id, approved)
                 * 
                 * Utilisé dans :
                 * - Commentaires approuvés d'un article
                 * - $post->comments()->where('approved', true)->get()
                 * 
                 * Impact : × 50 plus rapide que 2 index séparés
                 */
                $table->index(['post_id', 'approved'], 'idx_comments_post_approved');
            });

            /**
             * Indexes pour table categories
             */
            Schema::table('categories', function (Blueprint $table) {
                /**
                 * INDEX UNIQUE : slug
                 * 
                 * Utilisé dans :
                 * - Route Model Binding : WHERE slug = '...'
                 */
                // $table->unique('slug', 'idx_categories_slug_unique'); // Déjà existant
            });
        }

        /**
         * Supprimer les indexes (rollback)
         * 
         * Important : Supprimer dans ordre inverse de création
         */
        public function down(): void
        {
            Schema::table('posts', function (Blueprint $table) {
                // Supprimer index composite en premier
                $table->dropIndex('idx_posts_status_published_at');
                
                // Puis indexes simples
                $table->dropIndex('idx_posts_views_count');
                $table->dropIndex('idx_posts_published_at');
                $table->dropIndex('idx_posts_status');
            });

            Schema::table('comments', function (Blueprint $table) {
                $table->dropIndex('idx_comments_post_approved');
                $table->dropIndex('idx_comments_approved');
            });
        }
    };
    ```

    **Exécuter la migration :**

    ```bash
    php artisan migrate
    ```

    **Vérifier les indexes créés :**

    ```bash
    # MySQL
    php artisan tinker
    >>> DB::select('SHOW INDEX FROM posts');

    # Ou directement SQL
    mysql> SHOW INDEX FROM posts;
    ```

    !!! note "**Règles avancées indexation :**"
        
        **Quand créer index :**
        
        - ✅ Colonnes dans WHERE (80% des cas)
        - ✅ Colonnes dans JOIN (foreign keys)
        - ✅ Colonnes dans ORDER BY (tri)
        - ✅ Colonnes dans GROUP BY (agrégation)
        
        **Quand NE PAS créer index :**
        
        - ❌ Petites tables (<1000 lignes) : Full scan plus rapide
        - ❌ Colonnes mises à jour fréquemment : Index ralentit INSERT/UPDATE
        - ❌ Colonnes peu sélectives : ENUM avec 2 valeurs (true/false)
        - ❌ Trop d'indexes : Maximum 5-7 par table (balance lecture/écriture)

??? abstract "7.3.2 : Résolution Problème N+1 (Eager Loading)"

    **Contexte :**

    > Le **problème N+1** est le bug performance #1 des applications Laravel. Il survient quand on charge relations dans une boucle, générant **N requêtes SQL** au lieu d'une seule.

    !!! warning "**Exemple problème N+1 :**"
        ```php
        // Page d'accueil : 9 articles
        $posts = Post::all(); // 1 requête
        
        foreach ($posts as $post) {
            echo $post->user->name;     // 9 requêtes (1 par article)
            echo $post->category->name; // 9 requêtes (1 par article)
        }
        
        // Total : 1 + 9 + 9 = 19 requêtes SQL 😱
        ```

    **Solution : Eager Loading avec `with()`**

    **Vérifier tous les contrôleurs utilisent Eager Loading :**

    **Fichier : `app/Http/Controllers/HomeController.php`**

    ```php title="Fichier : app/Http/Controllers/HomeController.php"
    public function index()
    {
        /**
         * AVANT (N+1 problème) :
         * $posts = Post::published()->latest('published_at')->paginate(9);
         * 
         * Requêtes générées :
         * 1. SELECT * FROM posts WHERE status='published' AND published_at<=NOW() LIMIT 9
         * 2-10. SELECT * FROM users WHERE id=X (9 requêtes, 1 par article)
         * 11-19. SELECT * FROM categories WHERE id=X (9 requêtes, 1 par article)
         * 
         * Total : 19 requêtes
         */

        /**
         * APRÈS (Eager Loading) :
         * with(['user', 'category']) charge relations en 2 requêtes supplémentaires
         * 
         * Requêtes générées :
         * 1. SELECT * FROM posts WHERE status='published' AND published_at<=NOW() LIMIT 9
         * 2. SELECT * FROM users WHERE id IN (1, 2, 3, ...) (1 seule requête pour tous auteurs)
         * 3. SELECT * FROM categories WHERE id IN (1, 2, 3, ...) (1 seule requête pour toutes catégories)
         * 
         * Total : 3 requêtes (× 6 plus rapide)
         */
        $posts = Post::with(['user', 'category'])
            ->published()
            ->latest('published_at')
            ->paginate(9);

        /**
         * Catégories avec compteurs articles
         * withCount('posts') ajoute attribut virtuel posts_count
         * 
         * Requête générée :
         * SELECT categories.*, 
         *        (SELECT COUNT(*) FROM posts WHERE category_id = categories.id) as posts_count
         * FROM categories
         */
        $categories = Category::withCount('posts')->get();

        /**
         * Articles populaires (top 3 vues)
         * Eager Loading évite N+1 même pour 3 articles
         */
        $popularPosts = Post::with(['user', 'category'])
            ->published()
            ->orderBy('views_count', 'desc')
            ->limit(3)
            ->get();

        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
    ```

    **Fichier : `app/Http/Controllers/PostController.php`**

    ```php title="Fichier : app/Http/Controllers/PostController.php"
    public function show(Post $post)
    {
        /**
         * Eager Loading relations pour page article
         * 
         * Relations chargées :
         * - user : Auteur article (belongsTo)
         * - category : Catégorie article (belongsTo)
         * - comments : Commentaires approuvés (hasMany + scope)
         */
        $post->load([
            'user',
            'category',
            'comments' => function ($query) {
                /**
                 * Closure permet filtrage relation
                 * Charge seulement commentaires approuvés
                 */
                $query->where('approved', true)
                      ->latest()
                      ->with('post'); // Évite N+1 si commentaires affichent article
            }
        ]);

        // Contrôle d'accès brouillons
        if ($post->status === 'draft' && (!auth()->check() || auth()->id() !== $post->user_id)) {
            abort(404);
        }

        // Incrémenter compteur vues
        $post->incrementViews();

        /**
         * Articles similaires (même catégorie)
         * Eager Loading évite N+1 pour 3 articles similaires
         */
        $similarPosts = Post::with(['user', 'category'])
            ->where('category_id', $post->category_id)
            ->where('id', '!=', $post->id)
            ->published()
            ->latest('published_at')
            ->limit(3)
            ->get();

        return view('posts.show', compact('post', 'similarPosts'));
    }
    ```

    **Fichier : `app/Http/Controllers/CategoryController.php`**

    ```php title="Fichier : app/Http/Controllers/CategoryController.php"
    public function show(Category $category)
    {
        /**
         * Articles catégorie avec Eager Loading
         */
        $posts = $category->posts()
            ->with('user') // Charge auteurs (évite N+1)
            ->published()
            ->latest('published_at')
            ->paginate(9);

        return view('categories.show', compact('category', 'posts'));
    }
    ```

    **Fichier : `app/Http/Controllers/AuthorController.php`**

    ```php title="Fichier : app/Http/Controllers/AuthorController.php"
    public function show(User $user)
    {
        /**
         * Articles auteur avec Eager Loading
         */
        $posts = $user->posts()
            ->with('category') // Charge catégories (évite N+1)
            ->published()
            ->latest('published_at')
            ->paginate(6);

        /**
         * Statistiques publiques
         * 
         * withCount() évite N+1 pour compteurs
         */
        $stats = [
            'total_posts' => $user->posts()->published()->count(),
            'total_views' => $user->posts()->published()->sum('views_count'),
            'total_comments' => $user->posts()
                ->published()
                ->withCount('comments')
                ->get()
                ->sum('comments_count'),
        ];

        return view('authors.show', compact('user', 'posts', 'stats'));
    }
    ```

    **Fichier : `app/Http/Controllers/DashboardController.php`**

    ```php title="Fichier : app/Http/Controllers/DashboardController.php"
    public function index()
    {
        $user = auth()->user();

        /**
         * Tous articles auteur avec Eager Loading
         */
        $posts = Post::where('user_id', $user->id)
            ->with('category') // Évite N+1 pour affichage catégories
            ->latest()
            ->get();

        // Statistiques dashboard
        $stats = [
            'total_posts' => $posts->count(),
            'published_posts' => $posts->where('status', 'published')->count(),
            'draft_posts' => $posts->where('status', 'draft')->count(),
            'total_views' => $posts->sum('views_count'),
        ];

        /**
         * Article le plus populaire
         * Collection déjà chargée, pas de requête supplémentaire
         */
        $mostViewedPost = $posts->where('status', 'published')
            ->sortByDesc('views_count')
            ->first();

        return view('dashboard', compact('posts', 'stats', 'mostViewedPost'));
    }
    ```

    !!! note "**Techniques avancées Eager Loading :**"
        
        **1. Nested Eager Loading (relations imbriquées) :**
        ```php
        // Charger post → comments → user (auteur commentaire)
        $posts = Post::with(['comments.user'])->get();
        ```
        
        **2. Conditional Eager Loading :**
        ```php
        // Charger relation seulement si condition
        $posts = Post::with(['comments' => function ($query) {
            $query->where('approved', true)->latest();
        }])->get();
        ```
        
        **3. Lazy Eager Loading (charger après récupération) :**
        ```php
        $posts = Post::all();
        
        // Décider plus tard de charger relation
        if ($needUsers) {
            $posts->load('user');
        }
        ```
        
        **4. Load Missing (évite recharger) :**
        ```php
        // Charge seulement si pas déjà chargé
        $posts->loadMissing('user');
        ```

??? abstract "7.3.3 : Configuration Cache Laravel"

    **Contexte :**

    Laravel offre plusieurs niveaux de cache pour accélérer application. En production, **tous les caches doivent être activés**.

    !!! note "**Types de cache Laravel :**"
        
        1. **Config cache** : Fusionne tous fichiers config en 1 seul (bootstrap/cache/config.php)
        2. **Route cache** : Compile toutes routes en array PHP sérialisé
        3. **View cache** : Compile templates Blade en PHP pur
        4. **Event cache** : Cache listeners événements
        5. **Query cache** : Cache résultats requêtes BDD (manuel)

    **Commandes cache (à exécuter en production) :**

    **Créer un script de déploiement :**

    **Fichier : `scripts/optimize-production.sh`**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT OPTIMISATION PRODUCTION LARAVEL
    ###############################################################################
    # 
    # Usage : bash scripts/optimize-production.sh
    # 
    # Ce script :
    # 1. Clear tous les caches existants
    # 2. Recompile caches optimisés
    # 3. Optimise autoloader Composer
    # 4. Vérifie configuration production
    #
    ###############################################################################

    echo "🚀 Optimisation Laravel pour production..."

    ###############################################################################
    # ÉTAPE 1 : CLEAR CACHES EXISTANTS
    ###############################################################################
    echo ""
    echo "📦 Nettoyage caches existants..."

    # Clear application cache (Cache facade)
    php artisan cache:clear

    # Clear config cache
    php artisan config:clear

    # Clear route cache
    php artisan route:clear

    # Clear view cache (Blade templates compilés)
    php artisan view:clear

    # Clear event cache
    php artisan event:clear

    echo "✅ Caches nettoyés"

    ###############################################################################
    # ÉTAPE 2 : RECOMPILER CACHES OPTIMISÉS
    ###############################################################################
    echo ""
    echo "⚡ Compilation caches optimisés..."

    # Config cache : Fusionne tous config/*.php en 1 fichier
    # Impact : × 3 plus rapide chargement config
    # Fichier généré : bootstrap/cache/config.php
    php artisan config:cache

    # Route cache : Compile routes/web.php + api.php en array PHP
    # Impact : × 10 plus rapide résolution routes
    # Fichier généré : bootstrap/cache/routes-v7.php
    # 
    # ATTENTION : Désactive route closures (utiliser seulement contrôleurs)
    php artisan route:cache

    # View cache : Compile tous .blade.php en PHP pur
    # Impact : × 5 plus rapide rendu vues
    # Dossier : storage/framework/views/
    php artisan view:cache

    # Event cache : Cache listeners événements
    # Impact : × 2 plus rapide dispatch events
    php artisan event:cache

    echo "✅ Caches optimisés créés"

    ###############################################################################
    # ÉTAPE 3 : OPTIMISER AUTOLOADER COMPOSER
    ###############################################################################
    echo ""
    echo "📚 Optimisation autoloader Composer..."

    # Génère classmap optimisé (toutes classes mappées)
    # Impact : × 4 plus rapide chargement classes
    # Fichiers générés : vendor/composer/autoload_*.php
    composer install --optimize-autoloader --no-dev

    echo "✅ Autoloader optimisé"

    ###############################################################################
    # ÉTAPE 4 : VÉRIFICATION CONFIGURATION PRODUCTION
    ###############################################################################
    echo ""
    echo "🔍 Vérification configuration production..."

    # Vérifier APP_ENV=production
    if grep -q "APP_ENV=production" .env; then
        echo "✅ APP_ENV=production"
    else
        echo "⚠️  ATTENTION : APP_ENV n'est pas 'production'"
    fi

    # Vérifier APP_DEBUG=false
    if grep -q "APP_DEBUG=false" .env; then
        echo "✅ APP_DEBUG=false"
    else
        echo "⚠️  ATTENTION : APP_DEBUG devrait être 'false' en production"
    fi

    # Vérifier APP_KEY défini
    if grep -q "APP_KEY=base64:" .env; then
        echo "✅ APP_KEY défini"
    else
        echo "❌ ERREUR : APP_KEY non défini ! Exécuter : php artisan key:generate"
    fi

    ###############################################################################
    # RÉSUMÉ
    ###############################################################################
    echo ""
    echo "✅ Optimisation terminée !"
    echo ""
    echo "Fichiers générés :"
    echo "  - bootstrap/cache/config.php"
    echo "  - bootstrap/cache/routes-v7.php"
    echo "  - storage/framework/views/*.php"
    echo "  - vendor/composer/autoload_*.php"
    echo ""
    echo "⚡ Application optimisée pour production"
    ```

    **Rendre le script exécutable :**

    ```bash
    chmod +x scripts/optimize-production.sh
    ```

    **Exécuter l'optimisation :**

    ```bash
    bash scripts/optimize-production.sh
    ```

    !!! warning "**IMPORTANT : Route Cache et Closures**"
        
        `php artisan route:cache` **désactive** les closures dans routes.
        
        **Interdit en production :**
        ```php
        // routes/web.php
        Route::get('/', function () {
            return view('home');
        }); // ❌ Closure non supportée avec route:cache
        ```
        
        **Autorisé en production :**
        ```php
        // routes/web.php
        Route::get('/', [HomeController::class, 'index']); // ✅ Contrôleur supporté
        ```
        
        Toutes nos routes utilisent déjà des contrôleurs → Compatible route:cache ✅

    **Cache données métier (manuel) :**

    **Exemple : Cache sidebar catégories (rarement modifiées)**

    **Fichier : `app/Http/Controllers/HomeController.php`**

    ```php
    use Illuminate\Support\Facades\Cache;

    public function index()
    {
        $posts = Post::with(['user', 'category'])
            ->published()
            ->latest('published_at')
            ->paginate(9);

        /**
         * Cache catégories 24 heures
         * 
         * Cache::remember($key, $ttl, $callback) :
         * - Si clé existe : Retourne valeur en cache
         * - Si clé n'existe pas : Exécute callback + met en cache
         * 
         * TTL : 60 * 24 = 1440 minutes = 24 heures
         * 
         * Impact : × 50 plus rapide (évite requête BDD + calcul withCount)
         */
        $categories = Cache::remember('sidebar_categories', 60 * 24, function () {
            return Category::withCount('posts')->get();
        });

        /**
         * Cache articles populaires 1 heure
         * 
         * TTL : 60 minutes = 1 heure
         * Mis à jour fréquemment car views_count change souvent
         */
        $popularPosts = Cache::remember('popular_posts', 60, function () {
            return Post::with(['user', 'category'])
                ->published()
                ->orderBy('views_count', 'desc')
                ->limit(3)
                ->get();
        });

        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
    ```

    **Invalider cache quand catégorie créée/modifiée :**

    **Fichier : `app/Models/Category.php`**

    ```php
    use Illuminate\Support\Facades\Cache;

    protected static function booted()
    {
        /**
         * Invalider cache sidebar quand catégorie créée
         */
        static::created(function () {
            Cache::forget('sidebar_categories');
        });

        /**
         * Invalider cache sidebar quand catégorie mise à jour
         */
        static::updated(function () {
            Cache::forget('sidebar_categories');
        });

        /**
         * Invalider cache sidebar quand catégorie supprimée
         */
        static::deleted(function () {
            Cache::forget('sidebar_categories');
        });
    }
    ```

    !!! note "**Stratégies cache avancées :**"
        
        **1. Cache Tags (Redis/Memcached uniquement) :**
        ```php
        // Grouper clés par tags
        Cache::tags(['posts', 'homepage'])->put('key', 'value', 3600);
        
        // Invalider tous articles en 1 commande
        Cache::tags(['posts'])->flush();
        ```
        
        **2. Cache Forever (jusqu'à invalidation manuelle) :**
        ```php
        Cache::forever('settings', $settings);
        Cache::forget('settings'); // Invalider
        ```
        
        **3. Cache Atomic Lock (éviter race conditions) :**
        ```php
        $lock = Cache::lock('process-post-'.$postId, 10);
        
        if ($lock->get()) {
            // Traitement exclusif
            $lock->release();
        }
        ```

??? abstract "7.3.4 : Optimisation Assets (CSS/JS)"

    **Contexte :**

    Les assets (CSS, JS, images) représentent **70% du poids** d'une page web. Optimiser assets = réduire bande passante + accélérer chargement.

    !!! note "**Techniques optimisation assets :**"
        
        1. **Minification** : Supprimer espaces/commentaires (30% poids)
        2. **Compression** : Gzip/Brotli (70% poids)
        3. **Bundling** : Fusionner fichiers (réduire requêtes HTTP)
        4. **Cache navigateur** : Headers Cache-Control (éviter re-téléchargement)
        5. **CDN** : Servir depuis serveurs géographiquement proches

    **Laravel Vite (configuration par défaut)**

    Vite est déjà configuré pour optimisation production. Vérifier `vite.config.js` :

    **Fichier : `vite.config.js`**

    ```javascript
    import { defineConfig } from 'vite';
    import laravel from 'laravel-vite-plugin';

    export default defineConfig({
        plugins: [
            laravel({
                input: [
                    'resources/css/app.css',
                    'resources/js/app.js',
                ],
                refresh: true,
            }),
        ],
        
        /**
         * Configuration optimisation production
         * 
         * Activée automatiquement avec : npm run build
         */
        build: {
            /**
             * Minification JavaScript
             * 
             * Options :
             * - 'esbuild' : Rapide (défaut)
             * - 'terser' : Plus agressif (5% plus petit)
             */
            minify: 'esbuild',
            
            /**
             * Source maps en production
             * 
             * false : Désactive (recommandé production)
             * true : Active (debug production)
             */
            sourcemap: false,
            
            /**
             * Taille limite warning (Ko)
             * 
             * 500 Ko : Alerte si bundle trop gros
             */
            chunkSizeWarningLimit: 500,
            
            /**
             * Rollup options (bundler)
             */
            rollupOptions: {
                output: {
                    /**
                     * Noms fichiers buildés
                     * 
                     * [name] : Nom original (app)
                     * [hash] : Hash contenu (cache busting)
                     * 
                     * Exemple : app-a3f2c1b9.js
                     */
                    entryFileNames: 'assets/[name]-[hash].js',
                    chunkFileNames: 'assets/[name]-[hash].js',
                    assetFileNames: 'assets/[name]-[hash].[ext]',
                }
            }
        },
    });
    ```

    **Build production :**

    ```bash
    # Compiler assets pour production
    npm run build
    ```

    **Résultat :**

    ```
    vite v5.x.x building for production...
    ✓ 127 modules transformed.
    
    public/build/manifest.json                    0.45 kB │ gzip: 0.23 kB
    public/build/assets/app-a3f2c1b9.css          8.42 kB │ gzip: 2.15 kB
    public/build/assets/app-b7e4d3a1.js         142.37 kB │ gzip: 46.82 kB
    
    ✓ built in 3.24s
    ```

    **Vérifier références dans layout :**

    **Fichier : `resources/views/layouts/app.blade.php`**

    ```blade
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        {{-- Vite gère automatiquement :
             - Mode dev : http://localhost:5173/resources/css/app.css (HMR)
             - Mode prod : /build/assets/app-a3f2c1b9.css (minifié + hash) --}}
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body>
        <!-- Contenu -->
    </body>
    </html>
    ```

    !!! note "**Cache navigateur (headers HTTP) :**"
        
        **Configurer Nginx pour caching assets :**
        
        ```nginx
        # /etc/nginx/sites-available/blog.conf
        
        location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf)$ {
            # Cache 1 an (assets hashés = cache busting)
            expires 1y;
            add_header Cache-Control "public, immutable";
            
            # Compression Gzip
            gzip on;
            gzip_types text/css application/javascript image/svg+xml;
            gzip_vary on;
        }
        ```
        
        **Résultat headers HTTP :**
        ```
        Cache-Control: public, immutable, max-age=31536000
        Content-Encoding: gzip
        ```
        
        **Impact :** Assets téléchargés 1 fois, utilisés depuis cache ensuite

??? abstract "7.3.5 : Monitoring Performance (Laravel Debugbar)"

    **Contexte :**

    Impossible d'optimiser sans **mesurer**. Laravel Debugbar affiche métriques performance en temps réel : requêtes SQL, temps exécution, mémoire, etc.

    !!! warning "**Installation DÉVELOPPEMENT uniquement**"
        Debugbar ne doit **JAMAIS** être installé en production (fuite infos sensibles)

    **Installer Laravel Debugbar :**

    ```bash
    composer require barryvdh/laravel-debugbar --dev
    ```

    **Flag `--dev` :** Package installé uniquement en environnement développement (pas en production)

    **Configuration (optionnel) :**

    **Fichier : `config/debugbar.php`** (généré automatiquement)

    ```php
    return [
        /**
         * Activer Debugbar seulement si :
         * - APP_DEBUG=true
         * - Environnement local
         */
        'enabled' => env('DEBUGBAR_ENABLED', env('APP_DEBUG', false)),

        /**
         * Collectors activés
         */
        'collectors' => [
            'phpinfo'         => true,  // Infos PHP
            'messages'        => true,  // Messages debug
            'time'            => true,  // Temps exécution
            'memory'          => true,  // Mémoire utilisée
            'exceptions'      => true,  // Exceptions
            'log'             => true,  // Logs Laravel
            'db'              => true,  // Requêtes SQL ⚡ LE PLUS IMPORTANT
            'views'           => true,  // Vues Blade
            'route'           => true,  // Route actuelle
            'auth'            => false, // Utilisateur connecté
            'gate'            => true,  // Autorisations
            'session'         => true,  // Session
            'cache'           => true,  // Cache
            'events'          => false, // Événements
            'models'          => true,  // Modèles chargés
        ],
    ];
    ```

    **Utilisation Debugbar :**

    1. **Ouvrir application en développement** (APP_DEBUG=true)
    2. **Barre debug apparaît en bas de page**
    3. **Cliquer onglet "Queries"** pour voir requêtes SQL

    !!! note "**Métriques clés Debugbar :**"
        
        **Onglet Queries (requêtes SQL) :**
        
        - **Nombre requêtes** : <10 = excellent, 10-30 = moyen, >30 = problème N+1
        - **Temps total SQL** : <50ms = excellent, 50-200ms = moyen, >200ms = lent
        - **Duplicate queries** : Highlight rouge = même requête répétée (N+1)
        
        **Onglet Timeline :**
        
        - **Temps total** : <200ms = excellent, 200-500ms = moyen, >500ms = lent
        - **Temps PHP** : Logique métier pure
        - **Temps SQL** : Base de données
        
        **Onglet Memory :**
        
        - **Mémoire peak** : <16MB = excellent, 16-32MB = moyen, >32MB = fuite

    **Exemple détection N+1 avec Debugbar :**

    **AVANT optimisation (problème N+1) :**

    ```
    Queries: 19 (duplicate: 18)  |  Time: 342ms
    
    1. SELECT * FROM posts WHERE status='published' LIMIT 9        [12ms]
    2. SELECT * FROM users WHERE id=1                              [18ms]  ← Duplicate
    3. SELECT * FROM users WHERE id=2                              [17ms]  ← Duplicate
    4. SELECT * FROM users WHERE id=1                              [16ms]  ← Duplicate
    5. SELECT * FROM categories WHERE id=3                         [19ms]  ← Duplicate
    ...
    ```

    **APRÈS optimisation (Eager Loading) :**

    ```
    Queries: 3 (duplicate: 0)  |  Time: 45ms
    
    1. SELECT * FROM posts WHERE status='published' LIMIT 9        [12ms]
    2. SELECT * FROM users WHERE id IN (1, 2, 3)                   [15ms]
    3. SELECT * FROM categories WHERE id IN (1, 2, 3)              [18ms]
    ```

    **Impact : × 7.6 plus rapide + 16 requêtes économisées** ✅

=== "**Tableau Récapitulatif Optimisations**"

    | Optimisation | Impact Performance | Difficulté | Commande/Fichier |
    |--------------|-------------------|------------|------------------|
    | **Indexes BDD** | × 50-100 | Facile | Migration `add_indexes_to_posts_table` |
    | **Eager Loading** | × 5-10 | Facile | `with(['user', 'category'])` dans contrôleurs |
    | **Config cache** | × 3 | Facile | `php artisan config:cache` |
    | **Route cache** | × 10 | Facile | `php artisan route:cache` |
    | **View cache** | × 5 | Facile | `php artisan view:cache` |
    | **Autoloader** | × 4 | Facile | `composer install --optimize-autoloader --no-dev` |
    | **Assets minify** | × 2-3 | Facile | `npm run build` (Vite auto) |
    | **Query cache** | × 50 | Moyen | `Cache::remember()` manuel |
    | **Headers cache** | × ∞ | Moyen | Configuration Nginx/Apache |

=== "**Checklist Déploiement Production**"

    **Avant chaque déploiement, vérifier :**

    ```bash
    # 1. Variables environnement
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (php artisan key:generate)

    # 2. Optimisations Laravel
    ✅ php artisan config:cache
    ✅ php artisan route:cache
    ✅ php artisan view:cache
    ✅ php artisan event:cache

    # 3. Composer optimisé
    ✅ composer install --optimize-autoloader --no-dev

    # 4. Assets compilés
    ✅ npm run build

    # 5. Migrations à jour
    ✅ php artisan migrate --force

    # 6. Permissions correctes
    ✅ chmod -R 775 storage bootstrap/cache
    ✅ chown -R www-data:www-data storage bootstrap/cache

    # 7. Vérification santé
    ✅ php artisan route:list (vérifier routes compilées)
    ✅ php artisan config:show (vérifier config cached)
    ```

=== "**Comparaison Performance Avant/Après**"

    **Métriques page d'accueil (9 articles) :**

    | Métrique | Avant Optimisation | Après Optimisation | Amélioration |
    |----------|-------------------|-------------------|--------------|
    | **Requêtes SQL** | 19 | 3 | × 6.3 moins |
    | **Temps SQL** | 342ms | 45ms | × 7.6 plus rapide |
    | **Temps total** | 580ms | 120ms | × 4.8 plus rapide |
    | **Mémoire** | 24 MB | 18 MB | -25% |
    | **Taille page** | 850 KB | 320 KB | -62% (gzip) |
    | **TTFB** | 420ms | 85ms | × 4.9 plus rapide |

    **Résultat : Page d'accueil × 5 plus rapide** 🚀

✅ **Étape 7.3 Terminée !**

**Fichiers créés/modifiés :**

- `database/migrations/XXXX_add_indexes_to_posts_table.php` : Indexes BDD
- `scripts/optimize-production.sh` : Script optimisation automatique
- Tous contrôleurs : Eager Loading avec `with()`
- `vite.config.js` : Configuration build production

**Concepts maîtrisés :**

- Indexes simples et composites
- Eager Loading (with, load, withCount)
- Cache Laravel (config, route, view, query)
- Optimisation assets (Vite, minification)
- Monitoring performance (Debugbar)
- Headers cache navigateur
- Stratégies cache avancées

### Étape 7.4 : Sécurité et Hardening

**Contexte :**

> La sécurité est **non négociable** en production. Une faille exploitée = données volées, site défacé, réputation détruite. Laravel intègre protections natives mais nécessite configuration correcte.

!!! note "**Top 5 vulnérabilités web (OWASP 2024) :**"

    1. **Broken Access Control** : Utilisateur accède ressources non autorisées
    2. **Cryptographic Failures** : Données sensibles non chiffrées
    3. **Injection** : SQL, XSS, Command Injection
    4. **Insecure Design** : Architecture vulnérable par conception
    5. **Security Misconfiguration** : Erreurs configuration (debug=true prod)

**Protections Laravel natives (déjà actives) :**

- ✅ **CSRF** : Tokens anti-Cross-Site Request Forgery (`@csrf`)
- ✅ **XSS** : Échappement auto HTML (`{{ }}` vs `{!! !!}`)
- ✅ **SQL Injection** : Requêtes préparées (Eloquent/Query Builder)
- ✅ **Password Hashing** : Bcrypt automatique (mutateur)
- ✅ **Session Security** : Cookies HttpOnly, SameSite

??? abstract "7.4.1 : Rate Limiting (Protection Brute Force)"

    **Contexte :**

    Le **rate limiting** limite nombre de requêtes par IP/utilisateur. Empêche attaques brute force (login, formulaires, API).

    !!! warning "**Exemples attaques sans rate limiting :**"
        - **Login brute force** : 10 000 tentatives/seconde → mot de passe craqué
        - **Comment spam** : 1000 commentaires/minute → pollution base
        - **Scraping** : 100 000 requêtes/heure → vol contenu

    **Configurer rate limiting routes publiques :**

    **Fichier : `app/Providers/RouteServiceProvider.php`**

    ```php
    <?php

    namespace App\Providers;

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\RateLimiter;
    use Illuminate\Support\Facades\Route;

    class RouteServiceProvider extends ServiceProvider
    {
        public const HOME = '/dashboard';

        public function boot(): void
        {
            /**
             * Rate limiter API (déjà configuré par Laravel)
             * 60 requêtes/minute par IP
             */
            RateLimiter::for('api', function (Request $request) {
                return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
            });

            /**
             * Rate limiter CONNEXION
             * 
             * Protection brute force login :
             * - 5 tentatives par minute par IP
             * - Identifié par email + IP (empêche rotation IP)
             * - Response 429 Too Many Requests si dépassé
             */
            RateLimiter::for('login', function (Request $request) {
                $throttleKey = strtolower($request->input('email')).'|'.$request->ip();
                
                return Limit::perMinute(5)->by($throttleKey)->response(function () {
                    return response()->json([
                        'message' => 'Trop de tentatives de connexion. Réessayez dans 1 minute.'
                    ], 429);
                });
            });

            /**
             * Rate limiter COMMENTAIRES
             * 
             * Protection spam :
             * - 3 commentaires par minute par IP
             * - Empêche flood commentaires
             */
            RateLimiter::for('comments', function (Request $request) {
                return Limit::perMinute(3)->by($request->ip())->response(function () {
                    return back()->with('error', 'Trop de commentaires envoyés. Patientez 1 minute.');
                });
            });

            /**
             * Rate limiter CRÉATION ARTICLES
             * 
             * Protection spam articles :
             * - 10 articles par heure par utilisateur
             */
            RateLimiter::for('create-posts', function (Request $request) {
                return Limit::perHour(10)->by($request->user()->id);
            });

            $this->routes(function () {
                Route::middleware('api')
                    ->prefix('api')
                    ->group(base_path('routes/api.php'));

                Route::middleware('web')
                    ->group(base_path('routes/web.php'));
            });
        }
    }
    ```

    **Appliquer rate limiting aux routes :**

    **Fichier : `routes/web.php`**

    ```php
    use Illuminate\Support\Facades\Route;
    use App\Http\Controllers\{
        HomeController, PostController, CommentController,
        CategoryController, AuthorController, DashboardController, ProfileController
    };

    // Routes publiques
    Route::get('/', [HomeController::class, 'index'])->name('home');
    Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');
    Route::get('/category/{category:slug}', [CategoryController::class, 'show'])->name('categories.show');
    Route::get('/author/{user}', [AuthorController::class, 'show'])->name('authors.show');

    /**
     * Route commentaires avec rate limiting
     * middleware('throttle:comments') applique limiter 'comments'
     */
    Route::post('/posts/{post}/comments', [CommentController::class, 'store'])
        ->middleware('throttle:comments')
        ->name('comments.store');

    // Routes authentification Breeze (login déjà protégé dans auth.php)
    require __DIR__.'/auth.php';

    // Routes protégées (authentification requise)
    Route::middleware('auth')->group(function () {
        Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
        
        // Profil
        Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
        Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
        Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
        
        /**
         * Création/édition articles avec rate limiting
         */
        Route::middleware('throttle:create-posts')->group(function () {
            Route::get('/posts/create', [PostController::class, 'create'])->name('posts.create');
            Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
        });
        
        Route::get('/posts/{post}/edit', [PostController::class, 'edit'])->name('posts.edit');
        Route::put('/posts/{post}', [PostController::class, 'update'])->name('posts.update');
        Route::delete('/posts/{post}', [PostController::class, 'destroy'])->name('posts.destroy');
        
        // Modération commentaires
        Route::patch('/comments/{comment}/approve', [CommentController::class, 'approve'])->name('comments.approve');
        Route::delete('/comments/{comment}', [CommentController::class, 'destroy'])->name('comments.destroy');
    });
    ```

    **Tester rate limiting :**

    ```bash
    # Envoyer 10 commentaires rapidement (dépasser limite)
    for i in {1..10}; do
        curl -X POST http://localhost:8000/posts/mon-article/comments \
            -d "author_name=Test&author_email=test@example.com&content=Spam $i"
    done
    
    # Après 3 requêtes → 429 Too Many Requests
    ```

??? abstract "7.4.2 : Headers Sécurité HTTP"

    **Contexte :**

    Les **headers HTTP** contrôlent comportement navigateur. Headers sécurité protègent contre XSS, clickjacking, injection code.

    **Créer middleware headers sécurité :**

    ```bash
    php artisan make:middleware SecurityHeaders
    ```

    **Fichier : `app/Http/Middleware/SecurityHeaders.php`**

    ```php
    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class SecurityHeaders
    {
        /**
         * Ajoute headers sécurité à toutes les réponses
         */
        public function handle(Request $request, Closure $next): Response
        {
            $response = $next($request);

            /**
             * X-Content-Type-Options: nosniff
             * 
             * Empêche navigateur "deviner" type MIME
             * Force respect Content-Type déclaré
             * Protège contre attaques MIME sniffing
             */
            $response->headers->set('X-Content-Type-Options', 'nosniff');

            /**
             * X-Frame-Options: DENY
             * 
             * Empêche site être chargé dans <iframe>
             * Protège contre clickjacking
             * 
             * Alternatives :
             * - DENY : Interdit tous iframes
             * - SAMEORIGIN : Autorise iframes même domaine
             */
            $response->headers->set('X-Frame-Options', 'DENY');

            /**
             * X-XSS-Protection: 1; mode=block
             * 
             * Active filtre XSS navigateur (anciens navigateurs)
             * mode=block : Bloque page si XSS détecté
             * 
             * Note : Obsolète (remplacé CSP) mais compatible anciens navigateurs
             */
            $response->headers->set('X-XSS-Protection', '1; mode=block');

            /**
             * Referrer-Policy: strict-origin-when-cross-origin
             * 
             * Contrôle infos envoyées dans header Referer
             * 
             * Options :
             * - no-referrer : Jamais d'info referer
             * - same-origin : Referer seulement même domaine
             * - strict-origin-when-cross-origin : URL complète même origine, domaine seulement cross-origin
             */
            $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');

            /**
             * Content-Security-Policy (CSP)
             * 
             * Définit sources autorisées pour scripts, styles, images
             * Protection ultime contre XSS
             * 
             * Directives :
             * - default-src 'self' : Par défaut, seulement même origine
             * - script-src 'self' 'unsafe-inline' : Scripts même origine + inline (Vite HMR)
             * - style-src 'self' 'unsafe-inline' : CSS même origine + inline (Tailwind)
             * - img-src 'self' data: https: : Images même origine + data URIs + HTTPS externes
             * - font-src 'self' : Fonts même origine
             * - connect-src 'self' : AJAX/WebSocket même origine
             * 
             * Note : 'unsafe-inline' nécessaire pour Vite dev + Tailwind
             * Production : Remplacer par nonces ou hashes
             */
            $response->headers->set('Content-Security-Policy', 
                "default-src 'self'; " .
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; " .
                "style-src 'self' 'unsafe-inline'; " .
                "img-src 'self' data: https:; " .
                "font-src 'self'; " .
                "connect-src 'self';"
            );

            /**
             * Permissions-Policy
             * 
             * Contrôle accès APIs navigateur (géolocalisation, caméra, etc.)
             * 
             * Directives désactivées :
             * - geolocation : Géolocalisation
             * - microphone : Microphone
             * - camera : Caméra
             * - payment : API Payment Request
             */
            $response->headers->set('Permissions-Policy', 
                'geolocation=(), microphone=(), camera=(), payment=()'
            );

            /**
             * Strict-Transport-Security (HSTS)
             * 
             * Force HTTPS pendant 1 an
             * includeSubDomains : Applique sous-domaines
             * preload : Eligible liste preload navigateurs
             * 
             * ATTENTION : Activer SEULEMENT si certificat SSL configuré
             */
            if ($request->secure()) {
                $response->headers->set('Strict-Transport-Security', 
                    'max-age=31536000; includeSubDomains; preload'
                );
            }

            return $response;
        }
    }
    ```

    **Enregistrer middleware globalement :**

    **Fichier : `bootstrap/app.php`**

    ```php
    <?php

    use Illuminate\Foundation\Application;
    use Illuminate\Foundation\Configuration\Exceptions;
    use Illuminate\Foundation\Configuration\Middleware;

    return Application::configure(basePath: dirname(__DIR__))
        ->withRouting(
            web: __DIR__.'/../routes/web.php',
            commands: __DIR__.'/../routes/console.php',
            health: '/up',
        )
        ->withMiddleware(function (Middleware $middleware) {
            /**
             * Ajouter SecurityHeaders à toutes les requêtes web
             */
            $middleware->web(append: [
                \App\Http\Middleware\SecurityHeaders::class,
            ]);
        })
        ->withExceptions(function (Exceptions $exceptions) {
            //
        })->create();
    ```

    **Tester headers (DevTools) :**

    ```bash
    # Ouvrir page dans navigateur
    # F12 → Network → Sélectionner requête → Headers
    
    # Vérifier présence :
    ✅ X-Content-Type-Options: nosniff
    ✅ X-Frame-Options: DENY
    ✅ Content-Security-Policy: ...
    ✅ Strict-Transport-Security: ... (si HTTPS)
    ```

??? abstract "7.4.3 : Validation Stricte Entrées Utilisateur"

    **Contexte :**

    **"Never trust user input"** est la règle #1 sécurité. Toute donnée externe doit être validée côté serveur (validation client = contournable).

    **Renforcer validation contrôleurs :**

    **Fichier : `app/Http/Controllers/PostController.php`**

    ```php
    public function store(Request $request)
    {
        /**
         * Validation STRICTE
         * 
         * Règles renforcées :
         * - max:255 : Limite taille (prévient DOS)
         * - exists:... : Vérifie FK (prévient injection)
         * - min:100 : Force qualité contenu
         * - url : Valide format URL strict
         * - regex:... : Patterns spécifiques si besoin
         */
        $validated = $request->validate([
            'title' => [
                'required',
                'string',
                'max:255',
                // Optionnel : Interdire caractères spéciaux dangereux
                'regex:/^[a-zA-Z0-9\s\-\.\']+$/u',
            ],
            'category_id' => [
                'required',
                'integer',
                'exists:categories,id', // Vérifie catégorie existe
            ],
            'excerpt' => [
                'required',
                'string',
                'max:500',
            ],
            'content' => [
                'required',
                'string',
                'min:100',
                'max:50000', // Limite max (prévient DOS)
            ],
            'image' => [
                'nullable',
                'url', // Valide format URL
                'max:500',
            ],
            'status' => [
                'required',
                'in:draft,published', // Whitelist stricte (pas de "admin", etc.)
            ],
        ], [
            // Messages personnalisés français
            'title.required' => 'Le titre est obligatoire.',
            'title.max' => 'Le titre ne peut dépasser 255 caractères.',
            'title.regex' => 'Le titre contient des caractères non autorisés.',
            'category_id.exists' => 'La catégorie sélectionnée n\'existe pas.',
            'content.min' => 'Le contenu doit contenir au moins 100 caractères.',
            'content.max' => 'Le contenu ne peut dépasser 50 000 caractères.',
            'status.in' => 'Le statut doit être "brouillon" ou "publié".',
        ]);

        /**
         * Sanitization supplémentaire (optionnel)
         * 
         * Laravel échappe automatiquement HTML via {{ }}
         * Mais peut nettoyer davantage si besoin :
         */
        // $validated['title'] = strip_tags($validated['title']);
        // $validated['content'] = strip_tags($validated['content'], '<p><br><strong><em><ul><ol><li>');

        // Création article
        $post = auth()->user()->posts()->create($validated);

        return redirect()
            ->route('posts.show', $post->slug)
            ->with('success', 'Article créé avec succès.');
    }
    ```

    **Validation commentaires (protection spam) :**

    **Fichier : `app/Http/Controllers/CommentController.php`**

    ```php
    public function store(Request $request, Post $post)
    {
        $validated = $request->validate([
            'author_name' => [
                'required',
                'string',
                'max:255',
                // Interdire URLs dans nom (spam)
                'not_regex:/https?:\/\//',
            ],
            'author_email' => [
                'required',
                'email:rfc,dns', // Validation stricte email + DNS check
                'max:255',
            ],
            'content' => [
                'required',
                'string',
                'min:10',
                'max:1000',
                // Interdire URLs multiples (spam)
                function ($attribute, $value, $fail) {
                    if (substr_count($value, 'http') > 2) {
                        $fail('Le commentaire contient trop de liens.');
                    }
                },
            ],
        ], [
            'author_name.not_regex' => 'Le nom ne peut contenir de liens.',
            'author_email.email' => 'L\'adresse email n\'est pas valide.',
            'content.min' => 'Le commentaire doit contenir au moins 10 caractères.',
            'content.max' => 'Le commentaire ne peut dépasser 1000 caractères.',
        ]);

        /**
         * Honeypot anti-spam (optionnel)
         * 
         * Champ caché dans formulaire, invisible utilisateur
         * Si rempli → bot détecté → rejeter
         */
        if ($request->filled('website')) { // 'website' = champ honeypot
            return back()->with('error', 'Spam détecté.');
        }

        // Création commentaire (non approuvé par défaut)
        $post->comments()->create([
            ...$validated,
            'approved' => false,
        ]);

        return back()->with('success', 'Commentaire envoyé. Il sera visible après modération.');
    }
    ```

??? abstract "7.4.4 : Protection Variables Environnement"

    **Contexte :**

    Le fichier `.env` contient **secrets** (DB password, API keys). Il ne doit **JAMAIS** être commité Git ou accessible web.

    **Vérifier `.gitignore` (déjà configuré) :**

    **Fichier : `.gitignore`**

    ```gitignore
    # Fichiers sensibles (JAMAIS commiter)
    .env
    .env.backup
    .env.production
    .phpunit.result.cache

    # Caches Laravel
    /bootstrap/cache/*
    /storage/*.key
    /storage/logs/*

    # Node modules
    /node_modules
    /public/hot
    /public/storage
    /public/build

    # Vendor
    /vendor
    ```

    **Permissions fichier .env (serveur production) :**

    ```bash
    # .env lisible seulement par propriétaire (root ou www-data)
    chmod 600 .env
    chown www-data:www-data .env
    
    # Vérifier
    ls -la .env
    # -rw------- 1 www-data www-data 1024 Dec 11 10:30 .env
    ```

    **Bloquer accès .env via Nginx :**

    ```nginx
    # /etc/nginx/sites-available/blog.conf
    
    location ~ /\.env {
        deny all;
        return 404;
    }
    
    # Bloquer aussi autres fichiers sensibles
    location ~ /\.(git|svn|hg) {
        deny all;
        return 404;
    }
    ```

    **Exemple .env production sécurisé :**

    ```bash
    # Application
    APP_NAME="Mon Blog"
    APP_ENV=production
    APP_KEY=base64:GENERER_AVEC_php_artisan_key:generate
    APP_DEBUG=false  # ⚠️ TOUJOURS false en production
    APP_URL=https://monblog.com

    # Base de données
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=blog_prod
    DB_USERNAME=blog_user
    DB_PASSWORD=MOT_DE_PASSE_TRES_FORT_32_CHARS  # ⚠️ JAMAIS 'root' ou 'password'

    # Cache/Sessions
    CACHE_DRIVER=redis
    SESSION_DRIVER=redis
    QUEUE_CONNECTION=redis

    # Redis (si utilisé)
    REDIS_PASSWORD=MOT_DE_PASSE_REDIS_FORT

    # Mail
    MAIL_MAILER=smtp
    MAIL_HOST=smtp.mailtrap.io
    MAIL_PORT=587
    MAIL_USERNAME=your_username
    MAIL_PASSWORD=your_password  # ⚠️ Token API, pas password perso
    ```

=== "**Checklist Sécurité Production**"

    **Avant déploiement, vérifier :**

    ```bash
    # Configuration
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (32 chars aléatoires)
    
    # Base de données
    ✅ DB_PASSWORD fort (min 16 chars)
    ✅ DB_USERNAME dédié (PAS root)
    ✅ Accès BDD limité à localhost/IP serveur
    
    # Fichiers
    ✅ .env permissions 600
    ✅ storage/ permissions 775
    ✅ .env dans .gitignore
    
    # Headers HTTP
    ✅ SecurityHeaders middleware actif
    ✅ HTTPS forcé (HSTS)
    ✅ CSP configuré
    
    # Rate Limiting
    ✅ Login : 5/min
    ✅ Commentaires : 3/min
    ✅ Création articles : 10/h
    
    # Validation
    ✅ Règles strictes tous formulaires
    ✅ exists: sur toutes FK
    ✅ max: sur tous champs texte
    
    # Serveur
    ✅ Firewall actif (UFW/iptables)
    ✅ SSH clés uniquement (pas password)
    ✅ Fail2ban configuré
    ✅ Mises à jour auto sécurité
    ```

=== "**Tests Sécurité Automatisés**"

    **Scanner vulnérabilités avec Enlightn :**

    ```bash
    # Installer Enlightn Security Checker
    composer require enlightn/enlightn --dev
    
    # Exécuter scan sécurité
    php artisan enlightn
    
    # Résultat : Rapport détaillé vulnérabilités
    ```

    **Tester headers sécurité avec securityheaders.com :**

    ```bash
    # Analyser headers production
    https://securityheaders.com/?q=https://monblog.com
    
    # Score attendu : A+ (tous headers présents)
    ```

=== "**Résumé Protections Implémentées**"

    | Protection | Technologie | Fichier/Config |
    |------------|-------------|----------------|
    | **CSRF** | Token Laravel | `@csrf` (déjà actif) |
    | **XSS** | Échappement Blade | `{{ }}` (déjà actif) |
    | **SQL Injection** | Requêtes préparées | Eloquent (déjà actif) |
    | **Brute Force Login** | Rate limiting | `RouteServiceProvider` (5/min) |
    | **Comment Spam** | Rate limiting | `RouteServiceProvider` (3/min) |
    | **Clickjacking** | X-Frame-Options | `SecurityHeaders` middleware |
    | **MIME Sniffing** | X-Content-Type | `SecurityHeaders` middleware |
    | **Code Injection** | CSP | `SecurityHeaders` middleware |
    | **HTTPS** | HSTS | `SecurityHeaders` middleware |
    | **Validation** | Rules strictes | Tous contrôleurs |
    | **Secrets** | .env protégé | Permissions 600 + Nginx deny |

✅ **Étape 7.4 Terminée !**

**Fichiers créés/modifiés :**

- `app/Providers/RouteServiceProvider.php` : Rate limiting (login, comments, posts)
- `app/Http/Middleware/SecurityHeaders.php` : Headers sécurité HTTP
- `bootstrap/app.php` : Enregistrement middleware global
- `routes/web.php` : Application throttle aux routes
- Contrôleurs : Validation stricte renforcée

**Concepts maîtrisés :**

- Rate limiting (throttle)
- Headers sécurité HTTP (CSP, HSTS, X-Frame-Options)
- Validation stricte (regex, exists, custom rules)
- Protection .env (permissions, .gitignore)
- Middleware sécurité global
- Honeypot anti-spam

**Application maintenant protégée contre :**

- ✅ Brute force (login/formulaires)
- ✅ XSS (échappement + CSP)
- ✅ CSRF (tokens Laravel)
- ✅ SQL Injection (Eloquent)
- ✅ Clickjacking (X-Frame-Options)
- ✅ Spam commentaires (rate limiting + validation)
- ✅ MITM (HTTPS forcé HSTS)





























































### Étape 7.5 : Configuration Production

**Contexte :**

> La configuration production diffère fondamentalement du développement. Un `.env` mal configuré = performances dégradées, failles sécurité, ou pire : **perte de données**. Cette étape configure Laravel pour environnement production robuste.

**Différences dev vs production :**

| Paramètre | Développement | Production |
|-----------|---------------|------------|
| **APP_DEBUG** | `true` (traces erreurs) | `false` (messages génériques) |
| **APP_ENV** | `local` | `production` |
| **CACHE_DRIVER** | `file` (simple) | `redis` (performant) |
| **SESSION_DRIVER** | `file` | `redis` ou `database` |
| **QUEUE_CONNECTION** | `sync` (immédiat) | `redis` (asynchrone) |
| **LOG_LEVEL** | `debug` (tout) | `error` (critique uniquement) |

**Architecture production recommandée :**

```
┌─────────────────┐
│   Nginx/Apache  │ → Serveur web (reverse proxy)
└────────┬────────┘
         │
┌────────▼────────┐
│   PHP-FPM 8.2+  │ → Processeur PHP
└────────┬────────┘
         │
┌────────▼────────┐
│  Laravel App    │ → Application
└────┬───────┬────┘
     │       │
┌────▼───┐ ┌─▼─────┐
│ MySQL  │ │ Redis │ → Stockage données + cache
└────────┘ └───────┘
```

??? abstract "7.5.1 : Fichier .env Production (Template Complet)"

    **Créer fichier template production :**

    **Fichier : `.env.production.example`** (à copier en `.env` sur serveur)

    ```bash
    ###############################################################################
    # CONFIGURATION PRODUCTION - LARAVEL BLOG MULTI-AUTEURS
    ###############################################################################
    #
    # Ce fichier sert de template pour environnement production
    # 
    # INSTRUCTIONS DÉPLOIEMENT :
    # 1. Copier ce fichier : cp .env.production.example .env
    # 2. Remplir TOUTES les valeurs avec vrais credentials
    # 3. Générer APP_KEY : php artisan key:generate
    # 4. Sécuriser : chmod 600 .env && chown www-data:www-data .env
    # 5. Vérifier : php artisan config:show
    #
    ###############################################################################

    ###############################################################################
    # APPLICATION
    ###############################################################################

    # Nom application (affiché dans emails, notifications)
    APP_NAME="Mon Blog"

    # Environnement : TOUJOURS 'production' en prod
    # Valeurs possibles : local, staging, production
    APP_ENV=production

    # Clé chiffrement (32 chars aléatoires)
    # ⚠️ GÉNÉRER AVEC : php artisan key:generate
    # ⚠️ NE JAMAIS partager cette clé
    # ⚠️ NE JAMAIS changer en production (sessions/données chiffrées perdues)
    APP_KEY=

    # Debug mode : TOUJOURS false en production
    # ⚠️ true = FUITE INFOS SENSIBLES (stack traces, config, BDD)
    APP_DEBUG=false

    # URL application (avec protocole https://)
    # Utilisé pour génération liens emails, assets CDN
    APP_URL=https://monblog.com

    # Timezone application
    # Liste : https://www.php.net/manual/en/timezones.php
    APP_TIMEZONE=Europe/Paris

    # Locale (langue interface)
    APP_LOCALE=fr
    APP_FALLBACK_LOCALE=en

    ###############################################################################
    # BASE DE DONNÉES
    ###############################################################################

    # Driver : mysql, pgsql, sqlite, sqlsrv
    DB_CONNECTION=mysql

    # Host : 127.0.0.1 (local) ou IP serveur distant
    # Production : Toujours local (sécurité) ou IP interne VPC
    DB_HOST=127.0.0.1

    # Port : 3306 (MySQL), 5432 (PostgreSQL)
    DB_PORT=3306

    # Nom base de données
    # Convention : {app}_production
    DB_DATABASE=blog_production

    # Utilisateur dédié (PAS root)
    # Créer avec : CREATE USER 'blog_user'@'localhost' IDENTIFIED BY '...';
    DB_USERNAME=blog_user

    # Password FORT (min 16 chars, mix alphanum + symboles)
    # Générer : openssl rand -base64 24
    # ⚠️ JAMAIS 'root', 'password', 'admin'
    DB_PASSWORD=

    ###############################################################################
    # CACHE
    ###############################################################################

    # Driver cache : file, redis, memcached, database, array
    # Production : redis (performances optimales)
    # Alternative : memcached ou database si pas Redis
    CACHE_DRIVER=redis

    # Préfixe clés cache (évite collisions multi-apps)
    CACHE_PREFIX=blog_cache_

    ###############################################################################
    # SESSION
    ###############################################################################

    # Driver session : file, cookie, database, redis
    # Production : redis ou database (partage entre serveurs)
    # Éviter : file (pas scalable multi-serveurs)
    SESSION_DRIVER=redis

    # Durée session (minutes)
    # 120 = 2 heures (connexion utilisateur)
    SESSION_LIFETIME=120

    # Chiffrer cookies session (sécurité supplémentaire)
    SESSION_ENCRYPT=true

    # Cookies accessibles seulement via HTTP (pas JavaScript)
    # Protection XSS
    SESSION_HTTP_ONLY=true

    # SameSite : lax, strict, none
    # lax : Protection CSRF tout en permettant liens externes
    SESSION_SAME_SITE=lax

    # Cookies sécurisés (HTTPS uniquement)
    # ⚠️ true = HTTPS obligatoire
    SESSION_SECURE_COOKIE=true

    ###############################################################################
    # QUEUE (JOBS ASYNCHRONES)
    ###############################################################################

    # Driver queue : sync, database, redis, sqs, beanstalkd
    # Production : redis (performant, durable)
    # sync = développement (exécution immédiate)
    QUEUE_CONNECTION=redis

    ###############################################################################
    # REDIS
    ###############################################################################

    # Host Redis : 127.0.0.1 (local) ou IP serveur
    REDIS_HOST=127.0.0.1

    # Port Redis : 6379 (défaut)
    REDIS_PORT=6379

    # Password Redis (fortement recommandé production)
    # Configurer dans redis.conf : requirepass <password>
    REDIS_PASSWORD=

    # Base de données Redis (0-15)
    # Séparer cache/session/queue pour éviter flush accidentel
    REDIS_CACHE_DB=0
    REDIS_SESSION_DB=1
    REDIS_QUEUE_DB=2

    ###############################################################################
    # MAIL
    ###############################################################################

    # Mailer : smtp, sendmail, mailgun, ses, postmark
    # Production : Service dédié (Mailgun, SendGrid, AWS SES)
    MAIL_MAILER=smtp

    # Serveur SMTP
    # Exemples :
    # - Mailgun : smtp.mailgun.org
    # - SendGrid : smtp.sendgrid.net
    # - Gmail : smtp.gmail.com (déconseillé prod)
    MAIL_HOST=smtp.mailgun.org

    # Port SMTP : 587 (TLS), 465 (SSL), 25 (non chiffré - éviter)
    MAIL_PORT=587

    # Username SMTP (souvent email ou API key)
    MAIL_USERNAME=

    # Password SMTP ou API token
    MAIL_PASSWORD=

    # Chiffrement : tls, ssl, null
    # 587 → tls, 465 → ssl
    MAIL_ENCRYPTION=tls

    # Adresse expéditeur par défaut
    MAIL_FROM_ADDRESS=noreply@monblog.com
    MAIL_FROM_NAME="${APP_NAME}"

    ###############################################################################
    # LOGGING
    ###############################################################################

    # Channel : stack, single, daily, slack, syslog, errorlog
    # Production : daily (rotation automatique journalière)
    LOG_CHANNEL=daily

    # Niveau log : debug, info, notice, warning, error, critical, alert, emergency
    # Production : error (seulement erreurs critiques)
    # Développement : debug (tout)
    LOG_LEVEL=error

    # Rétention logs (jours)
    # daily channel : Supprime logs > X jours
    LOG_DAILY_DAYS=14

    ###############################################################################
    # BROADCASTING (TEMPS RÉEL - Optionnel)
    ###############################################################################

    # Driver : pusher, redis, log, null
    # null = désactivé (pas de temps réel)
    BROADCAST_DRIVER=null

    ###############################################################################
    # FILESYSTEM
    ###############################################################################

    # Disk par défaut : local, public, s3
    # Production : s3 (AWS) ou equivalent (DigitalOcean Spaces, Cloudflare R2)
    # local = développement uniquement
    FILESYSTEM_DISK=local

    # AWS S3 (si utilisé)
    # AWS_ACCESS_KEY_ID=
    # AWS_SECRET_ACCESS_KEY=
    # AWS_DEFAULT_REGION=eu-west-1
    # AWS_BUCKET=
    # AWS_USE_PATH_STYLE_ENDPOINT=false

    ###############################################################################
    # SERVICES EXTERNES (Optionnel)
    ###############################################################################

    # Vite (assets)
    # Production : npm run build génère manifeste
    # Développement : serveur HMR sur port 5173
    VITE_APP_NAME="${APP_NAME}"

    ###############################################################################
    # SÉCURITÉ ADDITIONNELLE
    ###############################################################################

    # Hasher : bcrypt, argon, argon2id
    # bcrypt = défaut Laravel (compatible, éprouvé)
    # argon2id = plus sécurisé (nécessite extension PHP)
    HASH_DRIVER=bcrypt

    # Rounds bcrypt (complexité hashing)
    # 10 = défaut (100ms hash)
    # 12 = plus sécurisé (400ms hash, ralentit brute force)
    BCRYPT_ROUNDS=10

    ###############################################################################
    # DÉBOGAGE PRODUCTION (À RETIRER EN PROD)
    ###############################################################################

    # Telescope (monitoring Laravel - dev/staging uniquement)
    # TELESCOPE_ENABLED=false

    # Debugbar (barre debug - dev uniquement)
    # DEBUGBAR_ENABLED=false
    ```

    **Générer password sécurisés :**

    ```bash
    # Password BDD (24 chars aléatoires)
    openssl rand -base64 24
    # Exemple : 7Kf2mP9xQw3nRt8sVb4cYh6d
    
    # Password Redis (32 chars aléatoires)
    openssl rand -base64 32
    # Exemple : 9Xm2pL7wQz5nRv8tYc4bHf6gJs3kDr1a
    
    # APP_KEY (généré par Laravel)
    php artisan key:generate
    # Écrit automatiquement dans .env
    ```

??? abstract "7.5.2 : Configuration Services Externes"

    **Contexte :**

    Production nécessite services externes robustes pour emails, cache, monitoring. Configuration optimale selon budget.

    **Option 1 : Budget limité (<10€/mois)**

    **Stack "All-in-One" :**

    - **Serveur** : VPS (Hetzner 5€/mois, DigitalOcean 6$/mois)
    - **BDD** : MySQL local (inclus)
    - **Cache** : Redis local (inclus)
    - **Mail** : Brevo (ex-Sendinblue) 300 emails/jour gratuit
    - **Assets** : Serveur local (pas CDN)

    **Configuration .env (budget limité) :**

    ```bash
    # Tout sur même serveur
    DB_HOST=127.0.0.1
    REDIS_HOST=127.0.0.1
    
    # Mail gratuit Brevo
    MAIL_MAILER=smtp
    MAIL_HOST=smtp-relay.brevo.com
    MAIL_PORT=587
    MAIL_USERNAME=votre-email@example.com
    MAIL_PASSWORD=votre-cle-api-brevo
    
    # Filesystem local
    FILESYSTEM_DISK=local
    ```

    **Option 2 : Budget moyen (50-100€/mois)**

    **Stack "Séparation Services" :**

    - **Serveur** : VPS (DigitalOcean 24$/mois)
    - **BDD** : Managed MySQL (DigitalOcean 15$/mois)
    - **Cache** : Managed Redis (DigitalOcean 15$/mois)
    - **Mail** : Mailgun 35$/mois (50k emails)
    - **Assets** : S3-compatible (Spaces 5$/mois 250GB)
    - **CDN** : Cloudflare gratuit

    **Configuration .env (budget moyen) :**

    ```bash
    # BDD managée
    DB_HOST=db-mysql-fra1-12345.ondigitalocean.com
    DB_PORT=25060
    DB_USERNAME=doadmin
    DB_PASSWORD=mot_de_passe_genere
    DB_SSLMODE=require  # Connexion chiffrée
    
    # Redis managé
    REDIS_HOST=redis-fra1-12345.ondigitalocean.com
    REDIS_PORT=25061
    REDIS_PASSWORD=mot_de_passe_genere
    REDIS_TLS=true  # Connexion chiffrée
    
    # Mail Mailgun
    MAIL_MAILER=mailgun
    MAILGUN_DOMAIN=mg.monblog.com
    MAILGUN_SECRET=cle-api-mailgun
    
    # S3-compatible (DigitalOcean Spaces)
    FILESYSTEM_DISK=s3
    AWS_ACCESS_KEY_ID=votre-access-key
    AWS_SECRET_ACCESS_KEY=votre-secret-key
    AWS_DEFAULT_REGION=fra1
    AWS_BUCKET=blog-assets
    AWS_ENDPOINT=https://fra1.digitaloceanspaces.com
    AWS_USE_PATH_STYLE_ENDPOINT=false
    ```

    **Option 3 : Budget entreprise (>200€/mois)**

    **Stack "Haute Disponibilité" :**

    - **Serveur** : Multi-instances (Load Balancer)
    - **BDD** : Cluster MySQL (réplication master-slave)
    - **Cache** : Cluster Redis (haute dispo)
    - **Mail** : SendGrid/AWS SES (volume illimité)
    - **Assets** : CloudFront CDN (AWS)
    - **Monitoring** : New Relic / Datadog
    - **Backup** : Automatisé quotidien

    **Configuration .env (entreprise) :**

    ```bash
    # BDD cluster avec read replicas
    DB_HOST=mysql-cluster-master.internal
    DB_PORT=3306
    DB_READ_HOSTS=mysql-replica1.internal,mysql-replica2.internal
    
    # Redis cluster
    REDIS_CLUSTER=true
    REDIS_HOSTS=redis1.internal:6379,redis2.internal:6379,redis3.internal:6379
    
    # AWS SES (emails)
    MAIL_MAILER=ses
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    AWS_DEFAULT_REGION=eu-west-1
    
    # CloudFront CDN
    AWS_CLOUDFRONT_DOMAIN=d123456abcdef.cloudfront.net
    
    # Monitoring New Relic
    NEW_RELIC_LICENSE_KEY=votre-cle-licence
    NEW_RELIC_APP_NAME="Mon Blog Production"
    ```

    !!! note "**Comparaison services mail (emails transactionnels) :**"
        
        | Service | Gratuit | Payant | Avantages | Inconvénients |
        |---------|---------|--------|-----------|---------------|
        | **Brevo** | 300/jour | 19€/mois (20k) | Simple, interface FR | Limite gratuite basse |
        | **Mailgun** | 5k/mois | 35$/mois (50k) | Fiable, analytics | Configuration DNS |
        | **SendGrid** | 100/jour | 15$/mois (40k) | Réputation, livrabilité | Interface complexe |
        | **AWS SES** | 62k/mois | $0.10/1000 | Très économique volume | Requiert compte AWS |
        | **Postmark** | Essai 100 | 15$/mois (10k) | Excellent support | Plus cher petit volume |

??? abstract "7.5.3 : Configuration Redis (Cache + Sessions + Queue)"

    **Installer Redis (si pas déjà fait) :**

    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install redis-server
    
    # Démarrer service
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Vérifier statut
    sudo systemctl status redis-server
    
    # Tester connexion
    redis-cli ping
    # Réponse attendue : PONG
    ```

    **Configurer Redis sécurisé :**

    **Fichier : `/etc/redis/redis.conf`**

    ```conf
    ###############################################################################
    # CONFIGURATION REDIS PRODUCTION
    ###############################################################################

    # Bind : Écoute seulement localhost (sécurité)
    # Production : 127.0.0.1 (local uniquement)
    # Multi-serveurs : IP interne VPC
    bind 127.0.0.1

    # Port : 6379 (défaut)
    port 6379

    # Password : TOUJOURS définir en production
    # Générer : openssl rand -base64 32
    requirepass VOTRE_PASSWORD_REDIS_FORT

    # Persistence : RDB (snapshots) + AOF (journal)
    # RDB : Snapshot toutes les 60s si ≥1000 changements
    save 60 1000
    save 300 100
    save 900 1

    # AOF : Journal append-only (durabilité)
    appendonly yes
    appendfsync everysec

    # Mémoire max : Limite selon RAM serveur
    # Exemple : 512MB sur serveur 2GB
    maxmemory 512mb

    # Éviction : Politique suppression clés si mémoire pleine
    # allkeys-lru : Supprime clés moins récemment utilisées (LRU)
    maxmemory-policy allkeys-lru

    # Logs
    loglevel notice
    logfile /var/log/redis/redis-server.log

    # Supervision (optionnel)
    supervised systemd
    ```

    **Redémarrer Redis après config :**

    ```bash
    sudo systemctl restart redis-server
    ```

    **Tester connexion avec password :**

    ```bash
    redis-cli
    127.0.0.1:6379> AUTH VOTRE_PASSWORD_REDIS_FORT
    OK
    127.0.0.1:6379> ping
    PONG
    127.0.0.1:6379> exit
    ```

    **Configurer Laravel pour utiliser Redis :**

    **Fichier : `config/database.php`** (vérifier configuration)

    ```php
    'redis' => [
        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
            'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        ],

        'default' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_DB', '0'),
        ],

        'cache' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_CACHE_DB', '1'),
        ],

        'session' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_SESSION_DB', '2'),
        ],
    ],
    ```

    **Installer extension PHP Redis :**

    ```bash
    # phpredis (extension native, plus performante)
    sudo apt install php8.2-redis
    
    # Ou predis (package PHP pur, fallback)
    composer require predis/predis
    
    # Redémarrer PHP-FPM
    sudo systemctl restart php8.2-fpm
    
    # Vérifier extension chargée
    php -m | grep redis
    # Doit afficher : redis
    ```

    **Tester connexion Laravel → Redis :**

    ```bash
    php artisan tinker
    
    # Tester cache Redis
    >>> Cache::put('test', 'Hello Redis', 60);
    >>> Cache::get('test');
    => "Hello Redis"
    
    # Vérifier dans Redis
    >>> exit
    
    redis-cli
    127.0.0.1:6379> AUTH VOTRE_PASSWORD
    OK
    127.0.0.1:6379> KEYS *test*
    1) "blog_cache_:test"
    127.0.0.1:6379> GET blog_cache_:test
    "s:11:\"Hello Redis\";"
    ```

??? abstract "7.5.4 : Vérification Configuration (Commandes Artisan)"

    **Commandes vérification pré-déploiement :**

    **Script vérification automatique :**

    **Fichier : `scripts/verify-production-config.sh`**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT VÉRIFICATION CONFIGURATION PRODUCTION
    ###############################################################################
    #
    # Usage : bash scripts/verify-production-config.sh
    #
    # Vérifie :
    # - Variables environnement critiques
    # - Connexions services (BDD, Redis, Mail)
    # - Permissions fichiers
    # - Optimisations actives
    #
    ###############################################################################

    echo "🔍 Vérification configuration production Laravel..."
    echo ""

    ###############################################################################
    # COULEURS (pour affichage terminal)
    ###############################################################################
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color

    ###############################################################################
    # COMPTEURS
    ###############################################################################
    ERRORS=0
    WARNINGS=0
    SUCCESS=0

    ###############################################################################
    # FONCTION : Vérifier variable .env
    ###############################################################################
    check_env() {
        local var_name=$1
        local expected=$2
        local value=$(grep "^${var_name}=" .env | cut -d '=' -f2)
        
        if [ "$value" == "$expected" ]; then
            echo -e "${GREEN}✅${NC} ${var_name}=${expected}"
            ((SUCCESS++))
        else
            echo -e "${RED}❌${NC} ${var_name}=${value} (attendu: ${expected})"
            ((ERRORS++))
        fi
    }

    ###############################################################################
    # FONCTION : Vérifier variable définie
    ###############################################################################
    check_env_set() {
        local var_name=$1
        local value=$(grep "^${var_name}=" .env | cut -d '=' -f2)
        
        if [ -n "$value" ]; then
            echo -e "${GREEN}✅${NC} ${var_name} défini"
            ((SUCCESS++))
        else
            echo -e "${RED}❌${NC} ${var_name} NON défini"
            ((ERRORS++))
        fi
    }

    ###############################################################################
    # ÉTAPE 1 : VÉRIFIER FICHIER .env EXISTE
    ###############################################################################
    echo "📋 Vérification fichier .env..."
    if [ -f .env ]; then
        echo -e "${GREEN}✅${NC} Fichier .env trouvé"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Fichier .env MANQUANT"
        echo "   Créer avec : cp .env.production.example .env"
        ((ERRORS++))
        exit 1
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 2 : VÉRIFIER VARIABLES CRITIQUES
    ###############################################################################
    echo "🔧 Vérification variables environnement critiques..."

    # APP_ENV doit être 'production'
    check_env "APP_ENV" "production"

    # APP_DEBUG doit être 'false'
    check_env "APP_DEBUG" "false"

    # APP_KEY doit être défini
    check_env_set "APP_KEY"

    # DB_PASSWORD doit être défini
    check_env_set "DB_PASSWORD"

    echo ""

    ###############################################################################
    # ÉTAPE 3 : TESTER CONNEXION BASE DE DONNÉES
    ###############################################################################
    echo "🗄️  Test connexion base de données..."
    if php artisan db:show > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} Connexion MySQL réussie"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Connexion MySQL ÉCHEC"
        echo "   Vérifier : DB_HOST, DB_USERNAME, DB_PASSWORD"
        ((ERRORS++))
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 4 : TESTER CONNEXION REDIS
    ###############################################################################
    echo "🔴 Test connexion Redis..."
    if php artisan tinker --execute="Cache::put('test', 'ok', 10); echo Cache::get('test');" | grep -q "ok"; then
        echo -e "${GREEN}✅${NC} Connexion Redis réussie"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Connexion Redis ÉCHEC (optionnel)"
        echo "   Cache utilisera driver 'file' (moins performant)"
        ((WARNINGS++))
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 5 : VÉRIFIER CACHES COMPILÉS
    ###############################################################################
    echo "⚡ Vérification caches optimisés..."

    # Config cache
    if [ -f bootstrap/cache/config.php ]; then
        echo -e "${GREEN}✅${NC} Config cache compilé"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Config cache manquant"
        echo "   Exécuter : php artisan config:cache"
        ((WARNINGS++))
    fi

    # Route cache
    if [ -f bootstrap/cache/routes-v7.php ]; then
        echo -e "${GREEN}✅${NC} Route cache compilé"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Route cache manquant"
        echo "   Exécuter : php artisan route:cache"
        ((WARNINGS++))
    fi

    # View cache
    if [ -d storage/framework/views ] && [ "$(ls -A storage/framework/views)" ]; then
        echo -e "${GREEN}✅${NC} View cache présent"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  View cache vide"
        echo "   Exécuter : php artisan view:cache"
        ((WARNINGS++))
    fi

    echo ""

    ###############################################################################
    # ÉTAPE 6 : VÉRIFIER PERMISSIONS FICHIERS
    ###############################################################################
    echo "🔐 Vérification permissions fichiers..."

    # .env doit être 600 (lisible propriétaire uniquement)
    ENV_PERMS=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null)
    if [ "$ENV_PERMS" == "600" ]; then
        echo -e "${GREEN}✅${NC} Permissions .env : 600 (sécurisé)"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Permissions .env : ${ENV_PERMS} (dangereux)"
        echo "   Corriger : chmod 600 .env"
        ((ERRORS++))
    fi

    # storage/ doit être 775
    STORAGE_PERMS=$(stat -c "%a" storage 2>/dev/null || stat -f "%A" storage 2>/dev/null)
    if [ "$STORAGE_PERMS" == "775" ]; then
        echo -e "${GREEN}✅${NC} Permissions storage/ : 775"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Permissions storage/ : ${STORAGE_PERMS}"
        echo "   Corriger : chmod -R 775 storage"
        ((WARNINGS++))
    fi

    echo ""

    ###############################################################################
    # ÉTAPE 7 : VÉRIFIER ASSETS COMPILÉS
    ###############################################################################
    echo "📦 Vérification assets production..."

    # Manifeste Vite doit exister
    if [ -f public/build/manifest.json ]; then
        echo -e "${GREEN}✅${NC} Assets Vite compilés"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Assets Vite NON compilés"
        echo "   Exécuter : npm run build"
        ((ERRORS++))
    fi

    echo ""

    ###############################################################################
    # RÉSUMÉ
    ###############################################################################
    echo "═══════════════════════════════════════════════════════════"
    echo "📊 RÉSUMÉ VÉRIFICATION"
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${GREEN}✅ Succès :${NC}       ${SUCCESS}"
    echo -e "${YELLOW}⚠️  Avertissements :${NC} ${WARNINGS}"
    echo -e "${RED}❌ Erreurs :${NC}      ${ERRORS}"
    echo ""

    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 Configuration production PARFAITE !${NC}"
        echo "   Prêt pour déploiement."
        exit 0
    elif [ $ERRORS -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Configuration fonctionnelle avec avertissements${NC}"
        echo "   Corriger les avertissements pour performances optimales."
        exit 0
    else
        echo -e "${RED}❌ Configuration INVALIDE${NC}"
        echo "   Corriger les erreurs avant déploiement."
        exit 1
    fi
    ```

    **Rendre le script exécutable :**

    ```bash
    chmod +x scripts/verify-production-config.sh
    ```

    **Exécuter vérification :**

    ```bash
    bash scripts/verify-production-config.sh
    ```

    **Résultat attendu :**

    ```
    🔍 Vérification configuration production Laravel...

    📋 Vérification fichier .env...
    ✅ Fichier .env trouvé

    🔧 Vérification variables environnement critiques...
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY défini
    ✅ DB_PASSWORD défini

    🗄️  Test connexion base de données...
    ✅ Connexion MySQL réussie

    🔴 Test connexion Redis...
    ✅ Connexion Redis réussie

    ⚡ Vérification caches optimisés...
    ✅ Config cache compilé
    ✅ Route cache compilé
    ✅ View cache présent

    🔐 Vérification permissions fichiers...
    ✅ Permissions .env : 600 (sécurisé)
    ✅ Permissions storage/ : 775

    📦 Vérification assets production...
    ✅ Assets Vite compilés

    ═══════════════════════════════════════════════════════════
    📊 RÉSUMÉ VÉRIFICATION
    ═══════════════════════════════════════════════════════════
    ✅ Succès :       13
    ⚠️  Avertissements : 0
    ❌ Erreurs :      0

    🎉 Configuration production PARFAITE !
       Prêt pour déploiement.
    ```

=== "**Checklist Configuration Production**"

    **Variables .env obligatoires :**

    ```bash
    # Application
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (php artisan key:generate)
    ✅ APP_URL=https://... (avec HTTPS)
    
    # Base de données
    ✅ DB_CONNECTION configuré
    ✅ DB_HOST défini
    ✅ DB_DATABASE créé
    ✅ DB_USERNAME dédié (pas root)
    ✅ DB_PASSWORD fort (16+ chars)
    
    # Cache/Sessions
    ✅ CACHE_DRIVER=redis (ou file si pas Redis)
    ✅ SESSION_DRIVER=redis (ou database)
    ✅ SESSION_SECURE_COOKIE=true (si HTTPS)
    
    # Redis (si utilisé)
    ✅ REDIS_PASSWORD défini
    ✅ REDIS_HOST correct
    
    # Mail
    ✅ MAIL_MAILER configuré
    ✅ MAIL_HOST défini
    ✅ MAIL_USERNAME défini
    ✅ MAIL_PASSWORD défini
    
    # Logging
    ✅ LOG_CHANNEL=daily
    ✅ LOG_LEVEL=error
    ```

=== "**Commandes Artisan Utiles Production**"

    ```bash
    # Afficher configuration complète
    php artisan config:show
    
    # Afficher infos base de données
    php artisan db:show
    
    # Lister toutes routes
    php artisan route:list
    
    # Tester connexion cache
    php artisan tinker
    >>> Cache::put('test', 'ok', 10);
    >>> Cache::get('test');
    
    # Tester envoi email
    php artisan tinker
    >>> Mail::raw('Test email', function($msg) {
        $msg->to('votre@email.com')->subject('Test');
    });
    
    # Vérifier queue workers
    php artisan queue:work --once
    
    # Clear tous les caches
    php artisan optimize:clear
    
    # Recompiler tous les caches
    php artisan optimize
    ```

=== "**Tableau Comparatif Drivers**"

    | Service | Driver Local | Driver Production | Avantages Production |
    |---------|-------------|-------------------|---------------------|
    | **Cache** | `file` | `redis` | × 50 plus rapide, partagé multi-serveurs |
    | **Session** | `file` | `redis` ou `database` | Scalable, persistant redémarrages |
    | **Queue** | `sync` | `redis` | Asynchrone, retry automatique, monitoring |
    | **Mail** | `log` | `smtp` ou `mailgun` | Délivrabilité, analytics, reputation |
    | **Logs** | `single` | `daily` | Rotation auto, disk non saturé |
    | **Filesystem** | `local` | `s3` | CDN, backups auto, scalable |

✅ **Étape 7.5 Terminée !**

**Fichiers créés :**

- `.env.production.example` : Template configuration production
- `scripts/verify-production-config.sh` : Script vérification automatique

**Concepts maîtrisés :**

- Configuration .env production complète
- Services externes (mail, cache, queue)
- Redis configuration sécurisée
- Vérification configuration automatisée
- Différences dev/staging/production
- Drivers optimaux par service

**Configuration production maintenant :**

- ✅ Variables environnement sécurisées
- ✅ Services externes configurés
- ✅ Redis cache + sessions + queue
- ✅ Logging optimisé
- ✅ Vérification automatisée
- ✅ Permissions correctes

**Prochaine étape :**

- 7.6 : Guide déploiement (serveur, domaine, SSL, mise en ligne)

Voulez-vous que je finalise avec l'étape 7.6 (Guide Déploiement Complet) pour clôturer la Phase 7 et le projet ?





### Étape 7.6 : Guide Déploiement Complet (OVH)

**Contexte :**

Le déploiement est l'étape finale : transformer application locale en site web accessible mondialement. Ce guide couvre **installation complète** d'un serveur production chez **OVH**, de la commande serveur jusqu'au premier visiteur.

!!! note "**Pourquoi OVH ?**"

    - ✅ **Hébergeur français** : Conformité RGPD, support français
    - ✅ **Tarifs compétitifs** : VPS dès 3,50€/mois HT
    - ✅ **Datacenters Europe** : Latence optimale France/Europe
    - ✅ **Bande passante illimitée** : Pas de surcoût trafic
    - ✅ **DDoS protection** : Incluse gratuitement

**Architecture déploiement :**

```
┌──────────────────────────────────────────────────────────┐
│                    INTERNET                              │
└────────────────────┬─────────────────────────────────────┘
                     │
            ┌────────▼────────┐
            │   DNS (OVH)     │ monblog.com → 51.83.45.123
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │  VPS OVH        │ Ubuntu 24.04 LTS
            │  51.83.45.123   │ 2 vCPU, 4GB RAM, 80GB SSD
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
   │  Nginx  │ │  PHP-FPM│ │  MySQL  │
   │  :80/443│ │  :9000  │ │  :3306  │
   └─────────┘ └─────────┘ └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
            ┌────────▼────────┐
            │ Laravel App     │ /var/www/blog
            │ + Redis (cache) │
            └─────────────────┘
```

---

??? abstract "7.6.1 : Commander et Configurer VPS OVH"

    **Étape 1 : Commander VPS OVH**

    **Se connecter : [ovh.com](https://www.ovh.com/fr/)**

    1. **Choisir VPS** → VPS → Découvrir nos VPS
    2. **Sélectionner gamme** :
       - **VPS Starter** : 3,50€/mois HT (1 vCPU, 2GB RAM) → Développement/Staging
       - **VPS Value** : 7€/mois HT (2 vCPU, 4GB RAM) → **RECOMMANDÉ Production**
       - **VPS Essential** : 14€/mois HT (2 vCPU, 8GB RAM) → Gros trafic

    **Configuration exemple (VPS Value) :**

    ```
    Gamme        : VPS Value
    Datacenter   : Gravelines (France) - GRA11
    OS           : Ubuntu 24.04 LTS
    Stockage     : 80 GB SSD NVMe
    RAM          : 4 GB
    CPU          : 2 vCores
    Bande passante : 500 Mbps (illimitée)
    IP           : 1 IPv4 dédiée
    
    Prix : 7€/mois HT (8,40€ TTC)
    Engagement : Mensuel (résiliable à tout moment)
    ```

    3. **Valider commande** → Paiement → Bon de commande N°12345678
    4. **Attendre provisionnement** : 10-30 minutes
    5. **Email confirmation** : Identifiants root + IP serveur

    **Email reçu (exemple simulé) :**

    ```
    ═══════════════════════════════════════════════════════════
    OVH - Votre VPS est prêt !
    ═══════════════════════════════════════════════════════════
    
    Votre serveur VPS vps-a1b2c3d4.vps.ovh.net est maintenant actif.
    
    Informations de connexion :
    ────────────────────────────────────────────────────────────
    Adresse IP     : 51.83.45.123
    Hostname       : vps-a1b2c3d4.vps.ovh.net
    OS             : Ubuntu 24.04 LTS
    Utilisateur    : root
    Mot de passe   : Kf8mP2xQw9nRt3sV
    
    Connexion SSH  : ssh root@51.83.45.123
    Panel OVH      : https://www.ovh.com/manager/dedicated/#/vps/vps-a1b2c3d4.vps.ovh.net
    ────────────────────────────────────────────────────────────
    
    ⚠️  Changez immédiatement le mot de passe root !
    ```

    **Étape 2 : Première connexion SSH**

    ```bash
    # Depuis votre machine locale
    ssh root@51.83.45.123
    
    # Saisir password temporaire : Kf8mP2xQw9nRt3sV
    
    # Premier message Ubuntu
    Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-49-generic x86_64)
    
    # Changer password root immédiatement
    passwd
    # Saisir nouveau password fort (16+ chars)
    # Exemple : 7Kf2mP9xQw3nRt8sVb4cYh6dJl1a
    ```

    **Étape 3 : Mise à jour système**

    ```bash
    # Mettre à jour cache packages
    apt update
    
    # Installer toutes mises à jour disponibles
    apt upgrade -y
    
    # Installer packages essentiels
    apt install -y \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates
    
    # Configurer timezone
    timedatectl set-timezone Europe/Paris
    
    # Vérifier
    date
    # Résultat : jeu. 11 déc. 2024 14:30:25 CET
    ```

    **Étape 4 : Créer utilisateur dédié (sécurité)**

    ```bash
    # Créer utilisateur 'deploy' (pas root pour Laravel)
    adduser deploy
    # Password : 9Xm2pL7wQz5nRv8tYc4b
    # Infos : Laisser vides (Enter x5)
    
    # Ajouter au groupe sudo
    usermod -aG sudo deploy
    
    # Autoriser connexion SSH utilisateur deploy
    mkdir -p /home/deploy/.ssh
    cp /root/.ssh/authorized_keys /home/deploy/.ssh/ 2>/dev/null || echo "Pas de clés SSH root"
    chown -R deploy:deploy /home/deploy/.ssh
    chmod 700 /home/deploy/.ssh
    chmod 600 /home/deploy/.ssh/authorized_keys 2>/dev/null || true
    
    # Tester connexion (depuis local)
    ssh deploy@51.83.45.123
    ```

??? abstract "7.6.2 : Installation Stack LEMP (Linux + Nginx + MySQL + PHP)"

    **Contexte :**

    **LEMP** = Linux + Nginx + MySQL + PHP. Stack moderne haute performance pour Laravel.

    **Installer Nginx (serveur web)**

    ```bash
    # Installer Nginx
    sudo apt install -y nginx
    
    # Démarrer et activer au boot
    sudo systemctl start nginx
    sudo systemctl enable nginx
    
    # Vérifier statut
    sudo systemctl status nginx
    # ● nginx.service - A high performance web server
    #    Active: active (running)
    
    # Tester
    curl http://localhost
    # Doit afficher page "Welcome to nginx!"
    ```

    **Installer PHP 8.2 + Extensions Laravel**

    ```bash
    # Ajouter repository PHP (ondrej/php)
    sudo add-apt-repository ppa:ondrej/php -y
    sudo apt update
    
    # Installer PHP 8.2 + extensions
    sudo apt install -y \
        php8.2-fpm \
        php8.2-cli \
        php8.2-common \
        php8.2-mysql \
        php8.2-zip \
        php8.2-gd \
        php8.2-mbstring \
        php8.2-curl \
        php8.2-xml \
        php8.2-bcmath \
        php8.2-redis \
        php8.2-intl
    
    # Vérifier version PHP
    php -v
    # PHP 8.2.25 (cli) (built: Nov 21 2024 15:37:21) (NTS)
    
    # Démarrer PHP-FPM
    sudo systemctl start php8.2-fpm
    sudo systemctl enable php8.2-fpm
    
    # Vérifier statut
    sudo systemctl status php8.2-fpm
    # ● php8.2-fpm.service - The PHP 8.2 FastCGI Process Manager
    #    Active: active (running)
    ```

    **Optimiser PHP pour production**

    ```bash
    # Éditer configuration PHP-FPM
    sudo nano /etc/php/8.2/fpm/php.ini
    ```

    **Modifications `php.ini` :**

    ```ini
    ; Mémoire allouée par script (Laravel peut consommer)
    memory_limit = 256M
    
    ; Taille max upload (images articles)
    upload_max_filesize = 20M
    post_max_size = 20M
    
    ; Temps exécution max (import données, migrations)
    max_execution_time = 60
    
    ; Affichage erreurs : DÉSACTIVER en production
    display_errors = Off
    log_errors = On
    error_reporting = E_ALL & ~E_DEPRECATED & ~E_STRICT
    
    ; Sessions sécurisées
    session.cookie_httponly = 1
    session.cookie_secure = 1
    session.use_strict_mode = 1
    
    ; Opcache : Cache bytecode PHP (× 3 performances)
    opcache.enable = 1
    opcache.memory_consumption = 128
    opcache.interned_strings_buffer = 8
    opcache.max_accelerated_files = 10000
    opcache.validate_timestamps = 0
    opcache.save_comments = 1
    opcache.fast_shutdown = 1
    ```

    **Redémarrer PHP-FPM :**

    ```bash
    sudo systemctl restart php8.2-fpm
    ```

    **Installer MySQL 8.0**

    ```bash
    # Installer serveur MySQL
    sudo apt install -y mysql-server
    
    # Démarrer et activer
    sudo systemctl start mysql
    sudo systemctl enable mysql
    
    # Sécuriser installation
    sudo mysql_secure_installation
    
    # Réponses recommandées :
    # - VALIDATE PASSWORD COMPONENT ? Y
    # - Password validation policy ? 1 (MEDIUM)
    # - New root password : 5Rt8Yc2bHf9xQw1mKl6pNz3d
    # - Remove anonymous users ? Y
    # - Disallow root login remotely ? Y
    # - Remove test database ? Y
    # - Reload privilege tables ? Y
    ```

    **Créer base de données + utilisateur Laravel :**

    ```bash
    # Connexion MySQL root
    sudo mysql -u root -p
    # Saisir password root : 5Rt8Yc2bHf9xQw1mKl6pNz3d
    ```

    **Dans console MySQL :**

    ```sql
    -- Créer base de données
    CREATE DATABASE blog_production CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
    -- Créer utilisateur dédié
    CREATE USER 'blog_user'@'localhost' IDENTIFIED BY '7Kf2mP9xQw3nRt8sVb4cYh6d';
    
    -- Accorder privilèges
    GRANT ALL PRIVILEGES ON blog_production.* TO 'blog_user'@'localhost';
    
    -- Appliquer changements
    FLUSH PRIVILEGES;
    
    -- Vérifier
    SHOW DATABASES;
    -- +--------------------+
    -- | Database           |
    -- +--------------------+
    -- | blog_production    |
    -- | information_schema |
    -- | mysql              |
    -- | performance_schema |
    -- | sys                |
    -- +--------------------+
    
    -- Quitter
    EXIT;
    ```

    **Tester connexion utilisateur Laravel :**

    ```bash
    mysql -u blog_user -p blog_production
    # Password : 7Kf2mP9xQw3nRt8sVb4cYh6d
    # Doit afficher : mysql>
    
    EXIT;
    ```

    **Installer Redis (cache + sessions)**

    ```bash
    # Installer serveur Redis
    sudo apt install -y redis-server
    
    # Configurer Redis pour systemd
    sudo nano /etc/redis/redis.conf
    ```

    **Modifications `redis.conf` :**

    ```conf
    # Supervision systemd
    supervised systemd
    
    # Bind localhost uniquement (sécurité)
    bind 127.0.0.1
    
    # Password obligatoire production
    requirepass 9Xm2pL7wQz5nRv8tYc4bHf6g
    
    # Persistence activée
    appendonly yes
    
    # Mémoire max 512MB
    maxmemory 512mb
    maxmemory-policy allkeys-lru
    ```

    **Redémarrer Redis :**

    ```bash
    sudo systemctl restart redis-server
    sudo systemctl enable redis-server
    
    # Tester connexion
    redis-cli
    127.0.0.1:6379> AUTH 9Xm2pL7wQz5nRv8tYc4bHf6g
    OK
    127.0.0.1:6379> PING
    PONG
    127.0.0.1:6379> exit
    ```

??? abstract "7.6.3 : Installation Composer et Node.js"

    **Installer Composer (gestionnaire dépendances PHP)**

    ```bash
    # Télécharger installateur Composer
    cd ~
    curl -sS https://getcomposer.org/installer -o composer-setup.php
    
    # Vérifier hash SHA-384 (sécurité)
    HASH="$(curl -sS https://composer.github.io/installer.sig)"
    php -r "if (hash_file('sha384', 'composer-setup.php') === '$HASH') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
    # Doit afficher : Installer verified
    
    # Installer Composer globalement
    sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer
    
    # Nettoyer
    rm composer-setup.php
    
    # Vérifier installation
    composer --version
    # Composer version 2.8.3 2024-11-20 15:37:25
    ```

    **Installer Node.js 20 LTS (pour Vite)**

    ```bash
    # Ajouter repository NodeSource
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    
    # Installer Node.js + npm
    sudo apt install -y nodejs
    
    # Vérifier versions
    node -v
    # v20.11.0
    
    npm -v
    # 10.2.4
    ```

??? abstract "7.6.4 : Configuration Nginx pour Laravel"

    **Créer configuration site Laravel**

    ```bash
    # Créer fichier configuration
    sudo nano /etc/nginx/sites-available/blog
    ```

    **Contenu `/etc/nginx/sites-available/blog` :**

    ```nginx
    ###############################################################################
    # CONFIGURATION NGINX - LARAVEL BLOG PRODUCTION
    ###############################################################################
    # Domain: monblog.com
    # Root: /var/www/blog/public
    ###############################################################################

    # Redirection HTTP → HTTPS (après installation SSL)
    server {
        listen 80;
        listen [::]:80;
        server_name monblog.com www.monblog.com;

        # Temporairement : autoriser trafic HTTP (avant SSL)
        # Après SSL : décommenter redirection
        # return 301 https://$server_name$request_uri;

        root /var/www/blog/public;
        index index.php index.html;

        # Logs
        access_log /var/log/nginx/blog-access.log;
        error_log /var/log/nginx/blog-error.log;

        # Bloquer fichiers sensibles
        location ~ /\.(env|git|svn) {
            deny all;
            return 404;
        }

        # Route Laravel (try_files)
        location / {
            try_files $uri $uri/ /index.php?$query_string;
        }

        # PHP-FPM
        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;

            # Timeout généreux pour migrations
            fastcgi_read_timeout 300;
        }

        # Cache assets statiques (CSS, JS, images)
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Bloquer accès storage/ (fichiers privés)
        location ^~ /storage/ {
            deny all;
        }

        # Bloquer accès bootstrap/cache/
        location ^~ /bootstrap/cache/ {
            deny all;
        }
    }

    # Configuration HTTPS (à activer après Let's Encrypt)
    # server {
    #     listen 443 ssl http2;
    #     listen [::]:443 ssl http2;
    #     server_name monblog.com www.monblog.com;
    #
    #     root /var/www/blog/public;
    #     index index.php index.html;
    #
    #     # Certificats SSL (générés par Certbot)
    #     ssl_certificate /etc/letsencrypt/live/monblog.com/fullchain.pem;
    #     ssl_certificate_key /etc/letsencrypt/live/monblog.com/privkey.pem;
    #
    #     # Configuration SSL moderne
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers HIGH:!aNULL:!MD5;
    #     ssl_prefer_server_ciphers on;
    #
    #     # HSTS (6 mois)
    #     add_header Strict-Transport-Security "max-age=15768000; includeSubDomains" always;
    #
    #     # [... Copier sections location depuis bloc HTTP ci-dessus ...]
    # }
    ```

    **Activer site et redémarrer Nginx :**

    ```bash
    # Créer lien symbolique sites-enabled
    sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
    
    # Supprimer site par défaut
    sudo rm /etc/nginx/sites-enabled/default
    
    # Tester configuration Nginx
    sudo nginx -t
    # nginx: configuration file /etc/nginx/nginx.conf test is successful
    
    # Redémarrer Nginx
    sudo systemctl restart nginx
    ```

??? abstract "7.6.5 : Déploiement Code Laravel via Git"

    **Étape 1 : Créer répertoire application**

    ```bash
    # Créer répertoire web
    sudo mkdir -p /var/www/blog
    
    # Donner ownership à utilisateur deploy
    sudo chown -R deploy:deploy /var/www/blog
    
    # Naviguer dans répertoire
    cd /var/www/blog
    ```

    **Étape 2 : Cloner repository Git**

    !!! note "**Prérequis : Code doit être sur Git (GitHub, GitLab, Bitbucket)**"
        Si pas encore versionné :
        ```bash
        # Sur machine locale
        git init
        git add .
        git commit -m "Initial commit"
        git remote add origin https://github.com/votre-username/laravel-blog.git
        git push -u origin main
        ```

    **Sur serveur :**

    ```bash
    # Cloner repository (exemple GitHub)
    git clone https://github.com/votre-username/laravel-blog.git .
    
    # Ou avec authentification si repository privé
    git clone https://votre-token@github.com/votre-username/laravel-blog.git .
    
    # Vérifier fichiers présents
    ls -la
    # drwxr-xr-x  app/
    # drwxr-xr-x  bootstrap/
    # -rw-r--r--  composer.json
    # drwxr-xr-x  config/
    # ...
    ```

    **Étape 3 : Installer dépendances Composer**

    ```bash
    # Installer dépendances PHP (production, optimisé)
    composer install --optimize-autoloader --no-dev
    
    # --optimize-autoloader : Autoloader optimisé (× 4 performances)
    # --no-dev : Exclut packages développement (tests, debugbar)
    
    # Temps installation : 2-5 minutes
    # Résultat : vendor/ créé avec toutes dépendances
    ```

    **Étape 4 : Installer dépendances npm et compiler assets**

    ```bash
    # Installer dépendances JavaScript
    npm ci
    # ci = clean install (reproductible, basé package-lock.json)
    
    # Compiler assets production
    npm run build
    
    # Résultat : public/build/ créé avec :
    # - assets/app-a3f2c1b9.css (minifié)
    # - assets/app-b7e4d3a1.js (minifié)
    # - manifest.json (références assets)
    ```

    **Étape 5 : Créer fichier .env production**

    ```bash
    # Copier template
    cp .env.production.example .env
    
    # Éditer avec vraies valeurs
    nano .env
    ```

    **Contenu `.env` production (exemple) :**

    ```bash
    APP_NAME="Mon Blog"
    APP_ENV=production
    APP_KEY=  # Sera généré étape suivante
    APP_DEBUG=false
    APP_URL=https://monblog.com

    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=blog_production
    DB_USERNAME=blog_user
    DB_PASSWORD=7Kf2mP9xQw3nRt8sVb4cYh6d

    CACHE_DRIVER=redis
    SESSION_DRIVER=redis
    SESSION_SECURE_COOKIE=true
    QUEUE_CONNECTION=redis

    REDIS_HOST=127.0.0.1
    REDIS_PORT=6379
    REDIS_PASSWORD=9Xm2pL7wQz5nRv8tYc4bHf6g
    REDIS_CACHE_DB=0
    REDIS_SESSION_DB=1
    REDIS_QUEUE_DB=2

    MAIL_MAILER=smtp
    MAIL_HOST=smtp-relay.brevo.com
    MAIL_PORT=587
    MAIL_USERNAME=votre-email@example.com
    MAIL_PASSWORD=votre-cle-api-brevo
    MAIL_FROM_ADDRESS=noreply@monblog.com
    MAIL_FROM_NAME="${APP_NAME}"

    LOG_CHANNEL=daily
    LOG_LEVEL=error
    ```

    **Étape 6 : Initialiser application Laravel**

    ```bash
    # Générer clé application (APP_KEY)
    php artisan key:generate
    # Application key set successfully.
    
    # Créer lien symbolique storage
    php artisan storage:link
    # The [public/storage] link has been connected to [storage/app/public].
    
    # Exécuter migrations (créer tables BDD)
    php artisan migrate --force
    # --force : Nécessaire car APP_ENV=production (confirmation automatique)
    
    # Résultat :
    # Migration table created successfully.
    # Migrating: 2014_10_12_000000_create_users_table
    # Migrated:  2014_10_12_000000_create_users_table (45.23ms)
    # ...
    
    # Seeders (données initiales - optionnel)
    php artisan db:seed --force
    # Database seeding completed successfully.
    ```

    **Étape 7 : Optimiser Laravel pour production**

    ```bash
    # Compiler caches optimisés
    php artisan config:cache
    php artisan route:cache
    php artisan view:cache
    php artisan event:cache
    
    # Résultat :
    # Configuration cache cleared successfully.
    # Configuration cached successfully.
    # ...
    ```

    **Étape 8 : Configurer permissions**

    ```bash
    # Propriétaire : utilisateur deploy
    sudo chown -R deploy:www-data /var/www/blog
    
    # Permissions dossiers
    sudo find /var/www/blog -type d -exec chmod 755 {} \;
    
    # Permissions fichiers
    sudo find /var/www/blog -type f -exec chmod 644 {} \;
    
    # Storage et cache : écriture www-data (Nginx)
    sudo chmod -R 775 /var/www/blog/storage
    sudo chmod -R 775 /var/www/blog/bootstrap/cache
    
    # .env : lecture propriétaire uniquement
    chmod 600 /var/www/blog/.env
    ```

    **Étape 9 : Tester application**

    ```bash
    # Vérifier configuration
    php artisan config:show
    
    # Tester connexion BDD
    php artisan db:show
    # MySQL 8.0.40 ··············································· blog_production
    
    # Tester routes
    php artisan route:list --columns=method,uri,name
    
    # Vérifier cache Redis
    php artisan tinker
    >>> Cache::put('test', 'ok', 60);
    >>> Cache::get('test');
    => "ok"
    >>> exit
    ```

??? abstract "7.6.6 : Configuration DNS et Domaine OVH"

    **Contexte :**

    Le domaine `monblog.com` doit pointer vers IP serveur `51.83.45.123`. Configuration via DNS OVH.

    **Étape 1 : Acheter domaine OVH (si pas déjà fait)**

    1. **OVH → Domaines → Commander**
    2. **Rechercher** : `monblog.com`
    3. **Vérifier disponibilité** : Disponible ✅
    4. **Tarif** : 6,99€ HT/an (TLD .com)
    5. **Valider commande** → Paiement

    **Étape 2 : Configurer zone DNS**

    **Se connecter : [ovh.com/manager](https://www.ovh.com/manager/web/)**

    1. **Domaines** → Sélectionner `monblog.com`
    2. **Zone DNS** → Modifier
    3. **Supprimer entrées existantes** (parking OVH)
    4. **Ajouter enregistrements DNS** :

    **Enregistrements à créer :**

    | Type | Sous-domaine | Cible | TTL |
    |------|-------------|-------|-----|
    | **A** | @ | 51.83.45.123 | 3600 |
    | **A** | www | 51.83.45.123 | 3600 |
    | **AAAA** | @ | 2001:41d0:... | 3600 |
    | **AAAA** | www | 2001:41d0:... | 3600 |

    !!! note "**Explications enregistrements :**"
        - **A** : Associe domaine à IPv4
        - **AAAA** : Associe domaine à IPv6 (optionnel)
        - **@** : Domaine principal (monblog.com)
        - **www** : Sous-domaine (www.monblog.com)
        - **TTL** : Durée cache (3600s = 1h)

    **Dans interface OVH :**

    ```
    Ajouter une entrée
    ─────────────────────────────────────────
    Type d'enregistrement : A
    Sous-domaine          : [laisser vide = @]
    Cible                 : 51.83.45.123
    TTL                   : 3600
    
    [Valider]
    
    Ajouter une entrée
    ─────────────────────────────────────────
    Type d'enregistrement : A
    Sous-domaine          : www
    Cible                 : 51.83.45.123
    TTL                   : 3600
    
    [Valider]
    ```

    **Étape 3 : Attendre propagation DNS**

    ```bash
    # Propagation DNS : 10 minutes - 24 heures (généralement <1h)
    
    # Vérifier propagation (depuis local)
    dig monblog.com +short
    # 51.83.45.123
    
    dig www.monblog.com +short
    # 51.83.45.123
    
    # Ou via service en ligne
    # https://www.whatsmydns.net/#A/monblog.com
    ```

    **Étape 4 : Tester accès HTTP**

    ```bash
    # Ouvrir navigateur
    http://monblog.com
    
    # Doit afficher page d'accueil Laravel
    # ⚠️ HTTP (pas sécurisé) - SSL prochaine étape
    ```

??? abstract "7.6.7 : Installation Certificat SSL (Let's Encrypt)"

    **Contexte :**

    **Let's Encrypt** fournit certificats SSL **gratuits** valides 90 jours (renouvellement automatique).

    **Étape 1 : Installer Certbot**

    ```bash
    # Installer Certbot + plugin Nginx
    sudo apt install -y certbot python3-certbot-nginx
    ```

    **Étape 2 : Obtenir certificat SSL**

    ```bash
    # Certbot mode automatique (modifie config Nginx)
    sudo certbot --nginx -d monblog.com -d www.monblog.com
    
    # Réponses interactives :
    # Email (notifications expiration) : votre@email.com
    # Terms of Service : (A)gree
    # Share email with EFF : (N)o
    # Redirect HTTP → HTTPS : 2 (Yes, redirect)
    
    # Certbot :
    # - Vérifie contrôle domaine (challenge HTTP)
    # - Génère certificats
    # - Modifie /etc/nginx/sites-available/blog (ajoute SSL)
    # - Recharge Nginx
    
    # Résultat :
    # Successfully received certificate.
    # Certificate is saved at: /etc/letsencrypt/live/monblog.com/fullchain.pem
    # Key is saved at:         /etc/letsencrypt/live/monblog.com/privkey.pem
    ```

    **Étape 3 : Vérifier renouvellement automatique**

    ```bash
    # Certbot installe cron job automatique
    # Tester renouvellement (dry-run)
    sudo certbot renew --dry-run
    
    # Résultat :
    # Congratulations, all simulated renewals succeeded:
    #   /etc/letsencrypt/live/monblog.com/fullchain.pem (success)
    ```

    **Étape 4 : Tester SSL**

    ```bash
    # Ouvrir navigateur
    https://monblog.com
    
    # Vérifier :
    # ✅ Cadenas vert (connexion sécurisée)
    # ✅ Certificat valide (Let's Encrypt Authority X3)
    # ✅ Expiration dans 90 jours
    
    # Test automatique
    # https://www.ssllabs.com/ssltest/analyze.html?d=monblog.com
    # Score attendu : A ou A+
    ```

    **Configuration Nginx post-Certbot :**

    Certbot a modifié `/etc/nginx/sites-available/blog` automatiquement :

    ```nginx
    # HTTP → HTTPS redirect (ajouté par Certbot)
    server {
        listen 80;
        server_name monblog.com www.monblog.com;
        
        return 301 https://$server_name$request_uri;
    }

    # HTTPS (ajouté par Certbot)
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name monblog.com www.monblog.com;

        root /var/www/blog/public;
        index index.php index.html;

        # Certificats SSL (gérés par Certbot)
        ssl_certificate /etc/letsencrypt/live/monblog.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/monblog.com/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        # [... reste configuration identique ...]
    }
    ```

??? abstract "7.6.8 : Configuration Firewall UFW"

    **Contexte :**

    **UFW** (Uncomplicated Firewall) bloque trafic non autorisé. Ouvrir seulement ports nécessaires.

    **Installer et configurer UFW :**

    ```bash
    # Installer UFW
    sudo apt install -y ufw
    
    # Configurer règles (AVANT d'activer)
    
    # Autoriser SSH (CRITIQUE - sinon perte accès serveur)
    sudo ufw allow 22/tcp
    
    # Autoriser HTTP (port 80)
    sudo ufw allow 80/tcp
    
    # Autoriser HTTPS (port 443)
    sudo ufw allow 443/tcp
    
    # Politique par défaut : refuser tout le reste
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Activer firewall
    sudo ufw enable
    # Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
    # Firewall is active and enabled on system startup
    
    # Vérifier statut
    sudo ufw status verbose
    
    # Status: active
    # 
    # To                         Action      From
    # --                         ------      ----
    # 22/tcp                     ALLOW       Anywhere
    # 80/tcp                     ALLOW       Anywhere
    # 443/tcp                    ALLOW       Anywhere
    ```

    !!! warning "**ATTENTION : Ne pas bloquer port SSH (22)**"
        Bloquer SSH = perte accès serveur définitive (nécessite console rescue OVH)

??? abstract "7.6.9 : Configuration Supervisor (Queue Workers)"

    **Contexte :**

    **Supervisor** maintient workers queue Redis actifs (traitement jobs asynchrones : emails, notifications).

    **Installer Supervisor :**

    ```bash
    sudo apt install -y supervisor
    ```

    **Créer configuration worker Laravel :**

    ```bash
    sudo nano /etc/supervisor/conf.d/laravel-worker.conf
    ```

    **Contenu `laravel-worker.conf` :**

    ```ini
    [program:laravel-worker]
    process_name=%(program_name)s_%(process_num)02d
    command=php /var/www/blog/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true
    user=deploy
    numprocs=2
    redirect_stderr=true
    stdout_logfile=/var/www/blog/storage/logs/worker.log
    stopwaitsecs=3600
    ```

    !!! note "**Explications configuration :**"
        - `command` : Commande worker Laravel
        - `--sleep=3` : Pause 3s entre vérifications queue
        - `--tries=3` : 3 tentatives avant échec définitif
        - `--max-time=3600` : Redémarre worker après 1h (libère mémoire)
        - `numprocs=2` : 2 workers parallèles (augmenter si beaucoup de jobs)
        - `user=deploy` : Exécute comme utilisateur deploy (pas root)

    **Démarrer workers :**

    ```bash
    # Recharger configuration Supervisor
    sudo supervisorctl reread
    # laravel-worker: available
    
    sudo supervisorctl update
    # laravel-worker: added process group
    
    # Démarrer workers
    sudo supervisorctl start laravel-worker:*
    # laravel-worker:laravel-worker_00: started
    # laravel-worker:laravel-worker_01: started
    
    # Vérifier statut
    sudo supervisorctl status
    # laravel-worker:laravel-worker_00   RUNNING   pid 12345, uptime 0:00:05
    # laravel-worker:laravel-worker_01   RUNNING   pid 12346, uptime 0:00:05
    ```

    **Commandes utiles Supervisor :**

    ```bash
    # Redémarrer workers (après déploiement code)
    sudo supervisorctl restart laravel-worker:*
    
    # Arrêter workers
    sudo supervisorctl stop laravel-worker:*
    
    # Voir logs worker
    sudo supervisorctl tail -f laravel-worker:laravel-worker_00
    ```

=== "**Checklist Post-Déploiement**"

    **Vérifier tous services fonctionnent :**

    ```bash
    # ✅ Nginx actif
    sudo systemctl status nginx | grep Active
    # Active: active (running)
    
    # ✅ PHP-FPM actif
    sudo systemctl status php8.2-fpm | grep Active
    # Active: active (running)
    
    # ✅ MySQL actif
    sudo systemctl status mysql | grep Active
    # Active: active (running)
    
    # ✅ Redis actif
    sudo systemctl status redis-server | grep Active
    # Active: active (running)
    
    # ✅ Supervisor actif
    sudo systemctl status supervisor | grep Active
    # Active: active (running)
    
    # ✅ Workers queue actifs
    sudo supervisorctl status
    # laravel-worker:laravel-worker_00   RUNNING
    ```

    **Tester fonctionnalités critiques :**

    ```bash
    # ✅ Page d'accueil charge
    curl -I https://monblog.com
    # HTTP/2 200
    
    # ✅ Connexion BDD fonctionne
    php artisan db:show
    
    # ✅ Cache Redis fonctionne
    php artisan tinker --execute="Cache::put('test', 'ok'); echo Cache::get('test');"
    # ok
    
    # ✅ Emails envoient (test)
    php artisan tinker --execute="Mail::raw('Test', fn(\$m) => \$m->to('test@example.com')->subject('Test'));"
    # Vérifier réception email
    ```

=== "**Script Déploiement Automatique**"

    **Créer script mise à jour production :**

    **Fichier : `deploy.sh` (racine projet)**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT DÉPLOIEMENT PRODUCTION - LARAVEL BLOG
    ###############################################################################
    # 
    # Usage : bash deploy.sh
    # 
    # Workflow :
    # 1. Pull code Git
    # 2. Installer dépendances Composer/npm
    # 3. Compiler assets
    # 4. Exécuter migrations
    # 5. Clear + recache optimisations
    # 6. Redémarrer services
    #
    ###############################################################################

    echo "🚀 Déploiement Laravel Blog Production..."
    echo ""

    # Mode maintenance (évite requêtes pendant déploiement)
    php artisan down --message="Mise à jour en cours" --retry=60

    # Pull dernières modifications Git
    echo "📥 Pull code Git..."
    git pull origin main

    # Installer dépendances Composer (production optimisé)
    echo "📦 Installation dépendances Composer..."
    composer install --optimize-autoloader --no-dev

    # Installer dépendances npm
    echo "📦 Installation dépendances npm..."
    npm ci

    # Compiler assets production
    echo "⚡ Compilation assets Vite..."
    npm run build

    # Exécuter migrations BDD
    echo "🗄️  Exécution migrations..."
    php artisan migrate --force

    # Clear tous caches
    echo "🧹 Nettoyage caches..."
    php artisan cache:clear
    php artisan config:clear
    php artisan route:clear
    php artisan view:clear

    # Recréer caches optimisés
    echo "⚡ Recompilation caches..."
    php artisan config:cache
    php artisan route:cache
    php artisan view:cache
    php artisan event:cache

    # Redémarrer queue workers
    echo "🔄 Redémarrage workers..."
    sudo supervisorctl restart laravel-worker:*

    # Redémarrer PHP-FPM
    echo "🔄 Redémarrage PHP-FPM..."
    sudo systemctl restart php8.2-fpm

    # Désactiver mode maintenance
    php artisan up

    echo ""
    echo "✅ Déploiement terminé avec succès !"
    echo ""
    echo "Vérifier : https://monblog.com"
    ```

    **Rendre exécutable et utiliser :**

    ```bash
    chmod +x deploy.sh
    
    # Déployer nouvelle version
    bash deploy.sh
    ```

=== "**Monitoring et Logs**"

    **Consulter logs application :**

    ```bash
    # Logs Laravel (storage/logs/)
    tail -f /var/www/blog/storage/logs/laravel.log
    
    # Logs Nginx (accès)
    tail -f /var/log/nginx/blog-access.log
    
    # Logs Nginx (erreurs)
    tail -f /var/log/nginx/blog-error.log
    
    # Logs PHP-FPM
    tail -f /var/log/php8.2-fpm.log
    
    # Logs workers queue
    tail -f /var/www/blog/storage/logs/worker.log
    ```

    **Installer monitoring (optionnel) :**

    ```bash
    # Installer netdata (monitoring temps réel)
    bash <(curl -Ss https://my-netdata.io/kickstart.sh)
    
    # Accès dashboard : http://51.83.45.123:19999
    # Métriques : CPU, RAM, disk, réseau, MySQL, Nginx, Redis
    ```

=== "**Maintenance Régulière**"

    **Tâches hebdomadaires :**

    ```bash
    # Mise à jour système
    sudo apt update && sudo apt upgrade -y
    
    # Nettoyer logs anciens (>30 jours)
    find /var/www/blog/storage/logs/*.log -mtime +30 -delete
    
    # Vérifier espace disque
    df -h
    ```

    **Tâches mensuelles :**

    ```bash
    # Optimiser tables MySQL
    sudo mysqlcheck -o --all-databases -u root -p
    
    # Backup base de données
    mysqldump -u blog_user -p blog_production > backup_$(date +%Y%m%d).sql
    
    # Compresser backup
    gzip backup_$(date +%Y%m%d).sql
    ```

    **Configurer backups automatiques (optionnel) :**

    ```bash
    # Créer script backup
    sudo nano /usr/local/bin/backup-blog.sh
    ```

    ```bash
    #!/bin/bash
    BACKUP_DIR="/home/deploy/backups"
    DATE=$(date +%Y%m%d_%H%M%S)
    
    # Backup BDD
    mysqldump -u blog_user -p'7Kf2mP9xQw3nRt8sVb4cYh6d' blog_production | gzip > $BACKUP_DIR/db_$DATE.sql.gz
    
    # Backup fichiers (uploads)
    tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /var/www/blog/storage/app/public
    
    # Supprimer backups >7 jours
    find $BACKUP_DIR -mtime +7 -delete
    ```

    **Cron job (exécution quotidienne 3h du matin) :**

    ```bash
    sudo crontab -e
    
    # Ajouter ligne :
    0 3 * * * /usr/local/bin/backup-blog.sh
    ```

✅ **Étape 7.6 Terminée complètement !**

✅ **PROJET LARAVEL BLOG MULTI-AUTEURS 100% TERMINÉ !**

**Infrastructure déployée :**

- ✅ VPS OVH (51.83.45.123) - Ubuntu 24.04 LTS
- ✅ Stack LEMP (Nginx + PHP 8.2 + MySQL 8.0 + Redis)
- ✅ Application Laravel production-ready
- ✅ Domaine configuré (monblog.com)
- ✅ SSL Let's Encrypt (HTTPS)
- ✅ Firewall UFW actif
- ✅ Queue workers Supervisor
- ✅ Script déploiement automatique

**URLs actives (simulation) :**

- 🌐 **Site web** : https://monblog.com
- 🔒 **SSL** : A+ (SSL Labs)
- 📊 **Monitoring** : http://51.83.45.123:19999
- 📧 **Email** : noreply@monblog.com

**Performances production :**

- ⚡ **TTFB** : <100ms
- ⚡ **Page complète** : <500ms
- ⚡ **Requêtes SQL** : 3 (Eager Loading)
- ⚡ **Score PageSpeed** : 90+ (prévu)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les kits de démarrage Laravel font gagner des semaines de développement, mais ils imposent de bien comprendre les flux sous-jacents. Ne traitez jamais l'authentification comme une simple boîte noire.

> [Passer à la phase suivante →](../index.md)
