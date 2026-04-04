---
description: "Tailwind CSS — Plugins & Theming Avancé : tailwind.config.js extend, plugins officiels forms et typography, création de plugins custom, intégration DaisyUI."
icon: lucide/book-open-check
tags: ["TAILWIND", "THEMES", "PLUGINS", "CONFIGURATION", "DAISYUI", "TYPOGRAPHY"]
---

# Plugins & Theming Avancé

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Atelier sur Mesure"
    Un artisan ébéniste ne se contente pas des outils standard — il affûte ses ciseaux, fabrique les gabarits adaptés à son projet, et ajoute parfois des machines spécialisées. La configuration avancée de Tailwind, c'est cet atelier sur mesure : `extend` ajoute vos propres valeurs sans briser les défauts, les plugins officiels ajoutent des composants clé-en-main (formulaires, typographie), et DaisyUI fournit une bibliothèque de thèmes visuels entiers construits sur Tailwind.

Ce module clôt la formation avec l'outillage qui fait la différence entre un projet Tailwind basique et un projet professionnel maintenable.

<br>

---

## Customisation via `tailwind.config.js`

### La Différence entre `theme` et `theme.extend`

```js title="JavaScript — tailwind.config.js : theme vs theme.extend"
module.exports = {
  content: ['./resources/**/*.{blade.php,js}'],

  theme: {
    // ⚠️ REMPLACE les valeurs Tailwind par défaut
    // À n'utiliser que si vous voulez un design system totalement custom
    colors: {
      // Si vous faites ça, TOUTES les couleurs Tailwind disparaissent
      // (plus de bg-blue-500, bg-gray-200, etc.)
      brand: '#3b82f6',
    },

    // ✅ ÉTEND les valeurs Tailwind — le plus courant et recommandé
    extend: {
      // Ajoute VOS couleurs sans supprimer celles de Tailwind
      colors: {
        brand: {
          50:  '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',   // Couleur principale
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        // Couleur de surface pour dark mode
        surface: {
          DEFAULT: '#ffffff',
          dark:    '#0f172a',
        },
      },
    },
  },
}
```

### Étendre Toutes les Catégories

```js title="JavaScript — tailwind.config.js : extend complet pour un design system"
module.exports = {
  content: ['./resources/**/*.{blade.php,js,vue}'],
  darkMode: 'class',

  theme: {
    extend: {
      // ─── Couleurs ──────────────────────────────────────────────────────────
      colors: {
        brand:   { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' },
        success: { 100: '#dcfce7', 500: '#22c55e', 700: '#15803d' },
        warning: { 100: '#fef9c3', 500: '#eab308', 700: '#a16207' },
        danger:  { 100: '#fee2e2', 500: '#ef4444', 700: '#b91c1c' },
      },

      // ─── Typographie ───────────────────────────────────────────────────────
      fontFamily: {
        // Ajoute une police custom (à charger depuis Google Fonts)
        sans:  ['Inter', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'monospace'],
        serif: ['Lora', 'Georgia', 'serif'],
      },

      fontSize: {
        'xxs': ['0.65rem', { lineHeight: '1rem' }],
        '2xs': ['0.7rem',  { lineHeight: '1rem' }],
      },

      // ─── Espacements ───────────────────────────────────────────────────────
      spacing: {
        '18': '4.5rem',   // gap manquant dans l'échelle standard
        '88': '22rem',
        '112': '28rem',
        '128': '32rem',
      },

      // ─── Border Radius ─────────────────────────────────────────────────────
      borderRadius: {
        '4xl': '2rem',
      },

      // ─── Box Shadow ────────────────────────────────────────────────────────
      boxShadow: {
        // Ombres colorées pour les cartes feature
        'brand':   '0 10px 30px -5px rgb(99 102 241 / 0.4)',
        'success': '0 10px 30px -5px rgb(34 197 94 / 0.4)',
      },

      // ─── Animation ─────────────────────────────────────────────────────────
      animation: {
        'fade-in':     'fadeIn 300ms ease-out',
        'slide-up':    'slideUp 400ms ease-out',
        'slide-down':  'slideDown 300ms ease-out',
        'accordion':   'accordion 300ms ease-out',
      },

      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%':   { opacity: '0', transform: 'translateY(-8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        accordion: {
          '0%':   { height: '0', opacity: '0' },
          '100%': { height: 'var(--radix-accordion-content-height)', opacity: '1' },
        },
      },

      // ─── Transitions ───────────────────────────────────────────────────────
      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
      },

      // ─── Taille max ────────────────────────────────────────────────────────
      maxWidth: {
        '8xl': '88rem',  // 1408px
        '9xl': '96rem',  // 1536px
      },
    },
  },
}
```

*Utiliser `extend` garantit que toutes les classes Tailwind natives restent disponibles. Vos ajouts s'accumulent plutôt que de remplacer.*

<br>

