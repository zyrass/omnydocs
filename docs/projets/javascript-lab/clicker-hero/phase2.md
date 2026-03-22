---
description: "Phase 2 : Polymorphisme d'entités avec la classe 'Upgrade'. Création de la boutique, gestion de l'inflation exponentielle (Math.pow), et liaisons inter-classes (Passer un Joueur à une Boutique)."
icon: lucide/trending-up
tags: ["JAVASCRIPT", "POO", "CLASS", "MATH", "POINTER"]
status: stable
---

# Phase 2 : La Classe Upgrade

<div
  class="omny-meta"
  data-level="🔴 Avancé (POO)"
  data-version="1.0"
  data-time="1h00">
</div>

!!! quote "Objectif de la Phase"
    Le Joueur (Phase 1) est une instance unique (Un Singleton, car il n'y a qu'un joueur). Mais les bâtiments (Mines, Temples, Clics Souris) sont multiples. Au lieu de coder 15 objets Javascript à la main, nous allons coder une "Usine à Bâtiments" : La classe `Upgrade`.

## 1. Création du Plan de Fabrication (L'Usine)

Toujours dans `game.js`, sous votre classe `Player` :

```javascript
/* --- game.js --- */

class Upgrade {
    
    // Le constructeur demande 3 arguments pour naître !
    constructor(name, baseCost, dpsBonus) {
        this.name = name;           // Le Tître ("Grand-Mère", "Mine de Fer")
        this.baseCost = baseCost;   // Le prix d'origine à 0 bâtiment possédé
        this.dpsBonus = dpsBonus;   // Combien d'or/sec ça rapporte ?
        this.level = 0;             // Au début, on en possède Zéro.
    }

    // 1. L'Intelligence Artificielle de l'Inflation : Le Prix Dynamique
    // Plus le joueur possède ce bâtiment, plus il coûte extrêmement cher.
    getCost() {
        // Formule Universelle Idle Game : Prix de Base * (Multiplicateur ^ Niveau)
        // Math.pow(1.15, level) = 1.15 puissance 'level'
        return Math.floor(this.baseCost * Math.pow(1.15, this.level));
    }

    // 2. L'Interaction Ultime : Acheter
    // C'est magique : La boutique REÇOIT l'objet Joueur en Argument 
    // afin de piocher dans SA propre bourse !
    buy(playerObj) {
        const currentPrice = this.getCost();

        // On fait communiquer l'Objet 'Boutique' avec l'Objet 'Player' !
        if (playerObj.spendGold(currentPrice)) {
            // Le joueur avait assez d'argent. L'achat est validé.
            this.level++;
            
            // On demande au joueur d'augmenter son score passif !
            playerObj.addDPS(this.dpsBonus);
            
            console.log(`L'usine [${this.name}] passe au niveau ${this.level}. Revenue: +${this.dpsBonus} Or/s`);
            return true;
        } else {
            console.warn(`[${this.name}] Fonds Insuffisants !`);
            return false;
        }
    }
}
```

## 2. Instanciation des Diverses Boutiques

C'est ici qu'on mesure la beauté terrifique de l'architecture par "Class".
Nous voulons créer 3 bâtiments extrêmement différents dans notre jeu. Devons-nous réécrire les formules mathématiques 3 fois ? Non !

Prouvez-le à vous-même en bas de votre fichier JS (dans votre terrain de test) :

```javascript
// On fabrique notre Humain
const hero = new Player();
// Tricherie pour lui donner de l'argent et tester l'économie
hero.gold = 500; 

// FABRICATION DES BOUTIQUES À LA VOLÉE
const autoClicker = new Upgrade("Souris Auto", 15, 1);
const grandma = new Upgrade("Grand-Mère du village", 100, 5);
const mine = new Upgrade("Mine de Charbon", 1100, 47);

// Le joueur essaie d'acheter !
console.log(`Argent de départ : ${hero.gold}`);

// On dit à l'Objet 'autoClicker': "Achète-toi, et facture l'Objet 'hero'".
autoClicker.buy(hero); 
// Le prix passe de 15 à 17 ! (15 * 1.15).
autoClicker.buy(hero);
autoClicker.buy(hero); 

// Essayons l'achat d'un bâtiment lourd !
grandma.buy(hero);

// Essayons la Mine (1100) avec un portefeuille de (500 - 15 - 17 - 19 - 100 = 349)
mine.buy(hero); // [Console : Fonds insuffisants !]

console.log(`Le joueur gagne PASSIVEMENT : ${hero.goldPerSecond} Or/s !`);
```

## Checklist de la Phase 2

- [ ] Je comprends fondamentalement la différence entre `Player` (Entité Unique) et `Upgrade` (Entité Multiple).
- [ ] La communication entre deux objets vous semble logique (L'objet A déclenche la méthode `.spendMoney()` appartenant à l'objet B).
- [ ] L'inflation est testée. L'achat d'un AutoClicker n'a pas impacté le prix de la Mine. La propriété `this.level` est strictement attachée à l'instance précise du bâtiment, l'environnement est hermétique !

L'économie fonctionne en circuit fermé parfait dans la RAM de l'ordinateur. Le drame s'installe cependant : le temps est figé.
*Rien* n'avance. L'Or Par Seconde (`dps`) est à 8, mais le portefeuille ne gonfle pas parce que le moteur central (Le Temps) n'existe pas. Il manque la dimension suprême des Jeux Virutels : **Le Game Engine (Phase 3).**

[Passer à la Phase 3 : Le Game Loop Temporel →](phase3.md)
