---
description: "Projet Algorithmique JS : Développement Complet du célèbre jeu Puissance 4. Comprendre les Tableaux Mutlidimensionnels, la CSS Grid Game Board, et de l'algorithme de détection de victoire complexe."
tags: ["JAVASCRIPT", "ALGORITHM", "2D-ARRAY", "LOGIC", "GAME-LOOP"]
---

# Puissance 4

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3 Heures">
</div>

!!! quote "Le Pitch"
    Le client (un réseau de salles d'arcade) souhaite numériser ses classiques. Le Puissance 4 est en apparence un "simple tableau de 6 lignes par 7 colonnes". Mais algorithmiquement, il exige que le développeur Front-End modélise une **Matrice (2D Array)**, applique une gravité (le jeton tombe tout en bas), vérifie les diagonales complexes, et dessine l'UI en Temps Réel. C'est l'essence du game dev en navigateur !

!!! abstract "Objectifs Pédagogiques"
    1.  **State Management Spatial** : Traduire un tableau JavaScript `grid[row][col]` en grille CSS (Divs HTML).
    2.  **La Gravité (Logique Métier)** : Trouver le dernier emplacement libre dans une colonne (Boucle `while` inversée ou `for`).
    3.  **Algorithme de Victoire** : Parcourir des index avec offset `[row+i][col+i]` pour scanner Horizontalement, Verticalement, et surtout Diagonale Nord-Est et Nord-Ouest.
    4.  **UI/UX (Reset Game)** : Réinitialiser un tableau lourd et nettoyer les classes HTML au lieu de recharger grossièrement la page avec `location.reload()`.

## 🏛️ Architecture du Projet

Ce projet est la parfaite illustration du motif algorithmique MVC (Modèle, Vue, Contrôleur).
Contrairement au projet Todolist, le Cerveau (La matrice 6x7) va piloter intensément la Vue (Le Flex/Grid CSS des trous bleus).

```mermaid
graph TD
    A[Joueur Clique (Colonne 3)] --> B(Vérifier si colonne pleine)
    B -->|Oui| C[Ignorer]
    B -->|Non| D(Trouver ligne la plus basse Y)
    D --> E[Mettre à jour: array[Y][3] = Joueur 1]
    E --> F(Dessiner le jeton Rouge dans le DOM CSS)
    F --> G{Vérifier conditions de Victoire (H, V, D)}
    G -->|4 alignés| H[Ecran de Victoire & Bloquer le jeu]
    G -->|Pas fini| I[Donner le Tour au Joueur 2 (Jaune)]
    
    style A fill:#f8fafc,stroke:#475569,stroke-width:2px,color:#000
    style D fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#000
    style E fill:#fca5a5,stroke:#dc2626,stroke-width:2px,color:#000
    style G fill:#93c5fd,stroke:#2563eb,stroke-width:2px,color:#000
    style H fill:#86efac,stroke:#16a34a,stroke-width:2px,color:#000
```

### Concepts Clés Abordés

#### 1. Le 2D Array (Tableau MultiD)
Pour stocker l'information en JS, on utilise un tableau contenant 6 tableaux de 7 cases.
```javascript
const grid = [
  [0, 0, 0, 0, 0, 0, 0], // Ligne 0 (Haut)
  [0, 0, 0, 0, 0, 0, 0], // Ligne 1
  [0, 0, 0, 0, 0, 0, 0], // Ligne 2
  [0, 0, 0, 0, 0, 0, 0], // Ligne 3
  [0, 1, 2, 0, 0, 0, 0], // Ligne 4 (Joueur 1 (Rouge), Joueur 2 (Jaune))
  [0, 1, 1, 2, 0, 0, 0]  // Ligne 5 (Base de la grille, tout en bas)
];
```

#### 2. Séparation de la Grille Logique et Visuelle
L'ordinateur ne "voit" pas les couleurs rouges ou jaunes. Il voit `1` ou `2`. Si `grid[2][5] === 1`, la fonction de rendu (Vue) va se contenter d'ajouter la classe CSS `.token-red` au div correspondant à l'index `[2][5]`. C'est le couplage magique Data -> Interface.

## 🚀 Le Plan de Vol (Phases)

La structure de ce projet se déploie en 4 phases chirurgicales.

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-8">

  <a href="./phase1/" class="block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-md transition-all">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      </div>
      <h3 class="font-bold text-gray-900 m-0">Phase 1 : CSS Grid & UI</h3>
    </div>
    <p class="text-sm text-gray-600 mb-0">Création visuelle du bloc de plastique bleu et des 42 trous ronds pour accueillir les jetons.</p>
  </a>

  <a href="./phase2/" class="block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-md transition-all">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m16 12-4-4-4 4"/><path d="M12 8v8"/></svg>
      </div>
      <h3 class="font-bold text-gray-900 m-0">Phase 2 : Gravité et Tour</h3>
    </div>
    <p class="text-sm text-gray-600 mb-0">Le joueur clique, la boucle cherche le "Plancher" vide, et met à jour le Tableau 2D JS.</p>
  </a>

  <a href="./phase3/" class="block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-md transition-all">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V10"/><path d="m18 20-6-10-6 10"/></svg>
      </div>
      <h3 class="font-bold text-gray-900 m-0">Phase 3 : Synthèse DOM</h3>
    </div>
    <p class="text-sm text-gray-600 mb-0">Colorisation instantanée du rond grâce à l'injection de classe `.red` ou `.yellow` en direct.</p>
  </a>

  <a href="./phase4/" class="block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-md transition-all">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-2 bg-blue-50 text-blue-600 rounded-lg">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4L12 14.01l-3-3"/></svg>
      </div>
      <h3 class="font-bold text-gray-900 m-0">Phase 4 : Algorithme de Victoire</h3>
    </div>
    <p class="text-sm text-gray-600 mb-0">Scanner les 4 directions et gérer le statut de Game Over, du bouton 'Reset' parfait.</p>
  </a>

</div>

## 🛠️ Outils & Prérequis

- Un fichier `game.js`, `style.css` et `index.html`.
- Une excellente maîtrise des boucles FOR imbriquées (Une boucle dans une boucle).
- Savoir moduler des calculs pour ne pas sortir des index mathématiques (Ex: Lire la colonne 8 d'un tableau à 7 cases fait crasher l'app en Javascript "undefined").

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectif de Validation</h4>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Créer un puissant Game Engine sans le moindre rechargement de page.</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le jeu informe (en haut) du "Tour de qui" (Rouge/Jaune).</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Le jeu détecte instantanément 4 jetons consécutifs dans un sens diagonal complexe.</span>
    </li>
  </ul>
</div>
