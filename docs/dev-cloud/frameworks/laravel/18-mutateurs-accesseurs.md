---
description: "Transformer l'injection et la sortie de vos données et sécuriser les entrées par Transactions de grappes."
icon: lucide/shield-alert
tags: ["LARAVEL", "MUTATEURS", "ACCESSEURS", "TRANSACTIONS"]
---

# Mutateurs & Transactions SQL

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Mutateurs et Accesseurs : formater le flux

Aussi étonnant que cela puisse paraitre, il faut modifier la donnée entre ce qui arrive en vue HTML, et ce qui est stocké sur la Base SQL. Il est par exemple dommage de devoir traiter les dates avec l'objet formaté PHP `Carbon::` systématiquement sur la page d'affichage, ou encore formater un URL au moment de sa rentrée en Base. Utilisons l'abstraction pour que le Framework le fasse à la trappe. 

### 1.1 Accesseurs : formater à la lecture

Un **accesseur** transforme une valeur **quand vous lisez** un attribut.
Le Mutateur est écrit dans le "Model" !

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function title(): Attribute
{
    // Tout les titres seront balancés sans aucun code en majucule dans les vues web : echo $post->title;
    return Attribute::make(
        get: fn (string $value) => strtoupper($value),
    );
}

protected function publishedAt(): Attribute
{
    // Format français DD/MM/YYYY d'une date retournée nativement par MySQL !
    return Attribute::make(
        get: fn ($value) => $value ? \Carbon\Carbon::parse($value)->format('d/m/Y') : null,
    );
}
```

### 1.2 Mutateurs : formater à l'écriture

Un **mutateur** transforme une valeur **quand vous l'assignez**.

```php
protected function title(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => ucfirst($value),
        set: function (string $value) {
            return [
                'title' => $value,
                // On créer la donnée supplémentaire avec la façade Str à partir d'une seule entrée.
                'slug' => \Str::slug($value),
            ];
        },
    );
}
```

<br>

---

## 2. Transactions : garantir l'intégrité des opérations (Banques, Achats)

Une problématique inévitable lorsqu'une méthode interroge de l'Eloquent : Que se passe t-il si l'élément 2 fait crasher PHP et ne se rends pas jusqu'au troisiéme Element pour l'achever ?

```php
// Créer la facture
$bill = Bill::create([...]);

// Créer le profil
$user = Profil::create([...]);

// ERREUR RESEAU - SCRIPT STOP !
// Attribuer l'id d'accès au profil. L'utilisateur a été facturé mais n'a pas accès au site !
$user->auth()->attach($bill); 
```

**Si une erreur survient au milieu du trait, on risque l'incohérence la plus totale.**
Une **transaction** garantit que **toutes les opérations réussissent ou échouent ensemble en grappes "Atomic"**.

### 2.1 Les blocs DB::transaction

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    // Si la moindre commande échoue ici, la base rembobine TOUTES les étapes et fait un effacement Rollback avant de générer une Error 500 pour vous protéger.
    $bill = Bill::create([...]);
    $user = Profil::create([...]);
    $user->auth()->attach($bill); 
});
```

Si le bloc s'exécute sans erreur, les changements sont validés (Le "Commit"). 

### 2.2 Controle total via Block Exceptionnels (Try / Catch)

```php
DB::beginTransaction();

try {
    // Opérations critiques
    $post = Post::create([...]);
    $post->tags()->attach([1, 2, 3]);
    
    // Si tout s'est bien passé
    DB::commit();

} catch (\Exception $e) {
    // Annuler tout si la moindre erreur PHP se souléve
    DB::rollback();
    
    // Loguer sa défaite pour en repérer l'auteur
    \Log::error('Erreur création post : ' . $e->getMessage());
    throw $e; 
}
```

<br>

---

## Conclusion 

Les filtres et le sécurisateurs transactionnels complètent le bouclier défensif de la base de donnée contre toutes actions du programmeur ou attaques non voulues. Il s'agit des méthodes de gestions Backend de flux avancés. Mais avez vous tout retenu ? C'est l'heure du bilan terminal de Module.
