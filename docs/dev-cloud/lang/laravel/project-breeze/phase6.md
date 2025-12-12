---
description: "Création de 9 vues Blade avec Tailwind CSS : layouts, grilles articles, formulaires CRUD, dashboard et design responsive."
icon: lucide/layout-template
tags: ["BLADE", "TAILWIND", "VIEWS", "FRONTEND", "UI-UX"]
---

# Phase 6 : Vues Blade & Interface

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3h-4h">
</div>

## Introduction aux Vues Blade et Interface Utilisateur

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

## Étape 6.1 : Modifier le Layout Principal (Structure Commune)

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

```html title="Fichier : resources/views/layouts/app.blade.php"
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

## Étape 6.2 : Créer la Page d'Accueil (Liste Articles + Sidebar)

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

```html title="Fichier : resources/views/home.blade.php"
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

### Tableau Récapitulatif des Directives Blade

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

## Étape 6.3 : Créer la Vue Article Individuel (Affichage Complet)

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

```html title="Fichier : resources/views/posts/show.blade.php"
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

## Étape 6.4 : Créer le Formulaire de Création d'Article

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

```html title="Fichier : resources/views/posts/create.blade.php"
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

## Étape 6.5 : Créer le Formulaire d'Édition d'Article

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

```html title="Fichier : resources/views/posts/edit.blade.php"
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

### Tableau Comparatif create.blade.php vs edit.blade.php

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

### Explications Techniques Approfondies

??? abstract "**1. Pourquoi @method('PUT') ?**"

    HTML ne supporte **nativement** que deux méthodes dans `<form method="">` :

    - GET : Récupération de données (navigation, recherche)
    - POST : Soumission de données (création, modification)

    Les méthodes RESTful supplémentaires (PUT, PATCH, DELETE) sont utilisées par les APIs et frameworks modernes mais **non supportées** par HTML classique.

    **Solution Laravel :**

    Laravel utilise le **method spoofing** : un champ caché `_method` indique la vraie méthode souhaitée.

    ```html title="Code Blade"
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

    ```html title="Code Blade"
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

    ```html title="Code Blade"
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

    ```html title="Code Blade"
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

## Étape 6.6 : Créer le Dashboard Auteur (Statistiques et Gestion Articles)

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

```html title="Fichier : resources/views/dashboard.blade.php"
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

### Tableau Anatomie des Cartes Statistiques

| Élément | Classes Tailwind | Rôle | Valeurs Possibles |
|---------|-----------------|------|-------------------|
| **Conteneur** | `bg-white shadow-sm rounded-lg` | Carte blanche avec ombre | Standard toutes cartes |
| **Padding** | `p-6` | Espacement interne | 1.5rem (24px) |
| **Layout** | `flex justify-between items-center` | Disposition texte/icône | Texte gauche, icône droite |
| **Label** | `text-sm font-medium text-gray-600` | Description métrique | "Total Articles", "Publiés", etc. |
| **Valeur** | `text-3xl font-bold text-[color]` | Chiffre statistique | Couleur selon contexte |
| **Icône cercle** | `w-12 h-12 bg-[color]-100 rounded-full` | Décoration visuelle | Emoji unicode |
| **Couleurs** | Variations `-100` (fond) et `-600` (texte) | Cohérence sémantique | Indigo, vert, jaune, bleu |

### Code Pattern Réutilisable

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

### Explications Techniques Approfondies

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

## Étape 6.7 : Créer la Page Catégorie (Filtrage Articles par Thématique)

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

```html title="Fichier : resources/views/categories/show.blade.php"
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

### Tableau Comparatif Méthodes Pagination Laravel

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

### Explications Techniques Approfondies

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

## Étape 6.8 : Créer la Page Auteur (Profil Public et Articles)

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

```html title="Fichier : resources/views/authors/show.blade.php"
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

### Tableau Comparatif Dashboard vs Page Auteur

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

### Explications Techniques Approfondies

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

## Étape 6.9 : Créer la Page Édition Profil Utilisateur (Paramètres Compte)

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

```html title="Fichier : resources/views/profile/edit.blade.php"
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

### Tableau Récapitulatif des 3 Formulaires

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

### Explications Techniques Approfondies

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

## Récapitulatif Phase 6

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

<br />