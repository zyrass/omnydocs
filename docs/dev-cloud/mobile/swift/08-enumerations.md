---
description: "Enumerations Swift : enums simples, raw values, associated values et pattern matching avancé."
icon: lucide/book-open-check
tags: ["SWIFT", "ENUM", "ASSOCIATED-VALUES", "PATTERN-MATCHING", "RAW-VALUES"]
---

# Enumerations

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Feu Tricolore Enrichi"
    Un feu tricolore classique a trois états fixes : rouge, orange, vert. C'est un enum simple. Mais imaginez un feu enrichi : quand il est rouge, il transporte une information supplémentaire — le nombre de secondes restantes. Quand il est vert, il précise si la voie est libre ou encombrée. Ce feu ne se contente plus de nommer un état — il transporte des données spécifiques à cet état.

    C'est exactement la puissance des **associated values** en Swift. Les enums deviennent des conteneurs de données structurées, pas de simples listes de constantes.

Les enums Swift sont des types à part entière — ils peuvent avoir des méthodes, des propriétés calculées, se conformer à des protocols, et transporter des données via leurs associated values. C'est l'une des fonctionnalités les plus avancées par rapport aux enums PHP ou JavaScript.

<br>

---

## Enum Simple

=== ":simple-swift: Swift"

    ```swift title="Swift - Enum de base"
    enum Direction {
        case nord
        case sud
        case est
        case ouest

        // On peut grouper sur une ligne
        // case nord, sud, est, ouest
    }

    var cap = Direction.nord
    cap = .sud   // Inférence du type : .sud = Direction.sud

    // switch avec enum : Swift exige d'être EXHAUSTIF
    switch cap {
    case .nord:
        print("Heading North")
    case .sud:
        print("Heading South")
    case .est:
        print("Heading East")
    case .ouest:
        print("Heading West")
    // Pas de default nécessaire : tous les cas sont couverts
    // Si on ajoute un case à l'enum, le compilateur signale les switch incomplets
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Enum simulé avec Object.freeze"
    // JavaScript n'a pas d'enum natif
    const Direction = Object.freeze({
        NORD: "nord",
        SUD: "sud",
        EST: "est",
        OUEST: "ouest"
    });

    let cap = Direction.NORD;

    switch (cap) {
        case Direction.NORD: console.log("Heading North"); break;
        case Direction.SUD:  console.log("Heading South"); break;
        // Pas d'exhaustivité garantie par le compilateur
        default: console.log("Unknown");
    }

    // TypeScript apporte des enums natifs
    // enum Direction { Nord = "nord", Sud = "sud" }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Enum (PHP 8.1+)"
    <?php
    // PHP 8.1 : enums natifs (proches des enums Swift simples)
    enum Direction {
        case Nord;
        case Sud;
        case Est;
        case Ouest;
    }

    $cap = Direction::Nord;

    // match() pour les enums PHP
    $message = match($cap) {
        Direction::Nord  => "Heading North",
        Direction::Sud   => "Heading South",
        Direction::Est   => "Heading East",
        Direction::Ouest => "Heading West",
    };
    echo $message;
    ```

=== ":simple-python: Python"

    ```python title="Python - Enum avec le module enum"
    from enum import Enum

    class Direction(Enum):
        NORD  = "nord"
        SUD   = "sud"
        EST   = "est"
        OUEST = "ouest"

    cap = Direction.NORD

    match cap:
        case Direction.NORD:  print("Heading North")
        case Direction.SUD:   print("Heading South")
        case Direction.EST:   print("Heading East")
        case Direction.OUEST: print("Heading West")
    ```

<br>

---

## Raw Values

Les raw values associent une valeur primitive (`String`, `Int`, `Double`) à chaque case d'un enum.

