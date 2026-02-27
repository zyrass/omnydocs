---
description: "WithPagination trait, datatables interactives, recherche/filtres/sorting, bulk actions, export CSV/Excel"
icon: lucide/book-open-check
tags: ["LIVEWIRE", "PAGINATION", "TABLES", "DATATABLE", "SEARCH", "FILTERS"]
---

# VIII — Pagination & Tables

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-duration="6-7 heures"
  data-lessons="9">
</div>

## Vue d'ensemble

!!! quote "Analogie pédagogique"
    _Imaginez une **bibliothèque universitaire avec système de catalogage avancé** : vous avez 50 000 livres (records database), mais le bibliothécaire ne vous apporte jamais les 50 000 livres à la fois. **Système de pagination** : il vous donne 20 livres par plateau (page), avec boutons "Précédent/Suivant" pour naviguer (WithPagination trait). **Système de recherche** : vous tapez "Python programming" dans terminal, le système filtre instantanément et n'affiche que 47 livres correspondants (search temps réel avec debounce). **Système de filtres** : vous cochez "Année > 2020" + "Catégorie = Informatique" + "Disponible", le système combine critères et affiche 12 livres précis (filtres cumulatifs). **Système de tri** : vous cliquez colonne "Auteur", tous livres se réorganisent alphabétiquement, cliquez à nouveau, ordre inverse (sorting bidirectionnel). **Système de sélection** : vous cochez 5 livres, cliquez "Exporter liste", le système génère Excel avec vos 5 sélections (bulk actions + export). **Livewire datatables fonctionnent exactement pareil** : pagination serveur (jamais charger 10 000 rows), recherche optimisée (query DB, pas JavaScript filter), filtres cumulatifs SQL (WHERE clauses), sorting dynamique (ORDER BY), sélection multiple (checkboxes + array), export intelligent (chunk grandes tables). C'est le **standard production pour gérer grandes données** : performance, UX fluide, scalabilité._

**Les datatables Livewire sont essentielles pour gérer grandes collections de données :**

- ✅ **WithPagination trait** = Pagination serveur automatique
- ✅ **Recherche temps réel** = Filtrage instantané avec debounce
- ✅ **Filtres multiples** = Critères cumulatifs (dates, statuts, catégories)
- ✅ **Sorting colonnes** = Tri ascendant/descendant dynamique
- ✅ **Bulk actions** = Sélection multiple et actions groupées
- ✅ **Export CSV/Excel** = Export données filtrées/triées
- ✅ **Gestion grandes tables** = Cursor pagination, chunk processing
- ✅ **Query optimization** = Eager loading, index DB, caching
- ✅ **UX avancée** = Loading states, skeleton, responsive

**Ce module couvre :**

1. WithPagination trait et configuration
2. Recherche temps réel avec debounce
3. Filtres multiples cumulatifs
4. Sorting colonnes (ascendant/descendant)
5. Bulk selection et actions groupées
6. Export CSV et Excel
7. Gestion grandes tables (cursor pagination)
8. Optimisation performance queries
9. Patterns datatables production

---

## Leçon 1 : WithPagination Trait

### 1.1 Configuration Basique

**`WithPagination` trait = Pagination serveur automatique**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;

class UserTable extends Component
{
    use WithPagination;

    /**
     * Nombre items par page
     */
    protected int $perPage = 10;

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::latest()->paginate($this->perPage)
        ]);
    }
}
```

```blade
{{-- resources/views/livewire/user-table.blade.php --}}
<div>
    {{-- Table --}}
    <table class="w-full">
        <thead>
            <tr>
                <th>Nom</th>
                <th>Email</th>
                <th>Rôle</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            @foreach($users as $user)
                <tr wire:key="user-{{ $user->id }}">
                    <td>{{ $user->name }}</td>
                    <td>{{ $user->email }}</td>
                    <td>{{ $user->role }}</td>
                    <td>
                        <button wire:click="edit({{ $user->id }})">Éditer</button>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>

    {{-- Pagination links --}}
    <div class="mt-4">
        {{ $users->links() }}
    </div>
</div>
```

### 1.2 Pagination Theme (Tailwind/Bootstrap)

**Configurer theme pagination globalement :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;

class UserTable extends Component
{
    use WithPagination;

    /**
     * Theme pagination : 'tailwind' ou 'bootstrap'
     */
    protected $paginationTheme = 'tailwind';

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(10)
        ]);
    }
}
```

**Ou configuration AppServiceProvider globale :**

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Livewire\Livewire;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // Theme Tailwind par défaut pour TOUS composants Livewire
        Livewire::useTailwindPagination();
        
        // Ou Bootstrap
        // Livewire::useBootstrapPagination();
    }
}
```

### 1.3 Pagination Query String

**Persister page dans URL (partage lien, bookmark)**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;

class UserTable extends Component
{
    use WithPagination;

    /**
     * Ajouter ?page=2 dans URL
     */
    protected $queryString = [
        'page' => ['except' => 1], // Exclure page=1 de l'URL
    ];

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(10)
        ]);
    }
}
```

**Résultat URL :**

```
/users           → Page 1 (pas de query string)
/users?page=2    → Page 2
/users?page=3    → Page 3
```

### 1.4 Reset Page (sur changement filtre)

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;

class UserTable extends Component
{
    use WithPagination;

    public string $search = '';
    public string $roleFilter = '';

    protected $queryString = [
        'search' => ['except' => ''],
        'roleFilter' => ['except' => ''],
        'page' => ['except' => 1],
    ];

    /**
     * Reset page quand search change
     */
    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    /**
     * Reset page quand roleFilter change
     */
    public function updatedRoleFilter(): void
    {
        $this->resetPage();
    }

