---
description: "Protocols et Extensions Swift : Protocol-Oriented Programming, Equatable, Comparable, Hashable, Identifiable, conformances et exercices."
icon: lucide/book-open-check
tags: ["SWIFT", "PROTOCOL", "EXTENSION", "POP", "EQUATABLE", "HASHABLE", "IDENTIFIABLE"]
---

# Protocols et Extensions

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="1.2"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Cahier des Charges et les Avenants"
    Un **protocol**, c'est un cahier des charges contractuel. Il dit : *"Tout type qui veut se présenter comme Payable doit obligatoirement implémenter une méthode `payer(montant:)`."* Le protocol ne dit pas **comment** — seulement **quoi**. Chaque type qui signe ce contrat l'implémente à sa manière.

    Une **extension**, c'est un avenant. Elle ajoute des fonctionnalités à un type **existant** — même un type que vous n'avez pas créé, comme `String` ou `Array`.

<br>

---

## Déclaration et Conformance

=== ":simple-swift: Swift"

    ```swift title="Swift - Protocol et conformance"
    protocol Décrivable {
        var description: String { get }
        func afficher()
    }

    struct Produit: Décrivable {
        let nom: String
        let prix: Double

        var description: String { "\(nom) — \(prix) €" }
        func afficher() { print("Produit : \(description)") }
    }

    class Commande: Décrivable {
        let numéro: Int
        var items: [Produit]

        init(numéro: Int) { self.numéro = numéro; self.items = [] }

        var description: String { "Commande #\(numéro) — \(items.count) article(s)" }
        func afficher() { print(description); items.forEach { $0.afficher() } }
    }

    let p = Produit(nom: "Clavier", prix: 89.0)
    p.afficher()   // "Produit : Clavier — 89.0 €"
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Interface simulée (TypeScript)"
    // TypeScript :
    // interface Décrivable {
    //     readonly description: string;
    //     afficher(): void;
    // }
    // class Produit implements Décrivable { ... }

    // JS pur : duck typing
    const produit = {
        get description() { return `${this.nom} — ${this.prix} €`; },
        afficher() { console.log(`Produit : ${this.description}`); },
        nom: "Clavier", prix: 89.0
    };
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Interface"
    <?php
    interface Décrivable {
        public function getDescription(): string;
        public function afficher(): void;
    }

    class Produit implements Décrivable {
        public function __construct(
            private string $nom,
            private float $prix
        ) {}

        public function getDescription(): string { return "{$this->nom} — {$this->prix} €"; }
        public function afficher(): void { echo $this->getDescription() . PHP_EOL; }
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Protocol (Python 3.8+)"
    from typing import Protocol

    class Décrivable(Protocol):
        @property
        def description(self) -> str: ...
        def afficher(self) -> None: ...

    class Produit:
        def __init__(self, nom: str, prix: float):
            self.nom, self.prix = nom, prix

        @property
        def description(self) -> str: return f"{self.nom} — {self.prix} €"
        def afficher(self) -> None: print(f"Produit : {self.description}")
    ```

<br>

---

## Protocols Standards Essentiels

Swift fournit des protocols standards que vous implémenterez constamment.

<br>

### `Equatable` — Comparer avec `==`

```swift title="Swift - Equatable : synthèse automatique et personnalisation"
// Swift synthétise Equatable automatiquement si toutes les propriétés sont Equatable
struct Point: Equatable {
    var x: Double
    var y: Double
    // == est généré automatiquement
}

let p1 = Point(x: 1.0, y: 2.0)
let p2 = Point(x: 1.0, y: 2.0)
print(p1 == p2)   // true

// Implémentation manuelle quand la logique est personnalisée
struct Utilisateur: Equatable {
    var id: Int
    var nom: String
    var dateConnexion: Date

    // Égalité basée uniquement sur l'id
    static func == (lhs: Utilisateur, rhs: Utilisateur) -> Bool {
        lhs.id == rhs.id
    }
}

// Equatable débloque : contains, firstIndex, ==, !=
let utilisateurs = [
    Utilisateur(id: 1, nom: "Alice", dateConnexion: .now),
    Utilisateur(id: 2, nom: "Bob",   dateConnexion: .now)
]
let cible = Utilisateur(id: 2, nom: "Bob", dateConnexion: .distantPast)
print(utilisateurs.contains(cible))   // true — car id == 2
```

<br>

### `Comparable` — Trier avec `<`

