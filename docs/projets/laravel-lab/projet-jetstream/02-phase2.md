---
description: "Création de la base de données relationnelle pour la plateforme de Pentest, modèles Eloquent avec scopes de Teams et logique métier."
icon: lucide/book-open-check
tags: ["JETSTREAM", "MIGRATIONS", "ELOQUENT", "POLICIES", "SERVICES"]
---

# Phase 2 : Modèles et Logique Pentest

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>

## Objectif de la Phase

> Au cœur de notre plateforme SaaS se trouve un modèle de données complexe qui doit supporter la fonctionnalité Multi-Tenancy (chaque "Team" voit uniquement ses propres missions). Nous allons créer la structure BDD d'une application de Pentest professionnelle : **Missions, Assets, Findings (vulnérabilités), Evidences et Remediations**. Nous mettrons également en place les Services responsables de la logique métier (comme le calculateur de score CVSS) et les Policies d'autorisation.

## Étape 2.1 : Création des Migrations et Modèles

Nous allons générer l'ensemble des modèles, avec leurs migrations (`-m`), factories (`-f`) et contrôleurs (`-c`) associés.

```bash
php artisan make:model Mission -mfc
php artisan make:model Asset -mfc
php artisan make:model Finding -mfc
php artisan make:model Evidence -mfc
php artisan make:model Remediation -mfc
```

### Structure des Migrations

Ouvrez les fichiers de migration créés dans `database/migrations/` et définissez les schémas. Notez l'importance absolue du `team_id` pour isoler les données.

#### 1. Missions

```php
public function up(): void
{
    Schema::create('missions', function (Blueprint $table) {
        $table->id();
        $table->foreignId('team_id')->constrained()->cascadeOnDelete();
        $table->string('name');
        $table->string('type'); // web, mobile, infrastructure, social_engineering
        $table->date('start_date');
        $table->date('end_date')->nullable();
        $table->enum('status', ['planning', 'active', 'reporting', 'completed'])->default('planning');
        $table->timestamps();
    });
}
```

#### 2. Assets (Cibles du Pentest)

```php
public function up(): void
{
    Schema::create('assets', function (Blueprint $table) {
        $table->id();
        $table->foreignId('mission_id')->constrained()->cascadeOnDelete();
        $table->string('name'); // ex: api.example.com
        $table->string('type'); // domain, ip, application, repository
        $table->boolean('in_scope')->default(true);
        $table->timestamps();
    });
}
```

#### 3. Findings (Vulnérabilités)

```php
public function up(): void
{
    Schema::create('findings', function (Blueprint $table) {
        $table->id();
        $table->foreignId('mission_id')->constrained()->cascadeOnDelete();
        $table->foreignId('asset_id')->nullable()->constrained()->nullOnDelete();
        $table->string('title');
        $table->decimal('cvss_score', 3, 1)->nullable(); // ex: 9.8
        $table->enum('severity', ['critical', 'high', 'medium', 'low', 'info']);
        $table->string('cwe_id')->nullable(); // ex: CWE-89
        $table->string('owasp_category')->nullable(); // ex: A03:2021-Injection
        $table->text('description');
        $table->text('impact');
        $table->text('poc'); // Proof of Concept
        $table->enum('status', ['open', 'fixed', 'accepted_risk'])->default('open');
        $table->timestamps();
    });
}
```

> N'oubliez pas d'exécuter `php artisan migrate` pour appliquer ces changements à votre base de données.

## Étape 2.2 : Modèles Eloquent et Relations

Maintenant que la base de données est structurée, définissons les relations dans les modèles Eloquent.

### Le Modèle Team (Fourni par Jetstream)

Modifiez le modèle `app/Models/Team.php` pour y lier les missions :

```php title="app/Models/Team.php"
class Team extends JetstreamTeam
{
    // ...

    public function missions()
    {
        return $this->hasMany(Mission::class);
    }
}
```

### Le Modèle Mission

```php title="app/Models/Mission.php"
class Mission extends Model
{
    protected $fillable = [
        'team_id', 'name', 'type', 'start_date', 'end_date', 'status'
    ];

    protected $casts = [
        'start_date' => 'date',
        'end_date' => 'date',
    ];

    public function team()
    {
        return $this->belongsTo(Team::class);
    }

    public function assets()
    {
        return $this->hasMany(Asset::class);
    }

    public function findings()
    {
        return $this->hasMany(Finding::class);
    }
}
```

### Le Global Scope "TeamTenant"

C'est ici que réside la vraie puissance de l'isolation SaaS. Nous allons créer un scope global qui force toutes les requêtes sur `Mission`, `Asset`, et `Finding` à être restreintes à la Team actuellement sélectionnée par l'utilisateur.

