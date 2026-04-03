---
description: "SwiftUI persistance : @AppStorage, UserDefaults, SwiftData (iOS 17+), @Model, @Query et modelContainer."
icon: lucide/book-open-check
tags: ["SWIFTUI", "PERSISTENCE", "SWIFTDATA", "APPSTORAGE", "USERDEFAULTS"]
---

# Persistance

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Trois Archives"
    Une bibliothèque a trois types de stockage : un post-it à l'accueil pour la note urgente (UserDefaults/AppStorage — rapide, petit), une armoire pour les dossiers courants (SwiftData/Core Data — structuré, local), et une salle des archives pour tout l'historique (base de données distante). Chaque besoin a son outil. Stocker une préférence utilisateur dans SwiftData est une complexité inutile — `@AppStorage` suffit. Stocker 10 000 articles de blog dans UserDefaults est une catastrophe de performance — SwiftData est conçu pour ça.

Ce module couvre les solutions de persistance locale par ordre de complexité croissante.

<br>

---

## `@AppStorage` — Préférences Simples

`@AppStorage` est un property wrapper SwiftUI qui lit et écrit directement dans `UserDefaults`. La vue se met à jour automatiquement quand la valeur change.

```swift title="Swift (SwiftUI) — @AppStorage : préférences utilisateur réactives"
import SwiftUI

struct PréférencesApp: View {

    // @AppStorage("clé") : lit/écrit dans UserDefaults.standard
    @AppStorage("modeSombre")        private var modeSombre = false
    @AppStorage("taillePolice")      private var taillePolice: Double = 16.0
    @AppStorage("langueInterface")   private var langueInterface = "fr"
    @AppStorage("nombreDémarrages")  private var nombreDémarrages = 0
    @AppStorage("nomUtilisateur")    private var nomUtilisateur = ""

    let langues = [("fr", "Français"), ("en", "English"), ("es", "Español")]

    var body: some View {
        NavigationStack {
            Form {
                Section("Apparence") {
                    Toggle("Mode sombre", isOn: $modeSombre)

                    VStack(alignment: .leading) {
                        Text("Taille de police : \(Int(taillePolice)) pt")
                        Slider(value: $taillePolice, in: 12...24, step: 1)
                    }
                }

                Section("Langue") {
                    Picker("Langue", selection: $langueInterface) {
                        ForEach(langues, id: \.0) { code, nom in
                            Text(nom).tag(code)
                        }
                    }
                }

                Section("Compte") {
                    TextField("Votre prénom", text: $nomUtilisateur)
                }

                Section("Statistiques") {
                    LabeledContent("Démarrages") {
                        Text("\(nombreDémarrages)")
                            .foregroundStyle(.secondary)
                    }

                    Button("Réinitialiser les statistiques") {
                        nombreDémarrages = 0
                    }
                    .foregroundStyle(.red)
                }
            }
            .navigationTitle("Préférences")
            .preferredColorScheme(modeSombre ? .dark : .light)
            .onAppear {
                nombreDémarrages += 1  // Incrémenté à chaque lancement
            }
        }
    }
}

// Dans l'environnement d'une app — synchronisation entre vues
struct VuePrincipale: View {
    @AppStorage("nomUtilisateur") private var nom = ""

    var body: some View {
        Text("Bonjour, \(nom.isEmpty ? "Visiteur" : nom) !")
        // Se met à jour automatiquement si nom change dans une autre vue
    }
}
```

*`@AppStorage` est limité aux types primitifs : `Bool`, `Int`, `Double`, `String`, `URL`, et les types `Codable` sérialisés en JSON. Pour les données structurées complexes, utilisez SwiftData.*

<br>

---

## SwiftData — Persistance Structurée (iOS 17+)

SwiftData est la solution moderne d'Apple pour la persistance locale (introduite en iOS 17). Il remplace Core Data avec une API déclarative et Swift-native.

!!! warning "SwiftData nécessite iOS 17+"
    SwiftData n'est disponible que depuis iOS 17, macOS 14 et watchOS 10. Pour iOS 16, utilisez Core Data ou une autre solution. Ce cours utilise SwiftData comme référence moderne — l'encadré Core Data est fourni en annexe pour référence.

```swift title="Swift (SwiftUI) — @Model : définir un modèle SwiftData"
import SwiftUI
import SwiftData

// ═══════════════════════════════════════════════
// MODÈLE SWIFTDATA — @Model remplace @Entity CoreData
// ═══════════════════════════════════════════════

// @Model : macro qui transforme la classe en modèle persistant
// - Ajoute automatiquement Codable, Hashable, Identifiable
// - Génère le schéma de base de données
@Model
final class NotePersistante {
    var titre: String
    var contenu: String
    var dateCreation: Date
    var estÉpinglée: Bool
    var catégorie: String

    // Relation : une Note peut avoir plusieurs Tags
    @Relationship(deleteRule: .cascade)
    var tags: [TagPersistant] = []

    init(titre: String, contenu: String = "", catégorie: String = "Général") {
        self.titre = titre
        self.contenu = contenu
        self.dateCreation = .now
        self.estÉpinglée = false
        self.catégorie = catégorie
    }
}

@Model
final class TagPersistant {
    var nom: String
    var couleurHex: String

    init(nom: String, couleurHex: String = "#6366F1") {
        self.nom = nom
        self.couleurHex = couleurHex
    }
}
```

