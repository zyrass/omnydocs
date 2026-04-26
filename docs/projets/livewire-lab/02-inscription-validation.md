---
description: "Projet 2 : Créer un formulaire d'inscription avec validation dynamique temps réel."
icon: lucide/user-plus
tags: ["PROJET", "LIVEWIRE", "FORMULAIRES", "VALIDATION", "UX"]
---

# Inscription et Validation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "La Magie de l'Expérience Utilisateur (UX)"
    Rien de pire qu'un utilisateur qui passe cinq minutes à remplir un formulaire, clique sur "Valider" et voit la page se recharger pour lui afficher une erreur obscure "Votre mot de passe doit faire 8 caractères". Ce temps est révolu. Dans ce second projet, nous allons créer un formulaire d'inscription qui valide chaque lettre saisie en temps réel (Real-Time Validation), grâce à l'énorme puissance de validation locale de Laravel.

<br>

![Livewire Signup Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_signup_1775233233507.png)
<p><em>Maquette UI conceptuelle du projet : Validation des entrées textuelles instantanée.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- Un formulaire de profil avec **Nom**, **Email**, et **Mot de Passe**.
- Si l'email est déjà utilisé dans la Base de Données, une pastille rouge d'erreur surgit avant même l'envoi.
- Si le mot de passe est trop faible, une recommandation s'affiche en temps réel.
- Le bouton de soumission doit s'adapter (bloqué si invalide, état de chargement lors de l'envoi).

### Concepts Livewire déployés
- Les attributs (Attributes) PHP `#[\Validate]` ou `$rules`.
- Le modifier `wire:model.live` (pour vérifier à chaque frappe) ou `.blur` (pour vérifier lors de la désélection d'un champ).
- L'injection du trait `WithValidation`.

<br>

---

## 2. Le Modèle PHP avec Attributs de Validation

Livewire 3 introduit une syntaxe divine pour valider les données sans efforts : les Attributs natifs de PHP 8.

```php title="app/Livewire/RegistrationForm.php"
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\Validate;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class RegistrationForm extends Component
{
    // On lie directement les règles de validation Laravel au-dessus de la variable !
    #[Validate('required|min:3', message: 'Le nom est trop court')]
    public $name = '';

    // unique:users vérifie en base de données de manière asynchrone
    #[Validate('required|email|unique:users,email')]
    public $email = '';

    #[Validate('required|min:8', message: 'Il faut 8 caractères dont une majuscule.')]
    public $password = '';

    public bool $isSuccess = false;

    public function register()
    {
        // En cas d'erreur de règle définie ci-dessus, le code s'arrête net ici et Livewire renvoie les erreurs à Blade.
        $this->validate();

        // Si tout est bon, on interagit réellement avec l'ORM (Eloquent)
        User::create([
            'name' => $this->name,
            'email' => $this->email,
            'password' => Hash::make($this->password),
        ]);

        $this->isSuccess = true;
        // Optionnel : $this->reset('name', 'email', 'password');
    }

    public function render()
    {
        return view('livewire.registration-form');
    }
}
```

_Le secret de Livewire est que sa validation repose à 100% sur un système natif Laravel. Vous utilisez le même lexique, les mêmes sécurités, avec la rapidité des SPAs JS._

<br>

---

## 3. La Vue Blade avec Indication Visuelle d'Erreurs

Maintenant que le back-end est sécurisé, il faut rendre l'expérience agréable sans avoir besoin d'un lourd script Javascript client pour jongler avec des regex.

```html title="resources/views/livewire/registration-form.blade.php"
<div class="max-w-lg mx-auto bg-white p-8 rounded shadow-md mt-10">

    <!-- État de réussite total -->
    @if($isSuccess)
    <div class="bg-green-100 text-green-800 p-4 rounded mb-6 border border-green-200">
        Bienvenue ! Votre compte est créé.
    </div>
    @else
    
    <form wire:submit="register">
        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">Nom</label>
            <!-- .blur déclenche l'aller/retour réseau *uniquement* lorsque l'usager quitte le focus du champ -->
            <input type="text" wire:model.blur="name" 
                   class="w-full border p-2 rounded @error('name') border-red-500 bg-red-50 @enderror">
            
            <!-- @error capte le problème pour le nom -->
            @error('name') 
                <span class="text-sm text-red-500 font-semibold">{{ $message }}</span> 
            @enderror
        </div>

        <div class="mb-4">
            <label class="block text-gray-700 font-bold mb-2">Adresse Email</label>
            <!-- .live forcerait une vérification réseau à chaque lettre frappée ! Optionnel, mais lourd -->
            <input type="email" wire:model.blur="email" 
                   class="w-full border p-2 rounded @error('email') border-red-500 bg-red-50 @enderror">
            
            @error('email') 
                <span class="text-sm text-red-500 font-semibold">{{ $message }}</span> 
            @enderror
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-bold mb-2">Mot de Passe Sécurisé</label>
            <input type="password" wire:model.live="password" 
                   class="w-full border p-2 rounded @error('password') border-red-500 @enderror">
            
            @error('password') 
                <span class="text-sm text-red-500 font-semibold">{{ $message }}</span> 
            @enderror
        </div>

        <!-- wire:loading est un helper masqué magique pour indiquer visuellement le travail en fond -->
        <button type="submit" 
                class="w-full bg-indigo-600 text-white p-3 rounded font-bold hover:bg-indigo-700 flex justify-center">
            
            <span wire:loading.remove>Créer mon compte</span>
            
            <!-- Affiché UNIQUEMENT pendant que le serveur travaille -->
            <span wire:loading class="animate-pulse">Vérifications en cours...</span>
        </button>
    </form>
    
    @endif
</div>
```

<br>

---

## Conclusion

!!! quote "Les Modifieurs"
    C'est la différence entre `.live`, `.blur` et rien du tout (`wire:model` traditionnel) qui signe la compétence réelle d'un développeur Livewire. Appeler le serveur à chaque lettre tapée `.live` doit être réservé à un besoin crucial local (comme la barre verte d'un mot de passe complexe). Souvent, utiliser `.blur` évite la surcharge réseau en n'effectuant la validation qu'en fin de frappe.
    
> Vous savez désormais capter la donnée, et surtout la contraindre. Il est temps d'intégrer dans le DOM une liste qui s'ajoute, s'efface et persiste : rendez-vous dans le [Projet 3 : Todo List Récative](./03-todo-list.md).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
