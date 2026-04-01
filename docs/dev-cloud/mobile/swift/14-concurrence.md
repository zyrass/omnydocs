---
description: "Concurrence moderne Swift : async/await, Task, Actor, @MainActor, Sendable et le modèle de concurrence Swift 6."
icon: lucide/book-open-check
tags: ["SWIFT", "ASYNC", "AWAIT", "ACTOR", "SENDABLE", "SWIFT6", "CONCURRENCE"]
---

# Concurrence Moderne

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.1"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Chef et les Brigades"
    Un chef de cuisine qui travaillerait seul devrait attendre que le pain soit cuit avant de commencer les légumes. Un vrai restaurant fonctionne différemment : plusieurs brigades travaillent en parallèle, chacune spécialisée, et le chef coordonne sans attendre l'une pour commencer l'autre.

    `async/await` est ce chef. Il vous permet d'écrire du code asynchrone — qui attend des opérations longues (réseau, fichier, base de données) — de façon linéaire et lisible, sans callbacks imbriqués. Les `Actor` sont les brigades isolées : chaque Actor gère son état sans interférer avec les autres. Et `Sendable` est le contrat de sécurité : il garantit qu'une valeur peut traverser une frontière de concurrence sans provoquer de race condition.

Swift 5.5 (2021) a introduit ce modèle. **Swift 6 (2024) l'a rendu obligatoire par défaut** — c'est pourquoi comprendre `Sendable` est indispensable aujourd'hui.

<br>

---

## `async` / `await`

```swift title="Swift - async/await : code asynchrone lisible"
import Foundation

func chargerProfil(userId: Int) async throws -> String {
    let url = URL(string: "https://api.example.com/users/\(userId)")!
    // await : suspend sans bloquer le thread
    let (données, réponse) = try await URLSession.shared.data(from: url)

    guard let http = réponse as? HTTPURLResponse,
          http.statusCode == 200 else {
        throw ErreurRéseau.httpErreur(code: 404, message: "Not Found")
    }

    return String(data: données, encoding: .utf8) ?? ""
}

func chargerPosts(pour utilisateur: String) async throws -> [String] {
    try await Task.sleep(for: .milliseconds(500))
    return ["Post 1", "Post 2", "Post 3"]
}

// Code séquentiel lisible — pas de callbacks imbriqués
func afficherProfil(userId: Int) async {
    do {
        let nom = try await chargerProfil(userId: userId)
        let posts = try await chargerPosts(pour: nom)
        print("\(nom) a \(posts.count) posts")
    } catch {
        print("Erreur : \(error.localizedDescription)")
    }
}
```

<br>

---

## `Task` — Lancer une Tâche Asynchrone

```swift title="Swift - Task pour démarrer du code async depuis un contexte synchrone"
// Task simple
Task {
    await afficherProfil(userId: 42)
}

// Task avec priorité
Task(priority: .userInitiated) {
    let données = try? await chargerProfil(userId: 42)
    print(données ?? "Échec")
}

// Annuler une Task
let tâche = Task {
    try await Task.sleep(for: .seconds(5))
    print("Terminé")   // N'imprimera pas si annulé
}
tâche.cancel()

// Vérifier l'annulation dans une longue tâche
func longueOpération() async throws {
    for i in 1...1000 {
        try Task.checkCancellation()
        print("Étape \(i)")
    }
}
```

<br>

---

## Parallélisme avec `async let`

```swift title="Swift - async let : deux opérations en parallèle"
// Séquentiel : 1s + 1s = 2s au total
func chargerSequentiel() async throws {
    let profil = try await chargerProfil(userId: 42)
    let posts  = try await chargerPosts(pour: profil)
    print("\(profil) : \(posts.count) posts")
}

// Parallèle avec async let : max(1s, 1s) = 1s au total
func chargerParallèle() async throws {
    async let profil = chargerProfil(userId: 42)
    async let posts  = chargerPosts(pour: "utilisateur")

    // await sur les deux : on attend que les DEUX soient terminés
    let (nom, listePosts) = try await (profil, posts)
    print("\(nom) : \(listePosts.count) posts")
}
```

<br>

---

## `withTaskGroup` — Parallélisme Dynamique

```swift title="Swift - withTaskGroup pour un nombre variable de tâches"
func chargerTousDonnées(userIds: [Int]) async throws -> [String] {
    try await withThrowingTaskGroup(of: String.self) { groupe in
        for id in userIds {
            groupe.addTask {
                try await chargerProfil(userId: id)
            }
        }

        var profils: [String] = []
        for try await profil in groupe {
            profils.append(profil)
        }
        return profils
    }
}
```

