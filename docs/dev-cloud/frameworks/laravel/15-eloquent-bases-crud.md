---
description: "Les opérations CRUD via la syntaxe Eloquent."
icon: lucide/book-open-check
tags: ["LARAVEL", "ELOQUENT", "CRUD"]
---

# Eloquent : Syntaxe CRUD

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Créer le Model d'abstraition centralisateur

Le Model Eloquent est au cœur des opérations.

```bash
# Artisan créé le modèle Post. Il induira qu'il cherche la table 'posts' de part le format singulier.
php artisan make:model Post
```

**Dissécoquons son système de protection de variables :**

```php title="app/Models/Post.php"
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Colonnes assignables en masse (mass assignment).
     * 
     * Protection contre l'injection de colonnes non désirées.
     * Exemple : si l'utilisateur envoie ['title' => '...', 'is_admin' => true],
     * seul 'title' sera accepté (is_admin n'est pas dans $fillable et sera avorté).
     */
    protected $fillable = [
        'user_id',
        'title',
        'slug',
        'body',
        'published_at',
    ];

    /**
     * Colonnes à caster (conversion automatique de type).
     * 
     * published_at sera automatiquement converti en objet Carbon pour le manipuler facilement sur les pages.
     */
    protected $casts = [
        'published_at' => 'datetime',
    ];
}
```

<br>

---

## 2. Le Cycle CREATE

**Le Formulaire standardisé Array() (Mass Assignment)**

```php
$post = Post::create([
    'user_id' => 1,
    'title' => 'Mon premier post',
    'body' => 'Contenu du post...',
]);

// C'est ce qui est massivement utilisé couplé avec la validation d'une Request Controller.
// Post::create($request->validated());
```

<br>

---

## 3. Le Cycle READ

A partir de ce moment, vos conditions IF et vos requêtes conditionnelles Select sont balayées.

**Récupération conditionnelle :**

```php
// SELECT * FROM posts WHERE user_id = 1
$posts = Post::where('user_id', 1)->get();

// SELECT * FROM posts WHERE title LIKE '%Laravel%'
$posts = Post::where('title', 'LIKE', '%Laravel%')->get();

// Exceptions en chaines conditionnelles
$posts = Post::where('user_id', 1)
    ->whereNotNull('published_at')
    ->get();
```

**Filtres et premier résultat :**

```php
// Trouver le premier element où l'author est Alain, et crache erreur 404 si introuvable.
$post = Post::where('user_name', 'Alain')->firstOrFail();

// Assigner le résultat du grand livre contable pour les afficher sur 10 items.
$posts = Post::latest()->limit(10)->get();

// Outils comptable de rapidité
$count = Post::where('user_id', 1)->count();
```

<br>

---

## 4. Le Cycle UPDATE

La méthode UPDATE s'utilise sur un modèle qui est déja repéré en Base (Et donc, chargé en variable par Route Model Binding ou par `find()`).

```php
// $post provient du controller (public function update(Request $request, Post $post))

$post->update([
    'title' => 'Titre modifié',
    'body' => 'Nouveau contenu',
]);
```

!!! danger "Performances"
    Il est possible de mettre en majuscule des milliers d'utilisateurs sans instancier tout les modeles :  
    `Post::where('user_id', 1)->update(['published_at' => now(),]);`  
    **Gare cependant**, cette approche rapide "aveugle" via chainage `update()` ne déclenchera aucun des écouteurs d'évènements automatiques, c'est considéré comme du forcing.

<br>

---

## 5. Le Cycle DELETE 

**Méthode de purge :**

```php
$post = Post::find(1);

// Exécute : DELETE FROM posts WHERE id = 1
$post->delete();

// Supprimer massivement ou sur conditions : (Toujours aveugle, pas d'évènements écoutés)
Post::destroy([1, 2, 3]);
Post::where('user_id', 1)->delete();
```

**Soft Delete (suppression douce) :**

Eloquent possède une mécanique native **`SoftDeletes`**. Au lieu de purger l'entrée de la table, Eloquent remplira un champs `deleted_at`, et **cachera instantanément les résultats** de toutes les requêtes frontales. Vous conservez ainsi vos archives pour les administrateurs sans risquer d'exoser au moteur de recherche des pages supprimées par des auteurs avec des remords.

<br>

---

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Eloquent ORM n'est pas un simple wrapper SQL — c'est un langage expressif qui transforme chaque table en objet vivant. La différence entre `Post::where('active', true)->latest()->take(5)->get()` et son équivalent SQL brut illustre parfaitement pourquoi Laravel est considéré comme le framework PHP le plus lisible au monde.

> [CRUD maîtrisé. Découvrez maintenant comment les modèles se parlent entre eux →](./16-relations-modeles.md)
