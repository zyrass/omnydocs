---
description: "Design patterns, traits réutilisables, component composition, state management, multi-tenant, API integration, architecture patterns"
icon: lucide/book-open-check
tags: ["LIVEWIRE", "PATTERNS", "ARCHITECTURE", "DESIGN-PATTERNS", "MULTI-TENANT", "API"]
---

# XIV — Advanced Patterns & Architecture

<div
  class="omny-meta"
  data-level="🔴 Expert"
  data-duration="8-9 heures"
  data-lessons="9">
</div>

## Vue d'ensemble

!!! quote "Analogie pédagogique"
    _Imaginez un **système de construction modulaire professionnel Lego Technic** : vous construisez machines complexes (applications) avec **briques standardisées réutilisables** (design patterns), **sous-assemblages préfabriqués** (traits), **plans architecturaux éprouvés** (architecture patterns). **Sans patterns** : chaque développeur invente SA méthode construire voiture, résultat chaotique, pièces incompatibles, maintenance cauchemar, nouveau dev perdu (code spaghetti). **Avec patterns professionnels** : **Repository Pattern** = garage organisé avec outils rangés emplacements précis (abstraction data access), **Service Layer Pattern** = chaîne assemblage (business logic centralisée), **Factory Pattern** = moule injection plastique (création objets standardisée), **Observer Pattern** = système alarme interconnecté (événements découplés), **Strategy Pattern** = boîte outils interchangeables (algorithmes swappables). **Architecture multi-tenant** : immeuble bureaux avec locataires isolés (1 app, multiples clients séparés), chaque étage isolé (données, config) mais infrastructure partagée (code, serveurs). **API Integration** : connecteurs standards USB-C (interfaces tierces propres), adaptateurs universels (wrappers services externes). **Component Composition** : briques Lego emboîtables (composants parents/enfants découplés), sous-assemblages réutilisables (traits mixins). **Patterns Livewire fonctionnent exactement pareil** : **Traits réutilisables** (`WithPagination`, `WithFileUploads`, custom traits), **Service Layer** (business logic hors composants), **Repository Pattern** (abstraction queries DB), **Factory Pattern** (création composants dynamiques), **Observer Pattern** (events/listeners découplés), **State Management** (Pinia-like avec Alpine stores), **Multi-tenant** (scopes globaux, config runtime), **API Wrappers** (services tiers encapsulés proprement). C'est la **différence junior vs senior developer** : même résultat fonctionnel, code junior = plat spaghetti, code senior = architecture LEGO modulaire maintenable scalable._

**Les patterns avancés Livewire permettent architecture robuste et maintenable :**

- ✅ **Design Patterns** = Repository, Service, Factory, Observer, Strategy
- ✅ **Traits réutilisables** = Mixins fonctionnalités cross-cutting
- ✅ **Component composition** = Parent/child, slots, dynamic components
- ✅ **State management** = Alpine stores, shared state, reactivity
- ✅ **Multi-tenant architecture** = SaaS isolation données/config
- ✅ **API integration** = Wrappers services tiers, rate limiting
- ✅ **Event-driven architecture** = Decoupling via events
- ✅ **CQRS pattern** = Command/Query separation
- ✅ **Hexagonal architecture** = Ports & adapters

**Ce module couvre :**

1. Repository Pattern (Data Access Layer)
2. Service Layer Pattern (Business Logic)
3. Traits réutilisables avancés
4. Component Composition patterns
5. State Management (Alpine stores)
6. Multi-tenant Architecture
7. API Integration patterns
8. Event-Driven Architecture
9. CQRS et Hexagonal Architecture

---

## Leçon 1 : Repository Pattern

### 1.1 Repository Pattern Concept

**Repository = Abstraction couche accès données (interface entre business logic et DB)**

```
Sans Repository :
Component → Eloquent direct → Database

Avec Repository :
Component → Repository Interface → Repository Implementation → Eloquent → Database

Avantages :
- Testabilité (mock repository)
- Changement DB facile (swap implementation)
- Business logic découplée data access
- Queries complexes centralisées
```

### 1.2 Repository Interface

```php
<?php

namespace App\Contracts;

use Illuminate\Support\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

interface UserRepositoryInterface
{
    /**
     * Récupérer tous users
     */
    public function all(): Collection;

    /**
     * Récupérer user par ID
     */
    public function find(int $id): ?User;

    /**
     * Créer user
     */
    public function create(array $data): User;

    /**
     * Mettre à jour user
     */
    public function update(int $id, array $data): User;

    /**
     * Supprimer user
     */
    public function delete(int $id): bool;

    /**
     * Paginer users
     */
    public function paginate(int $perPage = 15): LengthAwarePaginator;

    /**
     * Rechercher users
     */
    public function search(string $query): Collection;

    /**
     * Récupérer users par rôle
     */
    public function findByRole(string $role): Collection;

    /**
     * Récupérer users actifs
     */
    public function getActive(): Collection;
}
```

### 1.3 Repository Implementation

```php
<?php

namespace App\Repositories;

use App\Contracts\UserRepositoryInterface;
use App\Models\User;
use Illuminate\Support\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

class EloquentUserRepository implements UserRepositoryInterface
{
    protected User $model;

    public function __construct(User $model)
    {
        $this->model = $model;
    }

    public function all(): Collection
    {
        return $this->model->all();
    }

    public function find(int $id): ?User
    {
        return $this->model->find($id);
    }

    public function create(array $data): User
    {
        return $this->model->create($data);
    }

    public function update(int $id, array $data): User
    {
        $user = $this->find($id);
        $user->update($data);
        
        return $user->fresh();
    }

    public function delete(int $id): bool
    {
        $user = $this->find($id);
        
        return $user ? $user->delete() : false;
    }

    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return $this->model->paginate($perPage);
    }

    public function search(string $query): Collection
    {
        return $this->model
            ->where('name', 'like', "%{$query}%")
            ->orWhere('email', 'like', "%{$query}%")
            ->get();
    }

    public function findByRole(string $role): Collection
    {
        return $this->model
            ->where('role', $role)
            ->get();
    }

    public function getActive(): Collection
    {
        return $this->model
            ->where('status', 'active')
            ->get();
    }

    /**
     * Queries complexes encapsulées
     */
    public function getUsersWithRecentActivity(int $days = 7): Collection
    {
        return $this->model
            ->where('last_login_at', '>=', now()->subDays($days))
            ->withCount('posts', 'comments')
            ->orderBy('last_login_at', 'desc')
            ->get();
    }

    public function getTopContributors(int $limit = 10): Collection
    {
        return $this->model
            ->withCount('posts')
            ->orderBy('posts_count', 'desc')
            ->limit($limit)
            ->get();
    }
}
```

### 1.4 Enregistrer Repository (Service Provider)

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Contracts\UserRepositoryInterface;
use App\Repositories\EloquentUserRepository;

class RepositoryServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Binder interface → implementation
        $this->app->bind(
            UserRepositoryInterface::class,
            EloquentUserRepository::class
        );

        // Autres repositories
        $this->app->bind(
            PostRepositoryInterface::class,
            EloquentPostRepository::class
        );

        $this->app->bind(
            OrderRepositoryInterface::class,
            EloquentOrderRepository::class
        );
    }
}
```

**Enregistrer provider `config/app.php` :**

```php
<?php

