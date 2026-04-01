---
description: "KeyPaths Swift : \\Type.propriété, WritableKeyPath, usage dans ForEach, sorted(by:) et pont vers @Binding en SwiftUI."
icon: lucide/book-open-check
tags: ["SWIFT", "KEYPATH", "WRITABLEKEYPATH", "SWIFTUI", "FOREACH"]
---

# KeyPaths

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - L'Adresse Postale d'une Propriété"
    Un KeyPath, c'est l'adresse postale d'une propriété à l'intérieur d'un type. Quand vous écrivez `\.titre`, vous ne lisez pas la valeur de `titre` — vous décrivez **le chemin pour y accéder**. C'est une référence à la propriété elle-même, pas à sa valeur.

    Imaginez une fiche cartonnée représentant un `Article`. Le KeyPath `\.titre` est l'inscription *"Case n°2 : Titre"* sur la fiche. Vous pouvez passer cette instruction à quelqu'un d'autre — il sait où regarder sur n'importe quelle fiche de ce type, sans avoir la fiche sous les yeux au moment où il reçoit l'instruction.

Les KeyPaths apparaissent partout en SwiftUI et dans les APIs Apple sans jamais être explicités. Ce module les démystifie une bonne fois.

<br>

---

## Le Problème Sans KeyPaths

```swift title="Swift - Le problème : accès direct vs référence différée"
struct Article {
    let id: UUID
    var titre: String
    var nombreVues: Int
    var datePublication: Date
}

let article = Article(id: UUID(), titre: "Swift Avancé", nombreVues: 1250, datePublication: .now)

// Accès direct : on lit la valeur MAINTENANT
let titre = article.titre   // "Swift Avancé"

// Mais comment passer à une fonction "accède à la propriété titre de n'importe quel Article" ?
// Sans KeyPaths : on passe une closure
func extraire<T>(_ closure: (Article) -> T, depuis article: Article) -> T {
    closure(article)
}

let titreDérivé = extraire({ $0.titre }, depuis: article)   // Fonctionne mais verbeux

// Avec un KeyPath :
let titreDérivé2 = extraire(\.titre, depuis: article)   // Concis et lisible
```

<br>

---

## Syntaxe des KeyPaths

```swift title="Swift - Déclarer et utiliser un KeyPath"
struct Utilisateur {
    let id: Int
    var nom: String
    var âge: Int
    var estActif: Bool
}

// Un KeyPath se déclare avec le backslash suivi du chemin
let cheminNom: KeyPath<Utilisateur, String> = \.nom
let cheminÂge: KeyPath<Utilisateur, Int>    = \.âge

// Lire une valeur via un KeyPath avec l'opérateur subscript [keyPath:]
let alice = Utilisateur(id: 1, nom: "Alice", âge: 28, estActif: true)

let nom = alice[keyPath: cheminNom]   // "Alice"
let âge = alice[keyPath: cheminÂge]   // 28

// Le type est inféré — on écrit rarement le type complet
let nomInféré = alice[keyPath: \.nom]   // "Alice"

// KeyPaths imbriqués
struct Adresse {
    var ville: String
    var codePostal: String
}

struct Profil {
    var utilisateur: Utilisateur
    var adresse: Adresse
}

let profil = Profil(
    utilisateur: alice,
    adresse: Adresse(ville: "Lyon", codePostal: "69001")
)

// Accès imbriqué
let ville = profil[keyPath: \.adresse.ville]   // "Lyon"
```

*`[keyPath:]` est l'opérateur subscript spécial pour lire ou écrire via un KeyPath. Il fonctionne sur n'importe quelle instance du type racine du KeyPath.*

<br>

---

## Les Trois Types de KeyPaths

Swift distingue plusieurs variantes selon que la propriété est accessible en lecture seule ou en lecture/écriture.

```swift title="Swift - KeyPath, WritableKeyPath et ReferenceWritableKeyPath"
struct Point {
    var x: Double    // var : modifiable
    let y: Double    // let : lecture seule
}

class Nœud {
    var valeur: Int
    init(_ v: Int) { valeur = v }
}

// KeyPath<Root, Value> : lecture seule
// Utilisé pour les propriétés let et les propriétés calculées sans setter
let cheminY: KeyPath<Point, Double> = \.y

// WritableKeyPath<Root, Value> : lecture ET écriture sur les value types (struct)
let cheminX: WritableKeyPath<Point, Double> = \.x

var monPoint = Point(x: 3.0, y: 4.0)
monPoint[keyPath: cheminX] = 10.0   // Écriture possible
print(monPoint.x)   // 10.0
// monPoint[keyPath: cheminY] = 5.0   // ERREUR : cheminY est en lecture seule

// ReferenceWritableKeyPath<Root, Value> : lecture ET écriture sur les reference types (class)
let cheminValeur: ReferenceWritableKeyPath<Nœud, Int> = \.valeur

let nœud = Nœud(42)
nœud[keyPath: cheminValeur] = 99
print(nœud.valeur)   // 99
```

