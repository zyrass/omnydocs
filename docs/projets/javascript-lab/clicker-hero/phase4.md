---
description: "Phase 4 : DOM Reactive UI. La transformation du Cerveau JS en Pixels cliquables. Mise en place du bouton cliquable géant, du rendu automatique du catalogue de la boutique, et de la validation visuelle des achats impossibles."
icon: lucide/monitor-play
tags: ["JAVASCRIPT", "POO", "DOM", "EVENTS", "UI"]
status: stable
---

# Phase 4 : Rendu UI et Boucle de Rendu

<div
  class="omny-meta"
  data-level="🔴 Avancé (POO)"
  data-version="1.0"
  data-time="1h30">
</div>

!!! quote "Objectif de la Phase"
    Notre Moteur tourne de manière asynchrone dans le noir. Il est grand temps d'illuminer l'écran. 
    Nous allons injecter la dynamique : Un gros bouton (Le Monstre), une jauge d'or, et un tableau HTML généré dynamiquement à partir du champ `this.shopCatalog` de notre objet Game !

## 1. La Squelette HTML d'Origine

Créez `index.html` aux côtés de votre `game.js`.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Clicker Hero (POO Edition)</title>
    <style>
        /* Un CSS brut, basique, pour valider la structure */
        body { font-family: system-ui; text-align: center; background: #1e293b; color: white; padding: 2rem; }
        .hero-btn { font-size: 5rem; cursor: pointer; background: transparent; border: none; transition: transform 0.1s; }
        .hero-btn:active { transform: scale(0.9); }
        .shop { display: flex; flex-direction: column; gap: 10px; max-width: 400px; margin: 2rem auto; }
        .shop-item { background: #334155; padding: 1rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .shop-item button { padding: 10px; cursor: pointer; background: #3b82f6; color: white; border: none; border-radius: 4px; }
        .shop-item button:disabled { background: #64748b; cursor: not-allowed; opacity: 0.5; }
    </style>
</head>
<body>

    <h1>Mon Bilan Financier : <span id="gold-display">0</span> Or</h1>
    <h3>Revenu Passif : <span id="dps-display">0</span> Or / sec</h3>

    <!-- LE BOUTON GLOBAL (Le Monstre à Clic) -->
    <button id="main-clicker" class="hero-btn">👾</button>

    <h2>Boutique d'Investissement</h2>
    <!-- LE CONTENEUR VIDE DE LA BOUTIQUE -->
    <div id="shop-container" class="shop"></div>

    <script src="game.js"></script>
</body>
</html>
```

## 2. Le Dessin de la Boutique (Render)

Retournez dans `game.js`, dans la classe globale `Game`.
Nous allons combler la méthode `.init()` qui était vide de toute interaction DOM :

```javascript
/* --- game.js (Dans class Game) --- */

init() {
    console.log("Moteur de Jeu Allumé.");
    
    // 1. Écoute du Clic Principal !
    const mainBtn = document.getElementById('main-clicker');
    mainBtn.addEventListener('click', () => {
        // La méthode qu'on a codée en Phase 3
        this.handleGlobalClick();
    });

    // 2. Fabrication des balises de la Boutique (Une seule fois au démarrage)
    const shopDiv = document.getElementById('shop-container');
    
    this.shopCatalog.forEach((upgradeObj, index) => {
        // Création d'une div "shop-item" pour chaque Usine du catalogue
        const itemDiv = document.createElement('div');
        itemDiv.className = 'shop-item';
        
        // ATTENTION : On associe un ID Unique au bouton
        // pour que updateUI() (plus tard) puisse le retrouver sans refaire tout le HTML !
        itemDiv.innerHTML = `
            <div>
                <strong>${upgradeObj.name} (Niv. <span id="lvl-${index}">0</span>)</strong><br>
                <span>+${upgradeObj.dpsBonus} Or/s</span>
            </div>
            <button id="buy-btn-${index}">Acheter (<span id="cost-${index}">${upgradeObj.baseCost}</span>)</button>
        `;
        shopDiv.appendChild(itemDiv);

        // LE BINDING DU BOUTON ACHAT !
        document.getElementById(`buy-btn-${index}`).addEventListener('click', () => {
            // "Dis à cet Upgrade précis de s'Acheter en facturant le Joueur Global."
            if (upgradeObj.buy(this.player)) {
                this.updateUI(); // Succès = L'écran doit changer
            }
        });
    });

    // 3. Premier affichage
    this.updateUI();
    
    // 4. Lancement de la course temporelle (Déjà codée en Phase 3 !)
    this.startLoop();
}
```

!!! tip "La perfection de la fonction anonyme fléchée `() =>`"
    Pourquoi écrire `() => { this.handleGlobalClick(); }` et pas `function() { this... }` ?
    Dans un événement de souris `addEventListener`, une `function()` normale détruit le mot `this` et croit que "This = le bouton HTML". La fonction fléchée ES6 protège le contexte ! `this` continue de désigner la classe "Game". Sans ça, le jeu plante instantanément ("undefined is not a function").

## 3. L'Interface Reactive (UpdateUI)

La métode redoutable. Elle rafraîchit les 2 zones critiques à l'écran : Le compte en banque, et le "Grisage" des boutons de la boutique en fonction des fonds. C'est elle qui donne "vie" au jeu à chaque milliseconde.

```javascript
/* --- Dans class Game --- */

updateUI() {
    // 1. Mise à jour de la vitrine financière
    document.getElementById('gold-display').textContent = this.player.gold;
    document.getElementById('dps-display').textContent = this.player.goldPerSecond;

    // 2. Mise à jour du catalogue de la boutique
    this.shopCatalog.forEach((upgradeObj, index) => {
        // MAJ du Texte
        document.getElementById(`lvl-${index}`).textContent = upgradeObj.level;
        document.getElementById(`cost-${index}`).textContent = upgradeObj.getCost();

        // INTELLIGENCE ARTIFICIELLE DE L'UI : 
        // Si le joueur est plus pauvre que l'objet, alors le bouton HTML Disabled = TRUE
        const btn = document.getElementById(`buy-btn-${index}`);
        if (this.player.gold < upgradeObj.getCost()) {
            btn.disabled = true; // Bouton grisé par le CSS !
        } else {
            btn.disabled = false; // Bouton actif, bleu !
        }
    });
}
```

*Note: Le `setInterval` de notre gameLoop (Phase 3) appelant DÉJÀ cette méthode Chaque Seconde, les boutons s'activeront tous seuls dès lors que l'or passif accumulé couvrira le prix des objets ! Pas besoin d'écrire de code supplémentaire !*

## Conclusion de la Masterclass

- [ ] L'écran s'ouvre, vous avez `0` or. Tous les boutons d'achats sont grisés.
- [ ] Vous détruisez votre souris en cliquant très vite sur l'émoticon alien (👾). En haut, le chiffre grandit.
- [ ] DÈS que vous passez la barre des `15`, le bouton d'achat "Souris Auto" **s'illumine soudainement en bleu** (Il passe en `disabled = false`).
- [ ] Vous cliquez dessus. Votre or chute brutalement. Le bouton d'achat redevient Grisé. Son niveau passe à `1`. Le coût suivant passe à `17`.
- [ ] Vous lâchez la souris. L'or augmente infiniment de `1` chaque seconde sans que vous ne fassiez rien (`setInterval`). 

👑 **Mission Accomplie.**
Vous avez bâti le **Moteur de Jeu (Game Engine) asynchrone Singleton Object-Oriented**. Vous comprenez désormais fondamentalement comment est structuré un jeu, une application Desktop, ou même un système d'exploitation Windows : Une boucle globale qui tourne à l'infini, qui regarde l'heure, qui regarde votre clic de souris, et redessine l'écran en fonction des entités.

L'univers du JavaScript est désormais sous votre absolue maîtrise. Vous êtes diplômable.