'providers' => [
    // ...
    App\Providers\RepositoryServiceProvider::class,
],
```

### 1.5 Utilisation Repository dans Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Contracts\UserRepositoryInterface;

class UserManagement extends Component
{
    use WithPagination;

    public string $search = '';
    public string $roleFilter = '';

    protected UserRepositoryInterface $userRepository;

    /**
     * Injection dépendance repository
     */
    public function boot(UserRepositoryInterface $userRepository): void
    {
        $this->userRepository = $userRepository;
    }

    public function deleteUser(int $userId): void
    {
        // Utiliser repository au lieu Eloquent direct
        $this->userRepository->delete($userId);

        session()->flash('message', 'User supprimé.');
    }

    public function render()
    {
        // Query via repository
        if ($this->search) {
            $users = $this->userRepository->search($this->search);
        } elseif ($this->roleFilter) {
            $users = $this->userRepository->findByRole($this->roleFilter);
        } else {
            $users = $this->userRepository->paginate(20);
        }

        return view('livewire.user-management', [
            'users' => $users
        ]);
    }
}
```

**Avantages pattern :**

```php
<?php

// ✅ Testabilité : Mock repository facilement
public function test_user_deletion()
{
    $mockRepo = Mockery::mock(UserRepositoryInterface::class);
    $mockRepo->shouldReceive('delete')->once()->with(1)->andReturn(true);
    
    $this->app->instance(UserRepositoryInterface::class, $mockRepo);
    
    Livewire::test(UserManagement::class)
        ->call('deleteUser', 1);
}

// ✅ Swap implementation : Passer de Eloquent à MongoDB
$this->app->bind(
    UserRepositoryInterface::class,
    MongoUserRepository::class  // Nouvelle implementation
);

// ✅ Queries complexes centralisées
$topContributors = $this->userRepository->getTopContributors(10);
```

---

## Leçon 2 : Service Layer Pattern

### 2.1 Service Layer Concept

**Service = Business logic centralisée (entre Controller/Component et Repository)**

```
Architecture en couches :

Presentation Layer (Livewire Component)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Model Layer (Eloquent)
    ↓
Database
```

### 2.2 Service Example

```php
<?php

namespace App\Services;

use App\Contracts\UserRepositoryInterface;
use App\Contracts\NotificationServiceInterface;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\DB;

class UserService
{
    protected UserRepositoryInterface $userRepository;
    protected NotificationServiceInterface $notificationService;

    public function __construct(
        UserRepositoryInterface $userRepository,
        NotificationServiceInterface $notificationService
    ) {
        $this->userRepository = $userRepository;
        $this->notificationService = $notificationService;
    }

    /**
     * Créer user avec business logic
     */
    public function createUser(array $data): User
    {
        DB::beginTransaction();

        try {
            // Valider données (pourrait être validateur séparé)
            $this->validateUserData($data);

            // Hash password
            $data['password'] = Hash::make($data['password']);

            // Générer username si absent
            if (!isset($data['username'])) {
                $data['username'] = $this->generateUsername($data['name']);
            }

            // Créer user via repository
            $user = $this->userRepository->create($data);

            // Assigner rôle default
            $user->assignRole('user');

            // Envoyer email bienvenue
            $this->notificationService->sendWelcomeEmail($user);

            // Logger action
            activity()
                ->performedOn($user)
                ->causedBy(auth()->user())
                ->log('User créé');

            DB::commit();

            return $user;

        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        }
    }

    /**
     * Mettre à jour profil user
     */
    public function updateProfile(int $userId, array $data): User
    {
        DB::beginTransaction();

        try {
            $user = $this->userRepository->find($userId);

            // Vérifier autorisation
            if (!auth()->user()->can('update', $user)) {
                throw new \Exception('Non autorisé');
            }

            // Si email change, marquer non vérifié
            if (isset($data['email']) && $data['email'] !== $user->email) {
                $data['email_verified_at'] = null;
                $this->notificationService->sendEmailVerification($user);
            }

            // Update via repository
            $user = $this->userRepository->update($userId, $data);

            // Clear cache user
            cache()->forget("user-{$userId}");

            DB::commit();

            return $user;

        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        }
    }

    /**
     * Suspendre user (soft delete + désactiver)
     */
    public function suspendUser(int $userId, string $reason): void
    {
        DB::beginTransaction();

        try {
            $user = $this->userRepository->find($userId);

            // Update status
            $user->update([
                'status' => 'suspended',
                'suspended_at' => now(),
                'suspension_reason' => $reason,
            ]);

            // Révoquer sessions actives
            DB::table('sessions')
                ->where('user_id', $userId)
                ->delete();

            // Notifier user
            $this->notificationService->sendSuspensionNotice($user, $reason);

            // Logger
            activity()
                ->performedOn($user)
                ->causedBy(auth()->user())
                ->withProperties(['reason' => $reason])
                ->log('User suspendu');

            DB::commit();

        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        }
    }

    /**
     * Générer username unique
     */
    protected function generateUsername(string $name): string
    {
        $base = strtolower(str_replace(' ', '', $name));
        $username = $base;
        $counter = 1;

        while ($this->userRepository->findByUsername($username)) {
            $username = $base . $counter;
            $counter++;
        }

        return $username;
    }

    /**
     * Valider données user
     */
    protected function validateUserData(array $data): void
    {
        if (empty($data['email'])) {
            throw new \InvalidArgumentException('Email requis');
        }

        if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Email invalide');
        }

        // Vérifier email unique
        if ($this->userRepository->findByEmail($data['email'])) {
            throw new \InvalidArgumentException('Email déjà utilisé');
        }
    }
}
```

### 2.3 Utilisation Service dans Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\UserService;

class UserRegistration extends Component
{
    public string $name = '';
    public string $email = '';
    public string $password = '';

    protected UserService $userService;

    /**
     * Injection service
     */
    public function boot(UserService $userService): void
    {
        $this->userService = $userService;
    }

    public function register(): void
    {
        // Validation Livewire
        $this->validate([
            'name' => 'required|min:3',
            'email' => 'required|email',
            'password' => 'required|min:8',
        ]);

        try {
            // Business logic dans service (pas composant)
            $user = $this->userService->createUser([
                'name' => $this->name,
                'email' => $this->email,
                'password' => $this->password,
            ]);

            // Login user
            auth()->login($user);

            session()->flash('message', 'Inscription réussie !');

            return redirect()->route('dashboard');

        } catch (\Exception $e) {
            session()->flash('error', $e->getMessage());
        }
    }

    public function render()
    {
        return view('livewire.user-registration');
    }
}
```

### 2.4 Service avec Actions Atomiques

```php
<?php

namespace App\Services;

use App\Contracts\OrderRepositoryInterface;
use App\Contracts\PaymentGatewayInterface;
use App\Models\Order;
use Illuminate\Support\Facades\DB;

class OrderService
{
    protected OrderRepositoryInterface $orderRepository;
    protected PaymentGatewayInterface $paymentGateway;

    public function __construct(
        OrderRepositoryInterface $orderRepository,
        PaymentGatewayInterface $paymentGateway
    ) {
        $this->orderRepository = $orderRepository;
        $this->paymentGateway = $paymentGateway;
    }

