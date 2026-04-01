---
description: "Generics Swift : fonctions et types génériques, type constraints, associated types et where clauses."
icon: lucide/book-open-check
tags: ["SWIFT", "GENERICS", "TYPE-CONSTRAINTS", "ASSOCIATED-TYPES", "PARAMÉTRIQUE"]
---

# Generics

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Moule Universel"
    Imaginez un moule à gâteau qui fonctionne avec n'importe quelle pâte : chocolat, vanille, citron. Vous écrivez les instructions du moule une seule fois, et il s'adapte automatiquement à l'ingrédient fourni sans rien changer. C'est exactement ce que font les Generics : écrire du code qui fonctionne avec n'importe quel type, tout en restant complètement typé et sûr à la compilation.

    Sans Generics, vous écririez `trierTableauDeInt()`, `trierTableauDeString()`, `trierTableauDeProduit()`... Avec Generics, vous écrivez `trier<T>()` une seule fois — et Swift instancie automatiquement la version correcte selon le contexte. C'est exactement comme cela que `Array`, `Dictionary`, `Optional` et toute la bibliothèque standard Swift sont construits.

<br>

---

## Le Problème Sans Generics

```swift title="Swift - Le problème : duplication sans generics"
// Sans generics : une fonction par type
func inversерTableauDeInt(_ tableau: [Int]) -> [Int] {
    tableau.reversed()
}

func inverserTableauDeString(_ tableau: [String]) -> [String] {
    tableau.reversed()
}

func inverserTableauDeDouble(_ tableau: [Double]) -> [Double] {
    tableau.reversed()
}

// Le code est identique dans les trois cas — seul le type change
// Avec 50 types différents, on aurait 50 fonctions identiques
```

<br>

---

## Fonctions Génériques

=== ":simple-swift: Swift"

    ```swift title="Swift - Fonction générique avec paramètre de type T"
    // <T> déclare un paramètre de type : T est un placeholder pour n'importe quel type
    // T est une convention (Type), mais n'importe quel nom fonctionne
    func inverser<T>(_ tableau: [T]) -> [T] {
        tableau.reversed()
    }

    // Swift infère le type depuis les arguments
    let ints = inverser([1, 2, 3, 4, 5])       // [Int]
    let textes = inverser(["a", "b", "c"])       // [String]
    let décimaux = inverser([1.1, 2.2, 3.3])    // [Double]

    // Plusieurs paramètres de type
    func créerPaire<T, U>(_ premier: T, _ second: U) -> (T, U) {
        (premier, second)
    }

    let paire = créerPaire("Alice", 28)   // (String, Int)
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Fonctions génériques (TypeScript)"
    // JavaScript pur n'a pas de generics
    // TypeScript apporte les generics avec une syntaxe similaire à Swift

    // TypeScript :
    // function inverser<T>(tableau: T[]): T[] {
    //     return [...tableau].reverse();
    // }
    // const ints = inverser([1, 2, 3]);      // number[]
    // const textes = inverser(["a", "b"]);   // string[]

    // JavaScript pur : any (pas de sécurité de type)
    function inverser(tableau) {
        return [...tableau].reverse();
    }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Generics simulés avec templates PHPDoc"
    <?php
    // PHP n'a pas de generics natifs (en cours de réflexion pour PHP 9+)
    // PHPDoc permet de documenter les intentions sans les enforcer

    /**
     * @template T
     * @param array<T> $tableau
     * @return array<T>
     */
    function inverser(array $tableau): array {
        return array_reverse($tableau);
    }

    // phpstan et psalm vérifient les templates PHPDoc statiquement
    ```

=== ":simple-python: Python"

    ```python title="Python - Generics avec TypeVar"
    from typing import TypeVar, list as List

    T = TypeVar('T')

    def inverser(tableau: list[T]) -> list[T]:
        return list(reversed(tableau))

    # Python 3.12+ : nouvelle syntaxe plus proche de Swift
    # def inverser[T](tableau: list[T]) -> list[T]:
    #     return list(reversed(tableau))

    # Les generics Python sont pour la documentation/analyse statique (mypy)
    # Python lui-même ne les enforces pas à l'exécution
    ```

<br>

---

## Type Constraints — Restreindre les Types Acceptés

Sans contrainte, `T` accepte n'importe quel type. Les contraintes limitent `T` aux types conformes à un certain protocol.

```swift title="Swift - Type constraints avec where et : Protocol"
// Contrainte basique : T doit être Comparable (peut être comparé avec < et >)
func maximum<T: Comparable>(_ a: T, _ b: T) -> T {
    a > b ? a : b
}

print(maximum(3, 7))         // 7 — Int est Comparable
print(maximum("Alice", "Bob")) // "Bob" — String est Comparable
print(maximum(3.14, 2.71))   // 3.14 — Double est Comparable

// Contrainte multiple
func afficherEtTrier<T: Comparable & CustomStringConvertible>(_ éléments: [T]) -> [T] {
    let triés = éléments.sorted()
    triés.forEach { print($0.description) }
    return triés
}

// Clause where : pour des contraintes plus complexes
// Trier uniquement si les deux tableaux ont des éléments du même type Comparable
func fusionnerTrié<T: Comparable>(_ a: [T], _ b: [T]) -> [T] {
    (a + b).sorted()
}

print(fusionnerTrié([3, 1, 4], [1, 5, 9]))  // [1, 1, 3, 4, 5, 9]

// Extension générique contrainte : disponible seulement pour les tableaux d'éléments Comparable
extension Array where Element: Comparable {
    var minimum: Element? { self.min() }
    var maximum: Element? { self.max() }
    var plage: ClosedRange<Element>? {
        guard let min = minimum, let max = maximum else { return nil }
        return min...max
    }
}

let notes = [14, 18, 7, 15, 11]
print(notes.minimum ?? 0)   // 7
print(notes.maximum ?? 0)   // 18
print(notes.plage!)          // 7...18
```

