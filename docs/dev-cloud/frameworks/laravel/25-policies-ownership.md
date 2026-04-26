---
description: "Structurer la gestion des droits ciblés et granulaires par ressource (Ownership)."
icon: lucide/book-open-check
tags: ["LARAVEL", "AUTORISATION", "POLICIES", "OWNERSHIP"]
---

# Ownership & Policies

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. La limite des Gates : La "Policy" de ressource

Une **Policy** est une classe dédiée qui regroupe **toutes les règles d'autorisation** pour un modèle de votre base de donnée spécifique (Ici pour l'exemple qui sera souvent évoqué : Le Modele Post de vos articles).

Elle gère des **Scopes granulaires** ("Peut-il modifier CE post N°4 en particulier ?").

```bash
php artisan make:policy PostPolicy --model=Post
```

Une classe se créé et intègre un CRUD complet et formaté des accès que l'ont pourrait valider ou non.

```php title="app/Policies/PostPolicy.php"
class PostPolicy
{
    // L'utilisateur Alain a til le droit de MODIFIER l'Instance ID 4 du POST ciblé ?
    public function update(User $user, Post $post): bool
    {
        // OUI ! Car l'ID de L'auteur et de l'utilisateur correspond : OWNERSHIP !!
        if ($user->id === $post->user_id) { return true; } 
        
        // ET OUI !! L'utilisateur de la session à forcé le bypass car il etait ADMIN (Les admins peuvent modifier un post) !
        if ($user->is_super_admin) { return true; }    

        // Ou NON !!
        return false;
    }

    public function delete(User $user, Post $post): bool
    {
        // Un auteur ne peut pas détruire son post. La fonction booléenne est stricte pour SEULEMENT les admins.
        return $user->is_super_admin === true;
    }
}

// NOTE DE DECOUVERTE AUTO ! : Laravel 11 lie automatiquement "Modele" avec "ModelePolicy" de nommage ! Pas besoin déclarer cette logique manuelle !
```

<br>

---

## 2. Invoquer son Ownership dans le Controlleur Métier !

De retour dans notre Controller pour valider l'action d'édition une fois le bouton cliqué !

```php title="app/Http/Controllers/PostController.php"
class PostController extends Controller
{
    // Souvenez-vous, grâce au Route Model Binding, le Modele s'injecte tout seuls aux parametres d'update d'URL !
    public function update(Request $request, Post $post)
    {
        // 1. Autorisation de Sécurité ! Qui essaye de faire quoi ? Le framework injecte magiquement le User et l'Option.
        $this->authorize('update', $post); 
        
        // 2. C'est bon, on Valide et on envoie en base !
        $post->update($request->validate([ ... ]));
        return redirect()->route('posts.show', $post);
    }
}
```

```html title="resources/views/posts/element.blade.php"
{{-- Côté Vue Visuelle , La Directive Policy attends un Modele Ciblé si elle est de type 'update' !! --}}
@can('update', $post)
    <a href="{{ route('posts.edit', $post) }}">Modifier</a>
@endcan
```

```php title="routes/web.php"
// Côté Protection Réseau, Le Middleware attend une cible Modele par le slug {post} également !
Route::get('/posts/{post}/edit', [PostController::class, 'edit'])->middleware('can:update,post');
```

<br>

---

## L'exception `before()`

La méthode `before()` est exécutée en sous marin **avant TOUTES les autres méthodes** de la policy d'un bloc Modèle (Update, Delete, Edit, Create, etcc.).

Elle permet un **Super Admin Bypass**, ce qui allège grandement le code `|| $user->isAdmin()` qui parsemait la Policy dans les fonctions `update( )` plus haut si vous vous en souvenez ! Ce bypass s'execute donc, avant toute choses et force le oui :

```php title="app/Policies/PostPolicy.php"
class PostPolicy
{
    // AVANT MEME DE LIRE CE QU'IL SUIT, SI LE COMPTE EST SUPER ADMIN, NE CHERCHE PAS A COMPRENDRE LES REGLES ET DIS : OUI.
    public function before(User $user, string $ability): ?bool
    {
        if ($user->is_super_admin === true) { return true; } // Bypass.
        return null; // Si ça n'est qu'un "simple" utilisateur de base, laisse la suite checker ses droits.
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les Policies formalisent une règle fondamentale : la propriété d'une ressource ne doit jamais être vérifiée dans la vue ou dans le contrôleur. En déléguant cette logique à une Policy, vous créez un contrat explicite, testable et centralisé qui garantit qu'un utilisateur ne pourra jamais modifier l'article d'un autre, quelle que soit la route empruntée.

> [Policies maîtrisées. Structurez maintenant votre système de rôles applicatif →](./26-rbac-et-middlewares.md)
