---
description: "Phase 1 : Design de la structure globale du jeu. Apprendre à utiliser CSS Grid pour dessiner le plateau exact de 6x7 trous, et comment superposer un pseudo-élément 'Masque Bleu' pour recréer l'illusion du jeu original."
icon: lucide/grid-3x3
tags: ["HTML", "CSS", "GRID", "BOARD", "UI"]
status: stable
---

# Phase 1 : CSS Grid & UI du Board

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le Puissance 4 physique n'est rien d'autre qu'un bloc de plastique bleu percé de 42 trous circulaires. Votre mission est de traduire ce bloc physique en CSS pur sans recourir au Canvas JS afin d'apprendre la puissance architecturale de Grid.

## 1. La Sémantique (Structure HTML)

La force de notre approche, c'est que nous n'allons pas écrire 42 balises `<div>` à la main dans le code HTML. C'est le rôle de l'Ingénieur de la Phase 3 de le faire via une boucle `for` Javascript !

Pour le moment, l'HTML est d'une grande sobriété. Ouvrez `index.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Puissance 4 Électronique</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="game-container">
        
        <!-- EN-TÊTE : Informations Cruciales (Le Tour courant, le Gagnant) -->
        <header class="game-header">
            <h1>Puissance 4</h1>
            <h2 id="status-text">Au tour du Joueur Rouge</h2>
            <button id="reset-btn" class="btn-reset">Recommencer</button>
        </header>

        <!-- ZONE DE JEU (PLATEAU 6 Lignes / 7 Colonnes) -->
        <!-- Il est TOTALEMENT vide. Le JS fabriquera les 42 ronds -->
        <div id="board" class="board">
            
            <!-- EXEMPLE DE CE QUE JS INJECTERA LORS DU DEMARRAGE (Pour tester votre CSS) -->
            <!-- <div class="cell" data-col="0" data-row="0"></div> -->
            <!-- <div class="cell red" data-col="1" data-row="0"></div> -->
            
        </div>

    </main>

    <script src="game.js"></script>
</body>
</html>
```

Remarquez les attributs `data-col` et `data-row`. Ils permettront à notre futur JavaScript de faire le lien parfait entre un rond physique qu'on touche sur l'écran, et les coordonnées abstraites `[0][3]` du tableau.

## 2. Poudrage CSS et Plateau Magique

Créez `style.css`. 
C'est ici qu'on abandonne Flexbox au profit de l'immense puissance de CSS Grid pour générer des tableaux structurels (Row/Col) parfaits.

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

body {
    background-color: #1e293b; /* Arrière plan Nuit (Slate) */
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.game-container {
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

/* LE STATUT DU JEU (UI Text) */
#status-text {
    font-size: 1.5rem;
    padding: 1rem;
    border-radius: 8px;
    background: #334155;
    margin: 1rem 0;
}
/* Classes dynamiques que le JS injectera pour le statut */
.text-red { color: #ef4444; }
.text-yellow { color: #eab308; }

/* LE BOUTON RESET */
.btn-reset {
    background: #3b82f6; /* Bleu neutre */
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
}
.btn-reset:hover { background: #2563eb; }
```

### Le Cerveau CSS : Le Board (Plateau)

L'illusion du Puissance 4 repose sur des ronds évidés sur fond bleu.
Le plus simple en CSS moderne est de donner un fond Bleu au Board Global (`.board`), et de dire que les cellules (`.cell`) sont des ronds blancs par défaut (Le vide). Dès qu'un pion y tombera, ce rond blanc deviendra Jaune ou Rouge.

```css
/* --- LE PLATEAU DE JEU (BOARD) --- */
.board {
    /* Magie pure: On définit 7 colonnes de 60px et 6 lignes de 60px ! */
    display: grid;
    grid-template-columns: repeat(7, 60px);
    grid-template-rows: repeat(6, 60px);
    
    gap: 10px; /* L'espacement plastique bleu entre deux trous */
    background-color: #2563eb; /* Le fond Plastique Bleu Foncé */
    padding: 15px;
    border-radius: 10px;
    
    /* Une petite ombre pour soulever le tout */
    box-shadow: 0 10px 25px rgba(0,0,0, 0.5);
    border: 3px solid #1e40af;
}

/* --- LE TROU (Cellule vide) --- */
.cell {
    background-color: #0f172a; /* Par défaut, la couleur du mur nuit (Arrière plan) */
    border-radius: 50%; /* Arrondi parfait = Un cercle parfait ! */
    cursor: pointer;
    /* Adoucissement de l'apparition des couleurs */
    transition: background-color 0.3s ease, transform 0.1s;
    
    /* Un effet d'ombre interne pour donner du relief au trou ! */
    box-shadow: inset 0 3px 6px rgba(0,0,0, 0.4);
}

.cell:hover {
    /* Indiquer au joueur qu'il peut cliquer dans la colonne */
    background-color: #334155; 
}

/* --- LES ETATS JETONS (Classes que JS injectera dynamiquement) --- */
.cell.red {
    background-color: #ef4444; /* Rouge écarlate */
    box-shadow: inset 0 -3px 6px rgba(0,0,0, 0.3); /* Ombre de pion 3D */
    cursor: default; /* Ce trou est plein */
}

.cell.yellow {
    background-color: #eab308; /* Jaune or */
    box-shadow: inset 0 -3px 6px rgba(0,0,0, 0.3);
    cursor: default;
}

/* Animation lors de la chute d'un Pion */
@keyframes dropAnim {
    0%   { transform: translateY(-300px); opacity: 0; }
    80%  { transform: translateY(10px); }
    100% { transform: translateY(0); opacity: 1; }
}

/* On attache l'animation uniquement si le rond a un pion ! */
.cell.red, .cell.yellow {
    animation: dropAnim 0.4s ease-in-out;
}
```

## Checklist de la Phase 1

- [ ] L'écran de votre navigateur affiche l'entête "Au tour du Joueur...".
- [ ] Sous l'entête, un bloc vide se dessine (S'il n'y pas d'HTML, il n'y a pas de grille visible, c'est normal).
- [ ] Pour vérifier votre CSS : Dé-commentez temporairement (enlevez `<!-- -->`) de la balise `.cell.red` dans le HTML.
- [ ] Le cercle apparait avec la magnifique animation de gravité qui Tombe d'en haut ? Et son relief plastique 3D ? Le CSS est validé !

(Pensez à bien remettre le conteneur du plateau Totalement vide pour la suite). 
Le décor du jeu d'arcade est finalisé. Mais ce jeu est encore aveugle et idiot. Le Cerveau arrive en **Phase 2 : La Gravité Mathématique**.

[Passer à la Phase 2 : Gravité et Moteur de Jeu →](phase2.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
