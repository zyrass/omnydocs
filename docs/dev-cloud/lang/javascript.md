---
description: "Maîtriser JavaScript Vanilla : Fondamentaux avec Jeu Sudoku Complet"
icon: fontawesome/brands/js
tags: ["JAVASCRIPT", "VANILLA", "DOM", "EVENTS", "LOCALSTORAGE", "SUDOKU"]
status: production
---

# JavaScript Vanilla

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="JavaScript ES6+"
  data-time="16-18 heures">
</div>

## Introduction au Projet Sudoku Complet

!!! quote "Analogie pédagogique"
    _Imaginez un site web comme une **maison** : HTML = structure (murs, pièces), CSS = décoration (peinture, meubles), **JavaScript = électricité** (lumières qui s'allument, portes qui s'ouvrent automatiquement). Sans JavaScript, votre site est **statique** (photo fixe). Avec JavaScript, il devient **dynamique** (réagit aux clics, valide formulaires, anime éléments). Alpine.js et Angular sont des **systèmes électriques préfabriqués** qui cachent la complexité. Mais sans maîtriser JavaScript pur, vous ne comprenez pas comment fonctionne `@click` (Alpine) ou `(click)` (Angular). Ce guide vous enseigne JavaScript FONDAMENTAL pour comprendre TOUS les frameworks._

> Ce guide vous accompagne dans la création d'un **Jeu Sudoku complet** en JavaScript Vanilla. Vous construirez un sudoku avec génération automatique, 3 niveaux de difficulté (facile, moyen, difficile), validation en temps réel, timer, système de leaderboard avec localStorage, et authentification simulée (NON sécurisée) avec sessionStorage. CHAQUE concept JavaScript sera expliqué en détail (pourquoi, comment, quand). Ce guide couvre TOUS les fondamentaux JavaScript nécessaires avant d'apprendre Angular, Alpine.js, React, Vue.

!!! info "Pourquoi ce projet ?"
    - **Projet concret** : Jeu utilisable réellement
    - **Algorithme complexe** : Génération + résolution Sudoku
    - **DOM manipulation** : Création dynamique grille 9x9
    - **Events avancés** : Click, input, keyboard
    - **localStorage** : Sauvegarder scores persistants
    - **sessionStorage** : Authentification simulée (+ explications sécurité)
    - **Logique métier** : Validation Sudoku, timer, leaderboard

### Objectifs Pédagogiques

À la fin de ce guide, vous saurez :

- ✅ Variables (var, let, const)
- ✅ Types (string, number, boolean, object, array)
- ✅ Fonctions (déclaration, expression, arrow)
- ✅ Conditions (if, switch, ternaire)
- ✅ Boucles (for, while, forEach, map)
- ✅ Objets et Arrays (méthodes, destructuring)
- ✅ DOM manipulation (querySelector, createElement, addEventListener)
- ✅ Events (click, input, keyboard, custom)
- ✅ localStorage & sessionStorage (différences, sécurité)
- ✅ Algorithmes (génération Sudoku, backtracking)
- ✅ ES6+ (arrow functions, template literals, spread, destructuring)

### Aperçu Jeu Sudoku Final

```
┌───────────────────────────────────────────┐
│ 🎮 SUDOKU GAME                           │
│ ─────────────────────────────────────    │
│ Utilisateur: John Doe        [Déconnexion]│
│                                           │
│ Difficulté: [Facile] [Moyen] [Difficile]│
│                                           │
│ ┌─────────────────┐  Timer: 03:45        │
│ │ 5 3 _ │ _ 7 _ │ _ _ _ │               │
│ │ 6 _ _ │ 1 9 5 │ _ _ _ │               │
│ │ _ 9 8 │ _ _ _ │ _ 6 _ │               │
│ ├───────┼───────┼───────┤               │
│ │ 8 _ _ │ _ 6 _ │ _ _ 3 │               │
│ │ 4 _ _ │ 8 _ 3 │ _ _ 1 │  Score actuel│
│ │ 7 _ _ │ _ 2 _ │ _ _ 6 │  Erreurs: 2  │
│ ├───────┼───────┼───────┤               │
│ │ _ 6 _ │ _ _ _ │ 2 8 _ │               │
│ │ _ _ _ │ 4 1 9 │ _ _ 5 │               │
│ │ _ _ _ │ _ 8 _ │ _ 7 9 │               │
│ └─────────────────┘                      │
│                                           │
│ [Nouvelle Partie] [Valider] [Indice]    │
│                                           │
│ 🏆 LEADERBOARD                           │
│ 1. Alice - 05:23 (Facile)                │
│ 2. Bob - 08:45 (Moyen)                   │
│ 3. John - 12:30 (Difficile)              │
└───────────────────────────────────────────┘
```

### Structure Projet

```
sudoku-game/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── main.js               # Point d'entrée
│   ├── sudoku.js             # Logique Sudoku
│   ├── sudoku-generator.js   # Génération grilles
│   ├── sudoku-solver.js      # Résolution (backtracking)
│   ├── sudoku-validator.js   # Validation
│   ├── ui.js                 # Interface utilisateur
│   ├── timer.js              # Timer jeu
│   ├── storage.js            # localStorage/sessionStorage
│   ├── auth.js               # Authentification simulée
│   └── leaderboard.js        # Leaderboard système
└── README.md
```

### Phases de Développement

| Phase | Titre | Durée | Concepts |
|-------|-------|-------|----------|
| 1 | Fondamentaux JS | 2h | Variables, types, fonctions, conditions |
| 2 | DOM Manipulation | 2h | querySelector, createElement, innerHTML |
| 3 | Events & Interactions | 2h | addEventListener, event object, delegation |
| 4 | Objects & Arrays | 2h | Méthodes, destructuring, spread |
| 5 | Algorithme Sudoku | 3h | Génération, résolution, backtracking |
| 6 | UI Sudoku Complète | 2h | Grille dynamique, validation visuelle |
| 7 | Storage & Timer | 2h | localStorage, sessionStorage, timer |
| 8 | Auth & Leaderboard | 2h | Authentification simulée, scores |

**Durée totale : 17h**

---

## Phase 1 : Fondamentaux JavaScript (2h)

<div class="omny-meta" data-level="🟢 Débutant" data-time="2 heures"></div>

### Objectifs Phase 1

- ✅ Variables (var, let, const)
- ✅ Types primitifs
- ✅ Fonctions (déclaration, expression, arrow)
- ✅ Conditions (if, switch, ternaire)
- ✅ Boucles (for, while, forEach)

### 1.1 Variables : var, let, const

**POURQUOI 3 mots-clés ?**
- `var` : Ancien (ES5), éviter
- `let` : Variable modifiable (ES6+)
- `const` : Constante non réassignable (ES6+)

```javascript
/**
 * VAR (ANCIEN - À ÉVITER)
 * 
 * PROBLÈMES var :
 * 1. Function scope (pas block scope)
 * 2. Hoisting bizarre
 * 3. Peut redéclarer
 */

// Problème 1 : Function scope
if (true) {
    var x = 10;
}
console.log(x); // 10 (accessible hors if !)

// Problème 2 : Hoisting
console.log(y); // undefined (pas d'erreur !)
var y = 20;

// Problème 3 : Redéclaration
var z = 30;
var z = 40; // Pas d'erreur (mauvais)

/**
 * LET (ES6+ - RECOMMANDÉ)
 * 
 * AVANTAGES let :
 * 1. Block scope (limité au bloc {})
 * 2. Pas de hoisting bizarre
 * 3. Pas de redéclaration
 */

// Block scope
if (true) {
    let a = 10;
}
// console.log(a); // ERREUR (a pas accessible)

// Pas de hoisting bizarre
// console.log(b); // ERREUR (ReferenceError)
let b = 20;

// Pas de redéclaration
let c = 30;
// let c = 40; // ERREUR (SyntaxError)

// Réassignation OK
let score = 0;
score = 10; // OK
score += 5; // OK (score = 15)

/**
 * CONST (ES6+ - RECOMMANDÉ)
 * 
 * RÈGLE : Utiliser const par défaut, let si besoin réassigner
 * 
 * AVANTAGES const :
 * 1. Block scope
 * 2. Pas de réassignation (protection)
 * 3. Obligé d'initialiser
 */

const MAX_ERRORS = 3;
// MAX_ERRORS = 5; // ERREUR (TypeError)

// Obligé initialiser
// const MIN_ERRORS; // ERREUR (SyntaxError)

// ATTENTION : const protège référence, PAS contenu objet/array
const player = { name: "John", score: 0 };
player.score = 10; // OK (modifie propriété)
// player = {}; // ERREUR (réassigne référence)

const numbers = [1, 2, 3];
numbers.push(4); // OK (modifie array)
// numbers = []; // ERREUR (réassigne référence)
```

**RÈGLE D'OR :**
1. ✅ **const par défaut** (sauf si besoin réassigner)
2. ✅ **let si réassignation nécessaire**
3. ❌ **JAMAIS var** (ancien, problèmes)

### 1.2 Types Primitifs

```javascript
/**
 * TYPES PRIMITIFS (7 types)
 * 
 * 1. number : Nombres (entiers + décimaux)
 * 2. string : Textes
 * 3. boolean : true/false
 * 4. undefined : Variable non définie
 * 5. null : Absence valeur intentionnelle
 * 6. symbol : Identifiant unique (avancé)
 * 7. bigint : Nombres très grands (avancé)
 */

// NUMBER
let age = 25;                    // Entier
let price = 19.99;               // Décimal
let negative = -10;              // Négatif
let infinity = Infinity;         // Infini
let notANumber = NaN;            // Not a Number

// Opérations mathématiques
let sum = 10 + 5;                // 15 (addition)
let diff = 10 - 5;               // 5 (soustraction)
let product = 10 * 5;            // 50 (multiplication)
let quotient = 10 / 5;           // 2 (division)
let remainder = 10 % 3;          // 1 (modulo = reste division)
let power = 2 ** 3;              // 8 (puissance, 2^3)

// STRING
let firstName = "John";          // Guillemets doubles
let lastName = 'Doe';            // Guillemets simples (équivalent)
let fullName = `${firstName} ${lastName}`; // Template literal (ES6+)

// Concaténation
let greeting = "Hello " + firstName; // "Hello John"
let greeting2 = `Hello ${firstName}`; // "Hello John" (meilleur)

// Méthodes string
let text = "JavaScript";
text.length;                     // 10 (longueur)
text.toUpperCase();              // "JAVASCRIPT"
text.toLowerCase();              // "javascript"
text.includes("Script");         // true (contient)
text.startsWith("Java");         // true (commence par)
text.slice(0, 4);                // "Java" (extraction)
text.replace("Java", "Type");    // "TypeScript"

// BOOLEAN
let isPlaying = true;
let isGameOver = false;

// Comparaisons (retournent boolean)
10 > 5;                          // true
10 < 5;                          // false
10 >= 10;                        // true
10 === 10;                       // true (égalité stricte)
10 !== 5;                        // true (différence stricte)

// ATTENTION : == vs ===
10 == "10";                      // true (conversion implicite)
10 === "10";                     // false (types différents)
// RÈGLE : TOUJOURS utiliser === et !== (strict)

// UNDEFINED
let notDefined;                  // undefined (déclaré, pas assigné)
console.log(notDefined);         // undefined

// NULL
let emptyValue = null;           // null (absence intentionnelle)

// DIFFÉRENCE undefined vs null
// undefined = variable existe, valeur pas assignée
// null = variable existe, valeur explicitement vide

/**
 * TYPEOF : Vérifier type variable
 */
typeof 42;                       // "number"
typeof "Hello";                  // "string"
typeof true;                     // "boolean"
typeof undefined;                // "undefined"
typeof null;                     // "object" (bug historique JS)
typeof { name: "John" };         // "object"
typeof [1, 2, 3];                // "object" (array = objet spécial)

/**
 * CONVERSIONS DE TYPES
 */

// String → Number
let strNumber = "123";
Number(strNumber);               // 123 (fonction Number)
parseInt(strNumber);             // 123 (parse entier)
parseFloat("123.45");            // 123.45 (parse décimal)
+"123";                          // 123 (opérateur unaire +)

// Number → String
let num = 123;
String(num);                     // "123"
num.toString();                  // "123"
`${num}`;                        // "123" (template literal)

// Any → Boolean
Boolean(1);                      // true
Boolean(0);                      // false
Boolean("hello");                // true
Boolean("");                     // false (string vide = false)
Boolean(null);                   // false
Boolean(undefined);              // false

// Valeurs "falsy" (évaluent à false)
// false, 0, "", null, undefined, NaN
// Tout le reste = "truthy" (évalue à true)
```

### 1.3 Fonctions

