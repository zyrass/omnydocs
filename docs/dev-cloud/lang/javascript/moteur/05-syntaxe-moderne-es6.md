---
description: "Comprendre l'évolution vitale de la syntaxe JavaScript : let/const, les bases des fonctions, les fléchées, la destructuration et les opérateurs récents."
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "ES6", "FONCTIONS", "DESTRUCTURATION", "SPREAD"]
---

# Moteur et ES6+

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3 Heures">
</div>

## Introduction

!!! warning "Avertissement Pédagogique - Le Choc du Futur"
    *Ce module anticipe des concepts de programmation très modernes pour habituer votre œil aux standards industriels actuels.* 
    *Si vous vous sentez "flou" en lisant certains exemples, **c'est parfaitement normal**. L'assimilation du JavaScript prend du temps. Ne cherchez pas à tout retenir par cœur aujourd'hui, mais comprenez plutôt **pourquoi** ces nouveaux outils existent : ils sont là avec pour seule mission de vous faire gagner un temps précieux (réduire un bloc de 10 lignes à une seule lignede code).*

Le JavaScript a connu une révolution en 2015, nommée **ES6** (ECMAScript 2015). Depuis, le langage reçoit des mises à jour majeures chaque année, abandonnant son ancienne syntaxe très lourde au profit d'outils redoutables d'efficacité.

<br>

---

## Les Variables : Adieu `var`

Pendant très longtemps, JavaScript utilisait le mot-clé `var` pour stocker des données temporaires en mémoire. Le problème de `var` ? Il ne respectait pas "les murs" algorithmiques de votre code, créant des bugs cauchemardesques appelés "fuites de portée". 

!!! note "La règle d'or d'aujourd'hui"
    **On n'écrit absolument plus jamais `var`**. Tous les tutoriels ou vidéos YouTube l'utilisant datent de l'âge de pierre.

Le couple moderne est constitué de `let` et `const` :

1. **`const` (Constante)** : Une donnée qui, une fois déclarée, **ne peut plus jamais être réassignée**. À utiliser dans **95 % des cas**.
2. **`let` (Variable)** : Une donnée vouée à changer de valeur plus tard dans votre code (comme un compteur de score).

```javascript title="JavaScript — Le duo moderne : let et const"
// Score est modifiable
let score = 0;
score = 10; // OK !

// Le nom de l'utilisateur est fixe
const nomUtilisateur = "Sarah";
nomUtilisateur = "Alice"; // ERREUR CRITIQUE du moteur JS
```

<br>

---

## Rappel Indispensable : Les Fonctions

Avant de plonger dans les nouveautés, il est impératif de comprendre pourquoi nous utilisons des fonctions en programmation.

Une fonction est une **usine de traitement de données** (ou une recette de cuisine). Elle prend des ingrédients (les _Paramètres_), effectue un travail de transformation, et vous renvoie le plat fini (le _Return_).

1. **Réutilisabilité** : Si vous écrivez une fonction pour calculer la TVA, vous pourrez l'invoquer 10 000 fois dans votre vie sur 10 000 prix différents, sans jamais réécrire la logique mathématique.
2. **Portée Isolée (Scope)** : Ce qu'il se passe dans une fonction... reste dans la fonction ! Les variables inventées à l'intérieur d'une fonction ne s'échappent jamais à l'extérieur, protégeant le reste du programme.

```javascript title="JavaScript — Une fonction classique pré-ES6"
// Déclaration de l'usine "saluer" qui exige un "nom" comme paramètre
function saluer(nom) {
    let message = "Bienvenue, " + nom + " !";
    return message;
}

// Invocation de l'usine avec la matière première "Marc"
console.log(saluer("Marc")); // Rendu : "Bienvenue, Marc !"
```

### Les Fonctions Fléchées (Arrow Functions)

Pour écrire ces usines beaucoup plus rapidement, ES6 a inventé la syntaxe des **fonctions fléchées**. Elles retirent le vieux mot-clé `function` pour le remplacer par une flèche `=>`.

