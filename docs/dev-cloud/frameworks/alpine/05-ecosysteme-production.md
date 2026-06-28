---
description: "Architecture à grande échelle avec Alpine.data, état global via Alpine.store(), persistance de données et transition vers Flux UI sous Laravel 13."
icon: lucide/book-open-check
tags: ["THEORIE", "ALPINEJS", "ARCHITECTURE", "PRODUCTION", "FLUXUI"]
---

# Écosystème & Production

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire à 🔴 Avancé"
  data-version="3.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Bureau d'Études et la Chaîne de Montage"
    Lorsque vous bricolez un petit prototype en bois chez vous, vous pouvez garder tous vos outils en vrac sur la table (écrire du JavaScript brut directement au sein des balises HTML). Mais dès que vous lancez une production industrielle à grande échelle (un site web de production avec des dizaines d'écrans), vous devez structurer l'espace : dessiner des plans précis dans un bureau d'études (déporter la logique dans des fonctions JavaScript via `Alpine.data`), stocker les composants communs dans un entrepôt centralisé (les Stores globaux), et installer des robots d'assemblage standardisés (les composants Flux UI) pour monter le produit sans effort.

Ce module présente les patrons d'architecture pour concevoir des applications maintenables avec Alpine.js et détaille la transition vers l'écosystème **Flux UI** et **Laravel 13**.

<br>

---

## 1. Structurer la Logique Applicative avec `Alpine.data()`

Lorsque le code de votre composant s'étoffe, le conserver directement dans l'attribut HTML `x-data` nuit gravement à la lisibilité et à la maintenance du projet. La méthode `Alpine.data()` permet d'extraire et de structurer cette logique dans un script JavaScript séparé.

### Découplage de la logique métier

```html title="Blade - resources/views/livewire/⚡dashboard-card.blade.php : découplage x-data"
<!-- Le HTML reste minimaliste et déclaratif -->
<div x-data="dashboardController">
    <span x-text="userName"></span>
    <button @click="disconnect" class="bg-red-500 text-white px-3 py-1 rounded">
        Déconnexion
    </button>
</div>

<script>
// La logique est déportée au sein de l'initialisation d'Alpine
document.addEventListener('alpine:init', () => {
    Alpine.data('dashboardController', () => ({
        userName: 'Administrateur Principal',
        tokenActive: true,
        
        disconnect() {
            this.tokenActive = false;
            alert("Session clôturée.");
        }
    }))
})
</script>
```
_Découplage de la logique réactive au sein du contrôleur dashboardController enregistré sur l'événement d'initialisation d'Alpine._

<br>

---

## 2. Centralisation de l'État Global avec `Alpine.store()`

Les Stores permettent de partager des informations ou des états communs à travers des composants indépendants et éloignés dans l'arborescence HTML (comme le statut d'authentification ou le choix d'un thème visuel).

### Exemple d'utilisation d'un Store global

```html title="Blade - resources/views/layouts/⚡navigation.blade.php : store global"
<script>
document.addEventListener('alpine:init', () => {
    // Déclaration d'un Store global nommé 'settings'
    Alpine.store('settings', {
        darkMode: false,
        
        toggleTheme() {
            this.darkMode = !this.darkMode;
        }
    })
})
</script>

<!-- Utilisation du Store global dans n'importe quel élément HTML -->
<div x-data :class="$store.settings.darkMode ? 'bg-slate-900 text-white' : 'bg-white text-slate-900'" class="p-6">
    <button @click="$store.settings.toggleTheme()" class="border p-2 rounded">
        Changer le thème
    </button>
</div>
```
_Partage d'état universel via la propriété magique $store pour synchroniser les composants à chaud._

<br>

---

## 3. Persistance de Données avec `$persist`

Pour éviter de perdre l'état réactif lorsque l'utilisateur recharge sa page ou ferme son navigateur, le plugin `@alpinejs/persist` permet de stocker automatiquement les variables dans le stockage local (Local Storage) du navigateur.

```html title="Blade - layouts/app.blade.php : inclusion du plugin de persistance"
<!-- Le script du plugin doit impérativement être chargé AVANT le cœur d'Alpine -->
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```
_Ordre de chargement des scripts CDN assurant l'initialisation du plugin avant le cœur du framework._

```javascript title="JavaScript - Sauvegarde automatique de l'état"
Alpine.data('editorDraft', () => ({
    // La variable est lue et écrite automatiquement dans le Local Storage sous la clé 'saved_draft'
    content: Alpine.$persist('Rédigez ici...').as('saved_draft'),
}))
```
_Persistance transparente d'une variable de texte à l'aide de l'utilitaire magique $persist._

<br>

---

## 4. Intégration Laravel 13 & Bundling Vite

Dans un projet professionnel Laravel 13, les scripts ne sont plus chargés via des liens CDN externes, mais compilés localement à l'aide du bundler Vite.

### Fichier `resources/js/app.js`

```js title="JavaScript - resources/js/app.js : initialisation d'Alpine.js"
import Alpine from 'alpinejs';
import persist from '@alpinejs/persist';

// Enregistrement manuel des plugins importés
Alpine.plugin(persist);

// Liaison de l'objet Alpine à la fenêtre pour le débogage dans la console
window.Alpine = Alpine;

// Démarrage officiel d'Alpine
Alpine.start();
```
_Importation, configuration du plugin de persistance et initialisation globale d'Alpine au sein du bundle JavaScript._

Le fichier compilé est ensuite injecté dans votre template Blade via la directive de ressources `@vite('resources/js/app.js')`.

<br>

---

## 5. Transition vers Flux UI

**Flux UI** est la bibliothèque officielle de composants Livewire pour Laravel 13. Elle est construite sur la base de Livewire v4, Tailwind CSS v4 et s'appuie nativement sur **Alpine.js** pour la gestion de l'interactivité locale côté client.

### Pourquoi basculer vers Flux UI ?

*   **Composants accessibles prédéfinis :** Flux fournit des éléments d'interface réutilisables prêts à l'emploi (boutons, modales, menus déroulants, selects) qui intègrent toutes les normes d'accessibilité (WAI-ARIA) et la navigation au clavier.
*   **Abstraction d'Alpine.js :** Au lieu d'écrire manuellement des structures complexes pour gérer l'ouverture, la fermeture ou le focus des modales, Flux encapsule toute la logique Alpine sous-jacente au sein de balises simples.

### Exemple de modale interactive avec Flux UI

```html title="Blade - resources/views/welcome.blade.php : modale avec Flux UI"
<!-- Bouton d'ouverture abstrait par Flux -->
<flux:modal.trigger name="confirm-action">
    <flux:button>Déclencher l'action</flux:button>
</flux:modal.trigger>

<!-- Modale gérant l'accessibilité et la fermeture automatique sous Alpine.js -->
<flux:modal name="confirm-action" class="space-y-4">
    <flux:heading size="lg">Confirmer l'opération</flux:heading>
    
    <flux:subheading>
        Cette action est irréversible. Souhaitez-vous continuer ?
    </flux:subheading>
    
    <div class="flex justify-end gap-2">
        <flux:modal.close>
            <flux:button variant="ghost">Annuler</flux:button>
        </flux:modal.close>
        <flux:button variant="danger">Confirmer</flux:button>
    </div>
</flux:modal>
```
_Déclaration d'une modale réactive et accessible à l'aide de composants Flux UI exploitant Alpine.js en arrière-plan._

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Centraliser l'état d'un panier d'achat**

1. Créez un Store global Alpine nommé `cart` avec un tableau `items` vide et une méthode `addItem($product)`.
2. Créez deux composants distincts sur votre page : un bouton pour ajouter un article, et un compteur dans l'en-tête qui affiche la taille du tableau `items`.
3. Vérifiez la synchronisation instantanée sans lien de parenté direct.

**Exercice 2 — Sécuriser un Store avec Persist**

1. Combinez l'usage de `Alpine.store` et de `Alpine.$persist`.
2. Faites en sorte que l'état du Store `settings` (thème clair ou sombre) soit automatiquement sauvegardé dans le Local Storage et restauré lors du rafraîchissement de la page.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La directive `Alpine.data()` permet d'isoler le code JavaScript complexe en dehors du HTML. Les Stores (`Alpine.store()`) centralisent l'état partagé entre des composants indépendants, tandis que le plugin Persist écrit les données sur le disque local de l'utilisateur. Enfin, **Flux UI** représente le futur de la stack TALL en encapsulant la logique d'interactivité locale d'Alpine au sein de composants Blade réutilisables, optimisés et accessibles.

> **Parcours Alpine.js complété.** Vous maîtrisez désormais l'intégralité des outils front-end de la stack TALL. Poursuivez vers la section **[Cyber - Gouvernance](../../cyber/governance/index.md)** pour explorer les enjeux de conformité et de sécurité de vos applications.
