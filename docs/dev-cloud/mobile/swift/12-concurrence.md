---
description: "Concurrence moderne Swift : async/await, Task, Actor, @MainActor et gestion structurée de la concurrence."
icon: lucide/book-open-check
tags: ["SWIFT", "ASYNC", "AWAIT", "ACTOR", "CONCURRENCE", "TASK"]
---

# Concurrence Moderne

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="4-5 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique - Le Chef et les Brigades"
    Un chef de cuisine qui travaillerait seul devrait attendre que le pain soit cuit avant de commencer les légumes. C'est l'exécution séquentielle — une tâche à la fois. Un vrai restaurant fonctionne différemment : plusieurs brigades travaillent en parallèle, chaque brigade est spécialisée, et le chef coordonne l'ensemble sans attendre l'une pour commencer l'autre.

    `async/await` en Swift, c'est ce chef. Il vous permet d'écrire du code asynchrone — qui attend des opérations longues (réseau, fichier, base de données) — de façon linéaire et lisible, sans les callbacks imbriqués de JavaScript ou les continuations complexes. Et les `Actor` sont les brigades isolées : chaque Actor gère son propre état sans interférer avec les autres.

Swift 5.5 (2021) a introduit un modèle de concurrence structurée qui rivalise avec les meilleures implémentations des autres langages modernes.

<br>

---

## Le Problème Avant async/await

=== ":simple-swift: Swift"

    ```swift title="Swift - L'ancienne approche : callbacks imbriqués (à éviter)"
    // Avant Swift 5.5 : closures de completion (callback hell)
    func chargerProfil(userId: Int, completion: @escaping (Result<String, Error>) -> Void) {
        DispatchQueue.global().async {
            // Simulation d'une requête réseau
            DispatchQueue.main.async {
                completion(.success("Alice"))
            }
        }
    }

    func chargerPosts(pour utilisateur: String, completion: @escaping ([String]) -> Void) {
        DispatchQueue.global().async {
            DispatchQueue.main.async {
                completion(["Post 1", "Post 2"])
            }
        }
    }

    // Utilisation : pyramide de callbacks difficile à lire et maintenir
    chargerProfil(userId: 42) { résultat in
        switch résultat {
        case .success(let nom):
            chargerPosts(pour: nom) { posts in
                print("\(nom) a \(posts.count) posts")
                // Et si on doit charger encore autre chose ? Un niveau de plus...
            }
        case .failure(let erreur):
            print(erreur)
        }
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - callback hell puis Promise puis async/await"
    // Callback hell (historique)
    chargerProfil(42, (erreur, profil) => {
        if (erreur) { console.error(erreur); return; }
        chargerPosts(profil.nom, (erreur, posts) => {
            if (erreur) { console.error(erreur); return; }
            console.log(`${profil.nom} : ${posts.length} posts`);
        });
    });

    // Promise (meilleur, mais chainé)
    chargerProfil(42)
        .then(profil => chargerPosts(profil.nom))
        .then(posts => console.log(posts))
        .catch(console.error);

    // async/await (idiomatique moderne — très proche de Swift)
    async function afficherProfil(userId) {
        const profil = await chargerProfil(userId);
        const posts = await chargerPosts(profil.nom);
        console.log(`${profil.nom} : ${posts.length} posts`);
    }
    ```

<br>

---

## `async` / `await` — La Syntaxe Moderne

```swift title="Swift - async/await : code asynchrone lisible"
import Foundation

// async : cette fonction est asynchrone (peut être suspendue)
// throws : peut aussi lancer une erreur (async throws est courant)
func chargerProfil(userId: Int) async throws -> String {
    // await : suspend l'exécution ici jusqu'à la réponse
    // Le thread n'est PAS bloqué — il peut faire autre chose pendant l'attente
    let url = URL(string: "https://api.example.com/users/\(userId)")!
    let (données, réponse) = try await URLSession.shared.data(from: url)

    guard let http = réponse as? HTTPURLResponse, http.statusCode == 200 else {
        throw ErreurRéseau.httpErreur(code: 404, message: "Not Found")
    }

    return String(data: données, encoding: .utf8) ?? ""
}

func chargerPosts(pour utilisateur: String) async throws -> [String] {
    // Simulation
    try await Task.sleep(nanoseconds: 500_000_000)  // 0.5s de délai simulé
    return ["Post 1", "Post 2", "Post 3"]
}

// Utilisation : code SÉQUENTIEL lisible
func afficherProfil(userId: Int) async {
    do {
        // Exécution séquentielle : chargerProfil termine avant chargerPosts
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

```swift title="Swift - Task pour démarrer du code asynchrone"
// Task lance une tâche asynchrone depuis un contexte synchrone
// Nécessaire pour appeler du code async depuis viewDidLoad, init, etc.

