---
description: "Phase 2 : Algorithme Central. Création du Cerveau JS (Array Object) et des fonctions de modification d'état (Ajouter, Basculer, Supprimer)."
icon: lucide/cpu
tags: ["JAVASCRIPT", "ARRAY", "FUNCTIONS", "CRUD"]
status: stable
---

# Phase 2 : Logique Algorithmique (CRUD)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h00">
</div>

!!! quote "Objectif de la Phase"
    Le Formulaire est inerte. Nous allons capturer sa puissance (L'événement `submit`), l'empêcher de recharger la page, et construire une "Banque de Données" dans la RAM de l'ordinateur (Un Array de la forme `[{id:1, text:"Lait", done:false}]`).

## 1. Modéliser la Donnée (Le Cerveau)

Créez le fichier `script.js`.
Ne codez **rien** concernant le DOM pour l'instant. Concentrez-vous sur l'architecture de la donnée. C'est l'essence du métier d'Ingénieur.

```javascript
/* --- LE CERVEAU DE L'APPLICATION (STATE) --- */

// Notre source unique de vérité. Si c'est dans le tableau, ça existe. 
// Si ça n'y est pas, ça n'existe pas, même si le HTML dit le contraire.
let courses = [];

// Fonction de Création (Create)
function ajouterCourse(texteLabel) {
    const nouvelleCourse = {
        id: Date.now(),      // Un ID unique et temporel (ex: 1675239999120)
        label: texteLabel,   // Ce que l'utilisateur a écrit ("Pâtes")
        terminee: false      // Par défaut, quand on l'ajoute, elle n'est pas barrée !
    };
    
    // On pousse cet Objet dans le grand Tableau
    courses.push(nouvelleCourse);
}

// Fonction de Suppression (Delete)
function supprimerCourse(idASupprimer) {
    // La méthode magique .filter() "Garde tout dans le tableau, SAUF l'ID qu'on veut tuer"
    courses = courses.filter(item => item.id !== idASupprimer);
}

// Fonction de Bascule (Toggle)
function basculerEtat(idACocher) {
    // La méthode .find() cherche l'objet exact qui possède cet ID
    const objetTrouve = courses.find(item => item.id === idACocher);
    
    if (objetTrouve) {
        // S'il était 'true', il devient 'false'. S'il était 'false'...
        objetTrouve.terminee = !objetTrouve.terminee;
    }
}
```

Prenez une respiration. Ce code est 100% détaché du web. Il pourrait tourner dans l'ordinateur d'une voiture Tesla. C'est l'objectif.

## 2. Capturer le Formulaire (L'Événement DOM)

Maintenant, nous devons lier cette belle tuyauterie avec l'interaction humaine. Le visiteur va taper son texte dans l'Input HTML et frapper la touche Entrée !

Insérez ce code dans `script.js` (en dessous des fonctions précédentes) :

```javascript
/* --- LE LIEN HOMME-MACHINE (INTERFACE DOM) --- */

// 1. Cibler les éléments physiques importants
const formElement = document.getElementById('item-form');
const inputElement = document.getElementById('item-input');

// 2. Écouter la Soumission du Formulaire
formElement.addEventListener('submit', function(event) {
    // CRITIQUE : Bloquer le comportement natif du vieux Web 1.0 (Sinon la page se rafraichit !)
    event.preventDefault();
    
    // Récupérer ce que l'humain a tapé
    const valeurTapee = inputElement.value.trim(); // .trim() enlève les espaces vides "  Lait  " -> "Lait"
    
    if (valeurTapee !== "") {
        // 1. Envoyer cet ordre au Cerveau défini plus haut !
        ajouterCourse(valeurTapee);
        
        // 2. Vider le champ texte pour qu'il soit propre pour le prochain mot
        inputElement.value = "";
        
        // (Optionnel) Prouver que ça marche dans la console
        console.log("État Actuel du Cerveau :", courses);
        
        // FUTURE PHASE 3 : Rendre ça visuel à l'écran !
    }
});
```

!!! tip "La perfection du Form Submit"
    Pourquoi avons-nous écouté l'événement `submit` sur la balise `<form>`, plutôt que l'événement `click` sur le `<button>` ? Parce que dans 99% des cas, l'utilisateur d'ordinateur appuie sur "Entrée" sur son clavier pour valider. Le `submit` écoute le Clic **ET** le Clavier.

## Checklist de la Phase 2

- [ ] Je tape "Pommes" dans le champ, je tape Entrée. La page **NE SE RECHARGE PAS** (Pas de clignotement de l'onglet du navigateur). Le texte disparait, c'est bon signe !
- [ ] J'ouvre F12 (Inspecteur), onglet "Console". Je vois apparaître : `État Actuel du Cerveau : Array(1)`.
- [ ] Si je déroule cet Array, je vois `[{id: 1684940, label: "Pommes", terminee: false}]`.

La Logique est impeccable. L'utilisateur enregistre des paires de données valides dans la mémoire courte de l'ordinateur. Mais rien ne s'affiche à l'écran pour l'utilisateur.

Il nous faut convertir ces données abstraites en véritables balises `<li>`, `<span>` et `<button>` générées "à la volée"... C'est la Révélation de la Phase Finale !

[Passer à la Phase 3 : Le Rendu DOM et LocalStorage →](phase3.md)