```javascript
/**
 * FONCTIONS : 3 syntaxes
 * 
 * 1. Déclaration fonction (function declaration)
 * 2. Expression fonction (function expression)
 * 3. Arrow function (ES6+)
 */

// ==========================================
// 1. DÉCLARATION FONCTION
// ==========================================

/**
 * Calcule la somme de 2 nombres
 * 
 * @param {number} a - Premier nombre
 * @param {number} b - Deuxième nombre
 * @returns {number} Somme de a et b
 * 
 * SYNTAXE :
 * function nomFonction(paramètres) {
 *     // Code
 *     return valeur;
 * }
 * 
 * CARACTÉRISTIQUES :
 * - Hoisted (peut appeler avant déclaration)
 * - this dynamique (contexte appelant)
 */
function add(a, b) {
    return a + b;
}

// Appel fonction
const result = add(5, 3); // 8

// Hoisting
console.log(multiply(2, 3)); // 6 (fonctionne !)
function multiply(a, b) {
    return a * b;
}

// ==========================================
// 2. EXPRESSION FONCTION
// ==========================================

/**
 * SYNTAXE :
 * const nomFonction = function(paramètres) {
 *     // Code
 *     return valeur;
 * };
 * 
 * CARACTÉRISTIQUES :
 * - PAS hoisted (doit déclarer avant appeler)
 * - Peut être anonyme
 */
const subtract = function(a, b) {
    return a - b;
};

// Appel
subtract(10, 3); // 7

// PAS hoisted
// console.log(divide(10, 2)); // ERREUR (ReferenceError)
const divide = function(a, b) {
    return a / b;
};

// ==========================================
// 3. ARROW FUNCTION (ES6+)
// ==========================================

/**
 * SYNTAXE :
 * const nomFonction = (paramètres) => {
 *     // Code
 *     return valeur;
 * };
 * 
 * SYNTAXE COURTE (1 expression) :
 * const nomFonction = (paramètres) => expression;
 * 
 * CARACTÉRISTIQUES :
 * - Syntaxe concise
 * - this lexical (contexte parent)
 * - Pas de arguments
 * - RECOMMANDÉ pour fonctions courtes
 */

// Syntaxe complète
const power = (base, exponent) => {
    const result = base ** exponent;
    return result;
};

// Syntaxe courte (return implicite)
const square = (x) => x * x;
const cube = x => x ** 3; // 1 paramètre : () optionnels

// Sans paramètres
const getRandomNumber = () => Math.random();

// COMPARAISON : Fonction normale vs Arrow

// Fonction normale
function greet(name) {
    return `Hello ${name}`;
}

// Arrow équivalente
const greet2 = (name) => `Hello ${name}`;
const greet3 = name => `Hello ${name}`; // Plus court

// ==========================================
// PARAMÈTRES FONCTION
// ==========================================

// Paramètres par défaut (ES6+)
function calculateScore(points = 0, bonus = 10) {
    return points + bonus;
}

calculateScore();           // 10 (utilise défauts)
calculateScore(50);         // 60 (points=50, bonus=10)
calculateScore(50, 20);     // 70 (override défauts)

// Rest parameters (ES6+)
function sum(...numbers) {
    // numbers = array de tous arguments
    return numbers.reduce((total, num) => total + num, 0);
}

sum(1, 2, 3, 4, 5); // 15

// ==========================================
// RETURN
// ==========================================

// Return stoppe fonction
function checkWin(score) {
    if (score >= 100) {
        return "You win!"; // Stoppe ici si score >= 100
    }
    
    return "Keep playing"; // Sinon retourne ça
}

// Return multiple valeurs (via objet/array)
function getPlayerInfo() {
    return {
        name: "John",
        score: 85,
        level: 5
    };
}

const player = getPlayerInfo();
console.log(player.name); // "John"

// Sans return = undefined
function doSomething() {
    console.log("Hello");
    // Pas de return
}

const result2 = doSomething(); // undefined
```

### 1.4 Conditions

```javascript
/**
 * CONDITIONS : 3 syntaxes
 * 
 * 1. if / else if / else
 * 2. switch
 * 3. Ternaire (opérateur ?)
 */

// ==========================================
// 1. IF / ELSE IF / ELSE
// ==========================================

const score = 85;

if (score >= 90) {
    console.log("Excellent!");
} else if (score >= 70) {
    console.log("Good job!");
} else if (score >= 50) {
    console.log("Pass");
} else {
    console.log("Fail");
}

// Opérateurs logiques
// && : ET (AND)
// || : OU (OR)
// ! : NON (NOT)

const age2 = 20;
const hasLicense = true;

// ET (toutes conditions vraies)
if (age2 >= 18 && hasLicense) {
    console.log("Can drive");
}

// OU (au moins 1 condition vraie)
if (age2 < 18 || !hasLicense) {
    console.log("Cannot drive");
}

// NON (inverse)
if (!isGameOver) {
    console.log("Game continues");
}

// ==========================================
// 2. SWITCH
// ==========================================

/**
 * USAGE : Comparer 1 variable à plusieurs valeurs
 * AVANTAGE : Plus lisible que multiples if/else
 */

const difficulty = "medium";

switch (difficulty) {
    case "easy":
        console.log("40 cells removed");
        break; // IMPORTANT : stoppe switch
    
    case "medium":
        console.log("50 cells removed");
        break;
    
    case "hard":
        console.log("60 cells removed");
        break;
    
    default: // Si aucun case correspond
        console.log("Unknown difficulty");
}

// SANS break : "fall-through" (continue cases suivants)
const day = "monday";

switch (day) {
    case "monday":
    case "tuesday":
    case "wednesday":
    case "thursday":
    case "friday":
        console.log("Weekday");
        break;
    
    case "saturday":
    case "sunday":
        console.log("Weekend");
        break;
}

// ==========================================
// 3. TERNAIRE (Opérateur ?)
// ==========================================

/**
 * SYNTAXE : condition ? valeurSiVrai : valeurSiFaux
 * USAGE : If/else court (1 ligne)
 */

const isWinner = score >= 100;
const message = isWinner ? "You win!" : "Keep playing";

// Équivalent if/else
let message2;
if (isWinner) {
    message2 = "You win!";
} else {
    message2 = "Keep playing";
}

// Ternaires imbriqués (éviter si complexe)
const grade = score >= 90 ? "A" : score >= 70 ? "B" : "C";

// Nullish coalescing (??) (ES2020)
const username = null;
const displayName = username ?? "Guest"; // "Guest" (si null/undefined)

// vs OR (||)
const displayName2 = username || "Guest"; // "Guest" (si falsy)

// DIFFÉRENCE : ?? seulement null/undefined, || tous falsy
const count = 0;
const result3 = count ?? 10;  // 0 (count pas null/undefined)
const result4 = count || 10;  // 10 (count falsy)
```

### 1.5 Boucles

```javascript
/**
 * BOUCLES : Répéter code
 * 
 * 1. for : Nombre itérations connu
 * 2. while : Condition tant que vraie
 * 3. do...while : Execute au moins 1 fois
 * 4. for...of : Itérer array (ES6+)
 * 5. for...in : Itérer objet (clés)
 */

// ==========================================
// 1. FOR : Classique
// ==========================================

/**
 * SYNTAXE :
 * for (initialisation; condition; incrémentation) {
 *     // Code répété
 * }
 */

// Compter 0 → 9
for (let i = 0; i < 10; i++) {
    console.log(i);
}

// Décomposition :
// 1. let i = 0 : Initialisation (1 fois)
// 2. i < 10 : Condition (avant chaque itération)
// 3. i++ : Incrémentation (après chaque itération)

// Compter à l'envers
for (let i = 10; i > 0; i--) {
    console.log(i);
}

// Incrément personnalisé
for (let i = 0; i <= 100; i += 10) {
    console.log(i); // 0, 10, 20, ..., 100
}

// ==========================================
// 2. WHILE : Tant que condition vraie
// ==========================================

let attempts = 0;
const maxAttempts = 3;

while (attempts < maxAttempts) {
    console.log(`Attempt ${attempts + 1}`);
    attempts++;
}

// ATTENTION : Boucle infinie si condition toujours vraie
// while (true) {
//     console.log("Forever"); // DANGEREUX
// }

// ==========================================
// 3. DO...WHILE : Execute au moins 1 fois
// ==========================================

let input;

do {
    // input = prompt("Enter number 1-9:");
    input = 5; // Simulation
} while (input < 1 || input > 9);

// DIFFÉRENCE while vs do...while :
// while vérifie AVANT exécuter
// do...while exécute PUIS vérifie

// ==========================================
// 4. FOR...OF : Itérer array (ES6+)
// ==========================================

const numbers2 = [1, 2, 3, 4, 5];

// Ancienne méthode (for classique)
for (let i = 0; i < numbers2.length; i++) {
    console.log(numbers2[i]);
}

// Nouvelle méthode (for...of)
for (const num of numbers2) {
    console.log(num); // Directement valeur
}

// Avec index
for (const [index, num] of numbers2.entries()) {
    console.log(`Index ${index}: ${num}`);
}

// ==========================================
// 5. FOR...IN : Itérer objet (clés)
// ==========================================

const player2 = {
    name: "John",
    score: 85,
    level: 5
};

// Itérer clés
for (const key in player2) {
    console.log(`${key}: ${player2[key]}`);
    // name: John
    // score: 85
    // level: 5
}

// ATTENTION : for...in sur array (déconseillé)
const arr = [10, 20, 30];
for (const index in arr) {
    console.log(index); // "0", "1", "2" (STRING !)
}
// Préférer for...of sur arrays

// ==========================================
// BREAK & CONTINUE
// ==========================================

// BREAK : Sortir boucle
for (let i = 0; i < 10; i++) {
    if (i === 5) {
        break; // Stoppe boucle
    }
    console.log(i); // 0, 1, 2, 3, 4
}

// CONTINUE : Skip itération
for (let i = 0; i < 10; i++) {
    if (i % 2 === 0) {
        continue; // Skip pairs
    }
    console.log(i); // 1, 3, 5, 7, 9
}

// ==========================================
// MÉTHODES ARRAY (alternative boucles)
// ==========================================

const numbers3 = [1, 2, 3, 4, 5];

// forEach : Exécuter fonction sur chaque élément
numbers3.forEach((num, index) => {
    console.log(`Index ${index}: ${num}`);
});

// map : Transformer array
const doubled = numbers3.map(num => num * 2);
// [2, 4, 6, 8, 10]

// filter : Filtrer array
const evens = numbers3.filter(num => num % 2 === 0);
// [2, 4]

// reduce : Réduire array à 1 valeur
const sum2 = numbers3.reduce((total, num) => total + num, 0);
// 15

// find : Trouver 1er élément correspondant
const found = numbers3.find(num => num > 3);
// 4

// some : Au moins 1 élément vrai
const hasEven = numbers3.some(num => num % 2 === 0);
// true

// every : Tous éléments vrais
const allPositive = numbers3.every(num => num > 0);
// true
```

### Checkpoint Phase 1

- ✅ Variables (let, const) comprises
- ✅ Types primitifs maîtrisés
- ✅ Fonctions (déclaration, arrow) créées
- ✅ Conditions (if, switch, ternaire) utilisées
- ✅ Boucles (for, while, forEach) appliquées

---

*Je continue avec les Phases 2-8 dans le prochain message avec DOM, Events, Algorithme Sudoku complet, localStorage, etc...*

## Phase 2 : DOM Manipulation (2h)

<div class="omny-meta" data-level="🟢 Débutant" data-time="2 heures"></div>

### Objectifs Phase 2

- ✅ Comprendre le DOM (Document Object Model)
- ✅ Sélectionner éléments (querySelector, getElementById)
- ✅ Modifier contenu (innerHTML, textContent)
- ✅ Créer éléments (createElement, appendChild)
- ✅ Modifier styles et classes

### 2.1 DOM : Qu'est-ce que c'est ?

**DOM = Document Object Model = Représentation JavaScript de la page HTML**

```
HTML                       DOM (JavaScript)
──────                     ─────────────────
<div id="app">             document
  <h1>Title</h1>             ├── html
  <p>Text</p>                │   ├── head
</div>                       │   └── body
                             │       └── div#app
                             │           ├── h1 ("Title")
                             │           └── p ("Text")
```

**POURQUOI le DOM ?**
- HTML = texte statique
- DOM = objet JavaScript manipulable
- **JavaScript modifie DOM → navigateur met à jour HTML**

```javascript
/**
 * ACCÉDER AU DOCUMENT
 * 
 * document = objet global représentant page HTML
 * window = objet global navigateur
 */

console.log(document); // Affiche structure HTML
console.log(window.document); // Identique (window optionnel)

// Propriétés utiles
document.title;                  // Titre page (<title>)
document.URL;                    // URL actuelle
document.body;                   // <body>
document.head;                   // <head>
document.documentElement;        // <html>
```

### 2.2 Sélectionner Éléments

```javascript
/**
 * MÉTHODES SÉLECTION (du plus moderne au plus ancien)
 * 
 * 1. querySelector() : 1er élément correspondant (CSS selector)
 * 2. querySelectorAll() : Tous éléments correspondants
 * 3. getElementById() : Par ID unique
 * 4. getElementsByClassName() : Par classe (live)
 * 5. getElementsByTagName() : Par balise (live)
 */

// ==========================================
// 1. querySelector() - LE PLUS UTILISÉ
// ==========================================

/**
 * SYNTAXE : document.querySelector(selectorCSS)
 * RETOURNE : 1er élément correspondant OU null
 * 
 * AVANTAGE : Utilise sélecteurs CSS (comme CSS)
 */

// Par ID
const app = document.querySelector('#app');

// Par classe
const button = document.querySelector('.btn-primary');

// Par balise
const heading = document.querySelector('h1');

// Sélecteurs avancés
const firstListItem = document.querySelector('ul li:first-child');
const checkedInput = document.querySelector('input[type="checkbox"]:checked');
const directChild = document.querySelector('.container > .card');

// ==========================================
// 2. querySelectorAll() - TOUS LES ÉLÉMENTS
// ==========================================

/**
 * RETOURNE : NodeList (ressemble array, PAS array)
 * MÉTHODES DISPONIBLES : forEach, entries, keys, values
 * MÉTHODES MANQUANTES : map, filter, reduce (transformer en array)
 */

const allButtons = document.querySelectorAll('.btn');
console.log(allButtons); // NodeList [button, button, button]

// Itérer NodeList
allButtons.forEach((btn, index) => {
    console.log(`Button ${index}:`, btn);
});

// Transformer en array (pour map, filter)
const buttonsArray = Array.from(allButtons);
const buttonTexts = buttonsArray.map(btn => btn.textContent);

// Alternative spread operator
const buttonsArray2 = [...allButtons];

// ==========================================
// 3. getElementById() - PAR ID (ancien)
// ==========================================

/**
 * SYNTAXE : document.getElementById(id)
 * RETOURNE : Élément OU null
 * 
 * ATTENTION : ID sans # (contrairement querySelector)
 */

const sudokuGrid = document.getElementById('sudoku-grid');
// Équivalent : document.querySelector('#sudoku-grid')

// ==========================================
// 4. getElementsByClassName() - PAR CLASSE (ancien)
// ==========================================

/**
 * RETOURNE : HTMLCollection (LIVE = auto-update)
 * DIFFÉRENCE NodeList : Pas de forEach natif
 */

const cells = document.getElementsByClassName('cell');
// HTMLCollection [div.cell, div.cell, ...]

// Itérer HTMLCollection (convertir array)
Array.from(cells).forEach(cell => {
    console.log(cell);
});

// LIVE : Auto-update si DOM change
console.log(cells.length); // 10
document.body.innerHTML += '<div class="cell"></div>';
console.log(cells.length); // 11 (auto-update)

// ==========================================
// 5. getElementsByTagName() - PAR BALISE (ancien)
// ==========================================

const allDivs = document.getElementsByTagName('div');

// ==========================================
// RECOMMANDATION MODERNE
// ==========================================

// ✅ RECOMMANDÉ :
// - querySelector() pour 1 élément
// - querySelectorAll() pour plusieurs

// ❌ ÉVITER (anciens) :
// - getElementById, getElementsByClassName, getElementsByTagName
// SAUF si besoin LIVE collection
```