    /**
     * Traiter commande (action atomique complexe)
     */
    public function processOrder(array $orderData, array $paymentData): Order
    {
        return DB::transaction(function () use ($orderData, $paymentData) {
            
            // 1. Créer order
            $order = $this->orderRepository->create($orderData);

            // 2. Vérifier stock disponible
            foreach ($order->items as $item) {
                if ($item->product->stock < $item->quantity) {
                    throw new \Exception("Stock insuffisant : {$item->product->name}");
                }
            }

            // 3. Traiter paiement
            $payment = $this->paymentGateway->charge(
                $order->total,
                $paymentData['token']
            );

            if (!$payment['success']) {
                throw new \Exception("Paiement échoué : {$payment['error']}");
            }

            // 4. Déduire stock
            foreach ($order->items as $item) {
                $item->product->decrement('stock', $item->quantity);
            }

            // 5. Update order
            $order->update([
                'status' => 'paid',
                'payment_id' => $payment['transaction_id'],
                'paid_at' => now(),
            ]);

            // 6. Envoyer confirmation
            $order->customer->notify(new OrderConfirmation($order));

            // 7. Logger
            activity()
                ->performedOn($order)
                ->causedBy($order->customer)
                ->log('Order traité avec succès');

            return $order;
        });
    }

    /**
     * Annuler order (rollback complet)
     */
    public function cancelOrder(int $orderId, string $reason): void
    {
        DB::transaction(function () use ($orderId, $reason) {
            
            $order = $this->orderRepository->find($orderId);

            if ($order->status === 'shipped') {
                throw new \Exception('Commande déjà expédiée, annulation impossible');
            }

            // Rembourser si payé
            if ($order->status === 'paid') {
                $this->paymentGateway->refund($order->payment_id);
            }

            // Restaurer stock
            foreach ($order->items as $item) {
                $item->product->increment('stock', $item->quantity);
            }

            // Update order
            $order->update([
                'status' => 'cancelled',
                'cancelled_at' => now(),
                'cancellation_reason' => $reason,
            ]);

            // Notifier
            $order->customer->notify(new OrderCancelled($order, $reason));
        });
    }
}
```

---

## Leçon 3 : Traits Réutilisables Avancés

### 3.1 Trait WithFilters

```php
<?php

namespace App\Livewire\Concerns;

trait WithFilters
{
    public array $filters = [];
    public array $appliedFilters = [];

    /**
     * Initialiser filtres
     */
    public function initializeWithFilters(): void
    {
        $this->filters = $this->getAvailableFilters();
    }

    /**
     * Appliquer filtre
     */
    public function applyFilter(string $key, mixed $value): void
    {
        $this->appliedFilters[$key] = $value;
        $this->resetPage();
    }

    /**
     * Retirer filtre
     */
    public function removeFilter(string $key): void
    {
        unset($this->appliedFilters[$key]);
        $this->resetPage();
    }

    /**
     * Clear tous filtres
     */
    public function clearFilters(): void
    {
        $this->appliedFilters = [];
        $this->resetPage();
    }

    /**
     * Appliquer filtres à query
     */
    protected function applyFiltersToQuery($query)
    {
        foreach ($this->appliedFilters as $key => $value) {
            if (empty($value)) {
                continue;
            }

            $filterMethod = 'filter' . str_replace('_', '', ucwords($key, '_'));

            if (method_exists($this, $filterMethod)) {
                $this->$filterMethod($query, $value);
            } else {
                $query->where($key, $value);
            }
        }

        return $query;
    }

    /**
     * Filtres disponibles (à définir dans composant)
     */
    abstract protected function getAvailableFilters(): array;
}
```

**Utilisation trait :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Livewire\Concerns\WithFilters;
use App\Models\Product;

class ProductCatalog extends Component
{
    use WithPagination, WithFilters;

    protected function getAvailableFilters(): array
    {
        return [
            'category' => Category::pluck('name', 'id'),
            'brand' => Brand::pluck('name', 'id'),
            'price_range' => ['0-50', '50-100', '100-200', '200+'],
            'in_stock' => ['yes' => 'En stock', 'no' => 'Rupture'],
        ];
    }

    /**
     * Filtre custom category
     */
    protected function filterCategory($query, $categoryId)
    {
        $query->where('category_id', $categoryId);
    }

    /**
     * Filtre custom price range
     */
    protected function filterPriceRange($query, $range)
    {
        [$min, $max] = explode('-', $range);
        
        if ($max === '+') {
            $query->where('price', '>=', $min);
        } else {
            $query->whereBetween('price', [$min, $max]);
        }
    }

    /**
     * Filtre custom stock
     */
    protected function filterInStock($query, $value)
    {
        if ($value === 'yes') {
            $query->where('stock', '>', 0);
        } else {
            $query->where('stock', '=', 0);
        }
    }

    public function render()
    {
        $query = Product::query();
        
        // Appliquer filtres via trait
        $query = $this->applyFiltersToQuery($query);

        return view('livewire.product-catalog', [
            'products' => $query->paginate(20)
        ]);
    }
}
```

### 3.2 Trait WithBulkActions

```php
<?php

namespace App\Livewire\Concerns;

trait WithBulkActions
{
    public array $selected = [];
    public bool $selectAll = false;

    /**
     * Toggle select all
     */
    public function updatedSelectAll($value): void
    {
        if ($value) {
            $this->selected = $this->getSelectableIds();
        } else {
            $this->selected = [];
        }
    }

    /**
     * Select item
     */
    public function selectItem(int $id): void
    {
        if (in_array($id, $this->selected)) {
            $this->selected = array_diff($this->selected, [$id]);
        } else {
            $this->selected[] = $id;
        }
    }

    /**
     * Bulk delete
     */
    public function bulkDelete(): void
    {
        if (empty($this->selected)) {
            session()->flash('error', 'Aucun élément sélectionné');
            return;
        }

        $this->performBulkDelete($this->selected);

        session()->flash('message', count($this->selected) . ' élément(s) supprimé(s)');
        
        $this->selected = [];
        $this->selectAll = false;
    }

    /**
     * Bulk update
     */
    public function bulkUpdate(string $field, mixed $value): void
    {
        if (empty($this->selected)) {
            session()->flash('error', 'Aucun élément sélectionné');
            return;
        }

        $this->performBulkUpdate($this->selected, $field, $value);

        session()->flash('message', count($this->selected) . ' élément(s) mis à jour');
        
        $this->selected = [];
        $this->selectAll = false;
    }

    /**
     * Get selectable IDs (à implémenter dans composant)
     */
    abstract protected function getSelectableIds(): array;

    /**
     * Perform bulk delete (à implémenter dans composant)
     */
    abstract protected function performBulkDelete(array $ids): void;

    /**
     * Perform bulk update (à implémenter dans composant)
     */
    abstract protected function performBulkUpdate(array $ids, string $field, mixed $value): void;
}
```

### 3.3 Trait WithExport

```php
<?php

namespace App\Livewire\Concerns;

use Illuminate\Support\Facades\Storage;

trait WithExport
{
    public bool $exporting = false;

    /**
     * Export to CSV
     */
    public function exportCsv(): void
    {
        $this->exporting = true;

        try {
            $data = $this->getExportData();
            $headers = $this->getExportHeaders();

            $csv = $this->generateCsv($headers, $data);

            $filename = $this->getExportFilename() . '.csv';

            return response()->streamDownload(function () use ($csv) {
                echo $csv;
            }, $filename, [
                'Content-Type' => 'text/csv',
            ]);

        } finally {
            $this->exporting = false;
        }
    }

    /**
     * Export to Excel
     */
    public function exportExcel(): void
    {
        $this->exporting = true;

        try {
            $data = $this->getExportData();
            
            // Utiliser Laravel Excel ou autre lib
            $export = new GenericExport($data, $this->getExportHeaders());

            $filename = $this->getExportFilename() . '.xlsx';

            return Excel::download($export, $filename);

        } finally {
            $this->exporting = false;
        }
    }

    /**
     * Generate CSV string
     */
    protected function generateCsv(array $headers, $data): string
    {
        $csv = implode(',', $headers) . "\n";

        foreach ($data as $row) {
            $csv .= implode(',', array_map(fn($v) => '"' . str_replace('"', '""', $v) . '"', $row)) . "\n";
        }

        return $csv;
    }

    /**
     * Get export data (à implémenter dans composant)
     */
    abstract protected function getExportData();

    /**
     * Get export headers (à implémenter dans composant)
     */
    abstract protected function getExportHeaders(): array;

    /**
     * Get export filename
     */
    protected function getExportFilename(): string
    {
        return 'export-' . now()->format('Y-m-d-His');
    }
}
```

