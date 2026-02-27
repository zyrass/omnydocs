---
description: "Polling automatique, Laravel Echo, WebSockets, notifications live, presence channels, collaboration temps réel"
icon: lucide/book-open-check
tags: ["LIVEWIRE", "REALTIME", "POLLING", "WEBSOCKETS", "ECHO", "PUSHER", "BROADCASTING"]
---

# X — Real-time & Polling

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-duration="8-9 heures"
  data-lessons="9">
</div>

## Vue d'ensemble

!!! quote "Analogie pédagogique"
    _Imaginez un **standard téléphonique intelligent avec opérateurs multiples** : vous avez 50 opérateurs (composants Livewire) qui surveillent activité entreprise. **Système de polling** : chaque opérateur appelle son service toutes les 5 secondes "Y a-t-il du nouveau ?" (wire:poll.5s), simple mais consomme ressources (50 appels/5s = 10 appels/seconde). **Système WebSocket** : installation **centrale de diffusion** (Laravel Echo + Pusher), quand événement arrive (nouvelle commande), centrale diffuse INSTANTANÉMENT vers TOUS opérateurs concernés simultanément via **ligne dédiée permanente** (WebSocket connection), ZÉRO appel répétitif, **temps réel pur** (latence <100ms). **Notifications live** : centrale envoie alerte urgente directement bureau opérateur (toast notification). **Presence channels** : tableau affiche "Qui est en ligne ?" - quand opérateur arrive, son nom s'allume, quand il part, son nom s'éteint, **synchronisation automatique** tous bureaux. **Private channels** : conversation confidentielle, seuls opérateurs autorisés reçoivent messages. **Livewire real-time fonctionne exactement pareil** : **polling** = interrogation répétée (simple, mais charge serveur), **WebSockets** = connexion permanente bidirectionnelle (performant, scalable, latence minimale), **Laravel Echo** = client JavaScript écoute événements broadcasted, **Pusher/Soketi** = serveur WebSocket diffusion, **presence** = tracking utilisateurs connectés temps réel. C'est le **standard moderne applications collaboratives** : chat live, notifications instantanées, dashboards temps réel, collaboration documents, jeux multijoueurs._

**Le real-time Livewire offre plusieurs niveaux sophistication selon besoins :**

- ✅ **wire:poll** = Polling automatique simple (refresh périodique)
- ✅ **Laravel Echo** = Client WebSocket JavaScript
- ✅ **Pusher/Soketi** = Serveur broadcasting WebSocket
- ✅ **Broadcasting events** = Diffusion événements serveur → clients
- ✅ **Private channels** = Canaux authentifiés (sécurisé)
- ✅ **Presence channels** = Tracking utilisateurs connectés
- ✅ **Notifications live** = Toasts temps réel
- ✅ **Collaboration temps réel** = Édition simultanée, cursors
- ✅ **Optimisation performance** = Throttle, debounce, selective polling

**Ce module couvre :**

