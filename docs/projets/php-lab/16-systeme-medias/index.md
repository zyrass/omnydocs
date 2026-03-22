---
description: "Projet Pratique POO : Maîtriser l'Héritage et le Polymorphisme à travers un gestionnaire de Bibliothèque Multimédia (Vidéos, Audios, Textes)."
icon: lucide/film
tags: ["PHP", "POO", "HÉRITAGE", "POLYMORPHISME"]
status: stable
---

# Projet 16 : Bibliothèque de Médias

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Une Vidéo a une résolution, un Son a un format d'encodage (mp3). Mais ils ont tous les deux un _Auteur_, un _Titre_ et une _Durée_.
    Comment éviter de dupliquer les champs communs ? Avec l'**Héritage** (`extends`) !
    Comment faire une boucle sur TOUS ces médias sans se soucier de leur type exact ? Avec le **Polymorphisme** !

!!! abstract "Objectifs Pédagogiques"
    1.  **Classe Abstraite** : Comprendre pourquoi la classe mère `Media` ne doit jamais être instanciée directement (`abstract class`).
    2.  **Héritage Direct** : Utiliser `extends Media` et invoquer `parent::__construct()` pour ne pas réinventer la roue.
    3.  **Contrat Abstrait** : Forcer les enfants à coder leurs propres règles avec `abstract public function getDuration();`.
    4.  **Manipulation Polymorphique** : Parcourir un tableau d'objets hybrides et appeler `display()` sans jamais vérifier si c'est un son ou une vidéo.

## 1. La Classe Mère (Le Moule Abstrait)

La classe `Media` contient l'ADN commun. Mais n'étant ni une vidéo concrète, ni un texte concret, on empêche sa création directe via `abstract`.

> Fichier `Media.php`

```php
<?php
declare(strict_types=1);

abstract class Media {
    protected string $title; // "protected" car nos enfants (Video, Audio) en auront besoin !
    protected string $author;
    protected DateTime $publishedDate;
    protected int $views = 0;
    
    public function __construct(string $title, string $author) {
        $this->title = $title;
        $this->author = $author;
        $this->publishedDate = new DateTime();
    }
    
    // ============================================
    // CONTRATS IMPOSÉS AUX ENFANTS
    // ============================================
    // Tous les enfants DEVRONT obligatoirement coder ces méthodes.
    abstract public function display(): string;
    abstract public function getDuration(): int; // Secondes
    
    // ============================================
    // FONCTIONNALITÉS COMMUNES
    // ============================================
    public function incrementViews(): void {
        $this->views++;
    }
    
    public function getViews(): int {
        return $this->views;
    }
    
    public function getTitle(): string {
        return $this->title;
    }
    
    // "final" empêche les enfants de redéfinir ou de trafiquer cette méthode spécifique.
    final public function getMetadata(): array {
        return [
            'title' => $this->title,
            'author' => $this->author,
            'published' => $this->publishedDate->format('Y-m-d'),
            'views' => $this->views,
            'duration' => $this->getDuration() // Appelle la fonction de l'enfant courrant !
        ];
    }
}
?>
```

## 2. Les Classes Enfants (La Spécialisation)

Chacun de nos enfants va hériter de l'ADN de `Media`, et rajouter sa propre spécialité.

> Fichier `ClassesEnfants.php` (À séparer dans la vraie vie)

```php
<?php
declare(strict_types=1);

require_once 'Media.php';

// =============== LA VIDÉO ===============
class VideoMedia extends Media {
    private int $durationSeconds;
    private string $resolution;
    
    public function __construct(string $title, string $author, int $durationSeconds, string $resolution = '1080p') {
        // Obligatoire : On appelle le constructeur du Papa pour qu'il gère le titre et l'auteur !
        parent::__construct($title, $author);
        
        // Et on gère NOTRE spécialité
        $this->durationSeconds = $durationSeconds;
        $this->resolution = $resolution;
    }
    
    // On valide le contrat du parent !
    public function display(): string {
        return "🎥 Vidéo : {$this->title} ({$this->resolution})";
    }
    
    // On valide le contrat du parent !
    public function getDuration(): int {
        return $this->durationSeconds;
    }
}

// =============== LE PODCAST ===============
class AudioMedia extends Media {
    private int $durationSeconds;
    private string $format;
    
    public function __construct(string $title, string $author, int $durationSeconds, string $format = 'mp3') {
        parent::__construct($title, $author);
        $this->durationSeconds = $durationSeconds;
        $this->format = $format;
    }
    
    public function display(): string {
        return "🎵 Audio : {$this->title} ({$this->format})";
    }
    
    public function getDuration(): int {
        return $this->durationSeconds;
    }
}

// =============== L'ARTICLE TEXTE ===============
class TextMedia extends Media {
    private string $content;
    private int $wordCount;
    
    public function __construct(string $title, string $author, string $content) {
        parent::__construct($title, $author);
        $this->content = $content;
        $this->wordCount = str_word_count($content);
    }
    
    public function display(): string {
        return "📄 Article : {$this->title} - {$this->wordCount} mots";
    }
    
    public function getDuration(): int {
        // En moyenne, on lit 200 mots par minute. On convertit ça en temps de lecture (secondes)
        return (int)ceil($this->wordCount / 200) * 60;
    }
}
?>
```

## 3. Le Super Gestionnaire (Polymorphisme !)

La bibliothèque ne gère pas spécifiquement des Vidéos ou des Textes. Elle demande une entité Type `Media` ! PHP ira chercher tout seul la bonne méthode en fonction de la Classe exacte lors du déroulement.

> Fichier `index.php`

```php
<?php
declare(strict_types=1);

require_once 'Media.php';
require_once 'ClassesEnfants.php';

class MediaLibrary {
    private array $medias = [];
    
    // L'injection MAGIQUE ! On tape contre le TYPE ABSTRAIT père. 
    // Que ce soit une vidéo ou un son, tant qu'il "extends Media", il est accepté !
    public function addMedia(Media $media): void {
        $this->medias[] = $media;
    }
    
    public function displayAll(): void {
        foreach ($this->medias as $media) {
            // PHP appellera le bon "display()" automatiquement ! C'est le polymorphisme.
            echo $media->display() . "\n"; 
        }
    }
    
    public function getTotalDuration(): int {
        $total = 0;
        foreach ($this->medias as $media) {
            $total += $media->getDuration();
        }
        return $total;
    }
}


// --- EXÉCUTION DU PROGRAMME ---

$library = new MediaLibrary();

$video = new VideoMedia('PHP MVC Tutorial', 'Omnyvia', 1800, '4K');
$audio = new AudioMedia('Podcast Cybersécurité', 'Bob', 2400, 'flac');
$article = new TextMedia('Introduction à la POO', 'Charlie', 'La POO est un paradigme puissant. Il permet de faire tellement de choses géniales et magiques !');

// On injecte les enfants (qui sont tous fondamentalement des "Medias")
$library->addMedia($video);
$library->addMedia($audio);
$library->addMedia($article);

echo "============== CATALOGUE ===============\n";
$library->displayAll();

echo "\n============== ANALYTICS ===============\n";
echo "Durée totale estimée du catalogue : " . $library->getTotalDuration() . " secondes\n";

?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Vous constatez la beauté de la méthode <code>addMedia(Media $media)</code> : Elle démontre que la Classe Extérieure (Le Library) n'a jamais besoin de savoir si vous venez de coder un nouveau composant <code>VRMedia extends Media</code>. Le système principal ne sera jamais cassé par l'ajout de nouveaux membres enfants !</span>
    </li>
  </ul>
</div>