### 2.3 Lire & Modifier Contenu

```javascript
/**
 * PROPRIÉTÉS CONTENU
 * 
 * 1. textContent : Texte brut (recommandé)
 * 2. innerHTML : HTML (attention XSS)
 * 3. innerText : Texte visible (éviter, lent)
 * 4. value : Valeur input
 */

const heading2 = document.querySelector('h1');

// ==========================================
// 1. textContent - TEXTE BRUT
// ==========================================

// Lire
console.log(heading2.textContent); // "Sudoku Game"

// Modifier
heading2.textContent = "New Title";

// AVANTAGE : Sécurisé (échappe HTML)
heading2.textContent = "<script>alert('XSS')</script>";
// Affiche texte, PAS exécute script

// ==========================================
// 2. innerHTML - HTML COMPLET
// ==========================================

const container = document.querySelector('.container');

// Lire HTML
console.log(container.innerHTML);
// <div>Content</div>

// Modifier HTML
container.innerHTML = '<p class="text">New content</p>';

// DANGER : XSS (Cross-Site Scripting)
const userInput = '<img src=x onerror="alert(\'XSS\')">';
container.innerHTML = userInput; // DANGEREUX (exécute code)

// RÈGLE : JAMAIS innerHTML avec données utilisateur non échappées

// ==========================================
// 3. innerText - TEXTE VISIBLE (éviter)
// ==========================================

// DIFFÉRENCE textContent vs innerText :
// textContent : Tout texte (même caché)
// innerText : Seulement texte visible

const hiddenDiv = document.querySelector('.hidden');
hiddenDiv.textContent; // "Text" (même si display:none)
hiddenDiv.innerText;   // "" (vide si display:none)

// PROBLÈME innerText : LENT (recalcule styles)
// RECOMMANDATION : Utiliser textContent

// ==========================================
// 4. value - VALEUR INPUT
// ==========================================

const input = document.querySelector('#username');

// Lire valeur
console.log(input.value); // "john"

// Modifier valeur
input.value = "John Doe";

// Vider input
input.value = "";

// ATTENTION : value PAS textContent
// input.textContent = "text"; // NE MARCHE PAS
// input.value = "text"; // OK
```

### 2.4 Créer & Insérer Éléments

```javascript
/**
 * CRÉER ÉLÉMENTS
 * 
 * 1. createElement() : Créer élément
 * 2. appendChild() : Ajouter en dernier enfant
 * 3. insertBefore() : Insérer avant élément
 * 4. append() : Moderne (ES6+)
 * 5. remove() : Supprimer élément
 */

// ==========================================
// 1. createElement() - CRÉER ÉLÉMENT
// ==========================================

/**
 * SYNTAXE : document.createElement(tagName)
 * RETOURNE : Élément HTML (EN MÉMOIRE, pas encore dans page)
 */

// Créer div
const newDiv = document.createElement('div');

// Ajouter classe
newDiv.className = 'cell';
// OU
newDiv.classList.add('cell');

// Ajouter ID
newDiv.id = 'cell-0-0';

// Ajouter attributs
newDiv.setAttribute('data-row', '0');
newDiv.setAttribute('data-col', '0');

// Ajouter contenu
newDiv.textContent = '5';

// ==========================================
// 2. appendChild() - AJOUTER ENFANT
// ==========================================

/**
 * SYNTAXE : parent.appendChild(child)
 * EFFET : Ajoute child en DERNIER enfant de parent
 */

const grid = document.querySelector('#grid');
grid.appendChild(newDiv); // Ajoute div dans grid

// Créer plusieurs éléments
for (let i = 0; i < 9; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.textContent = i + 1;
    grid.appendChild(cell);
}

// ==========================================
// 3. insertBefore() - INSÉRER AVANT
// ==========================================

/**
 * SYNTAXE : parent.insertBefore(newNode, referenceNode)
 * EFFET : Insère newNode AVANT referenceNode
 */

const firstCell = grid.firstElementChild;
const newCell = document.createElement('div');
newCell.className = 'cell';
newCell.textContent = '0';

grid.insertBefore(newCell, firstCell); // Insère avant 1ère cell

// ==========================================
// 4. append() - MODERNE (ES6+)
// ==========================================

/**
 * DIFFÉRENCE appendChild vs append :
 * - appendChild : 1 seul élément, retourne élément
 * - append : Plusieurs éléments, texte, retourne undefined
 */

const container2 = document.querySelector('.container');

// append() accepte plusieurs arguments
container2.append(newDiv, "Text", anotherDiv);

// append() accepte texte directement
container2.append("Hello"); // OK
// container2.appendChild("Hello"); // ERREUR

// ==========================================
// 5. remove() - SUPPRIMER ÉLÉMENT
// ==========================================

const cellToRemove = document.querySelector('.cell');

// Moderne (ES6+)
cellToRemove.remove();

// Ancien (avant ES6)
cellToRemove.parentNode.removeChild(cellToRemove);

// Supprimer tous enfants
const container3 = document.querySelector('.container');
container3.innerHTML = ""; // Vide container

// Alternative (mieux pour performance)
while (container3.firstChild) {
    container3.removeChild(container3.firstChild);
}

// ==========================================
// EXEMPLE COMPLET : Créer grille Sudoku 9x9
// ==========================================

function createSudokuGrid() {
    const grid2 = document.querySelector('#sudoku-grid');
    
    // Vider grille
    grid2.innerHTML = "";
    
    // Créer 9x9 = 81 cells
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            // Créer cell
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            // Attributs data pour position
            cell.dataset.row = row;
            cell.dataset.col = col;
            
            // Bordures épaisses pour blocs 3x3
            if (col % 3 === 2 && col < 8) {
                cell.classList.add('border-right');
            }
            if (row % 3 === 2 && row < 8) {
                cell.classList.add('border-bottom');
            }
            
            // Ajouter cell à grid
            grid2.appendChild(cell);
        }
    }
}

// Appel fonction
createSudokuGrid();
```

### 2.5 Modifier Styles & Classes

```javascript
/**
 * MODIFIER STYLES
 * 
 * 1. style : Inline styles (éviter)
 * 2. classList : Classes CSS (recommandé)
 */

const cell2 = document.querySelector('.cell');

// ==========================================
// 1. style - INLINE STYLES (éviter)
// ==========================================

// Modifier 1 propriété
cell2.style.backgroundColor = 'red';
cell2.style.fontSize = '24px';
cell2.style.color = '#fff';

// ATTENTION : Propriétés camelCase
// CSS : background-color
// JS : backgroundColor

// Lire style inline
console.log(cell2.style.backgroundColor); // "red"

// LIMITATION : Seulement styles inline
// Si style défini dans CSS, style.prop retourne ""

// Lire styles computed (tous styles appliqués)
const computedStyle = window.getComputedStyle(cell2);
console.log(computedStyle.backgroundColor); // "rgb(255, 0, 0)"

// PROBLÈME style inline : Mélange CSS et JS (mauvais)
// SOLUTION : Utiliser classes CSS

// ==========================================
// 2. classList - CLASSES CSS (RECOMMANDÉ)
// ==========================================

/**
 * MÉTHODES classList :
 * - add() : Ajouter classe
 * - remove() : Supprimer classe
 * - toggle() : Ajouter/supprimer
 * - contains() : Vérifier présence
 * - replace() : Remplacer classe
 */

// Ajouter classe
cell2.classList.add('selected');
cell2.classList.add('highlight', 'active'); // Plusieurs classes

// Supprimer classe
cell2.classList.remove('selected');

// Toggle (ajouter si absent, supprimer si présent)
cell2.classList.toggle('selected'); // Ajoute
cell2.classList.toggle('selected'); // Supprime

// Vérifier présence
if (cell2.classList.contains('selected')) {
    console.log('Cell is selected');
}

// Remplacer classe
cell2.classList.replace('old-class', 'new-class');

// EXEMPLE : Sélection cell Sudoku
function selectCell(cell) {
    // Désélectionner toutes cells
    document.querySelectorAll('.cell').forEach(c => {
        c.classList.remove('selected');
    });
    
    // Sélectionner cell cliquée
    cell.classList.add('selected');
}

// ==========================================
// className vs classList
// ==========================================

// className : String complète (ancien)
cell2.className = "cell selected"; // Remplace toutes classes

// classList : Manipulation précise (moderne)
cell2.classList.add('selected'); // Ajoute sans supprimer autres
```

### Checkpoint Phase 2

- ✅ DOM compris (arbre JavaScript)
- ✅ Sélection éléments (querySelector)
- ✅ Modification contenu (textContent, innerHTML)
- ✅ Création éléments (createElement, appendChild)
- ✅ Styles et classes (classList)

---

## Phase 3 : Events & Interactions (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 3

- ✅ addEventListener (click, input, keyboard)
- ✅ Event object (target, preventDefault)
- ✅ Event delegation (efficacité)
- ✅ Custom events
- ✅ Event bubbling & capturing

### 3.1 addEventListener Basique

```javascript
/**
 * SYNTAXE : element.addEventListener(event, callback)
 * 
 * event : Type événement (string)
 * callback : Fonction exécutée
 * 
 * ÉVÉNEMENTS COURANTS :
 * - click : Clic souris
 * - input : Changement input
 * - change : Changement select/checkbox
 * - submit : Soumission formulaire
 * - keydown/keyup : Touche clavier
 * - mouseover/mouseout : Survol souris
 */

const button2 = document.querySelector('.btn');

// ==========================================
// CLICK EVENT
// ==========================================

// Syntaxe complète
button2.addEventListener('click', function() {
    console.log('Button clicked!');
});

// Arrow function (moderne)
button2.addEventListener('click', () => {
    console.log('Button clicked!');
});

// Fonction externe (réutilisable)
function handleClick() {
    console.log('Button clicked!');
}
button2.addEventListener('click', handleClick);

// ATTENTION : Ne PAS appeler fonction
// button2.addEventListener('click', handleClick()); // ERREUR
// button2.addEventListener('click', handleClick);   // OK

// ==========================================
// INPUT EVENT
// ==========================================

const input2 = document.querySelector('#username-input');

// Se déclenche à chaque frappe
input2.addEventListener('input', (event) => {
    console.log('Current value:', event.target.value);
});

// DIFFÉRENCE input vs change :
// input : À chaque frappe
// change : Quand focus perdu

input2.addEventListener('change', (event) => {
    console.log('Final value:', event.target.value);
});

// ==========================================
// SUBMIT EVENT
// ==========================================

const form = document.querySelector('#login-form');

form.addEventListener('submit', (event) => {
    // Empêcher rechargement page
    event.preventDefault();
    
    // Récupérer valeurs
    const username = form.username.value;
    const password = form.password.value;
    
    console.log('Username:', username);
    console.log('Password:', password);
});

// ==========================================
// KEYBOARD EVENTS
// ==========================================

const input3 = document.querySelector('#cell-input');

// Touche pressée
input3.addEventListener('keydown', (event) => {
    console.log('Key:', event.key); // Caractère
    console.log('Code:', event.code); // Code touche
    
    // Bloquer lettres (autoriser seulement chiffres)
    if (!/^[1-9]$/.test(event.key) && event.key !== 'Backspace') {
        event.preventDefault(); // Bloque touche
    }
});

// Touche relâchée
input3.addEventListener('keyup', (event) => {
    console.log('Key released:', event.key);
});

// Détection touches spéciales
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault(); // Bloquer Ctrl+S natif
        console.log('Save shortcut');
    }
    
    if (event.key === 'Escape') {
        console.log('Escape pressed');
    }
});
```

### 3.2 Event Object

```javascript
/**
 * EVENT OBJECT : Objet passé automatiquement au callback
 * 
 * PROPRIÉTÉS UTILES :
 * - target : Élément origine événement
 * - currentTarget : Élément avec listener
 * - type : Type événement
 * - preventDefault() : Bloquer action défaut
 * - stopPropagation() : Bloquer propagation
 */

button2.addEventListener('click', (event) => {
    // ==========================================
    // target : Élément CLIQUÉ
    // ==========================================
    console.log(event.target); // <button class="btn">...</button>
    
    // Modifier élément cliqué
    event.target.textContent = 'Clicked!';
    event.target.classList.add('active');
    
    // ==========================================
    // type : Type événement
    // ==========================================
    console.log(event.type); // "click"
    
    // ==========================================
    // preventDefault() : Bloquer action défaut
    // ==========================================
    
    // Exemples actions défaut :
    // - <a> : Navigation
    // - <form> : Soumission
    // - Touche clavier : Insertion caractère
    
    const link = document.querySelector('a');
    link.addEventListener('click', (e) => {
        e.preventDefault(); // Bloque navigation
        console.log('Link clicked, but not followed');
    });
    
    // ==========================================
    // AUTRES PROPRIÉTÉS UTILES
    // ==========================================
    
    // Position souris
    console.log(event.clientX, event.clientY); // Position viewport
    console.log(event.pageX, event.pageY);     // Position page
    
    // Bouton souris
    console.log(event.button); // 0=gauche, 1=milieu, 2=droit
    
    // Touches modificatrices
    console.log(event.ctrlKey);  // Ctrl pressé ?
    console.log(event.shiftKey); // Shift pressé ?
    console.log(event.altKey);   // Alt pressé ?
});
```

### 3.3 Event Delegation (Efficacité)

