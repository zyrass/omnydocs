---
description: "Upload de fichiers physiques, Polling temporels et les optimisations finales Livewire."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "UPLOADS", "PRODUCTION"]
---

# Uploads, Temps et Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Livewire 3.x"
  data-time="3 Heures">
</div>

!!! quote "Gérer le Lourd et le Réseaux"
    Pour être un développeur qualifié, savoir afficher un texte dynamique est insuffisant. Devez-vous uploader des avatars d'utilisateurs JPG de 5 Mo dans un Bucket Amazon S3 AWS ? Souhaitez-vous afficher des tableaux de bords analytiques qui se mettent visuellement à jour toutes les 10 secondes sans refresh `F5` pour de la supervision industrielle ? Il faut attaquer les APIs Avancées. 

<br>

---

## 1. La Tempête des Uploads Fichiers

Envoyer un document PDF lourd (Upload) a toujours été le cauchemar historique du développement Asynchrone AJAX en VanillaJs (`FormData()`, `Boundary`, Multi-Part...). Livewire résout cela brillamment en utilisant son trait spécial `WithFileUploads`.

```php title="app/Livewire/ProfileAvatarUploader.php"
<?php

namespace App\Livewire;

use Livewire\Component;
// 1. INJECTION OBLIGATOIRE DU TRAIT LIVEWIRE 
use Livewire\WithFileUploads; 

class ProfileAvatarUploader extends Component
{
    use WithFileUploads;

    // L'attribut physique va s'encapsuler dans cet objet mémoire temporaire réseau
    public $photo;

    public function save()
    {
        // 2. Validation native Laravel sur le poids (1024kb = 1mo)
        $this->validate([
            'photo' => 'image|max:1024', 
        ]);

        // 3. Stockage Sécurisé directement sur un Cloud / Disque réseau physique ! 
        // Generera un string Hashe indécodable.jpg dans le rep local /storage/app/public/avatars/
        $path = $this->photo->store('avatars', 'public');
        
        auth()->user()->update(['avatar_url' => $path]);
    }
}
```

```html title="Vue Blade avec Aperçu en Temps Réel"
<form wire:submit="save">
    <!-- Un File input natif, intercepté silencieusement -->
    <input type="file" wire:model="photo">

    <!-- Aperçu Magique Temporaire !
         (Si l'upload dans le navigateur est fini mais pas encore sauvegardé BD !) -->
    @if ($photo)
        Photo Selectionnée:
        <img src="{{ $photo->temporaryUrl() }}" width="100">
    @endif

    <button type="submit">Sauvegarder</button>

    <!-- La Directive loading s'applique aussi sur les fichiers pour une Jauge -->
    <div wire:loading wire:target="photo">Envoi de la photo vers le cloud...</div>
</form>
```

_Le workflow est majestueux : Lors de la sélection d'un fichier via le sélecteur Windows/Mac, Livewire contacte secrètement une route spéciale de l'API Laravel, encode votre fichier par petits Chunk, le stocke dans un dossier `/tmp`, vous fournit la preview (TemporaryUrl) et attend votre clic de confirmation final ! C'est ce qu'on appelle de l'Ingénierie Réseau pure._

<br>

---

## 2. Le Maître du Temps : wire:poll

Imaginez que vous deviez surveiller l'état d'un Serveur Minecraft. Comment afficher si plus de gens le rejoignent sans jamais obliger la secrétaire utilisant le portail web à cliquer sur `F5` pour rafraîchir ?

Au lieu d'implémenter des usines à gaz de Sockets Node.js (`Socket.io`), utilisez le polling.

```html title="Actualisation Cron Network automatique"
<!-- Ce composant va silencieusement "Mount()" et "Render()" en arrière-plan toutes les 5 Secondes de la vie du Navigateur ! -->
<div wire:poll.5s class="server-status">
    Statut actuel : {{ $etatDuServeurMinecraftBDD }}
    Joueurs simultanés: {{ $nombreDePlayersMySQL }}
</div>

<!-- Option Avancée : Ne s'active que si la fenêtre WEB de l'utilisateur est visible (Évite de drainer le serveur d'OmnyDocs si l'usager a réduit le site dans la barre de tâches en partant manger !) -->
<div wire:poll.visible.15s>
    Graphique de ventes (Màj 15 sec)
</div>
```

<br>

---

## Conclusion et Sécurité des Requêtes 

!!! quote "Performance et Optimisation"
    Avec les Traits de cycle-vie `WithPagination` (vu sur Lab 4) et `WithFileUploads`, votre maîtrise englobe désormais le backend physique et les tables des réseaux.
    Il existe tout de même un "Prix" a payer sur les "Polling" de boucle : chaque `.5s` envoie un Payload lourd réseau de 3kb à votre hébergement Web Linux, et consomme un cycle CPU sur la machine pour ouvrir la DB. Sur Internet, c'est insignifiant, mais une page surveillée par 5 000 salariés en même temps... c'est 5 000 requêtes MySQL/sec, soit la capacité d'un hébergement Cloud Lourd dédié ! D'où l'importance de `wire:poll.visible` ou l'apprentissage ultime des **WebSockets Echo**.
    
    
> Reste désormais la consécration de vos acquis à des interfaces fonctionnelles complexes. Affûtez vos claviers : [C'est l'heure du Laboratoire Livewire en attaquant le premier Projet !](../projets/livewire-lab/index.md).
