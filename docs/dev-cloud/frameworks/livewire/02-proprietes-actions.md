---
description: "Data Binding (wire:model), modificateurs de requêtes, déclenchement d'actions (wire:click) et soumission de formulaires sous format SFC Livewire v4."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "BINDING", "ACTIONS"]
---

# Propriétés & Actions

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="4.x"
  data-time="2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Neurotransmetteurs et le Réseau Nerveux"
    Dans le corps humain, les récepteurs sensoriels (les champs de saisie et boutons de votre page) envoient des signaux électriques (les requêtes HTTP) par les voies nerveuses (Livewire) jusqu'au cerveau (le serveur PHP) pour déclencher une réaction musculaire (la mise à jour du HTML). Livewire v4 orchestre ce réseau nerveux de manière transparente. Chaque fois qu'un utilisateur saisit du texte ou clique sur un élément, le neurotransmetteur `wire:` transmet instantanément l'information au serveur sans bloquer le reste de l'application.

Ce module détaille la gestion de l'état réactif et le traitement des actions utilisateurs dans les composants mono-fichiers de Livewire v4.

<br>

---

## 1. La liaison de données : `wire:model`

Le Data Binding bidirectionnel permet de lier une propriété de la classe PHP à un élément de saisie HTML. Toute modification de l'un met automatiquement à jour l'autre.

### Exemple de liaison de texte simple

```html title="Blade - resources/views/livewire/⚡text-input.blade.php : liaison bidirectionnelle"
<?php
use Livewire\Component;

new class extends Component {
    public $message = 'Bonjour Zensical';
};
?>

<div class="space-y-4">
    <!-- Le champ de saisie est lié à la propriété publique $message -->
    <input type="text" wire:model="message" class="border p-2 rounded w-full">
    
    <p class="text-slate-600">Valeur actuelle : <strong>{{ $message }}</strong></p>
</div>
```
_Liaison dynamique d'un champ de texte à la propriété publique $message au sein d'un composant mono-fichier._

Par défaut, Livewire diffère l'envoi de la requête de mise à jour jusqu'à ce qu'une action (comme un clic sur un bouton) soit déclenchée, afin d'économiser de la bande passante.

<br>

---

## 2. Modificateurs de liaison réactive

Pour contrôler le comportement et la fréquence d'envoi des requêtes réseau lors de la saisie, vous devez utiliser des modificateurs spécifiques.

### Les principaux modificateurs

- `.live` : Envoie une requête réseau immédiatement à chaque caractère tapé.
- `.blur` : Met à jour la propriété uniquement lorsque l'élément perd le focus (quand l'utilisateur clique en dehors du champ).
- `.debounce.[ms]` : Retarde la mise à jour réseau (par exemple de 500 ms) pour attendre que l'utilisateur ait fini de taper.

```html title="Blade - resources/views/livewire/⚡search-box.blade.php : modificateurs réactifs"
<?php
use Livewire\Component;

new class extends Component {
    public $query = '';
};
?>

<div class="p-4 bg-slate-50 rounded-lg">
    <!-- Recherche dynamique avec un temps d'attente de 300 millisecondes -->
    <input type="search" wire:model.live.debounce.300ms="query" 
           placeholder="Rechercher..." class="border p-2 rounded w-full">
           
    <p class="mt-2 text-sm text-slate-500">Requête en cours pour : {{ $query }}</p>
</div>
```
_Mise en place d'un champ de recherche réactif limitant les requêtes serveur grâce au modificateur debounce._

<br>

---

## 3. Déclenchement d'Actions avec `wire:click`

Les actions permettent d'exécuter des méthodes définies dans la classe PHP du composant en réponse aux interactions physiques des utilisateurs.

### Exemple d'actions multiples

```html title="Blade - resources/views/livewire/⚡counter-actions.blade.php : actions réactives"
<?php
use Livewire\Component;

new class extends Component {
    public $count = 0;

    public function incrementBy($amount)
    {
        $this->count += $amount;
    }

    public function resetCounter()
    {
        $this->count = 0;
    }
};
?>

<div class="flex flex-col items-center gap-4">
    <span class="text-3xl font-bold">{{ $count }}</span>
    
    <div class="flex gap-2">
        <!-- Appel d'une méthode avec des arguments directement depuis le clic -->
        <button wire:click="incrementBy(5)" class="bg-emerald-500 text-white px-4 py-2 rounded">
            +5
        </button>
        <button wire:click="resetCounter" class="bg-rose-500 text-white px-4 py-2 rounded">
            Réinitialiser
        </button>
    </div>
</div>
```
_Déclenchement de méthodes PHP avec passage d'arguments directement depuis les boutons HTML._

<br>

---

## 4. Soumission de Formulaires sécurisée

Pour éviter la perte de données et bloquer le rafraîchissement standard de la page lors de la validation d'un formulaire, vous devez utiliser le modificateur de soumission de Livewire.

### Soumission et blocage d'action

```html title="Blade - resources/views/livewire/⚡simple-form.blade.php : soumission de formulaire"
<?php
use Livewire\Component;

new class extends Component {
    public $email = '';

    public function save()
    {
        // Traitement de l'adresse e-mail
        session()->flash('status', 'Inscription réussie avec : ' . $this->email);
        $this->reset('email');
    }
};
?>

<form wire:submit="save" class="space-y-4 max-w-sm">
    @if (session()->has('status'))
        <div class="p-3 bg-green-100 text-green-850 rounded">
            {{ session('status') }}
        </div>
    @endif

    <div>
        <label for="email" class="block text-sm font-medium">Adresse Email</label>
        <input type="email" id="email" wire:model="email" required 
               class="border p-2 rounded w-full">
    </div>

    <!-- Le bouton soumet le formulaire et déclenche la méthode PHP save() -->
    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded w-full">
        S'abonner
    </button>
</form>
```
_Soumission asynchrone sécurisée d'un formulaire empêchant le comportement par défaut du navigateur._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Création d'une zone de texte réactive**

1. Créez un composant mono-fichier `⚡bio-editor.blade.php`.
2. Ajoutez un champ `<textarea>` lié à une propriété `$bio` à l'aide de `wire:model.blur`.
3. Affichez la biographie rédigée en dessous et constatez que la mise à jour ne se fait que lorsque vous quittez la zone de saisie.

**Exercice 2 — Gestionnaire de panier d'achat**

1. Créez un composant `⚡shopping-cart.blade.php` avec une propriété `$quantity` initialisée à 1.
2. Ajoutez deux boutons pour augmenter et diminuer la quantité, reliés à une méthode PHP `updateQuantity($change)`.
3. Ajoutez une condition pour empêcher la quantité de descendre en dessous de 1.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La liaison bidirectionnelle `wire:model` permet de synchroniser les entrées utilisateur avec le code PHP, et peut être optimisée grâce aux modificateurs `.live`, `.blur` et `.debounce`. Les actions (`wire:click`, `wire:submit`) relient les événements du DOM aux méthodes PHP de votre composant mono-fichier, offrant une réactivité fluide sans rafraîchissement global.

> Pour assurer la sécurité des données et valider les saisies des utilisateurs, passez au **[Module 3 — Formulaires & Validation](./03-formulaires-validation.md)**.
