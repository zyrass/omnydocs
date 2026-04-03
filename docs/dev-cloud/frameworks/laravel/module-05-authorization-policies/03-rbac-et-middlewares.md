---
description: "Développer une hiérarchisation des Utilisateurs (Lecteur, Auteur, Editeur, Admin)"
icon: lucide/contact
tags: ["LARAVEL", "PERMISSIONS", "RBAC", "MIDDLEWARE", "SEEDERS"]
---

# Contrôle Role-Based (RBAC)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Déclarer la Hiérarchie et les Modèles

**Un Role Based (Contrôle d'accès basé sur les rôles)** s'articule comme ceci : 
1. Définir des permissions à chaque rôles (`DeletePost`, `EditPost`). 
2. Assigner des rôles (`Author`, `Admin`).

```bash
# Migration : On implémente le role en dur qui aura de facto la valeur la plus basse.
php artisan make:migration add_role_to_users_table --table=users
```

```php title="app/Models/User.php"
class User extends Authenticatable
{
    // Ajouter les accès rapide à tester d'un bloc User instancié ($user->isAdmin)
    public function isAdmin(): bool { return $this->role === 'admin'; }
    public function isAuthor(): bool { return $this->role === 'author'; }
    // En array multi vérifications par le tableau PHP.
    public function hasAnyRole(array $roles): bool { return in_array($this->role, $roles); }
}
```

```php title="database/seeders/UserSeeder.php"
class UserSeeder extends Seeder
{
    public function run(): void
    {
        // Seeder les Rôles Test !
        User::create(['name' => 'Admin Boss', 'role' => 'admin']);
        User::create(['name' => 'Alice Ecrivaine', 'role' => 'author']);
        User::create(['name' => 'Bob Le Lecteur', 'role' => 'reader']);
    }
}
```

<br>

---

## 2. Le Super Middleware custom d'Interception RBAC

Il est judicieux de construire son propre module custom de Middleware si les Gates de base ne suffissent pas à faire plier toutes la rigueur métier de votre système d'entreprise (Et que les Policies sont trop chirugicale par rapport à l'envie général).

Ce Middleware est capable d'ingérer de l'exterieur une cascade d'autorisation en tableaux : `isAdmin()`, `isAuthor()`.

```bash
php artisan make:middleware EnsureUserHasRole
```

```php title="app/Http/Middleware/EnsureUserHasRole.php"
class EnsureUserHasRole
{
    // Le ...$roles capte n'importe quelle longueur d'argument en paramètre route
    public function handle(Request $request, Closure $next, ...$roles): Response
    {
        // helper natif Laravel :: auth->user()
        $user = auth()->user(); 
        if (!$user) { abort(403, 'Crash FATAL Public 403 : Non Authentifié'); }
        
        // C'est ici que l'on vérifie depuis le Modèle la règle.
        if (!$user->hasAnyRole($roles)) {
            abort(403, 'Accès refusé : rôle d\'Entreprise insuffisant.');
        }

        return $next($request);
    }
}
```

Déclarons la façade verbale de Routage dans App : `->withMiddleware()`
`'role' => \App\Http\Middleware\EnsureUserHasRole::class`

Et nous pouvons donc envelopper les routes vitales en imposant le tableau des conditions "Ou" sans utiliser les Policies et/ou les Gates !

```php title="routes/web.php"
// L'admin seul sur son dashboard : role:admin
Route::middleware(['auth', 'role:admin'])->group(function () {});

// L'author est autorisé avec l'admin à créer !
Route::middleware(['auth', 'role:admin,author'])->group(function () {});
```