```javascript title="JavaScript — Fonction Fléchée (Maintenant)"
// Avant : function(nom) { return "Salut " + nom; }

// Maintenant (Fonction Fléchée extrêmement compacte) :
const saluerRapide = (nom) => "Salut " + nom;

console.log(saluerRapide("Sophie"));
```

!!! danger "Attention au piège du `this`"
    Outre la vitesse de frappe, la fonction fléchée règle un très gros problème d'héritage d'objet en JS : **Elle ne crée pas son propre contexte `this`**. Elle hérite du `this` de son environnement parent. Dans un cas avancé (comme l'écoute d'un événement sur un bouton), une fonction classique ciblera le bouton cliqué pour son "this", mais une fonction fléchée fera crasher le concept et regardera le bloc le plus large par défaut.

<br>

### Les Fonctions comme Passagers (Callbacks)

En JavaScript, une fonction est considérée comme une **donnée normale** (comme un chiffre ou un texte). Cela signifie que vous pouvez passer une fonction en tant qu'argument à une *autre* fonction. 

On appelle cette fonction passée en argument un **Callback** (Rappel).

!!! quote "Analogie"
    *C'est comme donner une enveloppe scellée à un coursier (la fonction principale) et lui dire : "Ouvre cette enveloppe et fais ce qui est écrit dedans (le callback) uniquement quand tu seras arrivé à destination".*

C'est ce concept qui permet la programmation "réactive" : on demande au navigateur d'exécuter un bout de code spécifiquement au moment d'un clic ou d'une réponse réseau.

<br>

---

## L'Art d'Extraire : La Destructuration

En JavaScript Front-End, 90 % de votre travail d'architecte consistera à manipuler des objets complexes (par exemple, récupérer les informations depuis une base de données).

```javascript title="JavaScript — Avant (L'extraction lourde)"
const utilisateur = {
    nom: "Wick",
    prenom: "John",
    age: 45
};

// Avant ES6, il fallait taper ça :
const prenom = utilisateur.prenom;
const nom = utilisateur.nom;
const age = utilisateur.age;
```

**Maintenant, avec la Destructuration**, vous demandez à JavaScript de "cloner" instantanément les clés de l'objet dans de nouvelles variables en une seule micro-ligne !

```javascript title="JavaScript — Après (La Destructuration magique)"
// J'extrais "prenom" et "age" de l'objet "utilisateur" instantanément !
const { prenom, age } = utilisateur;

console.log(prenom); // "John"
console.log(age);    // 45
```

<br>

---

## L'Opérateur Rest/Spread (`...`)

Les trois petits points mystérieux (`...`) sont sans doute l'outil le plus puissant du JS moderne. Ils ont deux utilités opposées selon la situation :

### Spread (Le Disséminateur)
Permet de **déballer** le contenu d'un tableau ou d'un objet vers un autre (pour faire une copie parfaite).

```javascript title="JavaScript — Copier et fusionner avec Spread"
const armesArmurerie = ["Pistolet", "Fusil"];
const protectionEquipe = ["Gilet", "Casque"];

// Je fusionne instantanément les deux anciens inventaires :
const inventaireGlobal = [...armesArmurerie, ...protectionEquipe, "Couteau"];

console.log(inventaireGlobal);
// Résultat : ["Pistolet", "Fusil", "Gilet", "Casque", "Couteau"]
```

### Rest (Le Ramasse-miettes)
Permet de regrouper un nombre indéfini d'éléments restants dans un nouveau tableau compact. Très utilisé dans les fonctions quand on ne sait pas à l'avance combien d'ingrédients l'utilisateur va envoyer.

```javascript title="JavaScript — Récupérer le reste avec Rest"
const [premier, deuxieme, ...leResteDeLeursOutils] = ["Marteau", "Clou", "Vis", "Perceuse", "Tournevis"];

console.log(premier);              // "Marteau"
console.log(leResteDeLeursOutils); // ["Vis", "Perceuse", "Tournevis"]
```

<br>

---

## Les Outils Ultimes Récents (2020+)

Le langage JavaScript a encore évolué très récemment pour éviter des plantages serveurs récurrents, notamment face à des données "vides" introuvables. 