### 3.4 Trait WithCaching

```php
<?php

namespace App\Livewire\Concerns;

use Illuminate\Support\Facades\Cache;

trait WithCaching
{
    /**
     * Cache TTL (secondes)
     */
    protected int $cacheTtl = 3600;

    /**
     * Remember cached value
     */
    protected function remember(string $key, callable $callback, ?int $ttl = null)
    {
        return Cache::remember(
            $this->getCacheKey($key),
            $ttl ?? $this->cacheTtl,
            $callback
        );
    }

    /**
     * Remember forever
     */
    protected function rememberForever(string $key, callable $callback)
    {
        return Cache::rememberForever(
            $this->getCacheKey($key),
            $callback
        );
    }

    /**
     * Forget cache key
     */
    protected function forget(string $key): void
    {
        Cache::forget($this->getCacheKey($key));
    }

    /**
     * Flush all cache keys for component
     */
    protected function flushCache(): void
    {
        $prefix = $this->getCachePrefix();
        
        Cache::tags([$prefix])->flush();
    }

    /**
     * Get cache key with prefix
     */
    protected function getCacheKey(string $key): string
    {
        return $this->getCachePrefix() . ':' . $key;
    }

    /**
     * Get cache prefix (based on component class)
     */
    protected function getCachePrefix(): string
    {
        return strtolower(class_basename($this));
    }
}
```

**Utilisation multiple traits :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Livewire\Concerns\WithFilters;
use App\Livewire\Concerns\WithBulkActions;
use App\Livewire\Concerns\WithExport;
use App\Livewire\Concerns\WithCaching;

class AdvancedDataTable extends Component
{
    use WithPagination;
    use WithFilters;
    use WithBulkActions;
    use WithExport;
    use WithCaching;

    // Toutes fonctionnalités traits disponibles automatiquement ✓
}
```

---

## Leçon 4 : Component Composition Patterns

### 4.1 Parent/Child Communication

**Parent Component :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class TodoList extends Component
{
    public array $todos = [];

    public function mount(): void
    {
        $this->todos = Todo::all()->toArray();
    }

    /**
     * Listener enfant dispatch up
     */
    public function todoAdded($todo): void
    {
        $this->todos[] = $todo;
    }

    public function todoDeleted($todoId): void
    {
        $this->todos = array_filter(
            $this->todos,
            fn($todo) => $todo['id'] !== $todoId
        );
    }

    public function render()
    {
        return view('livewire.todo-list');
    }
}
```

```blade
{{-- resources/views/livewire/todo-list.blade.php --}}
<div>
    {{-- Child component (form) --}}
    <livewire:todo-form />

    {{-- List todos --}}
    <ul>
        @foreach($todos as $todo)
            {{-- Child component (item) --}}
            <livewire:todo-item :todo="$todo" :key="$todo['id']" />
        @endforeach
    </ul>
</div>
```

**Child Component (Form) :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class TodoForm extends Component
{
    public string $title = '';

    public function add(): void
    {
        $this->validate(['title' => 'required|min:3']);

        $todo = Todo::create(['title' => $this->title]);

        // Dispatch up vers parent
        $this->dispatch('todoAdded', $todo->toArray())->up();

        $this->reset('title');
    }

    public function render()
    {
        return view('livewire.todo-form');
    }
}
```

**Child Component (Item) :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class TodoItem extends Component
{
    public array $todo;

    public function delete(): void
    {
        Todo::destroy($this->todo['id']);

        // Dispatch up vers parent
        $this->dispatch('todoDeleted', $this->todo['id'])->up();
    }

    public function render()
    {
        return view('livewire.todo-item');
    }
}
```

### 4.2 Slots et Dynamic Components

```blade
{{-- Parent component avec slots --}}
<div class="card">
    {{-- Slot header --}}
    <div class="card-header">
        {{ $header }}
    </div>

    {{-- Slot default (body) --}}
    <div class="card-body">
        {{ $slot }}
    </div>

    {{-- Slot footer (optionnel) --}}
    @if(isset($footer))
        <div class="card-footer">
            {{ $footer }}
        </div>
    @endif
</div>
```

**Utilisation slots :**

```blade
<livewire:card>
    <x-slot:header>
        <h3>Titre Card</h3>
    </x-slot:header>

    <p>Contenu principal card</p>

    <x-slot:footer>
        <button>Action</button>
    </x-slot:footer>
</livewire:card>
```

**Dynamic Component Loading :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class DynamicDashboard extends Component
{
    public array $widgets = [
        'stats' => StatsWidget::class,
        'chart' => ChartWidget::class,
        'activity' => ActivityWidget::class,
    ];

    public array $activeWidgets = ['stats', 'chart'];

    public function toggleWidget(string $widget): void
    {
        if (in_array($widget, $this->activeWidgets)) {
            $this->activeWidgets = array_diff($this->activeWidgets, [$widget]);
        } else {
            $this->activeWidgets[] = $widget;
        }
    }

    public function render()
    {
        return view('livewire.dynamic-dashboard');
    }
}
```

```blade
<div>
    {{-- Widget selector --}}
    <div class="widget-selector">
        @foreach($widgets as $key => $class)
            <button wire:click="toggleWidget('{{ $key }}')">
                Toggle {{ $key }}
            </button>
        @endforeach
    </div>

    {{-- Dynamic widgets --}}
    <div class="widgets-grid">
        @foreach($activeWidgets as $widget)
            @livewire($widgets[$widget], key: $widget)
        @endforeach
    </div>
</div>
```

### 4.3 Renderless Components (Logic Only)

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class FormValidator extends Component
{
    public array $errors = [];

    /**
     * Validate data
     */
    public function validate(array $data, array $rules): bool
    {
        $validator = Validator::make($data, $rules);

        if ($validator->fails()) {
            $this->errors = $validator->errors()->toArray();
            return false;
        }

        $this->errors = [];
        return true;
    }

    /**
     * Pas de vue (renderless)
     */
    public function render()
    {
        return <<<'HTML'
        <div></div>
        HTML;
    }
}
```

**Utilisation renderless component :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class UserForm extends Component
{
    public string $name = '';
    public string $email = '';

    public function submit(): void
    {
        // Utiliser renderless component validation
        $validator = app(FormValidator::class);

        if ($validator->validate(
            ['name' => $this->name, 'email' => $this->email],
            ['name' => 'required|min:3', 'email' => 'required|email']
        )) {
            // Valid, save...
        } else {
            // Invalid, show errors
            session()->flash('errors', $validator->errors);
        }
    }

    public function render()
    {
        return view('livewire.user-form');
    }
}
```

---

## Leçon 5 : State Management (Alpine Stores)

### 5.1 Alpine Global Store

**Définir store global (`resources/js/app.js`) :**

```javascript
import Alpine from 'alpinejs';

