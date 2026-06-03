---
description: "Sécuriser les entrées de données via la validation serveur et les Form Requests."
icon: lucide/book-open-check
tags: ["LARAVEL", "VALIDATION", "REQUEST"]
---

# Validation côté serveur

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Pourquoi la validation serveur est indispensable

!!! danger "Règle d'or de la sécurité web"
    **JAMAIS** de confiance dans les données venant du client (navigateur). Même si vous validez en JavaScript côté client, un utilisateur malveillant peut contourner cette validation et envoyer des données invalides/malveillantes directement à votre serveur.

**La validation serveur est :**
- **Obligatoire** : Protège contre les attaques (Injections SQL, Scripts).
- **Automatique** : Laravel gère les erreurs et les redirections sans écrire de conditions à répétition.
- **Flexible** : Règles réutilisables et composables.

<br>

---

## 2. Validation dans le controller

### 2.1 Règles de validation courantes

La vérification se déclare sous forme de liste. La syntaxe est directe.

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'champ' => 'règle1|règle2|règle3',
    ]);
    
    // Si on arrive ici, la validation a réussi
    // $validated contient UNIQUEMENT les champs interceptés
}
```

| Règle | Signification | Exemple |
|-------|---------------|---------|
| `required` | Champ obligatoire | `'title' => 'required'` |
| `string` | Doit être une chaîne | `'title' => 'string'` |
| `min:X` | Longueur/valeur minimum | `'password' => 'min:8'` |
| `max:X` | Longueur/valeur maximum | `'title' => 'max:255'` |
| `unique:table,column` | Valeur unique en DB | `'email' => 'unique:users,email'` |
| `exists:table,column` | Valeur existe en DB | `'user_id' => 'exists:users,id'` |
| `confirmed` | Champ de confirmation | `'password' => 'confirmed'` |

### 2.2 Afficher les erreurs dans la vue Blade

Laravel stocke automatiquement les erreurs de validation dans une variable abstraite globale `$errors` accessible dans toutes les vues.

**Exemple de formulaire avec affichage d'erreurs :**

```html
{{-- resources/views/posts/create.blade.php --}}

<form method="POST" action="{{ route('posts.store') }}">
    @csrf
    
    <div>
        <label for="title">Titre :</label>
        <input 
            type="text" 
            id="title" 
            name="title" 
            value="{{ old('title') }}"
        >
        
        {{-- Affichage de l'erreur spécifique au champ --}}
        @error('title')
            <span style="color: red;">{{ $message }}</span>
        @enderror
    </div>
    
    <button type="submit">Créer</button>
</form>
```

**Explication des helpers Blade :**
1. **`@error('champ')`** : Bloc if spécifique ciblant un champs qui déclenche une erreur.
2. **`old('champ')`** : Récupère la valeur précédemment tapée (Évite à l'utilisateur de devoir tout resaisir si il se trompe sur 1 seul champ sur 10 présents).

<br>

---

## 3. Form Request : validation séparée (avancé)

Si votre logique de validation devient trop épaisse, sortez là du controller pour y dédier un nouveau fichier.

**Commande de génération :**

```bash
php artisan make:request StorePostRequest
```

**Fichier généré :**

```php title="app/Http/Requests/StorePostRequest.php"
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    /**
     * Retourner false ici génère une erreur 403 (Forbidden).
     * @return bool
     */
    public function authorize(): bool
    {
        // Pour l'instant, on autorise tout le monde
        return true;
    }

    /**
     * Définit les règles de validation.
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'body' => ['required', 'string', 'min:10'],
        ];
    }
}
```

**Utilisation dans le controller :**

```php
use App\Http\Requests\StorePostRequest;

// Remplacement du Request générique, par le Request typé
public function store(StorePostRequest $request)
{
    // La validation est automatique !
    $validated = $request->validated();
    $post = Post::create($validated);
    
    return redirect()
        ->route('posts.show', $post)
        ->with('success', 'Post créé !');
}
```

<br>

---

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation côté serveur n'est pas une option — c'est la dernière ligne de défense de votre application. Même si votre frontend valide parfaitement les données, un utilisateur malveillant peut contourner le navigateur et envoyer n'importe quelle requête directement à votre API. Laravel's `validate()` garantit que la logique métier ne reçoit jamais de données non conformes.

> [Validation sécurisée. Connectez maintenant votre application à une base de données →](./13-pourquoi-orm-et-migrations.md)
