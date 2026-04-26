---
description: "Phase 5 : Création de la Vue (UI Component) de la Todolist. Abonnement aux données du Store (MVC) et dessin de la liste via map() et join()."
icon: lucide/list-checks
tags: ["JAVASCRIPT", "DOM", "EVENTS", "ARRAY FILTER"]
status: stable
---

# Phase 5 : Injection DOM (Widget Todos)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le `todoStore.js` (Phase 4) gère la mémoire. Le `todoWidget.js` va gérer l'affichage. Ce fichier va capturer le texte tapé par l'utilisateur, l'envoyer au magasin (Store), puis demander au magasin sa nouvelle liste pour redessiner intégralement le carré HTML. C'est l'essence du triptyque Modèle/Vue.

## 1. Le Composant Rendu (La Vue)

Créez le fichier `src/components/todoWidget.js`.

```javascript
/* src/components/todoWidget.js */
import { getTodos, addTodo, toggleTodo, deleteTodo } from '../state/todoStore.js';

export function initTodos() {
    const inputEl = document.getElementById('todo-input');
    const btnEl = document.getElementById('add-todo-btn');
    const listEl = document.getElementById('todo-list');

    if (!inputEl || !btnEl || !listEl) return;

    // FONCTION MAÎTRESSE : Rendu HTML depuis le Tableau d'objets (Store)
    const render = () => {
        const todos = getTodos(); // 1. Je demande au store : "Donne-moi ta donnée !"

        // 2. Je transforme chaque Objet JS en Chaîne de caractères HTML
        const htmlArray = todos.map(todo => `
            <li class="todo-item ${todo.isDone ? 'done' : ''}" data-id="${todo.id}">
                <button class="toggle-btn" aria-label="Valider">
                    ${todo.isDone ? '✅' : '⬜'}
                </button>
                <span class="todo-text">${todo.text}</span>
                <button class="delete-btn" aria-label="Supprimer">🗑️</button>
            </li>
        `);

        // 3. J'écrase le vieux <ul> avec la nouvelle liste (Array converti en String via join)
        listEl.innerHTML = htmlArray.join('');
    };

    // ... La suite (Les intéractions Humaines) ira ici
}
```

## 2. L'Interaction Utilisateur (Les Boutons et l'Input)

Toujours dans la fonction `initTodos()`, après avoir déclaré `render()`, initialisons d'abord l'affichage de notre liste pré-enregistrée !

```javascript
    /* (Suite de initTodos) */

    render(); // Dessine immédiatement ce qu'il y a dans le LocalStorage

    // 1. AJOUTER UNE TÂCHE
    const handleAdd = () => {
        const text = inputEl.value; // Ce qu'il a écrit
        
        // J'ordonne au Cerveau (Store) de l'avaler
        const success = addTodo(text); 
        
        if (success) {
            inputEl.value = ''; // Je vide l'input texte pour qu'il soit propre
            render(); // JE FORCE LE RAFRAICHISSEMENT DE L'ÉCRAN
        }
    };

    btnEl.addEventListener('click', handleAdd);
    
    // Le confort absolu: S'il appuie sur "Entrée" depuis le clavier !
    inputEl.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleAdd();
    });
```

## 3. L'Écoute Déléguée (Event Delegation)

Si nous avons 500 tâches, ajouter un `addEventListener` privé sur les 500 boutons "Supprimer" ferait exploser la mémoire du navigateur.
L'astuce de l'ingénieur est la **Délégation**. On place UN SEUL écouteur sur le `<ul id="todo-list">` tout entier, et on demande "À l'intérieur de ce UL géant, sur quoi mon clic a-t-il atterri ?".

```javascript
    /* (Fin de initTodos) */

    // 2. SUPPRIMER OU COCHER UNE TÂCHE (Délégation sur parent)
    listEl.addEventListener('click', (event) => {
        
        // 'event.target' est le pixel exact où a cliqué la souris (un bouton ? un span ?)
        // .closest() demande: "Remonte jusqu'à trouver une balise <li>"
        const liElement = event.target.closest('.todo-item');
        if (!liElement) return; // Il a cliqué un espace vide du <ul>

        // Je récupère l'identifiant caché 'data-id="..."' de ma String HTML !
        const id = liElement.dataset.id; 

        // S'il a cliqué physiquement sur un truc de classe '.delete-btn'
        if (event.target.classList.contains('delete-btn')) {
            deleteTodo(id); // Informe le cerveau
            render();       // Rafraichit l'écran
        }

        // S'il a cliqué sur le bouton de Validation Check
        if (event.target.classList.contains('toggle-btn') || event.target.classList.contains('todo-text')) {
            toggleTodo(id); // Inverse l'état Booléen
            render();       // Pimente l'Ecran (Le rond blanc deviendra Validation Verte)
        }
    });

} // Fin de initTodos()
```

Importez `initTodos()` et lancez-la dans `main.js`. 

## Le Secret du Flow (One Way Data Binding originel)

Vous venez de toucher du doigt le concept majeur de **React.js**.
Dans votre composant, L'utilisateur clique sur la poubelle. Que se passe-t-il visuellement ? **Rien.** La ligne HTML n'est pas "détruite" manuellement avec une fonction sale comme `.remove()`. 
Non. L'ordre part au `deleteTodo()`. Le tableau du fichier `todoStore` coupe une donnée au fond du CPU Cerveau.
Puis, la fonction `render()` re-télécharge tout le tableau de mémoire, et repeint frénétiquement le carré blanc HTML en millisecondes. 
La Vue n'est que la photo Polaroïd d'une Data sous-jacente. Il n'y a qu'une unique vérité : Le Store (Local Storage).

## Checklist de la Phase 5

- [ ] L'application tourne. L'inspecteur HTML et Réseau est silencieux sans Erreur Rouge `Cannot read property 'value' of null`.
- [ ] Taper *"Finir le cours Omnydocs JS"* et frapper `ENTER` ajoute instantanément le mot avec un petit bouton corbeille sur sa droite.
- [ ] En cliquant sur la corbeille, une fonction invisible remonte vers Localstorage, exécute le `.filter` (Le tableau Javascript recrache l'élément ciblé), et l'interface HTML repeint la liste d'objet sans cet invité.
- [ ] En vidant votre caddie (Clear Chrome Cache, Remove Storage), tout redevient une simple application vierge par magie (`let todos = []`).

La Todolist est terminée. Votre Widget de Productivité tourne de manière isolée sans bloquer les Widgets Météo ni votre Horloge. **Le Bonus et la Fête** : Mettre en pratique, seul, vos notions de requêtes `FetchAPI` en Phase 6 sur une dernière donnée.

[Passer à la Phase 6 : Le Widget Blagues API →](phase6.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