```swift title="Swift - Comparable : activer le tri"
struct Produit: Equatable, Comparable {
    let nom: String
    let prix: Double

    // Seule méthode requise — >, <=, >= sont déduits automatiquement
    static func < (lhs: Produit, rhs: Produit) -> Bool {
        lhs.prix < rhs.prix
    }
}

let produits = [
    Produit(nom: "Moniteur", prix: 299.0),
    Produit(nom: "Clavier",  prix: 89.0),
    Produit(nom: "Souris",   prix: 45.0)
]

let triésParPrix = produits.sorted()
// Souris (45€), Clavier (89€), Moniteur (299€)

print(produits.min()?.nom ?? "")   // "Souris"
print(produits.max()?.nom ?? "")   // "Moniteur"
```

<br>

### `Hashable` — Utiliser dans `Set` et comme clé de `Dictionary`

```swift title="Swift - Hashable : unicité et indexation"
// Hashable est requis pour Set<T> et Dictionary<T, V> quand T est la clé
// Swift synthétise Hashable si Equatable est conforme et toutes les propriétés sont Hashable

struct Tag: Hashable {
    let nom: String
    let catégorie: String
}

var tags: Set<Tag> = []
tags.insert(Tag(nom: "iOS",   catégorie: "plateforme"))
tags.insert(Tag(nom: "Swift", catégorie: "langage"))
tags.insert(Tag(nom: "iOS",   catégorie: "plateforme"))   // Doublon ignoré
print(tags.count)   // 2

var compteurParTag: [Tag: Int] = [:]
let tagSwift = Tag(nom: "Swift", catégorie: "langage")
compteurParTag[tagSwift] = 42
```

<br>

### `Identifiable` — L'identité unique pour SwiftUI

`Identifiable` est un protocol simple mais **indispensable** en SwiftUI. Il exige qu'un type possède une propriété `id` unique, ce qui permet à SwiftUI de suivre chaque élément dans une liste et de mettre à jour uniquement ce qui a changé.

```swift title="Swift - Identifiable : requis par ForEach en SwiftUI"
// Le protocol Identifiable de la bibliothèque standard :
// public protocol Identifiable {
//     associatedtype ID: Hashable
//     var id: ID { get }
// }

struct Article: Identifiable {
    let id: UUID          // UUID est Hashable — parfait comme identifiant
    let titre: String
    let contenu: String
}

struct Tâche: Identifiable {
    let id: Int           // Int fonctionne aussi — n'importe quel Hashable
    var titre: String
    var estTerminée: Bool
}

// En SwiftUI, ForEach exige Identifiable :
// List {
//     ForEach(articles) { article in    ← fonctionne car Article: Identifiable
//         Text(article.titre)
//     }
// }
//
// Sans Identifiable, il faut préciser le keypath manuellement :
// ForEach(articles, id: \.id) { article in ... }

// UUID() génère un identifiant unique garanti
let a1 = Article(id: UUID(), titre: "Introduction Swift", contenu: "...")
let a2 = Article(id: UUID(), titre: "Optionals en pratique", contenu: "...")
```

*`UUID` (Universally Unique Identifier) est le type de référence pour les identifiants en Swift. `UUID()` génère une valeur de 128 bits garantie unique à chaque appel. C'est le choix standard pour les `id` dans les modèles de données SwiftUI.*

!!! tip "Codable + Identifiable : le modèle complet"
    En pratique, les structs de données SwiftUI combinent souvent les trois :

    ```swift title="Swift - Pattern complet d'un modèle SwiftUI"
    struct Article: Codable, Identifiable, Hashable {
        let id: UUID
        let titre: String
        let datePublication: Date
        var nombreVues: Int

        // Codable     : désérialisation depuis une API JSON
        // Identifiable : utilisation dans ForEach et List
        // Hashable     : utilisation dans NavigationSplitView, Set, etc.
    }
    ```

!!! note "Chaîne Equatable → Hashable → Identifiable"
    `Identifiable` ne requiert pas `Equatable` ni `Hashable` — mais le type de `id` doit être `Hashable`. En pratique, si votre modèle est `Identifiable`, il sera aussi `Hashable` dans la quasi-totalité des cas, car `UUID` et `Int` sont déjà `Hashable`.

<br>

---

## Extensions