<br>

### `@Query` et `modelContainer` — Lire et Injecter

```swift title="Swift (SwiftUI) — @Query pour lire les données persistantes"
import SwiftUI
import SwiftData

// ═══════════════════════════════════════════════
// CONFIGURATION — App.swift : injecter le container
// ═══════════════════════════════════════════════

@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup {
            NoteListView()
        }
        // .modelContainer injecte le container dans toutes les vues
        // SwiftData crée automatiquement la base de données SQLite
        .modelContainer(for: [NotePersistante.self, TagPersistant.self])
    }
}

// ═══════════════════════════════════════════════
// VUE — lecture et écriture avec @Query
// ═══════════════════════════════════════════════

struct NoteListView: View {

    // @Query : requête réactive — se met à jour automatiquement
    // Sort : ordre des résultats
    @Query(sort: \.dateCreation, order: .reverse)
    private var notes: [NotePersistante]

    // modelContext : permet d'insérer, modifier, supprimer
    @Environment(\.modelContext) private var contexte

    @State private var afficherAjout = false
    @State private var recherche = ""

    // Filtrage en Swift (non-optimisé pour les très grands ensembles)
    var notesFiltres: [NotePersistante] {
        guard !recherche.isEmpty else { return notes }
        return notes.filter {
            $0.titre.localizedCaseInsensitiveContains(recherche)
        }
    }

    var body: some View {
        NavigationStack {
            List {
                ForEach(notesFiltres) { note in
                    NavigationLink(value: note) {
                        NoteCellule(note: note)
                    }
                }
                .onDelete(perform: supprimer)
            }
            .navigationTitle("Notes (\(notes.count))")
            .navigationDestination(for: NotePersistante.self) { note in
                NoteEditView(note: note)
            }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Ajouter", systemImage: "plus") {
                        afficherAjout = true
                    }
                }
                ToolbarItem(placement: .topBarLeading) {
                    EditButton()
                }
            }
            .sheet(isPresented: $afficherAjout) {
                AjouterNoteView()
            }
            .searchable(text: $recherche)
        }
    }

    // Supprimer depuis les indices (onDelete)
    func supprimer(at indexSet: IndexSet) {
        for index in indexSet {
            // contexte.delete : marque la note pour suppression
            contexte.delete(notesFiltres[index])
        }
        // La suppression est automatiquement persistée
    }
}

struct NoteCellule: View {
    let note: NotePersistante

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                if note.estÉpinglée {
                    Image(systemName: "pin.fill")
                        .font(.caption)
                        .foregroundStyle(.orange)
                }
                Text(note.titre)
                    .font(.headline)
                    .lineLimit(1)
            }
            Text(note.contenu.isEmpty ? "Aucun contenu" : note.contenu)
                .font(.caption)
                .foregroundStyle(.secondary)
                .lineLimit(2)
            Text(note.dateCreation, style: .relative)
                .font(.caption2)
                .foregroundStyle(.tertiary)
        }
        .padding(.vertical, 2)
    }
}
```

<br>

### Ajouter et Modifier des Données

```swift title="Swift (SwiftUI) — Insérer et modifier des données SwiftData"
import SwiftUI
import SwiftData

// Créer une nouvelle note
struct AjouterNoteView: View {
    @Environment(\.modelContext) private var contexte
    @Environment(\.dismiss) private var dismiss

    @State private var titre = ""
    @State private var contenu = ""
    @State private var catégorie = "Général"

    let catégories = ["Général", "Travail", "Personnel", "Idées"]

    var body: some View {
        NavigationStack {
            Form {
                TextField("Titre", text: $titre)
                Picker("Catégorie", selection: $catégorie) {
                    ForEach(catégories, id: \.self) { Text($0) }
                }
                TextField("Contenu...", text: $contenu, axis: .vertical)
                    .lineLimit(5...10)
            }
            .navigationTitle("Nouvelle note")
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Annuler") { dismiss() }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Enregistrer") {
                        // Insérer le nouveau modèle dans le contexte
                        let note = NotePersistante(titre: titre, contenu: contenu, catégorie: catégorie)
                        contexte.insert(note)   // Persisté automatiquement
                        dismiss()
                    }
                    .disabled(titre.isEmpty)
                }
            }
        }
    }
}

// Modifier une note existante
struct NoteEditView: View {
    @Bindable var note: NotePersistante   // @Bindable pour éditer les @Model directement

    var body: some View {
        Form {
            Section("Titre") {
                TextField("Titre", text: $note.titre)  // Modifie directement le @Model
            }
            Section("Contenu") {
                TextField("Contenu...", text: $note.contenu, axis: .vertical)
                    .lineLimit(5...)
            }
            Section("Options") {
                Toggle("Épingler", isOn: $note.estÉpinglée)
            }
        }
        .navigationTitle("Modifier")
        // Les modifications sont sauvegardées automatiquement
        // Pas de bouton "Sauvegarder" nécessaire
    }
}

#Preview {
    NoteListView()
        .modelContainer(for: NotePersistante.self, inMemory: true)
        // inMemory: true — données en mémoire uniquement pour les previews
}
```