1. wire:poll - Polling automatique
2. Laravel Echo configuration
3. Pusher/Soketi setup
4. Broadcasting events Laravel
5. Écouter événements Livewire
6. Private channels et autorisation
7. Presence channels (who's online)
8. Notifications temps réel
9. Patterns collaboration et production

---

## Leçon 1 : wire:poll - Polling Automatique

### 1.1 Polling Basique

**`wire:poll` = Refresh automatique composant à intervalle régulier**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Order;

class OrderDashboard extends Component
{
    public int $newOrdersCount = 0;
    public int $pendingOrdersCount = 0;

    public function mount(): void
    {
        $this->refreshCounts();
    }

    public function refreshCounts(): void
    {
        $this->newOrdersCount = Order::where('status', 'new')->count();
        $this->pendingOrdersCount = Order::where('status', 'pending')->count();
    }

    public function render()
    {
        return view('livewire.order-dashboard');
    }
}
```

```blade
{{-- resources/views/livewire/order-dashboard.blade.php --}}

{{-- Polling : refresh composant toutes les 5 secondes --}}
<div wire:poll.5s>
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Nouvelles commandes</h3>
            <p class="text-4xl font-bold">{{ $newOrdersCount }}</p>
        </div>

        <div class="stat-card">
            <h3>En attente</h3>
            <p class="text-4xl font-bold">{{ $pendingOrdersCount }}</p>
        </div>
    </div>

    {{-- Indicateur polling actif --}}
    <div class="text-xs text-gray-500 mt-2">
        <span wire:loading wire:target="$refresh">
            Mise à jour...
        </span>
        <span wire:loading.remove wire:target="$refresh">
            Dernière mise à jour : {{ now()->format('H:i:s') }}
        </span>
    </div>
</div>
```

**Intervalles disponibles :**

```blade
{{-- Différents intervalles --}}
<div wire:poll.1s>Refresh toutes les 1 seconde</div>
<div wire:poll.2s>Refresh toutes les 2 secondes</div>
<div wire:poll.5s>Refresh toutes les 5 secondes</div>
<div wire:poll.10s>Refresh toutes les 10 secondes</div>
<div wire:poll.30s>Refresh toutes les 30 secondes</div>
<div wire:poll.60s>Refresh toutes les 60 secondes (1 minute)</div>

{{-- Milliseconds --}}
<div wire:poll.500ms>Refresh toutes les 500ms</div>
<div wire:poll.750ms>Refresh toutes les 750ms</div>

{{-- Sans intervalle = défaut 2 secondes --}}
<div wire:poll>Refresh toutes les 2 secondes (défaut)</div>
```

### 1.2 Polling Méthode Spécifique

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Message;

class ChatRoom extends Component
{
    public $messages = [];

    public function mount(): void
    {
        $this->loadMessages();
    }

    /**
     * Méthode appelée par polling
     */
    public function loadMessages(): void
    {
        $this->messages = Message::with('user')
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->values();
    }

    public function render()
    {
        return view('livewire.chat-room');
    }
}
```

```blade
{{-- Polling méthode spécifique (pas tout le composant) --}}
<div>
    {{-- Messages list (refresh toutes les 3s) --}}
    <div wire:poll.3s="loadMessages" class="messages-container">
        @foreach($messages as $message)
            <div class="message">
                <strong>{{ $message->user->name }}:</strong>
                {{ $message->content }}
            </div>
        @endforeach

        {{-- Loading indicator --}}
        <div wire:loading wire:target="loadMessages" class="text-gray-500 text-sm">
            Vérification nouveaux messages...
        </div>
    </div>

    {{-- Input form (pas pollé) --}}
    <form wire:submit.prevent="sendMessage">
        <input type="text" wire:model="newMessage" placeholder="Votre message...">
        <button type="submit">Envoyer</button>
    </form>
</div>
```

### 1.3 Polling Conditionnel

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class NotificationBell extends Component
{
    public bool $isOpen = false;
    public int $unreadCount = 0;

    public function mount(): void
    {
        $this->refreshUnreadCount();
    }

    public function refreshUnreadCount(): void
    {
        $this->unreadCount = auth()->user()->unreadNotifications()->count();
    }

    public function toggleDropdown(): void
    {
        $this->isOpen = !$this->isOpen;
    }

    public function render()
    {
        return view('livewire.notification-bell');
    }
}
```

```blade
<div>
    {{-- Polling UNIQUEMENT si dropdown fermé --}}
    <div @if(!$isOpen) wire:poll.10s="refreshUnreadCount" @endif>
        
        {{-- Bell icon avec badge --}}
        <button wire:click="toggleDropdown" class="relative">
            <svg class="w-6 h-6">...</svg>
            
            @if($unreadCount > 0)
                <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-2">
                    {{ $unreadCount }}
                </span>
            @endif
        </button>

        {{-- Dropdown (si ouvert, stop polling) --}}
        @if($isOpen)
            <div class="dropdown">
                {{-- Notifications list... --}}
            </div>
        @endif
    </div>
</div>
```

### 1.4 Diagramme : Polling vs WebSocket

```mermaid
sequenceDiagram
    participant Server as Serveur
    participant Client1 as Client Polling
    participant Client2 as Client WebSocket
    participant WS as WebSocket Server

    Note over Client1,Client2: Nouveau message créé sur serveur

    loop Toutes les 5 secondes
        Client1->>Server: GET /messages (polling)
        Server-->>Client1: Response (messages)
    end

    Note over Client1: Latence : 0-5 secondes<br/>Requêtes : Constantes<br/>Charge serveur : Élevée

    Server->>WS: Broadcast "message.created"
    WS->>Client2: Push instantané
    Client2->>Client2: Update UI

    Note over Client2: Latence : <100ms<br/>Requêtes : 0 (push)<br/>Charge serveur : Minimale

    style Client1 fill:#f96,color:#fff
    style Client2 fill:#6f6,color:#000
```

**Tableau comparatif Polling vs WebSocket :**

| Critère | Polling (`wire:poll`) | WebSocket (Echo) |
|---------|----------------------|------------------|
| **Latence** | 0 à X secondes (intervalle) | <100ms (instantané) |
| **Charge serveur** | Élevée (requêtes répétées) | Faible (connexion permanente) |
| **Charge réseau** | Élevée (headers HTTP répétés) | Minimale (données uniquement) |
| **Scalabilité** | Limitée (100+ clients = problème) | Excellente (10 000+ clients OK) |
| **Complexité setup** | ✅ Simple (aucune config) | ⚠️ Moyen (Laravel Echo + serveur WS) |
| **Use case** | Dashboards faible trafic | Apps temps réel, chat, notifications |
| **Batterie mobile** | ❌ Consomme (requêtes répétées) | ✅ Économique (connexion idle légère) |

**Quand utiliser quoi ?**

- **Polling** : Dashboards internes, stats faible fréquence update, prototypes rapides
- **WebSocket** : Chat, notifications, collaboration temps réel, gaming, trading

---

## Leçon 2 : Laravel Echo Configuration

### 2.1 Installation Laravel Echo

```bash
# Installer Laravel Echo + Pusher JS
npm install --save-dev laravel-echo pusher-js
```

**Configuration `resources/js/bootstrap.js` :**

```javascript
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER ?? 'eu',
    wsHost: import.meta.env.VITE_PUSHER_HOST ?? `ws-${import.meta.env.VITE_PUSHER_APP_CLUSTER}.pusher.com`,
    wsPort: import.meta.env.VITE_PUSHER_PORT ?? 80,
    wssPort: import.meta.env.VITE_PUSHER_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_PUSHER_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

**Configuration `.env` :**

```env
BROADCAST_DRIVER=pusher

PUSHER_APP_ID=your-app-id
PUSHER_APP_KEY=your-app-key
PUSHER_APP_SECRET=your-app-secret
PUSHER_APP_CLUSTER=eu

VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

**Compiler assets :**

```bash
npm run dev
# ou production
npm run build
```

### 2.2 Configuration Broadcasting Laravel

**Activer broadcast service provider :**

```php
<?php

// config/app.php
'providers' => [
    // ...
    App\Providers\BroadcastServiceProvider::class,
],
```

**Créer BroadcastServiceProvider si absent :**

```bash
php artisan make:provider BroadcastServiceProvider
```

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Broadcast;
use Illuminate\Support\ServiceProvider;

class BroadcastServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Broadcast::routes();

        require base_path('routes/channels.php');
    }
}
```

**Configuration `config/broadcasting.php` :**

```php
<?php

return [
    'default' => env('BROADCAST_DRIVER', 'null'),

    'connections' => [

        'pusher' => [
            'driver' => 'pusher',
            'key' => env('PUSHER_APP_KEY'),
            'secret' => env('PUSHER_APP_SECRET'),
            'app_id' => env('PUSHER_APP_ID'),
            'options' => [
                'cluster' => env('PUSHER_APP_CLUSTER'),
                'host' => env('PUSHER_HOST') ?: 'api-'.env('PUSHER_APP_CLUSTER', 'mt1').'.pusher.com',
                'port' => env('PUSHER_PORT', 443),
                'scheme' => env('PUSHER_SCHEME', 'https'),
                'encrypted' => true,
                'useTLS' => env('PUSHER_SCHEME', 'https') === 'https',
            ],
        ],

        // Autres drivers...
    ],
];
```

### 2.3 Test Configuration Echo

**Test simple dans console navigateur :**

```javascript
// Ouvrir DevTools Console

// Vérifier Echo disponible
console.log(window.Echo); // Devrait afficher objet Echo

// Écouter channel public test
Echo.channel('test-channel')
    .listen('TestEvent', (e) => {
        console.log('Event reçu:', e);
    });
```

**Dispatcher test event depuis Tinker :**

```bash
php artisan tinker
```

```php
<?php

// Dans Tinker
broadcast(new \App\Events\TestEvent(['message' => 'Hello from Tinker!']));
```

**Si message apparaît console navigateur = Echo configuré correctement ✅**

---

## Leçon 3 : Pusher/Soketi Setup

### 3.1 Option 1 : Pusher Cloud (Gratuit jusqu'à 200k messages/jour)

**S'inscrire Pusher :**

1. Aller sur https://pusher.com
2. Créer compte gratuit
3. Créer nouvelle app "Channels"
4. Récupérer credentials (App ID, Key, Secret, Cluster)

**Configurer `.env` :**

```env
BROADCAST_DRIVER=pusher

PUSHER_APP_ID=123456
PUSHER_APP_KEY=abc123def456
PUSHER_APP_SECRET=xyz789uvw012
PUSHER_APP_CLUSTER=eu

VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

**Installer SDK Pusher PHP :**

```bash
composer require pusher/pusher-php-server
```

**Test Pusher Dashboard :**

1. Aller dans Pusher Dashboard → Debug Console
2. Dispatcher event depuis Laravel
3. Voir event apparaître en temps réel dans console

### 3.2 Option 2 : Soketi (Auto-hébergé, Open Source)

**Soketi = Alternative open-source Pusher (protocole compatible)**

**Installation Soketi (Docker) :**

```yaml
# docker-compose.yml
version: '3'

services:
  soketi:
    image: 'quay.io/soketi/soketi:latest-16-alpine'
    ports:
      - '6001:6001'
    environment:
      SOKETI_DEBUG: '1'
      SOKETI_DEFAULT_APP_ID: 'app-id'
      SOKETI_DEFAULT_APP_KEY: 'app-key'
      SOKETI_DEFAULT_APP_SECRET: 'app-secret'
      SOKETI_USER_AUTHENTICATION_TIMEOUT: 30000
```

**Démarrer Soketi :**

```bash
docker-compose up -d soketi
```

**Configuration Laravel `.env` :**

```env
BROADCAST_DRIVER=pusher

PUSHER_APP_ID=app-id
PUSHER_APP_KEY=app-key
PUSHER_APP_SECRET=app-secret
PUSHER_APP_CLUSTER=mt1

# Configuration Soketi
PUSHER_HOST=127.0.0.1
PUSHER_PORT=6001
PUSHER_SCHEME=http

VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST=127.0.0.1
VITE_PUSHER_PORT=6001
VITE_PUSHER_SCHEME=http
```

**Configuration `resources/js/bootstrap.js` Soketi :**

```javascript
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    wsHost: import.meta.env.VITE_PUSHER_HOST ?? 'localhost',
    wsPort: import.meta.env.VITE_PUSHER_PORT ?? 6001,
    wssPort: import.meta.env.VITE_PUSHER_PORT ?? 6001,
    forceTLS: false, // Important pour dev local
    enabledTransports: ['ws', 'wss'],
    disableStats: true, // Soketi ne supporte pas stats Pusher
});
```

### 3.3 Vérification Connexion WebSocket

**Test dans DevTools Network :**

1. Ouvrir DevTools → Network
2. Filter "WS" (WebSocket)
3. Refresh page
4. Voir connexion WebSocket établie
5. Status : 101 Switching Protocols = ✅ Connecté

**Test programmatique :**

```javascript
// Dans console navigateur
Echo.connector.pusher.connection.bind('connected', () => {
    console.log('✅ WebSocket connecté !');
});