```bash
php artisan make:scope TeamTenantScope
```

```php title="app/Models/Scopes/TeamTenantScope.php"
namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;
use Illuminate\Support\Facades\Auth;

class TeamTenantScope implements Scope
{
    public function apply(Builder $builder, Model $model): void
    {
        if (Auth::hasUser() && Auth::user()->currentTeam) {
            $builder->where($model->getTable() . '.team_id', Auth::user()->current_team_id);
        }
    }
}
```

!!! danger "Application du Scope"
    Pour les modèles n'ayant pas directement de `team_id` (comme `Finding` qui appartient à une `Mission`), vous devrez ajuster ce scope ou utiliser des requêtes `whereHas`. Le plus simple dans un contexte SaaS est de dénormaliser légèrement en ajoutant le `team_id` sur toutes les tables principales.

## Étape 2.3 : Les Services Métier (Logique)

Nous isolons la logique métier complexe hors des contrôleurs pour la rendre testable et réutilisable.

```bash
mkdir app/Services
touch app/Services/CVSSCalculator.php
```

```php title="app/Services/CVSSCalculator.php"
namespace App\Services;

class CVSSCalculator
{
    /**
     * Détermine la sévérité textuelle à partir du score numérique CVSS v3.1
     */
    public static function getSeverityFromScore(float $score): string
    {
        if ($score >= 9.0) return 'critical';
        if ($score >= 7.0) return 'high';
        if ($score >= 4.0) return 'medium';
        if ($score >= 0.1) return 'low';
        return 'info';
    }
    
    /**
     * Calcul basique d'impact (simplifié pour l'exemple)
     */
    public static function calculateBaseScore(array $metrics): float
    {
        // Implémentation réelle de la formule CVSS 3.1
        // (Confidentiality, Integrity, Availability, etc.)
        return 9.8; // Stub
    }
}
```

## Étape 2.4 : Policies d'Autorisation

Bien que le Global Scope isole les données lues (requêtes SELECT), nous devons protéger les actions de modification (UPDATE, DELETE).

```bash
php artisan make:policy MissionPolicy --model=Mission
```

```php title="app/Policies/MissionPolicy.php"
namespace App\Policies;

use App\Models\Mission;
use App\Models\User;

class MissionPolicy
{
    /**
     * Vérifie si l'utilisateur appartient à la team de la mission
     * ET possède les droits "editor" ou "admin".
     */
    public function update(User $user, Mission $mission): bool
    {
        return $user->belongsToTeam($mission->team) && 
               $user->hasTeamPermission($mission->team, 'mission:update');
    }

    public function delete(User $user, Mission $mission): bool
    {
        return $user->belongsToTeam($mission->team) && 
               $user->hasTeamRole($mission->team, 'admin'); // Seul l'admin peut supprimer
    }
}
```

> **Note Jetstream** : Jetstream fournit nativement la gestion fine des permissions par rôles au sein d'une équipe, définis dans `app/Providers/JetstreamServiceProvider.php`.

## Étape 2.5 : Seeders (Données de Test)

Pour développer le Frontend Angular, il nous faut un jeu de données réaliste.

Ouvrez `database/seeders/DatabaseSeeder.php` :

```php title="database/seeders/DatabaseSeeder.php"
public function run(): void
{
    $user = \App\Models\User::factory()->withPersonalTeam()->create([
        'name' => 'Lead Pentester',
        'email' => 'admin@pentest.com',
    ]);

    $mission = \App\Models\Mission::create([
        'team_id' => $user->current_team_id,
        'name' => 'Audit Web Corp 2026',
        'type' => 'web',
        'start_date' => now(),
        'status' => 'active'
    ]);

    \App\Models\Finding::create([
        'mission_id' => $mission->id,
        'title' => 'SQL Injection in Login Panel',
        'cvss_score' => 9.8,
        'severity' => \App\Services\CVSSCalculator::getSeverityFromScore(9.8),
        'cwe_id' => 'CWE-89',
        'owasp_category' => 'A03:2021-Injection',
        'description' => 'The username parameter is vulnerable to boolean-based blind SQLi...',
        'impact' => 'Total database compromise...',
        'poc' => "Payload: admin' OR '1'='1",
    ]);
}
```

```bash
php artisan migrate:fresh --seed
```

## Conclusion de la Phase 2

Les fondations métier sont prêtes :
- ✅ Schéma de données complet généré et migré.
- ✅ L'isolation multi-tenancy (SaaS) est assurée au niveau base de données et applicatif via un Global Scope.
- ✅ Les Policies verrouillent les actions sensibles.
- ✅ Un jeu de données simulé est prêt à être requêté.

Dans la **Phase 3**, nous allons exposer ces données de manière sécurisée via une API REST JSON standardisée.