*`@Bindable` fonctionne avec les modèles `@Model` de SwiftData — exactement comme avec `@Observable`. Les modifications dans les TextFields sont automatiquement persistées sans appel explicite à save.*

<br>
![Schéma Relationnel SwiftData Base de Données](/assets/images/swiftui/swiftui-swiftdata-schema.png)
<br>

<br>

---

## `@Query` avec Filtres et Tri Complexes

```swift title="Swift (SwiftUI) — @Query avec prédicats et tris complexes"
import SwiftUI
import SwiftData

struct NotesÉpingléesView: View {

    // Filtre directement dans @Query — plus performant que filtrer dans Swift
    @Query(
        filter: #Predicate<NotePersistante> { $0.estÉpinglée == true },
        sort: \.dateCreation,
        order: .reverse
    )
    private var notesÉpinglées: [NotePersistante]

    var body: some View {
        List(notesÉpinglées) { note in
            Text(note.titre)
        }
        .navigationTitle("Épinglées (\(notesÉpinglées.count))")
    }
}

// @Query dynamique — créé dans init avec un paramètre
struct NotesCatégorieView: View {
    let catégorie: String

    // @Query avec prédicat dynamique (construit dans init)
    @Query private var notes: [NotePersistante]

    init(catégorie: String) {
        self.catégorie = catégorie
        // Filtre dynamique basé sur le paramètre
        _notes = Query(
            filter: #Predicate<NotePersistante> { $0.catégorie == catégorie },
            sort: \.dateCreation,
            order: .reverse
        )
    }

    var body: some View {
        List(notes) { note in
            Text(note.titre)
        }
        .navigationTitle(catégorie)
    }
}
```

*`#Predicate` est une macro Swift qui compile le prédicat en une requête SQL optimisée — bien plus performant que filtrer un tableau Swift pour les grandes collections.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Gestionnaire de préférences**

```swift title="Swift — Exercice 1 : écran de préférences avec @AppStorage"
// Créez un écran de préférences avec @AppStorage :
// - Thème : Clair / Sombre / Système (Picker)
// - Langue : Français / English / Español
// - Taille police : 12-24 (Stepper)
// - Notifications : Toggle
// - Première utilisation : Bool (afficher onboarding si true)
// Toutes les préférences persistent entre les lancements

struct ÉcranPréférences: View {
    // TODO : @AppStorage pour chaque préférence
    var body: some View { EmptyView() }
}
```

**Exercice 2 — Journal personnel SwiftData**

```swift title="Swift — Exercice 2 : journal avec SwiftData"
// Créez une application de journal avec SwiftData :
// @Model JournalEntry : titre, contenu, dateCreation, humeur (enum), estFavori
// - Liste des entrées, triées par date décroissante
// - Filtre par humeur (Picker dans la toolbar)
// - Ajouter, modifier, supprimer
// - Preview avec inMemory: true

enum Humeur: String, Codable, CaseIterable {
    case excellent = "😊 Excellent"
    case bien      = "🙂 Bien"
    case neutre    = "😐 Neutre"
    case moyen     = "😕 Moyen"
    case difficile = "😔 Difficile"
}

@Model
class JournalEntry {
    // TODO
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `@AppStorage("clé")` lie une variable SwiftUI à `UserDefaults` — idéal pour les préférences simples (`Bool`, `String`, `Double`). SwiftData (iOS 17+) est la solution moderne pour les données structurées : `@Model` définit la structure persistante, `@Query` lit les données avec filtres et tri en SQL optimisé, `contexte.insert()` et `contexte.delete()` modifient les données, la persistance est automatique. `@Bindable` sur un `@Model` permet l'édition directe via les bindings SwiftUI. `.modelContainer(for:)` injecte le container dans toute l'application. Pour les previews, `inMemory: true` évite de polluer la vraie base de données.

> Dans le module suivant, nous verrons le **Cycle de Vie de l'Application** — `@main`, `App`, `Scene`, `WindowGroup`, `onAppear`, `onDisappear`, `ScenePhase` et comment initialiser et nettoyer les ressources au bon moment.

<br>
