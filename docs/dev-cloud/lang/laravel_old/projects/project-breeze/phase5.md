---
description: "Middleware d'authentification, gates et policies pour sécuriser les routes et les actions sur les ressources."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 5 — Autorisation & Middleware

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Laravel 11"
  data-time="~45 minutes">
</div>

## Objectifs de la Phase 5

!!! info "Ce que vous allez faire"
    - Comprendre les middleware `auth` et `verified` de Breeze
    - Créer un middleware personnalisé (`EnsureProfileIsComplete`)
    - Implémenter une Policy de base pour protéger des ressources
    - Tester les redirections non autorisées

## Middleware Personnalisé

```bash
php artisan make:middleware EnsureProfileIsComplete
```

```php title="app/Http/Middleware/EnsureProfileIsComplete.php"
public function handle(Request $request, Closure $next): Response
{
    if (auth()->check() && !auth()->user()->bio) {
        return redirect()->route('profile.edit')
            ->with('warning', 'Veuillez compléter votre profil avant de continuer.');
    }

    return $next($request);
}
```

```php title="bootstrap/app.php — Enregistrement du middleware"
->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'profile.complete' => \App\Http\Middleware\EnsureProfileIsComplete::class,
    ]);
})
```

```php title="routes/web.php — Application du middleware"
Route::middleware(['auth', 'verified', 'profile.complete'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
});
```

## Policy Simple

```bash
php artisan make:policy PostPolicy --model=Post
```

```php title="app/Policies/PostPolicy.php"
public function update(User $user, Post $post): bool
{
    // Seul le propriétaire peut modifier son post
    return $user->id === $post->user_id;
}
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le middleware est le gardien des routes, la Policy est le gardien des ressources. Ces deux niveaux de protection sont complémentaires : le middleware vérifie si l'utilisateur peut **accéder à la route**, la Policy vérifie s'il peut **effectuer l'action sur cette ressource spécifique**. Confondre ces deux niveaux génère des failles de sécurité subtiles difficiles à détecter en revue de code.

> [Phase 6 — Tests PHPUnit de l'authentification →](./phase6.md)