<br>

---

## `Actor` — Protection de l'État Concurrent

```swift title="Swift - Actor : isolation automatique de l'état"
actor CompteurPartagé {
    private var valeur: Int = 0

    func incrémenter() { valeur += 1 }
    func valeurActuelle() -> Int { valeur }
}

let compteur = CompteurPartagé()

// Accès à un actor : toujours avec await
Task {
    await compteur.incrémenter()
    let v = await compteur.valeurActuelle()
    print("Valeur : \(v)")
}

// Cache thread-safe avec Actor générique
actor Cache<Clé: Hashable, Valeur> {
    private var stockage: [Clé: Valeur] = [:]

    func lire(_ clé: Clé) -> Valeur? { stockage[clé] }
    func écrire(_ valeur: Valeur, pour clé: Clé) { stockage[clé] = valeur }
}
```

<br>

---

## `@MainActor` — Thread Principal

```swift title="Swift - @MainActor pour les mises à jour UI"
@MainActor
class ViewModelArticle: ObservableObject {
    @Published var articles: [String] = []
    @Published var estEnChargement = false

    func charger() async {
        estEnChargement = true
        do {
            let (données, _) = try await URLSession.shared.data(
                from: URL(string: "https://api.example.com/articles")!
            )
            articles = ["Article 1", "Article 2"]
        } catch {
            print(error)
        }
        estEnChargement = false
    }
}
```

<br>

---

## `Sendable` — La Sécurité de Concurrence Swift 6

`Sendable` est un protocol marqueur : il certifie qu'une valeur peut être **transmise entre des contextes de concurrence** (entre Tasks, entre Actors, entre threads) sans provoquer de race condition.

C'est la nouveauté majeure de **Swift 6 (2024)** : le compilateur vérifie et **impose** `Sendable` par défaut. Un code qui compilait en Swift 5 peut maintenant produire des erreurs de concurrence en Swift 6.

=== ":simple-swift: Swift"

    ```swift title="Swift - Sendable : comprendre qui est conforme"
    import Foundation

    // Les value types (struct avec propriétés Sendable) sont automatiquement Sendable
    struct Message: Sendable {
        let id: Int
        let contenu: String
        let dateEnvoi: Date
    }

    // Les enums avec associated values Sendable sont Sendable
    enum StatutCommande: Sendable {
        case enAttente
        case expédiée(numéroSuivi: String)
        case livrée(dateEffective: Date)
    }

    // Les classes NE sont PAS automatiquement Sendable
    // car leurs propriétés mutables sont accessibles par plusieurs threads
    class ConfigurationApp {
        var thème: String = "clair"
        // Cette classe n'est PAS Sendable — le compilateur le refuse
    }

    // Pour rendre une class Sendable : la marquer @unchecked Sendable
    // et gérer la synchronisation manuellement (via un lock ou un Actor)
    final class ConfigurationSécurisée: @unchecked Sendable {
        private var thème: String = "clair"
        private let verrou = NSLock()

        func lireThème() -> String {
            verrou.withLock { thème }
        }

        func définirThème(_ nouveau: String) {
            verrou.withLock { thème = nouveau }
        }
    }
    ```

    ```swift title="Swift - Erreurs Sendable en Swift 6"
    // Swift 6 : active la vérification stricte de concurrence par défaut
    // Dans Xcode : Build Settings → Swift Language Version → Swift 6

    class UtilisateurNonSendable {
        var nom: String = "Alice"
    }

    let utilisateur = UtilisateurNonSendable()

    Task {
        // ERREUR Swift 6 :
        // Capture of 'utilisateur' with non-sendable type 'UtilisateurNonSendable'
        // in a @Sendable closure
        print(utilisateur.nom)
    }

    // Solution 1 : capturer une valeur Sendable
    let nom = utilisateur.nom   // String est Sendable
    Task {
        print(nom)   // OK
    }

    // Solution 2 : utiliser un Actor
    actor UtilisateurActor {
        var nom: String = "Alice"
    }

    // Solution 3 : Marquer @unchecked Sendable et gérer la synchronisation
    ```

    ```swift title="Swift - Sendable avec async/await"
    // Les fonctions async s'exécutent potentiellement sur plusieurs threads
    // Les paramètres et valeurs de retour doivent être Sendable

    // OK : String est Sendable
    func traiterNom(_ nom: String) async -> String {
        return nom.uppercased()
    }

    // OK : struct Sendable
    func traiterMessage(_ message: Message) async -> String {
        return "[\(message.id)] \(message.contenu)"
    }

    // Passing non-Sendable type across actor boundaries
    // Si ConfigurationApp n'est pas Sendable, ce code échoue en Swift 6
    func mettreAJourConfig(_ config: ConfigurationSécurisée) async {
        await MainActor.run {
            print(config.lireThème())   // OK car ConfigurationSécurisée est @unchecked Sendable
        }
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Pas d'équivalent (single-threaded)"
    // JavaScript est single-threaded — les race conditions n'existent pas
    // pour le code synchrone ordinaire.
    // Web Workers utilisent des messages (pas de mémoire partagée)
    // donc pas de concept de Sendable nécessaire.
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Pas d'équivalent (isolation par requête)"
    <?php
    // PHP traditionnel : chaque requête HTTP est un processus isolé
    // Pas de mémoire partagée entre requêtes = Sendable non nécessaire
    // Swoole/ReactPHP introduisent des problématiques similaires
    ```

