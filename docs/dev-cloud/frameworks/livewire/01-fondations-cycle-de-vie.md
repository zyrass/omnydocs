---
description: "Rôle, structure mono-fichier (SFC), cycle de vie et hydratation moderne d'un composant Livewire v4."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "SFC", "LARAVEL"]
---

# Fondations & Cycle de Vie

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="4.x"
  data-time="2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Illusionniste et la Lanterne Magique"
    Construire une interface interactive demandait traditionnellement d'écrire le code serveur dans un langage (PHP) et la logique d'affichage dans un autre (JavaScript), tout en gérant une passerelle complexe d'APIs. Livewire fonctionne comme une lanterne magique. Lorsqu'un utilisateur clique sur un bouton, l'événement est intercepté par le noyau JavaScript léger de Livewire. Une requête asynchrone ultra-rapide (AJAX) transmet l'état actuel au serveur PHP. Ce dernier met à jour le composant, recalcule la vue Blade, et renvoie uniquement la portion de HTML modifiée pour être injectée dans la page, sans aucun rechargement ni clignotement.

Ce module présente les fondations de Livewire v4.x, sa structure mono-fichier et son cycle de vie.

<br>

---

## 1. Pourquoi Livewire v4 et les composants mono-fichier (SFC) ?

Livewire v4 simplifie l'architecture en introduisant les **Single-File Components (SFC)** par défaut. Au lieu de jongler entre une classe PHP (`app/Livewire/Counter.php`) et un fichier Blade (`resources/views/livewire/counter.blade.php`), tout est centralisé dans un seul fichier Blade préfixé par un éclair `⚡` (ex: `⚡counter.blade.php`).

- **Cohésion maximale :** La logique métier et l'interface visuelle sont réunies au même endroit, éliminant la dispersion du code.
- **Sécurité et simplicité :** Pas d'API intermédiaire à déclarer. Le composant s'exécute directement dans le contexte Laravel, avec un accès direct aux modèles Eloquent et à l'authentification.
- **Hydratation partielle (Islands) :** Grâce à la directive `@island`, vous pouvez isoler des sections de votre page pour qu'elles se chargent et s'hydratent de manière autonome, réduisant drastiquement l'empreinte réseau.

<br>

---

## 2. Structure d'un composant mono-fichier

Lorsque vous générez un composant sous Livewire v4 avec `php artisan make:livewire Counter`, le framework crée par défaut un unique fichier dans le dossier des vues.

### Fichier `resources/views/livewire/⚡counter.blade.php`

```html title="Blade - structure mono-fichier d'un composant Livewire v4"
<?php
use Livewire\Component;

new class extends Component {
    // État du composant (State)
    public $count = 0;

    // Méthode réactive
    public function increment()
    {
        $this->count++;
    }
};
?>

<div class="p-6 bg-white rounded-xl shadow-md flex flex-col items-center gap-4">
    <h1 class="text-2xl font-bold text-slate-800">Compteur : {{ $count }}</h1>
    
    <!-- Bouton déclenchant la méthode PHP du bloc supérieur -->
    <button wire:click="increment" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Incrémenter
    </button>
</div>
```
_Composant mono-fichier hébergeant sa logique PHP dans une classe anonyme à sa tête, et son affichage Blade au pied._

*Note critique : Tout composant Livewire v4 doit posséder **un seul et unique élément HTML racine** (ici la balise `<div>`). Si plusieurs éléments se trouvent au même niveau de la racine, le moteur de rendu renverra une erreur d'intégration.*

<br>

---

## 3. Le cycle d'hydratation et de déshydratation

L'échange de données entre le navigateur (client) et Laravel (serveur) s'effectue via un protocole d'hydratation automatique :

1. **La Déshydratation (Dehydration) :** Lors du premier chargement ou après une modification, le serveur prend l'état du composant PHP, le sérialise sous forme de snapshot JSON sécurisé, génère le code HTML correspondant et envoie le tout au navigateur.
2. **L'Hydratation (Hydration) :** Lorsque l'utilisateur clique sur un bouton (`wire:click`), le navigateur envoie le snapshot JSON actuel et l'action demandée au serveur. Livewire reconstruit l'objet PHP à partir du JSON, applique la modification, exécute la méthode, puis déshydrate à nouveau le composant pour renvoyer le nouveau HTML.

<br>

---

## 4. Le Cycle de Vie (Lifecycle Hooks)

Livewire v4 unifie ses crochets de cycle de vie pour faciliter la gestion de l'état et de l'initialisation.

### Les crochets essentiels

```html title="Blade - gestion des cycles de vie dans la classe anonyme"
<?php
use Livewire\Component;
use App\Models\User;

new class extends Component {
    public $userId;
    public $user;

    // mount() s'exécute UNE SEULE FOIS lors de l'affichage initial de la page HTTP
    public function mount($userId)
    {
        $this->userId = $userId;
        $this->user = User::findOrFail($userId);
    }

    // boot() s'exécute à CHAQUE requête (initiale et AJAX), avant toute autre action
    public function boot()
    {
        if (!auth()->check()) {
            return redirect()->route('login');
        }
    }

    // updating() s'exécute juste avant qu'une propriété publique ne soit modifiée
    public function updating($property, $value)
    {
        if ($property === 'user.name') {
            // Exemple de validation ou transformation avant écriture
            $this->user->name = trim($value);
        }
    }
};
?>

<div>
    <h2>Profil de {{ $user->name }}</h2>
</div>
```
_Exemple de gestion de l'initialisation et du filtrage des propriétés via les crochets de cycle de vie._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Création d'un composant de bienvenue**

1. Créez un composant mono-fichier `⚡welcome-card.blade.php` dans `resources/views/livewire/`.
2. Déclarez une propriété `$name` initialisée à "Visiteur".
3. Affichez un message "Bienvenue, [nom]" et ajoutez un champ de texte relié à `$name`.
4. Constatez l'affichage dynamique lors de la saisie.

**Exercice 2 — Suivi des requêtes via les DevTools**

1. Ouvrez l'inspecteur de votre navigateur sur l'onglet "Réseau" (Network).
2. Cliquez sur le bouton d'action d'un composant Livewire.
3. Analysez le payload de la requête HTTP asynchrone envoyée par Livewire et observez le snapshot JSON transféré contenant l'état des variables.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Livewire v4 unifie la logique et l'interface au sein des composants mono-fichiers (SFC). Le protocole d'hydratation assure la synchronisation de l'état entre le navigateur et le serveur en convertissant les objets PHP en snapshots JSON. Les crochets de cycle de vie (`mount`, `boot`, `updating`) permettent d'intercepter ces transitions pour préparer les données ou appliquer des règles métier.

> Pour synchroniser dynamiquement les champs de saisie et réagir aux clics des utilisateurs, passez au **[Module 2 — Propriétés & Actions](./02-proprietes-actions.md)**.
