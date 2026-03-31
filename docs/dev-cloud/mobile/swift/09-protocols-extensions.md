---
description: "Protocols et Extensions Swift : Protocol-Oriented Programming, conformances, extensions de types existants et default implementations."
icon: lucide/book-open-check
tags: ["SWIFT", "PROTOCOL", "EXTENSION", "POP", "CONFORMANCE", "DEFAULT-IMPLEMENTATION"]
---

# Protocols et Extensions

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire → 🔴 Avancé"
  data-version="1.0"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Cahier des Charges et les Avenant"
    Un **protocol**, c'est un cahier des charges contractuel. Il dit : *"Tout type qui veut se présenter comme Payable doit obligatoirement implémenter une méthode `payer(montant:)`."* Le protocol ne dit pas **comment** faire — seulement **quoi** faire. Chaque type qui signe ce contrat l'implémente à sa manière.

    Une **extension**, c'est un avenant au cahier des charges. Elle ajoute des fonctionnalités à un type **existant** — même un type que vous n'avez pas créé, comme `String` ou `Array`. Elle peut aussi ajouter une implémentation par défaut dans un protocol, offrant ainsi un comportement gratuit à quiconque se conforme.

    C'est le **Protocol-Oriented Programming** (POP) — la philosophie centrale de Swift, recommandée par Apple depuis 2015 comme alternative à l'héritage orienté objet.

<br>

---

## Déclaration d'un Protocol

=== ":simple-swift: Swift"

    ```swift title="Swift - Déclaration et conformance d'un protocol"
    // Un protocol déclare des exigences — pas d'implémentation
    protocol Décrivable {
        // Propriété requise : get signifie accessible en lecture
        var description: String { get }

        // Méthode requise
        func afficher()
    }

    // Conformance : une struct implémente le protocol
    struct Produit: Décrivable {
        let nom: String
        let prix: Double

        // Implémentation des exigences du protocol
        var description: String {
            "\(nom) — \(prix) €"
        }

        func afficher() {
            print("Produit : \(description)")
        }
    }

    // Une class peut aussi se conformer
    class Commande: Décrivable {
        let numéro: Int
        var items: [Produit]

        init(numéro: Int) {
            self.numéro = numéro
            self.items = []
        }

        var description: String {
            "Commande #\(numéro) — \(items.count) article(s)"
        }

        func afficher() {
            print(description)
            items.forEach { $0.afficher() }
        }
    }

    let p = Produit(nom: "Clavier", prix: 89.0)
    p.afficher()   // "Produit : Clavier — 89.0 €"
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Interface simulée (pas de protocol natif)"
    // JavaScript n'a pas de protocol ni d'interface
    // TypeScript apporte les interfaces, proches des protocols Swift

    // TypeScript :
    // interface Décrivable {
    //     readonly description: string;
    //     afficher(): void;
    // }

    // class Produit implements Décrivable {
    //     constructor(public nom: string, public prix: number) {}
    //     get description() { return `${this.nom} — ${this.prix} €`; }
    //     afficher() { console.log(`Produit : ${this.description}`); }
    // }

    // En JS pur : duck typing — si l'objet a les bonnes méthodes, ça marche
    const produit = {
        nom: "Clavier",
        prix: 89.0,
        get description() { return `${this.nom} — ${this.prix} €`; },
        afficher() { console.log(`Produit : ${this.description}`); }
    };
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Interface (équivalent du protocol Swift)"
    <?php
    // PHP : interface est le concept le plus proche du protocol Swift
    interface Décrivable {
        public function getDescription(): string;
        public function afficher(): void;
    }

    class Produit implements Décrivable {
        public function __construct(
            private string $nom,
            private float $prix
        ) {}

        public function getDescription(): string {
            return "{$this->nom} — {$this->prix} €";
        }

        public function afficher(): void {
            echo "Produit : " . $this->getDescription() . PHP_EOL;
        }
    }
    ```

