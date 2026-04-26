---
description: "Installation Laravel 11, intégration Breeze, configuration base de données et premiers pas avec l'authentification."
icon: lucide/package-open
tags: ["BREEZE", "INSTALLATION", "LARAVEL", "SETUP"]
---

# Phase 1 : Installation & Configuration Base

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="30-45 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Créer l'authentification avec Breeze, c'est comme installer des serrures pré-certifiées dans une nouvelle maison. Plutôt que de fondre votre propre métal pour forger une clé, vous utilisez un standard industriel éprouvé, ce qui vous permet de vous concentrer sur la construction des vraies pièces de la maison._

## Introduction à l'Installation et sa Configuration

### Vue d'Ensemble de la Phase

> Cette première phase pose les **fondations techniques** de votre projet. Vous allez installer Laravel 11, configurer l'environnement de développement local, créer la base de données, puis installer Laravel Breeze pour obtenir un système d'authentification complet et fonctionnel. Cette étape est cruciale : un environnement mal configuré peut générer des erreurs difficiles à déboguer par la suite.

> À l'issue de cette phase, vous disposerez d'une application Laravel vierge avec authentification opérationnelle (**inscription**, **connexion**, **réinitialisation mot de passe**). Vous pourrez créer votre premier compte utilisateur et accéder au dashboard Breeze, confirmant ainsi que tout fonctionne correctement avant d'attaquer la logique métier du blog.

!!! warning "Prérequis à Vérifier avant de commencer, assurez-vous d'avoir installé PHP 8.1+, Composer, Node.js 22+, et votre environnement de développement local (Herd, Sail, ou stack native). Reportez-vous à la section **Prérequis et Environnement** si nécessaire."

## Étape 1.1 : Créer le Projet Laravel

Laravel propose désormais **deux méthodes officielles** pour créer un projet : via **Composer** (méthode universelle) ou via **l'installeur Laravel** (plus rapide). Nous utiliserons Composer car il fonctionne sur tous les systèmes sans installation préalable.

=== ":fontawesome-brands-windows: Windows"

    ```bash
    # Ouvrir PowerShell ou Terminal Windows
    # Naviguer vers le dossier où créer le projet (exemple : Bureau)
    cd C:\Users\VotreNom\Desktop
    
    # Créer le projet Laravel nommé "blog-breeze"
    composer create-project laravel/laravel blog-breeze
    
    # Patienter pendant l'installation (1-3 minutes selon connexion)
    # Composer télécharge Laravel et toutes ses dépendances
    
    # Naviguer dans le dossier projet
    cd blog-breeze
    ```

    **Vérification :**
    ```bash
    # Vérifier la version Laravel installée
    php artisan --version
    # Résultat attendu : Laravel Framework 11.x.x
    ```

=== ":fontawesome-brands-apple: macOS"

    ```bash
    # Ouvrir Terminal
    # Naviguer vers le dossier où créer le projet (exemple : Documents)
    cd ~/Documents
    
    # Créer le projet Laravel nommé "blog-breeze"
    composer create-project laravel/laravel blog-breeze
    
    # Patienter pendant l'installation (1-3 minutes selon connexion)
    # Composer télécharge Laravel et toutes ses dépendances
    
    # Naviguer dans le dossier projet
    cd blog-breeze
    ```

    **Vérification :**
    ```bash
    # Vérifier la version Laravel installée
    php artisan --version
    # Résultat attendu : Laravel Framework 11.x.x
    ```

=== ":fontawesome-brands-linux: Linux"

    ```bash
    # Ouvrir Terminal
    # Naviguer vers le dossier où créer le projet (exemple : home)
    cd ~/
    
    # Créer le projet Laravel nommé "blog-breeze"
    composer create-project laravel/laravel blog-breeze
    
    # Patienter pendant l'installation (1-3 minutes selon connexion)
    # Composer télécharge Laravel et toutes ses dépendances
    
    # Naviguer dans le dossier projet
    cd blog-breeze
    ```

    **Vérification :**
    ```bash
    # Vérifier la version Laravel installée
    php artisan --version
    # Résultat attendu : Laravel Framework 11.x.x
    ```