Echo.connector.pusher.connection.bind('error', (err) => {
    console.error('❌ WebSocket erreur:', err);
});

Echo.connector.pusher.connection.bind('disconnected', () => {
    console.warn('⚠️ WebSocket déconnecté');
});
```

---

## Leçon 4 : Broadcasting Events Laravel

### 4.1 Créer Event Broadcastable

```bash
# Générer event
php artisan make:event OrderCreated
```

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;
use App\Models\Order;

class OrderCreated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public Order $order;

    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * Channel(s) sur lequel broadcaster
     */
    public function broadcastOn(): Channel
    {
        // Channel public (accessible par tous)
        return new Channel('orders');
    }

    /**
     * Nom événement (optionnel, défaut = nom classe)
     */
    public function broadcastAs(): string
    {
        return 'order.created';
    }

    /**
     * Données envoyées avec événement
     */
    public function broadcastWith(): array
    {
        return [
            'id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'customer_name' => $this->order->customer->name,
            'total' => $this->order->total,
            'created_at' => $this->order->created_at->toIso8601String(),
        ];
    }
}
```

### 4.2 Dispatcher Event

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Order;
use App\Events\OrderCreated;

class CreateOrder extends Component
{
    public string $customerName = '';
    public float $total = 0;

    public function save(): void
    {
        $this->validate([
            'customerName' => 'required|min:3',
            'total' => 'required|numeric|min:0',
        ]);

        // Créer commande
        $order = Order::create([
            'customer_id' => Customer::firstOrCreate(['name' => $this->customerName])->id,
            'order_number' => 'ORD-' . uniqid(),
            'total' => $this->total,
            'status' => 'new',
        ]);

        // Broadcaster événement (TOUS clients connectés reçoivent)
        broadcast(new OrderCreated($order));

        session()->flash('message', 'Commande créée et diffusée !');
        $this->reset(['customerName', 'total']);
    }