### `.at()` — Les Tableaux
Dites adieu aux crochets monstrueux pour chercher le tout dernier élément d'une pile de 10 000 objets.

```javascript title="JavaScript — .at() pour l'envers des tableaux"
const couleurs = ["Rouge", "Vert", "Bleu"];

// Avant : syntaxe illisible pour avoir le dernier 
console.log(couleurs[couleurs.length - 1]); // "Bleu"

// Maintenant :
console.log(couleurs.at(-1)); // "Bleu" (Le dernier élément direct en partant de -1)
```

### L'Optional Chaining (`?.`)
Si vous cherchez un objet caché dans un autre objet, mais que ce sous-objet a été effacé en base de données, l'application Front-End **explose**. Le point d'interrogation la sauve, en renvoyant poliment `undefined` sans tout détruire sur son passage.

```javascript title="JavaScript — Le gardien du plantage (?.)"
const voiture = {
    marque: "Peugeot"
    // Je n'ai PAS de sous-catégorie ".moteur" ici !
};

// Console classique : l'application JS crash ! (Cannot read properties of undefined)
// console.log(voiture.moteur.cylindree);  

// Console Moderne : Si moteur n'existe pas, il arrête de lire et se tait !
console.log(voiture.moteur?.cylindree); // "undefined"
```

### Le Nullish Coalescing (`??`)
Permet de fournir une **"Roue de Secours Absolue"** uniquement si la donnée est dramatiquement non définie (`null` ou `undefined`).

```javascript title="JavaScript — La valeur de sécurité (??)"
let nomSaisiParJoueur = null; // Le joueur n'a rien mis...

// Si c'est Null (??), alors je remplace par "Invité" !
let nomAffiche = nomSaisiParJoueur ?? "Invité";

console.log(nomAffiche); // "Invité"
```

<br>

---

## Manipuler le Temps (L'Objet Date)

Le temps en informatique est complexe. JavaScript gère les dates via un objet intégré nommé **`Date`**.

### Créer une Date
```javascript title="JavaScript — L'instanciation de Date"
// 1. Date et Heure actuelle du système
const maintenant = new Date();

// 2. Créer une date précise (Année, Mois [0-11], Jour)
// ⚠️ Attention : En JS, les mois commencent à 0 (Janvier) !
const noel2026 = new Date(2026, 11, 25);
```

### Extraire des morceaux
Une fois la boîte de Date créée, vous pouvez l'interroger pour extraire des fragments précis :

```javascript title="JavaScript — Les Getters"
const aujourdhui = new Date();

console.log(aujourdhui.getFullYear()); // 2026
console.log(aujourdhui.getMonth());    // 2 (Mars car 0=Janvier, 1=Février, 2=Mars)
console.log(aujourdhui.getDate());     // 21 (Le jour du mois)
console.log(aujourdhui.getDay());      // Le jour de la semaine (0=Dimanche)
```

### Le Graal de l'affichage : `toLocaleDateString`
Pour ne plus jamais manipuler les dates "à la main" (comme concaténer jour + "/" + mois), on utilise les outils de localisation natifs puissants.

```javascript title="JavaScript — Formatage local automatique"
const aujourdhui = new Date();

// Format Français simple : "21/03/2026"
console.log(aujourdhui.toLocaleDateString('fr-FR'));

// Format complet et élégant : "samedi 21 mars 2026"
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
console.log(aujourdhui.toLocaleDateString('fr-FR', options));
```

!!! tip "Pourquoi le mois commence à zéro ?"
    C'est un héritage historique du langage C. Les mois sont stockés dans une liste listée (tableau), et comme nous l'avons vu dans les fondamentaux, les indices de tableaux commencent toujours à **0**. Janvier = 0, Décembre = 11. 
    *Cependant, l'usage des `options` dans `toLocaleDateString` vous permet d'ignorer totalement ce calcul mental.*

<br>

---

## Les Tableaux : La boîte à outils (Array Methods)

Au-delà de la boucle `for`, le JavaScript moderne propose des méthodes intégrées (des fonctions toutes prêtes) pour manipuler les données.

