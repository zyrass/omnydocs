---
description: "Installation de Laravel en mode API pure et configuration de Sanctum pour une authentification par Personal Access Tokens (Stateless)."
icon: lucide/book-open-check
tags: ["SANCTUM", "API", "TOKENS", "STATELESS", "AUTH"]
---

# Phase 1 : API Laravel + Sanctum

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h - 2h">
</div>


!!! quote "Analogie pédagogique"
    _Sécuriser une API avec Sanctum s'apparente à donner un jeton d'accès temporaire à un livreur. Au lieu de lui donner les clés de la maison (authentification de session), vous lui donnez un badge qui ne permet d'ouvrir que la porte du garage, et qui peut être révoqué à tout moment._

## Objectif de la Phase

> Bienvenue dans le Niveau 3 ! Pour notre jeu vidéo en ligne (Dungeon RPG), nous abandonnons la gestion de session par cookie. Un jeu vidéo (ou une application mobile native) nécessite une authentification **Stateless** (sans état) basée sur l'échange de clés secrètes. Nous allons configurer Laravel Sanctum pour générer et vérifier des **Personal Access Tokens (PAT)**. Le serveur ne retiendra aucune "session" ; chaque requête devra contenir le token dans son en-tête.

!!! warning "Prérequis Techniques"
    Assurez-vous d'avoir PHP 8.2+, Node.js 22+, Composer et MySQL/PostgreSQL prêts sur votre machine.

## Étape 1.1 : Création du Projet Laravel (Mode API)

Laravel permet d'être installé avec un squelette optimisé pour ne servir que des API.

```bash
# Créer le projet
composer create-project laravel/laravel dungeon-rpg-api

cd dungeon-rpg-api

# Installer l'échafaudage API (ajoute routes/api.php et Sanctum)
php artisan install:api
```

La commande `install:api` fait le gros du travail :
1. Publie les migrations de Sanctum (la table `personal_access_tokens`).
2. Crée le fichier `routes/api.php`.
3. Met à jour `bootstrap/app.php` pour acheminer les requêtes vers ces routes.

## Étape 1.2 : Configuration de la Base de Données

Créez une base de données `dungeon_rpg` dans votre SGBD.

Configurez votre `.env` :

```bash title=".env"
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=dungeon_rpg
DB_USERNAME=root
DB_PASSWORD=
```

Puis exécutez les migrations (qui incluront la table des tokens de Sanctum) :

```bash
php artisan migrate
```

## Étape 1.3 : Préparer le Modèle User

Pour qu'un utilisateur puisse émettre des tokens, son modèle doit utiliser le trait `HasApiTokens`. Ouvrez `app/Models/User.php` et vérifiez :

```php title="app/Models/User.php"
namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens; // <-- INDISPENSABLE

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
    
    // ...
}
```

## Étape 1.4 : Le Contrôleur d'Authentification (Auth API)

Contrairement à Breeze ou Jetstream qui génèrent toute la logique d'authentification pour nous, dans une API pure (Stateless), c'est à nous d'écrire les endpoints qui vérifient le mot de passe et génèrent le token.

```bash
php artisan make:controller Api/AuthController
```

```php title="app/Http/Controllers/Api/AuthController.php"
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    /**
     * Inscription d'un nouveau joueur
     */
    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255|unique:users', // Pseudo du joueur
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        // Génère un token avec un nom spécifique (ex: 'rpg-game-client')
        $token = $user->createToken('rpg-game-client')->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token
        ], 201);
    }

    /**
     * Connexion (Génération du Token)
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        $user = User::where('email', $request->email)->first();

        // Vérification explicite du hash
        if (! $user || ! Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['Les identifiants fournis sont incorrects.'],
            ]);
        }

        // Création du Token
        $token = $user->createToken('rpg-game-client')->plainTextToken;

        return response()->json([
            'user' => $user,
            'token' => $token // Ce token doit être stocké côté client (Local Storage)
        ]);
    }

    /**
     * Déconnexion (Révocation du Token)
     */
    public function logout(Request $request)
    {
        // Révocation du token qui a été utilisé pour authentifier la requête actuelle
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'Déconnexion réussie, token révoqué.'
        ]);
    }
}
```

## Étape 1.5 : Sécurisation des Routes API

Déclarons maintenant ces endpoints dans `routes/api.php`. Notez la différence entre les routes "publiques" (Login/Register) et les routes "protégées" (Logout, User info).

```php title="routes/api.php"
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;

// --- Routes Publiques (Pas besoin de Token) ---
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// --- Routes Protégées (Nécessitent un Token Valide) ---
// Le middleware 'auth:sanctum' lit l'en-tête "Authorization: Bearer <token>"
Route::middleware('auth:sanctum')->group(function () {
    
    // Endpoint pour vérifier l'identité du joueur
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    // Révocation du token
    Route::post('/logout', [AuthController::class, 'logout']);
    
});
```

## Étape 1.6 : Test de la mécanique API (Postman / Insomnia)

Il est indispensable de vérifier que le flux de jetons fonctionne avant de passer à la suite.

1. **Démarrer le serveur** : `php artisan serve`
2. **Requête Inscription (POST /api/register)** :
   Envoyez un body JSON avec `name`, `email`, `password`, `password_confirmation`.
   **Réponse attendue** : L'objet User + un long string `token` (ex: `1|18qM8s...`).
3. **Requête Accès Protégé (GET /api/user)** :
   - *Sans token* : Le serveur renvoie `401 Unauthorized`.
   - *Avec token* : Ajoutez un header HTTP `Authorization` avec la valeur `Bearer VOTRE_TOKEN_ICI`. Le serveur renvoie l'objet utilisateur `200 OK`.
4. **Requête Déconnexion (POST /api/logout)** :
   Utilisez le même en-tête `Authorization`. Le token sera supprimé de la base de données.
5. **Vérification Finale (GET /api/user)** :
   Tentez de refaire la requête 3 avec l'ancien token. Le serveur doit renvoyer `401 Unauthorized` car le token a été détruit.

!!! danger "Stockage des Tokens"
    Le token généré ne sera affiché qu'une **seule fois** (sous forme de `plainTextToken`). En base de données, Laravel ne stocke qu'un hash (empreinte SHA-256) du token. Si le client perd le token, il doit s'authentifier à nouveau (`/login`) pour en générer un nouveau.

## Conclusion de la Phase 1

L'authentification "API Pure" (Stateless) n'a plus de secret pour vous :
- ✅ **Sanctum** est configuré pour l'émission de Personal Access Tokens.
- ✅ Un contrôleur gère la **création**, la **validation** et la **révocation** sécurisée des clés.
- ✅ Les routes sont protégées et filtrent les accès non autorisés.

Dans la **Phase 2**, nous allons plonger dans le cœur de notre Jeu de Rôle (RPG) en modélisant les Personnages, les Monstres et la logique des Combats au tour par tour !

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Sanctum en mode API stateless (Personal Access Tokens) est fondamentalement différent du mode SPA : chaque requête transporte son token dans le header `Authorization: Bearer`. Ce modèle est conçu pour les clients mobiles, les applications tierces et les intégrations inter-services — pas pour les SPA hébergées sur le même domaine, où les cookies sont plus sécurisés.

> [Architecture API posée. Modélisez maintenant la base de données du projet →](./02-phase2.md)