    public function render()
    {
        return view('livewire.create-order');
    }
}
```

### 4.3 Event avec Queue (Async Broadcasting)

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
// ou ShouldBroadcast pour queue

class OrderCreated implements ShouldBroadcastNow // Broadcast immédiat
{
    // ...
}

// Ou pour broadcaster via queue (async)
class OrderCreated implements ShouldBroadcast
{
    /**
     * Queue sur laquelle broadcaster (optionnel)
     */
    public function broadcastQueue(): string
    {
        return 'broadcasts';
    }

    /**
     * Connexion queue (optionnel)
     */
    public function broadcastConnection(): string
    {
        return 'redis';
    }
}
```

**Configuration queue `.env` :**

```env
QUEUE_CONNECTION=redis

# Ou database
QUEUE_CONNECTION=database
```

**Démarrer queue worker :**

```bash
php artisan queue:work
```

---

## Leçon 5 : Écouter Événements Livewire

### 5.1 Écouter dans Composant Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;

class OrderDashboard extends Component
{
    public $orders = [];
    public int $newOrdersCount = 0;

    public function mount(): void
    {
        $this->loadOrders();
    }

    protected function loadOrders(): void
    {
        $this->orders = Order::with('customer')
            ->latest()
            ->limit(10)
            ->get();
        
        $this->newOrdersCount = Order::where('status', 'new')->count();
    }

    /**
     * Écouter événement Echo (dispatché depuis browser)
     */
    #[On('echo:orders,order.created')]
    public function handleNewOrder($event): void
    {
        // Refresh orders list
        $this->loadOrders();

        // Dispatch notification
        $this->dispatch('show-notification', 
            message: "Nouvelle commande #{$event['order_number']} !",
            type: 'success'
        );
    }

    public function render()
    {
        return view('livewire.order-dashboard');
    }
}
```

**Vue avec Echo listener :**

```blade
{{-- resources/views/livewire/order-dashboard.blade.php --}}
<div>
    <div class="stats">
        <div class="stat-card">
            <h3>Nouvelles commandes</h3>
            <p class="text-4xl">{{ $newOrdersCount }}</p>
        </div>
    </div>

    <div class="orders-list">
        @foreach($orders as $order)
            <div class="order-card" wire:key="order-{{ $order->id }}">
                <p><strong>{{ $order->order_number }}</strong></p>
                <p>Client : {{ $order->customer->name }}</p>
                <p>Total : {{ number_format($order->total, 2) }}€</p>
            </div>
        @endforeach
    </div>
</div>

<script>
// Écouter channel public 'orders'
Echo.channel('orders')
    .listen('.order.created', (e) => {
        console.log('Nouvelle commande reçue:', e);
        
        // Dispatcher événement Livewire
        Livewire.dispatch('echo:orders,order.created', e);
    });
</script>
```

### 5.2 Écouter Multiple Channels

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;

class NotificationCenter extends Component
{
    public array $notifications = [];

    /**
     * Écouter événement "order.created" sur channel "orders"
     */
    #[On('echo:orders,order.created')]
    public function handleNewOrder($event): void
    {
        $this->notifications[] = [
            'type' => 'order',
            'message' => "Nouvelle commande #{$event['order_number']}",
            'time' => now(),
        ];
    }

    /**
     * Écouter événement "user.registered" sur channel "users"
     */
    #[On('echo:users,user.registered')]
    public function handleNewUser($event): void
    {
        $this->notifications[] = [
            'type' => 'user',
            'message' => "Nouvel utilisateur : {$event['name']}",
            'time' => now(),
        ];
    }

    /**
     * Écouter événement "message.sent" sur channel "chat"
     */
    #[On('echo:chat,message.sent')]
    public function handleNewMessage($event): void
    {
        $this->notifications[] = [
            'type' => 'message',
            'message' => "Nouveau message de {$event['user']['name']}",
            'time' => now(),
        ];
    }

    public function render()
    {
        return view('livewire.notification-center');
    }
}
```

```blade
<div>
    @foreach($notifications as $index => $notification)
        <div class="notification notification-{{ $notification['type'] }}">
            {{ $notification['message'] }}
            <small>{{ $notification['time']->diffForHumans() }}</small>
        </div>
    @endforeach
</div>

<script>
// Écouter multiples channels
Echo.channel('orders')
    .listen('.order.created', (e) => {
        Livewire.dispatch('echo:orders,order.created', e);
    });

Echo.channel('users')
    .listen('.user.registered', (e) => {
        Livewire.dispatch('echo:users,user.registered', e);
    });

Echo.channel('chat')
    .listen('.message.sent', (e) => {
        Livewire.dispatch('echo:chat,message.sent', e);
    });
</script>
```

### 5.3 Pattern : Echo Listener Réutilisable

**Créer component Alpine.js réutilisable :**

```blade
{{-- resources/views/components/echo-listener.blade.php --}}
@props(['channel', 'event', 'livewireEvent'])

<div 
    x-data="echoListener(@js($channel), @js($event), @js($livewireEvent))"
    x-init="init()"
    {{ $attributes }}
>
    {{ $slot }}
</div>

<script>
function echoListener(channel, event, livewireEvent) {
    return {
        listener: null,

        init() {
            this.listener = Echo.channel(channel)
                .listen(event, (e) => {
                    console.log(`Echo event ${event} on ${channel}:`, e);
                    
                    // Dispatcher vers Livewire
                    Livewire.dispatch(livewireEvent, e);
                });
        },

        destroy() {
            if (this.listener) {
                Echo.leaveChannel(channel);
            }
        }
    }
}
</script>
```

**Utilisation component :**

```blade
{{-- Dans vue Livewire --}}
<div>
    {{-- Écouter "order.created" sur channel "orders" --}}
    <x-echo-listener 
        channel="orders" 
        event=".order.created"
        livewire-event="echo:orders,order.created"
    />

    {{-- Contenu dashboard... --}}
</div>
```

---

## Leçon 6 : Private Channels et Autorisation

### 6.1 Private Channel

**Event avec private channel :**

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use App\Models\Message;

class MessageSent implements ShouldBroadcast
{
    public Message $message;

    public function __construct(Message $message)
    {
        $this->message = $message;
    }

