---
description: "Remplir l'environnement de développement avec des données factices et encapsuler les queries."
icon: lucide/flask-conical
tags: ["LARAVEL", "FACTORY", "SEEDER", "SCOPES"]
---

# Hydratation & Scopes

<div
  class="omny-meta"
  data-level="🔵 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Comprendre l'hydratation (Seeding et Factory)

En développement, coder un Frontend sans contenu est impossible. Il est vital de pouvoir repeupler votre base d'essai local d'un coup de commutateur s'ils vous prenaient d'effacer volontairement la structure.

**Seeders** = Insérer des données fixes (ex: les catégories du site).
**Factories** = Générer des données aléatoires (ex: 100 textes latins pour articles factices).

### 1.1 Créer un Seeder statique

```bash
php artisan make:seeder CategorySeeder
```

```php title="database/seeders/CategorySeeder.php"
// Peuple la base avec des catégories prédéfinies non modifiables une pour toute.
public function run(): void
{
    $categories = [
        ['name' => 'Laravel'],
        ['name' => 'PHP'],
        ['name' => 'JavaScript'],
    ];

    foreach ($categories as $category) {
        Category::create($category);
    }
}
```

Il faut par la suite renseigner que votre nouveau "Seeder" doit être appelé par le gros engrenage global.

```php title="database/seeders/DatabaseSeeder.php"
public function run(): void
{
    // C'est ce fichier qui est appellé par defaut lors du Seeding Terminal !
    $this->call(CategorySeeder::class);
}
```

```bash
# Pour Exécuter une insertion (Ajoute +3 catégories, puis encore 3 si vous répéter la commande !)
php artisan db:seed

# Détruit littérallement toutes les tables avant de les restructurer et de faire passer DatabaseSeeder.
php artisan migrate:fresh --seed
```

### 1.2 La Factory (Usines à données)

Pour injecter 300 utilisateurs crédibles, la méthode statique n'est pas viable. On utilise "Fake()".

```bash
php artisan make:factory PostFactory
```

```php title="database/factories/PostFactory.php"
// Chaque appel à Post::factory()->create() génère un post avec des valeurs aléatoires.
public function definition(): array
{
    $title = fake()->sentence(); // Phrase style "Lorem..."
    
    return [
        'user_id' => User::inRandomOrder()->first()->id, // Rapatrie un ID membre au hasard...
        'title' => $title,
        'slug' => Str::slug($title),
        'body' => fake()->paragraphs(3, true),
        // Publié aléatoirement (70% de chance)
        'published_at' => fake()->boolean(70) ? fake()->dateTimeBetween('-1 month', 'now') : null,
    ];
}
```

Il suffira d'ajouter l'instruction à l'engrenage Seeder global !

```php title="database/seeders/DatabaseSeeder.php"
public function run(): void
{
    // Créer 10 utilisateurs d'abord...
    User::factory()->count(10)->create();
    
    // Puis lance les 50 posts aléatoires ! (Si c'était l'inverse, une erreur d'author ID sauterait aux yeux ! Il faut les acteurs avant l'action !)
    Post::factory()->count(50)->create();
}
```

<br>

---

## 2. Décupler votre Vitesse : Les "Query Scopes"

### 2.1 Le drame de la répétition

Il est fort probable que vous réecriviez une chaine incalculable de fois la structure `Post::whereNotNull('published_at')->get()`. Le faire dans le header, puis sur le profil utilisateur, etc... S'il faut soudainement modifier la logique de l'état Publié, c'est impossible.

### 2.2 La solution : Accès via Logic Scope

On inscrit le comportement régulier au seing de l'objet, dans sa matrice Model.

```php title="app/Models/Post.php"
/**
 * Scope : posts publiés uniquement.
 * Convention d'écriture : scope + Mot Clef ($query)
 */
public function scopePublished(Builder $query): Builder
{
    return $query->whereNotNull('published_at');
}

/**
 * Scope Argumentiel
 */
public function scopeByUser(Builder $query, int $userId): Builder
{
    return $query->where('user_id', $userId);
}
```

Le gain de visibilité dans le Back Office Web devient spectaculaire : 

```php 
// Produit SQL WHERE IN NOT NULL / WHERE ID = 1 / ORDER DESC !!!
$posts = Post::published()->byUser(1)->latest()->get();
```

<br>

---

## Conclusion 

Vos requêtes métier étant stocké sur le Model lié garantissent des Controllers extrêmements courts. La base de donnée ne sera ni plus ni moins qu'un terrain de jeu d'assemblage où Laravel masque des milliers de lignes SQL derrière un design pattern abstrait orienté objet, très propre. Il reste un dernier point sensible avant de clore le cycle DB : Le formatage à la volée.
