---
description: "Comprendre la structure d'un projet Laravel et son arborescence"
icon: lucide/folder-tree
tags: ["LARAVEL", "STRUCTURE", "ARBORESCENCE"]
---

# L'Arborescence Laravel

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## Vue d'ensemble de l'arborescence

Quand vous créez un projet Laravel, voici la structure générée :

```bash
blog-laravel/
├── app/                    # Code métier de l'application
│   ├── Exceptions/        # Gestionnaires d'exceptions
│   ├── Http/              # Controllers, Middleware, Requests
│   ├── Models/            # Modèles Eloquent (ORM)
│   └── Providers/         # Service Providers (bootstrapping)
├── bootstrap/             # Fichiers de démarrage du framework
├── config/                # Fichiers de configuration
├── database/              # Migrations, seeders, factories
├── public/                # Point d'entrée web (accessible HTTP)
├── resources/             # Vues (Blade), CSS, JS
├── routes/                # Définition des routes (web, api, console)
├── storage/               # Fichiers générés par l'app (logs, cache, uploads)
├── tests/                 # Tests automatisés
├── vendor/                # Dépendances Composer (NE PAS MODIFIER)
├── .env                   # Configuration environnement
└── artisan                # Executable CLI Laravel
```

<br>

---

## 1. Explication des dossiers critiques

Chaque dossier a un **rôle précis**. Comprendre cette organisation est essentiel.

### 1.1 Le dossier `app/`

**Rôle :** Contient **tout votre code métier**. C'est ici que vous passerez 80% de votre temps.

**Principe important :**  
Laravel suit le pattern **MVC** (Model-View-Controller). Vos **Models** vont dans `app/Models/`, vos **Controllers** dans `app/Http/Controllers/`, et vos **Views** dans `resources/views/`.

### 1.2 Le dossier `routes/`

**Rôle :** Définir les **URLs de votre application** et les mapper vers des actions (controllers).

**Exemple de route dans `routes/web.php` :**

```php
<?php

use Illuminate\Support\Facades\Route;

// Route GET vers la page d'accueil
Route::get('/', function () {
    return view('welcome'); // Retourne la vue resources/views/welcome.blade.php
});
```

!!! tip "Convention de nommage"
    Laravel utilise des **facades** (classes statiques apparentes) pour simplifier l'accès aux services. `Route::get()` est en réalité un appel à une instance du routeur injectée par le Service Container.

### 1.3 Le dossier `resources/views/`

**Rôle :** Contient les **templates Blade** (`.blade.php`).
Blade est le moteur de templates de Laravel. Il permet d'écrire du HTML avec des directives PHP simplifiées.

**Directives Blade courantes :**
- `{{ $variable }}` : Affiche une variable (échappement automatique)
- `@if`, `@else`, `@endif` : Structures de contrôle
- `@foreach`, `@endforeach` : Boucles

### 1.4 Le fichier `.env`

**Rôle :** Configuration **spécifique à l'environnement** (développement, production, test).

```env
APP_NAME="Blog Laravel"
APP_ENV=local
APP_KEY=base64:GeneratedKeyHere
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=sqlite
```

**Variables critiques :**
- `APP_KEY` : Clé de chiffrement (générée automatiquement, **JAMAIS** committée en clair)
- `APP_DEBUG` : Affichage des erreurs détaillées (true en dev, **false** en prod)
- `DB_CONNECTION` : Type de base de données (`sqlite`, `mysql`, `pgsql`)

!!! danger "Sécurité .env"
    Le fichier `.env` contient des **secrets** (clés API, mots de passe DB). Il est **git-ignored** par défaut. **JAMAIS** de commit de `.env` dans git. L'outil `php artisan key:generate` permet d'en générer une nouvelle.

<br>

---

## Conclusion

L'arborescence n'a désormais plus de secret, et la séparation MVC peut enfin se mettre en place. Sans surprise, le prochain sous-module explorera le cœur de l'approche MVC.
