---
description: "Installation de Laravel 11, configuration de l'environnement, intégration de Breeze et premier démarrage du serveur de développement."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 1 — Installation & Configuration

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Laravel 11"
  data-time="~45 minutes">
</div>

## Objectifs de la Phase 1

!!! info "Ce que vous allez faire"
    - Créer un nouveau projet Laravel 11 avec Composer
    - Installer et configurer Laravel Breeze (stack Blade + Tailwind)
    - Configurer la base de données MySQL dans `.env`
    - Exécuter les migrations d'authentification de base
    - Lancer le serveur de développement et valider l'installation

## 1. Création du Projet

```bash title="Installation"
# Créer le projet Laravel
composer create-project laravel/laravel projet-breeze

cd projet-breeze

# Installer Breeze
composer require laravel/breeze --dev

# Publier les vues, routes et contrôleurs Breeze (stack Blade)
php artisan breeze:install blade

# Installer les dépendances NPM et compiler les assets
npm install && npm run dev
```

## 2. Configuration `.env`

```dotenv title=".env — Configuration minimale"
APP_NAME="Projet Breeze"
APP_ENV=local
APP_KEY=              # Généré par artisan key:generate
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=breeze_db
DB_USERNAME=root
DB_PASSWORD=
```

```bash
# Générer la clé d'application
php artisan key:generate

# Créer la base de données (si elle n'existe pas)
mysql -u root -e "CREATE DATABASE breeze_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Exécuter les migrations
php artisan migrate
```

## 3. Validation de l'Installation

```bash
# Démarrer le serveur
php artisan serve
```

Ouvrez [http://localhost:8000](http://localhost:8000). Vous devriez voir la page d'accueil Laravel avec les liens **Login** et **Register** dans la navigation.

```bash
# Vérifier que les routes Breeze sont présentes
php artisan route:list | grep -E "(login|register|dashboard|password)"
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'installation de Breeze est déceptivement simple — `php artisan breeze:install` génère des dizaines de fichiers (vues, contrôleurs, routes, middleware) que vous **possédez** et pouvez modifier. Avant de passer à la phase suivante, prenez 10 minutes pour explorer `routes/auth.php` et `app/Http/Controllers/Auth/` : comprendre ce qui a été généré est aussi important que le faire fonctionner.

> [Phase 2 — Base de données et migrations avancées →](./phase2.md)
