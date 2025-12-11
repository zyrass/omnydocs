---
description: "Phase 0 : Découvrez la vision globale du projet Blog Multi-Auteurs, son architecture complète, la logique pédagogique et comment les 7 Phases s'articulent pour maîtriser Laravel Breeze et l'authentification."
icon: lucide/compass
tags: ["BREEZE", "BLOG", "VISION", "ARCHITECTURE", "LARAVEL"]
status: beta
---

# Projet Breezei

<div
  class="omny-meta"
  data-level="🟢 Débutant 🟡 Intermédiaire & 🔴 Avancé"
  data-version="0.0.3"
  data-time="2-4 heures">
</div>

## Introduction

Bienvenue dans ce projet **Blog Multi-Auteurs avec Laravel Breeze** ! Avant de commencer à "_coder_", "_"installer des dépendances"_ ou bien même de "_créer des migrations_", il est **crucial** que vous compreniez la vision d'ensemble du projet, son architecture complète et la logique pédagogique qui structure ce parcours d'apprentissage.

!!! note "Ce projet s’inscrit dans la continuité du module consacré aux fondamentaux de Breeze."

Cette phase **vous présente** :

- Les objectifs pédagogiques du projet
- L'architecture complète de l'application (base de données, modèles, contrôleurs, vues)
- Le rôle de Laravel Breeze dans le projet
- La structure logique des 7 Phases qui composent ce projet (Phases 1 à 7)
- Les compétences que vous allez acquérir étape par étape

!!! quote "Pourquoi commencer par la vision globale ?"
    Imaginez que vous construisez une **maison professionnelle**. Avant de couler les fondations, vous devez comprendre le plan d'ensemble : combien d'étages, où placer les pièces, comment organiser la plomberie et l'électricité. **C'est exactement le rôle de ce Phase** : vous donner le blueprint complet du blog avant d'écrire la première ligne de code. Sans cette vision, vous risquez de construire une pièce sans comprendre comment elle s'intègre au reste de la maison.

## Objectifs d'Apprentissage

!!! abstract "Avant le début de la première phase, **vous serez capable** :"

    - [ ] D'expliquer la finalité pédagogique du projet Blog Multi-Auteurs
    - [ ] D'identifier les 4 entités principales (**User**, **Post**, **Category**, **Comment**) et leurs relations
    - [ ] De comprendre le **rôle** de Laravel Breeze dans l'authentification
    - [ ] Décrire l'architecture **MVC** (_Model, View, Controller_) appliquée au blog
    - [ ] De situer chaque Phase (**1 à 7**) dans la progression logique du projet
    - [ ] D'anticiper les compétences Laravel que vous allez développer

## Finalité Pédagogique du Projet

### Pourquoi construire un blog multi-auteurs ?

!!! quote "Ce projet n'est **pas** un exercice théorique. C'est un **cas d'usage réel** que vous rencontrerez dans 80% des applications web professionnelles."

**Cas d'usage professionnels équivalents :**

- **Blog d'entreprise** → _Plateforme de publication avec modération_
- **Intranet collaboratif** → _Articles internes avec commentaires_
- **Base de connaissances** → _Documentation collaborative_
- **Plateforme e-learning** → _Cours publiés par formateurs_
- **Marketplace** → _Vendeurs publient produits avec reviews_

**Compétences transférables :**

- [x] Authentification utilisateur (**login**, **register**, **reset password**)
- [x] CRUD complet avec ownership (**un user gère SES ressources**)
- [x] Relations Eloquent (**1-N**, **N-N**)
- [x] Validation de formulaires
- [x] Système de rôles simplifié (**auteur vs visiteur**)
- [x] Modération de contenu (**commentaires**)
- [x] Dashboard statistiques

**Ce projet vous prépare directement pour :**

- CMS professionnels (**WordPress-like**)
- Applications **SaaS** avec gestion utilisateurs
- Plateformes collaboratives
- Systèmes de **tickets**/**support**

## Architecture Globale du Projet

### Modélisation Complète de la Base de Données

=== "UseCase - Cas d'utilisation"

    !!! quote "**Diagramme des cas d'utilisation** représentant les interactions entre les acteurs (Visiteur, Auteur, Système) et les fonctionnalités du blog."

    ```mermaid
    graph LR
        subgraph "Acteurs"
            V[Visiteur<br/>Non authentifié]
            A[Auteur<br/>Authentifié]
        end
        
        subgraph "Système Blog Multi-Auteurs"
            UC1[Consulter articles]
            UC2[Filtrer par catégorie]
            UC3[Voir profil auteur]
            UC4[Commenter article]
            
            UC5[S'inscrire]
            UC6[Se connecter]
            UC7[Gérer son profil]
            
            UC8[Créer article]
            UC9[Modifier article]
            UC10[Supprimer article]
            UC11[Gérer brouillons]
            
            UC12[Modérer commentaires]
            UC13[Consulter statistiques]
        end
        
        V --> UC1
        V --> UC2
        V --> UC3
        V --> UC4
        V --> UC5
        
        A --> UC1
        A --> UC2
        A --> UC3
        A --> UC6
        A --> UC7
        A --> UC8
        A --> UC9
        A --> UC10
        A --> UC11
        A --> UC12
        A --> UC13
        
        UC8 -.inclut.-> UC11
        UC9 -.inclut.-> UC11
        UC12 -.nécessite.-> UC9
        
        style V fill:#e3f3ff
        style A fill:#e3ffe3
    ```

    <small>*Le système distingue deux acteurs principaux : les **Visiteurs** (consultation et commentaires) et les **Auteurs** (gestion complète de leurs contenus). Les visiteurs peuvent s'inscrire pour devenir auteurs.*</small>

=== "MCD - Modèle Conceptuel"

    !!! quote "**Modèle Conceptuel de Données (MCD)** : Vue abstraite des entités métier et de leurs relations sans considération technique."

    ```mermaid
    classDiagram
        class USER {
            name : String
            email : String
            bio : Text
            avatar : String
        }
        
        class POST {
            title : String
            excerpt : Text
            content : Text
            status : Enum
            image : String
        }
        
        class CATEGORY {
            name : String
        }
        
        class COMMENT {
            author_name : String
            author_email : String
            content : Text
            approved : Boolean
        }
        
        USER "1" --> "0..*" POST : écrit
        POST "0..*" --> "1" CATEGORY : appartient_à
        POST "1" --> "0..*" COMMENT : reçoit
    ```
    <small>*Le MCD se concentre sur les **règles métier** sans détails techniques : un auteur peut écrire plusieurs articles, chaque article appartient à une seule catégorie, les commentaires sont attachés à un article spécifique.*</small>

    **Cardinalités expliquées (dans les deux sens) :**

    | Relation | Cardinalité | Signification |
    |----------|-------------|---------------|
    | **USER → POST** | 1 vers 0..* | Un auteur écrit de 0 à N articles |
    | **POST → USER** | 0..* vers 1 | N articles sont écrits par exactement 1 auteur |
    | **POST → CATEGORY** | 0..* vers 1 | N articles appartiennent à exactement 1 catégorie |
    | **CATEGORY → POST** | 1 vers 0..* | Une catégorie contient de 0 à N articles |
    | **POST → COMMENT** | 1 vers 0..* | Un article reçoit de 0 à N commentaires |
    | **COMMENT → POST** | 0..* vers 1 | N commentaires concernent exactement 1 article |


=== "MLD - Modèle Logique"

    !!! quote "**Modèle Logique de Données (MLD)** : Traduction du MCD en tables relationnelles avec clés primaires (PK) et clés étrangères (FK)."

    ```mermaid
    erDiagram
        USER ||--o{ POST : "écrit"
        USER {
            int id PK
            string name
            string email UK "UNIQUE"
            string password
            text bio "NULLABLE"
            string avatar "NULLABLE"
            timestamp email_verified_at "NULLABLE"
        }
        
        CATEGORY ||--o{ POST : "contient"
        CATEGORY {
            int id PK
            string name
            string slug UK "UNIQUE"
        }
        
        POST ||--o{ COMMENT : "reçoit"
        POST {
            int id PK
            int user_id FK
            int category_id FK
            string title
            string slug UK "UNIQUE"
            text excerpt
            text content
            string image "NULLABLE"
            string status "draft/published"
            timestamp published_at "NULLABLE"
            int views_count
        }
        
        COMMENT {
            int id PK
            int post_id FK
            string author_name
            string author_email
            text content
            boolean approved
        }
    ```
    <small>*Le MLD introduit les **clés techniques** pour établir les relations : **les clés étrangères `user_id`**, **`category_id`**, **`post_id` matérialisent les associations du MCD**. Les suppressions en cascade garantissent la cohérence.*</small>

    **Contraintes d'intégrité :**
    
    - **Clés primaires (PK)** : Identifiant unique auto-incrémenté pour chaque table
    - **Clés étrangères (FK)** :
        - `posts.user_id` référence `users.id` (CASCADE DELETE)
        - `posts.category_id` référence `categories.id` (CASCADE DELETE)
        - `comments.post_id` référence `posts.id` (CASCADE DELETE)
    - **Contraintes UNIQUE (UK)** : email (users), slug (categories, posts)
    - **Contraintes CHECK** : status IN ('draft', 'published')

=== "MPD - Modèle Physique"

    !!! quote "**Modèle Physique de Données (MPD)** : Structure finale implémentée en base MySQL avec types de données SQL précis, index et optimisations."

    ```mermaid
    erDiagram
        USER ||--o{ POST : "écrit"
        USER {
            int id PK "AUTO_INCREMENT"
            varchar_255 name
            varchar_255 email "UNIQUE INDEX"
            varchar_255 password
            text bio "NULLABLE"
            varchar_255 avatar "NULLABLE"
            timestamp email_verified_at "NULLABLE"
            timestamp created_at
            timestamp updated_at
        }
        
        POST ||--|| CATEGORY : "appartient_à"
        POST ||--o{ COMMENT : "reçoit"
        POST {
            int id PK "AUTO_INCREMENT"
            int user_id FK "INDEX, CASCADE DELETE"
            int category_id FK "INDEX, CASCADE DELETE"
            varchar_255 title
            varchar_255 slug "UNIQUE INDEX"
            text excerpt
            longtext content
            varchar_255 image "NULLABLE"
            enum status "DEFAULT 'draft'"
            timestamp published_at "NULLABLE, INDEX"
            int views_count "DEFAULT 0"
            timestamp created_at
            timestamp updated_at
        }
        
        CATEGORY ||--o{ POST : "contient"
        CATEGORY {
            int id PK "AUTO_INCREMENT"
            varchar_255 name
            varchar_255 slug "UNIQUE INDEX"
            timestamp created_at
            timestamp updated_at
        }
        
        COMMENT {
            int id PK "AUTO_INCREMENT"
            int post_id FK "INDEX, CASCADE DELETE"
            varchar_255 author_name
            varchar_255 author_email
            text content
            boolean approved "DEFAULT FALSE"
            timestamp created_at
            timestamp updated_at
        }
    ```

    <small>*Le MPD représente la **structure réelle MySQL** avec optimisations de performance : les index accélèrent les requêtes fréquentes (filtres par status, recherche par slug), les types de données sont dimensionnés au plus juste.*</small>

    **Optimisations physiques :**

    - **Index simples** : email, slug, published_at
    - **Index composites** : (user_id, status), (post_id, approved)
    - **Types de stockage** :
        - `longtext` pour content (jusqu'à 4 Go)
        - `text` pour excerpt, bio (jusqu'à 64 Ko)
        - `enum` pour status (1 octet vs varchar)
    - **Valeurs par défaut** : status='draft', approved=false, views_count=0
    - **Timestamps automatiques** : created_at, updated_at gérés par Laravel


## Architecture MVC Appliquée

### Flux de Données et Séparation des Responsabilités

Le pattern **MVC (Model-View-Controller)** est l'architecture fondamentale de Laravel. Il sépare clairement les responsabilités : les **Modèles** gèrent les données et la logique métier, les **Vues** affichent l'interface utilisateur, et les **Contrôleurs** orchestrent les interactions entre les deux. Cette séparation garantit un code maintenable, testable et évolutif.

Dans notre blog multi-auteurs, chaque requête HTTP suit un cycle précis : l'utilisateur interagit via son navigateur, les routes dirigent vers les contrôleurs appropriés (**authentification Breeze ou logique métier custom**), les contrôleurs interrogent les modèles Eloquent qui communiquent avec MySQL, puis retournent les vues Blade enrichies des données au navigateur.

```mermaid
graph LR
    subgraph "UTILISATEUR"
        Browser[Navigateur Web]
    end
    
    subgraph "ROUTES"
        WebRoutes[routes/web.php]
        AuthRoutes[routes/auth.php Breeze]
    end
    
    subgraph "CONTROLLERS"
        HomeCtrl[HomeController]
        PostCtrl[PostController]
        DashCtrl[DashboardController]
        CommentCtrl[CommentController]
        CategoryCtrl[CategoryController]
        AuthCtrl[Auth/* Breeze]
    end
    
    subgraph "MODELS"
        User[User]
        Post[Post]
        Category[Category]
        Comment[Comment]
    end
    
    subgraph "DATABASE"
        MySQL[(MySQL)]
    end
    
    subgraph "VIEWS"
        Home[home.blade.php]
        PostShow[posts/show.blade.php]
        Dashboard[dashboard.blade.php]
        AuthViews[auth/* Breeze]
    end
    
    Browser -->|HTTP Request| WebRoutes
    Browser -->|Login/Register| AuthRoutes
    
    WebRoutes --> HomeCtrl
    WebRoutes --> PostCtrl
    WebRoutes --> DashCtrl
    AuthRoutes --> AuthCtrl
    
    HomeCtrl --> Post
    PostCtrl --> Post
    PostCtrl --> Category
    CommentCtrl --> Comment
    
    Post --> MySQL
    User --> MySQL
    Category --> MySQL
    Comment --> MySQL
    
    HomeCtrl --> Home
    PostCtrl --> PostShow
    DashCtrl --> Dashboard
    AuthCtrl --> AuthViews
    
    Home --> Browser
    PostShow --> Browser
    Dashboard --> Browser
    
    style Browser fill:#e3f3ff
    style MySQL fill:#ffe3e3
    style User fill:#e3ffe3
    style Post fill:#e3ffe3
```

<small>*Le diagramme illustre le **cycle de vie d'une requête** : (1) le navigateur envoie une requête HTTP, (2) les routes (`web.php` ou `auth.php`) dirigent vers le contrôleur approprié, (3) le contrôleur interroge les modèles Eloquent pour récupérer/modifier les données, (4) les modèles communiquent avec MySQL, (5) le contrôleur charge une vue Blade avec les données, (6) la vue HTML est retournée au navigateur. Laravel Breeze gère automatiquement tout le flux d'authentification (partie droite du diagramme).*</small>

## Rôle de Laravel Breeze

### Qu'est-ce que Breeze apporte ?

Laravel Breeze est un **starter kit d'authentification minimaliste** qui génère automatiquement :

=== "Contrôleurs d'authentification"

    - `RegisteredUserController` → Inscription
    - `AuthenticatedSessionController` → Login/Logout
    - `PasswordResetLinkController` → Demande reset password
    - `NewPasswordController` → Reset password effectif
    - `EmailVerificationController` → Vérification email
    - `ProfileController` → Gestion profil

=== "Routes d'authentification"

    - `GET /register` → Formulaire inscription
    - `POST /register` → Créer compte
    - `GET /login` → Formulaire connexion
    - `POST /login` → Authentifier
    - `POST /logout` → Déconnexion
    - `GET /forgot-password` → Formulaire reset
    - `POST /forgot-password` → Envoyer email reset
    - etc.

=== "Vues Blade"

    - `auth/register.blade.php`
    - `auth/login.blade.php`
    - `auth/forgot-password.blade.php`
    - `profile/edit.blade.php`
    - etc.

=== "Middleware"

    - `auth` → Protéger routes (utilisateur connecté requis)
    - `verified` → Email vérifié requis

!!! tip "Breeze = Fondations Solides"
    Breeze vous **fait gagner 8-12 heures** de développement en générant du code authentification production-ready, testé et sécurisé. Vous vous concentrez sur **votre logique métier** (le blog) plutôt que réinventer l'authentification.

## Structure des 7 Phases

!!! quote "Au-delà de la compréhension de l’architecture globale, explorez les sept phases du projet, accompagnées du **temps estimé**, de **l’objectif visé** et **des livrables attendus**. Cette vue d’ensemble garantit une progression claire et sans ambiguïté."

<div class="cards grid" markdown>

- :fontawesome-solid-download: **Phase 1 : Installation et Configuration**

    ---

    **Temps :** 15-20 minutes  
    **Objectif :** Installer Laravel, Breeze, configurer BDD  
    **Livrables :**

    - Projet Laravel fonctionnel
    - Breeze installé et migrations exécutées
    - Authentification testée (register/login)

- :fontawesome-solid-database: **Phase 2 : Base de Données et Modèles**

    ---

    **Temps :** 30-40 minutes  
    **Objectif :** Créer structure BDD complète et modèles Eloquent  
    **Livrables :**

    - Migrations (categories, posts, comments)
    - Modèles avec relations (User, Post, Category, Comment)
    - Seeders avec données de test

- :fontawesome-solid-seedling: **Phase 3 : Seeders et Données de Test**

    ---

    **Temps :** 15-20 minutes  
    **Objectif :** Créer données de test pour développement  
    **Livrables :**

    - CategorySeeder avec 6 catégories
    - DatabaseSeeder avec 3 users + 7 posts + 2 comments
    - Commande `migrate:fresh --seed` fonctionnelle

- :fontawesome-solid-code: **Phase 4 : Contrôleurs et Logique Métier**

    ---

    **Temps :** 45-60 minutes  
    **Objectif :** Implémenter toute la logique CRUD et business  
    **Livrables :**

    - 7 contrôleurs complets (Home, Post, Dashboard, Comment, Category, Author, Profile)
    - Validation formulaires
    - Authorization (ownership)

- :fontawesome-solid-route: **Phase 5 : Routes et Organisation**

    ---

    **Temps :** 15-20 minutes  
    **Objectif :** Structurer routes publiques/protégées  
    **Livrables :**

    - Routes publiques (home, posts, categories)
    - Routes protégées (dashboard, CRUD posts)
    - Routes authentification (Breeze)

- :fontawesome-solid-eye: **Phase 6 : Vues Blade et Interface**

    ---

    **Temps :** 60-90 minutes  
    **Objectif :** Créer toute l'interface utilisateur  
    **Livrables :**

    - Layout principal (navigation, footer)
    - 9 vues complètes (home, post show, create, edit, dashboard, etc.)
    - Design Tailwind CSS responsive

</div>

<div class="cards grid" markdown>

- :fontawesome-solid-check-circle: **Phase 7 : Tests et Validation Finale**

    ---

    **Temps :** 15-20 minutes  
    **Objectif :** Tester toutes les fonctionnalités  
    **Livrables :**

    - Checklist tests complète
    - Blog 100% fonctionnel
    - Documentation utilisation

</div>

## Progression des Compétences

### Compétences Laravel Acquises

> Ce projet couvre l'ensemble des compétences fondamentales nécessaires pour développer une application Laravel professionnelle en conditions réelles. Vous maîtriserez non seulement la création de migrations et de modèles Eloquent, mais également l'orchestration complète du cycle MVC, la gestion des relations complexes entre entités, la validation des données, l'autorisation via les Policies, et l'intégration de l'authentification Breeze. Chaque phase du projet renforce progressivement votre expertise, de la structure de base de données jusqu'à l'interface utilisateur responsive.

!!! note "Le parcours d'apprentissage suit une progression logique : après avoir posé les fondations techniques (**BDD**, **modèles**, **seeders**), vous implémenterez la logique métier dans **les contrôleurs**, organiserez **le routage** de l'application, puis construirez **l'interface utilisateur** avec Blade et Tailwind CSS. Cette approche garantit une compréhension profonde de l'architecture Laravel et des bonnes pratiques de développement."

```mermaid
---
title: "Légende du Graph ci-dessous"
---
graph TB
  Phase12["🟢 Phases 1-2 : Débutant (suivre instructions)"]
  Phase34["🟡 Phases 3-4 : Intermédiaire (comprendre logique)"]
  Phase56["🔴 Phases 5-6 : Intermédiaire+ (autonomie requise)"]

  style Phase12 fill:#e3ffe3
  style Phase34 fill:#fff3e3
  style Phase56 fill:#ffe3e3

```

```mermaid
---
title: "Sept domaines de compétences Laravel"
---
graph LR
    M1[Phase 1<br/>Installation] --> M2[Phase 2<br/>Modèles]
    M2 --> M3[Phase 3<br/>Contrôleurs]
    M3 --> M4[Phase 4<br/>Routes]
    M4 --> M5[Phase 5<br/>Vues]
    M5 --> M6[Phase 6<br/>Tests]
    
    M1 -.-> C1[Composer<br/>Artisan CLI]
    M2 -.-> C2[Migrations<br/>Eloquent ORM<br/>Relations]
    M3 -.-> C3[Controllers<br/>Validation<br/>Authorization]
    M4 -.-> C4[Routes<br/>Middleware<br/>Route Groups]
    M5 -.-> C5[Blade Templates<br/>Layouts<br/>Components]
    M6 -.-> C6[Testing<br/>Debugging<br/>Best Practices]
    
    style M1 fill:#e3ffe3
    style M2 fill:#e3ffe3
    style M3 fill:#fff3e3
    style M4 fill:#fff3e3
    style M5 fill:#ffe3e3
    style M6 fill:#ffe3e3
```

<small>_Le diagramme présente les sept domaines de compétences Laravel développés tout au long du projet, avec leur niveau d'expertise atteint et leurs sous-compétences associées. Chaque compétence est contextualisée par rapport aux phases du projet : **les Migrations** et **Modèles Eloquent** sont acquis dès les phases 2-3, **les Contrôleurs** et **Routes** en phases 4-5, **les Vues Blade** en phase 6, tandis que **l'Authentification Breeze** est transversale (utilisée dès la phase 1 et enrichie jusqu'à la phase 7). Cette progression garantit une montée en compétence naturelle et structurée._</small>

## Fonctionnalités Complètes du Blog

### Pour les Visiteurs (Non Authentifiés)

<div class="cards grid" markdown>

- :fontawesome-solid-book-open: **Consultation**

    ---

    - Lire tous les articles publiés
    - Filtrer par catégorie
    - Voir profil auteurs
    - Rechercher articles (pagination)

- :fontawesome-solid-comments: **Interaction**

    ---

    - Commenter articles (nom + email)
    - Voir commentaires approuvés

</div>

### Pour les Auteurs (Utilisateurs Authentifiés)

<div class="cards grid" markdown>

- :fontawesome-solid-user-gear: **Gestion de compte**

    ---

    - S'inscrire avec vérification email
    - Se connecter / Déconnecter
    - Réinitialiser mot de passe oublié
    - Modifier profil (nom, email, bio, avatar)
    - Supprimer compte

- :fontawesome-solid-pen-to-square: **Gestion articles**

    ---

    - Créer article (brouillon ou publié)
    - Modifier ses articles uniquement
    - Supprimer ses articles
    - Voir statistiques (vues, commentaires)
    - Changer statut (brouillon ↔ publié)

- :fontawesome-solid-chart-line: **Dashboard personnel**

    ---

    - Statistiques globales (total articles, vues, commentaires)
    - Liste tous mes articles
    - Article le plus populaire
    - Accès rapide création/édition

- :fontawesome-solid-shield-halved: **Modération commentaires**

    ---

    - Approuver commentaires sur mes articles
    - Supprimer commentaires sur mes articles
</div>

## Architecture Technique Résumée

Cette section synthétise l'environnement technique complet du projet : de la stack technologique utilisée (**Laravel 11**, **MySQL**, **Blade**, **Tailwind CSS**) jusqu'à l'organisation concrète des fichiers et dossiers du projet. Comprendre cette architecture permet d'anticiper la structure du code, de localiser rapidement les composants lors du développement, et d'appréhender la séparation des responsabilités entre backend (**contrôleurs**, **modèles**), frontend (**vues Blade**), et persistance (**migrations**, **seeders**).

!!! info "Les deux vues présentées ci-dessous sont complémentaires"

    - la **Stack Technologique** détaille les outils et frameworks employés avec leur rôle précis
    - la **Structure Fichiers Finale** expose l'arborescence complète du projet une fois toutes les phases terminées.
    
    > Cette double lecture vous offre une vision stratégique (**quels outils**) et opérationnelle (**où trouver chaque fichier**).

=== "Stack Technologique"

    | Composant | Technologie | Rôle |
    |-----------|-------------|------|
    | **Backend** | Laravel 11 | Framework PHP MVC |
    | **Authentification** | Laravel Breeze | Starter kit auth |
    | **Base de Données** | MySQL 8.0+ | Stockage données |
    | **Frontend** | Blade + Tailwind CSS | Templates + Styling |
    | **Assets** | Vite | Compilation JS/CSS |
    | **ORM** | Eloquent | Mapping objet-relationnel |

=== "Structure Fichiers Finale"

    ```
    blog-breeze/
    ├── app/
    │   ├── Http/Controllers/
    │   │   ├── Auth/                    # Breeze (7 contrôleurs)
    │   │   ├── HomeController.php       # Page accueil
    │   │   ├── PostController.php       # CRUD articles
    │   │   ├── DashboardController.php  # Dashboard auteur
    │   │   ├── CommentController.php    # Gestion commentaires
    │   │   ├── CategoryController.php   # Filtres catégories
    │   │   ├── AuthorController.php     # Profil auteur
    │   │   └── ProfileController.php    # Édition profil
    │   └── Models/
    │       ├── User.php                 # Modèle utilisateur
    │       ├── Post.php                 # Modèle article
    │       ├── Category.php             # Modèle catégorie
    │       └── Comment.php              # Modèle commentaire
    ├── database/
    │   ├── migrations/
    │   │   ├── xxxx_create_users_table.php
    │   │   ├── xxxx_create_categories_table.php
    │   │   ├── xxxx_create_posts_table.php
    │   │   └── xxxx_create_comments_table.php
    │   └── seeders/
    │       ├── CategorySeeder.php       # 6 catégories
    │       └── DatabaseSeeder.php       # 3 users + 7 posts
    ├── resources/views/
    │   ├── layouts/app.blade.php        # Layout principal
    │   ├── home.blade.php               # Page accueil
    │   ├── dashboard.blade.php          # Dashboard auteur
    │   ├── posts/                       # Vues articles
    │   │   ├── show.blade.php
    │   │   ├── create.blade.php
    │   │   └── edit.blade.php
    │   ├── categories/show.blade.php    # Articles par catégorie
    │   ├── authors/show.blade.php       # Profil auteur public
    │   ├── profile/edit.blade.php       # Édition profil
    │   └── auth/                        # Vues Breeze auth
    └── routes/
        ├── web.php                      # Routes principales
        └── auth.php                     # Routes Breeze
    ```

## Prérequis et Environnement

Ce projet constitue la **suite naturelle d'un cours d'initiation à Laravel Breeze**, où vous avez déjà découvert les fondamentaux de l'authentification et du système de routing Laravel. Toutefois, **chaque concept sera systématiquement réexpliqué et contextualisé** dans les phases du projet, garantissant une compréhension complète même si vous abordez certains sujets pour la première fois. L'objectif est de consolider vos acquis sur Breeze tout en élargissant votre maîtrise de Laravel à travers un cas d'usage réel et professionnel.

Les prérequis techniques listés ci-dessous distinguent clairement les **connaissances indispensables** (bases PHP, SQL, HTML/CSS) des **compétences recommandées** (MVC, relations BDD) et des **technologies apprises durant le projet** (Eloquent, Blade). Cette distinction vous permet d'évaluer votre niveau de départ et d'anticiper les apprentissages à venir.

### Connaissances Requises

<div class="cards grid" markdown>

- :fontawesome-solid-circle-check: **Indispensables**

    ---

    - [x] Bases PHP (variables, fonctions, tableaux, classes)
    - [x] Bases SQL (SELECT, INSERT, UPDATE, DELETE)
    - [x] Bases HTML/CSS (structure page, sélecteurs)
    - [x] Terminal/Ligne de commande (cd, ls, navigation)

- :fontawesome-solid-circle-half-stroke: **Recommandées**

    ---

    - 🟡 MVC pattern (Model-View-Controller)
    - 🟡 Relations base de données (1-N, N-N)
    - 🟡 HTTP (GET, POST, sessions, cookies)
    - 🟡 Notions Laravel Breeze (authentification, middleware)

</div>

<div class="cards grid" markdown>

- :fontawesome-solid-graduation-cap: **Apprises durant le projet**

    ---

    - ✅ Laravel (architecture MVC complète)
    - ✅ Eloquent ORM (relations, scopes, mutators)
    - ✅ Blade templating (directives, components, layouts)
    - ✅ Validation et Authorization (Policies, Form Requests)
    - ✅ Migrations et Seeders (schema builder, factories)

</div>

<small>*Si vous avez suivi le cours d'initiation Laravel Breeze, vous possédez déjà les bases d'authentification (register, login, password reset) et la structure MVC de base. Ce projet enrichit ces connaissances en ajoutant la gestion complète d'un blog multi-auteurs avec relations complexes (User ↔ Post ↔ Category ↔ Comment), autorisation granulaire (ownership des articles), et interface utilisateur responsive. **Tous les concepts seront réexpliqués étape par étape**, y compris ceux vus dans le cours Breeze.*</small>

---

### Environnement Technique

**Logiciels requis :**

<div class="cards grid" markdown>

- :fontawesome-brands-php: **PHP & Composer**

    ---

    - **PHP 8.1+** (8.2 ou 8.3 recommandé)
    - **Composer 2.x** (gestionnaire dépendances)
    
    ```bash
    php -v        # Vérifier version PHP
    composer -V   # Vérifier version Composer
    ```

- :fontawesome-solid-database: **Base de Données**

    ---

    - **MySQL 8.0+** ou **MariaDB 10.5+**
    - Client GUI recommandé : phpMyAdmin, Adminer, DBeaver
    
    ```bash
    mysql --version   # Vérifier version MySQL
    ```

</div>

<div class="cards grid" markdown>

- :fontawesome-brands-node-js: **Node.js & NPM**

    ---

    - **Node.js 22+** (LTS recommandé)
    - **NPM 10+** (compilation assets Vite)
    
    ```bash
    node -v    # Vérifier version Node
    npm -v     # Vérifier version NPM
    ```

- :fontawesome-solid-code: **Éditeur de Code**

    ---

    - **VS Code** (recommandé)
    - Extensions utiles :
        - Laravel Extension Pack
        - PHP Intelephense
        - Blade Formatter
        - Tailwind CSS IntelliSense

</div>

---

**Systèmes d'exploitation supportés :**

| OS | Solutions | Recommandation |
|---|---|---|
| :fontawesome-brands-windows: **Windows 11** | Laravel Herd (officiel) | Docker Sail, Laragon |
| :fontawesome-brands-apple: **macOS** | Laravel Herd (officiel) | Docker Sail, Valet |
| :fontawesome-brands-linux: **Linux** | Docker Sail | Installation native (LAMP/LEMP) |

<small>_Laravel recommande officiellement **Laravel Herd** pour Windows et macOS : c'est un environnement de développement local ultra-rapide qui gère automatiquement PHP, Composer, Node.js et configure Laravel en un clic. **Docker Sail** est l'alternative cross-platform officielle, idéale pour Linux ou si vous souhaitez un environnement conteneurisé identique à la production. L'installation native reste possible mais nécessite une configuration manuelle plus complexe (voir [documentation officielle](https://laravel.com/docs/12.x/installation))._</small>


## Méthodologie d'Apprentissage

### Approche Pédagogique

!!! note "Ce projet suit une méthodologie très simple : **"Lire → Comprendre → Appliquer"**"

<div class="cards grid" markdown>

- :fontawesome-solid-book-open: **1 - LIRE** 
  
    ---

    > Chaque Phase commence par des explications claires

    - Vision d'ensemble de l'étape
    - Concepts théoriques nécessaires
    - Diagrammes et schémas

- :fontawesome-solid-lightbulb: **2. COMPRENDRE**

    ---

    > Pourquoi fait-on comme ça ?

    - Analogies concrètes
    - Comparaisons alternatives
    - Bonnes pratiques expliquées

</div>
<div class="cards grid" markdown>

- :fontawesome-solid-code: **3. APPLIQUER**

    ---

    > Code fonctionnel pas à pas

    - Commandes exactes à taper
    - Code complet à copier
    - Tests pour vérifier que ça marche

</div>

!!! tip "Philosophie : Zéro Magie Noire"
    **Vous ne copierez JAMAIS de code sans comprendre ce qu'il fait.** Chaque ligne est expliquée, chaque choix est justifié. L'objectif n'est pas de "faire marcher", c'est de **maîtriser**.

## Checklist de Validation

!!! quote "Avant de passer à la Phase 1, assurez-vous de pouvoir répondre OUI à toutes ces questions"

- [ ] Je comprends **pourquoi** on construit un blog multi-auteurs (cas d'usage réel)
- [ ] Je connais les **4 entités principales** (User, Post, Category, Comment)
- [ ] Je visualise les **relations entre entités** (1-N, N-1)
- [ ] Je comprends le **rôle de Breeze** (authentification pré-codée)
- [ ] Je sais ce que contiennent les **7 Phases** du projet
- [ ] Je connais la **durée estimée** de chaque Phase
- [ ] J'ai vérifié que j'ai les **prérequis techniques** (PHP, Composer, MySQL, Node.js)
- [ ] Je suis prêt à investir **2h-4h** pour compléter le projet

## Ce que vous allez construire

<div class="cards grid" markdown>

- :fontawesome-solid-users: **Un blog collaboratif professionnel**

    ---

    - [x] **Auteurs** peuvent s'inscrire, se connecter, vérifier leur email
    - [x] **Créer/Modifier/Supprimer** leurs propres articles
    - [x] **Gérer brouillons** avant publication
    - [x] **Assigner catégories** aux articles
    - [x] **Visiteurs** peuvent lire articles publiés et commenter
    - [x] **Dashboard personnel** avec statistiques (articles, vues, commentaires)
    - [x] **Page auteur** publique avec tous ses articles

- :fontawesome-solid-list-check: **Fonctionnalités détaillées**

    - Authentification complète (Register, Login, Reset Password, Email Verification)
    - CRUD articles avec ownership (user ne peut modifier que ses articles)
    - Système brouillon/publié
    - Commentaires publics (sans inscription)
    - Upload image d'article (optionnel)
    - Slug automatique pour URLs propres
    - Compteur de vues par article
    - Dashboard avec statistiques

</div>

## Sommaire Rapide

- [Phase 0 : Vision Globale](#phase-0-vision-globale)
- [Phase 1 : Installation et Configuration](#phase-1-installation-et-configuration-15-min)
- [Phase 2 : Base de Données et Modèles](#phase-2-créer-les-modèles-et-migrations-30-min)
- [Phase 3 : Seeders et Données de Test](#phase-3-seeders-pour-données-de-test-15-min)
- [Phase 4 : Contrôleurs et Logique Métier](#phase-4-contrôleurs-45-min)
- [Phase 5 : Routes](#phase-5-routes-15-min)
- [Phase 6 : Vues Blade et Interface](#phase-6-vues-blade-60-90-min)
- [Phase 7 : Tests Finaux](#phase-7-tests-finaux-et-vérification-15-min)


## PHASE 1 : Installation et Configuration (~20 min)

### Vue d'Ensemble de la Phase

> Cette première phase pose les **fondations techniques** de votre projet. Vous allez installer Laravel 11, configurer l'environnement de développement local, créer la base de données, puis installer Laravel Breeze pour obtenir un système d'authentification complet et fonctionnel. Cette étape est cruciale : un environnement mal configuré peut générer des erreurs difficiles à déboguer par la suite.

> À l'issue de cette phase, vous disposerez d'une application Laravel vierge avec authentification opérationnelle (**inscription**, **connexion**, **réinitialisation mot de passe**). Vous pourrez créer votre premier compte utilisateur et accéder au dashboard Breeze, confirmant ainsi que tout fonctionne correctement avant d'attaquer la logique métier du blog.

!!! warning "Prérequis à Vérifier avant de commencer, assurez-vous d'avoir installé PHP 8.1+, Composer, Node.js 22+, et votre environnement de développement local (Herd, Sail, ou stack native). Reportez-vous à la section **Prérequis et Environnement** si nécessaire."

### Étape 1.1 : Créer le Projet Laravel

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

### Étape 1.2 : Créer la Base de Données

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

### Étape 1.3 : Configurer le Fichier `.env`

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

### Étape 1.4 : Tester la Connexion Base de Données

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


### Étape 1.5 : Installer Laravel Breeze

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


### Étape 1.6 : Installer les Dépendances Frontend

> Breeze utilise **Vite** (_bundler moderne_) pour compiler les assets CSS (**Tailwind CSS**) et JavaScript (**Alpine.js**). Vous devez installer les dépendances Node.js et compiler les assets.

```bash
# Installer les dépendances NPM (définies dans package.json)
npm install

# Attendre la fin de l'installation (1-3 minutes)
# NPM télécharge Tailwind CSS, Vite, Alpine.js, PostCSS, etc.
```

**Compiler les assets :**

=== ":fontawesome-solid-hammer: Mode Développement (Watch)"

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

=== ":fontawesome-solid-box: Mode Production (Build)"

    ```bash
    # Compiler pour la production (minification, optimisation)
    npm run build
    
    # Résultat attendu :
    # vite v5.x.x building for production...
    # ✓ built in 3.45s
    ```
    
    !!! info "Utiliser `npm run build` uniquement avant déploiement production. En développement, préférer `npm run dev`."

<small>*Vite crée un serveur de développement sur `http://localhost:5173/` qui sert les assets compilés. Laravel charge automatiquement ces assets via la directive `@vite(['resources/css/app.css', 'resources/js/app.js'])` présente dans les layouts Blade. En production, `npm run build` génère des fichiers statiques optimisés dans `public/build/`.*</small>

!!! warning "Erreur Commune : Port 5173 Déjà Utilisé"
    Si vous voyez `Error: listen EADDRINUSE: address already in use :::5173`, c'est qu'une instance Vite tourne déjà. Fermez l'ancien terminal ou tuez le processus : 
    
    - **Windows** : `taskkill /F /IM node.exe`
    - **macOS/Linux** : `killall node`

### Étape 1.7 : Exécuter les Migrations Breeze

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

### Étape 1.8 : Démarrer le Serveur de Développement

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

### Étape 1.9 : Tester l'Authentification Breeze

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

### Étape 1.10 : Vérification Finale

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

### Résolution Problèmes Courants

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


## PHASE 2 : Base de Données et Modèles Eloquent (~30-40 minutes)

### Vue d'Ensemble de la Phase

> Cette deuxième phase constitue le **cœur technique** de votre blog multi-auteurs. Vous allez concevoir et implémenter la **structure de données complète** qui supportera toutes les fonctionnalités de l'application : utilisateurs, articles, catégories et commentaires. Cette phase se décompose en deux volets complémentaires : les **migrations** (structure des tables SQL) et les **modèles Eloquent** (représentation objet en PHP).

!!! note "Les migrations Laravel sont des **fichiers PHP versionnés** qui décrivent la structure de la base de données de manière programmatique. Contrairement aux scripts SQL bruts, elles permettent de **construire**, **modifier** et **supprimer** des tables de façon reproductible sur n'importe quel environnement (**développement**, **staging**, **production**). Chaque migration contient deux méthodes : **`up()`** pour appliquer les changements et **`down()`** pour les annuler."

!!! note "Les modèles Eloquent, quant à eux, sont des **classes PHP** qui représentent les tables de la base de données. Ils permettent d'interagir avec les données via une syntaxe orientée objet intuitive (**`$post->user->name`**) au lieu de requêtes SQL manuelles. Eloquent gère automatiquement les relations entre tables (**1-N**, **N-N**), **la validation**, **les événements** et bien plus."

!!! quote "À l'issue de cette phase, votre base de données disposera de **4 tables métier** (**`users`, `categories`, `posts`, `comments`**) avec **toutes leurs relations** configurées (**clés étrangères**, **cascade delete**), et vous pourrez manipuler ces données via des modèles Eloquent expressifs et puissants."

!!! danger "**Prérequis pour la Phase 2** : La Phase 1 doit être terminée avec succès : **projet Laravel créé**, **Breeze installé**, et **migrations de base exécutées**. Votre serveur de base de données (**MySQL**/**MariaDB**) doit être démarré."

### Étape 2.1 : Enrichir le Modèle User avec bio et avatar

**Contexte de l'étape :**

> Le modèle `User` généré par Breeze contient les colonnes essentielles pour l'authentification (`name`, `email`, `password`), mais notre blog nécessite des informations supplémentaires pour créer des **profils auteurs riches** : une biographie (`bio`) et un avatar (`avatar`). Plutôt que de créer une nouvelle migration, nous allons modifier la migration existante `create_users_table` avant de relancer toutes les migrations.

Cette approche est valide **uniquement en développement local** : si la migration avait déjà été exécutée en production, vous devriez créer une migration `ALTER TABLE` séparée. En développement, modifier la migration originale puis exécuter `migrate:fresh` est plus propre.

**Localiser et modifier la migration :**

Ouvrir le fichier `database/migrations/2014_10_12_000000_create_users_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table users avec colonnes authentification + profil auteur
     * 
     * Breeze fournit les colonnes de base (name, email, password).
     * On ajoute bio et avatar pour les profils publics d'auteurs.
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            // Clé primaire auto-incrémentée
            $table->id();
            
            // Colonnes authentification (fournies par Breeze)
            $table->string('name');                              // Nom complet de l'utilisateur
            $table->string('email')->unique();                   // Email (connexion + unicité)
            $table->timestamp('email_verified_at')->nullable();  // Date vérification email
            $table->string('password');                          // Mot de passe haché (bcrypt)
            
            // ✅ AJOUT : Colonnes profil auteur
            $table->text('bio')->nullable();      // Biographie auteur (max 65,535 caractères)
                                                   // nullable() = optionnel, peut être NULL
            $table->string('avatar')->nullable(); // URL image avatar (ex: Gravatar, Unsplash)
                                                   // string() = VARCHAR(255) par défaut
            
            // Token "Se souvenir de moi" (Breeze)
            $table->rememberToken();  // VARCHAR(100) pour cookie persistant
            
            // Timestamps automatiques (created_at, updated_at)
            $table->timestamps();     // Gérés automatiquement par Laravel
        });

        // Configuration session (Breeze)
        Schema::create('password_reset_tokens', function (Blueprint $table) {
            $table->string('email')->primary();
            $table->string('token');
            $table->timestamp('created_at')->nullable();
        });

        Schema::create('sessions', function (Blueprint $table) {
            $table->string('id')->primary();
            $table->foreignId('user_id')->nullable()->index();
            $table->string('ip_address', 45)->nullable();
            $table->text('user_agent')->nullable();
            $table->longText('payload');
            $table->integer('last_activity')->index();
        });
    }

    /**
     * Supprimer les tables créées
     * 
     * Méthode rollback : permet d'annuler la migration via php artisan migrate:rollback
     */
    public function down(): void
    {
        Schema::dropIfExists('sessions');
        Schema::dropIfExists('password_reset_tokens');
        Schema::dropIfExists('users');
    }
};
```

<small>*La colonne `bio` utilise le type `text` (jusqu'à 65 Ko) car une biographie peut contenir plusieurs paragraphes. La colonne `avatar` stocke une **URL** (pas le fichier binaire) : vous pouvez utiliser des services externes comme Gravatar, Unsplash, ou stocker l'image dans `storage/` et y pointer. Le modificateur `nullable()` signifie que ces champs peuvent rester vides : un utilisateur peut s'inscrire sans remplir sa bio ou choisir d'avatar.*</small>

!!! tip "Pourquoi pas une table `profiles` séparée ?"
    On pourrait créer une table `profiles` (1-1 avec `users`) pour séparer les données d'authentification des données de profil. C'est une bonne pratique pour des profils très volumineux (>10 colonnes), mais ici 2 colonnes supplémentaires ne justifient pas la complexité d'une jointure systématique.

### Étape 2.2 : Créer la Migration de la Table Categories

**Contexte de l'étape :**

Les catégories permettent d'**organiser les articles** par thématique (Technologie, Voyage, Cuisine, etc.). Chaque article appartiendra à exactement **une catégorie** (relation 1-N : une catégorie contient plusieurs articles). Cette table est volontairement simple : seulement un nom et un slug.

Le **slug** est une version URL-friendly du nom de la catégorie (`Technologie` → `technologie`), utilisé pour créer des URLs propres (`/category/technologie` au lieu de `/category/1`). Eloquent générera automatiquement les slugs via un événement `creating` dans le modèle.

**Générer le fichier de migration :**

```bash
# Créer une nouvelle migration pour la table categories
php artisan make:migration create_categories_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_categories_table
```

<small>*Artisan génère automatiquement le nom de classe `CreateCategoriesTable` et crée un fichier horodaté dans `database/migrations/`. Le timestamp garantit l'ordre d'exécution des migrations.*</small>

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_categories_table.php` :

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table categories
     * 
     * Structure minimaliste : chaque catégorie a un nom (affiché) 
     * et un slug (utilisé dans les URLs).
     * 
     * Exemple de données :
     * | id | name         | slug         | created_at | updated_at |
     * |----|--------------|--------------|------------|------------|
     * | 1  | Technologie  | technologie  | ...        | ...        |
     * | 2  | Voyage       | voyage       | ...        | ...        |
     */
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            // Clé primaire auto-incrémentée
            $table->id();
            
            // Nom de la catégorie (affiché dans l'interface)
            $table->string('name');  // VARCHAR(255) - Ex: "Technologie"
            
            // Slug URL-friendly (utilisé dans les routes)
            $table->string('slug')   // VARCHAR(255) - Ex: "technologie"
                  ->unique();        // INDEX UNIQUE : empêche doublons
                                     // Évite /category/technologie-1, technologie-2
            
            // Timestamps automatiques
            $table->timestamps();    // created_at, updated_at
        });
    }

    /**
     * Supprimer la table categories
     * 
     * ⚠️ CASCADE : Si on supprime cette table, les posts qui référencent 
     * ces catégories seront automatiquement supprimés (défini dans posts migration).
     */
    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
```

<small>*La contrainte `unique()` sur le slug est **critique** : elle empêche deux catégories d'avoir le même slug, ce qui causerait des conflits de routing (`/category/voyage` ne pourrait pas savoir quelle catégorie afficher). Laravel génère automatiquement un index unique en SQL : `UNIQUE KEY categories_slug_unique (slug)`.*</small>

**Tableau des types de colonnes utilisés :**

| Colonne | Type PHP | Type SQL | Taille Max | Indexation | Contrainte |
|---------|----------|----------|------------|------------|------------|
| `id` | `id()` | `BIGINT UNSIGNED` | 18 446 744 073 709 551 615 | PRIMARY KEY | AUTO_INCREMENT |
| `name` | `string()` | `VARCHAR(255)` | 255 caractères | Aucune | NOT NULL |
| `slug` | `string()` | `VARCHAR(255)` | 255 caractères | UNIQUE INDEX | NOT NULL, UNIQUE |
| `created_at` | `timestamps()` | `TIMESTAMP` | Date/heure | Aucune | NULLABLE |
| `updated_at` | `timestamps()` | `TIMESTAMP` | Date/heure | Aucune | NULLABLE |

### Étape 2.3 : Créer la Migration de la Table Posts

**Contexte de l'étape :**

La table `posts` est le **cœur du blog**. Elle stocke tous les articles avec leur contenu, métadonnées et relations vers `users` (auteur) et `categories`. Cette migration est plus complexe car elle introduit :

1. **Deux clés étrangères** : `user_id` (auteur) et `category_id` (thématique)
2. **Suppression en cascade** : si un user/catégorie est supprimé, ses posts le sont aussi
3. **Un système de statut** : `draft` (brouillon) ou `published` (publié)
4. **Des index de performance** : pour accélérer les requêtes fréquentes

**Générer la migration :**

```bash
# Créer la migration posts
php artisan make:migration create_posts_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_posts_table
```

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_posts_table.php` :

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table posts (articles du blog)
     * 
     * Cette table centralise tout le contenu du blog : titre, texte, image,
     * statut publication, compteurs de vues. Elle est reliée aux tables
     * users (auteur) et categories (thématique).
     * 
     * Structure relationnelle :
     * - Chaque post appartient à 1 user (relation N-1)
     * - Chaque post appartient à 1 category (relation N-1)
     * - Chaque post peut avoir N comments (relation 1-N)
     */
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            // Clé primaire
            $table->id();
            
            /*
            |--------------------------------------------------------------------------
            | RELATIONS (Clés étrangères)
            |--------------------------------------------------------------------------
            */
            
            // Relation vers users : qui a écrit cet article ?
            $table->foreignId('user_id')         // BIGINT UNSIGNED (même type que users.id)
                  ->constrained()                // Crée la contrainte FK vers users.id
                  ->onDelete('cascade');         // Si user supprimé → ses posts supprimés
                                                 // SQL: ON DELETE CASCADE
            
            // Relation vers categories : quelle est la thématique ?
            $table->foreignId('category_id')     // BIGINT UNSIGNED (même type que categories.id)
                  ->constrained()                // Crée la contrainte FK vers categories.id
                  ->onDelete('cascade');         // Si catégorie supprimée → posts supprimés
                                                 // SQL: ON DELETE CASCADE
            
            /*
            |--------------------------------------------------------------------------
            | CONTENU DE L'ARTICLE
            |--------------------------------------------------------------------------
            */
            
            // Titre de l'article
            $table->string('title');             // VARCHAR(255) - Ex: "Introduction à Laravel 11"
            
            // Slug URL-friendly (généré auto depuis le titre dans le modèle)
            $table->string('slug')               // VARCHAR(255) - Ex: "introduction-a-laravel-11"
                  ->unique();                    // INDEX UNIQUE - URLs uniques
            
            // Résumé court (affiché dans les listes d'articles)
            $table->text('excerpt');             // TEXT (max 65 Ko) - 2-3 phrases
                                                 // Ex: "Découvrez les nouveautés de Laravel 11..."
            
            // Contenu complet de l'article
            $table->longText('content');         // LONGTEXT (max 4 Go) - Article complet
                                                 // Peut contenir plusieurs milliers de mots
            
            /*
            |--------------------------------------------------------------------------
            | MÉTADONNÉES
            |--------------------------------------------------------------------------
            */
            
            // URL de l'image de couverture (optionnelle)
            $table->string('image')              // VARCHAR(255) - URL vers Unsplash, storage/...
                  ->nullable();                  // Peut être NULL si pas d'image
            
            // Statut de publication
            $table->enum('status', ['draft', 'published'])  // ENUM('draft','published')
                  ->default('draft');                       // Par défaut = brouillon
                                                            // draft = invisible public
                                                            // published = visible public
            
            // Date de publication effective (NULL si brouillon)
            $table->timestamp('published_at')    // TIMESTAMP - Quand l'article a été publié
                  ->nullable();                  // NULL si status = draft
                                                 // Rempli auto quand status passe à published
            
            // Compteur de vues (incrémenté à chaque visite)
            $table->unsignedInteger('views_count')  // INT UNSIGNED (max 4,294,967,295)
                  ->default(0);                     // Démarre à 0
            
            // Timestamps automatiques
            $table->timestamps();                // created_at, updated_at
            
            /*
            |--------------------------------------------------------------------------
            | INDEX DE PERFORMANCE
            |--------------------------------------------------------------------------
            | Ces index accélèrent les requêtes fréquentes. Sans eux, MySQL doit
            | parcourir TOUTE la table (FULL TABLE SCAN = lent sur >10k lignes).
            */
            
            // Index composite : requêtes "posts de cet auteur avec ce statut"
            $table->index(['user_id', 'status']);
            // Exemple SQL rapide : SELECT * FROM posts WHERE user_id=1 AND status='published'
            
            // Index simple : tri par date de publication (page d'accueil)
            $table->index('published_at');
            // Exemple SQL rapide : SELECT * FROM posts WHERE status='published' ORDER BY published_at DESC
        });
    }

    /**
     * Supprimer la table posts
     * 
     * ⚠️ Ordre important : cette table doit être supprimée AVANT users et categories
     * car elle contient des clés étrangères qui les référencent.
     * Laravel gère l'ordre automatiquement grâce aux timestamps des migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

<small>*Le choix de `longText` pour `content` permet de stocker des articles très longs (plusieurs dizaines de milliers de mots). Le type `text` (65 Ko) serait insuffisant pour des tutoriels détaillés. Le compteur `views_count` utilise `unsignedInteger` (jamais négatif) : avec 4 milliards de valeurs possibles, même un article viral ne débordera pas.*</small>

**Pourquoi ces index spécifiques ?**

| Index | Requête Accélérée | Gain de Performance |
|-------|-------------------|---------------------|
| `['user_id', 'status']` | "Afficher les articles publiés de cet auteur" (dashboard) | x10 à x100 sur 10k+ articles |
| `published_at` | "Lister les derniers articles publiés" (page d'accueil) | x5 à x50 avec ORDER BY |

!!! warning "Cascade Delete : Attention aux Suppressions"
    `onDelete('cascade')` signifie que **supprimer un utilisateur supprime automatiquement tous ses articles**. C'est voulu pour maintenir la cohérence des données (pas d'articles orphelins), mais il faut en informer l'utilisateur avant de supprimer son compte. Alternative : `onDelete('set null')` pour conserver les articles en les marquant "Auteur supprimé".

### Étape 2.4 : Créer la Migration de la Table Comments

**Contexte de l'étape :**

> La table `comments` gère les **commentaires publics** sur les articles. Particularité : les commentaires peuvent être laissés par des **visiteurs non inscrits** (pas de relation vers `users`), d'où les colonnes `author_name` et `author_email` au lieu d'une clé étrangère `user_id`.

!!! quote "Le système de **modération** (`approved`) permet aux auteurs d'articles de valider les commentaires avant qu'ils n'apparaissent publiquement, évitant ainsi le spam."

**Générer la migration :**

```bash
# Créer la migration comments
php artisan make:migration create_comments_table

# Résultat attendu :
# Created Migration: 2024_xx_xx_xxxxxx_create_comments_table
```

**Éditer le fichier généré :**

Ouvrir `database/migrations/202X_XX_XX_XXXXXX_create_comments_table.php` :

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Créer la table comments
     * 
     * Commentaires publics sur les articles du blog. Peuvent être laissés
     * par des visiteurs anonymes (pas besoin de compte). L'auteur de l'article
     * peut modérer (approuver/rejeter) chaque commentaire.
     * 
     * Relation : N comments appartiennent à 1 post (relation N-1)
     * Pas de relation vers users : les commentateurs ne sont pas inscrits
     */
    public function up(): void
    {
        Schema::create('comments', function (Blueprint $table) {
            // Clé primaire
            $table->id();
            
            /*
            |--------------------------------------------------------------------------
            | RELATION vers posts
            |--------------------------------------------------------------------------
            */
            
            // Sur quel article ce commentaire est-il posté ?
            $table->foreignId('post_id')         // BIGINT UNSIGNED (même type que posts.id)
                  ->constrained()                // Crée FK vers posts.id
                  ->onDelete('cascade');         // Si post supprimé → commentaires supprimés
                                                 // Logique : pas de commentaires orphelins
            
            /*
            |--------------------------------------------------------------------------
            | INFORMATIONS DU COMMENTATEUR (visiteur non inscrit)
            |--------------------------------------------------------------------------
            | Pas de user_id : les visiteurs peuvent commenter sans compte.
            | On stocke juste leur nom et email pour affichage et contact éventuel.
            */
            
            // Nom affiché publiquement
            $table->string('author_name');       // VARCHAR(255) - Ex: "Jean Durand"
                                                 // Saisi manuellement par le visiteur
            
            // Email (non affiché, sert pour gravatar ou contact)
            $table->string('author_email');      // VARCHAR(255) - Ex: "jean@example.com"
                                                 // Validé côté formulaire (format email)
            
            // Contenu du commentaire
            $table->text('content');             // TEXT (max 65 Ko) - Quelques paragraphes max
                                                 // Suffisant pour un commentaire classique
            
            /*
            |--------------------------------------------------------------------------
            | SYSTÈME DE MODÉRATION
            |--------------------------------------------------------------------------
            */
            
            // Statut d'approbation par l'auteur de l'article
            $table->boolean('approved')          // TINYINT(1) - 0 = en attente, 1 = approuvé
                  ->default(false);              // Par défaut = NON approuvé
                                                 // L'auteur doit manuellement approuver
            
            // Timestamps automatiques
            $table->timestamps();                // created_at (pour tri chronologique)
                                                 // updated_at (si commentaire édité)
            
            /*
            |--------------------------------------------------------------------------
            | INDEX DE PERFORMANCE
            |--------------------------------------------------------------------------
            */
            
            // Index composite : requête "commentaires approuvés de cet article"
            $table->index(['post_id', 'approved']);
            // Exemple SQL rapide : SELECT * FROM comments WHERE post_id=5 AND approved=1
            // Utilisé sur la page publique de l'article
        });
    }

    /**
     * Supprimer la table comments
     * 
     * Doit être supprimée AVANT posts car elle référence posts.id
     * (l'ordre des migrations garantit cela automatiquement).
     */
    public function down(): void
    {
        Schema::dropIfExists('comments');
    }
};
```

<small>*Le choix de `text` (65 Ko) pour `content` est suffisant : un commentaire de blog dépassant rarement 1000 mots. Le type `boolean` pour `approved` est stocké en SQL comme `TINYINT(1)` (0 ou 1) : plus compact qu'un `VARCHAR` et permet des index optimisés. L'index composite `['post_id', 'approved']` est crucial : sur un article avec 1000 commentaires, récupérer seulement les commentaires approuvés sans index nécessiterait de parcourir les 1000 lignes.*</small>

**Workflow de modération :**

1. **Visiteur poste un commentaire** → `approved = false` (invisible)
2. **Auteur de l'article reçoit une notification** (optionnel, à implémenter)
3. **Auteur modère** :
   - Approuver → `approved = true` (visible publiquement)
   - Rejeter/Supprimer → ligne supprimée de la BDD

!!! tip "Alternative : Modération automatique avec scoring"
    Pour éviter la modération manuelle, vous pourriez implémenter un système de **scoring anti-spam** : analyse des liens suspects, mots-clés spam, patterns (ex: Akismet API). Les commentaires avec score < seuil seraient auto-approuvés, les autres envoyés en modération.

### Étape 2.5 : Exécuter les Migrations

**Contexte de l'étape :**

> À ce stade, vous avez créé **4 fichiers de migration** (users modifié, categories, posts, comments), mais ils ne sont pas encore appliqués à la base de données MySQL. La commande `migrate:fresh` va :  
> 
> 1. **Supprimer toutes les tables existantes** (y compris celles de Breeze)
> 2. **Recréer toutes les tables** dans l'ordre chronologique des migrations
> 3. **Appliquer les contraintes** (clés étrangères, index, valeurs par défaut)

!!! danger "migrate:fresh DÉTRUIT les données"
    **Ne JAMAIS utiliser `migrate:fresh` en production** ! Cette commande supprime toutes les données. En production, utilisez `php artisan migrate` (applique uniquement les nouvelles migrations) ou créez des migrations `ALTER TABLE` pour modifier les tables existantes sans perte de données.

**Exécuter les migrations :**

```bash
# Supprimer toutes les tables et réappliquer toutes les migrations
php artisan migrate:fresh

# Alternative si migrate:fresh échoue (problème de permissions) :
# php artisan db:wipe  # Supprime tout
# php artisan migrate  # Recrée tout
```

**Sortie console attendue :**

```bash
Dropping all tables ...............................................DONE
Migration table created successfully.

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

Migrating: 2024_xx_xx_xxxxxx_create_categories_table
Migrated:  2024_xx_xx_xxxxxx_create_categories_table (18.23ms)

Migrating: 2024_xx_xx_xxxxxx_create_posts_table
Migrated:  2024_xx_xx_xxxxxx_create_posts_table (42.89ms)

Migrating: 2024_xx_xx_xxxxxx_create_comments_table
Migrated:  2024_xx_xx_xxxxxx_create_comments_table (25.34ms)
```

<small>*Chaque ligne `Migrated:` indique qu'une table a été créée avec succès. Le temps d'exécution (en millisecondes) est informatif : si une migration prend >5 secondes, c'est qu'elle contient beaucoup d'index ou de données initiales (seeders). L'ordre d'exécution respecte les timestamps des fichiers de migration (d'où l'importance de ne pas les renommer).*</small>

**Vérifier la structure créée dans MySQL :**

```bash
# Se connecter à MySQL
mysql -u root -p blog_breeze

# Lister toutes les tables
SHOW TABLES;
```

**Résultat attendu :**

```sql
+------------------------+
| Tables_in_blog_breeze  |
+------------------------+
| cache                  |  -- Breeze: cache applicatif
| cache_locks            |  -- Breeze: verrous cache distribué
| categories             |  ✅ Notre table
| comments               |  ✅ Notre table
| failed_jobs            |  -- Breeze: jobs en erreur
| jobs                   |  -- Breeze: file d'attente jobs
| migrations             |  -- Suivi des migrations exécutées
| password_reset_tokens  |  -- Breeze: reset password
| personal_access_tokens |  -- Sanctum API tokens (si utilisé)
| posts                  |  ✅ Notre table
| sessions               |  -- Breeze: sessions utilisateur
| users                  |  ✅ Notre table (enrichie)
+------------------------+
12 rows in set (0.00 sec)
```

**Inspecter la structure détaillée d'une table :**

```sql
-- Voir la structure complète de la table posts
DESCRIBE posts;

-- Résultat attendu :
+---------------+--------------------------------------------+------+-----+---------+----------------+
| Field         | Type                                       | Null | Key | Default | Extra          |
+---------------+--------------------------------------------+------+-----+---------+----------------+
| id            | bigint unsigned                            | NO   | PRI | NULL    | auto_increment |
| user_id       | bigint unsigned                            | NO   | MUL | NULL    |                |
| category_id   | bigint unsigned                            | NO   | MUL | NULL    |                |
| title         | varchar(255)                               | NO   |     | NULL    |                |
| slug          | varchar(255)                               | NO   | UNI | NULL    |                |
| excerpt       | text                                       | NO   |     | NULL    |                |
| content       | longtext                                   | NO   |     | NULL    |                |
| image         | varchar(255)                               | YES  |     | NULL    |                |
| status        | enum('draft','published')                  | NO   |     | draft   |                |
| published_at  | timestamp                                  | YES  | MUL | NULL    |                |
| views_count   | int unsigned                               | NO   |     | 0       |                |
| created_at    | timestamp                                  | YES  |     | NULL    |                |
| updated_at    | timestamp                                  | YES  |     | NULL    |                |
+---------------+--------------------------------------------+------+-----+---------+----------------+

-- Voir les clés étrangères et index
SHOW CREATE TABLE posts\G

-- Quitter MySQL
EXIT;
```

<small>*La colonne `Key` indique les index : `PRI` (clé primaire), `MUL` (index multiple/clé étrangère), `UNI` (index unique). Les contraintes `FOREIGN KEY` apparaissent dans `SHOW CREATE TABLE` avec leurs clauses `ON DELETE CASCADE`. Vérifiez que les types correspondent bien à vos attentes (notamment `enum` pour status et `longtext` pour content).*</small>

!!! success "Checkpoint Phase 2.5"
    À ce stade, votre base de données MySQL contient 12 tables dont 4 personnalisées (users, categories, posts, comments) avec toutes leurs relations et index. Vous pouvez passer aux modèles Eloquent.

### Étape 2.6 : Créer les Modèles Eloquent

**Contexte de l'étape :**

> Les migrations ont créé la **structure des tables en SQL**, mais pour **manipuler les données en PHP**, nous avons besoin de **modèles Eloquent**. Un modèle est une classe PHP qui représente une table et définit :

> 1. **Les colonnes modifiables** (`$fillable`) pour la protection contre mass-assignment
2. **Les relations** entre modèles (hasMany, belongsTo, etc.)
3. **Les scopes** : méthodes réutilisables pour filtrer les requêtes
4. **Les événements** : actions automatiques (ex: générer un slug à la création)
5. **Les casts** : conversion automatique de types (ex: `published_at` en objet Carbon)

!!! note "Laravel suit la convention "**nom de table pluriel = nom de modèle singulier**" : table `posts` ↔ modèle `Post`. Eloquent déduit automatiquement le nom de table, mais vous pouvez le forcer avec `protected $table = 'nom_table'`."

=== "Créer le Modèle Category"

    ```bash
    # Générer le modèle Category
    php artisan make:model Category

    # Résultat attendu :
    # Model created successfully.
    ```

    <small>*Cette commande crée le fichier `app/Models/Category.php`. Le flag `--migration` aurait créé automatiquement la migration associée, mais nous l'avons déjà faite manuellement.*</small>

    **Éditer `app/Models/Category.php` :**

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Support\Str;

    class Category extends Model
    {
        use HasFactory;  // Active les factories (génération données test)

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Les colonnes autorisées pour mass-assignment
         * 
         * Mass-assignment = remplir plusieurs colonnes d'un coup :
         * Category::create(['name' => 'Technologie', 'slug' => 'technologie']);
         * 
         * Sans $fillable, Laravel refuse par sécurité (protection contre injection).
         * Seules les colonnes listées ici peuvent être remplies massivement.
         * 
         * @var array<string>
         */
        protected $fillable = [
            'name',  // Nom de la catégorie
            'slug',  // Slug URL (généré auto, mais autorisé en cas d'override)
        ];

        /*
        |--------------------------------------------------------------------------
        | ÉVÉNEMENTS DU MODÈLE (Auto-génération du slug)
        |--------------------------------------------------------------------------
        */

        /**
         * Actions automatiques lors de la création/mise à jour
         * 
         * La méthode boot() s'exécute au chargement du modèle.
         * On y enregistre des événements (creating, updating, deleting, etc.)
         */
        protected static function boot()
        {
            parent::boot();  // Important : toujours appeler le boot parent

            /**
             * Événement creating : juste AVANT l'insertion en BDD
             * 
             * Si le slug est vide, on le génère automatiquement depuis le nom.
             * Exemple : "Technologie Web" → "technologie-web"
             */
            static::creating(function ($category) {
                // Si le slug n'est pas fourni manuellement
                if (empty($category->slug)) {
                    // Str::slug() convertit en URL-friendly :
                    // - Minuscules
                    // - Espaces → tirets
                    // - Accents supprimés (é → e)
                    // - Caractères spéciaux supprimés
                    $category->slug = Str::slug($category->name);
                }
            });

            /**
             * Alternative : gérer les doublons de slug
             * 
             * Si "Technologie" existe déjà, créer "technologie-1", "technologie-2", etc.
             * (Non implémenté ici pour rester simple, mais possible avec :)
             * 
             * $count = static::where('slug', 'LIKE', "{$category->slug}%")->count();
             * if ($count > 0) {
             *     $category->slug = "{$category->slug}-" . ($count + 1);
             * }
             */
        }

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Une catégorie a plusieurs posts (1-N)
         * 
         * Permet d'écrire : $category->posts (retourne Collection de Post)
         * 
         * Eloquent génère automatiquement la requête SQL :
         * SELECT * FROM posts WHERE category_id = ?
         * 
         * @return \Illuminate\Database\Eloquent\Relations\HasMany
         */
        public function posts()
        {
            return $this->hasMany(Post::class);
            // Équivaut à : return $this->hasMany(Post::class, 'category_id', 'id');
            // Laravel déduit automatiquement les clés (category_id, id)
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Nombre d'articles dans cette catégorie
         * 
         * Utilisation : $category->postsCount()
         * Alternative avec attribut : protected $appends = ['posts_count'];
         */
        public function postsCount()
        {
            return $this->posts()->count();
        }
    }
    ```

    <small>*La génération automatique du slug dans `boot()` est une **excellente pratique** : elle évite d'avoir à appeler manuellement `Str::slug()` partout dans le code. L'événement `creating` garantit que le slug est généré **avant** l'insertion en base, donc la contrainte `unique()` de la migration peut valider l'unicité immédiatement.*</small>

=== "Créer le Modèle Post"

    ```bash
    # Générer le modèle Post
    php artisan make:model Post

    # Résultat attendu :
    # Model created successfully.
    ```

    **Éditer `app/Models/Post.php` :**

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Support\Str;

    class Post extends Model
    {
        use HasFactory;

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * @var array<string>
         */
        protected $fillable = [
            'user_id',       // Auteur de l'article
            'category_id',   // Catégorie de l'article
            'title',         // Titre
            'slug',          // Slug URL (généré auto mais peut être overridé)
            'excerpt',       // Résumé court
            'content',       // Contenu complet
            'image',         // URL image couverture
            'status',        // draft ou published
            'published_at',  // Date publication (rempli auto si status=published)
        ];

        /**
         * Casts automatiques de types
         * 
         * Laravel convertit automatiquement ces colonnes :
         * - published_at (string en BDD) → objet Carbon (manipulation dates)
         * 
         * Exemple : $post->published_at->format('d/m/Y') fonctionne directement
         * 
         * @var array<string, string>
         */
        protected $casts = [
            'published_at' => 'datetime',  // TIMESTAMP → Carbon\Carbon
        ];

        /*
        |--------------------------------------------------------------------------
        | ÉVÉNEMENTS DU MODÈLE (Auto-slug et auto-publish_at)
        |--------------------------------------------------------------------------
        */

        protected static function boot()
        {
            parent::boot();

            /**
             * Événement creating : à la création d'un nouveau post
             */
            static::creating(function ($post) {
                // 1. Générer le slug si vide
                if (empty($post->slug)) {
                    $post->slug = Str::slug($post->title);
                    
                    // Gestion des doublons de slug
                    // Si "introduction-laravel" existe, créer "introduction-laravel-2"
                    $count = static::where('slug', 'LIKE', "{$post->slug}%")->count();
                    if ($count > 0) {
                        $post->slug = "{$post->slug}-" . ($count + 1);
                    }
                }
                
                // 2. Si status=published, définir published_at automatiquement
                if ($post->status === 'published' && empty($post->published_at)) {
                    $post->published_at = now();  // now() = Carbon::now()
                }
            });

            /**
             * Événement updating : lors d'une modification
             * 
             * Exemple : Un auteur passe son brouillon en publié
             */
            static::updating(function ($post) {
                // Si le status passe de draft à published
                if ($post->isDirty('status') &&           // La colonne status a changé
                    $post->status === 'published' &&      // Nouvelle valeur = published
                    empty($post->published_at)) {         // Et pas encore de date publication
                    
                    $post->published_at = now();          // On timestamp la publication
                }
            });

            /**
             * Note : On ne regénère PAS le slug lors de l'update du titre
             * Raison : changement d'URL casserait les liens existants (SEO)
             * Alternative : garder l'ancien slug ou créer une redirection 301
             */
        }

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un post appartient à un utilisateur (N-1)
         * 
         * Permet : $post->user (retourne instance de User)
         * SQL généré : SELECT * FROM users WHERE id = ?
         */
        public function user()
        {
            return $this->belongsTo(User::class);
        }
        
        /**
         * Alias de user() pour plus de clarté sémantique
         * 
         * Permet d'écrire : $post->author->name au lieu de $post->user->name
         */
        public function author()
        {
            return $this->user();
        }

        /**
         * Relation : Un post appartient à une catégorie (N-1)
         * 
         * Permet : $post->category (retourne instance de Category)
         */
        public function category()
        {
            return $this->belongsTo(Category::class);
        }

        /**
         * Relation : Un post a plusieurs commentaires (1-N)
         * 
         * Permet : $post->comments (retourne Collection de Comment)
         */
        public function comments()
        {
            return $this->hasMany(Comment::class);
        }

        /*
        |--------------------------------------------------------------------------
        | QUERY SCOPES (Filtres réutilisables)
        |--------------------------------------------------------------------------
        | Les scopes sont des méthodes de filtrage qu'on peut chaîner.
        | Convention : prefixe "scope" + nom en PascalCase
        | Utilisation : Post::published()->get()
        */

        /**
         * Scope : Récupérer seulement les posts publiés
         * 
         * Utilisation : Post::published()->get()
         * SQL : WHERE status='published' AND published_at IS NOT NULL AND published_at <= NOW()
         * 
         * @param \Illuminate\Database\Eloquent\Builder $query
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopePublished($query)
        {
            return $query->where('status', 'published')
                        ->whereNotNull('published_at')      // published_at doit être rempli
                        ->where('published_at', '<=', now()); // Date publication passée/actuelle
                                                              // (permet de programmer publication future)
        }

        /**
         * Scope : Récupérer seulement les brouillons
         * 
         * Utilisation : Post::draft()->get()
         */
        public function scopeDraft($query)
        {
            return $query->where('status', 'draft');
        }

        /**
         * Exemple de scope chaîné :
         * Post::published()->where('category_id', 1)->latest()->get()
         * = Articles publiés de la catégorie 1, triés par date DESC
         */

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Incrémenter le compteur de vues
         * 
         * Utilisation : $post->incrementViews()
         * SQL généré : UPDATE posts SET views_count = views_count + 1 WHERE id = ?
         * 
         * @return void
         */
        public function incrementViews()
        {
            $this->increment('views_count');
            // Équivaut à : $this->views_count++; $this->save();
            // Mais increment() génère un UPDATE optimisé en 1 seule requête
        }

        /**
         * Vérifier si le post est publié
         * 
         * @return bool
         */
        public function isPublished()
        {
            return $this->status === 'published' && $this->published_at !== null;
        }

        /**
         * Obtenir l'URL complète du post
         * 
         * @return string
         */
        public function getUrl()
        {
            return route('posts.show', $this->slug);
        }
    }
    ```

    <small>*Le scope `published()` est **crucial** : il évite d'écrire `where('status', 'published')` partout dans le code. Si demain vous ajoutez une condition supplémentaire (ex: `is_featured`), vous la modifiez une seule fois dans le scope, et tout le code en bénéficie automatiquement. La méthode `incrementViews()` utilise `increment()` plutôt que `$post->views_count++; $post->save();` pour éviter les conditions de concurrence (race conditions) si deux utilisateurs visitent l'article simultanément.*</small>

=== "Créer le Modèle Comment"

    ```bash
    # Générer le modèle Comment
    php artisan make:model Comment

    # Résultat attendu :
    # Model created successfully.
    ```

    **Éditer `app/Models/Comment.php` :**

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Factories\HasFactory;

    class Comment extends Model
    {
        use HasFactory;

        /*
        |--------------------------------------------------------------------------
        | CONFIGURATION DU MODÈLE
        |--------------------------------------------------------------------------
        */

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * @var array<string>
         */
        protected $fillable = [
            'post_id',       // Article commenté
            'author_name',   // Nom du commentateur (visiteur non inscrit)
            'author_email',  // Email du commentateur
            'content',       // Contenu du commentaire
            'approved',      // Statut modération (0=en attente, 1=approuvé)
        ];

        /**
         * Casts automatiques de types
         * 
         * approved (tinyint en BDD) → boolean en PHP
         * Permet d'écrire : if ($comment->approved) au lieu de if ($comment->approved == 1)
         * 
         * @var array<string, string>
         */
        protected $casts = [
            'approved' => 'boolean',
        ];

        /*
        |--------------------------------------------------------------------------
        | RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un commentaire appartient à un post (N-1)
         * 
         * Permet : $comment->post (retourne instance de Post)
         */
        public function post()
        {
            return $this->belongsTo(Post::class);
        }

        /**
         * Note : Pas de relation vers User
         * 
         * Les commentateurs ne sont pas des utilisateurs inscrits.
         * On stocke juste leur nom/email fournis dans le formulaire.
         * 
         * Alternative future : Permettre aux users connectés de commenter
         * avec auto-remplissage nom/email depuis leur profil.
         * → Ajouter colonne nullable('user_id') + relation belongsTo(User)
         */

        /*
        |--------------------------------------------------------------------------
        | QUERY SCOPES
        |--------------------------------------------------------------------------
        */

        /**
         * Scope : Récupérer seulement les commentaires approuvés
         * 
         * Utilisation : Comment::approved()->get()
         * Ou chaîné : $post->comments()->approved()->get()
         * 
         * @param \Illuminate\Database\Eloquent\Builder $query
         * @return \Illuminate\Database\Eloquent\Builder
         */
        public function scopeApproved($query)
        {
            return $query->where('approved', true);
        }

        /**
         * Scope : Commentaires en attente de modération
         * 
         * Utilisation : Comment::pending()->get()
         */
        public function scopePending($query)
        {
            return $query->where('approved', false);
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Approuver le commentaire
         * 
         * @return bool
         */
        public function approve()
        {
            $this->approved = true;
            return $this->save();
        }

        /**
         * Rejeter le commentaire (le marquer comme non approuvé)
         * 
         * @return bool
         */
        public function reject()
        {
            $this->approved = false;
            return $this->save();
        }

        /**
         * Obtenir l'avatar Gravatar du commentateur
         * 
         * @param int $size Taille de l'image en pixels
         * @return string URL de l'avatar
         */
        public function getGravatarUrl($size = 80)
        {
            $hash = md5(strtolower(trim($this->author_email)));
            return "https://www.gravatar.com/avatar/{$hash}?s={$size}&d=mp";
        }
    }
    ```

    <small>*Le scope `approved()` est essentiel pour afficher **uniquement les commentaires modérés** sur la page publique de l'article. La méthode `getGravatarUrl()` est une astuce pratique : elle génère automatiquement l'avatar du commentateur via son email en utilisant le service Gravatar (avatars universels associés aux emails). Si l'email n'a pas de Gravatar, Gravatar retourne un avatar par défaut (`d=mp` = mystère person).*</small>

=== "Enrichir le Modèle User"

    Le modèle `User` existe déjà (généré par Breeze), mais nous devons lui ajouter la relation vers `posts` et les colonnes `bio`/`avatar` dans `$fillable`.

    **Ouvrir `app/Models/User.php` et modifier :**

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable
    {
        use Notifiable;

        /**
         * Colonnes autorisées pour mass-assignment
         * 
         * ✅ AJOUTER bio et avatar à la liste existante
         * 
         * @var array<int, string>
         */
        protected $fillable = [
            'name',
            'email',
            'password',
            'bio',        // ✅ Ajouté : biographie auteur
            'avatar',     // ✅ Ajouté : URL avatar
        ];

        /**
         * Colonnes cachées lors de la sérialisation JSON
         * 
         * Important pour sécurité : empêche l'exposition du password hashé
         * dans les réponses API ou les logs.
         * 
         * @var array<int, string>
         */
        protected $hidden = [
            'password',
            'remember_token',
        ];

        /**
         * Casts automatiques
         * 
         * @return array<string, string>
         */
        protected function casts(): array
        {
            return [
                'email_verified_at' => 'datetime',
                'password' => 'hashed',  // Hash automatique du password à l'assignation
            ];
        }

        /*
        |--------------------------------------------------------------------------
        | ✅ AJOUTER : RELATIONS ELOQUENT
        |--------------------------------------------------------------------------
        */

        /**
         * Relation : Un utilisateur a plusieurs posts (1-N)
         * 
         * Permet : $user->posts (retourne Collection de Post)
         * Permet aussi : $user->posts()->published()->get() (chaîner scopes)
         * 
         * @return \Illuminate\Database\Eloquent\Relations\HasMany
         */
        public function posts()
        {
            return $this->hasMany(Post::class);
        }

        /*
        |--------------------------------------------------------------------------
        | MÉTHODES UTILITAIRES
        |--------------------------------------------------------------------------
        */

        /**
         * Obtenir l'initiale du nom (pour affichage avatar)
         * 
         * Exemple : "Alice Dupont" → "A"
         * Utilisé quand l'utilisateur n'a pas uploadé d'avatar
         * 
         * @return string
         */
        public function getInitial()
        {
            return strtoupper(substr($this->name, 0, 1));
        }

        /**
         * Vérifier si l'utilisateur a des articles publiés
         * 
         * @return bool
         */
        public function hasPublishedPosts()
        {
            return $this->posts()->published()->exists();
        }

        /**
         * Nombre total de vues sur tous les articles de l'auteur
         * 
         * @return int
         */
        public function totalViews()
        {
            return $this->posts()->sum('views_count');
        }
    }
    ```

    <small>*Les méthodes utilitaires `getInitial()`, `hasPublishedPosts()` et `totalViews()` ne sont pas obligatoires mais rendent le code des contrôleurs/vues plus lisible. Plutôt que d'écrire `strtoupper(substr($user->name, 0, 1))` partout, on écrit simplement `$user->getInitial()`. Ces méthodes sont appelées **accessors** ou **helper methods**.*</small>

### Récapitulatif Phase 2 : Ce que vous avez construit

=== "Migrations (Structure SQL)"

    - `users` enrichi avec `bio` et `avatar`
    - `categories` avec génération auto de slug
    - `posts` avec relations vers users/categories, statuts, compteur vues, index optimisés
    - `comments` avec modération, sans lien vers users (visiteurs anonymes)

=== "Modèles Eloquent (Représentation PHP)"

    - `Category` : génération auto slug, relation hasMany posts
    - `Post` : génération auto slug avec gestion doublons, auto-remplissage published_at, relations vers User/Category/Comment, scopes published/draft, méthode incrementViews
    - `Comment` : cast boolean pour approved, scopes approved/pending, méthodes approve/reject, génération Gravatar
    - `User` : relation hasMany posts, méthodes utilitaires (initial, total vues)

=== "Concepts Laravel maîtrisés"

    - Migrations avec clés étrangères, index, cascade delete
    - Eloquent relations (hasMany, belongsTo)
    - Mass assignment protection ($fillable)
    - Type casting ($casts)
    - Model events (boot, creating, updating)
    - Query scopes (filtres réutilisables)
    - Helper methods (méthodes utilitaires)

!!! success "Phase 2 Terminée - Votre architecture de données est maintenant **complète et opérationnelle**. Vous êtes prêt à passer à la **Phase 3 : Seeders** pour remplir la base avec des données de test réalistes, puis à la **Phase 4 : Contrôleurs** pour implémenter la logique métier du blog."






























## PHASE 3 : Seeders et Données de Test (~15-20 minutes)

### Vue d'Ensemble de la Phase

> Cette troisième phase constitue le **pont entre votre structure de données** (migrations + modèles) et **l'application fonctionnelle**. Les seeders sont des **classes PHP** qui peuplent automatiquement votre base de données avec des **données de test réalistes**. Sans eux, vous devriez créer manuellement chaque utilisateur, catégorie, article et commentaire via des formulaires, ce qui serait fastidieux et chronophage.

!!! note "Les seeders Laravel permettent de **réinitialiser rapidement** votre environnement de développement dans un état cohérent et prévisible"

    _Chaque fois que vous exécutez `migrate:fresh --seed`, Laravel supprime toutes les données existantes, recrée les tables, puis les remplit avec exactement les mêmes données de test. Cette reproductibilité est **essentielle** pour :_

    1. **Développer rapidement** : tester une fonctionnalité avec des données réalistes sans setup manuel
    2. **Déboguer efficacement** : reproduire un bug avec des données contrôlées
    3. **Onboarder de nouveaux développeurs** : un simple `migrate:fresh --seed` leur donne un environnement opérationnel
    4. **Démo client/manager** : présenter le projet avec des données professionnelles

!!! info "Laravel distingue deux approches pour générer des données"

    - **Seeders manuels** : vous définissez explicitement chaque enregistrement (idéal pour données de référence : catégories, rôles, paramètres)
    - **Factories** : génération aléatoire massive via Faker (idéal pour volumétrie : 1000+ users, 10 000+ posts)

Dans ce projet, nous utiliserons des **seeders manuels** pour garder le contrôle total sur les données de test : 3 auteurs avec des profils distincts, 7 articles variés (publiés + brouillons), 2 commentaires modérés. Ces données vous permettront de tester immédiatement toutes les fonctionnalités du blog sans configuration supplémentaire.

À l'issue de cette phase, votre base de données contiendra **un jeu de données complet et cohérent** : utilisateurs vérifiés, catégories diversifiées, articles avec différents statuts, compteurs de vues réalistes, et commentaires approuvés/en attente.

!!! warning "**Prérequis Phase 3** : Les Phases 1 et 2 doivent être terminées : migrations exécutées, modèles créés avec leurs relations. Votre base de données doit contenir les tables vides `users`, `categories`, `posts`, `comments`."

### Étape 3.1 : Créer le Seeder des Catégories

**Contexte de l'étape :**

> Les catégories constituent les **données de référence** (reference data) de votre blog : elles sont stables, définies en amont, et changent rarement une fois le blog en production. Plutôt que de laisser les utilisateurs créer des catégories anarchiquement, nous en définissons 6 cohérentes qui couvrent les grandes thématiques d'un blog généraliste.

!!! quote "Ce seeder sera appelé **en premier** par le `DatabaseSeeder` car les posts ont besoin de catégories existantes (contrainte de clé étrangère `posts.category_id`). L'ordre d'exécution des seeders est crucial pour respecter l'intégrité référentielle."

**Générer le fichier seeder :**

```bash
# Créer un seeder dédié aux catégories
php artisan make:seeder CategorySeeder

# Résultat attendu :
# Seeder created successfully.
# Created Seeder: Database\Seeders\CategorySeeder
```

<small>*Cette commande génère le fichier `database/seeders/CategorySeeder.php` avec une structure de base. Les seeders sont des classes normales PHP avec une méthode `run()` qui contient la logique d'insertion des données.*</small>

**Éditer le fichier généré :**

Ouvrir `database/seeders/CategorySeeder.php` et **remplacer tout le contenu** par :

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Category;

class CategorySeeder extends Seeder
{
    /**
     * Peupler la table categories avec les catégories de base du blog
     * 
     * Cette méthode est appelée par DatabaseSeeder::run() via $this->call().
     * Elle crée les 6 catégories principales qui structureront le contenu du blog.
     * 
     * Pourquoi définir manuellement plutôt que via une factory ?
     * - Les catégories sont des données de référence stables
     * - On veut un contrôle total sur les noms/slugs (pas de génération aléatoire)
     * - Le nombre est fixe et limité (6 catégories)
     * 
     * @return void
     */
    public function run(): void
    {
        /*
        |--------------------------------------------------------------------------
        | Définition des Catégories
        |--------------------------------------------------------------------------
        | Chaque catégorie est un tableau associatif avec :
        | - name : Nom affiché dans l'interface (ex: "Technologie")
        | - slug : Version URL-friendly (ex: "technologie")
        |
        | Note : Le slug pourrait être omis car le modèle Category le génère
        | automatiquement via l'événement creating(), mais on le spécifie ici
        | pour garantir des URLs prévisibles et éviter toute variation.
        */
        
        $categories = [
            // Catégorie 1 : Articles tech (Laravel, Vue.js, etc.)
            [
                'name' => 'Technologie',
                'slug' => 'technologie'
            ],
            
            // Catégorie 2 : Récits de voyage et guides destinations
            [
                'name' => 'Voyage',
                'slug' => 'voyage'
            ],
            
            // Catégorie 3 : Recettes et astuces culinaires
            [
                'name' => 'Cuisine',
                'slug' => 'cuisine'
            ],
            
            // Catégorie 4 : Actualité sportive et conseils fitness
            [
                'name' => 'Sport',
                'slug' => 'sport'
            ],
            
            // Catégorie 5 : Mode de vie, bien-être, développement personnel
            [
                'name' => 'Lifestyle',
                'slug' => 'lifestyle'
            ],
            
            // Catégorie 6 : Entrepreneuriat, marketing, business
            [
                'name' => 'Business',
                'slug' => 'business'
            ],
        ];

        /*
        |--------------------------------------------------------------------------
        | Insertion en Base de Données
        |--------------------------------------------------------------------------
        | On parcourt le tableau et on crée chaque catégorie via Eloquent.
        |
        | Méthode 1 (utilisée ici) : Boucle foreach + create()
        | - Simple et lisible
        | - Une requête INSERT par catégorie (6 requêtes au total)
        | - Idéal pour <50 enregistrements
        |
        | Méthode 2 (alternative pour volumétrie) : insert()
        | - Category::insert($categories);
        | - Une seule requête INSERT pour toutes les catégories
        | - Plus rapide, mais ne déclenche pas les événements Eloquent
        |   (created_at/updated_at non remplis automatiquement)
        */
        
        foreach ($categories as $category) {
            Category::create($category);
            // SQL généré : INSERT INTO categories (name, slug, created_at, updated_at) 
            //              VALUES ('Technologie', 'technologie', NOW(), NOW())
        }

        /*
        |--------------------------------------------------------------------------
        | Gestion des Doublons (Idempotence)
        |--------------------------------------------------------------------------
        | Si vous exécutez ce seeder plusieurs fois sans migrate:fresh,
        | vous obtiendrez une erreur UNIQUE constraint sur le slug.
        |
        | Pour rendre ce seeder idempotent (exécutable plusieurs fois),
        | vous pourriez utiliser updateOrCreate() :
        |
        | foreach ($categories as $category) {
        |     Category::updateOrCreate(
        |         ['slug' => $category['slug']],  // Critère de recherche
        |         $category                       // Données à créer/mettre à jour
        |     );
        | }
        |
        | SQL généré :
        | 1. SELECT * FROM categories WHERE slug = 'technologie'
        | 2. Si existe → UPDATE, sinon → INSERT
        |
        | Avantage : vous pouvez modifier le nom d'une catégorie et re-seeder
        | sans erreur. Inconvénient : 2x plus de requêtes (SELECT + INSERT/UPDATE).
        */
    }
}
```

<small>*Le choix de `create()` plutôt que `insert()` garantit que les événements Eloquent sont déclenchés (notamment `creating` qui génère le slug automatiquement si absent) et que les timestamps `created_at`/`updated_at` sont remplis. La méthode `insert()` serait plus performante pour insérer 1000+ catégories, mais ici 6 enregistrements ne justifient pas l'optimisation.*</small>

**Tableau récapitulatif des catégories créées :**

| ID | Nom | Slug | Usage Typique | Exemples d'Articles |
|----|-----|------|---------------|---------------------|
| 1 | Technologie | `technologie` | Tutoriels dev, actualité tech | Laravel 11, Vue.js, IA |
| 2 | Voyage | `voyage` | Guides destinations, carnets | Japon, Thaïlande, Islande |
| 3 | Cuisine | `cuisine` | Recettes, techniques culinaires | Tarte aux pommes, pâtes |
| 4 | Sport | `sport` | Actualité sportive, fitness | Marathon, yoga, nutrition |
| 5 | Lifestyle | `lifestyle` | Bien-être, mode, décoration | Minimalisme, slow life |
| 6 | Business | `business` | Entrepreneuriat, marketing | Stratégie, SEO, financement |

!!! tip "Personnalisation des Catégories - Vous pouvez adapter ces catégories à votre niche : pour un blog tech pur, remplacez Voyage/Cuisine par Backend/Frontend/DevOps. Pour un blog lifestyle, ajoutez Mode/Beauté/Parentalité. L'important est de définir des catégories **mutuellement exclusives** (un article appartient à une seule catégorie) et **exhaustives** (toute thématique d'article est couverte)."


### Étape 3.2 : Créer les Données de Test Complètes dans DatabaseSeeder

**Contexte de l'étape :**

> Le `DatabaseSeeder` est le **point d'entrée principal** de tous les seeders Laravel. C'est lui qui orchestre l'ordre d'exécution et appelle les seeders spécialisés via `$this->call()`. Dans notre cas, il va :

> 1. **Appeler CategorySeeder** pour créer les 6 catégories
2. **Créer 3 utilisateurs** avec des profils distincts (techie, voyageur, cuisinière)
3. **Créer 7 articles** : 6 publiés + 1 brouillon, répartis entre les auteurs
4. **Créer 2 commentaires** : 1 approuvé + 1 en attente de modération

!!! quote "Ce jeu de données est conçu pour **tester tous les cas d'usage** : articles d'auteurs différents, brouillons vs publiés, catégories variées, compteurs de vues réalistes, commentaires modérés. Vous pourrez immédiatement tester le dashboard, les filtres par catégorie, la modération, etc."

**Localiser et éditer le fichier existant :**

Le fichier `database/seeders/DatabaseSeeder.php` existe déjà (créé par Laravel).  
Ouvrir et **remplacer tout le contenu** par :

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Post;
use App\Models\Comment;
use App\Models\Category;

class DatabaseSeeder extends Seeder
{
    /**
     * Seeder principal : orchestre la création de toutes les données de test
     * 
     * Cette méthode est exécutée via : php artisan db:seed
     * Ou automatiquement via : php artisan migrate:fresh --seed
     * 
     * Ordre d'exécution CRITIQUE :
     * 1. Catégories (aucune dépendance)
     * 2. Users (aucune dépendance)
     * 3. Posts (dépend de users + categories)
     * 4. Comments (dépend de posts)
     * 
     * Si vous inversez l'ordre, vous obtiendrez des erreurs de clé étrangère.
     * 
     * @return void
     */
    public function run(): void
    {
        /*
        |--------------------------------------------------------------------------
        | ÉTAPE 1 : Créer les Catégories
        |--------------------------------------------------------------------------
        | On appelle le CategorySeeder qui crée les 6 catégories de base.
        | $this->call() exécute la méthode run() du seeder spécifié.
        */
        
        $this->call(CategorySeeder::class);
        
        // À ce stade : 6 catégories en BDD (Technologie, Voyage, Cuisine, etc.)

        /*
        |--------------------------------------------------------------------------
        | ÉTAPE 2 : Créer les Utilisateurs (Auteurs du Blog)
        |--------------------------------------------------------------------------
        | On crée 3 utilisateurs avec des profils distincts pour tester :
        | - Les relations user → posts (chaque user aura ses propres articles)
        | - Les permissions (ownership : un user ne peut modifier que SES articles)
        | - Les pages auteur publiques (profil avec bio, avatar, stats)
        |
        | Pourquoi 3 utilisateurs et pas plus ?
        | - Suffisant pour tester la multi-auteurs (>1)
        | - Assez petit pour rester lisible (on sait qui a écrit quoi)
        | - Correspond aux 3 catégories principales (tech, voyage, cuisine)
        */

        // Auteur 1 : Alice - Profil Tech/Dev
        $user1 = User::create([
            'name' => 'Alice Dupont',                // Nom complet
            'email' => 'alice@example.com',          // Email de connexion
            'password' => bcrypt('password'),        // Hash bcrypt du mot de passe
                                                     // En dev, on utilise 'password' pour simplifier
                                                     // En prod, générer des mots de passe forts aléatoires
            
            'bio' => 'Passionnée de technologie et de développement web.', // Biographie auteur
            
            'email_verified_at' => now(),            // Email déjà vérifié (évite étape vérification)
                                                     // now() = Carbon::now() = timestamp actuel
        ]);

        // Auteur 2 : Bob - Profil Voyage/Photo
        $user2 = User::create([
            'name' => 'Bob Martin',
            'email' => 'bob@example.com',
            'password' => bcrypt('password'),
            'bio' => 'Voyageur et photographe amateur.',
            'email_verified_at' => now(),
        ]);

        // Auteur 3 : Claire - Profil Cuisine/Food
        $user3 = User::create([
            'name' => 'Claire Bernard',
            'email' => 'claire@example.com',
            'password' => bcrypt('password'),
            'bio' => 'Chef cuisinière et blogueuse culinaire.',
            'email_verified_at' => now(),
        ]);

        /*
        |--------------------------------------------------------------------------
        | ÉTAPE 3 : Récupérer les Catégories pour les Associer aux Posts
        |--------------------------------------------------------------------------
        | On récupère TOUTES les catégories créées à l'étape 1.
        | On aurait pu faire Category::find(1), find(2), etc., mais utiliser
        | where('slug', 'technologie') est plus robuste si l'ordre change.
        */
        
        $categories = Category::all();  // Collection de 6 objets Category
        
        // Vérification de sécurité (optionnelle en dev, recommandée en prod)
        if ($categories->count() === 0) {
            throw new \Exception('Aucune catégorie trouvée. Exécutez CategorySeeder d\'abord.');
        }

        /*
        |--------------------------------------------------------------------------
        | ÉTAPE 4 : Créer les Articles (Posts)
        |--------------------------------------------------------------------------
        | On crée 7 posts au total :
        | - 3 posts pour Alice (2 publiés + 1 brouillon) → catégorie Technologie
        | - 2 posts pour Bob (2 publiés) → catégorie Voyage
        | - 2 posts pour Claire (1 publié + 1 publié) → catégories Cuisine + autre
        |
        | Cette répartition permet de tester :
        | - Dashboard avec plusieurs articles par auteur
        | - Brouillons (invisibles sauf pour l'auteur)
        | - Compteurs de vues variés
        | - Dates de publication échelonnées
        */

        /*
        |----------------------------------------------------------------------
        | Posts d'Alice (Technologie)
        |----------------------------------------------------------------------
        */
        
        // Post 1 : Article publié populaire (150 vues)
        $post1 = Post::create([
            'user_id' => $user1->id,  // Alice est l'auteure
            
            // Récupérer l'ID de la catégorie "Technologie"
            // where('slug', 'technologie') filtre par slug
            // first() retourne le premier résultat
            // ->id extrait la clé primaire
            'category_id' => $categories->where('slug', 'technologie')->first()->id,
            
            'title' => 'Introduction à Laravel 11',
            
            // Le slug sera généré automatiquement par le modèle Post (événement creating)
            // mais on pourrait le spécifier : 'slug' => 'introduction-a-laravel-11'
            
            'excerpt' => 'Découvrez les nouveautés de Laravel 11 et comment démarrer votre premier projet.',
            
            'content' => 'Laravel 11 apporte de nombreuses améliorations par rapport aux versions précédentes. '
                       . 'Dans cet article, nous allons explorer les principales nouveautés : '
                       . 'amélioration des performances, nouvelle syntaxe pour les routes, '
                       . 'intégration native de Vite, et bien plus encore. '
                       . 'Vous apprendrez également à installer Laravel 11 et à créer votre première application.',
            
            'status' => 'published',             // Article visible publiquement
            'published_at' => now()->subDays(5), // Publié il y a 5 jours
                                                 // now()->subDays(5) = Carbon::now()->subDays(5)
            
            'views_count' => 150,                // Compteur de vues réaliste
        ]);

        // Post 2 : Article publié récent (87 vues)
        Post::create([
            'user_id' => $user1->id,
            'category_id' => $categories->where('slug', 'technologie')->first()->id,
            'title' => 'Les Bases de Vue.js',
            'excerpt' => 'Un guide complet pour démarrer avec Vue.js 3.',
            'content' => 'Vue.js est un framework JavaScript progressif pour construire des interfaces utilisateur. '
                       . 'Contrairement à d\'autres frameworks monolithiques, Vue est conçu pour être adopté '
                       . 'de manière incrémentale. Ce tutoriel couvre les concepts fondamentaux : '
                       . 'composants, réactivité, directives, et computed properties.',
            'status' => 'published',
            'published_at' => now()->subDays(3),  // Publié il y a 3 jours
            'views_count' => 87,
        ]);

        // Post 3 : Brouillon (non publié, invisible)
        Post::create([
            'user_id' => $user1->id,
            'category_id' => $categories->where('slug', 'technologie')->first()->id,
            'title' => 'Brouillon : API REST avec Sanctum',
            'excerpt' => 'Comment sécuriser votre API avec Laravel Sanctum.',
            'content' => 'Laravel Sanctum fournit un système d\'authentification simple pour les SPA '
                       . '(Single Page Applications) et les API. Dans ce guide, nous verrons comment '
                       . 'configurer Sanctum pour protéger vos endpoints API.',
            'status' => 'draft',                  // Brouillon
            // published_at reste NULL (le modèle Post ne le remplit que si status=published)
        ]);

        /*
        |----------------------------------------------------------------------
        | Posts de Bob (Voyage)
        |----------------------------------------------------------------------
        */
        
        // Post 4 : Article le plus populaire du blog (230 vues)
        Post::create([
            'user_id' => $user2->id,
            'category_id' => $categories->where('slug', 'voyage')->first()->id,
            'title' => 'Découvrir le Japon en 2 Semaines',
            'excerpt' => 'Itinéraire complet pour un premier voyage au Japon.',
            'content' => 'Le Japon est une destination fascinante qui mélange tradition et modernité. '
                       . 'Dans cet article, je partage mon itinéraire de 2 semaines : '
                       . 'Tokyo (4 jours), Kyoto (3 jours), Mont Fuji (2 jours), Osaka (2 jours), '
                       . 'Hiroshima (2 jours), et retour à Tokyo (1 jour). '
                       . 'Conseils pratiques, budget, et bons plans inclus.',
            'status' => 'published',
            'published_at' => now()->subDays(7),  // Publié il y a 1 semaine
            'views_count' => 230,                 // Article viral
        ]);

        // Post 5 : Article récent (112 vues)
        Post::create([
            'user_id' => $user2->id,
            'category_id' => $categories->where('slug', 'voyage')->first()->id,
            'title' => 'Les Plus Belles Plages de Thaïlande',
            'excerpt' => 'Notre sélection des plages paradisiaques thaïlandaises.',
            'content' => 'La Thaïlande regorge de plages magnifiques. Voici mon top 5 : '
                       . '1. Railay Beach (Krabi) - Accessible uniquement en bateau, entourée de falaises '
                       . '2. Maya Bay (Koh Phi Phi) - Rendue célèbre par le film "La Plage" '
                       . '3. White Sand Beach (Koh Chang) - Sable blanc et eaux turquoise '
                       . '4. Sunrise Beach (Koh Lipe) - Idéale pour admirer le lever du soleil '
                       . '5. Patong Beach (Phuket) - Animation et vie nocturne',
            'status' => 'published',
            'published_at' => now()->subDays(2),  // Publié il y a 2 jours
            'views_count' => 112,
        ]);

        /*
        |----------------------------------------------------------------------
        | Posts de Claire (Cuisine)
        |----------------------------------------------------------------------
        */
        
        // Post 6 : Article populaire (342 vues)
        Post::create([
            'user_id' => $user3->id,
            'category_id' => $categories->where('slug', 'cuisine')->first()->id,
            'title' => 'Recette : Tarte aux Pommes Maison',
            'excerpt' => 'La recette traditionnelle de la tarte aux pommes française.',
            'content' => 'Ingrédients pour 6 personnes : '
                       . '- 1 pâte brisée ou feuilletée '
                       . '- 4 grosses pommes (Golden ou Granny Smith) '
                       . '- 50g de sucre '
                       . '- 30g de beurre '
                       . '- 1 sachet de sucre vanillé '
                       . 'Préparation : '
                       . '1. Préchauffer le four à 180°C '
                       . '2. Étaler la pâte dans un moule beurré '
                       . '3. Éplucher et couper les pommes en fines tranches '
                       . '4. Disposer les pommes en rosace sur la pâte '
                       . '5. Saupoudrer de sucre et parsemer de noisettes de beurre '
                       . '6. Enfourner 35-40 minutes jusqu\'à ce que les pommes soient dorées',
            'status' => 'published',
            'published_at' => now()->subDays(4),  // Publié il y a 4 jours
            'views_count' => 342,                 // Article très populaire
        });

        // Post 7 : Article Business (pour varier les catégories)
        Post::create([
            'user_id' => $user3->id,
            'category_id' => $categories->where('slug', 'business')->first()->id,
            'title' => 'Lancer son Blog Culinaire en 2024',
            'excerpt' => 'Guide complet pour monétiser votre passion de la cuisine.',
            'content' => 'Vous adorez cuisiner et souhaitez partager vos recettes ? '
                       . 'Créer un blog culinaire peut devenir une activité rentable. '
                       . 'Dans ce guide, je vous explique comment : '
                       . '- Choisir un nom et une niche '
                       . '- Créer un site WordPress avec des plugins adaptés '
                       . '- Photographier vos plats comme un pro '
                       . '- Optimiser vos recettes pour le SEO '
                       . '- Monétiser via affiliation, ebooks, et partenariats marques',
            'status' => 'published',
            'published_at' => now()->subDays(1),  // Publié hier
            'views_count' => 54,                  // Article récent, peu de vues encore
        ]);

        /*
        |--------------------------------------------------------------------------
        | ÉTAPE 5 : Créer les Commentaires
        |--------------------------------------------------------------------------
        | On crée 2 commentaires sur le premier article d'Alice :
        | - 1 commentaire approuvé (visible publiquement)
        | - 1 commentaire non approuvé (visible seulement par Alice dans son dashboard)
        |
        | Cela permet de tester :
        | - L'affichage public (seulement commentaires approved=true)
        | - La modération dans le dashboard auteur
        | - Les boutons "Approuver" / "Supprimer"
        */

        // Commentaire 1 : Approuvé (visible)
        Comment::create([
            'post_id' => $post1->id,              // Sur l'article "Introduction à Laravel 11"
            'author_name' => 'Jean Durand',       // Nom du commentateur (visiteur)
            'author_email' => 'jean@example.com', // Email (pour Gravatar)
            'content' => 'Excellent article ! Très clair et bien expliqué.',
            'approved' => true,                   // Approuvé par Alice
        ]);

        // Commentaire 2 : En attente de modération (invisible)
        Comment::create([
            'post_id' => $post1->id,
            'author_name' => 'Marie Lefebvre',
            'author_email' => 'marie@example.com',
            'content' => 'Merci pour ce tuto, ça m\'a beaucoup aidé !',
            'approved' => false,                  // En attente (Alice devra l'approuver)
        ]);

        /*
        |--------------------------------------------------------------------------
        | Affichage de Confirmation dans la Console
        |--------------------------------------------------------------------------
        | (Optionnel) Afficher un message pour confirmer le seeding réussi.
        | Utile lors du débogage ou pour suivre la progression.
        */
        
        $this->command->info('✅ Seeders exécutés avec succès !');
        $this->command->info('📊 Données créées :');
        $this->command->info('   - 6 catégories');
        $this->command->info('   - 3 utilisateurs (alice@example.com, bob@example.com, claire@example.com)');
        $this->command->info('   - 7 posts (6 publiés + 1 brouillon)');
        $this->command->info('   - 2 commentaires (1 approuvé + 1 en attente)');
        $this->command->info('🔐 Mot de passe pour tous les users : password');
    }
}
```

<small>*L'ordre d'insertion est **critique** : si vous créez les posts avant les catégories, MySQL retournera une erreur `FOREIGN KEY constraint fails` car `posts.category_id` référence une catégorie inexistante. Le helper `now()->subDays(X)` utilise Carbon pour créer des dates réalistes : cela permet de tester les filtres chronologiques et les pages "Articles récents". Le hash `bcrypt('password')` génère un hash sécurisé du mot de passe : **ne jamais stocker de mots de passe en clair** même en dev.*</small>

**Tableau récapitulatif des données créées :**

| Entité | Quantité | Détails |
|--------|----------|---------|
| **Users** | 3 | Alice (tech), Bob (voyage), Claire (cuisine) |
| **Categories** | 6 | Technologie, Voyage, Cuisine, Sport, Lifestyle, Business |
| **Posts** | 7 | 6 publiés (vues : 54-342) + 1 brouillon |
| **Comments** | 2 | 1 approuvé + 1 en attente |

**Répartition des articles par auteur :**

| Auteur | Publiés | Brouillons | Total Vues | Catégories |
|--------|---------|------------|------------|------------|
| Alice | 2 | 1 | 237 | Technologie |
| Bob | 2 | 0 | 342 | Voyage |
| Claire | 2 | 0 | 396 | Cuisine, Business |

!!! tip "Personnalisation des Données de Test"
    Vous pouvez enrichir ces seeders avec :
    - **Plus d'utilisateurs** : ajouter 5-10 auteurs pour tester la pagination des profils
    - **Plus d'articles** : créer 50-100 posts via une boucle `for` pour tester les performances de pagination
    - **Images de couverture** : ajouter des URLs Unsplash (`'image' => 'https://source.unsplash.com/random/800x600?technology'`)
    - **Commentaires massifs** : 10-20 commentaires par article pour tester la modération en volume

### Étape 3.3 : Exécuter les Seeders et Vérifier les Données

**Contexte de l'étape :**

> Maintenant que les seeders sont prêts, il faut **les exécuter** pour peupler la base de données. La commande `migrate:fresh --seed` combine deux actions :

> 1. **`migrate:fresh`** : Supprime toutes les tables + recrée toutes les tables (équivaut à DROP DATABASE + CREATE DATABASE + migrations)
2. **`--seed`** : Exécute automatiquement `DatabaseSeeder::run()` après les migrations

!!! quote "Cette combinaison garantit un **état initial propre et reproductible** : chaque fois que vous exécutez cette commande, vous obtenez exactement les mêmes données de test."

!!! danger "Perte de Données - **`migrate:fresh` détruit TOUTES les données existantes**. Ne jamais utiliser en production ! Alternative pour ajouter des seeders sans supprimer : `php artisan db:seed` (mais risque d'erreurs de doublons si seeders non idempotents)."

**Exécuter les migrations + seeders :**

```bash
# Réinitialiser la base de données complète et peupler avec données de test
php artisan migrate:fresh --seed

# Alternative en 2 étapes (équivalent) :
# php artisan migrate:fresh
# php artisan db:seed
```

**Sortie console attendue :**

```bash
Dropping all tables .......................................... 54ms DONE

  INFO  Preparing database.

  Creating migration table ..................................... 15ms DONE

  INFO  Running migrations.

  2014_10_12_000000_create_users_table ......................... 42ms DONE
  2014_10_12_100000_create_password_reset_tokens_table ......... 28ms DONE
  2019_08_19_000000_create_failed_jobs_table ................... 31ms DONE
  2019_12_14_000001_create_personal_access_tokens_table ........ 38ms DONE
  0001_01_01_000001_create_cache_table ......................... 25ms DONE
  0001_01_01_000002_create_jobs_table .......................... 33ms DONE
  2024_xx_xx_xxxxxx_create_categories_table .................... 18ms DONE
  2024_xx_xx_xxxxxx_create_posts_table ......................... 45ms DONE
  2024_xx_xx_xxxxxx_create_comments_table ...................... 27ms DONE

  INFO  Seeding database.

  Database\Seeders\CategorySeeder .............................. 12ms DONE
  Database\Seeders\DatabaseSeeder .............................. 87ms DONE

✅ Seeders exécutés avec succès !
📊 Données créées :
   - 6 catégories
   - 3 utilisateurs (alice@example.com, bob@example.com, claire@example.com)
   - 7 posts (6 publiés + 1 brouillon)
   - 2 commentaires (1 approuvé + 1 en attente)
🔐 Mot de passe pour tous les users : password
```

<small>*Chaque ligne indique le temps d'exécution en millisecondes. Les migrations prennent généralement 15-50ms chacune, les seeders 10-100ms selon la quantité de données. Si un seeder prend >2 secondes, c'est qu'il insère beaucoup de données ou fait des requêtes inefficaces (N+1 queries).*</small>

### Vérification des Données dans MySQL

**Méthode 1 : Ligne de commande MySQL**

```bash
# Se connecter à la base de données
mysql -u root -p blog_breeze

# Ou sans mot de passe si root n'en a pas (XAMPP/Laragon par défaut)
mysql -u root blog_breeze
```

**Vérifications à effectuer :**

=== ":fontawesome-solid-users: Utilisateurs"

    ```sql
    -- Lister tous les utilisateurs
    SELECT id, name, email, bio FROM users;
    
    -- Résultat attendu :
    +----+----------------+---------------------+------------------------------------------+
    | id | name           | email               | bio                                      |
    +----+----------------+---------------------+------------------------------------------+
    |  1 | Alice Dupont   | alice@example.com   | Passionnée de technologie et de déve...  |
    |  2 | Bob Martin     | bob@example.com     | Voyageur et photographe amateur.         |
    |  3 | Claire Bernard | claire@example.com  | Chef cuisinière et blogueuse culinaire.  |
    +----+----------------+---------------------+------------------------------------------+
    3 rows in set (0.00 sec)
    ```
    
    **Vérifications :**

    - ✅ 3 utilisateurs créés
    - ✅ Emails uniques
    - ✅ Colonnes `bio` remplies
    - ✅ `email_verified_at` non NULL (vérifiés)

=== ":fontawesome-solid-folder: Catégories"

    ```sql
    -- Lister toutes les catégories
    SELECT id, name, slug FROM categories;
    
    -- Résultat attendu :
    +----+-------------+-------------+
    | id | name        | slug        |
    +----+-------------+-------------+
    |  1 | Technologie | technologie |
    |  2 | Voyage      | voyage      |
    |  3 | Cuisine     | cuisine     |
    |  4 | Sport       | sport       |
    |  5 | Lifestyle   | lifestyle   |
    |  6 | Business    | business    |
    +----+-------------+-------------+
    6 rows in set (0.00 sec)
    ```
    
    **Vérifications :**

    - ✅ 6 catégories créées
    - ✅ Slugs uniques et URL-friendly
    - ✅ Tous les noms/slugs correspondent

=== ":fontawesome-solid-newspaper: Articles"

    ```sql
    -- Lister les articles avec auteur et catégorie
    SELECT 
        p.id, 
        p.title, 
        u.name AS author, 
        c.name AS category, 
        p.status, 
        p.views_count 
    FROM posts p
    JOIN users u ON p.user_id = u.id
    JOIN categories c ON p.category_id = c.id;
    
    -- Résultat attendu :
    +----+--------------------------------------+----------------+-------------+-----------+-------------+
    | id | title                                | author         | category    | status    | views_count |
    +----+--------------------------------------+----------------+-------------+-----------+-------------+
    |  1 | Introduction à Laravel 11            | Alice Dupont   | Technologie | published |         150 |
    |  2 | Les Bases de Vue.js                  | Alice Dupont   | Technologie | published |          87 |
    |  3 | Brouillon : API REST avec Sanctum    | Alice Dupont   | Technologie | draft     |           0 |
    |  4 | Découvrir le Japon en 2 Semaines     | Bob Martin     | Voyage      | published |         230 |
    |  5 | Les Plus Belles Plages de Thaïlande  | Bob Martin     | Voyage      | published |         112 |
    |  6 | Recette : Tarte aux Pommes Maison    | Claire Bernard | Cuisine     | published |         342 |
    |  7 | Lancer son Blog Culinaire en 2024    | Claire Bernard | Business    | published |          54 |
    +----+--------------------------------------+----------------+-------------+-----------+-------------+
    7 rows in set (0.00 sec)
    ```
    
    **Vérifications :**

    - ✅ 7 articles créés (6 publiés + 1 brouillon)
    - ✅ Relations user_id/category_id correctes
    - ✅ Compteurs views_count variés (54-342)
    - ✅ Slugs générés automatiquement

=== ":fontawesome-solid-comments: Commentaires"

    ```sql
    -- Lister les commentaires avec article associé
    SELECT 
        c.id, 
        p.title AS article, 
        c.author_name, 
        c.content, 
        c.approved 
    FROM comments c
    JOIN posts p ON c.post_id = p.id;
    
    -- Résultat attendu :
    +----+---------------------------+----------------+------------------------------------------+----------+
    | id | article                   | author_name    | content                                  | approved |
    +----+---------------------------+----------------+------------------------------------------+----------+
    |  1 | Introduction à Laravel 11 | Jean Durand    | Excellent article ! Très clair et bie... |        1 |
    |  2 | Introduction à Laravel 11 | Marie Lefebvre | Merci pour ce tuto, ça m'a beaucoup a... |        0 |
    +----+---------------------------+----------------+------------------------------------------+----------+
    2 rows in set (0.00 sec)
    ```
    
    **Vérifications :**

    - ✅ 2 commentaires créés
    - ✅ 1 approuvé (approved=1), 1 en attente (approved=0)
    - ✅ post_id correct (tous deux sur article #1)

**Quitter MySQL :**

```sql
EXIT;
```

**Méthode 2 : Interface Graphique (phpMyAdmin / Adminer)**

1. Ouvrir phpMyAdmin : `http://localhost/phpmyadmin`
2. Sélectionner la base `blog_breeze` dans la sidebar
3. Cliquer sur chaque table (`users`, `categories`, `posts`, `comments`)
4. Onglet **"Afficher"** : vérifier les données insérées

!!! info "**Avantages de l'interface graphique :**"

    - Visualisation tabulaire plus lisible que la console
    - Édition manuelle possible (pour tester des modifications)
    - Exportation SQL simplifiée (sauvegarde des données de test)

### Vérification via Tinker (REPL Laravel)

**Contexte :**

Laravel Tinker est un **REPL** (Read-Eval-Print Loop) interactif qui permet d'exécuter du code PHP/Eloquent directement dans le terminal. C'est l'équivalent de la console JavaScript dans le navigateur, mais pour Laravel.

**Lancer Tinker :**

```bash
# Ouvrir le REPL Tinker
php artisan tinker

# Résultat attendu :
# Psy Shell v0.12.0 (PHP 8.x.x)
# >>>
```

**Tests à effectuer :**

```php
// Compter les utilisateurs
>>> User::count()
=> 3

// Récupérer Alice avec ses posts
>>> $alice = User::where('email', 'alice@example.com')->first()
>>> $alice->name
=> "Alice Dupont"

>>> $alice->posts->count()
=> 3

// Lister les titres des posts d'Alice
>>> $alice->posts->pluck('title')
=> Illuminate\Support\Collection {
     all: [
       "Introduction à Laravel 11",
       "Les Bases de Vue.js",
       "Brouillon : API REST avec Sanctum",
     ],
   }

// Compter les posts publiés
>>> Post::published()->count()
=> 6

// Afficher le post le plus vu
>>> Post::orderBy('views_count', 'desc')->first()->title
=> "Recette : Tarte aux Pommes Maison"

// Lister les catégories avec nombre de posts
>>> Category::withCount('posts')->get(['name', 'posts_count'])
=> Illuminate\Database\Eloquent\Collection {
     all: [
       App\Models\Category {
         name: "Technologie",
         posts_count: 3,
       },
       App\Models\Category {
         name: "Voyage",
         posts_count: 2,
       },
       App\Models\Category {
         name: "Cuisine",
         posts_count: 1,
       },
       App\Models\Category {
         name: "Sport",
         posts_count: 0,
       },
       App\Models\Category {
         name: "Lifestyle",
         posts_count: 0,
       },
       App\Models\Category {
         name: "Business",
         posts_count: 1,
       },
     ],
   }

// Quitter Tinker
>>> exit
```

<small>*Tinker est **extrêmement utile** pour déboguer les relations Eloquent, tester des requêtes complexes, ou explorer la structure des modèles. Si une requête ne retourne pas les données attendues, Tinker permet d'isoler le problème rapidement.*</small>

!!! tip "Raccourcis Tinker Utiles"
    - `ls` : Lister les méthodes disponibles sur un objet
    - `doc User` : Afficher la documentation de la classe User
    - Flèche haut/bas : Historique des commandes
    - `Ctrl+C` : Annuler la commande en cours
    - `Ctrl+D` : Quitter Tinker

### Récapitulatif Phase 3 : Ce que vous avez construit

✅ **Seeders Créés** :

- `CategorySeeder` : 6 catégories de référence (Technologie, Voyage, Cuisine, Sport, Lifestyle, Business)
- `DatabaseSeeder` : orchestration complète (3 users, 7 posts, 2 comments)

✅ **Données de Test Réalistes** :

- **3 utilisateurs** avec profils distincts (bio, email vérifié, password identique pour simplicité)
- **6 catégories** couvrant les grandes thématiques d'un blog
- **7 articles** : 6 publiés (vues variées 54-342) + 1 brouillon (invisible)
- **2 commentaires** : 1 approuvé (visible) + 1 en attente (modération)

✅ **Testabilité Complète** :

- Dashboard auteur : chaque user a ses propres articles
- Filtres catégories : articles répartis sur 4 catégories différentes
- Système de statuts : brouillon vs publié testable immédiatement
- Modération : commentaires approved/pending visibles dans l'interface
- Compteurs de vues : données réalistes pour tester statistiques

✅ **Compétences Laravel Maîtrisées** :

- Création de seeders (`make:seeder`)
- Appel de seeders via `$this->call()`
- Mass-assignment Eloquent (`create()`)
- Relations Eloquent dans les seeders (récupération via `where()`, `first()`)
- Manipulation de dates avec Carbon (`now()->subDays()`)
- Hachage de mots de passe (`bcrypt()`)
- Commande combinée `migrate:fresh --seed`
- Vérification des données (MySQL, Tinker)

!!! success "Phase 3 Terminée"
    Votre base de données est maintenant **peuplée avec des données cohérentes et réalistes**. Vous pouvez :
    
    1. **Tester l'authentification** : Connexion avec `alice@example.com` / `password`
    2. **Parcourir le blog** : Voir les 6 articles publiés sur la page d'accueil
    3. **Filtrer par catégorie** : Accéder aux articles Technologie/Voyage/Cuisine
    4. **Tester le dashboard** : Alice voit ses 3 articles (2 publiés + 1 brouillon)
    5. **Modérer des commentaires** : Approuver le commentaire en attente
    
    Vous êtes prêt pour la **Phase 4 : Contrôleurs** où vous implémenterez toute la logique métier du blog (CRUD articles, modération, dashboard, etc.).























## PHASE 4 : Contrôleurs et Logique Métier (~45-60 minutes)

### Vue d'Ensemble de la Phase

> Cette quatrième phase constitue le **cœur de la logique applicative** de votre blog. Les contrôleurs sont les **chefs d'orchestre** de l'architecture MVC : ils reçoivent les requêtes HTTP, interrogent les modèles Eloquent pour récupérer/modifier les données, appliquent la logique métier (validation, autorisation, transformations), puis retournent les vues Blade enrichies des données.

!!! note "Dans Laravel, un contrôleur est une **classe PHP** contenant des méthodes publiques appelées **actions**. Chaque action correspond généralement à une route HTTP : `index()` pour lister, `show()` pour afficher un élément, `create()` pour le formulaire de création, `store()` pour enregistrer, `edit()` pour le formulaire d'édition, `update()` pour modifier, `destroy()` pour supprimer. C'est le pattern **CRUD** (Create, Read, Update, Delete)."

!!! quote "Contrairement aux frameworks où la logique métier est dispersée dans les vues (mauvaise pratique), Laravel impose une **séparation stricte** : **les contrôleurs gèrent la logique**, **les vues gèrent l'affichage**. Cette séparation garantit un code maintenable, testable et évolutif."

**Contrôleurs que nous allons créer :**

1. **HomeController** : Page d'accueil avec liste des articles publiés + sidebar
2. **PostController** : CRUD complet des articles (7 méthodes : index, show, create, store, edit, update, destroy)
3. **DashboardController** : Dashboard auteur avec statistiques et liste de ses articles
4. **CommentController** : Gestion des commentaires (création publique + modération auteur)
5. **CategoryController** : Affichage des articles par catégorie
6. **AuthorController** : Page profil public d'un auteur
7. **ProfileController** : Gestion du profil utilisateur (édition infos, changement password, suppression compte)

!!! quote "À l'issue de cette phase, votre application disposera de **toute la logique fonctionnelle** : un visiteur pourra consulter les articles et commenter, un auteur connecté pourra gérer ses articles et modérer les commentaires, et chaque utilisateur pourra personnaliser son profil."

!!! warning "Prérequis Phase 4 - Les Phases 1, 2 et 3 doivent être terminées : **projet Laravel créé**, **Breeze installé**, **migrations exécutées**, **modèles configurés**, **seeders exécutés**. Votre base de données doit contenir les données de test (**3 users**, **6 catégories**, **7 posts**, **2 comments**)."

### Étape 4.1 : Créer le HomeController

**Contexte de l'étape :**

> Le `HomeController` gère la **page d'accueil publique** du blog. C'est la première page que voit un visiteur lorsqu'il accède à `http://localhost:8000`. Cette page doit afficher :

> - **Une liste paginée** des articles publiés (9 par page)
- **Un sidebar** avec les catégories et leurs compteurs d'articles
- **Les 3 articles les plus populaires** (par nombre de vues)

!!! quote "Le contrôleur doit optimiser les requêtes SQL via **Eager Loading** (`with()`) pour éviter le problème N+1 : charger les relations `user` et `category` en une seule requête au lieu de N requêtes supplémentaires."

**Générer le contrôleur :**

```bash
# Créer le contrôleur HomeController
php artisan make:controller HomeController

# Résultat attendu :
# Controller created successfully.
# Created Controller: app/Http/Controllers/HomeController.php
```

**Éditer le fichier généré :**

Ouvrir `app/Http/Controllers/HomeController.php` et **remplacer tout le contenu** par :

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Category;
use Illuminate\Http\Request;

class HomeController extends Controller
{
    /**
     * Afficher la page d'accueil du blog
     * 
     * Route : GET /
     * Vue : resources/views/home.blade.php
     * 
     * Cette méthode récupère :
     * 1. Les articles publiés paginés (9 par page)
     * 2. Les catégories avec leur nombre d'articles (sidebar)
     * 3. Les 3 articles les plus vus (sidebar "Populaires")
     * 
     * @return \Illuminate\View\View
     */
    public function index()
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES PUBLIÉS
        |----------------------------------------------------------------------
        | On applique plusieurs optimisations :
        |
        | 1. with(['user', 'category']) = EAGER LOADING
        |    Charge les relations en UNE requête SQL au lieu de N+1 requêtes
        |    Exemple sans with() :
        |      SELECT * FROM posts            (1 requête)
        |      SELECT * FROM users WHERE id=1 (N requêtes, une par post)
        |      SELECT * FROM categories WHERE id=1 (N requêtes)
        |    Avec with() :
        |      SELECT * FROM posts
        |      SELECT * FROM users WHERE id IN (1,2,3)      (1 requête)
        |      SELECT * FROM categories WHERE id IN (1,2,3) (1 requête)
        |
        | 2. published() = SCOPE défini dans Post::scopePublished()
        |    Filtre automatiquement : status='published' 
        |                              AND published_at IS NOT NULL 
        |                              AND published_at <= NOW()
        |
        | 3. latest('published_at') = ORDER BY published_at DESC
        |    Trie par date de publication décroissante (plus récents d'abord)
        |
        | 4. paginate(9) = PAGINATION
        |    Divise les résultats en pages de 9 articles
        |    Génère automatiquement les liens "Précédent/Suivant"
        |    Ajoute ?page=2 dans l'URL
        */
        $posts = Post::with(['user', 'category'])  // Eager load pour performance
                     ->published()                  // Seulement les articles publiés
                     ->latest('published_at')       // Plus récents en premier
                     ->paginate(9);                 // 9 articles par page
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES CATÉGORIES (Sidebar)
        |----------------------------------------------------------------------
        | withCount('posts') ajoute un attribut virtuel 'posts_count' à chaque
        | catégorie contenant le nombre d'articles associés.
        |
        | SQL généré :
        | SELECT categories.*, 
        |        (SELECT COUNT(*) FROM posts 
        |         WHERE posts.category_id = categories.id) AS posts_count
        | FROM categories
        |
        | Permet d'afficher dans la sidebar :
        | Technologie (3)
        | Voyage (2)
        | Cuisine (1)
        */
        $categories = Category::withCount('posts')->get();
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES POPULAIRES (Sidebar)
        |----------------------------------------------------------------------
        | On récupère les 3 articles les plus vus parmi les articles publiés.
        |
        | orderBy('views_count', 'desc') = Tri décroissant par nombre de vues
        | limit(3) = Limite à 3 résultats (pas de pagination ici)
        | get() = Exécute la requête et retourne une Collection
        |
        | Note : On pourrait aussi ajouter ->with('user') si on affiche l'auteur
        | dans la liste des populaires.
        */
        $popularPosts = Post::published()                // Seulement publiés
                            ->orderBy('views_count', 'desc') // Plus vus d'abord
                            ->limit(3)                       // Top 3
                            ->get();
        
        /*
        |----------------------------------------------------------------------
        | RETOUR DE LA VUE
        |----------------------------------------------------------------------
        | compact() est un helper PHP qui crée un tableau associatif :
        | compact('posts', 'categories', 'popularPosts')
        | équivaut à :
        | ['posts' => $posts, 'categories' => $categories, 'popularPosts' => $popularPosts]
        |
        | Ces variables seront accessibles dans la vue Blade :
        | @foreach($posts as $post)
        */
        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
}
```

<small>*L'Eager Loading via `with()` est **crucial pour les performances** : sans lui, afficher 9 articles avec leur auteur et catégorie générerait 1 + 9 + 9 = 19 requêtes SQL. Avec `with()`, seulement 3 requêtes (1 pour les posts, 1 pour les users, 1 pour les categories). Sur une base de 10 000 articles, la différence est dramatique (500ms vs 50ms). Le scope `published()` centralise la logique de filtrage : si demain vous ajoutez une condition (ex: `is_featured`), vous la modifiez une seule fois dans `Post::scopePublished()` et tout le code en bénéficie.*</small>

### Étape 4.2 : Créer le PostController (CRUD Complet)

**Contexte de l'étape :**

> Le `PostController` est le **contrôleur le plus important** du blog. Il gère toutes les opérations CRUD sur les articles :

> - **show()** : Afficher un article individuel (public)
- **create()** : Formulaire de création (auth requis)
- **store()** : Enregistrer un nouvel article (auth requis)
- **edit()** : Formulaire d'édition (auth + ownership requis)
- **update()** : Mettre à jour un article (auth + ownership requis)
- **destroy()** : Supprimer un article (auth + ownership requis)

!!! quote "Les méthodes protégées (**create**, **store**, **edit**, **update**, **destroy**) nécessitent une **authentification** (middleware `auth`) et une **vérification d'ownership** : un utilisateur ne peut **modifier**/**supprimer que ses propres articles**."

**Générer le contrôleur :**

```bash
# Créer le contrôleur PostController
php artisan make:controller PostController

# Résultat attendu :
# Controller created successfully.
```

**Éditer le fichier généré :**

Ouvrir `app/Http/Controllers/PostController.php` et **remplacer tout le contenu** par :

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Category;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /*
    |--------------------------------------------------------------------------
    | AFFICHAGE PUBLIC D'UN ARTICLE
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher un article individuel (page publique)
     * 
     * Route : GET /posts/{post:slug}
     * Vue : resources/views/posts/show.blade.php
     * 
     * Cette méthode :
     * 1. Récupère l'article via son slug (binding automatique Laravel)
     * 2. Vérifie l'autorisation d'accès si l'article est un brouillon
     * 3. Incrémente le compteur de vues
     * 4. Charge les relations et commentaires approuvés
     * 5. Récupère 3 articles similaires (même catégorie)
     * 
     * @param Post $post Instance du post (injectée automatiquement par Laravel)
     * @return \Illuminate\View\View
     */
    public function show(Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | CONTRÔLE D'ACCÈS AUX BROUILLONS
        |----------------------------------------------------------------------
        | Les brouillons ne sont visibles QUE par leur auteur.
        | Si un visiteur ou un autre utilisateur tente d'y accéder → 404
        |
        | Logique :
        | - Si status = draft ET (pas connecté OU pas l'auteur) → abort(404)
        | - Sinon → affichage normal
        */
        if ($post->status === 'draft') {
            // auth()->check() retourne true si utilisateur connecté
            // auth()->id() retourne l'ID de l'utilisateur connecté (null si non connecté)
            
            if (!auth()->check() || auth()->id() !== $post->user_id) {
                // abort(404) génère une erreur 404 Not Found
                // Le visiteur verra la page d'erreur Laravel standard
                abort(404);
            }
        }
        
        /*
        |----------------------------------------------------------------------
        | INCRÉMENTATION DU COMPTEUR DE VUES
        |----------------------------------------------------------------------
        | On incrémente seulement pour les articles publiés.
        | Pour les brouillons, on ne compte pas les vues de l'auteur.
        |
        | incrementViews() est définie dans le modèle Post :
        | $this->increment('views_count')
        | SQL généré : UPDATE posts SET views_count = views_count + 1 WHERE id = ?
        |
        | Avantage : évite les race conditions (deux visiteurs simultanés)
        | Alternative non-safe : $post->views_count++; $post->save();
        */
        if ($post->status === 'published') {
            $post->incrementViews();
        }
        
        /*
        |----------------------------------------------------------------------
        | EAGER LOADING DES RELATIONS
        |----------------------------------------------------------------------
        | load() charge les relations APRÈS avoir récupéré le post.
        | Différence avec with() :
        | - with() : chargement AVANT la requête principale (dans la requête SQL)
        | - load() : chargement APRÈS (requête SQL séparée)
        |
        | Ici on utilise load() car le post est déjà récupéré via route binding.
        |
        | comments => function($query) : Closure pour filtrer les commentaires
        | - approved() : scope défini dans Comment::scopeApproved()
        | - latest() : ORDER BY created_at DESC (plus récents d'abord)
        */
        $post->load([
            'user',      // Auteur de l'article
            'category',  // Catégorie de l'article
            'comments' => function ($query) {
                // Seulement les commentaires approuvés, triés du plus récent au plus ancien
                $query->approved()->latest();
            }
        ]);
        
        /*
        |----------------------------------------------------------------------
        | ARTICLES SIMILAIRES (Même Catégorie)
        |----------------------------------------------------------------------
        | On récupère 3 autres articles publiés de la même catégorie.
        | Utilisé dans la vue pour afficher "Vous pourriez aussi aimer".
        |
        | where('id', '!=', $post->id) : Exclure l'article actuel
        | limit(3) : Maximum 3 résultats
        | inRandomOrder() : Optionnel, pour varier l'ordre à chaque visite
        */
        $relatedPosts = Post::published()
                            ->where('category_id', $post->category_id)  // Même catégorie
                            ->where('id', '!=', $post->id)              // Pas l'article actuel
                            ->limit(3)
                            ->get();
        
        // Retourner la vue avec les données
        return view('posts.show', compact('post', 'relatedPosts'));
    }
    
    /*
    |--------------------------------------------------------------------------
    | CRÉATION D'UN ARTICLE (Authentification Requise)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher le formulaire de création d'article
     * 
     * Route : GET /posts/create
     * Middleware : auth (utilisateur doit être connecté)
     * Vue : resources/views/posts/create.blade.php
     * 
     * @return \Illuminate\View\View
     */
    public function create()
    {
        // Récupérer toutes les catégories pour le select du formulaire
        $categories = Category::all();
        
        return view('posts.create', compact('categories'));
    }
    
    /**
     * Enregistrer un nouvel article en base de données
     * 
     * Route : POST /posts
     * Middleware : auth
     * 
     * Cette méthode :
     * 1. Valide les données du formulaire
     * 2. Crée l'article pour l'utilisateur connecté
     * 3. Redirige vers l'article créé avec message de succès
     * 
     * @param Request $request Objet contenant les données POST
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES DU FORMULAIRE
        |----------------------------------------------------------------------
        | validate() vérifie que les données respectent les règles.
        | Si validation échoue :
        | - Retour automatique au formulaire avec les erreurs
        | - Les anciennes valeurs sont conservées (old())
        | - Les messages d'erreur sont disponibles dans @error()
        |
        | Règles de validation :
        | - required : champ obligatoire
        | - max:255 : maximum 255 caractères
        | - exists:categories,id : l'ID doit exister dans la table categories
        | - nullable : champ optionnel
        | - url : doit être une URL valide (http:// ou https://)
        | - in:draft,published : doit être exactement 'draft' ou 'published'
        */
        $validated = $request->validate([
            'title' => 'required|max:255',
            'category_id' => 'required|exists:categories,id',
            'excerpt' => 'required|max:500',
            'content' => 'required|min:100',
            'image' => 'nullable|url',
            'status' => 'required|in:draft,published',
        ], [
            // Messages d'erreur personnalisés (optionnel)
            'title.required' => 'Le titre est obligatoire.',
            'category_id.required' => 'Veuillez sélectionner une catégorie.',
            'category_id.exists' => 'Cette catégorie n\'existe pas.',
            'excerpt.required' => 'Le résumé est obligatoire.',
            'excerpt.max' => 'Le résumé ne doit pas dépasser 500 caractères.',
            'content.required' => 'Le contenu est obligatoire.',
            'content.min' => 'Le contenu doit contenir au moins 100 caractères.',
            'image.url' => 'L\'image doit être une URL valide.',
            'status.in' => 'Le statut doit être "draft" ou "published".',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | CRÉATION DE L'ARTICLE
        |----------------------------------------------------------------------
        | auth()->user()->posts() accède à la relation hasMany définie dans User
        | create($validated) crée un nouvel article avec les données validées
        |
        | Équivaut à :
        | $post = new Post($validated);
        | $post->user_id = auth()->id();
        | $post->save();
        |
        | Avantage : plus concis, remplit automatiquement user_id
        |
        | Note : Le slug sera généré automatiquement par l'événement creating()
        | défini dans Post::boot()
        */
        $post = auth()->user()->posts()->create($validated);
        
        /*
        |----------------------------------------------------------------------
        | MESSAGE DE SUCCÈS SELON LE STATUT
        |----------------------------------------------------------------------
        | On personnalise le message selon que l'article est publié ou brouillon.
        | Ce message sera affiché via session()->get('success') dans la vue.
        */
        $message = $post->status === 'published' 
            ? 'Article publié avec succès !' 
            : 'Brouillon sauvegardé avec succès !';
        
        /*
        |----------------------------------------------------------------------
        | REDIRECTION AVEC MESSAGE FLASH
        |----------------------------------------------------------------------
        | redirect()->route('posts.show', $post) :
        | - Redirige vers la route nommée 'posts.show'
        | - Passe $post comme paramètre (Laravel génère /posts/{slug})
        |
        | with('success', $message) :
        | - Stocke le message dans la session (flash = disponible qu'une seule fois)
        | - Accessible dans la vue via session('success') ou @session('success')
        */
        return redirect()
            ->route('posts.show', $post)
            ->with('success', $message);
    }
    
    /*
    |--------------------------------------------------------------------------
    | ÉDITION D'UN ARTICLE (Ownership Requis)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Afficher le formulaire d'édition d'un article
     * 
     * Route : GET /posts/{post}/edit
     * Middleware : auth
     * Vue : resources/views/posts/edit.blade.php
     * 
     * Cette méthode vérifie que l'utilisateur connecté est bien l'auteur
     * de l'article avant d'afficher le formulaire.
     * 
     * @param Post $post
     * @return \Illuminate\View\View
     */
    public function edit(Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | VÉRIFICATION DE L'OWNERSHIP
        |----------------------------------------------------------------------
        | Un utilisateur ne peut modifier QUE ses propres articles.
        | Si un autre utilisateur tente d'accéder → erreur 403 Forbidden
        |
        | abort(403, $message) génère une exception HTTP 403
        | Le visiteur verra "403 Forbidden - Action non autorisée."
        */
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        // Récupérer toutes les catégories pour le select
        $categories = Category::all();
        
        return view('posts.edit', compact('post', 'categories'));
    }
    
    /**
     * Mettre à jour un article existant
     * 
     * Route : PUT /posts/{post}
     * Middleware : auth
     * 
     * @param Request $request
     * @param Post $post
     * @return \Illuminate\Http\RedirectResponse
     */
    public function update(Request $request, Post $post)
    {
        // Vérifier l'ownership (même logique que edit())
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        // Validation (mêmes règles que store())
        $validated = $request->validate([
            'title' => 'required|max:255',
            'category_id' => 'required|exists:categories,id',
            'excerpt' => 'required|max:500',
            'content' => 'required|min:100',
            'image' => 'nullable|url',
            'status' => 'required|in:draft,published',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | MISE À JOUR DE L'ARTICLE
        |----------------------------------------------------------------------
        | update($validated) met à jour toutes les colonnes du tableau $validated
        |
        | SQL généré :
        | UPDATE posts 
        | SET title = ?, category_id = ?, excerpt = ?, content = ?, 
        |     image = ?, status = ?, updated_at = NOW()
        | WHERE id = ?
        |
        | Note : Le slug n'est PAS regénéré lors de l'update (événement updating())
        | car changer l'URL casserait les liens existants (mauvais pour SEO).
        |
        | Si vous voulez regénérer le slug, ajoutez :
        | $post->slug = Str::slug($validated['title']);
        */
        $post->update($validated);
        
        // Message personnalisé selon le nouveau statut
        $message = $post->status === 'published' 
            ? 'Article mis à jour et publié !' 
            : 'Brouillon mis à jour !';
        
        return redirect()
            ->route('posts.show', $post)
            ->with('success', $message);
    }
    
    /*
    |--------------------------------------------------------------------------
    | SUPPRESSION D'UN ARTICLE (Ownership Requis)
    |--------------------------------------------------------------------------
    */
    
    /**
     * Supprimer un article
     * 
     * Route : DELETE /posts/{post}
     * Middleware : auth
     * 
     * Supprime l'article de la base de données.
     * Grâce à onDelete('cascade') dans les migrations, les commentaires
     * associés sont automatiquement supprimés.
     * 
     * @param Post $post
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Post $post)
    {
        // Vérifier l'ownership
        if (auth()->id() !== $post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | SUPPRESSION DE L'ARTICLE
        |----------------------------------------------------------------------
        | delete() supprime l'enregistrement de la base de données.
        |
        | SQL généré :
        | DELETE FROM posts WHERE id = ?
        |
        | Grâce à la contrainte CASCADE définie dans create_comments_table :
        | ->onDelete('cascade')
        | Tous les commentaires associés sont automatiquement supprimés.
        |
        | Alternative : Soft Delete (suppression logique)
        | Au lieu de supprimer physiquement, on marque comme supprimé :
        | use SoftDeletes; dans le modèle
        | Migration : $table->softDeletes();
        | Permet de restaurer les articles supprimés.
        */
        $post->delete();
        
        // Redirection vers le dashboard avec message
        return redirect()
            ->route('dashboard')
            ->with('success', 'Article supprimé avec succès !');
    }
}
```

<small>*La vérification d'ownership manuelle (`auth()->id() !== $post->user_id`) est basique mais efficace. Pour un projet plus complexe, utilisez les **Policies** Laravel : `php artisan make:policy PostPolicy --model=Post`, puis définissez des méthodes `update(User $user, Post $post)` et vérifiez via `$this->authorize('update', $post)` dans le contrôleur. Les Policies centralisent les règles d'autorisation et sont testables unitairement.*</small>

### Étape 4.3 : Créer le DashboardController

**Contexte de l'étape :**

> Le `DashboardController` gère le **tableau de bord personnel** de l'auteur connecté. Cette page affiche :

> - **Statistiques globales** : nombre total d'articles, publiés, brouillons, vues, commentaires
- **L'article le plus populaire** de l'auteur
- **La liste complète** de ses articles (publiés + brouillons)

!!! quote "Ce dashboard est accessible uniquement aux **utilisateurs authentifiés** (middleware `auth` défini dans les routes)."

**Générer le contrôleur :**

```bash
php artisan make:controller DashboardController
```

**Éditer le fichier généré :**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * Afficher le dashboard auteur (page privée)
     * 
     * Route : GET /dashboard
     * Middleware : auth (utilisateur doit être connecté)
     * Vue : resources/views/dashboard.blade.php
     * 
     * Cette méthode calcule toutes les statistiques de l'auteur connecté :
     * - Nombre d'articles (total, publiés, brouillons)
     * - Nombre total de vues
     * - Nombre total de commentaires
     * - Article le plus vu
     * 
     * @return \Illuminate\View\View
     */
    public function index()
    {
        // Récupérer l'utilisateur connecté
        // auth()->user() retourne l'instance du User authentifié
        $user = auth()->user();
        
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DE TOUS LES ARTICLES DE L'AUTEUR
        |----------------------------------------------------------------------
        | On récupère TOUS les articles de l'utilisateur (publiés + brouillons)
        | avec leur catégorie (Eager Loading), triés du plus récent au plus ancien.
        |
        | where('user_id', $user->id) filtre par auteur
        | with('category') charge la catégorie en une seule requête
        | latest() = ORDER BY created_at DESC
        | get() exécute la requête et retourne une Collection
        |
        | Alternative avec relation :
        | $posts = $user->posts()->with('category')->latest()->get();
        */
        $posts = Post::where('user_id', $user->id)
                     ->with('category')
                     ->latest()
                     ->get();
        
        /*
        |----------------------------------------------------------------------
        | CALCUL DES STATISTIQUES
        |----------------------------------------------------------------------
        | On utilise les méthodes de Collection pour calculer les stats.
        |
        | $posts->count() : Nombre total d'articles
        | $posts->where('status', 'published')->count() : Filtrer puis compter
        | $posts->sum('views_count') : Somme de la colonne views_count
        |
        | Pour les commentaires, on fait une requête séparée avec withCount() :
        | withCount('comments') ajoute un attribut virtuel 'comments_count'
        | Ensuite on somme tous les comments_count
        */
        $stats = [
            'total_posts' => $posts->count(),
            
            'published_posts' => $posts->where('status', 'published')->count(),
            
            'draft_posts' => $posts->where('status', 'draft')->count(),
            
            // Somme de toutes les vues de tous les articles
            'total_views' => $posts->sum('views_count'),
            
            // Nombre total de commentaires sur tous les articles
            // On récupère les posts avec leur nombre de commentaires
            'total_comments' => $user->posts()
                                     ->withCount('comments')
                                     ->get()
                                     ->sum('comments_count'),
        ];
        
        /*
        |----------------------------------------------------------------------
        | ARTICLE LE PLUS POPULAIRE (Plus de Vues)
        |----------------------------------------------------------------------
        | On filtre les articles publiés, on les trie par views_count décroissant,
        | et on prend le premier (ou null si aucun article publié).
        |
        | sortByDesc('views_count') trie la Collection en mémoire
        | first() retourne le premier élément ou null
        |
        | Alternative avec requête SQL directe :
        | $mostViewedPost = Post::where('user_id', $user->id)
        |                       ->published()
        |                       ->orderBy('views_count', 'desc')
        |                       ->first();
        */
        $mostViewedPost = $posts->where('status', 'published')
                                ->sortByDesc('views_count')
                                ->first();
        
        /*
        |----------------------------------------------------------------------
        | ARTICLES RÉCENTS (5 Derniers)
        |----------------------------------------------------------------------
        | take(5) limite à 5 éléments
        | La Collection $posts est déjà triée par latest(), donc take(5)
        | retourne les 5 plus récents.
        */
        $recentPosts = $posts->take(5);
        
        // Retourner la vue avec toutes les données
        return view('dashboard', compact('posts', 'stats', 'mostViewedPost', 'recentPosts'));
    }
}
```

<small>*L'utilisation de Collections (`$posts->where()`, `$posts->sum()`) au lieu de requêtes SQL séparées est efficace **si le nombre d'articles par auteur est limité** (<100). Au-delà, préférez des requêtes SQL directes avec `selectRaw()` pour décharger le travail sur MySQL. Exemple : `Post::where('user_id', $user->id)->selectRaw('SUM(views_count) as total_views')->value('total_views')`.*</small>

### Étape 4.4 : Créer le CommentController

**Contexte de l'étape :**

> Le `CommentController` gère deux fonctionnalités distinctes :

> 1. **Création de commentaires** (publique, sans authentification) : les visiteurs peuvent commenter
2. **Modération** (privée, auteur seulement) : approuver ou supprimer les commentaires sur ses articles

**Générer le contrôleur :**

```bash
php artisan make:controller CommentController
```

**Éditer le fichier généré :**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use App\Models\Comment;
use Illuminate\Http\Request;

class CommentController extends Controller
{
    /**
     * Créer un nouveau commentaire sur un article (action publique)
     * 
     * Route : POST /posts/{post}/comments
     * Accès : Public (pas d'authentification requise)
     * 
     * Les visiteurs non inscrits peuvent commenter en fournissant
     * leur nom et email. Le commentaire est créé en statut non approuvé
     * (approved=false) et l'auteur de l'article devra le modérer.
     * 
     * @param Request $request Données du formulaire
     * @param Post $post Article commenté (injecté automatiquement)
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request, Post $post)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES DU FORMULAIRE
        |----------------------------------------------------------------------
        | Règles :
        | - author_name : obligatoire, max 255 caractères
        | - author_email : obligatoire, format email valide
        | - content : obligatoire, min 10 caractères (évite spam), max 1000
        |
        | Note : On ne valide PAS l'unicité de l'email car plusieurs visiteurs
        | peuvent avoir le même nom/email (Jean Dupont, jean@example.com)
        */
        $validated = $request->validate([
            'author_name' => 'required|max:255',
            'author_email' => 'required|email',
            'content' => 'required|min:10|max:1000',
        ], [
            'author_name.required' => 'Veuillez indiquer votre nom.',
            'author_email.required' => 'Veuillez indiquer votre email.',
            'author_email.email' => 'Email invalide.',
            'content.required' => 'Le commentaire ne peut pas être vide.',
            'content.min' => 'Le commentaire doit contenir au moins 10 caractères.',
            'content.max' => 'Le commentaire ne doit pas dépasser 1000 caractères.',
        ]);
        
        /*
        |----------------------------------------------------------------------
        | CRÉATION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | $post->comments() accède à la relation hasMany définie dans Post
        | create() crée un nouvel enregistrement avec post_id rempli automatiquement
        |
        | ...$validated : Spread operator PHP (décompose le tableau)
        | Équivaut à : [...$validated, 'approved' => false]
        |
        | Le commentaire est créé avec approved=false par défaut.
        | L'auteur de l'article devra l'approuver manuellement.
        */
        $post->comments()->create([
            ...$validated,           // Spread : author_name, author_email, content
            'approved' => false,     // Non approuvé par défaut (modération manuelle)
        ]);
        
        /*
        |----------------------------------------------------------------------
        | REDIRECTION AVEC MESSAGE
        |----------------------------------------------------------------------
        | back() redirige vers la page précédente (l'article)
        | Équivaut à : redirect()->route('posts.show', $post)
        |
        | with('success', $message) stocke le message dans la session flash
        */
        return back()->with('success', 'Commentaire ajouté ! Il sera visible après modération par l\'auteur.');
    }
    
    /**
     * Approuver un commentaire (action auteur)
     * 
     * Route : PATCH /comments/{comment}/approve
     * Middleware : auth (utilisateur connecté requis)
     * 
     * Seul l'auteur de l'article peut approuver les commentaires.
     * 
     * @param Comment $comment Commentaire à approuver (injecté automatiquement)
     * @return \Illuminate\Http\RedirectResponse
     */
    public function approve(Comment $comment)
    {
        /*
        |----------------------------------------------------------------------
        | VÉRIFICATION DE L'OWNERSHIP
        |----------------------------------------------------------------------
        | On vérifie que l'utilisateur connecté est bien l'auteur du POST
        | auquel appartient ce commentaire.
        |
        | $comment->post : Accès à la relation belongsTo définie dans Comment
        | $comment->post->user_id : ID de l'auteur de l'article
        |
        | Si ce n'est pas l'auteur → erreur 403
        */
        if (auth()->id() !== $comment->post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | APPROBATION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | update() modifie la colonne approved à true
        |
        | SQL généré :
        | UPDATE comments SET approved = 1, updated_at = NOW() WHERE id = ?
        |
        | Alternative avec méthode helper définie dans Comment :
        | $comment->approve(); (si vous avez défini cette méthode dans le modèle)
        */
        $comment->update(['approved' => true]);
        
        // Rediriger vers la page de l'article avec message
        return back()->with('success', 'Commentaire approuvé !');
    }
    
    /**
     * Supprimer un commentaire (action auteur)
     * 
     * Route : DELETE /comments/{comment}
     * Middleware : auth
     * 
     * Seul l'auteur de l'article peut supprimer les commentaires.
     * 
     * @param Comment $comment
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Comment $comment)
    {
        // Vérifier l'ownership (même logique que approve())
        if (auth()->id() !== $comment->post->user_id) {
            abort(403, 'Action non autorisée.');
        }
        
        /*
        |----------------------------------------------------------------------
        | SUPPRESSION DU COMMENTAIRE
        |----------------------------------------------------------------------
        | delete() supprime l'enregistrement de la base de données
        |
        | SQL généré :
        | DELETE FROM comments WHERE id = ?
        */
        $comment->delete();
        
        return back()->with('success', 'Commentaire supprimé !');
    }
}
```

<small>*Le système de modération implémenté ici est simple mais efficace : tous les commentaires sont créés avec `approved=false`, l'auteur les voit dans son interface avec des boutons "Approuver"/"Supprimer", et seuls les commentaires approuvés apparaissent publiquement (filtrage via scope `approved()`). Pour un blog à fort trafic, ajoutez un système de **notifications** (email à l'auteur quand nouveau commentaire) ou un **scoring anti-spam** (Akismet API).*</small>

### Étape 4.5 : Créer le CategoryController

**Générer et éditer :**

```bash
php artisan make:controller CategoryController
```

```php
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    /**
     * Afficher tous les articles d'une catégorie (page publique)
     * 
     * Route : GET /category/{category:slug}
     * Vue : resources/views/categories/show.blade.php
     * 
     * Cette page liste tous les articles publiés appartenant à la catégorie.
     * 
     * @param Category $category Catégorie (injectée via slug)
     * @return \Illuminate\View\View
     */
    public function show(Category $category)
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES DE LA CATÉGORIE
        |----------------------------------------------------------------------
        | $category->posts() accède à la relation hasMany définie dans Category
        | with('user') charge l'auteur de chaque article (Eager Loading)
        | published() scope pour ne récupérer que les articles publiés
        | latest('published_at') tri par date de publication décroissante
        | paginate(9) pagination avec 9 articles par page
        */
        $posts = $category->posts()
                          ->with('user')
                          ->published()
                          ->latest('published_at')
                          ->paginate(9);
        
        return view('categories.show', compact('category', 'posts'));
    }
}
```

### Étape 4.6 : Créer l'AuthorController

```bash
php artisan make:controller AuthorController
```

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class AuthorController extends Controller
{
    /**
     * Afficher la page profil public d'un auteur
     * 
     * Route : GET /author/{user}
     * Vue : resources/views/authors/show.blade.php
     * 
     * Cette page affiche :
     * - Les informations publiques de l'auteur (nom, bio, avatar)
     * - Ses statistiques (nombre d'articles, vues, commentaires)
     * - La liste paginée de ses articles publiés
     * 
     * @param User $user Auteur (injecté automatiquement par Laravel)
     * @return \Illuminate\View\View
     */
    public function show(User $user)
    {
        /*
        |----------------------------------------------------------------------
        | RÉCUPÉRATION DES ARTICLES PUBLIÉS DE L'AUTEUR
        |----------------------------------------------------------------------
        | $user->posts() accède à la relation hasMany définie dans User
        | with('category') charge la catégorie (pour affichage badge)
        | published() scope pour ne récupérer que les publiés
        | latest('published_at') tri chronologique inversé
        | paginate(6) pagination avec 6 articles par page (moins que page accueil)
        */
        $posts = $user->posts()
                      ->with('category')
                      ->published()
                      ->latest('published_at')
                      ->paginate(6);
        
        /*
        |----------------------------------------------------------------------
        | CALCUL DES STATISTIQUES PUBLIQUES
        |----------------------------------------------------------------------
        | Ces stats sont visibles publiquement sur le profil auteur.
        | On ne montre QUE les articles publiés (pas les brouillons).
        |
        | sum('views_count') : Somme des vues de tous les articles publiés
        | withCount('comments') : Ajoute comments_count à chaque article
        | get()->sum('comments_count') : Somme tous les comments_count
        */
        $stats = [
            'total_posts' => $user->posts()->published()->count(),
            
            'total_views' => $user->posts()->published()->sum('views_count'),
            
            'total_comments' => $user->posts()
                                     ->published()
                                     ->withCount('comments')
                                     ->get()
                                     ->sum('comments_count'),
        ];
        
        return view('authors.show', compact('user', 'posts', 'stats'));
    }
}
```

### Étape 4.7 : Créer le ProfileController

```bash
php artisan make:controller ProfileController
```

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Hash;

class ProfileController extends Controller
{
    /**
     * Afficher le formulaire d'édition du profil
     * 
     * Route : GET /profile
     * Middleware : auth
     * Vue : resources/views/profile/edit.blade.php
     * 
     * @param Request $request
     * @return \Illuminate\View\View
     */
    public function edit(Request $request)
    {
        return view('profile.edit', [
            'user' => $request->user(),
        ]);
    }

    /**
     * Mettre à jour les informations du profil
     * 
     * Route : PATCH /profile
     * Middleware : auth
     * 
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function update(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | VALIDATION DES DONNÉES
        |----------------------------------------------------------------------
        | Rule::unique('users')->ignore($request->user()->id) :
        | L'email doit être unique SAUF pour l'utilisateur actuel.
        | Permet de garder son propre email sans erreur "déjà utilisé".
        */
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => [
                'required',
                'string',
                'email',
                'max:255',
                Rule::unique('users')->ignore($request->user()->id)
            ],
            'bio' => 'nullable|string|max:500',
            'avatar' => 'nullable|url',
        ]);

        // Récupérer l'utilisateur connecté
        $user = $request->user();
        
        // Remplir les nouvelles valeurs
        $user->fill($validated);

        /*
        |----------------------------------------------------------------------
        | RÉINITIALISER EMAIL_VERIFIED_AT SI EMAIL CHANGE
        |----------------------------------------------------------------------
        | Si l'utilisateur change son email, on réinitialise la vérification.
        | isDirty('email') retourne true si la colonne email a été modifiée.
        |
        | L'utilisateur devra re-vérifier son nouvel email.
        */
        if ($user->isDirty('email')) {
            $user->email_verified_at = null;
        }

        $user->save();

        return redirect()
            ->route('profile.edit')
            ->with('success', 'Profil mis à jour avec succès !');
    }

    /**
     * Supprimer le compte utilisateur
     * 
     * Route : DELETE /profile
     * Middleware : auth
     * 
     * Supprime définitivement le compte et toutes ses données associées.
     * Grâce à onDelete('cascade'), les articles et leurs commentaires
     * sont automatiquement supprimés.
     * 
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function destroy(Request $request)
    {
        /*
        |----------------------------------------------------------------------
        | CONFIRMATION PAR MOT DE PASSE
        |----------------------------------------------------------------------
        | current_password : règle de validation spéciale Laravel Breeze
        | Vérifie que le mot de passe fourni correspond au mot de passe actuel.
        |
        | Sécurité : empêche la suppression accidentelle ou par une personne
        | qui aurait accès à la session mais pas au mot de passe.
        */
        $request->validate([
            'password' => ['required', 'current_password'],
        ]);

        $user = $request->user();

        // Déconnecter l'utilisateur
        Auth::logout();

        // Supprimer le compte (cascade = supprime aussi posts et comments)
        $user->delete();

        // Invalider la session
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/')->with('success', 'Compte supprimé avec succès.');
    }
}
```

### Récapitulatif Phase 4

✅ **7 Contrôleurs Créés** :

| Contrôleur | Rôle | Méthodes | Accès |
|------------|------|----------|-------|
| `HomeController` | Page d'accueil | `index()` | Public |
| `PostController` | CRUD articles | `show()`, `create()`, `store()`, `edit()`, `update()`, `destroy()` | Public (show) / Auth (reste) |
| `DashboardController` | Dashboard auteur | `index()` | Auth |
| `CommentController` | Gestion commentaires | `store()`, `approve()`, `destroy()` | Public (store) / Auth (reste) |
| `CategoryController` | Articles par catégorie | `show()` | Public |
| `AuthorController` | Profil auteur public | `show()` | Public |
| `ProfileController` | Gestion profil | `edit()`, `update()`, `destroy()` | Auth |

✅ **Compétences Maîtrisées** :

- Route Model Binding automatique
- Eager Loading (`with()`, `load()`)
- Query Scopes (`published()`, `approved()`)
- Validation de formulaires
- Vérification d'ownership manuelle
- Messages flash (`with()`)
- Relations Eloquent dans contrôleurs
- Collections Laravel (filtrage, tri, agrégation)























## PHASE 5 : Routes et Organisation (~15-20 minutes)

### Vue d'Ensemble de la Phase

> Cette cinquième phase configure le **système de routing** de votre application. Les routes sont la **carte routière** de votre blog : elles définissent quelles URLs sont accessibles, quelles méthodes HTTP sont acceptées (GET, POST, PUT, DELETE), quels contrôleurs/méthodes sont appelés, et quels middlewares protègent l'accès.

!!! example "Laravel utilise un système de **routing expressif** dans les fichiers `routes/web.php` (routes web classiques) et `routes/auth.php` (routes d'authentification Breeze)."

    Chaque route associe une **URL pattern** à une **action** :

    ```php
    <?php
    Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');
    ```

    Cette ligne signifie : "Quand l'utilisateur visite `/posts/introduction-laravel-11` en GET, appelle la méthode `show()` de `PostController` en injectant automatiquement l'objet `Post` correspondant au slug, et nomme cette route `posts.show` pour générer facilement l'URL via `route('posts.show', $post)`."

**Organisation des routes :**

1. **Routes publiques** : accessibles sans authentification (home, posts.show, categories, comments)
2. **Routes authentification** : gérées par Breeze (`require __DIR__.'/auth.php'`)
3. **Routes protégées** : middleware `auth` requis (dashboard, CRUD posts, modération)

!!! note "À l'issue de cette phase, votre application disposera de **toutes les URLs fonctionnelles** et protégées correctement. Vous pourrez naviguer de la page d'accueil vers un article, créer un compte, publier un article, commenter, etc."

!!! warning "Prérequis Phase 5 - La Phase 4 doit être terminée : tous les contrôleurs créés et leurs méthodes implémentées."

### Étape 5.1 : Configurer Toutes les Routes

**Contexte de l'étape :**

> Nous allons configurer **toutes les routes** dans un seul fichier `routes/web.php` organisé en **3 sections** :

> 1. Routes publiques (accessibles sans connexion)
2. Routes Breeze (authentification)
3. Routes protégées (middleware `auth`)

!!! quote "Cette organisation claire facilite la maintenance et la compréhension du système de routing."

**Éditer le fichier principal :**

Ouvrir `routes/web.php` et **remplacer tout le contenu** par :

```php
<?php

use App\Http\Controllers\{
    HomeController,
    PostController,
    DashboardController,
    CommentController,
    CategoryController,
    AuthorController,
    ProfileController
};
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| ROUTES PUBLIQUES
|--------------------------------------------------------------------------
| Ces routes sont accessibles sans authentification.
| Elles constituent la partie "blog" visible par tous les visiteurs.
|
| Méthode HTTP :
| - GET : récupérer des données (affichage)
| - POST : envoyer des données (création)
*/

/**
 * Page d'accueil du blog
 * 
 * URL : http://localhost:8000/
 * Méthode : GET
 * Contrôleur : HomeController::index()
 * Nom : home
 * 
 * Affiche la liste paginée des articles publiés + sidebar
 */
Route::get('/', [HomeController::class, 'index'])->name('home');

/**
 * Afficher un article individuel
 * 
 * URL : http://localhost:8000/posts/introduction-laravel-11
 * Méthode : GET
 * Contrôleur : PostController::show()
 * Nom : posts.show
 * 
 * {post:slug} = Route Model Binding avec custom key
 * Laravel recherche automatiquement le Post via la colonne 'slug'
 * au lieu de 'id' par défaut.
 * 
 * Exemple : /posts/mon-article → recherche WHERE slug='mon-article'
 */
Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');

/**
 * Afficher les articles d'une catégorie
 * 
 * URL : http://localhost:8000/category/technologie
 * Méthode : GET
 * Contrôleur : CategoryController::show()
 * Nom : categories.show
 * 
 * {category:slug} = Binding par slug (comme posts)
 */
Route::get('/category/{category:slug}', [CategoryController::class, 'show'])->name('categories.show');

/**
 * Afficher le profil public d'un auteur
 * 
 * URL : http://localhost:8000/author/1
 * Méthode : GET
 * Contrôleur : AuthorController::show()
 * Nom : authors.show
 * 
 * {user} = Binding par id (défaut)
 * Alternative : {user:name} pour URLs /author/alice-dupont
 */
Route::get('/author/{user}', [AuthorController::class, 'show'])->name('authors.show');

/**
 * Créer un commentaire sur un article (action publique)
 * 
 * URL : http://localhost:8000/posts/123/comments
 * Méthode : POST
 * Contrôleur : CommentController::store()
 * Nom : comments.store
 * 
 * Les visiteurs non inscrits peuvent commenter.
 * Le commentaire sera créé en statut non approuvé.
 * 
 * Formulaire HTML correspondant :
 * <form action="{{ route('comments.store', $post) }}" method="POST">
 */
Route::post('/posts/{post}/comments', [CommentController::class, 'store'])->name('comments.store');

/*
|--------------------------------------------------------------------------
| ROUTES AUTHENTIFICATION (Laravel Breeze)
|--------------------------------------------------------------------------
| Ces routes sont définies dans routes/auth.php (généré par Breeze).
| Elles gèrent tout le système d'authentification :
|
| - GET /register → Formulaire inscription
| - POST /register → Créer compte
| - GET /login → Formulaire connexion
| - POST /login → Authentifier
| - POST /logout → Déconnexion
| - GET /forgot-password → Formulaire reset password
| - POST /forgot-password → Envoyer email reset
| - GET /reset-password/{token} → Formulaire nouveau password
| - POST /reset-password → Définir nouveau password
| - GET /verify-email → Page vérification email
| - GET /verify-email/{id}/{hash} → Lien vérification email
| - POST /email/verification-notification → Renvoyer email vérification
|
| require __DIR__.'/auth.php' : Inclut le fichier auth.php
| Équivaut à copier-coller tout le contenu de auth.php ici.
*/
require __DIR__.'/auth.php';

/*
|--------------------------------------------------------------------------
| ROUTES PROTÉGÉES (Authentification Requise)
|--------------------------------------------------------------------------
| Ces routes nécessitent que l'utilisateur soit connecté.
| Le middleware 'auth' vérifie la présence d'une session valide.
| Si non connecté → redirection vers /login
|
| Route::middleware(['auth'])->group(function() { ... })
| Applique le middleware 'auth' à toutes les routes du groupe.
|
| Alternative sans groupe :
| Route::get('/dashboard', ...)->middleware('auth');
| Mais le groupe est plus lisible pour plusieurs routes.
*/
Route::middleware(['auth'])->group(function () {
    
    /*
    |----------------------------------------------------------------------
    | DASHBOARD AUTEUR
    |----------------------------------------------------------------------
    */
    
    /**
     * Dashboard personnel de l'auteur
     * 
     * URL : http://localhost:8000/dashboard
     * Méthode : GET
     * Contrôleur : DashboardController::index()
     * Nom : dashboard
     * Middleware : auth
     * 
     * Affiche les statistiques et la liste des articles de l'auteur.
     */
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    
    /*
    |----------------------------------------------------------------------
    | GESTION DU PROFIL UTILISATEUR
    |----------------------------------------------------------------------
    */
    
    /**
     * Formulaire d'édition du profil
     * 
     * URL : http://localhost:8000/profile
     * Méthode : GET
     */
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    
    /**
     * Mettre à jour le profil
     * 
     * URL : http://localhost:8000/profile
     * Méthode : PATCH
     * 
     * PATCH = méthode HTTP pour mise à jour partielle
     * Différence avec PUT : PATCH modifie certains champs, PUT remplace tout
     * 
     * Formulaire HTML correspondant :
     * <form action="{{ route('profile.update') }}" method="POST">
     *     @csrf
     *     @method('PATCH')
     */
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    
    /**
     * Supprimer le compte
     * 
     * URL : http://localhost:8000/profile
     * Méthode : DELETE
     * 
     * DELETE = méthode HTTP pour suppression
     * 
     * Formulaire HTML :
     * <form action="{{ route('profile.destroy') }}" method="POST">
     *     @csrf
     *     @method('DELETE')
     */
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
    
    /*
    |----------------------------------------------------------------------
    | CRÉATION D'ARTICLE
    |----------------------------------------------------------------------
    */
    
    /**
     * Formulaire de création d'article
     * 
     * URL : http://localhost:8000/posts/create
     * Méthode : GET
     */
    Route::get('/posts/create', [PostController::class, 'create'])->name('posts.create');
    
    /**
     * Enregistrer un nouvel article
     * 
     * URL : http://localhost:8000/posts
     * Méthode : POST
     */
    Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
    
    /*
    |----------------------------------------------------------------------
    | ÉDITION / SUPPRESSION D'ARTICLE
    |----------------------------------------------------------------------
    | Ces routes vérifient l'ownership dans le contrôleur :
    | if (auth()->id() !== $post->user_id) abort(403);
    */
    
    /**
     * Formulaire d'édition d'article
     * 
     * URL : http://localhost:8000/posts/123/edit
     * Méthode : GET
     */
    Route::get('/posts/{post}/edit', [PostController::class, 'edit'])->name('posts.edit');
    
    /**
     * Mettre à jour un article
     * 
     * URL : http://localhost:8000/posts/123
     * Méthode : PUT
     * 
     * PUT = méthode HTTP pour mise à jour complète
     */
    Route::put('/posts/{post}', [PostController::class, 'update'])->name('posts.update');
    
    /**
     * Supprimer un article
     * 
     * URL : http://localhost:8000/posts/123
     * Méthode : DELETE
     */
    Route::delete('/posts/{post}', [PostController::class, 'destroy'])->name('posts.destroy');
    
    /*
    |----------------------------------------------------------------------
    | MODÉRATION DES COMMENTAIRES
    |----------------------------------------------------------------------
    | Seul l'auteur de l'article peut modérer ses commentaires.
    | Vérification ownership dans le contrôleur.
    */
    
    /**
     * Approuver un commentaire
     * 
     * URL : http://localhost:8000/comments/123/approve
     * Méthode : PATCH
     */
    Route::patch('/comments/{comment}/approve', [CommentController::class, 'approve'])->name('comments.approve');
    
    /**
     * Supprimer un commentaire
     * 
     * URL : http://localhost:8000/comments/123
     * Méthode : DELETE
     */
    Route::delete('/comments/{comment}', [CommentController::class, 'destroy'])->name('comments.destroy');
});

/*
|--------------------------------------------------------------------------
| ROUTES AVEC EMAIL VÉRIFICATION (Optionnel)
|--------------------------------------------------------------------------
| Si vous souhaitez forcer la vérification d'email pour certaines actions,
| ajoutez le middleware 'verified' :
|
| Route::middleware(['auth', 'verified'])->group(function () {
|     Route::get('/posts/create', ...);
|     // L'utilisateur doit avoir vérifié son email pour créer un article
| });
|
| Actuellement désactivé pour simplifier le développement.
*/
```

<small>*Le **Route Model Binding** (`{post:slug}`) est une fonctionnalité puissante de Laravel : au lieu de faire manuellement `Post::where('slug', $slug)->firstOrFail()` dans chaque méthode, Laravel l'injecte automatiquement. Si le slug n'existe pas, Laravel retourne une 404 automatiquement. Le middleware `auth` utilise les guards définis dans `config/auth.php` : par défaut, il vérifie la session web standard. Pour une API, vous utiliseriez `auth:sanctum`.*</small>

### Vérification des Routes Configurées

**Lister toutes les routes :**

```bash
# Afficher toutes les routes enregistrées
php artisan route:list

# Filtrer par nom
php artisan route:list --name=posts

# Filtrer par méthode
php artisan route:list --method=GET

# Sortie compacte (seulement URI, Méthode, Nom)
php artisan route:list --columns=uri,method,name
```

**Sortie attendue (extrait) :**

```
GET|HEAD  /                                home
GET|HEAD  /posts/{post:slug}               posts.show
GET|HEAD  /category/{category:slug}        categories.show
GET|HEAD  /author/{user}                   authors.show
POST      /posts/{post}/comments           comments.store

GET|HEAD  /login                           login
POST      /login                           
GET|HEAD  /register                        register
POST      /register                        
POST      /logout                          logout

GET|HEAD  /dashboard                       dashboard           auth
GET|HEAD  /profile                         profile.edit        auth
PATCH     /profile                         profile.update      auth
DELETE    /profile                         profile.destroy     auth
GET|HEAD  /posts/create                    posts.create        auth
POST      /posts                           posts.store         auth
GET|HEAD  /posts/{post}/edit               posts.edit          auth
PUT       /posts/{post}                    posts.update        auth
DELETE    /posts/{post}                    posts.destroy       auth
PATCH     /comments/{comment}/approve      comments.approve    auth
DELETE    /comments/{comment}              comments.destroy    auth
```

<small>*La colonne `Middleware` affiche les middlewares appliqués. Les routes avec `auth` nécessitent une authentification. Les routes Breeze (`/login`, `/register`, etc.) sont définies dans `routes/auth.php` et apparaissent sans nom pour certaines (Laravel les nomme automatiquement en interne).*</small>

---

### Tableau Récapitulatif des Routes

| URL | Méthode | Nom | Contrôleur | Action | Accès |
|-----|---------|-----|------------|--------|-------|
| `/` | GET | `home` | `HomeController` | Page d'accueil | Public |
| `/posts/{slug}` | GET | `posts.show` | `PostController` | Afficher article | Public |
| `/category/{slug}` | GET | `categories.show` | `CategoryController` | Articles catégorie | Public |
| `/author/{id}` | GET | `authors.show` | `AuthorController` | Profil auteur | Public |
| `/posts/{post}/comments` | POST | `comments.store` | `CommentController` | Créer commentaire | Public |
| **Breeze** | - | - | - | Auth complète | Public |
| `/dashboard` | GET | `dashboard` | `DashboardController` | Dashboard auteur | Auth |
| `/profile` | GET | `profile.edit` | `ProfileController` | Formulaire profil | Auth |
| `/profile` | PATCH | `profile.update` | `ProfileController` | MAJ profil | Auth |
| `/profile` | DELETE | `profile.destroy` | `ProfileController` | Supprimer compte | Auth |
| `/posts/create` | GET | `posts.create` | `PostController` | Formulaire création | Auth |
| `/posts` | POST | `posts.store` | `PostController` | Créer article | Auth |
| `/posts/{post}/edit` | GET | `posts.edit` | `PostController` | Formulaire édition | Auth |
| `/posts/{post}` | PUT | `posts.update` | `PostController` | MAJ article | Auth |
| `/posts/{post}` | DELETE | `posts.destroy` | `PostController` | Supprimer article | Auth |
| `/comments/{id}/approve` | PATCH | `comments.approve` | `CommentController` | Approuver | Auth |
| `/comments/{id}` | DELETE | `comments.destroy` | `CommentController` | Supprimer | Auth |

---

### Récapitulatif Phases 5

✅ **Phase 4 - 7 Contrôleurs Créés** :

- `HomeController` : Page d'accueil + sidebar
- `PostController` : CRUD complet (6 méthodes)
- `DashboardController` : Statistiques auteur
- `CommentController` : Création + modération
- `CategoryController` : Filtrage par catégorie
- `AuthorController` : Profil public
- `ProfileController` : Gestion compte

✅ **Phase 5 - Routes Configurées** :

- 5 routes publiques (home, show, category, author, comment)
- Routes Breeze (authentification complète)
- 12 routes protégées (dashboard, CRUD, modération)

✅ **Compétences Maîtrisées** :

- Architecture MVC complète
- Route Model Binding (`:slug`)
- Middleware (`auth`)
- Groupes de routes
- Nommage de routes (`name()`)
- Méthodes HTTP (GET, POST, PUT, PATCH, DELETE)
- Protection CSRF automatique
- Vérification ownership
- Eager Loading optimisé
- Validation de formulaires
- Messages flash

!!! success "Phases 4 & 5 Terminées - Votre application dispose maintenant de **toute la logique fonctionnelle** et **toutes les URLs configurées**. Il ne reste plus qu'à créer les **vues Blade** (Phase 6) pour afficher l'interface utilisateur, puis tester le tout (Phase 7). Vous êtes à 70% du projet terminé !"













## PHASE 6 : Vues Blade et Interface Utilisateur (~60-90 minutes)

### Vue d'Ensemble de la Phase

> Cette sixième phase constitue la **couche présentation** de votre application MVC. Les vues Blade transforment les données PHP en HTML interactif que les utilisateurs voient dans leur navigateur. C'est la phase où votre blog prend vie visuellement.

!!! info "**Qu'est-ce que Blade ?**"

    Blade est le **moteur de templates** de Laravel. Un moteur de templates est un outil qui permet de mélanger du code PHP et du HTML de manière élégante et sécurisée. Contrairement au PHP pur où vous écririez `<?php echo $variable; ?>`, Blade utilise une syntaxe concise et expressive : `{{ $variable }}`.

!!! success "**Avantages de Blade**"

    - **Syntaxe claire** : `{{ }}` pour afficher, `@if` pour conditions, `@foreach` pour boucles
    - **Échappement automatique** : `{{ $variable }}` échappe automatiquement le HTML (protection XSS)
    - **Héritage de layouts** : évite la duplication de code (header/footer)
    - **Directives puissantes** : `@auth`, `@guest`, `@error`, `@csrf`, etc.
    - **Compilation en PHP pur** : Blade compile vos templates en PHP natif pour de meilleures performances

**Architecture des vues :**

```
resources/views/
├── layouts/
│   └── app.blade.php          # Layout principal (structure commune)
├── home.blade.php              # Page d'accueil
├── dashboard.blade.php         # Dashboard auteur
├── posts/
│   ├── show.blade.php         # Affichage article
│   ├── create.blade.php       # Formulaire création
│   └── edit.blade.php         # Formulaire édition
├── categories/
│   └── show.blade.php         # Articles par catégorie
├── authors/
│   └── show.blade.php         # Profil public auteur
└── profile/
    └── edit.blade.php         # Édition profil utilisateur
```

**Concepts clés que vous allez maîtriser :**

1. **Layouts et héritage** : `@extends`, `@section`, `@yield`
2. **Directives de contrôle** : `@if`, `@foreach`, `@auth`, `@guest`
3. **Composants Breeze** : `<x-dropdown>`, `<x-dropdown-link>`
4. **Protection CSRF** : `@csrf`, `@method`
5. **Affichage conditionnel d'erreurs** : `@error`, `old()`
6. **Helpers Laravel** : `route()`, `Str::limit()`, `session()`
7. **Tailwind CSS** : classes utilitaires pour le style

**Workflow de rendu d'une vue :**

```
Contrôleur → return view('home', compact('posts'))
    ↓
Blade compile home.blade.php en PHP pur
    ↓
Laravel injecte les variables ($posts)
    ↓
PHP exécute le template compilé
    ↓
HTML final envoyé au navigateur
```

À l'issue de cette phase, votre application disposera d'une **interface utilisateur complète et responsive** : page d'accueil attrayante, articles lisibles, formulaires intuitifs, dashboard fonctionnel, et système de navigation cohérent.

!!! warning "Prérequis Phase 6 - Les Phases 1 à 5 doivent être terminées : contrôleurs créés, routes configurées, Tailwind CSS compilé via Vite. Lancez `npm run dev` dans un terminal séparé pour la compilation automatique des assets."

### Étape 6.1 : Modifier le Layout Principal (Structure Commune)

**Contexte de l'étape :**

> Le layout principal (`layouts/app.blade.php`) est le **squelette HTML** partagé par toutes les pages de votre blog. Il contient les éléments communs qui apparaissent sur chaque page :

> - **Header** avec navigation et logo
- **Menu** avec liens conditionnels (connecté/non connecté)
- **Messages flash** (succès/erreur) après actions utilisateur
- **Footer** avec informations copyright
- **Balises meta** et inclusion CSS/JS

!!! quote "L'héritage de layout est un concept fondamental de Blade : au lieu de dupliquer ce code dans chaque vue, vous le définissez **une seule fois** ici, et toutes les autres vues "héritent" de ce layout via `@extends('layouts.app')`."

**Principe de fonctionnement :**

```
Layout (app.blade.php)         Vue enfant (home.blade.php)
┌────────────────────┐         ┌──────────────────┐
│ <html>             │         │ @extends('layout')│
│   <head>...</head> │         │                   │
│   <body>           │         │ @section('content')│
│     <nav>...</nav> │  +  →   │   <h1>Accueil</h1>│
│     @yield('content')│       │ @endsection       │
│     <footer>...</footer>│    └──────────────────┘
│   </body>          │                  ↓
│ </html>            │         HTML final combiné
└────────────────────┘
```

**Ouvrir `resources/views/layouts/app.blade.php`** (créé par Breeze) et **remplacer TOUT le contenu** par :

```html
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
{{--
|------------------------------------------------------------------------------
| SECTION HEAD : Métadonnées et Ressources
|------------------------------------------------------------------------------
| Cette section contient toutes les balises meta, les liens CSS/JS et la
| configuration initiale du document HTML.
--}}
<head>
    {{-- Encodage UTF-8 pour support caractères accentués/spéciaux --}}
    <meta charset="utf-8">
    
    {{-- Viewport pour responsive design (mobile-friendly) --}}
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    {{--
    | CSRF Token : Protection contre les attaques Cross-Site Request Forgery
    | Ce token est injecté automatiquement dans tous les formulaires via @csrf
    | Laravel vérifie que chaque requête POST/PUT/DELETE contient ce token valide
    --}}
    <meta name="csrf-token" content="{{ csrf_token() }}">

    {{--
    | TITRE DYNAMIQUE
    | @yield('title', 'Défaut') : Affiche le contenu de @section('title') de la vue enfant
    | Si la vue enfant ne définit pas @section('title'), affiche 'Blog Multi-Auteurs'
    |
    | Exemple vue enfant :
    | @section('title', 'Accueil')
    | → Résultat : <title>Mon Blog - Accueil</title>
    |
    | config('app.name') : Récupère la valeur de 'name' dans config/app.php
    | Par défaut : 'Laravel', modifiable dans .env via APP_NAME
    --}}
    <title>{{ config('app.name', 'Laravel') }} - @yield('title', 'Blog Multi-Auteurs')</title>

    {{--
    | FONTS : Google Fonts via Bunny.net (alternative RGPD-compliant)
    | preconnect : établit une connexion anticipée au serveur de fonts
    | Optimise le chargement des polices (gain ~100-200ms)
    --}}
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

    {{--
    | VITE : Bundler moderne pour CSS et JS
    | @vite([...]) : Directive Laravel qui injecte les balises <link> et <script>
    | En dev (npm run dev) : Charge via serveur HMR (Hot Module Replacement)
    | En prod (npm run build) : Charge les fichiers minifiés/optimisés
    |
    | resources/css/app.css : Contient @tailwind directives
    | resources/js/app.js : Bootstrap JS pour Alpine.js (utilisé par Breeze)
    --}}
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>

{{--
|------------------------------------------------------------------------------
| SECTION BODY : Contenu Principal
|------------------------------------------------------------------------------
| font-sans : Police system par défaut (Tailwind)
| antialiased : Améliore le rendu des polices (lissage)
--}}
<body class="font-sans antialiased">
    {{--
    | min-h-screen : Hauteur minimale = 100vh (occupe toute la hauteur écran)
    | bg-gray-100 : Fond gris clair (Tailwind)
    --}}
    <div class="min-h-screen bg-gray-100">
        
        {{--
        |----------------------------------------------------------------------
        | NAVIGATION BAR
        |----------------------------------------------------------------------
        | bg-white : Fond blanc
        | border-b border-gray-100 : Bordure inférieure gris très clair
        --}}
        <nav class="bg-white border-b border-gray-100">
            {{--
            | max-w-7xl : Largeur maximale 80rem (1280px)
            | mx-auto : Centrage horizontal (margin left/right auto)
            | px-4 sm:px-6 lg:px-8 : Padding horizontal responsive
            |   - Mobile : 1rem (16px)
            |   - Tablet (sm) : 1.5rem (24px)
            |   - Desktop (lg) : 2rem (32px)
            --}}
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {{--
                | flex justify-between : Flexbox avec espacement entre éléments
                | h-16 : Hauteur fixe 4rem (64px)
                --}}
                <div class="flex justify-between h-16">
                    
                    {{-- PARTIE GAUCHE : Logo + Liens Navigation --}}
                    <div class="flex">
                        {{--
                        | LOGO
                        | shrink-0 : Empêche la réduction du logo en flexbox
                        --}}
                        <div class="shrink-0 flex items-center">
                            {{--
                            | route('home') : Génère l'URL de la route nommée 'home'
                            | Équivaut à : href="/"
                            | Avantage : Si vous changez l'URL de home dans routes/web.php,
                            | tous les liens se mettent à jour automatiquement
                            --}}
                            <a href="{{ route('home') }}" class="text-xl font-bold text-gray-800">
                                📝 {{ config('app.name', 'Blog') }}
                            </a>
                        </div>

                        {{--
                        | LIENS NAVIGATION DESKTOP
                        | hidden : Caché par défaut (mobile)
                        | sm:flex : Affiché en flexbox sur écrans ≥640px (tablet+)
                        | space-x-8 : Espacement horizontal 2rem entre éléments
                        | -my-px : Margin vertical négatif pour aligner bordure
                        --}}
                        <div class="hidden space-x-8 sm:-my-px sm:ml-10 sm:flex">
                            {{--
                            | LIEN ACCUEIL avec état actif
                            | request()->routeIs('home') : Retourne true si route actuelle = 'home'
                            | Ternaire (...) ? 'classes-actif' : 'classes-inactif'
                            | border-b-2 : Bordure inférieure 2px (indicateur page active)
                            --}}
                            <a href="{{ route('home') }}" 
                               class="inline-flex items-center px-1 pt-1 border-b-2 {{ request()->routeIs('home') ? 'border-indigo-400 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' }} text-sm font-medium">
                                Accueil
                            </a>
                            
                            {{--
                            | LIEN DASHBOARD (seulement si connecté)
                            | @auth : Directive Blade = if (auth()->check())
                            | N'affiche le contenu que si utilisateur authentifié
                            --}}
                            @auth
                            <a href="{{ route('dashboard') }}" 
                               class="inline-flex items-center px-1 pt-1 border-b-2 {{ request()->routeIs('dashboard') ? 'border-indigo-400 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' }} text-sm font-medium">
                                Dashboard
                            </a>
                            @endauth
                        </div>
                    </div>

                    {{--
                    | PARTIE DROITE : Actions Utilisateur
                    | hidden sm:flex sm:items-center sm:ml-6 : Caché mobile, visible tablet+
                    --}}
                    <div class="hidden sm:flex sm:items-center sm:ml-6">
                        {{--
                        | SI UTILISATEUR CONNECTÉ
                        | @auth équivaut à if (Auth::check())
                        --}}
                        @auth
                            {{--
                            | BOUTON CRÉER ARTICLE
                            | inline-flex : Flexbox inline pour aligner texte + icône
                            | px-4 py-2 : Padding horizontal 1rem, vertical 0.5rem
                            | bg-indigo-600 : Fond indigo (couleur primaire)
                            | rounded-md : Bordures arrondies 0.375rem
                            | uppercase tracking-widest : Texte majuscules + espacement lettres
                            | hover:bg-indigo-700 : Fond plus foncé au survol
                            | focus:ring-2 : Anneau focus pour accessibilité clavier
                            | transition ease-in-out duration-150 : Animation douce 150ms
                            --}}
                            <a href="{{ route('posts.create') }}" 
                               class="mr-4 inline-flex items-center px-4 py-2 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-indigo-700 focus:bg-indigo-700 active:bg-indigo-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition ease-in-out duration-150">
                                ✏️ Nouvel Article
                            </a>

                            {{--
                            | DROPDOWN UTILISATEUR (Composant Breeze)
                            | <x-dropdown> : Composant Blade (défini dans resources/views/components/)
                            | align="right" : Aligne le menu déroulant à droite
                            | width="48" : Largeur 12rem (48*0.25rem)
                            --}}
                            <x-dropdown align="right" width="48">
                                {{--
                                | SLOT "trigger" : Contenu du bouton déclencheur
                                | Les slots sont des zones de contenu nommées dans les composants
                                --}}
                                <x-slot name="trigger">
                                    <button class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-500 bg-white hover:text-gray-700 focus:outline-none transition ease-in-out duration-150">
                                        {{--
                                        | Auth::user()->name : Nom de l'utilisateur connecté
                                        | Équivaut à : auth()->user()->name
                                        --}}
                                        <div>{{ Auth::user()->name }}</div>

                                        {{-- Icône chevron-down (SVG) --}}
                                        <div class="ml-1">
                                            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                                            </svg>
                                        </div>
                                    </button>
                                </x-slot>

                                {{--
                                | SLOT "content" : Contenu du menu déroulant
                                | <x-dropdown-link> : Autre composant Breeze pour les items
                                --}}
                                <x-slot name="content">
                                    {{-- Lien vers édition profil --}}
                                    <x-dropdown-link :href="route('profile.edit')">
                                        Mon Profil
                                    </x-dropdown-link>

                                    {{--
                                    | DÉCONNEXION (nécessite POST + CSRF)
                                    | Les routes de déconnexion utilisent POST pour sécurité
                                    --}}
                                    <form method="POST" action="{{ route('logout') }}">
                                        {{--
                                        | @csrf : Génère un champ <input type="hidden" name="_token" value="...">
                                        | Obligatoire pour TOUTES les requêtes POST/PUT/PATCH/DELETE
                                        | Laravel rejette les requêtes sans token CSRF valide (protection)
                                        --}}
                                        @csrf

                                        {{--
                                        | onclick="event.preventDefault(); this.closest('form').submit();"
                                        | Empêche comportement par défaut du lien (navigation)
                                        | Soumet le formulaire parent via JavaScript
                                        --}}
                                        <x-dropdown-link :href="route('logout')"
                                                onclick="event.preventDefault();
                                                            this.closest('form').submit();">
                                            Déconnexion
                                        </x-dropdown-link>
                                    </form>
                                </x-slot>
                            </x-dropdown>
                        
                        {{--
                        | SI UTILISATEUR NON CONNECTÉ
                        | @else : Alternative à @auth (comme else en PHP)
                        --}}
                        @else
                            {{-- Lien Connexion --}}
                            <a href="{{ route('login') }}" class="text-sm text-gray-700 hover:text-gray-900 mr-4">Connexion</a>
                            
                            {{-- Bouton S'inscrire --}}
                            <a href="{{ route('register') }}" class="text-sm text-gray-700 hover:text-gray-900 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">S'inscrire</a>
                        @endauth
                    </div>
                </div>
            </div>
        </nav>

        {{--
        |----------------------------------------------------------------------
        | CONTENU PRINCIPAL DE LA PAGE
        |----------------------------------------------------------------------
        | <main> : Balise sémantique HTML5 pour contenu principal
        --}}
        <main>
            {{--
            | MESSAGES FLASH (Succès)
            | session('success') : Récupère la valeur de session('success')
            | Définie dans contrôleurs via : ->with('success', 'Message...')
            | La session flash est disponible une seule fois puis supprimée
            |
            | @if(session('success')) : Affiche seulement si session existe
            --}}
            @if (session('success'))
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
                    {{--
                    | ALERTE SUCCÈS (vert)
                    | role="alert" : Attribut ARIA pour accessibilité (lecteurs d'écran)
                    | bg-green-100 : Fond vert clair
                    | border-green-400 : Bordure verte
                    | text-green-700 : Texte vert foncé
                    --}}
                    <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                        {{--
                        | {{ session('success') }} : Affiche le message
                        | block sm:inline : Block sur mobile, inline sur tablet+
                        --}}
                        <span class="block sm:inline">{{ session('success') }}</span>
                    </div>
                </div>
            @endif

            {{--
            | MESSAGES FLASH (Erreur)
            | Même logique que succès mais style rouge
            --}}
            @if (session('error'))
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
                    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                        <span class="block sm:inline">{{ session('error') }}</span>
                    </div>
                </div>
            @endif

            {{--
            | @yield('content') : Point d'injection du contenu des vues enfants
            | Les vues enfants définissent @section('content') ... @endsection
            | Le contenu de cette section remplace @yield('content') ici
            |
            | Exemple :
            | Vue enfant home.blade.php :
            | @extends('layouts.app')
            | @section('content')
            |   <h1>Bienvenue</h1>
            | @endsection
            |
            | → @yield('content') sera remplacé par <h1>Bienvenue</h1>
            --}}
            @yield('content')
        </main>

        {{--
        |----------------------------------------------------------------------
        | FOOTER
        |----------------------------------------------------------------------
        | mt-12 : Margin-top 3rem (espace entre contenu et footer)
        --}}
        <footer class="bg-white border-t border-gray-200 mt-12">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {{--
                | text-center : Centrage horizontal du texte
                | date('Y') : Fonction PHP qui retourne l'année actuelle (ex: 2024)
                --}}
                <div class="text-center text-gray-500 text-sm">
                    © {{ date('Y') }} {{ config('app.name') }}. Blog Multi-Auteurs avec Laravel Breeze.
                </div>
            </div>
        </footer>
    </div>
</body>
</html>
```

<small>**Explication Tailwind CSS :** Les classes comme `px-4` signifient "padding-x (horizontal) de 1rem (16px)", `sm:px-6` applique "padding-x de 1.5rem sur écrans ≥640px". Tailwind utilise une échelle de 0.25rem : `px-1` = 0.25rem, `px-4` = 1rem, `px-8` = 2rem. Les préfixes `sm:`, `md:`, `lg:` sont des breakpoints responsive (mobile-first). Les couleurs utilisent une échelle 50-900 : `bg-gray-100` est très clair, `bg-gray-900` très foncé. **Protection CSRF :** Le token `@csrf` est généré par Laravel à chaque session et vérifié côté serveur. Sans lui, toute requête POST/PUT/DELETE est rejetée avec erreur 419 (protection contre attaques CSRF où un site malveillant tente de soumettre un formulaire à votre place). **Composants Breeze :** `<x-dropdown>` est un composant Blade réutilisable (fichier `resources/views/components/dropdown.blade.php`). Les slots (`<x-slot name="...">`) permettent d'injecter du contenu HTML dans des zones prédéfinies du composant. C'est l'équivalent Blade des composants React/Vue.</small>

### Étape 6.2 : Créer la Page d'Accueil (Liste Articles + Sidebar)

**Contexte de l'étape :**

> La page d'accueil est la **vitrine** de votre blog. Elle doit immédiatement capter l'attention du visiteur et l'inciter à explorer les articles. Cette page affiche :

> 1. **Hero Section** : Bandeau d'accueil avec titre accrocheur et appel à l'action
2. **Grille d'articles** : Liste paginée des 9 derniers articles publiés (cards avec image, titre, excerpt, méta)
3. **Sidebar** : Colonne latérale avec catégories (+ compteurs) et articles populaires (top 3 par vues)

!!! quote "Cette page utilise une **disposition en grille CSS** (2/3 pour articles, 1/3 pour sidebar sur desktop) qui s'adapte automatiquement sur mobile (colonne unique)."

**Variables disponibles dans la vue :**

Rappel du contrôleur `HomeController::index()` :

```php
<?php

return view('home', compact('posts', 'categories', 'popularPosts'));
```

- `$posts` : Collection paginée de 9 articles (objet `LengthAwarePaginator`)
- `$categories` : Collection de 6 catégories avec attribut virtuel `posts_count`
- `$popularPosts` : Collection de 3 articles triés par vues décroissantes

**Créer le fichier `resources/views/home.blade.php` :**

```html
{{--
|------------------------------------------------------------------------------
| PAGE D'ACCUEIL DU BLOG
|------------------------------------------------------------------------------
| Vue enfant qui hérite du layout principal (layouts/app.blade.php)
|
| @extends('layouts.app') : Indique que cette vue hérite de app.blade.php
| Toute la structure HTML (head, nav, footer) vient du layout parent
--}}
@extends('layouts.app')

{{--
| SECTION TITLE : Définit le titre de la page
| @section('title', 'Valeur') : Syntaxe courte pour sections simples
| Équivaut à :
| @section('title')
|     Accueil
| @endsection
|
| Ce contenu remplace @yield('title') dans le layout
| Résultat <title> : "Mon Blog - Accueil"
--}}
@section('title', 'Accueil')

{{--
| SECTION CONTENT : Contenu principal de la page
| @section('content') ... @endsection : Syntaxe longue pour sections complexes
| Ce contenu remplace @yield('content') dans le layout
--}}
@section('content')
{{--
| py-12 : Padding vertical 3rem (haut + bas)
| Crée de l'espace entre la nav et le contenu
--}}
<div class="py-12">
    {{--
    | CONTENEUR PRINCIPAL
    | max-w-7xl : Largeur max 1280px
    | mx-auto : Centrage horizontal
    | sm:px-6 lg:px-8 : Padding responsive (1.5rem tablet, 2rem desktop)
    --}}
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        
        {{--
        |----------------------------------------------------------------------
        | HERO SECTION (Bandeau d'Accueil)
        |----------------------------------------------------------------------
        | Section visible en premier, présente le blog aux visiteurs
        | overflow-hidden : Cache débordement (utile pour images/animations)
        | shadow-sm : Ombre légère (Tailwind prédéfini)
        | sm:rounded-lg : Bordures arrondies 0.5rem sur tablet+
        | mb-8 : Margin-bottom 2rem (espace sous la section)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-8">
            <div class="p-6 text-center">
                {{--
                | TITRE PRINCIPAL
                | text-4xl : Taille texte 2.25rem (36px)
                | font-bold : Graisse 700
                | mb-4 : Margin-bottom 1rem
                --}}
                <h1 class="text-4xl font-bold text-gray-900 mb-4">
                    Bienvenue sur notre Blog
                </h1>
                
                {{--
                | SOUS-TITRE
                | text-lg : Taille texte 1.125rem (18px)
                | text-gray-600 : Gris moyen
                --}}
                <p class="text-lg text-gray-600 mb-6">
                    Découvrez des articles passionnants sur la technologie, le voyage, la cuisine et plus encore.
                </p>
                
                {{--
                | BOUTON APPEL À L'ACTION (seulement si visiteur non connecté)
                | @guest : Directive Blade = if (!auth()->check())
                | Opposé de @auth, affiche contenu seulement si NON connecté
                --}}
                @guest
                <a href="{{ route('register') }}" 
                   class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                    Devenir Auteur
                </a>
                @endguest
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | DISPOSITION EN GRILLE : Articles (2/3) + Sidebar (1/3)
        |----------------------------------------------------------------------
        | grid grid-cols-1 : Grille 1 colonne par défaut (mobile)
        | lg:grid-cols-3 : Grille 3 colonnes sur écrans ≥1024px (desktop)
        | gap-8 : Espacement 2rem entre éléments de grille
        --}}
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {{--
            | COLONNE ARTICLES (occupe 2/3 de la largeur sur desktop)
            | lg:col-span-2 : Cette div occupe 2 colonnes sur 3 (desktop)
            | Sur mobile (1 colonne) : occupe toute la largeur
            --}}
            <div class="lg:col-span-2">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">Articles Récents</h2>
                
                {{--
                | VÉRIFICATION PRÉSENCE D'ARTICLES
                | @if($posts->count() > 0) : Condition Blade
                | $posts->count() : Nombre d'éléments dans la Collection paginée
                | Équivaut à : if ($posts->count() > 0) { ... }
                --}}
                @if($posts->count() > 0)
                    {{--
                    | GRILLE D'ARTICLES
                    | grid-cols-1 : 1 colonne mobile
                    | md:grid-cols-2 : 2 colonnes sur écrans ≥768px (tablet)
                    | gap-6 : Espacement 1.5rem entre cards
                    | mb-8 : Margin-bottom avant pagination
                    --}}
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        {{--
                        | BOUCLE SUR LES ARTICLES
                        | @foreach($posts as $post) : Itère sur chaque article
                        | $post : Instance du modèle Post avec relations chargées (user, category)
                        | Équivaut à : foreach ($posts as $post) { ... }
                        --}}
                        @foreach($posts as $post)
                        {{--
                        | CARD ARTICLE
                        | hover:shadow-md : Ombre moyenne au survol (feedback interactif)
                        | transition : Animation douce (150ms par défaut)
                        --}}
                        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg hover:shadow-md transition">
                            {{--
                            | IMAGE COUVERTURE (conditionnelle)
                            | @if($post->image) : Affiche seulement si colonne image non null
                            | h-48 : Hauteur fixe 12rem (192px)
                            | object-cover : Image couvre zone sans distorsion (crop si nécessaire)
                            --}}
                            @if($post->image)
                            <div class="h-48 bg-gray-200 overflow-hidden">
                                {{--
                                | {{ $post->image }} : Affiche URL image (échappement auto HTML)
                                | alt="{{ $post->title }}" : Texte alternatif pour accessibilité
                                --}}
                                <img src="{{ $post->image }}" alt="{{ $post->title }}" class="w-full h-full object-cover">
                            </div>
                            @endif
                            
                            <div class="p-6">
                                {{--
                                | BADGE CATÉGORIE
                                | inline-block : Pour appliquer padding sur élément inline
                                | rounded-full : Bordures complètement arrondies (pilule)
                                | $post->category->slug : Accès relation belongsTo
                                | Laravel charge automatiquement la catégorie via Eager Loading
                                --}}
                                <a href="{{ route('categories.show', $post->category->slug) }}" 
                                   class="inline-block px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-semibold rounded-full mb-3">
                                    {{ $post->category->name }}
                                </a>
                                
                                {{--
                                | TITRE ARTICLE
                                | hover:text-indigo-600 : Couleur change au survol (feedback)
                                --}}
                                <h3 class="text-xl font-bold text-gray-900 mb-2">
                                    <a href="{{ route('posts.show', $post->slug) }}" class="hover:text-indigo-600">
                                        {{ $post->title }}
                                    </a>
                                </h3>
                                
                                {{--
                                | EXCERPT (Résumé)
                                | Str::limit($text, 120) : Helper Laravel qui tronque à 120 caractères
                                | Ajoute "..." si tronqué
                                | Évite débordement texte sur cards
                                --}}
                                <p class="text-gray-600 text-sm mb-4">
                                    {{ Str::limit($post->excerpt, 120) }}
                                </p>
                                
                                {{--
                                | META INFORMATIONS (Auteur, Date, Vues)
                                | flex justify-between : Répartit espace entre 2 éléments
                                --}}
                                <div class="flex items-center justify-between text-xs text-gray-500">
                                    <div class="flex items-center">
                                        {{--
                                        | LIEN AUTEUR
                                        | route('authors.show', $post->user) : Passe objet User entier
                                        | Laravel génère : /author/1 (utilise $user->id)
                                        | Alternative : route('authors.show', $post->user_id)
                                        --}}
                                        <a href="{{ route('authors.show', $post->user) }}" class="hover:text-indigo-600">
                                            {{ $post->user->name }}
                                        </a>
                                        <span class="mx-2">•</span>
                                        {{--
                                        | DATE RELATIVE
                                        | $post->published_at : Instance Carbon (DateTime amélioré)
                                        | diffForHumans() : Convertit en format lisible
                                        | Exemples : "il y a 2 heures", "il y a 3 jours", "il y a 2 mois"
                                        | Alternative : format('d M Y') pour "10 Déc 2024"
                                        --}}
                                        <span>{{ $post->published_at->diffForHumans() }}</span>
                                    </div>
                                    <div>
                                        👁️ {{ $post->views_count }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        @endforeach
                    </div>

                    {{--
                    | PAGINATION
                    | {{ $posts->links() }} : Génère automatiquement les liens pagination
                    | Affiche : « Précédent | 1 2 3 ... | Suivant »
                    | Style par défaut : Tailwind (configuré dans AppServiceProvider)
                    | Gère automatiquement :
                    | - Ajout ?page=2 dans URL
                    | - Désactivation boutons si première/dernière page
                    | - Affichage ellipsis (...) si beaucoup de pages
                    --}}
                    <div class="mt-6">
                        {{ $posts->links() }}
                    </div>
                
                {{--
                | ÉTAT VIDE (si aucun article)
                | @else : Alternative au @if (comme else en PHP)
                --}}
                @else
                    <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                        <p class="text-gray-600">Aucun article publié pour le moment.</p>
                    </div>
                @endif
            </div>

            {{--
            |----------------------------------------------------------------------
            | SIDEBAR (Catégories + Articles Populaires)
            |----------------------------------------------------------------------
            | lg:col-span-1 : Occupe 1 colonne sur 3 (desktop)
            | space-y-6 : Espacement vertical 1.5rem entre sections
            --}}
            <div class="space-y-6">
                
                {{--
                | WIDGET CATÉGORIES
                --}}
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4">Catégories</h3>
                    {{--
                    | LISTE CATÉGORIES
                    | space-y-2 : Espacement vertical 0.5rem entre items
                    --}}
                    <ul class="space-y-2">
                        {{--
                        | BOUCLE SUR CATÉGORIES
                        | $category : Instance de Category avec attribut virtuel posts_count
                        | (ajouté via withCount('posts') dans le contrôleur)
                        --}}
                        @foreach($categories as $category)
                        <li>
                            <a href="{{ route('categories.show', $category->slug) }}" 
                               class="flex items-center justify-between text-gray-600 hover:text-indigo-600">
                                <span>{{ $category->name }}</span>
                                {{--
                                | BADGE COMPTEUR
                                | {{ $category->posts_count }} : Attribut virtuel ajouté par withCount()
                                | Ce n'est PAS une colonne de la table, mais calculé par Laravel
                                --}}
                                <span class="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded-full">
                                    {{ $category->posts_count }}
                                </span>
                            </a>
                        </li>
                        @endforeach
                    </ul>
                </div>

                {{--
                | WIDGET ARTICLES POPULAIRES
                --}}
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4">📈 Les Plus Lus</h3>
                    <ul class="space-y-4">
                        {{--
                        | BOUCLE SUR POPULAIRES (top 3)
                        --}}
                        @foreach($popularPosts as $popular)
                        <li class="border-b border-gray-200 pb-3 last:border-0">
                            {{--
                            | TITRE ARTICLE
                            | Str::limit($popular->title, 50) : Tronque à 50 caractères
                            | block : Force affichage en bloc (occupe toute la largeur)
                            --}}
                            <a href="{{ route('posts.show', $popular->slug) }}" 
                               class="text-sm font-medium text-gray-900 hover:text-indigo-600 block mb-1">
                                {{ Str::limit($popular->title, 50) }}
                            </a>
                            {{--
                            | META VUES
                            --}}
                            <div class="text-xs text-gray-500">
                                👁️ {{ $popular->views_count }} vues
                            </div>
                        </li>
                        @endforeach
                    </ul>
                </div>

            </div>
        </div>
    </div>
</div>
@endsection
```

<small>**Explication Pagination Laravel :** `$posts->links()` génère HTML complet (boutons Précédent/Suivant, numéros de pages, ellipsis). Laravel détecte automatiquement le paramètre `?page=` dans l'URL et récupère la bonne tranche de données. La méthode `paginate(9)` dans le contrôleur exécute 2 requêtes SQL : une pour compter le total (`SELECT COUNT(*)`), une pour récupérer les 9 articles de la page actuelle (`SELECT * LIMIT 9 OFFSET X`). **Helper Str::limit() :** Tronque intelligemment en respectant les mots complets (évite de couper au milieu d'un mot). Exemple : `Str::limit("Introduction à Laravel", 15)` retourne `"Introduction à..."` (16 caractères car respecte le mot). **Carbon diffForHumans() :** Convertit une date en format relatif localisé. Configure la locale dans `config/app.php` (`'locale' => 'fr'`) pour afficher "il y a 2 jours" au lieu de "2 days ago".</small>

**Tableau Récapitulatif des Directives Blade**

| Directive | Équivalent PHP | Usage | Exemple |
|-----------|----------------|-------|---------|
| `{{ $var }}` | `<?php echo htmlspecialchars($var); ?>` | Afficher variable (échappement auto) | `{{ $post->title }}` |
| `{!! $var !!}` | `<?php echo $var; ?>` | Afficher HTML brut (DANGEREUX) | `{!! $post->content !!}` |
| `@if($condition)` | `<?php if($condition): ?>` | Condition | `@if($posts->count() > 0)` |
| `@else` | `<?php else: ?>` | Sinon | `@else` |
| `@elseif($cond)` | `<?php elseif($cond): ?>` | Sinon si | `@elseif($user->isAdmin())` |
| `@endif` | `<?php endif; ?>` | Fin condition | `@endif` |
| `@foreach($items as $item)` | `<?php foreach($items as $item): ?>` | Boucle | `@foreach($posts as $post)` |
| `@endforeach` | `<?php endforeach; ?>` | Fin boucle | `@endforeach` |
| `@auth` | `<?php if(auth()->check()): ?>` | Si connecté | `@auth` |
| `@guest` | `<?php if(!auth()->check()): ?>` | Si NON connecté | `@guest` |
| `@csrf` | `<input type="hidden" name="_token" value="...">` | Token CSRF | `@csrf` |
| `@method('PUT')` | `<input type="hidden" name="_method" value="PUT">` | Spoofing méthode HTTP | `@method('PUT')` |
| `@error('field')` | Affiche erreur validation | Erreur champ | `@error('title')` |
| `@extends('layout')` | Hérite d'un layout | Héritage | `@extends('layouts.app')` |
| `@section('name')` | Définit section | Contenu nommé | `@section('content')` |
| `@yield('name')` | Injecte section | Point d'injection | `@yield('content')` |

### Étape 6.3 : Créer la Vue Article Individuel (Affichage Complet)

**Contexte de l'étape :**

> La page d'affichage d'un article est le **cœur de votre blog**. C'est ici que les visiteurs consomment le contenu principal. Cette vue doit être :

> - **Lisible** : Typographie claire, espacement généreux, hiérarchie visuelle
- **Interactive** : Commentaires, boutons partage, actions auteur
- **Engageante** : Articles similaires, compteurs sociaux, sidebar

> Cette page gère **plusieurs cas d'usage** :

> 1. **Visiteur anonyme** : Consulte article publié + commentaires approuvés
2. **Auteur de l'article** : Voit aussi les brouillons + boutons Modifier/Supprimer + commentaires en attente
3. **Autre utilisateur connecté** : Voit articles publiés mais pas les actions auteur

**Variables disponibles dans la vue :**

Rappel du contrôleur `PostController::show()` :

```php
return view('posts.show', compact('post', 'relatedPosts'));
```

- `$post` : Instance Post avec relations chargées (`user`, `category`, `comments` filtrés approuvés)
- `$relatedPosts` : Collection de 3 articles de la même catégorie

**Créer le dossier `resources/views/posts/` puis le fichier `resources/views/posts/show.blade.php` :**

```bash
# Créer le dossier posts
mkdir resources/views/posts

# Le fichier show.blade.php sera créé manuellement
```

**Contenu de `resources/views/posts/show.blade.php` :**

```html
{{--
|------------------------------------------------------------------------------
| PAGE ARTICLE INDIVIDUEL
|------------------------------------------------------------------------------
| Vue détaillée d'un article avec contenu complet, commentaires et similaires
--}}
@extends('layouts.app')

{{--
| TITRE DYNAMIQUE : Utilise le titre de l'article
| {{ $post->title }} sera échappé automatiquement (protection XSS)
--}}
@section('title', $post->title)

@section('content')
<div class="py-12">
    {{--
    | CONTENEUR ARTICLE (largeur réduite pour meilleure lisibilité)
    | max-w-4xl : Largeur max 56rem (896px) au lieu de 7xl (1280px)
    | Articles longs sont plus lisibles avec colonnes étroites (60-80 caractères/ligne)
    --}}
    <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
        
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-8">
                
                {{--
                |----------------------------------------------------------------------
                | ALERTE BROUILLON (seulement si status = draft)
                |----------------------------------------------------------------------
                | @if($post->status === 'draft') : Condition stricte (===)
                | Les brouillons ne sont visibles QUE par l'auteur (vérifié dans contrôleur)
                | Cette alerte rappelle à l'auteur que l'article n'est pas public
                --}}
                @if($post->status === 'draft')
                <div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mb-6">
                    {{--
                    | <strong> : Balise HTML pour texte important (graisse bold par défaut)
                    | ⚠️ : Emoji unicode pour alerte visuelle
                    --}}
                    <strong>⚠️ Brouillon :</strong> Cet article n'est visible que par vous.
                </div>
                @endif

                {{--
                | BADGE CATÉGORIE (lien cliquable)
                | $post->category : Relation belongsTo chargée via Eager Loading
                | $post->category->slug : Accès à l'attribut slug de la catégorie
                --}}
                <a href="{{ route('categories.show', $post->category->slug) }}" 
                   class="inline-block px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-semibold rounded-full mb-4">
                    {{ $post->category->name }}
                </a>

                {{--
                | TITRE ARTICLE (Balise H1)
                | text-4xl : Taille 2.25rem (36px)
                | mb-4 : Margin-bottom 1rem
                | Une seule H1 par page (SEO)
                --}}
                <h1 class="text-4xl font-bold text-gray-900 mb-4">
                    {{ $post->title }}
                </h1>

                {{--
                |----------------------------------------------------------------------
                | META INFORMATIONS (Auteur, Date, Stats)
                |----------------------------------------------------------------------
                | flex items-center : Flexbox avec alignement vertical centré
                | text-sm : Taille texte 0.875rem (14px)
                --}}
                <div class="flex items-center text-sm text-gray-500 mb-6">
                    {{--
                    | BLOC AUTEUR (Avatar + Nom + Date)
                    | hover:text-indigo-600 : Feedback visuel au survol
                    --}}
                    <a href="{{ route('authors.show', $post->user) }}" class="flex items-center hover:text-indigo-600">
                        {{--
                        | AVATAR (Initiale dans cercle)
                        | w-10 h-10 : Largeur/hauteur 2.5rem (40px)
                        | rounded-full : Bordures arrondies 100% (cercle parfait)
                        | substr($post->user->name, 0, 1) : Fonction PHP extraction 1er caractère
                        | Exemple : "Alice Dupont" → "A"
                        --}}
                        <div class="w-10 h-10 bg-gray-300 rounded-full mr-3 flex items-center justify-center text-lg">
                            {{ substr($post->user->name, 0, 1) }}
                        </div>
                        <div>
                            {{--
                            | NOM AUTEUR
                            | font-medium : Graisse 500 (entre normal 400 et bold 700)
                            --}}
                            <div class="font-medium text-gray-900">{{ $post->user->name }}</div>
                            {{--
                            | DATE PUBLICATION (ou "Brouillon")
                            | $post->published_at : Carbon instance (peut être null pour brouillons)
                            | ? : Opérateur ternaire PHP
                            | format('d M Y') : Formatage date "10 Déc 2024"
                            --}}
                            <div>{{ $post->published_at ? $post->published_at->format('d M Y') : 'Brouillon' }}</div>
                        </div>
                    </a>
                    
                    {{--
                    | SÉPARATEURS ET STATS
                    | mx-4 : Margin horizontal 1rem (espacement entre éléments)
                    | • : Caractère unicode bullet point
                    --}}
                    <span class="mx-4">•</span>
                    <span>👁️ {{ $post->views_count }} vues</span>
                    <span class="mx-4">•</span>
                    {{--
                    | COMPTEUR COMMENTAIRES
                    | $post->comments->count() : Compte éléments dans Collection comments
                    | Attention : Cette Collection contient SEULEMENT les commentaires approuvés
                    | (filtrés via Eager Loading dans le contrôleur)
                    --}}
                    <span>💬 {{ $post->comments->count() }} commentaires</span>
                </div>

                {{--
                | IMAGE COUVERTURE (conditionnelle)
                | @if($post->image) : Affiche seulement si colonne image non null
                | mb-8 : Margin-bottom 2rem (espace avant contenu)
                --}}
                @if($post->image)
                <div class="mb-8">
                    {{--
                    | h-96 : Hauteur fixe 24rem (384px)
                    | object-cover : Image couvre zone sans distorsion
                    | rounded-lg : Bordures arrondies 0.5rem
                    --}}
                    <img src="{{ $post->image }}" alt="{{ $post->title }}" class="w-full h-96 object-cover rounded-lg">
                </div>
                @endif

                {{--
                |----------------------------------------------------------------------
                | BOUTONS ACTIONS AUTEUR (Modifier + Supprimer)
                |----------------------------------------------------------------------
                | Visibles SEULEMENT si :
                | 1. Utilisateur connecté (@auth)
                | 2. Utilisateur = auteur de l'article (auth()->id() === $post->user_id)
                --}}
                @auth
                @if(auth()->id() === $post->user_id)
                <div class="flex gap-4 mb-6 pb-6 border-b border-gray-200">
                    {{--
                    | BOUTON MODIFIER
                    | gap-4 : Espacement 1rem entre boutons (Flexbox gap)
                    | bg-gray-800 : Fond gris très foncé (presque noir)
                    --}}
                    <a href="{{ route('posts.edit', $post) }}" 
                       class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700">
                        ✏️ Modifier
                    </a>
                    
                    {{--
                    | BOUTON SUPPRIMER (Formulaire avec confirmation JS)
                    | Nécessite formulaire POST + method spoofing DELETE + CSRF token
                    | onsubmit : Event handler JavaScript
                    | return confirm('...') : Affiche popup confirmation navigateur
                    | Si utilisateur clique "Annuler" → return false → soumission annulée
                    | Si utilisateur clique "OK" → return true → soumission continue
                    --}}
                    <form action="{{ route('posts.destroy', $post) }}" method="POST" 
                          onsubmit="return confirm('Êtes-vous sûr de vouloir supprimer cet article ?');">
                        {{--
                        | @csrf : Token CSRF obligatoire pour POST/PUT/DELETE
                        | Génère : <input type="hidden" name="_token" value="...">
                        --}}
                        @csrf
                        {{--
                        | @method('DELETE') : Spoofing méthode HTTP
                        | HTML ne supporte que GET et POST dans <form>
                        | Laravel convertit POST + _method=DELETE en vraie requête DELETE côté serveur
                        | Génère : <input type="hidden" name="_method" value="DELETE">
                        --}}
                        @method('DELETE')
                        <button type="submit" 
                                class="inline-flex items-center px-4 py-2 bg-red-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-red-700">
                            🗑️ Supprimer
                        </button>
                    </form>
                </div>
                @endif
                @endauth

                {{--
                |----------------------------------------------------------------------
                | CONTENU ARTICLE
                |----------------------------------------------------------------------
                | prose : Classe Tailwind Typography Plugin
                | Applique styles typographiques (marges, tailles, line-height)
                | prose-lg : Variante large (texte plus gros pour meilleure lisibilité)
                | max-w-none : Annule largeur max par défaut de prose
                | mb-12 : Margin-bottom 3rem (espace avant section commentaires)
                --}}
                <div class="prose prose-lg max-w-none mb-12">
                    {{--
                    | AFFICHAGE CONTENU AVEC SAUTS DE LIGNE
                    | {!! $var !!} : Affiche HTML SANS échappement (DANGEREUX si input utilisateur)
                    | nl2br() : Convertit \n en <br> (sauts de ligne visibles en HTML)
                    | e() : Échappe HTML (protection XSS)
                    |
                    | Ordre important :
                    | 1. e($post->content) : Échappe HTML malveillant (<script> devient &lt;script&gt;)
                    | 2. nl2br() : Convertit \n en <br>
                    | 3. {!! !!} : Affiche le résultat avec <br> fonctionnels
                    |
                    | Pourquoi {!! !!} et pas {{ }} ?
                    | {{ nl2br(e($post->content)) }} afficherait "&lt;br&gt;" (texte brut)
                    | {!! nl2br(e($post->content)) !!} affiche <br> (balise HTML)
                    |
                    | Alternative avec éditeur WYSIWYG (future amélioration) :
                    | {!! $post->content !!} directement (si contenu déjà HTML safe)
                    --}}
                    {!! nl2br(e($post->content)) !!}
                </div>

            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | ARTICLES SIMILAIRES (Même Catégorie)
        |----------------------------------------------------------------------
        | @if($relatedPosts->count() > 0) : Affiche seulement si articles trouvés
        | $relatedPosts : Collection de max 3 articles (définie dans contrôleur)
        --}}
        @if($relatedPosts->count() > 0)
        <div class="mt-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Articles Similaires</h2>
            {{--
            | GRILLE 3 COLONNES
            | grid-cols-1 : 1 colonne mobile
            | md:grid-cols-3 : 3 colonnes tablet+ (chaque article = 1 colonne)
            --}}
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {{--
                | BOUCLE SUR SIMILAIRES
                --}}
                @foreach($relatedPosts as $related)
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg hover:shadow-md transition">
                    <div class="p-6">
                        {{--
                        | TITRE (tronqué si trop long)
                        --}}
                        <h3 class="text-lg font-bold text-gray-900 mb-2">
                            <a href="{{ route('posts.show', $related->slug) }}" class="hover:text-indigo-600">
                                {{ $related->title }}
                            </a>
                        </h3>
                        {{--
                        | EXCERPT (résumé tronqué)
                        | Str::limit($related->excerpt, 100) : Tronque à 100 caractères
                        --}}
                        <p class="text-gray-600 text-sm">
                            {{ Str::limit($related->excerpt, 100) }}
                        </p>
                    </div>
                </div>
                @endforeach
            </div>
        </div>
        @endif

        {{--
        |----------------------------------------------------------------------
        | SECTION COMMENTAIRES
        |----------------------------------------------------------------------
        | mt-12 : Margin-top 3rem (séparation avec contenu principal)
        --}}
        <div class="mt-12">
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-8">
                {{--
                | TITRE SECTION avec compteur
                --}}
                <h2 class="text-2xl font-bold text-gray-900 mb-6">
                    💬 Commentaires ({{ $post->comments->count() }})
                </h2>

                {{--
                |----------------------------------------------------------------------
                | FORMULAIRE NOUVEAU COMMENTAIRE (Public, pas d'auth requise)
                |----------------------------------------------------------------------
                | bg-gray-50 : Fond gris très clair (distingue formulaire du reste)
                | p-6 : Padding 1.5rem
                | rounded-lg : Bordures arrondies 0.5rem
                --}}
                <div class="mb-8 bg-gray-50 p-6 rounded-lg">
                    <h3 class="text-lg font-bold text-gray-900 mb-4">Laisser un commentaire</h3>
                    
                    {{--
                    | FORMULAIRE POST vers route comments.store
                    | route('comments.store', $post) : Génère /posts/{id}/comments
                    | $post passé comme paramètre pour récupérer post_id dans contrôleur
                    --}}
                    <form action="{{ route('comments.store', $post) }}" method="POST">
                        @csrf
                        
                        {{--
                        | CHAMP NOM
                        | for="author_name" : Associe label au champ (clic label = focus input)
                        | id="author_name" : Identifiant unique (requis pour label + erreurs)
                        | name="author_name" : Nom du champ (clé dans $_POST)
                        | value="{{ old('author_name') }}" : Récupère ancienne valeur si erreur validation
                        | required : Attribut HTML5 (validation navigateur, backup validation serveur)
                        --}}
                        <div class="mb-4">
                            <label for="author_name" class="block text-sm font-medium text-gray-700 mb-2">
                                Nom *
                            </label>
                            <input type="text" 
                                   name="author_name" 
                                   id="author_name" 
                                   value="{{ old('author_name') }}"
                                   class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                   required>
                            {{--
                            | AFFICHAGE ERREUR VALIDATION
                            | @error('author_name') : Directive Blade pour erreurs validation
                            | Équivaut à : if ($errors->has('author_name'))
                            | $message : Variable automatique contenant message d'erreur
                            | Défini dans contrôleur via validate() ou règles FormRequest
                            --}}
                            @error('author_name')
                                <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                            @enderror
                        </div>

                        {{--
                        | CHAMP EMAIL
                        | type="email" : Validation HTML5 format email
                        --}}
                        <div class="mb-4">
                            <label for="author_email" class="block text-sm font-medium text-gray-700 mb-2">
                                Email *
                            </label>
                            <input type="email" 
                                   name="author_email" 
                                   id="author_email" 
                                   value="{{ old('author_email') }}"
                                   class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                   required>
                            @error('author_email')
                                <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                            @enderror
                        </div>

                        {{--
                        | CHAMP COMMENTAIRE (Textarea)
                        | rows="4" : Hauteur initiale 4 lignes
                        | {{ old('content') }} : Entre balises textarea (pas value="")
                        --}}
                        <div class="mb-4">
                            <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                                Commentaire *
                            </label>
                            <textarea name="content" 
                                      id="content" 
                                      rows="4"
                                      class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                      required>{{ old('content') }}</textarea>
                            @error('content')
                                <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                            @enderror
                        </div>

                        {{--
                        | BOUTON SOUMETTRE
                        --}}
                        <button type="submit" 
                                class="inline-flex items-center px-4 py-2 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-indigo-700">
                            Publier le commentaire
                        </button>
                    </form>
                </div>

                {{--
                |----------------------------------------------------------------------
                | LISTE DES COMMENTAIRES APPROUVÉS
                |----------------------------------------------------------------------
                | @if($post->comments->count() > 0) : Affiche si au moins 1 commentaire
                --}}
                @if($post->comments->count() > 0)
                <div class="space-y-6">
                    {{--
                    | BOUCLE SUR COMMENTAIRES
                    | $post->comments : Collection déjà filtrée (approved only) via Eager Loading
                    --}}
                    @foreach($post->comments as $comment)
                    <div class="border-b border-gray-200 pb-6 last:border-0">
                        {{--
                        | HEADER COMMENTAIRE (Auteur + Date + Actions)
                        | justify-between : Espace entre header gauche et actions droite
                        --}}
                        <div class="flex items-start justify-between mb-2">
                            <div>
                                {{--
                                | NOM AUTEUR COMMENTAIRE
                                | font-bold : Graisse 700
                                --}}
                                <span class="font-bold text-gray-900">{{ $comment->author_name }}</span>
                                {{--
                                | DATE COMMENTAIRE (format relatif)
                                | $comment->created_at : Carbon instance
                                | diffForHumans() : "il y a 2 heures", "il y a 3 jours"
                                --}}
                                <span class="text-sm text-gray-500 ml-2">
                                    {{ $comment->created_at->diffForHumans() }}
                                </span>
                                
                                {{--
                                | BADGE "EN ATTENTE" (seulement si non approuvé)
                                | Ce cas arrive si l'auteur de l'article consulte la page
                                | Les visiteurs ne voient PAS ces commentaires (filtrés)
                                --}}
                                @if(!$comment->approved)
                                <span class="ml-2 px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded">
                                    En attente de modération
                                </span>
                                @endif
                            </div>

                            {{--
                            | ACTIONS MODÉRATION (Approuver + Supprimer)
                            | Visibles SEULEMENT par l'auteur de l'article
                            --}}
                            @auth
                            @if(auth()->id() === $post->user_id)
                            <div class="flex gap-2">
                                {{--
                                | BOUTON APPROUVER (seulement si non approuvé)
                                | @if(!$comment->approved) : Double vérification
                                | (normalement les commentaires approuvés ne devraient pas avoir ce bouton)
                                --}}
                                @if(!$comment->approved)
                                <form action="{{ route('comments.approve', $comment) }}" method="POST">
                                    @csrf
                                    {{--
                                    | @method('PATCH') : Requête PATCH pour modification partielle
                                    | Sémantique REST : PATCH = mise à jour partielle (ici approved = true)
                                    | Alternative : POST (fonctionne aussi mais moins sémantique)
                                    --}}
                                    @method('PATCH')
                                    <button type="submit" 
                                            class="text-xs text-green-600 hover:text-green-800">
                                        ✓ Approuver
                                    </button>
                                </form>
                                @endif
                                
                                {{--
                                | BOUTON SUPPRIMER (avec confirmation)
                                --}}
                                <form action="{{ route('comments.destroy', $comment) }}" method="POST"
                                      onsubmit="return confirm('Supprimer ce commentaire ?');">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" 
                                            class="text-xs text-red-600 hover:text-red-800">
                                        ✗ Supprimer
                                    </button>
                                </form>
                            </div>
                            @endif
                            @endauth
                        </div>
                        
                        {{--
                        | CONTENU COMMENTAIRE
                        | {{ $comment->content }} : Échappement auto HTML (sécurité)
                        --}}
                        <p class="text-gray-700">{{ $comment->content }}</p>
                    </div>
                    @endforeach
                </div>
                
                {{--
                | MESSAGE ÉTAT VIDE (si aucun commentaire)
                | @else : Alternative au @if
                --}}
                @else
                <p class="text-gray-600 text-center py-8">Soyez le premier à commenter cet article !</p>
                @endif

            </div>
        </div>

    </div>
</div>
@endsection
```

<small>**Explication nl2br() + e() + {!! !!} :** Cette combinaison résout un problème de sécurité courant. Si vous utilisez `{!! $post->content !!}` directement, un utilisateur malveillant pourrait injecter `<script>alert('XSS')</script>` dans son article. En utilisant `e($post->content)`, Laravel échappe le HTML : `&lt;script&gt;alert('XSS')&lt;/script&gt;` (affiché comme texte brut). Ensuite, `nl2br()` convertit les sauts de ligne `\n` en balises `<br>`. Enfin, `{!! !!}` affiche le résultat avec les `<br>` fonctionnels mais les autres tags HTML échappés. **Helper old() :** Après échec validation, Laravel redirige vers le formulaire avec erreurs + anciennes valeurs en session. `old('author_name')` récupère la valeur soumise pour pré-remplir le champ. Évite à l'utilisateur de tout retaper. **Directive @error :** Raccourci pour `@if($errors->has('field'))`. Laravel stocke les erreurs de validation dans un objet `$errors` (instance de `ViewErrorBag`) automatiquement disponible dans toutes les vues. **Confirmation JavaScript :** `confirm()` est une fonction native navigateur qui affiche popup modale avec "OK" et "Annuler". Retourne `true` si OK, `false` si Annuler. En retournant la valeur avec `return confirm(...)`, on annule la soumission si utilisateur clique Annuler.</small>

### Étape 6.4 : Créer le Formulaire de Création d'Article

**Contexte de l'étape :**

> Le formulaire de création est l'**interface d'édition** pour les auteurs. Il doit être :

> - **Intuitif** : Labels clairs, placeholders, aide contextuelle
- **Robuste** : Validation côté client (HTML5) + serveur (Laravel)
- **Accessible** : Association label/input, messages d'erreur, navigation clavier

!!! quote "Ce formulaire utilise des **champs contrôlés** : les valeurs sont récupérées via `old()` après échec validation pour éviter de perdre le travail de l'utilisateur."

**Variables disponibles dans la vue :**

Rappel du contrôleur `PostController::create()` :

```php
return view('posts.create', compact('categories'));
```

- `$categories` : Collection de toutes les catégories (pour select dropdown)

**Créer le fichier `resources/views/posts/create.blade.php` :**

```html
{{--
|------------------------------------------------------------------------------
| FORMULAIRE CRÉATION ARTICLE
|------------------------------------------------------------------------------
| Accessible uniquement aux utilisateurs authentifiés (middleware auth dans routes)
--}}
@extends('layouts.app')

@section('title', 'Nouvel Article')

@section('content')
<div class="py-12">
    {{--
    | CONTENEUR FORMULAIRE (largeur moyenne)
    | max-w-3xl : Largeur max 48rem (768px)
    | Plus étroit que conteneur article pour meilleure concentration
    --}}
    <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
        
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-8">
                {{--
                | TITRE PAGE
                | ✏️ : Emoji unicode pour cohérence visuelle
                --}}
                <h1 class="text-3xl font-bold text-gray-900 mb-6">✏️ Créer un Nouvel Article</h1>

                {{--
                | FORMULAIRE POST vers route posts.store
                | action="{{ route('posts.store') }}" : Génère URL /posts
                | method="POST" : Méthode HTTP POST
                | Pas de enctype car pas d'upload fichier (seulement URL image)
                --}}
                <form action="{{ route('posts.store') }}" method="POST">
                    {{--
                    | @csrf : Token CSRF obligatoire
                    | Sans lui, Laravel rejette la requête avec erreur 419
                    --}}
                    @csrf

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP TITRE
                    |------------------------------------------------------------------
                    | mb-6 : Margin-bottom 1.5rem (espacement entre champs)
                    --}}
                    <div class="mb-6">
                        {{--
                        | LABEL
                        | block : Force affichage en bloc (occupe ligne complète)
                        | text-sm : Taille texte 0.875rem
                        | mb-2 : Margin-bottom 0.5rem (espace label-input)
                        --}}
                        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
                            Titre *
                        </label>
                        {{--
                        | INPUT TEXT
                        | type="text" : Champ texte simple (pas de validation HTML5 spéciale)
                        | name="title" : Clé dans $_POST et règles validation
                        | id="title" : Identifiant unique (associé au label, ciblé par @error)
                        | value="{{ old('title') }}" : Récupère ancienne valeur si erreur
                        | w-full : Largeur 100% (occupe tout le conteneur parent)
                        | rounded-md : Bordures arrondies 0.375rem
                        | border-gray-300 : Bordure grise par défaut
                        | shadow-sm : Ombre légère (profondeur visuelle)
                        | focus:border-indigo-500 : Bordure indigo au focus (clavier/souris)
                        | focus:ring-indigo-500 : Anneau indigo au focus (accessibilité)
                        | required : Attribut HTML5 (validation navigateur)
                        --}}
                        <input type="text" 
                               name="title" 
                               id="title" 
                               value="{{ old('title') }}"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        {{--
                        | AFFICHAGE ERREUR VALIDATION
                        | @error('title') : Vérifie si erreur existe pour champ 'title'
                        | $message : Variable auto contenant message défini dans contrôleur
                        | text-red-600 : Couleur rouge pour erreur
                        | mt-1 : Margin-top 0.25rem (espace input-erreur)
                        --}}
                        @error('title')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CATÉGORIE (Select Dropdown)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="category_id" class="block text-sm font-medium text-gray-700 mb-2">
                            Catégorie *
                        </label>
                        {{--
                        | SELECT
                        | <select> : Menu déroulant HTML
                        | name="category_id" : Clé dans $_POST (contiendra l'ID sélectionné)
                        --}}
                        <select name="category_id" 
                                id="category_id"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                required>
                            {{--
                            | OPTION PAR DÉFAUT (vide)
                            | value="" : Valeur vide (échoue validation required)
                            | Force l'utilisateur à choisir une catégorie
                            --}}
                            <option value="">Sélectionner une catégorie</option>
                            {{--
                            | BOUCLE SUR CATÉGORIES
                            | @foreach($categories as $category) : Itère sur Collection
                            --}}
                            @foreach($categories as $category)
                            {{--
                            | OPTION CATÉGORIE
                            | value="{{ $category->id }}" : ID envoyé au serveur
                            | {{ old('category_id') == $category->id ? 'selected' : '' }}
                            | Ternaire pour pré-sélectionner si erreur validation :
                            | - Si old('category_id') existe et = $category->id → 'selected'
                            | - Sinon → chaîne vide (pas de selected)
                            | L'attribut selected rend l'option pré-sélectionnée visuellement
                            --}}
                            <option value="{{ $category->id }}" {{ old('category_id') == $category->id ? 'selected' : '' }}>
                                {{ $category->name }}
                            </option>
                            @endforeach
                        </select>
                        @error('category_id')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP RÉSUMÉ (Textarea)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="excerpt" class="block text-sm font-medium text-gray-700 mb-2">
                            {{--
                            | <span> : Balise inline pour aide contextuelle
                            | text-gray-500 : Couleur grise (moins importante que label)
                            | text-xs : Taille texte 0.75rem (12px)
                            --}}
                            Résumé * <span class="text-gray-500 text-xs">(max 500 caractères)</span>
                        </label>
                        {{--
                        | TEXTAREA
                        | <textarea> : Champ multiligne
                        | rows="3" : Hauteur initiale 3 lignes (extensible par utilisateur)
                        | maxlength="500" : Limite HTML5 (500 caractères max)
                        | Empêche saisie au-delà (feedback immédiat pour utilisateur)
                        | {{ old('excerpt') }} : Entre balises textarea (PAS value="")
                        | Syntaxe correcte : <textarea>{{ old('excerpt') }}</textarea>
                        | Syntaxe incorrecte : <textarea value="{{ old('excerpt') }}"></textarea>
                        --}}
                        <textarea name="excerpt" 
                                  id="excerpt" 
                                  rows="3"
                                  maxlength="500"
                                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                  required>{{ old('excerpt') }}</textarea>
                        @error('excerpt')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CONTENU (Textarea Grande)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                            Contenu * <span class="text-gray-500 text-xs">(min 100 caractères)</span>
                        </label>
                        {{--
                        | TEXTAREA CONTENU PRINCIPAL
                        | rows="15" : Hauteur initiale 15 lignes (grande zone édition)
                        | Pas de maxlength (contenu peut être long)
                        | Validation min 100 caractères côté serveur (dans contrôleur)
                        --}}
                        <textarea name="content" 
                                  id="content" 
                                  rows="15"
                                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                  required>{{ old('content') }}</textarea>
                        @error('content')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP IMAGE URL (Optionnel)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="image" class="block text-sm font-medium text-gray-700 mb-2">
                            URL Image de couverture (optionnel)
                        </label>
                        {{--
                        | INPUT URL
                        | type="url" : Validation HTML5 format URL (http:// ou https://)
                        | placeholder : Texte d'exemple (disparaît au focus)
                        | Pas required (image optionnelle)
                        --}}
                        <input type="url" 
                               name="image" 
                               id="image" 
                               value="{{ old('image') }}"
                               placeholder="https://exemple.com/image.jpg"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                        @error('image')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                        {{--
                        | AIDE CONTEXTUELLE
                        | <p> : Paragraphe d'aide sous le champ
                        | <a target="_blank"> : Ouvre lien dans nouvel onglet
                        --}}
                        <p class="text-xs text-gray-500 mt-1">
                            Vous pouvez utiliser des services comme <a href="https://unsplash.com" target="_blank" class="text-indigo-600">Unsplash</a>
                        </p>
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP STATUT (Radio Buttons)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Statut *
                        </label>
                        {{--
                        | GROUPE RADIO BUTTONS
                        | space-y-2 : Espacement vertical 0.5rem entre options
                        --}}
                        <div class="space-y-2">
                            {{--
                            | OPTION 1 : BROUILLON (défaut)
                            | <label> conteneur : Toute la zone est cliquable
                            | inline-flex items-center : Aligne radio + texte horizontalement
                            --}}
                            <label class="inline-flex items-center">
                                {{--
                                | INPUT RADIO
                                | type="radio" : Bouton radio (un seul sélectionnable par groupe)
                                | name="status" : Même name pour toutes options (groupe radio)
                                | value="draft" : Valeur envoyée si sélectionné
                                | {{ old('status', 'draft') === 'draft' ? 'checked' : '' }}
                                | Ternaire avec valeur par défaut :
                                | - old('status', 'draft') : Récupère old OU 'draft' si inexistant
                                | - === 'draft' ? 'checked' : '' : Ajoute attribut checked si match
                                | Résultat : "Brouillon" coché par défaut au premier affichage
                                | rounded-full : Radio circulaire (au lieu de carré par défaut navigateur)
                                --}}
                                <input type="radio" 
                                       name="status" 
                                       value="draft" 
                                       {{ old('status', 'draft') === 'draft' ? 'checked' : '' }}
                                       class="rounded-full border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                {{--
                                | LABEL TEXTE
                                | ml-2 : Margin-left 0.5rem (espace entre radio et texte)
                                --}}
                                <span class="ml-2">Brouillon (visible seulement par vous)</span>
                            </label>
                            {{--
                            | <br> : Saut de ligne HTML (force retour à la ligne)
                            | Alternative : Supprimer <br> et utiliser flex-col sur conteneur parent
                            --}}
                            <br>
                            {{--
                            | OPTION 2 : PUBLIÉ
                            --}}
                            <label class="inline-flex items-center">
                                <input type="radio" 
                                       name="status" 
                                       value="published" 
                                       {{ old('status') === 'published' ? 'checked' : '' }}
                                       class="rounded-full border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                <span class="ml-2">Publier immédiatement</span>
                            </label>
                        </div>
                        @error('status')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | BOUTONS ACTIONS (Retour + Soumettre)
                    |------------------------------------------------------------------
                    | flex justify-between : Répartit espace entre 2 éléments
                    | items-center : Alignement vertical centré
                    --}}
                    <div class="flex items-center justify-between">
                        {{--
                        | LIEN RETOUR
                        | Pas un bouton <button> car c'est une navigation (lien <a>)
                        | hover:text-gray-900 : Couleur plus foncée au survol
                        --}}
                        <a href="{{ route('dashboard') }}" 
                           class="text-gray-600 hover:text-gray-900">
                            ← Retour au dashboard
                        </a>
                        
                        {{--
                        | BOUTON SOUMETTRE
                        | type="submit" : Soumet le formulaire au clic
                        | px-6 py-3 : Padding généreux (bouton principal)
                        | uppercase tracking-widest : Style moderne (lettres capitales espacées)
                        --}}
                        <button type="submit" 
                                class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                            Créer l'article
                        </button>
                    </div>

                </form>
            </div>
        </div>

    </div>
</div>
@endsection
```

<small>**Explication old() avec valeur par défaut :** `old('status', 'draft')` utilise la syntaxe `old($key, $default)`. Si la session contient `old('status')` (après erreur validation), retourne cette valeur. Sinon, retourne `'draft'`. Permet de pré-cocher "Brouillon" au premier affichage, puis pré-cocher la valeur soumise si erreur. **Radio buttons et name :** Tous les radio buttons d'un groupe doivent avoir le même `name`. Le navigateur garantit qu'un seul peut être sélectionné. La `value` du radio sélectionné est envoyée dans `$_POST['status']`. **Validation HTML5 vs Laravel :** Les attributs `required`, `maxlength`, `type="email"` assurent une première validation côté client (immédiate, sans requête serveur). Mais un utilisateur malveillant peut désactiver JavaScript ou modifier le HTML. Laravel DOIT TOUJOURS valider côté serveur via `$request->validate()`. **Textarea value vs contenu :** `<textarea value="...">` est invalide en HTML. La syntaxe correcte est `<textarea>contenu ici</textarea>`. C'est pourquoi `{{ old('content') }}` est entre les balises.</small>

### Étape 6.5 : Créer le Formulaire d'Édition d'Article

**Contexte de l'étape :**

> Le formulaire d'édition est **quasi-identique** au formulaire de création, avec quelques différences cruciales :

> 1. **Pré-remplissage** : Les champs affichent les valeurs actuelles de l'article (`$post->title`, `$post->content`, etc.)
2. **Route et méthode** : POST vers `/posts/{id}` avec spoofing PUT (RESTful update)
3. **Validation ownership** : Vérifiée dans le contrôleur (seul l'auteur peut modifier)
4. **Fallback old()** : `old('title', $post->title)` affiche la valeur soumise si erreur, sinon la valeur BDD

!!! info "**Pourquoi ne pas réutiliser create.blade.php ?**"

    Bien que les deux formulaires soient similaires, les séparer offre plusieurs avantages :

    - **Clarté** : Chaque vue a une responsabilité unique (SRP - Single Responsibility Principle)
    - **Flexibilité** : Vous pouvez ajouter des champs spécifiques à l'édition (ex: "Dernière modification le...")
    - **Maintenance** : Modifier l'un n'affecte pas l'autre
    - **Sémantique** : Routes RESTful distinctes (POST /posts vs PUT /posts/{id})

!!! note "**Alternative avancée (futur) :** Créer un composant Blade `<x-post-form>` réutilisable avec paramètres (`action`, `method`, `post`). Pour ce tutoriel, on privilégie la simplicité."

**Variables disponibles dans la vue :**

Rappel du contrôleur `PostController::edit()` :

```php
return view('posts.edit', compact('post', 'categories'));
```

- `$post` : Instance Post à modifier (injectée automatiquement via Route Model Binding)
- `$categories` : Collection de toutes les catégories (pour select dropdown)

**Créer le fichier `resources/views/posts/edit.blade.php` :**

```html
{{--
|------------------------------------------------------------------------------
| FORMULAIRE ÉDITION ARTICLE
|------------------------------------------------------------------------------
| Accessible uniquement à l'auteur de l'article (vérifié dans contrôleur)
| Quasi-identique à create.blade.php avec pré-remplissage des valeurs
--}}
@extends('layouts.app')

{{--
| TITRE DYNAMIQUE
| Utilise une apostrophe échappée : \'
| Alternative : @section('title', "Modifier l'article")
--}}
@section('title', 'Modifier l\'article')

@section('content')
<div class="py-12">
    <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
        
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-6">✏️ Modifier l'Article</h1>

                {{--
                |----------------------------------------------------------------------
                | FORMULAIRE PUT vers route posts.update
                |----------------------------------------------------------------------
                | DIFFÉRENCE MAJEURE avec create.blade.php :
                | - action : route('posts.update', $post) génère /posts/{id}
                | - method : POST (car HTML ne supporte que GET/POST)
                | - @method('PUT') : Spoofing pour Laravel (converti en vraie requête PUT)
                |
                | Pourquoi PUT et pas POST ?
                | Convention REST :
                | - POST /posts : Créer une nouvelle ressource
                | - PUT /posts/{id} : Remplacer entièrement une ressource existante
                | - PATCH /posts/{id} : Modifier partiellement une ressource
                |
                | Laravel accepte PUT/PATCH grâce au champ _method caché
                --}}
                <form action="{{ route('posts.update', $post) }}" method="POST">
                    @csrf
                    {{--
                    | @method('PUT') : Génère <input type="hidden" name="_method" value="PUT">
                    | Laravel détecte ce champ et traite la requête comme PUT côté serveur
                    | Alternative : @method('PATCH') fonctionne aussi (sémantiquement différent)
                    --}}
                    @method('PUT')

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP TITRE (Pré-rempli)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
                            Titre *
                        </label>
                        {{--
                        | PRÉ-REMPLISSAGE AVEC FALLBACK
                        | value="{{ old('title', $post->title) }}"
                        |
                        | Logique :
                        | 1. Si erreur validation → old('title') existe → affiche valeur soumise
                        | 2. Sinon → old('title') null → utilise fallback $post->title
                        |
                        | Exemple scénario :
                        | - Utilisateur modifie titre : "Mon Article" → "Mon Nouvel Article"
                        | - Soumission formulaire avec content < 100 caractères (erreur)
                        | - Laravel redirige vers edit avec old('title') = "Mon Nouvel Article"
                        | - Le champ affiche "Mon Nouvel Article" (pas "Mon Article" de la BDD)
                        | - L'utilisateur corrige content sans perdre sa modification de titre
                        |
                        | Sans old() :
                        | - Le champ afficherait "Mon Article" (BDD) après erreur
                        | - L'utilisateur perdrait sa modification "Mon Nouvel Article"
                        --}}
                        <input type="text" 
                               name="title" 
                               id="title" 
                               value="{{ old('title', $post->title) }}"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        @error('title')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CATÉGORIE (Pré-sélectionné)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="category_id" class="block text-sm font-medium text-gray-700 mb-2">
                            Catégorie *
                        </label>
                        <select name="category_id" 
                                id="category_id"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                required>
                            {{--
                            | BOUCLE SUR CATÉGORIES
                            | Pas d'option vide car catégorie déjà sélectionnée
                            --}}
                            @foreach($categories as $category)
                            {{--
                            | PRÉ-SÉLECTION DE LA CATÉGORIE ACTUELLE
                            | old('category_id', $post->category_id) == $category->id
                            |
                            | Logique :
                            | 1. Si erreur validation → compare old('category_id') avec $category->id
                            | 2. Sinon → compare $post->category_id avec $category->id
                            |
                            | Exemple scénario article Technologie (id=1) :
                            | - Premier affichage : $post->category_id = 1
                            |   → Option id=1 a selected="selected"
                            | - Utilisateur change pour Voyage (id=2)
                            | - Erreur validation titre vide
                            | - Retour formulaire : old('category_id') = 2
                            |   → Option id=2 a selected="selected"
                            |
                            | Note : == et non === car comparaison string (old) vs int (BDD)
                            | old('category_id') retourne string "1"
                            | $post->category_id est int 1
                            | "1" == 1 → true (coercition type PHP)
                            | "1" === 1 → false (types différents)
                            --}}
                            <option value="{{ $category->id }}" 
                                    {{ old('category_id', $post->category_id) == $category->id ? 'selected' : '' }}>
                                {{ $category->name }}
                            </option>
                            @endforeach
                        </select>
                        @error('category_id')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP RÉSUMÉ (Pré-rempli)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="excerpt" class="block text-sm font-medium text-gray-700 mb-2">
                            Résumé * <span class="text-gray-500 text-xs">(max 500 caractères)</span>
                        </label>
                        {{--
                        | PRÉ-REMPLISSAGE TEXTAREA
                        | {{ old('excerpt', $post->excerpt) }} : Entre balises textarea
                        | ATTENTION : Pas de value="" sur textarea (invalide HTML)
                        |
                        | Syntaxe correcte :
                        | <textarea>{{ $contenu }}</textarea>
                        |
                        | Syntaxe incorrecte :
                        | <textarea value="{{ $contenu }}"></textarea>
                        |
                        | Explication : <textarea> est un élément de contenu, pas un input void
                        | Son contenu initial est défini entre balises ouvrante/fermante
                        --}}
                        <textarea name="excerpt" 
                                  id="excerpt" 
                                  rows="3"
                                  maxlength="500"
                                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                  required>{{ old('excerpt', $post->excerpt) }}</textarea>
                        @error('excerpt')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CONTENU (Pré-rempli)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                            Contenu * <span class="text-gray-500 text-xs">(min 100 caractères)</span>
                        </label>
                        {{--
                        | PRÉ-REMPLISSAGE CONTENU PRINCIPAL
                        | {{ old('content', $post->content) }}
                        |
                        | Note sur l'échappement :
                        | {{ }} échappe automatiquement le HTML
                        | Si $post->content contient "<script>alert('XSS')</script>"
                        | L'affichage dans textarea sera : &lt;script&gt;alert('XSS')&lt;/script&gt;
                        | L'utilisateur voit le texte brut dans le formulaire (correct)
                        |
                        | Pourquoi c'est safe :
                        | Le textarea affiche du texte brut, pas du HTML interprété
                        | Même si l'échappement produit des entités HTML (&lt; &gt;)
                        | Le textarea les affiche littéralement à l'utilisateur
                        | Quand l'utilisateur soumet, les entités sont converties en caractères
                        --}}
                        <textarea name="content" 
                                  id="content" 
                                  rows="15"
                                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                  required>{{ old('content', $post->content) }}</textarea>
                        @error('content')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP IMAGE URL (Pré-rempli)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="image" class="block text-sm font-medium text-gray-700 mb-2">
                            URL Image de couverture (optionnel)
                        </label>
                        {{--
                        | PRÉ-REMPLISSAGE URL IMAGE
                        | old('image', $post->image) : Peut être null si image optionnelle
                        | Si $post->image === null → champ vide
                        | Si $post->image = "https://..." → champ pré-rempli
                        --}}
                        <input type="url" 
                               name="image" 
                               id="image" 
                               value="{{ old('image', $post->image) }}"
                               placeholder="https://exemple.com/image.jpg"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                        @error('image')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP STATUT (Radio Buttons Pré-cochés)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Statut *
                        </label>
                        <div class="space-y-2">
                            {{--
                            | OPTION 1 : BROUILLON
                            | old('status', $post->status) === 'draft' ? 'checked' : ''
                            |
                            | Logique :
                            | 1. Si erreur validation → utilise old('status')
                            | 2. Sinon → utilise $post->status (valeur BDD actuelle)
                            | 3. Si valeur === 'draft' → ajoute attribut checked
                            |
                            | Exemple scénario article PUBLIÉ :
                            | - Premier affichage : $post->status = 'published'
                            |   → "Publié" coché, "Brouillon" décoché
                            | - Utilisateur change pour "Brouillon"
                            | - Erreur validation titre vide
                            | - Retour formulaire : old('status') = 'draft'
                            |   → "Brouillon" coché
                            --}}
                            <label class="inline-flex items-center">
                                <input type="radio" 
                                       name="status" 
                                       value="draft" 
                                       {{ old('status', $post->status) === 'draft' ? 'checked' : '' }}
                                       class="rounded-full border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                <span class="ml-2">Brouillon</span>
                            </label>
                            <br>
                            {{--
                            | OPTION 2 : PUBLIÉ
                            --}}
                            <label class="inline-flex items-center">
                                <input type="radio" 
                                       name="status" 
                                       value="published" 
                                       {{ old('status', $post->status) === 'published' ? 'checked' : '' }}
                                       class="rounded-full border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                                <span class="ml-2">Publié</span>
                            </label>
                        </div>
                        @error('status')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | BOUTONS ACTIONS (Annuler + Mettre à jour)
                    |------------------------------------------------------------------
                    | DIFFÉRENCE avec create.blade.php :
                    | - Lien retour vers posts.show (pas dashboard)
                    | - Texte bouton "Mettre à jour" (pas "Créer")
                    --}}
                    <div class="flex items-center justify-between">
                        {{--
                        | LIEN ANNULER
                        | route('posts.show', $post) : Retour vers page article
                        | Génère : /posts/{slug}
                        |
                        | Pourquoi posts.show et pas dashboard ?
                        | - L'utilisateur vient probablement de consulter l'article
                        | - Bouton "Modifier" sur posts.show → edit → Annuler → retour posts.show
                        | - Cohérence UX : Annuler ramène à la page précédente
                        |
                        | Alternative : route('dashboard') si besoin différent
                        --}}
                        <a href="{{ route('posts.show', $post) }}" 
                           class="text-gray-600 hover:text-gray-900">
                            ← Annuler
                        </a>
                        
                        {{--
                        | BOUTON SOUMETTRE (Mettre à jour)
                        | type="submit" : Soumet le formulaire
                        | Action : POST /posts/{id} + _method=PUT
                        | Traité par Laravel comme : PUT /posts/{id}
                        | Route : Route::put('/posts/{post}', [PostController::class, 'update'])
                        | Contrôleur : PostController::update($request, $post)
                        --}}
                        <button type="submit" 
                                class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                            Mettre à jour
                        </button>
                    </div>

                </form>
            </div>
        </div>

    </div>
</div>
@endsection
```

**Tableau Comparatif create.blade.php vs edit.blade.php**

| Aspect | create.blade.php | edit.blade.php | Raison |
|--------|------------------|----------------|--------|
| **Route action** | `route('posts.store')` → `/posts` | `route('posts.update', $post)` → `/posts/{id}` | RESTful convention |
| **Méthode HTTP** | POST | POST + `@method('PUT')` | HTML supporte seulement GET/POST |
| **Pré-remplissage** | `old('title')` | `old('title', $post->title)` | Affiche valeurs BDD existantes |
| **Valeur par défaut** | `old('status', 'draft')` | `old('status', $post->status)` | Statut actuel pas "draft" forcément |
| **Lien retour** | `route('dashboard')` | `route('posts.show', $post)` | Cohérence navigation |
| **Texte bouton** | "Créer l'article" | "Mettre à jour" | Clarté action |
| **Titre page** | "Créer un Nouvel Article" | "Modifier l'Article" | Contexte utilisateur |
| **Select catégorie** | Option vide par défaut | Catégorie actuelle pré-sélectionnée | UX différente |

**Explications Techniques Approfondies**

??? abstract "**1. Pourquoi @method('PUT') ?**"

    HTML ne supporte **nativement** que deux méthodes dans `<form method="">` :

    - GET : Récupération de données (navigation, recherche)
    - POST : Soumission de données (création, modification)

    Les méthodes RESTful supplémentaires (PUT, PATCH, DELETE) sont utilisées par les APIs et frameworks modernes mais **non supportées** par HTML classique.

    **Solution Laravel :**

    Laravel utilise le **method spoofing** : un champ caché `_method` indique la vraie méthode souhaitée.

    ```blade
    <form method="POST">
        @method('PUT')
        <!-- Génère : <input type="hidden" name="_method" value="PUT"> -->
    </form>
    ```

    Côté serveur, Laravel détecte ce champ et **route la requête** vers la bonne méthode du contrôleur :

    ```php
    // routes/web.php
    Route::put('/posts/{post}', [PostController::class, 'update']);
    ```

    **Alternative sans spoofing (moins propre) :**

    ```php
    // routes/web.php
    Route::post('/posts/{post}/update', [PostController::class, 'update']);
    ```

    Mais cela viole les conventions REST et rend les routes moins sémantiques.

??? abstract "**2. Différence == vs === pour comparaisons**"

    PHP a deux opérateurs de comparaison :

    - **==** : Égalité avec **coercition de type** (conversion automatique)
    - **===** : Égalité **stricte** (même valeur ET même type)

    **Exemples :**

    ```php
    "1" == 1    // true  (string converti en int)
    "1" === 1   // false (string ≠ int)

    null == false   // true  (null = faux en booléen)
    null === false  // false (null ≠ bool)

    0 == "hello"   // true  (string non-numérique = 0)
    0 === "hello"  // false (int ≠ string)
    ```

    **Dans les formulaires Laravel :**

    ```blade
    {{ old('category_id', $post->category_id) == $category->id ? 'selected' : '' }}
    ```

    - `old('category_id')` retourne une **string** : `"1"`
    - `$post->category_id` est un **int** : `1`
    - `$category->id` est un **int** : `1`

    **Pourquoi == et pas === ?**

    - `old('category_id')` peut être string `"1"` (récupéré de $_POST)
    - `$post->category_id` est int `1` (récupéré de BDD)
    - `"1" === 1` → `false` → option pas sélectionnée (BUG)
    - `"1" == 1` → `true` → option sélectionnée (CORRECT)

    **Bonne pratique générale :**

    Préférez `===` par défaut pour éviter bugs subtils. Utilisez `==` seulement quand coercition nécessaire (formulaires, comparaisons lâches).

??? abstract "**3. Pourquoi séparer create et edit au lieu d'un formulaire unique ?**"

    **Arguments pour UN formulaire unique :**

    ✅ Moins de duplication code (DRY - Don't Repeat Yourself)  
    ✅ Maintenance simplifiée (un seul endroit à modifier)

    **Arguments pour DEUX formulaires séparés :**

    ✅ **Clarté** : Chaque vue a une responsabilité unique (SRP)  
    ✅ **Flexibilité** : Ajouter champs spécifiques sans conditions complexes  
    ✅ **Lisibilité** : Pas de `@if($post->exists)` partout  
    ✅ **Sémantique** : Routes RESTful distinctes (POST vs PUT)  
    ✅ **Testabilité** : Tests séparés pour création vs édition  

    **Exemple de complexité avec formulaire unique :**

    ```html
    {{-- Formulaire unique (complexe) --}}
    <form action="{{ $post->exists ? route('posts.update', $post) : route('posts.store') }}" method="POST">
        @csrf
        @if($post->exists)
            @method('PUT')
        @endif
        
        <input value="{{ old('title', $post->title ?? '') }}">
        
        @if($post->exists)
            <p>Dernière modification : {{ $post->updated_at }}</p>
        @endif
    </form>
    ```

    Vs formulaires séparés (simple) :

    ```html
    {{-- create.blade.php --}}
    <form action="{{ route('posts.store') }}" method="POST">
        <input value="{{ old('title') }}">
    </form>

    {{-- edit.blade.php --}}
    <form action="{{ route('posts.update', $post) }}" method="POST">
        @method('PUT')
        <input value="{{ old('title', $post->title) }}">
    </form>
    ```

    **Recommandation Laravel :**

    Pour formulaires simples (3-5 champs) : formulaire unique acceptable  
    Pour formulaires complexes (10+ champs, logique conditionnelle) : formulaires séparés préférables

??? abstract "**4. Comportement de old() avec fallback**"

    `old($key, $default)` suit cette logique :

    1. Vérifie si session contient `old($key)` (données flash après erreur validation)
    2. Si oui → retourne `old($key)`
    3. Si non → retourne `$default`

    **Scénario complet :**

    ```php
    // 1. Premier affichage (GET /posts/1/edit)
    old('title', $post->title)
    // Session vide → retourne $post->title = "Mon Article"

    // 2. Utilisateur modifie : "Mon Article" → "Mon Nouvel Article"
    // 3. Soumet avec erreur (content < 100 caractères)

    // 4. Contrôleur validation échoue
    $request->validate(['content' => 'min:100']);
    // Laravel flash old input : session(['_old_input' => $_POST])
    // Contient : ['title' => 'Mon Nouvel Article', 'content' => 'Trop court']

    // 5. Redirection vers formulaire (GET /posts/1/edit)
    old('title', $post->title)
    // Session contient old('title') → retourne "Mon Nouvel Article"

    // 6. Utilisateur corrige content et soumet
    // 7. Validation réussit → Article mis à jour → Redirection posts.show
    // 8. Session old input supprimée automatiquement

    // 9. Si utilisateur retourne sur edit
    old('title', $post->title)
    // Session vide → retourne $post->title = "Mon Nouvel Article" (nouvelle valeur BDD)
    ```

    **Astuce debug :**

    ```html
    {{-- Afficher contenu session old --}}
    @php
        dd(old()); // Dump all old input
    @endphp
    ```

    <small>**Explication spoofing méthode HTTP :** Le navigateur envoie `POST /posts/1` avec `_method=PUT` dans le corps de la requête. Le middleware `ConvertEmptyStringsToNull` et `TrimStrings` traitent les données, puis `MethodOverride` détecte `_method=PUT` et modifie l'objet Request pour indiquer méthode PUT. Laravel route ensuite vers `Route::put()` correspondante. **Pourquoi REST utilise PUT/PATCH/DELETE :** Architecture RESTful utilise les méthodes HTTP comme **verbes** sur des **ressources** (URLs). Exemple : `/posts/1` est une ressource "article #1". `GET /posts/1` = lire, `PUT /posts/1` = remplacer entièrement, `PATCH /posts/1` = modifier partiellement, `DELETE /posts/1` = supprimer. Cette convention facilite conception APIs prévisibles et auto-documentées. **Fallback null vs chaîne vide :** `old('image', $post->image)` peut retourner `null` si colonne nullable. Un input `<input value="{{ null }}">` affiche `value=""` (chaîne vide). C'est correct car input vide = pas d'URL image. Alternative : `old('image', $post->image ?? '')` garantit string mais ajoute complexité inutile.</small>


✅ **Étape 6.5 Terminée !**

**Fichier créé :**
- `resources/views/posts/edit.blade.php` : Formulaire d'édition avec pré-remplissage

**Concepts maîtrisés :**

- Spoofing méthode HTTP (`@method('PUT')`)
- Fallback old() avec valeurs BDD (`old('field', $model->field)`)
- Pré-sélection select/radio avec comparaison `==`
- Différences REST entre POST (create) et PUT (update)
- Bonnes pratiques séparation create/edit

### Étape 6.6 : Créer le Dashboard Auteur (Statistiques et Gestion Articles)

**Contexte de l'étape :**

> Le dashboard est l'**espace de travail personnel** de l'auteur. C'est la première page qu'il voit après connexion (si vous configurez la redirection post-login). Cette vue centralise toutes les **informations et actions** essentielles :

!!! note "**Sections du dashboard :**"

    1. **Message de bienvenue** : Personnalisé avec nom de l'utilisateur
    2. **Statistiques en cartes** : 4 métriques clés (total, publiés, brouillons, vues totales)
    3. **Mise en avant** : Article le plus populaire (bandeau coloré)
    4. **Actions rapides** : Boutons pour créer article, voir profil public, paramètres
    5. **Liste complète** : Tableau de tous les articles avec actions (modifier/supprimer)

!!! note "**Pourquoi un dashboard plutôt qu'une simple liste ?**"

    - **Vision d'ensemble** : Statistiques instantanées sans explorer chaque page
    - **Motivation** : Compteurs de vues/commentaires encouragent la création de contenu
    - **Efficacité** : Actions rapides (créer, modifier) accessibles en 1 clic
    - **Professionnalisme** : Interface moderne type CMS (WordPress, Ghost)

!!! note "**Design patterns utilisés :**"

    - **Cards** : Cartes statistiques avec icônes et couleurs distinctives
    - **Grid responsive** : 4 colonnes desktop → 2 colonnes tablet → 1 colonne mobile
    - **Data table** : Tableau HTML classique avec actions inline
    - **Empty state** : Message encourageant si aucun article (onboarding)
    - **Gradient background** : Mise en avant visuelle article populaire

**Variables disponibles dans la vue :**

Rappel du contrôleur `DashboardController::index()` :

```php
return view('dashboard', compact('posts', 'stats', 'mostViewedPost', 'recentPosts'));
```

- `$posts` : Collection de TOUS les articles de l'auteur (publiés + brouillons)
- `$stats` : Tableau associatif avec 5 clés :
  - `total_posts` : Nombre total d'articles
  - `published_posts` : Nombre d'articles publiés
  - `draft_posts` : Nombre de brouillons
  - `total_views` : Somme de toutes les vues
  - `total_comments` : Somme de tous les commentaires
- `$mostViewedPost` : Instance Post (peut être null si aucun article publié)
- `$recentPosts` : Collection des 5 derniers articles (non utilisée dans cette version simplifiée)

**Ouvrir `resources/views/dashboard.blade.php`** (créé par Breeze) et **remplacer TOUT le contenu** par :

```html
{{--
|------------------------------------------------------------------------------
| DASHBOARD AUTEUR
|------------------------------------------------------------------------------
| Page privée accessible uniquement aux utilisateurs authentifiés
| Affiche statistiques, actions rapides et liste complète des articles
--}}
@extends('layouts.app')

@section('title', 'Mon Dashboard')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        
        {{--
        |----------------------------------------------------------------------
        | HEADER DASHBOARD (Message de Bienvenue)
        |----------------------------------------------------------------------
        | mb-8 : Margin-bottom 2rem (espacement avant statistiques)
        --}}
        <div class="mb-8">
            {{--
            | TITRE PERSONNALISÉ
            | auth()->user()->name : Nom de l'utilisateur connecté
            | Auth::user()->name fonctionne aussi (même chose)
            |
            | Exemple rendu : "👋 Bienvenue, Alice Dupont !"
            |
            | Note sur {{ }} vs {!! !!} :
            | {{ auth()->user()->name }} échappe HTML (sécurité)
            | Si name = "<script>alert('XSS')</script>"
            | Affichage : &lt;script&gt;alert('XSS')&lt;/script&gt; (texte brut)
            |
            | Alternative avancée (avatar) :
            | <img src="{{ auth()->user()->avatar }}" class="inline w-8 h-8 rounded-full">
            --}}
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
                👋 Bienvenue, {{ auth()->user()->name }} !
            </h1>
            {{--
            | SOUS-TITRE
            | text-gray-600 : Gris moyen (moins important que h1)
            --}}
            <p class="text-gray-600">Gérez vos articles et consultez vos statistiques.</p>
        </div>

        {{--
        |----------------------------------------------------------------------
        | STATISTIQUES EN CARTES (4 Colonnes Responsives)
        |----------------------------------------------------------------------
        | grid : Active CSS Grid Layout
        | grid-cols-1 : 1 colonne par défaut (mobile)
        | md:grid-cols-2 : 2 colonnes sur écrans ≥768px (tablet)
        | lg:grid-cols-4 : 4 colonnes sur écrans ≥1024px (desktop)
        | gap-6 : Espacement 1.5rem entre cartes
        | mb-8 : Margin-bottom 2rem (espace avant section suivante)
        |
        | Pourquoi cette progression responsive ?
        | Mobile (320-767px) : 1 colonne (lisibilité, défilement vertical)
        | Tablet (768-1023px) : 2 colonnes (compromis espace/lisibilité)
        | Desktop (1024+px) : 4 colonnes (vue d'ensemble maximale)
        --}}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            
            {{--
            |------------------------------------------------------------------
            | CARTE 1 : TOTAL ARTICLES
            |------------------------------------------------------------------
            | Affiche nombre total d'articles (publiés + brouillons)
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                {{--
                | CONTENU CARTE
                | p-6 : Padding 1.5rem (toutes directions)
                --}}
                <div class="p-6">
                    {{--
                    | DISPOSITION FLEX (Icône à droite)
                    | flex : Active Flexbox
                    | items-center : Alignement vertical centré
                    | justify-between : Espace maximum entre éléments
                    | Résultat : Texte gauche, icône droite
                    --}}
                    <div class="flex items-center justify-between">
                        {{--
                        | BLOC TEXTE GAUCHE
                        --}}
                        <div>
                            {{--
                            | LABEL
                            | text-sm : Taille texte 0.875rem (14px)
                            | font-medium : Graisse 500
                            | text-gray-600 : Gris moyen (secondaire)
                            --}}
                            <p class="text-sm font-medium text-gray-600">Total Articles</p>
                            {{--
                            | VALEUR STATISTIQUE
                            | text-3xl : Taille texte 1.875rem (30px)
                            | font-bold : Graisse 700 (accent visuel important)
                            | {{ $stats['total_posts'] }} : Accès tableau associatif
                            |
                            | Rappel contrôleur :
                            | $stats = ['total_posts' => $posts->count()];
                            |
                            | Exemple rendu : "7" (si 7 articles)
                            --}}
                            <p class="text-3xl font-bold text-gray-900">{{ $stats['total_posts'] }}</p>
                        </div>
                        {{--
                        | ICÔNE DÉCORATIVE (Emoji)
                        | w-12 h-12 : Largeur/hauteur 3rem (48px)
                        | bg-indigo-100 : Fond indigo clair
                        | rounded-full : Bordures arrondies 100% (cercle parfait)
                        | flex items-center justify-center : Centre emoji dans cercle
                        | text-2xl : Taille emoji 1.5rem (24px)
                        |
                        | Pourquoi emoji et pas icône SVG ?
                        | - Simplicité : Pas de fichiers externes
                        | - Unicode : Support universel navigateurs
                        | - Rapidité : Affichage instantané
                        |
                        | Alternative avec SVG (Heroicons) :
                        | <svg class="w-12 h-12 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        |   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        | </svg>
                        --}}
                        <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center text-2xl">
                            📝
                        </div>
                    </div>
                </div>
            </div>

            {{--
            |------------------------------------------------------------------
            | CARTE 2 : ARTICLES PUBLIÉS
            |------------------------------------------------------------------
            | Même structure que carte 1, couleurs différentes (vert)
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">Publiés</p>
                            {{--
                            | text-green-600 : Couleur verte (positif, succès)
                            | Sémantique couleur :
                            | - Vert : Succès, actif, publié
                            | - Jaune : Attention, brouillon, en attente
                            | - Rouge : Erreur, suppression, danger
                            | - Bleu : Information, neutre, stats
                            --}}
                            <p class="text-3xl font-bold text-green-600">{{ $stats['published_posts'] }}</p>
                        </div>
                        <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">
                            ✅
                        </div>
                    </div>
                </div>
            </div>

            {{--
            |------------------------------------------------------------------
            | CARTE 3 : BROUILLONS
            |------------------------------------------------------------------
            | Couleurs jaunes (attention, en cours)
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">Brouillons</p>
                            <p class="text-3xl font-bold text-yellow-600">{{ $stats['draft_posts'] }}</p>
                        </div>
                        <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center text-2xl">
                            📄
                        </div>
                    </div>
                </div>
            </div>

            {{--
            |------------------------------------------------------------------
            | CARTE 4 : TOTAL VUES
            |------------------------------------------------------------------
            | Couleurs bleues (information, statistique)
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">Total Vues</p>
                            {{--
                            | {{ $stats['total_views'] }} : Somme de views_count
                            |
                            | Calcul dans contrôleur :
                            | 'total_views' => $posts->sum('views_count')
                            |
                            | Exemple :
                            | Article 1 : 150 vues
                            | Article 2 : 87 vues
                            | Article 3 : 230 vues
                            | Total : 467 vues
                            --}}
                            <p class="text-3xl font-bold text-blue-600">{{ $stats['total_views'] }}</p>
                        </div>
                        <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                            👁️
                        </div>
                    </div>
                </div>
            </div>

        </div>

        {{--
        |----------------------------------------------------------------------
        | ARTICLE LE PLUS VU (Mise en Avant)
        |----------------------------------------------------------------------
        | @if($mostViewedPost) : Affiche seulement si variable non null
        |
        | $mostViewedPost peut être null si :
        | - Auteur n'a aucun article publié
        | - Tous les articles publiés ont 0 vues
        |
        | Calcul dans contrôleur :
        | $mostViewedPost = $posts->where('status', 'published')
        |                         ->sortByDesc('views_count')
        |                         ->first();
        |
        | first() retourne null si Collection vide
        --}}
        @if($mostViewedPost)
        {{--
        | BANDEAU GRADIENT (Mise en Avant Visuelle)
        | bg-gradient-to-r : Dégradé de gauche à droite
        | from-indigo-500 to-purple-600 : Couleurs début → fin
        | shadow-sm : Ombre légère
        | mb-8 : Margin-bottom 2rem
        |
        | Pourquoi gradient au lieu de couleur unie ?
        | - Attire l'œil (contraste avec cartes blanches)
        | - Modernité (design tendance 2020+)
        | - Distinction visuelle (section spéciale)
        |
        | Note CSS :
        | bg-gradient-to-r génère :
        | background: linear-gradient(to right, #6366f1, #9333ea);
        --}}
        <div class="bg-gradient-to-r from-indigo-500 to-purple-600 overflow-hidden shadow-sm sm:rounded-lg mb-8">
            {{--
            | CONTENU BANDEAU
            | p-6 : Padding 1.5rem
            | text-white : Tout le texte en blanc (contraste sur fond foncé)
            --}}
            <div class="p-6 text-white">
                {{--
                | TITRE SECTION
                | text-lg : Taille texte 1.125rem (18px)
                | font-bold : Graisse 700
                | mb-2 : Margin-bottom 0.5rem
                --}}
                <h3 class="text-lg font-bold mb-2">🏆 Votre Article le Plus Populaire</h3>
                {{--
                | TITRE ARTICLE
                | text-2xl : Taille texte 1.5rem (24px)
                | mb-1 : Margin-bottom 0.25rem
                | {{ $mostViewedPost->title }} : Titre de l'article
                --}}
                <p class="text-2xl font-bold mb-1">{{ $mostViewedPost->title }}</p>
                {{--
                | MÉTA STATISTIQUES
                | text-indigo-100 : Blanc légèrement teinté (subtilité)
                | 
                | {{ $mostViewedPost->views_count }} : Nombre de vues
                | {{ $mostViewedPost->comments->count() }} : Nombre de commentaires
                |
                | Pourquoi ->count() et pas ->comments_count ?
                | La relation comments est chargée via Eager Loading dans contrôleur
                | $mostViewedPost->comments : Collection d'objets Comment
                | ->count() : Méthode Collection qui compte les éléments
                |
                | Alternative si withCount('comments') dans contrôleur :
                | {{ $mostViewedPost->comments_count }}
                --}}
                <p class="text-indigo-100">👁️ {{ $mostViewedPost->views_count }} vues • 💬 {{ $mostViewedPost->comments->count() }} commentaires</p>
                {{--
                | BOUTON VOIR ARTICLE
                | inline-block : Force comportement bloc sur élément inline (<a>)
                | mt-4 : Margin-top 1rem (espace au-dessus)
                | px-4 py-2 : Padding horizontal 1rem, vertical 0.5rem
                | bg-white : Fond blanc (contraste sur gradient)
                | text-indigo-600 : Texte indigo (rappelle couleur gradient)
                | hover:bg-indigo-50 : Fond indigo très clair au survol
                |
                | Pourquoi blanc et pas transparent ?
                | - Meilleure lisibilité (texte foncé sur fond clair)
                | - Contraste marqué (attire clic)
                | - Cohérence design (boutons primaires blancs)
                --}}
                <a href="{{ route('posts.show', $mostViewedPost) }}" 
                   class="inline-block mt-4 px-4 py-2 bg-white text-indigo-600 rounded-md font-semibold text-sm hover:bg-indigo-50">
                    Voir l'article →
                </a>
            </div>
        </div>
        @endif

        {{--
        |----------------------------------------------------------------------
        | ACTIONS RAPIDES (Boutons Principaux)
        |----------------------------------------------------------------------
        | Section avec 3 boutons d'actions fréquentes
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-8">
            <div class="p-6">
                <h3 class="text-lg font-bold text-gray-900 mb-4">⚡ Actions Rapides</h3>
                {{--
                | GROUPE BOUTONS
                | flex flex-wrap : Flexbox avec retour à la ligne si besoin
                | gap-4 : Espacement 1rem entre boutons
                |
                | Pourquoi flex-wrap ?
                | Mobile : Boutons sur plusieurs lignes si largeur insuffisante
                | Desktop : Boutons sur une seule ligne
                --}}
                <div class="flex flex-wrap gap-4">
                    {{--
                    | BOUTON 1 : NOUVEL ARTICLE (Primaire)
                    | bg-indigo-600 : Fond indigo (action principale)
                    | hover:bg-indigo-700 : Fond plus foncé au survol
                    --}}
                    <a href="{{ route('posts.create') }}" 
                       class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                        ✏️ Nouvel Article
                    </a>
                    {{--
                    | BOUTON 2 : PROFIL PUBLIC (Secondaire)
                    | bg-gray-200 : Fond gris clair (action secondaire)
                    | text-gray-700 : Texte gris foncé (contraste)
                    | hover:bg-gray-300 : Fond légèrement plus foncé
                    |
                    | route('authors.show', auth()->user()) : Profil public de l'auteur connecté
                    | Génère : /author/{id}
                    | Permet à l'auteur de voir son profil tel que les visiteurs le voient
                    --}}
                    <a href="{{ route('authors.show', auth()->user()) }}" 
                       class="inline-flex items-center px-6 py-3 bg-gray-200 border border-transparent rounded-md font-semibold text-sm text-gray-700 uppercase tracking-widest hover:bg-gray-300">
                        👤 Voir Mon Profil Public
                    </a>
                    {{--
                    | BOUTON 3 : PARAMÈTRES (Secondaire)
                    --}}
                    <a href="{{ route('profile.edit') }}" 
                       class="inline-flex items-center px-6 py-3 bg-gray-200 border border-transparent rounded-md font-semibold text-sm text-gray-700 uppercase tracking-widest hover:bg-gray-300">
                        ⚙️ Paramètres
                    </a>
                </div>
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | LISTE COMPLÈTE DES ARTICLES (Tableau)
        |----------------------------------------------------------------------
        | Section principale : Tableau de tous les articles avec actions
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                {{--
                | HEADER SECTION
                | flex justify-between : Répartit titre et compteur
                --}}
                <div class="flex items-center justify-between mb-6">
                    {{--
                    | TITRE + COMPTEUR
                    | {{ $posts->count() }} : Nombre total d'articles (Collection)
                    | Affiche : "📚 Mes Articles (7)"
                    --}}
                    <h3 class="text-lg font-bold text-gray-900">📚 Mes Articles ({{ $posts->count() }})</h3>
                </div>

                {{--
                | VÉRIFICATION PRÉSENCE D'ARTICLES
                | @if($posts->count() > 0) : Si au moins 1 article
                --}}
                @if($posts->count() > 0)
                    {{--
                    | CONTENEUR TABLEAU (Scroll horizontal si nécessaire)
                    | overflow-x-auto : Active défilement horizontal si tableau trop large
                    |
                    | Pourquoi nécessaire ?
                    | Mobile : Tableau 6 colonnes dépasse largeur écran
                    | overflow-x-auto permet scroll horizontal sans casser layout
                    |
                    | Alternative responsive (masquer colonnes mobile) :
                    | Ajouter classes hidden md:table-cell sur colonnes non essentielles
                    --}}
                    <div class="overflow-x-auto">
                        {{--
                        | TABLEAU HTML
                        | min-w-full : Largeur min 100% (occupe tout l'espace)
                        | divide-y divide-gray-200 : Bordures horizontales entre lignes
                        --}}
                        <table class="min-w-full divide-y divide-gray-200">
                            {{--
                            | EN-TÊTE TABLEAU
                            | bg-gray-50 : Fond gris clair (distingue header du corps)
                            --}}
                            <thead class="bg-gray-50">
                                {{--
                                | LIGNE EN-TÊTES
                                --}}
                                <tr>
                                    {{--
                                    | COLONNE 1 : TITRE
                                    | px-6 py-3 : Padding cellule (1.5rem horizontal, 0.75rem vertical)
                                    | text-left : Alignement texte gauche
                                    | text-xs : Taille texte 0.75rem (12px)
                                    | font-medium : Graisse 500
                                    | text-gray-500 : Gris moyen
                                    | uppercase : Texte majuscules
                                    | tracking-wider : Espacement lettres augmenté
                                    |
                                    | Ce style est typique des tableaux data modernes :
                                    | - Petites majuscules espacées (lisibilité)
                                    | - Couleur secondaire (moins important que données)
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Titre
                                    </th>
                                    {{--
                                    | COLONNE 2 : CATÉGORIE
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Catégorie
                                    </th>
                                    {{--
                                    | COLONNE 3 : STATUT
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Statut
                                    </th>
                                    {{--
                                    | COLONNE 4 : VUES
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Vues
                                    </th>
                                    {{--
                                    | COLONNE 5 : DATE
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Date
                                    </th>
                                    {{--
                                    | COLONNE 6 : ACTIONS
                                    --}}
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            {{--
                            | CORPS TABLEAU
                            | bg-white : Fond blanc (par défaut mais explicite)
                            | divide-y divide-gray-200 : Bordures horizontales entre lignes
                            --}}
                            <tbody class="bg-white divide-y divide-gray-200">
                                {{--
                                | BOUCLE SUR ARTICLES
                                | @foreach($posts as $post) : Itère sur Collection
                                | $posts : Collection de TOUS les articles (publiés + brouillons)
                                --}}
                                @foreach($posts as $post)
                                {{--
                                | LIGNE TABLEAU
                                | hover:bg-gray-50 : Fond gris très clair au survol (feedback)
                                --}}
                                <tr class="hover:bg-gray-50">
                                    {{--
                                    | CELLULE : TITRE
                                    | px-6 py-4 : Padding cellule
                                    --}}
                                    <td class="px-6 py-4">
                                        {{--
                                        | LIEN TITRE (vers page article)
                                        | text-sm : Taille texte 0.875rem (14px)
                                        | font-medium : Graisse 500 (accent visuel)
                                        | hover:text-indigo-600 : Couleur indigo au survol
                                        |
                                        | Str::limit($post->title, 50) : Tronque à 50 caractères
                                        | Évite débordement si titre très long
                                        | Exemple : "Introduction complète à Laravel 11..." (si > 50 char)
                                        --}}
                                        <a href="{{ route('posts.show', $post) }}" 
                                           class="text-sm font-medium text-gray-900 hover:text-indigo-600">
                                            {{ Str::limit($post->title, 50) }}
                                        </a>
                                    </td>
                                    {{--
                                    | CELLULE : CATÉGORIE (Badge)
                                    | whitespace-nowrap : Pas de retour ligne (garde badge sur 1 ligne)
                                    --}}
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        {{--
                                        | BADGE CATÉGORIE
                                        | px-2 : Padding horizontal 0.5rem
                                        | inline-flex : Flexbox inline (pour centrer texte)
                                        | text-xs : Taille texte 0.75rem (12px)
                                        | leading-5 : Line-height 1.25rem
                                        | font-semibold : Graisse 600
                                        | rounded-full : Bordures complètement arrondies (pilule)
                                        | bg-indigo-100 text-indigo-800 : Couleurs badge
                                        |
                                        | $post->category->name : Accès relation belongsTo
                                        | Charge automatiquement via Eager Loading (with('category'))
                                        --}}
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-indigo-100 text-indigo-800">
                                            {{ $post->category->name }}
                                        </span>
                                    </td>
                                    {{--
                                    | CELLULE : STATUT (Badge Conditionnel)
                                    --}}
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        {{--
                                        | AFFICHAGE CONDITIONNEL SELON STATUT
                                        | @if($post->status === 'published') : Si article publié
                                        --}}
                                        @if($post->status === 'published')
                                            {{--
                                            | BADGE VERT "PUBLIÉ"
                                            | bg-green-100 text-green-800 : Couleurs vertes (succès)
                                            --}}
                                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                ✅ Publié
                                            </span>
                                        @else
                                            {{--
                                            | BADGE JAUNE "BROUILLON"
                                            | @else : Sinon (status = 'draft')
                                            | bg-yellow-100 text-yellow-800 : Couleurs jaunes (attention)
                                            --}}
                                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                                📄 Brouillon
                                            </span>
                                        @endif
                                    </td>
                                    {{--
                                    | CELLULE : VUES
                                    | text-sm text-gray-500 : Texte petit et gris
                                    --}}
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        👁️ {{ $post->views_count }}
                                    </td>
                                    {{--
                                    | CELLULE : DATE CRÉATION
                                    | {{ $post->created_at->format('d/m/Y') }} : Formatage date
                                    | 
                                    | $post->created_at : Carbon instance (DateTime amélioré)
                                    | format('d/m/Y') : Méthode Carbon formatage personnalisé
                                    | Résultat : "10/12/2024" (jour/mois/année)
                                    |
                                    | Autres formats possibles :
                                    | format('d M Y') → "10 Déc 2024"
                                    | format('Y-m-d') → "2024-12-10" (ISO 8601)
                                    | format('d/m/Y H:i') → "10/12/2024 14:30"
                                    | diffForHumans() → "il y a 2 jours"
                                    |
                                    | Pourquoi created_at et pas published_at ?
                                    | - created_at : Date création (existe toujours)
                                    | - published_at : Date publication (null pour brouillons)
                                    | Ici on affiche date création pour avoir info même sur brouillons
                                    --}}
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                        {{ $post->created_at->format('d/m/Y') }}
                                    </td>
                                    {{--
                                    | CELLULE : ACTIONS (Modifier + Supprimer)
                                    | text-sm font-medium : Texte petit et moyen
                                    --}}
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        {{--
                                        | LIEN MODIFIER
                                        | text-indigo-600 : Couleur indigo (action principale)
                                        | hover:text-indigo-900 : Couleur plus foncée au survol
                                        | mr-3 : Margin-right 0.75rem (espace avant bouton supprimer)
                                        --}}
                                        <a href="{{ route('posts.edit', $post) }}" 
                                           class="text-indigo-600 hover:text-indigo-900 mr-3">
                                            Modifier
                                        </a>
                                        {{--
                                        | FORMULAIRE SUPPRIMER (Inline)
                                        | class="inline" : Affichage inline (sur même ligne que "Modifier")
                                        | onsubmit : Confirmation JavaScript avant soumission
                                        | return confirm(...) : Affiche popup confirmation
                                        --}}
                                        <form action="{{ route('posts.destroy', $post) }}" 
                                              method="POST" 
                                              class="inline"
                                              onsubmit="return confirm('Supprimer cet article ?');">
                                            @csrf
                                            @method('DELETE')
                                            {{--
                                            | BOUTON SUPPRIMER
                                            | type="submit" : Soumet formulaire au clic
                                            | text-red-600 : Couleur rouge (danger)
                                            | hover:text-red-900 : Rouge plus foncé au survol
                                            |
                                            | Pourquoi bouton et pas lien <a> ?
                                            | Actions destructives doivent utiliser POST/DELETE (pas GET)
                                            | Un lien <a> génère une requête GET
                                            | Un crawler/bot pourrait suivre le lien et supprimer l'article
                                            | Un bouton <button type="submit"> dans <form method="POST"> est sécurisé
                                            --}}
                                            <button type="submit" class="text-red-600 hover:text-red-900">
                                                Supprimer
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                
                {{--
                | ÉTAT VIDE (Aucun Article)
                | @else : Alternative au @if (si $posts->count() === 0)
                --}}
                @else
                    {{--
                    | MESSAGE ÉTAT VIDE
                    | text-center : Centrage horizontal texte
                    | py-12 : Padding vertical 3rem (espacement généreux)
                    --}}
                    <div class="text-center py-12">
                        {{--
                        | MESSAGE PRINCIPAL
                        | mb-4 : Margin-bottom 1rem (espace avant bouton)
                        --}}
                        <p class="text-gray-600 mb-4">Vous n'avez pas encore d'articles.</p>
                        {{--
                        | BOUTON CALL-TO-ACTION
                        | Encourage l'utilisateur à créer son premier article
                        | Style identique au bouton "Nouvel Article" (cohérence)
                        --}}
                        <a href="{{ route('posts.create') }}" 
                           class="inline-flex items-center px-4 py-2 bg-indigo-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-indigo-700">
                            ✏️ Créer Mon Premier Article
                        </a>
                    </div>
                @endif

            </div>
        </div>

    </div>
</div>
@endsection
```

**Tableau Anatomie des Cartes Statistiques**

| Élément | Classes Tailwind | Rôle | Valeurs Possibles |
|---------|-----------------|------|-------------------|
| **Conteneur** | `bg-white shadow-sm rounded-lg` | Carte blanche avec ombre | Standard toutes cartes |
| **Padding** | `p-6` | Espacement interne | 1.5rem (24px) |
| **Layout** | `flex justify-between items-center` | Disposition texte/icône | Texte gauche, icône droite |
| **Label** | `text-sm font-medium text-gray-600` | Description métrique | "Total Articles", "Publiés", etc. |
| **Valeur** | `text-3xl font-bold text-[color]` | Chiffre statistique | Couleur selon contexte |
| **Icône cercle** | `w-12 h-12 bg-[color]-100 rounded-full` | Décoration visuelle | Emoji unicode |
| **Couleurs** | Variations `-100` (fond) et `-600` (texte) | Cohérence sémantique | Indigo, vert, jaune, bleu |

**Code Pattern Réutilisable :**

```html
<div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
    <div class="p-6">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm font-medium text-gray-600">[LABEL]</p>
                <p class="text-3xl font-bold text-[COLOR]-600">[VALEUR]</p>
            </div>
            <div class="w-12 h-12 bg-[COLOR]-100 rounded-full flex items-center justify-center text-2xl">
                [EMOJI]
            </div>
        </div>
    </div>
</div>
```

**Explications Techniques Approfondies**

??? abstract "**1. Pourquoi Collection->count() et pas Query Builder count() ?**"

    **Dans le contrôleur :**

    ```php
    // Méthode 1 : Query Builder count() (1 requête SQL optimisée)
    $totalPosts = Post::where('user_id', $user->id)->count();
    // SQL : SELECT COUNT(*) FROM posts WHERE user_id = 1

    // Méthode 2 : Collection count() (1 requête + itération en mémoire)
    $posts = Post::where('user_id', $user->id)->get();
    $totalPosts = $posts->count();
    // SQL : SELECT * FROM posts WHERE user_id = 1
    // PHP : compte les éléments en mémoire
    ```

    **Pourquoi utiliser Collection count() dans le dashboard ?**

    ```php
    $posts = Post::where('user_id', $user->id)->with('category')->latest()->get();

    $stats = [
        'total_posts' => $posts->count(),               // Collection
        'published_posts' => $posts->where('status', 'published')->count(), // Collection
        'draft_posts' => $posts->where('status', 'draft')->count(),         // Collection
        'total_views' => $posts->sum('views_count'),    // Collection
    ];
    ```

    **Avantages :**

    - ✅ Une seule requête SQL (récupère tous les articles)
    - ✅ Calculs multiples en mémoire (pas de requêtes supplémentaires)
    - ✅ Réutilisation de `$posts` pour tableau et stats

    **Inconvénient :**

    - ❌ Si auteur a 1000+ articles, consomme beaucoup de RAM

    **Alternative pour gros volumes (>500 articles) :**

    ```php
    $stats = [
        'total_posts' => Post::where('user_id', $user->id)->count(),
        'published_posts' => Post::where('user_id', $user->id)->where('status', 'published')->count(),
        'draft_posts' => Post::where('user_id', $user->id)->where('status', 'draft')->count(),
        'total_views' => Post::where('user_id', $user->id)->sum('views_count'),
    ];
    // 4 requêtes SQL mais efficaces (COUNT/SUM optimisés MySQL)
    ```

    **Règle générale :**

    - <100 articles → Collection count() (1 requête)
    - >100 articles → Query Builder count() (N requêtes mais optimisées)

??? abstract "**2. Gestion responsive du tableau (overflow-x-auto)**"

    **Problème :**

    Tableau 6 colonnes dépasse largeur écran mobile (320-480px).

    **Solution 1 : Scroll horizontal (implémentée)**

    ```html
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <!-- 6 colonnes visibles via scroll -->
        </table>
    </div>
    ```

    **Avantages :**

    - ✅ Toutes les colonnes accessibles (scroll horizontal)
    - ✅ Simplicité (pas de classes conditionnelles)

    **Inconvénients :**

    - ❌ UX mobile moins idéale (scroll horizontal peu naturel)

    **Solution 2 : Masquer colonnes non essentielles mobile (alternative)**

    ```html
    <table>
        <thead>
            <tr>
                <th>Titre</th>
                <th class="hidden md:table-cell">Catégorie</th>
                <th>Statut</th>
                <th class="hidden lg:table-cell">Vues</th>
                <th class="hidden md:table-cell">Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>...</td>
                <td class="hidden md:table-cell">...</td>
                <td>...</td>
                <td class="hidden lg:table-cell">...</td>
                <td class="hidden md:table-cell">...</td>
                <td>...</td>
            </tr>
        </tbody>
    </table>
    ```

    **Résultat :**

    - Mobile : 3 colonnes (Titre, Statut, Actions)
    - Tablet (md) : 5 colonnes (+ Catégorie, Date)
    - Desktop (lg) : 6 colonnes (+ Vues)

    **Avantages :**

    - ✅ UX mobile optimale (pas de scroll horizontal)
    - ✅ Colonnes essentielles toujours visibles

    **Inconvénients :**

    - ❌ Complexité (classes répétées)
    - ❌ Info masquée sur mobile (catégorie, date)

    **Solution 3 : Cards mobiles, tableau desktop (avancé)**

    ```html
    {{-- Mobile : Cards --}}
    <div class="block md:hidden space-y-4">
        @foreach($posts as $post)
        <div class="bg-white p-4 rounded-lg shadow">
            <h4>{{ $post->title }}</h4>
            <span>{{ $post->category->name }}</span>
            <!-- Actions -->
        </div>
        @endforeach
    </div>

    {{-- Desktop : Tableau --}}
    <div class="hidden md:block overflow-x-auto">
        <table>...</table>
    </div>
    ```

    **Avantages :**

    - ✅ UX optimale chaque format
    - ✅ Design moderne (cards mobile standard)

    **Inconvénients :**

    - ❌ Code dupliqué (maintenance)
    - ❌ Complexité implémentation

    **Recommandation :**

    - Petits projets → overflow-x-auto (simplicité)
    - Projets moyens → Masquer colonnes (compromis)
    - Gros projets → Cards mobiles (UX optimale)

??? abstract "**3. Différence entre inline et inline-flex pour boutons**"

    **inline :**

    ```html
    <form class="inline">
        <button>Supprimer</button>
    </form>
    ```

    **Comportement :**

    - Formulaire devient élément inline (comme `<span>`)
    - Occupe seulement largeur contenu
    - Permet plusieurs formulaires sur même ligne

    **inline-flex :**

    ```html
    <a class="inline-flex items-center">
        ✏️ Modifier
    </a>
    ```

    **Comportement :**

    - Élément inline avec flexbox interne
    - `items-center` centre verticalement emoji + texte
    - Nécessaire quand contenu mixte (icône + texte)

    **Exemple comparatif :**

    ```html
    {{-- Sans inline-flex (désaligné) --}}
    <a class="inline">
        <span class="text-2xl">✏️</span> Modifier
    </a>
    {{-- Résultat : Emoji + texte pas alignés verticalement --}}

    {{-- Avec inline-flex (aligné) --}}
    <a class="inline-flex items-center">
        <span class="text-2xl">✏️</span> Modifier
    </a>
    {{-- Résultat : Emoji + texte centrés verticalement --}}
    ```

    **Règle générale :**

    - `inline` → Formulaires, éléments simples (1 type contenu)
    - `inline-flex` → Boutons/liens avec icônes (contenu mixte)


<small>**Explication dégradé CSS :** `bg-gradient-to-r from-indigo-500 to-purple-600` génère CSS `background: linear-gradient(to right, #6366f1 0%, #9333ea 100%);`. Le dégradé passe progressivement de la couleur début (indigo-500) à la couleur fin (purple-600) de gauche à droite. Alternatives : `bg-gradient-to-l` (droite→gauche), `bg-gradient-to-b` (haut→bas), `bg-gradient-to-br` (coin supérieur gauche→coin inférieur droit). **Format de date Carbon :** `format('d/m/Y')` utilise conventions PHP `DateTime` : `d` = jour 2 chiffres, `m` = mois 2 chiffres, `Y` = année 4 chiffres. Liste complète : https://www.php.net/manual/fr/datetime.format.php. **État vide (Empty State) :** Pattern UX recommandé : message explicite + illustration + action principale. Évite frustration utilisateur face à écran vide. Exemples célèbres : Dropbox ("Glissez fichiers ici"), GitHub ("Créez votre premier repo"), Slack ("Invitez votre équipe").</small>

✅ **Étape 6.6 Terminée !**

**Fichier modifié :**
- `resources/views/dashboard.blade.php` : Dashboard complet avec statistiques et tableau

**Concepts maîtrisés :**
- Grilles responsive multi-colonnes (`grid-cols-1 md:grid-cols-2 lg:grid-cols-4`)
- Cartes statistiques avec icônes circulaires
- Dégradés CSS (`bg-gradient-to-r`)
- Tableaux HTML avec hover states
- Badges conditionnels (statut publié/brouillon)
- État vide avec call-to-action
- Formulaires inline avec confirmation JS
- Collection methods (`count()`, `sum()`)
- Formatage dates Carbon

### Étape 6.7 : Créer la Page Catégorie (Filtrage Articles par Thématique)

**Contexte de l'étape :**

> La page catégorie est un **point d'entrée thématique** de votre blog. Elle permet aux visiteurs de découvrir tous les articles d'un sujet spécifique (Technologie, Voyage, Cuisine, etc.). Cette page joue plusieurs rôles cruciaux :

!!! note "**Rôles fonctionnels :**"

    1. **Navigation par thème** : Les visiteurs explorent le contenu par centres d'intérêt
    2. **SEO** : URLs descriptives (`/category/technologie`) indexées par moteurs de recherche
    3. **Découvrabilité** : Facilite exploration du catalogue d'articles
    4. **Engagement** : Encourage lecture multiple (articles similaires regroupés)

!!! note "**Architecture de la page :**"

    - **Header catégorie** : Bannière avec nom catégorie + compteur articles
    - **Grille articles** : Liste paginée (9 par page) avec même design que page d'accueil
    - **Pagination** : Navigation entre pages si >9 articles
    - **État vide** : Message encourageant si catégorie vide (+ lien retour accueil)

!!! note "**Différences avec page d'accueil :**"

    | Aspect | Page d'Accueil | Page Catégorie |
    |--------|----------------|----------------|
    | **Articles affichés** | Tous (toutes catégories) | Filtrés (1 catégorie) |
    | **Sidebar** | Oui (catégories + populaires) | Non (focus contenu) |
    | **Hero section** | Oui (présentation blog) | Non (direct au contenu) |
    | **Largeur** | 2/3 + 1/3 sidebar | 100% (pleine largeur) |
    | **Titre page** | "Bienvenue sur notre Blog" | "Catégorie : Technologie" |

**Variables disponibles dans la vue :**

Rappel du contrôleur `CategoryController::show()` :

```php
return view('categories.show', compact('category', 'posts'));
```

- `$category` : Instance Category avec attribut `slug` utilisé pour route binding
- `$posts` : Collection paginée (9 articles/page) filtrés par `category_id` + statut publié

**Créer le dossier et le fichier :**

```bash
# Créer le dossier categories
mkdir resources/views/categories

# Le fichier show.blade.php sera créé manuellement
```

**Créer le fichier `resources/views/categories/show.blade.php` :**

```html title="Code Blade"
{{--
|------------------------------------------------------------------------------
| PAGE CATÉGORIE (Filtrage par Thématique)
|------------------------------------------------------------------------------
| Vue publique accessible à tous les visiteurs
| Affiche tous les articles publiés d'une catégorie spécifique
|
| URL : /category/{slug}
| Exemple : /category/technologie
--}}
@extends('layouts.app')

{{--
| TITRE DYNAMIQUE
| 'Catégorie : ' . $category->name : Concaténation PHP
| {{ $category->name }} : Injection variable Blade
|
| Résultat <title> : "Mon Blog - Catégorie : Technologie"
|
| Note sur concaténation :
| @section('title', 'Catégorie : ' . $category->name)
| Équivaut à :
| @section('title')
|     Catégorie : {{ $category->name }}
| @endsection
|
| La syntaxe courte est préférable pour sections simples (1 ligne)
--}}
@section('title', 'Catégorie : ' . $category->name)

@section('content')
<div class="py-12">
    {{--
    | CONTENEUR PRINCIPAL (Pleine Largeur)
    | max-w-7xl : Largeur max 1280px (même que page d'accueil)
    | Pas de grid 2/3 + 1/3 car pas de sidebar sur cette page
    | Focus 100% sur les articles de la catégorie
    --}}
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        
        {{--
        |----------------------------------------------------------------------
        | HEADER CATÉGORIE (Bannière Présentation)
        |----------------------------------------------------------------------
        | Section distinctive qui identifie clairement la catégorie
        | mb-8 : Margin-bottom 2rem (espace avant grille articles)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-8">
            {{--
            | CONTENU HEADER
            | p-8 : Padding 2rem (plus généreux que cards standards p-6)
            | text-center : Centrage horizontal de tout le contenu
            |
            | Pourquoi centrage ?
            | - Attire l'œil (focal point)
            | - Symétrie visuelle (équilibre)
            | - Clarté hiérarchie (titre principal)
            --}}
            <div class="p-8 text-center">
                {{--
                | TITRE CATÉGORIE (H1)
                | text-4xl : Taille texte 2.25rem (36px)
                | font-bold : Graisse 700
                | mb-2 : Margin-bottom 0.5rem
                |
                | 📂 : Emoji dossier (contexte visuel "catégorie")
                | {{ $category->name }} : Nom catégorie (ex: "Technologie")
                |
                | Pourquoi H1 ici et pas sur page d'accueil ?
                | SEO : Chaque page doit avoir UN SEUL H1 descriptif
                | Page d'accueil : H1 = "Bienvenue sur notre Blog"
                | Page catégorie : H1 = "Catégorie : Technologie"
                | Aide moteurs de recherche comprendre sujet principal page
                --}}
                <h1 class="text-4xl font-bold text-gray-900 mb-2">
                    📂 {{ $category->name }}
                </h1>
                
                {{--
                | COMPTEUR ARTICLES
                | text-gray-600 : Gris moyen (info secondaire)
                | 
                | {{ $posts->total() }} : Nombre TOTAL d'articles (toutes pages)
                | Méthode spécifique objets paginés (LengthAwarePaginator)
                |
                | Différence $posts->total() vs $posts->count() :
                | 
                | $posts->total()  : Compte TOUS les articles (ex: 27)
                | $posts->count()  : Compte articles PAGE ACTUELLE (ex: 9)
                |
                | Exemple :
                | 27 articles au total, 9 par page
                | Page 1 : $posts->total() = 27, $posts->count() = 9
                | Page 2 : $posts->total() = 27, $posts->count() = 9
                | Page 3 : $posts->total() = 27, $posts->count() = 9
                | Page 4 : $posts->total() = 27, $posts->count() = 0 (n'existe pas)
                |
                | Str::plural('article', $posts->total()) : Pluralisation automatique
                | Retourne "article" si 1, "articles" si 0 ou >1
                | Exemples :
                | - 0 article → "0 articles"
                | - 1 article → "1 article"
                | - 5 articles → "5 articles"
                |
                | Note : Str::plural() est basique (ajoute 's')
                | Pour français complexe (cheval → chevaux), utilisez package spécialisé
                --}}
                <p class="text-gray-600">
                    {{ $posts->total() }} {{ Str::plural('article', $posts->total()) }} dans cette catégorie
                </p>
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | GRILLE ARTICLES (ou État Vide)
        |----------------------------------------------------------------------
        | @if($posts->count() > 0) : Vérifie présence articles PAGE ACTUELLE
        |
        | Pourquoi count() et pas total() ?
        | count() vérifie s'il y a articles à afficher sur cette page
        | total() pourrait être >0 mais page actuelle vide (page invalide)
        |
        | Exemple edge case :
        | URL : /category/technologie?page=999
        | $posts->total() = 27 (articles existent)
        | $posts->count() = 0 (page 999 vide)
        | → Affiche état vide (correct)
        --}}
        @if($posts->count() > 0)
            {{--
            | GRILLE ARTICLES RESPONSIVE
            | grid grid-cols-1 : 1 colonne par défaut (mobile)
            | md:grid-cols-2 : 2 colonnes sur écrans ≥768px (tablet)
            | lg:grid-cols-3 : 3 colonnes sur écrans ≥1024px (desktop)
            | gap-6 : Espacement 1.5rem entre cartes
            | mb-8 : Margin-bottom 2rem (espace avant pagination)
            |
            | Progression responsive :
            | Mobile (320-767px) : 1 colonne (100% largeur, défilement vertical)
            | Tablet (768-1023px) : 2 colonnes (2x ~50% largeur)
            | Desktop (1024+px) : 3 colonnes (3x ~33% largeur)
            |
            | Pourquoi 3 colonnes et pas 4 ?
            | - Lisibilité : Cards trop étroites en 4 colonnes
            | - Images : Format portrait/carré mieux en 3 colonnes
            | - Standard blog : 3 colonnes = norme industrie (Medium, Dev.to)
            --}}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {{--
                | BOUCLE SUR ARTICLES
                | @foreach($posts as $post) : Itère sur Collection paginée
                | $posts : 9 articles maximum (défini dans contrôleur paginate(9))
                --}}
                @foreach($posts as $post)
                {{--
                | CARD ARTICLE (Structure Identique Page Accueil)
                | hover:shadow-md : Ombre moyenne au survol (feedback interactif)
                | transition : Animation douce 150ms (propriété all par défaut)
                |
                | Pourquoi structure identique page d'accueil ?
                | - Cohérence UX : utilisateur reconnaît pattern
                | - Maintenance : modifications CSS impactent toutes pages
                | - Performance : navigateur met en cache styles
                |
                | Alternative avancée : Créer composant Blade réutilisable
                | <x-post-card :post="$post" />
                | Évite duplication code entre home.blade.php et categories/show.blade.php
                --}}
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg hover:shadow-md transition">
                    {{--
                    | IMAGE COUVERTURE (Conditionnelle)
                    | @if($post->image) : Affiche seulement si colonne image non null
                    | h-48 : Hauteur fixe 12rem (192px)
                    | bg-gray-200 : Fond gris si image ne charge pas (fallback)
                    | overflow-hidden : Masque débordement image (crop si trop grande)
                    --}}
                    @if($post->image)
                    <div class="h-48 bg-gray-200 overflow-hidden">
                        {{--
                        | IMAGE RESPONSIVE
                        | src="{{ $post->image }}" : URL image stockée en BDD
                        | alt="{{ $post->title }}" : Texte alternatif (accessibilité + SEO)
                        | w-full : Largeur 100% (occupe card entière)
                        | h-full : Hauteur 100% (occupe div h-48)
                        | object-cover : Couvre zone sans distorsion (crop intelligent)
                        |
                        | Différence object-cover vs object-contain :
                        | object-cover : Remplit ENTIÈREMENT zone (peut rogner)
                        | object-contain : Image ENTIÈRE visible (peut laisser espaces vides)
                        |
                        | Exemple image 800x400 dans zone 300x192 :
                        | object-cover : Image rognée à 384x192 (centré)
                        | object-contain : Image réduite à 300x150 (bandes grises haut/bas)
                        |
                        | Pour blog : object-cover préférable (esthétique uniforme)
                        --}}
                        <img src="{{ $post->image }}" alt="{{ $post->title }}" class="w-full h-full object-cover">
                    </div>
                    @endif
                    
                    {{--
                    | CONTENU CARD (Padding Interne)
                    | p-6 : Padding 1.5rem (toutes directions)
                    --}}
                    <div class="p-6">
                        {{--
                        | NOM AUTEUR (Lien Cliquable)
                        | hover:text-indigo-600 : Couleur indigo au survol
                        | 
                        | route('authors.show', $post->user) : Génère /author/{id}
                        | Passe objet User entier (Laravel extrait ->id automatiquement)
                        | 
                        | $post->user : Relation belongsTo chargée via Eager Loading
                        | Rappel contrôleur : ->with('user')
                        | Sans Eager Loading : N+1 problème (1 requête par article)
                        | Avec Eager Loading : 2 requêtes totales (articles + users)
                        --}}
                        <a href="{{ route('authors.show', $post->user) }}" class="hover:text-indigo-600">
                            {{ $post->user->name }}
                        </a>
                        {{--
                        | SÉPARATEUR VISUEL
                        | mx-2 : Margin horizontal 0.5rem (espace autour)
                        | • : Caractère unicode bullet point
                        --}}
                        <span class="mx-2">•</span>
                        {{--
                        | DATE PUBLICATION (Format Relatif)
                        | {{ $post->published_at->diffForHumans() }} : "il y a 2 jours"
                        | 
                        | $post->published_at : Instance Carbon (DateTime amélioré)
                        | diffForHumans() : Convertit en format lisible relatif
                        | 
                        | Exemples rendus :
                        | - Publié il y a 5 minutes → "il y a 5 minutes"
                        | - Publié il y a 2 heures → "il y a 2 heures"
                        | - Publié il y a 3 jours → "il y a 3 jours"
                        | - Publié il y a 2 mois → "il y a 2 mois"
                        |
                        | Configuration locale :
                        | Dans config/app.php : 'locale' => 'fr'
                        | Affiche "il y a" au lieu de "ago"
                        |
                        | Alternative format fixe :
                        | {{ $post->published_at->format('d M Y') }} → "10 Déc 2024"
                        | Moins personnel mais plus précis
                        --}}
                        <span>{{ $post->published_at->diffForHumans() }}</span>
                    </div>
                    <div>
                        {{--
                        | COMPTEUR VUES
                        | 👁️ : Emoji œil (contexte visuel "vues")
                        | {{ $post->views_count }} : Nombre de vues (colonne BIGINT UNSIGNED)
                        --}}
                        👁️ {{ $post->views_count }}
                    </div>
                </div>
            </div>
            @endforeach
        </div>

        {{--
        | PAGINATION (Navigation Entre Pages)
        | mt-6 : Margin-top 1.5rem (espace après grille)
        |
        | {{ $posts->links() }} : Génère HTML pagination automatiquement
        | Affiche : « Précédent | 1 2 3 ... | Suivant »
        |
        | Fonctionnement :
        | 1. Laravel détecte paramètre ?page=N dans URL
        | 2. paginate(9) dans contrôleur charge articles page N
        | 3. links() génère boutons avec ?page=N+1, ?page=N-1
        | 4. Clic bouton → Recharge page avec nouveau paramètre
        |
        | Personnalisation style :
        | Par défaut : Tailwind (configuré dans AppServiceProvider)
        | Personnalisé : php artisan vendor:publish --tag=laravel-pagination
        | Crée : resources/views/vendor/pagination/tailwind.blade.php
        |
        | Méthodes utiles LengthAwarePaginator :
        | $posts->currentPage() : Page actuelle (ex: 2)
        | $posts->lastPage() : Dernière page (ex: 4)
        | $posts->hasMorePages() : true si pages restantes
        | $posts->perPage() : Articles par page (ex: 9)
        | $posts->total() : Total articles (ex: 35)
        | $posts->count() : Articles page actuelle (ex: 9)
        --}}
        <div class="mt-6">
            {{ $posts->links() }}
        </div>
        
        {{--
        | ÉTAT VIDE (Aucun Article dans Catégorie)
        | @else : Alternative au @if (si $posts->count() === 0)
        --}}
        @else
            {{--
            | MESSAGE ÉTAT VIDE
            | p-8 : Padding 2rem (espacement généreux)
            | text-center : Centrage horizontal
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-8 text-center">
                {{--
                | MESSAGE PRINCIPAL
                | mb-4 : Margin-bottom 1rem (espace avant lien)
                | text-gray-600 : Gris moyen (ton neutre)
                --}}
                <p class="text-gray-600 mb-4">Aucun article dans cette catégorie pour le moment.</p>
                {{--
                | LIEN RETOUR ACCUEIL
                | text-indigo-600 : Couleur primaire (action principale)
                | hover:text-indigo-800 : Couleur plus foncée au survol
                | ← : Flèche unicode (indication direction retour)
                |
                | Pourquoi lien et pas bouton ?
                | Sémantique HTML : <a> pour navigation, <button> pour actions
                | Retour accueil = navigation → <a> approprié
                | Soumettre formulaire = action → <button> approprié
                --}}
                <a href="{{ route('home') }}" class="text-indigo-600 hover:text-indigo-800">
                    ← Retour à l'accueil
                </a>
            </div>
        @endif

    </div>
</div>
@endsection
```

**Tableau Comparatif Méthodes Pagination Laravel**

| Méthode | Retour | Usage | Exemple |
|---------|--------|-------|---------|
| `->count()` | `int` | Articles **page actuelle** | `$posts->count() → 9` |
| `->total()` | `int` | Articles **tous résultats** | `$posts->total() → 27` |
| `->perPage()` | `int` | Articles **par page** | `$posts->perPage() → 9` |
| `->currentPage()` | `int` | Numéro **page actuelle** | `$posts->currentPage() → 2` |
| `->lastPage()` | `int` | Numéro **dernière page** | `$posts->lastPage() → 3` |
| `->hasMorePages()` | `bool` | **Pages suivantes** existent | `$posts->hasMorePages() → true` |
| `->onFirstPage()` | `bool` | Sur **première page** | `$posts->onFirstPage() → false` |
| `->items()` | `array` | Articles **actuels** (array) | `$posts->items() → [Post, Post, ...]` |
| `->links()` | `string` | HTML **pagination** | `$posts->links() → "<nav>...</nav>"` |

!!! example "**Exemple calcul pages :**"

    ```php
    // Contrôleur
    $posts = Post::where('category_id', 1)->published()->paginate(9);

    // Page 1 (?page=1)
    $posts->currentPage()    // 1
    $posts->count()          // 9 (articles affichés)
    $posts->total()          // 27 (total BDD)
    $posts->lastPage()       // 3 (27 / 9 = 3)
    $posts->hasMorePages()   // true (page 2 existe)

    // Page 2 (?page=2)
    $posts->currentPage()    // 2
    $posts->count()          // 9
    $posts->total()          // 27
    $posts->hasMorePages()   // true (page 3 existe)

    // Page 3 (?page=3)
    $posts->currentPage()    // 3
    $posts->count()          // 9
    $posts->total()          // 27
    $posts->hasMorePages()   // false (dernière page)

    // Page 4 (?page=4) - N'existe pas
    $posts->currentPage()    // 4
    $posts->count()          // 0 (aucun article)
    $posts->total()          // 27 (total inchangé)
    ```

**Explications Techniques Approfondies**

??? abstract "**1. Différence count() vs total() sur objets paginés**"

    **Contexte :**

    !!! quote "Laravel utilise la classe `LengthAwarePaginator` pour les résultats paginés. Cette classe hérite de `Collection` mais ajoute des méthodes spécifiques pagination."

    **Méthode count() :**

    ```php
    $posts = Post::paginate(9); // Page 1

    $posts->count(); // Retourne 9 (articles sur page actuelle)
    ```

    **SQL généré :**

    ```sql
    SELECT * FROM posts LIMIT 9 OFFSET 0
    ```

    **count()** compte les éléments **chargés en mémoire** (items de la Collection actuelle).

    **Méthode total() :**

    ```php
    $posts->total(); // Retourne 27 (total articles BDD)
    ```

    **SQL généré (requête supplémentaire) :**

    ```sql
    SELECT COUNT(*) FROM posts
    ```

    **total()** exécute une requête `COUNT(*)` pour obtenir le **nombre total** d'enregistrements correspondant aux critères (ignorer LIMIT/OFFSET).

    **Pourquoi deux requêtes ?**

    Pagination nécessite deux informations :

    1. **Articles à afficher** (avec LIMIT/OFFSET) → `count()`
    2. **Nombre total** (pour calculer nombre de pages) → `total()`

    **Optimisation MySQL :**

    ```php
    // Requête lourde (scan complet)
    Post::where('status', 'published')->paginate(9);
    // SQL : SELECT COUNT(*) FROM posts WHERE status='published' (scan index)

    // Optimisation avec index sur status
    Schema::table('posts', function (Blueprint $table) {
        $table->index('status');
    });
    // COUNT(*) devient 10x-100x plus rapide
    ```

    **Cas spécial : simplePaginate() :**

    ```php
    $posts = Post::simplePaginate(9);
    // Pas de total() disponible
    // Affiche seulement "Précédent" et "Suivant"
    // 1 seule requête SQL (pas de COUNT)
    ```

    **Avantages simplePaginate :**

    - ✅ Performance (1 requête au lieu de 2)
    - ✅ Scalabilité (pas de COUNT sur millions de lignes)

    **Inconvénients simplePaginate :**

    - ❌ Pas de numéros de pages (1, 2, 3...)
    - ❌ Pas de "Aller à page N"

    **Recommandation :**

    - Blogs/CMS : `paginate()` (meilleure UX)
    - APIs/Feeds : `simplePaginate()` (performance)

??? abstract "**2. Pluralisation Str::plural() - Limitations et Alternatives**"

    **Helper Laravel Str::plural() :**

    ```php
    use Illuminate\Support\Str;

    Str::plural('article', 0); // "articles"
    Str::plural('article', 1); // "article"
    Str::plural('article', 5); // "articles"
    ```

    **Règles basiques (anglais) :**

    ```php
    Str::plural('post');    // "posts"
    Str::plural('child');   // "children" (irrégulier géré)
    Str::plural('person');  // "people" (irrégulier géré)
    Str::plural('ox');      // "oxen" (irrégulier géré)
    ```

    **Problème avec français :**

    ```php
    // Pluriels simples (OK)
    Str::plural('article'); // "articles" ✅
    Str::plural('blog');    // "blogs" ✅

    // Pluriels complexes (FAUX)
    Str::plural('cheval');  // "chevals" ❌ (correct: "chevaux")
    Str::plural('bijou');   // "bijous" ❌ (correct: "bijoux")
    Str::plural('œil');     // "œils" ❌ (correct: "yeux")
    ```

    **Solution 1 : Conditions manuelles (simple)**

    ```html title="Code Blade"
    @if($posts->total() === 0)
        Aucun article
    @elseif($posts->total() === 1)
        1 article
    @else
        {{ $posts->total() }} articles
    @endif
    ```

    **Solution 2 : Helper personnalisé (réutilisable)**

    ```php
    // app/Helpers/TextHelper.php
    namespace App\Helpers;

    class TextHelper
    {
        public static function pluralize($singular, $count, $plural = null)
        {
            if ($count === 1) {
                return $count . ' ' . $singular;
            }
            
            return $count . ' ' . ($plural ?? $singular . 's');
        }
    }
    ```

    **Usage :**

    ```html title="Code Blade"
    {{ TextHelper::pluralize('article', $posts->total()) }}
    // 0 article → "0 articles"
    // 1 article → "1 article"
    // 5 articles → "5 articles"

    {{ TextHelper::pluralize('cheval', 3, 'chevaux') }}
    // "3 chevaux"
    ```

    **Solution 3 : Package spécialisé (professionnel)**

    ```bash
    composer require jdferreira/auto-guesser
    ```

    ```php
    use JDFerreira\AutoGuesser\Pluralizer;

    Pluralizer::pluralize('cheval'); // "chevaux" ✅
    Pluralizer::pluralize('œil');    // "yeux" ✅
    ```

    **Recommandation :**

    - Mots simples (blog, article, post) → `Str::plural()` suffisant
    - Mots complexes français → Helper personnalisé ou package

??? abstract "**3. Route Model Binding avec custom key (slug)**"

    **Configuration dans routes/web.php :**

    ```php
    Route::get('/category/{category:slug}', [CategoryController::class, 'show']);
    ```

    **Syntaxe `{category:slug}` :**

    - `category` : Nom du paramètre (correspond au type-hint contrôleur)
    - `:slug` : Colonne BDD à utiliser pour recherche (au lieu de `id` par défaut)

    **Contrôleur :**

    ```php
    public function show(Category $category)
    {
        // Laravel charge automatiquement via :
        // Category::where('slug', 'technologie')->firstOrFail()
        
        // $category contient déjà l'instance Category
        // Pas besoin de :
        // $category = Category::where('slug', $slug)->firstOrFail();
    }
    ```

    **SQL généré :**

    ```sql
    -- URL : /category/technologie
    SELECT * FROM categories WHERE slug = 'technologie' LIMIT 1
    ```

    **Comparaison avec binding par ID (défaut) :**

    ```php
    // Route avec ID (défaut)
    Route::get('/category/{category}', [CategoryController::class, 'show']);

    // URL : /category/1
    // SQL : SELECT * FROM categories WHERE id = 1 LIMIT 1
    ```

    **Avantages slug vs ID :**

    | Aspect | ID | Slug |
    |--------|-----|------|
    | **SEO** | ❌ `/category/1` (peu descriptif) | ✅ `/category/technologie` (descriptif) |
    | **Lisibilité** | ❌ Incompréhensible humain | ✅ Clair pour humain |
    | **Partage** | ❌ URL cryptique | ✅ URL explicite |
    | **Index unique** | ✅ Clé primaire auto | ✅ Nécessite contrainte UNIQUE |
    | **Performance** | ✅ Index primaire | ⚠️ Index secondaire (légèrement plus lent) |

    **Edge case : Slug non trouvé**

    ```php
    // URL : /category/inexistant
    // Laravel exécute : Category::where('slug', 'inexistant')->firstOrFail()
    // Aucun résultat → Exception ModelNotFoundException
    // Laravel convertit automatiquement en 404 Not Found
    ```

    **Custom 404 message :**

    ```php
    public function show(Category $category)
    {
        // Pas besoin de vérifier manuellement
        // Laravel gère automatiquement 404 si slug invalide
        
        return view('categories.show', compact('category'));
    }
    ```

    **Personnalisation message 404 (optionnel) :**

    ```php
    // Dans le modèle Category
    protected static function boot()
    {
        parent::boot();
        
        static::retrieving(function ($category) {
            if (!$category->exists) {
                abort(404, "Catégorie '{$category->slug}' introuvable.");
            }
        });
    }
    ```

??? abstract "**4. Eager Loading vs Lazy Loading - Impact Performance**"

    **Sans Eager Loading (N+1 problème) :**

    ```php
    // Contrôleur
    $posts = Post::where('category_id', 1)->paginate(9);

    // Vue
    @foreach($posts as $post)
        {{ $post->user->name }} {{-- Déclenche requête SQL --}}
    @endforeach
    ```

    **SQL généré (10 requêtes) :**

    ```sql
    -- Requête 1 : Articles
    SELECT * FROM posts WHERE category_id = 1 LIMIT 9

    -- Requêtes 2-10 : Auteurs (1 par article)
    SELECT * FROM users WHERE id = 1
    SELECT * FROM users WHERE id = 2
    SELECT * FROM users WHERE id = 1  -- Duplication si même auteur
    SELECT * FROM users WHERE id = 3
    SELECT * FROM users WHERE id = 2  -- Duplication
    ...
    ```

    **Problème :**

    - 9 articles → 9 requêtes SQL supplémentaires
    - 100 articles → 100 requêtes SQL supplémentaires
    - Performance catastrophique (temps × 10-100)

    **Avec Eager Loading (optimisé) :**

    ```php
    // Contrôleur
    $posts = Post::where('category_id', 1)->with('user')->paginate(9);
    ```

    **SQL généré (2 requêtes) :**

    ```sql
    -- Requête 1 : Articles
    SELECT * FROM posts WHERE category_id = 1 LIMIT 9

    -- Requête 2 : Auteurs (tous en une fois)
    SELECT * FROM users WHERE id IN (1, 2, 3)
    ```

    **Avantages :**

    - ✅ 2 requêtes au lieu de 10
    - ✅ Pas de duplication (auteurs chargés une fois)
    - ✅ Performance × 5-50 meilleure

    **Eager Loading multiple relations :**

    ```php
    $posts = Post::with(['user', 'category', 'comments'])->paginate(9);
    // 4 requêtes : posts + users + categories + comments
    ```

    **Debug N+1 avec Laravel Debugbar :**

    ```bash
    composer require barryvdh/laravel-debugbar --dev
    ```

    **Détecte automatiquement :**

    - Nombre de requêtes SQL par page
    - Duplicate queries (même requête répétée)
    - Suggestion Eager Loading

<small>**Explication object-cover :** La propriété CSS `object-fit: cover` redimensionne l'image pour **remplir entièrement** le conteneur tout en **préservant le ratio**. Si l'image est trop grande, les parties débordantes sont rognées (crop centré par défaut). Alternative `object-fit: contain` affiche l'image **entière** quitte à laisser espaces vides (letterbox). Pour blog, `cover` préférable car uniformise hauteur cards même si images ont ratios différents. **Pagination offset calculation :** `paginate(9)` génère `LIMIT 9 OFFSET ?` où offset = `(page - 1) × perPage`. Page 1 : OFFSET 0 (articles 1-9), Page 2 : OFFSET 9 (articles 10-18), Page 3 : OFFSET 18 (articles 19-27). **Carbon diffForHumans() locale :** Configure dans `config/app.php` : `'locale' => 'fr'`. Carbon détecte automatiquement et traduit : "2 days ago" → "il y a 2 jours", "1 month ago" → "il y a 1 mois". Personnalisable via fichiers langue `resources/lang/fr/`.</small>

✅ **Étape 6.7 Terminée !**

**Fichier créé :**
- `resources/views/categories/show.blade.php` : Page catégorie avec filtrage et pagination

**Concepts maîtrisés :**
- Route Model Binding avec custom key (`:slug`)
- Pagination Laravel (`paginate()`, `links()`)
- Différence `count()` vs `total()` sur objets paginés
- Eager Loading pour performance (`with()`)
- Pluralisation avec `Str::plural()`
- Grille responsive 3 colonnes
- État vide avec lien retour
- Carbon `diffForHumans()` pour dates relatives

### Étape 6.8 : Créer la Page Auteur (Profil Public et Articles)

**Contexte de l'étape :**

> La page auteur est le **profil public** d'un utilisateur du blog. C'est une page accessible à tous les visiteurs qui présente l'auteur et son contenu. Cette vue joue plusieurs rôles stratégiques :

!!! note "**Rôles fonctionnels :**"

    1. **Identité auteur** : Présente l'auteur avec nom, bio, avatar (humanisation du contenu)
    2. **Crédibilité** : Statistiques (articles publiés, vues, commentaires) prouvent expertise
    3. **Découvrabilité** : Centralise tous les articles d'un auteur (exploration par créateur)
    4. **Social proof** : Compteurs engageants encouragent lecture ("342 vues = populaire")
    5. **SEO** : URLs `/author/{id}` indexées avec contenu auteur (expertise E-A-T)

!!! note "**Architecture de la page :**"

    - **Header profil** : Card avec avatar, nom, bio, statistiques (articles/vues/commentaires)
    - **Bouton édition** : Visible seulement si auteur consulte son propre profil (contexte auth)
    - **Liste articles** : Grille paginée 3 colonnes avec articles publiés uniquement
    - **État vide** : Message si auteur n'a aucun article publié

!!! note "**Différences avec dashboard :**"

    | Aspect | Dashboard (Privé) | Page Auteur (Public) |
    |--------|-------------------|----------------------|
    | **Visibilité** | Seulement l'auteur | Tous les visiteurs |
    | **Articles** | Publiés + Brouillons | Publiés uniquement |
    | **Statistiques** | Complètes (brouillons) | Publiques (publiés) |
    | **Actions** | Modifier/Supprimer | Aucune (lecture seule) |
    | **Mise en page** | Tableau dense | Grille visuelle |
    | **Bouton édition** | Dans header global | Dans profil (si propriétaire) |

!!! note "**Cas d'usage utilisateur :**"

    1. **Visiteur anonyme** : Découvre auteur depuis article → Clique nom auteur → Voit profil + autres articles
    2. **Auteur connecté** : Consulte son propre profil → Voit bouton "Modifier Mon Profil" → Accède édition
    3. **Autre auteur connecté** : Consulte profil collègue → Voit articles publiés → Pas de bouton édition

**Variables disponibles dans la vue :**

Rappel du contrôleur `AuthorController::show()` :

```php
return view('authors.show', compact('user', 'posts', 'stats'));
```

- `$user` : Instance User de l'auteur (injecté via Route Model Binding sur `id`)
- `$posts` : Collection paginée (6 articles/page) articles **publiés** uniquement
- `$stats` : Tableau associatif avec 3 clés :
  - `total_posts` : Nombre d'articles publiés (pas brouillons)
  - `total_views` : Somme vues articles publiés
  - `total_comments` : Somme commentaires articles publiés

**Créer le dossier et le fichier :**

```bash
# Créer le dossier authors
mkdir resources/views/authors

# Le fichier show.blade.php sera créé manuellement
```

**Créer le fichier `resources/views/authors/show.blade.php` :**

```html title="Code Blade"
{{--
|------------------------------------------------------------------------------
| PAGE PROFIL PUBLIC AUTEUR
|------------------------------------------------------------------------------
| Vue publique accessible à tous les visiteurs
| Affiche informations auteur + ses articles publiés
|
| URL : /author/{id}
| Exemple : /author/1 (Alice Dupont)
--}}
@extends('layouts.app')

{{--
| TITRE DYNAMIQUE
| 'Auteur : ' . $user->name : Concaténation PHP
| 
| Résultat <title> : "Mon Blog - Auteur : Alice Dupont"
|
| Note SEO :
| Format "Auteur : [Nom]" aide moteurs comprendre page profil auteur
| Alternative : $user->name directement (plus court)
--}}
@section('title', 'Auteur : ' . $user->name)

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        
        {{--
        |----------------------------------------------------------------------
        | CARD PROFIL AUTEUR
        |----------------------------------------------------------------------
        | Section principale : Présentation auteur avec statistiques
        | mb-8 : Margin-bottom 2rem (espace avant liste articles)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-8">
            {{--
            | CONTENU PROFIL
            | p-8 : Padding 2rem (généreux pour section importante)
            --}}
            <div class="p-8">
                {{--
                | DISPOSITION FLEX RESPONSIVE
                | flex flex-col : Flexbox colonne par défaut (mobile)
                | md:flex-row : Flexbox ligne sur écrans ≥768px (tablet+)
                | items-center : Alignement vertical centré (mobile)
                | md:items-start : Alignement vertical haut (desktop)
                | gap-6 : Espacement 1.5rem entre avatar et infos
                |
                | Progression responsive :
                | Mobile : Colonne (avatar au-dessus, infos en-dessous, centré)
                | Desktop : Ligne (avatar gauche, infos droite, aligné haut)
                |
                | Pourquoi items-start sur desktop ?
                | Avatar grand (128px) + texte long → alignement haut plus naturel
                | items-center créerait espaces vides disgracieux
                --}}
                <div class="flex flex-col md:flex-row items-center md:items-start gap-6">
                    
                    {{--
                    |------------------------------------------------------------------
                    | AVATAR AUTEUR (Image ou Initiale)
                    |------------------------------------------------------------------
                    | flex-shrink-0 : Empêche réduction avatar en flexbox
                    | Garantit taille fixe même si texte déborde
                    --}}
                    <div class="flex-shrink-0">
                        {{--
                        | AVATAR CONDITIONNEL (Image vs Initiale)
                        | @if($user->avatar) : Si colonne avatar non null
                        --}}
                        @if($user->avatar)
                            {{--
                            | IMAGE AVATAR
                            | src="{{ $user->avatar }}" : URL image (stockée en BDD)
                            | alt="{{ $user->name }}" : Texte alternatif (accessibilité)
                            | w-32 h-32 : Largeur/hauteur 8rem (128px)
                            | rounded-full : Bordures arrondies 100% (cercle parfait)
                            | object-cover : Couvre zone sans distorsion (crop centré)
                            |
                            | Taille 128px :
                            | - Assez grande pour voir détails visage
                            | - Pas trop grande (évite dominer page)
                            | - Standard industrie (GitHub, LinkedIn = 120-150px)
                            |
                            | Services avatar supportés :
                            | - Gravatar : https://gravatar.com/avatar/{hash}
                            | - Unsplash : https://source.unsplash.com/128x128/?portrait
                            | - UI Avatars : https://ui-avatars.com/api/?name=Alice+Dupont
                            | - Upload local (futur : Storage::disk('public'))
                            --}}
                            <img src="{{ $user->avatar }}" 
                                 alt="{{ $user->name }}" 
                                 class="w-32 h-32 rounded-full object-cover">
                        @else
                            {{--
                            | AVATAR FALLBACK (Initiale)
                            | Affiché si $user->avatar === null
                            | bg-indigo-100 : Fond indigo clair (couleur primaire)
                            | text-5xl : Taille texte 3rem (48px)
                            | text-indigo-600 : Couleur indigo foncé (contraste)
                            |
                            | substr($user->name, 0, 1) : Extraction 1er caractère
                            | Fonction PHP native : substr(string, start, length)
                            | Exemples :
                            | - "Alice Dupont" → "A"
                            | - "Bob Martin" → "B"
                            | - "Émilie Rousseau" → "É"
                            |
                            | Alternative multi-lettres (initiales prénom + nom) :
                            | $nameParts = explode(' ', $user->name);
                            | $initials = substr($nameParts[0], 0, 1) . substr($nameParts[1] ?? '', 0, 1);
                            | "Alice Dupont" → "AD"
                            |
                            | Pourquoi cercle initiale ?
                            | - Cohérence visuelle (même format que avatars images)
                            | - Identification rapide (couleur + lettre)
                            | - Esthétique moderne (Gmail, Slack, Teams)
                            --}}
                            <div class="w-32 h-32 bg-indigo-100 rounded-full flex items-center justify-center text-5xl text-indigo-600">
                                {{ substr($user->name, 0, 1) }}
                            </div>
                        @endif
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | INFORMATIONS AUTEUR (Texte)
                    |------------------------------------------------------------------
                    | flex-1 : Occupe espace restant (flexbox grow)
                    | text-center md:text-left : Centré mobile, aligné gauche desktop
                    |
                    | Pourquoi centrage mobile ?
                    | - Disposition colonne (avatar au-dessus)
                    | - Centrage plus équilibré visuellement
                    | - Convention mobile (profils centrés)
                    |
                    | Pourquoi alignement gauche desktop ?
                    | - Disposition ligne (avatar à gauche)
                    | - Lecture naturelle gauche→droite
                    | - Cohérence avec reste du contenu
                    --}}
                    <div class="flex-1 text-center md:text-left">
                        {{--
                        | NOM AUTEUR (H1)
                        | text-3xl : Taille texte 1.875rem (30px)
                        | font-bold : Graisse 700
                        | mb-2 : Margin-bottom 0.5rem
                        |
                        | Pourquoi H1 ?
                        | SEO : Chaque page doit avoir UN SEUL H1
                        | Page auteur : H1 = nom auteur (sujet principal)
                        | Aide moteurs identifier expertise/autorité auteur
                        --}}
                        <h1 class="text-3xl font-bold text-gray-900 mb-2">
                            {{ $user->name }}
                        </h1>
                        
                        {{--
                        | BIO AUTEUR (Conditionnelle)
                        | @if($user->bio) : Affiche seulement si bio non null
                        | mb-4 : Margin-bottom 1rem (espace avant statistiques)
                        |
                        | $user->bio : Colonne TEXT (max 65 Ko)
                        | Peut contenir plusieurs paragraphes (sauts de ligne)
                        | {{ }} échappe HTML (protection XSS)
                        |
                        | Alternative affichage multi-paragraphes :
                        | {!! nl2br(e($user->bio)) !!}
                        | Convertit \n en <br> (comme contenu articles)
                        --}}
                        @if($user->bio)
                        <p class="text-gray-600 mb-4">{{ $user->bio }}</p>
                        @endif

                        {{--
                        | STATISTIQUES PUBLIQUES
                        | flex flex-wrap : Flexbox avec retour ligne si besoin
                        | gap-6 : Espacement 1.5rem entre statistiques
                        | justify-center md:justify-start : Centré mobile, gauche desktop
                        | text-sm : Taille texte 0.875rem (14px)
                        |
                        | Pourquoi statistiques publiques ?
                        | - Social proof : "Alice a publié 12 articles" → crédibilité
                        | - Engagement : "342 vues totales" → contenu populaire
                        | - Transparence : Visiteurs voient activité auteur
                        |
                        | Note sécurité :
                        | Affiche SEULEMENT stats articles PUBLIÉS (pas brouillons)
                        | Brouillons = données privées (visibles dashboard uniquement)
                        --}}
                        <div class="flex flex-wrap gap-6 justify-center md:justify-start text-sm">
                            {{--
                            | STAT 1 : NOMBRE D'ARTICLES
                            | font-bold text-indigo-600 : Nombre en gras et indigo (accent)
                            | text-gray-600 : Label en gris (secondaire)
                            |
                            | {{ $stats['total_posts'] }} : Accès tableau associatif
                            | Rappel contrôleur :
                            | 'total_posts' => $user->posts()->published()->count()
                            |
                            | Str::plural('article', $stats['total_posts']) : Pluralisation
                            | 0 articles → "articles"
                            | 1 article → "article"
                            | 5 articles → "articles"
                            --}}
                            <div>
                                <span class="font-bold text-indigo-600">{{ $stats['total_posts'] }}</span>
                                <span class="text-gray-600"> {{ Str::plural('article', $stats['total_posts']) }}</span>
                            </div>
                            {{--
                            | STAT 2 : TOTAL VUES
                            | {{ $stats['total_views'] }} : Somme views_count articles publiés
                            | Rappel contrôleur :
                            | 'total_views' => $user->posts()->published()->sum('views_count')
                            |
                            | Exemple calcul :
                            | Article 1 : 150 vues
                            | Article 2 : 87 vues
                            | Article 3 : 342 vues (le plus populaire)
                            | Total : 579 vues
                            --}}
                            <div>
                                <span class="font-bold text-indigo-600">{{ $stats['total_views'] }}</span>
                                <span class="text-gray-600"> vues</span>
                            </div>
                            {{--
                            | STAT 3 : TOTAL COMMENTAIRES
                            | {{ $stats['total_comments'] }} : Somme commentaires articles publiés
                            | Rappel contrôleur :
                            | 'total_comments' => $user->posts()
                            |                           ->published()
                            |                           ->withCount('comments')
                            |                           ->get()
                            |                           ->sum('comments_count')
                            |
                            | Calcul complexe car relation many-to-many indirecte :
                            | User → Posts → Comments
                            | withCount('comments') ajoute attribut virtuel comments_count
                            | sum('comments_count') additionne tous les compteurs
                            |
                            | Alternative (si pas de withCount) :
                            | $user->posts()->published()->get()->sum(fn($p) => $p->comments->count())
                            |
                            | Str::plural('commentaire', ...) : Pluralisation français
                            | 0 commentaires → "commentaires"
                            | 1 commentaire → "commentaire"
                            | 5 commentaires → "commentaires"
                            --}}
                            <div>
                                <span class="font-bold text-indigo-600">{{ $stats['total_comments'] }}</span>
                                <span class="text-gray-600"> {{ Str::plural('commentaire', $stats['total_comments']) }}</span>
                            </div>
                        </div>

                        {{--
                        |--------------------------------------------------------------
                        | BOUTON ÉDITION (Seulement si Propriétaire)
                        |--------------------------------------------------------------
                        | @auth : Directive Blade = if (auth()->check())
                        | @if(auth()->id() === $user->id) : Vérification ownership
                        |
                        | Logique double condition :
                        | 1. Utilisateur doit être connecté (@auth)
                        | 2. Utilisateur connecté doit être l'auteur de ce profil
                        |
                        | Exemple scénarios :
                        | - Visiteur anonyme → Pas de bouton (pas @auth)
                        | - Alice (id=1) consulte profil Bob (id=2) → Pas de bouton (id ≠)
                        | - Alice (id=1) consulte son profil (id=1) → Bouton visible (id ===)
                        |
                        | Pourquoi triple égal (===) ?
                        | auth()->id() : int 1
                        | $user->id : int 1
                        | 1 === 1 → true
                        |
                        | Alternative (moins stricte mais fonctionne) :
                        | auth()->id() == $user->id (coercition type)
                        --}}
                        @auth
                        @if(auth()->id() === $user->id)
                        <div class="mt-4">
                            {{--
                            | LIEN ÉDITION PROFIL
                            | route('profile.edit') : Génère /profile
                            | bg-gray-800 : Fond gris très foncé (action secondaire)
                            | hover:bg-gray-700 : Fond légèrement plus clair au survol
                            |
                            | Pourquoi gray et pas indigo (primaire) ?
                            | - Action secondaire (pas prioritaire sur page)
                            | - Contexte lecture (visiteur consulte profil)
                            | - Indigo réservé actions principales (créer article)
                            |
                            | Alternative si action importante :
                            | bg-indigo-600 hover:bg-indigo-700 (primaire)
                            --}}
                            <a href="{{ route('profile.edit') }}" 
                               class="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700">
                                ⚙️ Modifier Mon Profil
                            </a>
                        </div>
                        @endif
                        @endauth
                    </div>

                </div>
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | SECTION ARTICLES DE L'AUTEUR
        |----------------------------------------------------------------------
        | Titre section + compteur total
        | mb-6 : Margin-bottom 1.5rem (espace avant grille)
        --}}
        <div class="mb-6">
            {{--
            | TITRE SECTION
            | text-2xl : Taille texte 1.5rem (24px)
            | font-bold : Graisse 700
            |
            | {{ $user->name }} : Nom auteur (personnalisation)
            | {{ $posts->total() }} : Total articles (toutes pages)
            |
            | Résultat : "📝 Articles de Alice Dupont (12)"
            |
            | Pourquoi total() et pas count() ?
            | - total() : Nombre total articles BDD (ex: 12)
            | - count() : Nombre articles page actuelle (ex: 6)
            | Titre section montre volume global, pas juste page actuelle
            --}}
            <h2 class="text-2xl font-bold text-gray-900">
                📝 Articles de {{ $user->name }} ({{ $posts->total() }})
            </h2>
        </div>

        {{--
        | VÉRIFICATION PRÉSENCE D'ARTICLES
        | @if($posts->count() > 0) : Si au moins 1 article sur page actuelle
        --}}
        @if($posts->count() > 0)
            {{--
            | GRILLE ARTICLES RESPONSIVE
            | grid grid-cols-1 : 1 colonne par défaut (mobile)
            | md:grid-cols-2 : 2 colonnes sur écrans ≥768px (tablet)
            | lg:grid-cols-3 : 3 colonnes sur écrans ≥1024px (desktop)
            | gap-6 : Espacement 1.5rem entre cartes
            | mb-8 : Margin-bottom 2rem (espace avant pagination)
            |
            | Même disposition que page catégorie :
            | - Mobile : 1 colonne (défilement vertical)
            | - Tablet : 2 colonnes (compromis)
            | - Desktop : 3 colonnes (vue d'ensemble)
            |
            | Différence avec dashboard :
            | Dashboard : Tableau (dense, données tabulaires)
            | Page auteur : Grille (visuelle, découverte contenu)
            --}}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {{--
                | BOUCLE SUR ARTICLES
                | @foreach($posts as $post) : Itère sur Collection paginée
                | $posts : 6 articles maximum par page (défini dans contrôleur)
                --}}
                @foreach($posts as $post)
                {{--
                | CARD ARTICLE
                | hover:shadow-md : Ombre moyenne au survol
                | transition : Animation douce 150ms
                --}}
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg hover:shadow-md transition">
                    {{--
                    | IMAGE COUVERTURE (Conditionnelle)
                    | @if($post->image) : Affiche seulement si image non null
                    --}}
                    @if($post->image)
                    <div class="h-48 bg-gray-200 overflow-hidden">
                        <img src="{{ $post->image }}" alt="{{ $post->title }}" class="w-full h-full object-cover">
                    </div>
                    @endif
                    
                    {{--
                    | CONTENU CARD
                    | p-6 : Padding 1.5rem (toutes directions)
                    --}}
                    <div class="p-6">
                        {{--
                        | BADGE CATÉGORIE
                        | inline-block : Force comportement bloc (pour padding)
                        | px-3 py-1 : Padding horizontal 0.75rem, vertical 0.25rem
                        | rounded-full : Bordures complètement arrondies (pilule)
                        | mb-3 : Margin-bottom 0.75rem (espace sous badge)
                        |
                        | route('categories.show', $post->category->slug)
                        | Génère : /category/{slug}
                        | Exemple : /category/technologie
                        |
                        | $post->category : Relation belongsTo chargée via Eager Loading
                        | Rappel contrôleur : ->with('category')
                        | Sans with() : N+1 problème (1 requête par article)
                        --}}
                        <a href="{{ route('categories.show', $post->category->slug) }}" 
                           class="inline-block px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-semibold rounded-full mb-3">
                            {{ $post->category->name }}
                        </a>
                        
                        {{--
                        | TITRE ARTICLE
                        | text-xl : Taille texte 1.25rem (20px)
                        | font-bold : Graisse 700
                        | mb-2 : Margin-bottom 0.5rem
                        |
                        | {{ $post->title }} : Titre complet (pas de Str::limit ici)
                        | Pourquoi pas de troncature ?
                        | - Cards grande (1/3 largeur desktop)
                        | - Espace suffisant pour titres longs
                        | - Meilleur SEO (titre complet)
                        |
                        | Alternative si titres trop longs :
                        | {{ Str::limit($post->title, 50) }}
                        --}}
                        <h3 class="text-xl font-bold text-gray-900 mb-2">
                            <a href="{{ route('posts.show', $post->slug) }}" class="hover:text-indigo-600">
                                {{ $post->title }}
                            </a>
                        </h3>
                        
                        {{--
                        | EXCERPT (Résumé)
                        | text-gray-600 : Gris moyen (contenu secondaire)
                        | text-sm : Taille texte 0.875rem (14px)
                        | mb-4 : Margin-bottom 1rem (espace avant méta)
                        |
                        | Str::limit($post->excerpt, 120) : Tronque à 120 caractères
                        | Évite débordement si excerpt trop long
                        | Rappel BDD : excerpt = TEXT (max 65 Ko)
                        | Mais formulaire création limite à 500 caractères (maxlength)
                        |
                        | Pourquoi 120 caractères ?
                        | - Cards 1/3 largeur (3 colonnes)
                        | - ~2-3 lignes de texte (lisibilité optimale)
                        | - Incite clic pour lire suite
                        |
                        | Alternative : Pas de limite (affiche excerpt complet)
                        | {{ $post->excerpt }}
                        --}}
                        <p class="text-gray-600 text-sm mb-4">
                            {{ Str::limit($post->excerpt, 120) }}
                        </p>
                        
                        {{--
                        | MÉTA INFORMATIONS (Date + Stats)
                        | flex items-center justify-between : Répartit espace
                        | text-xs : Taille texte 0.75rem (12px)
                        | text-gray-500 : Gris clair (info tertiaire)
                        --}}
                        <div class="flex items-center justify-between text-xs text-gray-500">
                            {{--
                            | DATE PUBLICATION
                            | {{ $post->published_at->format('d M Y') }} : Format fixe
                            |
                            | Différence avec diffForHumans() :
                            | - format('d M Y') : "10 Déc 2024" (précis)
                            | - diffForHumans() : "il y a 2 jours" (relatif)
                            |
                            | Pourquoi format fixe ici ?
                            | - Profil auteur = contexte temporel (chronologie)
                            | - Dates précises aident voir évolution activité
                            | - Pas besoin de "il y a X jours" (pas article individuel)
                            |
                            | Alternative : diffForHumans() si préféré
                            | {{ $post->published_at->diffForHumans() }}
                            --}}
                            <span>{{ $post->published_at->format('d M Y') }}</span>
                            {{--
                            | COMPTEURS (Vues + Commentaires)
                            | 👁️ : Emoji œil (vues)
                            | 💬 : Emoji bulle (commentaires)
                            |
                            | {{ $post->views_count }} : Colonne BDD BIGINT UNSIGNED
                            | {{ $post->comments->count() }} : Relation hasMany
                            |
                            | Pourquoi ->count() sur comments ?
                            | Relation chargée via Eager Loading dans contrôleur
                            | $posts->load('comments') (optionnel mais recommandé)
                            | Sans load() : N+1 problème (1 requête par article)
                            |
                            | Alternative (si pas de load) :
                            | Ajouter withCount('comments') dans contrôleur
                            | Afficher {{ $post->comments_count }}
                            --}}
                            <div>
                                👁️ {{ $post->views_count }} • 💬 {{ $post->comments->count() }}
                            </div>
                        </div>
                    </div>
                </div>
                @endforeach
            </div>

            {{--
            | PAGINATION
            | mt-6 : Margin-top 1.5rem (espace après grille)
            | {{ $posts->links() }} : Génère HTML pagination automatiquement
            |
            | Même fonctionnement que page catégorie :
            | - Détecte paramètre ?page=N dans URL
            | - Charge 6 articles page actuelle
            | - Génère boutons Précédent/Suivant + numéros pages
            --}}
            <div class="mt-6">
                {{ $posts->links() }}
            </div>
        
        {{--
        | ÉTAT VIDE (Aucun Article Publié)
        | @else : Alternative au @if (si $posts->count() === 0)
        --}}
        @else
            {{--
            | MESSAGE ÉTAT VIDE
            | p-8 : Padding 2rem (espacement généreux)
            | text-center : Centrage horizontal
            |
            | {{ $user->name }} : Nom auteur (personnalisation message)
            | "Alice Dupont n'a pas encore publié d'articles."
            |
            | Cas d'usage :
            | - Nouvel auteur (vient de s'inscrire, aucun article)
            | - Auteur inactif (tous articles en brouillon ou supprimés)
            | - Bug/test (compte test sans contenu)
            --}}
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-8 text-center">
                <p class="text-gray-600">{{ $user->name }} n'a pas encore publié d'articles.</p>
            </div>
        @endif

    </div>
</div>
@endsection
```

**Tableau Comparatif Dashboard vs Page Auteur**

| Aspect | Dashboard (Privé) | Page Auteur (Public) |
|--------|-------------------|----------------------|
| **Route** | `/dashboard` (auth requis) | `/author/{id}` (public) |
| **Articles affichés** | Publiés + Brouillons | Publiés uniquement |
| **Statistiques** | Total (incluant brouillons) | Publiés uniquement |
| **Avatar** | Non affiché | Affiché (cercle 128px) |
| **Bio** | Non affichée | Affichée si présente |
| **Layout articles** | Tableau HTML (dense) | Grille 3 colonnes (visuelle) |
| **Pagination** | Non (liste complète) | Oui (6 par page) |
| **Actions** | Modifier, Supprimer | Aucune (lecture seule) |
| **Bouton édition** | Header global | Profil (si propriétaire) |
| **Visibilité** | Seulement l'auteur | Tous les visiteurs |
| **SEO** | Non indexé (auth) | Indexé (URLs publiques) |

**Explications Techniques Approfondies**

??? abstract "**1. Pourquoi 6 articles par page au lieu de 9 ?**"

    **Contexte :**

    Page catégorie : `paginate(9)` (grille 3×3)  
    Page auteur : `paginate(6)` (grille 3×2)

    **Justification différence :**

    | Critère | Page Catégorie | Page Auteur |
    |---------|----------------|-------------|
    | **Focus** | Découverte large (toute thématique) | Focus auteur (personne spécifique) |
    | **Contenu** | Variété auteurs (perspectives multiples) | Un seul auteur (style cohérent) |
    | **Scroll** | Plus de scroll acceptable (exploration) | Moins de scroll (profil + articles) |
    | **Performance** | Volume potentiellement élevé | Volume généralement modéré |

    **Règle générale pagination :**

    - **Pages exploration** (catégories, recherche, archives) : 9-12 articles
    - **Pages focus** (auteur, tag, série) : 6-9 articles
    - **Homepage** : 9-15 articles (première impression)
    - **Flux RSS** : 10-20 articles (agrégateurs)

    **Alternative responsive :**

    ```php
    // Contrôleur
    $perPage = request()->input('per_page', 6); // ?per_page=12
    $posts = $user->posts()->published()->paginate($perPage);
    ```

    **Permet utilisateur choisir :**

    - ?per_page=6 (défaut)
    - ?per_page=12 (vue dense)
    - ?per_page=24 (power users)

??? abstract "**2. Gestion Avatar : Image vs Initiale vs Placeholder**"

    **Solution 1 : Image conditionnelle avec initiale fallback (implémentée)**

    ```html title="Code Blade"
    @if($user->avatar)
        <img src="{{ $user->avatar }}" class="w-32 h-32 rounded-full">
    @else
        <div class="w-32 h-32 bg-indigo-100 rounded-full">
            {{ substr($user->name, 0, 1) }}
        </div>
    @endif
    ```

    **Avantages :**

    - ✅ Simple (pas de service externe)
    - ✅ Toujours visible (initiale comme fallback)
    - ✅ Cohérence design (même format cercle)

    **Inconvénients :**

    - ❌ Basique (1 seule lettre)
    - ❌ Pas de variation couleur (tous indigo-100)

    **Solution 2 : Gravatar avec initiale fallback**

    ```html title="Code Blade"
    @php
        $gravatarHash = md5(strtolower(trim($user->email)));
        $gravatarUrl = "https://www.gravatar.com/avatar/{$gravatarHash}?s=128&d=404";
    @endphp

    <img src="{{ $gravatarUrl }}" 
        alt="{{ $user->name }}"
        onerror="this.onerror=null; this.src='{{ asset('images/default-avatar.png') }}';"
        class="w-32 h-32 rounded-full">
    ```

    **Avantages :**

    - ✅ Service gratuit universel
    - ✅ Utilisateurs reconnaissent leur avatar (si Gravatar configuré)
    - ✅ Fallback automatique (onerror)

    **Inconvénients :**

    - ❌ Dépendance service externe (Gravatar down = avatars cassés)
    - ❌ Requête HTTP supplémentaire (latence)

    **Solution 3 : UI Avatars API (générateur dynamique)**

    ```html title="Code Blade"
    @php
        $initials = substr($user->name, 0, 2);
        $avatarUrl = "https://ui-avatars.com/api/?name=" . urlencode($user->name) . "&size=128&background=6366f1&color=fff";
    @endphp

    <img src="{{ $avatarUrl }}" class="w-32 h-32 rounded-full">
    ```

    **Génère automatiquement :**

    - Initiales multi-lettres ("AD" pour "Alice Dupont")
    - Couleur fond aléatoire (basée sur nom)
    - Haute résolution (paramètre size)

    **Avantages :**

    - ✅ Avatars distincts visuellement (couleurs variées)
    - ✅ Initiales complètes (2-3 lettres)
    - ✅ Service gratuit sans compte

    **Inconvénients :**

    - ❌ Dépendance externe (API down = problème)
    - ❌ RGPD/Privacy (nom envoyé à service tiers)

    **Solution 4 : Upload local (professionnel)**

    ```php
    // Contrôleur ProfileController::update()
    if ($request->hasFile('avatar')) {
        $path = $request->file('avatar')->store('avatars', 'public');
        $user->avatar = Storage::url($path);
    }
    ```

    **Avantages :**

    - ✅ Contrôle total (pas de dépendance externe)
    - ✅ Performance (fichiers locaux)
    - ✅ Privacy (données restent sur serveur)

    **Inconvénients :**

    - ❌ Stockage serveur (coût disque)
    - ❌ Validation nécessaire (taille, type, malware)
    - ❌ Redimensionnement requis (intervention/image package)

    **Recommandation :**

    | Projet | Solution |
    |--------|----------|
    | **Prototype/MVP** | Initiale simple (implémentée) |
    | **Blog communautaire** | Gravatar + fallback |
    | **Application professionnelle** | Upload local + validation |
    | **SaaS/Startup** | Service CDN (Cloudinary, imgix) |

??? abstract "**3. Double condition @auth + ownership**"

    **Syntaxe :**

    ```html title="Code Blade"
    @auth
    @if(auth()->id() === $user->id)
        <a href="{{ route('profile.edit') }}">Modifier</a>
    @endif
    @endauth
    ```

    **Pourquoi deux conditions séparées ?**

    **Scénario 1 : Une seule condition (incorrect)**

    ```html title="Code Blade"
    @if(auth()->check() && auth()->id() === $user->id)
        <a href="{{ route('profile.edit') }}">Modifier</a>
    @endif
    ```

    **Problème :**

    Si utilisateur non connecté :
    - `auth()->check()` → `false`
    - `auth()->id()` → `null`
    - `null === $user->id` → `false`
    - **Résultat correct mais inélégant**

    **Scénario 2 : Deux conditions imbriquées (correct)**

    ```html title="Code Blade"
    @auth
        @if(auth()->id() === $user->id)
            <a href="{{ route('profile.edit') }}">Modifier</a>
        @endif
    @endauth
    ```

    **Avantages :**

    1. **Lisibilité** : Intention claire (connecté + propriétaire)
    2. **Performance** : `@auth` court-circuite (pas de vérification id si non connecté)
    3. **Blade idiomatique** : Directive `@auth` recommandée Laravel

    **Alternative avec gate/policy (avancé) :**

    ```php
    // App\Policies\UserPolicy
    public function update(User $authUser, User $user)
    {
        return $authUser->id === $user->id;
    }
    ```

    ```html title="Code Blade"
    @can('update', $user)
        <a href="{{ route('profile.edit') }}">Modifier</a>
    @endcan
    ```

    **Avantages policy :**

    - ✅ Logique centralisée (testable unitairement)
    - ✅ Réutilisable (contrôleurs + vues)
    - ✅ Évolution facile (ajout rôles admin, etc.)

??? abstract "**4. Statistiques publiques vs privées - Sécurité données**"

    **Statistiques dashboard (privées) :**

    ```php
    $stats = [
        'total_posts' => $posts->count(),              // Inclut brouillons
        'published_posts' => $posts->where('status', 'published')->count(),
        'draft_posts' => $posts->where('status', 'draft')->count(),
        'total_views' => $posts->sum('views_count'),   // Toutes vues
    ];
    ```

    **Statistiques page auteur (publiques) :**

    ```php
    $stats = [
        'total_posts' => $user->posts()->published()->count(),     // Publiés uniquement
        'total_views' => $user->posts()->published()->sum('views_count'),
        'total_comments' => $user->posts()->published()->withCount('comments')->get()->sum('comments_count'),
    ];
    ```

    **Différences critiques :**

    | Donnée | Dashboard (Privé) | Page Auteur (Public) |
    |--------|-------------------|----------------------|
    | **Brouillons** | ✅ Affichés | ❌ Masqués |
    | **Vues brouillons** | ✅ Comptées | ❌ Exclues |
    | **Commentaires brouillons** | ✅ Comptés | ❌ Exclus |
    | **Articles supprimés** | ❌ Exclus | ❌ Exclus |

    **Pourquoi masquer brouillons publiquement ?**

    **Sécurité :**

    - Brouillons = travail en cours (pas finalisé)
    - Peuvent contenir infos sensibles/confidentielles
    - Révèlent stratégie éditoriale (concurrents)

    **UX :**

    - Visiteurs attendent contenu publié (qualité)
    - Compter brouillons trompe visiteur (fausse promesse)
    - "12 articles" dont 8 brouillons = frustration

    **Alternative : Statistiques avancées (optionnel)**

    ```html title="Code Blade"
    {{-- Page auteur --}}
    <div>
        <span>{{ $stats['total_posts'] }} articles</span>
        <span>Publié son premier article {{ $firstPostDate->diffForHumans() }}</span>
        <span>Dernier article {{ $lastPostDate->diffForHumans() }}</span>
    </div>
    ```

    **Ajout contexte temporel :**

    - "Premier article il y a 2 ans" → auteur expérimenté
    - "Dernier article il y a 3 jours" → auteur actif

??? abstract "**5. Format date : format() vs diffForHumans() selon contexte**"

    **format() - Date précise :**

    ```html title="Code Blade"
    {{ $post->published_at->format('d M Y') }}
    // "10 Déc 2024"
    ```

    **Cas d'usage :**

    - ✅ Listes chronologiques (archives, profil auteur)
    - ✅ Événements futurs (date limite, lancement)
    - ✅ Contexte légal/contractuel (publication, signature)

    **diffForHumans() - Date relative :**

    ```html title="Code Blade"
    {{ $post->published_at->diffForHumans() }}
    // "il y a 2 jours"
    ```

    **Cas d'usage :**

    - ✅ Flux actualité (articles récents)
    - ✅ Commentaires (interaction récente)
    - ✅ Notifications (événement proche)

    **Tableau décisionnel :**

    | Page | Format | Raison |
    |------|--------|--------|
    | Page d'accueil | `diffForHumans()` | Actualité, récence importante |
    | Page article | `diffForHumans()` | Contexte lecture, engagement |
    | Page catégorie | `diffForHumans()` | Exploration, découverte |
    | **Page auteur** | `format()` | **Chronologie, portfolio** |
    | Dashboard | `format()` | Gestion, dates précises |
    | Archives | `format()` | Organisation temporelle |
    | Recherche | `format()` | Tri, comparaison dates |

    **Pourquoi format() sur page auteur ?**

    Page auteur = **portfolio chronologique** de l'auteur :

    - Visiteur explore historique publications
    - Dates précises aident voir évolution activité
    - "10 Déc 2024" plus informatif que "il y a 2 jours"

    **Alternative hybride (meilleur des deux mondes) :**

    ```html title="Code Blade"
    <span title="{{ $post->published_at->format('d M Y H:i') }}">
        {{ $post->published_at->diffForHumans() }}
    </span>
    ```

    **Résultat :**

    - Affichage : "il y a 2 jours"
    - Tooltip (survol) : "10 Déc 2024 14:30"

<small>**Explication substr() multi-bytes :** `substr($user->name, 0, 1)` extrait 1 byte, pas 1 caractère. Pour UTF-8 (accents, émojis), utilisez `mb_substr($user->name, 0, 1, 'UTF-8')`. Exemple : "Émilie" → `substr()` retourne `"�"` (byte incomplet), `mb_substr()` retourne `"É"` (caractère complet). **Eager Loading relations :** `$posts->load('comments')` charge relation APRÈS récupération initiale. Alternative : `$posts = Post::with('comments')->paginate(6)` charge relation PENDANT requête initiale. Résultat identique mais `with()` plus performant (1 requête SQL au lieu de 2). **Policy update vs view :** Policy `update()` vérifie "peut modifier", `view()` vérifie "peut voir". Page auteur publique utilise pas de policy car visible tous. Bouton édition utilise simple condition `auth()->id() === $user->id` suffisante pour ce cas.</small>

✅ **Étape 6.8 Terminée !**

**Fichier créé :**
- `resources/views/authors/show.blade.php` : Page profil public auteur avec articles

**Concepts maîtrisés :**
- Avatar conditionnel (image vs initiale fallback)
- Statistiques publiques filtrées (articles publiés uniquement)
- Double condition `@auth` + ownership pour bouton édition
- Grille responsive 3 colonnes (6 articles/page)
- Pagination sur profil auteur
- Format date précis (`format()`) pour contexte chronologique
- Eager Loading optimisé (`with('category')`)
- Différenciation dashboard privé vs profil public

### Étape 6.9 : Créer la Page Édition Profil Utilisateur (Paramètres Compte)

**Contexte de l'étape :**

> La page d'édition du profil est l'**espace de configuration personnel** de l'utilisateur. C'est ici qu'il peut modifier ses informations publiques, changer son mot de passe et gérer son compte. Cette vue est critique car elle touche à la **sécurité** et aux **données personnelles**.

!!! note "**Architecture de la page :**"

    La page est divisée en **3 sections distinctes** :

    1. **Informations du profil** : Nom, email, bio, avatar (données publiques)
    2. **Modifier le mot de passe** : Ancien password + nouveau password (sécurité)
    3. **Supprimer le compte** : Zone dangereuse avec confirmation (action irréversible)

!!! info "**Pourquoi 3 formulaires séparés ?**"

    - **Séparation des responsabilités** : Chaque formulaire a une route et validation différente
    - **Sécurité** : Changement password nécessite confirmation ancien password
    - **UX** : Utilisateur peut mettre à jour profil sans changer password
    - **Validation différenciée** : Règles distinctes (email unique vs password min 8 chars)

!!! note "**Pattern "Settings Page" :**"

    Cette structure est un **standard industrie** (GitHub, Twitter, Gmail, LinkedIn) :

    - Section profile → Infos visibles publiquement
    - Section security → Password, 2FA, sessions
    - Section danger zone → Suppression compte, révocation accès

**Variables disponibles dans la vue :**

Rappel du contrôleur `ProfileController::edit()` :

```php
return view('profile.edit', ['user' => $request->user()]);
```

- `$user` : Instance User de l'utilisateur connecté (via `$request->user()`)
- Alternative : `auth()->user()` (même résultat)

**Routes utilisées :**

```php
// Afficher formulaire
GET /profile → ProfileController::edit()

// Mettre à jour profil
PATCH /profile → ProfileController::update()

// Changer password
PUT /password → PasswordController::update() (Breeze)

// Supprimer compte
DELETE /profile → ProfileController::destroy()
```

**Ouvrir `resources/views/profile/edit.blade.php`** (créé par Breeze) et **remplacer TOUT le contenu** par :

```html title="Code Blade"
{{--
|------------------------------------------------------------------------------
| PAGE ÉDITION PROFIL UTILISATEUR
|------------------------------------------------------------------------------
| Vue privée accessible uniquement à l'utilisateur connecté
| Permet modification infos personnelles, password et suppression compte
|
| Structure : 3 formulaires indépendants (3 routes distinctes)
--}}
@extends('layouts.app')

@section('title', 'Modifier Mon Profil')

@section('content')
<div class="py-12">
    {{--
    | CONTENEUR FORMULAIRES (Largeur Moyenne)
    | max-w-3xl : Largeur max 48rem (768px)
    | Plus étroit que page d'accueil (meilleure concentration formulaires)
    | Largeur formulaire optimale : 600-800px (études UX)
    --}}
    <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
        
        {{--
        | TITRE PAGE
        | mb-8 : Margin-bottom 2rem (espace avant première section)
        --}}
        <h1 class="text-3xl font-bold text-gray-900 mb-8">⚙️ Paramètres du Compte</h1>

        {{--
        |----------------------------------------------------------------------
        | SECTION 1 : INFORMATIONS DU PROFIL
        |----------------------------------------------------------------------
        | Formulaire modification données publiques (nom, email, bio, avatar)
        | mb-6 : Margin-bottom 1.5rem (espace avant section suivante)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
            {{--
            | CONTENU SECTION
            | p-8 : Padding 2rem (toutes directions)
            --}}
            <div class="p-8">
                {{--
                | TITRE SECTION
                | text-xl : Taille texte 1.25rem (20px)
                | font-bold : Graisse 700
                | mb-6 : Margin-bottom 1.5rem (espace avant formulaire)
                --}}
                <h2 class="text-xl font-bold text-gray-900 mb-6">Informations du Profil</h2>

                {{--
                | FORMULAIRE MISE À JOUR PROFIL
                | action : route('profile.update') → /profile
                | method : POST (HTML standard)
                | @method('PATCH') : Spoofing pour Laravel (requête PATCH)
                |
                | Pourquoi PATCH et pas POST ?
                | Convention REST :
                | - POST : Créer nouvelle ressource
                | - PUT : Remplacer entièrement ressource
                | - PATCH : Modifier partiellement ressource
                |
                | Ici : Modification partielle (seulement champs soumis)
                | PATCH sémantiquement correct
                --}}
                <form action="{{ route('profile.update') }}" method="POST">
                    @csrf
                    {{--
                    | @method('PATCH') : Génère <input type="hidden" name="_method" value="PATCH">
                    | Laravel détecte ce champ et route vers Route::patch()
                    --}}
                    @method('PATCH')

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP NOM
                    |------------------------------------------------------------------
                    | mb-6 : Margin-bottom 1.5rem (espacement entre champs)
                    --}}
                    <div class="mb-6">
                        {{--
                        | LABEL
                        | for="name" : Associe label au champ (clic label = focus input)
                        | block : Force affichage bloc (occupe ligne complète)
                        | mb-2 : Margin-bottom 0.5rem (espace label-input)
                        --}}
                        <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                            Nom *
                        </label>
                        {{--
                        | INPUT NOM
                        | value="{{ old('name', $user->name) }}" : Pré-remplissage
                        |
                        | Logique :
                        | 1. Si erreur validation → old('name') existe → affiche valeur soumise
                        | 2. Sinon → old('name') null → utilise $user->name (BDD)
                        |
                        | Exemple scénario :
                        | - Utilisateur change "Alice" → "Alice Dupont Martin"
                        | - Soumet avec email invalide
                        | - Retour formulaire : old('name') = "Alice Dupont Martin"
                        | - Le champ affiche "Alice Dupont Martin" (pas "Alice")
                        |
                        | required : Attribut HTML5 (validation navigateur)
                        | Laravel valide aussi côté serveur (required dans $request->validate())
                        --}}
                        <input type="text" 
                               name="name" 
                               id="name" 
                               value="{{ old('name', $user->name) }}"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        {{--
                        | AFFICHAGE ERREUR VALIDATION
                        | @error('name') : Directive Blade = if ($errors->has('name'))
                        | $message : Variable auto contenant message erreur
                        |
                        | Messages définis dans contrôleur via validate() ou messages personnalisés
                        --}}
                        @error('name')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP EMAIL
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                            Email *
                        </label>
                        {{--
                        | INPUT EMAIL
                        | type="email" : Validation HTML5 format email
                        | value="{{ old('email', $user->email) }}" : Pré-remplissage
                        |
                        | Validation serveur (contrôleur) :
                        | 'email' => ['required', 'email', Rule::unique('users')->ignore($user->id)]
                        |
                        | Rule::unique()->ignore() : Email doit être unique SAUF pour utilisateur actuel
                        | Permet de garder son propre email sans erreur "déjà utilisé"
                        --}}
                        <input type="email" 
                               name="email" 
                               id="email" 
                               value="{{ old('email', $user->email) }}"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        @error('email')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                        
                        {{--
                        | AVERTISSEMENT VÉRIFICATION EMAIL
                        | @if ($user->isDirty('email')) : Si email modifié mais pas sauvegardé
                        |
                        | isDirty('email') : Méthode Eloquent qui retourne true si :
                        | - La colonne email a été modifiée dans l'instance $user
                        | - Les changements ne sont pas encore sauvegardés en BDD
                        |
                        | Scénario :
                        | 1. Utilisateur soumet formulaire avec nouvel email
                        | 2. Contrôleur valide et met à jour $user->email
                        | 3. $user->save() sauvegarde en BDD
                        | 4. Si email change, email_verified_at réinitialisé à null
                        | 5. Utilisateur redirigé vers profile.edit
                        | 6. $user->isDirty('email') = false (déjà sauvegardé)
                        |
                        | Note : Ce bloc n'est généralement PAS affiché car isDirty() = false après save()
                        | Conservé pour cohérence avec template Breeze standard
                        --}}
                        @if ($user->isDirty('email'))
                        <p class="text-sm text-gray-600 mt-1">
                            Votre adresse email n'est pas vérifiée. 
                            {{--
                            | BOUTON RENVOYER EMAIL VÉRIFICATION
                            | type="submit" : Soumet formulaire parent (formulaire profil)
                            |
                            | Note : Ce bouton soumet le formulaire de mise à jour profil
                            | Il ne renvoie PAS directement l'email de vérification
                            | Logique renvoi email gérée par routes Breeze séparées
                            --}}
                            <button type="submit" class="text-indigo-600 hover:text-indigo-800">
                                Cliquez ici pour renvoyer l'email de vérification.
                            </button>
                        </p>
                        @endif
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP BIOGRAPHIE (Optionnel)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="bio" class="block text-sm font-medium text-gray-700 mb-2">
                            Biographie (optionnel)
                        </label>
                        {{--
                        | TEXTAREA BIO
                        | rows="4" : Hauteur initiale 4 lignes
                        | maxlength="500" : Limite HTML5 (500 caractères max)
                        | placeholder : Texte d'exemple (disparaît au focus)
                        |
                        | {{ old('bio', $user->bio) }} : Pré-remplissage
                        | Entre balises textarea (PAS value="")
                        |
                        | Validation serveur (contrôleur) :
                        | 'bio' => 'nullable|string|max:500'
                        | nullable : Champ optionnel (peut être null)
                        --}}
                        <textarea name="bio" 
                                  id="bio" 
                                  rows="4"
                                  maxlength="500"
                                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                  placeholder="Parlez un peu de vous...">{{ old('bio', $user->bio) }}</textarea>
                        @error('bio')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                        {{--
                        | AIDE CONTEXTUELLE
                        | text-xs : Taille texte 0.75rem (12px)
                        | text-gray-500 : Gris clair (info tertiaire)
                        | mt-1 : Margin-top 0.25rem
                        --}}
                        <p class="text-xs text-gray-500 mt-1">Visible sur votre profil public (max 500 caractères)</p>
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP AVATAR URL (Optionnel)
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="avatar" class="block text-sm font-medium text-gray-700 mb-2">
                            URL Avatar (optionnel)
                        </label>
                        {{--
                        | INPUT URL AVATAR
                        | type="url" : Validation HTML5 format URL (http:// ou https://)
                        | placeholder : URL exemple
                        |
                        | Validation serveur (contrôleur) :
                        | 'avatar' => 'nullable|url'
                        | nullable : Champ optionnel (peut être null)
                        | url : Doit être URL valide si fourni
                        |
                        | Services avatar gratuits :
                        | - Gravatar : https://gravatar.com (basé sur email)
                        | - Unsplash : https://source.unsplash.com/128x128/?portrait
                        | - UI Avatars : https://ui-avatars.com/api/?name=Alice+Dupont
                        | - Placeholder : https://i.pravatar.cc/128?img=1
                        --}}
                        <input type="url" 
                               name="avatar" 
                               id="avatar" 
                               value="{{ old('avatar', $user->avatar) }}"
                               placeholder="https://exemple.com/avatar.jpg"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                        @error('avatar')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                        {{--
                        | AIDE CONTEXTUELLE AVEC LIEN
                        | target="_blank" : Ouvre lien dans nouvel onglet
                        | rel="noopener noreferrer" : Sécurité (pas ajouté ici mais recommandé)
                        --}}
                        <p class="text-xs text-gray-500 mt-1">
                            Utilisez <a href="https://gravatar.com" target="_blank" class="text-indigo-600">Gravatar</a> ou une URL d'image
                        </p>
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | BOUTON SAUVEGARDER
                    |------------------------------------------------------------------
                    | flex items-center justify-end : Aligne bouton à droite
                    --}}
                    <div class="flex items-center justify-end">
                        {{--
                        | BOUTON SOUMETTRE
                        | type="submit" : Soumet le formulaire
                        | px-6 py-3 : Padding généreux (bouton principal)
                        | bg-indigo-600 : Fond indigo (action principale)
                        | hover:bg-indigo-700 : Fond plus foncé au survol
                        --}}
                        <button type="submit" 
                                class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                            Sauvegarder les modifications
                        </button>
                    </div>

                </form>
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | SECTION 2 : MODIFIER LE MOT DE PASSE
        |----------------------------------------------------------------------
        | Formulaire changement password (nécessite ancien password)
        | mb-6 : Margin-bottom 1.5rem (espace avant section suivante)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
            <div class="p-8">
                <h2 class="text-xl font-bold text-gray-900 mb-6">Modifier le Mot de Passe</h2>

                {{--
                | FORMULAIRE CHANGEMENT PASSWORD
                | action : route('password.update') → /password
                | method : POST + @method('PUT')
                |
                | Note : route('password.update') est définie par Laravel Breeze
                | Gérée par PasswordController::update() (pas ProfileController)
                |
                | Pourquoi formulaire séparé ?
                | - Sécurité : Nécessite confirmation ancien password
                | - Validation différente : Règles password distinctes
                | - Route distincte : /password vs /profile
                --}}
                <form action="{{ route('password.update') }}" method="POST">
                    @csrf
                    @method('PUT')

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP MOT DE PASSE ACTUEL
                    |------------------------------------------------------------------
                    | Requis pour vérifier que c'est bien l'utilisateur (pas usurpateur)
                    --}}
                    <div class="mb-6">
                        <label for="current_password" class="block text-sm font-medium text-gray-700 mb-2">
                            Mot de passe actuel *
                        </label>
                        {{--
                        | INPUT PASSWORD
                        | type="password" : Masque la saisie (points/astérisques)
                        | autocomplete="current-password" : Aide gestionnaires passwords
                        |
                        | Pas de value (jamais pré-remplir passwords)
                        | Sécurité : Password ne doit jamais apparaître en clair dans HTML
                        |
                        | Validation serveur (Breeze) :
                        | 'current_password' => ['required', 'current_password']
                        | current_password : Règle Laravel qui vérifie hash BDD
                        --}}
                        <input type="password" 
                               name="current_password" 
                               id="current_password"
                               autocomplete="current-password"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        {{--
                        | ERREUR VALIDATION
                        | @error('current_password') : Affiche si ancien password incorrect
                        | Message typique : "Le mot de passe actuel est incorrect."
                        --}}
                        @error('current_password')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP NOUVEAU MOT DE PASSE
                    |------------------------------------------------------------------
                    --}}
                    <div class="mb-6">
                        <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                            Nouveau mot de passe *
                        </label>
                        {{--
                        | INPUT NOUVEAU PASSWORD
                        | name="password" : Nom standard Laravel (attendu par validation)
                        | autocomplete="new-password" : Aide gestionnaires passwords
                        |
                        | Validation serveur (Breeze) :
                        | 'password' => ['required', 'string', 'min:8', 'confirmed']
                        | min:8 : Minimum 8 caractères
                        | confirmed : Doit correspondre à password_confirmation
                        --}}
                        <input type="password" 
                               name="password" 
                               id="password"
                               autocomplete="new-password"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                        @error('password')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CONFIRMER NOUVEAU MOT DE PASSE
                    |------------------------------------------------------------------
                    | Évite erreurs de frappe (utilisateur tape 2 fois le nouveau password)
                    --}}
                    <div class="mb-6">
                        <label for="password_confirmation" class="block text-sm font-medium text-gray-700 mb-2">
                            Confirmer le nouveau mot de passe *
                        </label>
                        {{--
                        | INPUT CONFIRMATION PASSWORD
                        | name="password_confirmation" : Suffixe _confirmation détecté par Laravel
                        | Laravel compare automatiquement password et password_confirmation
                        | Si différents → erreur validation "confirmed"
                        |
                        | Pas de @error('password_confirmation') :
                        | L'erreur s'affiche sur champ 'password' (règle confirmed)
                        --}}
                        <input type="password" 
                               name="password_confirmation" 
                               id="password_confirmation"
                               autocomplete="new-password"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                               required>
                    </div>

                    {{--
                    | BOUTON SAUVEGARDER PASSWORD
                    --}}
                    <div class="flex items-center justify-end">
                        <button type="submit" 
                                class="inline-flex items-center px-6 py-3 bg-indigo-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-indigo-700">
                            Mettre à jour le mot de passe
                        </button>
                    </div>

                </form>
            </div>
        </div>

        {{--
        |----------------------------------------------------------------------
        | SECTION 3 : SUPPRIMER LE COMPTE (Zone Dangereuse)
        |----------------------------------------------------------------------
        | Formulaire suppression compte (action irréversible)
        | border border-red-200 : Bordure rouge (alerte danger)
        --}}
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg border border-red-200">
            <div class="p-8">
                {{--
                | TITRE SECTION (Rouge)
                | text-red-600 : Couleur rouge (danger)
                | mb-4 : Margin-bottom 1rem (espace avant texte avertissement)
                --}}
                <h2 class="text-xl font-bold text-red-600 mb-4">Zone Dangereuse</h2>
                {{--
                | AVERTISSEMENT
                | text-gray-600 : Gris moyen (texte informatif)
                | mb-6 : Margin-bottom 1.5rem (espace avant formulaire)
                |
                | Message clair sur conséquences :
                | - Suppression définitive (pas de restauration)
                | - Perte de toutes données (articles, commentaires)
                | - Action irréversible (pas d'annulation)
                --}}
                <p class="text-gray-600 mb-6">
                    Une fois votre compte supprimé, toutes vos données seront définitivement effacées. 
                    Avant de supprimer votre compte, veuillez télécharger toutes les données que vous souhaitez conserver.
                </p>

                {{--
                | FORMULAIRE SUPPRESSION COMPTE
                | action : route('profile.destroy') → /profile
                | method : POST + @method('DELETE')
                | onsubmit : Confirmation JavaScript (double sécurité)
                |
                | onsubmit="return confirm('...')" :
                | Affiche popup confirmation navigateur
                | Si utilisateur clique "Annuler" → return false → soumission annulée
                | Si utilisateur clique "OK" → return true → soumission continue
                |
                | Double protection :
                | 1. Popup JavaScript (annulable)
                | 2. Champ password (vérification serveur)
                --}}
                <form action="{{ route('profile.destroy') }}" 
                      method="POST"
                      onsubmit="return confirm('Êtes-vous absolument sûr de vouloir supprimer votre compte ? Cette action est irréversible.');">
                    @csrf
                    @method('DELETE')

                    {{--
                    |------------------------------------------------------------------
                    | CHAMP CONFIRMATION PAR MOT DE PASSE
                    |------------------------------------------------------------------
                    | Sécurité : Empêche suppression accidentelle ou par tierce personne
                    --}}
                    <div class="mb-4">
                        <label for="password_delete" class="block text-sm font-medium text-gray-700 mb-2">
                            Confirmez avec votre mot de passe *
                        </label>
                        {{--
                        | INPUT PASSWORD CONFIRMATION
                        | id="password_delete" : ID unique (différent de password_confirmation)
                        | name="password" : Nom standard (validation current_password)
                        | focus:border-red-500 focus:ring-red-500 : Anneau rouge (danger)
                        |
                        | Validation serveur (ProfileController::destroy) :
                        | 'password' => ['required', 'current_password']
                        | Vérifie que password correspond au hash BDD
                        |
                        | Pourquoi redemander password ?
                        | - Utilisateur peut avoir laissé session ouverte
                        | - Quelqu'un d'autre pourrait utiliser ordinateur
                        | - Protection contre suppression accidentelle (clic involontaire)
                        --}}
                        <input type="password" 
                               name="password" 
                               id="password_delete"
                               class="w-full rounded-md border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500"
                               required>
                        @error('password')
                            <p class="text-red-600 text-sm mt-1">{{ $message }}</p>
                        @enderror
                    </div>

                    {{--
                    | BOUTON SUPPRIMER COMPTE (Rouge)
                    | bg-red-600 : Fond rouge (danger)
                    | hover:bg-red-700 : Rouge plus foncé au survol
                    |
                    | Texte explicite : "Supprimer Définitivement Mon Compte"
                    | Emoji : 🗑️ (corbeille, contexte visuel suppression)
                    |
                    | UX best practice :
                    | - Couleur rouge (alerte danger)
                    | - Texte explicite (pas juste "Supprimer")
                    | - Confirmation double (popup + password)
                    | - Position section séparée (zone dangereuse)
                    --}}
                    <button type="submit" 
                            class="inline-flex items-center px-6 py-3 bg-red-600 border border-transparent rounded-md font-semibold text-sm text-white uppercase tracking-widest hover:bg-red-700">
                        🗑️ Supprimer Définitivement Mon Compte
                    </button>
                </form>
            </div>
        </div>

    </div>
</div>
@endsection
```

**Tableau Récapitulatif des 3 Formulaires**

| Section | Route | Méthode HTTP | Validation Clés | Action Contrôleur |
|---------|-------|--------------|-----------------|-------------------|
| **Profil** | `/profile` | PATCH | `name`, `email`, `bio`, `avatar` | `ProfileController::update()` |
| **Password** | `/password` | PUT | `current_password`, `password`, `password_confirmation` | `PasswordController::update()` (Breeze) |
| **Suppression** | `/profile` | DELETE | `password` | `ProfileController::destroy()` |

**Pourquoi 3 formulaires séparés ?**

1. **Routes distinctes** : Chaque action a sa propre route RESTful
2. **Validation différente** : Règles spécifiques (email unique vs password min 8)
3. **Sécurité** : Password et suppression nécessitent confirmation
4. **UX** : Utilisateur peut modifier profil sans changer password

**Explications Techniques Approfondies**

!!! abstract "**1. Règle de validation unique avec ignore (email)**"

    **Problème :**

    ```php
    // Validation naïve (incorrecte)
    $request->validate([
        'email' => 'required|email|unique:users',
    ]);
    ```

    **Scénario bug :**

    1. Utilisateur consulte `/profile` (email actuel : `alice@example.com`)
    2. Modifie nom : "Alice" → "Alice Dupont"
    3. Garde même email : `alice@example.com`
    4. Soumet formulaire
    5. Validation échoue : "Email déjà utilisé" ❌

    **Pourquoi erreur ?**

    `unique:users` vérifie que `alice@example.com` n'existe PAS dans table `users`.  
    Mais il existe déjà (l'utilisateur actuel) → erreur.

    **Solution : Ignorer utilisateur actuel**

    ```php
    use Illuminate\Validation\Rule;

    $request->validate([
        'email' => [
            'required',
            'email',
            Rule::unique('users')->ignore($user->id),
        ],
    ]);
    ```

    **SQL généré :**

    ```sql
    SELECT COUNT(*) FROM users 
    WHERE email = 'alice@example.com' 
    AND id != 1  -- Ignore utilisateur actuel
    ```

    **Résultat :**
    - Si email existe ET id différent → erreur (déjà pris)
    - Si email existe ET id identique → OK (même utilisateur)

    **Alternative avec where() :**

    ```php
    Rule::unique('users')->ignore($user->id)->where(function ($query) {
        $query->whereNull('deleted_at'); // Ignore soft deleted
    });
    ```

!!! abstract "**2. Validation password confirmation (confirmed)**"

    **Mécanisme Laravel :**

    ```php
    // Contrôleur
    $request->validate([
        'password' => ['required', 'min:8', 'confirmed'],
    ]);
    ```

    **Champs formulaire :**

    ```html title="Code Blade"
    <input name="password">           <!-- Nouveau password -->
    <input name="password_confirmation"> <!-- Confirmation -->
    ```

    **Comment ça marche ?**

    1. Laravel détecte règle `confirmed` sur champ `password`
    2. Cherche automatiquement champ `{field}_confirmation` dans requête
    3. Compare `password` et `password_confirmation`
    4. Si identiques → validation OK
    5. Si différents → erreur "The password confirmation does not match."

    **Personnalisation message :**

    ```php
    $request->validate([
        'password' => ['required', 'min:8', 'confirmed'],
    ], [
        'password.confirmed' => 'Les mots de passe ne correspondent pas.',
    ]);
    ```

    **Alternative manuelle (sans confirmed) :**

    ```php
    $request->validate([
        'password' => ['required', 'min:8'],
        'password_confirmation' => ['required', 'same:password'],
    ]);
    ```

    **same:password** : Valide que `password_confirmation` === `password`.  
    Résultat identique mais `confirmed` plus idiomatique Laravel.

!!! abstract "**3. Règle current_password (vérification ancien password)**"

    **Utilisation :**

    ```php
    $request->validate([
        'current_password' => ['required', 'current_password'],
    ]);
    ```

    **Fonctionnement interne :**

    ```php
    // vendor/laravel/framework/src/Illuminate/Validation/Rules/Password.php
    public function passes($attribute, $value)
    {
        return Hash::check($value, Auth::user()->password);
    }
    ```

    **SQL et Hash :**

    1. `Auth::user()->password` récupère hash BDD : `$2y$10$92IXU...`
    2. `Hash::check($value, $hash)` compare :
      - Prend password saisi en clair : `"monpassword123"`
      - Hash avec même salt : `bcrypt("monpassword123", $salt)`
      - Compare hashes : si identiques → true

    **Sécurité bcrypt :**

    - **One-way** : Hash impossible à inverser (déchiffrer)
    - **Salt** : Chaque hash unique même passwords identiques
    - **Slow** : ~100ms par hash (empêche brute force)

    **Exemple :**

    ```php
    // Utilisateur 1 : password "secret"
    // Hash BDD : $2y$10$abc123...def456

    // Utilisateur 2 : password "secret" (même password)
    // Hash BDD : $2y$10$xyz789...uvw012 (hash différent grâce au salt)

    Hash::check('secret', $user1->password); // true
    Hash::check('secret', $user2->password); // true
    Hash::check('wrong', $user1->password);  // false
    ```

!!! abstract "**4. Suppression cascade des données liées**"

    **Configuration migrations :**

    ```php
    // Migration create_posts_table.php
    $table->foreignId('user_id')->constrained()->onDelete('cascade');

    // Migration create_comments_table.php
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    ```

    **Effet cascade :**

    ```
    User (id=1)
    ├── Post 1 (user_id=1)
    │   ├── Comment 1 (post_id=1)
    │   └── Comment 2 (post_id=1)
    ├── Post 2 (user_id=1)
    │   └── Comment 3 (post_id=2)
    └── Post 3 (user_id=1)
    ```

    **Suppression utilisateur :**

    ```php
    $user->delete(); // User id=1
    ```

    **SQL exécuté automatiquement (MySQL) :**

    ```sql
    -- 1. Suppression commentaires (cascade post_id)
    DELETE FROM comments WHERE post_id IN (1, 2, 3);

    -- 2. Suppression articles (cascade user_id)
    DELETE FROM posts WHERE user_id = 1;

    -- 3. Suppression utilisateur
    DELETE FROM users WHERE id = 1;
    ```

    **Ordre important :**

    MySQL respecte les contraintes FK et supprime dans le bon ordre :
    1. Comments (dépend de posts)
    2. Posts (dépend de users)
    3. Users (aucune dépendance)

    **Alternative : Soft Deletes (suppression logique)**

    ```php
    // Migration
    $table->softDeletes(); // Ajoute colonne deleted_at

    // Modèle
    use SoftDeletes;

    // Suppression
    $user->delete(); // Met deleted_at = NOW(), pas de DELETE SQL

    // Restauration
    $user->restore(); // Met deleted_at = NULL

    // Suppression définitive
    $user->forceDelete(); // Vrai DELETE SQL
    ```

    **Avantages Soft Deletes :**

    - ✅ Données récupérables (undo possible)
    - ✅ Audit trail (historique suppressions)
    - ✅ Pas de cascade nécessaire (données restent)

    **Inconvénients :**

    - ❌ Base de données grandit indéfiniment
    - ❌ Requêtes plus complexes (WHERE deleted_at IS NULL partout)
    - ❌ Pas de vraie suppression RGPD

!!! abstract "**5. Différence isDirty() vs wasChanged()**"

    **isDirty() - Modifications non sauvegardées :**

    ```php
    $user = User::find(1);
    $user->name = "Alice Dupont";

    $user->isDirty(); // true (nom modifié mais pas save())
    $user->isDirty('name'); // true
    $user->isDirty('email'); // false

    $user->save();

    $user->isDirty(); // false (changements sauvegardés)
    ```

    **wasChanged() - Modifications sauvegardées :**

    ```php
    $user = User::find(1);
    $user->name = "Alice Dupont";
    $user->save();

    $user->wasChanged(); // true (nom modifié lors du dernier save())
    $user->wasChanged('name'); // true
    $user->wasChanged('email'); // false
    ```

    **Cas d'usage :**

    ```php
    // Réinitialiser email_verified_at si email change
    if ($user->isDirty('email')) {
        $user->email_verified_at = null;
    }

    $user->save();

    // Envoyer notification si password changé
    if ($user->wasChanged('password')) {
        Mail::to($user)->send(new PasswordChangedNotification);
    }
    ```

    **Différence clé :**

    - **isDirty()** : Modifications en mémoire (avant `save()`)
    - **wasChanged()** : Modifications persistées (après `save()`)

!!! abstract "**6. Autocomplete et gestionnaires de passwords**"

    **Attribut autocomplete :**

    ```html title="Code Blade"
    <input type="password" 
          name="current_password" 
          autocomplete="current-password">

    <input type="password" 
          name="password" 
          autocomplete="new-password">
    ```

    **Valeurs standards :**

    | Valeur | Usage | Gestionnaire Action |
    |--------|-------|---------------------|
    | `current-password` | Ancien password | Remplit depuis coffre-fort |
    | `new-password` | Nouveau password | Génère + propose sauvegarde |
    | `username` | Email/login | Remplit depuis coffre-fort |
    | `email` | Email | Remplit depuis coffre-fort |
    | `name` | Nom complet | Remplit depuis profil |

    **Comportement gestionnaires (1Password, LastPass, Bitwarden) :**

    **Formulaire connexion :**

    ```html title="Code Blade"
    <input type="email" autocomplete="username">
    <input type="password" autocomplete="current-password">
    ```

    → Gestionnaire propose remplissage auto credentials sauvegardés

    **Formulaire changement password :**

    ```html title="Code Blade"
    <input type="password" autocomplete="current-password">
    <input type="password" autocomplete="new-password">
    <input type="password" autocomplete="new-password">
    ```

    → Gestionnaire :

    1. Remplit ancien password
    2. Génère nouveau password sécurisé
    3. Propose sauvegarde nouveau password

    **Pourquoi important ?**

    - ✅ UX : Remplissage auto (gain temps)
    - ✅ Sécurité : Génération passwords forts
    - ✅ Accessibilité : Standard W3C

!!! abstract "**7. Confirmation JavaScript vs Validation Serveur**"

    **Popup JavaScript (onsubmit) :**

    ```html title="Code Blade"
    <form onsubmit="return confirm('Êtes-vous sûr ?');">
    ```

    **Niveau protection : Faible**

    - Peut être contournée (JavaScript désactivé)
    - Peut être ignorée (DevTools console)
    - Pas de vérification identité

    **Validation serveur (password requis) :**

    ```php
    $request->validate([
        'password' => ['required', 'current_password'],
    ]);
    ```

    **Niveau protection : Fort**

    - Impossible à contourner côté client
    - Vérifie identité (hash password)
    - Empêche scripts automatiques

    **Stratégie défense en profondeur :**

    1. **JavaScript** : Empêche clics accidentels (UX)
    2. **Password** : Vérifie identité (sécurité)
    3. **Rate limiting** : Empêche brute force (optionnel)

    **Exemple complet :**

    ```html title="Code Blade"
    {{-- Couche 1 : Confirmation visuelle --}}
    <form onsubmit="return confirm('Supprimer ?');">
        @csrf
        @method('DELETE')
        
        {{-- Couche 2 : Vérification identité --}}
        <input type="password" name="password" required>
        
        <button type="submit">Supprimer</button>
    </form>
    ```

    ```php
    // Contrôleur - Couche 3 : Validation serveur
    public function destroy(Request $request)
    {
        $request->validate([
            'password' => ['required', 'current_password'],
        ]);
        
        // Couche 4 : Rate limiting (optionnel)
        RateLimiter::attempt(
            'delete-account:' . $request->user()->id,
            1, // 1 tentative
            function() use ($request) {
                $request->user()->delete();
            },
            60 // Par minute
        );
    }
    ```

<small>**Explication bcrypt salt :** Le salt est une chaîne aléatoire ajoutée au password avant hashing. Même algorithm, même password → hash différent à chaque fois grâce au salt unique. Format bcrypt : `$2y$10$[22 chars salt][31 chars hash]`. Coût `10` = 2^10 = 1024 itérations (ajustable, plus élevé = plus lent = plus sécurisé). **Validation email format :** Règle `email` Laravel utilise `filter_var($email, FILTER_VALIDATE_EMAIL)` PHP qui vérifie format RFC 5322. Accepte : `user@domain.com`, `user+tag@domain.co.uk`, `user@subdomain.domain.com`. Rejette : `user@`, `@domain.com`, `user domain@test.com`. **onDelete('cascade') vs onUpdate('cascade') :** `onDelete('cascade')` supprime enfants si parent supprimé. `onUpdate('cascade')` met à jour clés étrangères enfants si clé primaire parent change (rare car IDs immutables). **Règle min:8 password :** Compromis sécurité/UX. NIST recommande min 8, OWASP recommande min 10. Ajoutez règle `regex:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/` pour forcer majuscule + minuscule + chiffre.</small>

✅ **Étape 6.9 Terminée ainsi que la Phase 6 entière !**

**Fichier modifié :**
- `resources/views/profile/edit.blade.php` : Page paramètres compte avec 3 formulaires

**Concepts maîtrisés :**
- 3 formulaires indépendants (3 routes distinctes)
- Validation `unique` avec `ignore()` (email)
- Règle `confirmed` (confirmation password)
- Règle `current_password` (vérification identité)
- Pré-remplissage formulaires `old($key, $default)`
- Suppression cascade (contraintes FK)
- Confirmation JavaScript + validation serveur
- Autocomplete pour gestionnaires passwords
- Zone dangereuse (design pattern)
- isDirty() vs wasChanged()

**Récapitulatif Complet Phase 6**

✅ **Toutes les vues créées (9 fichiers) :**

1. ✅ `layouts/app.blade.php` : Layout principal (navigation, footer, flash)
2. ✅ `home.blade.php` : Page d'accueil (grille + sidebar)
3. ✅ `posts/show.blade.php` : Article individuel (contenu + commentaires)
4. ✅ `posts/create.blade.php` : Formulaire création article
5. ✅ `posts/edit.blade.php` : Formulaire édition article
6. ✅ `dashboard.blade.php` : Dashboard auteur (stats + tableau)
7. ✅ `categories/show.blade.php` : Articles par catégorie (pagination)
8. ✅ `authors/show.blade.php` : Profil public auteur (grille articles)
9. ✅ `profile/edit.blade.php` : Paramètres compte (3 formulaires)

✅ **Compétences maîtrisées :**

- Héritage layouts (`@extends`, `@section`, `@yield`)
- Directives Blade (`@if`, `@foreach`, `@auth`, `@guest`, `@error`)
- Composants Breeze (`<x-dropdown>`, `<x-dropdown-link>`)
- Protection CSRF (`@csrf`)
- Spoofing méthodes HTTP (`@method('PUT')`)
- Grilles responsive Tailwind CSS
- Pagination Laravel (`paginate()`, `links()`)
- Formulaires contrôlés (`old()` avec fallback)
- Validation affichage erreurs (`@error`)
- Messages flash (`session('success')`)
- Helpers Laravel (`Str::limit()`, `route()`, `asset()`)
- Carbon formatage dates (`format()`, `diffForHumans()`)
- Eager Loading optimisation (`with()`)























































































## Phase 7 : Tests, Optimisation et Déploiement (~90-120 minutes)

**Vue d'ensemble de la phase :**

> La Phase 7 finalise le projet en garantissant **qualité**, **performance** et **sécurité**. C'est la différence entre un projet "qui fonctionne" et un projet **production-ready** déployable en entreprise.

!!! note "**Objectifs de la phase :**"

    1. **Tests automatisés** : Vérifier que le code fonctionne correctement (Feature + Unit)
    2. **Optimisation** : Améliorer performance (caching, indexes, queries)
    3. **Sécurité** : Renforcer protection (rate limiting, validation, headers)
    4. **Configuration production** : Préparer environnement déploiement (.env, optimizations)
    5. **Déploiement** : Guide mise en ligne (serveur, base de données, domaine)

!!! quote "**Structure de la phase :**"

    ```
    Phase 7 : Tests et Déploiement
    │
    ├── Étape 7.1 : Tests Feature (Contrôleurs)
    ├── Étape 7.2 : Tests Unit (Modèles et Helpers)
    ├── Étape 7.3 : Optimisation Performance
    ├── Étape 7.4 : Sécurité et Hardening
    ├── Étape 7.5 : Configuration Production
    └── Étape 7.6 : Guide Déploiement
    ```

### Étape 7.1 : Tests Feature (Contrôleurs et Routes)

**Contexte :**

> Les **Feature Tests** testent l'application **de bout en bout** : requêtes HTTP → contrôleurs → base de données → réponses. Ils simulent le comportement d'un utilisateur réel naviguant sur le site.

!!! note "**Avantages tests automatisés :**"

    - ✅ **Détection bugs** : Trouve erreurs avant production
    - ✅ **Refactoring sûr** : Modifie code sans casser fonctionnalités
    - ✅ **Documentation vivante** : Tests montrent comment utiliser code
    - ✅ **Confiance déploiement** : Vert = safe to deploy

**Framework Laravel : PHPUnit**

Laravel intègre PHPUnit avec helpers spécifiques :

```php
// Simuler requête HTTP
$response = $this->get('/posts/1');

// Vérifier status HTTP
$response->assertStatus(200);

// Vérifier contenu réponse
$response->assertSee('Titre Article');

// Vérifier redirection
$response->assertRedirect('/dashboard');

// Vérifier base de données
$this->assertDatabaseHas('posts', ['title' => 'Mon Article']);
```

??? abstract "7.1.1 : Configuration Base de Données Tests"

    **Créer base de données SQLite pour tests :**

    Laravel utilise par défaut une base SQLite **en mémoire** pour tests (ultra-rapide, isolée).

    **Ouvrir `phpunit.xml`** (racine projet) et **vérifier la configuration** :

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
            bootstrap="vendor/autoload.php"
            colors="true">
        <testsuites>
            <testsuite name="Unit">
                <directory>tests/Unit</directory>
            </testsuite>
            <testsuite name="Feature">
                <directory>tests/Feature</directory>
            </testsuite>
        </testsuites>
        
        <!--
        |--------------------------------------------------------------------------
        | VARIABLES D'ENVIRONNEMENT TESTS
        |--------------------------------------------------------------------------
        | Ces variables écrasent celles du .env lors de l'exécution des tests
        | Garantit isolation complète (pas de pollution base de données dev)
        -->
        <php>
            <!--
            | APP_ENV=testing : Mode test (Laravel ajuste comportements)
            | Exemple : Mails ne sont pas envoyés réellement, files pas créés réellement
            -->
            <env name="APP_ENV" value="testing"/>
            
            <!--
            | DB_CONNECTION=sqlite : Base de données SQLite (fichier unique)
            | Alternative MySQL : Créer base séparée "blog_test"
            -->
            <env name="DB_CONNECTION" value="sqlite"/>
            
            <!--
            | DB_DATABASE=:memory: : Base SQLite en RAM (pas de fichier disque)
            | Ultra-rapide : 100x plus rapide que MySQL/PostgreSQL
            | Détruite après chaque suite de tests (isolation garantie)
            | 
            | Alternative SQLite fichier (persistance) :
            | <env name="DB_DATABASE" value="database/testing.sqlite"/>
            -->
            <env name="DB_DATABASE" value=":memory:"/>
            
            <!--
            | BCRYPT_ROUNDS=4 : Réduit itérations bcrypt (passwords)
            | Défaut : 10 rounds (2^10 = 1024 itérations, ~100ms)
            | Tests : 4 rounds (2^4 = 16 itérations, ~1ms)
            | Accélère tests avec authentification × 100
            -->
            <env name="BCRYPT_ROUNDS" value="4"/>
            
            <!--
            | HASH_DRIVER=bcrypt : Force bcrypt (cohérence production)
            | Alternative : argon2id (plus sécurisé mais plus lent)
            -->
            <env name="HASH_DRIVER" value="bcrypt"/>
            
            <!--
            | CACHE_DRIVER=array : Cache en mémoire (pas Redis/Memcached)
            | Évite dépendance services externes pendant tests
            -->
            <env name="CACHE_DRIVER" value="array"/>
            
            <!--
            | QUEUE_CONNECTION=sync : Exécution synchrone (pas de workers)
            | Jobs exécutés immédiatement pendant tests
            | Évite attendre workers asynchrones
            -->
            <env name="QUEUE_CONNECTION" value="sync"/>
            
            <!--
            | SESSION_DRIVER=array : Sessions en mémoire
            | Pas de fichiers/Redis pendant tests
            -->
            <env name="SESSION_DRIVER" value="array"/>
            
            <!--
            | MAIL_MAILER=array : Mails interceptés (pas envoyés réellement)
            | Testables via Mail::assertSent()
            -->
            <env name="MAIL_MAILER" value="array"/>
        </php>
    </phpunit>
    ```

    **Exécuter les tests :**

    ```bash
    # Exécuter tous les tests
    php artisan test

    # Exécuter seulement tests Feature
    php artisan test --testsuite=Feature

    # Exécuter seulement tests Unit
    php artisan test --testsuite=Unit

    # Exécuter test spécifique
    php artisan test --filter=test_home_page_displays_posts

    # Mode verbose (détails)
    php artisan test -v

    # Coverage (nécessite xdebug)
    php artisan test --coverage
    ```

??? abstract "7.1.2 : Tests Feature - HomeController"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test HomeControllerTest
    ```

    **Éditer `tests/Feature/HomeControllerTest.php` :**

    ```php
    <?php

    namespace Tests\Feature;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Feature : HomeController
     * 
     * Teste la page d'accueil du blog
     * - Affichage des articles publiés
     * - Pagination fonctionnelle
     * - Sidebar catégories et articles populaires
     */
    class HomeControllerTest extends TestCase
    {
        /**
         * RefreshDatabase : Trait Laravel qui :
         * 1. Exécute toutes les migrations (schéma BDD)
         * 2. Utilise transaction pour chaque test
         * 3. Rollback automatique après chaque test
         * 
         * Résultat : Base de données vierge pour chaque test (isolation)
         * 
         * Alternative :
         * use DatabaseMigrations; // Migrations complètes (plus lent)
         * use DatabaseTransactions; // Rollback seulement (nécessite BDD existante)
         */
        use RefreshDatabase;

        /**
         * Test : Page d'accueil accessible
         * 
         * Vérifie :
         * - Route / retourne status 200 (OK)
         * - Page contient titre "Bienvenue"
         */
        public function test_home_page_is_accessible(): void
        {
            // Simuler requête GET /
            // $this->get() : Helper Laravel, retourne objet TestResponse
            $response = $this->get('/');

            // Assertions : Vérifications
            // assertStatus(200) : Code HTTP 200 (OK)
            // 200 = succès, 404 = non trouvé, 500 = erreur serveur
            $response->assertStatus(200);

            // assertSee('texte') : Vérifie présence texte dans HTML réponse
            // Par défaut : échappe HTML (cherche "Bienvenue" échappé)
            // assertSee('Bienvenue', false) : Désactive échappement (HTML brut)
            $response->assertSee('Bienvenue');
        }

        /**
        * Test : Articles publiés affichés sur page d'accueil
        * 
        * Vérifie :
        * - Articles publiés visibles
        * - Brouillons NON visibles
        * - Articles futurs NON visibles
        */
        public function test_published_posts_are_displayed(): void
        {
            // Arrange : Préparer données test
            // Factory Pattern : Génère données factices réalistes
            
            /**
            * User::factory()->create() : Crée utilisateur en BDD
            * Équivaut à :
            * INSERT INTO users (name, email, password, ...) VALUES (...)
            * 
            * factory() : Appelle UserFactory défini dans database/factories/
            * create() : Insère en BDD (vs make() qui crée instance sans INSERT)
            */
            $user = User::factory()->create();

            /**
            * Category::factory()->create() : Crée catégorie en BDD
            */
            $category = Category::factory()->create();

            /**
            * Post::factory()->create() : Crée article PUBLIÉ
            * 
            * Par défaut PostFactory génère :
            * - status = 'published'
            * - published_at = now()
            * 
            * Associations automatiques :
            * - user_id = $user->id
            * - category_id = $category->id
            */
            $publishedPost = Post::factory()->create([
                'title' => 'Article Publié Visible',
                'status' => 'published',
                'published_at' => now()->subDay(), // Hier
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            /**
            * Créer brouillon (NE DOIT PAS apparaître)
            */
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon Non Visible',
                'status' => 'draft',
                'published_at' => null, // Pas de date publication
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            /**
            * Créer article futur (NE DOIT PAS apparaître)
            */
            $futurePost = Post::factory()->create([
                'title' => 'Article Futur Non Visible',
                'status' => 'published',
                'published_at' => now()->addDay(), // Demain
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Exécuter action testée
            $response = $this->get('/');

            // Assert : Vérifier résultats
            $response->assertStatus(200);
            
            /**
            * assertSee() : Vérifie présence texte
            * Cherche dans HTML réponse (échappé par défaut)
            */
            $response->assertSee('Article Publié Visible');
            
            /**
            * assertDontSee() : Vérifie ABSENCE texte
            * Brouillon et article futur NE DOIVENT PAS être visibles
            */
            $response->assertDontSee('Brouillon Non Visible');
            $response->assertDontSee('Article Futur Non Visible');
        }

        /**
        * Test : Pagination fonctionne (9 articles par page)
        * 
        * Vérifie :
        * - Page 1 affiche 9 articles
        * - Page 2 accessible avec paramètre ?page=2
        * - Articles paginés correctement
        */
        public function test_pagination_works_correctly(): void
        {
            // Arrange : Créer 15 articles publiés
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Post::factory()->count(15)->create() : Crée 15 articles
            * 
            * Boucle équivalente :
            * for ($i = 0; $i < 15; $i++) {
            *     Post::factory()->create([...]);
            * }
            */
            Post::factory()->count(15)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Tester page 1
            $responsePage1 = $this->get('/');

            // Assert : Page 1 contient exactement 9 articles
            /**
            * assertViewHas('posts') : Vérifie variable 'posts' passée à la vue
            * 
            * Équivaut à vérifier dans contrôleur :
            * return view('home', compact('posts')); // $posts doit exister
            */
            $responsePage1->assertViewHas('posts');
            
            /**
            * $responsePage1->viewData('posts') : Récupère variable 'posts' de la vue
            * ->count() : Compte éléments Collection
            */
            $this->assertEquals(9, $responsePage1->viewData('posts')->count());

            // Act : Tester page 2
            $responsePage2 = $this->get('/?page=2');

            // Assert : Page 2 contient 6 articles restants (15 - 9 = 6)
            $responsePage2->assertStatus(200);
            $this->assertEquals(6, $responsePage2->viewData('posts')->count());
        }

        /**
        * Test : Sidebar catégories affichée avec compteurs
        * 
        * Vérifie :
        * - Catégories affichées dans sidebar
        * - Compteurs articles corrects (withCount)
        */
        public function test_sidebar_displays_categories_with_counts(): void
        {
            // Arrange
            $user = User::factory()->create();
            
            /**
            * Créer 2 catégories avec articles
            */
            $categoryTech = Category::factory()->create(['name' => 'Technologie']);
            $categoryVoyage = Category::factory()->create(['name' => 'Voyage']);

            // Catégorie Technologie : 3 articles
            Post::factory()->count(3)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $categoryTech->id,
            ]);

            // Catégorie Voyage : 2 articles
            Post::factory()->count(2)->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $categoryVoyage->id,
            ]);

            // Act
            $response = $this->get('/');

            // Assert : Vérifier présence catégories
            $response->assertStatus(200);
            $response->assertSee('Technologie');
            $response->assertSee('Voyage');

            /**
            * Vérifier compteurs
            * assertSee('3') : Cherche "3" dans HTML (compteur catégorie Tech)
            * assertSee('2') : Cherche "2" dans HTML (compteur catégorie Voyage)
            */
            $response->assertSee('3'); // Compteur Technologie
            $response->assertSee('2'); // Compteur Voyage
        }

        /**
        * Test : Articles populaires affichés (top 3 vues)
        * 
        * Vérifie :
        * - 3 articles les plus vus affichés dans sidebar
        * - Ordre décroissant (plus de vues en premier)
        */
        public function test_popular_posts_are_displayed(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Créer articles avec compteurs vues différents
            */
            $post1 = Post::factory()->create([
                'title' => 'Article Populaire #1',
                'views_count' => 500, // Le plus populaire
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post2 = Post::factory()->create([
                'title' => 'Article Populaire #2',
                'views_count' => 300, // Deuxième
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post3 = Post::factory()->create([
                'title' => 'Article Populaire #3',
                'views_count' => 100, // Troisième
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            $post4 = Post::factory()->create([
                'title' => 'Article Peu Populaire',
                'views_count' => 10, // Pas dans top 3
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act
            $response = $this->get('/');

            // Assert : Vérifier présence top 3
            $response->assertStatus(200);
            $response->assertSee('Article Populaire #1');
            $response->assertSee('Article Populaire #2');
            $response->assertSee('Article Populaire #3');
            
            /**
            * Vérifier absence article peu populaire
            * Ne doit PAS apparaître dans top 3
            */
            $response->assertDontSee('Article Peu Populaire');
        }
    }
    ```

??? abstract "7.1.3 : Tests Feature - PostController"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test PostControllerTest
    ```

    **Éditer `tests/Feature/PostControllerTest.php` :**

    ```php
    <?php

    namespace Tests\Feature;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Feature : PostController
     * 
     * Teste les fonctionnalités CRUD des articles
     */
    class PostControllerTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * Test : Article individuel accessible (page show)
         * 
         * Vérifie :
         * - Route /posts/{slug} retourne 200
         * - Contenu article affiché (titre, contenu, auteur)
         */
        public function test_published_post_is_accessible(): void
        {
            // Arrange
            $user = User::factory()->create(['name' => 'Alice Dupont']);
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'title' => 'Mon Article Test',
                'slug' => 'mon-article-test',
                'content' => 'Contenu complet de mon article test.',
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Accéder via slug
            $response = $this->get('/posts/' . $post->slug);

            // Assert
            $response->assertStatus(200);
            $response->assertSee('Mon Article Test');
            $response->assertSee('Contenu complet de mon article test.');
            $response->assertSee('Alice Dupont'); // Nom auteur
        }

        /**
        * Test : Brouillon non accessible publiquement (404)
        * 
        * Vérifie :
        * - Visiteur anonyme : 404 Not Found
        * - Autre utilisateur : 404 Not Found
        * - Auteur article : 200 OK (accès autorisé)
        */
        public function test_draft_post_not_accessible_to_public(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon Privé',
                'slug' => 'brouillon-prive',
                'status' => 'draft',
                'published_at' => null,
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Visiteur anonyme → 404
            $response = $this->get('/posts/' . $draftPost->slug);
            $response->assertStatus(404);

            // Act & Assert : Autre utilisateur connecté → 404
            /**
            * $this->actingAs($user) : Simule connexion utilisateur
            * 
            * Équivaut à :
            * Auth::login($user);
            * 
            * Tous les appels suivants considèrent $user comme connecté
            */
            $response = $this->actingAs($otherUser)->get('/posts/' . $draftPost->slug);
            $response->assertStatus(404);

            // Act & Assert : Auteur article → 200 (accès autorisé)
            $response = $this->actingAs($author)->get('/posts/' . $draftPost->slug);
            $response->assertStatus(200);
            $response->assertSee('Brouillon Privé');
        }

        /**
        * Test : Incrément compteur vues fonctionne
        * 
        * Vérifie :
        * - views_count incrémenté après visite
        * - Plusieurs visites = plusieurs incréments
        */
        public function test_post_views_count_is_incremented(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'views_count' => 0, // Initialement 0
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier valeur initiale
            $this->assertEquals(0, $post->views_count);

            // Act : Visiter article
            $this->get('/posts/' . $post->slug);

            // Assert : Vérifier incrément (+1)
            /**
            * $post->fresh() : Recharge modèle depuis BDD
            * 
            * Nécessaire car $post en mémoire n'est pas mis à jour automatiquement
            * après modifications en BDD
            */
            $this->assertEquals(1, $post->fresh()->views_count);

            // Act : Visiter à nouveau
            $this->get('/posts/' . $post->slug);

            // Assert : Vérifier nouvel incrément (+1, total = 2)
            $this->assertEquals(2, $post->fresh()->views_count);
        }

        /**
        * Test : Création article nécessite authentification
        * 
        * Vérifie :
        * - Visiteur anonyme redirigé vers /login
        * - Utilisateur connecté accède au formulaire
        */
        public function test_create_post_requires_authentication(): void
        {
            // Act : Visiteur anonyme tente accéder /posts/create
            $response = $this->get('/posts/create');

            // Assert : Redirection vers login
            /**
            * assertRedirect('/login') : Vérifie status 302 + header Location
            */
            $response->assertRedirect('/login');

            // Act : Utilisateur connecté accède formulaire
            $user = User::factory()->create();
            $response = $this->actingAs($user)->get('/posts/create');

            // Assert : Succès
            $response->assertStatus(200);
            $response->assertSee('Créer un Article'); // Titre formulaire
        }

        /**
        * Test : Création article avec données valides
        * 
        * Vérifie :
        * - Article créé en BDD
        * - Redirection vers article créé
        * - Message succès affiché
        * - Slug généré automatiquement
        */
        public function test_authenticated_user_can_create_post(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            /**
            * Données formulaire
            * Tableau associatif = $_POST en PHP
            */
            $postData = [
                'title' => 'Nouvel Article Créé',
                'category_id' => $category->id,
                'excerpt' => 'Résumé de mon nouvel article.',
                'content' => 'Contenu complet de mon nouvel article avec plus de 100 caractères pour passer validation.',
                'image' => 'https://example.com/image.jpg',
                'status' => 'published',
            ];

            // Act : Soumettre formulaire création
            /**
            * $this->actingAs($user)->post($url, $data) : Simule soumission POST
            * 
            * Équivaut à :
            * - Auth::login($user)
            * - Soumettre formulaire avec données $postData
            * - CSRF token ajouté automatiquement par Laravel
            */
            $response = $this->actingAs($user)
                ->post('/posts', $postData);

            // Assert : Vérifier création BDD
            /**
            * assertDatabaseHas('table', ['column' => 'value'])
            * 
            * Vérifie existence enregistrement en BDD
            * Équivaut à :
            * SELECT * FROM posts WHERE title = 'Nouvel Article Créé' LIMIT 1
            * assertTrue(count($result) > 0)
            */
            $this->assertDatabaseHas('posts', [
                'title' => 'Nouvel Article Créé',
                'user_id' => $user->id,
                'category_id' => $category->id,
                'status' => 'published',
            ]);

            // Assert : Vérifier slug auto-généré
            /**
            * Slug doit être généré via événement creating() dans modèle
            * "Nouvel Article Créé" → "nouvel-article-cree"
            */
            $post = Post::where('title', 'Nouvel Article Créé')->first();
            $this->assertEquals('nouvel-article-cree', $post->slug);

            // Assert : Vérifier redirection vers article créé
            $response->assertRedirect('/posts/' . $post->slug);

            // Assert : Vérifier message succès
            /**
            * assertSessionHas('success') : Vérifie variable flash session
            * 
            * Équivaut à vérifier dans contrôleur :
            * return redirect()->with('success', 'Article créé avec succès');
            */
            $response->assertSessionHas('success');
        }

        /**
        * Test : Validation formulaire création
        * 
        * Vérifie :
        * - Champs requis provoquent erreurs validation
        * - Erreurs affichées dans session
        */
        public function test_create_post_validation_fails_with_invalid_data(): void
        {
            // Arrange
            $user = User::factory()->create();

            /**
            * Données invalides :
            * - title : manquant (requis)
            * - category_id : invalide (n'existe pas en BDD)
            * - content : trop court (min 100 chars)
            */
            $invalidData = [
                'title' => '', // Vide (requis)
                'category_id' => 9999, // N'existe pas
                'excerpt' => 'Résumé valide.',
                'content' => 'Court', // < 100 caractères
                'status' => 'published',
            ];

            // Act : Soumettre données invalides
            $response = $this->actingAs($user)
                ->post('/posts', $invalidData);

            // Assert : Vérifier erreurs validation
            /**
            * assertSessionHasErrors(['field1', 'field2'])
            * 
            * Vérifie présence erreurs pour champs spécifiés
            * Équivaut à vérifier :
            * session()->has('errors') && $errors->has('title')
            */
            $response->assertSessionHasErrors(['title', 'category_id', 'content']);

            // Assert : Vérifier article PAS créé en BDD
            /**
            * assertDatabaseMissing('table', ['column' => 'value'])
            * 
            * Vérifie ABSENCE enregistrement en BDD
            */
            $this->assertDatabaseMissing('posts', [
                'excerpt' => 'Résumé valide.',
            ]);
        }

        /**
        * Test : Édition article nécessite être l'auteur
        * 
        * Vérifie :
        * - Auteur article : accès formulaire édition (200)
        * - Autre utilisateur : erreur 403 Forbidden
        * - Visiteur anonyme : redirection login
        */
        public function test_only_author_can_edit_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Visiteur anonyme → Redirection login
            $response = $this->get('/posts/' . $post->slug . '/edit');
            $response->assertRedirect('/login');

            // Act & Assert : Autre utilisateur → 403 Forbidden
            /**
            * assertStatus(403) : Vérifie erreur Forbidden
            * 403 = Authentifié mais pas autorisé (ownership check)
            */
            $response = $this->actingAs($otherUser)
                ->get('/posts/' . $post->slug . '/edit');
            $response->assertStatus(403);

            // Act & Assert : Auteur article → 200 OK
            $response = $this->actingAs($author)
                ->get('/posts/' . $post->slug . '/edit');
            $response->assertStatus(200);
            $response->assertSee('Modifier l\'Article'); // Titre formulaire
        }

        /**
        * Test : Mise à jour article avec données valides
        * 
        * Vérifie :
        * - Article modifié en BDD
        * - Redirection vers article mis à jour
        * - Message succès affiché
        */
        public function test_author_can_update_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'title' => 'Titre Original',
                'content' => 'Contenu original de l\'article avec suffisamment de texte pour validation.',
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Données mise à jour
            $updatedData = [
                'title' => 'Titre Modifié',
                'category_id' => $category->id,
                'excerpt' => 'Résumé modifié.',
                'content' => 'Contenu modifié de l\'article avec suffisamment de texte pour passer validation.',
                'image' => 'https://example.com/new-image.jpg',
                'status' => 'published',
            ];

            // Act : Soumettre mise à jour
            /**
            * $this->put($url, $data) : Simule requête PUT
            * 
            * Équivaut à formulaire HTML :
            * <form method="POST">
            *     @method('PUT')
            *     ...
            * </form>
            */
            $response = $this->actingAs($author)
                ->put('/posts/' . $post->slug, $updatedData);

            // Assert : Vérifier mise à jour BDD
            $this->assertDatabaseHas('posts', [
                'id' => $post->id,
                'title' => 'Titre Modifié',
                'content' => 'Contenu modifié de l\'article avec suffisamment de texte pour passer validation.',
            ]);

            // Assert : Vérifier redirection
            /**
            * $post->fresh()->slug : Recharge post depuis BDD
            * Slug peut avoir changé si titre modifié
            */
            $response->assertRedirect('/posts/' . $post->fresh()->slug);

            // Assert : Vérifier message succès
            $response->assertSessionHas('success');
        }

        /**
        * Test : Suppression article nécessite être l'auteur
        * 
        * Vérifie :
        * - Auteur article : suppression réussie (BDD)
        * - Autre utilisateur : erreur 403
        * - Redirection dashboard après suppression
        */
        public function test_only_author_can_delete_post(): void
        {
            // Arrange
            $author = User::factory()->create();
            $otherUser = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'user_id' => $author->id,
                'category_id' => $category->id,
            ]);

            // Act & Assert : Autre utilisateur tente supprimer → 403
            $response = $this->actingAs($otherUser)
                ->delete('/posts/' . $post->slug);
            $response->assertStatus(403);

            // Assert : Article toujours en BDD
            $this->assertDatabaseHas('posts', ['id' => $post->id]);

            // Act : Auteur supprime article
            $response = $this->actingAs($author)
                ->delete('/posts/' . $post->slug);

            // Assert : Article supprimé de BDD
            /**
            * assertDatabaseMissing() : Vérifie ABSENCE enregistrement
            */
            $this->assertDatabaseMissing('posts', ['id' => $post->id]);

            // Assert : Redirection dashboard
            $response->assertRedirect('/dashboard');

            // Assert : Message succès
            $response->assertSessionHas('success');
        }
    }
    ```

=== "**Tableau Récapitulatif Tests Feature**"

    | Test | Objectif | Assertions Clés |
    |------|----------|----------------|
    | `test_home_page_is_accessible` | Route / fonctionne | `assertStatus(200)`, `assertSee()` |
    | `test_published_posts_are_displayed` | Articles publiés visibles | `assertSee()`, `assertDontSee()` |
    | `test_pagination_works_correctly` | Pagination 9/page | `assertViewHas()`, `assertEquals()` |
    | `test_sidebar_displays_categories` | Catégories + compteurs | `assertSee()` (noms + nombres) |
    | `test_popular_posts_are_displayed` | Top 3 vues affiché | `assertSee()`, `assertDontSee()` |
    | `test_published_post_is_accessible` | Page article accessible | `assertStatus(200)`, `assertSee()` |
    | `test_draft_post_not_accessible` | Brouillons privés | `assertStatus(404/200)` selon user |
    | `test_post_views_count_incremented` | Compteur vues incrémenté | `assertEquals()`, `fresh()` |
    | `test_create_post_requires_auth` | Création nécessite login | `assertRedirect('/login')` |
    | `test_authenticated_user_can_create` | Création fonctionnelle | `assertDatabaseHas()`, `assertRedirect()` |
    | `test_create_validation_fails` | Validation formulaire | `assertSessionHasErrors()` |
    | `test_only_author_can_edit` | Édition réservée auteur | `assertStatus(403/200)` |
    | `test_author_can_update` | Mise à jour fonctionnelle | `assertDatabaseHas()` (données modifiées) |
    | `test_only_author_can_delete` | Suppression réservée auteur | `assertDatabaseMissing()` |

=== "**Exécuter les tests**"

    ```bash
    # Tous les tests
    php artisan test

    # Seulement HomeControllerTest
    php artisan test --filter=HomeControllerTest

    # Seulement PostControllerTest
    php artisan test --filter=PostControllerTest

    # Avec détails (verbose)
    php artisan test -v

    # Avec temps d'exécution
    php artisan test --profile
    ```

    **Résultat attendu :**

    ```
    PASS  Tests\Feature\HomeControllerTest
    ✓ home page is accessible (0.05s)
    ✓ published posts are displayed (0.08s)
    ✓ pagination works correctly (0.12s)
    ✓ sidebar displays categories with counts (0.09s)
    ✓ popular posts are displayed (0.10s)

    PASS  Tests\Feature\PostControllerTest
    ✓ published post is accessible (0.06s)
    ✓ draft post not accessible to public (0.11s)
    ✓ post views count is incremented (0.07s)
    ✓ create post requires authentication (0.05s)
    ✓ authenticated user can create post (0.13s)
    ✓ create post validation fails with invalid data (0.08s)
    ✓ only author can edit post (0.10s)
    ✓ author can update post (0.14s)
    ✓ only author can delete post (0.12s)

    Tests:    14 passed (19 assertions)
    Duration: 1.10s
    ```

✅ **Étape 7.1 Terminée !**

**Fichiers créés :**

- `tests/Feature/HomeControllerTest.php` : 5 tests page d'accueil
- `tests/Feature/PostControllerTest.php` : 9 tests CRUD articles

**Concepts maîtrisés :**

- RefreshDatabase trait (isolation tests)
- Factory Pattern (génération données tests)
- actingAs() (simulation authentification)
- assertStatus(), assertSee(), assertDontSee()
- assertDatabaseHas(), assertDatabaseMissing()
- assertRedirect(), assertSessionHas()
- assertViewHas(), viewData()
- fresh() (rechargement modèle depuis BDD)

### Étape 7.2 : Tests Unit (Modèles, Scopes et Helpers)

**Contexte :**

> Les **Tests Unit** testent des **unités de code isolées** : méthodes de modèles, scopes Eloquent, helpers personnalisés, calculs métier. Contrairement aux Feature Tests (bout en bout), les Unit Tests se concentrent sur une **fonction spécifique** sans dépendances externes.

!!! note "**Différences Unit vs Feature Tests :**"

    | Aspect | Tests Unit | Tests Feature |
    |--------|-----------|---------------|
    | **Portée** | Fonction isolée | Flux complet (HTTP → BDD) |
    | **Vitesse** | Ultra-rapide (<1ms) | Lent (50-200ms) |
    | **Dépendances** | Aucune (ou mockées) | Base données, routes, vues |
    | **Objectif** | Logique métier pure | Comportement utilisateur |
    | **Exemple** | `Post::generateSlug()` | `POST /posts → création BDD` |

**Avantages Tests Unit :**

- ✅ **Rapidité** : Exécution immédiate (pas de BDD, pas de HTTP)
- ✅ **Précision** : Localise bugs dans méthode spécifique
- ✅ **Refactoring** : Vérifie logique pure indépendamment du reste
- ✅ **Documentation** : Montre usage exact d'une méthode

**Structure Tests Unit Laravel :**

```php
class PostTest extends TestCase
{
    // Pas de RefreshDatabase (pas de BDD nécessaire)
    // Tests méthodes isolées du modèle Post
    
    public function test_slug_is_generated_correctly(): void
    {
        // Tester uniquement la génération de slug
        // Sans créer en BDD
    }
}
```

??? abstract "7.2.1 : Tests Unit - Modèle Post (Méthodes et Scopes)"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test PostTest --unit
    ```

    !!! note "**Flag `--unit` :**"
        Place le fichier dans `tests/Unit/` au lieu de `tests/Feature/`

    **Éditer `tests/Unit/PostTest.php` :**

    ```php
    <?php

    namespace Tests\Unit;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    /**
     * Tests Unit : Modèle Post
     * 
     * Teste les méthodes et scopes du modèle Post
     * - Génération slug automatique
     * - Scope published()
     * - Incrément views
     * - Relations Eloquent
     */
    class PostTest extends TestCase
    {
        /**
         * RefreshDatabase : Nécessaire ici car on teste relations Eloquent
         * 
         * Note : Certains tests unit peuvent se passer de BDD
         * Ici, on teste des méthodes qui interagissent avec BDD (scopes, relations)
         */
        use RefreshDatabase;

        /**
         * Test : Génération automatique du slug lors de la création
         * 
         * Vérifie :
         * - Slug généré à partir du titre
         * - Slug formaté en kebab-case
         * - Événement creating() déclenché correctement
         */
        public function test_slug_is_generated_automatically_on_create(): void
        {
            // Arrange : Créer utilisateur et catégorie
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Act : Créer article SANS spécifier slug
            /**
             * Note : slug n'est PAS fourni dans le tableau
             * Il doit être généré automatiquement par événement creating()
             */
            $post = Post::create([
                'title' => 'Mon Article de Test',
                'excerpt' => 'Résumé du test.',
                'content' => 'Contenu complet de l\'article de test avec suffisamment de caractères pour passer validation.',
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier slug généré correctement
            /**
             * "Mon Article de Test" doit devenir "mon-article-de-test"
             * 
             * Transformations attendues :
             * - Majuscules → minuscules
             * - Espaces → tirets
             * - Accents préservés ou supprimés (selon implémentation)
             */
            $this->assertEquals('mon-article-de-test', $post->slug);

            // Assert : Vérifier unicité du slug
            $this->assertNotNull($post->slug);
            $this->assertIsString($post->slug);
        }

        /**
         * Test : Gestion des slugs dupliqués (unicité)
         * 
         * Vérifie :
         * - Si titre identique, slug doit avoir suffixe numérique
         * - Slug1 : "mon-article"
         * - Slug2 : "mon-article-2"
         */
        public function test_duplicate_slugs_are_handled(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Act : Créer premier article
            $post1 = Post::factory()->create([
                'title' => 'Titre Identique',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Créer deuxième article avec même titre
            $post2 = Post::factory()->create([
                'title' => 'Titre Identique',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier slugs différents
            /**
             * $post1->slug : "titre-identique"
             * $post2->slug : "titre-identique-2" (suffixe ajouté)
             */
            $this->assertNotEquals($post1->slug, $post2->slug);
            
            /**
             * Vérifier format slug2 : doit contenir slug1 + suffixe
             */
            $this->assertStringStartsWith($post1->slug, $post2->slug);
            
            /**
             * Alternative : Vérifier que slug2 matche pattern "titre-identique-N"
             */
            $this->assertMatchesRegularExpression('/^titre-identique-\d+$/', $post2->slug);
        }

        /**
         * Test : Scope published() filtre correctement
         * 
         * Vérifie :
         * - Scope retourne seulement articles publiés
         * - Status 'published' AND published_at <= NOW()
         * - Exclut brouillons et articles futurs
         */
        public function test_published_scope_filters_correctly(): void
        {
            // Arrange : Créer utilisateur et catégorie
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer article publié (DOIT apparaître)
            $publishedPost = Post::factory()->create([
                'title' => 'Article Publié',
                'status' => 'published',
                'published_at' => now()->subDay(), // Hier
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer brouillon (NE DOIT PAS apparaître)
            $draftPost = Post::factory()->create([
                'title' => 'Brouillon',
                'status' => 'draft',
                'published_at' => null,
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer article futur (NE DOIT PAS apparaître)
            $futurePost = Post::factory()->create([
                'title' => 'Article Futur',
                'status' => 'published',
                'published_at' => now()->addDay(), // Demain
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Récupérer articles avec scope published()
            /**
             * Post::published() appelle scopePublished() du modèle
             * 
             * Équivaut à :
             * Post::where('status', 'published')
             *     ->where('published_at', '<=', now())
             *     ->get()
             */
            $publishedPosts = Post::published()->get();

            // Assert : Vérifier filtrage correct
            /**
             * count() : Doit retourner 1 (seulement article publié)
             */
            $this->assertCount(1, $publishedPosts);

            /**
             * contains() : Vérifie présence article publié
             */
            $this->assertTrue($publishedPosts->contains($publishedPost));

            /**
             * Vérifier ABSENCE brouillon et article futur
             */
            $this->assertFalse($publishedPosts->contains($draftPost));
            $this->assertFalse($publishedPosts->contains($futurePost));
        }

        /**
         * Test : Méthode incrementViews() incrémente compteur
         * 
         * Vérifie :
         * - views_count incrémenté de 1
         * - Méthode thread-safe (évite race conditions)
         * - Sauvegarde automatique en BDD
         */
        public function test_increment_views_increases_counter(): void
        {
            // Arrange : Créer article avec 0 vues
            $user = User::factory()->create();
            $category = Category::factory()->create();
            
            $post = Post::factory()->create([
                'views_count' => 0,
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier valeur initiale
            $this->assertEquals(0, $post->views_count);

            // Act : Incrémenter vues
            /**
             * incrementViews() : Méthode personnalisée du modèle Post
             * 
             * Implémentation attendue :
             * public function incrementViews()
             * {
             *     $this->increment('views_count');
             * }
             */
            $post->incrementViews();

            // Assert : Vérifier incrément (+1)
            /**
             * fresh() : Recharge depuis BDD
             * Vérifie que increment() a bien sauvegardé
             */
            $this->assertEquals(1, $post->fresh()->views_count);

            // Act : Incrémenter à nouveau
            $post->incrementViews();

            // Assert : Vérifier nouvel incrément (+1, total = 2)
            $this->assertEquals(2, $post->fresh()->views_count);
        }

        /**
         * Test : Méthode isDraft() détecte brouillons
         * 
         * Vérifie :
         * - isDraft() retourne true si status = 'draft'
         * - isDraft() retourne false si status = 'published'
         */
        public function test_is_draft_method_works_correctly(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer brouillon
            $draftPost = Post::factory()->create([
                'status' => 'draft',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer article publié
            $publishedPost = Post::factory()->create([
                'status' => 'published',
                'published_at' => now(),
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier isDraft()
            /**
             * isDraft() : Méthode personnalisée du modèle Post
             * 
             * Implémentation attendue :
             * public function isDraft(): bool
             * {
             *     return $this->status === 'draft';
             * }
             */
            $this->assertTrue($draftPost->isDraft());
            $this->assertFalse($publishedPost->isDraft());
        }

        /**
         * Test : Relation belongsTo avec User (auteur)
         * 
         * Vérifie :
         * - Relation user chargée correctement
         * - Attribut user_id correspond à user->id
         */
        public function test_belongs_to_user_relationship(): void
        {
            // Arrange
            $user = User::factory()->create(['name' => 'Alice Dupont']);
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation user
            /**
             * $post->user : Appelle méthode user() du modèle Post
             * 
             * public function user()
             * {
             *     return $this->belongsTo(User::class);
             * }
             */
            $postUser = $post->user;

            // Assert : Vérifier relation
            /**
             * assertInstanceOf() : Vérifie type objet
             */
            $this->assertInstanceOf(User::class, $postUser);

            /**
             * Vérifier ID correspondant
             */
            $this->assertEquals($user->id, $postUser->id);

            /**
             * Vérifier attribut name
             */
            $this->assertEquals('Alice Dupont', $postUser->name);
        }

        /**
         * Test : Relation belongsTo avec Category
         * 
         * Vérifie :
         * - Relation category chargée correctement
         * - Attribut category_id correspond à category->id
         */
        public function test_belongs_to_category_relationship(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create(['name' => 'Technologie']);

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation category
            $postCategory = $post->category;

            // Assert : Vérifier relation
            $this->assertInstanceOf(Category::class, $postCategory);
            $this->assertEquals($category->id, $postCategory->id);
            $this->assertEquals('Technologie', $postCategory->name);
        }

        /**
         * Test : Relation hasMany avec Comments
         * 
         * Vérifie :
         * - Relation comments retourne Collection
         * - Commentaires liés à l'article
         */
        public function test_has_many_comments_relationship(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Créer 3 commentaires pour cet article
            /**
             * Comment::factory()->count(3)->create() nécessite CommentFactory
             * 
             * Alternative manuelle :
             * for ($i = 0; $i < 3; $i++) {
             *     Comment::create([...]);
             * }
             */
            $post->comments()->createMany([
                [
                    'author_name' => 'Visiteur 1',
                    'author_email' => 'visiteur1@example.com',
                    'content' => 'Premier commentaire.',
                    'approved' => true,
                ],
                [
                    'author_name' => 'Visiteur 2',
                    'author_email' => 'visiteur2@example.com',
                    'content' => 'Deuxième commentaire.',
                    'approved' => true,
                ],
                [
                    'author_name' => 'Visiteur 3',
                    'author_email' => 'visiteur3@example.com',
                    'content' => 'Troisième commentaire.',
                    'approved' => false, // Non approuvé
                ],
            ]);

            // Act : Charger tous les commentaires
            $comments = $post->comments;

            // Assert : Vérifier relation
            /**
             * assertCount(3) : Vérifie nombre éléments Collection
             */
            $this->assertCount(3, $comments);

            /**
             * Vérifier type Collection
             */
            $this->assertInstanceOf(\Illuminate\Database\Eloquent\Collection::class, $comments);

            /**
             * Vérifier tous commentaires liés au post
             */
            foreach ($comments as $comment) {
                $this->assertEquals($post->id, $comment->post_id);
            }
        }

        /**
         * Test : Cast attribut published_at en Carbon
         * 
         * Vérifie :
         * - published_at retourné comme instance Carbon
         * - Méthodes Carbon accessibles (format, diffForHumans)
         */
        public function test_published_at_is_cast_to_carbon(): void
        {
            // Arrange
            $user = User::factory()->create();
            $category = Category::factory()->create();

            $post = Post::factory()->create([
                'published_at' => '2024-01-15 10:30:00',
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Assert : Vérifier cast Carbon
            /**
             * assertInstanceOf() : Vérifie type objet
             */
            $this->assertInstanceOf(\Illuminate\Support\Carbon::class, $post->published_at);

            /**
             * Vérifier méthodes Carbon fonctionnent
             */
            $formattedDate = $post->published_at->format('Y-m-d');
            $this->assertEquals('2024-01-15', $formattedDate);

            /**
             * Vérifier diffForHumans() disponible
             */
            $this->assertIsString($post->published_at->diffForHumans());
        }
    }
    ```

??? abstract "7.2.2 : Tests Unit - Modèle User (Méthodes)"

    **Créer le fichier de test :**

    ```bash
    php artisan make:test UserTest --unit
    ```

    **Éditer `tests/Unit/UserTest.php` :**

    ```php
    <?php

    namespace Tests\Unit;

    use App\Models\Category;
    use App\Models\Post;
    use App\Models\User;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Support\Facades\Hash;
    use Tests\TestCase;

    /**
     * Tests Unit : Modèle User
     * 
     * Teste les méthodes et relations du modèle User
     */
    class UserTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * Test : Relation hasMany avec Posts
         * 
         * Vérifie :
         * - Utilisateur a plusieurs articles
         * - Relation chargée correctement
         */
        public function test_user_has_many_posts(): void
        {
            // Arrange : Créer utilisateur
            $user = User::factory()->create();
            $category = Category::factory()->create();

            // Créer 3 articles pour cet utilisateur
            Post::factory()->count(3)->create([
                'user_id' => $user->id,
                'category_id' => $category->id,
            ]);

            // Act : Charger relation posts
            $userPosts = $user->posts;

            // Assert : Vérifier relation
            $this->assertCount(3, $userPosts);
            $this->assertInstanceOf(\Illuminate\Database\Eloquent\Collection::class, $userPosts);

            /**
             * Vérifier tous articles appartiennent à l'utilisateur
             */
            foreach ($userPosts as $post) {
                $this->assertEquals($user->id, $post->user_id);
            }
        }

        /**
         * Test : Password hashé automatiquement
         * 
         * Vérifie :
         * - Attribut password hashé via mutator
         * - Hash vérifié avec Hash::check()
         */
        public function test_password_is_hashed_automatically(): void
        {
            // Arrange : Créer utilisateur avec password en clair
            /**
             * Factory UserFactory hash automatiquement le password
             * Ici on teste le mutator setPasswordAttribute() du modèle
             */
            $user = User::factory()->create([
                'password' => 'plaintext-password',
            ]);

            // Assert : Vérifier password hashé en BDD
            /**
             * Password ne doit PAS être stocké en clair
             */
            $this->assertNotEquals('plaintext-password', $user->password);

            /**
             * Vérifier hash bcrypt (commence par $2y$)
             */
            $this->assertStringStartsWith('$2y$', $user->password);

            /**
             * Vérifier Hash::check() valide le password
             */
            $this->assertTrue(Hash::check('plaintext-password', $user->password));
        }

        /**
         * Test : Attribut email unique (contrainte BDD)
         * 
         * Vérifie :
         * - Duplication email provoque exception
         */
        public function test_email_must_be_unique(): void
        {
            // Arrange : Créer premier utilisateur
            User::factory()->create([
                'email' => 'alice@example.com',
            ]);

            // Act & Assert : Tenter créer second utilisateur avec même email
            /**
             * expectException() : Attend exception spécifique
             * 
             * QueryException : Exception MySQL/PostgreSQL pour violations contraintes
             */
            $this->expectException(\Illuminate\Database\QueryException::class);

            /**
             * Création doit échouer (email dupliqué)
             */
            User::factory()->create([
                'email' => 'alice@example.com',
            ]);
        }

        /**
         * Test : Cast email_verified_at en Carbon
         * 
         * Vérifie :
         * - email_verified_at retourné comme instance Carbon
         */
        public function test_email_verified_at_is_cast_to_carbon(): void
        {
            // Arrange : Créer utilisateur avec email vérifié
            $user = User::factory()->create([
                'email_verified_at' => now(),
            ]);

            // Assert : Vérifier cast Carbon
            $this->assertInstanceOf(\Illuminate\Support\Carbon::class, $user->email_verified_at);

            /**
             * Vérifier méthodes Carbon disponibles
             */
            $this->assertIsString($user->email_verified_at->format('Y-m-d'));
        }

        /**
         * Test : Attributs fillable protègent mass assignment
         * 
         * Vérifie :
         * - Seuls attributs fillable peuvent être assignés en masse
         * - Attribut password protégé (hors fillable si non défini)
         */
        public function test_fillable_attributes_protect_mass_assignment(): void
        {
            // Arrange : Données utilisateur avec attribut non autorisé
            $userData = [
                'name' => 'Test User',
                'email' => 'test@example.com',
                'password' => bcrypt('password'),
                'is_admin' => true, // Hypothétique attribut non fillable
            ];

            // Act : Créer utilisateur via mass assignment
            /**
             * User::create() utilise $fillable du modèle
             * Attributs non listés dans $fillable sont ignorés
             */
            $user = User::create($userData);

            // Assert : Vérifier attributs fillable assignés
            $this->assertEquals('Test User', $user->name);
            $this->assertEquals('test@example.com', $user->email);

            /**
             * Vérifier attribut non fillable ignoré
             * 
             * Note : is_admin n'existe pas dans User par défaut
             * Cet exemple montre le principe de protection
             */
            // $this->assertNull($user->is_admin);
        }
    }
    ```

??? abstract "7.2.3 : Tests Unit - Helper Str::slug() (Validation)"

    **Test intégré dans PostTest :**

    Ce test vérifie que la génération de slug utilise correctement le helper Laravel `Str::slug()`.

    **Ajouter dans `tests/Unit/PostTest.php` :**

    ```php
    /**
     * Test : Génération slug gère caractères spéciaux
     * 
     * Vérifie :
     * - Accents convertis ou supprimés
     * - Caractères spéciaux supprimés
     * - Espaces multiples réduits à un tiret
     */
    public function test_slug_handles_special_characters(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act : Créer article avec titre complexe
        $post = Post::factory()->create([
            'title' => 'Article avec Accents ÉÈÊ & Symboles @#$ !!!',
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Assert : Vérifier slug nettoyé
        /**
         * Str::slug() Laravel transforme :
         * - Accents → caractères ASCII (É → e)
         * - Espaces → tirets
         * - Symboles → supprimés
         * - Tout en minuscules
         */
        $expectedSlug = 'article-avec-accents-eee-symboles';
        
        /**
         * assertMatchesRegularExpression() : Vérifie pattern regex
         * 
         * Pattern attendu : lettres minuscules + tirets uniquement
         */
        $this->assertMatchesRegularExpression('/^[a-z0-9-]+$/', $post->slug);
        
        /**
         * Vérifier slug ne contient pas caractères spéciaux
         */
        $this->assertStringNotContainsString('&', $post->slug);
        $this->assertStringNotContainsString('@', $post->slug);
        $this->assertStringNotContainsString('!', $post->slug);
    }

    /**
     * Test : Slug vide/null généré depuis titre par défaut
     * 
     * Vérifie :
     * - Si slug non fourni, généré depuis titre
     * - Événement creating() déclenché
     */
    public function test_empty_slug_is_generated_from_title(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act : Créer article SANS slug explicite
        $post = Post::factory()->create([
            'title' => 'Titre Sans Slug Explicite',
            'slug' => null, // Explicitement null
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Assert : Vérifier slug généré automatiquement
        $this->assertNotNull($post->slug);
        $this->assertEquals('titre-sans-slug-explicite', $post->slug);
    }
    ```

=== "**Tableau Récapitulatif Tests Unit**"

    | Test | Modèle | Objectif | Assertions Clés |
    |------|--------|----------|-----------------|
    | `test_slug_is_generated_automatically` | Post | Slug auto depuis titre | `assertEquals()` |
    | `test_duplicate_slugs_are_handled` | Post | Slugs uniques (suffixes) | `assertNotEquals()`, regex |
    | `test_published_scope_filters` | Post | Scope published() filtre | `assertCount()`, `contains()` |
    | `test_increment_views_increases` | Post | Incrément views_count | `assertEquals()`, `fresh()` |
    | `test_is_draft_method_works` | Post | isDraft() détection | `assertTrue()`, `assertFalse()` |
    | `test_belongs_to_user_relationship` | Post | Relation belongsTo User | `assertInstanceOf()` |
    | `test_belongs_to_category` | Post | Relation belongsTo Category | `assertInstanceOf()` |
    | `test_has_many_comments` | Post | Relation hasMany Comments | `assertCount()` |
    | `test_published_at_cast_carbon` | Post | Cast Carbon published_at | `assertInstanceOf()` |
    | `test_slug_handles_special_chars` | Post | Slug caractères spéciaux | `assertMatchesRegularExpression()` |
    | `test_user_has_many_posts` | User | Relation hasMany Posts | `assertCount()` |
    | `test_password_is_hashed` | User | Mutator password hash | `Hash::check()` |
    | `test_email_must_be_unique` | User | Contrainte unique email | `expectException()` |
    | `test_email_verified_at_cast` | User | Cast Carbon email_verified_at | `assertInstanceOf()` |

=== "**Exécuter les tests Unit**"

    ```bash
    # Tous les tests Unit
    php artisan test --testsuite=Unit

    # Test spécifique
    php artisan test --filter=PostTest

    # Test spécifique avec méthode
    php artisan test --filter=PostTest::test_slug_is_generated_automatically

    # Avec détails
    php artisan test --testsuite=Unit -v

    # Avec temps d'exécution
    php artisan test --testsuite=Unit --profile
    ```

    **Résultat attendu :**

    ```
    PASS  Tests\Unit\PostTest
    ✓ slug is generated automatically on create (0.03s)
    ✓ duplicate slugs are handled (0.04s)
    ✓ published scope filters correctly (0.05s)
    ✓ increment views increases counter (0.03s)
    ✓ is draft method works correctly (0.04s)
    ✓ belongs to user relationship (0.03s)
    ✓ belongs to category relationship (0.03s)
    ✓ has many comments relationship (0.05s)
    ✓ published at is cast to carbon (0.02s)
    ✓ slug handles special characters (0.03s)
    ✓ empty slug is generated from title (0.03s)

    PASS  Tests\Unit\UserTest
    ✓ user has many posts (0.04s)
    ✓ password is hashed automatically (0.02s)
    ✓ email must be unique (0.03s)
    ✓ email verified at is cast to carbon (0.02s)

    Tests:    15 passed (32 assertions)
    Duration: 0.38s
    ```

!!! note "**Différence vitesse Unit vs Feature :**"
    - Feature Tests : 1.10s pour 14 tests (HTTP + BDD)
    - Unit Tests : 0.38s pour 15 tests (logique pure)
    - **× 3 plus rapide** malgré plus de tests !

✅ **Étape 7.2 Terminée !**

**Fichiers créés :**

- `tests/Unit/PostTest.php` : 11 tests modèle Post
- `tests/Unit/UserTest.php` : 4 tests modèle User

**Concepts maîtrisés :**

- Tests méthodes modèles (isDraft, incrementViews)
- Tests scopes Eloquent (published)
- Tests relations (belongsTo, hasMany)
- Tests casts (Carbon, Hash)
- Tests génération slug (Str::slug)
- Tests contraintes BDD (unique)
- assertInstanceOf(), assertCount()
- assertMatchesRegularExpression()
- expectException()

### Étape 7.3 : Optimisation Performance

**Contexte :**

> L'optimisation performance transforme une application "fonctionnelle" en application **production-ready**. Un blog avec 1000 articles peut afficher des temps de réponse de **5 secondes** sans optimisation, contre **200ms** après optimisation. La différence entre abandon utilisateur et expérience fluide.

!!! note "**Impact performance sur business :**"

    - ✅ **SEO** : Google pénalise sites lents (-50% trafic si >3s)
    - ✅ **Conversion** : Chaque 100ms perdue = -1% conversion
    - ✅ **UX** : 53% utilisateurs abandonnent si >3s chargement
    - ✅ **Coûts** : Moins de ressources serveur nécessaires

**Les 5 piliers de l'optimisation Laravel :**

1. **Base de données** : Indexes, requêtes optimisées, Eager Loading
2. **Cache** : Views, routes, config, données métier
3. **Assets** : Minification, compression, CDN
4. **Configuration** : Mode production, autoloading optimisé
5. **Monitoring** : Identifier goulots d'étranglement

**Méthodologie d'optimisation :**

```
1. Mesurer (baseline) → 2. Identifier bottlenecks → 3. Optimiser → 4. Re-mesurer → 5. Répéter
```

??? abstract "7.3.1 : Optimisation Base de Données (Indexes)"

    **Contexte :**

    > Les **indexes** sont des structures de données qui accélèrent les requêtes SQL. Sans index, MySQL doit scanner **toute la table** (full table scan). Avec index, recherche devient logarithmique O(log n) au lieu de linéaire O(n).

    !!! note "**Exemple impact index :**"
        Table 100 000 articles sans index : **500ms**  
        Table 100 000 articles avec index : **5ms**  
        **× 100 plus rapide**

    **Règle d'or indexation :**

    > Indexer toutes colonnes utilisées dans `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY`

    **Créer une migration d'indexes :**

    ```bash
    php artisan make:migration add_indexes_to_posts_table
    ```

    **Éditer `database/migrations/XXXX_XX_XX_add_indexes_to_posts_table.php` :**

    ```php
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    return new class extends Migration
    {
        /**
         * Ajout des indexes pour optimisation performance
         * 
         * Indexes créés :
         * - posts.status (WHERE status = 'published')
         * - posts.published_at (WHERE published_at <= NOW())
         * - posts.slug (WHERE slug = '...' - Route Model Binding)
         * - posts.user_id (JOIN users ON posts.user_id = users.id)
         * - posts.category_id (JOIN categories ON posts.category_id = categories.id)
         * - posts.views_count (ORDER BY views_count DESC)
         * 
         * Index composite :
         * - (status, published_at) : Optimise scope published()
         */
        public function up(): void
        {
            Schema::table('posts', function (Blueprint $table) {
                /**
                 * INDEX SIMPLE : status
                 * 
                 * Utilisé dans :
                 * - Post::where('status', 'published')->get()
                 * - Scope published() : WHERE status = 'published'
                 * 
                 * Impact : × 50 plus rapide sur table 10k lignes
                 * 
                 * Note : Index ENUM (status) très efficace car peu de valeurs distinctes
                 */
                $table->index('status', 'idx_posts_status');

                /**
                 * INDEX SIMPLE : published_at
                 * 
                 * Utilisé dans :
                 * - WHERE published_at <= NOW()
                 * - ORDER BY published_at DESC
                 * 
                 * Impact : × 30 plus rapide pour tri chronologique
                 */
                $table->index('published_at', 'idx_posts_published_at');

                /**
                 * INDEX UNIQUE : slug
                 * 
                 * Utilisé dans :
                 * - Route Model Binding : WHERE slug = '...'
                 * - Vérification unicité slug
                 * 
                 * UNIQUE : Empêche duplicatas + optimise recherches
                 * 
                 * Impact : × 100 plus rapide (hash index pour égalité stricte)
                 * 
                 * Note : slug déjà indexé par défaut via unique() dans migration
                 * Cette ligne redondante mais explicite (documentation)
                 */
                // $table->unique('slug', 'idx_posts_slug_unique'); // Déjà existant

                /**
                 * INDEX FOREIGN KEY : user_id
                 * 
                 * Utilisé dans :
                 * - JOIN users ON posts.user_id = users.id
                 * - WHERE user_id = X (articles d'un auteur)
                 * 
                 * Impact : × 40 plus rapide pour relations belongsTo
                 * 
                 * Note : Clé étrangère crée automatiquement index dans MySQL/PostgreSQL
                 * Explicite ici pour compatibilité SQLite (pas d'index auto)
                 */
                // $table->index('user_id', 'idx_posts_user_id'); // Déjà via foreignId()

                /**
                 * INDEX FOREIGN KEY : category_id
                 * 
                 * Utilisé dans :
                 * - JOIN categories ON posts.category_id = categories.id
                 * - WHERE category_id = X (articles d'une catégorie)
                 */
                // $table->index('category_id', 'idx_posts_category_id'); // Déjà via foreignId()

                /**
                 * INDEX SIMPLE : views_count
                 * 
                 * Utilisé dans :
                 * - ORDER BY views_count DESC (articles populaires)
                 * - WHERE views_count > X (seuils popularité)
                 * 
                 * Impact : × 20 plus rapide pour tri par popularité
                 */
                $table->index('views_count', 'idx_posts_views_count');

                /**
                 * INDEX COMPOSITE : (status, published_at)
                 * 
                 * Utilisé dans :
                 * - Scope published() : WHERE status = 'published' AND published_at <= NOW()
                 * 
                 * Avantage index composite :
                 * MySQL utilise UN SEUL index au lieu de deux
                 * Condition AND optimisée (index covering query)
                 * 
                 * Impact : × 70 plus rapide que 2 index séparés
                 * 
                 * Ordre colonnes crucial :
                 * (status, published_at) : Optimal (status élimine 50% lignes d'abord)
                 * (published_at, status) : Moins optimal (dates moins sélectives)
                 * 
                 * Règle : Colonne la plus sélective EN PREMIER
                 */
                $table->index(['status', 'published_at'], 'idx_posts_status_published_at');
            });

            /**
             * Indexes pour table comments
             */
            Schema::table('comments', function (Blueprint $table) {
                /**
                 * INDEX : post_id
                 * 
                 * Utilisé dans :
                 * - $post->comments (relation hasMany)
                 * - WHERE post_id = X
                 */
                // $table->index('post_id', 'idx_comments_post_id'); // Déjà via foreignId()

                /**
                 * INDEX : approved
                 * 
                 * Utilisé dans :
                 * - WHERE approved = true (affichage publics)
                 * - Scope approved()
                 * 
                 * Impact : × 15 plus rapide pour filtrage modération
                 */
                $table->index('approved', 'idx_comments_approved');

                /**
                 * INDEX COMPOSITE : (post_id, approved)
                 * 
                 * Utilisé dans :
                 * - Commentaires approuvés d'un article
                 * - $post->comments()->where('approved', true)->get()
                 * 
                 * Impact : × 50 plus rapide que 2 index séparés
                 */
                $table->index(['post_id', 'approved'], 'idx_comments_post_approved');
            });

            /**
             * Indexes pour table categories
             */
            Schema::table('categories', function (Blueprint $table) {
                /**
                 * INDEX UNIQUE : slug
                 * 
                 * Utilisé dans :
                 * - Route Model Binding : WHERE slug = '...'
                 */
                // $table->unique('slug', 'idx_categories_slug_unique'); // Déjà existant
            });
        }

        /**
         * Supprimer les indexes (rollback)
         * 
         * Important : Supprimer dans ordre inverse de création
         */
        public function down(): void
        {
            Schema::table('posts', function (Blueprint $table) {
                // Supprimer index composite en premier
                $table->dropIndex('idx_posts_status_published_at');
                
                // Puis indexes simples
                $table->dropIndex('idx_posts_views_count');
                $table->dropIndex('idx_posts_published_at');
                $table->dropIndex('idx_posts_status');
            });

            Schema::table('comments', function (Blueprint $table) {
                $table->dropIndex('idx_comments_post_approved');
                $table->dropIndex('idx_comments_approved');
            });
        }
    };
    ```

    **Exécuter la migration :**

    ```bash
    php artisan migrate
    ```

    **Vérifier les indexes créés :**

    ```bash
    # MySQL
    php artisan tinker
    >>> DB::select('SHOW INDEX FROM posts');

    # Ou directement SQL
    mysql> SHOW INDEX FROM posts;
    ```

    !!! note "**Règles avancées indexation :**"
        
        **Quand créer index :**
        
        - ✅ Colonnes dans WHERE (80% des cas)
        - ✅ Colonnes dans JOIN (foreign keys)
        - ✅ Colonnes dans ORDER BY (tri)
        - ✅ Colonnes dans GROUP BY (agrégation)
        
        **Quand NE PAS créer index :**
        
        - ❌ Petites tables (<1000 lignes) : Full scan plus rapide
        - ❌ Colonnes mises à jour fréquemment : Index ralentit INSERT/UPDATE
        - ❌ Colonnes peu sélectives : ENUM avec 2 valeurs (true/false)
        - ❌ Trop d'indexes : Maximum 5-7 par table (balance lecture/écriture)

??? abstract "7.3.2 : Résolution Problème N+1 (Eager Loading)"

    **Contexte :**

    > Le **problème N+1** est le bug performance #1 des applications Laravel. Il survient quand on charge relations dans une boucle, générant **N requêtes SQL** au lieu d'une seule.

    !!! warning "**Exemple problème N+1 :**"
        ```php
        // Page d'accueil : 9 articles
        $posts = Post::all(); // 1 requête
        
        foreach ($posts as $post) {
            echo $post->user->name;     // 9 requêtes (1 par article)
            echo $post->category->name; // 9 requêtes (1 par article)
        }
        
        // Total : 1 + 9 + 9 = 19 requêtes SQL 😱
        ```

    **Solution : Eager Loading avec `with()`**

    **Vérifier tous les contrôleurs utilisent Eager Loading :**

    **Fichier : `app/Http/Controllers/HomeController.php`**

    ```php
    public function index()
    {
        /**
         * AVANT (N+1 problème) :
         * $posts = Post::published()->latest('published_at')->paginate(9);
         * 
         * Requêtes générées :
         * 1. SELECT * FROM posts WHERE status='published' AND published_at<=NOW() LIMIT 9
         * 2-10. SELECT * FROM users WHERE id=X (9 requêtes, 1 par article)
         * 11-19. SELECT * FROM categories WHERE id=X (9 requêtes, 1 par article)
         * 
         * Total : 19 requêtes
         */

        /**
         * APRÈS (Eager Loading) :
         * with(['user', 'category']) charge relations en 2 requêtes supplémentaires
         * 
         * Requêtes générées :
         * 1. SELECT * FROM posts WHERE status='published' AND published_at<=NOW() LIMIT 9
         * 2. SELECT * FROM users WHERE id IN (1, 2, 3, ...) (1 seule requête pour tous auteurs)
         * 3. SELECT * FROM categories WHERE id IN (1, 2, 3, ...) (1 seule requête pour toutes catégories)
         * 
         * Total : 3 requêtes (× 6 plus rapide)
         */
        $posts = Post::with(['user', 'category'])
            ->published()
            ->latest('published_at')
            ->paginate(9);

        /**
         * Catégories avec compteurs articles
         * withCount('posts') ajoute attribut virtuel posts_count
         * 
         * Requête générée :
         * SELECT categories.*, 
         *        (SELECT COUNT(*) FROM posts WHERE category_id = categories.id) as posts_count
         * FROM categories
         */
        $categories = Category::withCount('posts')->get();

        /**
         * Articles populaires (top 3 vues)
         * Eager Loading évite N+1 même pour 3 articles
         */
        $popularPosts = Post::with(['user', 'category'])
            ->published()
            ->orderBy('views_count', 'desc')
            ->limit(3)
            ->get();

        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
    ```

    **Fichier : `app/Http/Controllers/PostController.php`**

    ```php
    public function show(Post $post)
    {
        /**
         * Eager Loading relations pour page article
         * 
         * Relations chargées :
         * - user : Auteur article (belongsTo)
         * - category : Catégorie article (belongsTo)
         * - comments : Commentaires approuvés (hasMany + scope)
         */
        $post->load([
            'user',
            'category',
            'comments' => function ($query) {
                /**
                 * Closure permet filtrage relation
                 * Charge seulement commentaires approuvés
                 */
                $query->where('approved', true)
                      ->latest()
                      ->with('post'); // Évite N+1 si commentaires affichent article
            }
        ]);

        // Contrôle d'accès brouillons
        if ($post->status === 'draft' && (!auth()->check() || auth()->id() !== $post->user_id)) {
            abort(404);
        }

        // Incrémenter compteur vues
        $post->incrementViews();

        /**
         * Articles similaires (même catégorie)
         * Eager Loading évite N+1 pour 3 articles similaires
         */
        $similarPosts = Post::with(['user', 'category'])
            ->where('category_id', $post->category_id)
            ->where('id', '!=', $post->id)
            ->published()
            ->latest('published_at')
            ->limit(3)
            ->get();

        return view('posts.show', compact('post', 'similarPosts'));
    }
    ```

    **Fichier : `app/Http/Controllers/CategoryController.php`**

    ```php
    public function show(Category $category)
    {
        /**
         * Articles catégorie avec Eager Loading
         */
        $posts = $category->posts()
            ->with('user') // Charge auteurs (évite N+1)
            ->published()
            ->latest('published_at')
            ->paginate(9);

        return view('categories.show', compact('category', 'posts'));
    }
    ```

    **Fichier : `app/Http/Controllers/AuthorController.php`**

    ```php
    public function show(User $user)
    {
        /**
         * Articles auteur avec Eager Loading
         */
        $posts = $user->posts()
            ->with('category') // Charge catégories (évite N+1)
            ->published()
            ->latest('published_at')
            ->paginate(6);

        /**
         * Statistiques publiques
         * 
         * withCount() évite N+1 pour compteurs
         */
        $stats = [
            'total_posts' => $user->posts()->published()->count(),
            'total_views' => $user->posts()->published()->sum('views_count'),
            'total_comments' => $user->posts()
                ->published()
                ->withCount('comments')
                ->get()
                ->sum('comments_count'),
        ];

        return view('authors.show', compact('user', 'posts', 'stats'));
    }
    ```

    **Fichier : `app/Http/Controllers/DashboardController.php`**

    ```php
    public function index()
    {
        $user = auth()->user();

        /**
         * Tous articles auteur avec Eager Loading
         */
        $posts = Post::where('user_id', $user->id)
            ->with('category') // Évite N+1 pour affichage catégories
            ->latest()
            ->get();

        // Statistiques dashboard
        $stats = [
            'total_posts' => $posts->count(),
            'published_posts' => $posts->where('status', 'published')->count(),
            'draft_posts' => $posts->where('status', 'draft')->count(),
            'total_views' => $posts->sum('views_count'),
        ];

        /**
         * Article le plus populaire
         * Collection déjà chargée, pas de requête supplémentaire
         */
        $mostViewedPost = $posts->where('status', 'published')
            ->sortByDesc('views_count')
            ->first();

        return view('dashboard', compact('posts', 'stats', 'mostViewedPost'));
    }
    ```

    !!! note "**Techniques avancées Eager Loading :**"
        
        **1. Nested Eager Loading (relations imbriquées) :**
        ```php
        // Charger post → comments → user (auteur commentaire)
        $posts = Post::with(['comments.user'])->get();
        ```
        
        **2. Conditional Eager Loading :**
        ```php
        // Charger relation seulement si condition
        $posts = Post::with(['comments' => function ($query) {
            $query->where('approved', true)->latest();
        }])->get();
        ```
        
        **3. Lazy Eager Loading (charger après récupération) :**
        ```php
        $posts = Post::all();
        
        // Décider plus tard de charger relation
        if ($needUsers) {
            $posts->load('user');
        }
        ```
        
        **4. Load Missing (évite recharger) :**
        ```php
        // Charge seulement si pas déjà chargé
        $posts->loadMissing('user');
        ```

??? abstract "7.3.3 : Configuration Cache Laravel"

    **Contexte :**

    Laravel offre plusieurs niveaux de cache pour accélérer application. En production, **tous les caches doivent être activés**.

    !!! note "**Types de cache Laravel :**"
        
        1. **Config cache** : Fusionne tous fichiers config en 1 seul (bootstrap/cache/config.php)
        2. **Route cache** : Compile toutes routes en array PHP sérialisé
        3. **View cache** : Compile templates Blade en PHP pur
        4. **Event cache** : Cache listeners événements
        5. **Query cache** : Cache résultats requêtes BDD (manuel)

    **Commandes cache (à exécuter en production) :**

    **Créer un script de déploiement :**

    **Fichier : `scripts/optimize-production.sh`**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT OPTIMISATION PRODUCTION LARAVEL
    ###############################################################################
    # 
    # Usage : bash scripts/optimize-production.sh
    # 
    # Ce script :
    # 1. Clear tous les caches existants
    # 2. Recompile caches optimisés
    # 3. Optimise autoloader Composer
    # 4. Vérifie configuration production
    #
    ###############################################################################

    echo "🚀 Optimisation Laravel pour production..."

    ###############################################################################
    # ÉTAPE 1 : CLEAR CACHES EXISTANTS
    ###############################################################################
    echo ""
    echo "📦 Nettoyage caches existants..."

    # Clear application cache (Cache facade)
    php artisan cache:clear

    # Clear config cache
    php artisan config:clear

    # Clear route cache
    php artisan route:clear

    # Clear view cache (Blade templates compilés)
    php artisan view:clear

    # Clear event cache
    php artisan event:clear

    echo "✅ Caches nettoyés"

    ###############################################################################
    # ÉTAPE 2 : RECOMPILER CACHES OPTIMISÉS
    ###############################################################################
    echo ""
    echo "⚡ Compilation caches optimisés..."

    # Config cache : Fusionne tous config/*.php en 1 fichier
    # Impact : × 3 plus rapide chargement config
    # Fichier généré : bootstrap/cache/config.php
    php artisan config:cache

    # Route cache : Compile routes/web.php + api.php en array PHP
    # Impact : × 10 plus rapide résolution routes
    # Fichier généré : bootstrap/cache/routes-v7.php
    # 
    # ATTENTION : Désactive route closures (utiliser seulement contrôleurs)
    php artisan route:cache

    # View cache : Compile tous .blade.php en PHP pur
    # Impact : × 5 plus rapide rendu vues
    # Dossier : storage/framework/views/
    php artisan view:cache

    # Event cache : Cache listeners événements
    # Impact : × 2 plus rapide dispatch events
    php artisan event:cache

    echo "✅ Caches optimisés créés"

    ###############################################################################
    # ÉTAPE 3 : OPTIMISER AUTOLOADER COMPOSER
    ###############################################################################
    echo ""
    echo "📚 Optimisation autoloader Composer..."

    # Génère classmap optimisé (toutes classes mappées)
    # Impact : × 4 plus rapide chargement classes
    # Fichiers générés : vendor/composer/autoload_*.php
    composer install --optimize-autoloader --no-dev

    echo "✅ Autoloader optimisé"

    ###############################################################################
    # ÉTAPE 4 : VÉRIFICATION CONFIGURATION PRODUCTION
    ###############################################################################
    echo ""
    echo "🔍 Vérification configuration production..."

    # Vérifier APP_ENV=production
    if grep -q "APP_ENV=production" .env; then
        echo "✅ APP_ENV=production"
    else
        echo "⚠️  ATTENTION : APP_ENV n'est pas 'production'"
    fi

    # Vérifier APP_DEBUG=false
    if grep -q "APP_DEBUG=false" .env; then
        echo "✅ APP_DEBUG=false"
    else
        echo "⚠️  ATTENTION : APP_DEBUG devrait être 'false' en production"
    fi

    # Vérifier APP_KEY défini
    if grep -q "APP_KEY=base64:" .env; then
        echo "✅ APP_KEY défini"
    else
        echo "❌ ERREUR : APP_KEY non défini ! Exécuter : php artisan key:generate"
    fi

    ###############################################################################
    # RÉSUMÉ
    ###############################################################################
    echo ""
    echo "✅ Optimisation terminée !"
    echo ""
    echo "Fichiers générés :"
    echo "  - bootstrap/cache/config.php"
    echo "  - bootstrap/cache/routes-v7.php"
    echo "  - storage/framework/views/*.php"
    echo "  - vendor/composer/autoload_*.php"
    echo ""
    echo "⚡ Application optimisée pour production"
    ```

    **Rendre le script exécutable :**

    ```bash
    chmod +x scripts/optimize-production.sh
    ```

    **Exécuter l'optimisation :**

    ```bash
    bash scripts/optimize-production.sh
    ```

    !!! warning "**IMPORTANT : Route Cache et Closures**"
        
        `php artisan route:cache` **désactive** les closures dans routes.
        
        **Interdit en production :**
        ```php
        // routes/web.php
        Route::get('/', function () {
            return view('home');
        }); // ❌ Closure non supportée avec route:cache
        ```
        
        **Autorisé en production :**
        ```php
        // routes/web.php
        Route::get('/', [HomeController::class, 'index']); // ✅ Contrôleur supporté
        ```
        
        Toutes nos routes utilisent déjà des contrôleurs → Compatible route:cache ✅

    **Cache données métier (manuel) :**

    **Exemple : Cache sidebar catégories (rarement modifiées)**

    **Fichier : `app/Http/Controllers/HomeController.php`**

    ```php
    use Illuminate\Support\Facades\Cache;

    public function index()
    {
        $posts = Post::with(['user', 'category'])
            ->published()
            ->latest('published_at')
            ->paginate(9);

        /**
         * Cache catégories 24 heures
         * 
         * Cache::remember($key, $ttl, $callback) :
         * - Si clé existe : Retourne valeur en cache
         * - Si clé n'existe pas : Exécute callback + met en cache
         * 
         * TTL : 60 * 24 = 1440 minutes = 24 heures
         * 
         * Impact : × 50 plus rapide (évite requête BDD + calcul withCount)
         */
        $categories = Cache::remember('sidebar_categories', 60 * 24, function () {
            return Category::withCount('posts')->get();
        });

        /**
         * Cache articles populaires 1 heure
         * 
         * TTL : 60 minutes = 1 heure
         * Mis à jour fréquemment car views_count change souvent
         */
        $popularPosts = Cache::remember('popular_posts', 60, function () {
            return Post::with(['user', 'category'])
                ->published()
                ->orderBy('views_count', 'desc')
                ->limit(3)
                ->get();
        });

        return view('home', compact('posts', 'categories', 'popularPosts'));
    }
    ```

    **Invalider cache quand catégorie créée/modifiée :**

    **Fichier : `app/Models/Category.php`**

    ```php
    use Illuminate\Support\Facades\Cache;

    protected static function booted()
    {
        /**
         * Invalider cache sidebar quand catégorie créée
         */
        static::created(function () {
            Cache::forget('sidebar_categories');
        });

        /**
         * Invalider cache sidebar quand catégorie mise à jour
         */
        static::updated(function () {
            Cache::forget('sidebar_categories');
        });

        /**
         * Invalider cache sidebar quand catégorie supprimée
         */
        static::deleted(function () {
            Cache::forget('sidebar_categories');
        });
    }
    ```

    !!! note "**Stratégies cache avancées :**"
        
        **1. Cache Tags (Redis/Memcached uniquement) :**
        ```php
        // Grouper clés par tags
        Cache::tags(['posts', 'homepage'])->put('key', 'value', 3600);
        
        // Invalider tous articles en 1 commande
        Cache::tags(['posts'])->flush();
        ```
        
        **2. Cache Forever (jusqu'à invalidation manuelle) :**
        ```php
        Cache::forever('settings', $settings);
        Cache::forget('settings'); // Invalider
        ```
        
        **3. Cache Atomic Lock (éviter race conditions) :**
        ```php
        $lock = Cache::lock('process-post-'.$postId, 10);
        
        if ($lock->get()) {
            // Traitement exclusif
            $lock->release();
        }
        ```

??? abstract "7.3.4 : Optimisation Assets (CSS/JS)"

    **Contexte :**

    Les assets (CSS, JS, images) représentent **70% du poids** d'une page web. Optimiser assets = réduire bande passante + accélérer chargement.

    !!! note "**Techniques optimisation assets :**"
        
        1. **Minification** : Supprimer espaces/commentaires (30% poids)
        2. **Compression** : Gzip/Brotli (70% poids)
        3. **Bundling** : Fusionner fichiers (réduire requêtes HTTP)
        4. **Cache navigateur** : Headers Cache-Control (éviter re-téléchargement)
        5. **CDN** : Servir depuis serveurs géographiquement proches

    **Laravel Vite (configuration par défaut)**

    Vite est déjà configuré pour optimisation production. Vérifier `vite.config.js` :

    **Fichier : `vite.config.js`**

    ```javascript
    import { defineConfig } from 'vite';
    import laravel from 'laravel-vite-plugin';

    export default defineConfig({
        plugins: [
            laravel({
                input: [
                    'resources/css/app.css',
                    'resources/js/app.js',
                ],
                refresh: true,
            }),
        ],
        
        /**
         * Configuration optimisation production
         * 
         * Activée automatiquement avec : npm run build
         */
        build: {
            /**
             * Minification JavaScript
             * 
             * Options :
             * - 'esbuild' : Rapide (défaut)
             * - 'terser' : Plus agressif (5% plus petit)
             */
            minify: 'esbuild',
            
            /**
             * Source maps en production
             * 
             * false : Désactive (recommandé production)
             * true : Active (debug production)
             */
            sourcemap: false,
            
            /**
             * Taille limite warning (Ko)
             * 
             * 500 Ko : Alerte si bundle trop gros
             */
            chunkSizeWarningLimit: 500,
            
            /**
             * Rollup options (bundler)
             */
            rollupOptions: {
                output: {
                    /**
                     * Noms fichiers buildés
                     * 
                     * [name] : Nom original (app)
                     * [hash] : Hash contenu (cache busting)
                     * 
                     * Exemple : app-a3f2c1b9.js
                     */
                    entryFileNames: 'assets/[name]-[hash].js',
                    chunkFileNames: 'assets/[name]-[hash].js',
                    assetFileNames: 'assets/[name]-[hash].[ext]',
                }
            }
        },
    });
    ```

    **Build production :**

    ```bash
    # Compiler assets pour production
    npm run build
    ```

    **Résultat :**

    ```
    vite v5.x.x building for production...
    ✓ 127 modules transformed.
    
    public/build/manifest.json                    0.45 kB │ gzip: 0.23 kB
    public/build/assets/app-a3f2c1b9.css          8.42 kB │ gzip: 2.15 kB
    public/build/assets/app-b7e4d3a1.js         142.37 kB │ gzip: 46.82 kB
    
    ✓ built in 3.24s
    ```

    **Vérifier références dans layout :**

    **Fichier : `resources/views/layouts/app.blade.php`**

    ```blade
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        {{-- Vite gère automatiquement :
             - Mode dev : http://localhost:5173/resources/css/app.css (HMR)
             - Mode prod : /build/assets/app-a3f2c1b9.css (minifié + hash) --}}
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body>
        <!-- Contenu -->
    </body>
    </html>
    ```

    !!! note "**Cache navigateur (headers HTTP) :**"
        
        **Configurer Nginx pour caching assets :**
        
        ```nginx
        # /etc/nginx/sites-available/blog.conf
        
        location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf)$ {
            # Cache 1 an (assets hashés = cache busting)
            expires 1y;
            add_header Cache-Control "public, immutable";
            
            # Compression Gzip
            gzip on;
            gzip_types text/css application/javascript image/svg+xml;
            gzip_vary on;
        }
        ```
        
        **Résultat headers HTTP :**
        ```
        Cache-Control: public, immutable, max-age=31536000
        Content-Encoding: gzip
        ```
        
        **Impact :** Assets téléchargés 1 fois, utilisés depuis cache ensuite

??? abstract "7.3.5 : Monitoring Performance (Laravel Debugbar)"

    **Contexte :**

    Impossible d'optimiser sans **mesurer**. Laravel Debugbar affiche métriques performance en temps réel : requêtes SQL, temps exécution, mémoire, etc.

    !!! warning "**Installation DÉVELOPPEMENT uniquement**"
        Debugbar ne doit **JAMAIS** être installé en production (fuite infos sensibles)

    **Installer Laravel Debugbar :**

    ```bash
    composer require barryvdh/laravel-debugbar --dev
    ```

    **Flag `--dev` :** Package installé uniquement en environnement développement (pas en production)

    **Configuration (optionnel) :**

    **Fichier : `config/debugbar.php`** (généré automatiquement)

    ```php
    return [
        /**
         * Activer Debugbar seulement si :
         * - APP_DEBUG=true
         * - Environnement local
         */
        'enabled' => env('DEBUGBAR_ENABLED', env('APP_DEBUG', false)),

        /**
         * Collectors activés
         */
        'collectors' => [
            'phpinfo'         => true,  // Infos PHP
            'messages'        => true,  // Messages debug
            'time'            => true,  // Temps exécution
            'memory'          => true,  // Mémoire utilisée
            'exceptions'      => true,  // Exceptions
            'log'             => true,  // Logs Laravel
            'db'              => true,  // Requêtes SQL ⚡ LE PLUS IMPORTANT
            'views'           => true,  // Vues Blade
            'route'           => true,  // Route actuelle
            'auth'            => false, // Utilisateur connecté
            'gate'            => true,  // Autorisations
            'session'         => true,  // Session
            'cache'           => true,  // Cache
            'events'          => false, // Événements
            'models'          => true,  // Modèles chargés
        ],
    ];
    ```

    **Utilisation Debugbar :**

    1. **Ouvrir application en développement** (APP_DEBUG=true)
    2. **Barre debug apparaît en bas de page**
    3. **Cliquer onglet "Queries"** pour voir requêtes SQL

    !!! note "**Métriques clés Debugbar :**"
        
        **Onglet Queries (requêtes SQL) :**
        
        - **Nombre requêtes** : <10 = excellent, 10-30 = moyen, >30 = problème N+1
        - **Temps total SQL** : <50ms = excellent, 50-200ms = moyen, >200ms = lent
        - **Duplicate queries** : Highlight rouge = même requête répétée (N+1)
        
        **Onglet Timeline :**
        
        - **Temps total** : <200ms = excellent, 200-500ms = moyen, >500ms = lent
        - **Temps PHP** : Logique métier pure
        - **Temps SQL** : Base de données
        
        **Onglet Memory :**
        
        - **Mémoire peak** : <16MB = excellent, 16-32MB = moyen, >32MB = fuite

    **Exemple détection N+1 avec Debugbar :**

    **AVANT optimisation (problème N+1) :**

    ```
    Queries: 19 (duplicate: 18)  |  Time: 342ms
    
    1. SELECT * FROM posts WHERE status='published' LIMIT 9        [12ms]
    2. SELECT * FROM users WHERE id=1                              [18ms]  ← Duplicate
    3. SELECT * FROM users WHERE id=2                              [17ms]  ← Duplicate
    4. SELECT * FROM users WHERE id=1                              [16ms]  ← Duplicate
    5. SELECT * FROM categories WHERE id=3                         [19ms]  ← Duplicate
    ...
    ```

    **APRÈS optimisation (Eager Loading) :**

    ```
    Queries: 3 (duplicate: 0)  |  Time: 45ms
    
    1. SELECT * FROM posts WHERE status='published' LIMIT 9        [12ms]
    2. SELECT * FROM users WHERE id IN (1, 2, 3)                   [15ms]
    3. SELECT * FROM categories WHERE id IN (1, 2, 3)              [18ms]
    ```

    **Impact : × 7.6 plus rapide + 16 requêtes économisées** ✅

=== "**Tableau Récapitulatif Optimisations**"

    | Optimisation | Impact Performance | Difficulté | Commande/Fichier |
    |--------------|-------------------|------------|------------------|
    | **Indexes BDD** | × 50-100 | Facile | Migration `add_indexes_to_posts_table` |
    | **Eager Loading** | × 5-10 | Facile | `with(['user', 'category'])` dans contrôleurs |
    | **Config cache** | × 3 | Facile | `php artisan config:cache` |
    | **Route cache** | × 10 | Facile | `php artisan route:cache` |
    | **View cache** | × 5 | Facile | `php artisan view:cache` |
    | **Autoloader** | × 4 | Facile | `composer install --optimize-autoloader --no-dev` |
    | **Assets minify** | × 2-3 | Facile | `npm run build` (Vite auto) |
    | **Query cache** | × 50 | Moyen | `Cache::remember()` manuel |
    | **Headers cache** | × ∞ | Moyen | Configuration Nginx/Apache |

=== "**Checklist Déploiement Production**"

    **Avant chaque déploiement, vérifier :**

    ```bash
    # 1. Variables environnement
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (php artisan key:generate)

    # 2. Optimisations Laravel
    ✅ php artisan config:cache
    ✅ php artisan route:cache
    ✅ php artisan view:cache
    ✅ php artisan event:cache

    # 3. Composer optimisé
    ✅ composer install --optimize-autoloader --no-dev

    # 4. Assets compilés
    ✅ npm run build

    # 5. Migrations à jour
    ✅ php artisan migrate --force

    # 6. Permissions correctes
    ✅ chmod -R 775 storage bootstrap/cache
    ✅ chown -R www-data:www-data storage bootstrap/cache

    # 7. Vérification santé
    ✅ php artisan route:list (vérifier routes compilées)
    ✅ php artisan config:show (vérifier config cached)
    ```

=== "**Comparaison Performance Avant/Après**"

    **Métriques page d'accueil (9 articles) :**

    | Métrique | Avant Optimisation | Après Optimisation | Amélioration |
    |----------|-------------------|-------------------|--------------|
    | **Requêtes SQL** | 19 | 3 | × 6.3 moins |
    | **Temps SQL** | 342ms | 45ms | × 7.6 plus rapide |
    | **Temps total** | 580ms | 120ms | × 4.8 plus rapide |
    | **Mémoire** | 24 MB | 18 MB | -25% |
    | **Taille page** | 850 KB | 320 KB | -62% (gzip) |
    | **TTFB** | 420ms | 85ms | × 4.9 plus rapide |

    **Résultat : Page d'accueil × 5 plus rapide** 🚀

✅ **Étape 7.3 Terminée !**

**Fichiers créés/modifiés :**

- `database/migrations/XXXX_add_indexes_to_posts_table.php` : Indexes BDD
- `scripts/optimize-production.sh` : Script optimisation automatique
- Tous contrôleurs : Eager Loading avec `with()`
- `vite.config.js` : Configuration build production

**Concepts maîtrisés :**

- Indexes simples et composites
- Eager Loading (with, load, withCount)
- Cache Laravel (config, route, view, query)
- Optimisation assets (Vite, minification)
- Monitoring performance (Debugbar)
- Headers cache navigateur
- Stratégies cache avancées

### Étape 7.4 : Sécurité et Hardening

**Contexte :**

> La sécurité est **non négociable** en production. Une faille exploitée = données volées, site défacé, réputation détruite. Laravel intègre protections natives mais nécessite configuration correcte.

!!! note "**Top 5 vulnérabilités web (OWASP 2024) :**"

    1. **Broken Access Control** : Utilisateur accède ressources non autorisées
    2. **Cryptographic Failures** : Données sensibles non chiffrées
    3. **Injection** : SQL, XSS, Command Injection
    4. **Insecure Design** : Architecture vulnérable par conception
    5. **Security Misconfiguration** : Erreurs configuration (debug=true prod)

**Protections Laravel natives (déjà actives) :**

- ✅ **CSRF** : Tokens anti-Cross-Site Request Forgery (`@csrf`)
- ✅ **XSS** : Échappement auto HTML (`{{ }}` vs `{!! !!}`)
- ✅ **SQL Injection** : Requêtes préparées (Eloquent/Query Builder)
- ✅ **Password Hashing** : Bcrypt automatique (mutateur)
- ✅ **Session Security** : Cookies HttpOnly, SameSite

??? abstract "7.4.1 : Rate Limiting (Protection Brute Force)"

    **Contexte :**

    Le **rate limiting** limite nombre de requêtes par IP/utilisateur. Empêche attaques brute force (login, formulaires, API).

    !!! warning "**Exemples attaques sans rate limiting :**"
        - **Login brute force** : 10 000 tentatives/seconde → mot de passe craqué
        - **Comment spam** : 1000 commentaires/minute → pollution base
        - **Scraping** : 100 000 requêtes/heure → vol contenu

    **Configurer rate limiting routes publiques :**

    **Fichier : `app/Providers/RouteServiceProvider.php`**

    ```php
    <?php

    namespace App\Providers;

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\RateLimiter;
    use Illuminate\Support\Facades\Route;

    class RouteServiceProvider extends ServiceProvider
    {
        public const HOME = '/dashboard';

        public function boot(): void
        {
            /**
             * Rate limiter API (déjà configuré par Laravel)
             * 60 requêtes/minute par IP
             */
            RateLimiter::for('api', function (Request $request) {
                return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
            });

            /**
             * Rate limiter CONNEXION
             * 
             * Protection brute force login :
             * - 5 tentatives par minute par IP
             * - Identifié par email + IP (empêche rotation IP)
             * - Response 429 Too Many Requests si dépassé
             */
            RateLimiter::for('login', function (Request $request) {
                $throttleKey = strtolower($request->input('email')).'|'.$request->ip();
                
                return Limit::perMinute(5)->by($throttleKey)->response(function () {
                    return response()->json([
                        'message' => 'Trop de tentatives de connexion. Réessayez dans 1 minute.'
                    ], 429);
                });
            });

            /**
             * Rate limiter COMMENTAIRES
             * 
             * Protection spam :
             * - 3 commentaires par minute par IP
             * - Empêche flood commentaires
             */
            RateLimiter::for('comments', function (Request $request) {
                return Limit::perMinute(3)->by($request->ip())->response(function () {
                    return back()->with('error', 'Trop de commentaires envoyés. Patientez 1 minute.');
                });
            });

            /**
             * Rate limiter CRÉATION ARTICLES
             * 
             * Protection spam articles :
             * - 10 articles par heure par utilisateur
             */
            RateLimiter::for('create-posts', function (Request $request) {
                return Limit::perHour(10)->by($request->user()->id);
            });

            $this->routes(function () {
                Route::middleware('api')
                    ->prefix('api')
                    ->group(base_path('routes/api.php'));

                Route::middleware('web')
                    ->group(base_path('routes/web.php'));
            });
        }
    }
    ```

    **Appliquer rate limiting aux routes :**

    **Fichier : `routes/web.php`**

    ```php
    use Illuminate\Support\Facades\Route;
    use App\Http\Controllers\{
        HomeController, PostController, CommentController,
        CategoryController, AuthorController, DashboardController, ProfileController
    };

    // Routes publiques
    Route::get('/', [HomeController::class, 'index'])->name('home');
    Route::get('/posts/{post:slug}', [PostController::class, 'show'])->name('posts.show');
    Route::get('/category/{category:slug}', [CategoryController::class, 'show'])->name('categories.show');
    Route::get('/author/{user}', [AuthorController::class, 'show'])->name('authors.show');

    /**
     * Route commentaires avec rate limiting
     * middleware('throttle:comments') applique limiter 'comments'
     */
    Route::post('/posts/{post}/comments', [CommentController::class, 'store'])
        ->middleware('throttle:comments')
        ->name('comments.store');

    // Routes authentification Breeze (login déjà protégé dans auth.php)
    require __DIR__.'/auth.php';

    // Routes protégées (authentification requise)
    Route::middleware('auth')->group(function () {
        Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
        
        // Profil
        Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
        Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
        Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
        
        /**
         * Création/édition articles avec rate limiting
         */
        Route::middleware('throttle:create-posts')->group(function () {
            Route::get('/posts/create', [PostController::class, 'create'])->name('posts.create');
            Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
        });
        
        Route::get('/posts/{post}/edit', [PostController::class, 'edit'])->name('posts.edit');
        Route::put('/posts/{post}', [PostController::class, 'update'])->name('posts.update');
        Route::delete('/posts/{post}', [PostController::class, 'destroy'])->name('posts.destroy');
        
        // Modération commentaires
        Route::patch('/comments/{comment}/approve', [CommentController::class, 'approve'])->name('comments.approve');
        Route::delete('/comments/{comment}', [CommentController::class, 'destroy'])->name('comments.destroy');
    });
    ```

    **Tester rate limiting :**

    ```bash
    # Envoyer 10 commentaires rapidement (dépasser limite)
    for i in {1..10}; do
        curl -X POST http://localhost:8000/posts/mon-article/comments \
            -d "author_name=Test&author_email=test@example.com&content=Spam $i"
    done
    
    # Après 3 requêtes → 429 Too Many Requests
    ```

??? abstract "7.4.2 : Headers Sécurité HTTP"

    **Contexte :**

    Les **headers HTTP** contrôlent comportement navigateur. Headers sécurité protègent contre XSS, clickjacking, injection code.

    **Créer middleware headers sécurité :**

    ```bash
    php artisan make:middleware SecurityHeaders
    ```

    **Fichier : `app/Http/Middleware/SecurityHeaders.php`**

    ```php
    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Http\Request;
    use Symfony\Component\HttpFoundation\Response;

    class SecurityHeaders
    {
        /**
         * Ajoute headers sécurité à toutes les réponses
         */
        public function handle(Request $request, Closure $next): Response
        {
            $response = $next($request);

            /**
             * X-Content-Type-Options: nosniff
             * 
             * Empêche navigateur "deviner" type MIME
             * Force respect Content-Type déclaré
             * Protège contre attaques MIME sniffing
             */
            $response->headers->set('X-Content-Type-Options', 'nosniff');

            /**
             * X-Frame-Options: DENY
             * 
             * Empêche site être chargé dans <iframe>
             * Protège contre clickjacking
             * 
             * Alternatives :
             * - DENY : Interdit tous iframes
             * - SAMEORIGIN : Autorise iframes même domaine
             */
            $response->headers->set('X-Frame-Options', 'DENY');

            /**
             * X-XSS-Protection: 1; mode=block
             * 
             * Active filtre XSS navigateur (anciens navigateurs)
             * mode=block : Bloque page si XSS détecté
             * 
             * Note : Obsolète (remplacé CSP) mais compatible anciens navigateurs
             */
            $response->headers->set('X-XSS-Protection', '1; mode=block');

            /**
             * Referrer-Policy: strict-origin-when-cross-origin
             * 
             * Contrôle infos envoyées dans header Referer
             * 
             * Options :
             * - no-referrer : Jamais d'info referer
             * - same-origin : Referer seulement même domaine
             * - strict-origin-when-cross-origin : URL complète même origine, domaine seulement cross-origin
             */
            $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');

            /**
             * Content-Security-Policy (CSP)
             * 
             * Définit sources autorisées pour scripts, styles, images
             * Protection ultime contre XSS
             * 
             * Directives :
             * - default-src 'self' : Par défaut, seulement même origine
             * - script-src 'self' 'unsafe-inline' : Scripts même origine + inline (Vite HMR)
             * - style-src 'self' 'unsafe-inline' : CSS même origine + inline (Tailwind)
             * - img-src 'self' data: https: : Images même origine + data URIs + HTTPS externes
             * - font-src 'self' : Fonts même origine
             * - connect-src 'self' : AJAX/WebSocket même origine
             * 
             * Note : 'unsafe-inline' nécessaire pour Vite dev + Tailwind
             * Production : Remplacer par nonces ou hashes
             */
            $response->headers->set('Content-Security-Policy', 
                "default-src 'self'; " .
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; " .
                "style-src 'self' 'unsafe-inline'; " .
                "img-src 'self' data: https:; " .
                "font-src 'self'; " .
                "connect-src 'self';"
            );

            /**
             * Permissions-Policy
             * 
             * Contrôle accès APIs navigateur (géolocalisation, caméra, etc.)
             * 
             * Directives désactivées :
             * - geolocation : Géolocalisation
             * - microphone : Microphone
             * - camera : Caméra
             * - payment : API Payment Request
             */
            $response->headers->set('Permissions-Policy', 
                'geolocation=(), microphone=(), camera=(), payment=()'
            );

            /**
             * Strict-Transport-Security (HSTS)
             * 
             * Force HTTPS pendant 1 an
             * includeSubDomains : Applique sous-domaines
             * preload : Eligible liste preload navigateurs
             * 
             * ATTENTION : Activer SEULEMENT si certificat SSL configuré
             */
            if ($request->secure()) {
                $response->headers->set('Strict-Transport-Security', 
                    'max-age=31536000; includeSubDomains; preload'
                );
            }

            return $response;
        }
    }
    ```

    **Enregistrer middleware globalement :**

    **Fichier : `bootstrap/app.php`**

    ```php
    <?php

    use Illuminate\Foundation\Application;
    use Illuminate\Foundation\Configuration\Exceptions;
    use Illuminate\Foundation\Configuration\Middleware;

    return Application::configure(basePath: dirname(__DIR__))
        ->withRouting(
            web: __DIR__.'/../routes/web.php',
            commands: __DIR__.'/../routes/console.php',
            health: '/up',
        )
        ->withMiddleware(function (Middleware $middleware) {
            /**
             * Ajouter SecurityHeaders à toutes les requêtes web
             */
            $middleware->web(append: [
                \App\Http\Middleware\SecurityHeaders::class,
            ]);
        })
        ->withExceptions(function (Exceptions $exceptions) {
            //
        })->create();
    ```

    **Tester headers (DevTools) :**

    ```bash
    # Ouvrir page dans navigateur
    # F12 → Network → Sélectionner requête → Headers
    
    # Vérifier présence :
    ✅ X-Content-Type-Options: nosniff
    ✅ X-Frame-Options: DENY
    ✅ Content-Security-Policy: ...
    ✅ Strict-Transport-Security: ... (si HTTPS)
    ```

??? abstract "7.4.3 : Validation Stricte Entrées Utilisateur"

    **Contexte :**

    **"Never trust user input"** est la règle #1 sécurité. Toute donnée externe doit être validée côté serveur (validation client = contournable).

    **Renforcer validation contrôleurs :**

    **Fichier : `app/Http/Controllers/PostController.php`**

    ```php
    public function store(Request $request)
    {
        /**
         * Validation STRICTE
         * 
         * Règles renforcées :
         * - max:255 : Limite taille (prévient DOS)
         * - exists:... : Vérifie FK (prévient injection)
         * - min:100 : Force qualité contenu
         * - url : Valide format URL strict
         * - regex:... : Patterns spécifiques si besoin
         */
        $validated = $request->validate([
            'title' => [
                'required',
                'string',
                'max:255',
                // Optionnel : Interdire caractères spéciaux dangereux
                'regex:/^[a-zA-Z0-9\s\-\.\']+$/u',
            ],
            'category_id' => [
                'required',
                'integer',
                'exists:categories,id', // Vérifie catégorie existe
            ],
            'excerpt' => [
                'required',
                'string',
                'max:500',
            ],
            'content' => [
                'required',
                'string',
                'min:100',
                'max:50000', // Limite max (prévient DOS)
            ],
            'image' => [
                'nullable',
                'url', // Valide format URL
                'max:500',
            ],
            'status' => [
                'required',
                'in:draft,published', // Whitelist stricte (pas de "admin", etc.)
            ],
        ], [
            // Messages personnalisés français
            'title.required' => 'Le titre est obligatoire.',
            'title.max' => 'Le titre ne peut dépasser 255 caractères.',
            'title.regex' => 'Le titre contient des caractères non autorisés.',
            'category_id.exists' => 'La catégorie sélectionnée n\'existe pas.',
            'content.min' => 'Le contenu doit contenir au moins 100 caractères.',
            'content.max' => 'Le contenu ne peut dépasser 50 000 caractères.',
            'status.in' => 'Le statut doit être "brouillon" ou "publié".',
        ]);

        /**
         * Sanitization supplémentaire (optionnel)
         * 
         * Laravel échappe automatiquement HTML via {{ }}
         * Mais peut nettoyer davantage si besoin :
         */
        // $validated['title'] = strip_tags($validated['title']);
        // $validated['content'] = strip_tags($validated['content'], '<p><br><strong><em><ul><ol><li>');

        // Création article
        $post = auth()->user()->posts()->create($validated);

        return redirect()
            ->route('posts.show', $post->slug)
            ->with('success', 'Article créé avec succès.');
    }
    ```

    **Validation commentaires (protection spam) :**

    **Fichier : `app/Http/Controllers/CommentController.php`**

    ```php
    public function store(Request $request, Post $post)
    {
        $validated = $request->validate([
            'author_name' => [
                'required',
                'string',
                'max:255',
                // Interdire URLs dans nom (spam)
                'not_regex:/https?:\/\//',
            ],
            'author_email' => [
                'required',
                'email:rfc,dns', // Validation stricte email + DNS check
                'max:255',
            ],
            'content' => [
                'required',
                'string',
                'min:10',
                'max:1000',
                // Interdire URLs multiples (spam)
                function ($attribute, $value, $fail) {
                    if (substr_count($value, 'http') > 2) {
                        $fail('Le commentaire contient trop de liens.');
                    }
                },
            ],
        ], [
            'author_name.not_regex' => 'Le nom ne peut contenir de liens.',
            'author_email.email' => 'L\'adresse email n\'est pas valide.',
            'content.min' => 'Le commentaire doit contenir au moins 10 caractères.',
            'content.max' => 'Le commentaire ne peut dépasser 1000 caractères.',
        ]);

        /**
         * Honeypot anti-spam (optionnel)
         * 
         * Champ caché dans formulaire, invisible utilisateur
         * Si rempli → bot détecté → rejeter
         */
        if ($request->filled('website')) { // 'website' = champ honeypot
            return back()->with('error', 'Spam détecté.');
        }

        // Création commentaire (non approuvé par défaut)
        $post->comments()->create([
            ...$validated,
            'approved' => false,
        ]);

        return back()->with('success', 'Commentaire envoyé. Il sera visible après modération.');
    }
    ```

??? abstract "7.4.4 : Protection Variables Environnement"

    **Contexte :**

    Le fichier `.env` contient **secrets** (DB password, API keys). Il ne doit **JAMAIS** être commité Git ou accessible web.

    **Vérifier `.gitignore` (déjà configuré) :**

    **Fichier : `.gitignore`**

    ```gitignore
    # Fichiers sensibles (JAMAIS commiter)
    .env
    .env.backup
    .env.production
    .phpunit.result.cache

    # Caches Laravel
    /bootstrap/cache/*
    /storage/*.key
    /storage/logs/*

    # Node modules
    /node_modules
    /public/hot
    /public/storage
    /public/build

    # Vendor
    /vendor
    ```

    **Permissions fichier .env (serveur production) :**

    ```bash
    # .env lisible seulement par propriétaire (root ou www-data)
    chmod 600 .env
    chown www-data:www-data .env
    
    # Vérifier
    ls -la .env
    # -rw------- 1 www-data www-data 1024 Dec 11 10:30 .env
    ```

    **Bloquer accès .env via Nginx :**

    ```nginx
    # /etc/nginx/sites-available/blog.conf
    
    location ~ /\.env {
        deny all;
        return 404;
    }
    
    # Bloquer aussi autres fichiers sensibles
    location ~ /\.(git|svn|hg) {
        deny all;
        return 404;
    }
    ```

    **Exemple .env production sécurisé :**

    ```bash
    # Application
    APP_NAME="Mon Blog"
    APP_ENV=production
    APP_KEY=base64:GENERER_AVEC_php_artisan_key:generate
    APP_DEBUG=false  # ⚠️ TOUJOURS false en production
    APP_URL=https://monblog.com

    # Base de données
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=blog_prod
    DB_USERNAME=blog_user
    DB_PASSWORD=MOT_DE_PASSE_TRES_FORT_32_CHARS  # ⚠️ JAMAIS 'root' ou 'password'

    # Cache/Sessions
    CACHE_DRIVER=redis
    SESSION_DRIVER=redis
    QUEUE_CONNECTION=redis

    # Redis (si utilisé)
    REDIS_PASSWORD=MOT_DE_PASSE_REDIS_FORT

    # Mail
    MAIL_MAILER=smtp
    MAIL_HOST=smtp.mailtrap.io
    MAIL_PORT=587
    MAIL_USERNAME=your_username
    MAIL_PASSWORD=your_password  # ⚠️ Token API, pas password perso
    ```

=== "**Checklist Sécurité Production**"

    **Avant déploiement, vérifier :**

    ```bash
    # Configuration
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (32 chars aléatoires)
    
    # Base de données
    ✅ DB_PASSWORD fort (min 16 chars)
    ✅ DB_USERNAME dédié (PAS root)
    ✅ Accès BDD limité à localhost/IP serveur
    
    # Fichiers
    ✅ .env permissions 600
    ✅ storage/ permissions 775
    ✅ .env dans .gitignore
    
    # Headers HTTP
    ✅ SecurityHeaders middleware actif
    ✅ HTTPS forcé (HSTS)
    ✅ CSP configuré
    
    # Rate Limiting
    ✅ Login : 5/min
    ✅ Commentaires : 3/min
    ✅ Création articles : 10/h
    
    # Validation
    ✅ Règles strictes tous formulaires
    ✅ exists: sur toutes FK
    ✅ max: sur tous champs texte
    
    # Serveur
    ✅ Firewall actif (UFW/iptables)
    ✅ SSH clés uniquement (pas password)
    ✅ Fail2ban configuré
    ✅ Mises à jour auto sécurité
    ```

=== "**Tests Sécurité Automatisés**"

    **Scanner vulnérabilités avec Enlightn :**

    ```bash
    # Installer Enlightn Security Checker
    composer require enlightn/enlightn --dev
    
    # Exécuter scan sécurité
    php artisan enlightn
    
    # Résultat : Rapport détaillé vulnérabilités
    ```

    **Tester headers sécurité avec securityheaders.com :**

    ```bash
    # Analyser headers production
    https://securityheaders.com/?q=https://monblog.com
    
    # Score attendu : A+ (tous headers présents)
    ```

=== "**Résumé Protections Implémentées**"

    | Protection | Technologie | Fichier/Config |
    |------------|-------------|----------------|
    | **CSRF** | Token Laravel | `@csrf` (déjà actif) |
    | **XSS** | Échappement Blade | `{{ }}` (déjà actif) |
    | **SQL Injection** | Requêtes préparées | Eloquent (déjà actif) |
    | **Brute Force Login** | Rate limiting | `RouteServiceProvider` (5/min) |
    | **Comment Spam** | Rate limiting | `RouteServiceProvider` (3/min) |
    | **Clickjacking** | X-Frame-Options | `SecurityHeaders` middleware |
    | **MIME Sniffing** | X-Content-Type | `SecurityHeaders` middleware |
    | **Code Injection** | CSP | `SecurityHeaders` middleware |
    | **HTTPS** | HSTS | `SecurityHeaders` middleware |
    | **Validation** | Rules strictes | Tous contrôleurs |
    | **Secrets** | .env protégé | Permissions 600 + Nginx deny |

✅ **Étape 7.4 Terminée !**

**Fichiers créés/modifiés :**

- `app/Providers/RouteServiceProvider.php` : Rate limiting (login, comments, posts)
- `app/Http/Middleware/SecurityHeaders.php` : Headers sécurité HTTP
- `bootstrap/app.php` : Enregistrement middleware global
- `routes/web.php` : Application throttle aux routes
- Contrôleurs : Validation stricte renforcée

**Concepts maîtrisés :**

- Rate limiting (throttle)
- Headers sécurité HTTP (CSP, HSTS, X-Frame-Options)
- Validation stricte (regex, exists, custom rules)
- Protection .env (permissions, .gitignore)
- Middleware sécurité global
- Honeypot anti-spam

**Application maintenant protégée contre :**

- ✅ Brute force (login/formulaires)
- ✅ XSS (échappement + CSP)
- ✅ CSRF (tokens Laravel)
- ✅ SQL Injection (Eloquent)
- ✅ Clickjacking (X-Frame-Options)
- ✅ Spam commentaires (rate limiting + validation)
- ✅ MITM (HTTPS forcé HSTS)





























































### Étape 7.5 : Configuration Production

**Contexte :**

> La configuration production diffère fondamentalement du développement. Un `.env` mal configuré = performances dégradées, failles sécurité, ou pire : **perte de données**. Cette étape configure Laravel pour environnement production robuste.

**Différences dev vs production :**

| Paramètre | Développement | Production |
|-----------|---------------|------------|
| **APP_DEBUG** | `true` (traces erreurs) | `false` (messages génériques) |
| **APP_ENV** | `local` | `production` |
| **CACHE_DRIVER** | `file` (simple) | `redis` (performant) |
| **SESSION_DRIVER** | `file` | `redis` ou `database` |
| **QUEUE_CONNECTION** | `sync` (immédiat) | `redis` (asynchrone) |
| **LOG_LEVEL** | `debug` (tout) | `error` (critique uniquement) |

**Architecture production recommandée :**

```
┌─────────────────┐
│   Nginx/Apache  │ → Serveur web (reverse proxy)
└────────┬────────┘
         │
┌────────▼────────┐
│   PHP-FPM 8.2+  │ → Processeur PHP
└────────┬────────┘
         │
┌────────▼────────┐
│  Laravel App    │ → Application
└────┬───────┬────┘
     │       │
┌────▼───┐ ┌─▼─────┐
│ MySQL  │ │ Redis │ → Stockage données + cache
└────────┘ └───────┘
```

??? abstract "7.5.1 : Fichier .env Production (Template Complet)"

    **Créer fichier template production :**

    **Fichier : `.env.production.example`** (à copier en `.env` sur serveur)

    ```bash
    ###############################################################################
    # CONFIGURATION PRODUCTION - LARAVEL BLOG MULTI-AUTEURS
    ###############################################################################
    #
    # Ce fichier sert de template pour environnement production
    # 
    # INSTRUCTIONS DÉPLOIEMENT :
    # 1. Copier ce fichier : cp .env.production.example .env
    # 2. Remplir TOUTES les valeurs avec vrais credentials
    # 3. Générer APP_KEY : php artisan key:generate
    # 4. Sécuriser : chmod 600 .env && chown www-data:www-data .env
    # 5. Vérifier : php artisan config:show
    #
    ###############################################################################

    ###############################################################################
    # APPLICATION
    ###############################################################################

    # Nom application (affiché dans emails, notifications)
    APP_NAME="Mon Blog"

    # Environnement : TOUJOURS 'production' en prod
    # Valeurs possibles : local, staging, production
    APP_ENV=production

    # Clé chiffrement (32 chars aléatoires)
    # ⚠️ GÉNÉRER AVEC : php artisan key:generate
    # ⚠️ NE JAMAIS partager cette clé
    # ⚠️ NE JAMAIS changer en production (sessions/données chiffrées perdues)
    APP_KEY=

    # Debug mode : TOUJOURS false en production
    # ⚠️ true = FUITE INFOS SENSIBLES (stack traces, config, BDD)
    APP_DEBUG=false

    # URL application (avec protocole https://)
    # Utilisé pour génération liens emails, assets CDN
    APP_URL=https://monblog.com

    # Timezone application
    # Liste : https://www.php.net/manual/en/timezones.php
    APP_TIMEZONE=Europe/Paris

    # Locale (langue interface)
    APP_LOCALE=fr
    APP_FALLBACK_LOCALE=en

    ###############################################################################
    # BASE DE DONNÉES
    ###############################################################################

    # Driver : mysql, pgsql, sqlite, sqlsrv
    DB_CONNECTION=mysql

    # Host : 127.0.0.1 (local) ou IP serveur distant
    # Production : Toujours local (sécurité) ou IP interne VPC
    DB_HOST=127.0.0.1

    # Port : 3306 (MySQL), 5432 (PostgreSQL)
    DB_PORT=3306

    # Nom base de données
    # Convention : {app}_production
    DB_DATABASE=blog_production

    # Utilisateur dédié (PAS root)
    # Créer avec : CREATE USER 'blog_user'@'localhost' IDENTIFIED BY '...';
    DB_USERNAME=blog_user

    # Password FORT (min 16 chars, mix alphanum + symboles)
    # Générer : openssl rand -base64 24
    # ⚠️ JAMAIS 'root', 'password', 'admin'
    DB_PASSWORD=

    ###############################################################################
    # CACHE
    ###############################################################################

    # Driver cache : file, redis, memcached, database, array
    # Production : redis (performances optimales)
    # Alternative : memcached ou database si pas Redis
    CACHE_DRIVER=redis

    # Préfixe clés cache (évite collisions multi-apps)
    CACHE_PREFIX=blog_cache_

    ###############################################################################
    # SESSION
    ###############################################################################

    # Driver session : file, cookie, database, redis
    # Production : redis ou database (partage entre serveurs)
    # Éviter : file (pas scalable multi-serveurs)
    SESSION_DRIVER=redis

    # Durée session (minutes)
    # 120 = 2 heures (connexion utilisateur)
    SESSION_LIFETIME=120

    # Chiffrer cookies session (sécurité supplémentaire)
    SESSION_ENCRYPT=true

    # Cookies accessibles seulement via HTTP (pas JavaScript)
    # Protection XSS
    SESSION_HTTP_ONLY=true

    # SameSite : lax, strict, none
    # lax : Protection CSRF tout en permettant liens externes
    SESSION_SAME_SITE=lax

    # Cookies sécurisés (HTTPS uniquement)
    # ⚠️ true = HTTPS obligatoire
    SESSION_SECURE_COOKIE=true

    ###############################################################################
    # QUEUE (JOBS ASYNCHRONES)
    ###############################################################################

    # Driver queue : sync, database, redis, sqs, beanstalkd
    # Production : redis (performant, durable)
    # sync = développement (exécution immédiate)
    QUEUE_CONNECTION=redis

    ###############################################################################
    # REDIS
    ###############################################################################

    # Host Redis : 127.0.0.1 (local) ou IP serveur
    REDIS_HOST=127.0.0.1

    # Port Redis : 6379 (défaut)
    REDIS_PORT=6379

    # Password Redis (fortement recommandé production)
    # Configurer dans redis.conf : requirepass <password>
    REDIS_PASSWORD=

    # Base de données Redis (0-15)
    # Séparer cache/session/queue pour éviter flush accidentel
    REDIS_CACHE_DB=0
    REDIS_SESSION_DB=1
    REDIS_QUEUE_DB=2

    ###############################################################################
    # MAIL
    ###############################################################################

    # Mailer : smtp, sendmail, mailgun, ses, postmark
    # Production : Service dédié (Mailgun, SendGrid, AWS SES)
    MAIL_MAILER=smtp

    # Serveur SMTP
    # Exemples :
    # - Mailgun : smtp.mailgun.org
    # - SendGrid : smtp.sendgrid.net
    # - Gmail : smtp.gmail.com (déconseillé prod)
    MAIL_HOST=smtp.mailgun.org

    # Port SMTP : 587 (TLS), 465 (SSL), 25 (non chiffré - éviter)
    MAIL_PORT=587

    # Username SMTP (souvent email ou API key)
    MAIL_USERNAME=

    # Password SMTP ou API token
    MAIL_PASSWORD=

    # Chiffrement : tls, ssl, null
    # 587 → tls, 465 → ssl
    MAIL_ENCRYPTION=tls

    # Adresse expéditeur par défaut
    MAIL_FROM_ADDRESS=noreply@monblog.com
    MAIL_FROM_NAME="${APP_NAME}"

    ###############################################################################
    # LOGGING
    ###############################################################################

    # Channel : stack, single, daily, slack, syslog, errorlog
    # Production : daily (rotation automatique journalière)
    LOG_CHANNEL=daily

    # Niveau log : debug, info, notice, warning, error, critical, alert, emergency
    # Production : error (seulement erreurs critiques)
    # Développement : debug (tout)
    LOG_LEVEL=error

    # Rétention logs (jours)
    # daily channel : Supprime logs > X jours
    LOG_DAILY_DAYS=14

    ###############################################################################
    # BROADCASTING (TEMPS RÉEL - Optionnel)
    ###############################################################################

    # Driver : pusher, redis, log, null
    # null = désactivé (pas de temps réel)
    BROADCAST_DRIVER=null

    ###############################################################################
    # FILESYSTEM
    ###############################################################################

    # Disk par défaut : local, public, s3
    # Production : s3 (AWS) ou equivalent (DigitalOcean Spaces, Cloudflare R2)
    # local = développement uniquement
    FILESYSTEM_DISK=local

    # AWS S3 (si utilisé)
    # AWS_ACCESS_KEY_ID=
    # AWS_SECRET_ACCESS_KEY=
    # AWS_DEFAULT_REGION=eu-west-1
    # AWS_BUCKET=
    # AWS_USE_PATH_STYLE_ENDPOINT=false

    ###############################################################################
    # SERVICES EXTERNES (Optionnel)
    ###############################################################################

    # Vite (assets)
    # Production : npm run build génère manifeste
    # Développement : serveur HMR sur port 5173
    VITE_APP_NAME="${APP_NAME}"

    ###############################################################################
    # SÉCURITÉ ADDITIONNELLE
    ###############################################################################

    # Hasher : bcrypt, argon, argon2id
    # bcrypt = défaut Laravel (compatible, éprouvé)
    # argon2id = plus sécurisé (nécessite extension PHP)
    HASH_DRIVER=bcrypt

    # Rounds bcrypt (complexité hashing)
    # 10 = défaut (100ms hash)
    # 12 = plus sécurisé (400ms hash, ralentit brute force)
    BCRYPT_ROUNDS=10

    ###############################################################################
    # DÉBOGAGE PRODUCTION (À RETIRER EN PROD)
    ###############################################################################

    # Telescope (monitoring Laravel - dev/staging uniquement)
    # TELESCOPE_ENABLED=false

    # Debugbar (barre debug - dev uniquement)
    # DEBUGBAR_ENABLED=false
    ```

    **Générer password sécurisés :**

    ```bash
    # Password BDD (24 chars aléatoires)
    openssl rand -base64 24
    # Exemple : 7Kf2mP9xQw3nRt8sVb4cYh6d
    
    # Password Redis (32 chars aléatoires)
    openssl rand -base64 32
    # Exemple : 9Xm2pL7wQz5nRv8tYc4bHf6gJs3kDr1a
    
    # APP_KEY (généré par Laravel)
    php artisan key:generate
    # Écrit automatiquement dans .env
    ```

??? abstract "7.5.2 : Configuration Services Externes"

    **Contexte :**

    Production nécessite services externes robustes pour emails, cache, monitoring. Configuration optimale selon budget.

    **Option 1 : Budget limité (<10€/mois)**

    **Stack "All-in-One" :**

    - **Serveur** : VPS (Hetzner 5€/mois, DigitalOcean 6$/mois)
    - **BDD** : MySQL local (inclus)
    - **Cache** : Redis local (inclus)
    - **Mail** : Brevo (ex-Sendinblue) 300 emails/jour gratuit
    - **Assets** : Serveur local (pas CDN)

    **Configuration .env (budget limité) :**

    ```bash
    # Tout sur même serveur
    DB_HOST=127.0.0.1
    REDIS_HOST=127.0.0.1
    
    # Mail gratuit Brevo
    MAIL_MAILER=smtp
    MAIL_HOST=smtp-relay.brevo.com
    MAIL_PORT=587
    MAIL_USERNAME=votre-email@example.com
    MAIL_PASSWORD=votre-cle-api-brevo
    
    # Filesystem local
    FILESYSTEM_DISK=local
    ```

    **Option 2 : Budget moyen (50-100€/mois)**

    **Stack "Séparation Services" :**

    - **Serveur** : VPS (DigitalOcean 24$/mois)
    - **BDD** : Managed MySQL (DigitalOcean 15$/mois)
    - **Cache** : Managed Redis (DigitalOcean 15$/mois)
    - **Mail** : Mailgun 35$/mois (50k emails)
    - **Assets** : S3-compatible (Spaces 5$/mois 250GB)
    - **CDN** : Cloudflare gratuit

    **Configuration .env (budget moyen) :**

    ```bash
    # BDD managée
    DB_HOST=db-mysql-fra1-12345.ondigitalocean.com
    DB_PORT=25060
    DB_USERNAME=doadmin
    DB_PASSWORD=mot_de_passe_genere
    DB_SSLMODE=require  # Connexion chiffrée
    
    # Redis managé
    REDIS_HOST=redis-fra1-12345.ondigitalocean.com
    REDIS_PORT=25061
    REDIS_PASSWORD=mot_de_passe_genere
    REDIS_TLS=true  # Connexion chiffrée
    
    # Mail Mailgun
    MAIL_MAILER=mailgun
    MAILGUN_DOMAIN=mg.monblog.com
    MAILGUN_SECRET=cle-api-mailgun
    
    # S3-compatible (DigitalOcean Spaces)
    FILESYSTEM_DISK=s3
    AWS_ACCESS_KEY_ID=votre-access-key
    AWS_SECRET_ACCESS_KEY=votre-secret-key
    AWS_DEFAULT_REGION=fra1
    AWS_BUCKET=blog-assets
    AWS_ENDPOINT=https://fra1.digitaloceanspaces.com
    AWS_USE_PATH_STYLE_ENDPOINT=false
    ```

    **Option 3 : Budget entreprise (>200€/mois)**

    **Stack "Haute Disponibilité" :**

    - **Serveur** : Multi-instances (Load Balancer)
    - **BDD** : Cluster MySQL (réplication master-slave)
    - **Cache** : Cluster Redis (haute dispo)
    - **Mail** : SendGrid/AWS SES (volume illimité)
    - **Assets** : CloudFront CDN (AWS)
    - **Monitoring** : New Relic / Datadog
    - **Backup** : Automatisé quotidien

    **Configuration .env (entreprise) :**

    ```bash
    # BDD cluster avec read replicas
    DB_HOST=mysql-cluster-master.internal
    DB_PORT=3306
    DB_READ_HOSTS=mysql-replica1.internal,mysql-replica2.internal
    
    # Redis cluster
    REDIS_CLUSTER=true
    REDIS_HOSTS=redis1.internal:6379,redis2.internal:6379,redis3.internal:6379
    
    # AWS SES (emails)
    MAIL_MAILER=ses
    AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    AWS_DEFAULT_REGION=eu-west-1
    
    # CloudFront CDN
    AWS_CLOUDFRONT_DOMAIN=d123456abcdef.cloudfront.net
    
    # Monitoring New Relic
    NEW_RELIC_LICENSE_KEY=votre-cle-licence
    NEW_RELIC_APP_NAME="Mon Blog Production"
    ```

    !!! note "**Comparaison services mail (emails transactionnels) :**"
        
        | Service | Gratuit | Payant | Avantages | Inconvénients |
        |---------|---------|--------|-----------|---------------|
        | **Brevo** | 300/jour | 19€/mois (20k) | Simple, interface FR | Limite gratuite basse |
        | **Mailgun** | 5k/mois | 35$/mois (50k) | Fiable, analytics | Configuration DNS |
        | **SendGrid** | 100/jour | 15$/mois (40k) | Réputation, livrabilité | Interface complexe |
        | **AWS SES** | 62k/mois | $0.10/1000 | Très économique volume | Requiert compte AWS |
        | **Postmark** | Essai 100 | 15$/mois (10k) | Excellent support | Plus cher petit volume |

??? abstract "7.5.3 : Configuration Redis (Cache + Sessions + Queue)"

    **Installer Redis (si pas déjà fait) :**

    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install redis-server
    
    # Démarrer service
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Vérifier statut
    sudo systemctl status redis-server
    
    # Tester connexion
    redis-cli ping
    # Réponse attendue : PONG
    ```

    **Configurer Redis sécurisé :**

    **Fichier : `/etc/redis/redis.conf`**

    ```conf
    ###############################################################################
    # CONFIGURATION REDIS PRODUCTION
    ###############################################################################

    # Bind : Écoute seulement localhost (sécurité)
    # Production : 127.0.0.1 (local uniquement)
    # Multi-serveurs : IP interne VPC
    bind 127.0.0.1

    # Port : 6379 (défaut)
    port 6379

    # Password : TOUJOURS définir en production
    # Générer : openssl rand -base64 32
    requirepass VOTRE_PASSWORD_REDIS_FORT

    # Persistence : RDB (snapshots) + AOF (journal)
    # RDB : Snapshot toutes les 60s si ≥1000 changements
    save 60 1000
    save 300 100
    save 900 1

    # AOF : Journal append-only (durabilité)
    appendonly yes
    appendfsync everysec

    # Mémoire max : Limite selon RAM serveur
    # Exemple : 512MB sur serveur 2GB
    maxmemory 512mb

    # Éviction : Politique suppression clés si mémoire pleine
    # allkeys-lru : Supprime clés moins récemment utilisées (LRU)
    maxmemory-policy allkeys-lru

    # Logs
    loglevel notice
    logfile /var/log/redis/redis-server.log

    # Supervision (optionnel)
    supervised systemd
    ```

    **Redémarrer Redis après config :**

    ```bash
    sudo systemctl restart redis-server
    ```

    **Tester connexion avec password :**

    ```bash
    redis-cli
    127.0.0.1:6379> AUTH VOTRE_PASSWORD_REDIS_FORT
    OK
    127.0.0.1:6379> ping
    PONG
    127.0.0.1:6379> exit
    ```

    **Configurer Laravel pour utiliser Redis :**

    **Fichier : `config/database.php`** (vérifier configuration)

    ```php
    'redis' => [
        'client' => env('REDIS_CLIENT', 'phpredis'),

        'options' => [
            'cluster' => env('REDIS_CLUSTER', 'redis'),
            'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        ],

        'default' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_DB', '0'),
        ],

        'cache' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_CACHE_DB', '1'),
        ],

        'session' => [
            'url' => env('REDIS_URL'),
            'host' => env('REDIS_HOST', '127.0.0.1'),
            'username' => env('REDIS_USERNAME'),
            'password' => env('REDIS_PASSWORD'),
            'port' => env('REDIS_PORT', '6379'),
            'database' => env('REDIS_SESSION_DB', '2'),
        ],
    ],
    ```

    **Installer extension PHP Redis :**

    ```bash
    # phpredis (extension native, plus performante)
    sudo apt install php8.2-redis
    
    # Ou predis (package PHP pur, fallback)
    composer require predis/predis
    
    # Redémarrer PHP-FPM
    sudo systemctl restart php8.2-fpm
    
    # Vérifier extension chargée
    php -m | grep redis
    # Doit afficher : redis
    ```

    **Tester connexion Laravel → Redis :**

    ```bash
    php artisan tinker
    
    # Tester cache Redis
    >>> Cache::put('test', 'Hello Redis', 60);
    >>> Cache::get('test');
    => "Hello Redis"
    
    # Vérifier dans Redis
    >>> exit
    
    redis-cli
    127.0.0.1:6379> AUTH VOTRE_PASSWORD
    OK
    127.0.0.1:6379> KEYS *test*
    1) "blog_cache_:test"
    127.0.0.1:6379> GET blog_cache_:test
    "s:11:\"Hello Redis\";"
    ```

??? abstract "7.5.4 : Vérification Configuration (Commandes Artisan)"

    **Commandes vérification pré-déploiement :**

    **Script vérification automatique :**

    **Fichier : `scripts/verify-production-config.sh`**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT VÉRIFICATION CONFIGURATION PRODUCTION
    ###############################################################################
    #
    # Usage : bash scripts/verify-production-config.sh
    #
    # Vérifie :
    # - Variables environnement critiques
    # - Connexions services (BDD, Redis, Mail)
    # - Permissions fichiers
    # - Optimisations actives
    #
    ###############################################################################

    echo "🔍 Vérification configuration production Laravel..."
    echo ""

    ###############################################################################
    # COULEURS (pour affichage terminal)
    ###############################################################################
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color

    ###############################################################################
    # COMPTEURS
    ###############################################################################
    ERRORS=0
    WARNINGS=0
    SUCCESS=0

    ###############################################################################
    # FONCTION : Vérifier variable .env
    ###############################################################################
    check_env() {
        local var_name=$1
        local expected=$2
        local value=$(grep "^${var_name}=" .env | cut -d '=' -f2)
        
        if [ "$value" == "$expected" ]; then
            echo -e "${GREEN}✅${NC} ${var_name}=${expected}"
            ((SUCCESS++))
        else
            echo -e "${RED}❌${NC} ${var_name}=${value} (attendu: ${expected})"
            ((ERRORS++))
        fi
    }

    ###############################################################################
    # FONCTION : Vérifier variable définie
    ###############################################################################
    check_env_set() {
        local var_name=$1
        local value=$(grep "^${var_name}=" .env | cut -d '=' -f2)
        
        if [ -n "$value" ]; then
            echo -e "${GREEN}✅${NC} ${var_name} défini"
            ((SUCCESS++))
        else
            echo -e "${RED}❌${NC} ${var_name} NON défini"
            ((ERRORS++))
        fi
    }

    ###############################################################################
    # ÉTAPE 1 : VÉRIFIER FICHIER .env EXISTE
    ###############################################################################
    echo "📋 Vérification fichier .env..."
    if [ -f .env ]; then
        echo -e "${GREEN}✅${NC} Fichier .env trouvé"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Fichier .env MANQUANT"
        echo "   Créer avec : cp .env.production.example .env"
        ((ERRORS++))
        exit 1
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 2 : VÉRIFIER VARIABLES CRITIQUES
    ###############################################################################
    echo "🔧 Vérification variables environnement critiques..."

    # APP_ENV doit être 'production'
    check_env "APP_ENV" "production"

    # APP_DEBUG doit être 'false'
    check_env "APP_DEBUG" "false"

    # APP_KEY doit être défini
    check_env_set "APP_KEY"

    # DB_PASSWORD doit être défini
    check_env_set "DB_PASSWORD"

    echo ""

    ###############################################################################
    # ÉTAPE 3 : TESTER CONNEXION BASE DE DONNÉES
    ###############################################################################
    echo "🗄️  Test connexion base de données..."
    if php artisan db:show > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} Connexion MySQL réussie"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Connexion MySQL ÉCHEC"
        echo "   Vérifier : DB_HOST, DB_USERNAME, DB_PASSWORD"
        ((ERRORS++))
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 4 : TESTER CONNEXION REDIS
    ###############################################################################
    echo "🔴 Test connexion Redis..."
    if php artisan tinker --execute="Cache::put('test', 'ok', 10); echo Cache::get('test');" | grep -q "ok"; then
        echo -e "${GREEN}✅${NC} Connexion Redis réussie"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Connexion Redis ÉCHEC (optionnel)"
        echo "   Cache utilisera driver 'file' (moins performant)"
        ((WARNINGS++))
    fi
    echo ""

    ###############################################################################
    # ÉTAPE 5 : VÉRIFIER CACHES COMPILÉS
    ###############################################################################
    echo "⚡ Vérification caches optimisés..."

    # Config cache
    if [ -f bootstrap/cache/config.php ]; then
        echo -e "${GREEN}✅${NC} Config cache compilé"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Config cache manquant"
        echo "   Exécuter : php artisan config:cache"
        ((WARNINGS++))
    fi

    # Route cache
    if [ -f bootstrap/cache/routes-v7.php ]; then
        echo -e "${GREEN}✅${NC} Route cache compilé"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Route cache manquant"
        echo "   Exécuter : php artisan route:cache"
        ((WARNINGS++))
    fi

    # View cache
    if [ -d storage/framework/views ] && [ "$(ls -A storage/framework/views)" ]; then
        echo -e "${GREEN}✅${NC} View cache présent"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  View cache vide"
        echo "   Exécuter : php artisan view:cache"
        ((WARNINGS++))
    fi

    echo ""

    ###############################################################################
    # ÉTAPE 6 : VÉRIFIER PERMISSIONS FICHIERS
    ###############################################################################
    echo "🔐 Vérification permissions fichiers..."

    # .env doit être 600 (lisible propriétaire uniquement)
    ENV_PERMS=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null)
    if [ "$ENV_PERMS" == "600" ]; then
        echo -e "${GREEN}✅${NC} Permissions .env : 600 (sécurisé)"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Permissions .env : ${ENV_PERMS} (dangereux)"
        echo "   Corriger : chmod 600 .env"
        ((ERRORS++))
    fi

    # storage/ doit être 775
    STORAGE_PERMS=$(stat -c "%a" storage 2>/dev/null || stat -f "%A" storage 2>/dev/null)
    if [ "$STORAGE_PERMS" == "775" ]; then
        echo -e "${GREEN}✅${NC} Permissions storage/ : 775"
        ((SUCCESS++))
    else
        echo -e "${YELLOW}⚠️${NC}  Permissions storage/ : ${STORAGE_PERMS}"
        echo "   Corriger : chmod -R 775 storage"
        ((WARNINGS++))
    fi

    echo ""

    ###############################################################################
    # ÉTAPE 7 : VÉRIFIER ASSETS COMPILÉS
    ###############################################################################
    echo "📦 Vérification assets production..."

    # Manifeste Vite doit exister
    if [ -f public/build/manifest.json ]; then
        echo -e "${GREEN}✅${NC} Assets Vite compilés"
        ((SUCCESS++))
    else
        echo -e "${RED}❌${NC} Assets Vite NON compilés"
        echo "   Exécuter : npm run build"
        ((ERRORS++))
    fi

    echo ""

    ###############################################################################
    # RÉSUMÉ
    ###############################################################################
    echo "═══════════════════════════════════════════════════════════"
    echo "📊 RÉSUMÉ VÉRIFICATION"
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${GREEN}✅ Succès :${NC}       ${SUCCESS}"
    echo -e "${YELLOW}⚠️  Avertissements :${NC} ${WARNINGS}"
    echo -e "${RED}❌ Erreurs :${NC}      ${ERRORS}"
    echo ""

    if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 Configuration production PARFAITE !${NC}"
        echo "   Prêt pour déploiement."
        exit 0
    elif [ $ERRORS -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Configuration fonctionnelle avec avertissements${NC}"
        echo "   Corriger les avertissements pour performances optimales."
        exit 0
    else
        echo -e "${RED}❌ Configuration INVALIDE${NC}"
        echo "   Corriger les erreurs avant déploiement."
        exit 1
    fi
    ```

    **Rendre le script exécutable :**

    ```bash
    chmod +x scripts/verify-production-config.sh
    ```

    **Exécuter vérification :**

    ```bash
    bash scripts/verify-production-config.sh
    ```

    **Résultat attendu :**

    ```
    🔍 Vérification configuration production Laravel...

    📋 Vérification fichier .env...
    ✅ Fichier .env trouvé

    🔧 Vérification variables environnement critiques...
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY défini
    ✅ DB_PASSWORD défini

    🗄️  Test connexion base de données...
    ✅ Connexion MySQL réussie

    🔴 Test connexion Redis...
    ✅ Connexion Redis réussie

    ⚡ Vérification caches optimisés...
    ✅ Config cache compilé
    ✅ Route cache compilé
    ✅ View cache présent

    🔐 Vérification permissions fichiers...
    ✅ Permissions .env : 600 (sécurisé)
    ✅ Permissions storage/ : 775

    📦 Vérification assets production...
    ✅ Assets Vite compilés

    ═══════════════════════════════════════════════════════════
    📊 RÉSUMÉ VÉRIFICATION
    ═══════════════════════════════════════════════════════════
    ✅ Succès :       13
    ⚠️  Avertissements : 0
    ❌ Erreurs :      0

    🎉 Configuration production PARFAITE !
       Prêt pour déploiement.
    ```

=== "**Checklist Configuration Production**"

    **Variables .env obligatoires :**

    ```bash
    # Application
    ✅ APP_ENV=production
    ✅ APP_DEBUG=false
    ✅ APP_KEY généré (php artisan key:generate)
    ✅ APP_URL=https://... (avec HTTPS)
    
    # Base de données
    ✅ DB_CONNECTION configuré
    ✅ DB_HOST défini
    ✅ DB_DATABASE créé
    ✅ DB_USERNAME dédié (pas root)
    ✅ DB_PASSWORD fort (16+ chars)
    
    # Cache/Sessions
    ✅ CACHE_DRIVER=redis (ou file si pas Redis)
    ✅ SESSION_DRIVER=redis (ou database)
    ✅ SESSION_SECURE_COOKIE=true (si HTTPS)
    
    # Redis (si utilisé)
    ✅ REDIS_PASSWORD défini
    ✅ REDIS_HOST correct
    
    # Mail
    ✅ MAIL_MAILER configuré
    ✅ MAIL_HOST défini
    ✅ MAIL_USERNAME défini
    ✅ MAIL_PASSWORD défini
    
    # Logging
    ✅ LOG_CHANNEL=daily
    ✅ LOG_LEVEL=error
    ```

=== "**Commandes Artisan Utiles Production**"

    ```bash
    # Afficher configuration complète
    php artisan config:show
    
    # Afficher infos base de données
    php artisan db:show
    
    # Lister toutes routes
    php artisan route:list
    
    # Tester connexion cache
    php artisan tinker
    >>> Cache::put('test', 'ok', 10);
    >>> Cache::get('test');
    
    # Tester envoi email
    php artisan tinker
    >>> Mail::raw('Test email', function($msg) {
        $msg->to('votre@email.com')->subject('Test');
    });
    
    # Vérifier queue workers
    php artisan queue:work --once
    
    # Clear tous les caches
    php artisan optimize:clear
    
    # Recompiler tous les caches
    php artisan optimize
    ```

=== "**Tableau Comparatif Drivers**"

    | Service | Driver Local | Driver Production | Avantages Production |
    |---------|-------------|-------------------|---------------------|
    | **Cache** | `file` | `redis` | × 50 plus rapide, partagé multi-serveurs |
    | **Session** | `file` | `redis` ou `database` | Scalable, persistant redémarrages |
    | **Queue** | `sync` | `redis` | Asynchrone, retry automatique, monitoring |
    | **Mail** | `log` | `smtp` ou `mailgun` | Délivrabilité, analytics, reputation |
    | **Logs** | `single` | `daily` | Rotation auto, disk non saturé |
    | **Filesystem** | `local` | `s3` | CDN, backups auto, scalable |

✅ **Étape 7.5 Terminée !**

**Fichiers créés :**

- `.env.production.example` : Template configuration production
- `scripts/verify-production-config.sh` : Script vérification automatique

**Concepts maîtrisés :**

- Configuration .env production complète
- Services externes (mail, cache, queue)
- Redis configuration sécurisée
- Vérification configuration automatisée
- Différences dev/staging/production
- Drivers optimaux par service

**Configuration production maintenant :**

- ✅ Variables environnement sécurisées
- ✅ Services externes configurés
- ✅ Redis cache + sessions + queue
- ✅ Logging optimisé
- ✅ Vérification automatisée
- ✅ Permissions correctes

**Prochaine étape :**

- 7.6 : Guide déploiement (serveur, domaine, SSL, mise en ligne)

Voulez-vous que je finalise avec l'étape 7.6 (Guide Déploiement Complet) pour clôturer la Phase 7 et le projet ?





### Étape 7.6 : Guide Déploiement Complet (OVH)

**Contexte :**

Le déploiement est l'étape finale : transformer application locale en site web accessible mondialement. Ce guide couvre **installation complète** d'un serveur production chez **OVH**, de la commande serveur jusqu'au premier visiteur.

!!! note "**Pourquoi OVH ?**"

    - ✅ **Hébergeur français** : Conformité RGPD, support français
    - ✅ **Tarifs compétitifs** : VPS dès 3,50€/mois HT
    - ✅ **Datacenters Europe** : Latence optimale France/Europe
    - ✅ **Bande passante illimitée** : Pas de surcoût trafic
    - ✅ **DDoS protection** : Incluse gratuitement

**Architecture déploiement :**

```
┌──────────────────────────────────────────────────────────┐
│                    INTERNET                              │
└────────────────────┬─────────────────────────────────────┘
                     │
            ┌────────▼────────┐
            │   DNS (OVH)     │ monblog.com → 51.83.45.123
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │  VPS OVH        │ Ubuntu 24.04 LTS
            │  51.83.45.123   │ 2 vCPU, 4GB RAM, 80GB SSD
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
   │  Nginx  │ │  PHP-FPM│ │  MySQL  │
   │  :80/443│ │  :9000  │ │  :3306  │
   └─────────┘ └─────────┘ └─────────┘
        │            │            │
        └────────────┼────────────┘
                     │
            ┌────────▼────────┐
            │ Laravel App     │ /var/www/blog
            │ + Redis (cache) │
            └─────────────────┘
```

---

??? abstract "7.6.1 : Commander et Configurer VPS OVH"

    **Étape 1 : Commander VPS OVH**

    **Se connecter : [ovh.com](https://www.ovh.com/fr/)**

    1. **Choisir VPS** → VPS → Découvrir nos VPS
    2. **Sélectionner gamme** :
       - **VPS Starter** : 3,50€/mois HT (1 vCPU, 2GB RAM) → Développement/Staging
       - **VPS Value** : 7€/mois HT (2 vCPU, 4GB RAM) → **RECOMMANDÉ Production**
       - **VPS Essential** : 14€/mois HT (2 vCPU, 8GB RAM) → Gros trafic

    **Configuration exemple (VPS Value) :**

    ```
    Gamme        : VPS Value
    Datacenter   : Gravelines (France) - GRA11
    OS           : Ubuntu 24.04 LTS
    Stockage     : 80 GB SSD NVMe
    RAM          : 4 GB
    CPU          : 2 vCores
    Bande passante : 500 Mbps (illimitée)
    IP           : 1 IPv4 dédiée
    
    Prix : 7€/mois HT (8,40€ TTC)
    Engagement : Mensuel (résiliable à tout moment)
    ```

    3. **Valider commande** → Paiement → Bon de commande N°12345678
    4. **Attendre provisionnement** : 10-30 minutes
    5. **Email confirmation** : Identifiants root + IP serveur

    **Email reçu (exemple simulé) :**

    ```
    ═══════════════════════════════════════════════════════════
    OVH - Votre VPS est prêt !
    ═══════════════════════════════════════════════════════════
    
    Votre serveur VPS vps-a1b2c3d4.vps.ovh.net est maintenant actif.
    
    Informations de connexion :
    ────────────────────────────────────────────────────────────
    Adresse IP     : 51.83.45.123
    Hostname       : vps-a1b2c3d4.vps.ovh.net
    OS             : Ubuntu 24.04 LTS
    Utilisateur    : root
    Mot de passe   : Kf8mP2xQw9nRt3sV
    
    Connexion SSH  : ssh root@51.83.45.123
    Panel OVH      : https://www.ovh.com/manager/dedicated/#/vps/vps-a1b2c3d4.vps.ovh.net
    ────────────────────────────────────────────────────────────
    
    ⚠️  Changez immédiatement le mot de passe root !
    ```

    **Étape 2 : Première connexion SSH**

    ```bash
    # Depuis votre machine locale
    ssh root@51.83.45.123
    
    # Saisir password temporaire : Kf8mP2xQw9nRt3sV
    
    # Premier message Ubuntu
    Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-49-generic x86_64)
    
    # Changer password root immédiatement
    passwd
    # Saisir nouveau password fort (16+ chars)
    # Exemple : 7Kf2mP9xQw3nRt8sVb4cYh6dJl1a
    ```

    **Étape 3 : Mise à jour système**

    ```bash
    # Mettre à jour cache packages
    apt update
    
    # Installer toutes mises à jour disponibles
    apt upgrade -y
    
    # Installer packages essentiels
    apt install -y \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates
    
    # Configurer timezone
    timedatectl set-timezone Europe/Paris
    
    # Vérifier
    date
    # Résultat : jeu. 11 déc. 2024 14:30:25 CET
    ```

    **Étape 4 : Créer utilisateur dédié (sécurité)**

    ```bash
    # Créer utilisateur 'deploy' (pas root pour Laravel)
    adduser deploy
    # Password : 9Xm2pL7wQz5nRv8tYc4b
    # Infos : Laisser vides (Enter x5)
    
    # Ajouter au groupe sudo
    usermod -aG sudo deploy
    
    # Autoriser connexion SSH utilisateur deploy
    mkdir -p /home/deploy/.ssh
    cp /root/.ssh/authorized_keys /home/deploy/.ssh/ 2>/dev/null || echo "Pas de clés SSH root"
    chown -R deploy:deploy /home/deploy/.ssh
    chmod 700 /home/deploy/.ssh
    chmod 600 /home/deploy/.ssh/authorized_keys 2>/dev/null || true
    
    # Tester connexion (depuis local)
    ssh deploy@51.83.45.123
    ```

??? abstract "7.6.2 : Installation Stack LEMP (Linux + Nginx + MySQL + PHP)"

    **Contexte :**

    **LEMP** = Linux + Nginx + MySQL + PHP. Stack moderne haute performance pour Laravel.

    **Installer Nginx (serveur web)**

    ```bash
    # Installer Nginx
    sudo apt install -y nginx
    
    # Démarrer et activer au boot
    sudo systemctl start nginx
    sudo systemctl enable nginx
    
    # Vérifier statut
    sudo systemctl status nginx
    # ● nginx.service - A high performance web server
    #    Active: active (running)
    
    # Tester
    curl http://localhost
    # Doit afficher page "Welcome to nginx!"
    ```

    **Installer PHP 8.2 + Extensions Laravel**

    ```bash
    # Ajouter repository PHP (ondrej/php)
    sudo add-apt-repository ppa:ondrej/php -y
    sudo apt update
    
    # Installer PHP 8.2 + extensions
    sudo apt install -y \
        php8.2-fpm \
        php8.2-cli \
        php8.2-common \
        php8.2-mysql \
        php8.2-zip \
        php8.2-gd \
        php8.2-mbstring \
        php8.2-curl \
        php8.2-xml \
        php8.2-bcmath \
        php8.2-redis \
        php8.2-intl
    
    # Vérifier version PHP
    php -v
    # PHP 8.2.25 (cli) (built: Nov 21 2024 15:37:21) (NTS)
    
    # Démarrer PHP-FPM
    sudo systemctl start php8.2-fpm
    sudo systemctl enable php8.2-fpm
    
    # Vérifier statut
    sudo systemctl status php8.2-fpm
    # ● php8.2-fpm.service - The PHP 8.2 FastCGI Process Manager
    #    Active: active (running)
    ```

    **Optimiser PHP pour production**

    ```bash
    # Éditer configuration PHP-FPM
    sudo nano /etc/php/8.2/fpm/php.ini
    ```

    **Modifications `php.ini` :**

    ```ini
    ; Mémoire allouée par script (Laravel peut consommer)
    memory_limit = 256M
    
    ; Taille max upload (images articles)
    upload_max_filesize = 20M
    post_max_size = 20M
    
    ; Temps exécution max (import données, migrations)
    max_execution_time = 60
    
    ; Affichage erreurs : DÉSACTIVER en production
    display_errors = Off
    log_errors = On
    error_reporting = E_ALL & ~E_DEPRECATED & ~E_STRICT
    
    ; Sessions sécurisées
    session.cookie_httponly = 1
    session.cookie_secure = 1
    session.use_strict_mode = 1
    
    ; Opcache : Cache bytecode PHP (× 3 performances)
    opcache.enable = 1
    opcache.memory_consumption = 128
    opcache.interned_strings_buffer = 8
    opcache.max_accelerated_files = 10000
    opcache.validate_timestamps = 0
    opcache.save_comments = 1
    opcache.fast_shutdown = 1
    ```

    **Redémarrer PHP-FPM :**

    ```bash
    sudo systemctl restart php8.2-fpm
    ```

    **Installer MySQL 8.0**

    ```bash
    # Installer serveur MySQL
    sudo apt install -y mysql-server
    
    # Démarrer et activer
    sudo systemctl start mysql
    sudo systemctl enable mysql
    
    # Sécuriser installation
    sudo mysql_secure_installation
    
    # Réponses recommandées :
    # - VALIDATE PASSWORD COMPONENT ? Y
    # - Password validation policy ? 1 (MEDIUM)
    # - New root password : 5Rt8Yc2bHf9xQw1mKl6pNz3d
    # - Remove anonymous users ? Y
    # - Disallow root login remotely ? Y
    # - Remove test database ? Y
    # - Reload privilege tables ? Y
    ```

    **Créer base de données + utilisateur Laravel :**

    ```bash
    # Connexion MySQL root
    sudo mysql -u root -p
    # Saisir password root : 5Rt8Yc2bHf9xQw1mKl6pNz3d
    ```

    **Dans console MySQL :**

    ```sql
    -- Créer base de données
    CREATE DATABASE blog_production CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
    -- Créer utilisateur dédié
    CREATE USER 'blog_user'@'localhost' IDENTIFIED BY '7Kf2mP9xQw3nRt8sVb4cYh6d';
    
    -- Accorder privilèges
    GRANT ALL PRIVILEGES ON blog_production.* TO 'blog_user'@'localhost';
    
    -- Appliquer changements
    FLUSH PRIVILEGES;
    
    -- Vérifier
    SHOW DATABASES;
    -- +--------------------+
    -- | Database           |
    -- +--------------------+
    -- | blog_production    |
    -- | information_schema |
    -- | mysql              |
    -- | performance_schema |
    -- | sys                |
    -- +--------------------+
    
    -- Quitter
    EXIT;
    ```

    **Tester connexion utilisateur Laravel :**

    ```bash
    mysql -u blog_user -p blog_production
    # Password : 7Kf2mP9xQw3nRt8sVb4cYh6d
    # Doit afficher : mysql>
    
    EXIT;
    ```

    **Installer Redis (cache + sessions)**

    ```bash
    # Installer serveur Redis
    sudo apt install -y redis-server
    
    # Configurer Redis pour systemd
    sudo nano /etc/redis/redis.conf
    ```

    **Modifications `redis.conf` :**

    ```conf
    # Supervision systemd
    supervised systemd
    
    # Bind localhost uniquement (sécurité)
    bind 127.0.0.1
    
    # Password obligatoire production
    requirepass 9Xm2pL7wQz5nRv8tYc4bHf6g
    
    # Persistence activée
    appendonly yes
    
    # Mémoire max 512MB
    maxmemory 512mb
    maxmemory-policy allkeys-lru
    ```

    **Redémarrer Redis :**

    ```bash
    sudo systemctl restart redis-server
    sudo systemctl enable redis-server
    
    # Tester connexion
    redis-cli
    127.0.0.1:6379> AUTH 9Xm2pL7wQz5nRv8tYc4bHf6g
    OK
    127.0.0.1:6379> PING
    PONG
    127.0.0.1:6379> exit
    ```

??? abstract "7.6.3 : Installation Composer et Node.js"

    **Installer Composer (gestionnaire dépendances PHP)**

    ```bash
    # Télécharger installateur Composer
    cd ~
    curl -sS https://getcomposer.org/installer -o composer-setup.php
    
    # Vérifier hash SHA-384 (sécurité)
    HASH="$(curl -sS https://composer.github.io/installer.sig)"
    php -r "if (hash_file('sha384', 'composer-setup.php') === '$HASH') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
    # Doit afficher : Installer verified
    
    # Installer Composer globalement
    sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer
    
    # Nettoyer
    rm composer-setup.php
    
    # Vérifier installation
    composer --version
    # Composer version 2.8.3 2024-11-20 15:37:25
    ```

    **Installer Node.js 20 LTS (pour Vite)**

    ```bash
    # Ajouter repository NodeSource
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    
    # Installer Node.js + npm
    sudo apt install -y nodejs
    
    # Vérifier versions
    node -v
    # v20.11.0
    
    npm -v
    # 10.2.4
    ```

??? abstract "7.6.4 : Configuration Nginx pour Laravel"

    **Créer configuration site Laravel**

    ```bash
    # Créer fichier configuration
    sudo nano /etc/nginx/sites-available/blog
    ```

    **Contenu `/etc/nginx/sites-available/blog` :**

    ```nginx
    ###############################################################################
    # CONFIGURATION NGINX - LARAVEL BLOG PRODUCTION
    ###############################################################################
    # Domain: monblog.com
    # Root: /var/www/blog/public
    ###############################################################################

    # Redirection HTTP → HTTPS (après installation SSL)
    server {
        listen 80;
        listen [::]:80;
        server_name monblog.com www.monblog.com;

        # Temporairement : autoriser trafic HTTP (avant SSL)
        # Après SSL : décommenter redirection
        # return 301 https://$server_name$request_uri;

        root /var/www/blog/public;
        index index.php index.html;

        # Logs
        access_log /var/log/nginx/blog-access.log;
        error_log /var/log/nginx/blog-error.log;

        # Bloquer fichiers sensibles
        location ~ /\.(env|git|svn) {
            deny all;
            return 404;
        }

        # Route Laravel (try_files)
        location / {
            try_files $uri $uri/ /index.php?$query_string;
        }

        # PHP-FPM
        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;

            # Timeout généreux pour migrations
            fastcgi_read_timeout 300;
        }

        # Cache assets statiques (CSS, JS, images)
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Bloquer accès storage/ (fichiers privés)
        location ^~ /storage/ {
            deny all;
        }

        # Bloquer accès bootstrap/cache/
        location ^~ /bootstrap/cache/ {
            deny all;
        }
    }

    # Configuration HTTPS (à activer après Let's Encrypt)
    # server {
    #     listen 443 ssl http2;
    #     listen [::]:443 ssl http2;
    #     server_name monblog.com www.monblog.com;
    #
    #     root /var/www/blog/public;
    #     index index.php index.html;
    #
    #     # Certificats SSL (générés par Certbot)
    #     ssl_certificate /etc/letsencrypt/live/monblog.com/fullchain.pem;
    #     ssl_certificate_key /etc/letsencrypt/live/monblog.com/privkey.pem;
    #
    #     # Configuration SSL moderne
    #     ssl_protocols TLSv1.2 TLSv1.3;
    #     ssl_ciphers HIGH:!aNULL:!MD5;
    #     ssl_prefer_server_ciphers on;
    #
    #     # HSTS (6 mois)
    #     add_header Strict-Transport-Security "max-age=15768000; includeSubDomains" always;
    #
    #     # [... Copier sections location depuis bloc HTTP ci-dessus ...]
    # }
    ```

    **Activer site et redémarrer Nginx :**

    ```bash
    # Créer lien symbolique sites-enabled
    sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
    
    # Supprimer site par défaut
    sudo rm /etc/nginx/sites-enabled/default
    
    # Tester configuration Nginx
    sudo nginx -t
    # nginx: configuration file /etc/nginx/nginx.conf test is successful
    
    # Redémarrer Nginx
    sudo systemctl restart nginx
    ```

??? abstract "7.6.5 : Déploiement Code Laravel via Git"

    **Étape 1 : Créer répertoire application**

    ```bash
    # Créer répertoire web
    sudo mkdir -p /var/www/blog
    
    # Donner ownership à utilisateur deploy
    sudo chown -R deploy:deploy /var/www/blog
    
    # Naviguer dans répertoire
    cd /var/www/blog
    ```

    **Étape 2 : Cloner repository Git**

    !!! note "**Prérequis : Code doit être sur Git (GitHub, GitLab, Bitbucket)**"
        Si pas encore versionné :
        ```bash
        # Sur machine locale
        git init
        git add .
        git commit -m "Initial commit"
        git remote add origin https://github.com/votre-username/laravel-blog.git
        git push -u origin main
        ```

    **Sur serveur :**

    ```bash
    # Cloner repository (exemple GitHub)
    git clone https://github.com/votre-username/laravel-blog.git .
    
    # Ou avec authentification si repository privé
    git clone https://votre-token@github.com/votre-username/laravel-blog.git .
    
    # Vérifier fichiers présents
    ls -la
    # drwxr-xr-x  app/
    # drwxr-xr-x  bootstrap/
    # -rw-r--r--  composer.json
    # drwxr-xr-x  config/
    # ...
    ```

    **Étape 3 : Installer dépendances Composer**

    ```bash
    # Installer dépendances PHP (production, optimisé)
    composer install --optimize-autoloader --no-dev
    
    # --optimize-autoloader : Autoloader optimisé (× 4 performances)
    # --no-dev : Exclut packages développement (tests, debugbar)
    
    # Temps installation : 2-5 minutes
    # Résultat : vendor/ créé avec toutes dépendances
    ```

    **Étape 4 : Installer dépendances npm et compiler assets**

    ```bash
    # Installer dépendances JavaScript
    npm ci
    # ci = clean install (reproductible, basé package-lock.json)
    
    # Compiler assets production
    npm run build
    
    # Résultat : public/build/ créé avec :
    # - assets/app-a3f2c1b9.css (minifié)
    # - assets/app-b7e4d3a1.js (minifié)
    # - manifest.json (références assets)
    ```

    **Étape 5 : Créer fichier .env production**

    ```bash
    # Copier template
    cp .env.production.example .env
    
    # Éditer avec vraies valeurs
    nano .env
    ```

    **Contenu `.env` production (exemple) :**

    ```bash
    APP_NAME="Mon Blog"
    APP_ENV=production
    APP_KEY=  # Sera généré étape suivante
    APP_DEBUG=false
    APP_URL=https://monblog.com

    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=blog_production
    DB_USERNAME=blog_user
    DB_PASSWORD=7Kf2mP9xQw3nRt8sVb4cYh6d

    CACHE_DRIVER=redis
    SESSION_DRIVER=redis
    SESSION_SECURE_COOKIE=true
    QUEUE_CONNECTION=redis

    REDIS_HOST=127.0.0.1
    REDIS_PORT=6379
    REDIS_PASSWORD=9Xm2pL7wQz5nRv8tYc4bHf6g
    REDIS_CACHE_DB=0
    REDIS_SESSION_DB=1
    REDIS_QUEUE_DB=2

    MAIL_MAILER=smtp
    MAIL_HOST=smtp-relay.brevo.com
    MAIL_PORT=587
    MAIL_USERNAME=votre-email@example.com
    MAIL_PASSWORD=votre-cle-api-brevo
    MAIL_FROM_ADDRESS=noreply@monblog.com
    MAIL_FROM_NAME="${APP_NAME}"

    LOG_CHANNEL=daily
    LOG_LEVEL=error
    ```

    **Étape 6 : Initialiser application Laravel**

    ```bash
    # Générer clé application (APP_KEY)
    php artisan key:generate
    # Application key set successfully.
    
    # Créer lien symbolique storage
    php artisan storage:link
    # The [public/storage] link has been connected to [storage/app/public].
    
    # Exécuter migrations (créer tables BDD)
    php artisan migrate --force
    # --force : Nécessaire car APP_ENV=production (confirmation automatique)
    
    # Résultat :
    # Migration table created successfully.
    # Migrating: 2014_10_12_000000_create_users_table
    # Migrated:  2014_10_12_000000_create_users_table (45.23ms)
    # ...
    
    # Seeders (données initiales - optionnel)
    php artisan db:seed --force
    # Database seeding completed successfully.
    ```

    **Étape 7 : Optimiser Laravel pour production**

    ```bash
    # Compiler caches optimisés
    php artisan config:cache
    php artisan route:cache
    php artisan view:cache
    php artisan event:cache
    
    # Résultat :
    # Configuration cache cleared successfully.
    # Configuration cached successfully.
    # ...
    ```

    **Étape 8 : Configurer permissions**

    ```bash
    # Propriétaire : utilisateur deploy
    sudo chown -R deploy:www-data /var/www/blog
    
    # Permissions dossiers
    sudo find /var/www/blog -type d -exec chmod 755 {} \;
    
    # Permissions fichiers
    sudo find /var/www/blog -type f -exec chmod 644 {} \;
    
    # Storage et cache : écriture www-data (Nginx)
    sudo chmod -R 775 /var/www/blog/storage
    sudo chmod -R 775 /var/www/blog/bootstrap/cache
    
    # .env : lecture propriétaire uniquement
    chmod 600 /var/www/blog/.env
    ```

    **Étape 9 : Tester application**

    ```bash
    # Vérifier configuration
    php artisan config:show
    
    # Tester connexion BDD
    php artisan db:show
    # MySQL 8.0.40 ··············································· blog_production
    
    # Tester routes
    php artisan route:list --columns=method,uri,name
    
    # Vérifier cache Redis
    php artisan tinker
    >>> Cache::put('test', 'ok', 60);
    >>> Cache::get('test');
    => "ok"
    >>> exit
    ```

??? abstract "7.6.6 : Configuration DNS et Domaine OVH"

    **Contexte :**

    Le domaine `monblog.com` doit pointer vers IP serveur `51.83.45.123`. Configuration via DNS OVH.

    **Étape 1 : Acheter domaine OVH (si pas déjà fait)**

    1. **OVH → Domaines → Commander**
    2. **Rechercher** : `monblog.com`
    3. **Vérifier disponibilité** : Disponible ✅
    4. **Tarif** : 6,99€ HT/an (TLD .com)
    5. **Valider commande** → Paiement

    **Étape 2 : Configurer zone DNS**

    **Se connecter : [ovh.com/manager](https://www.ovh.com/manager/web/)**

    1. **Domaines** → Sélectionner `monblog.com`
    2. **Zone DNS** → Modifier
    3. **Supprimer entrées existantes** (parking OVH)
    4. **Ajouter enregistrements DNS** :

    **Enregistrements à créer :**

    | Type | Sous-domaine | Cible | TTL |
    |------|-------------|-------|-----|
    | **A** | @ | 51.83.45.123 | 3600 |
    | **A** | www | 51.83.45.123 | 3600 |
    | **AAAA** | @ | 2001:41d0:... | 3600 |
    | **AAAA** | www | 2001:41d0:... | 3600 |

    !!! note "**Explications enregistrements :**"
        - **A** : Associe domaine à IPv4
        - **AAAA** : Associe domaine à IPv6 (optionnel)
        - **@** : Domaine principal (monblog.com)
        - **www** : Sous-domaine (www.monblog.com)
        - **TTL** : Durée cache (3600s = 1h)

    **Dans interface OVH :**

    ```
    Ajouter une entrée
    ─────────────────────────────────────────
    Type d'enregistrement : A
    Sous-domaine          : [laisser vide = @]
    Cible                 : 51.83.45.123
    TTL                   : 3600
    
    [Valider]
    
    Ajouter une entrée
    ─────────────────────────────────────────
    Type d'enregistrement : A
    Sous-domaine          : www
    Cible                 : 51.83.45.123
    TTL                   : 3600
    
    [Valider]
    ```

    **Étape 3 : Attendre propagation DNS**

    ```bash
    # Propagation DNS : 10 minutes - 24 heures (généralement <1h)
    
    # Vérifier propagation (depuis local)
    dig monblog.com +short
    # 51.83.45.123
    
    dig www.monblog.com +short
    # 51.83.45.123
    
    # Ou via service en ligne
    # https://www.whatsmydns.net/#A/monblog.com
    ```

    **Étape 4 : Tester accès HTTP**

    ```bash
    # Ouvrir navigateur
    http://monblog.com
    
    # Doit afficher page d'accueil Laravel
    # ⚠️ HTTP (pas sécurisé) - SSL prochaine étape
    ```

??? abstract "7.6.7 : Installation Certificat SSL (Let's Encrypt)"

    **Contexte :**

    **Let's Encrypt** fournit certificats SSL **gratuits** valides 90 jours (renouvellement automatique).

    **Étape 1 : Installer Certbot**

    ```bash
    # Installer Certbot + plugin Nginx
    sudo apt install -y certbot python3-certbot-nginx
    ```

    **Étape 2 : Obtenir certificat SSL**

    ```bash
    # Certbot mode automatique (modifie config Nginx)
    sudo certbot --nginx -d monblog.com -d www.monblog.com
    
    # Réponses interactives :
    # Email (notifications expiration) : votre@email.com
    # Terms of Service : (A)gree
    # Share email with EFF : (N)o
    # Redirect HTTP → HTTPS : 2 (Yes, redirect)
    
    # Certbot :
    # - Vérifie contrôle domaine (challenge HTTP)
    # - Génère certificats
    # - Modifie /etc/nginx/sites-available/blog (ajoute SSL)
    # - Recharge Nginx
    
    # Résultat :
    # Successfully received certificate.
    # Certificate is saved at: /etc/letsencrypt/live/monblog.com/fullchain.pem
    # Key is saved at:         /etc/letsencrypt/live/monblog.com/privkey.pem
    ```

    **Étape 3 : Vérifier renouvellement automatique**

    ```bash
    # Certbot installe cron job automatique
    # Tester renouvellement (dry-run)
    sudo certbot renew --dry-run
    
    # Résultat :
    # Congratulations, all simulated renewals succeeded:
    #   /etc/letsencrypt/live/monblog.com/fullchain.pem (success)
    ```

    **Étape 4 : Tester SSL**

    ```bash
    # Ouvrir navigateur
    https://monblog.com
    
    # Vérifier :
    # ✅ Cadenas vert (connexion sécurisée)
    # ✅ Certificat valide (Let's Encrypt Authority X3)
    # ✅ Expiration dans 90 jours
    
    # Test automatique
    # https://www.ssllabs.com/ssltest/analyze.html?d=monblog.com
    # Score attendu : A ou A+
    ```

    **Configuration Nginx post-Certbot :**

    Certbot a modifié `/etc/nginx/sites-available/blog` automatiquement :

    ```nginx
    # HTTP → HTTPS redirect (ajouté par Certbot)
    server {
        listen 80;
        server_name monblog.com www.monblog.com;
        
        return 301 https://$server_name$request_uri;
    }

    # HTTPS (ajouté par Certbot)
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name monblog.com www.monblog.com;

        root /var/www/blog/public;
        index index.php index.html;

        # Certificats SSL (gérés par Certbot)
        ssl_certificate /etc/letsencrypt/live/monblog.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/monblog.com/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        # [... reste configuration identique ...]
    }
    ```

??? abstract "7.6.8 : Configuration Firewall UFW"

    **Contexte :**

    **UFW** (Uncomplicated Firewall) bloque trafic non autorisé. Ouvrir seulement ports nécessaires.

    **Installer et configurer UFW :**

    ```bash
    # Installer UFW
    sudo apt install -y ufw
    
    # Configurer règles (AVANT d'activer)
    
    # Autoriser SSH (CRITIQUE - sinon perte accès serveur)
    sudo ufw allow 22/tcp
    
    # Autoriser HTTP (port 80)
    sudo ufw allow 80/tcp
    
    # Autoriser HTTPS (port 443)
    sudo ufw allow 443/tcp
    
    # Politique par défaut : refuser tout le reste
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    
    # Activer firewall
    sudo ufw enable
    # Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
    # Firewall is active and enabled on system startup
    
    # Vérifier statut
    sudo ufw status verbose
    
    # Status: active
    # 
    # To                         Action      From
    # --                         ------      ----
    # 22/tcp                     ALLOW       Anywhere
    # 80/tcp                     ALLOW       Anywhere
    # 443/tcp                    ALLOW       Anywhere
    ```

    !!! warning "**ATTENTION : Ne pas bloquer port SSH (22)**"
        Bloquer SSH = perte accès serveur définitive (nécessite console rescue OVH)

??? abstract "7.6.9 : Configuration Supervisor (Queue Workers)"

    **Contexte :**

    **Supervisor** maintient workers queue Redis actifs (traitement jobs asynchrones : emails, notifications).

    **Installer Supervisor :**

    ```bash
    sudo apt install -y supervisor
    ```

    **Créer configuration worker Laravel :**

    ```bash
    sudo nano /etc/supervisor/conf.d/laravel-worker.conf
    ```

    **Contenu `laravel-worker.conf` :**

    ```ini
    [program:laravel-worker]
    process_name=%(program_name)s_%(process_num)02d
    command=php /var/www/blog/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true
    user=deploy
    numprocs=2
    redirect_stderr=true
    stdout_logfile=/var/www/blog/storage/logs/worker.log
    stopwaitsecs=3600
    ```

    !!! note "**Explications configuration :**"
        - `command` : Commande worker Laravel
        - `--sleep=3` : Pause 3s entre vérifications queue
        - `--tries=3` : 3 tentatives avant échec définitif
        - `--max-time=3600` : Redémarre worker après 1h (libère mémoire)
        - `numprocs=2` : 2 workers parallèles (augmenter si beaucoup de jobs)
        - `user=deploy` : Exécute comme utilisateur deploy (pas root)

    **Démarrer workers :**

    ```bash
    # Recharger configuration Supervisor
    sudo supervisorctl reread
    # laravel-worker: available
    
    sudo supervisorctl update
    # laravel-worker: added process group
    
    # Démarrer workers
    sudo supervisorctl start laravel-worker:*
    # laravel-worker:laravel-worker_00: started
    # laravel-worker:laravel-worker_01: started
    
    # Vérifier statut
    sudo supervisorctl status
    # laravel-worker:laravel-worker_00   RUNNING   pid 12345, uptime 0:00:05
    # laravel-worker:laravel-worker_01   RUNNING   pid 12346, uptime 0:00:05
    ```

    **Commandes utiles Supervisor :**

    ```bash
    # Redémarrer workers (après déploiement code)
    sudo supervisorctl restart laravel-worker:*
    
    # Arrêter workers
    sudo supervisorctl stop laravel-worker:*
    
    # Voir logs worker
    sudo supervisorctl tail -f laravel-worker:laravel-worker_00
    ```

=== "**Checklist Post-Déploiement**"

    **Vérifier tous services fonctionnent :**

    ```bash
    # ✅ Nginx actif
    sudo systemctl status nginx | grep Active
    # Active: active (running)
    
    # ✅ PHP-FPM actif
    sudo systemctl status php8.2-fpm | grep Active
    # Active: active (running)
    
    # ✅ MySQL actif
    sudo systemctl status mysql | grep Active
    # Active: active (running)
    
    # ✅ Redis actif
    sudo systemctl status redis-server | grep Active
    # Active: active (running)
    
    # ✅ Supervisor actif
    sudo systemctl status supervisor | grep Active
    # Active: active (running)
    
    # ✅ Workers queue actifs
    sudo supervisorctl status
    # laravel-worker:laravel-worker_00   RUNNING
    ```

    **Tester fonctionnalités critiques :**

    ```bash
    # ✅ Page d'accueil charge
    curl -I https://monblog.com
    # HTTP/2 200
    
    # ✅ Connexion BDD fonctionne
    php artisan db:show
    
    # ✅ Cache Redis fonctionne
    php artisan tinker --execute="Cache::put('test', 'ok'); echo Cache::get('test');"
    # ok
    
    # ✅ Emails envoient (test)
    php artisan tinker --execute="Mail::raw('Test', fn(\$m) => \$m->to('test@example.com')->subject('Test'));"
    # Vérifier réception email
    ```

=== "**Script Déploiement Automatique**"

    **Créer script mise à jour production :**

    **Fichier : `deploy.sh` (racine projet)**

    ```bash
    #!/bin/bash

    ###############################################################################
    # SCRIPT DÉPLOIEMENT PRODUCTION - LARAVEL BLOG
    ###############################################################################
    # 
    # Usage : bash deploy.sh
    # 
    # Workflow :
    # 1. Pull code Git
    # 2. Installer dépendances Composer/npm
    # 3. Compiler assets
    # 4. Exécuter migrations
    # 5. Clear + recache optimisations
    # 6. Redémarrer services
    #
    ###############################################################################

    echo "🚀 Déploiement Laravel Blog Production..."
    echo ""

    # Mode maintenance (évite requêtes pendant déploiement)
    php artisan down --message="Mise à jour en cours" --retry=60

    # Pull dernières modifications Git
    echo "📥 Pull code Git..."
    git pull origin main

    # Installer dépendances Composer (production optimisé)
    echo "📦 Installation dépendances Composer..."
    composer install --optimize-autoloader --no-dev

    # Installer dépendances npm
    echo "📦 Installation dépendances npm..."
    npm ci

    # Compiler assets production
    echo "⚡ Compilation assets Vite..."
    npm run build

    # Exécuter migrations BDD
    echo "🗄️  Exécution migrations..."
    php artisan migrate --force

    # Clear tous caches
    echo "🧹 Nettoyage caches..."
    php artisan cache:clear
    php artisan config:clear
    php artisan route:clear
    php artisan view:clear

    # Recréer caches optimisés
    echo "⚡ Recompilation caches..."
    php artisan config:cache
    php artisan route:cache
    php artisan view:cache
    php artisan event:cache

    # Redémarrer queue workers
    echo "🔄 Redémarrage workers..."
    sudo supervisorctl restart laravel-worker:*

    # Redémarrer PHP-FPM
    echo "🔄 Redémarrage PHP-FPM..."
    sudo systemctl restart php8.2-fpm

    # Désactiver mode maintenance
    php artisan up

    echo ""
    echo "✅ Déploiement terminé avec succès !"
    echo ""
    echo "Vérifier : https://monblog.com"
    ```

    **Rendre exécutable et utiliser :**

    ```bash
    chmod +x deploy.sh
    
    # Déployer nouvelle version
    bash deploy.sh
    ```

=== "**Monitoring et Logs**"

    **Consulter logs application :**

    ```bash
    # Logs Laravel (storage/logs/)
    tail -f /var/www/blog/storage/logs/laravel.log
    
    # Logs Nginx (accès)
    tail -f /var/log/nginx/blog-access.log
    
    # Logs Nginx (erreurs)
    tail -f /var/log/nginx/blog-error.log
    
    # Logs PHP-FPM
    tail -f /var/log/php8.2-fpm.log
    
    # Logs workers queue
    tail -f /var/www/blog/storage/logs/worker.log
    ```

    **Installer monitoring (optionnel) :**

    ```bash
    # Installer netdata (monitoring temps réel)
    bash <(curl -Ss https://my-netdata.io/kickstart.sh)
    
    # Accès dashboard : http://51.83.45.123:19999
    # Métriques : CPU, RAM, disk, réseau, MySQL, Nginx, Redis
    ```

=== "**Maintenance Régulière**"

    **Tâches hebdomadaires :**

    ```bash
    # Mise à jour système
    sudo apt update && sudo apt upgrade -y
    
    # Nettoyer logs anciens (>30 jours)
    find /var/www/blog/storage/logs/*.log -mtime +30 -delete
    
    # Vérifier espace disque
    df -h
    ```

    **Tâches mensuelles :**

    ```bash
    # Optimiser tables MySQL
    sudo mysqlcheck -o --all-databases -u root -p
    
    # Backup base de données
    mysqldump -u blog_user -p blog_production > backup_$(date +%Y%m%d).sql
    
    # Compresser backup
    gzip backup_$(date +%Y%m%d).sql
    ```

    **Configurer backups automatiques (optionnel) :**

    ```bash
    # Créer script backup
    sudo nano /usr/local/bin/backup-blog.sh
    ```

    ```bash
    #!/bin/bash
    BACKUP_DIR="/home/deploy/backups"
    DATE=$(date +%Y%m%d_%H%M%S)
    
    # Backup BDD
    mysqldump -u blog_user -p'7Kf2mP9xQw3nRt8sVb4cYh6d' blog_production | gzip > $BACKUP_DIR/db_$DATE.sql.gz
    
    # Backup fichiers (uploads)
    tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /var/www/blog/storage/app/public
    
    # Supprimer backups >7 jours
    find $BACKUP_DIR -mtime +7 -delete
    ```

    **Cron job (exécution quotidienne 3h du matin) :**

    ```bash
    sudo crontab -e
    
    # Ajouter ligne :
    0 3 * * * /usr/local/bin/backup-blog.sh
    ```

✅ **Étape 7.6 Terminée complètement !**

✅ **PROJET LARAVEL BLOG MULTI-AUTEURS 100% TERMINÉ !**

**Infrastructure déployée :**

- ✅ VPS OVH (51.83.45.123) - Ubuntu 24.04 LTS
- ✅ Stack LEMP (Nginx + PHP 8.2 + MySQL 8.0 + Redis)
- ✅ Application Laravel production-ready
- ✅ Domaine configuré (monblog.com)
- ✅ SSL Let's Encrypt (HTTPS)
- ✅ Firewall UFW actif
- ✅ Queue workers Supervisor
- ✅ Script déploiement automatique

**URLs actives (simulation) :**

- 🌐 **Site web** : https://monblog.com
- 🔒 **SSL** : A+ (SSL Labs)
- 📊 **Monitoring** : http://51.83.45.123:19999
- 📧 **Email** : noreply@monblog.com

**Performances production :**

- ⚡ **TTFB** : <100ms
- ⚡ **Page complète** : <500ms
- ⚡ **Requêtes SQL** : 3 (Eager Loading)
- ⚡ **Score PageSpeed** : 90+ (prévu)
















































## CONCLUSION : Projet Laravel Blog Multi-Auteurs v0.0.3

**Félicitations ! Vous avez créé de A à Z une application Laravel production-ready.**

Ce projet marathon de **7 phases** vous a fait parcourir l'intégralité du cycle de développement web moderne : de l'installation locale jusqu'au déploiement production sur serveur réel. Vous disposez maintenant d'une base solide pour construire des applications web professionnelles.


### Statistiques du Projet

=== "**Volume de Travail**"

    | Métrique | Valeur |
    |----------|--------|
    | **Durée totale** | 90-120 heures |
    | **Phases complétées** | 7/7 (100%) |
    | **Fichiers créés** | 50+ |
    | **Lignes de code** | 3 500+ |
    | **Tests automatisés** | 29 (Feature + Unit) |
    | **Migrations BDD** | 5 |
    | **Contrôleurs** | 7 |
    | **Vues Blade** | 9 |
    | **Modèles Eloquent** | 4 |

=== "**Performance Application**"

    | Métrique | Avant Optimisation | Après Optimisation | Amélioration |
    |----------|-------------------|-------------------|--------------|
    | **Requêtes SQL** | 19 | 3 | × 6.3 moins |
    | **Temps total** | 580ms | 120ms | × 4.8 plus rapide |
    | **Mémoire** | 24 MB | 18 MB | -25% |
    | **TTFB** | 420ms | 85ms | × 4.9 plus rapide |

### Fonctionnalités Implémentées

??? abstract "**Authentification (Laravel Breeze)**"

    **Laravel Breeze** est la solution d'authentification **la plus simple** de l'écosystème Laravel. Parfaite pour :
    
    - ✅ Applications traditionnelles (web classique)
    - ✅ Projets solos ou petites équipes
    - ✅ Blogs, CMS, dashboards simples
    - ✅ Prototypage rapide
    - ✅ Apprentissage Laravel
    
    **Fonctionnalités incluses :**
    
    | Fonctionnalité | Implémentée | Description |
    |----------------|-------------|-------------|
    | **Register** | ✅ | Inscription utilisateur (email + password) |
    | **Login** | ✅ | Connexion avec email/password |
    | **Logout** | ✅ | Déconnexion sécurisée |
    | **Password Reset** | ✅ | Réinitialisation par email |
    | **Email Verification** | ✅ | Confirmation email (optionnel) |
    | **Profile Management** | ✅ | Édition infos personnelles |
    | **Password Update** | ✅ | Changement mot de passe |
    | **Account Deletion** | ✅ | Suppression compte utilisateur |
    
    !!! note "**Alternatives Laravel Breeze**"
        
        Laravel propose **3 solutions d'authentification** selon vos besoins :
        
        **1. Laravel Breeze (utilisé dans ce projet)**
        
        - ✅ **Le plus simple** : Installation en 5 minutes
        - ✅ **Léger** : Minimal, sans dépendances lourdes
        - ✅ **Personnalisable** : Code complet dans votre projet
        - ✅ **Idéal pour** : Blogs, sites vitrine, dashboards simples
        
        **2. Laravel Jetstream (prochainement)**
        
        - 🚀 **Plus riche** : Breeze + fonctionnalités avancées
        - 🚀 **Teams** : Gestion équipes/organisations
        - 🚀 **2FA** : Authentification à deux facteurs
        - 🚀 **API Tokens** : Gestion tokens API intégrée
        - 🚀 **Livewire/Inertia** : Choix stack frontend
        - 🚀 **Idéal pour** : SaaS, applications multi-utilisateurs, dashboards entreprise
        
        **3. Laravel Sanctum (prochainement)**
        
        - 🔐 **API-first** : Authentification APIs (SPAs, mobile)
        - 🔐 **Token-based** : JWT-like léger
        - 🔐 **CSRF** : Protection intégrée SPAs
        - 🔐 **Simple** : Plus simple qu'OAuth/Passport
        - 🔐 **Idéal pour** : APIs REST, applications Vue/React/Angular, apps mobiles

??? abstract "**Gestion Articles (CRUD Complet)**"

    | Fonctionnalité | Implémentée | Description |
    |----------------|-------------|-------------|
    | **Créer article** | ✅ | Formulaire création (brouillon ou publié) |
    | **Éditer article** | ✅ | Modification avec pré-remplissage |
    | **Supprimer article** | ✅ | Suppression avec confirmation JavaScript |
    | **Slug automatique** | ✅ | Génération depuis titre (événement `creating`) |
    | **Statuts** | ✅ | Brouillon (privé) / Publié (public) |
    | **Ownership** | ✅ | Sécurité (seul auteur peut modifier) |
    | **Catégories** | ✅ | Classification articles |
    | **Images** | ✅ | URL image couverture |
    | **Excerpt** | ✅ | Résumé court (500 chars max) |
    | **Views Counter** | ✅ | Compteur vues incrémental |

??? abstract "**Système Commentaires**"

    | Fonctionnalité | Implémentée | Description |
    |----------------|-------------|-------------|
    | **Commentaires publics** | ✅ | Formulaire sans authentification |
    | **Modération** | ✅ | Approbation manuelle par auteur |
    | **Approve/Reject** | ✅ | Boutons modération (auteur seulement) |
    | **Suppression** | ✅ | Supprimer commentaires spam |
    | **Affichage** | ✅ | Liste commentaires approuvés uniquement |
    | **Rate Limiting** | ✅ | Max 3 commentaires/minute (anti-spam) |
    | **Validation** | ✅ | Nom, email, contenu (10-1000 chars) |

??? abstract "**Interface Utilisateur (Blade + Tailwind)**"

    | Fonctionnalité | Implémentée | Description |
    |----------------|-------------|-------------|
    | **Layout responsive** | ✅ | Navigation adaptative mobile/desktop |
    | **Page d'accueil** | ✅ | Grille articles + sidebar catégories |
    | **Page article** | ✅ | Contenu complet + commentaires + similaires |
    | **Dashboard auteur** | ✅ | Statistiques + tableau articles |
    | **Profil public** | ✅ | Page auteur avec tous ses articles |
    | **Formulaires CRUD** | ✅ | Création/édition articles avec validation |
    | **Pagination** | ✅ | Navigation pages (9 articles/page) |
    | **Messages flash** | ✅ | Succès/erreur (sessions Laravel) |
    | **Confirmations** | ✅ | Popup JavaScript suppression |
    | **État vide** | ✅ | Messages si aucun contenu |

??? abstract "**Performance et Optimisation**"

    | Optimisation | Implémentée | Impact |
    |--------------|-------------|--------|
    | **Indexes BDD** | ✅ | × 50-100 plus rapide |
    | **Eager Loading** | ✅ | × 5-10 plus rapide (N+1 résolu) |
    | **Config cache** | ✅ | × 3 plus rapide |
    | **Route cache** | ✅ | × 10 plus rapide |
    | **View cache** | ✅ | × 5 plus rapide |
    | **Autoloader optimisé** | ✅ | × 4 plus rapide |
    | **Assets minifiés** | ✅ | × 2-3 plus légers |
    | **Redis cache** | ✅ | × 50 plus rapide (queries) |

??? abstract "**Sécurité**"

    | Protection | Implémentée | Description |
    |------------|-------------|-------------|
    | **CSRF** | ✅ | Tokens anti-Cross-Site Request Forgery |
    | **XSS** | ✅ | Échappement HTML automatique (Blade) |
    | **SQL Injection** | ✅ | Requêtes préparées (Eloquent) |
    | **Password Hashing** | ✅ | Bcrypt automatique |
    | **Rate Limiting** | ✅ | Login (5/min), Commentaires (3/min) |
    | **Headers Sécurité** | ✅ | CSP, HSTS, X-Frame-Options |
    | **Validation stricte** | ✅ | Règles validation tous formulaires |
    | **Firewall** | ✅ | UFW (ports 22, 80, 443 uniquement) |
    | **SSL/TLS** | ✅ | HTTPS forcé (Let's Encrypt) |
    | **Ownership** | ✅ | Vérification auteur avant modification |

??? abstract "**Tests Automatisés**"

    | Type de Test | Nombre | Couverture |
    |--------------|--------|------------|
    | **Feature Tests** | 14 | HomeController, PostController |
    | **Unit Tests** | 15 | Modèles Post, User, Relations |
    | **Total** | 29 | Fonctionnalités critiques |
    | **Taux de réussite** | 100% | ✅ Tous les tests passent |

### Compétences Acquises

=== "**Laravel Core**"

    | Concept | Niveau | Description |
    |---------|--------|-------------|
    | **Routes** | ⭐⭐⭐⭐⭐ | Publiques, protégées, groupes, middleware, Model Binding |
    | **Controllers** | ⭐⭐⭐⭐⭐ | CRUD complet, validation, ownership, redirections |
    | **Models Eloquent** | ⭐⭐⭐⭐⭐ | Relations (hasMany, belongsTo), scopes, casts, événements |
    | **Migrations** | ⭐⭐⭐⭐⭐ | Structure BDD, foreign keys, indexes, rollback |
    | **Seeders** | ⭐⭐⭐⭐ | Factories, données test, faker |
    | **Blade Templates** | ⭐⭐⭐⭐⭐ | Layouts, sections, directives, composants |
    | **Validation** | ⭐⭐⭐⭐⭐ | Rules, messages personnalisés, old(), @error |
    | **Authorization** | ⭐⭐⭐⭐ | Ownership, middleware auth, gates (bases) |

=== "**Laravel Breeze**"

    | Concept | Maîtrisé | Description |
    |---------|----------|-------------|
    | **Installation** | ✅ | Commande artisan, choix stack (Blade) |
    | **Routes auth** | ✅ | Fichier `routes/auth.php`, routes protégées |
    | **Contrôleurs** | ✅ | RegisterController, LoginController, etc. |
    | **Middleware** | ✅ | `auth`, `verified`, `guest` |
    | **Views** | ✅ | Personnalisation templates Breeze |
    | **Profile** | ✅ | Édition infos, password, suppression compte |
    | **Customisation** | ✅ | Ajout colonnes user (bio, avatar) |

=== "**Base de Données**"

    | Concept | Maîtrisé | Description |
    |---------|----------|-------------|
    | **MySQL** | ✅ | Installation, configuration, optimisation |
    | **Relations** | ✅ | One-to-Many, Many-to-One, Foreign Keys |
    | **Indexes** | ✅ | Simples, composites, UNIQUE, performance |
    | **Eager Loading** | ✅ | Résolution N+1, with(), load(), withCount() |
    | **Query Builder** | ✅ | Where, orderBy, paginate, scopes |
    | **Transactions** | ✅ | Intégrité données (bases) |

=== "**Frontend**"

    | Concept | Maîtrisé | Description |
    |---------|----------|-------------|
    | **Tailwind CSS** | ✅ | Classes utilitaires, responsive, hover states |
    | **Blade** | ✅ | Directives, layouts, components, slots |
    | **Vite** | ✅ | Build production, minification, cache busting |
    | **JavaScript** | ✅ | Confirmations, interactions basiques |
    | **Forms** | ✅ | Validation HTML5, CSRF, method spoofing |

=== "**DevOps et Production**"

    | Concept | Maîtrisé | Description |
    |---------|----------|-------------|
    | **Linux Ubuntu** | ✅ | Commandes shell, permissions, services systemd |
    | **Nginx** | ✅ | Configuration serveur web, SSL, reverse proxy |
    | **PHP-FPM** | ✅ | Configuration pool, optimisation php.ini |
    | **Redis** | ✅ | Cache, sessions, queue, configuration sécurisée |
    | **Supervisor** | ✅ | Gestion workers queue, restart automatique |
    | **SSL/TLS** | ✅ | Let's Encrypt, Certbot, renouvellement auto |
    | **DNS** | ✅ | Configuration enregistrements A, propagation |
    | **Firewall** | ✅ | UFW, règles ports, sécurisation serveur |
    | **Git** | ✅ | Clone, pull, déploiement via Git |
    | **Composer** | ✅ | Installation dépendances, optimisation autoloader |

=== "**Tests et Qualité**"

    | Concept | Maîtrisé | Description |
    |---------|----------|-------------|
    | **PHPUnit** | ✅ | Tests Feature, tests Unit, assertions |
    | **RefreshDatabase** | ✅ | Isolation tests, transactions |
    | **Factories** | ✅ | Génération données test, actingAs() |
    | **Mocking** | ⭐⭐⭐ | Bases (à approfondir) |
    | **TDD** | ⭐⭐⭐ | Principes (à pratiquer davantage) |

### Évolutions Possibles

??? abstract "**1. Fonctionnalités Avancées**"

    | Fonctionnalité | Difficulté | Temps estimé | Apports |
    |----------------|-----------|--------------|---------|
    | **Upload images réel** | Facile | 2h | Storage Laravel, thumbnails (intervention/image) |
    | **Tags articles** | Facile | 3h | Relation Many-to-Many, table pivot |
    | **Likes/Favoris** | Moyen | 4h | Relation polymorphic, compteurs |
    | **Recherche full-text** | Moyen | 5h | Scout Laravel + Algolia/Meilisearch |
    | **Commentaires imbriqués** | Moyen | 6h | Self-referencing relation, arbre hiérarchique |
    | **Notifications** | Moyen | 4h | Notifications Laravel (email, BDD, broadcast) |
    | **Rôles/Permissions** | Moyen | 6h | Spatie Permission package |
    | **Multi-langue** | Difficile | 8h | Localization Laravel, fichiers lang/ |
    | **API REST** | Difficile | 10h | API Resources, Sanctum auth |

??? abstract "**2. Optimisations Supplémentaires**"

    | Optimisation | Impact | Complexité | Description |
    |--------------|--------|------------|-------------|
    | **CDN Assets** | Élevé | Facile | Cloudflare, AWS CloudFront |
    | **Image lazy loading** | Moyen | Facile | Attribut `loading="lazy"`, Intersection Observer |
    | **Cache queries** | Élevé | Facile | Cache::remember() sur requêtes fréquentes |
    | **Horizon** | Moyen | Moyen | Dashboard monitoring queue |
    | **Telescope** | Moyen | Facile | Debug production (staging uniquement) |
    | **Load Balancer** | Élevé | Difficile | Répartition charge multi-serveurs |
    | **Database Read Replicas** | Élevé | Difficile | Séparation lecture/écriture BDD |

??? abstract "**3. SEO et Marketing**"

    | Amélioration | Impact SEO | Temps | Description |
    |--------------|-----------|-------|-------------|
    | **Meta descriptions** | ⭐⭐⭐⭐⭐ | 2h | Balises `<meta name="description">` dynamiques |
    | **Open Graph** | ⭐⭐⭐⭐ | 2h | Partage social (Facebook, Twitter) |
    | **Sitemap.xml** | ⭐⭐⭐⭐⭐ | 1h | Package spatie/laravel-sitemap |
    | **Schema.org** | ⭐⭐⭐⭐ | 3h | Structured data (Article, Author) |
    | **RSS Feed** | ⭐⭐⭐ | 2h | Flux RSS articles |
    | **AMP** | ⭐⭐⭐ | 8h | Accelerated Mobile Pages |
    | **Analytics** | ⭐⭐⭐⭐⭐ | 1h | Google Analytics 4, Matomo |

??? abstract "**4. Sécurité Avancée**"

    | Mesure | Priorité | Complexité | Description |
    |--------|----------|------------|-------------|
    | **2FA** | Haute | Moyen | Authentification deux facteurs (Google Authenticator) |
    | **CAPTCHA** | Haute | Facile | reCAPTCHA v3 formulaires publics |
    | **WAF** | Haute | Moyen | Web Application Firewall (Cloudflare) |
    | **Honeypot** | Moyenne | Facile | Champs cachés anti-spam bots |
    | **Content Security Policy** | Haute | Moyen | CSP stricte (nonces au lieu d'unsafe-inline) |
    | **Backup automatique** | Haute | Moyen | Cron jobs BDD + fichiers, stockage distant |
    | **Monitoring uptime** | Haute | Facile | UptimeRobot, Pingdom |
    | **Logs centralisés** | Moyenne | Moyen | Papertrail, Loggly, ELK Stack |

### Ressources pour Aller Plus Loin

=== "**Documentation Officielle**"

    | Ressource | URL | Description |
    |-----------|-----|-------------|
    | **Laravel** | [laravel.com/docs](https://laravel.com/docs) | Documentation officielle complète |
    | **Laravel Breeze** | [laravel.com/docs/starter-kits](https://laravel.com/docs/starter-kits) | Guide Breeze, Jetstream, Fortify |
    | **Tailwind CSS** | [tailwindcss.com/docs](https://tailwindcss.com/docs) | Framework CSS utilitaire |
    | **Eloquent ORM** | [laravel.com/docs/eloquent](https://laravel.com/docs/eloquent) | Guide complet Eloquent |

=== "**Packages Recommandés**"

    | Package | Usage | Installation |
    |---------|-------|--------------|
    | **spatie/laravel-permission** | Rôles et permissions | `composer require spatie/laravel-permission` |
    | **spatie/laravel-medialibrary** | Gestion uploads | `composer require spatie/laravel-medialibrary` |
    | **laravel/scout** | Recherche full-text | `composer require laravel/scout` |
    | **laravel/horizon** | Queue monitoring | `composer require laravel/horizon` |
    | **barryvdh/laravel-debugbar** | Debug (dev) | `composer require barryvdh/laravel-debugbar --dev` |

### Prochains Tutoriels (À Venir)

!!! note "**Série Authentification Laravel**"
    
    **1. Laravel Breeze (✅ Terminé - ce projet)**
    
    - Authentification simple web classique
    - Idéal pour blogs, CMS, dashboards
    
    **2. Laravel Jetstream (🔜 Prochainement)**
    
    - Breeze + fonctionnalités entreprise
    - Teams, 2FA, API tokens, sessions management
    - Choix Livewire ou Inertia.js
    
    **3. Laravel Sanctum (🔜 Prochainement)**
    
    - Authentification APIs (SPAs, mobile apps)
    - Token-based léger
    - Alternative moderne à OAuth/Passport

### Conclusion Finale

**Vous avez maintenant une base solide pour :**

✅ **Développer applications Laravel** de A à Z  
✅ **Gérer authentification** avec Breeze (et comprendre alternatives)  
✅ **Construire CRUDs** robustes et sécurisés  
✅ **Optimiser performances** (cache, indexes, Eager Loading)  
✅ **Déployer en production** sur serveur réel  
✅ **Tester automatiquement** avec PHPUnit  
✅ **Sécuriser applications** (OWASP Top 10)

**Ce projet démontre votre capacité à :**

- Livrer code production-ready
- Respecter standards sécurité
- Optimiser performances
- Écrire tests automatisés
- Documenter code proprement
- Maintenir architecture MVC

**Félicitations pour ce travail exceptionnel !**

Vous êtes désormais équipé pour construire des applications web modernes et scalables avec Laravel. Les compétences acquises dans ce projet sont **directement transférables en entreprise** et constituent une base solide pour votre évolution vers des sujets plus avancés (microservices, APIs GraphQL, applications temps réel avec WebSockets, etc.).

**Continuez à pratiquer, expérimenter et surtout : construisez vos propres projets ! **

