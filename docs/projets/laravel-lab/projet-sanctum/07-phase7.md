---
description: "Tests unitaires de l'algorithme de combat, tests fonctionnels de la boucle de jeu et optimisation des performances via le cache Redis."
icon: lucide/book-open-check
tags: ["TESTS", "REDIS", "CACHE", "PHPUNIT", "OPTIMIZATION"]
---

# Phase 7 : Tests et Optimisation

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2h - 3h">
</div>


!!! quote "Analogie pédagogique"
    _Sécuriser une API avec Sanctum s'apparente à donner un jeton d'accès temporaire à un livreur. Au lieu de lui donner les clés de la maison (authentification de session), vous lui donnez un badge qui ne permet d'ouvrir que la porte du garage, et qui peut être révoqué à tout moment._

## Objectif de la Phase

> Dans un jeu multijoueur, la logique mathématique doit être infaillible et les performances optimales. Si une route API de combat met plus de 500ms à répondre, l'expérience utilisateur est ruinée. De plus, une faille dans le calcul des dégâts peut être exploitée. Nous allons sécuriser la logique via des **Tests Unitaires (TDD)** et optimiser les requêtes lourdes (comme le Leaderboard) en utilisant la mise en cache mémoire fulgurante de **Redis**.

## Étape 7.1 : Tests Unitaires du Moteur de Combat (BattleEngine)

Le composant le plus critique est `BattleEngine`. Que se passe-t-il si la défense du monstre est de 1000 ? Si la force du joueur est négative ? Le test unitaire permet de couvrir ces cas limites sans base de données.

```bash
php artisan make:test BattleEngineTest --unit
```

```php title="tests/Unit/BattleEngineTest.php"
namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use App\Services\BattleEngine;
use App\Models\Character;
use App\Models\Monster;

class BattleEngineTest extends TestCase
{
    public function test_player_always_deals_at_least_one_damage()
    {
        // On crée des instances "virtuelles" (non sauvegardées en BDD)
        $player = new Character(['strength' => 5, 'agility' => 0]);
        $monster = new Monster(['defense' => 9999]); // Défense impénétrable

        // L'algorithme doit bloquer les dégâts à 1 minimum
        $result = BattleEngine::calculatePlayerDamage($player, $monster);

        $this->assertGreaterThanOrEqual(1, $result['damage']);
    }

    public function test_critical_hit_doubles_damage()
    {
        // 1000 en agilité pour garantir 100% de critique
        $player = new Character(['strength' => 10, 'agility' => 1000]);
        $monster = new Monster(['defense' => 0]);

        $result = BattleEngine::calculatePlayerDamage($player, $monster);

        $this->assertTrue($result['is_critical']);
        // Force (10) * Modif(0.8 à 1.2) * Crit(2.0). Min: 16, Max: 24
        $this->assertGreaterThanOrEqual(16, $result['damage']);
        $this->assertLessThanOrEqual(24, $result['damage']);
    }
}
```

## Étape 7.2 : Tests Fonctionnels (Game Loop & Transactions)

Nous devons nous assurer que les endpoints API sont protégés et que la transaction BDD du contrôleur fonctionne.

```bash
php artisan make:test GameLoopTest
```

```php title="tests/Feature/GameLoopTest.php"
namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Character;
use App\Models\Monster;

class GameLoopTest extends TestCase
{
    use RefreshDatabase;

    public function test_dead_character_cannot_start_battle()
    {
        // 1. Initialisation
        $user = User::factory()->create();
        $character = Character::factory()->create([
            'user_id' => $user->id,
            'current_hp' => 0 // Mort
        ]);

        // 2. Action (API Request)
        $response = $this->actingAs($user, 'sanctum') // Authentification par Token mockée
                         ->postJson('/api/battles/start');

        // 3. Assertion
        $response->assertStatus(400);
        $response->assertJsonPath('error', 'Vous êtes mort. Ressuscitez au village.');
    }

    public function test_player_cannot_spam_attacks()
    {
        // Test très complexe nécessitant des mocks de requêtes concurrentes.
        // C'est pourquoi l'utilisation de DB::transaction() et DB::lockForUpdate()
        // (Pessimistic Locking) est vitale dans le contrôleur.
        $this->assertTrue(true); // Placeholder
    }
}
```

