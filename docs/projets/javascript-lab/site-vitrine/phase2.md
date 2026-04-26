---
description: "Phase 2 : Écoute d'événements asynchrones et manipulation du DOM. Remplacement du Hack CSS par un logique algorithmique claire et résiliente."
icon: lucide/mouse-pointer-click
tags: ["JAVASCRIPT", "DOM", "EVENTS", "REFACTORING"]
status: stable
---

# Phase 2 : Refactoring du Menu Mobile

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30 - 45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Objectif de la Phase"
    Le "Checkbox Hack" CSS (Phase 2 du projet précédent) fonctionnait bien, mais il avait une faille d'expérience utilisateur (UX) : le menu restait ouvert même si l'utilisateur cliquait sur le lien "Services". Or, un menu doit disparaître une fois qu'on a fait un choix. Le JavaScript va réparer cette lacune native.

## 1. Nettoyage du Code HTML/CSS Obsolète

Ouvrez `index.html`. Repérez la zone `<nav>` et supprimez la balise `<input type="checkbox">` ainsi que le tag `<label for="...">`. Nous les remplaçons par un véritable bouton métier, accessible pour les liseuses d'écran (`aria-label`).

```html
<header class="main-header">
  <nav class="navbar">
    <a href="index.html" class="logo">Digital<span>Craft</span></a>

    <!-- LE NOUVEL ELEMENT DOM -->
    <button class="hamburger-btn" aria-label="Ouvrir le menu">
      <span></span><span></span><span></span>
    </button>

    <ul class="nav-links">
      <li>...</li>
    </ul>
  </nav>
</header>
```

Ouvrez `style.css`.
Supprimez la règle complexe `.menu-toggle:checked ~ .nav-links`.
Créez plutôt une classe utilitaire "passive". C'est le JS qui se chargera de l'ajouter on de l'enlever au `<ul>` selon ses caprices.

```css
/* Anciennement .menu-toggle:checked ~ .nav-links */
/* Maintenant, c'est une classe d'état que JS manipulera */
.nav-links.nav-active {
  transform: translateX(0); 
}

/* L'animation de la croix du burger au clic (Optionnel mais classe !) */
.hamburger-btn.toggle-active span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger-btn.toggle-active span:nth-child(2) {
  opacity: 0;
}
.hamburger-btn.toggle-active span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
```

## 2. Le Cœur JS : Électrification du DOM

Le Navigateur web expose une API monumentale appelée **DOM (Document Object Model)**.
Ouvrez votre fichier métier `src/menuHandler.js` créé en Phase 1.

```javascript
/* src/menuHandler.js */

export function initMenu() {
    // 1. CIBLAGE (Querying)
    const burgerBtn = document.querySelector('.hamburger-btn');
    const navMenu = document.querySelector('.nav-links');
    const navItems = document.querySelectorAll('.nav-links a'); // Tous les <a> du menu

    // Sécurité: Si le script tourne sur une page sans menu, on quitte.
    if (!burgerBtn || !navMenu) return;

    // 2. ÉCOUTE DE L'ÉVÉNEMENT CLIC
    // Dès que le visiteur clique sur l'icône, j'appelle une fonction anonyme '() => {}'
    burgerBtn.addEventListener('click', () => {
        // .toggle() ajoute la classe si elle est absente, la retire si elle est présente.
        navMenu.classList.toggle('nav-active');
        burgerBtn.classList.toggle('toggle-active');
    });

    // 3. LA CORRECTION MÉTIER MANQUANTE EN HTML PUR
    // Quand l'utilisateur clique sur un lien, je DOIS forcer la fermeture du menu !
    navItems.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('nav-active');      // Ferme le tiroir
            burgerBtn.classList.remove('toggle-active'); // Remet les 3 barres
        });
    });
}
```

Prenez le temps d'observer le flux :
1. Le V8 Engine lie l'écouteur `addEventListener` et reste endormi.
2. Le visiteur clique avec sa souris.
3. V8 Engine se réveille.
4. Par l'API `classList.toggle()`, V8 va informer le moteur CSS qu'une classe a été ajoutée.
5. CSS réagit immédiatement et exécute son `transform: translateX(0)`. Le tiroir s'ouvre !

## Checklist de la Phase 2

- [ ] L'inspecteur Chromium F12 ne lève aucune erreur `null is not an object`.
- [ ] Le clic sur le Burger Panel ouvre et ferme le menu latéral à droite.
- [ ] Le clic sur un des mots du menu **entraîne obligatoirement la fermeture instantanée du menu** (contrairement au précédent exercice).

**Mission Accomplie**. Vous avez remplacé un hack sémantique peu fiable par de la véritable Algorithmique Asynchrone. L'interface est désormais connectée à un "cerveau".

C'est ce même concept (L'Event Listener couplé au State) qui vous permettra, dans la phase suivante, d'attaquer la bête noire des intégrateurs débutants : Le Dark Mode Local.

[Passer à la Phase 3 : Theme Manager & Dark Mode →](phase3.md)

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
