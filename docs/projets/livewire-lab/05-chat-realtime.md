---
description: "Projet 5 : Créer une application de messagerie instantanée en Websockets / Polling."
icon: lucide/messages-square
tags: ["PROJET", "LIVEWIRE", "WEBSOCKETS", "ECHO", "REALTIME"]
---

# Chat Real-Time

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Livewire 3.x"
  data-time="4 Heures">
</div>

!!! quote "Briser le cycle HTTP Classique"
    Jusqu'à présent, le modèle d'interaction était toujours provoqué par l'utilisateur (un clic, ou une lettre tapée) : c'est le client qui interpelle le serveur. Comment faire lorsqu'on souhaite que le serveur "pousse" une information sur l'écran d'un client *sans* que celui-ci ait fait la moindre action ? (Ex: recevoir un message d'un ami). Il faut utiliser des canaux persistants comme les **WebSockets** (Pusher / Laravel Reverb), ou opérer la technique rudimentaire mais facile du **Polling**.

<br>

![Livewire Chat Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_chat_1775233287922.png)
<p><em>Maquette UI conceptuelle du projet : Application de messagerie instantanée dotée du rafraichissement WebSocket.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- Afficher une bulle de Chat centrale.
- Pouvoir taper un message et l'envoyer.
- Lorsqu'une *autre* personne envoie un message sur la plateforme, le voir s'afficher de mon côté **de manière instantanée**.
- Un indicateur "En train d'écrire...".

### Concepts Livewire déployés
- `#[On('evenement')]` : Les écouteurs d'événements.
- `wire:poll` (Mode secours) : La boucle de relance chronométrée.
- *Laravel Echo / Pusher* (Mode avancé) : Les Broadcasting Drivers.

<br>

---

## 2. Le Modèle PHP : L'Écoute (Listening)

Pour bien comprendre la mécanique, nous allons d'abord créer le modèle sans WebSocket. Le composant gère simplement sa liste de messages locaux.

```php title="app/Livewire/ChatRoom.php"
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Message;
use Livewire\Attributes\On;

class ChatRoom extends Component
{
    public $messageText = '';

    public function sendMessage()
    {
        $this->validate(['messageText' => 'required|string']);

        Message::create([
            'user_id' => auth()->id(), // Utilisateur connecté via DB
            'content' => $this->messageText
        ]);

        $this->messageText = '';
        
        // Broadcast manuel classique depuis Laravel !
        // App\Events\MessageSentEvent::dispatch();
    }

    // Le Getter récupère toujours les 20 derniers messages à l'instant - T
    public function getMessagesProperty()
    {
        return Message::with('user')->latest()->take(20)->get()->reverse();
    }

    // METHODE MAGIQUE : 
    // Cet attribut demande à Livewire de rafraichir entièrement le composant
    // Dès qu'on entend parler du WebSocket Laravel 'echo:channel,event'
    #[On('echo:chat,MessageSentEvent')]
    public function updateTimeline()
    {
        // En s'exécutant à vide, la fonction force le Render() !
        // Et comme le Render appelle le Getter getMessagesProperty()...
        // ...Les nouveaux messages apparaissent à l'écran !
    }

    public function render()
    {
        return view('livewire.chat-room');
    }
}
```

<br>

---

## 3. La Vue Blade de Communication

### Option A : Le Mode Secours Sans Installation (Polling)

Si vous ne possédez pas de serveur WebSocket (Laravel Echo / Reverb) sur votre machinerie de production, vous pouvez recourir à l'instruction la plus violente et facile de Livewire : `wire:poll`.

```html title="resources/views/livewire/chat-room.blade.php (Version Polling)"
<!-- wire:poll.2000ms force la Div à demander au serveur PHP de se regénérer toutes les 2 secondes, coûte que coûte. Cela créera l'illusion du temps réel en échange d'une surcharge processeur/réseau effroyable. -->
<div class="chat-container max-w-2xl mx-auto border" wire:poll.2000ms>
    
    <div class="h-96 overflow-y-auto bg-gray-50 p-4">
        @foreach($this->messages as $msg)
            <div class="{{ $msg->user_id === auth()->id() ? 'text-right' : 'text-left' }} mb-2">
                <span class="inline-block p-2 rounded {{ $msg->user_id === auth()->id() ? 'bg-blue-500 text-white' : 'bg-white block' }}">
                    {{ $msg->content }}
                </span>
                <div class="text-xs text-gray-400 mt-1">{{ $msg->user->name }}</div>
            </div>
        @endforeach
    </div>

    <!-- Le formulaire pour envoyer -->
    <form wire:submit="sendMessage" class="flex border-t p-2">
        <input type="text" wire:model="messageText" class="w-full border p-2">
        <button type="submit" class="bg-blue-600 text-white p-2">Envoyer</button>
    </form>
</div>
```

### Option B : La Version Écologique Websocket

Si vous avez inclus les bibliothèques JS de **Laravel Echo** en haut de page, le code précédent utilisant `#On(echo:chat)` du backend gère tout organiquement en gardant un tunnel asynchrone ouvert (Port TCP 6001). Dans ce cas, **retirez** `wire:poll` et Livewire attendra passivement le `Pusher/Reverb` event venant du routeur !

<br>

---

## Conclusion

!!! quote "Choix de l'agilité"
    Le `wire:poll` est excellent pour de petits dashboards d'administration avec très peu d'ouvertures de fenêtres. Pour déployer massivement à des milliers d'utilisateurs, utilisez `#On` avec **Laravel Reverb**. Le code d'envoi et de tri métier reste scrupuleusement identique et purement localisé en PHP.

> Vous contrôlez désormais le temps. Il est vital de finaliser cette certification Masterclass en regroupant des autorisations complexes, un export PDF, la cryptographie et la gestion de layout partagés dans le projet d'achèvement monstrueux : [Le Dashboard SaaS](./06-dashboard-saas.md).
