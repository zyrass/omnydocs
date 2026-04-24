---
description: "Tests automatisés backend (isolation Teams), optimisation et déploiement de l'API Laravel et du frontend Angular en production."
icon: lucide/book-open-check
tags: ["TESTS", "DEPLOYMENT", "PRODUCTION", "OPTIMIZATION", "VPS"]
---

# Phase 8 : Tests et Déploiement

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>

## Objectif de la Phase

> Une plateforme SaaS manipulant des données de cybersécurité ne peut pas être mise en production sans une couverture de tests irréprochable (en particulier sur l'isolation des données entre les clients). Dans cette ultime phase, nous écrirons des tests automatisés (PHPUnit/Pest) pour garantir l'étanchéité de notre architecture Multi-Tenancy. Enfin, nous optimiserons les performances et déploierons le Backend et le Frontend sur des environnements de production distincts.

## Étape 8.1 : Tests d'Isolation (Feature Tests)

La faille la plus critique dans une application SaaS (B2B) serait qu'un client (Team A) puisse accéder aux données d'un autre client (Team B) via l'API (IDOR - Insecure Direct Object Reference).

Nous allons écrire un Feature Test pour nous assurer que notre Global Scope (`TeamTenantScope`) et nos Policies fonctionnent parfaitement.

```bash
php artisan make:test MissionIsolationTest
```

```php title="tests/Feature/MissionIsolationTest.php"
namespace Tests\Feature;

use App\Models\User;
use App\Models\Mission;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class MissionIsolationTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_cannot_access_other_teams_missions()
    {
        // 1. Création de deux utilisateurs avec leurs propres équipes (Teams)
        $userA = User::factory()->withPersonalTeam()->create();
        $userB = User::factory()->withPersonalTeam()->create();

        // 2. Création d'une mission appartenant à la Team de l'Utilisateur A
        $missionA = Mission::factory()->create([
            'team_id' => $userA->current_team_id
        ]);

        // 3. Utilisateur B tente d'accéder à la liste des missions
        $responseList = $this->actingAs($userB)->getJson('/api/missions');
        
        // 4. Assertion : La mission A NE DOIT PAS être dans la réponse JSON
        $responseList->assertStatus(200);
        $responseList->assertJsonMissing([
            'id' => $missionA->id
        ]);

        // 5. Utilisateur B tente d'accéder directement à la mission A (IDOR)
        $responseDetail = $this->actingAs($userB)->getJson('/api/missions/' . $missionA->id);
        
        // 6. Assertion : Accès refusé (403) ou Non Trouvé (404 via Scope)
        $responseDetail->assertStatus(404);
    }
}
```

## Étape 8.2 : Tests Unitaires (Logique Métier)

Testons la classe `CVSSCalculator` que nous avons créée en Phase 2. Les tests unitaires doivent être extrêmement rapides et isolés (sans base de données).

```bash
php artisan make:test CVSSCalculatorTest --unit
```

```php title="tests/Unit/CVSSCalculatorTest.php"
namespace Tests\Unit;

use PHPUnit\Framework\TestCase; // Attention: TestCase natif, pas celui de Laravel
use App\Services\CVSSCalculator;

class CVSSCalculatorTest extends TestCase
{
    public function test_severity_mapping()
    {
        $this->assertEquals('critical', CVSSCalculator::getSeverityFromScore(9.8));
        $this->assertEquals('critical', CVSSCalculator::getSeverityFromScore(9.0));
        
        $this->assertEquals('high', CVSSCalculator::getSeverityFromScore(8.9));
        $this->assertEquals('high', CVSSCalculator::getSeverityFromScore(7.0));
        
        $this->assertEquals('medium', CVSSCalculator::getSeverityFromScore(6.9));
        $this->assertEquals('medium', CVSSCalculator::getSeverityFromScore(4.0));
        
        $this->assertEquals('low', CVSSCalculator::getSeverityFromScore(3.9));
        $this->assertEquals('low', CVSSCalculator::getSeverityFromScore(0.1));
        
        $this->assertEquals('info', CVSSCalculator::getSeverityFromScore(0.0));
    }
}
```

```bash
# Exécuter toute la suite de tests
php artisan test
```

## Étape 8.3 : Optimisation Backend (Laravel)

Avant le déploiement en production, vous devez compiler et mettre en cache les configurations, routes et vues.

```bash
# Sur le serveur de production (via SSH ou script CI/CD)

# 1. Optimisation de l'autoloader Composer
composer install --optimize-autoloader --no-dev

# 2. Mise en cache globale Laravel
php artisan optimize

# (Équivalent à ces 3 commandes individuelles) :
# php artisan config:cache
# php artisan route:cache
# php artisan view:cache
```

!!! warning "APP_DEBUG=false"
    N'oubliez **JAMAIS** de passer `APP_DEBUG=false` dans le fichier `.env` de production. Laisser le mode debug activé exposera vos identifiants de base de données à n'importe quel visiteur lors d'une erreur 500.

## Étape 8.4 : Build Production Frontend (Angular)

Le frontend doit être compilé en fichiers statiques minimisés (HTML, JS, CSS).

```bash
# Dans le dossier de votre projet Angular
ng build
```

Angular génère un dossier `dist/pentest-platform/browser/`. Ces fichiers sont de l'ordre de quelques kilo-octets (grâce au Tree Shaking et à l'AOT Compilation) et prêts à être servis par n'importe quel serveur web.