### Ajouter et Supprimer
```javascript title="JavaScript — Modifier une liste"
const fruits = ["Pomme", "Banane"];

fruits.push("Orange");    // Ajoute à la fin
fruits.unshift("Fraise"); // Ajoute au début

fruits.pop();   // Supprime le dernier
fruits.shift(); // Supprime le premier
```

### Transformer et Filtrer (Le duo gagnant)
Dans 90% des cas, vous utiliserez ces deux méthodes pour traiter des données reçues d'une API.

```javascript title="JavaScript — .map() et .filter()"
const prixHT = [10, 20, 30, 40, 50];

// 1. .map() : Applique une fonction sur chaque élément et RENVOIE une nouvelle liste
const prixTTC = prixHT.map(prix => prix * 1.20); 

// 2. .filter() : Garde uniquement les éléments qui respectent une condition
const grosAchats = prixTTC.filter(prix => prix > 30);
```

### Ordonner et Accumuler
*   **`.sort()`** : Trie le tableau (attention, `.sort()` modifie le tableau original !).
*   **`.reduce()`** : Permet de calculer une valeur unique à partir d'un tableau (ex: la somme totale d'un panier).

<br>

---

## L'Énigme du `this`

Le mot-clé **`this`** représente le "contexte" actuel. C'est l'objet qui est en train de "posséder" le code qui s'exécute.

```javascript title="JavaScript — L'importance du contexte"
const utilisateur = {
    nom: "Wick",
    saluer: function() {
        // "this" représente ici l'objet "utilisateur"
        console.log("Bonjour, je suis Mr " + this.nom);
    }
};

utilisateur.saluer(); // "Bonjour, je suis Mr Wick"
```

!!! danger "Le piège des fonctions fléchées"
    Les **fonctions fléchées** ne créent pas leur propre `this`. Elles utilisent celui de leur "parent". 
    *Si vous utilisez une flèche `=>` dans l'exemple ci-dessus, `this.nom` sera indéfini car la flèche cherchera le nom de la fenêtre globale du navigateur, pas celui de l'objet.*

<br>

---

## Architecture Industrielle : Les Classes

Historiquement, le JavaScript utilisait un système complexe de "Prototypes". Aujourd'hui, on utilise le **Sucre Syntaxique** des **Classes**, beaucoup plus lisible et standard.

```javascript title="JavaScript — Créer une entité avec une Class"
class Personnage {
    // Le constructeur est la fonction qui se lance à la "naissance" de l'objet
    constructor(nom, pointsDeVie) {
        this.nom = nom;
        this.pv = pointsDeVie;
    }

    // Une méthode (une action que le personnage peut faire)
    attaquer() {
        console.log(this.nom + " lance une attaque !");
    }
}

// "new" crée une nouvelle "Instance" (une copie réelle du plan)
const hero = new Personnage("Aragorn", 100);
hero.attaquer(); // "Aragorn lance une attaque !"
```

### L'Héritage et le mot-clé `super`
Parfois, une classe doit "hériter" des caractéristiques d'une autre pour éviter de se répéter. Par exemple, un `Magicien` est un `Personnage`, il a donc ses PV et son Nom, mais avec une barre de Mana en plus.

```javascript title="JavaScript — L'héritage (extends & super)"
// La classe "Enfant" hérite de "Personnage" (le Parent)
class Magicien extends Personnage {
    constructor(nom, pv, pointsDeMana) {
        // "super" appelle le constructeur du Parent (Personnage)
        // C'est OBLIGATOIRE avant d'utiliser "this"
        super(nom, pv); 
        this.mana = pointsDeMana;
    }

    lancerSort() {
        console.log(this.nom + " lance une boule de feu avec ses " + this.mana + " de mana !");
    }
}

const gandalf = new Magicien("Gandalf", 80, 200);
gandalf.attaquer();  // Méthode héritée du Parent
gandalf.lancerSort(); // Méthode spécifique au Magicien
```

### L'Encapsulation : Public vs Privé

