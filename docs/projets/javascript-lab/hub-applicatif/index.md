---
description: "Masterclass JS Front-End : Créez de Zéro le Hub Applicatif personnel incluant une Web App Météo (API Fetch Async), une Todo-list (State Management CRUD), et un environnement ES6 ultra-modulaire propulsé par Vite."
tags: ["JAVASCRIPT", "ASYNC", "FETCH", "PROMESSE", "CRUD", "ARCHITECTURE"]
---

# Hub Applicatif

<div
  class="omny-meta"
  data-level="🔴 Avancé (Certifiant)"
  data-version="2.0"
  data-time="6-10 heures (6 phases)">
</div>

## Introduction du Projet - Le Terminal Personnalisé

L'intégration d'interfaces statiques et la dynamisation basique n'ont plus de secret pour vous. Mais le vrai cœur du web moderne, c'est **la donnée asynchrone**. Dans ce projet monumental ("From Scratch"), vous allez construire une **véritable Single Page Application (SPA)**, constituée de multiples widgets autonomes dialoguant avec des serveurs planétaires et votre stockage local.

!!! note "Ce Hub Applicatif est votre rite de passage. Il réunit toutes les briques de l'ingénierie Web Vanilla : requêtes réseau `async/await`, architecture de fichiers poussée (SOC - Separation of Concerns), CRUD (Create Read Update Delete), et synchronisation de l'état (State) avec l'Interface Utilisateur (DOM)."

Cette phase **zéro vous présente** :

- L'architecture de répertoires industrielle requise pour scaler une Single Page App sans framework.
- La notion de "State" (l'État de l'application) et la dérivation vers le DOM.
- La mécanique de l'Event Loop lors de l'interrogation de l'API **OpenWeatherMap**.
- Le fonctionnement d'un CRUD complet via un magasin (Store) adossé au réseau.
- La validation des 6 Phases, de la pose du socle Vite jusqu'à la sécurisation des requêtes.
- La transition logique vers les frameworks d'entreprise (React, Angular).

!!! quote "Pourquoi s'acharner à tout faire en 'Vanilla Async' ?"
    Construire une SPA Météo + Todo en Vanilla JS est extrêmement verbeux. Pourquoi ne pas utiliser React ? Parce que si vous apprenez React en pensant que la fonction `fetch` et les méthodes `.map()` sont "de la magie React", vous serez bloqué au moindre bug industriel. Ce projet vous plonge les mains dans le moteur de l'**Event Loop Javascript** : gérer les Promesses, attraper les erreurs (`try/catch`), dessiner l'interface en attendant la donnée (Loaders), et modéliser de la donnée complexe dans `localStorage`. 

## Objectifs d'Apprentissage

!!! abstract "À l'issue de cette Masterclass, **vous serez capable de** :"

    - [ ] Architecturer des dizaines de fichiers JS autour d'une logique métier (MVC Pattern).
    - [ ] Émuler un **State Manager** natif pour centraliser les données de la Web App.
    - [ ] Déclencher, intercepter, et traiter des **appels HTTP (API REST)** via `fetch`.
    - [ ] Gérer l'**Event Loop** avec élégance (`async`, `await`, `Promise.all`).
    - [ ] Construire un **CRUD complet** fonctionnant intégralement depuis la mémoire client (LocalStorage).
    - [ ] Scinder votre vue HTML en **Composants JS** (Web Components factices) qui se rafraîchissent seuls.

## Finalité Pédagogique et Professionnelle

### Le tremplin vers les SPA Frameworks

!!! quote "Ce laboratoire certifie votre compréhension de JavaScript côté client. À la fin de ce projet, vous n'apprendrez plus de syntaxe JS fondamentale, vous apprendrez des écosystèmes (React, Vue) car tout le reste sera acquis."

**Cas d'usage professionnels directs :**

- **Dashboard B2B** → Agrégation de métriques d'entreprises depuis plusieurs sources (APIs multiples).
- **Plateforme Client** → Gérer les états de chargement (Loaders, Skeletons) pour ne pas frustrer l'utilisateur lent.
- **Outillage Interne** → Création d'applis de gestion rapides et maintenables hors ligne.
- **Résilience** → Apprendre à concevoir une application qui "ne plante pas" physiquement quand le wifi de l'utilisateur tombe.

