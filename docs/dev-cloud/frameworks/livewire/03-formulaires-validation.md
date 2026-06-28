---
description: "Validation de formulaires en temps réel, règles de validation et gestion des messages d'erreur au sein de composants mono-fichiers Livewire v4."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "VALIDATION", "FORMULAIRES"]
---

# Formulaires & Validation

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="4.x"
  data-time="2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Douanier et le Contrôle de Sécurité"
    Imaginez un voyageur (les données soumises par l'utilisateur) se présentant à la frontière (votre serveur applicatif). Le douanier (le système de validation) vérifie méthodiquement son passeport, son visa et ses bagages en les confrontant aux lois nationales (vos règles de validation) avant de l'autoriser à entrer sur le territoire. Si un document manque ou est invalide, le douanier refuse l'accès et signale immédiatement le problème au voyageur pour qu'il le corrige. Dans Livewire v4, ce contrôle de sécurité s'effectue en temps réel, bloquant les entrées frauduleuses avant même qu'elles n'atteignent votre base de données.

Ce module présente les mécanismes de validation robustes de Livewire v4 et leur intégration dans les formulaires mono-fichiers.

<br>

---

## 1. Règles de validation de base

Pour protéger l'intégrité de votre application, toute donnée saisie par l'utilisateur doit être validée côté serveur avant d'être persistée en base de données.

### Exemple de validation à la soumission

```html title="Blade - resources/views/livewire/⚡register-form.blade.php : formulaire de base validé"
<?php
use Livewire\Component;

new class extends Component {
    public $name = '';
    public $email = '';

    // Définition des règles de validation
    protected $rules = [
        'name' => 'required|min:3',
        'email' => 'required|email|unique:users,email',
    ];

    public function submit()
    {
        // Exécute la validation en se basant sur les règles $rules
        $this->validate();

        // Si la validation réussit, traitement de l'enregistrement
        session()->flash('success', 'Utilisateur validé et enregistré.');
    }
};
?>

<form wire:submit="submit" class="space-y-4 max-w-md p-6 bg-white rounded-lg shadow">
    @if (session()->has('success'))
        <div class="p-3 bg-green-150 text-green-800 rounded">
            {{ session('success') }}
        </div>
    @endif

    <div>
        <label for="name" class="block text-sm font-medium">Nom complet</label>
        <input type="text" id="name" wire:model="name" class="border p-2 rounded w-full">
        @error('name') 
            <span class="text-rose-600 text-xs mt-1 block">{{ $message }}</span> 
        @enderror
    </div>

    <div>
        <label for="email" class="block text-sm font-medium">Adresse Email</label>
        <input type="email" id="email" wire:model="email" class="border p-2 rounded w-full">
        @error('email') 
            <span class="text-rose-600 text-xs mt-1 block">{{ $message }}</span> 
        @enderror
    </div>

    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded w-full hover:bg-blue-700">
        Enregistrer
    </button>
</form>
```
_Formulaire mono-fichier complet gérant la validation et l'affichage ciblé des erreurs à l'aide de la directive @error._

<br>

---

## 2. Validation en temps réel avec `updated`

Pour offrir une meilleure expérience utilisateur, vous pouvez valider les champs individuels dès que l'utilisateur a fini de les remplir, sans attendre la soumission finale du formulaire.

### Déclenchement de la validation au fil de l'eau

```html title="Blade - resources/views/livewire/⚡realtime-validation.blade.php : validation réactive"
<?php
use Livewire\Component;

new class extends Component {
    public $username = '';

    protected $rules = [
        'username' => 'required|alpha_dash|min:4|max:20',
    ];

    // Hook appelé automatiquement après la mise à jour d'une propriété publique
    public function updated($propertyName)
    {
        // Valide uniquement la propriété modifiée
        $this->validateOnly($propertyName);
    }

    public function save()
    {
        $this->validate();
        session()->flash('message', 'Nom d\'utilisateur réservé avec succès.');
    }
};
?>

<div class="space-y-4 max-w-sm">
    <div>
        <label for="username" class="block text-sm font-medium">Nom d'utilisateur</label>
        <!-- Utilisation de wire:model.blur pour valider lorsque le focus est perdu -->
        <input type="text" id="username" wire:model.blur="username" class="border p-2 rounded w-full">
        @error('username') 
            <span class="text-rose-500 text-xs mt-1 block">{{ $message }}</span> 
        @enderror
    </div>

    <button wire:click="save" class="bg-slate-800 text-white px-4 py-2 rounded w-full">
        Créer mon compte
    </button>
</div>
```
_Validation à chaud déclenchée par le crochet cycle de vie updated lors de la modification des champs._

<br>

---

## 3. Personnalisation des Messages d'Erreur

Vous pouvez personnaliser les règles de validation et redéfinir les messages d'erreur standard de Laravel pour les adapter à votre contexte applicatif.

### Déclaration de messages personnalisés

```html title="Blade - resources/views/livewire/⚡custom-messages.blade.php : messages d'erreurs ciblés"
<?php
use Livewire\Component;

new class extends Component {
    public $password = '';

    protected $rules = [
        'password' => 'required|min:8',
    ];

    // Définition des messages d'erreur personnalisés
    protected $messages = [
        'password.required' => 'Le mot de passe ne doit pas rester vide.',
        'password.min' => 'Sécurité insuffisante : le mot de passe doit comporter au moins 8 caractères.',
    ];

    public function check()
    {
        $this->validate();
        session()->flash('status', 'Mot de passe sécurisé enregistré.');
    }
};
?>

<div class="space-y-4 max-w-sm">
    <div>
        <label for="password" class="block text-sm font-medium">Mot de passe</label>
        <input type="password" id="password" wire:model="password" class="border p-2 rounded w-full">
        @error('password') 
            <span class="text-amber-600 text-xs mt-1 block font-semibold">{{ $message }}</span> 
        @enderror
    </div>

    <button wire:click="check" class="bg-indigo-600 text-white px-4 py-2 rounded w-full">
        Valider la sécurité
    </button>
</div>
```
_Définition de messages d'erreur explicites pour guider l'utilisateur lors de la saisie d'informations complexes._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Validateur de longueur de texte**

1. Créez un composant mono-fichier `⚡tweet-box.blade.php`.
2. Ajoutez un champ de saisie limité par une règle de validation `max:140`.
3. Affichez en temps réel un compteur de caractères restants et le message d'erreur de dépassement dès que la limite est franchie.

**Exercice 2 — Formulaire de mot de passe avec confirmation**

1. Créez un composant `⚡password-match.blade.php` avec deux propriétés `$password` et `$password_confirmation`.
2. Déclarez les règles de validation correspondantes à l'aide de la règle Laravel `confirmed` (ex: `'password' => 'required|confirmed'`).
3. Validez l'affichage et le masquage des erreurs d'incohérence à chaque saisie.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La validation dans Livewire v4 repose sur la déclaration de la propriété `$rules` et l'appel à `$this->validate()`. La validation en temps réel s'effectue simplement en surchargeant le crochet de cycle de vie `updated()` avec la méthode `$this->validateOnly()`. La directive Blade `@error` permet d'afficher des retours ciblés et interactifs aux utilisateurs en cas d'erreurs de saisie.

> Pour déclencher des actions entre plusieurs composants indépendants de votre page, passez au **[Module 4 — Événements & Communication](./04-evenements-communication.md)**.