```swift title="Swift - Enum avec raw values"
// Raw values String : chaque case a une valeur String associée
enum HTTPMethod: String {
    case get    = "GET"
    case post   = "POST"
    case put    = "PUT"
    case delete = "DELETE"
    case patch  = "PATCH"
}

let méthode = HTTPMethod.post
print(méthode.rawValue)   // "POST"

// Initialisation depuis une raw value — retourne un Optional
let méthodeDepuisTexte = HTTPMethod(rawValue: "GET")   // Optional(.get)
let inconnue = HTTPMethod(rawValue: "OPTIONS")          // nil

// Raw values Int avec auto-incrémentation
enum Priorité: Int {
    case basse   = 1   // 1
    case normale       // 2 (auto-incrémenté)
    case haute         // 3
    case critique      // 4
}

let p = Priorité.haute
print(p.rawValue)   // 3

// Utilisation : trier par priorité
let tâches: [(String, Priorité)] = [
    ("Email", .normale),
    ("Bug critique", .critique),
    ("Documentation", .basse)
]

let triées = tâches.sorted { $0.1.rawValue > $1.1.rawValue }
// Bug critique, Email, Documentation
```

<br>

---

## Associated Values — La Vraie Puissance

Les associated values permettent à chaque case de transporter des données de types différents. C'est ce qui rend les enums Swift fondamentalement différents des enums des autres langages.

=== ":simple-swift: Swift"

    ```swift title="Swift - Associated values pour modéliser des états riches"
    // Modéliser le résultat d'une requête réseau
    enum RésultatRequête {
        case succès(données: Data, statusCode: Int)
        case échecServeur(code: Int, message: String)
        case échecRéseau(erreur: Error)
        case annulée
    }

    // Chaque case transporte des données différentes et typées
    func traiterRésultat(_ résultat: RésultatRequête) {
        switch résultat {
        case .succès(let données, let code):
            print("OK (\(code)) : \(données.count) bytes reçus")

        case .échecServeur(let code, let message):
            print("Erreur serveur \(code) : \(message)")

        case .échecRéseau(let erreur):
            print("Erreur réseau : \(erreur.localizedDescription)")

        case .annulée:
            print("Requête annulée")
        }
    }

    // Exemple d'usage
    let résultat = RésultatRequête.échecServeur(code: 404, message: "Not Found")
    traiterRésultat(résultat)
    // "Erreur serveur 404 : Not Found"
    ```

    ```swift title="Swift - Associated values pour une forme géométrique"
    enum Forme {
        case cercle(rayon: Double)
        case rectangle(largeur: Double, hauteur: Double)
        case triangle(base: Double, hauteur: Double)
        case point   // Pas de données associées

        // Les enums peuvent avoir des propriétés calculées et des méthodes
        var aire: Double {
            switch self {
            case .cercle(let r):
                return Double.pi * r * r
            case .rectangle(let l, let h):
                return l * h
            case .triangle(let b, let h):
                return 0.5 * b * h
            case .point:
                return 0
            }
        }
    }

    let c = Forme.cercle(rayon: 5.0)
    let r = Forme.rectangle(largeur: 4.0, hauteur: 6.0)

    print(c.aire)   // 78.53...
    print(r.aire)   // 24.0
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Associated values simulés (union discriminante)"
    // JavaScript n'a pas d'associated values
    // Pattern courant : union discriminante avec un champ type

    // Simuler RésultatRequête
    const résultat = {
        type: "échecServeur",
        code: 404,
        message: "Not Found"
    };

    switch (résultat.type) {
        case "succès":
            console.log(`OK (${résultat.statusCode})`);
            break;
        case "échecServeur":
            console.log(`Erreur ${résultat.code} : ${résultat.message}`);
            break;
    }

    // TypeScript : discriminated unions (plus proche des associated values Swift)
    // type Résultat =
    //   | { type: "succès"; données: Uint8Array; statusCode: number }
    //   | { type: "échecServeur"; code: number; message: string }
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Enums avec méthodes (PHP 8.1)"
    <?php
    // PHP 8.1 : backed enums (raw values) mais pas d'associated values natives
    // Pour associated values : on utilise des classes

    enum Statut: string {
        case Actif   = "actif";
        case Inactif = "inactif";
        case Banni   = "banni";

        public function label(): string {
            return match($this) {
                Statut::Actif   => "Compte actif",
                Statut::Inactif => "Compte inactif",
                Statut::Banni   => "Compte banni",
            };
        }
    }

    echo Statut::Actif->label();  // "Compte actif"
    echo Statut::Actif->value;    // "actif"
    ```

