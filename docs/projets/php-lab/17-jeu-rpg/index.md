---
description: "Projet Pratique POO : Forger un système de combat RPG au trait (Tour par tour) en PHP en exploitant l'Héritage et les classes abstraites."
icon: lucide/swords
tags: ["PHP", "POO", "JEU", "HÉRITAGE", "POLYMORPHISME"]
status: stable
---

# Projet 17 : Jeu RPG (Personnages)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Concevoir un jeu vidéo est l'un des meilleurs moyens d'assimiler la Programmation Orientée Objet !
    Dans un RPG (Role Playing Game), tous les protagonistes ont des points de vie (HP), un Niveau et la capacité de prendre des dégâts. En revanche, la manière d'**attaquer** est radicalement différente selon qu'il s'agisse d'un Mage, d'un Guerrier ou d'un Archer.

!!! abstract "Objectifs Pédagogiques"
    1.  **Héritage Comportemental** : Construire la Classe Mère `Character` regroupant l'état civil de l'Entité (HP, Level, Nom).
    2.  **Polymorphisme Magique** : Coder la méthode abstraite `attack(Character $target)` dont l'Implémentation physique diffèrera dans les Enfants.
    3.  **Encapsulation des Dégâts** : Sécuriser la santé via `takeDamage($damage)` pour s'assurer que les HP ne tombent jamais en dessous de Zéro.
    4.  **Boucle de Gameplay** : Faire interagir deux objets `Guerrier` et `Mage` jusqu'à la mort de l'un d'eux.

## 1. La Classe Abstraite `Character`

C'est LE fondement du moteur de jeu. Elle ne peut pas exister par elle-même, on n'invoque jamais un "Personnage" générique sur un champ de bataille. C'est purement une idée mathématique.

```php
<?php
declare(strict_types=1);

abstract class Character {
    
    protected string $name;
    protected int $health;
    protected int $maxHealth;
    protected int $level = 1;
    protected int $experience = 0;
    
    public function __construct(string $name, int $maxHealth) {
        $this->name = $name;
        $this->maxHealth = $maxHealth;
        $this->health = $maxHealth; // Rempli à 100% au spawn
    }
    
    // ============================================
    // LE CONTRAT ABSOLU (Polymorphisme)
    // ============================================
    // Chaque enfant DOIT expliquer COMMENT il attaque. 
    // Prend un AUTRE Personnage (Ennemi) en Cible !
    abstract public function attack(Character $target): int;
    abstract public function getClassName(): string;
    
    // ============================================
    // LES ACTIONS MUTUELLES (Moteur de Physique)
    // ============================================
    
    final public function takeDamage(int $damage): void {
        $this->health -= $damage;
        
        // Empêcher les HP Négatifs
        if ($this->health < 0) {
            $this->health = 0;
        }
        
        echo "💥 <b>{$this->name}</b> subit {$damage} Dégât. HP: {$this->health}/{$this->maxHealth}\n";
    }
    
    final public function heal(int $amount): void {
        $this->health += $amount;
        
        if ($this->health > $this->maxHealth) {
            $this->health = $this->maxHealth;
        }
    }
    
    final public function isAlive(): bool {
        return $this->health > 0;
    }
    
    public function getName(): string {
        return $this->name;
    }
}
?>
```

## 2. Les Différentes Classes Spécialisées

A présent, injectons de la brutalité et de la magie au sein de notre architecture !

