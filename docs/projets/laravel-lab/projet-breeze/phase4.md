---
description: "Création de 7 contrôleurs avec CRUD complet, validation formulaires, ownership et logique métier articles/commentaires."
icon: lucide/cpu
tags: ["CONTROLLERS", "CRUD", "VALIDATION", "BUSINESS-LOGIC"]
---

# Phase 4 : Contrôleurs & Logique Métier

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2h-3h">
</div>


!!! quote "Analogie pédagogique"
    _Créer l'authentification avec Breeze, c'est comme installer des serrures pré-certifiées dans une nouvelle maison. Plutôt que de fondre votre propre métal pour forger une clé, vous utilisez un standard industriel éprouvé, ce qui vous permet de vous concentrer sur la construction des vraies pièces de la maison._

## Introduction aux Contrôleurs et à la Logique Métier

### Vue d'Ensemble de la Phase

> Cette quatrième phase constitue le **cœur de la logique applicative** de votre blog. Les contrôleurs sont les **chefs d'orchestre** de l'architecture MVC : ils reçoivent les requêtes HTTP, interrogent les modèles Eloquent pour récupérer/modifier les données, appliquent la logique métier (validation, autorisation, transformations), puis retournent les vues Blade enrichies des données.

!!! note "Dans Laravel, un contrôleur est une **classe PHP** contenant des méthodes publiques appelées **actions**. Chaque action correspond généralement à une route HTTP : `index()` pour lister, `show()` pour afficher un élément, `create()` pour le formulaire de création, `store()` pour enregistrer, `edit()` pour le formulaire d'édition, `update()` pour modifier, `destroy()` pour supprimer. C'est le pattern **CRUD** (Create, Read, Update, Delete)."

!!! quote "Contrairement aux frameworks où la logique métier est dispersée dans les vues (mauvaise pratique), Laravel impose une **séparation stricte** : **les contrôleurs gèrent la logique**, **les vues gèrent l'affichage**. Cette séparation garantit un code maintenable, testable et évolutif."

**Contrôleurs que nous allons créer :**

1. **HomeController** : Page d'accueil avec liste des articles publiés + sidebar
2. **PostController** : CRUD complet des articles (7 méthodes : index, show, create, store, edit, update, destroy)
3. **DashboardController** : Dashboard auteur avec statistiques et liste de ses articles
4. **CommentController** : Gestion des commentaires (création publique + modération auteur)
5. **CategoryController** : Affichage des articles par catégorie
6. **AuthorController** : Page profil public d'un auteur
7. **ProfileController** : Gestion du profil utilisateur (édition infos, changement password, suppression compte)

!!! quote "À l'issue de cette phase, votre application disposera de **toute la logique fonctionnelle** : un visiteur pourra consulter les articles et commenter, un auteur connecté pourra gérer ses articles et modérer les commentaires, et chaque utilisateur pourra personnaliser son profil."

!!! warning "Prérequis Phase 4 - Les Phases 1, 2 et 3 doivent être terminées : **projet Laravel créé**, **Breeze installé**, **migrations exécutées**, **modèles configurés**, **seeders exécutés**. Votre base de données doit contenir les données de test (**3 users**, **6 catégories**, **7 posts**, **2 comments**)."

## Étape 4.1 : Créer le HomeController

**Contexte de l'étape :**

> Le `HomeController` gère la **page d'accueil publique** du blog. C'est la première page que voit un visiteur lorsqu'il accède à `http://localhost:8000`. Cette page doit afficher :

> - **Une liste paginée** des articles publiés (9 par page)
- **Un sidebar** avec les catégories et leurs compteurs d'articles
- **Les 3 articles les plus populaires** (par nombre de vues)

!!! quote "Le contrôleur doit optimiser les requêtes SQL via **Eager Loading** (`with()`) pour éviter le problème N+1 : charger les relations `user` et `category` en une seule requête au lieu de N requêtes supplémentaires."

**Générer le contrôleur :**

```bash
# Créer le contrôleur HomeController
php artisan make:controller HomeController

# Résultat attendu :
# Controller created successfully.
# Created Controller: app/Http/Controllers/HomeController.php
```

**Éditer le fichier généré :**

Ouvrir `app/Http/Controllers/HomeController.php` et **remplacer tout le contenu** par :

