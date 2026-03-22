---
description: "Phase 1 : Mise en place d'un SOC (Separation of Concerns) granulaire avec Vite.js. Construction d'un Dashboard modulaire Grid et de l'Horloge temps réel."
icon: lucide/box
tags: ["JAVASCRIPT", "VITE", "ARCHITECTURE", "GRID"]
status: stable
---

# Phase 1 : Socle Modulaire & Dashboard

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2.0"
  data-time="1h00">
</div>

!!! quote "Objectif de la Phase"
    Un Hub Applicatif (Dashboard) n'est pas un site web descendant que l'on fait défiler. C'est un écran de contrôle massif affichant simultanément plusieurs blocs d'informations vitales. Votre mission est de poser les fondations architecturales strictes et de paver l'écran avec une Grille Bento (Bento Grid) pour recevoir les futurs widgets.

## 1. Topologie de l'Application

Vous l'aurez compris, on supprime tout et on repart de zéro avec la commande d'initialisation de projet.

```bash
# Dans votre dossier de projets
npm create vite@latest hub-personnel -- --template vanilla
cd hub-personnel
npm install
npm run dev
```

Nettoyez le répertoire généré et construisez immédiatement cette arborescence dans le dossier `/src` :

```text
hub-personnel/
├── index.html        (L'unique page HTML du Hub)
├── package.json      (Configuration du projet)
└── src/
    ├── main.js       (Chef d'orchestre global)
    ├── style.css     (Design System / Reset)
    ├── api/          (Réservé aux fonctions fetch)
    ├── components/   (Réservé aux fonctions dessinant le DOM)
    └── state/        (Réservé à la mémoire locale CRUD)
```

## 2. Le Canevas Dashboard (CSS Grid Bento)

Le "Bento Grid" (inspiré des boîtes-repas japonaises) est le standard UX 2026 pour les WebApps. C'est un système où les modules (Todo, Météo, News) ont des tailles différentes mais s'emboîtent parfaitement.

Ouvrez `index.html` :

```html
<body>
  <div class="dashboard-wrap">
    
    <!-- HEADER GLOBAL -->
    <header class="hub-header">
      <h1>Mon Hub Digital</h1>
      <div id="clock-widget" class="clock">00:00:00</div>
    </header>

    <!-- LA BENTO GRID -->
    <main class="bento-grid">
      <!-- Zone 1 : Météo -->
      <section class="widget widget-weather" id="weather-module">
        <h2>Météo Locale</h2>
        <div id="weather-content" class="widget-content">Loading...</div>
      </section>

      <!-- Zone 2 : Todolist Massive -->
      <section class="widget widget-todos" id="todo-module">
        <h2>Mes Tâches</h2>
        <div class="input-group">
            <input type="text" id="todo-input" placeholder="Ajouter une tâche...">
            <button id="add-todo-btn">Ajouter</button>
        </div>
        <ul id="todo-list" class="todo-items"></ul>
      </section>

      <!-- Zone 3 : Blagues développeurs (Le bonus) -->
      <section class="widget widget-jokes" id="joke-module">
        <h2>Détente</h2>
        <button id="get-joke-btn">Nouvelle Blague</button>
        <p id="joke-text" class="joke-text">Cliquer pour sourire.</p>
      </section>
    </main>

  </div>
  <script type="module" src="/src/main.js"></script>
</body>
```

Ouvrez `src/style.css`.
Mettez en place votre Reset Universel, votre `:root` contenant le Dark Mode, et créez la magie Bento :

```css
.dashboard-wrap {
  min-height: 100vh;
  padding: 2rem;
  background-color: #f1f5f9; /* Slate clair */
}

/* Grille Auto Responsive Magique */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  grid-auto-rows: 350px; /* Les widgets ont une taille stricte */
  gap: 1.5rem;
  margin-top: 2rem;
}

/* Sur les grands écrans, on dit que les Tâches prennent 2 colonnes */
@media (min-width: 1024px) {
  .widget-todos {
    grid-column: span 2;
  }
}

.widget {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  display: flex;
  flex-direction: column;
}
```

## 3. Premier Composant Vivant : L'horloge native

Pour vérifier que la tuyauterie Vite.js fonctionne, nous allons créer un widget d'horloge qui se met à jour toutes les secondes en manipulant le DOM depuis un fichier isolé.

Créez `src/components/clockWidget.js` :

```javascript
/* src/components/clockWidget.js */

export function initClock() {
    const clockElement = document.getElementById('clock-widget');
    if (!clockElement) return;

    // Fonction de rafraichissement direct
    const tick = () => {
        const now = new Date();
        // .toLocaleTimeString() gère automatiquement 14:02:44 au lieu de 14:2:44.
        clockElement.textContent = now.toLocaleTimeString('fr-FR');
    };

    // On affiche l'heure immédiatement à l'ouverture, sans attendre 1 seconde
    tick();

    // On dit au moteur Javascript : "Appelle tick() toutes les 1000 millisecondes"
    setInterval(tick, 1000);
}
```

Allez dans `main.js` :

```javascript
import './style.css'
import { initClock } from './components/clockWidget.js'

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    // Plus tard : initWeather() et initTodos() !
});
```

## Checklist de la Phase 1

- [ ] Votre dossier `src/` correspond au pixel près à l'architecture imposée.
- [ ] Le layout affiche au minimum 3 rectangles blancs sur fond gris, le widget Todo s'élargissant automatiquement sur grand écran de PC de Pureau.
- [ ] **L'heure s'écoule en haut de l'écran sans que le navigateur ne "charge". Le Javascript attaque le DOM en permanence !**

Parfait. Votre salle des machines est prête. Il est temps de brancher l'antenne extérieure vers les serveurs de la planète Terre.

[Passer à la Phase 2 : Asynchrone & Geolocation API →](phase2.md)
