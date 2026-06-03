---
description: "Découvrir la légèreté de l'aspect Javascript et remplacer ses scripts par des attributs natifs HTML"
icon: lucide/book-open-check
tags: ["LARAVEL", "ALPINE", "FRONTEND", "INTERACTIVE"]
---

# L'Interactivité d'Alpine

<div
  class="omny-meta"
  data-level="🟢 Débutant/Intermédiaire"
  data-version="1.0"
  data-time="2 Heures">
</div>

## 1. A la rencontre d'AlpineJS

**Alpine.js** (Le A de "TALL") est le framework JavaScript de 15KB qui est inclus dans le kit d'architecture pro `Breeze` ! L'idée principale ? Oubliez la balise `<script> let maVar = 0; document.truc() </script>`. Vous manipulez le Javascript dans les tag de vos Divisions HTML sur vos Views Blade ! Et en direct !

**Avant AlpineJS sur mon Dropdown de Navigation :**
```html
<script>
    let menuOpen = false;
    document.getElementById('menu-button').addEventListener('click', () => {
        menuOpen = !menuOpen;
        document.getElementById('menu').classList.toggle('hidden');
    });
</script>

<button id="menu-button">Menu</button>
<div id="menu" class="hidden"><a>Lien Profil</a></div>
```

**La même chose en AlpineJS sur une Vue :**
```html
<!-- x-data : Stocke les var "Javascript" dans mon Div ! -->
<div x-data="{ open: false }">

    <!-- @click modifie ma valeur ! -->
    <button @click="open = !open">Menu</button>
    
    <!-- x-show analyse TRUE ou FALSE et manipule le CSS (Il cache par css l'enfant) ! -->
    <div x-show="open">
        <a>Lien Profil</a>
    </div>

</div>
```

<br>

---

## 2. Découverte des attributs "X-" Alpine.

Sa courbe d'apprentissage est redoutable car elle ne requiert pas de logique serveur ni Back. Ces attributs peuvent par exemple gérer un Tabulateur cliquable de pages de paramètres !

#### 1. X-IF : Manipulation Destructrice
Cousin de `X-Show`. A la simple différence que si un de vos tableaux cache milles objets lours qu'on ne veut pas charger à l'oeil nu par CSS, Alors `x-if` retire physiquement le Div enfant de la page (Economie de rame) plutot que le cacher !

#### 2. X-MODEL : Binding Data Input
Liaison Bi-Directionelle Formidable que seul des framework mastodondes possedent ! S'affiche sans serveur à la frappe. On l'utilise généralement pour chercher du texte.
```html
<div x-data="{ tapemoi: '' }">
    <input type="text" x-model="tapemoi">
    <p>Vous êtes en train de taper en temps réel le mot : <span x-text="tapemoi"></span></p>
</div>
```

#### 3. Clic OutSide
Celui ci permet au modale d'écran de se fermer ou au menus si l'utilisateur ne clique pas dans la zone en question ! Trèèès utile au design !
```html
<div x-data="{ panel: false }">
    <button @click="panel = !panel">Panel</button>
    <!-- Le @click.outside capte l'extérieur !! Magique ! -->
    <div x-show="panel" @click.outside="panel = false" ></div>
```

La suite n'est qu'affaire de documentation et est incroyablement agréable. Mais si nous puissions mélanger à la fois la puissance magique du Front et le coté Dynamique PHP Côté base de données ? 
Allons voir le `L` de la stack. Livewire !

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Alpine.js est la réponse de la Stack TALL à une question fondamentale : 'Ai-je vraiment besoin de React pour afficher ou masquer un menu déroulant ?' La réponse est non. Alpine résout 80% des besoins d'interactivité côté client en 15kb, sans build step, sans complexité de state management.

> [Interactivité côté client maîtrisée. Passez maintenant à la réactivité côté serveur avec Livewire →](./38-livewire-reactif.md)