```php title="Fichier : app/Http/Controllers/HomeController.php"
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Category;
use Illuminate\Http\Request;

class HomeController extends Controller
{
    /**
     * Afficher la page d'accueil du blog
     * 
     * Route : GET /
     * Vue : resources/views/home.blade.php
     * 
     * Cette méthode récupère :
     * 1. Les articles publiés paginés (9 par page)
     * 2. Les catégories avec leur nombre d'articles (sidebar)
     * 3. Les 3 articles les plus vus (sidebar "Populaires")
     * 
     * @return \Illuminate\View\View
     */
    public function index()
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES PUBLIÉS
        |----------------------------------------------------------------------
        | On applique plusieurs optimisations :
        |
        | 1. with(['user', 'category']) = EAGER LOADING
        |    Charge les relations en UNE requête SQL au lieu de N+1 requêtes
        |    Exemple sans with() :
        |      SELECT * FROM posts            (1 requête)
        |      SELECT * FROM users WHERE id=1 (N requêtes, une par post)
        |      SELECT * FROM categories WHERE id=1 (N requêtes)
        |    Avec with() :
        |      SELECT * FROM posts
        |      SELECT * FROM users WHERE id IN (1,2,3)      (1 requête)
        |      SELECT * FROM categories WHERE id IN (1,2,3) (1 requête)
        |
        | 2. published() = SCOPE défini dans Post::scopePublished()
        |    Filtre automatiquement : status='published' 
        |                              AND published_at IS NOT NULL 
        |                              AND published_at <= NOW()
        |
        | 3. latest('published_at') = ORDER BY published_at DESC
        |    Trie par date de publication décroissante (plus récents d'abord)
        |
        | 4. paginate(9) = PAGINATION
        |    Divise les résultats en pages de 9 articles
        |    Génère automatiquement les liens "Précédent/Suivant"
        |    Ajoute ?page=2 dans l'URL
        */
        $posts = Post::with(['user', 'category'])  // Eager load pour performance
                     ->published()                  // Seulement les articles publiés
                     ->latest('published_at')       // Plus récents en premier
                     ->paginate(9);                 // 9 articles par page
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES CATÉGORIES (Sidebar)
        |----------------------------------------------------------------------
        | withCount('posts') ajoute un attribut virtuel 'posts_count' à chaque
        | catégorie contenant le nombre d'articles associés.
        |
        | SQL généré :
        | SELECT categories.*, 
        |        (SELECT COUNT(*) FROM posts 
        |         WHERE posts.category_id = categories.id) AS posts_count
        | FROM categories
        |
        | Permet d'afficher dans la sidebar :
        | Technologie (3)
        | Voyage (2)
        | Cuisine (1)
        */
        $categories = Category::withCount('posts')->get();
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES POPULAIRES (Sidebar)
        |----------------------------------------------------------------------
        | On récupère les 3 articles les plus vus parmi les articles publiés.
        |
        | orderBy('views_count', 'desc') = Tri décroissant par nombre de vues
        | limit(3) = Limite à 3 résultats (pas de pagination ici)
        | get() = Exécute la requête et retourne une Collection
        |
        | Note : On pourrait aussi ajouter ->with('user') si on affiche l'auteur
        | dans la liste des populaires.
        */
        $popularPosts = Post::published()                // Seulement publiés
                            ->orderBy('views_count', 'desc') // Plus vus d'abord
                            ->limit(3)                       // Top 3
                            ->get();
        
        /*
        |----------------------------------------------------------------------
        | RETOUR DE LA VUE
        |----------------------------------------------------------------------
        | compact() est un helper PHP qui crée un tableau associatif :
        | compact('posts', 'categories', 'popularPosts')
        | équivaut à :
        | ['posts' => $posts, 'categories' => $categories, 'popularPosts' => $popularPosts]
        |
        | Ces variables seront accessibles dans la vue Blade :
        | @foreach($posts as $post)
        */
        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
}
```

<small>*L'Eager Loading via `with()` est **crucial pour les performances** : sans lui, afficher 9 articles avec leur auteur et catégorie générerait 1 + 9 + 9 = 19 requêtes SQL. Avec `with()`, seulement 3 requêtes (1 pour les posts, 1 pour les users, 1 pour les categories). Sur une base de 10 000 articles, la différence est dramatique (500ms vs 50ms). Le scope `published()` centralise la logique de filtrage : si demain vous ajoutez une condition (ex: `is_featured`), vous la modifiez une seule fois dans `Post::scopePublished()` et tout le code en bénéficie.*</small>

## Étape 4.2 : Créer le PostController (CRUD)

**Contexte de l'étape :**

> Le `PostController` est le **contrôleur le plus important** du blog. Il gère toutes les opérations CRUD sur les articles :

> - **show()** : Afficher un article individuel (public)
- **create()** : Formulaire de création (auth requis)
- **store()** : Enregistrer un nouvel article (auth requis)
- **edit()** : Formulaire d'édition (auth + ownership requis)
- **update()** : Mettre à jour un article (auth + ownership requis)
- **destroy()** : Supprimer un article (auth + ownership requis)

!!! quote "Les méthodes protégées (**create**, **store**, **edit**, **update**, **destroy**) nécessitent une **authentification** (middleware `auth`) et une **vérification d'ownership** : un utilisateur ne peut **modifier**/**supprimer que ses propres articles**."

**Générer le contrôleur :**

```bash
# Créer le contrôleur PostController
php artisan make:controller PostController

# Résultat attendu :
# Controller created successfully.
```

**Éditer le fichier généré :**

Ouvrir `app/Http/Controllers/PostController.php` et **remplacer tout le contenu** par :

