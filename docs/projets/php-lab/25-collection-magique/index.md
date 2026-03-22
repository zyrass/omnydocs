---
description: "Projet Pratique POO : Maîtriser le summum du polymorphisme natif PHP en construisant un Objet se comportant exactement comme un Tableau (ArrayAccess, Countable, Iterator)."
icon: lucide/box
tags: ["PHP", "POO", "MAGIC", "ARRAY", "COLLECTION"]
status: stable
---

# Projet 25 : Array Object (Collection Magique)

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="8.3"
  data-time="2 Heures">
</div>

!!! quote "Le Pitch"
    En PHP, un `array` classique n'est pas un Objet. Il n'a pas de méthodes. Mais parfois, on aimerait pouvoir manipuler une liste d'utilisateurs avec des méthodes Objet ET avec des crochets `[]` de tableau !
    En implémentant les **Interfaces Natives Standard de PHP** (`ArrayAccess`, `Countable`) et les **Méthodes Magiques** (`__get`, `__set`), on peut forger une chimère parfaite : La `Collection`.

!!! abstract "Objectifs Pédagogiques"
    1.  **Le Masque ArrayAccess** : Permettre à notre instance d'objet de réagir quand on tape `$collection['clé']`.
    2.  **L'Illusion Countable** : Permettre à la fonction native `count($collection)` de fonctionner sur notre Objet.
    3.  **L'Esprit de Boucle** : Implémenter `IteratorAggregate` pour que la boucle `foreach ($collection as $item)` parcourt notre attribut protégé.

## 1. Implémenter le Trio d'Interfaces Natives PHP

Quand une classe "Implémente" des interfaces natives, le coeur du moteur PHP en est informé et traite l'objet d'une manière spéciale.

```php
<?php
declare(strict_types=1);

// Implémenter ces 3 interfaces obligent à écrire des méthodes au nom très spécifique !
class MagicCollection implements ArrayAccess, Countable, IteratorAggregate {
    
    // La liste cachée et protégée qui retiendra les vraies données.
    private array $items = [];
    
    // ==========================================
    // 1. ArrayAccess : L'illusion des Crochets []
    // ==========================================
    
    public function offsetExists(mixed $offset): bool {
        return isset($this->items[$offset]);
    }
    
    public function offsetGet(mixed $offset): mixed {
        return $this->items[$offset] ?? null;
    }
    
    public function offsetSet(mixed $offset, mixed $value): void {
        if ($offset === null) {
            $this->items[] = $value; // [] = $valeur (Ajout basique)
        } else {
            $this->items[$offset] = $value; // ['cle'] = $valeur
        }
    }
    
    public function offsetUnset(mixed $offset): void {
        unset($this->items[$offset]);
    }
    
    // ==========================================
    // 2. Countable : L'illusion Mathématique
    // ==========================================
    
    public function count(): int {
        return count($this->items);
    }
    
    // ==========================================
    // 3. IteratorAggregate : L'illusion de la Boucle
    // ==========================================
    
    // Traversable est une classe système spéciale pour les foreach
    public function getIterator(): Traversable {
        return new ArrayIterator($this->items);
    }
}
?>
```

## 2. Le Vernis des Méthodes Magiques (Double Accession)

Nous venons de faire en sorte que l'Objet réagisse aux crochets `$obj['clé']`. Maintenant, grâce aux méthodes magiques on va faire en sorte que les flèches d'attributs dynamiques fonctionnent : `$obj->clé`. 

```php
<?php
declare(strict_types=1);

class MagicCollection implements ArrayAccess, Countable, IteratorAggregate {

    private array $items = [];

    // ... (Gardez le code du dessus) ...
    
    // ==========================================
    // Les Méthodes Magiques pour la syntaxe Objet ->
    // ==========================================

    // Dès qu'on appelle un attribut qui n'existe pas : `$obj->titre`
    public function __get(string $name): mixed {
        return $this->items[$name] ?? null;
    }
    
    // Dès qu'on force l'assignation d'un attribut inexistant : `$obj->titre = 'OK'`
    public function __set(string $name, mixed $value): void {
        $this->items[$name] = $value;
    }
    
    public function __isset(string $name): bool {
        return isset($this->items[$name]);
    }
    
    public function __unset(string $name): void {
        unset($this->items[$name]);
    }
    
    // ==========================================
    // Magie Ultime : Gérer l'affichage Brut
    // ==========================================
    
    // Que se passe t-il si le visiteur tente de faire "echo $obj;" ??
    public function __toString(): string {
        return json_encode($this->items);
    }
}
?>
```

## 3. L'Essai en Action (Le Cerveau qui Fume)

Testons la puissance ahurissante de la Chimère Objet/Tableau.

```php
<?php
require_once 'MagicCollection.php';

$collection = new MagicCollection();

// 1. Test de l'ArrayAccess (Crochets)
$collection[0] = 'Alice';
$collection['boss'] = 'Bob';

// 2. Test des Méthodes Magiques (Flèches Objet)
$collection->stagiaire = 'Charlie';

// 3. Test du Countable
echo "Il y a " . count($collection) . " membres.\n"; 
// Affiche "3 membres." (La fonction PHP native fonctionne sur NOTRE objet !)

// 4. Test IterateAggregate
foreach ($collection as $cle => $personne) {
    echo "- [$cle] : $personne \n";
}
/* Sortie :
- [0] : Alice
- [boss] : Bob
- [stagiaire] : Charlie 
*/

// 5. Test String Magique
echo $collection;
// Affiche le JSON Brut : {"0":"Alice","boss":"Bob","stagiaire":"Charlie"}
?>
```

<div class="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-8">
  <h4 class="text-lg font-bold text-gray-900 mt-0 mb-4">✅ Objectifs de Validation</h4>
  <p class="mb-4 text-gray-700">Vous venez de réaliser l'un des patterns les plus cachés mais les plus utilisés par le célèbre Framework Laravel (La "Collection Laravel" est construite très exactement comme cela). En manipulant les interfaces systèmes, vous forcez PHP à altérer ce qu'il est en capacité de comprendre structurellement d'un Objet.</p>
</div>