<small>*La commande `composer create-project` génère une nouvelle application Laravel avec toute la structure de dossiers (`app/`, `database/`, `resources/`, `routes/`, etc.) et installe automatiquement les dépendances PHP définies dans `composer.json`. Le nom `blog-breeze` devient le nom du dossier projet et peut être personnalisé selon vos préférences.*</small>

!!! success "Résultat Attendu"
    À ce stade, vous devez voir un dossier `blog-breeze/` contenant toute la structure Laravel. La commande affiche en fin d'exécution : `Application ready! Build something amazing.`

## Étape 1.2 : Créer la Base de Données

!!! quote "Laravel nécessite une base de données relationnelle pour stocker les utilisateurs, articles, catégories et commentaires. Vous pouvez utiliser **MySQL 8.0+** ou **MariaDB 10.5+** indifféremment."

> **MariaDB est un fork open-source de MySQL avec compatibilité quasi-totale**).

=== ":fontawesome-solid-database: MySQL"

    **Méthode 1 : Via ligne de commande**
    
    ```bash
    # Se connecter au serveur MySQL (mot de passe root demandé)
    mysql -u root -p
    
    # Une fois connecté, créer la base de données
    CREATE DATABASE blog_breeze CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
    # Vérifier la création
    SHOW DATABASES;
    # Vous devez voir "blog_breeze" dans la liste
    
    # Quitter MySQL
    EXIT;
    ```
    
    **Méthode 2 : Via phpMyAdmin / Adminer**
    
    1. Ouvrir phpMyAdmin dans votre navigateur (généralement `http://localhost/phpmyadmin`)
    2. Cliquer sur l'onglet **"Bases de données"**
    3. Dans le champ **"Créer une base de données"**, saisir : `blog_breeze`
    4. **Interclassement** : Sélectionner `utf8mb4_unicode_ci`
    5. Cliquer **"Créer"**

=== ":fontawesome-solid-database: MariaDB"

    **Méthode 1 : Via ligne de commande**
    
    ```bash
    # Se connecter au serveur MariaDB (mot de passe root demandé)
    mariadb -u root -p
    # OU
    mysql -u root -p
    
    # Une fois connecté, créer la base de données
    CREATE DATABASE blog_breeze CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
    # Vérifier la création
    SHOW DATABASES;
    # Vous devez voir "blog_breeze" dans la liste
    
    # Quitter MariaDB
    EXIT;
    ```
    
    **Méthode 2 : Via phpMyAdmin / Adminer**
    
    1. Ouvrir phpMyAdmin dans votre navigateur (généralement `http://localhost/phpmyadmin`)
    2. Cliquer sur l'onglet **"Bases de données"**
    3. Dans le champ **"Créer une base de données"**, saisir : `blog_breeze`
    4. **Interclassement** : Sélectionner `utf8mb4_unicode_ci`
    5. Cliquer **"Créer"**

<small>*Le charset `utf8mb4` est obligatoire pour supporter les emojis et caractères spéciaux (arabe, chinois, etc.). L'interclassement `utf8mb4_unicode_ci` garantit des comparaisons de chaînes insensibles à la casse et conformes aux standards Unicode. Sans cette configuration, vous risquez des erreurs d'encodage lors du stockage de caractères non-latins.*</small>

!!! tip "Pourquoi utf8mb4 et pas utf8 ?"
    L'ancien charset `utf8` de MySQL est limité à 3 octets par caractère, ce qui exclut certains emojis modernes (4 octets). Laravel impose `utf8mb4` par défaut depuis la version 5.4 pour éviter ces limitations.

## Étape 1.3 : Configurer le Fichier `.env`

> Le fichier `.env` (situé à la racine du projet) stocke toutes les **variables d'environnement** : connexion base de données, clés API, paramètres mail, etc. C'est le seul fichier à personnaliser pour chaque environnement (développement, production).

**Ouvrir le fichier `.env` dans votre éditeur de code** et modifier les sections suivantes :

