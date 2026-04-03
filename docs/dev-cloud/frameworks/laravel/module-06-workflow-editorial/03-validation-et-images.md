---
description: "Découvrir la classe request dédiée et configurer le stockage du fichier localement"
icon: lucide/image-up
tags: ["LARAVEL", "UPLOAD", "STOREREQUEST", "VALIDATION"]
---

# Fichiers et Class Request

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Déporter la validation et sa structure de la vue...

S'il vous est apparu à la fin de notre processus que valider des tableaux contenant 5 éléments, des limites de taille, ou des extensions peut virer au cauchemar pour l'expérience et la lisibilité du controller... Une extraction sous le nom `FormRequest` est disponible.

```bash
php artisan make:request StorePostRequest
```

Cette classe prend en charge toutes les vérifications imaginables sur Laravel avant même que votre Controlleur ne lève le doigt sur les données ! En prime ? Vous pouvez y rajouter l'Auth de la vue si celà vous chante. `StoreImagePourNoel2025Request`, `UpdateEmailAuthRequest`, ces classes sont infinies, très modulaires !

```php title="app/Http/Requests/StorePostRequest.php"
class StorePostRequest extends FormRequest
{
    public function authorize(): bool { return true; } // On l'a déja couvert par policy ailleurs.

    // A. L'array massif du Formulaire Frontend validé
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
            'body' => ['required', 'string', 'min:10'],
            
            // Les Inputs des Images Multiples du Formulaire !!!
            'images' => ['required', 'array', 'min:1', 'max:5'],
            'images.*' => [
                'required',
                'image',                    // Doit être une image du côté Mime header ! (Sécurité Base)
                'mimes:jpeg,jpg,png,webp',  // Formats autorisés (Bloque les SVG scripts, etc)
                'max:2048',                 // 2MB max
                'dimensions:min_width=800,min_height=600', // Trop petit tu sors !
            ],
        ];
    }

    // B. Re-Mappe (override) de la config JSON des réponses natifs, avec des strings FR custom.
    public function messages(): array
    {
        return [
            'images.*.mimes' => 'Hé copain, tes formats déconnent. Le webp te sera bénéfique..',
            'images.*.dimensions' => 'Dimensions minimales : 800x600px.',
        ];
    }
}
```

<br>

---

## 2. Préparation du Système Local de Fichier

La configuration par défaut d'un espace local sans serveur Cloud est très stricte. Tout y sera privé sauf si explicitement listé. Si cela s'avère inutile en mode de développement "Run local", vous comprendrez très vite la nécéssité une fois votre application branché sur le vrai World Wide Web.

### Le Lien Physique Symlink

Pour qu'un fichier soit accessible via l'URL (`votre-site.com/storage/app/public/image.jpg`), il faut créer un lien symbolique.

```bash
php artisan storage:link
```
Cela crée un lien `public/storage` → `storage/app/public`. Cette commande simule une sorte de "raccourci". Ce que l'utilisateur lit ou ce que son navigateur va lire se redirige sur un "chemin dur" des méandres du coeur serveur web où est niché la VRAIE image (Ex `/var/www/mon-site-laravel/storage/app/public/images/avatar.jpg`). 

### L'upload de Fichier Multiples

Dans notre controller d'Auteur qui écrit un Brouillon par exemple... Voici comment son FormFrontend l'affecte de la manière la plus propre existante de l'ORM Laravel grace à notre Super Filtre : L'Application du Bouclier Custom `StorePostRequest`.

```php title="app/Http/Controllers/PostController.php"
    // Regardez bien ceci ! $request d'origine à disparu !! Le bouclier est actif !
    public function store(StorePostRequest $request)
    {
        $validated = $request->validated();
        
        $post = Post::create([
            'user_id' => user()->id,
            'title' => $validated['title'],
            'body' => $validated['body'],
        ]);

        // Uploader et enregistrer chaque image...
        foreach ($request->file('images') as $index => $image) {
            // Methode magique pour créer le fichier sur Disque local. $path est le texte de son URL sur DB ! (ex : /app/uploads/023924_test.jpg)
            $path = $image->store("posts/{$post->id}", 'public');
            
            // NOTE : Créer en parallèle l'enregistrement en table DB avec Model ImagePostImage::create();
        }
        return redirect()->route('posts.show', $post);
    }
```

Pour appeler depuis son Modèle (`ImagePost`) ce ficher fraichement rangé localement :
```php 
return Storage::url($this->path); 
// Ou suppression par Disque Dur Local et non plus DB 
return Storage::delete($this->path); 
```
