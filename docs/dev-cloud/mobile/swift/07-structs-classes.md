---
description: "Structs et Classes Swift : value types vs reference types, propriétés, méthodes, initialiseurs et choix architectural."
icon: lucide/book-open-check
tags: ["SWIFT", "STRUCT", "CLASS", "VALUE-TYPE", "REFERENCE-TYPE", "ARC"]
---

# Structs et Classes

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - La Photocopie et le Panneau"
    Une `struct`, c'est comme une fiche papier. Quand vous la donnez à quelqu'un, vous lui donnez une **photocopie** — il peut écrire dessus sans affecter votre original. Une `class`, c'est comme un panneau indicateur en ville. Quand vous donnez l'adresse du panneau à quelqu'un, vous lui donnez un moyen d'accéder au **même objet physique** — si l'un de vous le modifie, l'autre verra la modification.

    Cette distinction — **value type vs reference type** — est la décision architecturale la plus importante en Swift. SwiftUI est entièrement construit sur des structs, ce qui explique son comportement prévisible.

<br>

---

## Struct — Value Type

=== ":simple-swift: Swift"

    ```swift title="Swift - Déclaration et utilisation d'une struct"
    struct Point {
        // Propriétés stockées
        var x: Double
        var y: Double

        // Propriété calculée (pas de stockage, calculée à la demande)
        var description: String {
            "(\(x), \(y))"
        }

        var distanceOrigine: Double {
            (x * x + y * y).squareRoot()
        }

        // Méthode — doit être marquée mutating pour modifier les propriétés
        mutating func déplacer(dx: Double, dy: Double) {
            x += dx
            y += dy
        }

        // Méthode non mutante (lecture seule)
        func distance(vers autre: Point) -> Double {
            let dx = x - autre.x
            let dy = y - autre.y
            return (dx * dx + dy * dy).squareRoot()
        }
    }

    // Initialiseur synthétique : Swift le génère automatiquement
    var p1 = Point(x: 3.0, y: 4.0)
    print(p1.description)          // "(3.0, 4.0)"
    print(p1.distanceOrigine)      // 5.0

    p1.déplacer(dx: 1.0, dy: 0.0)
    print(p1)   // Point(x: 4.0, y: 4.0)
    ```

    ```swift title="Swift - La copie en action (value semantics)"
    var a = Point(x: 1.0, y: 2.0)
    var b = a   // COPIE — b est indépendant de a

    b.x = 99.0

    print(a.x)  // 1.0 — a n'est pas affecté
    print(b.x)  // 99.0

    // Avec let : aucune modification possible (toutes les propriétés sont immuables)
    let c = Point(x: 5.0, y: 5.0)
    // c.x = 10.0   // ERREUR : cannot assign to property: 'c' is a 'let' constant
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Object (référence par défaut)"
    // JavaScript n'a pas de struct — les objets sont des références
    // Pour simuler une struct : objet littéral ou classe

    // Les objets JS sont toujours des références
    const a = { x: 1.0, y: 2.0 };
    const b = a;   // Référence, pas une copie

    b.x = 99.0;
    console.log(a.x);  // 99.0 — a EST modifié (même référence)

    // Pour copier : spread operator
    const c = { ...a };
    c.x = 0;
    console.log(a.x);  // 99.0 — a non modifié cette fois

    // TypeScript : interface pour typer un objet struct-like
    // interface Point { x: number; y: number; }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Classe (référence) ou tableau associatif (valeur)"
    <?php
    // PHP n'a pas de struct native — on utilise des classes ou des tableaux

    // Tableau associatif (value semantics comme struct Swift)
    $a = ["x" => 1.0, "y" => 2.0];
    $b = $a;   // Copie en PHP pour les tableaux
    $b["x"] = 99.0;
    echo $a["x"];  // 1.0 — non modifié

    // PHP 8.2+ : readonly class (immuable, proche de struct Swift immuable)
    readonly class Point {
        public function __construct(
            public float $x,
            public float $y
        ) {}
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - dataclass (proche de struct Swift)"
    from dataclasses import dataclass
    import math

    @dataclass
    class Point:
        x: float
        y: float

        @property
        def distance_origine(self) -> float:
            return math.sqrt(self.x ** 2 + self.y ** 2)

        def distance(self, autre: "Point") -> float:
            return math.sqrt((self.x - autre.x)**2 + (self.y - autre.y)**2)

    # Python : les dataclass sont des références, pas des valeurs
    a = Point(1.0, 2.0)
    b = a           # Référence
    b.x = 99.0
    print(a.x)      # 99.0 — a modifié

    # Pour une copie : copy.copy()
    import copy
    c = copy.copy(a)
    ```

<br>

---

## Class — Reference Type

