---
description: "Personnalisation du modèle User, création de migrations complémentaires (profil, avatar) et relations Eloquent."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 2 — Base de Données & Modèles

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Laravel 11"
  data-time="~1 heure">
</div>

## Objectifs de la Phase 2

!!! info "Ce que vous allez faire"
    - Ajouter des colonnes au modèle User (`bio`, `avatar`, `last_login_at`)
    - Créer une migration propre avec `php artisan make:migration`
    - Mettre à jour le modèle User (fillable, casts)
    - Créer une relation User → Posts si applicable

## 1. Nouvelle Migration — Colonnes de Profil

```bash
php artisan make:migration add_profile_columns_to_users_table --table=users
```

```php title="database/migrations/xxxx_add_profile_columns_to_users_table.php"
public function up(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->text('bio')->nullable()->after('email');
        $table->string('avatar')->nullable()->after('bio');
        $table->timestamp('last_login_at')->nullable()->after('remember_token');
    });
}

public function down(): void
{
    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['bio', 'avatar', 'last_login_at']);
    });
}
```

```bash
php artisan migrate
```

## 2. Mise à Jour du Modèle User

```php title="app/Models/User.php"
protected $fillable = [
    'name',
    'email',
    'password',
    'bio',
    'avatar',
];

protected $casts = [
    'email_verified_at' => 'datetime',
    'last_login_at'     => 'datetime',
    'password'          => 'hashed',
];
```

## 3. Factory Mise à Jour

```php title="database/factories/UserFactory.php"
public function definition(): array
{
    return [
        'name'     => fake()->name(),
        'email'    => fake()->unique()->safeEmail(),
        'password' => static::$password ??= Hash::make('password'),
        'bio'      => fake()->sentence(10),
    ];
}
```

```bash
# Créer 10 utilisateurs de test
php artisan tinker
User::factory(10)->create();
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les migrations sont le contrat historique de votre base de données. Chaque modification doit passer par une migration dédiée — jamais directement dans la base. Cette discipline vous permet de reproduire l'état exact de votre BDD sur n'importe quel environnement (dev, staging, prod) avec un simple `php artisan migrate`.

> [Phase 3 — Personnalisation des vues Blade →](./phase3.md)