```javascript
/**
 * EVENT DELEGATION : Écouter parent au lieu d'enfants
 * 
 * POURQUOI :
 * 1. Performance (1 listener au lieu de 81 pour Sudoku)
 * 2. Fonctionne avec éléments créés dynamiquement
 */

// ==========================================
// ❌ MAUVAISE APPROCHE : Listener sur chaque cell
// ==========================================

const cells2 = document.querySelectorAll('.cell');

cells2.forEach(cell => {
    cell.addEventListener('click', () => {
        console.log('Cell clicked');
    });
});

// PROBLÈMES :
// - 81 listeners (performance)
// - Pas d'événement sur cells ajoutées après

// ==========================================
// ✅ BONNE APPROCHE : Event delegation (1 listener parent)
// ==========================================

const grid2 = document.querySelector('#sudoku-grid');

grid2.addEventListener('click', (event) => {
    // Vérifier si cell cliquée
    const cell = event.target.closest('.cell');
    
    if (cell) {
        console.log('Cell clicked');
        console.log('Row:', cell.dataset.row);
        console.log('Col:', cell.dataset.col);
        
        // Sélectionner cell
        selectCell(cell);
    }
});

// AVANTAGES :
// - 1 seul listener (performance)
// - Fonctionne avec cells ajoutées dynamiquement

// ==========================================
// closest() : Trouver ancêtre correspondant
// ==========================================

/**
 * SYNTAXE : element.closest(selector)
 * RETOURNE : 1er ancêtre correspondant (y compris element)
 */

// HTML :
// <div class="grid">
//   <div class="row">
//     <div class="cell">
//       <span>5</span>
//     </div>
//   </div>
// </div>

const span = document.querySelector('span');

span.closest('.cell');  // <div class="cell">
span.closest('.row');   // <div class="row">
span.closest('.grid');  // <div class="grid">

// USAGE : Event delegation sur éléments imbriqués
grid2.addEventListener('click', (event) => {
    const cell = event.target.closest('.cell');
    if (!cell) return; // Click hors cell
    
    // Traiter click cell
});
```

### 3.4 Event Bubbling & Capturing

```javascript
/**
 * EVENT PROPAGATION : Ordre déclenchement events
 * 
 * 3 PHASES :
 * 1. Capturing : Root → Target (descendant)
 * 2. Target : Élément cible
 * 3. Bubbling : Target → Root (remontant)
 * 
 * PAR DÉFAUT : Bubbling phase
 */

// HTML :
// <div class="grandparent">
//   <div class="parent">
//     <div class="child">Click me</div>
//   </div>
// </div>

const grandparent = document.querySelector('.grandparent');
const parent = document.querySelector('.parent');
const child = document.querySelector('.child');

// ==========================================
// BUBBLING (défaut)
// ==========================================

child.addEventListener('click', () => {
    console.log('Child clicked');
});

parent.addEventListener('click', () => {
    console.log('Parent clicked');
});

grandparent.addEventListener('click', () => {
    console.log('Grandparent clicked');
});

// Click sur child affiche :
// Child clicked
// Parent clicked        (bubbling)
// Grandparent clicked   (bubbling)

// ==========================================
// stopPropagation() : Stopper bubbling
// ==========================================

child.addEventListener('click', (event) => {
    event.stopPropagation(); // Stoppe bubbling
    console.log('Child clicked');
});

// Maintenant : Seulement "Child clicked"

// ==========================================
// CAPTURING (rare)
// ==========================================

// 3e paramètre addEventListener : { capture: true }
grandparent.addEventListener('click', () => {
    console.log('Grandparent (capturing)');
}, { capture: true });

parent.addEventListener('click', () => {
    console.log('Parent (capturing)');
}, { capture: true });

child.addEventListener('click', () => {
    console.log('Child clicked');
});

// Click sur child affiche :
// Grandparent (capturing)  (descend)
// Parent (capturing)       (descend)
// Child clicked           (target)
```

### Checkpoint Phase 3

- ✅ addEventListener maîtrisé
- ✅ Event object utilisé
- ✅ Event delegation implémenté
- ✅ Propagation (bubbling/capturing) compris

---

## Phase 4 : Objects & Arrays (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 4

- ✅ Objets (création, propriétés, méthodes)
- ✅ Arrays (méthodes modernes)
- ✅ Destructuring
- ✅ Spread operator
- ✅ JSON (localStorage)

### 4.1 Objets

```javascript
/**
 * OBJET : Collection clé-valeur
 * 
 * SYNTAXE : { key: value, key2: value2 }
 */

// ==========================================
// CRÉATION OBJET
// ==========================================

// Objet littéral (recommandé)
const player3 = {
    name: "John",
    score: 0,
    level: 1,
    isPlaying: false
};

// new Object() (ancien, éviter)
const player4 = new Object();
player4.name = "Jane";

// ==========================================
// ACCÈS PROPRIÉTÉS
// ==========================================

// Dot notation (recommandé)
console.log(player3.name);    // "John"
console.log(player3.score);   // 0

// Bracket notation (si clé dynamique/invalide)
console.log(player3["name"]); // "John"

const prop = "score";
console.log(player3[prop]);   // 0 (variable)

// Clés avec espaces/caractères spéciaux
const obj = {
    "first name": "John",  // Guillemets obligatoires
    "user-id": 123
};
console.log(obj["first name"]); // "John"

// ==========================================
// MODIFIER/AJOUTER PROPRIÉTÉS
// ==========================================

// Modifier
player3.score = 100;

// Ajouter
player3.lives = 3;

// Supprimer
delete player3.lives;

// ==========================================
// MÉTHODES (fonctions dans objet)
// ==========================================

const player5 = {
    name: "John",
    score: 0,
    
    // Méthode
    addPoints(points) {
        this.score += points;
    },
    
    // Getter
    get displayScore() {
        return `Score: ${this.score}`;
    },
    
    // Setter
    set playerName(newName) {
        this.name = newName.toUpperCase();
    }
};

// Appel méthode
player5.addPoints(50);
console.log(player5.score); // 50

// Getter (comme propriété)
console.log(player5.displayScore); // "Score: 50"

// Setter (comme propriété)
player5.playerName = "jane";
console.log(player5.name); // "JANE"

// ==========================================
// THIS : Contexte actuel
// ==========================================

const game = {
    score: 0,
    
    addScore() {
        this.score += 10; // this = game
    },
    
    // Arrow function : this = contexte parent
    addScoreArrow: () => {
        // this.score += 10; // ERREUR (this !== game)
    }
};

// RÈGLE : Méthodes objet → fonction normale (pas arrow)

// ==========================================
// SHORTHAND PROPERTIES (ES6+)
// ==========================================

const name2 = "John";
const score2 = 85;

// Ancien
const player6 = {
    name: name2,
    score: score2
};

// Moderne (si même nom)
const player7 = {
    name2,    // Équivalent name: name
    score2    // Équivalent score: score
};

// ==========================================
// COMPUTED PROPERTY NAMES (ES6+)
// ==========================================

const key = "difficulty";
const value = "medium";

const settings = {
    [key]: value  // difficulty: "medium"
};

// ==========================================
// OBJECT METHODS
// ==========================================

const player8 = {
    name: "John",
    score: 85,
    level: 5
};

// Object.keys() : Array clés
Object.keys(player8); // ["name", "score", "level"]

// Object.values() : Array valeurs
Object.values(player8); // ["John", 85, 5]

// Object.entries() : Array [clé, valeur]
Object.entries(player8);
// [["name", "John"], ["score", 85], ["level", 5]]

// Itérer objet
Object.entries(player8).forEach(([key, value]) => {
    console.log(`${key}: ${value}`);
});

// Object.assign() : Fusionner objets
const defaults = { lives: 3, time: 0 };
const current = { score: 50 };
const merged = Object.assign({}, defaults, current);
// { lives: 3, time: 0, score: 50 }

// Spread operator (moderne)
const merged2 = { ...defaults, ...current };
```

### 4.2 Arrays Modernes

```javascript
/**
 * ARRAY METHODS (ES6+)
 * 
 * TRANSFORMATIONS :
 * - map() : Transformer
 * - filter() : Filtrer
 * - reduce() : Réduire
 * - find() : Trouver 1er
 * - findIndex() : Trouver index
 * - some() : Au moins 1 vrai
 * - every() : Tous vrais
 * 
 * MODIFICATIONS :
 * - push() : Ajouter fin
 * - pop() : Supprimer fin
 * - shift() : Supprimer début
 * - unshift() : Ajouter début
 * - splice() : Insérer/supprimer
 * - slice() : Extraire (immutable)
 */

const numbers4 = [1, 2, 3, 4, 5];

// ==========================================
// map() : TRANSFORMER array
// ==========================================

// Doubler valeurs
const doubled2 = numbers4.map(num => num * 2);
// [2, 4, 6, 8, 10]

// Transformer objets
const players = [
    { name: "John", score: 85 },
    { name: "Jane", score: 92 }
];

const names = players.map(player => player.name);
// ["John", "Jane"]

// ==========================================
// filter() : FILTRER array
// ==========================================

// Nombres pairs
const evens2 = numbers4.filter(num => num % 2 === 0);
// [2, 4]

// Scores > 90
const topPlayers = players.filter(p => p.score > 90);
// [{ name: "Jane", score: 92 }]

// ==========================================
// reduce() : RÉDUIRE à 1 valeur
// ==========================================

/**
 * SYNTAXE : array.reduce((accumulator, current) => {}, initial)
 * 
 * accumulator : Valeur accumulée
 * current : Élément actuel
 * initial : Valeur initiale accumulator
 */

// Somme
const sum3 = numbers4.reduce((total, num) => total + num, 0);
// 15

// Score maximum
const maxScore = players.reduce((max, p) => 
    p.score > max ? p.score : max
, 0);
// 92

// Grouper par propriété
const sudokuCells = [
    { row: 0, col: 0, value: 5 },
    { row: 0, col: 1, value: 3 },
    { row: 1, col: 0, value: 6 }
];

const byRow = sudokuCells.reduce((acc, cell) => {
    if (!acc[cell.row]) acc[cell.row] = [];
    acc[cell.row].push(cell);
    return acc;
}, {});
// { 0: [{...}, {...}], 1: [{...}] }

// ==========================================
// find() : TROUVER 1er élément
// ==========================================

const found2 = players.find(p => p.score > 90);
// { name: "Jane", score: 92 }

// Si pas trouvé
const notFound = players.find(p => p.score > 100);
// undefined

// ==========================================
// findIndex() : TROUVER INDEX
// ==========================================

const index = players.findIndex(p => p.name === "Jane");
// 1

// ==========================================
// some() : AU MOINS 1 vrai
// ==========================================

const hasHighScore = players.some(p => p.score > 90);
// true

// ==========================================
// every() : TOUS vrais
// ==========================================

const allPassed = players.every(p => p.score >= 50);
// true

// ==========================================
// MODIFICATIONS (mutent array original)
// ==========================================

const arr2 = [1, 2, 3];

// push() : Ajouter fin
arr2.push(4); // [1, 2, 3, 4]

// pop() : Supprimer fin
arr2.pop(); // [1, 2, 3]

// shift() : Supprimer début
arr2.shift(); // [2, 3]

// unshift() : Ajouter début
arr2.unshift(0); // [0, 2, 3]

// splice() : Insérer/supprimer
arr2.splice(1, 1); // Supprime index 1
// [0, 3]

arr2.splice(1, 0, 1, 2); // Insère à index 1
// [0, 1, 2, 3]

// ==========================================
// slice() : EXTRAIRE (immutable)
// ==========================================

const arr3 = [1, 2, 3, 4, 5];
const subArr = arr3.slice(1, 4); // [2, 3, 4]
console.log(arr3); // [1, 2, 3, 4, 5] (inchangé)

// ==========================================
// SPREAD OPERATOR (...)
// ==========================================

// Copier array
const original = [1, 2, 3];
const copy = [...original];

// Fusionner arrays
const arr1 = [1, 2];
const arr4 = [3, 4];
const merged3 = [...arr1, ...arr4]; // [1, 2, 3, 4]

// Ajouter éléments
const extended = [...arr1, 5, 6]; // [1, 2, 5, 6]

// ==========================================
// DESTRUCTURING
// ==========================================

// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
console.log(first);  // 1
console.log(second); // 2
console.log(rest);   // [3, 4, 5]

// Object destructuring
const player9 = { name: "John", score: 85, level: 5 };
const { name, score, level } = player9;
console.log(name);  // "John"
console.log(score); // 85

// Renommer
const { name: playerName, score: playerScore } = player9;
console.log(playerName); // "John"

// Valeur par défaut
const { lives = 3 } = player9;
console.log(lives); // 3 (défaut)
```

### 4.3 JSON & localStorage

```javascript
/**
 * JSON : JavaScript Object Notation
 * Format texte pour échanger données
 * 
 * MÉTHODES :
 * - JSON.stringify() : Object → String
 * - JSON.parse() : String → Object
 */

// ==========================================
// JSON.stringify() : Object → String
// ==========================================

const player10 = {
    name: "John",
    score: 85,
    level: 5
};

const jsonString = JSON.stringify(player10);
console.log(jsonString);
// '{"name":"John","score":85,"level":5}'

// localStorage accepte seulement strings
localStorage.setItem('player', jsonString);

// ==========================================
// JSON.parse() : String → Object
// ==========================================

const storedJson = localStorage.getItem('player');
const parsedPlayer = JSON.parse(storedJson);
console.log(parsedPlayer);
// { name: "John", score: 85, level: 5 }

// ==========================================
// localStorage COMPLET (Phase 7)
// ==========================================

// Sera détaillé Phase 7 avec :
// - Différence localStorage vs sessionStorage
// - Sécurité (DANGER authentification)
// - Leaderboard persistant
```

### Checkpoint Phase 4

- ✅ Objets maîtrisés (propriétés, méthodes)
- ✅ Arrays modernes (map, filter, reduce)
- ✅ Destructuring & spread
- ✅ JSON (stringify, parse)

---

*Je continue avec les Phases 5-8 dans le prochain message : Algorithme Sudoku complet, UI, localStorage, authentification...*

## Phase 5 : Algorithme Sudoku (3h)

<div class="omny-meta" data-level="🔴 Avancé" data-time="3 heures"></div>