```php title="Fichier : app/Http/Controllers/PostController.php"
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Category;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | AFFICHAGE PUBLIC D'UN ARTICLE
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher un article individuel (page publique)
     * 
     * Route : GET /posts/{post:slug}
     * Vue : resources/views/posts/show.blade.php
     * 
     * Cette méthode :
     * 1. Récupère l'article via son slug (binding automatique Laravel)
     * 2. Vérifie l'autorisation d'accès si l'article est un brouillon
     * 3. Incrémente le compteur de vues
     * 4. Charge les relations et commentaires approuvés
     * 5. Récupère 3 articles similaires (même catégorie)
     * 
     * @param Post $post Instance du post (injectée automatiquement par Laravel)
     * @return \Illuminate\View\View
     */
    public function show(Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | CONTRÔLE D'ACCÈS AUX BROUILLONS
        |----------------------------------------------------------------------
        | Les brouillons ne sont visibles QUE par leur auteur.
        | Si un visiteur ou un autre utilisateur tente d'y accéder → 404
        |
        | Logique :
        | - Si status = draft ET (pas connecté OU pas l'auteur) → abort(404)
        | - Sinon → affichage normal
        */
        if ($post->status === 'draft') {
            // auth()->check() retourne true si utilisateur connecté
            // auth()->id() retourne l'ID de l'utilisateur connecté (null si non connecté)
            
            if (!auth()->check() || auth()->id() !== $post->user_id) {
                // abort(404) génère une erreur 404 Not Found
                // Le visiteur verra la page d'erreur Laravel standard
                abort(404);
            }
        }
        
        /*
        |----------------------------------------------------------------------
        | INCRÉMENTATION DU COMPTEUR DE VUES
        |----------------------------------------------------------------------
        | On incrémente seulement pour les articles publiés.
        | Pour les brouillons, on ne compte pas les vues de l'auteur.
        |
        | incrementViews() est définie dans le modèle Post :
        | $this->increment('views_count')
        | SQL généré : UPDATE posts SET views_count = views_count + 1 WHERE id = ?
        |
        | Avantage : évite les race conditions (deux visiteurs simultanés)
        | Alternative non-safe : $post->views_count++; $post->save();
        */
        if ($post->status === 'published') {
            $post->incrementViews();
        }
        
        /*
        |----------------------------------------------------------------------
        | EAGER LOADING DES RELATIONS
        |----------------------------------------------------------------------
        | load() charge les relations APRÈS avoir récupéré le post.
        | Différence avec with() :
        | - with() : chargement AVANT la requête principale (dans la requête SQL)
        | - load() : chargement APRÈS (requête SQL séparée)
        |
        | Ici on utilise load() car le post est déjà récupéré via route binding.
        |
        | comments => function($query) : Closure pour filtrer les commentaires
        | - approved() : scope défini dans Comment::scopeApproved()
        | - latest() : ORDER BY created_at DESC (plus récents d'abord)
        */
        $post->load([
            'user',      // Auteur de l'article
            'category',  // Catégorie de l'article
            'comments' => function ($query) {
                // Seulement les commentaires approuvés, triés du plus récent au plus ancien
                $query->approved()->latest();
            }
        ]);
        
        /*
        |----------------------------------------------------------------------
        | ARTICLES SIMILAIRES (Même Catégorie)
        |----------------------------------------------------------------------
        | On récupère 3 autres articles publiés de la même catégorie.
        | Utilisé dans la vue pour afficher "Vous pourriez aussi aimer".
        |
        | where('id', '!=', $post->id) : Exclure l'article actuel
        | limit(3) : Maximum 3 résultats
        | inRandomOrder() : Optionnel, pour varier l'ordre à chaque visite
        */
        $relatedPosts = Post::published()
                            ->where('category_id', $post->category_id)  // Même catégorie
                            ->where('id', '!=', $post->id)              // Pas l'article actuel
                            ->limit(3)
                            ->get();
        
        // Retourner la vue avec les données
        return view('posts.show', compact('post', 'relatedPosts'));
    }
    
    /*
    |--------------------------------------------------------------------------
    | CRÉATION D'UN ARTICLE (Authentification Requise)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher le formulaire de création d'article
     * 
     * Route : GET /posts/create
     * Middleware : auth (utilisateur doit être connecté)
     * Vue : resources/views/posts/create.blade.php
     * 
     * @return \Illuminate\View\View
     */
    public function create()
    {
        // Récupérer toutes les catégories pour le select du formulaire
        $categories = Category::all();
        
        return view('posts.create', compact('categories'));
    }
    
    /**
     * Enregistrer un nouvel article en base de données
     * 
     * Route : POST /posts
     * Middleware : auth
     * 
     * Cette méthode :
     * 1. Valide les données du formulaire
     * 2. Crée l'article pour l'utilisateur connecté
     * 3. Redirige vers l'article créé avec message de succès
     * 
     * @param Request $request Objet contenant les données POST
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES DU FORMULAIRE
        |----------------------------------------------------------------------
        | validate() vérifie que les données respectent les règles.
        | Si validation échoue :
        | - Retour automatique au formulaire avec les erreurs
        | - Les anciennes valeurs sont conservées (old())
        | - Les messages d'erreur sont disponibles dans @error()
        |
        | Règles de validation :
        | - required : champ obligatoire
        | - max:255 : maximum 255 caractères
        | - exists:categories,id : l'ID doit exister dans la table categories
        | - nullable : champ optionnel
        | - url : doit être une URL valide (http:// ou https://)
        | - in:draft,published : doit être exactement 'draft' ou 'published'
        */
        $validated = $request->validate([
            'title' => 'required|max:255',
            'category_id' => 'required|exists:categories,id',
            'excerpt' => 'required|max:500',
            'content' => 'required|min:100',
            'image' => 'nullable|url',
            'status' => 'required|in:draft,published',
        ], [
            // Messages d'erreur personnalisés (optionnel)
            'title.required' => 'Le titre est obligatoire.',
            'category_id.required' => 'Veuillez sélectionner une catégorie.',
            'category_id.exists' => 'Cette catégorie n\'existe pas.',
            'excerpt.required' => 'Le résumé est obligatoire.',
            'excerpt.max' => 'Le résumé ne doit pas dépasser 500 caractères.',
            'content.required' => 'Le contenu est obligatoire.',
            'content.min' => 'Le contenu doit contenir au moins 100 caractères.',
            'image.url' => 'L\'image doit être une URL valide.',
            'status.in' => 'Le statut doit être "draft" ou "published".',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | CRÉATION DE L'ARTICLE
        |----------------------------------------------------------------------
        | auth()->user()->posts() accède à la relation hasMany définie dans User
        | create($validated) crée un nouvel article avec les données validées
        |
        | Équivaut à :
        | $post = new Post($validated);
        | $post->user_id = auth()->id();
        | $post->save();
        |
        | Avantage : plus concis, remplit automatiquement user_id
        |
        | Note : Le slug sera généré automatiquement par l'événement creating()
        | défini dans Post::boot()
        */
        $post = auth()->user()->posts()->create($validated);
        
        /*
        |----------------------------------------------------------------------
        | MESSAGE DE SUCCÈS SELON LE STATUT
        |----------------------------------------------------------------------
        | On personnalise le message selon que l'article est publié ou brouillon.
        | Ce message sera affiché via session()->get('success') dans la vue.
        */
        $message = $post->status === 'published' 
            ? 'Article publié avec succès !' 
            : 'Brouillon sauvegardé avec succès !';
        
        /*
        |----------------------------------------------------------------------
        | REDIRECTION AVEC MESSAGE FLASH
        |----------------------------------------------------------------------
        | redirect()->route('posts.show', $post) :
        | - Redirige vers la route nommée 'posts.show'
        | - Passe $post comme paramètre (Laravel génère /posts/{slug})
        |
        | with('success', $message) :
        | - Stocke le message dans la session (flash = disponible qu'une seule fois)
        | - Accessible dans la vue via session('success') ou @session('success')
        */
        return redirect()
            ->route('posts.show', $post)
            ->with('success', $message);
    }
    
    /*
    |--------------------------------------------------------------------------
    | ÉDITION D'UN ARTICLE (Ownership Requis)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher le formulaire d'édition d'un article
     * 
     * Route : GET /posts/{post}/edit
     * Middleware : auth
     * Vue : resources/views/posts/edit.blade.php
     * 
     * Cette méthode vérifie que l'utilisateur connecté est bien l'auteur
     * de l'article avant d'afficher le formulaire.
     * 
     * @param Post $post
     * @return \Illuminate\View\View
     */
    public function edit(Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | VÉRIFICATION DE L'OWNERSHIP
        |----------------------------------------------------------------------
        | Un utilisateur ne peut modifier QUE ses propres articles.
        | Si un autre utilisateur tente d'accéder → erreur 403 Forbidden
        |
        | abort(403, $message) génère une exception HTTP 403
        | Le visiteur verra "403 Forbidden - Action non autorisée."
        */
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        // Récupérer toutes les catégories pour le select
        $categories = Category::all();
        
        return view('posts.edit', compact('post', 'categories'));
    }
    
    /**
     * Mettre à jour un article existant
     * 
     * Route : PUT /posts/{post}
     * Middleware : auth
     * 
     * @param Request $request
     * @param Post $post
     * @return \Illuminate\Http\RedirectResponse
     */
    public function update(Request $request, Post $post)
    {
        // Vérifier l'ownership (même logique que edit())
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        // Validation (mêmes règles que store())
        $validated = $request->validate([
            'title' => 'required|max:255',
            'category_id' => 'required|exists:categories,id',
            'excerpt' => 'required|max:500',
            'content' => 'required|min:100',
            'image' => 'nullable|url',
            'status' => 'required|in:draft,published',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | MISE À JOUR DE L'ARTICLE
        |----------------------------------------------------------------------
        | update($validated) met à jour toutes les colonnes du tableau $validated
        |
        | SQL généré :
        | UPDATE posts 
        | SET title = ?, category_id = ?, excerpt = ?, content = ?, 
        |     image = ?, status = ?, updated_at = NOW()
        | WHERE id = ?
        |
        | Note : Le slug n'est PAS regénéré lors de l'update (événement updating())
        | car changer l'URL casserait les liens existants (mauvais pour SEO).
        |
        | Si vous voulez regénérer le slug, ajoutez :
        | $post->slug = Str::slug($validated['title']);
        */
        $post->update($validated);
        
        // Message personnalisé selon le nouveau statut
        $message = $post->status === 'published' 
            ? 'Article mis à jour et publié !' 
            : 'Brouillon mis à jour !';
        
        return redirect()
            ->route('posts.show', $post)
            ->with('success', $message);
    }
    
    /*
    |--------------------------------------------------------------------------
    | SUPPRESSION D'UN ARTICLE (Ownership Requis)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Supprimer un article
     * 
     * Route : DELETE /posts/{post}
     * Middleware : auth
     * 
     * Supprime l'article de la base de données.
     * Grâce à onDelete('cascade') dans les migrations, les commentaires
     * associés sont automatiquement supprimés.
     * 
     * @param Post $post
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Post $post)
    {
        // Vérifier l'ownership
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | SUPPRESSION DE L'ARTICLE
        |----------------------------------------------------------------------
        | delete() supprime l'enregistrement de la base de données.
        |
        | SQL généré :
        | DELETE FROM posts WHERE id = ?
        |
        | Grâce à la contrainte CASCADE définie dans create_comments_table :
        | ->onDelete('cascade')
        | Tous les commentaires associés sont automatiquement supprimés.
        |
        | Alternative : Soft Delete (suppression logique)
        | Au lieu de supprimer physiquement, on marque comme supprimé :
        | use SoftDeletes; dans le modèle
        | Migration : $table->softDeletes();
        | Permet de restaurer les articles supprimés.
        */
        $post->delete();
        
        // Redirection vers le dashboard avec message
        return redirect()
            ->route('dashboard')
            ->with('success', 'Article supprimé avec succès !');
    }
}
```