// Task simple
Task {
    await afficherProfil(userId: 42)
}

// Task avec priorité
Task(priority: .userInitiated) {
    let données = try? await chargerProfil(userId: 42)
    print(données ?? "Echec")
}

// Task.detached : tâche sans contexte parent (rare)
Task.detached(priority: .background) {
    // S'exécute sans hériter du contexte de la Task parente
}

// Annuler une Task
let tâche = Task {
    try await Task.sleep(nanoseconds: 5_000_000_000)
    print("Terminé")   // N'imprimera pas si annulé avant
}

tâche.cancel()   // Annule la tâche

// Vérifier l'annulation dans une longue tâche
func longueOpération() async throws {
    for i in 1...1000 {
        // Vérifier régulièrement si la tâche a été annulée
        try Task.checkCancellation()
        print("Étape \(i)")
    }
}
```

<br>

---

## Parallélisme avec `async let`

```swift title="Swift - async let pour exécuter plusieurs opérations en parallèle"
// Séquentiel : chargerProfil PUIS chargerPosts — total ~2s si chacun prend 1s
func chargerSequentiel() async throws {
    let profil = try await chargerProfil(userId: 42)    // Attend 1s
    let posts = try await chargerPosts(pour: profil)    // Attend encore 1s
    // Total : ~2s
    print("\(profil) : \(posts.count) posts")
}

// Parallèle avec async let : les deux démarrent SIMULTANÉMENT — total ~1s
func chargerParallèle() async throws {
    // async let démarre immédiatement sans attendre
    async let profil = chargerProfil(userId: 42)
    async let posts = chargerPosts(pour: "utilisateur")

    // await ici : on attend que LES DEUX soient terminés
    let (nom, listePosts) = try await (profil, posts)
    // Total : ~1s (le temps du plus long des deux)
    print("\(nom) : \(listePosts.count) posts")
}
```

<br>

---

## `withTaskGroup` — Parallélisme Dynamique

```swift title="Swift - withTaskGroup pour un nombre variable de tâches"
func chargerToutesDonnées(userIds: [Int]) async throws -> [String] {
    // withTaskGroup crée un groupe de tâches qui s'exécutent en parallèle
    try await withThrowingTaskGroup(of: String.self) { groupe in
        // Lancer une tâche par userId
        for id in userIds {
            groupe.addTask {
                try await chargerProfil(userId: id)
            }
        }

        // Collecter les résultats au fur et à mesure qu'ils arrivent
        var profils: [String] = []
        for try await profil in groupe {
            profils.append(profil)
        }
        return profils
    }
}