    public function render()
    {
        $query = User::query();

        if ($this->search) {
            $query->where('name', 'like', "%{$this->search}%")
                  ->orWhere('email', 'like', "%{$this->search}%");
        }

        if ($this->roleFilter) {
            $query->where('role', $this->roleFilter);
        }

        return view('livewire.user-table', [
            'users' => $query->paginate(10)
        ]);
    }
}
```

**Pourquoi `resetPage()` ?**

Sans reset : User sur page 5, tape recherche, reste page 5 mais peut être vide → UX confuse.
Avec reset : Recherche ramène automatiquement à page 1 → UX logique.

### 1.5 Per Page Dynamique

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;

class UserTable extends Component
{
    use WithPagination;

    public int $perPage = 10;

    protected $queryString = [
        'perPage' => ['except' => 10],
    ];

    /**
     * Reset page si perPage change
     */
    public function updatedPerPage(): void
    {
        $this->resetPage();
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate($this->perPage)
        ]);
    }
}
```

```blade
<div>
    {{-- Per page selector --}}
    <div class="flex items-center space-x-2 mb-4">
        <label>Afficher :</label>
        <select wire:model.live="perPage" class="border rounded px-2 py-1">
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
        </select>
        <span>par page</span>
    </div>

    {{-- Table --}}
    <table>...</table>

    {{-- Pagination --}}
    {{ $users->links() }}
</div>
```

---

## Leçon 2 : Recherche Temps Réel

### 2.1 Search Input avec Debounce

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Product;

class ProductTable extends Component
{
    use WithPagination;

    public string $search = '';
    public int $perPage = 20;

    protected $queryString = [
        'search' => ['except' => ''],
        'perPage' => ['except' => 20],
    ];