<small>*La vérification d'ownership manuelle (`auth()->id() !== $post->user_id`) est basique mais efficace. Pour un projet plus complexe, utilisez les **Policies** Laravel : `php artisan make:policy PostPolicy --model=Post`, puis définissez des méthodes `update(User $user, Post $post)` et vérifiez via `$this->authorize('update', $post)` dans le contrôleur. Les Policies centralisent les règles d'autorisation et sont testables unitairement.*</small>

## Étape 4.3 : Créer le DashboardController

**Contexte de l'étape :**

> Le `DashboardController` gère le **tableau de bord personnel** de l'auteur connecté. Cette page affiche :

> - **Statistiques globales** : nombre total d'articles, publiés, brouillons, vues, commentaires
- **L'article le plus populaire** de l'auteur
- **La liste complète** de ses articles (publiés + brouillons)

!!! quote "Ce dashboard est accessible uniquement aux **utilisateurs authentifiés** (middleware `auth` défini dans les routes)."

**Générer le contrôleur :**

```bash
php artisan make:controller DashboardController
```

**Éditer le fichier généré :**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * Afficher le dashboard auteur (page privée)
     * 
     * Route : GET /dashboard
     * Middleware : auth (utilisateur doit être connecté)
     * Vue : resources/views/dashboard.blade.php
     * 
     * Cette méthode calcule toutes les statistiques de l'auteur connecté :
     * - Nombre d'articles (total, publiés, brouillons)
     * - Nombre total de vues
     * - Nombre total de commentaires
     * - Article le plus vu
     * 
     * @return \Illuminate\View\View
     */
    public function index()
    {
        // Récupérer l'utilisateur connecté
        // auth()->user() retourne l'instance du User authentifié
        $user = auth()->user();
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DE TOUS LES ARTICLES DE L'AUTEUR
        |----------------------------------------------------------------------
        | On récupère TOUS les articles de l'utilisateur (publiés + brouillons)
        | avec leur catégorie (Eager Loading), triés du plus récent au plus ancien.
        |
        | where('user_id', $user->id) filtre par auteur
        | with('category') charge la catégorie en une seule requête
        | latest() = ORDER BY created_at DESC
        | get() exécute la requête et retourne une Collection
        |
        | Alternative avec relation :
        | $posts = $user->posts()->with('category')->latest()->get();
        */
        $posts = Post::where('user_id', $user->id)
                     ->with('category')
                     ->latest()
                     ->get();
        
        /*
        |----------------------------------------------------------------------
        | CALCUL DES STATISTIQUES
        |----------------------------------------------------------------------
        | On utilise les méthodes de Collection pour calculer les stats.
        |
        | $posts->count() : Nombre total d'articles
        | $posts->where('status', 'published')->count() : Filtrer puis compter
        | $posts->sum('views_count') : Somme de la colonne views_count
        |
        | Pour les commentaires, on fait une requête séparée avec withCount() :
        | withCount('comments') ajoute un attribut virtuel 'comments_count'
        | Ensuite on somme tous les comments_count
        */
        $stats = [
            'total_posts' => $posts->count(),
            
            'published_posts' => $posts->where('status', 'published')->count(),
            
            'draft_posts' => $posts->where('status', 'draft')->count(),
            
            // Somme de toutes les vues de tous les articles
            'total_views' => $posts->sum('views_count'),
            
            // Nombre total de commentaires sur tous les articles
            // On récupère les posts avec leur nombre de commentaires
            'total_comments' => $user->posts()
                                     ->withCount('comments')
                                     ->get()
                                     ->sum('comments_count'),
        ];
        
        /*
        |----------------------------------------------------------------------
        | ARTICLE LE PLUS POPULAIRE (Plus de Vues)
        |----------------------------------------------------------------------
        | On filtre les articles publiés, on les trie par views_count décroissant,
        | et on prend le premier (ou null si aucun article publié).
        |
        | sortByDesc('views_count') trie la Collection en mémoire
        | first() retourne le premier élément ou null
        |
        | Alternative avec requête SQL directe :
        | $mostViewedPost = Post::where('user_id', $user->id)
        |                       ->published()
        |                       ->orderBy('views_count', 'desc')
        |                       ->first();
        */
        $mostViewedPost = $posts->where('status', 'published')
                                ->sortByDesc('views_count')
                                ->first();
        
        /*
        |----------------------------------------------------------------------
        | ARTICLES RÉCENTS (5 Derniers)
        |----------------------------------------------------------------------
        | take(5) limite à 5 éléments
        | La Collection $posts est déjà triée par latest(), donc take(5)
        | retourne les 5 plus récents.
        */
        $recentPosts = $posts->take(5);
        
        // Retourner la vue avec toutes les données
        return view('dashboard', compact('posts', 'stats', 'mostViewedPost', 'recentPosts'));
    }
}
```

<small>*L'utilisation de Collections (`$posts->where()`, `$posts->sum()`) au lieu de requêtes SQL séparées est efficace **si le nombre d'articles par auteur est limité** (<100). Au-delà, préférez des requêtes SQL directes avec `selectRaw()` pour décharger le travail sur MySQL. Exemple : `Post::where('user_id', $user->id)->selectRaw('SUM(views_count) as total_views')->value('total_views')`.*</small>

## Étape 4.4 : Créer le CommentController

**Contexte de l'étape :**

> Le `CommentController` gère deux fonctionnalités distinctes :

> 1. **Création de commentaires** (publique, sans authentification) : les visiteurs peuvent commenter
2. **Modération** (privée, auteur seulement) : approuver ou supprimer les commentaires sur ses articles

**Générer le contrôleur :**

```bash
php artisan make:controller CommentController
```

**Éditer le fichier généré :**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Comment;
use Illuminate\Http\Request;

class CommentController extends Controller
{
    /**
     * Créer un nouveau commentaire sur un article (action publique)
     * 
     * Route : POST /posts/{post}/comments
     * Accès : Public (pas d'authentification requise)
     * 
     * Les visiteurs non inscrits peuvent commenter en fournissant
     * leur nom et email. Le commentaire est créé en statut non approuvé
     * (approved=false) et l'auteur de l'article devra le modérer.
     * 
     * @param Request $request Données du formulaire
     * @param Post $post Article commenté (injecté automatiquement)
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request, Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES DU FORMULAIRE
        |----------------------------------------------------------------------
        | Règles :
        | - author_name : obligatoire, max 255 caractères
        | - author_email : obligatoire, format email valide
        | - content : obligatoire, min 10 caractères (évite spam), max 1000
        |
        | Note : On ne valide PAS l'unicité de l'email car plusieurs visiteurs
        | peuvent avoir le même nom/email (Jean Dupont, jean@example.com)
        */
        $validated = $request->validate([
            'author_name' => 'required|max:255',
            'author_email' => 'required|email',
            'content' => 'required|min:10|max:1000',
        ], [
            'author_name.required' => 'Veuillez indiquer votre nom.',
            'author_email.required' => 'Veuillez indiquer votre email.',
            'author_email.email' => 'Email invalide.',
            'content.required' => 'Le commentaire ne peut pas être vide.',
            'content.min' => 'Le commentaire doit contenir au moins 10 caractères.',
            'content.max' => 'Le commentaire ne doit pas dépasser 1000 caractères.',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | CRÉATION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | $post->comments() accède à la relation hasMany définie dans Post
        | create() crée un nouvel enregistrement avec post_id rempli automatiquement
        |
        | ...$validated : Spread operator PHP (décompose le tableau)
        | Équivaut à : [...$validated, 'approved' => false]
        |
        | Le commentaire est créé avec approved=false par défaut.
        | L'auteur de l'article devra l'approuver manuellement.
        */
        $post->comments()->create([
            ...$validated,           // Spread : author_name, author_email, content
            'approved' => false,     // Non approuvé par défaut (modération manuelle)
        ]);
        
        /*
        |----------------------------------------------------------------------
        | REDIRECTION AVEC MESSAGE
        |----------------------------------------------------------------------
        | back() redirige vers la page précédente (l'article)
        | Équivaut à : redirect()->route('posts.show', $post)
        |
        | with('success', $message) stocke le message dans la session flash
        */
        return back()->with('success', 'Commentaire ajouté ! Il sera visible après modération par l\'auteur.');
    }
    
    /**
     * Approuver un commentaire (action auteur)
     * 
     * Route : PATCH /comments/{comment}/approve
     * Middleware : auth (utilisateur connecté requis)
     * 
     * Seul l'auteur de l'article peut approuver les commentaires.
     * 
     * @param Comment $comment Commentaire à approuver (injecté automatiquement)
     * @return \Illuminate\Http\RedirectResponse
     */
    public function approve(Comment $comment)
    {
        /*
        |----------------------------------------------------------------------
        | VÉRIFICATION DE L'OWNERSHIP
        |----------------------------------------------------------------------
        | On vérifie que l'utilisateur connecté est bien l'auteur du POST
        | auquel appartient ce commentaire.
        |
        | $comment->post : Accès à la relation belongsTo définie dans Comment
        | $comment->post->user_id : ID de l'auteur de l'article
        |
        | Si ce n'est pas l'auteur → erreur 403
        */
        if (auth()->id() !== $comment->post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | APPROBATION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | update() modifie la colonne approved à true
        |
        | SQL généré :
        | UPDATE comments SET approved = 1, updated_at = NOW() WHERE id = ?
        |
        | Alternative avec méthode helper définie dans Comment :
        | $comment->approve(); (si vous avez défini cette méthode dans le modèle)
        */
        $comment->update(['approved' => true]);
        
        // Rediriger vers la page de l'article avec message
        return back()->with('success', 'Commentaire approuvé !');
    }
    
    /**
     * Supprimer un commentaire (action auteur)
     * 
     * Route : DELETE /comments/{comment}
     * Middleware : auth
     * 
     * Seul l'auteur de l'article peut supprimer les commentaires.
     * 
     * @param Comment $comment
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Comment $comment)
    {
        // Vérifier l'ownership (même logique que approve())
        if (auth()->id() !== $comment->post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | SUPPRESSION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | delete() supprime l'enregistrement de la base de données
        |
        | SQL généré :
        | DELETE FROM comments WHERE id = ?
        */
        $comment->delete();
        
        return back()->with('success', 'Commentaire supprimé !');
    }
}
```

