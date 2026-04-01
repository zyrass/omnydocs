---
description: "Glossaire — Développement Mobile : Swift, SwiftUI, UIKit, iOS, Xcode et l'écosystème Apple."
icon: lucide/book-a
tags: ["GLOSSAIRE", "MOBILE", "SWIFT", "IOS", "APPLE", "SWIFTUI"]
---

# Développement Mobile

<div
  class="omny-meta"
  data-level="🟢 Tout niveau"
  data-version="1.0"
  data-time="Consultation">
</div>

## A

!!! note "ABI"
    > Interface binaire définissant comment le code compilé interagit avec le système d'exploitation et les autres bibliothèques au niveau machine.

    L'ABI (Application Binary Interface) est ce qui permet à Swift d'être stable depuis Swift 5.0 — le code compilé avec une version du compilateur peut s'exécuter avec une version différente de la runtime Swift, sans recompilation.

    - **Acronyme :** Application Binary Interface
    - **Stabilité Swift :** atteinte avec Swift 5.0 en 2019 — fondamentale pour la distribution sur l'App Store
    - **Conséquence :** Swift est livré avec iOS depuis iOS 12.2, plus besoin de l'embarquer dans l'app

    ```mermaid
    graph LR
        A[ABI] --> B[Code compilé]
        A --> C[Runtime Swift]
        A --> D[Stabilité iOS 12.2+]
    ```

<br>

---

!!! note "Actor"
    > Type de référence Swift conçu pour la concurrence sécurisée, garantissant qu'un seul thread accède à son état mutable à la fois.

    Les actors isolent leur état — tout accès se fait de manière asynchrone. Swift Concurrency utilise les actors pour éliminer les data races sans verrous manuels, rendant le code concurrent à la fois sûr et lisible.

    - **Syntaxe :** `actor BankAccount { var balance: Double }`
    - **MainActor :** actor spécial garantissant l'exécution sur le thread principal (UI)
    - **Différence :** classe ordinaire (accès concurrent non protégé) vs. actor (accès sérialisé)

    ```swift title="Swift — Déclaration d'un actor"
    actor BankAccount {
        var balance: Double = 0.0

        func deposit(_ amount: Double) {
            balance += amount // sécurisé, un seul accès concurrent
        }
    }
    ```

    _Un `actor` protège son état interne : tout appel de méthode depuis l'extérieur est implicitement `await`._

    ```mermaid
    graph LR
        A[Actor] --> B[Isolation état]
        A --> C[Swift Concurrency]
        A --> D[MainActor — UI]
    ```

<br>

---

!!! note "App Lifecycle"
    > Ensemble des états et transitions qu'une application iOS traverse depuis son lancement jusqu'à sa fermeture.

    Comprendre le cycle de vie est essentiel pour gérer correctement les ressources. Une app peut être active, en arrière-plan, suspendue ou terminée — chaque transition déclenche des callbacks spécifiques à exploiter.

    - **États (UIKit) :** Not Running → Inactive → Active → Background → Suspended
    - **SwiftUI :** `@Environment(\.scenePhase)` avec les valeurs `.active`, `.inactive`, `.background`
    - **Callbacks clés :** `applicationDidBecomeActive`, `applicationDidEnterBackground`, `sceneDidBecomeActive`

    ```mermaid
    graph LR
        A[App Lifecycle] --> B[Not Running]
        B --> C[Active]
        C --> D[Background]
        D --> E[Suspended]
    ```

<br>

---

