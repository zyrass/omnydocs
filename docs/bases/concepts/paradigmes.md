---
description: "Découverte des grands styles de programmation : Procédural, Orienté Objet et Fonctionnel."
icon: lucide/book-open-check
tags: ["PARADIGME", "POO", "FONCTIONNEL", "PROCEDURAL", "ARCHITECTURE"]
---

# Paradigmes de Programmation

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="1.0"
  data-time="20 - 30 minutes">
</div>


!!! quote "Analogie pédagogique"
    _Un paradigme de programmation est comme un style culinaire. Vous pouvez préparer des œufs à la poêle (procédural), utiliser une machine qui prépare le petit-déjeuner idéal (orienté objet) ou déclarer que vous voulez des œufs sans dire comment les faire (déclaratif)._

!!! quote "Des philosophies de conception"
    _Un paradigme de programmation n'est pas un langage en soi, mais un **style**, une façon de penser et de structurer son code pour résoudre un problème. Tout comme un architecte peut choisir de construire en béton brut ou en ossature bois, un développeur choisit un paradigme (ou les combine) selon la nature du projet. Les langages modernes (PHP, JavaScript, Python, Swift) sont pour la plupart "multi-paradigmes", permettant de piocher le meilleur de chaque monde._

## 1. La Programmation Impérative et Procédurale

C'est le paradigme historique, la façon la plus "naturelle" d'expliquer une tâche à un ordinateur.

**La Philosophie :** "Fais ceci, puis fais cela". Le code est une suite d'instructions linéaires qui modifient l'état global du programme.
La variante *Procédurale* introduit simplement les fonctions (procédures) pour regrouper le code redondant, mais la logique reste une longue recette de cuisine.

### L'approche en pratique
Vous définissez des variables, et des fonctions viennent lire ou modifier ces variables. Les données (le "Quoi") et les comportements (le "Comment") sont séparés.

```php
// État global (Données)
$balance = 1000;

// Procédure (Comportement)
function withdrawMoney(int $amount) {
    global $balance;
    if ($balance >= $amount) {
        $balance -= $amount;
        return true;
    }
    return false;
}

// Exécution linéaire
withdrawMoney(200);
```

### Le Cas d'usage
Parfait pour les petits scripts système (bash), les micro-contrôleurs (C), ou les algorithmes mathématiques purs. Cependant, sur des projets massifs (des milliers de lignes), l'approche procédurale devient vite un "code spaghetti" impossible à maintenir.

---

## 2. La Programmation Orientée Objet (POO)

Apparue pour résoudre les problèmes de complexité de la programmation procédurale, la POO est aujourd'hui le standard absolu du monde professionnel (Java, C#, PHP moderne).

**La Philosophie :** Modéliser le programme comme une collection d'**Objets** qui interagissent. 

Un objet est une capsule qui regroupe intimement :
- **Son état** (ses propriétés/attributs).
- **Ses comportements** (ses méthodes).

### Les 4 Piliers de la POO

1. **L'Encapsulation** : L'objet protège ses données internes (`private`) et expose une interface publique stricte pour interagir avec lui. Vous ne pouvez pas modifier directement son solde bancaire, vous devez utiliser la méthode `withdrawMoney()`.
2. **L'Héritage** : Une classe `Guerrier` peut hériter des propriétés de la classe mère `Personnage` et y ajouter ses propres spécificités.
3. **Le Polymorphisme** : Des objets différents peuvent partager la même méthode (ex: `calculerSalaire()`), mais chaque objet l'exécutera à sa manière (un Vendeur n'est pas calculé comme un Manager).
4. **L'Abstraction** : Se concentrer sur *ce que* fait l'objet (l'Interface) et cacher les détails complexes de *comment* il le fait.

```php
// La Classe (le Moule)
class BankAccount {
    // Encapsulation de l'état
    private int $balance;

    public function __construct(int $initialBalance) {
        $this->balance = $initialBalance;
    }

    // Le Comportement (Méthode)
    public function withdraw(int $amount): bool {
        if ($this->balance >= $amount) {
            $this->balance -= $amount;
            return true;
        }
        return false;
    }
}

// L'Objet (l'Instance)
$account = new BankAccount(1000);
$account->withdraw(200);
```

---

## 3. La Programmation Fonctionnelle (PF)

Longtemps réservée au monde académique (Lisp, Haskell), la programmation fonctionnelle a envahi le développement web ces dernières années (React, JavaScript moderne).

**La Philosophie :** La PF est basée sur l'évaluation de fonctions mathématiques. Le concept central est l'**Immutabilité** : les données ne changent jamais.

### Les principes fondamentaux

1. **Fonctions Pures** : Une fonction pure, si on lui donne les mêmes entrées, retournera toujours la même sortie, **sans effet de bord** (side-effect). Elle ne lit ni ne modifie aucune variable extérieure (ni base de données, ni fichier global).
2. **L'Immutabilité** : Au lieu de modifier un tableau en place pour y ajouter un élément, on crée un *nouveau* tableau qui contient l'ancien élément + le nouveau.
3. **Fonctions de Première Classe (First-Class)** : Les fonctions sont traitées comme des variables. On peut passer une fonction en paramètre d'une autre fonction (ex: les Callbacks, `map`, `filter`, `reduce`).

```javascript
// Les données d'origine (Ne seront jamais modifiées)
const transactions = [100, -50, 200, -10];

// Fonction Pure : Retourne un NOUVEAU tableau sans toucher l'original
const extractDeposits = (arr) => arr.filter(amount => amount > 0);

// Fonction Pure de calcul
const sum = (arr) => arr.reduce((total, amount) => total + amount, 0);

// Exécution par composition
const totalDeposits = sum(extractDeposits(transactions)); // Retourne 300
```

### Le Cas d'usage
L'approche fonctionnelle excelle dans la **concurrence** (multi-threading). Puisque les données sont immuables, il n'y a aucun risque que deux fils d'exécution modifient la même variable en même temps. Elle est aussi très appréciée pour la gestion d'interface utilisateur réactive (State management).

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La maîtrise du concept de paradigmes est un pilier de l'informatique fondamentale. Au-delà de la syntaxe technique, c'est cette compréhension théorique qui différencie un simple technicien d'un véritable ingénieur capable de concevoir des systèmes robustes et maintenables.

Aujourd'hui, vous n'avez plus à choisir un camp. Dans une application Laravel ou Swift moderne :
- Vous utilisez l'**Orienté Objet** pour structurer l'architecture globale (Modèles, Contrôleurs, Services).
- Vous utilisez des principes **Fonctionnels** à l'intérieur de vos méthodes (collections, map, filter) pour traiter la donnée proprement et sans effet de bord.