<br>

---

## Types Génériques

Les types (structs, classes, enums) peuvent aussi être génériques.

```swift title="Swift - Struct générique : une pile (Stack)"
// Une pile générique — fonctionne avec n'importe quel type
struct Pile<Élément> {
    private var éléments: [Élément] = []

    var estVide: Bool { éléments.isEmpty }
    var sommet: Élément? { éléments.last }

    mutating func empiler(_ élément: Élément) {
        éléments.append(élément)
    }

    @discardableResult
    mutating func dépiler() -> Élément? {
        éléments.popLast()
    }
}

// Utilisation avec différents types
var pileDeInt = Pile<Int>()
pileDeInt.empiler(1)
pileDeInt.empiler(2)
pileDeInt.empiler(3)
print(pileDeInt.dépiler() ?? 0)  // 3
print(pileDeInt.sommet ?? 0)     // 2

var pileDeTexte = Pile<String>()
pileDeTexte.empiler("Swift")
pileDeTexte.empiler("iOS")
print(pileDeTexte.sommet ?? "")  // "iOS"
```

```swift title="Swift - Enum générique : Result<T, E>"
// Le type Result de la bibliothèque standard Swift est un enum générique
// Voici une version simplifiée pour comprendre sa structure
enum Résultat<Succès, Échec: Error> {
    case succès(Succès)
    case échec(Échec)
}

enum ErreurAPI: Error {
    case nonTrouvé
    case serveurIndisponible
    case nonAutorisé
}

func chargerUtilisateur(id: Int) -> Résultat<String, ErreurAPI> {
    guard id > 0 else {
        return .échec(.nonTrouvé)
    }
    return .succès("Alice")   // Simulation
}

let résultat = chargerUtilisateur(id: 42)
switch résultat {
case .succès(let nom):
    print("Utilisateur : \(nom)")
case .échec(let erreur):
    print("Erreur : \(erreur)")
}
```

<br>

---

## Associated Types dans les Protocols

Les associated types permettent aux protocols d'être génériques — c'est la fondation de nombreux protocols de la bibliothèque standard Swift.

```swift title="Swift - Associated types dans un protocol"
// Un protocol avec associated type
protocol Conteneur {
    // associatedtype déclare un type placeholder dans le protocol
    associatedtype Élément

    var compte: Int { get }
    mutating func ajouter(_ élément: Élément)
    func élément(à index: Int) -> Élément
}

// Struct conforme : Élément est inféré comme Int
struct FileDAttente<T>: Conteneur {
    typealias Élément = T   // Liaison explicite (souvent inférée automatiquement)
    private var éléments: [T] = []

    var compte: Int { éléments.count }

    mutating func ajouter(_ élément: T) {
        éléments.append(élément)
    }

    func élément(à index: Int) -> T {
        éléments[index]
    }

    mutating func retirer() -> T? {
        éléments.isEmpty ? nil : éléments.removeFirst()
    }
}

var file = FileDAttente<String>()
file.ajouter("Première tâche")
file.ajouter("Deuxième tâche")
print(file.retirer() ?? "")  // "Première tâche" — FIFO
```

<br>

---

## Clause `some` et Opaque Types

```swift title="Swift - some : retourner un type opaque"
protocol Forme {
    var aire: Double { get }
}

struct Cercle: Forme {
    var rayon: Double
    var aire: Double { Double.pi * rayon * rayon }
}

struct Carré: Forme {
    var côté: Double
    var aire: Double { côté * côté }
}

// some Forme : le compilateur connaît le type exact, l'appelant ne le voit pas
// Avantage vs any Forme : pas de coût d'allocation dynamique
func créerForme(estCercle: Bool) -> some Forme {
    // ATTENTION : avec some, TOUTES les branches doivent retourner le même type
    Cercle(rayon: 5.0)
}

// any Forme : peut retourner des types différents selon les branches
func créerFormeVariable(estCercle: Bool) -> any Forme {
    estCercle ? Cercle(rayon: 5.0) : Carré(côté: 4.0)
}

// En SwiftUI :
// var body: some View { ... }
// some View garantit un seul type de vue (perf optimale) sans l'exposer
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les **Generics** permettent d'écrire du code qui fonctionne avec n'importe quel type tout en restant statiquement typé. Le paramètre de type `<T>` est un placeholder résolu par le compilateur à chaque utilisation. Les **type constraints** (`T: Comparable`) limitent les types acceptés aux conformants d'un protocol. Les **associated types** dans les protocols permettent aux protocols d'être eux-mêmes génériques. `some Protocol` retourne un type opaque — le compilateur connaît le type exact, l'appelant non — c'est la base de `some View` en SwiftUI.

> Dans le module suivant, nous couvrirons la **Gestion des Erreurs** — `throws`, `do/catch`, `try` et le type `Result<T, E>` qui s'appuie directement sur les Generics que vous venez de maîtriser.

<br>