// Global cart store
Alpine.store('cart', {
    items: [],
    
    get count() {
        return this.items.reduce((sum, item) => sum + item.quantity, 0);
    },
    
    get total() {
        return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    
    add(product, quantity = 1) {
        const existing = this.items.find(item => item.id === product.id);
        
        if (existing) {
            existing.quantity += quantity;
        } else {
            this.items.push({ ...product, quantity });
        }
        
        this.saveToStorage();
    },
    
    remove(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.saveToStorage();
    },
    
    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = quantity;
            this.saveToStorage();
        }
    },
    
    clear() {
        this.items = [];
        this.saveToStorage();
    },
    
    saveToStorage() {
        localStorage.setItem('cart', JSON.stringify(this.items));
    },
    
    loadFromStorage() {
        const stored = localStorage.getItem('cart');
        if (stored) {
            this.items = JSON.parse(stored);
        }
    },
    
    init() {
        this.loadFromStorage();
    }
});

// Initialize store
Alpine.store('cart').init();

window.Alpine = Alpine;
Alpine.start();
```

**Utilisation store dans Livewire :**

```blade
{{-- Product card --}}
<div x-data>
    <h3>{{ $product->name }}</h3>
    <p>{{ $product->price }}€</p>
    
    {{-- Add to cart (Alpine store) --}}
    <button 
        @click="$store.cart.add({ 
            id: {{ $product->id }}, 
            name: '{{ $product->name }}', 
            price: {{ $product->price }} 
        })"
    >
        Ajouter au panier
    </button>
</div>

{{-- Cart widget (anywhere in app) --}}
<div x-data class="cart-widget">
    <span x-text="$store.cart.count"></span> article(s)
    <span x-text="$store.cart.total + '€'"></span>
</div>
```

### 5.2 Sync Alpine Store ↔ Livewire

**Livewire component :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class ShoppingCart extends Component
{
    public array $items = [];

    public function mount(): void
    {
        // Charger items depuis session
        $this->items = session('cart', []);
    }

    /**
     * Sync depuis Alpine store
     */
    public function syncFromClient(array $items): void
    {
        $this->items = $items;
        session(['cart' => $items]);
    }

    /**
     * Checkout (server-side)
     */
    public function checkout(): void
    {
        // Valider items server-side
        foreach ($this->items as $item) {
            $product = Product::find($item['id']);
            
            if (!$product || $product->price !== $item['price']) {
                session()->flash('error', 'Prix produit modifié');
                return;
            }
        }

        // Créer order...
        
        // Clear cart
        $this->items = [];
        session()->forget('cart');
        
        // Clear Alpine store via JS
        $this->dispatch('cart-cleared');
    }

    public function render()
    {
        return view('livewire.shopping-cart');
    }
}
```

```blade
<div 
    x-data="{
        syncToServer() {
            $wire.syncFromClient($store.cart.items);
        }
    }"
    x-init="
        // Sync vers serveur toutes les 30s
        setInterval(() => syncToServer(), 30000);
    "
    @cart-cleared.window="$store.cart.clear()"
>
    {{-- Cart items --}}
    <template x-for="item in $store.cart.items" :key="item.id">
        <div class="cart-item">
            <span x-text="item.name"></span>
            <span x-text="item.quantity"></span>
            <span x-text="item.price + '€'"></span>
            
            <button @click="$store.cart.remove(item.id)">
                Supprimer
            </button>
        </div>
    </template>

    {{-- Total --}}
    <div class="cart-total">
        Total : <span x-text="$store.cart.total + '€'"></span>
    </div>

    {{-- Checkout --}}
    <button wire:click="checkout">
        Valider commande
    </button>
</div>
```

### 5.3 Persistent State (localStorage)

```javascript
// resources/js/stores/preferences.js

Alpine.store('preferences', {
    theme: 'light',
    language: 'fr',
    notifications: true,
    
    setTheme(theme) {
        this.theme = theme;
        this.save();
        document.documentElement.setAttribute('data-theme', theme);
    },
    
    setLanguage(language) {
        this.language = language;
        this.save();
    },
    
    toggleNotifications() {
        this.notifications = !this.notifications;
        this.save();
    },
    
    save() {
        localStorage.setItem('preferences', JSON.stringify({
            theme: this.theme,
            language: this.language,
            notifications: this.notifications,
        }));
    },
    
    load() {
        const stored = localStorage.getItem('preferences');
        if (stored) {
            const prefs = JSON.parse(stored);
            this.theme = prefs.theme || 'light';
            this.language = prefs.language || 'fr';
            this.notifications = prefs.notifications !== false;
        }
        
        // Apply theme
        document.documentElement.setAttribute('data-theme', this.theme);
    },
    
    init() {
        this.load();
    }
});

Alpine.store('preferences').init();
```

**Utilisation preferences store :**

```blade
<div x-data>
    {{-- Theme toggle --}}
    <button @click="$store.preferences.setTheme($store.preferences.theme === 'light' ? 'dark' : 'light')">
        Toggle theme
    </button>

    {{-- Language selector --}}
    <select @change="$store.preferences.setLanguage($event.target.value)">
        <option value="fr" :selected="$store.preferences.language === 'fr'">Français</option>
        <option value="en" :selected="$store.preferences.language === 'en'">English</option>
    </select>

    {{-- Notifications toggle --}}
    <label>
        <input 
            type="checkbox" 
            :checked="$store.preferences.notifications"
            @change="$store.preferences.toggleNotifications()"
        >
        Activer notifications
    </label>
</div>
```

---

## Leçon 6 : Multi-tenant Architecture

### 6.1 Multi-tenant Database Design

**Approches multi-tenant :**

```
1. Database par tenant (isolation maximale)
   tenant1_db, tenant2_db, tenant3_db...

2. Schema par tenant (PostgreSQL)
   tenant1, tenant2, tenant3... (schemas)

3. Table partagée avec tenant_id (approche commune)
   users: id, tenant_id, name, email...
```

**Migration multi-tenant :**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        // Table tenants
        Schema::create('tenants', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('subdomain')->unique();
            $table->string('database')->nullable();
            $table->json('settings')->nullable();
            $table->boolean('active')->default(true);
            $table->timestamps();
        });

        // Table users (multi-tenant)
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->foreignId('tenant_id')->constrained()->onDelete('cascade');
            $table->string('name');
            $table->string('email');
            $table->string('password');
            $table->timestamps();
            
            // Index tenant
            $table->index('tenant_id');
            $table->unique(['tenant_id', 'email']); // Email unique par tenant
        });

        // Table posts (multi-tenant)
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('tenant_id')->constrained()->onDelete('cascade');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('title');
            $table->text('content');
            $table->timestamps();
            
            $table->index('tenant_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
        Schema::dropIfExists('users');
        Schema::dropIfExists('tenants');
    }
};
```

### 6.2 Tenant Identification Middleware

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use App\Models\Tenant;

class IdentifyTenant
{
    public function handle(Request $request, Closure $next)
    {
        // Méthode 1 : Subdomain
        $subdomain = $this->getSubdomain($request);
        
        if ($subdomain) {
            $tenant = Tenant::where('subdomain', $subdomain)->first();
            
            if (!$tenant || !$tenant->active) {
                abort(404, 'Tenant non trouvé');
            }
            
            // Stocker tenant en session
            app()->instance('tenant', $tenant);
            config(['app.tenant' => $tenant]);
            
            return $next($request);
        }

        // Méthode 2 : Header (API)
        $tenantId = $request->header('X-Tenant-ID');
        
        if ($tenantId) {
            $tenant = Tenant::find($tenantId);
            
            if (!$tenant) {
                return response()->json(['error' => 'Invalid tenant'], 400);
            }
            
            app()->instance('tenant', $tenant);
            
            return $next($request);
        }

        abort(400, 'Tenant non identifié');
    }

    protected function getSubdomain(Request $request): ?string
    {
        $host = $request->getHost();
        $parts = explode('.', $host);
        
        // Si >= 3 parties (subdomain.domain.tld)
        if (count($parts) >= 3) {
            return $parts[0];
        }
        
        return null;
    }
}
```