### Objectifs Phase 5

- ✅ Comprendre règles Sudoku
- ✅ Générer grille valide
- ✅ Résolution backtracking (récursion)
- ✅ Validation (lignes, colonnes, blocs 3x3)
- ✅ Niveaux difficulté (40, 50, 60 cells retirées)

### 5.1 Règles Sudoku

**RÈGLES FONDAMENTALES :**
1. Grille 9x9 (81 cells)
2. 9 blocs 3x3
3. Chaque ligne : chiffres 1-9 uniques
4. Chaque colonne : chiffres 1-9 uniques
5. Chaque bloc 3x3 : chiffres 1-9 uniques

```
┌─────────────────┐
│ 5 3 _ │ _ 7 _ │ _ _ _ │  Règles :
│ 6 _ _ │ 1 9 5 │ _ _ _ │  - Ligne 1 : Pas de doublon 5,3,7
│ _ 9 8 │ _ _ _ │ _ 6 _ │  - Colonne 1 : Pas de doublon 5,6
├───────┼───────┼───────┤  - Bloc haut-gauche : Pas doublon 5,3,6,9,8
│ 8 _ _ │ _ 6 _ │ _ _ 3 │
│ 4 _ _ │ 8 _ 3 │ _ _ 1 │
│ 7 _ _ │ _ 2 _ │ _ _ 6 │
├───────┼───────┼───────┤
│ _ 6 _ │ _ _ _ │ 2 8 _ │
│ _ _ _ │ 4 1 9 │ _ _ 5 │
│ _ _ _ │ _ 8 _ │ _ 7 9 │
└─────────────────┘
```

### 5.2 Structure Données Sudoku

**Fichier :** `js/sudoku.js`

```javascript
/**
 * STRUCTURE SUDOKU
 * 
 * REPRÉSENTATION : Array 2D (9x9)
 * board[row][col] = valeur (0 = vide, 1-9 = chiffre)
 * 
 * POURQUOI Array 2D ?
 * - Accès direct : board[row][col]
 * - Facile itérer lignes/colonnes
 * - Intuitif (correspond grille visuelle)
 */

class Sudoku {
    constructor() {
        /**
         * Créer grille vide 9x9
         * 0 = cell vide
         */
        this.board = this.createEmptyBoard();
        
        /**
         * Grille solution (complète)
         * Pour vérifier validité saisies utilisateur
         */
        this.solution = null;
        
        /**
         * Grille initiale (avec cells retirées)
         * Pour reset partie
         */
        this.initial = null;
    }
    
    /**
     * Créer grille vide 9x9
     * 
     * @returns {number[][]} Grille 9x9 remplie de 0
     * 
     * POURQUOI Array.from() ?
     * new Array(9).fill([]) créerait 9 références au MÊME array
     * Array.from() crée 9 arrays DIFFÉRENTS
     */
    createEmptyBoard() {
        return Array.from({ length: 9 }, () => Array(9).fill(0));
    }
    
    /**
     * Copier grille
     * 
     * @param {number[][]} board - Grille à copier
     * @returns {number[][]} Copie profonde
     * 
     * POURQUOI copie profonde ?
     * [...board] copierait seulement 1er niveau (shallow)
     * On doit copier aussi arrays internes
     */
    copyBoard(board) {
        return board.map(row => [...row]);
    }
    
    /**
     * Afficher grille (debug)
     */
    printBoard(board = this.board) {
        console.log('\n');
        for (let row = 0; row < 9; row++) {
            if (row % 3 === 0 && row !== 0) {
                console.log('------+-------+------');
            }
            
            let rowStr = '';
            for (let col = 0; col < 9; col++) {
                if (col % 3 === 0 && col !== 0) {
                    rowStr += '| ';
                }
                rowStr += board[row][col] === 0 ? '_ ' : board[row][col] + ' ';
            }
            console.log(rowStr);
        }
        console.log('\n');
    }
}
```

### 5.3 Validation Sudoku

**Fichier :** `js/sudoku-validator.js`

```javascript
/**
 * VALIDATION SUDOKU
 * 
 * RÈGLES :
 * 1. Ligne valide : Pas de doublons 1-9
 * 2. Colonne valide : Pas de doublons 1-9
 * 3. Bloc 3x3 valide : Pas de doublons 1-9
 */

class SudokuValidator {
    /**
     * Vérifier si nombre valide à position
     * 
     * @param {number[][]} board - Grille Sudoku
     * @param {number} row - Ligne (0-8)
     * @param {number} col - Colonne (0-8)
     * @param {number} num - Nombre à tester (1-9)
     * @returns {boolean} true si valide
     * 
     * LOGIQUE :
     * Valide SI :
     * - Pas dans ligne
     * - Pas dans colonne
     * - Pas dans bloc 3x3
     */
    static isValid(board, row, col, num) {
        // Vérifier ligne
        if (!this.isValidInRow(board, row, num)) {
            return false;
        }
        
        // Vérifier colonne
        if (!this.isValidInColumn(board, col, num)) {
            return false;
        }
        
        // Vérifier bloc 3x3
        if (!this.isValidInBox(board, row, col, num)) {
            return false;
        }
        
        return true;
    }
    
    /**
     * Vérifier ligne
     * 
     * @param {number[][]} board
     * @param {number} row - Ligne à vérifier
     * @param {number} num - Nombre cherché
     * @returns {boolean} true si num PAS dans ligne
     * 
     * LOGIQUE :
     * Parcourir toutes colonnes de la ligne
     * Si num trouvé → invalide
     */
    static isValidInRow(board, row, num) {
        for (let col = 0; col < 9; col++) {
            if (board[row][col] === num) {
                return false; // Doublon trouvé
            }
        }
        return true; // Pas de doublon
    }
    
    /**
     * Vérifier colonne
     * 
     * @param {number[][]} board
     * @param {number} col - Colonne à vérifier
     * @param {number} num - Nombre cherché
     * @returns {boolean} true si num PAS dans colonne
     * 
     * LOGIQUE :
     * Parcourir toutes lignes de la colonne
     * Si num trouvé → invalide
     */
    static isValidInColumn(board, col, num) {
        for (let row = 0; row < 9; row++) {
            if (board[row][col] === num) {
                return false; // Doublon trouvé
            }
        }
        return true; // Pas de doublon
    }
    
    /**
     * Vérifier bloc 3x3
     * 
     * @param {number[][]} board
     * @param {number} row - Ligne cell
     * @param {number} col - Colonne cell
     * @param {number} num - Nombre cherché
     * @returns {boolean} true si num PAS dans bloc 3x3
     * 
     * LOGIQUE :
     * 1. Trouver coin haut-gauche bloc 3x3
     * 2. Parcourir 3x3 cases du bloc
     * 3. Si num trouvé → invalide
     * 
     * CALCUL coin bloc :
     * row 4 → bloc commence à 3 (4 - 4%3 = 3)
     * col 7 → bloc commence à 6 (7 - 7%3 = 6)
     * 
     * POURQUOI Math.floor(row / 3) * 3 ?
     * row 0,1,2 → bloc 0 (0*3 = 0)
     * row 3,4,5 → bloc 1 (1*3 = 3)
     * row 6,7,8 → bloc 2 (2*3 = 6)
     */
    static isValidInBox(board, row, col, num) {
        // Trouver coin haut-gauche bloc 3x3
        const boxStartRow = Math.floor(row / 3) * 3;
        const boxStartCol = Math.floor(col / 3) * 3;
        
        // Parcourir bloc 3x3
        for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
                const currentRow = boxStartRow + r;
                const currentCol = boxStartCol + c;
                
                if (board[currentRow][currentCol] === num) {
                    return false; // Doublon trouvé
                }
            }
        }
        
        return true; // Pas de doublon
    }
    
    /**
     * Vérifier si grille complète et valide
     * 
     * @param {number[][]} board
     * @returns {boolean} true si résolu
     * 
     * LOGIQUE :
     * Grille complète SI :
     * - Aucune cell vide (0)
     * - Toutes lignes valides
     * - Toutes colonnes valides
     * - Tous blocs 3x3 valides
     */
    static isSolved(board) {
        // Vérifier cells vides
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (board[row][col] === 0) {
                    return false; // Cell vide trouvée
                }
            }
        }
        
        // Vérifier validité (lignes, colonnes, blocs)
        for (let i = 0; i < 9; i++) {
            if (!this.isRowValid(board, i) ||
                !this.isColumnValid(board, i) ||
                !this.isBoxValidByIndex(board, i)) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Vérifier ligne complète (pas de doublons)
     */
    static isRowValid(board, row) {
        const seen = new Set();
        for (let col = 0; col < 9; col++) {
            const num = board[row][col];
            if (num !== 0) {
                if (seen.has(num)) return false;
                seen.add(num);
            }
        }
        return true;
    }
    
    /**
     * Vérifier colonne complète
     */
    static isColumnValid(board, col) {
        const seen = new Set();
        for (let row = 0; row < 9; row++) {
            const num = board[row][col];
            if (num !== 0) {
                if (seen.has(num)) return false;
                seen.add(num);
            }
        }
        return true;
    }
    
    /**
     * Vérifier bloc 3x3 par index (0-8)
     */
    static isBoxValidByIndex(board, boxIndex) {
        const boxStartRow = Math.floor(boxIndex / 3) * 3;
        const boxStartCol = (boxIndex % 3) * 3;
        
        const seen = new Set();
        for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
                const num = board[boxStartRow + r][boxStartCol + c];
                if (num !== 0) {
                    if (seen.has(num)) return false;
                    seen.add(num);
                }
            }
        }
        return true;
    }
}
```

### 5.4 Résolution Sudoku (Backtracking)

**Fichier :** `js/sudoku-solver.js`

```javascript
/**
 * RÉSOLUTION SUDOKU : BACKTRACKING
 * 
 * ALGORITHME BACKTRACKING :
 * Technique récursive pour trouver solution
 * 
 * PRINCIPE :
 * 1. Trouver cell vide
 * 2. Essayer chiffres 1-9
 * 3. Si valide, placer et continuer
 * 4. Si bloqué, REVENIR en arrière (backtrack)
 * 5. Essayer autre chiffre
 * 
 * ANALOGIE :
 * Labyrinthe : Avancer, si mur → reculer, essayer autre chemin
 */

class SudokuSolver {
    /**
     * Résoudre Sudoku (backtracking)
     * 
     * @param {number[][]} board - Grille à résoudre
     * @returns {boolean} true si solution trouvée
     * 
     * COMPLEXITÉ :
     * Pire cas : O(9^m) où m = nombre cells vides
     * Pratique : Beaucoup plus rapide (contraintes réduisent espace)
     * 
     * RÉCURSION :
     * Fonction s'appelle elle-même jusqu'à :
     * - Solution trouvée (return true)
     * - Impossible résoudre (return false)
     */
    static solve(board) {
        // Trouver cell vide
        const emptyCell = this.findEmptyCell(board);
        
        // Si pas de cell vide → grille complète
        if (!emptyCell) {
            return true; // Solution trouvée !
        }
        
        const [row, col] = emptyCell;
        
        // Essayer chiffres 1-9
        for (let num = 1; num <= 9; num++) {
            // Vérifier si num valide à cette position
            if (SudokuValidator.isValid(board, row, col, num)) {
                // Placer num (essai)
                board[row][col] = num;
                
                // RÉCURSION : Continuer avec num placé
                if (this.solve(board)) {
                    return true; // Solution trouvée !
                }
                
                // BACKTRACKING : num ne mène pas à solution
                // Retirer num et essayer suivant
                board[row][col] = 0;
            }
        }
        
        // Aucun num valide → backtrack
        return false;
    }
    
    /**
     * Trouver première cell vide
     * 
     * @param {number[][]} board
     * @returns {[number, number] | null} [row, col] ou null
     * 
     * POURQUOI première cell ?
     * Stratégie simple : Ordre ligne par ligne
     * 
     * OPTIMISATIONS POSSIBLES :
     * - MRV (Minimum Remaining Values) : Cell avec moins de possibilités
     * - Degree heuristic : Cell impactant plus de cells
     */
    static findEmptyCell(board) {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (board[row][col] === 0) {
                    return [row, col];
                }
            }
        }
        return null; // Pas de cell vide
    }
    
    /**
     * Compter solutions possibles
     * 
     * @param {number[][]} board
     * @param {number} limit - Limite comptage (performance)
     * @returns {number} Nombre solutions
     * 
     * USAGE :
     * Vérifier grille a solution UNIQUE
     * countSolutions(board, 2) :
     * - 0 : Pas de solution
     * - 1 : Solution unique (bon)
     * - 2+ : Multiples solutions (mauvais pour Sudoku)
     */
    static countSolutions(board, limit = 2) {
        let count = 0;
        
        const backtrack = (board) => {
            if (count >= limit) return; // Stop si limite atteinte
            
            const emptyCell = this.findEmptyCell(board);
            
            if (!emptyCell) {
                count++; // Solution trouvée
                return;
            }
            
            const [row, col] = emptyCell;
            
            for (let num = 1; num <= 9; num++) {
                if (SudokuValidator.isValid(board, row, col, num)) {
                    board[row][col] = num;
                    backtrack(board);
                    board[row][col] = 0;
                }
            }
        };
        
        // Copier board (éviter mutation)
        const boardCopy = board.map(row => [...row]);
        backtrack(boardCopy);
        
        return count;
    }
}
```

### 5.5 Génération Sudoku

**Fichier :** `js/sudoku-generator.js`

