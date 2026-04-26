---
description: "Phase 3 : Injection & Interface DOM. Connecter l'Abstract Array JS (Le Cerveau) à la CSS Grid Visuelle, et générer les balises 'Cell' manquantes avec document.createElement."
icon: lucide/refresh-cw
tags: ["JAVASCRIPT", "DOM", "GRID", "UI"]
status: stable
---

# Phase 3 : Synthèse DOM & UI

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le Joueur a cliqué, la gravité a calculé sa chute, et le 2D Array a stocké le pion ROUGE en case `[4][3]`. Ce fichier va transformer le vide de l'écran en un damier de 42 trous, et s'assurer que le trou `[4][3]` reçoive purement et simplement la class CSS ".red". C'est de l'injection d'État.

## 1. La Fabrication des Trous au Chargement (Draw Board)

Détruisez vos commentaires d'essai dans `index.html`. La balise `<div id="board">` doit rester vierge.
Rendez-vous dans la fonction `initGame()` de votre `game.js` et ajoutons la création plastique :

```javascript
/* --- LE RENDU DEUXIÈME PARTIE : L'Usine des Trous Bleus --- */

// (Code de la Phase 2 juste au dessus...)

function initGame() {
    grid = [];
    currentPlayer = 1;
    isGameOver = false;
    
    // Le conteneur du fond Bleu Vierge
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = ''; // Grand nettoyage d'été si on vient de Recommencer

    // 1. Double boucle FOR pour balayer 6x7 = 42 opérations.
    for (let r = 0; r < ROWS; r++) {
        const row = [];
        for (let c = 0; c < COLS; c++) {
            row.push(0);
            
            // 2. CRÉATION DU HTML
            const cell = document.createElement('div');
            // On attribue la class "cell" (Le rond vide de couleur Nuit de notre CSS)
            cell.classList.add('cell');
            // On greffe les attributs de ciblage "Dataset" indispensables
            cell.dataset.row = r;
            cell.dataset.col = c;
            
            // 3. Pose dans le DOM !
            boardElement.appendChild(cell);
        }
        grid.push(row);
    }
    
    // 4. On réaligne le texte en haut "C'est à tel joueur..."
    updateStatusText();
}
```

## 2. Peindre l'État (L'Update DOM)

Lorsqu'un visiteur clique sur un trou vide, la gravité est calculée (Phase 2, Fonction `playTurn`). À cet endroit crucial (là où nous avons déposé les "TODO Phase 3 et 4"), il est temps de demander au navigateur de **peindre** la tuile `[y][x]` !

```javascript
// La fonction appelée juste après avoir inséré un '1' ou '2' dans le tableau Javascript
function updateDOM(r, c, playerNumber) {
    // 1. Chercher le DIV exact grâce aux Selecteurs d'Attributs de CSS
    // On veut le Div qui a data-row="4" ET data-col="3" !
    const targetCell = document.querySelector(`.cell[data-row='${r}'][data-col='${c}']`);
    
    if (targetCell) {
        // 2. Ajouter la couleur
        if (playerNumber === 1) {
            targetCell.classList.add('red'); // CSS Phase 1 ! (L'animation Drop Anim tombe toute seule)
        } else {
            targetCell.classList.add('yellow');
        }
    }
}
```

Appelons cette merveille à la fin de la fonction `playTurn` de l'épisode précédent :

```javascript
// ... Dans Moteur Physique (playTurn)
// Si le trou est libre...
grid[r][colIndex] = currentPlayer;

// Mettre à jour l'écran IMMÉDIATEMENT
updateDOM(r, colIndex, currentPlayer);

// TODO Phase 4: Vérifier Victoire

// On switch !
currentPlayer = (currentPlayer === 1) ? 2 : 1; 
updateStatusText();
return;
```

## 3. Le Statut Joueur (Feedback UX)

Enfin, n'oubliez pas d'indiquer à l'humain qui doit jouer pour ne pas le rendre fou.

```javascript
function updateStatusText() {
    const statusText = document.getElementById('status-text');
    
    // Si la partie est finie, ignorer l'update. (Sera géré par Win())
    if (isGameOver) return;
    
    if (currentPlayer === 1) {
        statusText.textContent = "Tour du Joueur : Rouge";
        statusText.className = "text-red";
    } else {
        statusText.textContent = "Tour du Joueur : Jaune";
        statusText.className = "text-yellow";
    }
}
```

Reliez le magnifique bouton "Recommencer" (Reset) à notre fonction mère :

```javascript
document.getElementById('reset-btn').addEventListener('click', () => {
    initGame(); // Efface la Matrice + le HTML et recommence au Tour 1.
});
```

## Checklist de la Phase 3

- [ ] L'écran s'ouvre. Ce n'est plus une page vide. Le CSS Grid 6x7 trous se génère de nulle part sous vos yeux en 1 milliseconde via le DOM Level 2 (`appendChild`).
- [ ] L'entête écrit "Tour du Joueur Rouge".
- [ ] Mettez le curseur de la souris sur le haut de la colonne du milieu, et cliquez.
- [ ] Le Jeton s'affiche tout en bas ! Pensez à admirer la fluidité incroyable de la `dropAnim` native du CSS 3D.
- [ ] L'entête écrit désormais "Tour du Joueur Jaune". 
- [ ] Cliquez 6 fois sur la même colonne... Les jetons s'empilent. Au 7ème clic : RIEN ! C'est ce qu'on appelle la maturité technologique (L'Anti-Cheat Phase 2 marche).

Vous êtes face au dernier sommet. Votre jeu tourne parfaitement, mais est absolument interminable et sans enjeux. Il faut que l'ordinateur vérifie des dimensions spatiales. Il lui faut **l'Algorithme de Détection de Lignes**. 

[Passer à la Phase 4 : Conditions de Victoire Mathématique →](phase4.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
