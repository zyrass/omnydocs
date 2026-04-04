---
description: "Tailwind CSS — États & Interactions : hover, focus, active, group-hover, peer, transitions et animations pour des interfaces réactives sans JavaScript."
icon: lucide/book-open-check
tags: ["TAILWIND", "HOVER", "FOCUS", "GROUP", "PEER", "TRANSITIONS", "ANIMATIONS"]
---

# États & Interactions

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="3.x"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Feu de Signalisation"
    Un feu de signalisation change de couleur selon son état — vert, orange, rouge. Il ne nécessite pas de conducteur pour décider : la règle est fixée et s'applique automatiquement. Les variantes d'état Tailwind fonctionnent pareil : `hover:bg-blue-700` signifie "quand l'élément est survolé, applique `bg-blue-700`". La règle est dans le HTML, CSS la déclenche automatiquement — aucun JavaScript nécessaire pour 90% des interactions visuelles.

Tailwind fournit des **variantes d'état** qui s'appliquent à presque toutes les classes. La syntaxe est toujours `état:classe`.

<br>

---

## États de Base

```html title="HTML (Tailwind) — États fondamentaux : hover, focus, active, disabled"
<!-- hover : au survol de la souris -->
<button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
  Enregistrer
</button>

<!-- focus : lorsque l'élément reçoit le focus (clavier/clic) -->
<input class="border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
              rounded-lg px-3 py-2 outline-none" />

<!-- active : pendant le clic -->
<button class="bg-blue-600 hover:bg-blue-700 active:bg-blue-800 
               active:scale-95 transition text-white px-4 py-2 rounded-lg">
  Cliquer
</button>

<!-- disabled : élément désactivé -->
<button disabled class="bg-gray-300 cursor-not-allowed text-gray-500 px-4 py-2 rounded-lg
                        disabled:opacity-50">
  Action indisponible
</button>

<!-- focus-visible : seulement avec navigation clavier (meilleure UX) -->
<button class="focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2
               rounded-lg px-4 py-2 outline-none">
  Accessible
</button>

<!-- checked : case à cocher ou radio cochée -->
<input type="checkbox"
       class="checked:bg-blue-600 checked:border-blue-600 border-2 border-gray-300 rounded" />

<!-- placeholder : le texte placeholder des inputs -->
<input placeholder="Rechercher..."
       class="placeholder:text-gray-400 placeholder:text-sm px-3 py-2 border rounded-lg" />
```

<br>

---

## Transitions

```html title="HTML (Tailwind) — Transitions : durée, propriétés, timing function"
<!-- transition : applique une transition sur les propriétés qui changent -->
<button class="bg-blue-600 hover:bg-blue-700 transition text-white px-4 py-2 rounded-lg">
  <!-- transition = transition-property: all; transition-duration: 150ms -->
</button>

<!-- Cibler des propriétés spécifiques (plus performant) -->
<div class="transition-colors duration-200">   <!-- Seulement les couleurs -->
<div class="transition-opacity duration-300">  <!-- Seulement l'opacité -->
<div class="transition-transform duration-200"> <!-- Seulement les transformations -->

<!-- Durée -->
<div class="transition duration-75">   <!-- 75ms -->
<div class="transition duration-150">  <!-- 150ms — défaut -->
<div class="transition duration-200">  <!-- 200ms -->
<div class="transition duration-300">  <!-- 300ms -->
<div class="transition duration-500">  <!-- 500ms -->
<div class="transition duration-700">  <!-- 700ms -->
<div class="transition duration-1000"> <!-- 1000ms -->

<!-- Timing function (ease) -->
<div class="transition ease-linear">    <!-- linear -->
<div class="transition ease-in">        <!-- ease-in -->
<div class="transition ease-out">       <!-- ease-out -->
<div class="transition ease-in-out">    <!-- ease-in-out — défaut -->
```

### Exemple — Bouton avec Effet Complet

```html title="HTML (Tailwind) — Bouton : transitions multiples coordonnées"
<button class="
  bg-blue-600 text-white font-medium px-6 py-3 rounded-xl
  hover:bg-blue-700
  hover:shadow-lg hover:shadow-blue-500/25
  hover:-translate-y-0.5
  active:translate-y-0 active:shadow-none
  transition-all duration-200 ease-out
">
  Publier l'article
</button>
```

*`-translate-y-0.5` fait monter l'élément de 2px au survol. `active:translate-y-0` le remet à sa position originale au clic. `shadow-blue-500/25` est une ombre colorée à 25% d'opacité.*

<br>

---

## Transformations

```html title="HTML (Tailwind) — Transform : scale, translate, rotate"
<!-- Scale -->
<img class="hover:scale-105 transition-transform duration-200 rounded-lg" />
<button class="active:scale-95 transition-transform">Clic</button>

<!-- Translate -->
<div class="hover:-translate-y-1 transition-transform duration-200">
  Carte qui monte au survol
</div>
<div class="hover:translate-x-1 transition-transform">
  Icône qui glisse à droite
</div>

<!-- Rotate -->
<svg class="hover:rotate-90 transition-transform duration-200 w-5 h-5">
  Icône qui pivote
</svg>
<div class="group-open:rotate-180 transition-transform">
  Chevron de <details>
</div>
```

<br>

---

## Group — Styles selon le Parent Survolé

La variante `group` permet de styliser un enfant en fonction de l'état du parent.

