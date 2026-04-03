---
description: "Architecture à grande échelle, gestion d'état global avec Alpine.store(), Persistence."
icon: lucide/mountain
tags: ["THEORIE", "ALPINE", "ARCHITECTURE", "PRODUCTION"]
---

# 05. Écosystème & Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Alpine 3.x"
  data-time="3 Heures">
</div>

!!! quote "Penser Logiciel, Penser Architecture"
    Au fur et à mesure que l'intranet de votre entreprise grossit, le code Alpine.js intégré dans votre HTML peut devenir lourd et indéchiffrable s'il n'est pas proprement isolé. Et que se passe-t-il si un composant isolé (`Panier utilisateur`) veut mettre à jour la pastille rouge de la `Barre de Navigation` ? Ce chapitre démontre comment le framework est capable d'abandonner ses habits d'outil léger pour rivaliser avec des architectures d'Apps Completes, de type Redux.

<br>

---

## 1. Déporter les Composants Réutilisables

Quand un composant (ex: un Carrousel d'images, ou une Modale avancée) requiert une trentaine de lignes de fonctions pures, il est inconcevable de le laisser traîner dans la balise HTML. `Alpine.data()` est le constructeur externe à appeler.

```html title="Découpler la logique métier du HTML"
<!-- 1. Le HTML redevient mince et sémantique -->
<div x-data="gestionDashboard()">
    <span x-text="userName"></span>
    <button @click="disconnect()">Déconnexion Rapide</button>
</div>

<script>
// 2. Le script peut être externalisé dans un main.js ou import ES6 !
document.addEventListener('alpine:init', () => {
    Alpine.data('gestionDashboard', () => ({
        userName: 'Administrateur Principal',
        tokenActive: true,
        
        disconnect() {
            this.tokenActive = false;
            alert("Réseau fermé.");
        }
    }))
})
</script>
```

_Utiliser le namespace global `Alpine.data` en dehors du cycle d'initialisation de l'arbre assure que le code Javascript est validable par le linter et factorisable par nom._

<br>

---

## 2. Les Stores : Le Coeur Global (Redux / VueX Style)

Les "Stores" sont le cœur nucléaire des applications modernes. Ils permettent de stocker des valeurs **omniprésentes** et utilisables sur toute la page par absolument n'importe quelle balise, même si elles n'ont aucun rapport entres-elles (Ex: L'état "Connecté", le thème Sombre, un Panier E-commerce).

```html title="Transmission d'État Universel"
<script>
document.addEventListener('alpine:init', () => {
    // Mon application crée une mémo globale appelée "auth"
    Alpine.store('auth', {
        isBanned: false,
        currentUser: null,
        
        banPlayer() {
            this.isBanned = true;
        }
    })
})
</script>

<!-- Vue 1: Le Menu affiché seulement si connecté !! -->
<nav x-data x-show="!$store.auth.isBanned">
    Bonjour Aventurier
</nav>

<!-- Vue 2: L'inventaire qui le bannit !! -->
<footer>
    <button x-data @click="$store.auth.banPlayer()">
        Lancer la triche (CheatEngine)
    </button>
</footer>
```

_Grâce à la propriété magique appelée avec son préfixe `$store.auth`, n'importe quelle balise HTML de la hiérarchie DOM y a accès. C'est l'équivalent léger de Context API dans ReactJS._

<br>

---

## 3. Ajout de Super-Pouvoirs avec les Plugins

Le Framework est architecturé par strates. Le fichier lourd originel ne charge que le coeur. Pour implémenter des fonctionnalités exceptionnelles, il est adossé à un catalogue de Plugins. Le plus puissant est **Persist**.

### Sauvegarder sur le disque dur avec Persist

Si votre utilisateur recharge sauvagement son navigateur, tout `x-data` est effacé de la mémoire RAM du PC. Avec le Plugin `@alpinejs/persist`, The variables s'inscrivent directement dans la base de données Cache du Navigateur Local Storage de manière chiffrée.

```html title="Injection du CDN Persist"
<head>
    <!-- LE PLUGIN AVANT LE COEUR !! -->
    <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.x.x/dist/cdn.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
```

```javascript title="Sauvegarde Magique"
Alpine.data('brouillonEditeur', () => ({
    // À chaque modification, Alpine écrit l'objet dans le disque dur de Windows
    contenu: Alpine.$persist('Rédigez votre article...').as('articleTemp'),
}))
```

<br>

---

## Conclusion Finale

!!! quote "Vous êtes prêts pour le Fullstack"
    Alpine.js ne rivalise pas avec les Single Page Applications conçues pour Spotify, et telle ne fut jamais son intention. C'est l'arme absolue pour rajouter des widgets, des dashboards connectés asynchrones et des interfaces tactiles sur des applications servies par Laravel, C# ou GoLang sans briser l'accessibilité ou détruire le SEO.

> L'heure de vérité est arrivée. Réinvestissez cette maîtrise théorique globale en réalisant les défis du laboratoire ! Rendez-vous sur les 3 modules de [Lab - Alpine](../projets/alpine-lab/index.md).
