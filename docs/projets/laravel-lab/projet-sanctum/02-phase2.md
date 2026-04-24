---
description: "Modélisation de la base de données du RPG (Personnages, Monstres, Combats) et implémentation de la logique métier de jeu vidéo (Dégâts, Expérience, Level Up)."
icon: lucide/book-open-check
tags: ["RPG", "LOGIC", "MODELS", "ELOQUENT", "ALGORITHM"]
---

# Phase 2 : Modèles et Logique RPG

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3h - 4h">
</div>

## Objectif de la Phase

> Le développement d'un jeu vidéo, même textuel ou en grille 2D, implique une logique algorithmique complexe. Cette phase est consacrée à la modélisation de notre **Dungeon RPG**. Nous allons concevoir les tables pour les Personnages (Joueurs), les Monstres (Bestiaire), les Objets (Inventaire) et les Combats (Historique des tours). L'accent sera mis sur la **logique métier (Calcul de dégâts, gestion des Points de Vie (HP) et de Magie (MP), algorithme de Level Up)**, qui doit être strictement gérée côté serveur pour éviter la triche (anti-cheat).

## Étape 2.1 : Structure de la Base de Données

Générons les modèles et leurs fichiers associés (`-mfc` pour migration, factory, controller).

```bash
php artisan make:model Character -mfc
php artisan make:model Monster -mfc
php artisan make:model Item -mfc
php artisan make:model Battle -mfc
php artisan make:model BattleLog -mfc
```

### 1. Personnages (Characters)

Le personnage est lié à un utilisateur (User). Il possède des statistiques RPG classiques.

```php title="database/migrations/xxxx_create_characters_table.php"
public function up(): void
{
    Schema::create('characters', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->cascadeOnDelete();
        $table->string('name')->unique();
        $table->enum('class', ['warrior', 'mage', 'rogue']);
        
        // Statistiques de base
        $table->integer('level')->default(1);
        $table->integer('experience')->default(0);
        $table->integer('gold')->default(0);
        
        // HP / MP
        $table->integer('max_hp')->default(100);
        $table->integer('current_hp')->default(100);
        $table->integer('max_mp')->default(50);
        $table->integer('current_mp')->default(50);
        
        // Attributs
        $table->integer('strength')->default(10); // Dégâts physiques
        $table->integer('intelligence')->default(10); // Dégâts magiques
        $table->integer('agility')->default(10); // Esquive / Critique
        $table->integer('defense')->default(10); // Réduction de dégâts
        
        $table->timestamps();
    });
}
```

### 2. Bestiaire (Monsters)

Les monstres sont les ennemis contrôlés par le serveur.

```php title="database/migrations/xxxx_create_monsters_table.php"
public function up(): void
{
    Schema::create('monsters', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('type'); // goblin, orc, dragon...
        $table->integer('level');
        $table->integer('max_hp');
        $table->integer('attack');
        $table->integer('defense');
        // Récompenses en cas de victoire
        $table->integer('exp_reward');
        $table->integer('gold_reward');
        $table->string('image_url')->nullable();
        $table->timestamps();
    });
}
```

### 3. Instance de Combat (Battles)

Un combat est une entité temporaire qui lie un Joueur et un Monstre jusqu'à la mort de l'un des deux ou la fuite.

```php title="database/migrations/xxxx_create_battles_table.php"
public function up(): void
{
    Schema::create('battles', function (Blueprint $table) {
        $table->id();
        $table->foreignId('character_id')->constrained()->cascadeOnDelete();
        $table->foreignId('monster_id')->constrained();
        
        // État de l'instance du monstre (le monstre de la BDD est un "template",
        // ici on stocke ses HP actuels pour CE combat)
        $table->integer('monster_current_hp');
        
        $table->enum('status', ['in_progress', 'victory', 'defeat', 'fled'])->default('in_progress');
        $table->integer('turn_count')->default(0);
        $table->timestamps();
    });
}
```

*(N'oubliez pas d'exécuter `php artisan migrate` !)*

## Étape 2.2 : Relations Eloquent et Sécurité

Un point crucial : un Utilisateur peut avoir plusieurs Personnages, mais lors d'une requête API (ex: "Attaquer"), le serveur doit **vérifier que le Personnage appartient bien à l'Utilisateur authentifié** (anti-triche / anti-IDOR).

```php title="app/Models/User.php"
public function characters()
{
    return $this->hasMany(Character::class);
}
```

```php title="app/Models/Character.php"
class Character extends Model
{
    protected $guarded = []; // Nous contrôlerons strictement les updates via les Services

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function currentBattle()
    {
        // Récupère la bataille en cours (in_progress)
        return $this->hasOne(Battle::class)->where('status', 'in_progress');
    }
}
```

## Étape 2.3 : La Logique RPG (Algorithmes)

Dans un jeu multijoueur (même asynchrone), **le client (Frontend Angular) ne doit jamais envoyer de valeurs telles que "J'ai infligé 9999 dégâts"**. Le client envoie une **Action** ("Attaque de base"), et le **Serveur calcule le résultat**.

Nous allons isoler cette logique mathématique dans un Service.

```bash
mkdir app/Services
touch app/Services/BattleEngine.php
```

