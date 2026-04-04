---
description: "Validation des Entrées, Messages d'Erreur natifs et Form objects avec Livewire."
icon: lucide/box
tags: ["THEORIE", "LIVEWIRE", "VALIDATION", "FORMULAIRES"]
---

# 03. Formulaires et Validation

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Livewire 3.x"
  data-time="2 Heures">
</div>

!!! quote "Garde Frontière"
    Ne faites jamais, **absolument jamais**, confiance aux données entrées par vos utilisateurs depuis un navigateur web. Un nom de 2 millions de caractères peut écraser un serveur. Un String reçu à la place d'un Tableau Integer déclenche un Crash DB Fatal. Contrairement aux API REST classiques où les codes d'erreur doivent être refaçonnés pour des Frontends React, Livewire utilise les entrailles de Laravel : les règles et la langue de validation sont fusionnées entre le front et le backend en natif !

<br>

---

## 1. Le Nouvel Attribut `#[Validate]` PHP 8

Dans les précédentes versions 1 et 2 de Livewire, l'usager écrivait une longue méthode `$rules = []`. Livewire 3 exploite les syntaxes novatrices via Attributs pour valider le composant "à la source", au plus près de la déclaration.

```php title="Déclaration des filtres d'intégrité de la Classe"
<?php

namespace App\Livewire;

use Livewire\Component;
use Livewire\Attributes\Validate;

class SignUser extends Component
{
    // Ce champ exige d'être pré-rempli, et au minimum 4 lettres
    #[Validate('required|min:4')]
    public $title = '';

    // Ce champ garantit l'unicité dans la Base de Données (Anti DB-Hack)
    // Et lève un message spécial traduit !
    #[Validate('required|email|unique:users,email', message: 'Cet email est déjà pris')]
    public $email = '';

    public function create()
    {
        // 1. Livewire STOPE la fonction nette ici si email ou title sont mauvais
        // 2. Et il RAPPELLE la méthode render() avec la table d'erreurs !
        $this->validate(); 

        User::create([
            'title' => $this->title,
            'email' => $this->email
        ]);
        
        // Vidange du formulaire
        $this->reset('title', 'email'); 
    }
}
```

_Note : Si `$this->validate()` échoue (throw d'une exception `ValidationException`), la fonction `create()` ne lit **jamais** les lignes suivantes et empêche ainsi Eloquent de polluer la Base SQL. C'est le principe du Guard Clause naturel._

<br>

---

## 2. Renvoyer L'Erreur Côté Blade HTML

Lorsque le `validate()` coupe le circuit, il renvoie un "Errors Bag" (Sac d'Erreurs) à la page. La directive `@error` traditionnelle de Blade s'en empare et affiche les données sans même nécessiter de programmation JavaScript supplémentaire.

```html title="Capture des erreurs au Focus du Champ"
<form wire:submit="create" class="p-4">
    <!-- Évite le saut de route HTTP en interceptant avec 'wire:submit' -->
    
    <div>
        <label>Titre de Compte</label>
        <input type="text" wire:model.blur="title">
        
        <!-- Le helper Laravel pour cibler la faille du string "title" -->
        @error('title') 
            <span class="text-sm text-red-600 font-bold">
                {{ $message }}
            </span> 
        @enderror
    </div>

    <button type="submit">Valider</button>
</form>
```

_Le modificateur `.blur` a été couplé avec le modèle. Cela signifie que l'utilisateur tapera son titre en paix, cliquera sur un autre champ, et SEULEMENT à ce moment-là la requête partira à Laravel pour activer le validateur `[#Validate]`, soulevant l'alerte `@error` sans même recharger le bouton "Validation". C'est de l'expérience utilisateur Parfaite._

<br>

---

## 3. Formulaire Massif : Livewire Form Objects

S'il y a 20 propriétés liées au profil utilisateur (`$nom`, `$prenom`, `$cp`, `$ville`, etc.), la classe Livewire principale va hériter d'une trentaine de variables publiques, devenant illisible. On délègue tout via les *Form Objects*.

```php title="app/Livewire/Forms/PostForm.php (Création d'un Sous-Fichier dédié)"
<?php

namespace App\Livewire\Forms;

use Livewire\Attributes\Validate;
use Livewire\Form;

// Notre objet dérive de Livewire\Form au lieu de Component
class PostForm extends Form 
{
    #[Validate('required|min:5')]
    public $title = '';

    #[Validate('required')]
    public $content = '';
    
    public function store() {
        $this->validate();
        Post::create($this->all());
    }
}
```

```php title="Injection de ce Form Object dans le Composant Livewire normal !"
class CreatePost extends Component
{
    // C'est magique : Toutes les vars et la validation sont condensées dans un namespace 'form' !!
    public PostForm $form; 

    public function save()
    {
        $this->form->store();
    }
}
```

Dans le Blade, on appellera alors `wire:model="form.title"` au lieu de `wire:model="title"`. 

<br>

---

## Conclusion

!!! quote "Les Entrées Cloisonnées"
    Vous avez maintenant transformé votre base de données ouverte à tous les vents en un coffre numérique géré avec précision militaire sans avoir installé une seule librairie Axios, Fetch API ou Joi Validator. L'univers PHP dicte la loi, L'univers Javascript la dessine.

> Néanmoins, ce composant "Formulaire", qui vit dans son coin du Code... Comment peut-il informer le voisin, le "Composant Liste d'articles", qu'il doit télécharger les nouveaux éléments sans recharger la page ? Retrouvez ces réponses dans la communication inter-composant dans le [Chapitre 4: Evénements et Communications.](./04-evenements-communication.md).
