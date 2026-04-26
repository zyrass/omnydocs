---
description: "Vérrouiller les URLs et créer des sessions persistantes."
icon: lucide/book-open-check
tags: ["LARAVEL", "MIDDLEWARE", "HELPER", "REMEMBER"]
---

# Middlewares & Sessions Longues

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Protéger et Cacher : Les Intercepteurs (Middlewares)

Nous ne l'avons pas précisé pendant le routage de l'étape précédente, mais sans une méthode global d'arrêt pour empêcher n'importe quelle requête URL brute vers des écrans privés, votre base est exposée.
Il faut créer les fameux mots clefs de bouclage de section routières : `->middleware('guest')` par exemple.

### 1.1 Le Bouclier Auth (Accès Privés)

```bash
php artisan make:middleware Authenticate
```

```php title="app/Http/Middleware/Authenticate.php"
// Vérifie si l'utilisateur est connecté (session). Si non, le bloque !
class Authenticate
{
    public function handle(Request $request, Closure $next): Response
    {
        if (!$request->session()->has('user_id')) {
            // intended() bloque l'action et redirige ou l'on souhaite.
            return redirect()->guest(route('login'));
        }

        // Il détient son jeton de session. Autorisé. Continuer... => $next
        return $next($request);
    }
}
```

### 1.2 Le Bouclier Guest (Redirections Inverse)

La page d'inscription et de login n'a aucune utilité si l'utilisateur est déjà dans son panel de controle ! Vous ne voulez pas qu'il puisse y accéder, ça briserait le processus logique.

```bash
php artisan make:middleware RedirectIfAuthenticated
```

```php title="app/Http/Middleware/RedirectIfAuthenticated.php"
// Laisse accès librement si Non Identifié, bloque l'accès si un utilisateur l'est.
class RedirectIfAuthenticated
{
    public function handle(Request $request, Closure $next): Response
    {
        // Si l'utilisateur est déjà connecté... 
        if ($request->session()->has('user_id')) {
            return redirect()->route('dashboard'); // On le jete sur le panel controle
        }

        return $next($request); // On le laisse passer libre.
    }
}
```

L'application de ses "mots clefs d'interception" s'effectue dans le noyaux du code, puis, elle s'utilise facilement dans le groupe des Web Routes.

```php title="bootstrap/app.php"
->withMiddleware(function (Middleware $middleware) {
    // Relier les classes de blocage vers le mot clef sémantique facile pour le routier
    $middleware->alias([
        'auth' => \App\Http\Middleware\Authenticate::class,
        'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    ]);
})
```

```php title="routes/web.php"
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', function () { return view('dashboard'); });
});
```

<br>

---

## 2. Le Helper de Session (Connaitre son Utilisateur)

Vos routes étant protégés et l'accès autorisé, il y a de grosses probabilités que vos vues nécessitent d'afficher le `Nom` ou l'`Avatar` de la personne en train de lire le site !

```html
@if (user())
    <span>Bonjour, {{ user()->name }} !</span>
@else
    <a href="{{ route('login') }}">Connexion</a>
@endif
```

Sémantiquement, cela s'écrira `auth()->user()`. Avoir un accès rapide à cette fonctionnalité par le raccourci `user()` est commun si le framework vous bloque l'accès aux variables magiques (`{{ Auth::user()->name }}`).

C'est d'ailleurs ce procédé qui vous permets de bloquer l'usage des commentaires à cet utilisateur précis depuis le controller :
`$comment->user_id = auth()->user()->id;` ou d'hydrater la base avec the relations : `$user->comments()->create($request->validated());`

<br>

---

## 3. Options : "Remember Me" (Rester connecté)

Par défaut, la session du site et son jeton éphémères disparaissent à la fermeture de toute fenêtre web de l'ordinateur de l'utilisateur. S'il n'est pas logué depuis 6 heures, un script le détruit également. Vous pouvez imposer un Cookie Longue Durée de validation.

* **Étape 1 :** Assurez un champs token en mode `nullable` dans votre migrations Database User pour stocker sa longévité : (`$table->rememberToken();`).
* **Étape 2 :** Générez le token persistant à l'endroit ou vous lui cédez le passage lors de l'auth. 

```php title="app/Http/Controllers/Auth/AuthController.php"
// Dans la méthode de soumission de Login ! Après la regénération par protection.

if ($request->boolean('remember')) { // Checkbox Remember cochée !
        
        $token = \Str::random(60); // Random Chaine de caracteres massives.
        $user->remember_token = $token;
        $user->save(); // Inséré dans le model 
        
        // Forger en Cookie Persistant du coté des entrailles du navigateur Visiteur sur 30 Jours !
        cookie()->queue(
            'remember_token',
            $token,
            60 * 24 * 30 
        );
}
```

* **Étape 3** : Modifier le middleware d'interception d'origine ! Eh oui, si ce visiteur revient le lendemain sur le dashboard, avant de le bloquer en `$next`, il faudra relire ce ficher magique enfoui !

```php title="app/Http/Middleware/Authenticate.php"
// Si vous échouez par ID classique dans le controller Auth... On intercepte et compare si une variable se balade chez lui.
$rememberFileNavigator = $request->cookie('remember_token');
    
if ($rememberFileNavigator) {
    // Il a le fichier vieux de 25 jours chez lui. Le cherche t-on sur la base de donnée globale de l'app ?
    $userModel = User::where('remember_token', $rememberFileNavigator)->first();
    
    if ($userModel) {
        $request->session()->put('user_id', $userModel->id); // On re-valide ce faux contact !
        return $next($request); 
    }
}
```

Sans oublier de demander à votre fonction de délogement de supprimer par `make($cookie)->forget()` cette chaine si l'utilisateur décide volontairement de la révoquer de sa propre initiative dans son panel.

<br>

---

## Conclusion 

Le système complet de routage protégé des requêtes URL et de gestions d'informations par session d'une durée illimité est en place. Un système complet vous évitera alors la lourde tache de réinventer l'Authentication par vous même comme nous venons de l'apprendre. Mais avant de passer aux starter-kits de l'écosystème Laravel, il est temps de boucler nos connaissance de sécurisation sur les Failles Hackeurs.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un middleware est un gardien transparent. Il intercepte la requête avant qu'elle n'atteigne le contrôleur, applique une règle (est-ce que l'utilisateur est authentifié ? son email est-il vérifié ?) et laisse passer ou bloque. Cette séparation évite de polluer chaque méthode de contrôleur avec des vérifications d'accès répétitives.

> [Middlewares maîtrisés. Approfondissez avec la sécurité CSRF et l'anti-bruteforce →](./23-securite-csrf-bruteforce.md)
