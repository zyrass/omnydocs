---
description: "Projet 3 : Créer une Todo List Réactive complète avec Eloquent ORM."
icon: lucide/check-square
tags: ["PROJET", "LIVEWIRE", "CRUD", "ELOQUENT"]
---

# Todo List Réactive

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>

!!! quote "Gérer le Modèle Dynamique"
    Maintenant que nous savons envoyer des données propres (avec la validation du Projet 2), il est indispensable d'apprendre à les lister et à les altérer dynamiquement sans clignotement. La "Todo List" est le point de conjonction où *l'affichage du DOM*, *la mutation Livewire* et *le système Eloquent (Base de Données)* s'entremêlent intimement. 

<br>

![Livewire Todo List Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_todolist_1775233249017.png)
<p><em>Maquette UI conceptuelle du projet : Ajout, rature, et filtrage en direct de tâches en base de données.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- Un champ pour **ajouter** rapidement une nouvelle tâche en appuyant sur "Entrée".
- **Lister** dynamiquement toutes les tâches enregistrées dans MySQL.
- Une case pour **marquer** une tâche comme terminée (la raturer visuellement).
- Un bouton unique pour **supprimer** définitivement un point.
- **Bonus** : Trois boutons de filtrage (Toutes, Actives, Complétées).

### Concepts Livewire déployés
- Le cycle de rendu conditionnel avec boucle `@foreach`.
- La communication fluide avec une DB Laravel `Task::all()`.
- Typage strict sur un Model Eloquent public.

<br>

---

## 2. L'Architecture Serveur (Component)

Le secret de ce code "sans effort" repose sur l'intégration parfaite entre Livewire et le modèle natif Laravel (`App\Models\Task`). Livewire comprend l'ORM pour envoyer la liste.

```php title="app/Livewire/TodoList.php"
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Task;
use Livewire\Attributes\Validate;

class TodoList extends Component
{
    // C'est ce titre de nouvelle tâche qu'on associera au HTML
    #[Validate('required|min:3')]
    public $newTask = '';

    // État pour savoir quel filtre est actuellement sélectionné par l'usager
    public $filter = 'all'; // all, active, completed

    // Ajouter en BDD
    public function add()
    {
        $this->validate();

        Task::create([
            'title' => $this->newTask,
            'is_completed' => false
        ]);

        $this->newTask = ''; // On vide automatiquement le formulaire client HTML !
    }

    // Bascule (Toggle) l'état de la checkbox en BDD
    public function toggleComplete(Task $task)
    {
        $task->is_completed = !$task->is_completed;
        $task->save();
    }

    // Supprime la donnée définitivement
    public function delete(Task $task)
    {
        $task->delete();
    }

    // Le Getter du tableau filtré
    public function getTasksProperty()
    {
        $query = Task::query()->latest();

        if ($this->filter === 'active') {
            $query->where('is_completed', false);
        } elseif ($this->filter === 'completed') {
            $query->where('is_completed', true);
        }

        return $query->get();
    }

    public function render()
    {
        // On n'a pas besoin de passer $tasks dans un array, on utilise la Computed Property !
        return view('livewire.todo-list');
    }
}
```

_Notez l'usage brillant du Type-Hinting `public function delete(Task $task)`. Au lieu d'envoyer seulement un identifiant de type entier (id), Livewire réalise pour nous le "Route Model Binding" et instancie la magie d'Eloquent._

<br>

---

## 3. L'Interface (Vue Blade)

Une seule vue se charge d'absorber tous les événements natifs utilisateur.

```html title="resources/views/livewire/todo-list.blade.php"
<div class="max-w-xl mx-auto mt-10">
    <div class="bg-white rounded-lg shadow-xl overflow-hidden border border-gray-100">
        
        <div class="p-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Ma Liste de Tâches</h2>

            <!-- Formulaire d'ajout intercepté par Livewire au submit (ou si on presse Entrée) -->
            <form wire:submit="add" class="flex mb-6">
                <input type="text" wire:model="newTask" placeholder="Que devez-vous accomplir ?" 
                       class="flex-1 border-gray-300 rounded-l-lg border-r-0 focus:ring-1 focus:ring-blue-500">
                <button type="submit" class="bg-blue-600 text-white font-bold px-6 py-2 rounded-r-lg hover:bg-blue-700">
                    Insérer
                </button>
            </form>

            <!-- Gestion des filtres visuels -->
            <div class="flex space-x-2 text-sm text-gray-600 mb-4 border-b pb-4">
                <button wire:click="$set('filter', 'all')" 
                        class="@if($filter === 'all') font-bold text-blue-600 @endif hover:text-blue-500">
                    Toutes
                </button>
                <button wire:click="$set('filter', 'active')"
                        class="@if($filter === 'active') font-bold text-blue-600 @endif hover:text-blue-500">
                    En cours
                </button>
                <button wire:click="$set('filter', 'completed')"
                        class="@if($filter === 'completed') font-bold text-blue-600 @endif hover:text-blue-500">
                    Originales
                </button>
            </div>

            <!-- Boucle de Rendu. Livewire utilise magiquement la fonction getTasksProperty() -->
            <ul class="space-y-3">
                @foreach($this->tasks as $task)
                <li wire:key="task-{{ $task->id }}"
                    class="flex items-center justify-between p-3 border rounded shadow-sm {{ $task->is_completed ? 'bg-gray-50 opacity-75' : 'bg-white' }}">
                    
                    <div class="flex items-center space-x-3">
                        <input type="checkbox" wire:click="toggleComplete({{ $task->id }})" 
                               {{ $task->is_completed ? 'checked' : '' }} class="h-5 w-5 text-blue-600 cursor-pointer">
                        
                        <span class="{{ $task->is_completed ? 'line-through text-gray-400' : 'text-gray-800 font-medium' }}">
                            {{ $task->title }}
                        </span>
                    </div>

                    <button wire:click="delete({{ $task->id }})" 
                            wire:confirm="Sûr de supprimer cette tâche ?"
                            class="text-red-500 hover:text-red-700 p-1">
                        Supprimer
                    </button>
                </li>
                @endforeach
            </ul>

        </div>
    </div>
</div>
```

<br>

---

## Conclusion

!!! quote "Les helpers vitaux : wire:key et wire:confirm"
    Dans une liste d'éléments asynchrones, Livewire peut parfois s'emmêler les pinceaux et rafraichir le modèle du mauvais composant HTML. C'est pourquoi **vous devez absolument fournir un ID unique via `wire:key`** à l'élément racine de votre boucle pour que Livewire traque le modèle correctement. Également, `wire:confirm` bloque l'exécution PHP le temps de réclamer une "SweetAlert" native du navigateur pour protéger une action destructrice.

> En maîtrisant la boucle simple (`@foreach`), il est aisé d'imaginer des systèmes infiniment plus vastes, disposant de tableaux croisés (Datatables) avec recherche de masse ! Accédez au [Projet 4 : Datatable CRUD Avancé](./04-datatable-crud.md).
