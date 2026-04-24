---
description: "Gérer l'interaction de l'utilisateur avec Alpine.js : Clics, Formulaires et Two-way Binding."
icon: lucide/book-open-check
tags: ["THEORIE", "ALPINE", "JAVASCRIPT", "FORMS"]
---

# Interactions et Événements

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Alpine 3.x"
  data-time="2 Heures">
</div>

!!! quote "L'Écouteur aux Portes"
    Dans une architecture Web classique, il fallait sans cesse relier le bouton d'interface `<button>` à un script JavaScript distant `document.querySelector('button').addEventListener('click')`. Avec Alpine.js, le **câblage (Binding)** est organique. C'est comme brancher un instrument de musique directement à un amplificateur : votre interface devient "connectée" aux données !

<br>

---

## 1. Intercepter le Comportement Utilisateur (`@click` et événements natifs)

Alpine.js simplifie l'API événementielle du navigateur native (clics, survols, envois). Pour écouter n'importe quel événement, utilisez `@nom_evenement` ou la syntaxe longue `x-on:nom_evenement`.

```html title="Événements Simples et Modificateurs"
<div x-data="{ count: 0 }">
    <!-- Clic classique -->
    <button @click="count++">
        Incrémenter
    </button>
    
    <!-- Survol (Hover) lié à une fonction JS -->
    <div @mouseenter="console.log('Survol détecté!')" class="box">
        Passez la souris ici
    </div>

    <!-- Modificateur .prevent équivaut à e.preventDefault() en JS classique -->
    <form @submit.prevent="alert('Formulaire non soumis au serveur !')">
        <button type="submit">Valider Localement</button>
    </form>
</div>
```

_Le symbole de l'arobase `@` est un alias parfait pour éviter d'alourdir le code. Les modificateurs comme `.prevent`, `.stop` ou même `.outside` (pour fermer un modal en cliquant à l'extérieur) rendent Alpine inestimable comparé à JS natif._

<br>

---

## 2. Le "Two-Way Binding" avec x-model

Ce mécanisme permet d'instaurer une relation miroir entre une variable logicielle et l'interface HTML : on modifie l'input HTML, la variable se met à jour ; on modifie logiciellement la variable, le texte HTML dans l'input se synchronise tout seul.

```html title="Relier les entrées utilisateurs"
<div x-data="{ search: '', darkTheme: false }">
    
    <!-- Tout ce que l'utilisateur tape ici finit dans la variable "search" -->
    <input type="text" x-model="search" placeholder="Rechercher une faille CVSS...">
    
    <p>Vous recherchez : <span x-text="search"></span></p>

    <!-- Le Two-Way Binding gère aussi les cases à cocher ! -->
    <label>
        <input type="checkbox" x-model="darkTheme">
        Mode Nuit activé ? (<span x-text="darkTheme"></span>)
    </label>

</div>
```

_Que ce soit des champs `input`, des menus déroulants `select`, ou de grosses zones de texte `textarea`, le Two-Way Binding remplace plus de 20 lignes de pure mécanique d'écouteurs en VanillaJS._

<br>

---

## 3. Dynamiser les Attributs : x-bind

Le HTML vit de ses attributs `class`, `disabled`, `href`, `src`. Alpine peut muter n'importe quel attribut conditionnellement. La syntaxe `x-bind` dispose aussi de son alias : les deux points `:`.

```html title="Le contrôle d'attributs avec x-bind / alias :"
<div x-data="{ imageId: 44, isValid: false }">
    <!-- Change dynamiquement de lien ou de source d'image -->
    <img :src="`https://picsum.photos/id/${imageId}/200/300`">

    <!-- Désactivation visuelle liée au scope -->
    <button :disabled="!isValid" :class="isValid ? 'bg-green' : 'bg-gray'">
        Valider Projet
    </button>
    <button @click="isValid = true">Déverrouiller le Cadenas</button>
</div>
```

_L'alias `:` permet littéralement de programmer son code HTML. Dès que le booléen `isValid` devient vrai, l'attribut `disabled` disparaît informatiquement et le système de classes CSS permute._

<br>

---

## Conclusion

!!! quote "Les Contrôleurs du Cockpit"
    Avec `@` pour recevoir des commandes et `:` pour actionner les moteurs, votre HTML est désormais une machine réactive complète et autonome pilotable par l'App. 

> Comment gère-t-on le cycle de temps : appeler des informations du réseau, rafraîchir d'anciennes variables sans se perdre, ou modifier le DOM natif ? Toutes les subtilités d'architecture dans le [Chapitre 4 : Mécanismes Avancés](./04-reactivite-avancee.md).
