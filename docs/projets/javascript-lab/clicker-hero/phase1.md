---
description: "Phase 1 : Design Architectural Orienté Objet. Conception de la classe 'Player', encapsulation des données sensibles (Or, DPS) dans le Constructeur, et méthodes métiers."
icon: lucide/user
tags: ["JAVASCRIPT", "POO", "CLASS", "CONSTRUCTOR", "THIS"]
status: stable
---

# Phase 1 : La Classe Player (POO)

<div
  class="omny-meta"
  data-level="🔴 Avancé (POO)"
  data-version="1.0"
  data-time="45m">
</div>

!!! quote "Objectif de la Phase"
    Pour échapper au chaos des dizaines de variables éparpillées (`let gold = 0`, `let dps = 0`, `let clickPower = 1`), nous allons créer un "Plan d'Architecte" appelé `Class`. Ce plan définira ce qu'**est** un Joueur (Ses propriétés) et ce que **sait faire** un Joueur (Ses méthodes). C'est le pilier de l'encapsulation.

## 1. Création de la Classe Joueur

Créez le fichier `game.js`. (Pas besoin d'HTML pour le moment, c'est de l'architecture pure !).

Le mot clé `class` définit une entité.
Le mot clé `constructor() { ... }` est la fonction magique qui s'exécute **une seule fois** lorsque vous créez un joueur physique à partir de ce plan abstrait. C'est l'ADN de l'objet.

```javascript
/* --- game.js --- */

class Player {
    
    // Le code qui s'exécute le Jour de la Naissance de l'objet
    constructor() {
        // Le mot 'this' signifie "Moi-Même".
        // "Ma propre bourse d'or est de 0".
        this.gold = 0;              
        
        // "Ma propre force de clic est de 1".
        this.clickPower = 1;        
        
        // "Mes Dégâts Par Seconde (Revenu passif) sont nuls"
        this.goldPerSecond = 0;     
    }

    // --- LES MÉTHODES MÉTIER (Ce que l'entité SAIT faire) ---

    // 1. Le Joueur prend sa hache et frappe le monstre
    clickMonster() {
        this.gold += this.clickPower;
        console.log(`Le joueur a cliqué ! Il possède maintenant ${this.gold} Or.`);
    }

    // 2. Le Joueur tente d'acheter une chose (Si son portefeuille le permet)
    spendGold(amount) {
        if (this.gold >= amount) {
            this.gold -= amount;
            return true; // Transaction validée
        } else {
            return false; // Transaction refusée (Fonds insuffisants)
        }
    }

    // 3. Le Joueur devient plus puissant passivement (Après l'achat d'une usine)
    addDPS(amount) {
        this.goldPerSecond += amount;
    }
}
```

Prenez le temps d'assimiler ce paradigme. La classe `Player` gère ses *propres* affaires. Elle refuse de modifier l'or sans passer par `spendGold()`. C'est ce qu'on appelle la **Responsabilité Unique (SRP)**.

## 2. Instanciation (La Naissance)

Une `class` n'existe pas dans le monde réel tant qu'elle n'est pas instanciée avec le mot-clé `new`.

Ajoutez ceci tout en bas de votre `game.js` pour tester votre prouesse architecturale :

```javascript
// On instancie la classe. 'hero' est un Véritable Objet vivant en mémoire !
const hero = new Player();

// Le joueur clique 3 fois frénétiquement
hero.clickMonster();
hero.clickMonster();
hero.clickMonster();

// Ilessaie d'acheter une épée à 5 Or
const achatEpee = hero.spendGold(5);
console.log(`Le marchand a-t-il accepté mon argent ? ${achatEpee}`); // False !

// Le joueur gagne au loto manuellement
hero.gold += 100;

// Il réessaie
const nouvelAchat = hero.spendGold(5);
console.log(`Le marchand a-t-il accepté ? ${nouvelAchat}`); // True !
console.log(`Argent restant du Héro : ${hero.gold}`); // 98 (100+3-5)
```

## Checklist de la Phase 1

- [ ] Lisez attentivement la syntaxe "Class". Remarquez-vous l'absence du mot de liaison `function` devant `clickMonster()` ? Dans une classe Javascript, les fonctions s'écrivent directement par leur nom.
- [ ] Ouvre le fichier avec NodeJs ou la console F12 de votre navigateur. Observez la beauté des objets qui se modifient eux-mêmes.
- [ ] **Évidence logique** : Le joueur ne possède aucune méthode du type `dessinerBouton()`. C'est parfaitement normal ! Un joueur n'est pas censé connaître le HTML ou le CSS. Le code de rendu (UI) sera géré par la classe "Game" plus tard.

Le "Héro" est prêt. Mais dans un vrai "Idle Game", on passe son temps à acheter des bâtiments passifs (Mines, Temples, Usines, Curseur de Souris). Créons l'usine à bâtiments dans la **Phase 2 : La Classe Upgrade**.

[Passer à la Phase 2 : Classe Upgrade et Inflation Mathématique →](phase2.md)
