---
description: "Fonctionnalités avancées de Livewire v4 : upload de fichiers en streaming, polling, sécurité CSRF, smart keys et checklist pour la mise en production."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "PRODUCTION", "UPLOADS", "POLLING"]
---

# Avancé & Production

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="4.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Décollage de la Fusée et le Centre de Contrôle"
    Développer une application en local, c'est comme concevoir une fusée dans un hangar sécurisé : vous pouvez tester les moteurs, vérifier les cadrans et ajuster les pièces sans aucun risque extérieur. La mise en production est le moment du décollage réel vers l'espace (le Web public). Le centre de contrôle (votre configuration de production) doit veiller à ce que la fusée résiste aux frottements de l'atmosphère (les attaques de sécurité), gère correctement le carburant (les uploads lourds) et maintienne une liaison de télémétrie stable (le polling et le suivi des composants). Sans cette préparation rigoureuse, la fusée risque de perdre le contact à mi-chemin.

Ce module présente les concepts de production et les fonctionnalités avancées de Livewire v4.x sous format mono-fichier.

<br>

---

## 1. Upload de Fichiers en Streaming avec `WithFileUploads`

Livewire gère le transfert de fichiers en créant un flux temporaire sécurisé vers le serveur, évitant de surcharger la mémoire lors du traitement de gros volumes.

### Exemple de formulaire d'upload

```html title="Blade - resources/views/livewire/⚡file-uploader.blade.php : upload de fichiers"
<?php
use Livewire\Component;
use Livewire\WithFileUploads; // Trait requis pour activer le streaming de fichiers

new class extends Component {
    use WithFileUploads;

    public $photo;

    protected $rules = [
        'photo' => 'image|max:1024', // Limitation à 1 Mo
    ];

    public function upload()
    {
        $this->validate();

        // Sauvegarde de l'image dans le dossier de stockage 'photos' privé
        $path = $this->photo->store('photos');

        session()->flash('status', 'Fichier enregistré avec succès sous : ' . $path);
    }
};
?>

<form wire:submit="upload" class="p-6 bg-white rounded-lg shadow-md max-w-sm">
    @if (session()->has('status'))
        <div class="p-3 bg-green-100 text-green-800 rounded text-sm mb-4">
            {{ session('status') }}
        </div>
    @endif

    <div class="space-y-4">
        <label class="block text-sm font-medium">Charger une photo (Max 1Mo)</label>
        <input type="file" wire:model="photo" class="block w-full text-sm text-slate-500">
        
        @error('photo') 
            <span class="text-rose-500 text-xs block">{{ $message }}</span> 
        @enderror

        <!-- Zone de prévisualisation temporaire générée par Livewire -->
        @if ($photo)
            <div class="mt-4">
                <span class="text-xs text-slate-500 block mb-1">Prévisualisation :</span>
                <img src="{{ $photo->temporaryUrl() }}" class="w-32 h-32 object-cover rounded border">
            </div>
        @endif

        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded w-full">
            Téléverser l'image
        </button>
    </div>
</form>
```
_Formulaire mono-fichier gérant le téléversement progressif et la prévisualisation asynchrone d'une image._

<br>

---

## 2. Actualisation Régulière Automatique : `wire:poll`

Le mécanisme de polling permet de demander à Livewire de rafraîchir le composant à intervalles réguliers (par exemple toutes les 5 secondes) pour afficher des données fraîches sans aucune action de l'utilisateur.

### Exemple de suivi de statut

```html title="Blade - resources/views/livewire/⚡status-tracker.blade.php : rafraîchissement asynchrone"
<?php
use Livewire\Component;
use App\Models\Server;

new class extends Component {
    public function getStatus()
    {
        // Retourne le statut mis à jour
        return rand(1, 2) === 1 ? 'Actif' : 'Maintenance';
    }
};
?>

<!-- Le composant se met à jour automatiquement toutes les 5 secondes -->
<div wire:poll.5s class="p-4 bg-slate-800 text-white rounded flex items-center justify-between">
    <span>🖥️ Statut du serveur :</span>
    <span class="px-2 py-0.5 rounded text-xs font-bold bg-green-550">
        {{ $this->getStatus() }}
    </span>
</div>
```
_Mise à jour à chaud périodique du composant via le mécanisme de polling de Livewire._

<br>

---

## 3. Sécurité et Checklist de Production

Lors de la mise en ligne de vos composants Livewire v4, plusieurs règles de sécurité et de performances doivent être appliquées.

### Sécurité CSRF et validation stricte

Livewire inclut par défaut une protection contre les attaques de type Cross-Site Request Forgery (CSRF). À chaque requête asynchrone, un jeton de session est validé par le middleware de Laravel.

- **Smart Keys actives par défaut :** Livewire v4 active la configuration `smart_wire_keys` par défaut. Cela garantit que chaque élément du DOM au sein de boucles complexes (`@foreach`) possède une clé unique de suivi (`wire:key`), évitant les corruptions d'état et les injections lors de mises à jour croisées.
- **Désactiver le mode débogage :** Dans votre fichier `.env` de production, assurez-vous que `APP_DEBUG=false` et que `DEBUGBAR_ENABLED=false` sont bien configurés pour éviter la divulgation d'informations sensibles (clés d'API, structures de tables) en cas d'erreur.

```env title="Configuration - .env : configuration de production"
APP_ENV=production
APP_DEBUG=false
```
_Définition de l'environnement de production pour verrouiller la journalisation et interdire l'affichage des traces d'erreurs en clair._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Uploader de documents de sécurité**

1. Créez un composant mono-fichier `⚡document-vault.blade.php`.
2. Ajoutez une validation limitant le type de fichier au format PDF uniquement (`'document' => 'mimes:pdf|max:2048'`).
3. Enregistrez le document dans un sous-dossier privé du disque de stockage de votre projet.

**Exercice 2 — Panneau d'administration dynamique**

1. Créez un composant de dashboard qui affiche le nombre de commandes en cours.
2. Ajoutez une mise à jour régulière toutes les 10 secondes à l'aide de `wire:poll.10s`.
3. Vérifiez dans l'inspecteur réseau que les appels réseau se déclenchent régulièrement sans rafraîchir le reste de la page.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les uploads de fichiers s'effectuent de manière asynchrone grâce à l'utilisation du trait `WithFileUploads` et à la génération de chemins temporaires d'affichage (`temporaryUrl`). Le polling (`wire:poll`) permet de maintenir l'interface à jour automatiquement par cycles réguliers. Enfin, la mise en production requiert de verrouiller le mode débogage (`APP_DEBUG=false`) et de s'assurer de la présence systématique des clés d'identification des éléments (`wire:key`).

> La formation Livewire v4 est maintenant terminée. Pour découvrir la gestion globale de l'interactivité client côté navigateur, passez à la **[formation Alpine.js](../alpine/index.md)**.
