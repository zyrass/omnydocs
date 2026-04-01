---
description: "Result Builders Swift : @resultBuilder, buildBlock, @ViewBuilder et la syntaxe déclarative de SwiftUI expliquée."
icon: lucide/book-open-check
tags: ["SWIFT", "RESULT-BUILDER", "VIEWBUILDER", "SWIFTUI", "DSL"]
---

# Result Builders

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Monteur Vidéo"
    Imaginez un monteur vidéo. Vous lui apportez une liste de clips dans un ordre précis. Lui, il prend cette liste, l'assemble selon des règles définies, et vous restitue une séquence vidéo cohérente — une seule valeur unifiée à partir de plusieurs éléments.

    Un **Result Builder**, c'est ce monteur. Vous lui donnez une liste d'expressions Swift dans un bloc `{ }`, il les assemble selon les règles que vous avez définies, et produit une valeur unique. C'est exactement ce que fait `@ViewBuilder` en SwiftUI : il prend une liste de `View` dans `body` et les assemble en une seule `View` composite.

    Sans comprendre les Result Builders, la question *"pourquoi est-ce que je peux écrire plusieurs vues dans `body` sans virgule ni `return` explicite ?"* reste sans réponse satisfaisante.

<br>

---

## Le Problème Que les Result Builders Résolvent

```swift title="Swift - Sans Result Builder : la syntaxe verbeuse"
import SwiftUI

// Sans Result Builder, construire une VStack nécessiterait :
let vue = VStack(content: {
    return TupleView((
        Text("Titre"),
        Text("Sous-titre"),
        Button("Action", action: {})
    ))
})

// Avec @ViewBuilder (un Result Builder) :
let vueSimplifiée = VStack {
    Text("Titre")
    Text("Sous-titre")
    Button("Action") {}
}
// Pas de return, pas de virgules, pas de TupleView explicite
// @ViewBuilder transforme la liste en une valeur unique automatiquement
```

*La syntaxe déclarative de SwiftUI — celle que vous utiliserez chaque jour — est entièrement rendue possible par `@ViewBuilder`, qui est un Result Builder.*

<br>

---

## Anatomie d'un Result Builder

Un Result Builder est un type annoté `@resultBuilder`. Il doit implémenter au minimum une méthode statique `buildBlock`.

```swift title="Swift - Créer un Result Builder minimal"
// @resultBuilder : marque ce type comme un Result Builder
@resultBuilder
struct AssembleurDeTextes {
    // buildBlock : méthode statique OBLIGATOIRE
    // Elle reçoit les expressions du bloc et les assemble
    // Le nombre de paramètres dépend de ce qu'on veut supporter

    // Bloc avec un seul élément
    static func buildBlock(_ composant: String) -> String {
        composant
    }

    // Bloc avec deux éléments
    static func buildBlock(_ c1: String, _ c2: String) -> String {
        c1 + "\n" + c2
    }

    // Bloc avec trois éléments
    static func buildBlock(_ c1: String, _ c2: String, _ c3: String) -> String {
        c1 + "\n" + c2 + "\n" + c3
    }
}

// Utilisation : annoter un paramètre de fonction avec @AssembleurDeTextes
func créerDocument(@AssembleurDeTextes contenu: () -> String) -> String {
    contenu()
}

let document = créerDocument {
    "Titre principal"
    "Corps du texte"
    "Conclusion"
}

print(document)
// "Titre principal
//  Corps du texte
//  Conclusion"
```

*Les trois expressions dans le bloc `{ }` sont interceptées par `buildBlock(_ c1:, _ c2:, _ c3:)`. Le compilateur Swift transforme silencieusement le bloc en un appel à `buildBlock`.*

<br>

---

## Les Méthodes de Construction

Un Result Builder peut implémenter plusieurs méthodes pour gérer différents scénarios — conditions, boucles, optionnels.