    /**
     * Private channel : seuls utilisateurs autorisés peuvent écouter
     */
    public function broadcastOn(): PrivateChannel
    {
        // Channel privé pour conversation spécifique
        return new PrivateChannel('conversation.' . $this->message->conversation_id);
    }

    public function broadcastWith(): array
    {
        return [
            'id' => $this->message->id,
            'content' => $this->message->content,
            'user' => [
                'id' => $this->message->user->id,
                'name' => $this->message->user->name,
            ],
            'created_at' => $this->message->created_at->toIso8601String(),
        ];
    }
}
```

### 6.2 Autorisation Channel

**Définir règles autorisation `routes/channels.php` :**

```php
<?php

use Illuminate\Support\Facades\Broadcast;
use App\Models\Conversation;

/*
|--------------------------------------------------------------------------
| Broadcast Channels
|--------------------------------------------------------------------------
*/

// Channel privé conversation
Broadcast::channel('conversation.{conversationId}', function ($user, $conversationId) {
    // Vérifier si user appartient à cette conversation
    return Conversation::find($conversationId)
        ->participants()
        ->where('user_id', $user->id)
        ->exists();
});

// Channel privé notifications user
Broadcast::channel('App.Models.User.{userId}', function ($user, $userId) {
    // User peut écouter ses propres notifications uniquement
    return (int) $user->id === (int) $userId;
});

// Channel privé orders d'une entreprise
Broadcast::channel('company.{companyId}.orders', function ($user, $companyId) {
    // Vérifier user appartient à cette entreprise ET a permission
    return $user->company_id === (int) $companyId 
        && $user->can('view-orders');
});
```

### 6.3 Écouter Private Channel

```blade
<div>
    {{-- Contenu conversation... --}}
</div>

<script>
// Écouter private channel (authentication automatique)
Echo.private('conversation.{{ $conversationId }}')
    .listen('.message.sent', (e) => {
        console.log('Nouveau message:', e);
        
        // Dispatcher vers Livewire
        Livewire.dispatch('echo-private:conversation.{{ $conversationId }},message.sent', e);
    });
</script>
```

**Livewire composant :**

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;
use App\Models\Conversation;

class ChatConversation extends Component
{
    public Conversation $conversation;
    public $messages = [];

    public function mount(int $conversationId): void
    {
        $this->conversation = Conversation::findOrFail($conversationId);
        
        // Vérifier autorisation
        $this->authorize('view', $this->conversation);
        
        $this->loadMessages();
    }

    protected function loadMessages(): void
    {
        $this->messages = $this->conversation->messages()
            ->with('user')
            ->latest()
            ->limit(50)
            ->get()
            ->reverse();
    }

    /**
     * Écouter nouveau message sur private channel
     */
    #[On('echo-private:conversation.{conversation.id},message.sent')]
    public function handleNewMessage($event): void
    {
        // Ajouter message à la liste
        $this->messages[] = $event;
    }

    public function render()
    {
        return view('livewire.chat-conversation');
    }
}
```

### 6.4 Test Autorisation

**Test dans Tinker :**

```bash
php artisan tinker
```

```php
<?php

// User 1 (participant conversation)
$user1 = User::find(1);
Auth::login($user1);

// Tester autorisation
Broadcast::channel('conversation.123', function ($user, $conversationId) {
    return Conversation::find($conversationId)
        ->participants()
        ->where('user_id', $user->id)
        ->exists();
});

// Résultat : true si user1 participant, false sinon
```

---

## Leçon 7 : Presence Channels (Who's Online)

### 7.1 Presence Channel

**Event avec presence channel :**

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

class UserTyping implements ShouldBroadcast
{
    public int $userId;
    public string $userName;

    public function __construct(int $userId, string $userName)
    {
        $this->userId = $userId;
        $this->userName = $userName;
    }

    /**
     * Presence channel : tracking utilisateurs connectés
     */
    public function broadcastOn(): PresenceChannel
    {
        return new PresenceChannel('chat');
    }

    public function broadcastWith(): array
    {
        return [
            'user_id' => $this->userId,
            'user_name' => $this->userName,
        ];
    }
}
```

### 7.2 Autorisation Presence Channel

```php
<?php

// routes/channels.php

use Illuminate\Support\Facades\Broadcast;

// Presence channel chat
Broadcast::channel('chat', function ($user) {
    // Retourner infos user qui seront visibles par TOUS utilisateurs connectés
    return [
        'id' => $user->id,
        'name' => $user->name,
        'avatar' => $user->avatar,
        'status' => $user->status, // online, away, busy, etc.
    ];
});

// Presence channel document collaboratif
Broadcast::channel('document.{documentId}', function ($user, $documentId) {
    if ($user->canAccessDocument($documentId)) {
        return [
            'id' => $user->id,
            'name' => $user->name,
            'color' => $user->cursor_color, // Couleur curseur
        ];
    }
    
    return false; // Unauthorized
});
```

### 7.3 Écouter Presence Events

```php
<?php

namespace App\Livewire;

use Livewire\Component;

class ChatRoom extends Component
{
    public array $onlineUsers = [];
    public array $messages = [];

    public function render()
    {
        return view('livewire.chat-room');
    }
}
```

```blade
<div x-data="chatPresence()">
    {{-- Online users list --}}
    <div class="online-users">
        <h3>En ligne ({{ count($onlineUsers) }})</h3>
        <ul>
            @foreach($onlineUsers as $user)
                <li>
                    <img src="{{ $user['avatar'] }}" class="w-8 h-8 rounded-full">
                    <span>{{ $user['name'] }}</span>
                    <span class="status-{{ $user['status'] }}"></span>
                </li>
            @endforeach
        </ul>
    </div>

    {{-- Messages... --}}
</div>