```swift title="Swift - Déclaration et comportement référence d'une class"
class CompteBancaire {
    // Propriétés stockées
    var solde: Double
    let titulaire: String   // Même avec let dans la class, var vs let s'applique

    // Initialiseur personnalisé (pas de synthèse automatique pour les classes)
    init(titulaire: String, soldeInitial: Double = 0.0) {
        self.titulaire = titulaire
        self.solde = soldeInitial
    }

    // Pas besoin de mutating pour les classes
    func déposer(_ montant: Double) {
        solde += montant
    }

    func retirer(_ montant: Double) -> Bool {
        guard solde >= montant else { return false }
        solde -= montant
        return true
    }

    // Destructeur : appelé quand l'objet est libéré de la mémoire (ARC)
    deinit {
        print("CompteBancaire de \(titulaire) libéré")
    }
}

// Les classes sont des références
let compteDAlice = CompteBancaire(titulaire: "Alice", soldeInitial: 1000.0)
let référenceAuMêmeCompte = compteDAlice   // Même objet en mémoire

référenceAuMêmeCompte.déposer(500.0)

print(compteDAlice.solde)              // 1500.0 — modifié via l'autre référence
print(référenceAuMêmeCompte.solde)    // 1500.0 — même objet

// === : vérifier si deux variables pointent vers le MÊME objet
print(compteDAlice === référenceAuMêmeCompte)   // true — même identité

let autreCompte = CompteBancaire(titulaire: "Alice", soldeInitial: 1000.0)
print(compteDAlice === autreCompte)  // false — objets distincts même si égaux
```

<br>

---

## Les Initialiseurs

```swift title="Swift - Initialiseurs personnalisés et convenience"
struct Rectangle {
    var largeur: Double
    var hauteur: Double

    // Initialiseur désigné (principal)
    init(largeur: Double, hauteur: Double) {
        self.largeur = largeur
        self.hauteur = hauteur
    }

    // Initialiseur de convenance (appelle le principal)
    init(côté: Double) {
        self.init(largeur: côté, hauteur: côté)   // Carré
    }

    var aire: Double { largeur * hauteur }
    var périmètre: Double { 2 * (largeur + hauteur) }
}

let rect = Rectangle(largeur: 10.0, hauteur: 5.0)
let carré = Rectangle(côté: 8.0)

print(rect.aire)     // 50.0
print(carré.aire)    // 64.0

// Initialiseur faillible : retourne un Optional si les paramètres sont invalides
struct Temperature {
    let kelvin: Double

    init?(celsius: Double) {
        guard celsius >= -273.15 else { return nil }  // 0 Kelvin absolu
        kelvin = celsius + 273.15
    }
}

let t1 = Temperature(celsius: 20.0)    // Optional(Temperature)
let t2 = Temperature(celsius: -300.0)  // nil — température impossible

if let t = t1 {
    print("\(t.kelvin) K")   // 293.15 K
}
```

<br>

---

## Propriétés Avancées

```swift title="Swift - Propriétés observées et lazy"
class Formulaire {
    // willSet / didSet : observer les modifications
    var nom: String = "" {
        willSet {
            print("nom va changer de '\(nom)' à '\(newValue)'")
        }
        didSet {
            print("nom a changé de '\(oldValue)' à '\(nom)'")
        }
    }

    // lazy : initialisée seulement à la première utilisation
    lazy var analyseComplexe: [String] = {
        print("Calcul coûteux exécuté une seule fois")
        return ["résultat1", "résultat2"]
    }()

    // Propriété statique : partagée entre toutes les instances
    static var nombreInstances = 0

    init() {
        Formulaire.nombreInstances += 1
    }
}

var f = Formulaire()
f.nom = "Alice"
// "nom va changer de '' à 'Alice'"
// "nom a changé de '' à 'Alice'"

print(f.analyseComplexe)   // Déclenche le calcul
print(f.analyseComplexe)   // Utilise le cache — calcul pas répété
```

<br>

---

## Struct vs Class : Quand Choisir

La règle d'Apple est explicite : **préférez les structs par défaut**. Utilisez une classe uniquement quand l'identité partagée est nécessaire.

| Critère | Struct | Class |
| --- | --- | --- |
| Sémantique | Value type (copie) | Reference type (référence) |
| Héritage | Non | Oui |
| `deinit` | Non | Oui |
| Thread safety | Plus sûr (copies indépendantes) | Risques de concurrence |
| Usage SwiftUI | Presque toujours | ViewModels (`@ObservableObject`) |
| Exemples Apple | `CGPoint`, `Array`, `String` | `UIViewController`, `URLSession` |

!!! tip "La règle d'Apple"
    Depuis Swift 5 et SwiftUI, Apple recommande : *"Use structures by default."* Les structs sont prévisibles (copie = isolation), plus performantes en mémoire dans la plupart des cas, et naturellement thread-safe. Utilisez une classe uniquement si vous avez besoin d'héritage, de `deinit`, ou d'une identité partagée entre plusieurs parties du code.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les **structs** sont des value types : chaque assignation crée une copie indépendante. Les **classes** sont des reference types : les variables partagent le même objet en mémoire. Les structs nécessitent `mutating` pour les méthodes qui modifient leurs propriétés. Les classes ont `deinit` et supportent l'héritage. Préférez toujours les structs — utilisez les classes quand l'identité partagée est explicitement nécessaire.

> Dans le module suivant, nous couvrirons les **Enumerations** Swift — une version radicalement plus puissante que les enums classiques, avec les associated values qui peuvent transporter des données.

<br>