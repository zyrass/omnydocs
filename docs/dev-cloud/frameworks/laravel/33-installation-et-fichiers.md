---
description: "Installer proprement le starter-kit sans conflits avec un projet vide ou en cours."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "INSTALLATION", "TAILWIND"]
---

# Installation du Package

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. La Stratégie d'Installation

Idéalement il faut comprendre ce postulat : **Vous installez Breeze AVANT de taper la moindre d'idée de code**. Un site ou les tables "users", "sessions" se baladent déjà créerons d'importants conflits dont vous n'aurez plus la maitrise.

Pour la cause de l'éducation nous sommes donc obligés de vous annoncer deux approches théoriques de l'exercice que nous allons faire.

1. **Incremental** : On tire son package `composer require ...` dans cet espace de travail actuel, on casse tout le code qui gène, et on nettoie l'ancien en priant de rien oublier pour laisser place au nouveau.
2. **La Voix de La Raison : Fresh Install** : On recrée d'un coup de commande console un nouveau projet vierge dans un autre dossier. On installe le package. On vérifie que son layout fonctionne. **Et on Copy/Paste notre Modèle Projet et Modèle Controlleur** (Les dossiers de Workflows qu'on a écrit).

*Notre choix de lecture vers l'entreprise sur Zensical vous impose la 2eme option.*

<br>

---

## 2. Le Terminal de Base

Dans votre invite de commande locale, au même niveau que vos essais jusqu'à présent de la Masterclass :

```bash
# 1. On repart a 0.
composer create-project laravel/laravel omny-breeze
cd omny-breeze

# 2. On installe l'Environnement de développement du Package.
composer require laravel/breeze --dev

# 3. L'exécuteur propose ses saveurs : Blade pur ? React/Vue ? Livewire ?
php artisan breeze:install blade

# Options lors de l'installation :
# - Stack: blade
# - Dark mode support: yes ou no (Sauf si vous fuyiez Tailwindcss...)
# - Testing framework: Pest 
```

**Que s'est t'il passé derrière pendant les chargements serveurs ?**
* Les controleurs Auth sont créés et injectés dans App.
* Des composants et des Layouts Blade + Tailwind (CSS) + AlpineJS
* Ajout du Fichier de Routes auth.php 
* Tests Pest inclus fonctionnels..

<br>

---

## 3. Démarage d'Usine

Votre projet a besoin de NodeJS (`npm`) d'installé globalement sur votre machine pour compiler ce nouveau moteur Tailwind qu'a rajouté Breeze :

```bash
# Permet au Framework NPM de télécharger en local ses sources.
npm install 
# Lance la compilation Tailwind et l'affiche EN TEMPS REEL !
npm run dev
```

En parallèle sur un DEUXIEME Onglet Console, dans le dossier. Préparez votre SQLite et le serveur Artisan, et tout fonctionnera à neuf, en attendant d'être recopié par vos soins. 

```bash
touch database/database.sqlite
php artisan migrate
php artisan serve
```

Vous constaterez l'interface Tailwindcss et son dashboard tout neuf pré à vous accueillir avec un `Login` !