```bash title=".env"
# =========================================
# Configuration Application
# =========================================
APP_NAME="Blog Breeze"           # Nom affiché dans l'interface
APP_ENV=local                    # Environnement : local, staging, production
APP_DEBUG=true                   # Mode debug (affiche erreurs détaillées)
APP_URL=http://localhost:8000    # URL racine de l'application

# =========================================
# Configuration Base de Données
# =========================================
DB_CONNECTION=mysql              # Driver : mysql ou mariadb (identiques)
DB_HOST=127.0.0.1                # Adresse serveur BDD (local = 127.0.0.1)
DB_PORT=3306                     # Port MySQL/MariaDB par défaut
DB_DATABASE=blog_breeze          # Nom de la base créée à l'étape précédente
DB_USERNAME=root                 # Utilisateur MySQL (root par défaut en local)
DB_PASSWORD=                     # Mot de passe root (vide par défaut sur XAMPP/Laragon)

# =========================================
# Configuration Mail (Mode LOG pour développement)
# =========================================
MAIL_MAILER=log                  # "log" = emails sauvegardés dans storage/logs
                                 # Pas d'envoi réel, idéal pour dev
```

<small>*Le fichier `.env` n'est **jamais versionné** (présent dans `.gitignore`) car il contient des données sensibles (mots de passe, clés API). Chaque développeur doit créer son propre `.env` en copiant `.env.example`. Laravel charge automatiquement ces variables au démarrage via la fonction `env('NOM_VARIABLE')`.*</small>

!!! danger "Modifier le Mot de Passe BDD - Si vous avez défini un mot de passe pour l'utilisateur `root` MySQL/MariaDB, **vous devez le saisir dans `DB_PASSWORD=`**. Sur Laragon et XAMPP par défaut, le mot de passe root est vide, d'où `DB_PASSWORD=` sans valeur."

**Tableau récapitulatif des variables critiques :**

| Variable | Valeur Dev | Valeur Production | Description |
|----------|-----------|-------------------|-------------|
| `APP_ENV` | `local` | `production` | Active/désactive debug, cache, optimisations |
| `APP_DEBUG` | `true` | `false` | Affiche stack traces d'erreurs (désactiver en prod) |
| `APP_URL` | `http://localhost:8000` | `https://votredomaine.com` | URL racine pour génération liens |
| `DB_PASSWORD` | (vide ou simple) | (complexe) | Mot de passe BDD fort en production |
| `MAIL_MAILER` | `log` | `smtp` | Log = fichiers, SMTP = envoi réel |

## Étape 1.4 : Tester la Connexion Base de Données

!!! quote "Avant d'installer Breeze, vérifions que Laravel communique correctement avec la base de données."

```bash
# Vérifier l'état des migrations (doit se connecter à la BDD)
php artisan migrate:status
```

<small>*La commande `php artisan migrate:status` interroge la base de données pour lister l'état des migrations. Si elle échoue, c'est qu'il y a un problème de configuration `.env` ou que le serveur BDD n'est pas actif. Résoudre cette étape est impératif avant de continuer.*</small>

**Résultats possibles :**

=== ":fontawesome-solid-circle-check: Succès"

    ```bash
    Migration table not found.
    ```
    
    !!! success "**Signification :** Aucune erreur de connexion. La table `migrations` n'existe pas encore (normal, on n'a pas encore migré). Laravel a réussi à se connecter."

=== ":fontawesome-solid-circle-xmark: Échec - Erreur Connexion"

    ```bash
    SQLSTATE[HY000] [1045] Access denied for user 'root'@'localhost'
    ```
    
    !!! note "**Cause :** Mot de passe BDD incorrect dans `.env`"
    
    !!! tip "**Solution :** Vérifier `DB_USERNAME` et `DB_PASSWORD` dans `.env`"

=== ":fontawesome-solid-circle-xmark: Échec - Base Introuvable"

    ```bash
    SQLSTATE[HY000] [1049] Unknown database 'blog_breeze'
    ```
    
    !!! note "**Cause :** La base de données n'existe pas ou nom mal orthographié"
    
    !!! tip "**Solution :** Retourner à l'étape 1.2 pour créer la base, ou vérifier `DB_DATABASE` dans `.env`"

