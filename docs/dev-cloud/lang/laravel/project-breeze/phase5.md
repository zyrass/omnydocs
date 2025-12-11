---
description: "Configuration des routes publiques/protégées, middleware auth, Route Model Binding et organisation architecture."
icon: lucide/route
tags: ["ROUTES", "MIDDLEWARE", "ROUTING", "ARCHITECTURE"]
status: stable
---

# Phase 5 : Routes & Organisation

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30-45 minutes">
</div>

## Introduction aux Routes et Organisation


### Vue d'Ensemble de la Phase

> Cette cinquième phase configure le **système de routing** de votre application. Les routes sont la **carte routière** de votre blog : elles définissent quelles URLs sont accessibles, quelles méthodes HTTP sont acceptées (GET, POST, PUT, DELETE), quels contrôleurs/méthodes sont appelés, et quels middlewares protègent l'accès.

!!! example "Laravel utilise un système de **routing expressif** dans les fichiers `routes/web.php` (routes web classiques) et `routes/auth.php` (routes d'authentification Breeze)."

    Chaque route associe une **URL pattern** à une **action** :

    ```php
    <?php
    Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');
    ```

    Cette ligne signifie : "Quand l'utilisateur visite `/posts/introduction-laravel-11` en GET, appelle la méthode `show()` de `PostController` en injectant automatiquement l'objet `Post` correspondant au slug, et nomme cette route `posts.show` pour générer facilement l'URL via `route('posts.show', $post)`."

**Organisation des routes :**

1. **Routes publiques** : accessibles sans authentification (home, posts.show, categories, comments)
2. **Routes authentification** : gérées par Breeze (`require __DIR__.'/auth.php'`)
3. **Routes protégées** : middleware `auth` requis (dashboard, CRUD posts, modération)

!!! note "À l'issue de cette phase, votre application disposera de **toutes les URLs fonctionnelles** et protégées correctement. Vous pourrez naviguer de la page d'accueil vers un article, créer un compte, publier un article, commenter, etc."

!!! warning "Prérequis Phase 5 - La Phase 4 doit être terminée : tous les contrôleurs créés et leurs méthodes implémentées."

## Étape 5.1 : Configurer Toutes les Routes

**Contexte de l'étape :**

> Nous allons configurer **toutes les routes** dans un seul fichier `routes/web.php` organisé en **3 sections** :

> 1. Routes publiques (accessibles sans connexion)
2. Routes Breeze (authentification)
3. Routes protégées (middleware `auth`)

!!! quote "Cette organisation claire facilite la maintenance et la compréhension du système de routing."

**Éditer le fichier principal :**

Ouvrir `routes/web.php` et **remplacer tout le contenu** par :

