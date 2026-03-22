---
description: "Phase 2 : Maîtriser l'API de Géolocalisation du navigateur. Gestion des Callbacks asynchrones, des autorisations utilisateur, et des états d'erreur."
icon: lucide/map-pin
tags: ["JAVASCRIPT", "ASYNC", "GEOLOCATION", "CALLBACKS"]
status: stable
---

# Phase 2 : Asynchrone & Geolocation API

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="1h30">
</div>

!!! quote "Objectif de la Phase"
    Pour afficher la météo, nous avons besoin de savoir où se trouve l'utilisateur. Historiquement, on demandait à l'utilisateur de taper son code postal. Aujourd'hui, les navigateurs modernes embarquent la `Geolocation API`. Mais attention : obtenir une position par satellite ou par triangulation IP n'est **pas immédiat**. Cela prend 2 à 5 secondes. C'est votre premier combat contre le "Temps".

## 1. La Nature de l'API Geolocation

Si le code Javascript s'exécute de haut en bas instantanément (Synchrone), que se passe-t-il si la ligne 3 a besoin de 4 secondes pour obtenir le GPS du téléphone ? Si le moteur JavaScript attendait (bloquait), le site entier "gèlerait".

Pour résoudre cela, JavaScript utilise le **modèle des Callbacks** (et plus tard, les Promesses). On donne au navigateur deux fonctions de rappel : "Quand tu auras fini dans 5 secondes, si ça s'est bien passé, exécute la fonction A. S'il y a eu une erreur, exécute la fonction B. Moi, en attendant, je continue d'exécuter la ligne 4."

## 2. Le Widget Weather : Première Brique

Créons notre deuxième composant, chargé d'orchestrer la Météo.

```javascript
/* src/components/weatherWidget.js */

export function initWeather() {
    const weatherContainer = document.getElementById('weather-content');
    if (!weatherContainer) return;

    // 1. On modifie l'UI immédiatement pour rassurer le visiteur.
    weatherContainer.innerHTML = `
        <div class="loader-spinner"></div>
        <p>Localisation en cours...</p>
    `;

    // 2. Vérification : le navigateur possède-t-il un GPS/Localisateur ?
    if (!navigator.geolocation) {
        weatherContainer.innerHTML = `<p class="error">Géolocalisation non supportée par votre navigateur.</p>`;
        return;
    }

    // 3. L'Appel Asynchrone
    // Syntaxe : navigator.geolocation.getCurrentPosition(successCallback, errorCallback)
    navigator.geolocation.getCurrentPosition(
        (position) => {
            // SUCCESS CALLBACK: V8 exécutera ceci dans le futur (quand le satellite répondra)
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            console.log(`Position trouvée : ${lat}, ${lon}`);
            weatherContainer.innerHTML = `<p>Position : ${lat.toFixed(2)}, ${lon.toFixed(2)}</p>`;
            
            // Prochaine étape : Envoyer ces coordonnées à l'API OpenWeather !
        },
        (error) => {
            // ERROR CALLBACK: L'utilisateur a cliqué sur "Bloquer" ou n'a pas de data.
            console.warn(`Erreur GPS : ${error.message}`);
            
            // Le plan de secours robuste (Fallback) :
            weatherContainer.innerHTML = `
                <p>Géolocalisation refusée.</p>
                <button id="retry-geo-btn" class="btn">Réessayer</button>
            `;
        }
    );
}
```

Importez `initWeather()` dans `main.js` et appelez-la juste en-dessous de `initClock()`.

## 3. Le Loader Visuel (Amélioration UX)

Pendant que `getCurrentPosition` cherche la position, le DOM affiche "Localisation en cours". Rendons cela professionnel en CSS dans `style.css`.

```css
/* Animation de rotation infinie */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loader-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-light); /* Gris clair */
  border-top: 4px solid var(--color-primary); /* Bleu électrique */
  border-radius: 50%; /* Fait un rond */
  animation: spin 1s linear infinite; /* Tourne pour toujours */
  margin: 0 auto 1rem auto;
}

/* On centre le contenu du conteneur météo pendant le chargement */
.widget-weather {
  text-align: center;
}
```

## Checklist de la Phase 2

- [ ] Je rafraîchis la page. Un anneau bleu tourne pendant une fraction de seconde avec le texte "Localisation en cours".
- [ ] Le navigateur me demande "Autoriser localhost:5173 à connaître votre position ?".
- [ ] Si je clique sur "Autoriser", la latitude et longitude s'affichent. L'horloge d'à côté a continué de tourner pendant tout ce processus !
- [ ] **Test de résilience** : Je révoque l'autorisation en haut à gauche de la barre d'adresse de Chrome (Icône cadenas > Restituer l'autorisation) et je rafraîchis. Le bloc affiche bien "Géolocalisation refusée".

!!! note "L'Event Loop en Action"
    Avez-vous remarqué ? Pendant que le navigateur attendait votre clic sur "Autoriser ou Bloquer" la géolocalisation, les secondes de votre Horloge (Phase 1) **continuaient de défiler**. C'est la prevue absolue du caractère non-bloquant de JavaScript. Le "Main Thread" dessine l'heure, pendant qu'un thread secondaire (WebAPI) gère la popup de position.

Nous avons les coordonnées de longitude et latitude ! Il est temps d'envoyer ces chiffres à un véritable serveur public et de formater le retour JSON. **Direction la Phase 3.**

[Passer à la Phase 3 : Fetch API & Parsing JSON →](phase3.md)