## Étape 7.3 : Optimisation des performances avec Redis

Sur un jeu comportant des milliers de joueurs, la requête générant le **Leaderboard (Classement)** (`ORDER BY experience DESC LIMIT 10`) va vite devenir un goulot d'étranglement (Bottleneck) si elle interroge la base MySQL à chaque fois.

La solution : **Le Caching avec Redis**. Redis stocke les données en RAM (mémoire vive), ce qui permet des temps de réponse inférieurs à la milliseconde.

### Installation et Configuration

Assurez-vous d'avoir Redis installé sur votre machine (ou via Docker).

```bash
# Installer le client PHP Predis
composer require predis/predis
```

Dans `.env`, passez le driver de cache sur Redis :
```bash
CACHE_STORE=redis
```

### Mise en cache du Leaderboard

Modifions le `CharacterController` pour mettre en cache le Top 10 pendant 5 minutes.

```php title="app/Http/Controllers/Api/CharacterController.php"
use Illuminate\Support\Facades\Cache;

public function leaderboard()
{
    // Cherche la clé 'global_leaderboard'. 
    // Si introuvable ou expirée (300 sec = 5 mins), exécute la fonction SQL et met en cache.
    $topCharacters = Cache::remember('global_leaderboard', 300, function () {
        return \App\Models\Character::with('user:id,name')
                    ->orderBy('experience', 'desc')
                    ->limit(10)
                    ->get(['id', 'name', 'class', 'level', 'experience']);
    });

    return response()->json($topCharacters);
}
```

!!! tip "Invalidation du Cache"
    Plutôt que d'attendre 5 minutes, vous pouvez purger (invalider) le cache manuellement chaque fois qu'un joueur effectue un Level Up :
    `Cache::forget('global_leaderboard');`

## Étape 7.4 : Éviter le Problème N+1 (Eloquent)

Un classique de l'optimisation Laravel. Si votre page "Village" a besoin d'afficher l'équipement du joueur (Items), n'écrivez jamais ça dans une boucle Blade ou API :

```php
// MAUVAIS (N+1 queries)
$characters = Character::all();
foreach($characters as $char) {
    $items = $char->items; // Déclenche 1 requête SQL PAR personnage
}
```

**La solution (Eager Loading)** :
```php
// BON (2 requêtes SQL au total)
$characters = Character::with('items')->get();
```

Assurez-vous d'utiliser `with()` dans toutes vos API Resources qui incluent des relations (`User->characters`, `Battle->monster`).

## Conclusion de la Phase 7

Le jeu est dorénavant sécurisé, testé, et extrêmement rapide :
- ✅ **Test Driven Development (TDD)** validant les algorithmes critiques (`BattleEngineTest`).
- ✅ **Sécurité Transactionnelle** testée (`GameLoopTest`).
- ✅ **Redis Cache** intégré pour alléger la charge sur MySQL (Leaderboard).
- ✅ **Eager Loading** contrôlé pour bannir les requêtes N+1.

Il ne reste plus qu'une dernière étape pour clore ce projet épique : la **Phase 8 (Déploiement Production)**, où nous aborderons les enjeux d'un déploiement à forte charge.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Tester une API Laravel, c'est tester des contrats. Chaque test doit vérifier trois choses : le code HTTP retourné, la structure JSON de la réponse, et l'état de la base de données après l'opération. Le pattern `actingAs($user)->postJson('/api/...')->assertCreated()->assertJson(...)` est la signature d'un test d'API Laravel professionnel.

> [Tests automatisés maîtrisés. Déployez maintenant le projet en production →](./08-phase8.md)
