---
description: "SwiftUI données asynchrones : .task{}, async/await dans les vues, états de chargement, gestion d'erreurs et pattern ViewModel async."
icon: lucide/book-open-check
tags: ["SWIFTUI", "ASYNC", "AWAIT", "TASK", "RÉSEAU", "VIEWMODEL"]
---

# Données Asynchrones

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Serveur et les Commandes"
    Un serveur de restaurant ne bloque pas toute la salle pendant qu'un plat se prépare. Il prend la commande, passe en cuisine, et continue de servir les autres tables. Quand le plat est prêt, il revient le servir. `async/await` fonctionne ainsi : `.task { }` passe la commande réseau, SwiftUI continue de maintenir l'interface réactive, et quand les données arrivent (await), la vue se met à jour. L'interface ne "gèle" jamais.

Ce module connecte le cours Swift (module 14 — Concurrence) à SwiftUI. Vous savez écrire des fonctions `async` — ici, vous apprenez à les orchestrer dans le cycle de vie d'une vue.

<br>

---

## `.task { }` — Le Modificateur de Chargement SwiftUI

`.task { }` lance une tâche `async` liée au cycle de vie de la vue : démarrée quand la vue apparaît, annulée automatiquement quand elle disparaît.

```swift title="Swift (SwiftUI) — .task : chargement automatique lié au cycle de vie"
import SwiftUI

// Modèle — conforme à Codable pour le décodage JSON
struct Post: Identifiable, Codable {
    let id: Int
    let title: String
    let body: String
    let userId: Int
}

struct VuePostsSimple: View {

    @State private var posts: [Post] = []
    @State private var estEnChargement = false

    var body: some View {
        NavigationStack {
            Group {
                if estEnChargement {
                    ProgressView("Chargement...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    List(posts) { post in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(post.title)
                                .font(.headline)
                                .lineLimit(2)
                            Text(post.body)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                                .lineLimit(3)
                        }
                        .padding(.vertical, 4)
                    }
                }
            }
            .navigationTitle("Posts")
            // .task : lancé quand la vue apparaît, annulé quand elle disparaît
            .task {
                await chargerPosts()
            }
        }
    }

    func chargerPosts() async {
        estEnChargement = true
        defer { estEnChargement = false }  // Toujours exécuté, même en cas d'erreur

        do {
            let url = URL(string: "https://jsonplaceholder.typicode.com/posts")!
            let (données, _) = try await URLSession.shared.data(from: url)
            // Décodage sur le thread courant — @MainActor garantit l'UI
            posts = try JSONDecoder().decode([Post].self, from: données)
        } catch {
            print("Erreur : \(error)")
        }
    }
}
```

*`.task { }` est préféré à `.onAppear { Task { } }` car il gère automatiquement l'annulation — si l'utilisateur quitte la vue avant la fin du chargement, URLSession est annulée proprement.*

<br>

---

## Pattern ViewModel Async — Architecture Complète

Le pattern recommandé sépare la logique de chargement dans un ViewModel.

