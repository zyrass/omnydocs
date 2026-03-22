---
description: "Le Projet Ultime : Architecture complète d'un Blog avec PDO, Authentification, Routeur Front Controller et Modèle MVC simplifié."
icon: lucide/database
tags: ["PHP", "PROCÉDURAL", "MVC", "PDO", "PROJET FINAL"]
status: stable
---

# Projet 13 : Blog MVC Complet (Projet Final)

<div
  class="omny-meta"
  data-level="🔴 Avancé+"
  data-version="8.3"
  data-time="4 Heures">
</div>

!!! quote "Le Pitch"
    C'est l'heure de l'examen final. Finies les pages PHP isolées qui font tout (Vue, Logique, BDD).
    Pour ce dernier projet procédural, nous allons construire un Blog Full-Stack en adoptant une architecture "Front Controller" (Un seul `index.php` qui centralise et route tout le trafic) et en séparant la base de données (Model), la logique (Controller) et le HTML (Vue). C'est l'antichambre des Frameworks modernes comme Laravel ou Symfony.

!!! abstract "Objectifs Pédagogiques"
    1.  **Modélisation Relationnelle** : Créer un Schéma SQL complet (Utilisateurs, Articles, Commentaires, Catégories) avec des Clés Étrangères (`FOREIGN KEY`).
    2.  **Singleton PDO** : Coder une classe de connexion à la Base de données qui ne s'instancie qu'une seule fois pour économiser la RAM de votre serveur.
    3.  **Front Controller & Routing** : Dire adieu à l'accès direct aux fichiers `.php` en forçant tout le trafic web à passer par `public/index.php`.
    4.  **Templating Basique** : Séparer strictement le Backend PHP pur des vues Frontend (inclusions HTML).

## 1. La Base de Données (Le Cœur du Système)

Lancez PhpMyAdmin ou votre CLI MySQL et exécutez ce script pour forger les tables fondamentales d'un CMS.

```sql
-- Création de la forteresse
CREATE DATABASE IF NOT EXISTS omny_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE omny_blog;

-- 1. LES AUTEURS (Administrateurs du blog)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pseudo VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('auteur', 'admin') DEFAULT 'auteur',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. LES ARTICLES (Le contenu)
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    status ENUM('brouillon', 'publie') DEFAULT 'brouillon',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- La Clé Étrangère : ON DELETE CASCADE signifie "Si on supprime l'Auteur, supprime tous ses Articles"
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. LES COMMENTAIRES (L'interaction)
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    author_name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
) ENGINE=InnoDB;
```

## 2. L'Architecture des Dossiers (MVC)

Dans un vrai projet, l'internaute n'a le droit de visiter **que le dossier `public/`**. Tout le reste est caché côté Serveur Inaccessible. Mettez en place cette hiérarchie :

```text
mon-super-blog/
│
├── config/
│   └── database.php       <-- Vos identifiants PDO
│
├── src/
│   ├── Database.php       <-- Le Singleton de Connexion PDO
│   ├── Controllers/       <-- Les Cerveaux (Logique)
│   │   ├── HomeController.php
│   │   └── PostController.php
│   └── Models/            <-- Les Muscles (Requêtes SQL)
│       └── PostManager.php
│
├── views/                 <-- Le Visage (HTML)
│   ├── layout.php
│   ├── home.php
│   └── article-detail.php
│
└── public/                <-- La Porte d'Entrée
    ├── index.php          <-- Le Front Controller (Routeur)
    └── css/
        └── style.css
```

---

## 3. Implémentation du Coeur (Backend)

### A. Le Singleton PDO (`src/Database.php`)
Il assure que peu importe le nombre d'articles affichés, nous ne ferons qu'**une seule** connexion à la base de données.

```php
<?php
declare(strict_types=1);

class Database {
    private static ?PDO $instance = null;

    public static function getConnection(): PDO {
        if (self::$instance === null) {
            // Dans la vraie vie, on REQUIRE config/database.php ici
            $dsn = 'mysql:host=localhost;dbname=omny_blog;charset=utf8mb4';
            
            self::$instance = new PDO($dsn, 'root', '', [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false, // Sécurité Maximale
            ]);
        }
        return self::$instance;
    }
}
```

### B. Le Modèle (`src/Models/PostManager.php`)
Gère exclusivement le dialogue avec la table `posts`.

```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/../Database.php';

class PostManager {
    private PDO $db;

    public function __construct() {
        $this->db = Database::getConnection();
    }

    public function getPublishedPosts(): array {
        // Prévention du Problème N+1 avec un INNER JOIN
        $sql = "SELECT p.id, p.title, p.slug, p.created_at, u.pseudo AS author 
                FROM posts p 
                INNER JOIN users u ON p.user_id = u.id 
                WHERE p.status = 'publie' 
                ORDER BY p.created_at DESC";
                
        return $this->db->query($sql)->fetchAll();
    }
}
```

### C. Le Contrôleur (`src/Controllers/HomeController.php`)
Le chef d'orchestre. Il appelle le modèle, récupère les données, puis charge la Vue.