**Enregistrer middleware :**

```php
<?php

// app/Http/Kernel.php

protected $middlewareGroups = [
    'web' => [
        // ...
        \App\Http\Middleware\IdentifyTenant::class,
    ],
];
```

### 6.3 Global Tenant Scope

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class TenantScope implements Scope
{
    /**
     * Apply scope automatiquement à TOUTES queries
     */
    public function apply(Builder $builder, Model $model): void
    {
        $tenant = app('tenant');
        
        if ($tenant) {
            $builder->where($model->getTable() . '.tenant_id', $tenant->id);
        }
    }
}
```

**Appliquer scope global à modèle :**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use App\Models\Scopes\TenantScope;

class Post extends Model
{
    protected static function booted()
    {
        // Appliquer TenantScope automatiquement
        static::addGlobalScope(new TenantScope);

        // Auto-assign tenant_id à la création
        static::creating(function (Post $post) {
            $tenant = app('tenant');
            
            if ($tenant && !$post->tenant_id) {
                $post->tenant_id = $tenant->id;
            }
        });
    }
}
```

**Résultat :**

```php
<?php

// TOUTES queries automatiquement scopées par tenant

Post::all();
// SELECT * FROM posts WHERE tenant_id = 1

Post::where('published', true)->get();
// SELECT * FROM posts WHERE tenant_id = 1 AND published = 1

// Bypass scope si nécessaire (admin)
Post::withoutGlobalScope(TenantScope::class)->get();
// SELECT * FROM posts (tous tenants)
```

### 6.4 Tenant-aware Livewire Component

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\WithPagination;
use App\Models\Post;

class TenantPosts extends Component
{
    use WithPagination;

    /**
     * Queries automatiquement scopées par TenantScope ✓
     */
    public function render()
    {
        return view('livewire.tenant-posts', [
            'posts' => Post::latest()->paginate(20)
            // Query : WHERE tenant_id = {current_tenant}
        ]);
    }

    public function createPost(): void
    {
        $post = Post::create([
            'title' => 'New Post',
            'content' => 'Content',
            // tenant_id auto-assigné via model event ✓
        ]);
    }
}
```

### 6.5 Tenant Configuration Override

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tenant extends Model
{
    protected $casts = [
        'settings' => 'array',
    ];

    /**
     * Appliquer settings tenant à config runtime
     */
    public function applySettings(): void
    {
        $settings = $this->settings ?? [];

        // Override config app
        if (isset($settings['app_name'])) {
            config(['app.name' => $settings['app_name']]);
        }

        // Override config mail
        if (isset($settings['mail_from'])) {
            config(['mail.from.address' => $settings['mail_from']['address']]);
            config(['mail.from.name' => $settings['mail_from']['name']]);
        }

        // Override config services (Stripe, etc.)
        if (isset($settings['stripe_key'])) {
            config(['services.stripe.key' => $settings['stripe_key']]);
        }
    }
}
```

**Appliquer settings dans middleware :**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class IdentifyTenant
{
    public function handle(Request $request, Closure $next)
    {
        // Identifier tenant...
        $tenant = Tenant::where('subdomain', $subdomain)->first();
        
        app()->instance('tenant', $tenant);
        
        // Appliquer settings tenant
        $tenant->applySettings();
        
        return $next($request);
    }
}
```

---

## Leçon 7 : API Integration Patterns

### 7.1 API Wrapper Service

```php
<?php

namespace App\Services\External;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;

class StripeService
{
    protected string $apiKey;
    protected string $baseUrl = 'https://api.stripe.com/v1';

    public function __construct()
    {
        $this->apiKey = config('services.stripe.secret');
    }

    /**
     * Create payment intent
     */
    public function createPaymentIntent(int $amount, string $currency = 'eur'): array
    {
        $response = Http::withHeaders([
            'Authorization' => 'Bearer ' . $this->apiKey,
        ])->post($this->baseUrl . '/payment_intents', [
            'amount' => $amount,
            'currency' => $currency,
        ]);

        if ($response->failed()) {
            throw new \Exception('Stripe API error: ' . $response->json()['error']['message']);
        }

        return $response->json();
    }

    /**
     * Retrieve customer
     */
    public function getCustomer(string $customerId): array
    {
        // Cache customer data 1 heure
        return Cache::remember("stripe-customer-{$customerId}", 3600, function () use ($customerId) {
            $response = Http::withHeaders([
                'Authorization' => 'Bearer ' . $this->apiKey,
            ])->get($this->baseUrl . "/customers/{$customerId}");

            if ($response->failed()) {
                throw new \Exception('Customer not found');
            }

            return $response->json();
        });
    }

    /**
     * Create refund
     */
    public function refund(string $paymentIntentId, ?int $amount = null): array
    {
        $data = ['payment_intent' => $paymentIntentId];
        
        if ($amount) {
            $data['amount'] = $amount;
        }

        $response = Http::withHeaders([
            'Authorization' => 'Bearer ' . $this->apiKey,
        ])->post($this->baseUrl . '/refunds', $data);

        if ($response->failed()) {
            throw new \Exception('Refund failed: ' . $response->json()['error']['message']);
        }

        return $response->json();
    }
}
```

### 7.2 Rate Limiting API Calls

```php
<?php

namespace App\Services\External;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\RateLimiter;

class ExternalApiService
{
    protected string $baseUrl;
    protected string $apiKey;

    /**
     * Make rate-limited API call
     */
    protected function rateLimitedRequest(string $method, string $endpoint, array $data = [])
    {
        $key = 'api-call:external-service';

        // Limiter : 100 requêtes par minute
        if (RateLimiter::tooManyAttempts($key, 100)) {
            $seconds = RateLimiter::availableIn($key);
            
            throw new \Exception("Rate limit atteint. Réessayez dans {$seconds}s");
        }

        RateLimiter::hit($key, 60);

        // Make request
        $response = Http::withHeaders([
            'Authorization' => 'Bearer ' . $this->apiKey,
        ])->$method($this->baseUrl . $endpoint, $data);

        if ($response->failed()) {
            throw new \Exception('API error: ' . $response->body());
        }

        return $response->json();
    }

    public function get(string $endpoint)
    {
        return $this->rateLimitedRequest('get', $endpoint);
    }

    public function post(string $endpoint, array $data)
    {
        return $this->rateLimitedRequest('post', $endpoint, $data);
    }
}
```

### 7.3 Retry Failed Requests

```php
<?php

namespace App\Services\External;

use Illuminate\Support\Facades\Http;

class ResilientApiService
{
    protected int $maxRetries = 3;
    protected int $retryDelay = 1000; // milliseconds

