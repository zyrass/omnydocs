---
description: "Phase 3 : Intégration du Dark Mode via un Theme Manager. Maîtrise avancée du Web Storage API (LocalStorage) pour sauvegarder les préférences utilisateur."
icon: lucide/moon
tags: ["JAVASCRIPT", "LOCALSTORAGE", "STATE", "CSS VARIABLES"]
status: stable
---

# Phase 3 : Theme Manager (Dark Mode)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le "Dark Mode" n'est plus un simple gadget. C'est une obligation d'accessibilité visuelle. Mais le défi est algorithmique : si l'utilisateur met le site en noir pour ne pas se brûler les yeux à 2h du matin, puis clique sur "Contact"... Il passe sur une autre page. Comment dire à cette page page **avant même de s'afficher** : "Hé, ce type préfère le noir !" ? Bienvenue dans la manipulation d'état système avec l'API Web `LocalStorage`.

## 1. Mettre en place le Bouton Bascule (UI)

Ouvrons `index.html`. Dans notre header, ajoutons un simple bouton ou une simple case à cocher pour "basculer" le thème sombre. Placez le juste à côté du bouton Hamburger.

```html
<!-- DANS LE HEADER HTML -->
<button class="theme-toggle" aria-label="Changer le thème">
    <!-- Un icône soleil par défaut -->
    <svg viewBox="0 0 24 24" fill="none" class="sun-icon">
        <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/>
        <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor"/>
        <!-- (suite de l'icône, cf ressources) -->
    </svg>
</button>
```

## 2. Assombrir les Variables du Design System

Allez dans `style.css`.
Actuellement, votre site repose sur ces variables à la racine `:root` :

```css
:root {
  --color-light: hsl(0, 0%, 98%);  /* Blanc */
  --color-dark: hsl(220, 20%, 15%);  /* Noir */
}
```

La stratégie est la suivante : on va créer un nouveau scope (portée) qui va **écraser** ces variables si et seulement si la balise `<body>` possède la classe `.dark-mode`.

```css
/* L'état sombre de votre Design System */
body.dark-mode {
  /* Inversion radicale des variables fondamentales ! */
  --color-light: hsl(220, 20%, 15%); /* Ce qui était blanc devient noir profond */
  --color-dark: hsl(0, 0%, 98%);   /* Ce qui était texte noir devient texte blanc */
  
  /* Vous pourriez aussi assombrir le primary (Bleu), baisser la saturation... */
  --color-border: hsl(220, 10%, 25%);
}

body {
  /* On ajoute une transition pour le style de la page pour éviter le flash brut */
  transition: background-color 0.4s ease, color 0.4s ease;
}
```

## 3. Le Cerveau : ThemeManager.js

C'est ici que l'ingénierie opère. Dans `src/`, créez `themeManager.js`.

```javascript
/* src/themeManager.js */

export function initTheme() {
    const btn = document.querySelector('.theme-toggle');
    const THEME_KEY = 'digitalcraft_theme'; // Une constante propre pour le dico de stockage

    // 1. LECTURE : Interroger le disque dur au démarrage.
    // L'ordinateur du visiteur retient-il la clé 'digitalcraft_theme' ?
    const savedTheme = localStorage.getItem(THEME_KEY);

    // Si la valeur stockée était "dark", on force l'application de la classe
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }

    // 2. ÉCRITURE : Écouteur de l'Événement clic
    if (!btn) return;
    
    btn.addEventListener('click', () => {
        // Ajoute "dark-mode" si absent, retire si présent
        document.body.classList.toggle('dark-mode');

        // Mais n'oublions pas de sauvegarder ce choix !
        // Si le body possède la classe dark-mode, on sauvegarde "dark", sinon "light".
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem(THEME_KEY, 'dark');
        } else {
            localStorage.setItem(THEME_KEY, 'light');
        }
    });
}
```

N'oubliez pas d'importer `initTheme()` dans votre `main.js` pour l'exécuter.

## L'Épreuve du Flash Blanc

Ceci est la différence entre un Dev Classique et un Ingénieur Front-End.

Si l'utilisateur recharge la page, le navigateur va :
1. Lire le HTML.
2. Dessiner le Body d'origine (Donc Blanc).
3. Charger le CSS.
4. Au bout d'un quart de seconde, lire `main.js`.
5. Lire le LocalStorage.
6. Dire "Ah, il est en dark mode !", rajouter la classe au Body.

Résultat ? **Pendant 0.2s, on brûle les yeux du visiteur avec un écran immaculé.**
Pour contrer cela, nous devons exécuter la partie "Lecture" de notre script **AVANT** même l'apparition graphique.

Prenez cette fonction utilitaire, et placez-la directement dans l'entête `<head>` de votre `index.html` via une balise `<script>`. (Hors de logiques modulaires différées de Vite).

```html
<head>
    <!-- ... vos metas et CSS ... -->

    <!-- SCRIPT DE BLOQUAGE DU RENDU. Exécuté INSTANTANÉMENT avant le <Body> -->
    <script>
        // Si l'ordi connait le dark mode, injecte immédiatement la classe.
        if (localStorage.getItem('digitalcraft_theme') === 'dark') {
            document.documentElement.classList.add('dark-mode'); // <html> tag
        }
    </script>
</head>
```
*Note : Assurez-vous alors de cibler `:root.dark-mode` ou `html.dark-mode` dans votre CSS si vous appliquez la classe à la balise `<html>` via `documentElement`.*

## Checklist de la Phase 3

- [ ] Je clique sur mon bouton de mode "Sombre", les variables CSS basculent, mon site devient noir.
- [ ] J'ouvre l'**Inspecteur (F12) > Application > Local Storage > `http://localhost:5173`**. Je vois bien mon dictionnaire avec la Clé `digitalcraft_theme` et la valeur `dark`.
- [ ] Le crash test ultime : Je clique sur 'Sombre', je ferme complètement l'onglet. J'ouvre un nouvel onglet, je charge mon site. **S'il se lance en sombre dès la milliseconde 0, j'ai réussi.**

[Passer à la Phase 4 : Filtres Portfolio (Data Object Array) →](phase4.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
