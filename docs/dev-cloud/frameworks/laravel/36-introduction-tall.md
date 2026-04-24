---
description: "Dépasser la boucle de requêtes traditionnelles et unifier Vue et Serveur avec la Stack TALL."
icon: lucide/book-open-check
tags: ["LARAVEL", "TALL-STACK", "FRONTEND", "ARCHITECTURE"]
---

# L'Architecture TALL

<div
  class="omny-meta"
  data-level="🟢 Débutant/Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Introduction au module

!!! quote "Analogie pédagogique"
    _Au fil de ces Modules nous vous avons apprit les méthodes de bâtisseurs anciens. Les murs de parpaings montés à la main du Module 4. Sauf que les clients modernes réclament un peu de magie. Des fenêtres qui teintent la couleur avec la lumière du soleil. De la domotique... Pour l'heure votre serveur renvoie des pages "Textes" inertes... Mais que dire de la révolution **TALL** ? L'architecture pré-fabriquée réactive._

Le monde évolue. Les interfaces modernes demandent de l'interactivité sans que la page ai un comportement lourd de chargemment (rechargement total du navigateur F5 à chaque clic pour valider l'action)... Et Laravel n'est qu'un Back end Côté Serveur, son Javascript Vamilla inclus sur nos views n'est pas taillé pour ces manipulations chirurgicales.

Vous devez faire un choix. Accepter les technologies Modernes et complexes : Application SPA (Single Web Page : Avec React/VueJS) ou adopter **Le TALL Stack** ?

<br>

---

## 1. La Stack TALL

**TALL** est l'acronyme désignant l'assemblage officiel de Laravel pour contrer "MERN" (React) ou "MEAN" (Angular) de la façon la plus douce et abordable pour les amoureux natifs de PHP : 

- **T : Tailwind CSS** (Framework CSS Sans fichier css, avec des classes)
- **A : Alpine.js** (Mini Frame JavaScript minimaliste en HTml)
- **L : Livewire** (Composants Laravel PHP Réactifs temps réel ! MAGIE ! )
- **L : Laravel** (La base)

**Principe central de cette solution :** Rester dans l'écosystème Laravel en tapant du code Laravel, tout va générer le coté Front (JavaScript) en sous marin.

| Stack | Backend | Frontend | JavaScript Requis ? | Courbe d'Apprentissage |
|-------|---------|----------|---------------------|------------------------|
| **La Stack TALL** | Laravel | Blade + Livewire | **(minime)** Alpine.js | ⭐⭐ Modérée |
| **La Stack MERN** | Node.js | React | **OUI** (Lourd) | ⭐⭐⭐ Élevée |
| **Laravel + Vue** | Laravel | Vue.js | **OUI** (Moyen) | ⭐⭐⭐ Élevée |


## 1.2 Pourquoi refuser TALL selon le contexte !

**Vous adorez la stack que si :** Vous voulez être extrèment rapide au developpement, vous êtes une équipe majoritairement PHP/Backend, Votre interface s'apparente à des backoffoces basiques (boutiques, crud modéré) sans grande folie. La Maintenance est un plaisir car y'a qu'un espace : Laravel. Et le temps de DEV est redoutablement expéditif. Pas besoin de créer une API JSON pour la moindre action vers le visuel externe (React) !

**MAIS... C'est pas la Potion magique. Ne l'utilisez plus si :** 
Votre application requiert 100% de rapidité visuel (Dashboard boursier en temps réel), si la perte de connection paralyse le cache client (Offline-First crucial !). Et le comble du TALL : Ca ne sera **jamais porté pour Android et Ios de façon Native !!** (Ce qu'un Back Laravel en JSON associé à un ReactJS aurait pu réussir).

<br>

---

L'évolution est un choix de structure. Et comme vu au module 7, *Breeze* à lui seul vous a déjà propulsé dans la dimension (TA-L), Tailwind, Alpine, Laravel. Que sont les deux premiers outils `TA` qu'il vient de vous imposer ? Rendez-vous au chapitre TALL - Alpine.