<small>*Le système de modération implémenté ici est simple mais efficace : tous les commentaires sont créés avec `approved=false`, l'auteur les voit dans son interface avec des boutons "Approuver"/"Supprimer", et seuls les commentaires approuvés apparaissent publiquement (filtrage via scope `approved()`). Pour un blog à fort trafic, ajoutez un système de **notifications** (email à l'auteur quand nouveau commentaire) ou un **scoring anti-spam** (Akismet API).*</small>

## Étape 4.5 : Créer le CategoryController

**Générer et éditer :**

```bash
php artisan make:controller CategoryController
```

```php
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    /**
     * Afficher tous les articles d'une catégorie (page publique)
     * 
     * Route : GET /category/{category:slug}
     * Vue : resources/views/categories/show.blade.php
     * 
     * Cette page liste tous les articles publiés appartenant à la catégorie.
     * 
     * @param Category $category Catégorie (injectée via slug)
     * @return \Illuminate\View\View
     */
    public function show(Category $category)
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES DE LA CATÉGORIE
        |----------------------------------------------------------------------
        | $category->posts() accède à la relation hasMany définie dans Category
        | with('user') charge l'auteur de chaque article (Eager Loading)
        | published() scope pour ne récupérer que les articles publiés
        | latest('published_at') tri par date de publication décroissante
        | paginate(9) pagination avec 9 articles par page
        */
        $posts = $category->posts()
                          ->with('user')
                          ->published()
                          ->latest('published_at')
                          ->paginate(9);
        
        return view('categories.show', compact('category', 'posts'));
    }
}
```

