---
description: "Phase 4 : Algorithmique complexe. Développement du scanner de Victoire dans la matrice bi-dimensionnelle (Horizontal, Vertical, Diagonales). Finalisation de l'Ui de succès."
icon: lucide/trophy
tags: ["JAVASCRIPT", "ALGORITHM", "MATH", "LOGIC", "WIN"]
status: stable
---

# Phase 4 : Condition de Victoire & Reset

<div
  class="omny-meta"
  data-level="🔴 Avancé (Certifiant)"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le vrai test de logique mathématique d'un développeur commence ici.
    Comment savoir, après qu'un pion a été déposé en case `[R][C]`, que 4 pions de même couleur se touchent ? Il faut scanner la grille Horizontalement, Verticalement, et Diagonalement (Sens montant et descendant), en s'assurant de ne jamais lire "en dehors du cadre" pour ne pas faire crasher Javascript (`undefined`).

## 1. La Fonction Principale et l'Encapuslateur

La stratégie universelle consiste à créer une fonction d'aide (Helper) qui prend 4 coordonnées, et qui renvoie `true` si les 4 coordonnées contiennent le numéro `1` (ou `2`).

```javascript
/* --- HELPER CHECK --- */
function checkMatch(r1, c1, r2, c2, r3, c3, r4, c4) {
    const val = currentPlayer;
    
    // Si TOUTES les cases existent dans le tableau (Pas en dehors du board)
    // ET qu'elles contiennent toutes la VRAIE valeur du joueur Actif
    if (grid[r1] !== undefined && grid[r1][c1] === val &&
        grid[r2] !== undefined && grid[r2][c2] === val &&
        grid[r3] !== undefined && grid[r3][c3] === val &&
        grid[r4] !== undefined && grid[r4][c4] === val) {
            return true;
    }
    return false;
}
```

Désormais, après CHAQUE pion lâché, on va vérifier l'ENSEMBLE de l'échiquier pour voir si l'on trouve ce fameux schéma.

## 2. Le Scanner Vectoriel Spatial (Brute Force)

Voici la fonction de victoire complète et certifiante. Elle balaye `r` (Row) et `c` (Col).
Puisqu'on cherche 4 pions, ce n'est pas la peine de scanner jusqu'au bord extrême droit, car un alignement vers la droite doit forcément commencer à 3 cases du bord.

```javascript
/* --- ALGORITHME DE VICTOIRE (WIN CHECK) --- */
function checkWin() {
    
    // 1. SCAN HORIZONTAL (Ligne par ligne, on s'arrête 3 cases avant la fin droite)
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS - 3; c++) {
            if (checkMatch(r, c, r, c+1, r, c+2, r, c+3)) return true;
        }
    }

    // 2. SCAN VERTICAL (Colonne par colonne, on s'arrête 3 cases avant le fond Bas)
    for (let c = 0; c < COLS; c++) {
        for (let r = 0; r < ROWS - 3; r++) {
            if (checkMatch(r, c, r+1, c, r+2, c, r+3, c)) return true;
        }
    }

    // 3. SCAN DIAGONALE DESCENDANTE (\)
    // On doit avoir 3 cases libres vers le bas ET vers la droite
    for (let r = 0; r < ROWS - 3; r++) {
        for (let c = 0; c < COLS - 3; c++) {
            if (checkMatch(r, c, r+1, c+1, r+2, c+2, r+3, c+3)) return true;
        }
    }

    // 4. SCAN DIAGONALE MONTANTE (/)
    // On doit avoir 3 cases libres vers le HAUT et vers la DROITE
    for (let r = 3; r < ROWS; r++) { // On démarre ligne 3 pour avoir de la marge vers le 0 (Haut)
        for (let c = 0; c < COLS - 3; c++) {
            if (checkMatch(r, c, r-1, c+1, r-2, c+2, r-3, c+3)) return true;
        }
    }

    return false; // S'il a scanné tout l'univers et ne trouve rien
}
```

## 3. Le Verrouillage de la Partie (Game Over UI)

Rappelez-vous les `#TODO` de la **Phase 2** dans notre `playTurn`. Il est temps de les remplacer.

```javascript
/* Extrait du Moteur de Jeu playTurn(colIndex) de la PHASE 2 */

// ... (Pion inséré) ...
updateDOM(r, colIndex, currentPlayer);

// L'Appel à l'API de Victoire
if (checkWin()) {
    isGameOver = true; // Empêche tout futur clic !
    const statusText = document.getElementById('status-text');
    
    // On écrase le texte par l'annonce !
    statusText.textContent = `🎉 VICTOIRE DU JOUEUR ${(currentPlayer === 1)?'ROUGE':'JAUNE'} ! 🎉`;
    
    // Petit effet de surbrillance CSS bonus
    statusText.style.background = (currentPlayer === 1) ? '#ef4444' : '#eab308';
    statusText.style.color = (currentPlayer === 1) ? 'white' : 'black';
    return; // FIN TOTALE DU TOUR ET DE LA PARTIE
}

// Sinon, la partie continue, on switch
currentPlayer = (currentPlayer === 1) ? 2 : 1; 
updateStatusText();
```

!!! note "L'Egalité Parfaite (Draw)"
    Dans code ci-dessus, il manque la condition où les 42 trous sont pleins et personne n'a gagné ! Saurez-vous rajouter un compteur de coups qui, s'il atteint `42`, déclare *"Égalité"* ?

## Checklist Pédagogique et Conclusion

- [ ] L'algorithme mathématique ne provoque pas de bugs rouges si vous jouez sur les bords extrêmes du tableau.
- [ ] Alignez 4 jetons Jaunes à l'horizontale. L'écran du haut crie "VICTOIRE".
- [ ] **Essai Critique** : Essayez de cliquer de nouveau pour remplir la grille. Que se passe-t-il ? Absolument rien ! L'anti-fraude `isGameOver` arrête le joueur.
- [ ] Cliquez sur "Recommencer". L'UI redevient Bleu sombre pure. Le message texte revient à "Au tour du...".

🏆 **Validation Absolue.**
Ce projet est un Monument du Développement Front-End. Il valide vos acquis en Modélisations Spatialles (Matrices 2D), en algorithme de tri (`For Loop`), et confirme que vous avez compris que **Le HTML n'est que la peinture, Le Javascript en est le Cerveau**.

Vous pouvez utiliser cette base mathématique pour cloner des monstres de logique comme _Tetris_, le _Démineur_, ou un _Morpion_. L'architecture MVC est en vous.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
