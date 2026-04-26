---
description: "Projet 1 : Créer une calculatrice interactive avec data binding bidirectionnel."
icon: lucide/calculator
tags: ["PROJET", "LIVEWIRE", "BASES", "DATA-BINDING"]
---

# Calculatrice Interactive

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Les Fondations de la Réactivité"
    Bienvenue dans le premier projet du Lab Livewire. L'objectif ici est de comprendre comment une simple classe PHP peut contrôler une vue Blade instantanément sans nécessiter une ligne de JavaScript. La calculatrice est l'exercice parfait : elle demande de l'état (les deux nombres, l'opérateur) et des actions déclenchées par l'utilisateur (le clic sur le bouton "Égal").

<br>

![Livewire Calculator Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_calculator_1775233216679.png)
<p><em>Maquette UI conceptuelle du projet : Calculatrice moderne avec binding instantané.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- **Saisir deux nombres** dans des champs textes.
- **Sélectionner un opérateur** (+, -, *, /) via un menu déroulant ou des boutons.
- **Afficher le résultat** réactivement sans rechargement de page.
- **Sauvegarder un historique** de calculs sous la calculatrice.

### Concepts Livewire déployés
- `wire:model` : Liaison bidirectionnelle des champs inputs vers les propriétés PHP.
- `wire:click` : Déclenchement d'une méthode de classe PHP depuis un bouton HTML.
- Propriétés publiques : Le cœur de l'état du composant.

<br>

---

## 2. Le Modèle PHP

Voici la classe qui gère toute la logique pure (le "Cerveau"). Remarquez comme c'est du pur code PHP classique, étendu par `Component`.

```php title="app/Livewire/Calculator.php"
<?php

namespace App\Livewire;

use Livewire\Component;

class Calculator extends Component
{
    // C'est l'État Local de notre composant (State)
    public $number1 = 0;
    public $number2 = 0;
    public $operator = '+';
    public $result = 0;
    public $history = []; // Un tableau pour garder une trace

    // La méthode déclenchée par le clic utilisateur
    public function calculate()
    {
        // Validation basique instantanée !
        if ($this->operator === '/' && $this->number2 == 0) {
            $this->result = "Erreur: Division par 0";
            return;
        }

        switch ($this->operator) {
            case '+': $this->result = $this->number1 + $this->number2; break;
            case '-': $this->result = $this->number1 - $this->number2; break;
            case '*': $this->result = $this->number1 * $this->number2; break;
            case '/': $this->result = $this->number1 / $this->number2; break;
        }

        // On push dans le tableau de l'historique
        $this->history[] = "{$this->number1} {$this->operator} {$this->number2} = {$this->result}";
    }

    public function render()
    {
        // On retourne la vue HTML associée
        return view('livewire.calculator');
    }
}
```

_Toute propriété déclarée `public` est **automatiquement disponible** dans le fichier de vue Blade, et modifiable depuis l'interface client de manière sécurisée._

<br>

---

## 3. La Vue Blade

La vue prend les commandes magiques de Livewire pour raccorder les composants visuels à notre fameuse classe PHP.

```html title="resources/views/livewire/calculator.blade.php"
<div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg border border-gray-100">
    
    <h2 class="text-2xl font-bold text-gray-800 text-center mb-6">Calculatrice Livewire</h2>

    <!-- wire:model connecte l'input à la variable publique PHP $number1 -->
    <div class="flex space-x-4 mb-4">
        <input type="number" wire:model="number1" class="w-full border p-2 rounded">
        
        <select wire:model="operator" class="border p-2 rounded bg-gray-50">
            <option value="+">+</option>
            <option value="-">-</option>
            <option value="*">x</option>
            <option value="/">/</option>
        </select>
        
        <input type="number" wire:model="number2" class="w-full border p-2 rounded">
    </div>

    <!-- wire:click invoque la méthode 'calculate' PHP en mode asynchrone (AJAX) -->
    <button wire:click="calculate" 
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded mb-6 transition-colors shadow">
        Calculer
    </button>

    <div class="bg-blue-50 text-blue-800 text-2xl font-black text-center py-4 rounded mb-6">
        Résultat : {{ $result }}
    </div>

    <!-- @foreach natif de Laravel Blade -->
    @if(count($history) > 0)
    <div class="border-t pt-4 text-sm text-gray-500">
        <h4 class="font-bold mb-2 uppercase text-xs">Historique</h4>
        <ul>
            @foreach($history as $item)
                <li class="border-b py-1">{{ $item }}</li>
            @endforeach
        </ul>
    </div>
    @endif
</div>
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Cette calculatrice illustre la magie de Livewire : une interaction fluide en temps réel côté client, entièrement pilotée par une logique backend robuste en PHP, sans avoir à écrire et maintenir du Javascript.

!!! quote "Récapitulatif"
    C'est aussi simple que cela. Sans aucune configuration d'API, d'Axios ou de JavaScript, nous avons conçu un outil qui gère des interactions de manière fluide. Livewire se charge d'envoyer la demande chiffrée, de récupérer la réponse, et de mettre à jour le DOM HTML là où il le faut de manière quasi imperceptible.
    
> Passons à l'étape supérieure où nous validerons de la donnée entrante en temps réel sans devoir recharger la page. Rendez-vous dans le [Projet 2 : Inscription et Validation](./02-inscription-validation.md).
