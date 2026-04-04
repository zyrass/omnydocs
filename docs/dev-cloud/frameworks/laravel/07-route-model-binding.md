---
description: "Injecter directement l'objet Modele concerné dans la route pour simplifier la syntaxe."
icon: lucide/git-merge
tags: ["LARAVEL", "BINDING", "MODEL"]
---

# Le Route Model Binding

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="1 Heure">
</div>

## 1. La Problématique

Regardez ce code répétitif classique d'un controller :

```php
public function show($id)
{
    $post = Post::findOrFail($id); // Répétition
    return view('posts.show', ['post' => $post]);
}

public function edit($id)
{
    $post = Post::findOrFail($id); // Répétition
    return view('posts.edit', ['post' => $post]);
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id); // Répétition
    $post->update($request->validated());
}
```

**Répétition flagrante :** `Post::findOrFail($id)` dans chaque méthode. Laravel peut automatiser cette recherche.

<br>

---

## 2. Route Model Binding automatique

Si vous remplacez l'ID et que vous exigez que la route trouve le modèle `Post` à votre place, la méthode sera allégée.

**Avant (manuel) :**

```php
Route::get('/posts/{id}', [PostController::class, 'show']);

public function show($id)
{
    $post = Post::findOrFail($id);
    // ...
}
```

**Après (automatique) :**

```php
// 1. Paramètre de route nommé {post} (singulier du modèle visé)
Route::get('/posts/{post}', [PostController::class, 'show']);

// 2. Type-hinting Post dans la signature de méthode au lieu de l'$ID int
public function show(Post $post)
{
    // Laravel a déja fait la requête failOuTrouve ($post)
    return view('posts.show', ['post' => $post]);
}
```

**Que s'est-t-il passé ?**

1. Laravel voit `{post}` dans le fichier des routes
2. Laravel voit `Post $post` dans la méthode `show()` du controller
3. Laravel demande automatiquement à la base de donnée `Post::where('id', $valeurDansURL)->firstOrFail()`
4. Si le post n'existe pas, retour automatique d'une erreur 404 neutre.

### 2.2 Paramètre de route alternatif (Le Slug)

Si vous voulez qu'un URL affiche un mot (Exemple : `/posts/mon-dernier-article`) plutot qu'un ID abstrait en chiffre, vous pouvez demander le Mode Binding de changer son capteur d'information vers `slug`.

**Étape 1 : Le Modéle**

```php title="app/Models/Post.php"
class Post extends Model
{
    // Autoriser la surcharge sur le getRouteKeyName par défaut
    public function getRouteKeyName()
    {
        return 'slug';
    }
}
```

**Étape 2 : Controller et Vues adaptées**

```php
// Les appels de routes doivent maintenant fournir le model post complet ou la clef associée.
// URL générée : /posts/mon-premier-article (A la place de l'ID 42)
<a href="{{ route('posts.show', $post) }}">Voir</a>
```

<br>

---

## Conclusion

Cette syntaxe accélère drastiquement le développement et nettoie la lisibilité de vos methodes Controller. La gestion de la donnée transmise se clôture par son atterrissage vers une vue ou une redirection.