    /**
     * Reset page à chaque nouvelle recherche
     */
    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    public function render()
    {
        $query = Product::query();

        if ($this->search) {
            $query->where(function ($q) {
                $q->where('name', 'like', "%{$this->search}%")
                  ->orWhere('sku', 'like', "%{$this->search}%")
                  ->orWhere('description', 'like', "%{$this->search}%");
            });
        }

        return view('livewire.product-table', [
            'products' => $query->latest()->paginate($this->perPage)
        ]);
    }
}
```

```blade
<div>
    {{-- Search bar avec debounce --}}
    <div class="mb-4">
        <input 
            type="text" 
            wire:model.live.debounce.300ms="search"
            placeholder="Rechercher produit (nom, SKU, description)..."
            class="w-full px-4 py-2 border rounded"
        >
        
        {{-- Loading indicator --}}
        <span wire:loading wire:target="search" class="text-gray-500 text-sm ml-2">
            Recherche en cours...
        </span>
        
        {{-- Résultats count --}}
        @if($search)
            <p class="text-sm text-gray-600 mt-2">
                {{ $products->total() }} résultat(s) pour "{{ $search }}"
            </p>
        @endif
    </div>

    {{-- Table products --}}
    <table class="w-full">
        <thead>
            <tr>
                <th>SKU</th>
                <th>Nom</th>
                <th>Prix</th>
                <th>Stock</th>
            </tr>
        </thead>
        <tbody>
            @forelse($products as $product)
                <tr wire:key="product-{{ $product->id }}">
                    <td>{{ $product->sku }}</td>
                    <td>{{ $product->name }}</td>
                    <td>{{ $product->price }}€</td>
                    <td>{{ $product->stock }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="text-center py-4 text-gray-500">
                        Aucun produit trouvé.
                    </td>
                </tr>
            @endforelse
        </tbody>
    </table>

    {{-- Pagination --}}
    <div class="mt-4">
        {{ $products->links() }}
    </div>
</div>
```

### 2.2 Search avec Highlight Résultats

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;

class ProductTable extends Component
{
    use WithPagination;

    public string $search = '';

    /**
     * Highlight search terms dans texte
     */
    public function highlightSearch(string $text): string
    {
        if (!$this->search) {
            return $text;
        }

        return preg_replace(
            '/(' . preg_quote($this->search, '/') . ')/i',
            '<mark class="bg-yellow-200">$1</mark>',
            $text
        );
    }

    public function render()
    {
        // Query...
        return view('livewire.product-table', [
            'products' => $query->paginate(20)
        ]);
    }
}
```

```blade
<tbody>
    @foreach($products as $product)
        <tr wire:key="product-{{ $product->id }}">
            <td>{{ $product->sku }}</td>
            <td>{!! $this->highlightSearch($product->name) !!}</td>
            <td>{!! $this->highlightSearch($product->description) !!}</td>
        </tr>
    @endforeach
</tbody>
```

### 2.3 Search avec Full-Text Index

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Article;

class ArticleTable extends Component
{
    use WithPagination;

    public string $search = '';

    public function render()
    {
        $query = Article::query();

        if ($this->search) {
            // Full-text search (nécessite index FULLTEXT MySQL)
            $query->whereRaw(
                'MATCH(title, content) AGAINST(? IN BOOLEAN MODE)',
                [$this->search]
            );
        }

        return view('livewire.article-table', [
            'articles' => $query->paginate(20)
        ]);
    }
}
```

**Créer index FULLTEXT (migration) :**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('articles', function (Blueprint $table) {
            // Créer index FULLTEXT sur colonnes title et content
            DB::statement('ALTER TABLE articles ADD FULLTEXT fulltext_index (title, content)');
        });
    }

    public function down(): void
    {
        Schema::table('articles', function (Blueprint $table) {
            DB::statement('ALTER TABLE articles DROP INDEX fulltext_index');
        });
    }
};
```

---

## Leçon 3 : Filtres Multiples Cumulatifs

### 3.1 Filtres Basiques

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Order;

class OrderTable extends Component
{
    use WithPagination;

    // Filtres
    public string $search = '';
    public string $statusFilter = '';
    public string $dateFrom = '';
    public string $dateTo = '';
    public float $minAmount = 0;
    public float $maxAmount = 10000;

    protected $queryString = [
        'search' => ['except' => ''],
        'statusFilter' => ['except' => ''],
        'dateFrom' => ['except' => ''],
        'dateTo' => ['except' => ''],
        'minAmount' => ['except' => 0],
        'maxAmount' => ['except' => 10000],
    ];

    /**
     * Reset page si n'importe quel filtre change
     */
    public function updated($propertyName): void
    {
        if (str_starts_with($propertyName, 'search') || 
            str_contains($propertyName, 'Filter') ||
            str_contains($propertyName, 'date') ||
            str_contains($propertyName, 'Amount')) {
            $this->resetPage();
        }
    }

    /**
     * Clear tous filtres
     */
    public function clearFilters(): void
    {
        $this->reset([
            'search',
            'statusFilter',
            'dateFrom',
            'dateTo',
            'minAmount',
            'maxAmount',
        ]);
        $this->resetPage();
    }

    public function render()
    {
        $query = Order::with('customer');

        // Filtre recherche
        if ($this->search) {
            $query->where(function ($q) {
                $q->where('order_number', 'like', "%{$this->search}%")
                  ->orWhereHas('customer', function ($q) {
                      $q->where('name', 'like', "%{$this->search}%")
                        ->orWhere('email', 'like', "%{$this->search}%");
                  });
            });
        }

        // Filtre status
        if ($this->statusFilter) {
            $query->where('status', $this->statusFilter);
        }

        // Filtre date range
        if ($this->dateFrom) {
            $query->whereDate('created_at', '>=', $this->dateFrom);
        }
        if ($this->dateTo) {
            $query->whereDate('created_at', '<=', $this->dateTo);
        }

        // Filtre montant range
        $query->whereBetween('total', [$this->minAmount, $this->maxAmount]);

        return view('livewire.order-table', [
            'orders' => $query->latest()->paginate(20)
        ]);
    }
}
```

```blade
<div>
    {{-- Filtres panel --}}
    <div class="bg-gray-100 p-4 rounded mb-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            {{-- Search --}}
            <div>
                <label class="block text-sm font-medium mb-1">Recherche</label>
                <input 
                    type="text" 
                    wire:model.live.debounce.300ms="search"
                    placeholder="N° commande, client..."
                    class="w-full px-3 py-2 border rounded"
                >
            </div>

            {{-- Status filter --}}
            <div>
                <label class="block text-sm font-medium mb-1">Statut</label>
                <select wire:model.live="statusFilter" class="w-full px-3 py-2 border rounded">
                    <option value="">Tous</option>
                    <option value="pending">En attente</option>
                    <option value="processing">En cours</option>
                    <option value="completed">Terminée</option>
                    <option value="cancelled">Annulée</option>
                </select>
            </div>

            {{-- Date from --}}
            <div>
                <label class="block text-sm font-medium mb-1">Du</label>
                <input 
                    type="date" 
                    wire:model.live="dateFrom"
                    class="w-full px-3 py-2 border rounded"
                >
            </div>

            {{-- Date to --}}
            <div>
                <label class="block text-sm font-medium mb-1">Au</label>
                <input 
                    type="date" 
                    wire:model.live="dateTo"
                    class="w-full px-3 py-2 border rounded"
                >
            </div>

            {{-- Amount range --}}
            <div>
                <label class="block text-sm font-medium mb-1">Montant min</label>
                <input 
                    type="number" 
                    wire:model.live.debounce.500ms="minAmount"
                    min="0"
                    step="10"
                    class="w-full px-3 py-2 border rounded"
                >
            </div>

            <div>
                <label class="block text-sm font-medium mb-1">Montant max</label>
                <input 
                    type="number" 
                    wire:model.live.debounce.500ms="maxAmount"
                    min="0"
                    step="10"
                    class="w-full px-3 py-2 border rounded"
                >
            </div>
        </div>

        {{-- Clear filters button --}}
        <div class="mt-4">
            <button 
                wire:click="clearFilters"
                class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
            >
                Réinitialiser filtres
            </button>
        </div>

        {{-- Active filters count --}}
        <div class="mt-2 text-sm text-gray-600">
            @php
                $activeFilters = 0;
                if($search) $activeFilters++;
                if($statusFilter) $activeFilters++;
                if($dateFrom || $dateTo) $activeFilters++;
                if($minAmount > 0 || $maxAmount < 10000) $activeFilters++;
            @endphp
            
            @if($activeFilters > 0)
                <span>{{ $activeFilters }} filtre(s) actif(s)</span>
            @endif
        </div>
    </div>

    {{-- Table orders --}}
    <table class="w-full">
        <thead>
            <tr>
                <th>N° Commande</th>
                <th>Client</th>
                <th>Date</th>
                <th>Montant</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            @foreach($orders as $order)
                <tr wire:key="order-{{ $order->id }}">
                    <td>{{ $order->order_number }}</td>
                    <td>{{ $order->customer->name }}</td>
                    <td>{{ $order->created_at->format('d/m/Y') }}</td>
                    <td>{{ number_format($order->total, 2) }}€</td>
                    <td>
                        <span class="badge badge-{{ $order->status }}">
                            {{ ucfirst($order->status) }}
                        </span>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>

    {{-- Pagination --}}
    <div class="mt-4">
        {{ $orders->links() }}
    </div>
</div>
```

### 3.2 Filtres avec Compteurs

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Product;

class ProductTable extends Component
{
    public string $categoryFilter = '';

    /**
     * Computed : Compter produits par catégorie
     */
    public function getCategoryCountsProperty()
    {
        return Product::selectRaw('category, COUNT(*) as count')
            ->groupBy('category')
            ->pluck('count', 'category');
    }

    public function render()
    {
        $query = Product::query();

        if ($this->categoryFilter) {
            $query->where('category', $this->categoryFilter);
        }

        return view('livewire.product-table', [
            'products' => $query->paginate(20)
        ]);
    }
}
```

```blade
{{-- Filtres avec compteurs --}}
<div class="flex space-x-2 mb-4">
    <button 
        wire:click="$set('categoryFilter', '')"
        class="px-4 py-2 rounded {{ $categoryFilter === '' ? 'bg-blue-600 text-white' : 'bg-gray-200' }}"
    >
        Tous ({{ $this->categoryCounts->sum() }})
    </button>

    @foreach($this->categoryCounts as $category => $count)
        <button 
            wire:click="$set('categoryFilter', '{{ $category }}')"
            class="px-4 py-2 rounded {{ $categoryFilter === $category ? 'bg-blue-600 text-white' : 'bg-gray-200' }}"
        >
            {{ ucfirst($category) }} ({{ $count }})
        </button>
    @endforeach
</div>
```

---

## Leçon 4 : Sorting Colonnes

### 4.1 Sorting Bidirectionnel

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;

class UserTable extends Component
{
    use WithPagination;

    // Sorting
    public string $sortField = 'created_at';
    public string $sortDirection = 'desc';

    protected $queryString = [
        'sortField' => ['except' => 'created_at'],
        'sortDirection' => ['except' => 'desc'],
    ];

    /**
     * Toggle sort direction ou change field
     */
    public function sortBy(string $field): void
    {
        if ($this->sortField === $field) {
            // Si même field, toggle direction
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            // Nouveau field, default asc
            $this->sortField = $field;
            $this->sortDirection = 'asc';
        }
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::orderBy($this->sortField, $this->sortDirection)
                ->paginate(20)
        ]);
    }
}
```

```blade
<table class="w-full">
    <thead>
        <tr>
            {{-- Sortable column name --}}
            <th>
                <button 
                    wire:click="sortBy('name')"
                    class="flex items-center space-x-1 hover:text-blue-600"
                >
                    <span>Nom</span>
                    @if($sortField === 'name')
                        @if($sortDirection === 'asc')
                            <span>↑</span>
                        @else
                            <span>↓</span>
                        @endif
                    @endif
                </button>
            </th>

            {{-- Sortable column email --}}
            <th>
                <button 
                    wire:click="sortBy('email')"
                    class="flex items-center space-x-1 hover:text-blue-600"
                >
                    <span>Email</span>
                    @if($sortField === 'email')
                        @if($sortDirection === 'asc')
                            <span>↑</span>
                        @else
                            <span>↓</span>
                        @endif
                    @endif
                </button>
            </th>

            {{-- Sortable column created_at --}}
            <th>
                <button 
                    wire:click="sortBy('created_at')"
                    class="flex items-center space-x-1 hover:text-blue-600"
                >
                    <span>Date inscription</span>
                    @if($sortField === 'created_at')
                        @if($sortDirection === 'asc')
                            <span>↑</span>
                        @else
                            <span>↓</span>
                        @endif
                    @endif
                </button>
            </th>

            {{-- Non-sortable column --}}
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        @foreach($users as $user)
            <tr wire:key="user-{{ $user->id }}">
                <td>{{ $user->name }}</td>
                <td>{{ $user->email }}</td>
                <td>{{ $user->created_at->format('d/m/Y') }}</td>
                <td><button>Éditer</button></td>
            </tr>
        @endforeach
    </tbody>
