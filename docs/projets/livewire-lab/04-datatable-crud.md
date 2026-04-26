---
description: "Projet 4 : Créer un tableau de données complexe avec tri, pagination et recherche."
icon: lucide/table
tags: ["PROJET", "LIVEWIRE", "DATATABLE", "PAGINATION", "SEARCH"]
---

# DateTable CRUD Avancé

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Livewire 3.x"
  data-time="3 Heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Manipuler la Big Data Sans Effort"
    Lorsqu'une liste d'éléments grossit, afficher manuellement 5 000 employés est suicidaire pour la charge navigateur. C'est là que le framework montre sa suprématie sur les technos pure front-end : **Livewire délègue le travail MySQL au serveur Blade, et demande organiquement au navigateur web de ne redessiner que le delta de données visible (Pagination / Recherche).** Adieu les plugins lourds comme _jQuery Datatables_ ou les usines à gaz de _Vuex_.

<br>

![Livewire Datatable Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_datatable_1775233269786.png)
<p><em>Maquette UI conceptuelle du projet : Un panneau d'administration professionnel équipé de filtres avancés.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- Afficher une liste d'utilisateurs par section de **10 par page (Pagination)** sans que l'URL ne rafraichisse.
- Disposer d'une **Barre de recherche textuelle globale**.
- Intégrer des flèches (`↑` / `↓`) sur l'entête de chaque colonne gérant le **Tri** (SortBy Order ASC/DESC).
- Coche permettant des actions de groupe "Bulk Actions" (Supprimer x éléments simultanément).
- **Le tout sans jamais "clignoter"**.

### Concepts Livewire déployés
- Le Trait unique `WithPagination` de Laravel transformé.
- Traitement de requête Eloquent `where` lié à une variable publique `wire:model`.
- Le modificateur asynchrone `throttle` ou `debounce` pour éviter d'inonder la base de données de requêtes MySQL à chaque lettre pressée.

<br>

---

## 2. Le Modèle PHP (La Logique de Filtration)

Dans ce projet, le classe Livewire est chargée d'interpréter 4 paramètres croisés pour construire la requête SQL en temps réel.

```php title="app/Livewire/UsersDataTable.php"
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\User;
use Livewire\WithPagination;

class UsersDataTable extends Component
{
    // Ce trait essentiel injecte la pagination AJAX
    use WithPagination;

    // Variables de conditions
    public $search = '';
    public $sortBy = 'name';
    public $sortDirection = 'asc';
    
    // Suivi des éléments cochables
    public $selectedRows = [];

    // Magic methode : Quand la "search" est modifiée par l'UX, on réinitialise la numérotation !
    public function updatingSearch()
    {
        $this->resetPage();
    }

    // Basculer l'ordre
    public function sort($column)
    {
        if ($this->sortBy === $column) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortBy = $column;
            $this->sortDirection = 'asc';
        }
    }

    // Suppression Massive (Bulk)
    public function deleteSelected()
    {
        User::whereIn('id', $this->selectedRows)->delete();
        $this->selectedRows = [];
    }

    public function render()
    {
        $query = User::query();

        // Si le champ texte est rempli, on rajoute des clauses
        if (!empty($this->search)) {
            $query->where('name', 'like', '%' . $this->search . '%')
                  ->orWhere('email', 'like', '%' . $this->search . '%');
        }

        // Exécution de l'ordre conditionnel
        $query->orderBy($this->sortBy, $this->sortDirection);

        // On expédie à la vue
        return view('livewire.users-data-table', [
            // Le ->paginate() est intercepté sans rechargement par Laravel Livewire
            'users' => $query->paginate(10),
        ]);
    }
}
```

_En observant le `updatingSearch()`, on comprend la notion capitale du cycle de vis des "Lifecycle Hooks". `updatingPropriété` est intercepté par PHP avant même que la nouvelle valeur saisie n'écrase l'ancienne._ 

<br>

---

## 3. La Vue Blade de la DataTable

Ici, une grande maîtrise des attributs Blade est nécessaire pour dynamiser la table. Assurez-vous que l'utilisation du debounce est en place.

```html title="resources/views/livewire/users-data-table.blade.php"
<div class="bg-white shadow rounded-lg p-6 overflow-hidden">
    
    <div class="flex justify-between items-center mb-6">
        <div class="w-1/3">
            <!-- debounce.300ms permet d'attendre 0.3s après la frappe clavier pour lancer la search. Cela repose le serveur SQL !! -->
            <input type="text" wire:model.live.debounce.300ms="search" placeholder="Rechercher par nom ou email..." 
                   class="w-full border p-2 rounded focus:ring-purple-500">
        </div>
        
        <div>
            @if(count($selectedRows) > 0)
            <button wire:click="deleteSelected" class="bg-red-500 text-white px-4 py-2 rounded">
                Supprimer {count($selectedRows)} employés
            </button>
            @endif
        </div>
    </div>

    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="p-3 w-10">#</th>
                <!-- On passe l'identifiant de la colonne dans le système de tri (wire:click="sort") -->
                <th wire:click="sort('name')" class="p-3 cursor-pointer text-left font-bold text-gray-500">
                    Nom Complet 
                    @if($sortBy === 'name') {{ $sortDirection === 'asc' ? '↑' : '↓' }} @endif
                </th>
                <th wire:click="sort('email')" class="p-3 cursor-pointer text-left font-bold text-gray-500">
                    Adresse Email
                    @if($sortBy === 'email') {{ $sortDirection === 'asc' ? '↑' : '↓' }} @endif
                </th>
                <th class="text-left font-bold text-gray-500">Enregistré le</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200" wire:loading.class="opacity-50">
            @forelse($users as $user)
            <!-- Le wire:key vital !! -->
            <tr wire:key="row-{{ $user->id }}" class="hover:bg-gray-50">
                <td class="p-3">
                    <!-- Liaison automatique du paramètre $selectedRows array à des checkbox multiples -->
                    <input type="checkbox" wire:model.live="selectedRows" value="{{ $user->id }}">
                </td>
                <td class="p-3">{{ $user->name }}</td>
                <td class="p-3 text-gray-500">{{ $user->email }}</td>
                <td class="p-3 text-xs">{{ $user->created_at->format('d/m/Y') }}</td>
            </tr>
            @empty
            <tr>
                <td colspan="4" class="p-4 text-center text-gray-400">Aucun utilisateur trouvé.</td>
            </tr>
            @endforelse
        </tbody>
    </table>

    <!-- Le système d'UI de pagination par défaut Laravel injecté sans refresh ! -->
    <div class="mt-4">
        {{ $users->links() }}
    </div>

</div>
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le composant de tableau de bord (Datatable) est un incontournable du développement métier. Livewire brille particulièrement sur ce type d'interface interactive (recherche en temps réel, tri, pagination), rendant sa conception redoutablement rapide.

!!! quote "Gains majeurs pour les Entreprises"
    En 30 minutes de travail et avec aucune bibliothèque JavaScript additionnelle, votre portail web est équipé du même tableau de productivité qu'utilisent les administrateurs centraux.
    
> Ce laboratoire ne fait que commencer à dévoiler le potentiel applicatif réseau (Network) de la plateforme. Comment gérer des modifications simultanées poussées *par* le réseau en temps réel ? Faisons appel aux WebSockets dans le [Projet 5 : Chat Real-time](./05-chat-realtime.md).
