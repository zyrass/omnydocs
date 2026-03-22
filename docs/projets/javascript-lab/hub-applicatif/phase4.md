---
description: "Phase 4 : Modélisation d'une Todo List CRUD complète. Séparation stricte des responsabilités (SOC) : Construction du Store local (State Management) délié du rendu visuel."
icon: lucide/database
tags: ["JAVASCRIPT", "CRUD", "LOCALSTORAGE", "STATE MANAGEMENT"]
status: stable
---

# Phase 4 : Architecture State & CRUD

<div
  class="omny-meta"
  data-level="🔴 Avancé (Certifiant)"
  data-version="2.0"
  data-time="2 Heures">
</div>

!!! quote "Objectif de la Phase"
    Le Widget "Mes Tâches" est le plus complexe de votre Hub. L'utilisateur veut ajouter une tâche (Create), la voir (Read), la cocher/décocher (Update), et la jeter à la poubelle (Delete).
    L'erreur fatale du développeur junior serait de coder ce CRUD directement dans le DOM (ex: `nouvelleLi.remove()`). L'ingénieur, lui, conçoit un "Cerveau" (Store) qui gère des Objets en mémoire, puis demande à la "Vue" (UI) de se redessiner d'après ce Cerveau.

## 1. La Définition du Cerveau (Le Store)

Créez un dossier `src/state/` et un fichier `todoStore.js`.
Ce fichier sera le SEUL autorisé à parler avec `localStorage` ou à modifier le tableau des tâches. C'est votre "Base de Données" locale (Single Source of Truth).

```javascript
/* src/state/todoStore.js */

// 1. LECTURE INITIALE (Read)
// Au chargement du projet, on tente de récupérer le tableau sauvegardé.
// S'il n'existe pas en mémoire, JSON.parse va échouer et on renverra un tableau vide []
const STORAGE_KEY = 'hub_todos';
let todos = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

// 2. LA FONCTION DE PERSISTANCE (Le bouton de sauvegarde)
// Cette fonction privée n'est pas exportée. Elle est utilisée en interne.
function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

// 3. ENVOYER LA COPIE (Get)
export function getTodos() {
    // On pourrait exporter directement 'todos', mais 
    // par sécurité, on exporte les données pour la vue métier
    return todos;
}

// 4. CREATION (Create)
export function addTodo(textValue) {
    if (!textValue.trim()) return null; // Sécurité anti-tâche vide (Espaces vierges)
    
    // On modélise un "Modèle de Donnée" métier strict
    const newTodo = {
        id: Date.now(), // Un ID unique basé sur l'horloge
        text: textValue.trim(),
        isDone: false   // Par défaut, la tâche n'est pas faite
    };
    
    todos.push(newTodo); // Ajout au cerveau RAM
    saveState();         // Ajout au cerveau Disque Dur
    return newTodo;
}

// 5. MISE À JOUR (Update) booléenne
export function toggleTodo(idToFind) {
    // Array.find() cherche l'objet exact qui correspond à cet ID unique
    const todo = todos.find(t => t.id === Number(idToFind));
    if (todo) {
        todo.isDone = !todo.isDone; // Si True -> False. Si False -> True.
        saveState();
    }
}

// 6. SUPPRESSION (Delete)
export function deleteTodo(idToDelete) {
    // .filter() garde tout le monde SAUF celui qu'on veut tuer
    todos = todos.filter(t => t.id !== Number(idToDelete));
    saveState();
}
```

Prenez une minute pour analyser l'élégance de ce code.
Il n'a **aucune** idée qu'il sera affiché sur un site internet ! Il n'y a pas un seul `div` ni `console.log`. C'est de l'Algorithmie pure. Ce store pourrait être utilisé pour créer un bot Discord ou une app de Ligne de Commande. C'est la beauté du ** découplage **.

## 2. Pousser l'État dans la console

Pour vérifier que notre "Cerveau" (Store) marche, ouvrez provisoirement `src/main.js` et écrivez simplement, tout en bas :

```javascript
// Test Crash du Store
import { addTodo, getTodos, deleteTodo, toggleTodo } from './state/todoStore.js';

window.addTodo = addTodo;
window.getTodos = getTodos;
```

Ouvrez la console du navigateur (F12) et tapez vos commandes manuelles :
1. `addTodo("Faire les courses")`
2. `getTodos()` -> Vous voyez un [Array] avec votre objet !
3. Rafraîchissez la page. Tapez de nouveau `getTodos()`. L'objet est toujours là. Le disque dur a mémorisé votre ordre.

⚠️ N'oubliez pas d'effacer ce test grossier dans `main.js` une fois terminé.

## Checklist de la Phase 4

- [ ] Je comprends la différence entre les 3 lettres "R" (Read), "C" (Create), et "D" (Delete) dans mon fichier `todoStore`.
- [ ] L'attribut `Date.now()` crée bien un nombre massif du type `17892348510` servant de clef primaire robuste.
- [ ] J'ai constaté (F12 > Stockage Local) qu'une clé `hub_todos` s'est bien formée lorsque je code la commande dans la console web ou bien lorsque le Store est initialement vide avec un `[]`.

C'est parfait. Votre base de données interne et modérée est prête. Il nous faut relier ce Cerveau algorithmique à la Vue Humaine (DOM). C'est le Rendu Visuel : **Phase 5**.

[Passer à la Phase 5 : Injection DOM de la Todo →](phase5.md)