```php
<?php
declare(strict_types=1);
require_once __DIR__ . '/../Models/PostManager.php';

class HomeController {
    
    public function index(): void {
        // 1. Demande des données
        $manager = new PostManager();
        $articles = $manager->getPublishedPosts();
        
        // 2. Déclaration du titre de la page pour le Layout
        $titrePage = "Accueil du Blog";
        
        // 3. Inclusion de la Vue (qui utilisera la variable $articles)
        require_once __DIR__ . '/../../views/home.php';
    }
}
```

---

## 4. Implémentation de la Vue (Frontend)

### A. Le Layout Général (`views/layout.php`)
Le squelette commun de tout votre site (Menu, Footer).

```php
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <!-- $titrePage est dynamiquement fourni par le Contrôleur ! -->
    <title><?= htmlspecialchars($titrePage ?? 'Mon Blog', ENT_QUOTES, 'UTF-8') ?></title>
    <!-- Le CSS est appelé en Absolu depuis le dossier public/ -->
    <link rel="stylesheet" href="/css/style.css">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">

    <nav class="bg-indigo-600 text-white p-4 shadow-md">
        <div class="container mx-auto font-bold text-xl">🚀 Mon Super Blog</div>
    </nav>

    <main class="container mx-auto p-6 mt-8 bg-white shadow rounded-lg min-h-[500px]">
        <!-- LA MAGIE EST ICI : On injecte la sous-vue spécifique -->
        <?= $contenuHTML ?>
    </main>

    <footer class="text-center p-4 text-gray-500 text-sm mt-8">
        &copy; <?= date('Y') ?> - Architecture MVC Masterclass
    </footer>

</body>
</html>
```

### B. La Page d'Accueil (`views/home.php`)
Elle va "tamponner" son HTML pour l'envoyer au Layout.

```php
<?php
// On active le "Tampon de Sortie" (Output Buffering). 
// PHP garde le code HTML qui suit en mémoire au lieu de l'afficher direct à l'écran.
ob_start(); 
?>

<h1 class="text-3xl font-extrabold text-gray-800 border-b-2 border-indigo-500 pb-2 mb-6">
    Derniers Articles
</h1>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <?php if (empty($articles)): ?>
        <p class="text-gray-500 italic">Aucun article n'a été publié pour le moment...</p>
    <?php else: ?>
        <?php foreach ($articles as $post): ?>
            <article class="p-6 border border-gray-200 rounded-lg hover:shadow-lg transition">
                <h2 class="text-xl font-bold text-indigo-600 mb-2">
                    <a href="/article?id=<?= $post['id'] ?>">
                        <?= htmlspecialchars($post['title'], ENT_QUOTES, 'UTF-8') ?>
                    </a>
                </h2>
                <div class="text-sm text-gray-500">
                    Rédigé par <span class="font-semibold"><?= htmlspecialchars($post['author'], ENT_QUOTES, 'UTF-8') ?></span> 
                    le <?= date('d/m/Y', strtotime($post['created_at'])) ?>
                </div>
            </article>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<?php 
// Fin du tampon. On stocke tout ce HTML généré dans la variable $contenuHTML
$contenuHTML = ob_get_clean(); 

// On appelle ENFIN le squelette de base qui imprimera $titrePage et $contenuHTML
require __DIR__ . '/layout.php'; 
?>
```

---

## 5. Le Chef d'Orchestre (Front Controller)

C'est le SEUL fichier de votre application. Le vigile à l'entrée de la boite de nuit.
`public/index.php`

```php
<?php
declare(strict_types=1);

// Le système d'Autoload basique (Charge automatiquement vos classes sans require !)
spl_autoload_register(function ($class) {
    $cheminControllers = __DIR__ . '/../src/Controllers/' . $class . '.php';
    if (file_exists($cheminControllers)) require $cheminControllers;
});

// ==== LE ROUTEUR ====
// On attrape le paramètre GET "page". S'il n'existe pas, on est sur l'accueil.
$pageVoulue = $_GET['page'] ?? 'home';

try {
    switch ($pageVoulue) {
        
        case 'home':
            $controller = new HomeController();
            $controller->index();
            break;
            
        case 'article':
            // Ici on appellerait un PostController
            echo "Page de l'article spécifique en construction...";
            break;
            
        default:
            http_response_code(404);
            echo "Erreur 404 : Cette route MVC est inconnue au bataillon.";
            break;
    }
} catch (Exception $e) {
    // Si la Base de données explose, on atterrit ici avec grâce.
    http_response_code(500);
    die("Alerte Rouge Serveur : " . $e->getMessage());
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Votre application n'est plus un gâchis procédural mais un système modulaire orienté composant :</p>
  <ul class="space-y-2 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Vous avez appris le concept du <code>ob_start()</code> (Output Buffering). C'est ce qui permet aux vues Layout d'encastrer des sous-vues de manière propre. C'est la base des moteurs comme Blade (Laravel) ou Twig (Symfony).</span>
    </li>
    <li class="flex items-start gap-2">
      <span class="text-green-500">✓</span>
      <span class="text-gray-700">Toutes les requêtes SQL sont encapsulées loin de l'HTML (Dans le dossier <strong>Models</strong>).</span>
    </li>
  </ul>
</div>
