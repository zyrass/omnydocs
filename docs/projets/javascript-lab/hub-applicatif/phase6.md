---
description: "Phase 6 : Création du composant Joke API. Exercice de validation autonome des acquis sur l'asynchrone, la gestion du loader d'interface, et les Promise."
icon: lucide/smile
tags: ["JAVASCRIPT", "FETCH", "API", "PROMISE"]
status: stable
---

# Phase 6 : Widget Blagues API (Bonus Rest)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le Widget Météo nécessitait une clé API (Phase 3). Le Widget Toto liste exigeait la conception d'un Store Local (Phase 4). Ce dernier Widget est votre "Épreuve Blanche". Vous devez créer de A à Z un client HTTP pour une API publique *sans authentification*, et rafraîchir le texte du DOM au clic.

## 1. L'API Publique Objective

Nous allons utiliser l'API officielle : `https://official-joke-api.appspot.com/random_joke`.

Si vous copiez cette URL dans votre navigateur, vous obtiendrez un JSON très simple (Contrairement au monolithe de 500 lignes de OpenWeather) :

```json
{
  "type": "programming",
  "setup": "Why do programmers always mix up Halloween and Christmas?",
  "punchline": "Because Oct 31 equals Dec 25.",
  "id": 27
}
```

## 2. Le Client Réseau

De manière 100% autonome, créez le fichier `src/api/jokeClient.js`.

```javascript
/* src/api/jokeClient.js */

export async function fetchRandomJoke() {
    try {
        const response = await fetch('https://official-joke-api.appspot.com/random_joke');
        
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // On retourne la fusion de la blague (Setup + Punchline)
        return `${data.setup} ... ${data.punchline}`;
        
    } catch (error) {
        console.error("Impossible de récupérer la blague", error);
        return "Erreur serveur. Pas de blague pour l'instant !";
    }
}
```

## 3. Le Widget Controller

Créez le composant UI `src/components/jokeWidget.js`.

**Défi spécifique** : L'utilisateur ne doit pas pouvoir cliquer "50 fois par seconde" sur le bouton "Nouvelle blague", sinon il risque de se faire bannir de l'interface publique (HTTP 429 Too Many Requests). Vous devez **désactiver le bouton** (Disable) tant que l'appel réseau The Promise n'est pas terminé (Résolu ou Rejeté).

```javascript
/* src/components/jokeWidget.js */
import { fetchRandomJoke } from '../api/jokeClient.js';

export function initJokes() {
    const btnParams = document.getElementById('get-joke-btn');
    const textParams = document.getElementById('joke-text');

    if (!btnParams || !textParams) return;

    // Définition de l'action asynchrone assignée au bouton
    const loadJoke = async () => {
        
        // 1. Verrouillage de l'UI (Désactivation du bouton et texte d'attente)
        btnParams.disabled = true;
        btnParams.textContent = "Téléchargement...";
        textParams.textContent = "...";

        // 2. Le Facteur réseau est lancé ! Le Thread principal attend le Retour.
        const jokeString = await fetchRandomJoke();

        // 3. Libération de l'UI et Collage du texte
        textParams.textContent = jokeString;
        btnParams.textContent = "Nouvelle Blague";
        btnParams.disabled = false;
    };

    // Chargement de la première blague dès l'ouverture du Hub
    loadJoke();

    // Abonnement aux clics suivants
    btnParams.addEventListener('click', loadJoke);
}
```

N'oubliez pas d'importer `initJokes()` dans votre ultime chef d'orchestre `main.js`.

## L'Art Majeur : Les Promesses Concurrentes

Pour les curieux, que se passe-t-il dans `main.js` actuellement ?

```javascript
document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initWeather(); // Fonction asynchrone qui prend 2 secondes
    initTodos();
    initJokes();   // Fonction asynchrone qui prend 1 seconde
});
```

Si ces fonctions étaient "bloquantes" (synchrones), l'écran resterait blanc pendant `2 + 1 = 3 secondes`.
Parce qu'elles utilisent le modèle asynchrone (via leurs propres callbacks internes), le navigateur lance la météo "dans le vide", puis lance la blague "dans le vide", et affiche la Todolist instantanément. Quand la blague revient 1 seconde plus tard, le texte s'affiche. Quand la météo revient 2 secondes plus tard, l'icône s'affiche. 

C'est l'Architecture Parallèle asynchrone du Navigateur.

## 🏁 Checklist de la Phase 6 & Mission Complète

- [ ] L'ajout de ces 2 nouveaux fichiers n'a pas déclenché d'erreur rouge `Import Module Error`.
- [ ] Le clic consécutif rapide sur "Nouvelle Blague" est physiquement impossible, car le bouton devient "Grisé/Disabled" pendant l'appel vers l'API.

**FÉLICITATIONS ! 🎉**

Votre Hub Applicatif personnel est achevé. Il agrège la temporalité locale (`setInterval`), le State Local (`localStorage`), les APIs protégées par token asynchrone (`OpenWeather fetch`), et les APIs publiques gérées intelligemment.
Vous possédez désormais l'intégralité du bagage intellectuel et conceptuel exigé des Développeurs Front-End natifs. La prochaine grande barrière vous mènera à la conception de vos PROPRES API... **Bienvenue dans le développement Back-End PHP, Laravel, ou Go/Gin.**

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
