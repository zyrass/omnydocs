---
description: "Tailwind CSS — Composants & Extraction : @apply, Blade components, conventions d'organisation pour maintenir un projet Tailwind propre à grande échelle."
icon: lucide/book-open-check
tags: ["TAILWIND", "COMPOSANTS", "APPLY", "BLADE", "ORGANISATION", "MAINTENABILITE"]
---

# Composants & Extraction

<div
  class="omny-meta"
  data-level="🟡→🔴 Avancé"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothèque de Briques LEGO"
    Un maître LEGO ne réassemble pas les mêmes briques à chaque construction — il crée des sous-ensembles réutilisables (une porte, une fenêtre, un pignon) qu'il assemble ensuite en maisons différentes. `@apply` et les Blade Components jouent ce rôle dans Tailwind : extraire les combinaisons de classes répétées en composants nommés, sans sortir du paradigme utility-first.

L'objection la plus fréquente à Tailwind est la répétition. Ce module montre **quand et comment extraire** des classes en composants, et comment organiser un projet Tailwind à grande échelle.

<br>

---

## Le Problème de la Répétition

```html title="HTML (Tailwind) — Anti-pattern : copier-coller de classes"
{{-- MAL : 3 boutons "primary" identiques, copiés-collés --}}
<button class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition">
  Enregistrer
</button>
<button class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition">
  Publier
</button>
<button class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition">
  Valider
</button>
{{-- Si on change le design, il faut modifier 3 endroits --}}
```

**La règle d'or :** Si vous copiez-collez les mêmes classes Tailwind plus de 2-3 fois, c'est le signal d'extraction.

<br>

---

## Solution 1 — Blade Components (Recommandé)

La meilleure pratique Tailwind + Laravel : extraire dans des **Blade Components**.

```bash title="Bash — Créer un composant Blade avec Artisan"
# Créer le composant Button
php artisan make:component Button

# Génère :
# app/View/Components/Button.php  (classe PHP)
# resources/views/components/button.blade.php (template)
```

```php title="PHP — app/View/Components/Button.php : logique du composant"
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Button extends Component
{
    /**
     * @param string $variant Variante visuelle : primary, secondary, danger, ghost
     * @param string $size    Taille : sm, md, lg
     * @param string $type    Type HTML : button, submit, reset
     */
    public function __construct(
        public string $variant = 'primary',
        public string $size    = 'md',
        public string $type    = 'button',
    ) {}

    /**
     * Retourne les classes Tailwind selon la variante
     */
    public function variantClasses(): string
    {
        return match($this->variant) {
            'primary'   => 'bg-blue-600 hover:bg-blue-700 text-white',
            'secondary' => 'bg-gray-100 hover:bg-gray-200 text-gray-700',
            'danger'    => 'bg-red-600 hover:bg-red-700 text-white',
            'ghost'     => 'hover:bg-gray-100 text-gray-600',
            default     => 'bg-blue-600 hover:bg-blue-700 text-white',
        };
    }

    /**
     * Retourne les classes Tailwind selon la taille
     */
    public function sizeClasses(): string
    {
        return match($this->size) {
            'sm' => 'text-xs px-3 py-1.5',
            'md' => 'text-sm px-4 py-2',
            'lg' => 'text-base px-6 py-3',
            default => 'text-sm px-4 py-2',
        };
    }

    public function render()
    {
        return view('components.button');
    }
}
```

```html title="Blade — resources/views/components/button.blade.php : template"
{{-- Fusionne les classes du composant avec celles passées par l'appelant --}}
<button
    {{ $attributes->merge([
        'type'  => $type,
        'class' => $variantClasses() . ' ' . $sizeClasses() .
                   ' font-medium rounded-lg transition-colors duration-200 inline-flex items-center gap-2'
    ]) }}
>
    {{-- Slot par défaut : contenu du bouton --}}
    {{ $slot }}
</button>
```