**Compétences d'Ingénieur Frontend requises :**

- [x] Injection de templates HTML complexes via des String Interpolations (` `).
- [x] Utilisation avancée des fonctions de rappel (Callbacks).
- [x] Parsing de structures JSON massives envoyées par OpenWeather.
- [x] Récupération et contrôle de la Latitude/Longitude (Geolocation API).
- [x] Modélisation de la donnée sous forme de classe ECMAScript 6 (`class Todo { ... }`).

## Architecture Globale du Hub

### Le Flow de l'Event Loop (API Météo)

```mermaid
graph TB
    subgraph "Thread Principal (Bloquant) - Interface Utilisateur"
        UI[Bouton 'Obtenir Météo' cliqué]
        LOADER[Affichage du Spinner / Loader]
        RENDER[Écran rafraîchi avec les T°C]
    end
    
    subgraph "Moteur Asynchrone (Non-Bloquant)"
        GEO[Demande des autorisations GeoAPI<br/>Callback Poussé]
        FETCH[Envoi de la requête HTTP GET<br/>api.openweathermap.org]
    end
    
    subgraph "L'Internet Extérieur"
        SERVER[(Serveur Météo Externe)]
    end
    
    UI --> LOADER
    UI -.-> GEO
    GEO -.-> FETCH
    FETCH -.-> SERVER
    SERVER -.->|Réponse JSON (200 OK)| FETCH
    FETCH -.-> RENDER
    
    style UI fill:#e3f3ff
    style LOADER fill:#fff4e5
    style RENDER fill:#e3ffe3
    style GEO fill:#ffe3e3,stroke:#ff0000,stroke-dasharray: 5 5
    style FETCH fill:#ffe3e3,stroke:#ff0000,stroke-dasharray: 5 5
    style SERVER fill:#eeeeee
```

<small>*C'est le génie du JavaScript Web. Pendant que la requête traverse l'océan atlantique pendant 400 millisecondes (Zone rouge pointillée), le navigateur de votre utilisateur ne "freeze" pas. Il peut continuer de cocher ses tâches sur le Widget Todo.*</small>

### Architecture Modulaire Industrielle

=== "Arbre des fichiers"

    !!! quote "**Structure de fichiers ciblée** : Une séparation stricte des Responsabilités (Separation of Concerns)."

    ```text
    /src
      /api
         weatherClient.js    => Ne fait QUE des requêtes réseau (fetch)
         jokeClient.js       => Interroge l'API Chuck Norris
      /components
         todoList.js         => S'occupe de dessiner le <ul> et <li>
         weatherWidget.js    => S'occupe de dessiner l'icône et la température
      /state
         todoStore.js        => Contient le cerveau CRUD (LocalStorage)
      /styles
         hub.css             => Design System
      main.js                => Le chef d'orchestre global
    ```

    <small>*Vous ne devez absolument **rien** exporter par défaut. Chaque fichier a un but unique. Un composant dessine. Un client fait du réseau. Un store retient dans la mémoire. Main.js attache les pièces du moteur entre elles.*</small>

