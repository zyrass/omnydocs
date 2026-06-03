---
description: "Personnalisation des vues Blade générées par Breeze : layout, navigation, dashboard et formulaires stylisés avec Tailwind CSS."
icon: lucide/book-open-check
tags: ["LARAVEL", "BREEZE", "PROJET GUIDÉ"]
---

# Phase 3 — Vues Blade & Interface

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Laravel 11"
  data-time="~1h30">
</div>

## Objectifs de la Phase 3

!!! info "Ce que vous allez faire"
    - Comprendre la structure des vues Breeze (`resources/views/auth/`, `layouts/`)
    - Personnaliser le layout principal et la navigation
    - Styliser le dashboard avec Tailwind CSS
    - Modifier les formulaires d'inscription et de connexion

## Structure des Vues Breeze

```
resources/views/
├── auth/
│   ├── login.blade.php        # Formulaire de connexion
│   ├── register.blade.php     # Formulaire d'inscription
│   ├── forgot-password.blade.php
│   └── reset-password.blade.php
├── layouts/
│   ├── app.blade.php          # Layout principal (auth)
│   └── guest.blade.php        # Layout invité (login/register)
├── components/
│   ├── nav-link.blade.php
│   └── responsive-nav-link.blade.php
└── dashboard.blade.php        # Page d'accueil post-connexion
```

## Personnalisation du Dashboard

```html title="resources/views/dashboard.blade.php"
<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Tableau de bord') }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6 text-gray-900">
                    Bonjour, <strong>{{ Auth::user()->name }}</strong> !
                    Vous êtes connecté depuis {{ Auth::user()->last_login_at?->diffForHumans() ?? 'maintenant' }}.
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
```

```bash
# Recompiler les assets après modification du CSS
npm run dev
```


<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les vues Blade de Breeze ne sont pas un template figé — elles sont le point de départ de **votre** interface. La puissance des composants Blade (`<x-app-layout>`, `<x-input-label>`) est qu'ils sont réutilisables : modifiez le composant une fois, et le changement se propage partout où il est utilisé. C'est la composition au service de la cohérence visuelle.

> [Phase 4 — Page de profil et upload d'avatar →](./phase4.md)
