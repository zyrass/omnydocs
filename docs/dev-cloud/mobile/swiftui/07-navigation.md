---
description: "SwiftUI Navigation : NavigationStack, NavigationLink, navigationDestination, NavigationPath et NavigationSplitView."
icon: lucide/book-open-check
tags: ["SWIFTUI", "NAVIGATION", "NAVIGATIONSTACK", "NAVIGATIONLINK", "DEEP-LINK"]
---

# Navigation — NavigationStack & SplitView

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Pile de Dossiers"
    Un guichetier d'administration empile les dossiers à traiter. Chaque nouveau dossier est posé sur la pile (push). Quand il est traité, il est retiré par le dessus (pop). Le guichetier ne peut traiter qu'un dossier à la fois — le plus haut de la pile. `NavigationStack` fonctionne exactement ainsi : une pile de vues. Pousser une vue (NavigationLink) l'affiche. Revenir (bouton Retour ou dismiss) la retire de la pile. L'ordre n'est jamais perdu, et on peut toujours remonter.

Depuis iOS 16, Apple a introduit `NavigationStack` pour remplacer l'ancien `NavigationView` — plus puissant, plus prévisible, et avec un état externalisé qui permet le deep linking.

<br>

---

## `NavigationStack` — La Racine de Navigation

`NavigationStack` gère une pile de vues. Vous y naviguez en avant avec `NavigationLink`, en arrière avec le bouton système ou `dismiss`.

```swift title="Swift (SwiftUI) — NavigationStack : structure de base"
import SwiftUI

// Structure de données - Identifiable requis pour les listes
struct Article: Identifiable {
    let id = UUID()
    let titre: String
    let auteur: String
    let contenu: String
    let tempsLecture: Int  // en minutes
}

// Données exemple
extension Article {
    static let exemples: [Article] = [
        Article(titre: "Introduction à SwiftUI",
                auteur: "Alice Martin",
                contenu: "SwiftUI est un framework déclaratif...",
                tempsLecture: 5),
        Article(titre: "Les Property Wrappers",
                auteur: "Bob Dupont",
                contenu: "Les property wrappers encapsulent...",
                tempsLecture: 8),
        Article(titre: "Async/Await en pratique",
                auteur: "Alice Martin",
                contenu: "La concurrence moderne avec Swift...",
                tempsLecture: 12),
    ]
}

// Vue racine avec NavigationStack
struct VueListeArticles: View {
    let articles = Article.exemples

    var body: some View {
        // NavigationStack : le container qui gère la pile
        NavigationStack {
            List(articles) { article in

                // NavigationLink(value:) — navigation par valeur (iOS 16+)
                // value : la valeur passée à .navigationDestination()
                NavigationLink(value: article) {
                    // Contenu du lien — la cellule visible dans la liste
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(article.titre)
                                .font(.headline)
                            Text(article.auteur)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Label("\(article.tempsLecture) min", systemImage: "clock")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 4)
                }
            }
            .navigationTitle("Articles")
            // .navigationDestination : décrit quelle vue afficher pour quel type de valeur
            .navigationDestination(for: Article.self) { article in
                VueDétailArticle(article: article)
            }
        }
    }
}

// Vue de détail — affichée quand on navigue vers un Article
struct VueDétailArticle: View {
    let article: Article

    // @Environment(\.dismiss) : ferme la vue actuelle (pop)
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(article.titre)
                    .font(.title)
                    .bold()

                HStack {
                    Label(article.auteur, systemImage: "person")
                    Spacer()
                    Label("\(article.tempsLecture) min", systemImage: "clock")
                }
                .font(.caption)
                .foregroundStyle(.secondary)

                Divider()

                Text(article.contenu)
                    .lineSpacing(6)
            }
            .padding()
        }
        .navigationTitle(article.titre)
        .navigationBarTitleDisplayMode(.inline)  // Titre compact dans la barre
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button("Partager") {
                    // Action de partage
                }
            }
        }
    }
}

#Preview {
    VueListeArticles()
}
```

