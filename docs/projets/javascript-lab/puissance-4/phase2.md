---
description: "Phase 2 : Initialisation Mathématique & Moteur V8. Générer le 2D Array, capturer le clic du joueur sur une colonne, et coder l'algorithme de Gravité (While). "
icon: lucide/function-square
tags: ["JAVASCRIPT", "LOGIC", "MATH", "ALGORITHM"]
status: stable
---

# Phase 2 : Gravité et Moteur de Jeu

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le CSS Grid affiche virtuellement 42 cases, mais le Javascript est aveugle. Nous devons construire la Matrice en mémoire (un tableau dans un tableau `grid[y][x]`), écouter le clic d'un humain, et faire "tomber" le jeton en modifiant les chiffres `0` en `1` ou `2`.

## 1. Initialiser le Cerveau (L'État / State)

Ouvrez `game.js`. L'ingénierie réclame l'usage de constantes pour éviter les "Magic Numbers" éparpillés dans le code.

```javascript
/* --- CONSTANTES PHYSIQUES --- */
const ROWS = 6;
const COLS = 7;

/* --- LE CERVEAU --- */
let grid = []; // Le fameux Tableau 2D
let currentPlayer = 1; // 1 = Rouge, 2 = Jaune
let isGameOver = false; // Le verrouillage

// Fonction vitale : Fabriquer la grille vide (Des zéros partout)
function initGame() {
    grid = []; // Nettoyage total
    currentPlayer = 1;
    isGameOver = false;

    // Boucle de construction de matrice
    for (let r = 0; r < ROWS; r++) {
        const row = []; // On fabrique une Ligne
        for (let c = 0; c < COLS; c++) {
            row.push(0); // On met 7 Zéros dedans
        }
        grid.push(row); // On insère la ligne dans la Grille Globale
    }
    
    // Pour l'instant on ne fait que logger, la magie HTML viendra après
    console.table(grid); 
}

initGame();
```

!!! tip "La perfection du console.table()"
    Regardez la console (F12) de votre navigateur. La commande `console.table(grid)` dessine un magnifique tableau Excel avec les index des Lignes (Y) et des Colonnes (X). C'est votre GPS mental absolu pour ne jamais vous perdre.

## 2. Capturer la Dépression Plastique (Clic)

Le Puissance 4 physique n'a pas 42 boutons. Il n'a que **7 Entrées**, en haut des colonnes.
Toutefois sur un écran, l'utilisateur va cliquer "n'importe où" sur le plateau de plastique. Notre script doit répondre "Ah, tu as cliqué sur le trou [2][5], donc tu essaies de jouer dans la Colonne 5 !".

Nous utiliserons la Délégation d'Évenements (Cf Projet Hub Applicatif).
*(Ne faites pas l'erreur de cibler `.cell` car elles ne sont pas encore construites en HTML !)*

```javascript
/* --- ECOUTE DÉLÉGUÉE --- */
const boardElement = document.getElementById('board');

boardElement.addEventListener('click', (e) => {
    // Si le jeu est fini, la souris est morte.
    if (isGameOver) return;
    
    // Remonte l'arbre du clic jusqu'à trouver l'éventuelle classe .cell
    const clickedCell = e.target.closest('.cell');
    if (!clickedCell) return; // Il a cliqué sur le plastique bleu.

    // On extirpe la COLONNE depuis l'attribut HTML "data-col" (ex: "5")
    const targetCol = parseInt(clickedCell.dataset.col);
    
    // On passe cette colonne au mécanicien (La Gravité)
    playTurn(targetCol);
});
```

## 3. L'Algorithme de Gravité Verticale

Voici le test de recrutement classique pour un développeur JS.
*Problème : Je lâche un pion en Colonne 5. Je dois parcourir la colonne de TOUT EN BAS jusqu'en haut, scanner s'il y a de l'espace (0), et écraser le 0 avec mon Joueur.*

```javascript
/* --- LE MOTEUR PHYSIQUE --- */

function playTurn(colIndex) {
    if (isGameOver) return; // Verrou ultime

    // On part du sol (Ligne 5) et on remonte (-1) jusqu'au plafond (Ligne 0)
    for (let r = ROWS - 1; r >= 0; r--) {
        
        // Est-ce que ce "trou" de ma Matrice est vide ?
        if (grid[r][colIndex] === 0) {
            
            // OUI ! La gravité s'arrête ici. 
            // J'écrase le vide avec l'empreinte digitale du Joueur Actuel.
            grid[r][colIndex] = currentPlayer;

            console.log(`Pion inséré en Ligne ${r}, Colonne ${colIndex}`);
            console.table(grid); // Observez l'état du Cerveau !

            // TODO : Phase 3 = Appelez updateDOM() pour dessiner le pion

            // TODO : Phase 4 = Appelez checkWin() pour la condition d'arrêt

            // Fin du Tour. Inversion Booléenne du Joueur !
            currentPlayer = (currentPlayer === 1) ? 2 : 1; 

            // IMPORTANT : Interruption de l'algorithme car le jeton a atterri.
            return; 
        }
    }
    
    // Si la boucle For se termine sans jamais déclencher de "return", 
    // l'algorithme a atteint le Plafond et n'a trouvé aucun trou !
    console.warn("Colonne pleine ! Opération interdite.");
}
```

## Checklist de la Phase 2

- [ ] L'application HTML est toujours vide, ce qui est normal (-). Mais la Formule 1 vrombit dans la console.
- [ ] J'ouvre F12. Mon écran `console.table` affiche bien un parterre de zéros.
- [ ] Dans la console, j'écris manuellement `playTurn(3)`. Le tableau s'actualise, et je vois un beau `1` tout en bas de l'échiquier (Ligne 5, Col 3).
- [ ] Si je tape encore `playTurn(3)`, un `2` apparaît juste au dessus (Ligne 4, Col 3).
- [ ] Si je tape frénétiquement plein de fois `playTurn(3)`, la console criera `Colonne pleine`. L'Anti-Cheat (L'anti-fraude) est en place.

Le Cerveau fonctionne à un niveau divin. Mais l'humain devant son navigateur Chrome s'ennuie car l'écran reste blanc. Branchons les câbles du rendu visuel de la **Phase 3 : Injection & Interface DOM**.

[Passer à la Phase 3 : Rendu et Synthèse DOM →](phase3.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
