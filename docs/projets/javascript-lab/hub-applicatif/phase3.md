---
description: "Phase 3 : Fetch API. Comment dialoguer avec un serveur distant, traiter une chaîne JSON complexe, encadrer les erreurs via Try/Catch, et dessiner le résultat météo."
icon: lucide/cloud-lightning
tags: ["JAVASCRIPT", "FETCH", "JSON", "API", "ASYNC AWAIT"]
status: stable
---

# Phase 3 : Fetch API & Widget Météo

<div
  class="omny-meta"
  data-level="🔴 Avancé (Certifiant)"
  data-version="2.0"
  data-time="2 Heures">
</div>

!!! quote "Objectif de la Phase"
    Le navigateur connaît votre position (Latitude, Longitude). Mais il ne connait pas la météo de cette position. Il faut envoyer un "coursier" virturel (La requête HTTP GET) au serveur d'OpenWeatherMap pour lui poser la question : "Quelle température fait-il au point X, Y ?".
    Ici, nous passons du Callback classique (Phase 2) à la syntaxe moderne **Async / Await**.
    
## 1. Création de sa Clé API Publique

Les serveurs météo coûtent cher à entretenir. L'entreprise *OpenWeather* limite volontairement l'accès à ses données pour éviter que votre Hub applicatif ne les "Spam" d'un million de requêtes par seconde (DDoS).

1. Allez sur **[OpenWeatherMap](https://openweathermap.org/)** et créez un compte.
2. Allez dans l'onglet **My API Keys**.
3. Copiez la clé secrète générée (Une grande chaîne de lettres et chiffres ex: `a1b2c3...`).

## 2. Le Client Réseau (Le Facteur)

Dans le dossier `src/api/`, créez le fichier `weatherClient.js`. Ce fichier n’interagira **jamais** avec le `<div id="...">` HTML. Son seul métier, c'est de parler au serveur météo, d'attendre la réponse, de la nettoyer, et de la renvoyer. C'est l'essence du pattern **Separation of Concerns**.

```javascript
/* src/api/weatherClient.js */

// VOTRE clé personnelle. Jamais la mienne.
const API_KEY = "REMPLACEZ_CECI_PAR_VOTRE_CLE";

// Le mot-clé async transforme la fonction. Elle renverra TOUJOURS une Promesse.
export async function fetchWeatherByCoords(lat, lon) {
    // Construction de l'URL exacte demandée par la documentation d'OpenWeather
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=fr`;

    try {
        // AWAIT : Fais pause sur la Ligne 13 tant que l'Atlantique n'a pas été traversée 
        const response = await fetch(url);
        
        // Sécurité : Est-ce qu'Openweather m'a dit 401 Unauthorized ? (Clé API fausse)
        // Ou 429 Too Many Requests ?
        if (!response.ok) {
            throw new Error(`Erreur réseau: Statut ${response.status}`);
        }

        // AWAIT : On a un énorme bloc de texte (Payload), on le parse en Objet JS exploitable
        const data = await response.json();
        
        // On purge la donnée inutile pour ne renvoyer que le strict nécessaire
        return {
            city: data.name,
            temp: Math.round(data.main.temp),       // Ex: 14.532 -> 15
            description: data.weather[0].description, // Ex: "ciel clair"
            iconCode: data.weather[0].icon          // Ex: "01d"
        };
        
    } catch (error) {
        // Ce catch s'active SI et SEULEMENT SI le fetch() a crashé 
        // ou si l'API a retourné une erreur manuelle (throw).
        console.error("Échec Weather Client:", error);
        return null; // Renvoie 'vide' poliment au lieu de faire imploser le site.
    }
}
```

## 3. L'Assemblage (Relier le GPS, le Réseau et l'UI)

Retournons dans le fichier d'interface `src/components/weatherWidget.js` (issu de la Phase 2) pour lier ce nouveau Client Réseau.

```javascript
/* src/components/weatherWidget.js */
import { fetchWeatherByCoords } from '../api/weatherClient.js';

export function initWeather() {
    const weatherContainer = document.getElementById('weather-content');
    if (!weatherContainer) return;

    weatherContainer.innerHTML = '<div class="loader-spinner"></div><p>Localisation...</p>';

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            // SUCCESS
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            // On a le GPS. On modifie l'UI pour dire "Téléchargement..."
            weatherContainer.innerHTML = '<div class="loader-spinner"></div><p>Analyse atmosphérique...</p>';

            // On utilise MAINTENANT notre facteur asynchrone (Le fameux await !)
            const weatherData = await fetchWeatherByCoords(lat, lon);

            if (weatherData) {
                // On peint le DOM final si et seulement si l'API a répondu poliment :
                const iconUrl = `https://openweathermap.org/img/wn/${weatherData.iconCode}@2x.png`;
                weatherContainer.innerHTML = `
                    <div class="weather-result">
                        <h3>${weatherData.city}</h3>
                        <img src="${iconUrl}" alt="${weatherData.description}" class="weather-icon">
                        <div class="weather-temp">${weatherData.temp}°C</div>
                        <p class="weather-desc">${weatherData.description}</p>
                    </div>
                `;
            } else {
                weatherContainer.innerHTML = `<p class="error">Impossible de récupérer la météo.</p>`;
            }
        },
        (error) => {
            weatherContainer.innerHTML = `<p>Géolocalisation refusée.</p>`;
        }
    );
}

```

Et voilà ! L'implémentation est totale. Le visiteur accorde la permission, la popup disparaît, l'écran tourne en bleu, puis les températures de son quartier s'affichent avec l'icône HD et descriptive de la météo.

## Checklist de la Phase 3 & Résilience

- [ ] L'inspecteur réseau (F12 > Network) me montre *en rouge* la requête URL (`api.openweathermap.org/data/2...`) s'exécuter après ma validation GPS.
- [ ] La température de la ville s'affiche (Si elle affiche 290 au lieu de 17°C, vous avez oublié le paramètre `&units=metric` dans l'URL de l'API !).
- [ ] Modifiez volontairement votre clé `API_KEY` en `xxxxxx` dans le fichier `weatherClient.js`. **Sauvegardez**.
- [ ] Que se passe-t-il sur votre site ? Un écran blanc qui plante ? Non. **Un message élégant "Impossible de récupérer la météo"** s'affiche car le Catch a fonctionné. C'est l'architecture anti-fragile. 

Le composant Météo est achevé. L'Horloge également.
Dans les deux cas, le cycle de vie est géré par un automate naturel sans sauvegarde sur l'ordinateur. Le prochain très gros composant réclame une toute autre logique métier. **La Todo List CRUD**.

[Passer à la Phase 4 : Architecture State & CRUD →](phase4.md)
