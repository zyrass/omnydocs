---
description: "Dispatcheur d'événements, isolation et communication inter-composants."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "EVENTS", "LISTENERS"]
---

# Événements Globaux (Event Bus)

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>

!!! quote "Architecturer au-delà du composant unique"
    Rares sont les Pages unifiées où un "Formulaire" se charge seul d'afficher la "Liste" qui l'accompagne. En réalité, on imbrique les données : Un composant d'Entête de Page porte un indicateur de Notifications, et Composant isolé dans une Page Contact porte un Formulaire. Comment faire pour qu'après validation du Formulaire Contact (Composant A), L'indicateur du Header (Composant B) s'incrémente mathématiquement de "+ 1 Message non lu"  sans faire recharger la vraie URL complète HTTP de notre App ? Le **Message Dispatching (Event Bus)** est la clef.

<br>

---

## 1. Répandre un signal global : the Dispatch()

Un composant Livewire décide "d'hurler" dans le vide serveur qu'un événement s'est produit. Tout composant qui l'écoute peut s'activer, à fortiori lui-même !

```php title="app/Livewire/CreatePost.php (L'Émetteur)"
class CreatePost extends Component
{
    public function saveAction()
    {
        // Enregistrement BD ...
        Post::create([...]);

        // C'est le hurlement système. Le nom de l'évent est arbitraire ("post-created").
        // On peut (optionnellement) ajouter un payload pour dire QUEL post a été créé.
        $this->dispatch('post-created'); 
    }
}
```

<br>

---

## 2. Intercepter le signal global : L'Attribut `#[On]`

Pendant ce temps, à des milliers de milles virtuels, un obscur module "NotificationCount" attendait que quelqu'un déclenche cet alias ("post-created").

```php title="app/Livewire/NotificationCount.php (Le Récepteur)"
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\On; 

class NotificationCount extends Component
{
    public $count = 0;

    // Cette fonction sera MAGIQUEMENT invoquée dès que QUELQU'UN exécute un dispatch('post-created') sur le serveur.
    #[On('post-created')] 
    public function incrementNotifications()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.badge-counter');
    }
}
```

_Le système sous-jacent est orchestré par le Javascript Livewire centralisé de la page finale. Lors du Refresh de l'Émetteur, ce JS détecte l'existence de l'événement et renvoie silencieusement une requête PHP au Récepteur qui s'allume._

<br>

---

## 3. L'Écoute coté Client (Javascript) via Events

Imaginons que nous n'ayons pas un *autre composant Livewire* Récepteur, mais qu'on souhaite ouvrir une Fenêtre "SweetAlert 2" (Qui est une bibliothèque pur script Javascript local (Frontend) !) ?

Il suffit de l'intercepter via Alpine.js ou en VanillaJS !

```html title="Dans une Vue Blade globale (footer, app.layout...)"
<!-- Avec un écouteur système pur Window natif (Javascript Vanilla classique) -->
<script>
    document.addEventListener('livewire:initialized', () => {
        // En lien avec $this->dispatch('post-created') du serveur PHP !!
        Livewire.on('post-created', (eventPayload) => {
            alert('Un utilisateur a créé un nouveau message ! Pensez à rafraichir !');
            // Ou invoquer Toastify, SweetAlert, Notifications System Push HTML...
        });
    });
</script>

<!-- Avec la méthode d'extension propre Alpine.JS -->
<div x-data @post-created.window="alert('Alerte Alpine.JS Interceptée !')">
</div>
```

_Rien n'est inaccessible. L'événement est transitoire (Global Window/Navigator Event). Que vous l'écoutez en PHP, JS, Vue, React ou Alpine : le pont technologique est absolu._

<br>

---

## Conclusion

!!! quote "Event Sourcing : Découplage"
    Les développeurs qui codent tous leurs affichages et calculs lourds dans 100% de la même classe finiront avec les monstrueux **God Controllers**. Grâce à `$dispatch()`, un composant A s'en moque de qui l'entoure. Il avertit : _J'ai supprimé la facture n°X_. Libre au composant "Facture" de se désintégrer de lui même et au composant "Total Global Header" de se recalculer, délestant leur concepteur de toute responsabilité intra-hiérarchique complexe !

> C'en est fini des structures abstraites de manipulation de données. Vous devez maintenant maîtriser le dernier socle de l'expertise "Advanced" : La gestion de Fichiers Physiques (Storage), le Polling (Interrogatoires temporiels réguliers), et les WebSockets instantanés. Poursuivez sur l'[Expérience de Production et Fonctionnalités Avancées.](./05-avance-production.md).