---

## Plugins Officiels

### @tailwindcss/forms

```bash title="Bash — Installation du plugin forms"
npm install -D @tailwindcss/forms
```

```js title="JavaScript — tailwind.config.js : activer le plugin forms"
module.exports = {
  plugins: [
    // Réinitialise le style des <input>, <select>, <textarea>, <checkbox>
    // pour les rendre facilement stylisables avec des classes Tailwind
    require('@tailwindcss/forms'),

    // Option : strategy class pour n'affecter que les éléments avec la classe 'form-*'
    // require('@tailwindcss/forms')({ strategy: 'class' }),
  ],
}
```

```html title="HTML (Tailwind) — Formulaire avec @tailwindcss/forms"
{{-- Sans @tailwindcss/forms : les inputs ont des styles OS inconsistants --}}
{{-- Avec : base reset appliqué, classes Tailwind prennent l'effet immédiatement --}}

<form class="space-y-4">
  {{-- Input text --}}
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
    <input type="text"
           class="w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500 text-sm" />
  </div>

  {{-- Select --}}
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">Catégorie</label>
    <select class="w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500 text-sm">
      <option>Laravel</option>
      <option>Alpine.js</option>
      <option>Tailwind</option>
    </select>
  </div>

  {{-- Checkbox --}}
  <label class="flex items-center gap-2">
    <input type="checkbox"
           class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
    <span class="text-sm text-gray-700">Accepter les conditions</span>
  </label>
</form>
```

### @tailwindcss/typography

```bash title="Bash — Installation du plugin typography"
npm install -D @tailwindcss/typography
```

```js title="JavaScript — tailwind.config.js : activer le plugin typography"
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

```html title="HTML (Tailwind) — Rendu Markdown avec la classe prose"
{{-- La classe 'prose' stylise automatiquement le contenu HTML arbitraire --}}
{{-- Idéal pour : articles de blog, documentation, contenu Markdown converti --}}

<article class="prose prose-lg prose-blue max-w-prose mx-auto">
  {{-- Tout le contenu suivant est automatiquement stylisé : --}}
  <h1>Titre de l'article</h1>           {{-- Titre en grande police --}}
  <p>Introduction du contenu...</p>      {{-- Paragraphes avec bonne hauteur de ligne --}}
  <h2>Sous-titre</h2>
  <ul>
    <li>Élément de liste</li>           {{-- Listes stylisées --}}
  </ul>
  <code>du code inline</code>           {{-- Code avec fond gris --}}
  <pre><code>bloc de code</code></pre>  {{-- Bloc de code avec coloration --}}
  <blockquote>Citation</blockquote>     {{-- Blockquote avec bordure gauche --}}
</article>

{{-- Variantes taille : prose-sm, prose (défaut), prose-lg, prose-xl, prose-2xl --}}
{{-- Couleurs : prose-blue (liens bleus), prose-gray, prose-slate, etc. --}}
{{-- Dark mode : dark:prose-invert (inverse les couleurs en mode sombre) --}}

<article class="prose dark:prose-invert max-w-prose">
  {!! $article->content !!}
</article>
```

<br>

---

## Créer un Plugin Custom

```js title="JavaScript — tailwind.config.js : plugin custom pour les patterns répétitifs"
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    // Plugin inline pour des utilitaires custom
    plugin(function({ addUtilities, addComponents, theme }) {

      // ─── Utilitaires personnalisés ────────────────────────────────────────
      addUtilities({
        // Utilitaire pour les textes tronqués sur plusieurs lignes
        '.line-clamp-2': {
          display:            '-webkit-box',
          '-webkit-line-clamp': '2',
          '-webkit-box-orient': 'vertical',
          overflow:           'hidden',
        },
        '.line-clamp-3': {
          display:            '-webkit-box',
          '-webkit-line-clamp': '3',
          '-webkit-box-orient': 'vertical',
          overflow:           'hidden',
        },
        // Scroll snap
        '.scroll-snap-x': { 'scroll-snap-type': 'x mandatory' },
        '.scroll-snap-start': { 'scroll-snap-align': 'start' },
      });

      // ─── Composants personnalisés (@layer components) ─────────────────────
      addComponents({
        // Conteneur de mise en page standard
        '.container-app': {
          width:    '100%',
          maxWidth: '80rem',   // 1280px = max-w-7xl
          margin:   '0 auto',
          padding:  '0 1rem',
          '@screen sm': { padding: '0 1.5rem' },
          '@screen lg': { padding: '0 2rem' },
        },
      });
    }),
  ],
}
```

```html title="HTML (Tailwind) — Utilisation du plugin custom"
{{-- Utilitaire line-clamp : tronque à 2 lignes --}}
<p class="line-clamp-2">
  Ce texte très long sera automatiquement tronqué au bout de deux lignes
  avec des points de suspension, peu importe la taille de l'écran.
</p>

