---
description: "Phase 2 : Développement du Header global (Logo + Liens), Flexbox multi-résolutions, et intégration asynchrone du Menu Hamburger sans utiliser de JavaScript."
icon: lucide/menu
tags: ["CSS", "FLEXBOX", "CHECKBOX HACK", "RESPONSIVE"]
status: stable
---

# Phase 2 : Navbar & Menu Mobile "Zéro JS"

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h30">
</div>

!!! quote "Le Défi du Client"
    "C'est bien que le site s'affiche sur un écran géant de 27 pouces, mais la majorité de notre trafic (75%) provient d'Instagram et LinkedIn via des **Smartphones**. Notre logo doit être à gauche, et le menu doit être caché sous une petite icône de trois barres horizontales. Au clic, le menu apparaît."

C'est ici que la maîtrise absolue de l'Intégration Web prend tout son sens. Le comportement d'ouverture/fermeture d'un menu est un état (State). Puisque nous n'avons pas le droit au JavaScript, nous allons utiliser le moteur du HTML (Les formulaires) pour mémoriser cet état, via l'astuce légendaire du **Checkbox Hack**.

## 1. La balise nav et Flexbox

Ouvrez `index.html`. Immédiatement enfant de `<body>`, créez la section sémantique d'entête.

```html
<header class="main-header">
  <nav class="navbar">
    <!-- Le LOGO -->
    <a href="index.html" class="logo">
      Digital<span>Craft</span>
    </a>

    <!-- Le Burger Menu Icon (Label) et l'Input caché -->
    <input type="checkbox" id="menu-toggle" class="menu-toggle">
    <label for="menu-toggle" class="burger-icon">
      <!-- 3 traits pour faire l'icône -->
      <span></span>
      <span></span>
      <span></span>
    </label>

    <!-- La liste des vrais liens -->
    <ul class="nav-links">
      <li><a href="index.html">Accueil</a></li>
      <li><a href="services.html">Services</a></li>
      <li><a href="portfolio.html">Portfolio</a></li>
      <li><a href="#contact" class="btn btn-primary">Nous Contacter</a></li>
    </ul>
  </nav>
</header>
```

### Explication du flux

- Le `<header>` est le contenant complet.
- La `<nav>` contient 3 blocs majeurs (le Logo, le Mécanisme Burger, la Liste `ul`).
- Le bouton `.btn-primary` réutilise notre Variable CSS (voir plus bas).

## 2. Flexbox Mobile-First

Ouvrez `style.css`. Appliquons la structure de base, pensée pour l'écran de téléphone de l'utilisateur.

```css
/* --- HEADER GLOABAL --- */
.main-header {
  background-color: var(--color-light);
  box-shadow: var(--shadow-sm); /* Une ombre légère pour détacher le header */
  position: sticky; /* Reste collé en haut lors du défilement */
  top: 0;
  z-index: 1000; /* Passe par-dessus les autres images du site */
}

/* --- NAVIGATION FLEXBOX --- */
.navbar {
  display: flex;
  justify-content: space-between; /* Écarte le Logo à gauche, le Reste à droite */
  align-items: center; /* Centre verticalement si le logo est grand */
  padding: var(--spacing-md) var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

/* Le design du Logo */
.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-dark);
}

.logo span {
  color: var(--color-primary); /* Rendre le mot 'Craft' bleu électrique */
}
```

À ce stade, votre logo est à gauche, votre `<ul>` est à droite, mais le menu sur Téléphone prend trop de place et gâche l'affichage.

## 3. Le Checkbox Hack (Zéro JavaScript)

C'est la magie noire du CSS. Nous allons forcer le menu (`.nav-links`) à disparaître sous l'écran côté droit (`transform: translateX(100%)`). S'il clique sur l'icône burger (le `<label>`), ça coche l'input invisible. Grâce au CSS `input:checked`, on ramène le menu à `translateX(0)`.

```css
/* 1. On cache l'affreux bouton Vrai/Faux natif */
.menu-toggle {
  display: none;
}

/* 2. Style de l'icône Burger (Les 3 traits via span) */
.burger-icon {
  display: flex;
  flex-direction: column;
  gap: 5px;
  cursor: pointer; /* Montre une main au survol */
}

.burger-icon span {
  width: 25px;
  height: 3px;
  background-color: var(--color-dark);
  border-radius: 2px;
  transition: all 0.3s ease; /* Pour les animations fluides plus tard */
}

/* 3. Comportement du Menu sur Mobile */
.nav-links {
  position: absolute; /* Sort du flux flexbox, flotte au-dessus du site */
  top: 70px; /* En dessous du header */
  right: 0;
  background-color: var(--color-light);
  width: 100%; /* Prend tout l'écran en largeur */
  height: calc(100vh - 70px); /* Hauteur de l'écran téléphone moins l'entête */
  
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: var(--spacing-xl);
  gap: var(--spacing-lg);

  /* Le secret : on pousse le menu en dehors de l'écran vers la droite */
  transform: translateX(100%);
  transition: transform 0.4s ease-in-out; 
}

/* 4. LE DECLENCHEUR ASYNCHRONE ! 
 * Si (l'input est checké) ET (je sélectionne le .nav-links juste après lui en HTML)
 */
.menu-toggle:checked ~ .nav-links {
  transform: translateX(0); /* On le ramène sur l'écran */
}
```

### Le Résultat en Live
Testez ! Cliquez sur les 3 barres. Le menu glisse de la droite (100% à 0). Re-cliquez. Il disparaît. **Vous venez de recréer l'état (State) JavaScript de la fonction `toggle` exclusivement grâce à DOM/CSS.**

## 4. Breakpoint Desktop (`@media` Query)

Notre site mobile est parfait. Mais si vous étirez la fenêtre de Visual Studio Code ou Chrome à plus de 768 pixels, c'est chaotique : le Burger est visible, le menu nav-links est caché (translateX).

Nous devons créer l'exception "Ecran Large".

```css
/* --- GRAND ECRANS (Tablettes & Desktop) --- */
@media (min-width: 768px) {
  
  /* On cache l'icône Burger (Inutile sur Desktop) */
  .burger-icon {
    display: none;
  }

  /* On annule totalement les transformations tactiles du menu mobile */
  .nav-links {
    position: static; /* Rentre de nouveau dans le flux Flexbox du Header */
    height: auto;
    width: auto;
    flex-direction: row; /* Colonne -> Ligne ! */
    padding-top: 0;
    gap: var(--spacing-lg);
    background-color: transparent;
    transform: translateX(0); /* Toujours visible */
  }

  /* Effet survol propre sur ordinateur */
  .nav-links a:hover {
    color: var(--color-primary);
  }
}
```

## Checklist de la Phase 2

- [ ] L'inspecteur (F12) avec le bouton *Toggle Device Toolbar* confirme que le Header est fluide en version Tél et Desktop.
- [ ] Le Checkbox Hack fonctionne (affichage/masquage du fond blanc complet).
- [ ] La pseudo-classe `~` est bien comprise (Sélecteur Fraternel Général).

!!! tip "Pourquoi ça ne marche peut-être pas chez vous ?"
    Si `menu-toggle:checked ~ .nav-links` ne s'ouvre pas, vérifiez votre structure HTML. La balise `<ul class="nav-links">` **DOIT ABSOLUMENT** être placée au même niveau (être le petit frère) de la balise `<input>` dans l'arborescence du DOM, pas enfanté au fond d'une mauvaise Div.

[Passer à la Phase 3 : Accueil & Hero Call To Action →](phase3.md)