=== ":simple-python: Python"

    ```python title="Python - Protocol (Python 3.8+ via typing)"
    from typing import Protocol

    class Décrivable(Protocol):
        @property
        def description(self) -> str: ...
        def afficher(self) -> None: ...

    # Conformance implicite (structural subtyping)
    class Produit:
        def __init__(self, nom: str, prix: float):
            self.nom = nom
            self.prix = prix

        @property
        def description(self) -> str:
            return f"{self.nom} — {self.prix} €"

        def afficher(self) -> None:
            print(f"Produit : {self.description}")

    # mypy vérifie la conformance statiquement
    ```

<br>

---

## Protocols Multiples

Un type peut se conformer à plusieurs protocols simultanément — c'est la réponse de Swift à l'héritage multiple, sans ses problèmes.

```swift title="Swift - Conformance à plusieurs protocols"
protocol Sérialisable {
    func versDictionnaire() -> [String: Any]
}

protocol Validable {
    var estValide: Bool { get }
    func valider() throws
}

// Erreur personnalisée pour la validation
enum ErreurValidation: Error {
    case champManquant(String)
    case formatInvalide(String, valeur: String)
}

// Un type peut se conformer aux deux protocols
struct UtilisateurForm: Décrivable, Sérialisable, Validable {
    var email: String
    var motDePasse: String

    var description: String { "Formulaire : \(email)" }
    func afficher() { print(description) }

    func versDictionnaire() -> [String: Any] {
        ["email": email, "password": motDePasse]
    }

    var estValide: Bool {
        !email.isEmpty && email.contains("@") && motDePasse.count >= 8
    }

    func valider() throws {
        guard !email.isEmpty else {
            throw ErreurValidation.champManquant("email")
        }
        guard email.contains("@") else {
            throw ErreurValidation.formatInvalide("email", valeur: email)
        }
        guard motDePasse.count >= 8 else {
            throw ErreurValidation.champManquant("motDePasse — minimum 8 caractères")
        }
    }
}

// Protocol composition : exiger plusieurs conformances simultanément
func enregistrer(_ form: Sérialisable & Validable) throws {
    try form.valider()
    let données = form.versDictionnaire()
    print("Enregistrement : \(données)")
}
```

<br>

---

## Extensions

Une extension ajoute des fonctionnalités à un type **existant** — sans modifier son code source, sans sous-classer.

```swift title="Swift - Extensions sur des types existants"
// Extension de String : ajouter des méthodes personnalisées
extension String {
    // Vérifie si la chaîne est un email valide (simplifié)
    var estUnEmail: Bool {
        contains("@") && contains(".") && count > 5
    }

    // Tronquer la chaîne à une longueur maximale
    func tronquer(à longueur: Int, suffixe: String = "...") -> String {
        guard count > longueur else { return self }
        return String(prefix(longueur)) + suffixe
    }

    // Répéter une chaîne
    func répéter(_ fois: Int) -> String {
        String(repeating: self, count: fois)
    }
}

print("alice@example.com".estUnEmail)          // true
print("pas-un-email".estUnEmail)               // false
print("Bonjour tout le monde".tronquer(à: 10)) // "Bonjour to..."
print("ha".répéter(3))                         // "hahaha"

// Extension d'Array avec contrainte de type
extension Array where Element: Numeric {
    var somme: Element {
        reduce(0, +)
    }

    var moyenne: Double {
        Double(somme as! Int) / Double(count)
        // Note : simplification — la vraie implémentation utilise des generics
    }
}

let notes = [14, 18, 12, 15, 17]
print(notes.somme)   // 76
```