=== "Exemple : L'API asynchrone (weatherClient.js)"

    !!! quote "**Code Asynchrone Moderne :** Les mots clés magiques `async` et `await` remplacent l'ancien système des `.then()` imbriqués."

    ```javascript
    // api/weatherClient.js
    const API_KEY = "VOTRE_CLE_API_GRATUITE";

    export async function fetchCityWeather(cityName) {
        try {
            // L'exécution "pause" ici sans bloquer le navigateur
            const response = await fetch(
                `https://api.openweathermap.org/data/2.5/weather?q=${cityName}&appid=${API_KEY}&units=metric`
            );

            // Gérer les cas où la ville n'existe pas (404 Not Found)
            if (!response.ok) throw new Error("Erreur de récupération météo");

            // Extraction asynchrone du format texte au format Objet JS
            const data = await response.json();
            return {
                temp: data.main.temp,
                weather: data.weather[0].main,
                icon: data.weather[0].icon
            };
        } catch (error) {
            console.error("Échec API : ", error.message);
            // Retour propre en cas de crash réseau 
            return null; 
        }
    }
    ```
    <small>*Le code ci-dessus est indestructible. Si le serveur de l'API tombe, ou si le nom de la ville est une erreur de frappe courante, le bloc `catch` va attraper l'exception et protéger le reste de l'application (Hub) d'un écran blanc de la mort.*</small>

=== "Exemple : Le State Manager CRUD (todoStore.js)"

    !!! quote "**Composant TodoList CRUD** : Créer (C), Lire (R), Mettre à jour (U), Détruire (D). Modèle de données universel."

    ```javascript
    // state/todoStore.js
    
    let todos = JSON.parse(localStorage.getItem('my_todos')) || [];

    // [C]REATE
    export function addTodo(title) {
        const newTodo = { id: Date.now(), text: title, isDone: false };
        todos.push(newTodo);
        saveState();
        return newTodo;
    }

    // [U]PDATE
    export function toggleTodo(id) {
        // Renvoie l'objet dont l'id correspond
        const todoSelected = todos.find(t => t.id === id); 
        if(todoSelected) {
            todoSelected.isDone = !todoSelected.isDone; // Inverse le true/false
            saveState();
        }
    }

    // [D]ELETE
    export function deleteTodo(id) {
        todos = todos.filter(t => t.id !== id);
        saveState();
    }

    /** Helper pour sauver la mutation d'état dans le local */
    function saveState() {
        localStorage.setItem('my_todos', JSON.stringify(todos));
    }
    ```

    <small>*Le composant d'UI (`todoList.js`) dans un autre fichier n'aura plus qu'à inclure `import { addTodo, deleteTodo } from './todoStore.js'` et réagir au clic des boutons poubelle !*</small>

## Structure des 6 Phases

!!! quote "Progression Logique : On prépare le Hub, on lance nos requêtes réseau Météo, puis on bétonne notre mémoire locale avec la Todolist."

<div class="cards grid" markdown>

- :fontawesome-solid-layer-group: **Phase 1 : Socle Industriel Vite**

    ---

    **Temps :** 1h  
    **Objectif :** Instancier le socle vide modulaire du projet depuis le terminal.
    **Livrables :**

    - Architecture à 3 widgets (Météo, Todos, Blagues API).
    - Design System en Grille Dashboard (Bento Grid conseillée en CSS pur).
    - Un header commun avec l'heure dynamique temps réel (`setInterval`).

    ---

    🟡 Intermédiaire

- :fontawesome-solid-cloud-sun: **Phase 2 : Asynchrone & Geolocation API**

    ---

    **Temps :** 1h30  
    **Objectif :** Obtenir les Droits du Navigateur et utiliser les Callbacks de haut niveau.  
    **Livrables :**

    - Invocation de `navigator.geolocation.getCurrentPosition`.
    - Gestion du Callback Succès (Extraction Lat/Lng).
    - Gestion du Callback Erreur (Utilisateur a refusé la position géographique ! Que faire ? -> Proposer une saisie manuelle).

    ---

    🔴 Avancé

- :fontawesome-solid-bolt: **Phase 3 : Fetch API & Parsing JSON (Widget Météo)**

    ---

    **Temps :** 2h  
    **Objectif :** Communiquer avec la planète terre.  
    **Livrables :**

    - Inscription au portail OpenWeatherMap pour obtenir votre Clé Privée.
    - Écriture exclusive du module `weatherClient.js`.
    - Maîtrise absolue du bloc `try ... catch` et construction saine des URLs.
    - Écoute de l'API, traitement du JSON massif, et injection sélective (Température, Humidité, Icône conditionnelle) dans le DOM Widget 1.

    ---

    🔴 Avancé

- :fontawesome-solid-list-check: **Phase 4 : Architecture State & CRUD (Widget Todos 1)**

    ---

    **Temps :** 2h  
    **Objectif :** Séparer la logique des Objets JS du rendu visuel.  
    **Livrables :**

    - Écriture du fichier `todoStore.js`. Le cerveau.
    - Création logique des 4 fonctions majeures : ajout, suppression, alternance booléenne `isDone`, lecture.
    - Synchronisation stricte au LocalStorage.

    ---

    🔴 Avancé

- :fontawesome-solid-desktop: **Phase 5 : Injection DOM (Widget Todos 2)**

    ---

    **Temps :** 1h30  
    **Objectif :** Traduire l'état de la mémoire en dessins HTML vivants.  
    **Livrables :**

    - Écriture du fichier composant `todoList.js`. Le peintre.
    - Ciblage de l'Input Formulaire "Ajouter tâche", "Enter => declenche la fonction create".
    - Vider la liste (`innerHTML = ''`) et repeindre chaque objet avec un `.map().join('')` ou création de `document.createElement('li')`.

    ---

    🔴 Avancé

- :fontawesome-solid-face-smile: **Phase 6 : Le Widget Bonus (Les Blagues de programmeur)**

    ---

    **Temps :** 1h  
    **Objectif :** Validations d'acquis de l'API Fetch.  
    **Livrables :**

    - Widget avec simple bouton de génération.
    - Utilisation d'une API gratuite sans authentification (ex: Official Joke API).
    - Gestion de l'état bloqué / de chargement : Le composant DOM est "Disabled" puis "Re-Enabled" lors du retour asynchrone pour éviter 200 clics successifs.

    ---

    🟡 Intermédiaire

</div>

## Prérequis et Environnement

<div class="cards grid" markdown>

- :fontawesome-solid-circle-check: **Indispensables**

    ---

    - [x] Un niveau absolu en manipulation d'URLs de Base (Query Params `?q=paris&appid=key`).
    - [x] L'architecture Globale des ES Modulaires (`import {} from './xx'`).
    - [x] Les Promesses (`Promise`) et les requêtes serveurs.
    - [x] Un environnement Node.js opérationnel.

- :fontawesome-solid-circle-half-stroke: **Recommandées**

    ---

    - 🟡 Conscience des performances réseau (Onglet Network du navigateur !).
    - 🟡 Sensibilité à la gestion de l'état (State UI).

- :fontawesome-solid-graduation-cap: **Apprises durant la création du projet**

    ---

    - [x] Requêtes REST asynchrones.
    - [x] Gestion centralisée d'une base de données factice `Array of Objects`.
    - [x] Modèle MVC (Modèle-Vue-Contrôleur) naissant.

</div>

## Checklist de Validation Certifiante

1. Récupère ta clé API météo sur un service tiers.
2. Formate l'ensemble de ton application avec la stack de compilation ultra-rapide Vite.js.
3. Développe widget par widget, jamais les trois en même temps. Un widget fini, un commit de fait.
4. **Validation Majeure :**
   - [ ] Si l'ordinateur de l'utilisateur n'est pas branché au réseau internet (`navigator.onLine == false`) ou si l'API est morte, l'application de TodoListe fonctionne TOUJOURS parfaitement.
   - [ ] L'application n'a **aucune** page blanche vide pendant que l'API cherche la météo. Un écran de squelette (Skeleton) ou un loader d'attente s'affiche de suite et disparaît après.
   - [ ] Toute mon architecture logicielle est découplée : je ne fais pas de `.innerHTML +=` au milieu de mon fichier de requête météo.

> Vous avez franchi la plus grande barrière du développement Front-End. Le Web Asynchrone. Vous lisez des données depuis une API, vous écrivez des données de l'interface vers le magasin d'État. Ce patron de conception universel vous offre maintenant la capacité sereine d'étudier un véritable Framework Industriel comme (React.js / Vue.js) ou de dériver vos compétences vers la persistance back-end avec des bases de données réelles (SQL) via PHP Laravel ou Go ! Et nous arrivons justement à la section suivante et cruciale... **Le Back-End (Go / PHP)**.