{{-- Conteneur app standard --}}
<div class="container-app py-12">
  Contenu centré avec padding responsive
</div>
```

<br>

---

## DaisyUI — Bibliothèque de Thèmes

DaisyUI est un plugin Tailwind qui ajoute des composants sémantiques et des thèmes visuels.

```bash title="Bash — Installation de DaisyUI"
npm install -D daisyui@latest
```

```js title="JavaScript — tailwind.config.js : intégration DaisyUI"
module.exports = {
  plugins: [
    require('daisyui'),
  ],

  daisyui: {
    // Thèmes disponibles : light, dark, cupcake, bumblebee, emerald, corporate,
    //                      synthwave, retro, cyberpunk, valentine, halloween,
    //                      garden, forest, aqua, lofi, pastel, fantasy, black, luxury, etc.
    themes: ['light', 'dark', 'corporate'],

    // Thème actif par défaut
    darkTheme: 'dark',

    // Désactiver si vous n'avez pas besoin de tous les composants DaisyUI
    // et préférez cibler uniquement ce que vous utilisez
    base:       true,
    styled:     true,
    utils:      true,
    logs:       false,
  },
}
```

```html title="HTML (DaisyUI) — Composants DaisyUI avec classes sémantiques"
{{-- DaisyUI ajoute des classes sémantiques au-dessus de Tailwind --}}

{{-- Boutons DaisyUI --}}
<button class="btn btn-primary">Enregistrer</button>
<button class="btn btn-secondary btn-sm">Annuler</button>
<button class="btn btn-error btn-outline">Supprimer</button>
<button class="btn loading">Chargement...</button>

{{-- Card DaisyUI --}}
<div class="card bg-base-100 shadow-xl">
  <div class="card-body">
    <h2 class="card-title">Module Tailwind</h2>
    <p>Formation complète du débutant à l'avancé.</p>
    <div class="card-actions justify-end">
      <button class="btn btn-primary">Commencer</button>
    </div>
  </div>
</div>

{{-- Alert DaisyUI --}}
<div class="alert alert-success">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
  <span>Article publié avec succès !</span>
</div>

{{-- Badge DaisyUI --}}
<div class="badge badge-primary">Laravel</div>
<div class="badge badge-outline">Tailwind</div>

{{-- Modal DaisyUI --}}
<dialog id="modal_confirm" class="modal">
  <form method="dialog" class="modal-box">
    <h3 class="font-bold text-lg">Confirmer la suppression</h3>
    <p class="py-4">Cette action est irréversible. Êtes-vous sûr ?</p>
    <div class="modal-action">
      <button class="btn">Annuler</button>
      <button class="btn btn-error">Supprimer</button>
    </div>
  </form>
</dialog>
```

*DaisyUI coexiste parfaitement avec Tailwind — vous pouvez mélanger classes DaisyUI (`btn btn-primary`) et classes Tailwind (`mt-4 text-sm`) sur le même élément.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Design System Custom**

```js title="JavaScript — Exercice 1 : configurer un design system complet"
// Dans tailwind.config.js, étendez le thème avec :
// - Palette de couleurs "brand" (indigo/violet, 50-950)
// - Police sans-serif : Inter (charger depuis Google Fonts dans le layout)
// - 2 animations custom : fadeIn (opacité 0→1) et slideUp (translateY 16px→0)
// - Shadow colorée "brand-glow" pour les cartes feature
// Vérifiez que les nouvelles classes sont disponibles dans le HTML
```

**Exercice 2 — Comparaison**

```html title="HTML — Exercice 2 : mêmes composants Tailwind vs DaisyUI"
<!-- Recréez ce formulaire en deux versions :
     Version A : uniquement with classes Tailwind utilitaires
     Version B : avec DaisyUI (btn, input, label, card)
     
     Formulaire : champ nom, champ email, select catégorie, checkbox CGU, bouton submit
     
     Comparez la quantité de classes, la lisibilité, la personnalisabilité -->
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `theme.extend` est le mécanisme central pour personnaliser Tailwind sans perdre les défauts — couleurs, fonts, spacings, animations, shadows sont tous extensibles. `@tailwindcss/forms` normalise les inputs entre navigateurs. `@tailwindcss/typography` stylise le contenu Markdown via la classe `prose`. Les plugins custom permettent d'ajouter des utilitaires et composants métier. DaisyUI superpose une couche de composants sémantiques sur Tailwind — idéal pour prototyper rapidement tout en gardant la flexibilité utility-first pour les détails.

> **Formation complète.** Vous maîtrisez maintenant Tailwind CSS de la philosophie utility-first jusqu'au theming avancé. La prochaine étape naturelle est d'appliquer Tailwind dans le contexte de la **Stack TALL** — [Alpine.js](../alpine/index.md), [Livewire](../livewire/index.md), [Laravel](../laravel/index.md) vous attendent.

<br>