## Étape 8.5 : Stratégies de Déploiement

Dans une architecture découplée (API + SPA), vous avez deux options principales de déploiement :

### Option A : Déploiement Mono-Serveur (VPS Linux)

Vous louez un VPS (DigitalOcean, Linode) avec Nginx installé.
- **Nginx** sert directement les fichiers statiques Angular depuis un dossier (`/var/www/pentest-platform/dist/`).
- **Nginx** redirige toutes les requêtes commençant par `/api` ou `/sanctum` vers **PHP-FPM** (votre API Laravel dans `/var/www/saas-pentest/public/`).

*Avantage* : Moins cher, configuration CORS très simple (tout est sur le même domaine).

### Option B : Déploiement Distribué (Vercel + Vapor/VPS)

C'est l'approche Serverless moderne.
- **Frontend** : Vous connectez votre repo Angular à **Vercel** ou **Netlify**. Le build et le déploiement sont automatiques et distribués sur un CDN global (`https://app.votredomaine.com`).
- **Backend API** : Déployé sur **Laravel Vapor** (AWS Serverless) ou Laravel Forge (VPS géré) (`https://api.votredomaine.com`).

*Avantage* : Scalabilité infinie, performances CDN mondiales.
*Inconvénient* : Vous devez configurer rigoureusement les CORS et Sanctum `stateful` domains pour accepter les requêtes de `app.votredomaine.com` vers `api.votredomaine.com`.

## Étape 8.6 : HTTPS (SSL/TLS) Obligatoire

Sanctum s'appuie sur des cookies sécurisés. En production, ces cookies doivent avoir l'attribut `Secure` (qui exige du HTTPS).

Dans votre `.env` Laravel en production :
```bash
SESSION_SECURE_COOKIE=true
```

Configurez toujours des certificats SSL (ex: **Let's Encrypt**) sur votre serveur de production.

## Conclusion de la Phase 8

Félicitations ! Vous avez couvert le cycle de vie complet d'une application SaaS professionnelle.
- ✅ **Sécurité validée** par des Feature Tests vérifiant l'isolation des données (Multi-Tenancy).
- ✅ **Code optimisé** via les commandes de cache Laravel et le build AOT d'Angular.
- ✅ **Architecture de déploiement** décidée (Frontend CDN + Backend API).

Votre plateforme de Pentest SaaS est maintenant **Production-Ready**. Passez à la conclusion du projet Jetstream pour le bilan final de vos compétences.