```php
<?php

use App\Http\Controllers\{
    HomeController,
    PostController,
    DashboardController,
    CommentController,
    CategoryController,
    AuthorController,
    ProfileController
};
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| ROUTES PUBLIQUES
|--------------------------------------------------------------------------
| Ces routes sont accessibles sans authentification.
| Elles constituent la partie "blog" visible par tous les visiteurs.
|
| Méthode HTTP :
| - GET : récupérer des données (affichage)
| - POST : envoyer des données (création)
*/

/**
 * Page d'accueil du blog
 * 
 * URL : http://localhost:8000/
 * Méthode : GET
 * Contrôleur : HomeController::index()
 * Nom : home
 * 
 * Affiche la liste paginée des articles publiés + sidebar
 */
Route::get('/', [HomeController::class, 'index'])->name('home');

/**
 * Afficher un article individuel
 * 
 * URL : http://localhost:8000/posts/introduction-laravel-11
 * Méthode : GET
 * Contrôleur : PostController::show()
 * Nom : posts.show
 * 
 * {post:slug} = Route Model Binding avec custom key
 * Laravel recherche automatiquement le Post via la colonne 'slug'
 * au lieu de 'id' par défaut.
 * 
 * Exemple : /posts/mon-article → recherche WHERE slug='mon-article'
 */
Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');

/**
 * Afficher les articles d'une catégorie
 * 
 * URL : http://localhost:8000/category/technologie
 * Méthode : GET
 * Contrôleur : CategoryController::show()
 * Nom : categories.show
 * 
 * {category:slug} = Binding par slug (comme posts)
 */
Route::get('/category/{category:slug}', [CategoryController::class, 'show'])->name('categories.show');

/**
 * Afficher le profil public d'un auteur
 * 
 * URL : http://localhost:8000/author/1
 * Méthode : GET
 * Contrôleur : AuthorController::show()
 * Nom : authors.show
 * 
 * {user} = Binding par id (défaut)
 * Alternative : {user:name} pour URLs /author/alice-dupont
 */
Route::get('/author/{user}', [AuthorController::class, 'show'])->name('authors.show');

/**
 * Créer un commentaire sur un article (action publique)
 * 
 * URL : http://localhost:8000/posts/123/comments
 * Méthode : POST
 * Contrôleur : CommentController::store()
 * Nom : comments.store
 * 
 * Les visiteurs non inscrits peuvent commenter.
 * Le commentaire sera créé en statut non approuvé.
 * 
 * Formulaire HTML correspondant :
 * <form action="{{ route('comments.store', $post) }}" method="POST">
 */
Route::post('/posts/{post}/comments', [CommentController::class, 'store'])->name('comments.store');

/*
|--------------------------------------------------------------------------
| ROUTES AUTHENTIFICATION (Laravel Breeze)
|--------------------------------------------------------------------------
| Ces routes sont définies dans routes/auth.php (généré par Breeze).
| Elles gèrent tout le système d'authentification :
|
| - GET /register → Formulaire inscription
| - POST /register → Créer compte
| - GET /login → Formulaire connexion
| - POST /login → Authentifier
| - POST /logout → Déconnexion
| - GET /forgot-password → Formulaire reset password
| - POST /forgot-password → Envoyer email reset
| - GET /reset-password/{token} → Formulaire nouveau password
| - POST /reset-password → Définir nouveau password
| - GET /verify-email → Page vérification email
| - GET /verify-email/{id}/{hash} → Lien vérification email
| - POST /email/verification-notification → Renvoyer email vérification
|
| require __DIR__.'/auth.php' : Inclut le fichier auth.php
| Équivaut à copier-coller tout le contenu de auth.php ici.
*/
require __DIR__.'/auth.php';

/*
|--------------------------------------------------------------------------
| ROUTES PROTÉGÉES (Authentification Requise)
|--------------------------------------------------------------------------
| Ces routes nécessitent que l'utilisateur soit connecté.
| Le middleware 'auth' vérifie la présence d'une session valide.
| Si non connecté → redirection vers /login
|
| Route::middleware(['auth'])->group(function() { ... })
| Applique le middleware 'auth' à toutes les routes du groupe.
|
| Alternative sans groupe :
| Route::get('/dashboard', ...)->middleware('auth');
| Mais le groupe est plus lisible pour plusieurs routes.
*/
Route::middleware(['auth'])->group(function () {
    
    /*
    |----------------------------------------------------------------------
    | DASHBOARD AUTEUR
    |----------------------------------------------------------------------
    */
    
    /**
     * Dashboard personnel de l'auteur
     * 
     * URL : http://localhost:8000/dashboard
     * Méthode : GET
     * Contrôleur : DashboardController::index()
     * Nom : dashboard
     * Middleware : auth
     * 
     * Affiche les statistiques et la liste des articles de l'auteur.
     */
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    
    /*
    |----------------------------------------------------------------------
    | GESTION DU PROFIL UTILISATEUR
    |----------------------------------------------------------------------
    */
    
    /**
     * Formulaire d'édition du profil
     * 
     * URL : http://localhost:8000/profile
     * Méthode : GET
     */
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    
    /**
     * Mettre à jour le profil
     * 
     * URL : http://localhost:8000/profile
     * Méthode : PATCH
     * 
     * PATCH = méthode HTTP pour mise à jour partielle
     * Différence avec PUT : PATCH modifie certains champs, PUT remplace tout
     * 
     * Formulaire HTML correspondant :
     * <form action="{{ route('profile.update') }}" method="POST">
     *     @csrf
     *     @method('PATCH')
     */
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    
    /**
     * Supprimer le compte
     * 
     * URL : http://localhost:8000/profile
     * Méthode : DELETE
     * 
     * DELETE = méthode HTTP pour suppression
     * 
     * Formulaire HTML :
     * <form action="{{ route('profile.destroy') }}" method="POST">
     *     @csrf
     *     @method('DELETE')
     */
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
    
    /*
    |----------------------------------------------------------------------
    | CRÉATION D'ARTICLE
    |----------------------------------------------------------------------
    */
    
    /**
     * Formulaire de création d'article
     * 
     * URL : http://localhost:8000/posts/create
     * Méthode : GET
     */
    Route::get('/posts/create', [PostController::class, 'create'])->name('posts.create');
    
    /**
     * Enregistrer un nouvel article
     * 
     * URL : http://localhost:8000/posts
     * Méthode : POST
     */
    Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
    
    /*
    |----------------------------------------------------------------------
    | ÉDITION / SUPPRESSION D'ARTICLE
    |----------------------------------------------------------------------
    | Ces routes vérifient l'ownership dans le contrôleur :
    | if (auth()->id() !== $post->user_id) abort(403);
    */
    
    /**
     * Formulaire d'édition d'article
     * 
     * URL : http://localhost:8000/posts/123/edit
     * Méthode : GET
     */
    Route::get('/posts/{post}/edit', [PostController::class, 'edit'])->name('posts.edit');
    
    /**
     * Mettre à jour un article
     * 
     * URL : http://localhost:8000/posts/123
     * Méthode : PUT
     * 
     * PUT = méthode HTTP pour mise à jour complète
     */
    Route::put('/posts/{post}', [PostController::class, 'update'])->name('posts.update');
    
    /**
     * Supprimer un article
     * 
     * URL : http://localhost:8000/posts/123
     * Méthode : DELETE
     */
    Route::delete('/posts/{post}', [PostController::class, 'destroy'])->name('posts.destroy');
    
    /*
    |----------------------------------------------------------------------
    | MODÉRATION DES COMMENTAIRES
    |----------------------------------------------------------------------
    | Seul l'auteur de l'article peut modérer ses commentaires.
    | Vérification ownership dans le contrôleur.
    */
    
    /**
     * Approuver un commentaire
     * 
     * URL : http://localhost:8000/comments/123/approve
     * Méthode : PATCH
     */
    Route::patch('/comments/{comment}/approve', [CommentController::class, 'approve'])->name('comments.approve');
    
    /**
     * Supprimer un commentaire
     * 
     * URL : http://localhost:8000/comments/123
     * Méthode : DELETE
     */
    Route::delete('/comments/{comment}', [CommentController::class, 'destroy'])->name('comments.destroy');
});

/*
|--------------------------------------------------------------------------
| ROUTES AVEC EMAIL VÉRIFICATION (Optionnel)
|--------------------------------------------------------------------------
| Si vous souhaitez forcer la vérification d'email pour certaines actions,
| ajoutez le middleware 'verified' :
|
| Route::middleware(['auth', 'verified'])->group(function () {
|     Route::get('/posts/create', ...);
|     // L'utilisateur doit avoir vérifié son email pour créer un article
| });
|
| Actuellement désactivé pour simplifier le développement.
*/
```