=== ":fontawesome-solid-circle-xmark: Échec - Serveur Inaccessible"

    ```bash
    SQLSTATE[HY000] [2002] Connection refused
    ```
    
    !!! note "**Cause :** Le serveur MySQL/MariaDB n'est pas démarré"
    
    !!! tip "**Solution :**" 
    
          - **Windows (XAMPP/Laragon)** : Démarrer MySQL dans le panneau de contrôle
          - **macOS (Homebrew)** : `brew services start mysql` ou `brew services start mariadb`
          - **Linux** : `sudo systemctl start mysql` ou `sudo systemctl start mariadb`


## Étape 1.5 : Installer Laravel Breeze

> Laravel Breeze est un **starter kit d'authentification minimaliste** qui génère automatiquement tous les contrôleurs, routes, vues et migrations nécessaires pour un système d'authentification complet (**inscription**, **connexion**, **réinitialisation mot de passe**, **vérification email**, **gestion profil**).

```bash
# Installer le package Breeze via Composer
composer require laravel/breeze --dev

# Attendre la fin de l'installation (30 secondes - 1 minute)
# Composer télécharge Breeze et ses dépendances
```

**Publier les fichiers Breeze dans le projet :**

```bash
# Exécuter l'installeur Breeze
php artisan breeze:install blade

# Questions interactives posées par l'installeur :
```

**Réponses aux questions interactives :**

| Question | Réponse Recommandée | Explication |
|----------|---------------------|-------------|
| **Which Breeze stack would you like to install?** | `blade` | Stack Blade + Alpine.js (la plus simple) |
| **Would you like dark mode support?** | `No` | Facultatif (on se concentre sur la fonctionnalité) |
| **Which testing framework do you prefer?** | `PHPUnit` | Framework de tests par défaut Laravel |

<small>*L'installeur Breeze copie tous les fichiers nécessaires dans votre projet : contrôleurs d'authentification dans `app/Http/Controllers/Auth/`, vues Blade dans `resources/views/auth/`, routes dans `routes/auth.php`, et migrations pour les tables `users`, `password_reset_tokens`, etc. Il modifie également `routes/web.php` pour inclure les routes Breeze.*</small>

!!! info "Stacks Breeze Disponibles"
    - **Blade** : Vues Blade traditionnelles + Alpine.js (JavaScript léger)
    - **Livewire** : Composants Livewire réactifs (sans JavaScript explicite)
    - **React** : Frontend React avec Inertia.js
    - **Vue** : Frontend Vue.js avec Inertia.js
    
    > Pour ce projet, **Blade** est optimal : **simple**, **performant**, et **parfait** pour apprendre Laravel.


## Étape 1.6 : Installer les Dépendances Frontend

> Breeze utilise **Vite** (_bundler moderne_) pour compiler les assets CSS (**Tailwind CSS**) et JavaScript (**Alpine.js**). Vous devez installer les dépendances Node.js et compiler les assets.

```bash
# Installer les dépendances NPM (définies dans package.json)
npm install

# Attendre la fin de l'installation (1-3 minutes)
# NPM télécharge Tailwind CSS, Vite, Alpine.js, PostCSS, etc.
```

**Compiler les assets :**

<div class="cards grid" markdown>

- :fontawesome-solid-hammer: Mode Développement (Watch)

    ```bash
    # Compiler et surveiller les changements (hot reload)
    npm run dev
    
    # Résultat attendu :
    # VITE v5.x.x  ready in 1234 ms
    # ➜  Local:   http://localhost:5173/
    # ➜  Network: use --host to expose
    # ➜  press h + enter to show help
    ```
    
    !!! note "**Laisser ce terminal ouvert** : Vite recompile automatiquement à chaque modification de fichier CSS/JS."

</div>
<div class="cards grid" markdown>

- :fontawesome-solid-box: Mode Production (Build)

    ```bash
    # Compiler pour la production (minification, optimisation)
    npm run build
    
    # Résultat attendu :
    # vite v5.x.x building for production...
    # ✓ built in 3.45s
    ```
    
    !!! info "Utiliser `npm run build` uniquement avant déploiement production. En développement, préférer `npm run dev`."