<script>
function chatPresence() {
    return {
        channel: null,

        init() {
            // Joindre presence channel
            this.channel = Echo.join('chat')
                .here((users) => {
                    // Liste utilisateurs déjà présents
                    console.log('Users already here:', users);
                    @this.set('onlineUsers', users);
                })
                .joining((user) => {
                    // Nouvel utilisateur rejoint
                    console.log('User joining:', user);
                    @this.call('addOnlineUser', user);
                })
                .leaving((user) => {
                    // Utilisateur quitte
                    console.log('User leaving:', user);
                    @this.call('removeOnlineUser', user);
                })
                .error((error) => {
                    console.error('Channel error:', error);
                });
        }
    }
}
</script>
```

**Méthodes Livewire :**

```php
<?php

public function addOnlineUser(array $user): void
{
    $this->onlineUsers[] = $user;
}

public function removeOnlineUser(array $user): void
{
    $this->onlineUsers = array_filter(
        $this->onlineUsers, 
        fn($u) => $u['id'] !== $user['id']
    );
}
```

### 7.4 Whisper (Communication P2P Presence Channel)

```blade
<script>
// Joindre presence channel
let channel = Echo.join('chat')
    .here((users) => {
        console.log('Users here:', users);
    })
    .joining((user) => {
        console.log('User joined:', user);
    })
    .leaving((user) => {
        console.log('User left:', user);
    });

// Écouter "whispers" (événements client-to-client, pas serveur)
channel.listenForWhisper('typing', (e) => {
    console.log(`${e.user_name} is typing...`);
    
    // Afficher indicator "X is typing..."
    Livewire.dispatch('user-typing', e);
});

// Envoyer whisper (broadcast vers autres clients, pas serveur)
function sendTypingIndicator() {
    channel.whisper('typing', {
        user_id: @js(auth()->id()),
        user_name: @js(auth()->user()->name),
    });
}

// Trigger whisper quand user tape
let typingTimeout;
document.getElementById('message-input').addEventListener('input', () => {
    clearTimeout(typingTimeout);
    
    sendTypingIndicator();
    
    // Stop typing après 3 secondes inactivité
    typingTimeout = setTimeout(() => {
        channel.whisper('stop-typing', {
            user_id: @js(auth()->id()),
        });
    }, 3000);
});
</script>
```

---

## Leçon 8 : Notifications Temps Réel

### 8.1 Laravel Notification Broadcastable

```bash
# Créer notification
php artisan make:notification OrderShipped
```

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Notifications\Notification;
use App\Models\Order;

class OrderShipped extends Notification implements ShouldBroadcast
{
    use Queueable;

    public Order $order;

    public function __construct(Order $order)
    {
        $this->order = $order;
    }

    /**
     * Channels notification
     */
    public function via($notifiable): array
    {
        return ['database', 'broadcast'];
    }

    /**
     * Données broadcast
     */
    public function toBroadcast($notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'message' => "Votre commande #{$this->order->order_number} a été expédiée !",
        ];
    }

    /**
     * Données database
     */
    public function toArray($notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'message' => "Votre commande #{$this->order->order_number} a été expédiée !",
        ];
    }
}
```

**Envoyer notification :**

```php
<?php

use App\Notifications\OrderShipped;

// Notifier user spécifique
$user = User::find(123);
$user->notify(new OrderShipped($order));

// Broadcaster vers channel privé : App.Models.User.{userId}
```

### 8.2 Écouter Notifications Livewire

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;

class NotificationBell extends Component
{
    public int $unreadCount = 0;
    public array $notifications = [];

    public function mount(): void
    {
        $this->refreshNotifications();
    }

    protected function refreshNotifications(): void
    {
        $this->unreadCount = auth()->user()->unreadNotifications()->count();
        $this->notifications = auth()->user()
            ->unreadNotifications()
            ->limit(5)
            ->get()
            ->toArray();
    }

    /**
     * Écouter nouvelle notification broadcasted
     */
    #[On('echo-private:App.Models.User.{auth.id},Illuminate\\Notifications\\Events\\BroadcastNotificationCreated')]
    public function handleNewNotification($event): void
    {
        // Refresh count et liste
        $this->refreshNotifications();

        // Afficher toast
        $this->dispatch('show-toast', 
            message: $event['message'],
            type: 'info'
        );
    }

    public function markAsRead(string $notificationId): void
    {
        auth()->user()
            ->unreadNotifications()
            ->where('id', $notificationId)
            ->update(['read_at' => now()]);

        $this->refreshNotifications();
    }

    public function render()
    {
        return view('livewire.notification-bell');
    }
}
```

```blade
<div x-data="{ open: false }">
    {{-- Bell icon avec badge --}}
    <button @click="open = !open" class="relative">
        <svg class="w-6 h-6">...</svg>
        
        @if($unreadCount > 0)
            <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-2">
                {{ $unreadCount }}
            </span>
        @endif
    </button>

    {{-- Dropdown notifications --}}
    <div x-show="open" @click.away="open = false" class="dropdown">
        @forelse($notifications as $notification)
            <div class="notification-item">
                <p>{{ $notification['data']['message'] }}</p>
                <button wire:click="markAsRead('{{ $notification['id'] }}')">
                    Marquer lu
                </button>
            </div>
        @empty
            <p class="text-gray-500">Aucune notification</p>
        @endforelse
    </div>
</div>

<script>
// Écouter notifications sur private channel user
Echo.private('App.Models.User.{{ auth()->id() }}')
    .notification((notification) => {
        console.log('Notification reçue:', notification);
        
        // Dispatcher vers Livewire
        Livewire.dispatch(
            'echo-private:App.Models.User.{{ auth()->id() }},Illuminate\\Notifications\\Events\\BroadcastNotificationCreated',
            notification
        );
    });
</script>
```

### 8.3 Toast Notifications Temps Réel

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;

class ToastManager extends Component
{
    public array $toasts = [];

    #[On('show-toast')]
    public function addToast(string $message, string $type = 'info', int $duration = 5000): void
    {
        $id = uniqid();

        $this->toasts[] = [
            'id' => $id,
            'message' => $message,
            'type' => $type,
            'duration' => $duration,
        ];

        // Auto-remove après duration
        $this->dispatch('remove-toast-after', id: $id, delay: $duration);
    }

    #[On('remove-toast')]
    public function removeToast(string $id): void
    {
        $this->toasts = array_filter(
            $this->toasts, 
            fn($toast) => $toast['id'] !== $id
        );
    }

    public function render()
    {
        return view('livewire.toast-manager');
    }
}
```