**Tableau des variantes :**

| Type | Struct | Class | Accès |
| --- | --- | --- | --- |
| `KeyPath` | ✓ | ✓ | Lecture seule |
| `WritableKeyPath` | ✓ | — | Lecture + Écriture |
| `ReferenceWritableKeyPath` | — | ✓ | Lecture + Écriture |

<br>

---

## KeyPaths dans les APIs Standard

Les KeyPaths simplifient considérablement les tris et transformations sur les collections.

=== ":simple-swift: Swift"

    ```swift title="Swift - sorted(by:), map et filter avec KeyPaths"
    struct Produit: Identifiable {
        let id: UUID
        var nom: String
        var prix: Double
        var stock: Int
    }

    let produits = [
        Produit(id: UUID(), nom: "Moniteur", prix: 299.0, stock: 5),
        Produit(id: UUID(), nom: "Clavier",  prix: 89.0,  stock: 12),
        Produit(id: UUID(), nom: "Souris",   prix: 45.0,  stock: 0)
    ]

    // Trier par prix avec une closure classique
    let parPrixClosure = produits.sorted { $0.prix < $1.prix }

    // Trier par prix avec un KeyPath (Swift 5.7+)
    let parPrix = produits.sorted(using: KeyPathComparator(\.prix))

    // map avec KeyPath : extraire tous les noms
    let noms = produits.map(\.nom)   // ["Moniteur", "Clavier", "Souris"]

    // filter : produits en stock
    let enStock = produits.filter(\.stock.isZero == false)
    // Alternative classique :
    let enStock2 = produits.filter { $0.stock > 0 }

    // min et max via KeyPath
    let moinsCher = produits.min(by: { $0.prix < $1.prix })
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Pas de KeyPaths natifs"
    // JavaScript n'a pas de KeyPaths
    // Équivalent le plus proche : string comme clé de propriété

    const produits = [
        { nom: "Moniteur", prix: 299 },
        { nom: "Clavier",  prix: 89 },
    ];

    // Trier par une propriété passée comme string
    function trierPar(tableau, clé) {
        return [...tableau].sort((a, b) => a[clé] < b[clé] ? -1 : 1);
    }

    trierPar(produits, "prix");   // Pas de typage, pas de sécurité
    ```

=== ":simple-php: PHP"

    ```php title="PHP - usort avec callback"
    <?php
    $produits = [
        ["nom" => "Moniteur", "prix" => 299],
        ["nom" => "Clavier",  "prix" => 89],
    ];

    // PHP : pas de KeyPaths — callback ou array_column
    usort($produits, fn($a, $b) => $a["prix"] <=> $b["prix"]);

    // array_column : extraction d'une colonne (proche de map(\.nom))
    $noms = array_column($produits, "nom");
    ```

=== ":simple-python: Python"

    ```python title="Python - operator.attrgetter (proche des KeyPaths)"
    from operator import attrgetter

    class Produit:
        def __init__(self, nom, prix):
            self.nom, self.prix = nom, prix

    produits = [Produit("Moniteur", 299), Produit("Clavier", 89)]

    # attrgetter est l'équivalent conceptuel le plus proche d'un KeyPath
    triés = sorted(produits, key=attrgetter("prix"))

    # map avec attrgetter
    noms = list(map(attrgetter("nom"), produits))
    ```

<br>

---

## KeyPaths et `ForEach` en SwiftUI

C'est l'utilisation la plus fréquente des KeyPaths pour un développeur SwiftUI débutant.