```swift title="Swift - Étendre des types existants"
extension String {
    var estUnEmail: Bool {
        contains("@") && contains(".") && count > 5
    }

    func tronquer(à longueur: Int, suffixe: String = "...") -> String {
        guard count > longueur else { return self }
        return String(prefix(longueur)) + suffixe
    }
}

print("alice@example.com".estUnEmail)           // true
print("Bonjour tout le monde".tronquer(à: 10))  // "Bonjour to..."

// Extension contrainte
extension Array where Element: Numeric {
    var somme: Element { reduce(0, +) }
}

print([14, 18, 12, 15, 17].somme)   // 76

// Organiser les conformances en extensions séparées
struct Article: Identifiable {
    let id: UUID
    let titre: String
    let datePublication: Date
    var nombreVues: Int
}

extension Article: Equatable {
    static func == (lhs: Article, rhs: Article) -> Bool { lhs.id == rhs.id }
}

extension Article: Comparable {
    static func < (lhs: Article, rhs: Article) -> Bool {
        lhs.datePublication < rhs.datePublication
    }
}

extension Article: CustomStringConvertible {
    var description: String { "[\(nombreVues) vues] \(titre)" }
}
```

<br>

---

## Default Implementations

```swift title="Swift - Comportement gratuit via extensions de protocol"
protocol Journalisable {
    var nomType: String { get }
    func journaliser(_ message: String)
    func avertir(_ message: String)
    func erreur(_ message: String)
}

extension Journalisable {
    var nomType: String { String(describing: type(of: self)) }

    func avertir(_ message: String) {
        journaliser("[AVERTISSEMENT] [\(nomType)] \(message)")
    }

    func erreur(_ message: String) {
        journaliser("[ERREUR] [\(nomType)] \(message)")
    }
}

struct ServicePaiement: Journalisable {
    func journaliser(_ message: String) { print("[LOG] \(message)") }

    func traiterPaiement(montant: Double) {
        journaliser("Paiement de \(montant) € initié")
        avertir("Délai de traitement élevé")   // Hérité du protocol
    }
}
```

<br>

---

## Protocols comme Types

```swift title="Swift - any et some"
// any Décrivable : boîte polymorphe
var éléments: [any Décrivable] = []
éléments.append(Produit(nom: "Souris", prix: 45.0))
éléments.append(Commande(numéro: 1001))

for élément in éléments { élément.afficher() }

// some Décrivable : type opaque — compilateur connaît le type, l'appelant non
// C'est exactement : var body: some View { ... } en SwiftUI
func créerDécrivable() -> some Décrivable {
    Produit(nom: "Clavier", prix: 89.0)
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Conformance Equatable personnalisée**

```swift title="Swift - Exercice 1"
// Créez struct Livre avec : isbn (String), titre (String), auteur (String), prix (Double)
// Deux livres sont égaux si leur ISBN est identique (ignorer le prix)

// let l1 = Livre(isbn: "978-0-000", titre: "Swift", auteur: "Apple", prix: 29.0)
// let l2 = Livre(isbn: "978-0-000", titre: "Swift", auteur: "Apple", prix: 35.0)
// print(l1 == l2)   // true
```

**Exercice 2 — Modèle SwiftUI complet**

```swift title="Swift - Exercice 2"
// Créez une struct Tâche conforme à Codable, Identifiable et Comparable
// - id : UUID
// - titre : String
// - priorité : Int (1 à 5)
// - estTerminée : Bool
// - dateÉchéance : Date
//
// Comparable : trier par priorité décroissante
// Testez :
// var tâches = [Tâche(...), Tâche(...), Tâche(...)]
// let triées = tâches.sorted()   // Priorité 5 en premier
```

**Exercice 3 — Protocol avec default implementation**

```swift title="Swift - Exercice 3"
// Créez protocol Validable avec :
//   - var estValide: Bool { get }
//   - var messageErreur: String { get }
//   - func valider() throws  ← default implementation qui utilise estValide
//
// Conformez EmailForm et AgeForm en utilisant la default implementation
// sans réécrire valider() dans chaque struct
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un **protocol** définit un contrat sans implémentation. `Equatable` active `==`, `Comparable` active le tri, `Hashable` active `Set` et les clés de `Dictionary`. `Identifiable` fournit un `id` unique — **requis par `ForEach` et `List` en SwiftUI**, il s'implémente en une ligne avec un `UUID`. Le pattern complet d'un modèle SwiftUI combine `Codable + Identifiable + Hashable`. Les **extensions** enrichissent n'importe quel type existant. Les **default implementations** offrent un comportement gratuit aux types conformes.

> Dans le module suivant, nous couvrirons **Codable** — la sérialisation et désérialisation JSON automatique en Swift.

<br>