```swift title="Swift (SwiftUI) — ViewModel async avec états de chargement"
import SwiftUI

// Enum représentant tous les états possibles du chargement
enum ÉtatChargement<T> {
    case inactif            // Pas encore démarré
    case chargement         // En cours
    case succès(T)          // Données reçues
    case erreur(String)     // Erreur avec message
}

// ViewModel — responsable du chargement et de l'état
@MainActor  // Toutes les modifications de @Published sur le thread principal
class ViewModelPosts: ObservableObject {

    @Published var état: ÉtatChargement<[Post]> = .inactif

    // La fonction async : peut être annulée par .task{}
    func charger() async {
        état = .chargement

        do {
            let url = URL(string: "https://jsonplaceholder.typicode.com/posts")!

            // try await : suspension sans blocage du thread principal
            let (données, réponse) = try await URLSession.shared.data(from: url)

            // Vérifier le code HTTP
            guard let http = réponse as? HTTPURLResponse,
                  (200...299).contains(http.statusCode) else {
                état = .erreur("Le serveur a retourné une erreur")
                return
            }

            let posts = try JSONDecoder().decode([Post].self, from: données)
            état = .succès(posts)

        } catch is CancellationError {
            // Tâche annulée (utilisateur a quitté la vue) — pas d'erreur affichée
            état = .inactif
        } catch {
            état = .erreur(error.localizedDescription)
        }
    }

    func recharger() async {
        await charger()
    }
}

// Vue — observe l'état et affiche la vue adaptée
struct VuePostsAvecViewModel: View {

    @StateObject private var viewModel = ViewModelPosts()

    var body: some View {
        NavigationStack {
            contenuPourÉtat
                .navigationTitle("Posts API")
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button {
                            Task { await viewModel.recharger() }
                        } label: {
                            Image(systemName: "arrow.clockwise")
                        }
                    }
                }
                .task {
                    // .task annule automatiquement si la vue disparaît
                    await viewModel.charger()
                }
        }
    }

    // Vue adaptée selon l'état — computed property pour garder body lisible
    @ViewBuilder
    var contenuPourÉtat: some View {
        switch viewModel.état {
        case .inactif:
            Text("Prêt à charger")
                .foregroundStyle(.secondary)

        case .chargement:
            VStack(spacing: 16) {
                ProgressView()
                    .scaleEffect(1.5)
                Text("Chargement en cours...")
                    .foregroundStyle(.secondary)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)

        case .succès(let posts):
            ListePosts(posts: posts)

        case .erreur(let message):
            ContentUnavailableView {
                Label("Erreur de chargement", systemImage: "wifi.slash")
            } description: {
                Text(message)
            } actions: {
                Button("Réessayer") {
                    Task { await viewModel.charger() }
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }
}

struct ListePosts: View {
    let posts: [Post]

    var body: some View {
        List(posts) { post in
            VStack(alignment: .leading, spacing: 4) {
                Text(post.title.capitalized)
                    .font(.headline)
                    .lineLimit(1)
                Text(post.body)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }
            .padding(.vertical, 4)
        }
    }
}

#Preview {
    VuePostsAvecViewModel()
}
```

<br>
![Séquence de Récupération de Données Async](/assets/images/swiftui/swiftui-async-fetch-sequence.png)
<br>

*`@MainActor` sur le ViewModel garantit que toutes les modifications de `@Published` s'exécutent sur le thread principal — nécessaire car SwiftUI ne peut être mis à jour que depuis le thread principal.*

<br>

---

## Chargement avec `.task(id:)` — Rechargement Conditionnel

`.task(id:)` relance la tâche chaque fois que la valeur de `id` change.

```swift title="Swift (SwiftUI) — .task(id:) pour recharger selon un paramètre"
import SwiftUI

struct VuePostsParUtilisateur: View {

    @State private var utilisateurId: Int = 1
    @State private var posts: [Post] = []
    @State private var chargement = false

    var body: some View {
        NavigationStack {
            VStack {
                // Picker pour changer d'utilisateur
                Picker("Utilisateur", selection: $utilisateurId) {
                    ForEach(1...5, id: \.self) { id in
                        Text("Utilisateur \(id)").tag(id)
                    }
                }
                .pickerStyle(.segmented)
                .padding()

                if chargement {
                    ProgressView()
                } else {
                    List(posts) { post in
                        Text(post.title)
                    }
                }
            }
            .navigationTitle("Posts utilisateur \(utilisateurId)")
            // task(id:) : relancé chaque fois que utilisateurId change
            // La tâche précédente est annulée automatiquement avant la relance
            .task(id: utilisateurId) {
                chargement = true
                defer { chargement = false }

                do {
                    let url = URL(string: "https://jsonplaceholder.typicode.com/posts?userId=\(utilisateurId)")!
                    let (données, _) = try await URLSession.shared.data(from: url)
                    posts = try JSONDecoder().decode([Post].self, from: données)
                } catch {
                    posts = []
                }
            }
        }
    }
}
```

*`.task(id: utilisateurId)` annule la requête précédente avant d'en démarrer une nouvelle — évite les race conditions où une réponse lente d'ancienne requête "écrase" une réponse rapide de la nouvelle.*

<br>

---

## Chargement Paginé — `AsyncSequence`