```php
<?php
declare(strict_types=1);

// Inclusion du "Moteur"
require_once 'Character.php';

// ============================================
// CLASSE GUERRIER ⚔️
// ============================================
class Warrior extends Character {
    
    private int $strength;
    private bool $rageMode = false;
    
    public function __construct(string $name, int $maxHealth, int $strength) {
        parent::__construct($name, $maxHealth);
        $this->strength = $strength;
    }
    
    // Implémentation du contrat d'Attaque Physique
    public function attack(Character $target): int {
        
        // Si la Rage est active, dégâts doublés !
        $multiplier = $this->rageMode ? 2 : 1;
        $totalDamage = $this->strength * $multiplier;
        
        echo "⚔️ <b>{$this->name} (Guerrier)</b> enrage et frappe <b>{$target->getName()}</b> !\n";
        
        $target->takeDamage($totalDamage); // L'ennemi reçoit l'impact physique
        
        $this->rageMode = false; // La rage se consume après le coup
        
        return $totalDamage;
    }
    
    public function activateRage(): void {
        echo "😡 <b>{$this->name}</b> hurle vers les cieux ! Prochaine attaque DOUBLÉE !\n";
        $this->rageMode = true;
    }
    
    public function getClassName(): string {
        return 'Guerrier Sanglant';
    }
}

// ============================================
// CLASSE MAGE 🔮
// ============================================
class Mage extends Character {
    
    private int $spellPower;
    
    public function __construct(string $name, int $maxHealth, int $spellPower) {
        parent::__construct($name, $maxHealth);
        $this->spellPower = $spellPower;
    }
    
    // Implémentation du contrat d'Attaque Magique
    public function attack(Character $target): int {
        
        // La Magie peut "Coup Critique" avec 30% de chance !
        $isCritical = (rand(1, 100) > 70);
        $totalDamage = $isCritical ? (int)($this->spellPower * 1.5) : $this->spellPower;
        
        echo "🔮 <b>{$this->name} (Mage)</b> murmure une incantation vers <b>{$target->getName()}</b> !\n";
        
        if ($isCritical) {
            echo "✨ <b>COUP CRITIQUE MAGIQUE !</b>\n";
        }
        
        $target->takeDamage($totalDamage); // Impact de Feu
        
        return $totalDamage;
    }
    
    public function getClassName(): string {
        return 'Mage Élémentaire';
    }
}
?>
```

## 3. L'Arène de Combat (Game Loop)

Faisons se rencontrer un Barbare avec beaucoup de PV et un Mage avec peu de PV mais capable de "Critiques". La boucle de mort se chargera de faire l'arbitre.

```php
<?php
// On affiche dans le terminal ou navigateur avec <br> pour la beauté du style.
echo "<h1>🗡️ OMNYVIA ARENA 🔮</h1>";

// 1. Initialisation des Gladiateurs
$barbare = new Warrior('Conan', 150, 15); // 150 HP, 15 Force
$sorcier = new Mage('Gandalf', 80, 22);   // 80 HP, 22 SpellPower

$tour = 1;

// 2. La Boucle de la Mort : La bagarre dure tant que Personne n'est mort.
while ($barbare->isAlive() && $sorcier->isAlive()) {
    
    echo "<h3>--- ROUND $tour ---</h3>";
    
    // A. Action du Mage (Plus rapide dans ce scénario arbitraire)
    $sorcier->attack($barbare);
    
    // Si le barbare meurt sur le coup du Mage, FIN DU JEU.
    if (!$barbare->isAlive()) {
        break;
    }
    
    echo "<br>";
    
    // B. Action du Guerrier
    // Une chance sur cinq d'activer sa RAGE au lieu d'attaquer
    if (rand(1, 100) > 80) {
        $barbare->activateRage();
    } else {
        $barbare->attack($sorcier);
    }
    
    $tour++;
    echo "<hr>";
}

// 3. Déclaration du Vainqueur
echo "<h2>🏆 GAME OVER 🏆</h2>";

if ($barbare->isAlive()) {
    echo "Victoire écrasante du Guerrier : <b>{$barbare->getName()}</b> avec {$barbare->getHealth()} HP Restants !";
} else {
    echo "Victoire de la Connaissance du Mage : <b>{$sorcier->getName()}</b> avec {$sorcier->getHealth()} HP Restants !";
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Vous avez réussi à instancier un Moteur Physique orienté objet. Vous pouvez dès à présent rajouter les Classes enfants :</p>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700"><code>class Archer extends Character</code> : Moins de dégâts bruts mais ne manque jamais sa cible, ou capacité d'esquive totale...</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">2</span>
      <span class="text-gray-700"><code>class Paladin extends Character</code> : Qui, en plus d'attaquer, possède une fonction <code>$this->heal(5)</code> qu'il s'auto-lance sur lui-même à chaque fin de tour s'il est bas en vie. C'est l'essence des MMoRPG (World of Warcraft) !</span>
    </li>
  </ul>
</div>
