---
description: "Projet Pratique POO : Maîtriser la gestion des Erreurs et des Exceptions (Try/Catch) à travers la construction d'un système de manipulation de fichiers robuste."
icon: lucide/folder-open
tags: ["PHP", "POO", "EXCEPTIONS", "FILESYSTEM", "SÉCURITÉ"]
status: stable
---

# Projet 22 : Gestionnaire de Fichiers

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    Tenter de lire un fichier qui n'existe pas en PHP procédural génère un affreux *Warning* jaune qui pollue l'écran et continue le script incognito.
    En POO Moderne, on ne rigole pas avec ça. On **Lance (`throw`) des Exceptions** typées que l'on pourra **Attraper (`catch`)** plus haut pour informer gracieusement l'utilisateur du problème ("Oops, disque dur plein !").

!!! abstract "Objectifs Pédagogiques"
    1.  **Typage des Catastrophes** : Créer ses propres classes d'Exceptions (`FileNotFoundException`, `DirectoryNotWritableException`) pour que le système sache repérer EXACTEMENT quel est le problème.
    2.  **L'Émetteur (Le code qui pète)** : Construire `FileManager` qui ne fait pas de `echo "Erreur"`, mais qui lance farouchement des Exceptions quand une manipulation Unix foire.
    3.  **Le Récepteur (Le contrôleur)** : Coder la boucle métier qui enrobe l'exécution dangereuse dans une combinaison protectrice de `try / catch / finally`.

## 1. La Hiérarchie des Malheurs (Custom Exceptions)

Il est essentiel de créer un arbre généalogique d'Exceptions. De cette façon on pourra attraper soit un problème hyper spécifique, soit la racine pour tout choper d'un coup.

```php
<?php
declare(strict_types=1);

// L'Arbre des Erreurs de notre Module
class FileException extends Exception {}

// Les Branches hyper spécifiques
class FileNotFoundException extends FileException {}
class FileNotReadableException extends FileException {}
class FileNotWritableException extends FileException {}
class DirectoryNotWritableException extends FileException {}
?>
```

## 2. Le Manipulateur de Fichiers (La Zone Dangereuse)

Cette classe n'avertit jamais l'utilisateur de l'interface Front-End. Si elle souffre, elle crie (`throw`) sa douleur sous forme d'Objet Exception.

```php
<?php
declare(strict_types=1);

class FileManager {
    
    public function read(string $path): string {
        // 1. Dégainer l'Exception si introuvable
        if (!file_exists($path)) {
            throw new FileNotFoundException("🚨 Le fichier est introuvable au chemin : $path");
        }
        
        // 2. Dégainer si droits UNIX insuffisants (chmod 000)
        if (!is_readable($path)) {
            throw new FileNotReadableException("🔒 Le fichier n'est pas lisible : $path");
        }
        
        // Exécution de la fonction native
        $content = file_get_contents($path);
        
        // 3. File Exception générique (Problème bas niveau inattendu)
        if ($content === false) {
            throw new FileException("🔥 Crash IO lors de la lecture de : $path");
        }
        
        return $content;
    }
    
    public function write(string $path, string $content): void {
        $directory = dirname($path);
        
        // Création conditionnelle si le dossier parent manque
        if (!is_dir($directory)) {
            if (!mkdir($directory, 0755, true)) {
                // Impossible de créer le dossier (Pas les droits sur le serveur !!)
                throw new DirectoryNotWritableException("❌ Impossible de forger le dossier parent : $directory");
            }
        }
        
        if (file_exists($path) && !is_writable($path)) {
            throw new FileNotWritableException("❌ Fichier en lecture-seule, modification interdite : $path");
        }
        
        if (file_put_contents($path, $content) === false) {
            throw new FileException("🔥 Crash IO lors de l'écriture dans : $path");
        }
    }
    
    // ... D'autres méthodes (delete, copy) suivant exactement le même pattern.
}
?>
```

## 3. L'Interface de l'Utilisateur (La Gestion des Crises)

C'est ici que l'on manipule la Zone Dangereuse. On s'équipe du scaphandre `try/catch`. 
*Note importante : L'Ordre des Catch est crucial. Du plus spécifique au plus global.*

```php
<?php
// On inclut les Exceptions et la Classe
require_once 'FileManager.php';

$fileManager = new FileManager();

echo "<h3>Tentative de Manipulation Disque Dur</h3>";

try {
    
    // 💀 LA ZONE DE DANGER MAGMAFIIÉE 💀
    // ==================================
    $fileManager->write('documents/factures/client-709.txt', 'Facture Payée : 500€');
    echo "<p>✅ Écriture Validée.</p>";
    
    // On essaie de lire un fichier qui n'existe pas du tout.
    $lecture = $fileManager->read('documents/factures/client-404-fantome.txt');
    echo "<p>Lecture : $lecture</p>"; // Cette ligne ne sera JAMAIS exécutée !
    // ==================================
    
} catch (FileNotFoundException $e) {
    // Si c'est juste "Introuvable", on peut formater un message gentil au visiteur.
    echo "<div style='color:orange;'>⚠️ Oups : " . $e->getMessage() . "</div>";
    
} catch (DirectoryNotWritableException $e) {
    // Si c'est un soucis de droit d'écriture, c'est grave, appel à l'Admin.
    echo "<div style='color:red;'>🚨 ALERTE PERMISSIONS SERVEUR : " . $e->getMessage() . "</div>";
    
} catch (FileException $e) {
    // Le filet de sécurité final de notre module (Couvre TOUTES ses sous-exceptions si elles ont traversé les autres filtres)
    echo "<div style='color:darkred;'>🔥 ERREUR FATALE FICHIER : " . $e->getMessage() . "</div>";
    
} catch (Exception $e) {
    // Le Paravent Global Absolu (L'Exception Divine Native PHP de laquelle tout découle)
    // S'il se passe n'importe quoi d'autre (Base de donnée qui crash sans rapport)
    echo "<div style='color:black; background:red; color:white;'>💥 APOCALYPSE SYSTÈME : " . $e->getMessage() . "</div>";
}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Comprendre que la Ligne 18 : <code>echo "Lecture : $lecture"</code> ne s'exécute pas est la clé des Exceptions. Au moment précis où <code>read()</code> a crié <code>throw new</code>, le moteur PHP fait exploser la boule de feu. L'exécution de la zone s'arrête instantanément, la boule de feu remonte à travers le code jusqu'à se fracasser sur le rempart du premier <code>Catch</code> qui correspond à son nom.</p>
</div>