```swift title="Swift - ForEach avec Identifiable et KeyPath id:"
import SwiftUI

struct Article: Identifiable {
    let id: UUID
    var titre: String
}

// Cas 1 : Article est Identifiable → ForEach utilise \.id automatiquement
struct ListeArticles: View {
    let articles: [Article]

    var body: some View {
        List {
            ForEach(articles) { article in   // Pas besoin de id: — Identifiable suffit
                Text(article.titre)
            }
        }
    }
}

// Cas 2 : Le type n'est PAS Identifiable → on précise le KeyPath manuellement
struct ListeSimple: View {
    let noms = ["Alice", "Bob", "Charlie"]

    var body: some View {
        List {
            // id: \.self indique que la valeur elle-même sert d'identifiant
            // String est Hashable, donc \.self fonctionne
            ForEach(noms, id: \.self) { nom in
                Text(nom)
            }
        }
    }
}

// Cas 3 : Type avec un identifiant non-standard
struct Ligne {
    var numéro: Int
    var contenu: String
    // Pas de conformance Identifiable
}

struct ListeLignes: View {
    let lignes: [Ligne]

    var body: some View {
        List {
            // On précise explicitement quel KeyPath utilise comme identifiant
            ForEach(lignes, id: \.numéro) { ligne in
                Text(ligne.contenu)
            }
        }
    }
}
```

*`id: \.self` est le pattern à connaître pour les types simples comme `String` et `Int`. Il indique que la valeur elle-même est l'identifiant — ce qui fonctionne seulement si le type est `Hashable`.*

<br>

---

## KeyPaths et `@Binding` en SwiftUI

Les KeyPaths sont le mécanisme sous-jacent des `Binding` en SwiftUI. Comprendre ce lien éclaire pourquoi `$variable.propriété` fonctionne.

```swift title="Swift - Binding et KeyPaths : le lien direct"
import SwiftUI

struct Formulaire {
    var nom: String = ""
    var email: String = ""
    var accepteLesConditions: Bool = false
}

struct VueFormulaire: View {
    @State private var formulaire = Formulaire()

    var body: some View {
        Form {
            // $formulaire est un Binding<Formulaire>
            // $formulaire.nom est un Binding<String>
            // Swift dérive ce Binding via un KeyPath WritableKeyPath<Formulaire, String>
            TextField("Nom", text: $formulaire.nom)
            TextField("Email", text: $formulaire.email)
            Toggle("J'accepte les conditions", isOn: $formulaire.accepteLesConditions)
        }
    }
}

// Le mécanisme sous-jacent :
// $formulaire.nom est équivalent à :
// Binding(
//     get: { formulaire.nom },
//     set: { formulaire.nom = $0 }
// )
// ... qui utilise le WritableKeyPath<Formulaire, String> \.nom
```

*`$variable.propriété` utilise le subscript de `Binding` qui prend un `WritableKeyPath`. SwiftUI génère automatiquement un `Binding<Value>` pour chaque propriété accessible via un chemin écrivable.*

<br>

---

## KeyPaths comme Fonctions

Depuis Swift 5.2, un KeyPath peut être utilisé directement là où une fonction `(Root) -> Value` est attendue.

```swift title="Swift - KeyPath comme fonction"
struct Article {
    let id: UUID
    var titre: String
    var nombreVues: Int
}

let articles = [
    Article(id: UUID(), titre: "Swift Avancé",    nombreVues: 1250),
    Article(id: UUID(), titre: "Protocols",        nombreVues: 890),
    Article(id: UUID(), titre: "Combine",          nombreVues: 2100)
]

// Un KeyPath peut remplacer une closure (Root) -> Value
let titres = articles.map(\.titre)
// Équivalent à : articles.map { $0.titre }

let totalVues = articles.map(\.nombreVues).reduce(0, +)   // 4240

// Trier par nombreVues avec sorted(by:) et KeyPath comme comparateur
let parVues = articles.sorted { $0.nombreVues > $1.nombreVues }

// Avec compactMap et KeyPath
struct Profil {
    var adresse: Adresse?
}

struct Adresse {
    var ville: String
}

let profils = [Profil(adresse: Adresse(ville: "Lyon")), Profil(adresse: nil)]
let villes = profils.compactMap(\.adresse?.ville)   // ["Lyon"]
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un **KeyPath** est une référence à une propriété — pas sa valeur, mais le chemin pour y accéder. La syntaxe est `\.nomPropriété`. `KeyPath` est en lecture seule, `WritableKeyPath` permet l'écriture sur les structs, `ReferenceWritableKeyPath` sur les classes. En SwiftUI, `ForEach(items, id: \.id)` et `$formulaire.nom` utilisent des KeyPaths. Depuis Swift 5.2, un KeyPath peut remplacer une closure `(Root) -> Value` — ce qui simplifie `map`, `filter` et `sorted`.

> Dans le module suivant, nous aborderons les **Result Builders** — le mécanisme qui rend la syntaxe déclarative de SwiftUI possible et transforme une liste d'expressions en une valeur unique.

<br>