</div>

<small>*Vite crée un serveur de développement sur `http://localhost:5173/` qui sert les assets compilés. Laravel charge automatiquement ces assets via la directive `@vite(['resources/css/app.css', 'resources/js/app.js'])` présente dans les layouts Blade. En production, `npm run build` génère des fichiers statiques optimisés dans `public/build/`.*</small>

!!! warning "Erreur Commune : Port 5173 Déjà Utilisé"
    Si vous voyez `Error: listen EADDRINUSE: address already in use :::5173`, c'est qu'une instance Vite tourne déjà. Fermez l'ancien terminal ou tuez le processus : 
    
    - **Windows** : `taskkill /F /IM node.exe`
    - **macOS/Linux** : `killall node`

## Étape 1.7 : Exécuter les Migrations Breeze

> Les migrations créent les **tables de base de données** nécessaires à l'authentification : `users`, `password_reset_tokens`, `sessions`, `failed_jobs`, etc.

```bash
# Exécuter toutes les migrations en attente
php artisan migrate
```

```bash title="Résultat attendu (chronologie d'exécution) :"
Migration table created successfully.               # Création table "migrations"
Migrating: 2014_10_12_000000_create_users_table
Migrated:  2014_10_12_000000_create_users_table (45.67ms)
Migrating: 2014_10_12_100000_create_password_reset_tokens_table
Migrated:  2014_10_12_100000_create_password_reset_tokens_table (32.14ms)
Migrating: 2019_08_19_000000_create_failed_jobs_table
Migrated:  2019_08_19_000000_create_failed_jobs_table (28.91ms)
Migrating: 2019_12_14_000001_create_personal_access_tokens_table
Migrated:  2019_12_14_000001_create_personal_access_tokens_table (35.42ms)
Migrating: 0001_01_01_000001_create_cache_table
Migrated:  0001_01_01_000001_create_cache_table (22.78ms)
Migrating: 0001_01_01_000002_create_jobs_table
Migrated:  0001_01_01_000002_create_jobs_table (30.56ms)
```

<small>*Chaque migration correspond à un fichier dans `database/migrations/`. Laravel exécute les migrations dans l'ordre chronologique (préfixe timestamp). La table `migrations` enregistre les migrations déjà exécutées pour éviter les doublons. Vous pouvez vérifier la structure créée dans phpMyAdmin ou via `SHOW TABLES;` en MySQL.*</small>

**Vérifier les tables créées :**

```bash
# Se connecter à MySQL/MariaDB
mysql -u root -p blog_breeze

# Lister les tables
SHOW TABLES;

# Résultat attendu :
# +------------------------+
# | Tables_in_blog_breeze  |
# +------------------------+
# | cache                  |
# | cache_locks            |
# | failed_jobs            |
# | jobs                   |
# | migrations             |
# | password_reset_tokens  |
# | personal_access_tokens |
# | sessions               |
# | users                  |
# +------------------------+

# Quitter
EXIT;
```

!!! tip "Commandes Migrations Utiles"
    - `php artisan migrate:status` : Liste l'état des migrations
    - `php artisan migrate:rollback` : Annule la dernière batch de migrations
    - `php artisan migrate:fresh` : Supprime toutes les tables et remigre (utile en dev)
    - `php artisan migrate:fresh --seed` : Fresh + seeders (données de test)

## Étape 1.8 : Démarrer le Serveur de Dev

!!! quote "Laravel embarque un serveur PHP intégré pour le développement local (**ne JAMAIS utiliser en production**)."

=== ":fontawesome-brands-windows: Windows"

    ```bash
    # Ouvrir un NOUVEAU terminal (laisser npm run dev tourner)
    # Naviguer dans le projet
    cd C:\Users\VotreNom\Desktop\blog-breeze
    
    # Démarrer le serveur sur le port 8000
    php artisan serve
    
    # Résultat attendu :
    #   INFO  Server running on [http://127.0.0.1:8000].
    #   Press Ctrl+C to stop the server
    ```

