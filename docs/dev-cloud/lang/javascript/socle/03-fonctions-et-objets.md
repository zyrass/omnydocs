---
description: "Rappel accéléré des deux blocs de lego les plus importants d'une architecture applicative : l'Usine (La Fonction) et l'Entité (L'Objet clé:valeur)."
icon: lucide/book-open-check
tags: ["JAVASCRIPT", "FONCTIONS", "OBJETS", "STRUCTURE"]
---

# Fonctions et Objets

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Introduction

!!! warning "Ce module est un rafraichissement !"
    De même que le module précédent, si les termes "Paramètres", "Arguments" et "Return" ne vous évoquent aucun souvenir, faites une pause et lisez le cours transversal sur les **[Fonctions IT](../../../../../bases/fondamentaux/fonctions.md)**.

Un bon mécanicien ne jette pas tous ses outils en vrac au sol. Il les regroupe dans des boîtes scellées avec des étiquettes (les Objets), et il automatise les actions répétitives en appuyant sur de grosses machines (les Fonctions).

<br>

---

## La Machine à tout faire : La Fonction

En JavaScript pur, tout le code écrit à la "racine" du fichier s'exécute d'un coup quand la page charge. Imaginez un jeu vidéo où l'attaque ultime de votre personnage part toute seule dès le lancement du jeu, puis plus rien le reste de la partie.
C'est dramatique : **Le code doit savoir ÊTRE MIS SUR PAUSE**, et n'être déclenché **QUE** lorsque l'on en a besoin.

C'est le rôle fondamental de la fonction. Elle gèle un bout de code, et attend patiemment l'ordre d'être invoquée.

```javascript title="JavaScript — L'anatomie d'une fonction"

// 1. DÉCLARATION : L'usine est construite (Rien ne se passe à l'écran)
// Nom = calculerTVA
// Paramètre EXIGÉ (Ingrédient) : un "prixBrut"
function calculerTVA(prixBrut) {
    let tvaActuelle = 1.20;
    
    // Le mot "return" expulse le résultat vers la sortie de l'usine
    return prixBrut * tvaActuelle; 
}


// 2. INVOCATION : Je lance la machine de mon propre fait, avec ma donnée réelle (l'argument 150)
let monAchatFinal = calculerTVA(150);

console.log(monAchatFinal); // Affichera 180 !
```

Le code `prixBrut * tvaActuelle` a pu être isolé, et ne s'exécutera qu'au doux moment où *vous* l'aurez décidé, sans affecter le reste du programme.

<br>

---

## Décrire le monde réel : Les Objets

Si vous devez modéliser une voiture avec ce que nous savons, vous allez naturellement faire ceci :

```javascript
// La fausse bonne idée
let marqueVoiture = "Toyota";
let anneeVoiture = 2021;
let couleurVoiture = "Rouge";
```
Désormais, imaginez un parking de 10 000 voitures. Vous allez obtenir 30 000 variables volantes totalement indépendantes et anonymes qui se baladent sans aucun lien entre elles. Dans le monde web, cela est ingérable.

Le JavaScript permet la modélisation sous forme de **Dictionnaire JSON-like** (L'Objet). 

```javascript title="JavaScript — Les accolades salvatrices (L'Objet)"
// La variable voiture possède des "Clés", qui mènent à une "Valeur" !
let voiture = {
    marque: "Toyota",
    annee: 2021,
    couleur: "Rouge",
    options: ["GPS", "Toit ouvrant"]
};

// Lecture de la valeur associée à la clé 'marque' (le Point de navigation)
console.log(voiture.marque); // "Toyota"

// Modification profonde
voiture.couleur = "Noire"; 
```

L'objet JavaScript, via sa fantastique syntaxe en accolade `{}`, est si puissant et standardisé qu'il a inspiré tout le format universel d'échange de données mondial nommé **JSON** *(JavaScript Object Notation)* !

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Auparavant, lors de la préhistoire du Web, le JavaScript était un fichier gigantesque de 10 000 lignes, fait de Fonctions isolées par-ci, ou d'Objets par-là, avec une architecture chaotique importée par de vieilles balises `<script>` HTML.
    Aujourd'hui, c'est **fini**.

> Ce crash-course des fondations JavaScript n'était là que pour s'assurer que vous et l'architecture moderne habillez le même vocabulaire. Il est l'heure de fermer la parenthèse du passé. 
Plongeons à pieds joints dans le Front-End applicatif d'aujourd'hui, l'Outillage de Compilation et la Révolution ES6. 
**[Direction le module 04 : L'Environnement et les Modules (Vite.js) !](../moteur/04-environnement-modules.md)**

<br>