</table>
```

### 4.2 Sortable Header Component Réutilisable

```blade
{{-- resources/views/components/sortable-header.blade.php --}}
@props(['field', 'sortField', 'sortDirection'])

<button 
    wire:click="sortBy('{{ $field }}')"
    class="flex items-center space-x-1 hover:text-blue-600 font-medium"
>
    <span>{{ $slot }}</span>
    
    @if($sortField === $field)
        @if($sortDirection === 'asc')
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
            </svg>
        @else
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
        @endif
    @else
        <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
        </svg>
    @endif
</button>
```

**Utilisation component :**

```blade
<thead>
    <tr>
        <th>
            <x-sortable-header field="name" :sortField="$sortField" :sortDirection="$sortDirection">
                Nom
            </x-sortable-header>
        </th>
        <th>
            <x-sortable-header field="email" :sortField="$sortField" :sortDirection="$sortDirection">
                Email
            </x-sortable-header>
        </th>
        <th>
            <x-sortable-header field="created_at" :sortField="$sortField" :sortDirection="$sortDirection">
                Date inscription
            </x-sortable-header>
        </th>
    </tr>
</thead>
```

### 4.3 Sorting avec Relations

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Post;

class PostTable extends Component
{
    use WithPagination;

    public string $sortField = 'created_at';
    public string $sortDirection = 'desc';

    public function sortBy(string $field): void
    {
        if ($this->sortField === $field) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortField = $field;
            $this->sortDirection = 'asc';
        }
    }

    public function render()
    {
        $query = Post::with('author');

        // Sorting selon field
        if ($this->sortField === 'author_name') {
            // Sorting par relation (JOIN)
            $query->join('users', 'posts.user_id', '=', 'users.id')
                  ->select('posts.*')
                  ->orderBy('users.name', $this->sortDirection);
        } else {
            // Sorting colonne directe
            $query->orderBy($this->sortField, $this->sortDirection);
        }

        return view('livewire.post-table', [
            'posts' => $query->paginate(20)
        ]);
    }
}
```