    /**
     * Make request avec retry automatique
     */
    protected function makeRequest(string $method, string $url, array $data = [])
    {
        $attempt = 0;

        while ($attempt < $this->maxRetries) {
            try {
                $response = Http::timeout(10)
                    ->$method($url, $data);

                if ($response->successful()) {
                    return $response->json();
                }

                // Si 5xx, retry
                if ($response->serverError()) {
                    $attempt++;
                    
                    if ($attempt < $this->maxRetries) {
                        // Exponential backoff
                        usleep($this->retryDelay * pow(2, $attempt - 1) * 1000);
                        continue;
                    }
                }

                // Autre erreur (4xx), ne pas retry
                throw new \Exception('API error: ' . $response->body());

            } catch (\Illuminate\Http\Client\ConnectionException $e) {
                $attempt++;
                
                if ($attempt >= $this->maxRetries) {
                    throw new \Exception('API unavailable after ' . $this->maxRetries . ' attempts');
                }

                usleep($this->retryDelay * pow(2, $attempt - 1) * 1000);
            }
        }

        throw new \Exception('Max retries exceeded');
    }
}
```

### 7.4 API Response Caching

```php
<?php

namespace App\Services\External;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;

class CachedApiService
{
    /**
     * Get avec cache
     */
    public function getCached(string $endpoint, int $ttl = 3600)
    {
        $cacheKey = 'api:' . md5($endpoint);

        return Cache::remember($cacheKey, $ttl, function () use ($endpoint) {
            return $this->get($endpoint);
        });
    }

    /**
     * Invalidate cache
     */
    public function invalidateCache(string $endpoint): void
    {
        $cacheKey = 'api:' . md5($endpoint);
        Cache::forget($cacheKey);
    }

    /**
     * Get fresh (bypass cache)
     */
    public function getFresh(string $endpoint)
    {
        $this->invalidateCache($endpoint);
        return $this->getCached($endpoint);
    }
}
```

### 7.5 Utilisation API Service dans Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\External\StripeService;

class PaymentForm extends Component
{
    public float $amount = 0;
    public ?array $paymentIntent = null;

    protected StripeService $stripe;

    public function boot(StripeService $stripe): void
    {
        $this->stripe = $stripe;
    }

    public function createIntent(): void
    {
        try {
            // API call via service wrapper
            $this->paymentIntent = $this->stripe->createPaymentIntent(
                (int) ($this->amount * 100), // Convert to cents
                'eur'
            );

            session()->flash('message', 'Payment intent créé');

        } catch (\Exception $e) {
            session()->flash('error', $e->getMessage());
        }
    }

    public function render()
    {
        return view('livewire.payment-form');
    }
}
```

---

## Leçon 8 : Event-Driven Architecture

### 8.1 Domain Events

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderPlaced
{
    use Dispatchable, SerializesModels;

    public Order $order;

    public function __construct(Order $order)
    {
        $this->order = $order;
    }
}

class OrderPaid
{
    use Dispatchable, SerializesModels;

    public Order $order;
    public string $transactionId;

    public function __construct(Order $order, string $transactionId)
    {
        $this->order = $order;
        $this->transactionId = $transactionId;
    }
}

class OrderShipped
{
    use Dispatchable, SerializesModels;

    public Order $order;
    public string $trackingNumber;

    public function __construct(Order $order, string $trackingNumber)
    {
        $this->order = $order;
        $this->trackingNumber = $trackingNumber;
    }
}
```

### 8.2 Event Listeners

```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Notifications\OrderConfirmation;

class SendOrderConfirmation
{
    public function handle(OrderPlaced $event): void
    {
        $event->order->customer->notify(
            new OrderConfirmation($event->order)
        );
    }
}

class UpdateInventory
{
    public function handle(OrderPlaced $event): void
    {
        foreach ($event->order->items as $item) {
            $item->product->decrement('stock', $item->quantity);
        }
    }
}

class CreateInvoice
{
    public function handle(OrderPaid $event): void
    {
        Invoice::create([
            'order_id' => $event->order->id,
            'transaction_id' => $event->transactionId,
            'amount' => $event->order->total,
            'issued_at' => now(),
        ]);
    }
}
```

### 8.3 Enregistrer Listeners

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        OrderPlaced::class => [
            SendOrderConfirmation::class,
            UpdateInventory::class,
        ],

        OrderPaid::class => [
            CreateInvoice::class,
            SendPaymentReceipt::class,
        ],

        OrderShipped::class => [
            SendShippingNotification::class,
            UpdateOrderStatus::class,
        ],
    ];
}
```

### 8.4 Dispatcher Events dans Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\OrderService;
use App\Events\OrderPlaced;

class Checkout extends Component
{
    public array $cart = [];
    public array $shippingAddress = [];

    protected OrderService $orderService;

    public function boot(OrderService $orderService): void
    {
        $this->orderService = $orderService;
    }

    public function placeOrder(): void
    {
        $this->validate([
            'shippingAddress.name' => 'required',
            'shippingAddress.address' => 'required',
        ]);

        try {
            // Create order via service
            $order = $this->orderService->createOrder([
                'items' => $this->cart,
                'shipping_address' => $this->shippingAddress,
            ]);

            // Dispatch domain event (déclenche listeners)
            event(new OrderPlaced($order));

            session()->flash('message', 'Commande créée !');
            
            return redirect()->route('order.success', $order);

        } catch (\Exception $e) {
            session()->flash('error', $e->getMessage());
        }
    }

    public function render()
    {
        return view('livewire.checkout');
    }
}
```

### 8.5 Event Subscribers (Multiple Events)

```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Events\OrderPaid;
use App\Events\OrderShipped;
use Illuminate\Events\Dispatcher;

