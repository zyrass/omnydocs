---
description: "Projet 6 : Construire une plateforme d'administration SaaS complète Livewire."
icon: lucide/layout-dashboard
tags: ["PROJET", "LIVEWIRE", "LARAVEL", "SAAS", "ARCHITECTURE"]
---

# Dashboard SaaS Complet

<div
  class="omny-meta"
  data-level="⚫ Expert"
  data-version="Livewire 3.x"
  data-time="5 Heures">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "Le Projet Pilier de l'Infrastructure Cœur"
    Tous vos apprentissages (Data Binding de base, Validation, Recherche avancée, Asynchrone temporel) se concentrent dans ce panel d'Administration à l'image des grands SaaS commerciaux (Stripe ou TailwindUI). Gérer multiples bases de données, protéger des routes en autorisant un usage Livewire uniquement sous certaines conditions (`Policies`) : c'est notre épreuve de force Terminale.
    
<br>

![Livewire Cloud Dashboard Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/livewire_dashboard_1775233304550.png)
<p><em>Maquette UI conceptuelle du projet : Un panel applicatif de rang entreprise.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu
- **Sécurisation (Auth) totale** : le composant de page doit vérifier les ACL (Access Controls).
- **Navigation (SPA Style)** via les directives Livewire Nav.
- **Tableau de Bord centralisé** : Un système consolidant des graphiques métriques (avec intégration Alpine.js pour Chart.js).
- **Facturation (Billing)** interactif : Upgrade de plan avec un modal sans reset visuel.

### Concepts Livewire Ultra-Avancés déployés
- Les composantes de Pleine Page (Full-Page Components).
- L'activation de la navigation ultra-rapide `wire:navigate`.
- Entremêlement avec (Alpine.js) et le `@entangle`.
- Protections de méthodes lourdes (`Authorize`).

<br>

---

## 2. Le Modèle d'Architecture Full-Page

Une "Full-Page Component" signifie que Livewire intercepte directement l'URL demandée par les `routes/web.php` du framework. Il n'est plus appelé en tant que petit module `livewire:user-card` au sein d'une page Blade parente, il est le maître absolu des lieux.

```php title="routes/web.php"
<?php
// On associe l'URL complète directement à la classe Livewire ! 
Route::get('/saas/dashboard', App\Livewire\SaasDashboard::class)->middleware('auth');
```

```php title="app/Livewire/SaasDashboard.php"
<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Invoice;
use Livewire\Attributes\Layout;

// Ce simple attribut indique quel <HEAD> HTML et barre de menu master charger !
#[Layout('components.layouts.app')]
class SaasDashboard extends Component
{
    public $activeTab = 'overview';
    public $showUpgradeModal = false;

    // Protocole de sécurité bloquant de Livewire 3
    public function mount()
    {
        // Seules les admins peuvent charger le module mémoire
        if (!auth()->user()->is_admin) {
            abort(403);
        }
    }

    public function getRevenueProperty()
    {
        return Invoice::where('paid', true)->sum('amount');
    }

    public function generateMonthlyReportExport()
    {
        // ... Logique de génération ...
        return response()->download($filepath); // Livewire supporte le download natif !
    }

    public function render()
    {
        return view('livewire.saas-dashboard');
    }
}
```

<br>

---

## 3. L'Entremêlement SPA (Single Page) et Alpine.js

Si notre utilisateur clique sur la Facturation, le menu et l'entête global ne doivent pas vaciller. Nous activons `wire:navigate` pour court-circuiter le comportement du réseau.

```html title="resources/views/livewire/saas-dashboard.blade.php"
<div>
    <!-- Navigation SPA (Single Page Application) magique de Livewire v3 !! -->
    <nav class="sidebar">
        <!-- Livewire empêche le navigateur de s'éteindre. Il va fetcher le HTML et faire la transition tout seul ! -->
        <a href="/saas/dashboard" wire:navigate class="active">Overview</a>
        <a href="/saas/invoices" wire:navigate>Factures</a>
        <a href="/saas/settings" wire:navigate>Paramètres</a>
    </nav>
    
    <main class="content">
        <h1>Overview : Chiffre généré {{ $this->revenue }}€</h1>
        
        <!-- On ouvre un Modal (Géré par AlpineJS en Front !!) -->
        <!-- @entangle connecte organiquement la variable X-DATA avec la variable PHP LIVEWIRE du serveur !! -->
        <div x-data="{ open: @entangle('showUpgradeModal') }">
            <button @click="open = true">Passer en Premium SaaS</button>
            
            <div x-show="open" class="modal-design" style="display:none;">
                <p>Nouveau Plan Ultra !</p>
                <!-- Ce clic appellera une méthode PHP qui changera la BD, et si elle fait un $this->showUpgradeModal = false, le Modal Alpine.JS se fermera tout seul !! -->
                <button wire:click="upgradePlan">Valider la Carte Crédit</button>
            </div>
        </div>
        
    </main>
</div>
```

<br>

---

## Conclusion et Certification de fin

!!! quote "Félicitations, vous maîtrisez l'Architecture Laravel Avancée !"
    Intégrer les vues ReactJS ou Vue.js avec Next est parfois indispensable pour les applications de pur divertissement ou les calculs mathématiques locaux (Jeux Vidéo, Streaming Video Web). En revanche, **construire l'UI d'un ERP B2B complexe en Livewire divise par trois la maintenance d'équipe.** Vous venez d'assister à la fin d'un débat stérile (Front VS Back) : la Stack TALL et le compositing `wire:navigate` avec `@entangle` propulsent PHP dans l'Ère Ultra-Moderne.

> Votre épreuve Livewire Lab est réussie. Vous êtes aptes à développer en entreprise un SI ou un panel d'outils interactifs complexes sur demande de spécifications métiers.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