```swift title="Swift - Extensions pour organiser le code"
// Une pratique courante : séparer les conformances en extensions séparées
struct Article {
    let titre: String
    let contenu: String
    let datePublication: Date
    var nombreVues: Int
}

// Extension pour Equatable
extension Article: Equatable {
    static func == (lhs: Article, rhs: Article) -> Bool {
        lhs.titre == rhs.titre
    }
}

// Extension pour Comparable
extension Article: Comparable {
    static func < (lhs: Article, rhs: Article) -> Bool {
        lhs.datePublication < rhs.datePublication
    }
}

// Extension pour CustomStringConvertible
extension Article: CustomStringConvertible {
    var description: String {
        "[\(nombreVues) vues] \(titre)"
    }
}
```

<br>

---

## Default Implementations — Comportement Gratuit

Un protocol peut fournir une implémentation par défaut via une extension. Les types conformes héritent de cette implémentation gratuitement, et peuvent la surcharger si besoin.

```swift title="Swift - Default implementations dans les protocols"
protocol Journalisable {
    var nomType: String { get }
    func journaliser(_ message: String)
    func avertir(_ message: String)
    func erreur(_ message: String)
}

// Extension du protocol : implémentation par défaut
extension Journalisable {
    // nomType : par défaut, le nom du type Swift
    var nomType: String {
        String(describing: type(of: self))
    }

    // Implémentation par défaut pour avertir et erreur
    func avertir(_ message: String) {
        journaliser("⚠️ [\(nomType)] \(message)")
    }

    func erreur(_ message: String) {
        journaliser("❌ [\(nomType)] \(message)")
    }
}

// Service minimal : implémente seulement journaliser
// Les autres méthodes sont fournies gratuitement
struct ServicePaiement: Journalisable {
    func journaliser(_ message: String) {
        print("[LOG \(Date())] \(message)")
    }

    func traiterPaiement(montant: Double) {
        journaliser("Paiement de \(montant) € initié")
        // ... logique de paiement
        avertir("Délai de traitement élevé")   // Méthode héritée du protocol
    }
}

// Service avec surcharge : personnalise l'implémentation
struct ServiceNotification: Journalisable {
    func journaliser(_ message: String) {
        print(message)
    }

    // Surcharge de la default implementation
    func erreur(_ message: String) {
        journaliser("ERREUR CRITIQUE: \(message)")
        // Envoyer une alerte PagerDuty...
    }
}
```

<br>

---

## Protocols comme Types

Un protocol peut être utilisé comme type — une variable de type `Décrivable` peut contenir n'importe quel type conforme.

```swift title="Swift - Protocols comme types polymorphes"
// any Décrivable : peut contenir n'importe quel type conforme (Swift 5.7+)
var éléments: [any Décrivable] = []
éléments.append(Produit(nom: "Souris", prix: 45.0))
éléments.append(Commande(numéro: 1001))

for élément in éléments {
    élément.afficher()
}

// some Décrivable : type opaque — un type précis mais non nommé (pour les retours)
// Utilisé massivement dans SwiftUI : var body: some View { ... }
func créerDécrivable() -> some Décrivable {
    Produit(nom: "Clavier", prix: 89.0)
    // Le type de retour exact est Produit, mais l'appelant voit seulement Décrivable
}
```

!!! note "any vs some — la distinction SwiftUI"
    `any Protocol` est une boîte qui peut contenir n'importe quel type conforme (existential type — a un coût de performance). `some Protocol` est un type opaque : le compilateur connaît le type exact mais l'appelant ne le voit pas — c'est ce qu'utilise SwiftUI avec `some View`. Cette distinction deviendra centrale en SwiftUI.

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un **protocol** définit un contrat — des propriétés et méthodes requises, sans implémentation. N'importe quel type (struct, class, enum) peut s'y conformer. Une **extension** enrichit un type existant sans le modifier — même les types de la bibliothèque standard comme `String` ou `Array`. Les **default implementations** dans les extensions de protocols offrent un comportement gratuit aux types conformes. Un type peut se conformer à plusieurs protocols simultanément — c'est l'alternative Swift à l'héritage multiple.

> Dans le module suivant, nous aborderons les **Generics** — le mécanisme qui permet d'écrire du code qui fonctionne avec n'importe quel type tout en restant statiquement typé.

<br>