=== ":simple-python: Python"

    ```python title="Python - threading.Lock (gestion manuelle)"
    import threading

    # Python : le GIL protège partiellement, mais pas pour tous les cas
    class ConfigurationSécurisée:
        def __init__(self):
            self._theme = "clair"
            self._verrou = threading.Lock()

        def lire_theme(self) -> str:
            with self._verrou:
                return self._theme

        def définir_theme(self, nouveau: str):
            with self._verrou:
                self._theme = nouveau
    ```

<br>

### Types naturellement Sendable

```swift title="Swift - Inventaire des types Sendable"
// Sendable automatiquement (conformance synthétisée) :
// - Tous les types value (struct, enum) dont les propriétés sont Sendable
// - Int, Double, String, Bool, Date, URL
// - Array<T>, Dictionary<K,V>, Optional<T> si T, K, V sont Sendable
// - Tuples de valeurs Sendable
// - Fonctions sans captures (les closures @Sendable)

// NON Sendable par défaut :
// - Classes (reference types mutables)
// - Closures qui capturent des références non-Sendable

// Vérifier si un type est Sendable :
func exiger<T: Sendable>(_ valeur: T) { _ = valeur }

exiger("texte")     // OK
exiger(42)          // OK
exiger(Message(id: 1, contenu: "test", dateEnvoi: .now))  // OK
// exiger(ConfigurationApp())  // ERREUR : not Sendable
```

<br>

### Migration Swift 5 → Swift 6

```swift title="Swift - Stratégie de migration progressive"
// Étape 1 : Activer les avertissements Swift 6 dans Swift 5
// Build Settings → Strict Concurrency Checking → Complete

// Étape 2 : Marquer les types évidents
struct RéponseAPI: Codable, Sendable {
    let data: [String]
}

// Étape 3 : Pour les classes existantes non-critiques : @unchecked Sendable
// comme déclaration d'intention ("je gère la synchronisation moi-même")
final class LegacyService: @unchecked Sendable {
    // La synchronisation est garantie par l'architecture,
    // même si le compilateur ne peut pas le vérifier
}

// Étape 4 : Isoler l'état mutable dans des Actors
actor ServiceCache {
    private var cache: [String: Data] = [:]
    // Plus besoin de @unchecked Sendable — l'Actor garantit l'isolation
}
```

<br>

---

## Résumé des Outils de Concurrence

| Outil | Usage |
| --- | --- |
| `async func` | Déclarer une fonction asynchrone |
| `await` | Attendre le résultat sans bloquer le thread |
| `Task { }` | Lancer du code async depuis un contexte synchrone |
| `async let` | Démarrer plusieurs opérations en parallèle |
| `withTaskGroup` | Parallélisme sur un nombre variable de tâches |
| `actor` | Protéger un état partagé contre les race conditions |
| `@MainActor` | Garantir l'exécution sur le thread principal |
| `Sendable` | Certifier qu'une valeur est sûre entre threads |
| `@unchecked Sendable` | Déclarer la conformance avec synchronisation manuelle |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `async/await` transforme le code asynchrone en code séquentiel lisible. `Task` lance du code asynchrone depuis un contexte synchrone. `async let` démarre des opérations en parallèle. `Actor` sérialise les accès à l'état partagé. `@MainActor` garantit les mises à jour UI sur le thread principal. `Sendable` est le protocol de sécurité de concurrence de Swift 6 — il certifie qu'une valeur peut traverser une frontière de thread sans race condition. En Swift 6, la vérification `Sendable` est activée par défaut — les value types (struct, enum) sont naturellement conformes, les classes doivent être adaptées.

> Dans le dernier module, nous aborderons **ARC et la Gestion Mémoire** — le mécanisme de libération automatique de la mémoire et les pièges des cycles de rétention dans les closures.

<br>