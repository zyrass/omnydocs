---
description: "Application pratique de vos connaissances et auto évaluation."
icon: lucide/clipboard-list
tags: ["LARAVEL", "PRATIQUE", "EXERCICE", "BILAN"]
---

# Bilan du routing & Exercice pratique

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Exercice pratique : CRUD complet Catégories

Il est recommandé de se frotter au code au lieu de le lire pour retenir cet enseignement. L'objectif est ici de répéter de zéro un panel de controle sur le thème d'une **Catégorie**.

1. Lister toutes les catégories (Méthode Index)
2. Créer une nouvelle catégorie (Méthode Create & Store)
3. Afficher une catégorie (Méthode Show)
4. Modifier une catégorie (Méthode Edit & Update)
5. Supprimer une catégorie (Méthode Destroy)

**Contraintes :**
- Utiliser la console via `Route::resource()` et `-mcr`
- Utiliser le Route Model Binding
- Valider les données (Nom obligatoire, Type String, max 100 char)
- Afficher les messages flash de confirmation.

> La correction et l'entiéreté du code est disponible ci-dessous si le framework vous bloque.

### 1.1 Solution Terminal Artisan

```bash
# Génére la migration en BDD, le Model pour Laravel et le Controller Resource avec les 7 méthodes d'un coup.
php artisan make:model Category -mcr
```

```php title="database/migrations/xxxx_create_categories_table.php"
// Déplacer vous dans la database migration et insérez le nouveau champs Name.
public function up(): void
{
    Schema::create('categories', function (Blueprint $table) {
        $table->id();
        $table->string('name', 100);
        $table->timestamps();
    });
}
```

```bash
# Poussez la structure dans le Coffre Fort.
php artisan migrate
```

```php title="routes/web.php"
// Branchez la route générale Resource
Route::resource('categories', CategoryController::class);
```

### 1.2 Solution Controller

```php title="app/Http/Controllers/CategoryController.php"
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    public function index()
    {
        $categories = Category::latest()->get();
        return view('categories.index', compact('categories'));
    }

    public function create()
    {
        return view('categories.create');
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:100',
        ]);
        
        $category = Category::create($validated);
        
        return redirect()
            ->route('categories.index')
            ->with('success', 'Catégorie créée avec succès !');
    }

    public function show(Category $category)
    {
        return view('categories.show', compact('category'));
    }

    public function edit(Category $category)
    {
        return view('categories.edit', compact('category'));
    }

    public function update(Request $request, Category $category)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:100',
        ]);
        
        $category->update($validated);
        
        return redirect()
            ->route('categories.show', $category)
            ->with('success', 'Catégorie mise à jour !');
    }

    public function destroy(Category $category)
    {
        $category->delete();
        
        return redirect()
            ->route('categories.index')
            ->with('success', 'Catégorie supprimée !');
    }
}
```

### 1.3 Solution Interface Visual (Blade)

```html title="resources/views/categories/index.blade.php"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Catégories</title>
</head>
<body>
    <h1>Catégories</h1>
    
    @if (session('success'))
        <p style="color: green;">{{ session('success') }}</p>
    @endif
    
    <p><a href="{{ route('categories.create') }}">Nouvelle catégorie</a></p>
    
    <ul>
        @foreach ($categories as $category)
            <li>
                <!-- Un clic équivaut a une requete Method: Get -->
                <a href="{{ route('categories.show', $category) }}">
                    {{ $category->name }}
                </a>
                
                <!-- On englobe en Form car un simple Clic / Lien d'ancre HTML ne peut pas générer de method: Delete HTTP -->
                <form method="POST" action="{{ route('categories.destroy', $category) }}" style="display:inline;">
                    @csrf
                    @method('DELETE')
                    <button type="submit">Supprimer</button>
                </form>
            </li>
        @endforeach
    </ul>
</body>
</html>
```

<br>

---

## 2. Quiz d'auto-évaluation 

Avant de quitter le Module 2, validez les points suivants :

1. **Question :** Quelle est la différence entre PUT et PATCH ?
   <details>
   <summary>Réponse</summary>
   PUT remplace **entièrement** la ressource, PATCH la modifie **partiellement**. En pratique, Laravel traite les deux de manière similaire.
   </details>

2. **Question :** Que fait `Route::resource('posts', PostController::class)` ?
   <details>
   <summary>Réponse</summary>
   Génère automatiquement 7 routes CRUD (index, create, store, show, edit, update, destroy) avec leurs noms de route et méthodes HTTP correspondantes en une seule microscopique ligne.
   </details>

3. **Question :** Pourquoi utiliser `old('title')` dans un formulaire HTML ?
   <details>
   <summary>Réponse</summary>
   Pour réafficher la valeur que l'utilisateur venait de soumettre si il recoit une page d'erreur de validation retour, cela lui évite de retaper tout d'un coup.
   </details>

<br>

---

## Conclusion Générale

!!! quote "Récapitulatif"
    Le **routing et les controllers** sont le **système nerveux** de votre application Laravel. Chaque clic utilisateur, chaque formulaire soumis, passe par ce système. 
    
    Puisque ces concepts sont des standards universels, que vous construisiez un blog, un e-commerce ou une API REST, votre apprentissage d'un code propre est terminé et vous passez à la persistance des données complexe.

**Prochaine étape :**  
Le **Module 3** va transformer ces controllers en actions concrête et va percer les concepts de la Base de données (Database) avec la magie de l'ORM Eloquent. Il nous faudra générer des relations entitées (1 Utilisateur peut avoir N articles, etc).