## Étape 4.6 : Créer l'AuthorController

```bash
php artisan make:controller AuthorController
```

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class AuthorController extends Controller
{
    /**
     * Afficher la page profil public d'un auteur
     * 
     * Route : GET /author/{user}
     * Vue : resources/views/authors/show.blade.php
     * 
     * Cette page affiche :
     * - Les informations publiques de l'auteur (nom, bio, avatar)
     * - Ses statistiques (nombre d'articles, vues, commentaires)
     * - La liste paginée de ses articles publiés
     * 
     * @param User $user Auteur (injecté automatiquement par Laravel)
     * @return \Illuminate\View\View
     */
    public function show(User $user)
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES PUBLIÉS DE L'AUTEUR
        |----------------------------------------------------------------------
        | $user->posts() accède à la relation hasMany définie dans User
        | with('category') charge la catégorie (pour affichage badge)
        | published() scope pour ne récupérer que les publiés
        | latest('published_at') tri chronologique inversé
        | paginate(6) pagination avec 6 articles par page (moins que page accueil)
        */
        $posts = $user->posts()
                      ->with('category')
                      ->published()
                      ->latest('published_at')
                      ->paginate(6);
        
        /*
        |----------------------------------------------------------------------
        | CALCUL DES STATISTIQUES PUBLIQUES
        |----------------------------------------------------------------------
        | Ces stats sont visibles publiquement sur le profil auteur.
        | On ne montre QUE les articles publiés (pas les brouillons).
        |
        | sum('views_count') : Somme des vues de tous les articles publiés
        | withCount('comments') : Ajoute comments_count à chaque article
        | get()->sum('comments_count') : Somme tous les comments_count
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
}
```

## Étape 4.7 : Créer le ProfileController

```bash
php artisan make:controller ProfileController
```

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Hash;

class ProfileController extends Controller
{
    /**
     * Afficher le formulaire d'édition du profil
     * 
     * Route : GET /profile
     * Middleware : auth
     * Vue : resources/views/profile/edit.blade.php
     * 
     * @param Request $request
     * @return \Illuminate\View\View
     */
    public function edit(Request $request)
    {
        return view('profile.edit', [
            'user' => $request->user(),
        ]);
    }

    /**
     * Mettre à jour les informations du profil
     * 
     * Route : PATCH /profile
     * Middleware : auth
     * 
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function update(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES
        |----------------------------------------------------------------------
        | Rule::unique('users')->ignore($request->user()->id) :
        | L'email doit être unique SAUF pour l'utilisateur actuel.
        | Permet de garder son propre email sans erreur "déjà utilisé".
        */
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => [
                'required',
                'string',
                'email',
                'max:255',
                Rule::unique('users')->ignore($request->user()->id)
            ],
            'bio' => 'nullable|string|max:500',
            'avatar' => 'nullable|url',
        ]);

        // Récupérer l'utilisateur connecté
        $user = $request->user();
        
        // Remplir les nouvelles valeurs
        $user->fill($validated);

        /*
        |----------------------------------------------------------------------
        | RÉINITIALISER EMAIL_VERIFIED_AT SI EMAIL CHANGE
        |----------------------------------------------------------------------
        | Si l'utilisateur change son email, on réinitialise la vérification.
        | isDirty('email') retourne true si la colonne email a été modifiée.
        |
        | L'utilisateur devra re-vérifier son nouvel email.
        */
        if ($user->isDirty('email')) {
            $user->email_verified_at = null;
        }

        $user->save();

        return redirect()
            ->route('profile.edit')
            ->with('success', 'Profil mis à jour avec succès !');
    }

    /**
     * Supprimer le compte utilisateur
     * 
     * Route : DELETE /profile
     * Middleware : auth
     * 
     * Supprime définitivement le compte et toutes ses données associées.
     * Grâce à onDelete('cascade'), les articles et leurs commentaires
     * sont automatiquement supprimés.
     * 
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | CONFIRMATION PAR MOT DE PASSE
        |----------------------------------------------------------------------
        | current_password : règle de validation spéciale Laravel Breeze
        | Vérifie que le mot de passe fourni correspond au mot de passe actuel.
        |
        | Sécurité : empêche la suppression accidentelle ou par une personne
        | qui aurait accès à la session mais pas au mot de passe.
        */
        $request->validate([
            'password' => ['required', 'current_password'],
        ]);

        $user = $request->user();

        // Déconnecter l'utilisateur
        Auth::logout();

        // Supprimer le compte (cascade = supprime aussi posts et comments)
        $user->delete();

        // Invalider la session
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/')->with('success', 'Compte supprimé avec succès.');
    }
}
```

## Récapitulatif Phase 4

✅ **7 Contrôleurs Créés** :

| Contrôleur | Rôle | Méthodes | Accès |
|------------|------|----------|-------|
| `HomeController` | Page d'accueil | `index()` | Public |
| `PostController` | CRUD articles | `show()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Public (show) / Auth (reste) |
| `DashboardController` | Dashboard auteur | `index()` | Auth |
| `CommentController` | Gestion commentaires | `store()`, `approve()`, `destroy()` | Public (store) / Auth (reste) |
| `CategoryController` | Articles par catégorie | `show()` | Public |
| `AuthorController` | Profil auteur public | `show()` | Public |
| `ProfileController` | Gestion profil | `edit()`, `update()`, `destroy()` | Auth |

✅ **Compétences Maîtrisées** :

- Route Model Binding automatique
- Eager Loading (`with()`, `load()`)
- Query Scopes (`published()`, `approved()`)
- Validation de formulaires
- Vérification d'ownership manuelle
- Messages flash (`with()`)
- Relations Eloquent dans contrôleurs
- Collections Laravel (filtrage, tri, agrégation)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les kits de démarrage Laravel font gagner des semaines de développement, mais ils imposent de bien comprendre les flux sous-jacents. Ne traitez jamais l'authentification comme une simple boîte noire.

> [Passer à la phase suivante →](../index.md)
