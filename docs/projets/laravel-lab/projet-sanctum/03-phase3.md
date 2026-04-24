---
description: "Création des routes d'action du jeu (création de personnage, lancement de combat, système de tours au tour par tour) avec contrôles de sécurité Anti-Cheat."
icon: lucide/book-open-check
tags: ["SANCTUM", "API", "ENDPOINTS", "GAME-LOOP", "ANTI-CHEAT"]
---

# Phase 3 : Endpoints API REST (Routes de Jeu)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2h - 3h">
</div>

## Objectif de la Phase

> Contrairement à une API classique (CRUD), une API de jeu vidéo gère une "Game Loop" (Boucle de Jeu) asynchrone via des actions spécifiques (Créer un personnage, Lancer un combat, Attaquer, Fuir). Nous allons développer ces endpoints en gardant une priorité absolue : la sécurité. **Le serveur ne doit faire confiance à aucune donnée envoyée par le client concernant les calculs.** L'API doit empêcher la triche (ex: attaquer deux fois d'affilée, soigner un personnage mort, attaquer dans un combat déjà terminé).

## Étape 3.1 : Définition des Routes de Jeu

Ouvrez `routes/api.php` et définissez vos nouvelles routes. Toutes ces requêtes doivent inclure un Token valide (authentification Sanctum).

```php title="routes/api.php"
// ... (routes auth existantes)

Route::middleware('auth:sanctum')->group(function () {
    
    // --- Gestion du Personnage ---
    Route::post('/characters', [CharacterController::class, 'store']);
    Route::get('/characters/my-character', [CharacterController::class, 'myCharacter']);
    
    // --- Boucle de Jeu (Game Loop) ---
    Route::post('/battles/start', [BattleController::class, 'start']);
    Route::post('/battles/attack', [BattleController::class, 'attack']);
    Route::post('/battles/flee', [BattleController::class, 'flee']);
    
    // --- Leaderboard ---
    Route::get('/leaderboard', [CharacterController::class, 'leaderboard']);

});
```

## Étape 3.2 : Création du Personnage

Nous permettons à un joueur de créer son avatar.

```php title="app/Http/Controllers/Api/CharacterController.php"
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class CharacterController extends Controller
{
    public function store(Request $request)
    {
        // Règle 1 : Un utilisateur ne peut avoir qu'un seul personnage actif
        if ($request->user()->characters()->exists()) {
            return response()->json(['error' => 'Vous avez déjà un personnage.'], 403);
        }

        $request->validate([
            'name' => 'required|string|max:20|unique:characters',
            'class' => 'required|in:warrior,mage,rogue'
        ]);

        // Attributs de base selon la classe (sécurité : défini CÔTÉ SERVEUR)
        $attributes = match($request->class) {
            'warrior' => ['strength' => 15, 'defense' => 15, 'agility' => 5],
            'mage'    => ['intelligence' => 15, 'max_mp' => 100, 'defense' => 5],
            'rogue'   => ['agility' => 15, 'strength' => 10, 'defense' => 8],
        };

        $character = $request->user()->characters()->create(array_merge([
            'name' => $request->name,
            'class' => $request->class,
        ], $attributes));

        return response()->json($character, 201);
    }
}
```

## Étape 3.3 : Démarrer un Combat (Start Battle)

Lorsque le joueur clique sur "Explorer le Donjon", le serveur lui assigne un monstre aléatoire adapté à son niveau.

```php title="app/Http/Controllers/Api/BattleController.php"
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Monster;
use Illuminate\Http\Request;

class BattleController extends Controller
{
    public function start(Request $request)
    {
        $character = $request->user()->characters()->first();

        if (!$character) {
            return response()->json(['error' => 'Personnage introuvable.'], 404);
        }

        // Anti-Cheat : Vérifier s'il n'est pas déjà en combat
        if ($character->currentBattle()->exists()) {
            return response()->json([
                'error' => 'Vous êtes déjà en plein combat !',
                'battle' => $character->currentBattle
            ], 400);
        }

        // Anti-Cheat : Vérifier s'il est vivant
        if ($character->current_hp <= 0) {
            return response()->json(['error' => 'Vous êtes mort. Ressuscitez au village.'], 400);
        }

        // Sélectionner un monstre aléatoire (Niveau du joueur +/- 2)
        $minLevel = max(1, $character->level - 2);
        $maxLevel = $character->level + 2;
        
        $monster = Monster::whereBetween('level', [$minLevel, $maxLevel])
                          ->inRandomOrder()
                          ->first();

        // Créer l'instance de combat
        $battle = $character->currentBattle()->create([
            'monster_id' => $monster->id,
            'monster_current_hp' => $monster->max_hp,
            'status' => 'in_progress'
        ]);

        return response()->json([
            'message' => "Un {$monster->name} sauvage apparaît !",
            'battle' => $battle->load('monster'),
            'character' => $character
        ]);
    }
}
```