---

## Leçon 5 : Bulk Selection et Actions Groupées

### 5.1 Sélection Multiple

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;

class UserTable extends Component
{
    use WithPagination;

    // Sélection
    public array $selected = [];
    public bool $selectAll = false;

    /**
     * Toggle select all items sur page courante
     */
    public function updatedSelectAll($value): void
    {
        if ($value) {
            // Sélectionner tous IDs page courante
            $this->selected = User::pluck('id')->toArray();
        } else {
            // Désélectionner tous
            $this->selected = [];
        }
    }

    /**
     * Supprimer sélectionnés
     */
    public function deleteSelected(): void
    {
        User::whereIn('id', $this->selected)->delete();

        $this->selected = [];
        $this->selectAll = false;

        session()->flash('message', count($this->selected) . ' utilisateur(s) supprimé(s).');
    }

    /**
     * Bulk update status
     */
    public function updateStatusSelected(string $status): void
    {
        User::whereIn('id', $this->selected)->update(['status' => $status]);

        session()->flash('message', count($this->selected) . ' utilisateur(s) mis à jour.');
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(20)
        ]);
    }
}
```

```blade
<div>
    {{-- Bulk actions bar (si sélection) --}}
    @if(count($selected) > 0)
        <div class="bg-blue-100 border border-blue-300 rounded p-4 mb-4 flex items-center justify-between">
            <span class="font-medium">
                {{ count($selected) }} utilisateur(s) sélectionné(s)
            </span>
            
            <div class="flex space-x-2">
                <button 
                    wire:click="updateStatusSelected('active')"
                    class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                    Activer
                </button>
                
                <button 
                    wire:click="updateStatusSelected('inactive')"
                    class="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
                >
                    Désactiver
                </button>
                
                <button 
                    wire:click="deleteSelected"
                    onclick="return confirm('Supprimer {{ count($selected) }} utilisateur(s) ?')"
                    class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                    Supprimer
                </button>
            </div>
        </div>
    @endif

    {{-- Table --}}
    <table class="w-full">
        <thead>
            <tr>
                {{-- Select all checkbox --}}
                <th class="w-12">
                    <input 
                        type="checkbox" 
                        wire:model.live="selectAll"
                        class="rounded"
                    >
                </th>
                <th>Nom</th>
                <th>Email</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            @foreach($users as $user)
                <tr wire:key="user-{{ $user->id }}">
                    {{-- Individual checkbox --}}
                    <td>
                        <input 
                            type="checkbox" 
                            wire:model.live="selected"
                            value="{{ $user->id }}"
                            class="rounded"
                        >
                    </td>
                    <td>{{ $user->name }}</td>
                    <td>{{ $user->email }}</td>
                    <td>
                        <span class="badge badge-{{ $user->status }}">
                            {{ $user->status }}
                        </span>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>

    {{-- Pagination --}}
    {{ $users->links() }}
</div>
```

### 5.2 Select All Across Pages

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;

class UserTable extends Component
{
    use WithPagination;

    public array $selected = [];
    public bool $selectAll = false;
    public bool $selectAllPages = false;

    /**
     * Select all items sur page courante
     */
    public function updatedSelectAll($value): void
    {
        if ($value) {
            // Sélectionner IDs page courante
            $this->selected = User::paginate(20)->pluck('id')->toArray();
        } else {
            $this->selected = [];
            $this->selectAllPages = false;
        }
    }

    /**
     * Select ALL items across ALL pages
     */
    public function selectAllPagesToggle(): void
    {
        if ($this->selectAllPages) {
            // Sélectionner TOUS les IDs (toutes pages)
            $this->selected = User::pluck('id')->toArray();
        } else {
            // Revenir à sélection page courante
            $this->selected = User::paginate(20)->pluck('id')->toArray();
        }
    }

    public function deleteSelected(): void
    {
        User::whereIn('id', $this->selected)->delete();

        $this->selected = [];
        $this->selectAll = false;
        $this->selectAllPages = false;

        session()->flash('message', 'Utilisateurs supprimés.');
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(20),
            'totalUsers' => User::count(),
        ]);
    }
}
```

```blade
{{-- Bulk actions bar --}}
@if(count($selected) > 0)
    <div class="bg-blue-100 border border-blue-300 rounded p-4 mb-4">
        <div class="flex items-center justify-between">
            <div>
                <span class="font-medium">
                    {{ count($selected) }} utilisateur(s) sélectionné(s)
                </span>
                
                {{-- Select all pages option --}}
                @if(count($selected) === $users->count() && !$selectAllPages && $users->total() > $users->count())
                    <div class="mt-2">
                        <button 
                            wire:click="selectAllPagesToggle"
                            class="text-blue-600 hover:underline text-sm"
                        >
                            Sélectionner les {{ $totalUsers }} utilisateurs (toutes pages)
                        </button>
                    </div>
                @endif

                @if($selectAllPages)
                    <div class="mt-2 text-sm text-blue-700">
                        Tous les {{ $totalUsers }} utilisateurs sont sélectionnés.
                        <button 
                            wire:click="$set('selectAllPages', false)"
                            class="hover:underline"
                        >
                            Annuler
                        </button>
                    </div>
                @endif
            </div>

            <div class="flex space-x-2">
                <button 
                    wire:click="deleteSelected"
                    onclick="return confirm('Supprimer {{ count($selected) }} utilisateur(s) ?')"
                    class="px-4 py-2 bg-red-600 text-white rounded"
                >
                    Supprimer
                </button>
            </div>
        </div>
    </div>
@endif
```