```html title="HTML (Tailwind) — group-hover : styler un enfant depuis le parent"
<!-- Étape 1 : marquer le conteneur avec class="group" -->
<!-- Étape 2 : utiliser group-hover: sur les enfants -->
<div class="group bg-white hover:bg-blue-600 rounded-xl p-6 cursor-pointer
            border border-gray-200 hover:border-blue-600 transition-all duration-200">

  <!-- L'icône change de couleur quand le parent est survolé -->
  <div class="w-10 h-10 bg-blue-100 group-hover:bg-blue-500/20 rounded-lg
              flex items-center justify-center mb-4 transition-colors">
    <svg class="w-5 h-5 text-blue-600 group-hover:text-white transition-colors">
      <!-- icône -->
    </svg>
  </div>

  <!-- Le titre change de couleur -->
  <h3 class="font-semibold text-gray-900 group-hover:text-white mb-2 transition-colors">
    Module Tailwind
  </h3>

  <!-- La description change d'opacité -->
  <p class="text-gray-500 group-hover:text-blue-100 text-sm transition-colors">
    Apprenez Tailwind CSS de zéro à avancé.
  </p>

  <!-- La flèche glisse vers la droite -->
  <div class="flex items-center gap-1 mt-4 text-blue-600 group-hover:text-white transition-colors">
    <span class="text-sm font-medium">Accéder</span>
    <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform">
      <!-- flèche droite -->
    </svg>
  </div>
</div>
```

*Ce pattern "carte interactive" est l'un des plus utilisés dans les interfaces Tailwind. Sans JavaScript, sans CSS custom — uniquement `group` + `group-hover:`.*

<br>

---

## Peer — Styles selon un Élément Frère

La variante `peer` permet de styliser un élément selon l'état d'un élément frère précédent.

```html title="HTML (Tailwind) — peer : label qui réagit au focus/erreur de l'input"
<!-- Étape 1 : marquer l'input avec class="peer" -->
<!-- Étape 2 : utiliser peer-focus: peer-invalid: etc. sur les voisins SUIVANTS -->

<div class="space-y-1">
  <label class="text-sm font-medium text-gray-700">Email</label>

  <input
    type="email"
    placeholder="vous@exemple.com"
    class="peer w-full border border-gray-300 rounded-lg px-3 py-2
           focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20
           invalid:border-red-400 invalid:focus:border-red-500
           outline-none transition"
  />

  <!-- Message d'aide : visible au focus -->
  <p class="text-xs text-blue-500 hidden peer-focus:block">
    Entrez votre adresse email complète.
  </p>

  <!-- Message d'erreur : visible si l'email est invalide -->
  <p class="text-xs text-red-500 hidden peer-invalid:block peer-focus:peer-invalid:block">
    Format d'email invalide.
  </p>
</div>
```

*`peer-focus:block` s'active quand l'input `.peer` est en focus. `peer-invalid:block` s'active quand l'input est invalide (validation HTML native). Ce pattern remplace du JavaScript de validation simple.*

<br>

---

## Animations Built-in

```html title="HTML (Tailwind) — Animations natives : pulse, spin, bounce, ping"
<!-- Spinner de chargement -->
<svg class="animate-spin h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24">
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
</svg>

<!-- Skeleton loading (contenu en cours de chargement) -->
<div class="animate-pulse space-y-3">
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
  <div class="h-4 bg-gray-200 rounded w-5/6"></div>
</div>

<!-- Notification badge qui clignote -->
<span class="relative flex h-3 w-3">
  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
</span>

<!-- Flèche qui rebondit (scroll indicator) -->
<svg class="animate-bounce w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
</svg>
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Card Interactive**

```html title="HTML — Exercice 1 : carte avec group-hover"
<!-- Créez une carte de module de formation avec :
     - group sur le conteneur
     - Fond blanc → bleu foncé au hover (transition 300ms)
     - Titre gris foncé → blanc au hover
     - Description gris → bleu clair au hover
     - Icône dans une bulle qui change de couleur
     - Flèche qui glisse de 4px vers la droite au hover
     - Active:scale-98 pour le feedback de clic -->
```

**Exercice 2 — Formulaire avec peer**

```html title="HTML — Exercice 2 : input avec validation visuelle"
<!-- Créez un champ de mot de passe avec :
     - Label flottant qui monte au focus (technique avancée avec peer)
     - Bordure rouge si invalide (moins de 8 caractères → minlength="8")
     - Bordure verte si valide
     - Message d'aide visible au focus
     - Message d'erreur visible si invalide + pas en focus -->
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les variantes d'état Tailwind (`hover:`, `focus:`, `active:`, `disabled:`) transforment n'importe quelle classe en règle conditionnelle — sans JavaScript, sans CSS custom. `group` + `group-hover:` permet de styler un enfant depuis l'état du parent : c'est le pattern des cartes interactives. `peer` + `peer-focus:` permet de styler un voisin selon l'état d'un input : c'est le pattern des formulaires validés. `transition-all duration-200` crée des interactions fluides sur 200ms. `animate-spin`, `animate-pulse`, `animate-ping` couvrent les cas de chargement les plus fréquents.

> Dans le module suivant, nous abordons l'**organisation et l'extraction** — `@apply`, Blade components, conventions de nommage — pour maintenir un projet Tailwind propre à grande échelle.

<br>