// Toutes les requêtes s'exécutent en parallèle
// plutôt que séquentiellement une par une
let profils = try await chargerToutesDonnées(userIds: [1, 2, 3, 4, 5])
```

<br>

---

## `Actor` — Protection de l'État Concurrent

Un `Actor` est un type référence (comme une class) dont l'accès à l'état interne est **sérialisé** automatiquement par Swift. Il garantit qu'un seul appelant à la fois peut modifier l'état interne — éliminant les race conditions sans verrous manuels.

=== ":simple-swift: Swift"

    ```swift title="Swift - Actor pour l'isolation de l'état concurrent"
    // actor : déclare un type avec isolation automatique
    actor CompteurPartagé {
        private var valeur: Int = 0

        // Méthode accessible depuis n'importe quel contexte asynchrone
        func incrémenter() {
            valeur += 1
        }

        func valeurActuelle() -> Int {
            valeur
        }
    }

    let compteur = CompteurPartagé()

    // Accès à un actor : toujours avec await
    Task {
        await compteur.incrémenter()
        let v = await compteur.valeurActuelle()
        print("Valeur : \(v)")
    }

    // Exemple concret : cache thread-safe
    actor Cache<Clé: Hashable, Valeur> {
        private var stockage: [Clé: Valeur] = [:]

        func lire(_ clé: Clé) -> Valeur? {
            stockage[clé]
        }

        func écrire(_ valeur: Valeur, pour clé: Clé) {
            stockage[clé] = valeur
        }

        func supprimer(_ clé: Clé) {
            stockage.removeValue(forKey: clé)
        }
    }
    ```

=== ":simple-javascript: JavaScript"

    ```js title="JavaScript - Pas d'équivalent (single-threaded)"
    // JavaScript est single-threaded — les race conditions n'existent pas
    // pour le code synchrone.
    // Pour les Web Workers (vrai parallélisme) : communication par messages,
    // pas de mémoire partagée — approche différente des Actors Swift.

    // Les Promises et async/await JS ne créent pas de vrais threads parallèles
    // mais de la concurrence coopérative sur un seul thread.
    ```

=== ":simple-php: PHP"

    ```php title="PHP - Pas d'équivalent natif (un processus = une requête)"
    <?php
    // PHP traditionnel : chaque requête HTTP est un processus isolé
    // Pas de mémoire partagée entre requêtes = pas de race conditions
    // Pour la concurrence : Swoole, ReactPHP, ou processus séparés
    ```

<br>

---

## `@MainActor` — Opérations sur le Thread Principal

```swift title="Swift - @MainActor pour les mises à jour d'interface"
// En iOS : toutes les mises à jour d'interface doivent se faire sur le thread principal
// @MainActor garantit l'exécution sur le thread principal

@MainActor
class ViewModelArticle: ObservableObject {
    @Published var articles: [String] = []
    @Published var estEnChargement = false
    @Published var erreur: String?

    // Toutes les méthodes sont automatiquement sur le thread principal
    func charger() async {
        estEnChargement = true
        erreur = nil

        do {
            // La requête réseau se fait sur un autre thread (via URLSession)
            let données = try await URLSession.shared.data(from: URL(string: "https://api.example.com/articles")!).0
            // Le retour de await revient automatiquement sur le MainActor
            articles = ["Article 1", "Article 2"]   // Mise à jour UI : thread principal
        } catch {
            erreur = error.localizedDescription
        }

        estEnChargement = false
    }
}

// Appeler une méthode MainActor depuis un contexte non-MainActor
func tâcheEnArrièrePlan() async {
    // await pour passer sur le MainActor
    await MainActor.run {
        print("Exécuté sur le thread principal")
    }
}
```

<br>

---

## Résumé des Outils de Concurrence

| Outil | Usage |
| --- | --- |
| `async func` | Déclarer une fonction asynchrone |
| `await` | Attendre le résultat d'une fonction async |
| `Task { }` | Lancer du code async depuis un contexte synchrone |
| `async let` | Démarrer plusieurs opérations en parallèle |
| `withTaskGroup` | Parallélisme sur un nombre variable de tâches |
| `actor` | Protéger un état partagé contre les race conditions |
| `@MainActor` | Garantir l'exécution sur le thread principal |
| `Task.checkCancellation()` | Vérifier et respecter l'annulation |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `async/await` transforme le code asynchrone en code séquentiel lisible — sans callbacks imbriqués. `await` suspend la fonction sans bloquer le thread. `Task` lance du code asynchrone depuis un contexte synchrone. `async let` démarre des opérations en parallèle. `withTaskGroup` gère un parallélisme dynamique. `Actor` sérialise automatiquement les accès à l'état partagé — éliminant les race conditions sans verrous manuels. `@MainActor` garantit les mises à jour d'interface sur le thread principal.

> Dans le dernier module, nous aborderons **ARC et la Gestion Mémoire** — le mécanisme qui libère automatiquement la mémoire en Swift et les pièges des cycles de rétention dans les closures.

<br>