---
description: "Data Binding (wire:model), Actions (wire:click) et modificateurs réseaux."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "BINDING", "ACTIONS"]
---

# 02. Propriétés et Actions

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>

!!! quote "Les Neuro-Transmetteurs"
    Comment faire comprendre au serveur situé en Irlande qu'un utilisateur à Paris vient de cliquer sur "Inverser la liste" ou "Changer la valeur du champ Titre" ? La solution Livewire consiste à ajouter aux attributs `<input>` et `<button>` un préfixe intelligent nommé `wire:`. Ces mots-clés sont surveillés par le noyau JS de Livewire côté navigateur, qui convertit l'action en Payload, l'envoie au PHP, et redessine l'écran avec la réponse.

<br>

---

## 1. La liaison de variables : wire:model

C'est la fonctionnalité phare du Data-Binding. Relier un tag Form (Input, Select, TxtArea, Radio) à une variable du PHP.

```html title="Liaisons bidirectionnelles (Front/Back) instantanées"
<!-- Si l'utilisateur tape 'abc', $title côté serveur vaudra 'abc' !! -->
<input type="text" wire:model="title">

<!-- Modificateur .live : La requête part à CHAQUE lettre (Dangereux pour le SQL ! mais idéal pour un password strength checker) -->
<input type="text" wire:model.live="searchQuery">

<!-- Modificateur .blur : N'envoie la valeur que lorsque l'utilisateur a fini d'écrire et clique à côté -->
<input type="text" wire:model.blur="email">
```

_Livewire v3 opère par défaut un Defer Loading. Historiquement (la v2), tout `<input wire:model>` envoyait une rafraîchissement global à chaque touche. Désormais, c'est désactivé (Deferred) et requiert le modificateur `.live` explicitement pour des calculs denses._

<br>

---

## 2. Déclencher le Contrôleur : wire:click

Pour les interactions sans écriture, l'API d'écoute événementielle remplace parfaitement les `addEventListener` natifs.

```html title="Les actions utilisateur (Clics, Submit, KeyPress)"
<!-- Appel simple d'une fonction PHP clearCache() -->
<button wire:click="clearCache">Vider Cache</button>

<!-- Passage d'un Paramètre au backend PHP depuis le HTML ! -->
<button wire:click="deleteArticle({{ $article->id }})">Effacer Article</button>

<!-- Demander systématiquement "Êtes-vous sûr(e)" devant le navigateur pour éviter l'erreur (via le modificateur wire:confirm) -->
<button wire:click="delete" wire:confirm="Action Destructrice, certain ?">
    Nucléaire
</button>
```

_Le passage de paramètres est extrêmement robuste. Le code Javascript va le transformer en chaîne encodée et le transmettra en appel RPC à votre `$id` dans la méthode `deleteArticle($id)` du PHP._

<br>

---

## 3. Optimisation UX avec le Chargement (wire:loading)

Une simple addition de nombres prend une milliseconde à un serveur PHP local. Mais qu'en est-il d'un appel vers l'API Cloud de Stripe nécessitant 4,5 secondes ? L'utilisateur risque de cliquer 8 fois sur "Acheter" pensant que cela dysfonctionne. 

```html title="Gérer l'interface utilisateur pendant l'attente du Serveur"
<div>
    <button wire:click="launchBackup" class="btn">
        <!-- Text normal, disparait à l'action -->
        <span wire:loading.remove>Lancer la Sauvegarde Lente !</span>
        
        <!-- N'apparait que lorsque la requête fetch() interne est en cours -->
        <span wire:loading>... Backup en cours (ne pas fermer) ...</span>
    </button>

    <!-- Appliquer un filtre CSS (Opacité 50%) sur tout un conteneur ! -->
    <div wire:loading.class="opacity-50 blur-sm" class="table-data">
        Contenu qui devient flou si Livewire "rafraîchit" cette donnée...
    </div>
</div>
```

_Ajouter du visuel d'attente (Spinners) sans faire une once de JavaScript transforme une expérience rigide de l'ère Web des années 2010 en une authentique SPAs Moderne._

<br>

---

## Conclusion

!!! quote "Séparation des rôles de l'état"
    Nous manipulons désormais l'état de PHP (`wire:model`) et déclenchons la commande PHP (`wire:click`) tout en rassurant l'UX (`wire:loading`). Nous avons répliqué VueJS.
    
> Reste un problème dramatique : les utilisateurs n'écriront jamais un "Email" correct, ni un âge valide. Livewire, situé sous l'égide de Laravel, ne se trompe jamais sur cette tâche : Passons au fonctionnement crucial du [Chapitre 3 : Formulaires et Validation](./03-formulaires-validation.md).