=== ":fontawesome-brands-apple: macOS"

    ```bash
    # Ouvrir un NOUVEAU terminal (laisser npm run dev tourner)
    # Naviguer dans le projet
    cd ~/Documents/blog-breeze
    
    # Démarrer le serveur sur le port 8000
    php artisan serve
    
    # Résultat attendu :
    #   INFO  Server running on [http://127.0.0.1:8000].
    #   Press Ctrl+C to stop the server
    ```

=== ":fontawesome-brands-linux: Linux"

    ```bash
    # Ouvrir un NOUVEAU terminal (laisser npm run dev tourner)
    # Naviguer dans le projet
    cd ~/blog-breeze
    
    # Démarrer le serveur sur le port 8000
    php artisan serve
    
    # Résultat attendu :
    #   INFO  Server running on [http://127.0.0.1:8000].
    #   Press Ctrl+C to stop the server
    ```

<small>*Le serveur `php artisan serve` utilise le serveur web intégré de PHP. Il écoute par défaut sur `http://127.0.0.1:8000` (équivalent à `localhost:8000`). Ce serveur recharge automatiquement les fichiers PHP modifiés, mais **Vite (`npm run dev`)** doit tourner en parallèle pour recompiler les assets CSS/JS en temps réel.*</small>

!!! info "Port Personnalisé - Si le port 8000 est déjà utilisé, spécifiez-en un autre : **`php artisan serve --port=8080`**"

!!! note "**Ouvrir votre navigateur et accéder à : `http://localhost:8000`**"

## Étape 1.9 : Tester l'Authentification Breeze

!!! quote "Vous devez maintenant vérifier que tout fonctionne en créant un compte utilisateur."

**Page d'Accueil Laravel :**

Vous devez voir la **page d'accueil Laravel par défaut** avec :

- :fontawesome-solid-bars: Menu de navigation en haut à droite : **"Log in"** et **"Register"**
- :fontawesome-solid-house: Logo Laravel ou texte "Laravel" en haut à gauche
- :fontawesome-solid-file-lines: Contenu central avec liens vers la documentation

!!! success "Étape Validée - Si vous voyez cette page, **l'installation Laravel + Breeze est réussie**."

??? abstract "**Test 1 : Inscription d'un Utilisateur**"

    1. Cliquer sur **"Register"** (en haut à droite)
    2. Remplir le formulaire :

        | Champ | Valeur Exemple |
        |-------|----------------|
        | **Name** | `Alice Dupont` |
        | **Email** | `alice@example.com` |
        | **Password** | `password` (minimum 8 caractères) |
        | **Confirm Password** | `password` |

    3. Cliquer **"Register"**
    4. **Redirection automatique** vers `/dashboard`

    **Résultat Attendu :**

    - :fontawesome-solid-circle-check: URL change pour `http://localhost:8000/dashboard`
    - :fontawesome-solid-circle-check: Message de bienvenue : "You're logged in!"
    - :fontawesome-solid-circle-check: Menu navigation affiche votre nom (**Alice Dupont**) avec dropdown

    <small>*Lors de l'inscription, Laravel hache automatiquement le mot de passe avec bcrypt avant stockage dans `users.password`. Le token de session est stocké dans la table `sessions`. Si vous avez configuré `MAIL_MAILER=log`, un email de vérification est généré dans `storage/logs/laravel.log` (mais pas envoyé réellement).*</small>

??? abstract "**Test 2 : Déconnexion**"

    1. Cliquer sur votre nom en haut à droite (**Alice Dupont**)
    2. Sélectionner **"Log Out"** dans le dropdown
    3. **Redirection automatique** vers la page d'accueil

    **Résultat Attendu :**

    - :fontawesome-solid-circle-check: Retour sur la page d'accueil
    - :fontawesome-solid-circle-check: Menu affiche à nouveau **"Log in"** et **"Register"**

