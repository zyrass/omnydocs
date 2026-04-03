---
description: "Rediriger le flux utilisateur via des Flash Messages, des groupes de routes et des Middlewares."
icon: lucide/arrow-right-left
tags: ["LARAVEL", "REDIRECTIONS", "FLASH", "MIDDLEWARE"]
---

# Redirections, Messages Flash & Groupes de Routes

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="1 Heure">
</div>

## 1. Redirections et messages flash

### 1.1 Types de redirections

Laravel offre plusieurs façons de renvoyer l'utilisateur vers de l'affichage HTML :

```php
// Redirection absolue (A éviter en production)
return redirect('/posts');

// Redirection via les noms de route (Recommandé)
return redirect()->route('posts.index');

// Redirection vers une route nommée comprenant des paramètres modèles
return redirect()->route('posts.show', $post);

// Redirection vers la page précédente (ex: après une erreur de validation)
return back();

// Redirection vers la page d'accueil principale configurée
return redirect()->home();
```

### 1.2 Messages flash (Session jetable)

Les **messages flash** sont des données stockées dans la session PHP pour **une seule requête** (elles disparaissent après s'être affichées une fois à l'utilisateur).

**Définir un message flash :**

```php
return redirect()
    ->route('posts.index')
    ->with('success', 'Post créé avec succès !');
    
// Des équivalents sémantiques sont utilisables pour 'success'
// Exemple : error, warning, info
```

**Afficher le message dans l'interface (Blade) :**

Idéalement il ne faut pas mettre cela par page, mais dans un Fichier Maître de Layout général pour que cela englobe la structure web.

```html
@if (session('success'))
    <div style="background: green; color: white; padding: 10px;">
        {{ session('success') }}
    </div>
@endif
```

<br>

---

## 2. Groupes de routes et Middlewares

Pour éviter la répétition dans le fichier `web.php`, il est de coutume de regrouper les routes partageant un préfixe textuel pour l'URL ou un intercepteur logique (Middleware).

### 2.1 Structurer par Groupe

**Sans groupe (Trop Tôt) :**

```php
Route::get('/admin/users', [AdminController::class, 'users']);
Route::get('/admin/posts', [AdminController::class, 'posts']);
Route::get('/admin/settings', [AdminController::class, 'settings']);
```

**Avec groupe combiné (Pro) :**

```php
Route::prefix('admin')->name('admin.')->group(function () {
    Route::get('/users', [AdminController::class, 'users'])->name('users');
    
    // Impact:
    // URL générée attendue: /admin/users
    // Nom généré attendu (pour les vues Blade): route('admin.users')
});
```

### 2.2 Appliquer un intercepteur (Middleware) à un groupe complet

Les **middlewares** sont des "douanes" appliquées aux requêtes. Nous aborderons leur création plus loin, mais voici comment les associer.

**Exemple : Protéger les routes admin d'un visiteur non loggué :**

```php
// Le middleware global `auth` est invoqué et renvoi à la page de Login s'il échoue.
Route::prefix('admin')
    ->name('admin.')
    ->middleware('auth')
    ->group(function () {
        
        Route::get('/dashboard', [AdminController::class, 'dashboard'])
            ->name('dashboard');
            
    });
```

<br>

---

## Conclusion

Le circuit est fermé, les données sont redirigées avec accusé de réception ou conditionnées, et le visiteur reste bloqué s'il va trop vite dans des URL protégées par vos groupes. L'achèvement du Module 2 requiert une évaluation des acquis.
