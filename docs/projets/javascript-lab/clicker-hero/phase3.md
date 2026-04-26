---
description: "Phase 3 : L'Orchestrateur Suprême. Conception de la classe 'Game' (Le Singleton) qui englobe le joueur et les boutiques. Création de l'horloge interne globale."
icon: lucide/clock
tags: ["JAVASCRIPT", "POO", "CLASS", "SETINTERVAL", "GAME-LOOP"]
status: stable
---

# Phase 3 : Le Game Engine (Game Loop)

<div
  class="omny-meta"
  data-level="🔴 Avancé (POO)"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le Joueur (Phase 1) sait gérer son or. L'Usine (Phase 2) sait gérer son prix. Mais "Qu'est ce que le Jeu ?"
    En architecture logicielle, on crée un objet Maître, le Moteur (Engine), qui contient toutes les autres pièces du puzzle et qui les fait avancer dans le temps. C'est l'essence de la boucle `Update()`.

## 1. La Classe Game (Le Chef d'Orchestre)

Toujours dans `game.js`, tout en haut du fichier (car c'est l'entité suprême) :

```javascript
/* --- game.js --- */

class Game {
    
    // Le Jour 1 du Jeu
    constructor() {
        // Le Jeu "possède" un joueur.
        // Il l'instancie LUI-MÊME depuis le Plan de la Phase 1 !
        this.player = new Player();

        // Le Jeu "possède" toute la liste des boutiques existantes.
        // Il les instancie LUI-MÊME depuis le Plan de la Phase 2 !
        // C'est un simple Tableau d'Objets [Upgrade, Upgrade]
        this.shopCatalog = [
            new Upgrade('Clic Souris Amélioré', 15, 1),
            new Upgrade('Grand-Mère', 100, 5),
            new Upgrade('Mine de Charbon', 1100, 47)
        ];

        // L'horloge interne
        this.timer = null;
    }

    // 1. Initialiser le Moteur au lancement du site web
    init() {
        console.log("Moteur de Jeu Allumé. Bienvenue dans Clicker Hero.");
        
        // Tout de suite, on allume l'horloge biologique du jeu
        this.startLoop();
    }

    // 2. LA BOUCLE TEMPORELLE (Le Cœur Battant)
    startLoop() {
        // setInterval exécute le code interne chaque seconde (1000ms)
        this.timer = setInterval(() => {
            
            // Si le joueur gagne 10 Or/Sec, eh bien ajoute virtuellement 10 à la Bourse
            if (this.player.goldPerSecond > 0) {
                this.player.gold += this.player.goldPerSecond;
                console.log(`[TEMPS] : +${this.player.goldPerSecond}. Total: ${this.player.gold}`);
            }

            // Avertir le Rendu Visuel (Phase 4) qu'il faut se mettre à jour
            this.updateUI();

        }, 1000);
    }

    // 3. Agence de Routage : Le clic manuel atterrit ici
    handleGlobalClick() {
        this.player.clickMonster();
        this.updateUI(); // Le chiffre doit changer immédiatement à l'écran
    }

    // 4. Agence de l'Interaction CSS
    updateUI() {
        // La Phase 4 ira ici ! (Modification du DOM HTML)
    }
}
```

Prenez conscience de l'élégance de cette structure : Aucun composant "ne traîne dans le vide" (En espace global Windows). Tout ce qui compose l'univers du jeu se trouve **à l'intérieur** de l'Accolade de `class Game`.

## 2. Le Boot (L'Allumage)

Effacez tous vos anciens codes de tests de la fin de `game.js`. (Adieu le `const hero = new Player()`).
Désormais, le lancement de l'application tient en **deux** lignes impériales, et rien de plus.

```javascript
/* --- game.js --- (TOUT EN BAS) */

// L'application entière est encapsulée dans cet objet unique.
const App = new Game();

// Allumage.
App.init();

// Pour vos tests manuels : Tapez App.handleGlobalClick() dans la console du navigateur !
// Observez le chiffre augmenter. Activez la boucle temporelle.
```

## Checklist de la Phase 3

- [ ] "Moteur de jeu allumé" s'imprime bien dans la console navigateur F12.
- [ ] Mettez le `dpsBonus` de "Souris Auto" à `1` et forcez un test : achetez la "Souris Auto" en ligne de commande locale : `App.shopCatalog[0].buy(App.player)`. 
- [ ] Regardez passivement votre console. Que se passe-t-il ? Toutes les 1 secondes exactes, le statut `[TEMPS]` s'imprime en augmentant la valeur originelle. Le jeu vit de manière autonome.

Votre moteur est immaculé. Ses rouages mathématiques tournoient dans le noir absolu de la mémoire RAM, hors de la vue de l'humain assis devant le PC. Il faut matérialiser ce génie informatique sous forme visible. C'est l'objectif de la phase ultime : **Phase 4 - La Vue DOM Reactive**.

[Passer à la Phase 4 : Interface DOM Reactive →](phase4.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