```swift title="Swift - Result Builder avec support des conditions et optionnels"
@resultBuilder
struct AssembleurHTML {

    // Bloc de base : assemble N composants
    static func buildBlock(_ composants: String...) -> String {
        composants.joined(separator: "\n")
    }

    // Optionnel : buildOptional — gère if sans else
    static func buildOptional(_ composant: String?) -> String {
        composant ?? ""
    }

    // Condition : buildEither — gère if/else
    static func buildEither(first composant: String) -> String {
        composant
    }

    static func buildEither(second composant: String) -> String {
        composant
    }

    // Tableau : buildArray — gère for...in
    static func buildArray(_ composants: [String]) -> String {
        composants.joined(separator: "\n")
    }
}

func html(@AssembleurHTML contenu: () -> String) -> String {
    "<div>\n\(contenu())\n</div>"
}

let estConnecté = true
let articles = ["Swift", "SwiftUI", "Vapor"]

let page = html {
    "<h1>OmnyDocs</h1>"

    // if/else : utilise buildEither(first:) et buildEither(second:)
    if estConnecté {
        "<p>Bienvenue, Alice</p>"
    } else {
        "<p>Veuillez vous connecter</p>"
    }

    // for...in : utilise buildArray
    for article in articles {
        "<li>\(article)</li>"
    }
}

print(page)
```

<br>

---

## `@ViewBuilder` — Le Result Builder de SwiftUI

`@ViewBuilder` est le Result Builder qu'Apple fournit pour construire des hiérarchies de vues. C'est le même mécanisme que nous venons de créer, mais appliqué au type `View`.

```swift title="Swift - Comment @ViewBuilder fonctionne"
import SwiftUI

// @ViewBuilder est défini approximativement comme suit dans la bibliothèque Apple :
// @resultBuilder
// public struct ViewBuilder {
//     public static func buildBlock() -> EmptyView
//     public static func buildBlock<C0: View>(_ c0: C0) -> C0
//     public static func buildBlock<C0: View, C1: View>(_ c0: C0, _ c1: C1) -> TupleView<(C0, C1)>
//     public static func buildBlock<C0, C1, C2>(...) -> TupleView<(C0, C1, C2)>
//     // ... jusqu'à 10 éléments
//     public static func buildOptional<C: View>(_ component: C?) -> C?
//     public static func buildEither<T: View, F: View>(first: T) -> _ConditionalContent<T, F>
//     public static func buildEither<T: View, F: View>(second: F) -> _ConditionalContent<T, F>
// }

// Donc quand vous écrivez :
struct MaVue: View {
    @State private var afficherDétails = false

    var body: some View {
        // Le protocole View déclare : @ViewBuilder var body: some View { get }
        // Ce @ViewBuilder transforme le contenu du bloc en une View composite
        VStack {
            Text("Titre")            // View 1
            Text("Sous-titre")       // View 2

            if afficherDétails {     // buildEither — _ConditionalContent
                Text("Détails...")
            }

            Button("Toggle") {       // View 3
                afficherDétails.toggle()
            }
        }
        // VStack reçoit un @ViewBuilder — il peut prendre plusieurs vues sans virgule
    }
}
```

*`TupleView<(C0, C1, C2)>` est le type réel retourné quand vous mettez 3 vues dans un bloc. C'est pour cette raison que SwiftUI impose une limite de 10 vues directes dans un même bloc — `buildBlock` n'est défini que jusqu'à 10 paramètres. Au-delà, il faut utiliser `Group { }` pour regrouper.*

<br>

---

## Annoter ses Propres Fonctions avec `@ViewBuilder`

Vous pouvez annoter vos propres paramètres et méthodes avec `@ViewBuilder` pour créer des composants SwiftUI réutilisables.