!!! note "App Store Connect"
    > Plateforme Apple de gestion des applications distribuées sur l'App Store — soumission, métadonnées, pricing et analytics.

    App Store Connect est le portail central pour tout développeur Apple. On y soumet les builds (via Xcode ou Transporter), on configure les métadonnées (descriptions, screenshots, mots-clés), on gère les testeurs TestFlight et on consulte les analytics de performance.

    - **Fonctions :** soumission d'apps, TestFlight (beta), analytics, gestion des In-App Purchases, certificats
    - **Review :** chaque soumission est revue par l'équipe Apple (délai : quelques heures à quelques jours)
    - **URL :** [appstoreconnect.apple.com](https://appstoreconnect.apple.com)

    ```mermaid
    graph LR
        A[App Store Connect] --> B[Soumission builds]
        A --> C[TestFlight beta]
        A --> D[Analytics performances]
    ```

<br>

---

!!! note "Async/Await"
    > Syntaxe Swift moderne pour l'écriture de code asynchrone de manière séquentielle et lisible, sans callbacks ni completion handlers.

    Avant Swift Concurrency, la gestion des opérations asynchrones reposait sur des closures imbriquées ("callback hell") ou des frameworks comme Combine/RxSwift. `async/await` rend le code asynchrone aussi lisible que du code synchrone.

    - **Introduit :** Swift 5.5 (iOS 15, Xcode 13) — compatible iOS 13+ avec back-deployment partiel
    - **`async` :** marque une fonction comme asynchrone
    - **`await` :** suspend l'exécution jusqu'à la complétion de la tâche asynchrone

    ```swift title="Swift — Async/Await vs. completion handler"
    // Avant : callback hell
    fetchUser(id: 1) { user in
        fetchPosts(for: user) { posts in
            display(posts)
        }
    }

    // Avec async/await : séquentiel et lisible
    let user  = try await fetchUser(id: 1)
    let posts = try await fetchPosts(for: user)
    display(posts)
    ```

    _`await` indique un point de suspension — le thread peut traiter d'autres tâches en attendant._

    ```mermaid
    graph LR
        A[Async/Await] --> B[Swift Concurrency]
        A --> C[Code séquentiel lisible]
        A --> D[Task — exécution]
    ```

<br>

---

## B

!!! note "Bundle Identifier"
    > Chaîne de caractères unique identifiant une application Apple sur l'ensemble des plateformes et services Apple.

    Le Bundle ID est l'empreinte digitale de votre application dans l'écosystème Apple. Il suit le format DNS inversé (`com.nomEntreprise.nomApp`) et doit être unique sur l'App Store. Il est utilisé pour les push notifications, les entitlements, iCloud, et la signature du code.

    - **Format :** `com.example.monApp` (DNS inversé)
    - **Immuable :** une fois soumis sur l'App Store, ne peut plus être changé
    - **Usage :** push notifications (APNs), Universal Links, App Clips, entitlements

    ```mermaid
    graph LR
        A[Bundle Identifier] --> B[Identité app Apple]
        A --> C[App Store unique]
        A --> D[Push notifications APNs]
    ```

<br>

---

## C

!!! note "Closure"
    > Bloc de code autonome et de première classe pouvant être stocké, passé en paramètre et capturant son contexte environnant.

    Les closures sont l'équivalent Swift des lambdas ou fonctions anonymes. Elles capturent les variables de leur contexte (`[weak self]` pour éviter les cycles de rétention). Elles sont omniprésentes dans les APIs UIKit (completion handlers, animations, callbacks).

    - **Capture list :** `[weak self]`, `[unowned self]` pour éviter les retain cycles
    - **Trailing closure :** syntaxe compacte si la closure est le dernier paramètre
    - **Escaping :** `@escaping` si la closure est appelée après le retour de la fonction

    ```swift title="Swift — Closure avec capture list"
    // Trailing closure
    UIView.animate(withDuration: 0.3) {
        self.view.alpha = 0
    }

    // Escaping closure avec [weak self]
    networkService.fetchData { [weak self] result in
        guard let self = self else { return }
        self.updateUI(with: result)
    }
    ```

    _`[weak self]` empêche la closure de retenir fortement `self` — essentiel pour éviter les fuites mémoire._

    ```mermaid
    graph LR
        A[Closure] --> B[Capture context]
        A --> C[Callbacks UIKit]
        A --> D[weak self retain cycle]
    ```

<br>

---

!!! note "Codable"
    > Protocole Swift combinant `Encodable` et `Decodable` pour sérialiser et désérialiser des données JSON/XML automatiquement.

    `Codable` est l'une des fonctionnalités les plus pratiques de Swift. Une struct ou classe conforme à `Codable` peut être encodée en JSON et décodée depuis JSON automatiquement, sans écrire manuellement de code de parsing.

    - **Composition :** `Codable = Encodable + Decodable`
    - **CodingKeys :** enum permettant de mapper des clés JSON vers des propriétés Swift au nom différent
    - **JSONDecoder / JSONEncoder :** les classes standard pour encoder/décoder

    ```swift title="Swift — Struct Codable et décodage JSON"
    struct User: Codable {
        let id: Int
        let name: String
        let email: String
    }

    // Décodage depuis JSON
    let json = """{"id": 1, "name": "Alice", "email": "alice@example.com"}"""
    let data = json.data(using: .utf8)!
    let user = try JSONDecoder().decode(User.self, from: data)
    ```

    _Swift synthétise automatiquement les méthodes `encode` et `decode` pour les types conformes à `Codable`._

    ```mermaid
    graph LR
        A[Codable] --> B[JSON parsing]
        A --> C[JSONDecoder]
        A --> D[Encodable / Decodable]
    ```

<br>

---

!!! note "Combine"
    > Framework Apple de programmation réactive (reactive programming) permettant de chaîner et de transformer des flux de valeurs asynchrones.

    Combine introduit les concepts de Publisher (émetteur de valeurs) et Subscriber (consommateur). Il permet de composer des pipelines de traitement de données asynchrones — transformation, filtrage, fusion, gestion d'erreurs — de manière déclarative.

    - **Introduit :** iOS 13, macOS 10.15 — framework First-Party Apple
    - **Concepts :** Publisher, Subscriber, Subject, Operator (`map`, `filter`, `flatMap`, `combineLatest`)
    - **Intégration SwiftUI :** `@Published` + `ObservableObject` reposent sur Combine

    ```swift title="Swift — Pipeline Combine"
    import Combine

    let publisher = [1, 2, 3, 4, 5].publisher
    publisher
        .filter { $0 % 2 == 0 }   // garde les pairs
        .map    { $0 * 10 }        // multiplie par 10
        .sink   { print($0) }      // affiche : 20, 40
    ```

    _Chaque opérateur retourne un nouveau Publisher — les pipelines Combine sont composables à l'infini._

    ```mermaid
    graph LR
        A[Combine] --> B[Publisher Subscriber]
        A --> C[Reactive programming]
        A --> D[SwiftUI @Published]
    ```

<br>

---

!!! note "Core Data"
    > Framework Apple de persistance et de gestion objet-graphe pour stocker, requêter et synchroniser des données structurées sur iOS.

    Core Data n'est pas une base de données — c'est une couche de gestion d'objet-graphe. Derrière, il peut utiliser SQLite, des fichiers binaires ou mémoire. Il gère automatiquement les relations entre objets, les migrations de schéma et l'intégration avec CloudKit (synchronisation iCloud).

    - **Stack :** NSPersistentContainer (simplifié), NSManagedObjectContext, NSManagedObject
    - **Intégration SwiftUI :** `@FetchRequest`, `@Environment(\.managedObjectContext)`
    - **Alternatives modernes :** SwiftData (iOS 17+), Realm, SQLite.swift

    ```mermaid
    graph LR
        A[Core Data] --> B[Persistance SQLite]
        A --> C[Object graph]
        A --> D[CloudKit iCloud sync]
    ```

<br>

---

## D

!!! note "Delegate Pattern"
    > Patron de conception permettant à un objet de déléguer certaines de ses responsabilités à un autre objet via un protocole.

    Le pattern Delegate est au cœur de UIKit. `UITableViewDelegate`, `UITextFieldDelegate`, `URLSessionDelegate` — des dizaines d'APIs Apple fonctionnent ainsi. L'objet délégant définit un protocole, l'objet délégué l'implémente.

    - **Mécanisme :** protocole + propriété `weak var delegate: MonProtocole?`
    - **`weak` obligatoire :** éviter les retain cycles (A retient B, B retient A)
    - **Alternative moderne :** closures / callbacks, Combine, async/await

    ```swift title="Swift — Delegate pattern"
    protocol DataServiceDelegate: AnyObject {
        func didReceiveData(_ data: [String])
    }

    class DataService {
        weak var delegate: DataServiceDelegate?

        func fetch() {
            // ... appel réseau ...
            delegate?.didReceiveData(["item1", "item2"])
        }
    }
    ```

    _`weak var delegate` est impératif — une référence forte créerait un cycle de rétention._

    ```mermaid
    graph LR
        A[Delegate Pattern] --> B[Protocole]
        A --> C[UIKit APIs]
        A --> D[weak — retain cycle]
    ```

<br>

---

## E

!!! note "Enum avec associated values"
    > Énumération Swift pouvant stocker des données supplémentaires de types différents pour chaque case.

    Les enums Swift sont bien plus puissants que dans la plupart des langages. Chaque case peut porter des valeurs associées de types différents — ce qui permet de modéliser des états complexes de manière typée et exhaustive, notamment pour la gestion des résultats d'API.

    - **Syntaxe :** `case success(Data)` — la donnée fait partie du case
    - **Pattern matching :** `if case .failure(let error) = result { ... }`
    - **`Result<Success, Failure>` :** type standard Swift utilisant des associated values

    ```swift title="Swift — Enum avec associated values"
    enum NetworkResult {
        case success(Data)
        case failure(Error)
        case loading
    }

    func handle(_ result: NetworkResult) {
        switch result {
        case .success(let data):   process(data)
        case .failure(let error):  showError(error)
        case .loading:             showSpinner()
        }
    }
    ```

    _Le compilateur Swift vérifie l'exhaustivité du `switch` — chaque case doit être traité._

    ```mermaid
    graph LR
        A[Enum associated values] --> B[Modélisation états]
        A --> C[Result type]
        A --> D[Pattern matching]
    ```

<br>

---

## G

!!! note "Generics"
    > Mécanisme Swift permettant d'écrire du code flexible et réutilisable qui fonctionne avec n'importe quel type satisfaisant des contraintes données.

    Les generics sont fondamentaux dans Swift — `Array<Element>`, `Optional<Wrapped>`, `Result<Success, Failure>` sont tous des types génériques. Ils permettent d'écrire une logique une seule fois, valide pour de nombreux types différents.

    - **Syntaxe :** `func swap<T>(_ a: inout T, _ b: inout T)`
    - **Contraintes :** `where T: Comparable`, `T: Codable`, `T: Equatable`
    - **Opaque types :** `some View` (SwiftUI) est un type générique opaque

    ```swift title="Swift — Fonction générique avec contrainte"
    // Fonctionne avec tout type Comparable
    func maximum<T: Comparable>(_ a: T, _ b: T) -> T {
        return a > b ? a : b
    }

    maximum(3, 7)           // → 7 (Int)
    maximum("apple", "zen") // → "zen" (String)
    ```

    _Une contrainte (`T: Comparable`) garantit que seuls les types compatibles peuvent être utilisés._

    ```mermaid
    graph LR
        A[Generics] --> B[Réutilisabilité]
        A --> C[Type safety compile-time]
        A --> D[Array Optional Result]
    ```

<br>

---

## N

!!! note "NavigationStack"
    > Container SwiftUI gérant la navigation par pile (push/pop) entre vues, avec support des deep links et des états externalisés.

    `NavigationStack` (introduit iOS 16) remplace `NavigationView` en offrant un contrôle programmatique complet de la pile de navigation. L'état de navigation est externalisé dans un tableau, permettant des deep links, des bookmarks et des tests.

    - **Introduit :** iOS 16, remplace `NavigationView`
    - **Navigation par valeur :** `.navigationDestination(for: Type.self)` + `NavigationPath`
    - **Deep linking :** la pile de navigation peut être reconstruite depuis un URL ou un état sauvegardé

    ```swift title="Swift — NavigationStack avec navigationDestination"
    NavigationStack {
        List(items) { item in
            NavigationLink(value: item) {
                Text(item.name)
            }
        }
        .navigationDestination(for: Item.self) { item in
            ItemDetailView(item: item)
        }
    }
    ```

    _Chaque `NavigationLink(value:)` pousse la `navigationDestination` correspondante sur la pile._

    ```mermaid
    graph LR
        A[NavigationStack] --> B[Navigation par pile]
        A --> C[Deep linking URL]
        A --> D[NavigationPath état]
    ```

<br>

---

## O

!!! note "Observable"
    > Macro Swift (iOS 17+) remplaçant `ObservableObject` + `@Published` par une observation automatique et granulaire des propriétés.

    `@Observable` est la nouvelle façon de gérer l'état dans SwiftUI. Le compilateur instrumente automatiquement les accès aux propriétés — seules les vues qui lisent une propriété spécifique se re-rendent quand elle change, ce qui améliore les performances.

    - **Introduit :** Swift 5.9, iOS 17 (via le framework Observation)
    - **Migration :** `class ViewModel: ObservableObject` + `@Published` → `@Observable class ViewModel`
    - **Avantage :** observation granulaire (propriété par propriété, pas struct entière)

    ```swift title="Swift — @Observable vs. ObservableObject"
    // Avant (iOS 13+)
    class ViewModel: ObservableObject {
        @Published var count = 0
        @Published var name  = ""
    }

    // Avec @Observable (iOS 17+)
    @Observable class ViewModel {
        var count = 0
        var name  = ""
    }
    ```

    _Avec `@Observable`, SwiftUI ne re-rend que les vues qui lisent `count` si `count` change — pas toutes les vues abonnées à `ViewModel`._

    ```mermaid
    graph LR
        A[Observable] --> B[iOS 17 Macro]
        A --> C[Observation granulaire]
        A --> D[ObservableObject migration]
    ```

<br>

---

!!! note "Optionals"
    > Type Swift représentant explicitement l'absence possible d'une valeur, éliminant les NullPointerExceptions au niveau du système de types.

    `Optional<T>` est l'une des décisions de design les plus importantes de Swift — toute valeur pouvant être `nil` doit être déclarée explicitement comme `Optional`. Le compilateur force le développeur à gérer ce cas, éliminant la principale source de bugs dans les langages à valeur nulle implicite.

    - **Syntaxe :** `var name: String?` est équivalent à `var name: Optional<String>`
    - **Unwrapping :** `if let`, `guard let`, `??` (nil coalescing), `!` (force — dangereux)
    - **Optional chaining :** `user?.address?.city` — retourne `nil` si n'importe quel maillon est `nil`

    ```swift title="Swift — Gestion sécurisée des optionals"
    var city: String? = "Paris"

    // if let (safe unwrap)
    if let c = city { print(c) }

    // guard let (early exit)
    guard let c = city else { return }

    // nil coalescing (valeur par défaut)
    let display = city ?? "Ville inconnue"

    // optional chaining (ne crash pas)
    let upper = city?.uppercased()
    ```

    _Préférez `if let` / `guard let` au force-unwrap `!` — une valeur `nil` forcée provoque un crash immédiat._

    ```mermaid
    graph LR
        A[Optionals] --> B[Absence de valeur]
        A --> C[Type safety — nil explicite]
        A --> D[if let guard let]
    ```

<br>

---

## P

!!! note "Protocol"
    > Contrat définissant un ensemble de propriétés et méthodes qu'un type doit implémenter pour être considéré conforme.

    Swift est un langage "protocol-oriented" — les protocoles sont un mécanisme de polymorphisme plus flexible que l'héritage de classes. Un type peut se conformer à plusieurs protocoles, permettant une composition puissante.

    - **Protocol extensions :** permettent d'ajouter des implémentations par défaut à un protocole
    - **`some Protocol` :** type opaque — le type concret exact est caché au consommateur
    - **`any Protocol` :** existentiel — boîte générique pour tout type conforme

    ```swift title="Swift — Protocole avec extension"
    protocol Describable {
        var description: String { get }
    }

    // Extension : implémentation par défaut
    extension Describable {
        func printDescription() {
            print(description)
        }
    }

    struct User: Describable {
        var name: String
        var description: String { "Utilisateur : \(name)" }
    }
    ```

    _Les extensions de protocole offrent du comportement partagé sans héritage — c'est le "protocol-oriented programming"._

    ```mermaid
    graph LR
        A[Protocol] --> B[Contrat de type]
        A --> C[Protocol extensions]
        A --> D[some any — types opaques]
    ```

<br>

---

!!! note "Property Wrappers"
    > Mécanisme Swift permettant d'encapsuler la logique de stockage et d'accès d'une propriété dans un type réutilisable.

    Les property wrappers sont la magie derrière tout l'écosystème SwiftUI — `@State`, `@Binding`, `@Published`, `@AppStorage`, `@FetchRequest` sont tous des property wrappers. Ils permettent d'ajouter du comportement personnalisé autour d'une propriété de manière transparente.

    - **Syntaxe :** `@propertyWrapper struct MyWrapper<T> { var wrappedValue: T }`
    - **SwiftUI built-in :** `@State`, `@Binding`, `@StateObject`, `@ObservedObject`, `@EnvironmentObject`, `@AppStorage`
    - **Accès :** `$myProp` accède au `projectedValue` du wrapper (ex. `Binding` pour `@State`)

    ```mermaid
    graph LR
        A[Property Wrappers] --> B[State Management]
        A --> C[SwiftUI @State @Binding]
        A --> D[Logique réutilisable]
    ```

<br>

---

## S

!!! note "SPM"
    > Gestionnaire de paquets officiel Swift pour déclarer, résoudre et intégrer des dépendances dans les projets Xcode et Swift.

    Swift Package Manager est l'outil officiel d'Apple pour la gestion des dépendances. Il est intégré nativement dans Xcode depuis Xcode 11 et offre une alternative moderne à CocoaPods et Carthage.

    - **Acronyme :** Swift Package Manager
    - **Fichier de configuration :** `Package.swift` (DSL Swift, fortement typé)
    - **Intégration Xcode :** File → Add Package Dependencies → URL du package
    - **Alternatives historiques :** CocoaPods (plus populaire, écosystème plus large), Carthage

    ```mermaid
    graph LR
        A[SPM] --> B[Dépendances Swift]
        A --> C[Package.swift]
        A --> D[CocoaPods alternative]
    ```

<br>

---

!!! note "Struct vs. Class"
    > Distinction fondamentale en Swift entre les types valeur (struct) et les types référence (classe), avec des implications importantes sur la mémoire et le comportement.

    La règle générale Swift : préférer les structs. Elles sont copiées (value semantics), thread-safe par nature, et optimisées par le compilateur. Les classes sont nécessaires quand l'identité d'objet (référence partagée) ou l'héritage est requis.

    - **Struct :** value type, copié à l'affectation, pas d'héritage, `mutating` pour modifier
    - **Class :** reference type, partagé par référence, héritage possible, ARC pour la mémoire
    - **SwiftUI :** `View` = struct, `ViewModel` = class (`@Observable` ou `ObservableObject`)

    ```swift title="Swift — Value vs. Reference semantics"
    struct Point { var x: Int; var y: Int }
    var a = Point(x: 1, y: 2)
    var b = a     // b est une COPIE indépendante
    b.x = 99
    print(a.x)    // → 1 (a n'est pas modifié)

    class Node  { var value: Int = 0 }
    let n1 = Node(); let n2 = n1  // n2 pointe sur le MÊME objet
    n2.value = 42
    print(n1.value) // → 42 (partagé)
    ```

    _La sémantique de valeur des structs élimine les bugs de partage d'état implicite — raison pour laquelle SwiftUI utilise des structs pour les vues._

    ```mermaid
    graph LR
        A[Struct vs Class] --> B[Value type — copie]
        A --> C[Reference type — partagé]
        A --> D[ARC mémoire classes]
    ```

<br>

---

!!! note "SwiftData"
    > Framework Apple de persistance moderne (iOS 17+) utilisant des macros Swift pour remplacer et simplifier Core Data.

    SwiftData modernise la persistance sur iOS avec une syntaxe déclarative basée sur les macros Swift. Là où Core Data nécessitait un modèle XCDataModel graphique, SwiftData définit le schéma directement en code Swift, avec support natif de Swift Concurrency et SwiftUI.

    - **Introduit :** iOS 17, macOS 14 (WWDC 2023)
    - **Syntaxe :** `@Model class User { var name: String }` — le modèle est du code Swift pur
    - **SwiftUI :** `@Query` pour fetcher les données, `@Environment(\.modelContext)` pour le contexte
    - **Migration :** chemin de migration depuis Core Data officiel

    ```swift title="Swift — Modèle SwiftData"
    import SwiftData

    @Model
    class Task {
        var title: String
        var isDone: Bool = false
        var createdAt: Date = Date()

        init(title: String) { self.title = title }
    }
    ```

    _`@Model` génère automatiquement le schéma de persistance — plus besoin de fichier `.xcdatamodeld`._

    ```mermaid
    graph LR
        A[SwiftData] --> B[iOS 17 macros]
        A --> C[Core Data modernisé]
        A --> D[SwiftUI @Query]
    ```

<br>

---

!!! note "SwiftUI"
    > Framework Apple de création d'interfaces utilisateur déclaratif, multi-plateformes et réactif, introduit en 2019.

    SwiftUI représente un changement de paradigme fondamental — au lieu de décrire comment construire l'UI étape par étape (UIKit impératif), on décrit ce qu'elle doit afficher en fonction de l'état (déclaratif). L'UI se met automatiquement à jour quand l'état change.

    - **Introduit :** iOS 13, macOS 10.15 (WWDC 2019)
    - **Plateformes :** iOS, macOS, watchOS, tvOS, visionOS — un seul codebase
    - **Paradigme :** déclaratif (`View = f(state)`) vs. UIKit impératif
    - **Interopérabilité :** `UIViewRepresentable` et `UIViewControllerRepresentable` pour wraper UIKit

    ```swift title="Swift — Vue SwiftUI simple"
    struct ContentView: View {
        @State private var count = 0

        var body: some View {
            VStack(spacing: 16) {
                Text("Compteur : \(count)")
                    .font(.title)
                Button("Incrémenter") {
                    count += 1
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }
    ```

    _SwiftUI re-calcule `body` automatiquement chaque fois que `count` change — l'UI est toujours synchronisée avec l'état._

    ```mermaid
    graph LR
        A[SwiftUI] --> B[Déclaratif réactif]
        A --> C[Multi-plateformes Apple]
        A --> D[UIKit interop]
    ```

<br>

---

!!! note "Swift Concurrency"
    > Modèle de concurrence moderne de Swift basé sur async/await, actors et structured concurrency pour écrire du code asynchrone sûr.

    Swift Concurrency résout les problèmes historiques de GCD (Grand Central Dispatch) : data races, callback hell, gestion complexe des erreurs, annulation difficile. Il introduit un modèle structuré où les tâches ont une durée de vie explicite.

    - **Éléments :** `async/await`, `Task`, `TaskGroup`, `Actor`, `@Sendable`, `AsyncSequence`
    - **Structured concurrency :** les tâches enfants ne peuvent pas outliver leur parent
    - **Sendable :** protocole garantissant qu'un type peut être partagé entre concurrency domains sans data races

    ```swift title="Swift — Task et TaskGroup"
    // Lancer une tâche asynchrone
    Task {
        let data = try await fetchData()
        await MainActor.run { updateUI(data) }
    }

    // Exécution parallèle avec TaskGroup
    let results = try await withTaskGroup(of: Data.self) { group in
        group.addTask { try await fetchA() }
        group.addTask { try await fetchB() }
        return await group.reduce(into: []) { $0.append($1) }
    }
    ```

    _`TaskGroup` lance plusieurs tâches en parallèle et attend toutes leurs complétion — remplace efficacement `DispatchGroup`._

    ```mermaid
    graph LR
        A[Swift Concurrency] --> B[async await]
        A --> C[Actor isolation]
        A --> D[Structured concurrency]
    ```

<br>

---

## T

!!! note "TestFlight"
    > Plateforme Apple de distribution beta permettant de tester des applications iOS auprès d'utilisateurs internes et externes avant la mise en production.

    TestFlight est le pipeline entre développement et App Store. Il permet de distribuer des builds à des testeurs (jusqu'à 10 000 testeurs externes) qui reçoivent des mises à jour automatiques et peuvent soumettre des feedbacks directement depuis l'app.

    - **Testeurs internes :** membres de l'équipe App Store Connect (max 100)
    - **Testeurs externes :** invitation par email ou lien public (max 10 000)
    - **Durée build :** 90 jours maximum, puis suppression automatique

    ```mermaid
    graph LR
        A[TestFlight] --> B[Beta testing]
        A --> C[10000 testeurs externes]
        A --> D[Feedback intégré]
    ```

<br>

---

## U

!!! note "UIKit"
    > Framework Apple de création d'interfaces utilisateur impératif, fondement du développement iOS depuis 2008.

    UIKit est le framework historique du développement iOS — des millions d'applications en production en dépendent. Son modèle impératif (`viewDidLoad`, delegates, `IBOutlet`) contraste avec SwiftUI déclaratif. Il offre un contrôle granulaire sur chaque aspect de l'UI.

    - **Architecture :** MVC (Model-View-Controller) — pattern imposé par UIKit
    - **Composants clés :** `UIViewController`, `UIView`, `UITableView`, `UICollectionView`, `UINavigationController`
    - **Interface :** Storyboard (graphique) ou code pur (`programmatic UI`)
    - **Coexistence :** SwiftUI et UIKit peuvent s'utiliser ensemble via `UIViewControllerRepresentable`

    ```mermaid
    graph LR
        A[UIKit] --> B[MVC iOS historique]
        A --> C[UIViewController]
        A --> D[SwiftUI interop]
    ```

<br>

---

## X

!!! note "Xcode"
    > Environnement de développement intégré (IDE) officiel Apple pour développer des applications iOS, macOS, watchOS, tvOS et visionOS.

    Xcode est l'outil central de tout développeur Apple — il intègre l'éditeur de code Swift, le simulateur iOS, Instruments (profiling), le débogueur LLDB, le gestionnaire de packages SPM, et le processus de signature/distribution vers l'App Store.

    - **Composants :** éditeur Swift, Interface Builder, Simulator, Instruments, LLDB
    - **Build system :** compilateur Swift (swiftc), LLVM, linker
    - **Téléchargement :** gratuit sur le Mac App Store (macOS uniquement)
    - **Version :** chaque nouvelle version d'iOS requiert la dernière version Xcode pour soumettre

    ```mermaid
    graph LR
        A[Xcode] --> B[IDE Apple]
        A --> C[Simulateur iOS]
        A --> D[Instruments profiling]
    ```

<br>

---

!!! note "Xcode Instruments"
    > Suite d'outils de profiling et d'analyse de performance intégrée à Xcode pour diagnostiquer fuites mémoire, CPU et problèmes réseau.

    Instruments est le microscope du développeur iOS. Il permet d'analyser en temps réel la consommation CPU, la mémoire (et détecter les retain cycles via Leaks), les appels réseau, les I/O disque et les performances de rendu (Core Animation).

    - **Outils clés :** Time Profiler (CPU), Leaks (fuites mémoire), Allocations, Network, Core Animation
    - **Utilisation :** Product → Profile dans Xcode (⌘ + I)
    - **Conseil :** toujours profiler sur device physique, pas sur simulateur

    ```mermaid
    graph LR
        A[Instruments] --> B[Time Profiler CPU]
        A --> C[Leaks mémoire]
        A --> D[Core Animation rendu]
    ```

<br>

---

## Conclusion

!!! quote "Résumé — Développement Mobile (Swift / iOS)"
    Le développement iOS moderne repose sur trois piliers : le langage Swift (Optionals, Generics, Protocols, Closures, Swift Concurrency), les frameworks Apple (SwiftUI, UIKit, Core Data, SwiftData, Combine) et l'outillage ecosystème (Xcode, Instruments, TestFlight, App Store Connect, SPM). Maîtriser ce vocabulaire, c'est pouvoir naviguer entre les APIs Apple, comprendre la documentation officielle et collaborer efficacement avec des équipes mobile.

> Continuez avec le [Glossaire Cybersécurité](./cybersecurite.md) pour explorer les concepts de sécurité informatique, cryptographie et réponse aux incidents.