```php title="app/Services/BattleEngine.php"
namespace App\Services;

use App\Models\Character;
use App\Models\Monster;

class BattleEngine
{
    /**
     * Calcule les dégâts d'une attaque physique du joueur vers le monstre
     */
    public static function calculatePlayerDamage(Character $player, Monster $monster): array
    {
        // 1. Dégâts de base = Force du joueur * modificateur aléatoire (0.8 à 1.2)
        $baseDamage = $player->strength * (rand(80, 120) / 100);
        
        // 2. Chance de coup critique (Basée sur l'agilité)
        $isCritical = rand(1, 100) <= ($player->agility / 2); // Ex: 10 Agi = 5% Crit
        $multiplier = $isCritical ? 2.0 : 1.0;
        
        // 3. Réduction d'armure du monstre (Mitigation)
        // Formule simple : Dégâts * (100 / (100 + Défense))
        $mitigation = 100 / (100 + $monster->defense);
        
        $finalDamage = (int) round(($baseDamage * $multiplier) * $mitigation);
        
        // Les dégâts ne peuvent pas être négatifs
        $finalDamage = max(1, $finalDamage);
        
        return [
            'damage' => $finalDamage,
            'is_critical' => $isCritical,
            'text' => $isCritical ? "Coup Critique ! Vous infligez {$finalDamage} dégâts." : "Vous infligez {$finalDamage} dégâts."
        ];
    }
    
    /**
     * Calcule les dégâts du monstre vers le joueur
     */
    public static function calculateMonsterDamage(Monster $monster, Character $player): array
    {
        $baseDamage = $monster->attack * (rand(90, 110) / 100);
        
        // Esquive basée sur l'agilité du joueur
        $dodgeChance = min(30, $player->agility); // Cap à 30% d'esquive
        $isDodged = rand(1, 100) <= $dodgeChance;
        
        if ($isDodged) {
            return [
                'damage' => 0,
                'is_dodged' => true,
                'text' => "Vous avez esquivé l'attaque du monstre !"
            ];
        }
        
        $mitigation = 100 / (100 + $player->defense);
        $finalDamage = (int) round($baseDamage * $mitigation);
        
        return [
            'damage' => max(1, $finalDamage),
            'is_dodged' => false,
            'text' => "Le monstre vous inflige {$finalDamage} dégâts."
        ];
    }
}
```

## Étape 2.4 : La Logique d'Évolution (Level Up)

Le gain de niveau est une mécanique fondamentale. Créons un service `CharacterService` pour gérer la santé et l'expérience.

```php title="app/Services/CharacterService.php"
namespace App\Services;

use App\Models\Character;

class CharacterService
{
    /**
     * Ajoute de l'expérience et gère la montée en niveau (Level Up)
     */
    public function addExperience(Character $character, int $amount): array
    {
        $character->experience += $amount;
        $leveledUp = false;
        
        // Formule d'XP requise : (Niveau * 100) * 1.5
        $xpRequired = (int) (($character->level * 100) * 1.5);
        
        while ($character->experience >= $xpRequired) {
            $character->experience -= $xpRequired;
            $character->level++;
            
            // Augmentation des statistiques
            $character->max_hp += 20;
            $character->current_hp = $character->max_hp; // Soin complet au Level Up !
            
            // Augmentation basée sur la classe
            if ($character->class === 'warrior') {
                $character->strength += 3;
                $character->defense += 2;
            } elseif ($character->class === 'mage') {
                $character->intelligence += 4;
                $character->max_mp += 10;
            } else {
                $character->agility += 3;
                $character->strength += 1;
            }
            
            $leveledUp = true;
            // Recalcul de l'XP requise pour le niveau suivant
            $xpRequired = (int) (($character->level * 100) * 1.5);
        }
        
        $character->save();
        
        return [
            'leveled_up' => $leveledUp,
            'current_level' => $character->level
        ];
    }
}
```

## Étape 2.5 : Création du Bestiaire (Seeders)

Pour que notre jeu soit fonctionnel, générons un bestiaire de monstres de différents niveaux.

```php title="database/seeders/MonsterSeeder.php"
public function run(): void
{
    $monsters = [
        ['name' => 'Slime Vert', 'type' => 'slime', 'level' => 1, 'max_hp' => 30, 'attack' => 5, 'defense' => 2, 'exp_reward' => 20, 'gold_reward' => 5],
        ['name' => 'Gobelin Pillard', 'type' => 'goblin', 'level' => 2, 'max_hp' => 50, 'attack' => 12, 'defense' => 5, 'exp_reward' => 45, 'gold_reward' => 12],
        ['name' => 'Squelette Guerrier', 'type' => 'undead', 'level' => 4, 'max_hp' => 80, 'attack' => 25, 'defense' => 15, 'exp_reward' => 110, 'gold_reward' => 30],
        ['name' => 'Orc Berzerker', 'type' => 'orc', 'level' => 7, 'max_hp' => 200, 'attack' => 45, 'defense' => 20, 'exp_reward' => 300, 'gold_reward' => 80],
        ['name' => 'Dragon Rouge (Boss)', 'type' => 'dragon', 'level' => 15, 'max_hp' => 1500, 'attack' => 120, 'defense' => 80, 'exp_reward' => 2500, 'gold_reward' => 1000],
    ];

    foreach ($monsters as $monster) {
        \App\Models\Monster::create($monster);
    }
}
```

## Conclusion de la Phase 2

Les fondations mathématiques de notre monde virtuel sont en place :
- ✅ **Base de données RPG** structurée (Personnages, Bestiaire, Combats).
- ✅ **Algorithmes de Dégâts** (Coups critiques, Mitigation, Esquive) encapsulés dans un Service.
- ✅ **Machine à états de Level Up** sécurisée côté serveur.
- ✅ **Bestiaire initialisé** avec différents niveaux de difficulté.

Dans la **Phase 3**, nous allons ouvrir les "portes du donjon" en créant les **Endpoints API REST** qui permettront au Frontend d'exécuter des actions (Attaquer, Fuir, Se soigner) en appelant ces algorithmes.