<small>*Le **Route Model Binding** (`{post:slug}`) est une fonctionnalité puissante de Laravel : au lieu de faire manuellement `Post::where('slug', $slug)->firstOrFail()` dans chaque méthode, Laravel l'injecte automatiquement. Si le slug n'existe pas, Laravel retourne une 404 automatiquement. Le middleware `auth` utilise les guards définis dans `config/auth.php` : par défaut, il vérifie la session web standard. Pour une API, vous utiliseriez `auth:sanctum`.*</small>

### Vérification des Routes Configurées

**Lister toutes les routes :**

```bash
# Afficher toutes les routes enregistrées
php artisan route:list

# Filtrer par nom
php artisan route:list --name=posts

# Filtrer par méthode
php artisan route:list --method=GET

# Sortie compacte (seulement URI, Méthode, Nom)
php artisan route:list --columns=uri,method,name
```

**Sortie attendue (extrait) :**

```
GET|HEAD  /                                home
GET|HEAD  /posts/{post:slug}               posts.show
GET|HEAD  /category/{category:slug}        categories.show
GET|HEAD  /author/{user}                   authors.show
POST      /posts/{post}/comments           comments.store

GET|HEAD  /login                           login
POST      /login                           
GET|HEAD  /register                        register
POST      /register                        
POST      /logout                          logout

GET|HEAD  /dashboard                       dashboard           auth
GET|HEAD  /profile                         profile.edit        auth
PATCH     /profile                         profile.update      auth
DELETE    /profile                         profile.destroy     auth
GET|HEAD  /posts/create                    posts.create        auth
POST      /posts                           posts.store         auth
GET|HEAD  /posts/{post}/edit               posts.edit          auth
PUT       /posts/{post}                    posts.update        auth
DELETE    /posts/{post}                    posts.destroy       auth
PATCH     /comments/{comment}/approve      comments.approve    auth
DELETE    /comments/{comment}              comments.destroy    auth
```