<br>
![Architecture Navigation Stack SwiftUI](/assets/images/swiftui/swiftui-navigation-stack.png)
<br>

*`NavigationLink(value:)` (iOS 16+) est préféré à `NavigationLink(destination:)` car la destination est découplée du lien — elle est définie une seule fois dans `.navigationDestination()`. Cela améliore la testabilité et permet le deep linking.*

<br>

---

## Navigation Programmatique avec `NavigationPath`

`NavigationPath` est l'état de la pile de navigation — une file de valeurs. Vous pouvez la modifier directement pour naviguer, revenir, ou reconstruire une pile depuis un lien profond.

```swift title="Swift (SwiftUI) — NavigationPath : navigation programmatique"
import SwiftUI

// Types pour la navigation
struct Rubrique: Hashable {
    let nom: String
    let icône: String
}

struct SousRubrique: Hashable {
    let nom: String
    let couleur: Color
}

struct VueNavigationProgrammatique: View {

    // @State sur NavigationPath : l'état de la pile de navigation
    @State private var chemin = NavigationPath()

    let rubriques = [
        Rubrique(nom: "Swift", icône: "swift"),
        Rubrique(nom: "SwiftUI", icône: "desktopcomputer"),
        Rubrique(nom: "Vapor", icône: "server.rack"),
    ]

    var body: some View {
        NavigationStack(path: $chemin) {  // Passer $chemin pour le contrôle
            List(rubriques, id: \.nom) { rubrique in
                NavigationLink(value: rubrique) {
                    Label(rubrique.nom, systemImage: rubrique.icône)
                }
            }
            .navigationTitle("OmnyDocs")
            .navigationDestination(for: Rubrique.self) { rubrique in
                VueRubrique(rubrique: rubrique, chemin: $chemin)
            }
            .navigationDestination(for: SousRubrique.self) { sousRubrique in
                VueSousRubrique(sousRubrique: sousRubrique)
            }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    // Navigation programmatique : pousser directement une valeur
                    Button("Aller à Swift") {
                        chemin.append(Rubrique(nom: "Swift", icône: "swift"))
                    }
                }
            }
        }
    }
}

struct VueRubrique: View {
    let rubrique: Rubrique
    @Binding var chemin: NavigationPath

    let sousRubriques = [
        SousRubrique(nom: "Module 1", couleur: .blue),
        SousRubrique(nom: "Module 2", couleur: .indigo),
        SousRubrique(nom: "Module 3", couleur: .purple),
    ]

    var body: some View {
        List(sousRubriques, id: \.nom) { sr in
            NavigationLink(value: sr) {
                Label(sr.nom, systemImage: "doc.text")
                    .foregroundStyle(sr.couleur)
            }
        }
        .navigationTitle(rubrique.nom)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                // Retour à la racine : vider le chemin
                Button("Accueil") {
                    chemin = NavigationPath()  // Vide la pile → retour à la racine
                }
            }
        }
    }
}

struct VueSousRubrique: View {
    let sousRubrique: SousRubrique

    var body: some View {
        Text(sousRubrique.nom)
            .font(.largeTitle)
            .foregroundStyle(sousRubrique.couleur)
            .navigationTitle(sousRubrique.nom)
    }
}
```

*`chemin = NavigationPath()` vide instantanément toute la pile et ramène à la vue racine — parfait pour les boutons "Retour à l'accueil". `chemin.append(valeur)` navigue vers la vue correspondante sans interagir avec l'UI.*

<br>

---

## `NavigationSplitView` — iPad & Mac

Sur iPad et Mac, l'interface est souvent en deux ou trois colonnes. `NavigationSplitView` gère automatiquement cette mise en page.