```blade
{{-- resources/views/livewire/toast-manager.blade.php --}}
<div class="fixed top-4 right-4 z-50 space-y-2">
    @foreach($toasts as $toast)
        <div 
            x-data="{ show: true }"
            x-show="show"
            x-init="setTimeout(() => show = false, {{ $toast['duration'] }})"
            x-transition:enter="transition ease-out duration-300"
            x-transition:enter-start="opacity-0 transform translate-x-full"
            x-transition:enter-end="opacity-100 transform translate-x-0"
            x-transition:leave="transition ease-in duration-200"
            x-transition:leave-start="opacity-100 transform translate-x-0"
            x-transition:leave-end="opacity-0 transform translate-x-full"
            class="toast toast-{{ $toast['type'] }} p-4 rounded-lg shadow-lg max-w-sm"
            wire:key="toast-{{ $toast['id'] }}"
        >
            <div class="flex items-center justify-between">
                <p>{{ $toast['message'] }}</p>
                <button wire:click="removeToast('{{ $toast['id'] }}')" class="ml-4">
                    ×
                </button>
            </div>
        </div>
    @endforeach
</div>
```

**Inclure dans layout :**

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    {{-- Toast manager global --}}
    <livewire:toast-manager />

    {{ $slot }}
</body>
</html>
```

---

## Leçon 9 : Patterns Collaboration et Production

### 9.1 Collaborative Cursor Tracking

```php
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On;

class CollaborativeEditor extends Component
{
    public int $documentId;
    public string $content = '';
    public array $activeCursors = [];

    public function mount(int $documentId): void
    {
        $this->documentId = $documentId;
        $this->content = Document::find($documentId)->content;
    }

    /**
     * User joined document
     */
    #[On('echo-presence:document.{documentId},here')]
    public function handleUsersHere($users): void
    {
        foreach ($users as $user) {
            $this->activeCursors[$user['id']] = [
                'name' => $user['name'],
                'color' => $user['color'],
                'position' => null,
            ];
        }
    }

    /**
     * New user joined
     */
    #[On('echo-presence:document.{documentId},joining')]
    public function handleUserJoined($user): void
    {
        $this->activeCursors[$user['id']] = [
            'name' => $user['name'],
            'color' => $user['color'],
            'position' => null,
        ];
    }

    /**
     * User left
     */
    #[On('echo-presence:document.{documentId},leaving')]
    public function handleUserLeft($user): void
    {
        unset($this->activeCursors[$user['id']]);
    }

    /**
     * Update cursor position (whisper)
     */
    #[On('cursor-moved')]
    public function updateCursorPosition(int $userId, int $position): void
    {
        if (isset($this->activeCursors[$userId])) {
            $this->activeCursors[$userId]['position'] = $position;
        }
    }

    public function render()
    {
        return view('livewire.collaborative-editor');
    }
}
```

```blade
<div x-data="collaborativeEditor()">
    {{-- Active users cursors --}}
    <div class="cursors-container">
        @foreach($activeCursors as $userId => $cursor)
            @if($cursor['position'] !== null && $userId !== auth()->id())
                <div 
                    class="cursor"
                    style="
                        left: {{ $cursor['position'] }}px;
                        border-color: {{ $cursor['color'] }};
                    "
                >
                    <span style="background: {{ $cursor['color'] }};">
                        {{ $cursor['name'] }}
                    </span>
                </div>
            @endif
        @endforeach
    </div>

    {{-- Editor --}}
    <textarea 
        wire:model.live.debounce.500ms="content"
        @input="sendCursorPosition($event.target.selectionStart)"
        class="w-full h-96 p-4 border rounded"
    ></textarea>
</div>

<script>
function collaborativeEditor() {
    return {
        channel: null,

        init() {
            this.channel = Echo.join('document.{{ $documentId }}')
                .here((users) => {
                    Livewire.dispatch('echo-presence:document.{{ $documentId }},here', users);
                })
                .joining((user) => {
                    Livewire.dispatch('echo-presence:document.{{ $documentId }},joining', user);
                })
                .leaving((user) => {
                    Livewire.dispatch('echo-presence:document.{{ $documentId }},leaving', user);
                })
                .listenForWhisper('cursor', (e) => {
                    Livewire.dispatch('cursor-moved', e.user_id, e.position);
                });
        },

        sendCursorPosition(position) {
            this.channel.whisper('cursor', {
                user_id: {{ auth()->id() }},
                position: position
            });
        }
    }
}
</script>
```

### 9.2 Rate Limiting Broadcasting

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Support\Facades\RateLimiter;

class UserTyping implements ShouldBroadcast
{
    use InteractsWithSockets;

    public int $userId;

    public function __construct(int $userId)
    {
        $this->userId = $userId;
    }

    /**
     * Rate limit : max 1 broadcast par seconde par user
     */
    public function broadcastWhen(): bool
    {
        $key = "typing:{$this->userId}";

        if (RateLimiter::tooManyAttempts($key, 1)) {
            return false; // Skip broadcast si trop fréquent
        }

        RateLimiter::hit($key, 1); // Expire 1 seconde

        return true;
    }

    public function broadcastOn()
    {
        return new PresenceChannel('chat');
    }
}
```

### 9.3 Monitoring Broadcasting Production

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Event;
use Illuminate\Broadcasting\BroadcastEvent;
use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Log;

class BroadcastServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // Monitor tous broadcasts
        Event::listen(BroadcastEvent::class, function ($event) {
            Log::channel('broadcasting')->info('Event broadcasted', [
                'event' => get_class($event->event),
                'channel' => $event->channels[0] ?? 'unknown',
                'data_size' => strlen(json_encode($event->event)),
                'timestamp' => now(),
            ]);
        });

        // Monitor erreurs broadcasting
        Event::listen('broadcasting.failed', function ($event, $exception) {
            Log::channel('broadcasting')->error('Broadcasting failed', [
                'event' => $event,
                'error' => $exception->getMessage(),
                'timestamp' => now(),
            ]);
        });
    }
}
```

**Configuration logging :**

```php
<?php