=== ":simple-python: Python"

    ```python title="Python - Enum avec données (simulation via dataclass)"
    from enum import Enum
    from dataclasses import dataclass

    # Python n'a pas d'associated values natifs
    # Simulation avec des classes dédiées par état

    @dataclass
    class Succès:
        données: bytes
        status_code: int

    @dataclass
    class ÉchecServeur:
        code: int
        message: str

    # Union de types avec type hints
    RésultatRequête = Succès | ÉchecServeur | None

    def traiter(résultat: RésultatRequête):
        match résultat:
            case Succès(données, code):
                print(f"OK ({code})")
            case ÉchecServeur(code, message):
                print(f"Erreur {code} : {message}")
            case None:
                print("Annulée")
    ```

<br>

---

## Le Type `Optional` est un Enum

Maintenant que vous connaissez les associated values, voici un secret : `Optional<T>` en Swift n'est rien d'autre qu'un enum avec deux cases.

```swift title="Swift - Optional<T> dévoilé"
// La définition réelle de Optional dans la bibliothèque standard Swift
// (simplifiée pour la lisibilité)
enum Optional<Wrapped> {
    case some(Wrapped)   // Contient une valeur de type Wrapped
    case none            // Pas de valeur (= nil)
}

// Ces deux formes sont identiques :
var a: String? = "Alice"
var b: Optional<String> = .some("Alice")

// nil est du sucre syntaxique pour .none
var c: String? = nil
var d: Optional<String> = .none

// if let déstructure le case .some
if case .some(let valeur) = a {
    print(valeur)   // "Alice"
}

// Forme équivalente et habituelle
if let valeur = a {
    print(valeur)   // "Alice"
}
```

*Comprendre qu'Optional est un enum avec associated values révèle pourquoi `compactMap` fonctionne, pourquoi `map` sur un Optional existe, et pourquoi le pattern matching avec `if let` a ce comportement.*

<br>

---

## Enums Récursifs avec `indirect`

```swift title="Swift - Enum indirect pour les structures récursives"
// Un enum qui référence lui-même doit être marqué indirect
// (nécessaire pour l'allocation mémoire)
indirect enum ArbreExpression {
    case nombre(Double)
    case addition(ArbreExpression, ArbreExpression)
    case multiplication(ArbreExpression, ArbreExpression)
}

func évaluer(_ expr: ArbreExpression) -> Double {
    switch expr {
    case .nombre(let n):
        return n
    case .addition(let gauche, let droite):
        return évaluer(gauche) + évaluer(droite)
    case .multiplication(let gauche, let droite):
        return évaluer(gauche) * évaluer(droite)
    }
}

// Représente : (3 + 4) * 2
let expr = ArbreExpression.multiplication(
    .addition(.nombre(3), .nombre(4)),
    .nombre(2)
)

print(évaluer(expr))   // 14.0
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les enums Swift sont des types à part entière, pas de simples listes de constantes. Les **raw values** associent une valeur primitive à chaque case et permettent l'initialisation depuis une valeur externe. Les **associated values** permettent à chaque case de transporter des données de types différents — c'est la fonctionnalité la plus puissante et la plus distincte des enums classiques. Le `switch` sur un enum est exhaustif — le compilateur détecte les cas manquants. `Optional<T>` est lui-même un enum avec associated values.

> Dans le module suivant, nous aborderons **Protocols et Extensions** — la philosophie centrale de Swift qui remplace l'héritage multiple et permet d'enrichir n'importe quel type existant.

<br>