Dans des langages comme **PHP** ou **Java**, on utilise les mots-clés `public`, `private` ou `protected` pour verrouiller l'accès à certaines données depuis l'extérieur d'une classe.

En **JavaScript**, c'est historiquement plus "libre". Par défaut, n'importe qui peut lire ou modifier n'importe quelle variable d'une classe.

#### 1. La convention de politesse (`_underscore`)
Pendant plus de 20 ans, le JavaScript n'avait pas de mot-clé pour le "Privé". Les développeurs ont donc instauré une convention : si une variable commence par un tiret bas `_`, cela signifie : *"Ceci est une donnée interne, n'y touchez pas depuis l'extérieur"*.

```javascript title="JavaScript — L'encapsulation par convention"
class CompteBancaire {
    constructor(soldeInitial) {
        // C'est techniquement modifiable, mais le "_" prévient le développeur
        this._solde = soldeInitial; 
    }
}

const monCompte = new CompteBancaire(1000);
monCompte._solde = 0; // ⚠️ Possible, mais considéré comme une très mauvaise pratique.
```

#### 2. Le standard moderne : Le symbole `#`
Aujourd'hui, le JavaScript a enfin son propre système de "vrai privé". Si vous préfixez une variable par le symbole **`#`**, elle devient **physiquement inaccessible** hors de la classe.

```javascript title="JavaScript — Le véritable Privé (#)"
class CoffreFort {
    #codeSecret = "1234"; // Déclarée directement en haut de classe

    verifierCode(saisie) {
        // On peut l'utiliser INTERNEMENT
        return saisie === this.#codeSecret;
    }
}

const coffre = new CoffreFort();
console.log(coffre.#codeSecret); // ❌ ERREUR : Le navigateur refuse l'accès !
```

!!! tip "Différence avec PHP"
    Contrairement au PHP où l'on écrit `private $variable`, le JavaScript utilise le préfixe `#` (`#variable`). C'est un choix de design du langage pour permettre au moteur JS de savoir instantanément, sans même lire tout le fichier, que cette donnée est protégée.

<br>

---

## Le Filet de Sécurité : `try...catch`

En programmation, le crash est inévitable (ex: le serveur est hors-ligne, ou une donnée est corrompue). Pour éviter que toute votre page ne devienne blanche, on "encapsule" le code dangereux.

### Gérer l'accident
```javascript title="JavaScript — Le bloc try...catch"
try {
    const resultat = codeTresDangereux();
    console.log(resultat);
} catch (error) {
    // Si ça plante, on tombe ICI au lieu de crasher le navigateur
    console.warn("Désolé, une erreur est survenue :", error.message);
} finally {
    // S'exécute quoi qu'il arrive (succès ou échec)
    console.log("Tentative terminée.");
}
```

### Provoquer une erreur : `throw`
Si vous construisez votre propre règle métier, vous pouvez décider vous-même que le script "doit" s'arrêter si une condition n'est pas remplie.

```javascript title="JavaScript — Créer sa propre erreur"
function diviser(a, b) {
    if (b === 0) {
        // On "lance" (throw) une erreur personnalisée
        throw new Error("Impossible de diviser par zéro !");
    }
    return a / b;
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Aujourd'hui, coder efficacement en Front-End passe incontestablement par ces outils. `const` protège de la mutation par accident. Les fonctions fléchées `=>` sauvent du temps. La destructuration `{ data } = reponse` lit vos bases de données plus vite. Les **méthodes de tableaux** (`map`, `filter`) gèrent la logique des listes en une ligne, et les **Classes** structurent proprement vos entités. Enfin, le `?.` et le `try...catch` empêchent le navigateur d'afficher un écran blanc suite à une petite erreur.

> Ce bagage syntaxique est le carburant de votre moteur logique. Il est temps à présent de connecter tout cela au monde purement visible : attraper vos boutons HTML, changer les couleurs CSS, et donner de la réactivité visuelle à la page au clic de la souris. 
**Bienvenue dans l'interface absolue du métier : [Le Module sur Le DOM et les Événements](../application/06-dom-manipulation.md)**

<br>