---

## Leçon 6 : Export CSV et Excel

### 6.1 Export CSV Simple

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;

class UserTable extends Component
{
    use WithPagination;

    public string $search = '';

    /**
     * Export CSV avec filtres appliqués
     */
    public function exportCsv(): void
    {
        $query = User::query();

        if ($this->search) {
            $query->where('name', 'like', "%{$this->search}%")
                  ->orWhere('email', 'like', "%{$this->search}%");
        }

        $users = $query->get();

        // Générer CSV
        $csv = "Nom,Email,Rôle,Date inscription\n";
        
        foreach ($users as $user) {
            $csv .= "{$user->name},{$user->email},{$user->role},{$user->created_at->format('d/m/Y')}\n";
        }

        // Retourner download response
        return response()->streamDownload(function () use ($csv) {
            echo $csv;
        }, 'users-' . now()->format('Y-m-d') . '.csv', [
            'Content-Type' => 'text/csv',
        ]);
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(20)
        ]);
    }
}
```

```blade
{{-- Export button --}}
<div class="mb-4">
    <button 
        wire:click="exportCsv"
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
    >
        <span wire:loading.remove wire:target="exportCsv">
            📥 Exporter CSV
        </span>
        <span wire:loading wire:target="exportCsv">
            Génération CSV...
        </span>
    </button>
</div>
```

### 6.2 Export Excel avec Laravel Excel

```bash
# Installer Laravel Excel
composer require maatwebsite/excel
```

```php
<?php

namespace App\Exports;

use App\Models\User;
use Maatwebsite\Excel\Concerns\FromQuery;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;

class UsersExport implements FromQuery, WithHeadings, WithMapping
{
    protected $search;

    public function __construct(?string $search = null)
    {
        $this->search = $search;
    }

    /**
     * Query avec filtres
     */
    public function query()
    {
        $query = User::query();

        if ($this->search) {
            $query->where('name', 'like', "%{$this->search}%")
                  ->orWhere('email', 'like', "%{$this->search}%");
        }

        return $query;
    }

    /**
     * Headers Excel
     */
    public function headings(): array
    {
        return [
            'ID',
            'Nom',
            'Email',
            'Rôle',
            'Date inscription',
        ];
    }

    /**
     * Mapper chaque row
     */
    public function map($user): array
    {
        return [
            $user->id,
            $user->name,
            $user->email,
            $user->role,
            $user->created_at->format('d/m/Y H:i'),
        ];
    }
}
```

**Livewire component :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\User;
use App\Exports\UsersExport;
use Maatwebsite\Excel\Facades\Excel;

class UserTable extends Component
{
    use WithPagination;

    public string $search = '';

    /**
     * Export Excel
     */
    public function exportExcel()
    {
        return Excel::download(
            new UsersExport($this->search),
            'users-' . now()->format('Y-m-d') . '.xlsx'
        );
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(20)
        ]);
    }
}
```

```blade
{{-- Export buttons --}}
<div class="flex space-x-2 mb-4">
    <button 
        wire:click="exportCsv"
        class="px-4 py-2 bg-green-600 text-white rounded"
    >
        📥 Export CSV
    </button>
    
    <button 
        wire:click="exportExcel"
        class="px-4 py-2 bg-green-700 text-white rounded"
    >
        📊 Export Excel
    </button>
</div>
```

### 6.3 Export Sélection Uniquement

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\User;

class UserTable extends Component
{
    public array $selected = [];

    /**
     * Export seulement items sélectionnés
     */
    public function exportSelected(): void
    {
        if (empty($this->selected)) {
            session()->flash('error', 'Aucun utilisateur sélectionné.');
            return;
        }

        $users = User::whereIn('id', $this->selected)->get();

        $csv = "Nom,Email,Rôle\n";
        
        foreach ($users as $user) {
            $csv .= "{$user->name},{$user->email},{$user->role}\n";
        }

        return response()->streamDownload(function () use ($csv) {
            echo $csv;
        }, 'users-selection-' . now()->format('Y-m-d') . '.csv');
    }

    public function render()
    {
        return view('livewire.user-table', [
            'users' => User::paginate(20)
        ]);
    }
}
```

```blade
{{-- Export selection button (visible si sélection) --}}
@if(count($selected) > 0)
    <div class="mb-4">
        <button 
            wire:click="exportSelected"
            class="px-4 py-2 bg-blue-600 text-white rounded"
        >
            📥 Exporter sélection ({{ count($selected) }})
        </button>
    </div>
@endif
```

---

## Leçon 7 : Gestion Grandes Tables

### 7.1 Cursor Pagination (Memory Efficient)

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Log;

class LogTable extends Component
{
    use WithPagination;

    /**
     * Cursor pagination pour GRANDES tables (millions rows)
     * Plus efficient que offset pagination
     */
    public function render()
    {
        return view('livewire.log-table', [
            'logs' => Log::latest()->cursorPaginate(50)
        ]);
    }
}
```

**Différence offset vs cursor :**

```sql
-- Offset pagination (LENT sur grandes tables)
SELECT * FROM logs ORDER BY id DESC LIMIT 50 OFFSET 500000;
-- Doit scanner 500050 rows

-- Cursor pagination (RAPIDE)
SELECT * FROM logs WHERE id < 1234567 ORDER BY id DESC LIMIT 50;
-- Utilise index, scan minimal
```

### 7.2 Chunk Processing Export

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Order;

