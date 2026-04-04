---
description: "Configuration globale de l'environnement de travail (.env) et base de données."
icon: lucide/settings
tags: ["LARAVEL", "ENV", "DATABASE", "SQLITE"]
---

# Configuration & Pratique

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. Le fichier d'environnement `.env`

Le fichier `.env` centralise **toutes les variables privées**. Ce fichier ne doit strictement **jamais** être envoyé sur un Github public.

Voici un extrait de configuration standard :

```env
APP_NAME="Blog Laravel"
APP_ENV=local
APP_KEY=base64:votre_cle_generee_ici
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_CONNECTION=sqlite
```

### 1.1 Accéder aux variables dans le code
Bien que Laravel fournisse le Helper `env('APP_NAME')`, il est **fortement recommandé** d'utiliser son proxy `config('app.name')` dans votre code métier.

Pourquoi ? En production, la configuration est mise en cache mémoire (`php artisan config:cache`) pour des raisons de vitesse, rendant les appels directs à `env()` invalides. 

<br>

---

## 2. Configurer la Base de Données

Dans ce guide, bien que Laravel supporte nativement PostgreSQL ou MySQL, nous vous recommandons d'utiliser le moteur sans-serveur **SQLite** pour débuter.

- **Avantages SQLite :** Zéro configuration (tout tient dans un fichier)

**Configuration `.env` :**
```env
DB_CONNECTION=sqlite
```

**Création du coffre fort (Bdd) :**
```bash
# Crée un fichier SQLite vide sur mac/linux
touch database/database.sqlite

# L'équivalent sur Windows :
type nul > database\database.sqlite
```

<br>

---

## 3. L'heure de la Pratique (Page Contact)

Récapitulons : nous avons configuré notre `.env`, nous avons accés à l'interface en ligne de commande. Mettons ceci en pratique en créant une route "A Propos".

### 3.1 Définir la Route
L'endroit où "attraper" les gens qui surfent sur le web.

```php title="routes/web.php"
<?php

use Illuminate\Support\Facades\Route;

// On intercepte la route /about
Route::get('/about', function () {
    // On passe une variable `$siteName` à la vue HTML 
    return view('about', [
        'siteName' => 'Blog Laravel Professionnel'
    ]);
});
```

### 3.2 Imprimer la page
Dites à Laravel ce qu'il doit afficher à l'utilisateur.

```html title="resources/views/about.blade.php"
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>À propos - {{ $siteName }}</title>
</head>
<body>
    <h1>À propos</h1>
    
    <p>Nom du site : <strong>{{ $siteName }}</strong></p>
    
    <p><a href="/">Retour à l'accueil</a></p>
</body>
</html>
```

Lancez `php artisan serve` et testez `http://localhost:8000/about` : Félicitation, vous avez passé de l'information serveur sécurisée à l'intérieur d'un rendu HTML (via les Moustaches de variables double accolades `{{ }}`).

<br>

---

## Conclusion

L'environnement est isolé et maitrisé, et nos pages virtuelles communiquent du contenu dynamique. Avant d'avancer vers le Module 2, il est important de clôturer les fondations par un système standard de conventions typographiques.