```javascript
/**
 * GÉNÉRATION SUDOKU
 * 
 * ALGORITHME :
 * 1. Créer grille vide
 * 2. Remplir diagonales 3x3 (indépendantes)
 * 3. Résoudre reste (backtracking)
 * 4. Retirer cells selon difficulté
 * 5. Vérifier solution unique
 * 
 * POURQUOI diagonales d'abord ?
 * Blocs diagonaux sont INDÉPENDANTS (aucun partage ligne/col)
 * → Remplissage aléatoire direct (pas de contraintes entre eux)
 */

class SudokuGenerator {
    /**
     * Générer Sudoku complet
     * 
     * @param {string} difficulty - "easy", "medium", "hard"
     * @returns {Object} { board, solution }
     * 
     * DIFFICULTÉS :
     * - easy : 40 cells retirées
     * - medium : 50 cells retirées
     * - hard : 60 cells retirées
     */
    static generate(difficulty = 'medium') {
        // 1. Créer grille vide
        const board = Array.from({ length: 9 }, () => Array(9).fill(0));
        
        // 2. Remplir diagonales 3x3
        this.fillDiagonalBoxes(board);
        
        // 3. Résoudre reste
        SudokuSolver.solve(board);
        
        // 4. Sauvegarder solution
        const solution = board.map(row => [...row]);
        
        // 5. Retirer cells selon difficulté
        const cellsToRemove = this.getCellsToRemove(difficulty);
        this.removeCells(board, cellsToRemove);
        
        return {
            board,      // Grille avec cells retirées
            solution    // Grille complète
        };
    }
    
    /**
     * Remplir blocs diagonaux 3x3
     * 
     * @param {number[][]} board
     * 
     * BLOCS DIAGONAUX (3 blocs) :
     * [0,0] [1,1] [2,2]
     * 
     * ┌─────────────────┐
     * │ X X X │ . . . │ . . . │
     * │ X X X │ . . . │ . . . │
     * │ X X X │ . . . │ . . . │
     * ├───────┼───────┼───────┤
     * │ . . . │ Y Y Y │ . . . │
     * │ . . . │ Y Y Y │ . . . │
     * │ . . . │ Y Y Y │ . . . │
     * ├───────┼───────┼───────┤
     * │ . . . │ . . . │ Z Z Z │
     * │ . . . │ . . . │ Z Z Z │
     * │ . . . │ . . . │ Z Z Z │
     * └─────────────────┘
     * 
     * X, Y, Z sont INDÉPENDANTS (pas même ligne/col)
     */
    static fillDiagonalBoxes(board) {
        // Remplir 3 blocs diagonaux
        for (let box = 0; box < 3; box++) {
            this.fillBox(board, box * 3, box * 3);
        }
    }
    
    /**
     * Remplir bloc 3x3 aléatoirement
     * 
     * @param {number[][]} board
     * @param {number} startRow - Ligne début bloc
     * @param {number} startCol - Colonne début bloc
     * 
     * LOGIQUE :
     * 1. Créer array [1,2,3,4,5,6,7,8,9]
     * 2. Mélanger aléatoirement (shuffle)
     * 3. Remplir bloc 3x3 avec array mélangé
     */
    static fillBox(board, startRow, startCol) {
        // Créer array 1-9
        const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        
        // Mélanger (Fisher-Yates shuffle)
        this.shuffleArray(numbers);
        
        // Remplir bloc 3x3
        let index = 0;
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 3; col++) {
                board[startRow + row][startCol + col] = numbers[index];
                index++;
            }
        }
    }
    
    /**
     * Mélanger array aléatoirement (Fisher-Yates)
     * 
     * @param {Array} array - Array à mélanger (muté)
     * 
     * ALGORITHME FISHER-YATES :
     * Pour chaque position i (fin → début) :
     * - Choisir index aléatoire j entre 0 et i
     * - Échanger array[i] et array[j]
     * 
     * POURQUOI Fisher-Yates ?
     * Garantit TOUTES permutations équiprobables
     * Complexité O(n) - optimal
     */
    static shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            // Random index entre 0 et i
            const j = Math.floor(Math.random() * (i + 1));
            
            // Échanger array[i] et array[j]
            [array[i], array[j]] = [array[j], array[i]];
        }
    }
    
    /**
     * Nombre cells à retirer selon difficulté
     * 
     * @param {string} difficulty
     * @returns {number} Nombre cells à retirer
     * 
     * NIVEAUX :
     * - easy : 40 cells (49% vides)
     * - medium : 50 cells (62% vides)
     * - hard : 60 cells (74% vides)
     * 
     * LIMITE : Maximum ~64 cells
     * Au-delà : Multiples solutions possibles
     */
    static getCellsToRemove(difficulty) {
        const levels = {
            easy: 40,
            medium: 50,
            hard: 60
        };
        
        return levels[difficulty] || levels.medium;
    }
    
    /**
     * Retirer cells de grille (créer puzzle)
     * 
     * @param {number[][]} board - Grille complète
     * @param {number} count - Nombre cells à retirer
     * 
     * ALGORITHME :
     * 1. Choisir cell aléatoire non vide
     * 2. Sauvegarder valeur
     * 3. Retirer valeur (mettre 0)
     * 4. Vérifier solution UNIQUE
     * 5. Si unique → garder retiré, sinon → restaurer
     * 6. Répéter jusqu'à count cells retirées
     * 
     * POURQUOI vérifier solution unique ?
     * Sudoku valide = 1 seule solution
     * Plusieurs solutions = puzzle ambigu (mauvais)
     */
    static removeCells(board, count) {
        let removed = 0;
        const attempts = count * 3; // Limite tentatives
        let attemptCount = 0;
        
        while (removed < count && attemptCount < attempts) {
            attemptCount++;
            
            // Choisir cell aléatoire
            const row = Math.floor(Math.random() * 9);
            const col = Math.floor(Math.random() * 9);
            
            // Skip si déjà vide
            if (board[row][col] === 0) {
                continue;
            }
            
            // Sauvegarder valeur
            const backup = board[row][col];
            
            // Retirer valeur
            board[row][col] = 0;
            
            // Vérifier solution unique
            const solutions = SudokuSolver.countSolutions(board, 2);
            
            if (solutions === 1) {
                // Solution unique → OK
                removed++;
            } else {
                // Plusieurs solutions → restaurer
                board[row][col] = backup;
            }
        }
        
        // Si pas assez retiré, forcer (accepter multiples solutions)
        if (removed < count) {
            console.warn(`Only ${removed}/${count} cells removed with unique solution`);
        }
    }
}
```

### 5.6 Intégration Sudoku Class

**Fichier :** `js/sudoku.js` (suite)

```javascript
/**
 * SUDOKU CLASS COMPLÈTE
 * Intègre génération, validation, résolution
 */

class Sudoku {
    constructor() {
        this.board = this.createEmptyBoard();
        this.solution = null;
        this.initial = null;
        this.difficulty = 'medium';
    }
    
    // ... méthodes précédentes ...
    
    /**
     * Nouvelle partie
     * 
     * @param {string} difficulty - "easy", "medium", "hard"
     * 
     * LOGIQUE :
     * 1. Générer grille
     * 2. Sauvegarder solution
     * 3. Sauvegarder grille initiale (reset)
     */
    newGame(difficulty = 'medium') {
        this.difficulty = difficulty;
        
        // Générer Sudoku
        const { board, solution } = SudokuGenerator.generate(difficulty);
        
        // Sauvegarder
        this.board = board;
        this.solution = solution;
        this.initial = this.copyBoard(board);
        
        console.log('New game generated:');
        this.printBoard();
    }
    
    /**
     * Placer nombre
     * 
     * @param {number} row
     * @param {number} col
     * @param {number} num
     * @returns {boolean} true si placement valide
     */
    placeNumber(row, col, num) {
        // Vérifier cell modifiable
        if (this.initial[row][col] !== 0) {
            return false; // Cell initiale (non modifiable)
        }
        
        // Placer nombre
        this.board[row][col] = num;
        
        // Vérifier si correct
        return num === this.solution[row][col];
    }
    
    /**
     * Vérifier si gagné
     */
    isComplete() {
        return SudokuValidator.isSolved(this.board);
    }
    
    /**
     * Obtenir indice
     * 
     * @returns {Object|null} { row, col, value } ou null
     * 
     * LOGIQUE :
     * Trouver cell vide aléatoire
     * Retourner sa valeur solution
     */
    getHint() {
        const emptyCells = [];
        
        // Trouver toutes cells vides
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (this.board[row][col] === 0) {
                    emptyCells.push({ row, col });
                }
            }
        }
        
        if (emptyCells.length === 0) {
            return null; // Pas de cell vide
        }
        
        // Choisir cell aléatoire
        const randomCell = emptyCells[
            Math.floor(Math.random() * emptyCells.length)
        ];
        
        return {
            row: randomCell.row,
            col: randomCell.col,
            value: this.solution[randomCell.row][randomCell.col]
        };
    }
    
    /**
     * Reset grille (état initial)
     */
    reset() {
        this.board = this.copyBoard(this.initial);
    }
}

// Export (si modules ES6)
// export { Sudoku, SudokuValidator, SudokuSolver, SudokuGenerator };
```

### Checkpoint Phase 5

- ✅ Règles Sudoku comprises
- ✅ Validation (lignes, colonnes, blocs) implémentée
- ✅ Backtracking algorithm maîtrisé
- ✅ Génération grille complète
- ✅ Niveaux difficulté créés

---

*Je continue avec les Phases 6-8 dans le prochain message : UI complète, localStorage, authentification simulée...*

## Phase 6 : UI Sudoku Complète (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 6

- ✅ Créer grille 9x9 dynamique
- ✅ Sélection cell + highlight
- ✅ Input clavier (1-9, Backspace, Arrow keys)
- ✅ Validation visuelle (vert/rouge)
- ✅ Compteur erreurs
- ✅ Boutons contrôle (Nouvelle partie, Valider, Indice)

### 6.1 HTML Structure

**Fichier :** `index.html`

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sudoku Game - JavaScript Vanilla</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <h1>🎮 Sudoku Game</h1>
        <div class="user-info" id="user-info">
            <span id="username-display"></span>
            <button class="btn-logout" id="btn-logout">Déconnexion</button>
        </div>
    </header>
    
    <!-- Main Game -->
    <main class="container">
        <!-- Difficulty Selection -->
        <section class="difficulty-section">
            <h3>Difficulté :</h3>
            <div class="difficulty-buttons">
                <button class="btn-difficulty active" data-difficulty="easy">
                    Facile
                </button>
                <button class="btn-difficulty" data-difficulty="medium">
                    Moyen
                </button>
                <button class="btn-difficulty" data-difficulty="hard">
                    Difficile
                </button>
            </div>
        </section>
        
        <!-- Game Info -->
        <div class="game-info">
            <div class="timer">
                <span class="label">Timer:</span>
                <span id="timer-display">00:00</span>
            </div>
            <div class="errors">
                <span class="label">Erreurs:</span>
                <span id="errors-display">0</span>
            </div>
        </div>
        
        <!-- Sudoku Grid -->
        <div class="sudoku-grid" id="sudoku-grid">
            <!-- 81 cells générées dynamiquement -->
        </div>
        
        <!-- Controls -->
        <div class="controls">
            <button class="btn btn-primary" id="btn-new-game">
                Nouvelle Partie
            </button>
            <button class="btn btn-secondary" id="btn-validate">
                Valider
            </button>
            <button class="btn btn-info" id="btn-hint">
                Indice
            </button>
        </div>
        
        <!-- Leaderboard -->
        <section class="leaderboard" id="leaderboard">
            <h3>🏆 Leaderboard</h3>
            <div id="leaderboard-list"></div>
        </section>
    </main>
    
    <!-- Login Modal -->
    <div class="modal" id="login-modal">
        <div class="modal-content">
            <h2>Connexion</h2>
            
            <!-- ⚠️ WARNING SECURITY -->
            <div class="security-warning">
                <strong>⚠️ ATTENTION SÉCURITÉ :</strong>
                <p>
                    Cette authentification est simulée et <strong>NON SÉCURISÉE</strong>.
                    Utilise sessionStorage (visible dans DevTools).
                    <strong>JAMAIS</strong> utiliser cette méthode en production.
                </p>
            </div>
            
            <form id="login-form">
                <div class="form-group">
                    <label for="username">Nom d'utilisateur</label>
                    <input 
                        type="text" 
                        id="username" 
                        required 
                        placeholder="John Doe"
                    >
                </div>
                
                <div class="form-group">
                    <label for="password">Mot de passe (simulé)</label>
                    <input 
                        type="password" 
                        id="password" 
                        required 
                        placeholder="Pas de vérification réelle"
                    >
                </div>
                
                <button type="submit" class="btn btn-primary">
                    Se connecter
                </button>
            </form>
        </div>
    </div>
    
    <!-- JavaScript -->
    <script src="js/sudoku.js"></script>
    <script src="js/sudoku-validator.js"></script>
    <script src="js/sudoku-solver.js"></script>
    <script src="js/sudoku-generator.js"></script>
    <script src="js/ui.js"></script>
    <script src="js/timer.js"></script>
    <script src="js/storage.js"></script>
    <script src="js/auth.js"></script>
    <script src="js/leaderboard.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
```

### 6.2 UI Controller

**Fichier :** `js/ui.js`

```javascript
/**
 * UI CONTROLLER
 * Gère interface utilisateur Sudoku
 */

class SudokuUI {
    constructor() {
        this.grid = document.getElementById('sudoku-grid');
        this.selectedCell = null;
        this.errorCount = 0;
        
        // Références éléments
        this.timerDisplay = document.getElementById('timer-display');
        this.errorsDisplay = document.getElementById('errors-display');
    }
    
