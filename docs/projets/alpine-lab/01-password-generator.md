---
description: "Projet 1 : Créer un générateur de mots de passe interactif avec Alpine.js"
icon: lucide/key
tags: ["PROJET", "ALPINE", "PASSWORD", "STATE", "BINDING"]
---

# Password Generator

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Alpine 3.x"
  data-time="1 Heure">
</div>


!!! quote "Analogie pédagogique"
    _Travailler sur un projet complet est comparable à l'assemblage final d'une voiture sur une ligne de production. C'est ici que toutes les pièces individuelles (concepts appris précédemment) doivent s'emboîter parfaitement pour créer un produit fonctionnel et sécurisé._

!!! quote "La Magie de l'État Local"
    Dans ce tout premier projet Alpine Lab, nous allons concevoir un **Générateur de Mots de Passe**. Pourquoi ce choix ? Car c'est l'exercice parfait pour manipuler des états réactifs (`x-data`), lier la longueur du mot de passe à un curseur (`x-model`), intercepter des clics de copie (`@click`) et rafraîchir dynamiquement l'interface en temps réel. Avec Alpine, pas besoin d'écrire de gros sélecteurs `document.getElementById()`, tout se gère directement dans le HTML !

<br>

![Alpine Password Generator Mockup](file:///C:/Users/alain/.gemini/antigravity/brain/9e92fb0e-7515-41e9-81d3-d924f9af076c/alpine_password_generator_1775229125424.png)
<p><em>Maquette UI conceptuelle du projet : Panneau de contrôle avec curseur et état réactif générant le mot de passe.</em></p>

<br>

---

## 1. Cahier des Charges et Objectifs

### Enjeux du rendu

- **Afficher un mot de passe généré** visuellement grand et lisible au centre.
- **Un champ de type "range" (curseur)** pour choisir la longueur du mot de passe (ex: de 8 à 32 caractères).
- **Des cases à cocher (checkbox)** pour inclure ou exclure : Majuscules, Nombres, Symboles.
- **Un bouton "Copier"** qui sauvegarde le mot de passe dans le presse-papier et affiche brièvement "Copié !".

### Concepts Alpine.js abordés

- `x-data` : Pour déclarer les variables réactives (longueur, options, mot de passe actuel).
- `x-model` : Pour lier les inputs HTML ("Two-way data binding").
- `x-text` : Pour afficher la valeur Javascript dans le HTML.
- `@click` : Pour écouter les interactions simples.

<br>

---

## 2. L'Architecture du Composant

Notre application tiendra dans une seule balise `<div>` globale qui agira comme son propre composant.

```mermaid
flowchart TB
    UI[Interface HTML] <-->|x-model| State[(État Alpine)]
    
    subgraph "x-data : variables"
    State --> Length[length: 16]
    State --> Opt[hasSymbols, hasNumbers...]
    State --> PW[password: '...']
    end
    
    Btn(Bouton Générer) -->|@click| Func[Fonction generate()]
    Func -->|Génère une chaine| PW
    PW -->|x-text Re-render| UI
    
    style State fill:#43a047,color:#fff,stroke:#333
```

<br>

---

## 3. Implémentation du Code

### Étape 3.1 : Déclaration de l'État (x-data)

La force d'Alpine est de pouvoir écrire la logique directement dans la déclaration du scope.

```html title="Initialisation et Modèle Réactif"
<!-- Le x-init permet d'exécuter la fonction de génération dès l'ouverture de la page -->
<div x-data="{ 
        length: 16, 
        hasUpper: true, 
        hasNumbers: true, 
        hasSymbols: true,
        password: '',
        copied: false,
        
        generate() {
            let charset = 'abcdefghijklmnopqrstuvwxyz';
            if (this.hasUpper) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            if (this.hasNumbers) charset += '0123456789';
            if (this.hasSymbols) charset += '!@#$%^&*()_+~`|}{[]:;?><,./-=';
            
            let res = '';
            for (let i = 0, n = charset.length; i < this.length; ++i) {
                res += charset.charAt(Math.floor(Math.random() * n));
            }
            this.password = res;
            this.copied = false;
        },

        copyToClipboard() {
            navigator.clipboard.writeText(this.password);
            this.copied = true;
            setTimeout(() => this.copied = false, 2000);
        }
    }" 
    x-init="generate()"
    class="max-w-md mx-auto mt-10 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-lg shadow-green-500/10">
    
    <!-- Le contenu de l'interface viendra ici -->
    
</div>
```

*Avec cette seule balise d'ouverture, nous avons instancié notre logique métier. Les fonctions `generate()` et `copyToClipboard()` peuvent maintenant utiliser les variables internes via `this.` !*

<br>

### Étape 3.2 : Construire l'Interface et les Bindings

Nous branchons directement nos éléments de formulaire (Inputs) aux variables Alpine grâce au mot-clé magique `x-model`.

```html title="L'interface de l'Application"
    <!-- Affichage du Mot de Passe -->
    <div class="relative bg-gray-100 dark:bg-gray-700 p-4 rounded-lg flex justify-between items-center mb-6">
        <span class="text-xl font-mono text-gray-800 dark:text-gray-100" x-text="password"></span>
        
        <button @click="copyToClipboard()" class="text-green-500 hover:text-green-600 transition">
            <span x-show="!copied">Copier</span>
            <span x-show="copied" x-transition>✔️ Copié !</span>
        </button>
    </div>

    <!-- Réglage de la longueur -->
    <div class="mb-4">
        <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400 mb-2">
            <label>Longueur</label>
            <span x-text="length" class="font-bold text-green-500"></span>
        </div>
        <!-- @input assure la mise à jour réactive au moindre glissement -->
        <input type="range" min="8" max="32" x-model="length" @input="generate()"
               class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
    </div>

    <!-- Options avec Cases à Cocher -->
    <div class="space-y-3 mb-6 border-t border-gray-200 dark:border-gray-700 pt-4 text-gray-700 dark:text-gray-300">
        <label class="flex items-center space-x-3 cursor-pointer">
            <input type="checkbox" x-model="hasUpper" @change="generate()" class="text-green-500 rounded">
            <span>Inclure des Majuscules</span>
        </label>
        
        <label class="flex items-center space-x-3 cursor-pointer">
            <input type="checkbox" x-model="hasNumbers" @change="generate()" class="text-green-500 rounded">
            <span>Inclure des Chiffres</span>
        </label>
        
        <label class="flex items-center space-x-3 cursor-pointer">
            <input type="checkbox" x-model="hasSymbols" @change="generate()" class="text-green-500 rounded">
            <span>Inclure des Symboles</span>
        </label>
    </div>

    <!-- Bouton d'action principal -->
    <button @click="generate()" 
            class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 rounded-lg transition-colors shadow-lg">
        Générer un autre
    </button>
```

<br>

---

## Conclusion

!!! quote "Le Two-Way Binding simplifié"
    Avez-vous remarqué comment le changement visuel du curseur HTML met immédiatement à jour la variable `length`, qui appelle elle-même `generate()`, qui modifie enfin la vue du mot de passe généré ? C'est le principe du **Binding Réactif**. Avec moins de 50 lignes de code, vous venez de recréer un outil incontournable de cybersécurité !
    
> Ce projet rudimentaire vous donne des bases d'état, nous pouvons passer à une notion fondamentale supérieure : demander des données à internet et utiliser des boucles ! Rendez-vous au projet 2 (Convertisseur de devises).

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La validation de cette étape confirme votre capacité à intégrer des concepts avancés dans un flux de travail professionnel. L'architecture globale prend maintenant tout son sens.

> [Retour à l'index du projet →](../index.md)
