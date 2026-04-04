---
description: "Série de projets de formation intenses pour maitriser Livewire 3"
icon: lucide/hammer
tags: ["PROJET", "LIVEWIRE", "LAB", "INDEX"]
---

# Livewire Lab

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire à ⚫ Expert"
  data-version="Livewire 3.x"
  data-time="20 Heures">
</div>

!!! quote "Au Front du Framework"
    La [Théorie Native](../../dev-cloud/frameworks/livewire/index.md) a posé les bases conceptuelles. Cependant, un développeur PHP senior ne se forge pas en lisant la documentation, il le devient en conceptualisant une architecture serveur complète. Dans ces *Ateliers Intensifs*, nous couvrirons les paradigmes de développement en commençant par manipuler de simples compteurs locaux, jusqu'à sécuriser un panneau d'administration total capable de résister à la prod.

<br>

---

## Modèles et Progession

Ce laboratoire a été extrait et reclassifié en 6 Projets progressifs pour simuler de réelles applications d'entreprises. Ne sautez pas les étapes, car l'architecture du composant global SaaS utilisera les compétences de pagination et d'Events vues au préalable.


### 🟢 Les Projets Fondamentaux

* **[Projet 1 : Calculatrice Interactive](./01-calculatrice.md)**  
  Comprendre "L'État". Initiez un petit composant réactif en une heure. Modifiez des variables et regardez votre résultat mathématique se dessiner tout seul en DOM.
  
* **[Projet 2 : Inscription et Validation en direct](./02-inscription-validation.md)**  
  Gérer "L'Erreur". Réceptionnez un Formulaire, testez-le avec une sécurité maximale, implémentez les Messages d'Erreur sans un seul rechargement URL (Post HTTP Fixe).


### 🟡 Les Projets Média & Données massives

* **[Projet 3 : Todo List Réactive CRUD](./03-todo-list.md)**  
  Piloter "L'Architecture". Les Create, Read, Update, Delete sur Base de Données Laravel couplés à l'interface Livewire. Fini JavaScript pour traiter des listes rapides à trier !
  
* **[Projet 4 : DataTable Admin Complexe](./04-datatable-crud.md)**  
  Aborder "La Big Data". Vous apprendrez le composant fétiche des SI : la Recherche Live dynamique + Tri par colonnes + Éléments conditionnels par Pagination Serveur AJAX. 


### 🔴 L'Ingénierie Avancée en Temps Réel

* **[Projet 5 : Chat Real-Time et Polling](./05-chat-realtime.md)**  
  S'affranchir du "Temps". Apprenez comment configurer votre application Laravel pour écouter le monde extérieur sans interaction de votre propre utilisateur, et utilisez Websocket & Listeners locaux pour re-synchroniser le front-end sans code !
  
* **[Projet 6 : Dashboard SAAS Total](./06-dashboard-saas.md)**  
  Atteindre "La Full-Page Component". Oubliez votre route standard, la Page Master entière (URL comprise) ne fait qu'un ! Intégration Alpine.js `($entangle)` pour les Modales ultra-rapides et gestion Sécurisée Middleware.

<br>

---

L'infrastructure matérielle réclamera impérativement un terminal en local et la présence d'un **PHP Artisan `Serve`** allumé avec sa BDD SQLite/MySQL branchée sur `.env` pour stocker vos créations.

> Accédez à l'éditeur et passez à [La Calculatrice Interactive](./01-calculatrice.md).