??? abstract "**Test 3 : Connexion**"

    1. Cliquer **"Log in"**
    2. Remplir le formulaire :

        | Champ | Valeur |
        |-------|--------|
        | **Email** | `alice@example.com` |
        | **Password** | `password` |

    3. **Optionnel** : Cocher **"Remember me"** (cookie persistent 5 ans)
    4. Cliquer **"Log in"**
    5. **Redirection vers `/dashboard`**

    **Résultat Attendu :**

    - :fontawesome-solid-circle-check: Accès au dashboard
    - :fontawesome-solid-circle-check: Session active (votre nom affiché dans le menu)

??? abstract "**Test 4 : Réinitialisation Mot de Passe (Optionnel)**"

    1. **Se déconnecter**
    2. Page login → Cliquer **"Forgot your password?"**
    3. Entrer email : `alice@example.com`
    4. Cliquer **"Email Password Reset Link"**
    5. **Vérifier le log** : `storage/logs/laravel.log`

    **Contenu du log :**

    ```
    [2024-XX-XX XX:XX:XX] local.INFO: Password Reset Link: http://localhost:8000/reset-password/TOKEN_HASH
    ```

    6. Copier l'URL complète du log et la coller dans le navigateur
    7. Définir nouveau mot de passe : `newpassword`
    8. Confirmer et se connecter avec le nouveau mot de passe

    <small>*En développement avec `MAIL_MAILER=log`, Laravel écrit les emails dans `storage/logs/laravel.log` au lieu de les envoyer. En production (SMTP configuré), l'email serait envoyé réellement. Le token de réinitialisation expire après 60 minutes par défaut (configurable dans `config/auth.php`).*</small>

## Étape 1.10 : Vérification Finale

> Avant de passer à la Phase 2, assurez-vous que tous les éléments suivants sont **validés** :

**Checklist de Validation Phase 1 :**

- [x] **Projet Laravel créé** : Dossier `blog-breeze/` avec structure complète
- [x] **Base de données créée** : `blog_breeze` existe dans MySQL/MariaDB
- [x] **Fichier `.env` configuré** : Connexion BDD fonctionnelle
- [x] **Breeze installé** : Fichiers auth présents dans `app/Http/Controllers/Auth/` et `resources/views/auth/`
- [x] **Assets compilés** : `npm run dev` tourne sans erreur, styles Tailwind visibles
- [x] **Migrations exécutées** : Tables `users`, `sessions`, etc. créées
- [x] **Serveur démarré** : `http://localhost:8000` accessible
- [x] **Inscription testée** : Compte créé et connexion réussie
- [x] **Dashboard accessible** : URL `/dashboard` affiche "You're logged in!"

!!! success "Si tous les points sont cochés, **félicitations la phase 1 est Terminée avec succès !** Vous disposez d'une application Laravel fonctionnelle avec authentification complète. Vous êtes prêt à passer à la **Phase 2 : Création des Modèles et Migrations** pour construire la structure de données du blog."

## Résolution Problèmes Courants

??? fail "Erreur : `Class 'Composer\InstalledVersions' not found`"
    **Cause :** Cache Composer corrompu
    
    **Solution :**
    ```bash
    composer clear-cache
    composer install
    ```

??? fail "Erreur : `npm ERR! code ENOENT`"
    **Cause :** `package.json` manquant ou Node.js non installé
    
    **Solution :**
    ```bash
    node -v  # Vérifier version Node (22+)
    npm -v   # Vérifier version NPM (10+)
    # Si manquants, réinstaller Node.js depuis nodejs.org
    ```

??? fail "Erreur : `Vite manifest not found`"
    **Cause :** Assets non compilés
    
    **Solution :**
    ```bash
    npm install
    npm run build
    # Puis relancer php artisan serve
    ```

??? fail "Page Blanche après `php artisan serve`"
    **Cause :** Erreur PHP silencieuse ou permissions fichiers
    
    **Solution :**
    ```bash
    # Vérifier les logs
    tail -f storage/logs/laravel.log
    
    # Corriger permissions (Linux/macOS)
    chmod -R 775 storage bootstrap/cache
    ```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les kits de démarrage Laravel font gagner des semaines de développement, mais ils imposent de bien comprendre les flux sous-jacents. Ne traitez jamais l'authentification comme une simple boîte noire.

> [Passer à la phase suivante →](../index.md)
