---
description: "Projet Pratique POO : Découvrir la structuration professionnelle d'une application PHP en répartissant les responsabilités (MVC, Repositories, Services) grâce aux Namespaces PSR-4."
icon: lucide/network
tags: ["PHP", "POO", "NAMESPACES", "MVC", "ARCHITECTURE"]
status: stable
---

# Projet 24 : Architecture MVC (Namespaces)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Mettre l'intégralité de ses classes PHP dans le dossier racine avec des tonnes de `require_once` mène au désastre.
    Le standard **PSR-4** définit une norme où le chemin du dossier correspond strictement au `Namespace` de la classe, ce qui permet à l'outil `Composer` de charger automatiquement vos fichiers au bon moment (*Autoloading*).
    Nous allons architecturer un mini-Blog.

!!! abstract "Objectifs Pédagogiques"
    1.  **Le Fichier de Dépendances** : Configurer `composer.json` pour déclarer que la racine du namespace `Blog\` correspond au dossier physique `src/`.
    2.  **Séparation des Couches** : Isoler les `Models` (Données brutes), les `Repositories` (Requêtes SQL), les `Services` (Logique Métier) et les `Controllers` (Réception HTTP).
    3.  **L'Auto-Loader Master** : Découvrir qu'un seul petit fichier (`vendor/autoload.php`) remplace les centaines de `require` d'une application bas de gamme.

## 1. Topologie du Projet (Dossiers)

C'est ainsi que sont construits **tous** les Frameworks PHP du monde entier (Symfony, Laravel).

```text
mon-blog/
├── composer.json          # Règle d'autoloading
├── public/                # Le SEUL dossier accessible depuis le Navigateur Web !
│   └── index.php          # Le Front-Controller (Routeur Unique)
└── src/                   # Le Coeur de l'App (Namespace Racine : Blog\)
    ├── Models/
    │   ├── Post.php       # -> Blog\Models\Post
    │   └── Category.php   # -> Blog\Models\Category
    ├── Repositories/
    │   └── PostRepository.php
    ├── Services/
    │   └── PostService.php
    └── Controllers/
        └── PostController.php
```

## 2. Le Déclencheur (composer.json)

Pour que la magie opère, il faut créer ce fichier à la racine de votre projet et taper la commande `composer dump-autoload` dans votre terminal.

```json
{
    "autoload": {
        "psr-4": {
            "Blog\\": "src/"
        }
    }
}
```

## 3. L'Arbre Généalogique des Classes

Voici les codes des 4 composants isolés. Observez l'incessante danse des `namespace` et des `use` !

### A. Le Modèle (La Donnée)
```php
<?php
// Fichier : src/Models/Post.php
namespace Blog\Models; // Je me trouve dans le dossier src/Models !

use DateTime; // J'importe la classe native de PHP depuis la racine Globale (\)

class Post {
    private ?int $id = null;
    private string $title;
    
    public function __construct(string $title) {
        $this->title = $title;
        // ...
    }
}
?>
```

### B. Le Repository (Le Sourd-Muet qui parle à la BDD)
```php
<?php
// Fichier : src/Repositories/PostRepository.php
namespace Blog\Repositories;

use Blog\Models\Post; // J'ai besoin de savoir ce qu'est un "Post" !
use PDO; // Classe native PHP

class PostRepository {
    private PDO $pdo;
    
    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }
    
    // Il extrait la data SQL brute qu'il transforme en "Objet Post" (Hydratation)
    public function findBySlug(string $slug): ?Post {
        $stmt = $this->pdo->prepare("SELECT * FROM posts WHERE slug = ?");
        $stmt->execute([$slug]);
        $data = $stmt->fetch();
        
        return $data ? new Post($data['title']) : null;
    }
}
?>
```

### C. Le Service (Le Métier / Le Cerveau)
```php
<?php
// Fichier : src/Services/PostService.php
namespace Blog\Services;

use Blog\Models\Post;
use Blog\Repositories\PostRepository;

// Il utilise le Repository pour récupérer les données, fait des vérifications intelligentes puis rend l'info.
class PostService {
    private PostRepository $repository;
    
    public function __construct(PostRepository $repository) {
        $this->repository = $repository;
    }
    
    public function getPostBySlug(string $slug): ?Post {
        return $this->repository->findBySlug($slug);
    }
}
?>
```

### D. Le Contrôleur (Le Standardiste Téléphonique)
```php
<?php
// Fichier : src/Controllers/PostController.php
namespace Blog\Controllers;

use Blog\Services\PostService;

// Il réceptionne la requête HTTP, demande le résultat au Service, et charge une Vue (HTML)
class PostController {
    
    private PostService $postService;
    
    public function __construct(PostService $postService) {
        $this->postService = $postService;
    }
    
    public function show(string $slug): void {
        
        $post = $this->postService->getPostBySlug($slug);
        
        if (!$post) {
            http_response_code(404);
            echo "Erreur 404 : Cet article n'existe pas ou plus.";
            return; // Coupe l'exécution.
        }
        
        // Simulation d'une vue (Twig/Blade)
        require __DIR__ . '/../../views/posts/show.php';
    }
}
?>
```

## 4. Le Routeur Final (index.php)

L'entièreté de l'application passe obligatoirement par ce micro-fichier (Le vigile à la porte de la boite de nuit). Pas UN SEUL script ne comporte un `require_once` de la classe voisine. 

```php
<?php
// Fichier : public/index.php

// 💥 LA LIGNE QUI CHANGE TOUT ! 💥
// L'Autoloader scannera vos Namespaces à la lueur des dossiers physiques pour instancier la bonne classe dynamiquement.
require __DIR__ . '/../vendor/autoload.php';

use Blog\Controllers\PostController;
use Blog\Repositories\PostRepository;
use Blog\Services\PostService;

// Assemblage de l'Oignon de dépendances (De l'écorce vers le Noyau dur)
// C'est ce qu'on appelle un "Container d'Injection de Dépendances" à l'ancienne.
$pdo = new PDO('mysql:host=localhost;dbname=blog', 'root', '');
$repository = new PostRepository($pdo);
$service = new PostService($repository);
$controller = new PostController($service);

// ROUTING NAÏF MAIS EFFICACE
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($uri === '/') {
    $controller->index();
    
} elseif (preg_match('#^/post/([a-z0-9-]+)$#', $uri, $matches)) {
    // on a chopé l'ID dans le "/post/mon-article-slug" ! On envoie au Controller.
    $controller->show($matches[1]);
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Vous avez franchi le dernier palier qui sépare un amateur d'un développeur professionnel. En utilisant la norme **PSR-4**, votre code est immédiatement compréhensible et réutilisable dans des Frameworks gigantesques comme Symfony ou Laravel.</p>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
