---
description: "Projet Pratique POO : Construire une véritable entité (Classe) pour représenter un Article de Blog selon les standards PHP modernes."
icon: lucide/file-text
tags: ["PHP", "POO", "CLASSE", "OBJET"]
status: stable
---

# Projet 14 : Classe Article de Blog

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="8.3"
  data-time="1 - 2 heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Pitch"
    Dites adieu aux tableaux associatifs (`$post['title']`). 
    En Programation Orientée Objet (POO), nous allons créer une **Entité**. Une "Classe" qui définit très exactement ce qu'est un Article (ses propriétés) et ce qu'il peut faire (ses méthodes : publier, archiver, lire).

!!! abstract "Objectifs Pédagogiques"
    1.  **Encapsulation** : Cacher la donnée (`private`) pour forcer l'usage des `Getters` et `Setters`.
    2.  **Méthodes Magiques** : Comprendre le rôle fondamental de `__construct()` à l'instanciation de l'objet.
    3.  **Propriétés Statiques** : Compter toutes les instances de la classe créées en mémoire avec `self::$count`.
    4.  **Exceptions** : Rejeter formellement la donnée via `throw new InvalidArgumentException` si le titre est trop court.

## La Classe `BlogPost`

Voici la définition architecturale de ce qu'est un article. Créez un fichier `BlogPost.php`.

```php
<?php
declare(strict_types=1);

/**
 * Représentation d'une ligne de la table 'posts' sous forme d'Objet Manipulable
 */
class BlogPost {
    
    // Propriété Statique : Appartient à la Classe (le Moule), pas aux objets.
    // Idéal pour compter le nombre de gâteaux qui sont sortis du moule.
    private static int $totalPosts = 0;
    
    // Propriétés d'Instance (Typées PHP 7.4+)
    private int $id;
    private string $title;
    private string $content;
    private string $author;
    private string $status; // 'draft', 'published', 'archived'
    private DateTime $createdAt;
    private ?DateTime $publishedAt = null; // Propriété Nullable (peut être vide au départ)
    private int $views = 0;
    
    /**
     * LE CONSTRUCTEUR
     * Exécuté automatiquement lors du "new BlogPost(...)"
     */
    public function __construct(string $title, string $content, string $author) {
        
        // On incrémente le compteur global de la classe
        self::$totalPosts++;
        $this->id = self::$totalPosts;
        
        // On utilise les Setters au sein du constructeur pour profiter de leur validation sécurisée !
        $this->setTitle($title);
        $this->setContent($content);
        
        $this->author = $author;
        $this->status = 'draft';
        $this->createdAt = new DateTime(); // Timestamp de création
    }
    
    // ============================================
    // GETTERS (Accesseurs) : Lire la donnée
    // ============================================
    
    public function getId(): int {
        return $this->id;
    }
    
    public function getTitle(): string {
        return $this->title;
    }
    
    public function getStatus(): string {
        return $this->status;
    }
    
    // ============================================
    // SETTERS (Mutateurs) : Écrire la donnée
    // ============================================
    
    public function setTitle(string $title): void {
        // Validation très stricte imposée par la Classe
        if (strlen($title) < 5 || strlen($title) > 200) {
            throw new InvalidArgumentException("Titre incorrect (min 5, max 200).");
        }
        $this->title = $title;
    }
    
    public function setContent(string $content): void {
        if (strlen($content) < 50) {
            throw new InvalidArgumentException("Le contenu est trop léger (min 50 chars).");
        }
        $this->content = $content;
    }
    
    // ============================================
    // MÉTHODES MÉTIERS (Le Comportement)
    // ============================================
    
    /**
     * Publier l'article et figer la date de publication
     */
    public function publish(): bool {
        if ($this->status === 'published') {
            return false; // Déjà publié
        }
        
        $this->status = 'published';
        $this->publishedAt = new DateTime();
        return true;
    }
    
    /**
     * Extraire l'introduction intelligente
     */
    public function getExcerpt(int $length = 150): string {
        if (strlen($this->content) <= $length) {
            return $this->content;
        }
        return substr($this->content, 0, $length) . '...';
    }
    
    /**
     * Calculer le temps de lecture
     */
    public function getReadingTime(): int {
        // On estime la vitesse moyenne de lecture à 200 mots/minute
        $wordCount = str_word_count($this->content);
        return (int)ceil($wordCount / 200);
    }
    
    // ============================================
    // MÉTHODE STATIQUE
    // ============================================
    
    public static function getTotalPostsCreatedInSession(): int {
        return self::$totalPosts;
    }
}
?>
```

## Manipuler l'Objet (Le Programme)

Maintenant, créons un script index.php qui va inclure notre classe et "Jouer" avec.

```php
<?php
require_once 'BlogPost.php';

try {
    // Instanciation de l'Objet
    $article = new BlogPost(
        'Introduction à la POO Masterclass', // Titre validé (Plus de 5 chars)
        "La Programmation Orientée Objet est un paradigme qui organise le code autour d'objets. Les objets combinent données et comportements dans des structures cohérentes. Cette approche améliore la réutilisabilité et la maintenabilité d'énormes projets. Ne loupez pas le coche.", // Contenu validé (Plus de 50 chars)
        'Zyrass'
    );

    echo "== ÉTAT INITIAL ==\n";
    echo "ID du post : " . $article->getId() . "\n";
    echo "Auteur : " . $article->getAuthor() . "\n";
    echo "Statut Actuel : " . $article->getStatus() . "\n";
    echo "Temps de lecture estimé : " . $article->getReadingTime() . " minute(s)\n";
    
    echo "\n== ACTION MÉTIER ==\n";
    // On actionne un comportement !
    $article->publish();
    echo "L'article vient d'être publié avec succès.\n";
    echo "Nouveau Statut : " . $article->getStatus() . "\n";
    
    // Preuve des champs protégés
    echo "\nTotal articles générés en RAM : " . BlogPost::getTotalPostsCreatedInSession() . "\n";

} catch (Exception $e) {
    // Si $article = new BlogPost("yo", "trop court", "Max")
    // Le code explosera proprement sans tout crasher, et cette section attrapera l'explication !
    echo "[X] Erreur d'Instanciation : " . $e->getMessage();
}
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Comprenez bien la notion de <strong>Visibilité Murailles (Private)</strong>. Il est impossible dans votre <code>index.php</code> de faire <code>$article->title = "Hacked";</code>. Le système plantera. Vous devez demander à l'Objet d'accepter le changement via sa méthode autorisée <code>$article->setTitle("Hacked")</code>, qui pourra, elle, refuser car vous n'avez pas respecté les règles. C'est l'essence de la POO.</span>
    </li>
  </ul>
</div

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
