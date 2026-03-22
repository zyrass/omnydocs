---
description: "Projet Pratique POO : Maîtriser le principe de Ségrégation des Interfaces et l'Injection de Dépendance avec un gestionnaire de Sauvegarde Multi-supports."
icon: lucide/hard-drive
tags: ["PHP", "POO", "INTERFACE", "SOLID", "STOCKAGE"]
status: stable
---

# Projet 18 : Système de Stockage

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Votre application doit sauvegarder des factures. Au début, vous les enregistrez sur le Disque Dur (`LocalStorage`). Demain, l'entreprise grandit et veut tout mettre sur Amazon S3 Cloud.
    Comment faire évoluer le code sans casser le système principal `FileService` ?
    Réponse : Grâce aux **Interfaces** !

!!! abstract "Objectifs Pédagogiques"
    1.  **Le Contrat (Interface)** : Créer une structure 100% abstraite `StorageInterface` imposant les méthodes `put()`, `get()` et `delete()`.
    2.  **L'Implémentation (`implements`)** : Coder deux classes distinctes (`LocalStorage` et `InMemoryStorage`) qui respectent ce contrat à la lettre.
    3.  **L'Injection de Dépendance** : Le système "Master" `FileService` ne demandera ni le disque local, ni le Cloud : il demandera "_Quelque chose qui respecte la StorageInterface_". 

## 1. Le Contrat Stricte

Une Interface ne contient **AUCUN** code logique. C'est uniquement un contrat juridique. Toutes les méthodes doivent être publiques.

```php
<?php
declare(strict_types=1);

interface StorageInterface {
    public function put(string $key, string $content): bool;
    public function get(string $key): ?string;
    public function exists(string $key): bool;
    public function delete(string $key): bool;
    public function list(string $prefix = ''): array;
}
?>
```

## 2. Les Implémentations Multiples

Voici deux Classes qui n'ont rien en commun physiologiquement (l'une écrit sur le disque C:, l'autre garde ça en RAM PHP), mais qui partagent une signature identique imposée par l'interface.

```php
<?php
declare(strict_types=1);

require_once 'StorageInterface.php';

// ============================================
// COMPOSANT 1 : SAUVEGARDE SUR DISQUE LOCAL
// ============================================
class LocalStorage implements StorageInterface {
    
    private string $basePath;
    
    public function __construct(string $basePath) {
        $this->basePath = rtrim($basePath, '/');
        
        // Crée le dossier s'il n'existe pas
        if (!is_dir($this->basePath)) {
            mkdir($this->basePath, 0755, true);
        }
    }
    
    public function put(string $key, string $content): bool {
        $path = $this->getPath($key);
        $dir = dirname($path);
        
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        return file_put_contents($path, $content) !== false;
    }
    
    public function get(string $key): ?string {
        $path = $this->getPath($key);
        if (!file_exists($path)) {
            return null;
        }
        return file_get_contents($path);
    }
    
    public function exists(string $key): bool {
        return file_exists($this->getPath($key));
    }
    
    public function delete(string $key): bool {
        $path = $this->getPath($key);
        if (file_exists($path)) {
            return unlink($path);
        }
        return false;
    }
    
    public function list(string $prefix = ''): array {
        // Logique complexe pour scanner le disque Windows/Linux
        $files = [];
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($this->basePath)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $relativePath = str_replace($this->basePath . '/', '', $file->getPathname());
                if ($prefix === '' || str_starts_with($relativePath, $prefix)) {
                    $files[] = $relativePath;
                }
            }
        }
        return $files;
    }
    
    private function getPath(string $key): string {
        return $this->basePath . '/' . $key;
    }
}

// ============================================
// COMPOSANT 2 : SAUVEGARDE EN MÉMOIRE VIVE (RAM)
// ============================================
class InMemoryStorage implements StorageInterface {
    
    // Un simple tableau associatif éphémère
    private array $storage = [];
    
    public function put(string $key, string $content): bool {
        $this->storage[$key] = $content;
        return true;
    }
    
    public function get(string $key): ?string {
        return $this->storage[$key] ?? null;
    }
    
    public function exists(string $key): bool {
        return isset($this->storage[$key]);
    }
    
    public function delete(string $key): bool {
        if (isset($this->storage[$key])) {
            unset($this->storage[$key]);
            return true;
        }
        return false;
    }
    
    public function list(string $prefix = ''): array {
        if ($prefix === '') {
            return array_keys($this->storage);
        }
        return array_filter(
            array_keys($this->storage),
            fn($key) => str_starts_with($key, $prefix)
        );
    }
}
?>
```

## 3. L'Orchestrateur Suprême (Injection de Dépendance)

C'est ici qu'on va observer la Puissance du concept. `FileService` s'en fout royalement de savoir s'il tourne sur Amazon, sur Google Cloud ou sur un PC Portable Local.

```php
<?php
declare(strict_types=1);

require_once 'StorageInterface.php';
require_once 'LocalStorage.php';
require_once 'InMemoryStorage.php';

class FileService {
    
    // 🔥 L'INJECTION CLÉ 🔥
    // On ne tape pas sur "LocalStorage" ! On tape sur "N'importe quelle Classe qui a signé le contrat StorageInterface"
    public function __construct(private StorageInterface $storage) {}
    
    public function saveInvoice(string $filename, string $content): bool {
        echo "[FileService] Requête de sauvegarde pour la facture : {$filename}\n";
        return $this->storage->put($filename, $content);
    }
    
    public function readInvoice(string $filename): ?string {
        return $this->storage->get($filename);
    }
}

// --- ESSAI EN PRODUCTION RÉELLE (DISQUE DUR) ---
$disqueDur = new LocalStorage(__DIR__ . '/factures');
$serviceProd = new FileService($disqueDur);

$serviceProd->saveInvoice('facture_001.txt', 'Montant : 500€');
echo "Lecture DD : " . $serviceProd->readInvoice('facture_001.txt') . "\n";


// --- ESSAI POUR LES TESTS UNITAIRES (RAM RAPIDE) ---
// On ne veut pas écrire sur le disque pour tester le serveur CI/CD
$memoireRam = new InMemoryStorage();
$serviceTest = new FileService($memoireRam); // Magique, ça marche car il implémente l'interface !

$serviceTest->saveInvoice('facture_fictive.txt', 'Ceci est un test RAM');
echo "Lecture RAM : " . $serviceTest->readInvoice('facture_fictive.txt') . "\n";
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <ul class="space-y-4 mb-0">
    <li class="flex items-start gap-2">
      <span class="text-green-500 font-bold mt-1">1</span>
      <span class="text-gray-700">Vous avez réalisé l'<strong>Injection de Dépendance par l'Interface</strong>. Demain, si l'entreprise achète l'accès Amazon AWS S3, vous n'aurez qu'à coder <code>CloudS3Storage implements StorageInterface</code> et faire <code>new FileService($aws)</code>. Pas une seule ligne de la logique métier principale (<code>FileService</code>) ne sera modifiée ! C'est le principe Ouvert/Fermé (Open/Closed Principle) du modèle SOLID.</span>
    </li>
  </ul>
</div>