```swift title="Swift - Utiliser @ViewBuilder dans ses propres composants"
import SwiftUI

// Créer un composant de carte réutilisable qui accepte n'importe quelle vue en contenu
struct Carte<Contenu: View>: View {
    let titre: String
    // @ViewBuilder : le contenu peut être n'importe quelle(s) vue(s)
    let contenu: Contenu

    // init avec @ViewBuilder sur le paramètre closure
    init(titre: String, @ViewBuilder contenu: () -> Contenu) {
        self.titre = titre
        self.contenu = contenu()
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(titre)
                .font(.headline)

            Divider()

            contenu   // Le contenu passé par l'utilisateur
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 4)
    }
}

// Utilisation : le contenu peut être n'importe quelle combinaison de vues
struct ExempleVue: View {
    var body: some View {
        VStack {
            // Carte avec une seule vue
            Carte(titre: "Résumé") {
                Text("Total : 42 articles")
            }

            // Carte avec plusieurs vues — @ViewBuilder les assemble
            Carte(titre: "Statistiques") {
                HStack {
                    Label("Articles", systemImage: "doc")
                    Spacer()
                    Text("42")
                }
                HStack {
                    Label("Vues", systemImage: "eye")
                    Spacer()
                    Text("12 450")
                }
            }

            // Carte avec condition — @ViewBuilder gère if/else
            Carte(titre: "Statut") {
                if true {
                    Label("Actif", systemImage: "checkmark.circle.fill")
                        .foregroundColor(.green)
                } else {
                    Label("Inactif", systemImage: "xmark.circle")
                        .foregroundColor(.red)
                }
            }
        }
    }
}
```

<br>

---

## Créer un DSL avec un Result Builder

Les Result Builders permettent de créer des **DSL** (Domain Specific Languages) — des mini-langages expressifs pour un domaine précis. NSAttributedString, SwiftUI, et même certaines bibliothèques de test utilisent ce pattern.

```swift title="Swift - DSL de validation avec Result Builder"
// Un Result Builder pour construire des règles de validation
protocol RègleValidation {
    func valider(_ texte: String) -> String?   // nil = valide, String = message d'erreur
}

struct LongueurMinimale: RègleValidation {
    let minimum: Int
    func valider(_ texte: String) -> String? {
        texte.count >= minimum ? nil : "Minimum \(minimum) caractères requis"
    }
}

struct ContientChiffre: RègleValidation {
    func valider(_ texte: String) -> String? {
        texte.first(where: { $0.isNumber }) != nil ? nil : "Doit contenir au moins un chiffre"
    }
}

struct ContientMajuscule: RègleValidation {
    func valider(_ texte: String) -> String? {
        texte.first(where: { $0.isUppercase }) != nil ? nil : "Doit contenir une majuscule"
    }
}

@resultBuilder
struct ValidateurMotDePasse {
    static func buildBlock(_ règles: any RègleValidation...) -> [any RègleValidation] {
        Array(règles)
    }
}

func valider(
    motDePasse: String,
    @ValidateurMotDePasse règles: () -> [any RègleValidation]
) -> [String] {
    règles().compactMap { $0.valider(motDePasse) }
}

// Utilisation : syntaxe déclarative claire
let erreurs = valider(motDePasse: "abc") {
    LongueurMinimale(minimum: 8)
    ContientChiffre()
    ContientMajuscule()
}

print(erreurs)
// ["Minimum 8 caractères requis", "Doit contenir au moins un chiffre", "Doit contenir une majuscule"]
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Un **Result Builder** transforme une liste d'expressions dans un bloc `{ }` en une valeur unique. `buildBlock` est la méthode centrale — elle assemble les composants. `buildOptional`, `buildEither` et `buildArray` ajoutent le support des `if`, `if/else` et `for` dans le bloc. **`@ViewBuilder`** est le Result Builder de SwiftUI — il transforme vos listes de vues en une `View` composite. La limite de 10 vues directes dans un bloc SwiftUI est une conséquence directe du nombre de variantes de `buildBlock` définies. Annoter vos propres paramètres avec `@ViewBuilder` vous permet de créer des composants SwiftUI réutilisables.

> Dans le module suivant, nous aborderons **Combine** — le framework réactif d'Apple qui alimente `@Published`, `ObservableObject` et la communication entre les vues et les ViewModels en SwiftUI.

<br>