class OrderTable extends Component
{
    /**
     * Export grande table par chunks (éviter memory overflow)
     */
    public function exportLarge()
    {
        return response()->streamDownload(function () {
            $handle = fopen('php://output', 'w');

            // Headers CSV
            fputcsv($handle, ['ID', 'Order Number', 'Customer', 'Total', 'Date']);

            // Chunk 1000 rows à la fois
            Order::with('customer')->chunk(1000, function ($orders) use ($handle) {
                foreach ($orders as $order) {
                    fputcsv($handle, [
                        $order->id,
                        $order->order_number,
                        $order->customer->name,
                        $order->total,
                        $order->created_at->format('d/m/Y'),
                    ]);
                }
            });

            fclose($handle);
        }, 'orders-export-' . now()->format('Y-m-d') . '.csv');
    }

    public function render()
    {
        return view('livewire.order-table', [
            'orders' => Order::paginate(50)
        ]);
    }
}
```

### 7.3 Database Indexes

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            // Index colonnes souvent filtrées/triées
            $table->index('status');
            $table->index('created_at');
            $table->index(['customer_id', 'status']); // Composite index
            
            // Fulltext index pour recherche
            $table->fullText(['order_number', 'notes']);
        });
    }

    public function down(): void
    {
        Schema::table('orders', function (Blueprint $table) {
            $table->dropIndex(['status']);
            $table->dropIndex(['created_at']);
            $table->dropIndex(['customer_id', 'status']);
            $table->dropFullText(['order_number', 'notes']);
        });
    }
};
```

---

## Leçon 8 : Optimisation Performance

### 8.1 Eager Loading Relations

```php
<?php

// ❌ MAUVAIS : N+1 queries
public function render()
{
    return view('livewire.post-table', [
        'posts' => Post::paginate(20) // N+1 sur author, category, tags
    ]);
}
```

```php
<?php

// ✅ BON : Eager loading
public function render()
{
    return view('livewire.post-table', [
        'posts' => Post::with([
            'author:id,name',           // Select colonnes spécifiques
            'category:id,name',
            'tags:id,name',
        ])
        ->withCount('comments')         // Compter sans charger
        ->paginate(20)
    ]);
}
```

### 8.2 Select Specific Columns

```php
<?php

// ❌ MAUVAIS : SELECT * (toutes colonnes)
$users = User::paginate(20);

// ✅ BON : SELECT colonnes nécessaires uniquement
$users = User::select('id', 'name', 'email', 'role', 'created_at')
    ->paginate(20);

// Économise mémoire et bande passante
```

### 8.3 Cache Queries Lourdes

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Cache;

class StatisticsTable extends Component
{
    public function getStatsProperty()
    {
        // Cache 10 minutes
        return Cache::remember('dashboard-stats', 600, function () {
            return [
                'total_users' => User::count(),
                'active_users' => User::where('status', 'active')->count(),
                'total_revenue' => Order::sum('total'),
                'avg_order_value' => Order::avg('total'),
            ];
        });
    }

    public function refreshStats(): void
    {
        Cache::forget('dashboard-stats');
    }

    public function render()
    {
        return view('livewire.statistics-table');
    }
}
```

### 8.4 Query Optimization Tips

```php
<?php

// ❌ Éviter whereHas avec collections grandes
$posts = Post::whereHas('comments', function ($query) {
    $query->where('approved', true);
})->get();

// ✅ Préférer join si possible
$posts = Post::join('comments', 'posts.id', '=', 'comments.post_id')
    ->where('comments.approved', true)
    ->select('posts.*')
    ->distinct()
    ->get();

// ❌ Éviter count() sur collections
$count = Post::all()->count();

// ✅ Count directement en DB
$count = Post::count();

// ❌ Éviter pluck() sans select
$names = User::all()->pluck('name');

// ✅ Pluck directement
$names = User::pluck('name');
```

---

## Leçon 9 : Patterns Datatables Production

### 9.1 Trait Réutilisable WithDataTable

```php
<?php

namespace App\Livewire\Concerns;

use Livewire\WithPagination;

trait WithDataTable
{
    use WithPagination;

    // Sorting
    public string $sortField = 'created_at';
    public string $sortDirection = 'desc';

    // Filtering
    public string $search = '';
    public int $perPage = 20;

    // Selection
    public array $selected = [];
    public bool $selectAll = false;

    protected $queryString = [
        'search' => ['except' => ''],
        'sortField' => ['except' => 'created_at'],
        'sortDirection' => ['except' => 'desc'],
        'perPage' => ['except' => 20],
    ];

    public function sortBy(string $field): void
    {
        if ($this->sortField === $field) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortField = $field;
            $this->sortDirection = 'asc';
        }
    }

    public function updatedSearch(): void
    {
        $this->resetPage();
    }

    public function updatedPerPage(): void
    {
        $this->resetPage();
    }

    public function clearFilters(): void
    {
        $this->reset(['search', 'sortField', 'sortDirection']);
        $this->resetPage();
    }
}
```

**Utilisation trait :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Livewire\Concerns\WithDataTable;
use App\Models\Product;

class ProductTable extends Component
{
    use WithDataTable; // Toutes fonctionnalités datatable incluses

    public function render()
    {
        $query = Product::query();

        if ($this->search) {
            $query->where('name', 'like', "%{$this->search}%");
        }

        return view('livewire.product-table', [
            'products' => $query->orderBy($this->sortField, $this->sortDirection)
                ->paginate($this->perPage)
        ]);
    }
}
```

### 9.2 DataTable Component Complet

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Order;
use Maatwebsite\Excel\Facades\Excel;
use App\Exports\OrdersExport;

