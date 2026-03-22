---
description: "Rappel accéléré de la syntaxe de base en JS : Déclarer une donnée, utiliser des conditions, et la magie des tableaux (listes) avec les boucles."
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "ALGORITHMIQUE", "RAPPEL", "VARIABLES", "BOUCLES"]
---

# Bases (Rappel)

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Introduction

!!! warning "Ce module est un rafraichissement !"
    Si les concepts de "Variable", de "Condition", ou de "Boucle" vous sont rigoureusement étrangers, **vous ne devez pas continuer**. Dirigez-vous vers le module fondamental dédié à l'**[Algorithmique (Variables, Tableaux, Boucles)](../../../../../bases/fondamentaux/index.md)** pour construire une fondation intellectuelle saine.

Ici, nous n'allons pas réexpliquer *pourquoi* une variable existe, mais strictement **comment on l'écrit** en JavaScript.

<br>

---

## Les Variables (Les tiroirs)

Pour demander à la RAM de l'ordinateur de retenir une information vivante, le JavaScript utilise le mot-clé `let` (qui signifie *"laisse cette boîte être..."*).

```javascript title="JavaScript — Déclaration d'une variable"
// 1. Je déclare mon tiroir fermé avec "let" et j'y glisse un nombre
let viesRestantes = 3;

// 2. Le joueur meurt. Je modifie le contenu du tiroir. (SANS let !)
viesRestantes = 2; 

// Si je tente de refaire "let viesRestantes = 10", le JavaScript plantera ! 
// On ne fabrique pas le même tiroir deux fois !
```

Le JavaScript connait de base trois "types" profonds (Ingrédients) :

- Les **Nombres** (Pas de guillemets) : `let age = 42;`
- Le **Texte** (String, avec des guillemets) : `let nom = "Alice";`
- Les **Booléens** (Vrai ou Faux) : `let estConnecte = true;`

!!! note "Nous aborderons la différence vitale entre `let` et sa soeur la constante `const` dans le module dédié à la syntaxe moderne !"

<br>

---

## La Logique (Prendre des décisions)

Le JavaScript est idiot. Il s'exécute de haut en bas sans réfléchir, sauf si vous lui apprenez à observer le monde grâce aux embranchements `if / else`.

```javascript title="JavaScript — La condition if / else"
let heureLocale = 14;

if (heureLocale < 12) {
    console.log("Bonjour, il fait beau ce matin !");
} else {
    // Si la condition du dessus est fausse, le code chute automatiquement ici.
    console.log("Bon après-midi !");
}
```

Méfiez-vous des opérateurs de comparaison :

- `==` (Égalité souple, très dangeureuse : `"2" == 2` sera vrai).
- `===` (Égalité stricte absolue : `"2" === 2` sera faux, car le type diffère). **On n'utilise QUE celui-ci.**

<br>

---

## Les Tableaux et les Boucles (Les Listes de courses)

Stocker le niveau d'un seul joueur dans une seule variable, c'est facile. Stocker les 500 objets de son inventaire dans 500 variables (`let objet1 = "Arc"`, `let objet2 = "Flèche"`), c'est une folie mentale. 

L'ordinateur adore les listes, appelées **Tableaux** (Arrays).
```javascript title="JavaScript — L'armoire à pharmacie (Le Tableau)"
// Les crochets définissent une "Armoire", chaque élément est séparé par une virgule.
let inventairePoches = ["Clés", "Portefeuille", "Téléphone"];

// Combien j'ai d'objets dans la poche ?
console.log(inventairePoches.length); // 3

// L'ordinateur compte mystérieusement à partir de zéro...
console.log(inventairePoches[0]); // Affiche "Clés". (Le premier tiroir est le n°0).
console.log(inventairePoches[2]); // Affiche "Téléphone".
```

### La Répétition (Automatique)
Si l'inventaire comporte 500 armes, et que le joueur tombe dans la lave, il faut les lui retirer une par une (`inventaire[0] = null;`). Le moyen absolu d'automatiser cette tâche, c'est la **Boucle `for`** !

La boucle la plus moderne et lisible de l'histoire du JavaScript est la boucle `for...of` (Pour... chaque élément de type [Singulier] de [MonTableauGlobal]).

```javascript title="JavaScript — Traiter une liste géante en 3 secondes"
let inventairePoches = ["Clés", "Portefeuille", "Téléphone"];

// Pour [chaque "objet"] pris un par un dans l'armoire [inventairePoches]
for (let objet of inventairePoches) {
    // L'ordinateur va relire ce bloc autant de fois qu'il y a d'éléments (soit 3 fois)
    console.log(`Le feu détruit l'objet : ${objet} !`);
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un code JavaScript se décompose comme un roman algorithmique très simple :
    Je stocke l'état du monde avec des **Variables** (`let`), je vérifie des règles avec mes **Conditions** (`if`), et le cas échéant, je gère ou j'automatise des tas de données listées (`[...]`) grâce à l'implacable rouleau compresseur de la **Boucle**. 

> Il ne nous manque plus qu'une brique fondamentale pour coder proprement sans répéter 100 fois la même série de code dans notre fichier : **[Les Fonctions et les Objets (Le Dictionnaire JS).](./03-fonctions-et-objets.md)**.

<br>