```swift title="Swift (SwiftUI) — NavigationSplitView pour iPad et macOS"
import SwiftUI

// Modèle
struct Catégorie: Identifiable, Hashable {
    let id = UUID()
    let nom: String
    let icône: String
}

struct Leçon: Identifiable {
    let id = UUID()
    let titre: String
    let durée: String
    let catégorieId: UUID
}

struct VueSplitView: View {

    // Sélection dans la sidebar
    @State private var catégorieSelectionnée: Catégorie?
    @State private var leçonSelectionnée: Leçon?

    let catégories = [
        Catégorie(nom: "Swift", icône: "swift"),
        Catégorie(nom: "SwiftUI", icône: "square.stack"),
        Catégorie(nom: "Vapor", icône: "server.rack"),
    ]

    let leçons = [
        Leçon(titre: "Introduction", durée: "2h", catégorieId: UUID()),
        Leçon(titre: "Types et Variables", durée: "3h", catégorieId: UUID()),
    ]

    var body: some View {
        // Deux colonnes : sidebar + contenu
        NavigationSplitView {
            // Sidebar — liste des catégories
            List(catégories, selection: $catégorieSelectionnée) { cat in
                Label(cat.nom, systemImage: cat.icône)
                    .tag(cat)
            }
            .navigationTitle("Cours")

        } detail: {
            // Contenu — adapté selon la sélection
            if let catégorie = catégorieSelectionnée {
                Text("Contenu de \(catégorie.nom)")
                    .navigationTitle(catégorie.nom)
            } else {
                // Placeholder si rien n'est sélectionné (iPhone)
                ContentUnavailableView(
                    "Choisissez un cours",
                    systemImage: "sidebar.left",
                    description: Text("Sélectionnez une rubrique dans la liste")
                )
            }
        }
    }
}
```

*Sur iPhone, `NavigationSplitView` se comporte comme un `NavigationStack` standard. Sur iPad et Mac, il affiche les colonnes côte à côte. Une seule vue, deux comportements — sans code conditionnel.*

<br>

---

## Modificateurs de Navigation Essentiels

```swift title="Swift (SwiftUI) — Modificateurs de la barre de navigation"
import SwiftUI

struct VueAvecNavigation: View {
    @State private var recherche = ""

    var body: some View {
        NavigationStack {
            List {
                Text("Item 1")
                Text("Item 2")
            }
            // Titre de la navigation
            .navigationTitle("Ma Vue")

            // Style du titre : .large (par défaut), .inline, .automatic
            .navigationBarTitleDisplayMode(.large)

            // Barre de recherche intégrée (iOS 15+)
            .searchable(text: $recherche, prompt: "Rechercher...")

            // Boutons dans la barre de navigation
            .toolbar {
                // Position : .topBarLeading, .topBarTrailing, .bottomBar, .principal
                ToolbarItem(placement: .topBarLeading) {
                    Button("Filtrer") { }
                }

                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        // action
                    } label: {
                        Label("Ajouter", systemImage: "plus")
                    }
                }

                // Groupe de boutons — regroupés automatiquement
                ToolbarItemGroup(placement: .bottomBar) {
                    Button("Option 1") { }
                    Spacer()
                    Button("Option 2") { }
                }
            }
        }
    }
}
```

<br>

---

## Présentation Modale — `sheet`, `fullScreenCover`, `confirmationDialog`

La navigation "modale" affiche une vue par-dessus la vue courante (sans rejoindre la pile).