    /**
     * Créer grille 9x9 (81 cells)
     * 
     * @param {number[][]} board - Grille Sudoku
     * @param {number[][]} initial - Grille initiale (cells fixes)
     * 
     * STRUCTURE DOM :
     * <div class="sudoku-grid">
     *   <div class="cell" data-row="0" data-col="0">5</div>
     *   <div class="cell" data-row="0" data-col="1"></div>
     *   ...
     * </div>
     */
    renderGrid(board, initial) {
        // Vider grille
        this.grid.innerHTML = '';
        
        // Créer 81 cells
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                const cell = this.createCell(row, col, board, initial);
                this.grid.appendChild(cell);
            }
        }
        
        // Reset erreurs
        this.errorCount = 0;
        this.updateErrorDisplay();
    }
    
    /**
     * Créer cell individuelle
     * 
     * @param {number} row
     * @param {number} col
     * @param {number[][]} board
     * @param {number[][]} initial
     * @returns {HTMLElement} Cell div
     * 
     * CLASSES CSS :
     * - cell : Base
     * - fixed : Cell initiale (non modifiable)
     * - border-right : Bordure droite blocs 3x3
     * - border-bottom : Bordure bas blocs 3x3
     */
    createCell(row, col, board, initial) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        
        // Attributs data pour position
        cell.dataset.row = row;
        cell.dataset.col = col;
        
        // Valeur cell
        const value = board[row][col];
        if (value !== 0) {
            cell.textContent = value;
            
            // Cell fixe (initiale)
            if (initial[row][col] !== 0) {
                cell.classList.add('fixed');
            }
        }
        
        // Bordures blocs 3x3
        if (col % 3 === 2 && col < 8) {
            cell.classList.add('border-right');
        }
        if (row % 3 === 2 && row < 8) {
            cell.classList.add('border-bottom');
        }
        
        // Event listener
        cell.addEventListener('click', () => this.selectCell(cell));
        
        return cell;
    }
    
    /**
     * Sélectionner cell
     * 
     * @param {HTMLElement} cell
     * 
     * LOGIQUE :
     * 1. Désélectionner cell précédente
     * 2. Sélectionner nouvelle cell
     * 3. Highlight ligne, colonne, bloc
     */
    selectCell(cell) {
        // Ne pas sélectionner cell fixe
        if (cell.classList.contains('fixed')) {
            return;
        }
        
        // Désélectionner toutes cells
        this.grid.querySelectorAll('.cell').forEach(c => {
            c.classList.remove('selected', 'highlighted');
        });
        
        // Sélectionner cell
        cell.classList.add('selected');
        this.selectedCell = cell;
        
        // Highlight ligne, colonne, bloc
        this.highlightRelatedCells(cell);
    }
    
    /**
     * Highlight cells liées (ligne, colonne, bloc)
     * 
     * @param {HTMLElement} cell
     * 
     * POURQUOI highlight ?
     * Aide visuelle : Voir conflits potentiels
     */
    highlightRelatedCells(cell) {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        // Trouver bloc 3x3
        const boxStartRow = Math.floor(row / 3) * 3;
        const boxStartCol = Math.floor(col / 3) * 3;
        
        // Highlight toutes cells grille
        this.grid.querySelectorAll('.cell').forEach(c => {
            const r = parseInt(c.dataset.row);
            const co = parseInt(c.dataset.col);
            
            // Même ligne OU colonne OU bloc
            const sameRow = r === row;
            const sameCol = co === col;
            const sameBox = (
                r >= boxStartRow && r < boxStartRow + 3 &&
                co >= boxStartCol && co < boxStartCol + 3
            );
            
            if (sameRow || sameCol || sameBox) {
                c.classList.add('highlighted');
            }
        });
        
        // Re-add selected (pour Z-index)
        cell.classList.add('selected');
    }
    
    /**
     * Placer nombre dans cell
     * 
     * @param {number} num - Nombre 1-9
     * @returns {boolean} true si correct
     * 
     * LOGIQUE :
     * 1. Vérifier cell sélectionnée
     * 2. Placer nombre
     * 3. Valider (vert si correct, rouge si erreur)
     * 4. Mettre à jour erreurs
     */
    placeNumber(num) {
        if (!this.selectedCell) return false;
        
        const row = parseInt(this.selectedCell.dataset.row);
        const col = parseInt(this.selectedCell.dataset.col);
        
        // Placer dans modèle
        const isCorrect = window.sudoku.placeNumber(row, col, num);
        
        // Afficher dans UI
        this.selectedCell.textContent = num;
        
        // Validation visuelle
        this.selectedCell.classList.remove('correct', 'incorrect');
        
        if (isCorrect) {
            this.selectedCell.classList.add('correct');
        } else {
            this.selectedCell.classList.add('incorrect');
            this.errorCount++;
            this.updateErrorDisplay();
        }
        
        return isCorrect;
    }
    
    /**
     * Effacer cell sélectionnée
     */
    clearCell() {
        if (!this.selectedCell) return;
        
        const row = parseInt(this.selectedCell.dataset.row);
        const col = parseInt(this.selectedCell.dataset.col);
        
        // Effacer modèle
        window.sudoku.board[row][col] = 0;
        
        // Effacer UI
        this.selectedCell.textContent = '';
        this.selectedCell.classList.remove('correct', 'incorrect');
    }
    
    /**
     * Mettre à jour affichage erreurs
     */
    updateErrorDisplay() {
        this.errorsDisplay.textContent = this.errorCount;
    }
    
    /**
     * Afficher indice
     * 
     * @param {Object} hint - { row, col, value }
     */
    showHint(hint) {
        if (!hint) {
            alert('Aucun indice disponible');
            return;
        }
        
        // Trouver cell
        const cell = this.grid.querySelector(
            `[data-row="${hint.row}"][data-col="${hint.col}"]`
        );
        
        if (cell) {
            // Placer valeur
            cell.textContent = hint.value;
            cell.classList.add('hint');
            
            // Mettre à jour modèle
            window.sudoku.board[hint.row][hint.col] = hint.value;
        }
    }
    
    /**
     * Vérifier victoire
     * 
     * @returns {boolean} true si gagné
     */
    checkWin() {
        return window.sudoku.isComplete();
    }
    
    /**
     * Afficher message victoire
     * 
     * @param {number} time - Temps en secondes
     */
    showWinMessage(time) {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        const timeStr = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        alert(`🎉 Félicitations ! Vous avez gagné en ${timeStr} avec ${this.errorCount} erreur(s).`);
        
        // Sauvegarder score (Phase 7-8)
        window.leaderboard.addScore({
            username: window.auth.getUsername(),
            time,
            errors: this.errorCount,
            difficulty: window.sudoku.difficulty,
            date: new Date().toISOString()
        });
    }
}
```

### 6.3 Gestion Clavier

**Fichier :** `js/ui.js` (suite)

```javascript
/**
 * KEYBOARD CONTROLLER
 * Gère input clavier
 */

class KeyboardController {
    constructor(ui) {
        this.ui = ui;
        this.setupListeners();
    }
    
    /**
     * Configurer event listeners
     * 
     * TOUCHES GÉRÉES :
     * - 1-9 : Placer nombre
     * - Backspace/Delete : Effacer
     * - Arrow keys : Navigation
     */
    setupListeners() {
        document.addEventListener('keydown', (event) => {
            this.handleKeyPress(event);
        });
    }
    
    /**
     * Gérer pression touche
     * 
     * @param {KeyboardEvent} event
     */
    handleKeyPress(event) {
        // Ignorer si input focusé (modal login)
        if (event.target.tagName === 'INPUT') {
            return;
        }
        
        // Chiffres 1-9
        if (/^[1-9]$/.test(event.key)) {
            const num = parseInt(event.key);
            this.ui.placeNumber(num);
            event.preventDefault();
        }
        
        // Backspace / Delete
        else if (event.key === 'Backspace' || event.key === 'Delete') {
            this.ui.clearCell();
            event.preventDefault();
        }
        
        // Arrow keys (navigation)
        else if (event.key.startsWith('Arrow')) {
            this.handleArrowKey(event.key);
            event.preventDefault();
        }
    }
    
    /**
     * Gérer touches flèches (navigation grille)
     * 
     * @param {string} key - "ArrowUp", "ArrowDown", etc.
     * 
     * LOGIQUE :
     * 1. Trouver cell actuelle
     * 2. Calculer nouvelle position
     * 3. Sélectionner nouvelle cell
     */
    handleArrowKey(key) {
        if (!this.ui.selectedCell) {
            // Sélectionner première cell
            const firstCell = this.ui.grid.querySelector('.cell');
            if (firstCell) this.ui.selectCell(firstCell);
            return;
        }
        
        let row = parseInt(this.ui.selectedCell.dataset.row);
        let col = parseInt(this.ui.selectedCell.dataset.col);
        
        // Calculer nouvelle position
        switch (key) {
            case 'ArrowUp':
                row = (row - 1 + 9) % 9; // Wrap around
                break;
            case 'ArrowDown':
                row = (row + 1) % 9;
                break;
            case 'ArrowLeft':
                col = (col - 1 + 9) % 9;
                break;
            case 'ArrowRight':
                col = (col + 1) % 9;
                break;
        }
        
        // Sélectionner nouvelle cell
        const newCell = this.ui.grid.querySelector(
            `[data-row="${row}"][data-col="${col}"]`
        );
        
        if (newCell) {
            this.ui.selectCell(newCell);
        }
    }
}
```

### Checkpoint Phase 6

- ✅ Grille 9x9 dynamique créée
- ✅ Sélection cell + highlight
- ✅ Input clavier fonctionnel
- ✅ Validation visuelle (vert/rouge)
- ✅ Navigation arrow keys

---

## Phase 7 : Storage & Timer (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 7

- ✅ localStorage vs sessionStorage (différences)
- ✅ Timer système
- ✅ Sauvegarder scores persistants
- ✅ **EXPLICATIONS SÉCURITÉ** (pourquoi pas sécurisé)

### 7.1 localStorage vs sessionStorage

```javascript
/**
 * WEB STORAGE API
 * 
 * 2 TYPES :
 * 1. localStorage : Persistant (pas d'expiration)
 * 2. sessionStorage : Session seulement (onglet fermé = effacé)
 * 
 * CARACTÉRISTIQUES :
 * - Stockage client-side (navigateur)
 * - Limite ~5-10 MB par domaine
 * - Synchrone (bloque thread)
 * - Seulement strings (JSON.stringify pour objets)
 * 
 * ⚠️ SÉCURITÉ :
 * - VISIBLE dans DevTools (F12 → Application → Storage)
 * - PAS crypté
 * - Accessible JavaScript (XSS attacks)
 * - JAMAIS stocker :
 *   × Mots de passe
 *   × Tokens sensibles (API keys)
 *   × Données personnelles sensibles (CB, SSN)
 * 
 * ✅ USAGE LÉGITIME :
 * - Préférences UI (thème, langue)
 * - Scores jeux
 * - Panier e-commerce (temporaire)
 * - Cache données non sensibles
 */

// ==========================================
// localStorage : PERSISTANT
// ==========================================

// Sauvegarder
localStorage.setItem('username', 'John');
localStorage.setItem('score', '100');

// Récupérer
const username = localStorage.getItem('username'); // "John"
const score = localStorage.getItem('score');       // "100"

// Supprimer
localStorage.removeItem('username');

// Tout supprimer
localStorage.clear();

// Objet → JSON
const player = { name: 'John', score: 85 };
localStorage.setItem('player', JSON.stringify(player));

// JSON → Objet
const storedPlayer = JSON.parse(localStorage.getItem('player'));

// ==========================================
// sessionStorage : SESSION SEULEMENT
// ==========================================

// API IDENTIQUE à localStorage
sessionStorage.setItem('sessionId', 'abc123');
const sessionId = sessionStorage.getItem('sessionId');

// DIFFÉRENCE : Effacé quand onglet fermé
// localStorage persiste après fermeture

// ==========================================
// COMPARAISON
// ==========================================

/**
 * | Critère        | localStorage | sessionStorage |
 * |----------------|--------------|----------------|
 * | Persistance    | Permanent    | Session        |
 * | Portée         | Domaine      | Onglet         |
 * | Taille         | ~5-10 MB     | ~5-10 MB       |
 * | Expiration     | Jamais       | Fermeture      |
 * | Partage        | Tous onglets | Onglet seul    |
 */
```

**Fichier :** `js/storage.js`

```javascript
/**
 * STORAGE MANAGER
 * Gère localStorage/sessionStorage
 */

class StorageManager {
    /**
     * Sauvegarder données localStorage
     * 
     * @param {string} key
     * @param {any} value - Converti en JSON automatiquement
     */
    static saveLocal(key, value) {
        try {
            const jsonValue = JSON.stringify(value);
            localStorage.setItem(key, jsonValue);
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }
    
    /**
     * Récupérer données localStorage
     * 
     * @param {string} key
     * @param {any} defaultValue - Valeur si clé inexistante
     * @returns {any} Valeur parsée
     */
    static loadLocal(key, defaultValue = null) {
        try {
            const jsonValue = localStorage.getItem(key);
            return jsonValue ? JSON.parse(jsonValue) : defaultValue;
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return defaultValue;
        }
    }
    
    /**
     * Supprimer clé localStorage
     */
    static removeLocal(key) {
        localStorage.removeItem(key);
    }
    
    /**
     * Sauvegarder session (sessionStorage)
     * 
     * ⚠️ ATTENTION SÉCURITÉ :
     * sessionStorage n'est PAS sécurisé
     * Visible dans DevTools
     * JAMAIS stocker mots de passe ici
     */
    static saveSession(key, value) {
        try {
            const jsonValue = JSON.stringify(value);
            sessionStorage.setItem(key, jsonValue);
        } catch (error) {
            console.error('Error saving to sessionStorage:', error);
        }
    }
    
    /**
     * Récupérer session
     */
    static loadSession(key, defaultValue = null) {
        try {
            const jsonValue = sessionStorage.getItem(key);
            return jsonValue ? JSON.parse(jsonValue) : defaultValue;
        } catch (error) {
            console.error('Error loading from sessionStorage:', error);
            return defaultValue;
        }
    }
    
    /**
     * Supprimer session
     */
    static removeSession(key) {
        sessionStorage.removeItem(key);
    }
}
```

### 7.2 Timer Système

**Fichier :** `js/timer.js`

```javascript
/**
 * TIMER SYSTÈME
 * Gère chronomètre partie
 */

class Timer {
    constructor(displayElement) {
        this.display = displayElement;
        this.seconds = 0;
        this.intervalId = null;
        this.isRunning = false;
    }
    
    /**
     * Démarrer timer
     * 
     * LOGIQUE :
     * setInterval() exécute callback chaque seconde
     * Incrémente seconds et met à jour affichage
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.intervalId = setInterval(() => {
            this.seconds++;
            this.updateDisplay();
        }, 1000); // 1000ms = 1 seconde
    }
    
    /**
     * Arrêter timer
     */
    stop() {
        if (!this.isRunning) return;
        
        clearInterval(this.intervalId);
        this.isRunning = false;
    }
    
    /**
     * Reset timer
     */
    reset() {
        this.stop();
        this.seconds = 0;
        this.updateDisplay();
    }
    