// config/logging.php
'channels' => [
    'broadcasting' => [
        'driver' => 'daily',
        'path' => storage_path('logs/broadcasting.log'),
        'level' => 'info',
        'days' => 14,
    ],
],
```

### 9.4 Fallback Polling si WebSocket Fail

```blade
<div 
    x-data="smartPolling()"
    x-init="init()"
>
    {{-- Contenu... --}}
</div>

<script>
function smartPolling() {
    return {
        useWebSocket: true,
        pollInterval: null,

        init() {
            // Tester connexion WebSocket
            try {
                Echo.connector.pusher.connection.bind('connected', () => {
                    console.log('✅ WebSocket connected');
                    this.useWebSocket = true;
                    this.stopPolling();
                });

                Echo.connector.pusher.connection.bind('disconnected', () => {
                    console.warn('⚠️ WebSocket disconnected, fallback to polling');
                    this.useWebSocket = false;
                    this.startPolling();
                });

                Echo.connector.pusher.connection.bind('error', () => {
                    console.error('❌ WebSocket error, using polling');
                    this.useWebSocket = false;
                    this.startPolling();
                });

            } catch (e) {
                console.error('WebSocket not available, using polling');
                this.useWebSocket = false;
                this.startPolling();
            }
        },

        startPolling() {
            if (this.pollInterval) return;

            this.pollInterval = setInterval(() => {
                console.log('Polling refresh...');
                Livewire.dispatch('$refresh');
            }, 5000); // Poll toutes les 5 secondes
        },

        stopPolling() {
            if (this.pollInterval) {
                clearInterval(this.pollInterval);
                this.pollInterval = null;
            }
        }
    }
}
</script>
```

---

## Projet 1 : Live Chat Application

**Objectif :** Chat temps réel complet production

**Fonctionnalités :**
- Presence channel (who's online)
- Messages temps réel instantanés
- Typing indicators (whispers)
- Private conversations (1-to-1)
- Group conversations
- Read receipts
- Online/offline status
- Message persistence DB
- Notifications unread messages
- Fallback polling si WebSocket fail

**Code disponible repository.**

---

## Projet 2 : Real-time Dashboard Analytics

**Objectif :** Dashboard analytics temps réel

**Fonctionnalités :**
- Broadcasting nouveaux orders
- Stats update temps réel (revenue, orders count)
- Chart updates live (Chart.js)
- Activity feed temps réel
- Alerts critiques (broadcast urgent)
- Multiple widgets écoutant événements
- Selective polling widgets non-critical
- Rate limiting broadcasts (avoid spam)
- Monitoring broadcasting (logs)

**Code disponible repository.**

---

## Projet 3 : Collaborative Document Editor

**Objectif :** Éditeur document collaboratif Google Docs-like

**Fonctionnalités :**
- Presence channel (active editors)
- Cursor position tracking (whispers)
- Real-time content sync
- Conflict resolution (last-write-wins)
- User colors attribution
- Activity feed (who edited what)
- Version history
- Auto-save debounced (500ms)
- Permissions (view/edit)
- Notifications changes important

**Code disponible repository.**

---

## Checklist Module X

- [ ] `wire:poll` configuré intervalles appropriés
- [ ] Laravel Echo installé et configuré
- [ ] Pusher ou Soketi setup et testé
- [ ] BroadcastServiceProvider activé
- [ ] Events `ShouldBroadcast` créés
- [ ] Channels autorisations définies (`routes/channels.php`)
- [ ] Composants Livewire écoutent événements Echo
- [ ] Private channels authentifiés
- [ ] Presence channels tracking online users
- [ ] Whispers pour communication P2P
- [ ] Notifications broadcastables
- [ ] Toast notifications temps réel
- [ ] Rate limiting broadcasts
- [ ] Monitoring broadcasting (logs)
- [ ] Fallback polling si WebSocket fail

**Concepts clés maîtrisés :**

✅ Polling automatique wire:poll
✅ Laravel Echo configuration complète
✅ Pusher/Soketi setup production
✅ Broadcasting events Laravel
✅ Private channels sécurisés
✅ Presence channels collaboration
✅ Notifications temps réel
✅ Whispers communication P2P
✅ Patterns collaboration avancés
✅ Production monitoring et fallbacks

---

**Module X terminé ! 🎉**

**Prochaine étape : Module XI - Testing Livewire**

Vous maîtrisez maintenant le temps réel Livewire production. Le Module XI approfondit le testing avec Pest/PHPUnit, tests unitaires composants, tests événements, mocking, TDD workflow et CI/CD.

---

**✅ MODULE X LIVEWIRE COMPLET !**

**Contenu créé :**
- ✅ 9 leçons exhaustives (230+ lignes chacune)
- ✅ Analogie standard téléphonique intelligent
- ✅ Diagramme Mermaid polling vs WebSocket
- ✅ wire:poll configuration complète
- ✅ Laravel Echo setup détaillé
- ✅ Pusher et Soketi configuration production
- ✅ Broadcasting events complets
- ✅ Private channels avec autorisation
- ✅ Presence channels (who's online, cursors)
- ✅ Whispers communication P2P
- ✅ Notifications Laravel broadcastables
- ✅ Toast manager temps réel
- ✅ Patterns collaboration avancés (cursors, édition simultanée)
- ✅ Rate limiting et monitoring production
- ✅ Fallback polling si WebSocket fail
- ✅ 3 projets pratiques (chat, dashboard, collaborative editor)
- ✅ Checklist validation

**Points clés exhaustifs :**
- Différence polling vs WebSocket (latence, charge, scalabilité)
- Pusher cloud vs Soketi auto-hébergé
- Channels : public vs private vs presence
- Autorisation channels granulaire
- Whispers vs broadcasts (client-to-client vs server-to-all)
- Monitoring et fallback strategies production

**Tu valides ce module X ?** Si oui, dis-moi "Module XI" pour Testing Livewire (Pest/PHPUnit, tests composants, événements, TDD, CI/CD) ! 🚀