class OrderEventSubscriber
{
    /**
     * Register event listeners
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            OrderPlaced::class => 'handleOrderPlaced',
            OrderPaid::class => 'handleOrderPaid',
            OrderShipped::class => 'handleOrderShipped',
        ];
    }

    public function handleOrderPlaced(OrderPlaced $event): void
    {
        // Logger event
        activity()
            ->performedOn($event->order)
            ->log('Order placed');
    }

    public function handleOrderPaid(OrderPaid $event): void
    {
        activity()
            ->performedOn($event->order)
            ->withProperties(['transaction_id' => $event->transactionId])
            ->log('Order paid');
    }

    public function handleOrderShipped(OrderShipped $event): void
    {
        activity()
            ->performedOn($event->order)
            ->withProperties(['tracking' => $event->trackingNumber])
            ->log('Order shipped');
    }
}
```

**Enregistrer subscriber :**

```php
<?php

// app/Providers/EventServiceProvider.php

protected $subscribe = [
    OrderEventSubscriber::class,
];
```

---

## Leçon 9 : CQRS et Hexagonal Architecture

### 9.1 CQRS Pattern (Command Query Separation)

**Commands (Write) :**

```php
<?php

namespace App\Commands;

class CreateUserCommand
{
    public string $name;
    public string $email;
    public string $password;

    public function __construct(string $name, string $email, string $password)
    {
        $this->name = $name;
        $this->email = $email;
        $this->password = $password;
    }
}

class UpdateUserCommand
{
    public int $userId;
    public array $data;

    public function __construct(int $userId, array $data)
    {
        $this->userId = $userId;
        $this->data = $data;
    }
}
```

**Command Handlers :**

```php
<?php

namespace App\Handlers;

use App\Commands\CreateUserCommand;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class CreateUserHandler
{
    public function handle(CreateUserCommand $command): User
    {
        return User::create([
            'name' => $command->name,
            'email' => $command->email,
            'password' => Hash::make($command->password),
        ]);
    }
}
```

**Queries (Read) :**

```php
<?php

namespace App\Queries;

class GetUserQuery
{
    public int $userId;

    public function __construct(int $userId)
    {
        $this->userId = $userId;
    }
}

class GetActiveUsersQuery
{
    public ?string $role;

    public function __construct(?string $role = null)
    {
        $this->role = $role;
    }
}
```

**Query Handlers :**

```php
<?php

namespace App\Handlers;

use App\Queries\GetUserQuery;
use App\Models\User;

class GetUserHandler
{
    public function handle(GetUserQuery $query): ?User
    {
        return User::find($query->userId);
    }
}

class GetActiveUsersHandler
{
    public function handle(GetActiveUsersQuery $query)
    {
        $users = User::where('status', 'active');

        if ($query->role) {
            $users->where('role', $query->role);
        }

        return $users->get();
    }
}
```

**Command/Query Bus :**

```php
<?php

namespace App\Services;

class CommandBus
{
    public function dispatch($command)
    {
        $handlerClass = $this->getHandlerClass($command);
        $handler = app($handlerClass);
        
        return $handler->handle($command);
    }

    protected function getHandlerClass($command): string
    {
        $commandClass = get_class($command);
        return str_replace('Commands', 'Handlers', $commandClass) . 'Handler';
    }
}
```

**Utilisation CQRS dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Services\CommandBus;
use App\Commands\CreateUserCommand;
use App\Queries\GetActiveUsersQuery;

class UserManagement extends Component
{
    public string $name = '';
    public string $email = '';
    public string $password = '';

    protected CommandBus $commandBus;

    public function boot(CommandBus $commandBus): void
    {
        $this->commandBus = $commandBus;
    }

    public function createUser(): void
    {
        // Dispatch command
        $user = $this->commandBus->dispatch(
            new CreateUserCommand($this->name, $this->email, $this->password)
        );

        session()->flash('message', 'User créé');
        $this->reset(['name', 'email', 'password']);
    }

    public function render()
    {
        // Dispatch query
        $users = $this->commandBus->dispatch(
            new GetActiveUsersQuery()
        );

        return view('livewire.user-management', [
            'users' => $users
        ]);
    }
}
```

### 9.2 Hexagonal Architecture (Ports & Adapters)

**Port (Interface) :**

```php
<?php

namespace App\Ports;

interface PaymentGatewayPort
{
    public function charge(int $amount, string $token): array;
    public function refund(string $transactionId, ?int $amount = null): array;
}
```

**Adapters (Implementations) :**

```php
<?php

namespace App\Adapters;

use App\Ports\PaymentGatewayPort;

class StripeAdapter implements PaymentGatewayPort
{
    public function charge(int $amount, string $token): array
    {
        // Stripe-specific implementation
        $stripe = new \Stripe\StripeClient(config('services.stripe.secret'));
        
        $intent = $stripe->paymentIntents->create([
            'amount' => $amount,
            'currency' => 'eur',
            'payment_method' => $token,
            'confirm' => true,
        ]);

        return [
            'success' => $intent->status === 'succeeded',
            'transaction_id' => $intent->id,
        ];
    }

    public function refund(string $transactionId, ?int $amount = null): array
    {
        $stripe = new \Stripe\StripeClient(config('services.stripe.secret'));
        
        $refund = $stripe->refunds->create([
            'payment_intent' => $transactionId,
            'amount' => $amount,
        ]);

        return [
            'success' => $refund->status === 'succeeded',
            'refund_id' => $refund->id,
        ];
    }
}

class PayPalAdapter implements PaymentGatewayPort
{
    public function charge(int $amount, string $token): array
    {
        // PayPal-specific implementation
        // ...
    }

    public function refund(string $transactionId, ?int $amount = null): array
    {
        // PayPal-specific implementation
        // ...
    }
}
```

**Binder adapter dans Service Provider :**

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Ports\PaymentGatewayPort;
use App\Adapters\StripeAdapter;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Swap adapter facilement
        $this->app->bind(
            PaymentGatewayPort::class,
            StripeAdapter::class  // ou PayPalAdapter::class
        );
    }
}
```

**Utilisation port dans Livewire :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Ports\PaymentGatewayPort;

class PaymentForm extends Component
{
    public float $amount = 0;
    public string $token = '';

    protected PaymentGatewayPort $paymentGateway;

    public function boot(PaymentGatewayPort $paymentGateway): void
    {
        $this->paymentGateway = $paymentGateway;
    }

    public function processPayment(): void
    {
        try {
            // Utiliser port (adapter swap transparent)
            $result = $this->paymentGateway->charge(
                (int) ($this->amount * 100),
                $this->token
            );

            if ($result['success']) {
                session()->flash('message', 'Paiement réussi !');
            } else {
                session()->flash('error', 'Paiement échoué');
            }

        } catch (\Exception $e) {
            session()->flash('error', $e->getMessage());
        }
    }

    public function render()
    {
        return view('livewire.payment-form');
    }
}
```

---

## Projet 1 : Multi-tenant SaaS Platform

**Objectif :** Plateforme SaaS complète multi-tenant

**Architecture :**

- Tenant identification subdomain
- Global tenant scope modèles
- Settings runtime par tenant
- Isolation données stricte
- Admin panel super-admin
- Tenant dashboard

**Fonctionnalités :**

- CRUD users par tenant
- Plans/subscriptions
- Billing Stripe
- Custom branding par tenant
- Analytics par tenant
- API multi-tenant

**Code disponible repository.**

---

## Projet 2 : E-commerce Event-Driven

**Objectif :** E-commerce architecture event-driven

**Patterns appliqués :**

- Repository pattern (data access)
- Service layer (business logic)
- CQRS (commands/queries)
- Domain events
- Event subscribers
- Hexagonal architecture (payment ports)

**Features :**

- Order placement (events cascade)
- Payment processing (Stripe adapter)
- Inventory management (event-driven)
- Notification system (listeners)
- Invoice generation (OrderPaid event)
- Shipping tracking (OrderShipped event)

**Code disponible repository.**

---

## Projet 3 : Advanced Component Library

**Objectif :** Bibliothèque composants réutilisables

**Components :**

- DataTable (traits: pagination, filters, bulk, export)
- Form Builder (dynamic fields, validation)
- Modal Manager (dynamic modals)
- Notification Center (Alpine store)
- File Manager (upload, preview, organize)
- Wizard (multi-step, state persistence)

**Traits réutilisables :**

- WithFilters
- WithBulkActions
- WithExport
- WithCaching
- WithSorting

**Code disponible repository.**

---

## Checklist Module XIV

- [ ] Repository pattern implémenté (interfaces)
- [ ] Service layer business logic centralisée
- [ ] Traits réutilisables créés
- [ ] Component composition maîtrisée
- [ ] Alpine stores state management
- [ ] Multi-tenant architecture (scope global)
- [ ] API wrappers services tiers
- [ ] Rate limiting API calls
- [ ] Domain events définis
- [ ] Event listeners enregistrés
- [ ] CQRS pattern appliqué (commands/queries)
- [ ] Hexagonal architecture (ports/adapters)

**Concepts clés maîtrisés :**

✅ Design patterns professionnels
✅ Architecture en couches
✅ Traits réutilisables avancés
✅ Component composition
✅ State management global
✅ Multi-tenant SaaS
✅ API integration propre
✅ Event-driven architecture
✅ CQRS et Hexagonal
✅ Patterns production scalables

---

**Module XIV terminé ! 🎉**

**Formation Livewire COMPLÈTE - 14 modules terminés !** 🏆

**Tu as maintenant une formation Livewire EXHAUSTIVE et PROFESSIONNELLE couvrant TOUS les aspects essentiels + patterns architecturaux avancés !**

Prêt pour le **Module XV** (dernier module bonus) ou veux-tu que je crée l'**index final complet** de toute la formation ? 🚀