```swift title="Swift (SwiftUI) — Simulation d'un chargement paginé infini"
import SwiftUI

struct VueChargementInfini: View {

    @State private var posts: [Post] = []
    @State private var page = 1
    @State private var aEncore = true
    @State private var chargement = false

    var body: some View {
        NavigationStack {
            List {
                ForEach(posts) { post in
                    VStack(alignment: .leading) {
                        Text(post.title).font(.headline).lineLimit(1)
                        Text(post.body).font(.caption).foregroundStyle(.secondary).lineLimit(2)
                    }
                    // Déclencher le chargement de la page suivante
                    // quand le dernier élément devient visible
                    .task {
                        if post.id == posts.last?.id && aEncore && !chargement {
                            await chargerPage()
                        }
                    }
                }

                if chargement {
                    HStack {
                        Spacer()
                        ProgressView()
                        Spacer()
                    }
                    .listRowSeparator(.hidden)
                }
            }
            .navigationTitle("Feed")
            .task {
                await chargerPage()  // Première page
            }
        }
    }

    func chargerPage() async {
        guard !chargement, aEncore else { return }
        chargement = true
        defer { chargement = false }

        do {
            let url = URL(string: "https://jsonplaceholder.typicode.com/posts?_page=\(page)&_limit=10")!
            let (données, _) = try await URLSession.shared.data(from: url)
            let nouveauxPosts = try JSONDecoder().decode([Post].self, from: données)

            if nouveauxPosts.isEmpty {
                aEncore = false  // Plus de données
            } else {
                posts.append(contentsOf: nouveauxPosts)
                page += 1
            }
        } catch {
            aEncore = false
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Météo avec API publique**

```swift title="Swift — Exercice 1 : appel API Open-Meteo"
// Utilisez l'API gratuite Open-Meteo :
// https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current=temperature_2m,wind_speed_10m
//
// Créez :
// - Un modèle Codable pour la réponse
// - Un ViewModel avec @MainActor et état ÉtatChargement<MétéoRéponse>
// - Une vue avec spinner, données affichées, et bouton refresh

struct MétéoRéponse: Codable {
    struct Current: Codable {
        let temperature_2m: Double    // °C
        let wind_speed_10m: Double    // km/h
    }
    let current: Current
}

@MainActor
class MétéoViewModel: ObservableObject {
    @Published var état: ÉtatChargement<MétéoRéponse> = .inactif
    // TODO : implémenter charger()
}
```

**Exercice 2 — Recherche en temps réel**

```swift title="Swift — Exercice 2 : recherche avec debounce"
// Implémentez une recherche en temps réel :
// - Un TextField pour la requête
// - Lancer la recherche 500ms après que l'utilisateur arrête de taper (debounce)
// - Utiliser .task(id: termeRecherche) pour annuler les requêtes précédentes
// - Afficher les résultats de https://jsonplaceholder.typicode.com/posts?title_like=TERME

struct VueRecherche: View {
    @State private var termeRecherche = ""
    @State private var résultats: [Post] = []

    var body: some View {
        NavigationStack {
            List(résultats) { post in
                Text(post.title)
            }
            .searchable(text: $termeRecherche)
            // TODO : .task(id: termeRecherche) avec sleep de debounce
            .navigationTitle("Recherche")
        }
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `.task { }` lance une tâche `async` liée au cycle de vie de la vue — démarrée à l'apparition, annulée à la disparition. `.task(id:)` relance la tâche chaque fois que l'identifiant change — idéal pour les filtres et la recherche, avec annulation automatique de la tâche précédente. Le pattern ViewModel avec `ÉtatChargement<T>` (inactif/chargement/succès/erreur) produit des interfaces claires et maintenables. `@MainActor` sur le ViewModel garantit que les mises à jour de `@Published` s'exécutent sur le thread principal. `ContentUnavailableView` est le composant système standard pour les états vides et d'erreur.

> Dans le module suivant, nous abordons les **Formulaires et la Validation** — `Form`, `Section`, `TextField`, `Toggle`, `Picker`, `DatePicker` et la validation en temps réel avec feedback utilisateur.

<br>
