---
description: "Installation de Laravel 11, intégration de Jetstream (Teams, 2FA) et configuration de Sanctum pour une API SPA."
icon: lucide/book-open-check
tags: ["JETSTREAM", "INSTALLATION", "TEAMS", "SANCTUM", "API"]
---

# Phase 1 : API Laravel Jetstream

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="1h30 - 2h">
</div>

## Objectif de la Phase

> Cette première phase consiste à poser les **fondations backend** de notre plateforme SaaS de Pentest. Contrairement au projet Breeze, nous n'allons pas utiliser les vues Blade fournies par Jetstream. Nous allons utiliser Jetstream uniquement comme une **API d'authentification robuste** (avec gestion des Teams, 2FA et Tokens API) qui sera consommée par notre frontend Angular 21.

!!! warning "Prérequis Techniques"
    Assurez-vous d'avoir PHP 8.2+, Node.js 22+, Composer et MySQL/PostgreSQL prêts sur votre machine.

## Étape 1.1 : Création du Projet Laravel

Nous commençons par instancier une nouvelle application Laravel vierge.

```bash
# Créer un nouveau projet Laravel nommé "saas-pentest"
composer create-project laravel/laravel saas-pentest

# Entrer dans le dossier
cd saas-pentest
```

## Étape 1.2 : Configuration de la Base de Données

Créez une base de données nommée `saas_pentest` dans votre gestionnaire (phpMyAdmin, TablePlus, ou ligne de commande).

Puis, ouvrez le fichier `.env` à la racine du projet et configurez la connexion :

```bash title=".env"
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=saas_pentest
DB_USERNAME=root
DB_PASSWORD=
```

!!! tip "Vérification"
    Exécutez `php artisan migrate:status` pour vérifier que la connexion à la base de données fonctionne correctement avant de poursuivre.

## Étape 1.3 : Installation de Laravel Jetstream

Jetstream est un starter kit complet qui intègre l'authentification forte, la gestion de profil, et la logique Multi-Tenancy (Teams).

```bash
# Installer le package Jetstream via Composer
composer require laravel/jetstream
```

Nous allons installer Jetstream avec **Livewire** (qui est la stack recommandée), mais nous l'utiliserons en mode **API** (grâce à Sanctum). Nous activons également la fonctionnalité **Teams**.

```bash
# Installer Jetstream avec la stack Livewire et activer les Teams
php artisan jetstream:install livewire --teams --api
```

### Que fait cette commande ?

<div class="grid cards" markdown>

-   :lucide-users:{ .lg .middle } **Teams**
    
    ---
    Génère les migrations et modèles pour la gestion d'équipes (`Team`, `TeamInvitation`, `Membership`). Permet l'isolation des données entre différents clients (multi-tenancy).

-   :lucide-key:{ .lg .middle } **API Tokens**
    
    ---
    Active la création de Personal Access Tokens (via Sanctum) directement depuis l'interface profil, idéal pour l'accès API tierces ou scanners automatisés.

</div>

### Compilation des assets et Migration

Bien que nous visions une architecture API, nous devons compiler les assets par défaut de Jetstream pour accéder à l'interface de connexion et de gestion de compte si nécessaire en fallback.

```bash
npm install
npm run build
php artisan migrate
```

## Étape 1.4 : Configuration de Sanctum pour une SPA

Puisque notre frontend (Angular 21) sera une Single Page Application (SPA) s'exécutant sur un domaine ou port différent en développement (ex: `localhost:4200`), nous devons configurer Sanctum pour l'authentification par cookies de session (Stateful).

Ouvrez le fichier `config/sanctum.php` et vérifiez/ajoutez le port de votre frontend dans les `stateful` domains :

```php title="config/sanctum.php"
'stateful' => explode(',', env('SANCTUM_STATEFUL_DOMAINS', sprintf(
    '%s%s%s',
    'localhost,localhost:3000,localhost:4200,127.0.0.1,127.0.0.1:8000,::1',
    Sanctum::currentApplicationUrlWithPort()
))),
```

Puis dans votre `.env`, assurez-vous d'avoir :

```bash title=".env"
SANCTUM_STATEFUL_DOMAINS=localhost:4200,localhost:8000,127.0.0.1:4200
SESSION_DOMAIN=localhost
```

## Étape 1.5 : Configuration des CORS

Pour que le frontend Angular puisse communiquer avec l'API Laravel, vous devez autoriser le partage des ressources cross-origin (CORS).

Ouvrez `config/cors.php` :

```php title="config/cors.php"
'paths' => ['api/*', 'sanctum/csrf-cookie', 'login', 'logout', 'register'],

'allowed_methods' => ['*'],

'allowed_origins' => ['http://localhost:4200'], // URL de l'app Angular

'allowed_origins_patterns' => [],

'allowed_headers' => ['*'],

'exposed_headers' => [],

'max_age' => 0,

'supports_credentials' => true, // OBLIGATOIRE pour l'auth SPA Sanctum
```

!!! danger "supports_credentials"
    L'option `'supports_credentials' => true` est **critique**. Sans elle, le navigateur refusera d'envoyer les cookies de session avec les requêtes AJAX/Fetch provenant d'Angular, rendant l'authentification impossible.

## Étape 1.6 : Activation de la Double Authentification (2FA)

Dans un contexte B2B (Cybersécurité), la **2FA est indispensable**. Jetstream l'intègre nativement, mais nous allons nous assurer qu'elle est bien activée.

Ouvrez `config/fortify.php` et vérifiez la section `features` :

```php title="config/fortify.php"
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    // Features::emailVerification(),
    Features::updateProfileInformation(),
    Features::updatePasswords(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
        // 'window' => 0,
    ]),
],
```

## Étape 1.7 : Tests avec Postman (Validation API)

Avant d'écrire la moindre ligne de frontend, nous devons valider que l'API Sanctum fonctionne.

1. **Démarrer le serveur local** : `php artisan serve`
2. **Obtenir le cookie CSRF** :
   Faites une requête `GET` sur `http://localhost:8000/sanctum/csrf-cookie`
   *Vous devriez recevoir des cookies (`XSRF-TOKEN` et `laravel_session`).*
3. **S'inscrire (Register)** :
   Faites une requête `POST` sur `http://localhost:8000/register` en incluant l'en-tête `X-XSRF-TOKEN` et le body :
   ```json
   {
       "name": "Pentest Admin",
       "email": "admin@pentest.com",
       "password": "password123",
       "password_confirmation": "password123"
   }
   ```
4. **Vérifier l'accès utilisateur** :
   Faites une requête `GET` sur `http://localhost:8000/api/user`. Vous devez recevoir l'objet JSON de votre utilisateur, incluant le `current_team_id`.

## Conclusion de la Phase 1

Vous avez posé les bases backend :
- ✅ **Laravel 11** est installé.
- ✅ **Jetstream** est configuré pour gérer les Équipes (Teams).
- ✅ **Sanctum** est prêt pour les requêtes stateful depuis notre futur frontend SPA.
- ✅ Les règles **CORS** sont paramétrées pour autoriser les flux de données croisés.

Dans la **Phase 2**, nous plongerons dans la modélisation de notre base de données métier (Missions, Findings, Évidences).