```swift title="Swift (SwiftUI) — Sheets, covers et dialogs modaux"
import SwiftUI

struct VuePrincipale: View {
    @State private var afficherSheet = false
    @State private var afficherFullScreen = false
    @State private var afficherDialog = false
    @State private var afficherAlert = false

    var body: some View {
        VStack(spacing: 20) {

            // Sheet : glisse depuis le bas, peut être partiel (iOS 16+)
            Button("Ouvrir Sheet") {
                afficherSheet = true
            }
            .sheet(isPresented: $afficherSheet) {
                VueSheet()
                    .presentationDetents([.medium, .large])  // iOS 16+ : hauteur partielle
                    .presentationDragIndicator(.visible)
            }

            // Full Screen Cover : toute la surface
            Button("Full Screen") {
                afficherFullScreen = true
            }
            .fullScreenCover(isPresented: $afficherFullScreen) {
                VuePleinEcran(afficher: $afficherFullScreen)
            }

            // Confirmation Dialog (action sheet modernisée)
            Button("Supprimer", role: .destructive) {
                afficherDialog = true
            }
            .confirmationDialog("Confirmer la suppression ?",
                                isPresented: $afficherDialog,
                                titleVisibility: .visible) {
                Button("Supprimer définitivement", role: .destructive) { }
                Button("Annuler", role: .cancel) { }
            }

            // Alert
            Button("Alerte") {
                afficherAlert = true
            }
            .alert("Erreur réseau", isPresented: $afficherAlert) {
                Button("Réessayer") { }
                Button("Annuler", role: .cancel) { }
            } message: {
                Text("Impossible de charger les données. Vérifiez votre connexion.")
            }
        }
        .padding()
    }
}

struct VueSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack {
            Text("Contenu de la Sheet")
                .font(.title2)
            Button("Fermer") { dismiss() }
                .buttonStyle(.bordered)
        }
        .padding()
    }
}

struct VuePleinEcran: View {
    @Binding var afficher: Bool

    var body: some View {
        ZStack {
            Color.indigo.ignoresSafeArea()
            VStack {
                Text("Plein écran").foregroundStyle(.white).font(.title)
                Button("Fermer") { afficher = false }
                    .buttonStyle(.bordered)
                    .tint(.white)
            }
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Application de notes avec navigation**

```swift title="Swift — Exercice 1 : liste de notes navigable"
// Créez une app de notes avec :
// - Une liste de notes (titre + date)
// - NavigationStack avec NavigationLink(value:)
// - Une vue de détail qui affiche le contenu complet
// - Un bouton "+" dans la toolbar pour créer une note
// - Un sheet de création (TextField pour titre et contenu)

struct Note: Identifiable, Hashable {
    let id = UUID()
    var titre: String
    var contenu: String
    var date: Date = .now
}

struct AppNotes: View {
    @State private var notes: [Note] = []
    @State private var afficherCréation = false

    var body: some View {
        // TODO : NavigationStack + List + NavigationLink(value:)
        // + .navigationDestination(for: Note.self)
        // + toolbar avec bouton + qui affiche le sheet
        NavigationStack {
            EmptyView()
        }
    }
}
```

**Exercice 2 — Navigation programmatique**

```swift title="Swift — Exercice 2 : wizard multi-étapes"
// Créez un wizard d'inscription en 3 étapes avec NavigationPath :
// Étape 1 : saisie du nom (bouton Suivant → push Étape 2)
// Étape 2 : saisie de l'email (bouton Suivant → push Étape 3)
// Étape 3 : résumé + confirmation (bouton Valider → vider le chemin)
// Bonus : bouton "Recommencer" dans la toolbar → retour à l'étape 1

enum ÉtapeInscription: Hashable {
    case email
    case confirmation(nom: String, email: String)
}

struct WizardInscription: View {
    @State private var chemin = NavigationPath()
    @State private var nom = ""

    var body: some View {
        NavigationStack(path: $chemin) {
            // TODO : Étape 1 — saisie du nom
            // .navigationDestination(for: ÉtapeInscription.self)
            EmptyView()
        }
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `NavigationStack` gère une pile de vues — pousser (NavigationLink), dépiler (bouton Retour ou dismiss). `NavigationLink(value:)` + `.navigationDestination(for:)` découple la destination du lien — la bonne pratique iOS 16+. `NavigationPath` externalise l'état de la pile — navigation programmatique, deep linking, retour à la racine avec `chemin = NavigationPath()`. `NavigationSplitView` produit un layout sidebar/detail pour iPad et Mac avec le même code qu'un NavigationStack sur iPhone. `.sheet()`, `.fullScreenCover()`, `.confirmationDialog()` et `.alert()` gèrent les présentations modales.

> Dans le module suivant, nous abordons les **Listes et Collections** — `List`, `ForEach`, swipe actions, sections, `EditButton`, et les grilles `LazyVGrid` pour les interfaces de données riches.

<br>