```html title="Blade — Utilisation du composant Button dans vos vues"
{{-- Bouton primary md (défaut) --}}
<x-button>Enregistrer</x-button>

{{-- Variantes --}}
<x-button variant="secondary">Annuler</x-button>
<x-button variant="danger">Supprimer</x-button>
<x-button variant="ghost">Voir plus</x-button>

{{-- Tailles --}}
<x-button size="sm">Compact</x-button>
<x-button size="lg">Proéminent</x-button>

{{-- Type submit avec classes supplémentaires --}}
<x-button type="submit" class="w-full mt-4">
    <x-icon name="save" class="w-4 h-4" />
    Sauvegarder les modifications
</x-button>

{{-- Classes Tailwind supplémentaires via $attributes->merge --}}
<x-button class="ml-auto">Action à droite</x-button>
```

*`$attributes->merge()` fusionne les attributs du composant avec ceux passés par l'appelant — les classes `class="w-full"` s'ajoutent aux classes du composant sans les remplacer.*

<br>

---

## Solution 2 — @apply (Usage Limité)

`@apply` permet d'extraire des classes Tailwind dans du CSS.

```css title="CSS — resources/css/app.css : @apply pour les patterns très répétitifs"
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ─── Composants @layer ──────────────────────────────────────────────────── */
/* Restriction : @apply est approprié pour les éléments HTML natifs
   (input, select, table) ou pour les classes très courtes et souvent utilisées.
   Préférez les Blade Components pour tout le reste. */

@layer components {
  /* Input standard */
  .input-base {
    @apply w-full border border-gray-300 rounded-lg px-3 py-2
           focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
           outline-none transition-colors duration-200
           placeholder:text-gray-400 text-sm;
  }

  /* Input avec erreur */
  .input-error {
    @apply input-base border-red-400 focus:border-red-500 focus:ring-red-500/20;
  }

  /* Badge générique */
  .badge {
    @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
  }
}
```

```html title="HTML (Tailwind) — Utilisation des classes @apply"
{{-- Input standard --}}
<input type="text" class="input-base" placeholder="Nom d'utilisateur" />

{{-- Input avec erreur --}}
<input type="email" class="input-error" placeholder="Email invalide" />

{{-- Badges --}}
<span class="badge bg-blue-100 text-blue-700">Laravel</span>
<span class="badge bg-emerald-100 text-emerald-700">Publié</span>
```

!!! warning "Limites de @apply"
    `@apply` ne supporte pas les variantes (`hover:`, `md:`) dans les versions récentes de Tailwind. Il est réservé aux classes statiques simples. Pour la majorité des composants, les **Blade Components** sont la bonne solution.

<br>

---

## Organisation d'un Projet Tailwind

### Structure de Fichiers Recommandée

```
resources/
├── css/
│   └── app.css               # @tailwind base/components/utilities + @apply limités
├── js/
│   └── app.js
└── views/
    ├── components/           # Blade Components (UI réutilisable)
    │   ├── button.blade.php
    │   ├── card.blade.php
    │   ├── badge.blade.php
    │   ├── input.blade.php
    │   ├── modal.blade.php
    │   └── alert.blade.php
    ├── layouts/              # Layouts de page
    │   ├── app.blade.php     # Layout principal avec nav + footer
    │   └── auth.blade.php    # Layout pour login/register
    └── pages/                # Pages de l'application
        ├── dashboard.blade.php
        └── profile.blade.php
```

### Composant Card Complet

```php title="PHP — app/View/Components/Card.php"
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Card extends Component
{
    public function __construct(
        public string  $padding = 'md',
        public bool    $shadow  = true,
        public bool    $border  = true,
        public ?string $title   = null,
        public ?string $footer  = null,
    ) {}

    public function paddingClasses(): string
    {
        return match($this->padding) {
            'none' => '',
            'sm'   => 'p-3',
            'md'   => 'p-6',
            'lg'   => 'p-8',
            default => 'p-6',
        };
    }

    public function render()
    {
        return view('components.card');
    }
}
```