class OrderDataTable extends Component
{
    use WithPagination;

    // Sorting
    public string $sortField = 'created_at';
    public string $sortDirection = 'desc';

    // Filtering
    public string $search = '';
    public string $statusFilter = '';
    public string $dateFrom = '';
    public string $dateTo = '';
    public int $perPage = 20;

    // Selection
    public array $selected = [];

    protected $queryString = [
        'search' => ['except' => ''],
        'statusFilter' => ['except' => ''],
        'dateFrom' => ['except' => ''],
        'dateTo' => ['except' => ''],
        'sortField' => ['except' => 'created_at'],
        'sortDirection' => ['except' => 'desc'],
        'perPage' => ['except' => 20],
    ];

    public function updated($propertyName): void
    {
        if (in_array($propertyName, ['search', 'statusFilter', 'dateFrom', 'dateTo', 'perPage'])) {
            $this->resetPage();
        }
    }

    public function sortBy(string $field): void
    {
        if ($this->sortField === $field) {
            $this->sortDirection = $this->sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            $this->sortField = $field;
            $this->sortDirection = 'asc';
        }
    }

    public function clearFilters(): void
    {
        $this->reset(['search', 'statusFilter', 'dateFrom', 'dateTo']);
        $this->resetPage();
    }

    public function deleteSelected(): void
    {
        Order::whereIn('id', $this->selected)->delete();
        $this->selected = [];
        session()->flash('message', 'Commandes supprimées.');
    }

    public function exportExcel()
    {
        return Excel::download(
            new OrdersExport($this->search, $this->statusFilter, $this->dateFrom, $this->dateTo),
            'orders-' . now()->format('Y-m-d') . '.xlsx'
        );
    }

    public function render()
    {
        $query = Order::with('customer');

        // Search
        if ($this->search) {
            $query->where(function ($q) {
                $q->where('order_number', 'like', "%{$this->search}%")
                  ->orWhereHas('customer', function ($q) {
                      $q->where('name', 'like', "%{$this->search}%");
                  });
            });
        }

        // Status filter
        if ($this->statusFilter) {
            $query->where('status', $this->statusFilter);
        }

        // Date range
        if ($this->dateFrom) {
            $query->whereDate('created_at', '>=', $this->dateFrom);
        }
        if ($this->dateTo) {
            $query->whereDate('created_at', '<=', $this->dateTo);
        }

        // Sorting
        $query->orderBy($this->sortField, $this->sortDirection);

        return view('livewire.order-data-table', [
            'orders' => $query->paginate($this->perPage)
        ]);
    }
}
```

**Code disponible repository complet.**

---

## Projet 1 : User Management DataTable

**Objectif :** DataTable users complète production

**Fonctionnalités :**
- Pagination 10/25/50/100 par page
- Recherche temps réel (nom, email)
- Filtres (rôle, statut, date inscription)
- Sorting toutes colonnes
- Bulk select + actions (activer, désactiver, supprimer)
- Export CSV/Excel filtré
- Cursor pagination (si 100k+ users)
- Eager loading avatar relation
- Query optimization (index DB)

**Code disponible repository.**

---

## Projet 2 : E-commerce Order Manager

**Objectif :** Gestion commandes e-commerce

**Fonctionnalités :**
- Table orders avec customer, items, total
- Recherche (order number, customer name)
- Filtres (status, date range, amount range)
- Sorting (date, total, status)
- Bulk update status
- Export Excel avec formatting
- Statistics row (total orders, revenue)
- Eager load (customer, items, products)
- Cache stats 5 minutes

**Code disponible repository.**

---

## Projet 3 : Log Viewer DataTable

**Objectif :** Visualiseur logs application

**Fonctionnalités :**
- Table logs (millions rows)
- Cursor pagination (performance)
- Recherche fulltext (message, context)
- Filtres (level, date range, user)
- Sorting (timestamp, level)
- Export chunks (éviter memory)
- Color coding levels (error=red, warning=yellow)
- Auto-refresh polling 10s
- DB indexes optimisés

**Code disponible repository.**

---

## Checklist Module VIII

- [ ] `WithPagination` trait pour pagination serveur
- [ ] `paginate()` ou `cursorPaginate()` selon taille table
- [ ] `resetPage()` sur changement filtre/recherche
- [ ] Recherche temps réel avec `.debounce.300ms`
- [ ] Filtres multiples cumulatifs (WHERE clauses)
- [ ] Sorting bidirectionnel (`sortBy()` method)
- [ ] `wire:key` dans boucles table (ID unique)
- [ ] Bulk selection array `$selected`
- [ ] Actions groupées (delete, update status)
- [ ] Export CSV/Excel avec filtres appliqués
- [ ] Chunk processing export grandes tables
- [ ] Eager loading relations (`with()`)
- [ ] Select colonnes spécifiques (performance)
- [ ] Cache queries lourdes
- [ ] Index DB colonnes filtrées/triées

**Concepts clés maîtrisés :**

✅ Pagination serveur optimisée
✅ Recherche temps réel performante
✅ Filtres cumulatifs avancés
✅ Sorting colonnes dynamique
✅ Bulk actions production
✅ Export CSV/Excel
✅ Cursor pagination grandes tables
✅ Query optimization complète
✅ Patterns datatables réutilisables

---

**Module VIII terminé ! 🎉**

**Prochaine étape : Module IX - File Uploads**

Vous maîtrisez maintenant les datatables Livewire production. Le Module IX approfondit les uploads fichiers avec `wire:model`, validation, preview temps réel, upload S3, chunked uploads, images processing et gestion fichiers temporaires.
<br />