<small>*La colonne `Middleware` affiche les middlewares appliqués. Les routes avec `auth` nécessitent une authentification. Les routes Breeze (`/login`, `/register`, etc.) sont définies dans `routes/auth.php` et apparaissent sans nom pour certaines (Laravel les nomme automatiquement en interne).*</small>

### Tableau Récapitulatif des Routes

| URL | Méthode | Nom | Contrôleur | Action | Accès |
|-----|---------|-----|------------|--------|-------|
| `/` | GET | `home` | `HomeController` | Page d'accueil | Public |
| `/posts/{slug}` | GET | `posts.show` | `PostController` | Afficher article | Public |
| `/category/{slug}` | GET | `categories.show` | `CategoryController` | Articles catégorie | Public |
| `/author/{id}` | GET | `authors.show` | `AuthorController` | Profil auteur | Public |
| `/posts/{post}/comments` | POST | `comments.store` | `CommentController` | Créer commentaire | Public |
| **Breeze** | - | - | - | Auth complète | Public |
| `/dashboard` | GET | `dashboard` | `DashboardController` | Dashboard auteur | Auth |
| `/profile` | GET | `profile.edit` | `ProfileController` | Formulaire profil | Auth |
| `/profile` | PATCH | `profile.update` | `ProfileController` | MAJ profil | Auth |
| `/profile` | DELETE | `profile.destroy` | `ProfileController` | Supprimer compte | Auth |
| `/posts/create` | GET | `posts.create` | `PostController` | Formulaire création | Auth |
| `/posts` | POST | `posts.store` | `PostController` | Créer article | Auth |
| `/posts/{post}/edit` | GET | `posts.edit` | `PostController` | Formulaire édition | Auth |
| `/posts/{post}` | PUT | `posts.update` | `PostController` | MAJ article | Auth |
| `/posts/{post}` | DELETE | `posts.destroy` | `PostController` | Supprimer article | Auth |
| `/comments/{id}/approve` | PATCH | `comments.approve` | `CommentController` | Approuver | Auth |
| `/comments/{id}` | DELETE | `comments.destroy` | `CommentController` | Supprimer | Auth |

## Récapitulatif Phases 5

✅ **Phase 5 - Routes Configurées** :

- 5 routes publiques (home, show, category, author, comment)
- Routes Breeze (authentification complète)
- 12 routes protégées (dashboard, CRUD, modération)

✅ **Compétences Maîtrisées** :

- Architecture MVC complète
- Route Model Binding (`:slug`)
- Middleware (`auth`)
- Groupes de routes
- Nommage de routes (`name()`)
- Méthodes HTTP (GET, POST, PUT, PATCH, DELETE)
- Protection CSRF automatique
- Vérification ownership
- Eager Loading optimisé
- Validation de formulaires
- Messages flash

!!! success "Phases 5 Terminées - Votre application dispose maintenant de **toute la logique fonctionnelle** et **toutes les URLs configurées**. Il ne reste plus qu'à créer les **vues Blade** (Phase 6) pour afficher l'interface utilisateur, puis tester le tout (Phase 7). Vous êtes à 70% du projet terminé !"
