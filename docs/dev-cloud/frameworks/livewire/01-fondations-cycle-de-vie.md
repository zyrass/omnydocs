---
description: "Rôle, Installation et Cycle de vie de requêtes Full-Stack d'un composant."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "CYCLE", "LARAVEL"]
---

# 01. Fondations & Cycle de Vie

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>

!!! quote "Illusion du Javascript"
    Construire de l'interactivité a toujours nécessité d'écrire en un langage (PHP, Ruby) pour gérer la base de données, et de créer une autre codebase en JavaScript (React, Vue) pour l'affichage visuel, impliquant de douloureuses APIs (`fetch`) entre eux. **Livewire est une puissante illusion.** Il intercepte les clics depuis le HTML pour vous, envoie une mini-requête AJAX (XHR) invisible au serveur PHP, qui modifie la variable PHP, recalcule une portion de vue Blade et remplace la zone du clavier **sans la faire clignoter**. Vous codez en PHP, l'utilisateur a l'impression d'être sur une App JavaScript ultra-rapide.

<br>

---

## 1. Pourquoi Livewire au lieu de React / Vue ?

Livewire 3.x n'est pas conçu pour faire des expériences immersives comme des Jeux Web de Canvas 3D ou des plateformes lourdes comme Figma. Son **Sweet Spot** (point idéal), ce sont les S.I (Systèmes d'Information) et les SaaS !

- **Sécurité Unifiée :** Pas d'API. Le composant est écrit au milieu de Laravel, avec accès instantané aux Helpers `auth()`, Modèles Eloquent et Validations FormRequests.
- **Zéro NPM Bloat :** Aucune configuration de `webpack`, `rollup` ou de compilateur NPM complexe.
- **SEO Ready :** C'est du "Server Side Render". Lors du premier affichage URL, c'est du vrai HTML lisible par les robots Google, l'interactivité AJAX ne remplace la carte que plus tard!

<br>

---

## 2. Structure d'un Composant

Lorsque vous tapez `php artisan make:livewire Counter`, deux fichiers jumeaux (un Backend PHP et un Frontend HTML Blade) viennent au monde. Ils fonctionnent en symbiose.

```php title="Le Cerveau: app/Livewire/Counter.php"
<?php

namespace App\Livewire;

use Livewire\Component;

class Counter extends Component
{
    // C'est votre State. Accessible dans Render.
    public $initialWord = 'Zensical';

    public function render()
    {
        return view('livewire.counter');
    }
}
```

```html title="Les Yeux: resources/views/livewire/counter.blade.php"
<div>
    <h1>Bienvenue sur {{ $initialWord }}</h1>
</div>
```

_Note vitale Zensical : La vue d'un composant Livewire v3 DOIT **Absolument** n'avoir qu'un seul Element HTML Racine (ici la balise `<div>`). Si vous mettez le `<h1>` et le `<div>` au même niveau sans parent invisible (Wrapper), Livewire vous insultera avec une erreur dans votre Console._

<br>

---

## 3. Le fameux Lifecycle (Cycle de Vie)

Contrairement à de simples variables dans un Controller, un Composant Livewire vieillit et subit des événements d'exécution (Lifecycle Hooks). Vous pouvez capter trois temps de sa vie : `mount`, `hydrate` et `updating`.

```php title="Le Constructeur et la Mémoire"
class UserCard extends Component
{
    public $user;

    // S'exécute UNE SEULE FOIS, tout au début, lors du chargement de la page HTTP classique. (C'est le Constructeur pour Livewire).
    public function mount($identifiant)
    {
        $this->user = User::findOrFail($identifiant);
    }

    // S'exécute à CHAQUE FOIS qu'un bouton est cliqué et qu'une requête AJAX Livewire réveille le composant depuis la mémoire cache du serveur (Pour vérifier qui a appelé !)
    public function hydrate()
    {
        // Utile si on veut vérifier des droits d'accès après 5min d'attente
        if (!auth()->check()) { return redirect('/login'); }
    }

    // S'exécute JUSTE AVANT qu'une de vos "public" variables soit modifiée 
    // par le client. Idéal pour faire un "Replace" d'une majuscule !
    public function updating($property, $value)
    {
        if ($property === 'user.title') {
            $this->user->title = strtoupper($value);
        }
    }
}
```

<br>

---

## Conclusion

!!! quote "Architecture Globale"
    Pensez la création d'un composant Livewire comme un mini-contrôleur Laravel dédié exclusivement à un seul carré de votre maquette UI. Le `mount()` est votre injecteur initial.

> Mais alors ? Comment le fameux composant comprend que l'utilisateur en frontend est en train d'écrire un mot ou clique sur un bouton ? Tout relève de la notion cruciale du Data Transfer. Plongeons dans le [Chapitre 2 : Propriétés et Actions](./02-proprietes-actions.md).
