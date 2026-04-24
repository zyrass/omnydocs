---
description: "Découvrir la subtilité entre authentifier et autoriser, puis l'appuyer techniquement via des Gates."
icon: lucide/book-open-check
tags: ["LARAVEL", "AUTORISATION", "GATES", "PERMISSIONS"]
---

# L'Autorisation vs Authentification

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Introduction au module

!!! quote "Analogie pédagogique"
    _Au module de Sécurité 4, vous avez implémenté le badge (Authentification). Ici, nous implémentons le laisser passer **(L'Autorisation)**. Le PDG peut consulter les comptes, le développeur les serveurs, mais pas les audits. C'est le système de permissions : qui ? que ? ou ? et comment ?_

| Concept | Question posée | Mécanisme Laravel |
|---------|----------------|-------------------|
| **Authentification** | Qui es-tu ? | Sessions, cookies, tokens |
| **Autorisation** | Que peux-tu faire ? | Gates, Policies |

<br>

---

## 1. La définition de Gates ("Les Portes")

Un **Gate** est une barrière qui encadre une Action Booléenne Globale au sein du code de Laravel.

- **Scope** : Très Modeste. Se base sur le système et non le Modèle Modifié.
- **Retourne** : `true` ou `false`

1. Exemples de conditions : L'utilisateur est-il admin ?
2. Exemples de conditions : L'utilisateur peut-il accéder au backoffice ?
   
### 1.1 Configurer les Permissions Globales 

On le déclare dans le Fournisseur Global de tous nos codes `AppServiceProvider.php` :

```php title="app/Providers/AppServiceProvider.php"
use Illuminate\Support\Facades\Gate;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // 1. Definition du Role
        Gate::define('admin', function (User $user) {
            return $user->is_super_admin === true; // On admet que true est l'ID 1
        });
        
        // 2. Definition d'Actions Complexes liées au Role !
        Gate::define('submit-post', function (User $user) {
            // Est T-IL Auteur ? ET N'EST-IL PAS Banni ?
            return $user->is_author_approved === true && $user->is_banned !== true;
        });
    }
}
```

### 1.2 Invoquer l'autorisation

Maintenant ce profil créé, le framework s'empare lui même dans ces contrôleurs Web de l'intelligence pour savoir si un humain à l'accès. 

```php title="app/Http/Controllers/Private/DashboardController.php"
class DashboardController extends Controller
{
    public function index()
    {
        // "Est-ce qu'il peut passer la condition ADMIN de mon AppService ?" 
        // Si OUI : Poursuit le script. / Si NON : Crash volontaire du site en ERREUR FATALE PUBLIC 403 !
        Gate::authorize('admin');
        
        // Autre solution : Un test non destructif avec Redirection si ECHEC.
        if (Gate::denies('admin')) { abort(403, 'Accès refusé : réservé aux administrateurs.'); }
        
        // Autre solution (Inverse) : Un test non destructif avec Action direct (Allows plutôt que Denies).
        if (Gate::allows('admin')) { return view('admin.dashboard'); }
    }
}
```

### 1.3 Cacher le rendu visuel selon autorisation

Etant l'essence des écrans interactifs, vous pourrez masquer très facilement un objet si l'utilisateur courant ne détient pas **ce droit global**.

```html title="resources/views/posts/list.blade.php"
{{-- Se base sur votre AppServiceProvider -> 'author' --}}
@can('author')
    <a href="{{ route('posts.create') }}">Nouveau post</a>
@endcan

@cannot('author')
    <p>Votre compte auteur est en attente de validation.</p>
@endcannot
```

<br>

---

## 2. Bloquer les URLs au routage global !

Un système de sécurité sans protection URL des Controller par Intercepteur (`Middlewares`) est un gruyère.
Si vous vous souvenez bien, il suffirait de créer la fonction `Gate` en forme de Bouclier.

Cependant depuis Laravel 11+, un middleware `can` est pré-construit dans le moteur et vous vous dispense l'écriture d'une couche Bouclier dans le dossier Controller en testant la chaine du ServiceProvider :

```php title="routes/web.php"
Route::middleware('can:admin')->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'dashboard']);
});
```

<br>

---

## Conclusion 

Les Gates sont très basiques. Elles limitent le paramétrage sans aucune analyse de ressource, "Est t'il l'auteur de l'article ?", pour celà il va nous falloir utiliser les Policies.