    /**
     * Mettre à jour affichage
     * 
     * FORMAT : MM:SS
     * Exemple : 125 secondes → "02:05"
     */
    updateDisplay() {
        const minutes = Math.floor(this.seconds / 60);
        const seconds = this.seconds % 60;
        
        // padStart(2, '0') : Ajoute 0 devant si < 10
        // 5 → "05", 12 → "12"
        const timeStr = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        this.display.textContent = timeStr;
    }
    
    /**
     * Obtenir temps actuel (secondes)
     */
    getTime() {
        return this.seconds;
    }
}
```

### Checkpoint Phase 7

- ✅ localStorage vs sessionStorage compris
- ✅ Timer fonctionnel
- ✅ Storage manager créé
- ✅ Explications sécurité détaillées

---

## Phase 8 : Auth Simulée & Leaderboard (2h)

<div class="omny-meta" data-level="🟡 Intermédiaire" data-time="2 heures"></div>

### Objectifs Phase 8

- ✅ Authentification simulée (NON SÉCURISÉE)
- ✅ Modale login stylisée
- ✅ Leaderboard localStorage
- ✅ **EXPLICATIONS SÉCURITÉ DÉTAILLÉES**

### 8.1 Authentification Simulée (⚠️ NON SÉCURISÉE)

**Fichier :** `js/auth.js`

```javascript
/**
 * ⚠️ ⚠️ ⚠️ AUTHENTIFICATION SIMULÉE ⚠️ ⚠️ ⚠️
 * 
 * CETTE IMPLÉMENTATION EST **NON SÉCURISÉE** ET **PUREMENT ÉDUCATIVE**
 * 
 * POURQUOI C'EST DANGEREUX :
 * 
 * 1. PAS DE SERVEUR
 *    - Authentification réelle nécessite serveur backend
 *    - Client-side auth = TOUJOURS contournable
 * 
 * 2. PAS DE VÉRIFICATION MOT DE PASSE
 *    - Mot de passe n'est pas vérifié
 *    - N'importe qui peut "se connecter"
 * 
 * 3. sessionStorage VISIBLE
 *    - F12 → Application → Session Storage
 *    - Données modifiables par n'importe qui
 * 
 * 4. PAS DE CRYPTAGE
 *    - Données en clair
 *    - Vulnérable XSS (Cross-Site Scripting)
 * 
 * 5. PAS DE PROTECTION CSRF
 *    - Cross-Site Request Forgery
 *    - Attaquant peut faire requêtes au nom utilisateur
 * 
 * VRAIE AUTHENTIFICATION NÉCESSITE :
 * ✅ Backend serveur (Node.js, PHP, Python, etc.)
 * ✅ Hash mots de passe (bcrypt, Argon2)
 * ✅ Sessions serveur OU JWT (JSON Web Tokens)
 * ✅ HTTPS (SSL/TLS)
 * ✅ Protection CSRF tokens
 * ✅ Rate limiting (limite tentatives)
 * ✅ 2FA (Two-Factor Authentication)
 * 
 * CETTE SIMULATION EST OK POUR :
 * ✅ Apprendre JavaScript
 * ✅ Prototyper UI
 * ✅ Projets éducatifs
 * 
 * JAMAIS UTILISER EN PRODUCTION
 */

class Auth {
    constructor() {
        this.currentUser = null;
        this.loadSession();
    }
    
    /**
     * "Connexion" simulée (PAS SÉCURISÉ)
     * 
     * @param {string} username
     * @param {string} password - IGNORÉ (pas de vérification)
     * @returns {boolean} true si "connecté"
     * 
     * ⚠️ DANGER :
     * - Mot de passe pas vérifié
     * - Pas de hash
     * - Pas de serveur
     */
    login(username, password) {
        // ⚠️ SIMULATION : Accepter n'importe quel username/password
        if (!username || username.trim() === '') {
            return false;
        }
        
        // Créer objet "utilisateur"
        this.currentUser = {
            username: username.trim(),
            loginTime: new Date().toISOString()
        };
        
        // ⚠️ DANGER : Stocker dans sessionStorage (PAS SÉCURISÉ)
        StorageManager.saveSession('user', this.currentUser);
        
        return true;
    }
    
    /**
     * Déconnexion
     */
    logout() {
        this.currentUser = null;
        StorageManager.removeSession('user');
    }
    
    /**
     * Vérifier si connecté
     */
    isLoggedIn() {
        return this.currentUser !== null;
    }
    
    /**
     * Obtenir username
     */
    getUsername() {
        return this.currentUser ? this.currentUser.username : 'Guest';
    }
    
    /**
     * Charger session (si existe)
     */
    loadSession() {
        this.currentUser = StorageManager.loadSession('user');
    }
}
```

### 8.2 Modale Login Stylisée

**Fichier :** `css/styles.css` (extrait modale)

```css
/**
 * MODAL LOGIN
 */

.modal {
    /* Position fixe plein écran */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    
    /* Overlay semi-transparent */
    background: rgba(0, 0, 0, 0.7);
    
    /* Centrage contenu */
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* Z-index haut (au-dessus tout) */
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 20px 25px rgba(0, 0, 0, 0.3);
}

.security-warning {
    background: #fff3cd;
    border: 2px solid #ffc107;
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.security-warning strong {
    color: #856404;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-group input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #ddd;
    border-radius: 0.5rem;
    font-size: 1rem;
}

.form-group input:focus {
    outline: none;
    border-color: #6366f1;
}
```

### 8.3 Leaderboard Système

**Fichier :** `js/leaderboard.js`

```javascript
/**
 * LEADERBOARD SYSTÈME
 * Gère classement scores
 */

class Leaderboard {
    constructor(displayElement) {
        this.display = displayElement;
        this.scores = [];
        this.loadScores();
    }
    
    /**
     * Charger scores depuis localStorage
     */
    loadScores() {
        this.scores = StorageManager.loadLocal('leaderboard', []);
    }
    
    /**
     * Sauvegarder scores
     */
    saveScores() {
        StorageManager.saveLocal('leaderboard', this.scores);
    }
    
    /**
     * Ajouter score
     * 
     * @param {Object} score - { username, time, errors, difficulty, date }
     */
    addScore(score) {
        this.scores.push(score);
        
        // Trier par temps (plus rapide = meilleur)
        this.scores.sort((a, b) => a.time - b.time);
        
        // Garder top 10 seulement
        if (this.scores.length > 10) {
            this.scores = this.scores.slice(0, 10);
        }
        
        this.saveScores();
        this.render();
    }
    
    /**
     * Afficher leaderboard
     */
    render() {
        if (this.scores.length === 0) {
            this.display.innerHTML = '<p class="no-scores">Aucun score enregistré</p>';
            return;
        }
        
        let html = '<ol class="scores-list">';
        
        this.scores.forEach((score, index) => {
            const minutes = Math.floor(score.time / 60);
            const seconds = score.time % 60;
            const timeStr = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            // Emoji médailles top 3
            const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
            
            html += `
                <li class="score-item ${index < 3 ? 'top-three' : ''}">
                    <span class="rank">${medal || (index + 1)}</span>
                    <span class="username">${score.username}</span>
                    <span class="time">${timeStr}</span>
                    <span class="difficulty">${score.difficulty}</span>
                </li>
            `;
        });
        
        html += '</ol>';
        
        this.display.innerHTML = html;
    }
    
    /**
     * Reset leaderboard
     */
    reset() {
        if (confirm('Effacer tous les scores ?')) {
            this.scores = [];
            this.saveScores();
            this.render();
        }
    }
}
```

### 8.4 Main Application

**Fichier :** `js/main.js`

```javascript
/**
 * APPLICATION PRINCIPALE
 * Point d'entrée, orchestration
 */

// Instances globales
window.sudoku = new Sudoku();
window.ui = new SudokuUI();
window.auth = new Auth();
window.timer = new Timer(document.getElementById('timer-display'));
window.leaderboard = new Leaderboard(document.getElementById('leaderboard-list'));
window.keyboard = new KeyboardController(window.ui);

// Éléments DOM
const loginModal = document.getElementById('login-modal');
const loginForm = document.getElementById('login-form');
const usernameDisplay = document.getElementById('username-display');
const btnLogout = document.getElementById('btn-logout');
const btnNewGame = document.getElementById('btn-new-game');
const btnValidate = document.getElementById('btn-validate');
const btnHint = document.getElementById('btn-hint');
const difficultyButtons = document.querySelectorAll('.btn-difficulty');

/**
 * Initialisation application
 */
function init() {
    // Vérifier authentification
    if (!auth.isLoggedIn()) {
        showLoginModal();
    } else {
        hideLoginModal();
        updateUserDisplay();
        startNewGame('medium');
    }
    
    // Event listeners
    setupEventListeners();
    
    // Afficher leaderboard
    leaderboard.render();
}

/**
 * Configuration event listeners
 */
function setupEventListeners() {
    // Login
    loginForm.addEventListener('submit', handleLogin);
    
    // Logout
    btnLogout.addEventListener('click', handleLogout);
    
    // Nouvelle partie
    btnNewGame.addEventListener('click', () => {
        const difficulty = document.querySelector('.btn-difficulty.active').dataset.difficulty;
        startNewGame(difficulty);
    });
    
    // Valider
    btnValidate.addEventListener('click', handleValidate);
    
    // Indice
    btnHint.addEventListener('click', handleHint);
    
    // Difficulté
    difficultyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            difficultyButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

/**
 * Gérer login (simulé)
 */
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (auth.login(username, password)) {
        hideLoginModal();
        updateUserDisplay();
        startNewGame('medium');
    } else {
        alert('Veuillez entrer un nom d\'utilisateur');
    }
}

/**
 * Gérer logout
 */
function handleLogout() {
    if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
        auth.logout();
        showLoginModal();
        timer.stop();
    }
}

/**
 * Démarrer nouvelle partie
 */
function startNewGame(difficulty) {
    // Générer Sudoku
    sudoku.newGame(difficulty);
    
    // Afficher grille
    ui.renderGrid(sudoku.board, sudoku.initial);
    
    // Reset timer
    timer.reset();
    timer.start();
}

/**
 * Valider grille
 */
function handleValidate() {
    if (ui.checkWin()) {
        timer.stop();
        ui.showWinMessage(timer.getTime());
    } else {
        alert('La grille n\'est pas encore complète ou contient des erreurs');
    }
}

/**
 * Afficher indice
 */
function handleHint() {
    const hint = sudoku.getHint();
    ui.showHint(hint);
}

/**
 * Afficher/cacher modale login
 */
function showLoginModal() {
    loginModal.style.display = 'flex';
}

function hideLoginModal() {
    loginModal.style.display = 'none';
}

/**
 * Mettre à jour affichage utilisateur
 */
function updateUserDisplay() {
    usernameDisplay.textContent = `Utilisateur: ${auth.getUsername()}`;
}

// Démarrer application
init();
```

### Checkpoint Phase 8

- ✅ Authentification simulée (avec WARNINGS sécurité)
- ✅ Modale login stylisée
- ✅ Leaderboard localStorage
- ✅ Application complète assemblée

---

## Conclusion

!!! success "JavaScript Vanilla Maîtrisé avec Jeu Sudoku Complet"
    
    **17h formation • 8 phases • Sudoku production-ready avec explications exhaustives**
    
    Vous avez créé un jeu Sudoku complet avec TOUS les fondamentaux JavaScript !

### Récapitulatif Compétences

**Phase 1 : Fondamentaux JavaScript**

- ✅ Variables (let, const vs var)
- ✅ Types primitifs (string, number, boolean)
- ✅ Fonctions (déclaration, expression, arrow)
- ✅ Conditions (if, switch, ternaire)
- ✅ Boucles (for, while, forEach, map, filter, reduce)

**Phase 2 : DOM Manipulation**

- ✅ Sélection éléments (querySelector, querySelectorAll)
- ✅ Modification contenu (textContent, innerHTML)
- ✅ Création éléments (createElement, appendChild)
- ✅ Styles et classes (classList)

**Phase 3 : Events & Interactions**

- ✅ addEventListener (click, input, keyboard)
- ✅ Event object (target, preventDefault)
- ✅ Event delegation (performance)
- ✅ Event propagation (bubbling, capturing)

**Phase 4 : Objects & Arrays**

- ✅ Objets (propriétés, méthodes, this)
- ✅ Arrays modernes (map, filter, reduce, find)
- ✅ Destructuring & spread operator
- ✅ JSON (stringify, parse)

**Phase 5 : Algorithme Sudoku**

- ✅ **Backtracking algorithm** (récursion)
- ✅ Génération grille valide
- ✅ Résolution automatique
- ✅ Validation (lignes, colonnes, blocs)
- ✅ Niveaux difficulté

**Phase 6 : UI Sudoku**

- ✅ Grille 9x9 dynamique
- ✅ Sélection cells + highlight
- ✅ Input clavier (1-9, Arrow keys)
- ✅ Validation visuelle (vert/rouge)
- ✅ Timer + compteur erreurs

**Phase 7 : Storage & Timer**

- ✅ **localStorage vs sessionStorage** (différences)
- ✅ Timer système (setInterval)
- ✅ Sauvegarder scores persistants
- ✅ **EXPLICATIONS SÉCURITÉ**

**Phase 8 : Auth & Leaderboard**

- ✅ **Authentification simulée** (⚠️ NON SÉCURISÉE)
- ✅ Modale login stylisée
- ✅ Leaderboard localStorage
- ✅ **EXPLICATIONS SÉCURITÉ DÉTAILLÉES**

### Vous Êtes Prêt Pour

✅ **Angular** : Comprendre components, directives, services  
✅ **Alpine.js** : Comprendre x-data, x-on, x-bind  
✅ **React** : Comprendre JSX, props, state, hooks  
✅ **Vue.js** : Comprendre v-if, v-for, v-model  
✅ **Node.js** : Backend JavaScript  
✅ **Projets professionnels** : Jeu Sudoku utilisable  

---

*Guide rédigé avec ❤️ pour la communauté web*  
*Version 1.0 - JavaScript ES6+ Vanilla - Décembre 2025*