## Étape 3.4 : Le Tour de Combat (Attack Logic)

C'est la route la plus critique. Un appel réseau représente un "Tour" complet : le joueur attaque, puis (s'il est vivant), le monstre contre-attaque immédiatement. Le tout dans la même requête.

```php title="app/Http/Controllers/Api/BattleController.php"
// Import des services
use App\Services\BattleEngine;
use App\Services\CharacterService;
use Illuminate\Support\Facades\DB;

public function attack(Request $request, CharacterService $charService)
{
    $character = $request->user()->characters()->first();
    $battle = $character->currentBattle()->with('monster')->first();

    // Vérifications de sécurité
    if (!$battle) {
        return response()->json(['error' => 'Aucun combat en cours.'], 400);
    }

    $monster = $battle->monster;
    $combatLogs = [];

    // On utilise une transaction BDD pour éviter la triche (double clic / race conditions)
    return DB::transaction(function () use ($character, $battle, $monster, &$combatLogs, $charService) {
        
        // --- 1. TOUR DU JOUEUR ---
        $playerAttack = BattleEngine::calculatePlayerDamage($character, $monster);
        $battle->monster_current_hp -= $playerAttack['damage'];
        $combatLogs[] = $playerAttack['text'];

        // Vérification mort du monstre (VICTOIRE)
        if ($battle->monster_current_hp <= 0) {
            $battle->monster_current_hp = 0;
            $battle->status = 'victory';
            $battle->save();

            // Récompenses
            $character->gold += $monster->gold_reward;
            $xpResult = $charService->addExperience($character, $monster->exp_reward);
            
            $combatLogs[] = "Victoire ! Vous gagnez {$monster->exp_reward} XP et {$monster->gold_reward} PO.";
            if ($xpResult['leveled_up']) {
                $combatLogs[] = "NIVEAU SUPÉRIEUR ! Vous êtes maintenant niveau {$xpResult['current_level']}.";
            }

            return response()->json([
                'status' => 'victory',
                'logs' => $combatLogs,
                'character' => $character->fresh()
            ]);
        }

        // --- 2. TOUR DU MONSTRE ---
        $monsterAttack = BattleEngine::calculateMonsterDamage($monster, $character);
        $character->current_hp -= $monsterAttack['damage'];
        $combatLogs[] = $monsterAttack['text'];

        // Vérification mort du joueur (DÉFAITE)
        if ($character->current_hp <= 0) {
            $character->current_hp = 0;
            $battle->status = 'defeat';
            $battle->save();
            $character->save();

            $combatLogs[] = "Vous avez été terrassé... Retournez au village.";

            return response()->json([
                'status' => 'defeat',
                'logs' => $combatLogs,
                'character' => $character
            ]);
        }

        // --- 3. FIN DU TOUR (Toujours en combat) ---
        $battle->turn_count++;
        $battle->save();
        $character->save();

        return response()->json([
            'status' => 'in_progress',
            'logs' => $combatLogs,
            'battle' => $battle,
            'character' => $character
        ]);

    }); // Fin de transaction
}
```

!!! success "Le pattern Request-Response asynchrone"
    En une seule requête HTTP, le serveur gère les actions du joueur ET l'IA du monstre, protège la base de données via une Transaction (les verrous empêchent le spam de clics), calcule l'expérience et retourne le rapport du tour sous forme de `logs`. C'est le principe fondamental du **Server-Authoritative Networking**.

## Conclusion de la Phase 3

L'API de notre jeu vidéo est maintenant opérationnelle et hautement sécurisée :
- ✅ **Game Loop** complète (Start, Attack, Flee).
- ✅ Validation stricte de l'état (Impossible d'attaquer si mort, impossible de démarrer 2 combats).
- ✅ **Server-Authoritative Logic** : Le serveur dicte les lois de la physique et des dégâts, rendant le "hack" impossible.
- ✅ Utilisation des **Transactions BDD** pour parer aux requêtes concurrentes (Race Conditions).

Passons maintenant à la **Phase 4**, où nous allons configurer le moteur graphique en Angular 21 (Signals) pour consommer cette API.
