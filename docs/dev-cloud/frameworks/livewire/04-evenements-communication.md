---
description: "Communication inter-composants dans Livewire v4 : dispatching d'événements, écouteurs, attributs #[On] et intégration avec les événements du navigateur (JavaScript)."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "EVENEMENTS", "COMMUNICATION"]
---

# Événements & Communication

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire à 🔴 Avancé"
  data-version="4.x"
  data-time="2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Système d'Interphone dans un Immeuble"
    Imaginez un grand immeuble résidentiel (votre page web) abritant plusieurs appartements (vos composants Livewire indépendants). Si l'habitant du troisième étage (le panier d'achat) veut signaler à la loge du gardien (le compteur de la barre de navigation) qu'un colis vient d'être déposé, il n'a pas besoin de descendre l'escalier en courant ni de passer par les canalisations. Il utilise l'interphone (le système d'événements de Livewire) pour envoyer un message vocal (un événement dispatché) sur la ligne commune. La loge du gardien, qui est branchée sur cette ligne (écoute l'événement), reçoit le message et met à jour son registre (son affichage) instantanément.

Ce module présente les mécanismes de communication asynchrones entre les différents composants mono-fichiers de Livewire v4.

<br>

---

## 1. Dispatcher des Événements avec `$dispatch`

Pour transmettre une information à un autre composant de la même page sans lien de parenté direct, vous devez dispatcher un événement.

### Exemple de composant émetteur

```html title="Blade - resources/views/livewire/⚡add-to-cart.blade.php : dispatching d'événements"
<?php
use Livewire\Component;

new class extends Component {
    public $productId = 101;

    public function addToCart()
    {
        // Traitement de l'ajout
        // ...

        // Dispatch de l'événement avec des données jointes
        $this->dispatch('item-added', productId: $this->productId);
    }
};
?>

<div class="p-4 bg-white rounded shadow flex justify-between items-center">
    <span>Produit Pro #101</span>
    <button wire:click="addToCart" class="bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700">
        Ajouter au panier
    </button>
</div>
```
_Déclenchement et envoi d'un événement global avec paramètres depuis un composant mono-fichier._

<br>

---

## 2. Écouter des Événements avec l'Attribut `#[On]`

Pour capter un événement émis sur la page, Livewire v4 utilise des attributs PHP natifs directement positionnés au-dessus des méthodes réactives de la classe.

### Exemple de composant récepteur

```html title="Blade - resources/views/livewire/⚡cart-counter.blade.php : écoute d'événements"
<?php
use Livewire\Component;
use Livewire\Attributes\On; // Importation obligatoire de l'attribut On

new class extends Component {
    public $count = 0;

    // Attribut déclenchant la méthode à la réception de l'événement
    #[On('item-added')]
    public function incrementCount($productId)
    {
        // Incrémente le compteur global du panier
        $this->count++;
    }
};
?>

<div class="bg-slate-800 text-white px-4 py-2 rounded flex items-center gap-2">
    <span>🛒 Mon Panier :</span>
    <span class="bg-blue-550 text-white rounded-full px-2 py-0.5 text-xs font-bold">
        {{ $count }}
    </span>
</div>
```
_Réception de l'événement et mise à jour automatique de l'affichage à l'aide de l'attribut de méthode #[On]._

<br>

---

## 3. Communication avec le Navigateur (JavaScript)

Vous pouvez utiliser les événements de Livewire pour envoyer des instructions directement au code JavaScript ou aux directives Alpine.js s'exécutant sur le navigateur de l'utilisateur.

### Dispatcher un événement vers le navigateur

```html title="Blade - resources/views/livewire/⚡toast-notification.blade.php : événement navigateur"
<?php
use Livewire\Component;

new class extends Component {
    public function triggerAlert()
    {
        // Envoi d'un événement capté par le DOM JavaScript global
        $this->dispatch('show-toast', message: 'Opération effectuée avec succès !');
    }
};
?>

<div class="p-4 bg-slate-100 rounded">
    <button wire:click="triggerAlert" class="bg-slate-800 text-white px-4 py-2 rounded">
        Afficher la notification
    </button>
    
    <!-- Alpine.js écoute l'événement Livewire global et affiche une alerte -->
    <div x-data="{ show: false, text: '' }" 
         @show-toast.window="show = true; text = $event.detail.message; setTimeout(() => show = false, 3000)"
         x-show="show"
         x-transition
         class="fixed bottom-4 right-4 bg-green-500 text-white p-3 rounded shadow-lg"
         style="display: none;">
        <span x-text="text"></span>
    </div>
</div>
```
_Pont de communication asynchrone entre la logique PHP et les directives d'affichage interactives d'Alpine.js._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Émetteur de notifications système**

1. Créez un composant mono-fichier `⚡event-trigger.blade.php` doté d'un bouton.
2. Au clic sur le bouton, dispatchez un événement global `system-status` avec une propriété `online = true`.
3. Créez un second composant `⚡event-listener.blade.php` qui écoute cet événement et affiche un voyant vert ou rouge en fonction de la valeur reçue.

**Exercice 2 — Fermeture automatique d'une modale**

1. Créez un composant de formulaire réactif de saisie de profil dans une modale Alpine.js.
2. Lorsque la sauvegarde PHP réussit, dispatchez un événement `profile-saved` vers le navigateur.
3. Utilisez la directive Alpine `@profile-saved.window="open = false"` pour fermer automatiquement la modale.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La communication asynchrone entre les composants Livewire v4 repose sur le système d'événements : `$this->dispatch()` pour envoyer un message global, et l'attribut de classe `#[On('nom-evenement')]` pour intercepter les messages. Le couplage avec JavaScript s'effectue simplement en écoutant les événements au niveau de l'objet global `window` à l'aide des directives Alpine.js (ex: `@nom-evenement.window`).

> Pour gérer les transferts de fichiers en streaming et préparer le déploiement en production, passez au **[Module 5 — Avancé & Production](./05-avance-production.md)**.