```html title="Blade — resources/views/components/card.blade.php"
<div {{ $attributes->merge([
    'class' => 'bg-white rounded-xl ' .
               ($border  ? 'border border-gray-200 ' : '') .
               ($shadow  ? 'shadow-sm ' : '') .
               ($padding !== 'none' ? '' : '')
]) }}>

    {{-- Header optionnel --}}
    @if($title)
    <div class="{{ $paddingClasses() }} border-b border-gray-200">
        <h3 class="text-base font-semibold text-gray-900">{{ $title }}</h3>
    </div>
    @endif

    {{-- Contenu --}}
    <div class="{{ $paddingClasses() }}">
        {{ $slot }}
    </div>

    {{-- Footer optionnel --}}
    @if($footer)
    <div class="{{ $paddingClasses() }} border-t border-gray-100 bg-gray-50 rounded-b-xl">
        {{ $footer }}
    </div>
    @endif
</div>
```

```html title="Blade — Utilisation du composant Card"
{{-- Carte simple --}}
<x-card>
    <p>Contenu simple</p>
</x-card>

{{-- Carte avec titre et footer --}}
<x-card title="Informations de profil">
    <form><!-- ... --></form>

    <x-slot:footer>
        <div class="flex justify-end gap-3">
            <x-button variant="secondary">Annuler</x-button>
            <x-button type="submit">Enregistrer</x-button>
        </div>
    </x-slot:footer>
</x-card>

{{-- Carte sans ombre ni bordure --}}
<x-card :shadow="false" :border="false" padding="none">
    Contenu sans décoration
</x-card>
```

<br>

---

## Conventions de Nommage

| Convention | Recommandé | Éviter |
|---|---|---|
| **Composants Blade** | `x-button`, `x-card`, `x-alert` | Créer des `.css` pour chaque composant |
| **@apply** | Classes HTML natives, patterns < 3 classes | Composants complexes |
| **Classes arbitraires** | `w-[312px]`, `top-[60px]` (unique) | En masse, partout |
| **Valeurs custom** | Via `tailwind.config.js → extend` | `style=""` ou CSS inline |
| **Dark mode** | `dark:` sur chaque classe concernée | Fichiers CSS séparés |

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Composant Alert**

```bash title="Bash — Exercice 1 : créer le composant Alert"
# Créez un composant x-alert avec :
# - Variantes : success, warning, error, info
# - Chaque variante a sa couleur de fond, icône, texte
# - Slot pour le message
# - Slot:title optionnel pour le titre
# - Bouton de fermeture optionnel (Alpine.js : x-data x-show @click)
php artisan make:component Alert
```

**Exercice 2 — Composant Input**

```bash title="Bash — Exercice 2 : créer le composant Input"
# Créez un composant x-input avec :
# - Props : label, name, type, placeholder, error (message d'erreur), hint
# - Affiche le label au-dessus si fourni
# - Affiche le message d'erreur en rouge si fourni
# - Affiche le hint en gris si fourni (sinon le message d'erreur le remplace)
# - Intégration avec $errors de Laravel Livewire
php artisan make:component Input
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La réponse au problème de répétition Tailwind est **les Blade Components** — pas `@apply`. `@apply` reste utile pour les éléments HTML natifs (`input`, `select`) et les patterns très courts. Les composants Blade offrent la logique PHP (`match` pour les variantes), les props typées, les slots nommés, et `$attributes->merge()` pour la composition de classes. La structure de fichiers recommandée sépare `layouts/`, `components/`, et `pages/`. Une règle simple : si vous copiez-collez plus de 2 fois, extrayez en Blade Component.

> Dans le dernier module, nous couvrons le **theming avancé et les plugins** — personnaliser `tailwind.config.js`, les plugins officiels (`@tailwindcss/forms`, `@tailwindcss/typography`), et l'intégration de DaisyUI.

<br>
