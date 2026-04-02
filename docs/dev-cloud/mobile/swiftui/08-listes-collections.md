---
description: "SwiftUI List, ForEach, sections, swipe actions, EditButton, LazyVGrid pour les interfaces de données riches et performantes."
icon: lucide/book-open-check
tags: ["SWIFTUI", "LIST", "FOREACH", "GRID", "SWIPE", "COLLECTIONS"]
---

# Listes & Collections

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Tableau de Bord de l'Aéroport"
    Un tableau des départs d'aéroport affiche des dizaines de vols. Il ne crée pas 200 afficheurs physiques pour 200 vols — il en crée peut-être 20 (ceux visibles) et les remplace dynamiquement quand vous faites défiler. C'est le principe des vues `Lazy` en SwiftUI. `ForEach` génère des vues à la demande. `LazyVStack` et `LazyVGrid` ne créent les cellules que quand elles entrent dans la zone visible — essentiel pour les longues listes.

`List` est le composant de liste le plus utilisé dans les applications iOS. Il fournit les chevrons, les swipe, les sections et l'apparence native — avec très peu de code.

<br>

---

## `List` — Le Container de Liste Standard

```swift title="Swift (SwiftUI) — List : de la liste simple à la liste configurable"
import SwiftUI

struct Tâche: Identifiable {
    let id = UUID()
    var titre: String
    var estFaite: Bool = false
    var priorité: Priorité = .normale

    enum Priorité: String, CaseIterable {
        case haute  = "Haute"
        case normale = "Normale"
        case basse  = "Basse"

        var couleur: Color {
            switch self {
            case .haute:  return .red
            case .normale: return .orange
            case .basse:   return .green
            }
        }
    }
}

struct VueListeTâches: View {

    @State private var tâches: [Tâche] = [
        Tâche(titre: "Configurer Xcode", estFaite: true,  priorité: .haute),
        Tâche(titre: "Apprendre @State",  priorité: .haute),
        Tâche(titre: "Créer premier projet", priorité: .normale),
        Tâche(titre: "Lire la documentation", priorité: .basse),
        Tâche(titre: "Faire les exercices", priorité: .normale),
    ]

    var body: some View {
        NavigationStack {
            // List avec ForEach implicite (données Identifiable)
            List($tâches) { $tâche in
                // $tâche : Binding vers chaque tâche (pour Toggle)
                HStack {
                    // Toggle directement sur la propriété via Binding
                    Toggle(isOn: $tâche.estFaite) {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(tâche.titre)
                                .strikethrough(tâche.estFaite) // Barré si faite
                                .foregroundStyle(tâche.estFaite ? .secondary : .primary)

                            // Badge de priorité
                            Text(tâche.priorité.rawValue)
                                .font(.caption2)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(tâche.priorité.couleur.opacity(0.15))
                                .foregroundStyle(tâche.priorité.couleur)
                                .clipShape(Capsule())
                        }
                    }
                    .toggleStyle(.checkmark)  // Apparence checkbox
                }
            }
            .navigationTitle("Mes Tâches")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}
```

*`List($tâches) { $tâche in }` — le `$` devant `tâches` et chaque `tâche` dans la closure crée des `Binding` sur chaque élément. C'est ce qui permet à `Toggle(isOn: $tâche.estFaite)` de modifier directement le tableau.*

<br>

---

## Swipe Actions — Actions Glissées

```swift title="Swift (SwiftUI) — .swipeActions : actions personnalisées"
import SwiftUI

struct VueTâchesAvecSwipe: View {

    @State private var tâches = [
        Tâche(titre: "Module 01 — Introduction"),
        Tâche(titre: "Module 02 — Vues"),
        Tâche(titre: "Module 03 — Layout"),
        Tâche(titre: "Module 04 — @State"),
    ]

    var body: some View {
        NavigationStack {
            List {
                ForEach($tâches) { $tâche in
                    HStack {
                        Image(systemName: tâche.estFaite ? "checkmark.circle.fill" : "circle")
                            .foregroundStyle(tâche.estFaite ? .green : .gray)
                        Text(tâche.titre)
                            .foregroundStyle(tâche.estFaite ? .secondary : .primary)
                    }
                    // Actions glissées vers la gauche (leading)
                    .swipeActions(edge: .leading, allowsFullSwipe: true) {
                        Button {
                            withAnimation { tâche.estFaite.toggle() }
                        } label: {
                            Label(
                                tâche.estFaite ? "Défaire" : "Terminer",
                                systemImage: tâche.estFaite ? "xmark.circle" : "checkmark.circle"
                            )
                        }
                        .tint(.green)
                    }
                    // Actions glissées vers la droite (trailing)
                    .swipeActions(edge: .trailing) {
                        Button(role: .destructive) {
                            withAnimation {
                                tâches.removeAll { $0.id == tâche.id }
                            }
                        } label: {
                            Label("Supprimer", systemImage: "trash")
                        }
                    }
                }
            }
            .navigationTitle("Tâches")
        }
    }
}
```

*`allowsFullSwipe: true` permet de déclencher la première action en glissant complètement sans relâcher. `role: .destructive` colore automatiquement l'action en rouge — cohérent avec les HIG Apple.*

<br>

---

## Sections — Organiser en Groupes

```swift title="Swift (SwiftUI) — List avec sections et en-têtes"
import SwiftUI

struct Contact: Identifiable {
    let id = UUID()
    let prénom: String
    let nom: String
    let initiale: Character
}

struct ListeContacts: View {

    let contacts = [
        Contact(prénom: "Alice", nom: "Martin", initiale: "A"),
        Contact(prénom: "André", nom: "Dupont", initiale: "A"),
        Contact(prénom: "Bob",   nom: "Bernard", initiale: "B"),
        Contact(prénom: "Claire", nom: "Bruno",  initiale: "C"),
        Contact(prénom: "David", nom: "Lambert", initiale: "D"),
    ]

    // Grouper par initiale
    var contactsParInitiale: [Character: [Contact]] {
        Dictionary(grouping: contacts, by: { $0.initiale })
    }

    // Clés triées
    var initiales: [Character] {
        contactsParInitiale.keys.sorted()
    }

    var body: some View {
        NavigationStack {
            List {
                ForEach(initiales, id: \.self) { initiale in
                    // Section avec en-tête de lettre
                    Section(header: Text(String(initiale)).textCase(.uppercase)) {
                        ForEach(contactsParInitiale[initiale] ?? []) { contact in
                            // Ligne de contact
                            HStack(spacing: 12) {
                                // Avatar avec initiale
                                Circle()
                                    .fill(Color.indigo)
                                    .frame(width: 40, height: 40)
                                    .overlay {
                                        Text(String(contact.prénom.prefix(1)))
                                            .foregroundStyle(.white)
                                            .font(.headline)
                                    }

                                VStack(alignment: .leading) {
                                    Text("\(contact.prénom) \(contact.nom)")
                                        .font(.headline)
                                }
                            }
                        }
                    }
                }
            }
            .listStyle(.insetGrouped)  // Style iOS moderne (groupé avec coins arrondis)
            .navigationTitle("Contacts")
        }
    }
}
```

*`listStyle` change l'apparence globale : `.plain` (sans séparateurs), `.inset` (marges internes), `.insetGrouped` (style iOS moderne — le plus courant), `.sidebar` (pour les sidebars iPad).*

<br>

---

## `ForEach` — Générer des Vues Dynamiquement

`ForEach` est distinct de `List` — il génère des vues dans n'importe quel container.

```swift title="Swift (SwiftUI) — ForEach : les différentes formes"
import SwiftUI

struct DémoForEach: View {

    let fruits = ["Pomme", "Poire", "Cerise", "Mangue"]
    let couleurs: [Color] = [.red, .green, .blue, .orange, .purple]

    var body: some View {
        VStack(spacing: 20) {

            // ForEach avec identifiant explicite
            HStack {
                ForEach(fruits, id: \.self) { fruit in
                    Text(fruit)
                        .font(.caption)
                        .padding(6)
                        .background(Color.mint.opacity(0.2))
                        .cornerRadius(6)
                }
            }

            // ForEach avec indice
            HStack {
                ForEach(Array(couleurs.enumerated()), id: \.offset) { index, couleur in
                    Circle()
                        .fill(couleur)
                        .frame(width: 30, height: 30)
                        .overlay { Text("\(index)").font(.caption).foregroundStyle(.white) }
                }
            }

            // ForEach sur une plage
            HStack {
                ForEach(1...5, id: \.self) { nombre in
                    Image(systemName: "\(nombre).circle.fill")
                        .foregroundStyle(.indigo)
                        .font(.title2)
                }
            }
        }
    }
}
```

<br>

---

## Édition de Liste — `onDelete` & `onMove`

```swift title="Swift (SwiftUI) — Rendre une liste éditable"
import SwiftUI

struct ListeÉditable: View {

    @State private var éléments = ["Swift", "SwiftUI", "Vapor", "Xcode", "Instruments"]
    @State private var modeÉdition = EditMode.inactive

    var body: some View {
        NavigationStack {
            List {
                ForEach(éléments, id: \.self) { élément in
                    Text(élément)
                }
                // Swipe pour supprimer individuel
                .onDelete { indexSet in
                    éléments.remove(atOffsets: indexSet)
                }
                // Drag pour réordonner
                .onMove { source, destination in
                    éléments.move(fromOffsets: source, toOffset: destination)
                }
            }
            .navigationTitle("Outils")
            .environment(\.editMode, $modeÉdition)  // Injecter le mode d'édition
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    // EditButton : bascule automatiquement entre "Modifier" et "OK"
                    EditButton()
                }
                ToolbarItem(placement: .topBarLeading) {
                    Button("Ajouter") {
                        éléments.append("Nouvel outil \(éléments.count + 1)")
                    }
                }
            }
        }
    }
}
```

*`EditButton()` est un bouton système qui bascule entre les modes actif et inactif automatiquement. En mode édition, la liste affiche les poignées de réordonnement et les boutons de suppression.*

<br>

---

## `LazyVStack` pour les Longues Listes

Pour les très longues listes au sein d'un `ScrollView` (quand `List` n'est pas adapté), préférez `LazyVStack`.

```swift title="Swift (SwiftUI) — LazyVStack vs VStack pour les performances"
import SwiftUI

struct ListeMilleÉléments: View {

    var body: some View {
        ScrollView {
            // LazyVStack : les vues sont créées seulement quand elles entrent dans
            // la zone visible. Idéal pour les collections de 100+ éléments.
            LazyVStack(spacing: 0, pinnedViews: [.sectionHeaders]) {

                Section {
                    ForEach(1...500, id: \.self) { index in
                        HStack {
                            Text("Élément \(index)")
                                .padding()
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundStyle(.secondary)
                                .padding()
                        }
                        .background(Color(.systemBackground))
                        Divider()
                    }
                } header: {
                    // pinnedViews: l'en-tête reste visible pendant le défilement
                    Text("500 éléments")
                        .font(.headline)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(Color(.systemGray6))
                }
            }
        }
    }
}

// À éviter pour les longues listes :
struct ListeNonOptimisée: View {
    var body: some View {
        ScrollView {
            // VStack crée TOUTES les vues immédiatement — lent pour 500+ éléments
            VStack {
                ForEach(1...500, id: \.self) { index in
                    Text("Élément \(index)")
                }
            }
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Gestionnaire de contacts**

```swift title="Swift — Exercice 1 : liste de contacts avec swipe et sections"
// Créez une liste de contacts avec :
// - Modèle Contact (id, nom, prénom, favori: Bool, catégorie: String)
// - Séparés en sections par catégorie (Famille, Amis, Travail)
// - Swipe gauche : marquer favori (étoile jaune / grise)
// - Swipe droite : supprimer (destructive)
// - Tri : favoris en premiers dans chaque section

struct Contact2: Identifiable, Hashable {
    let id = UUID()
    var nom: String
    var prénom: String
    var estFavori: Bool = false
    var catégorie: String  // "Famille" | "Amis" | "Travail"
}

struct GestionnaireContacts: View {
    @State private var contacts: [Contact2] = [
        // TODO : ajouter 6+ contacts avec catégories variées
    ]

    var body: some View {
        // TODO
        EmptyView()
    }
}
```

**Exercice 2 — Liste réordonnée avec persistance**

```swift title="Swift — Exercice 2 : liste réordonnée avec @AppStorage"
// Créez une liste ordonnée de priorités :
// - Affichée dans List avec EditButton
// - Les priorités peuvent être réordonnées (onMove)
// - L'ordre est sauvegardé dans UserDefaults via @AppStorage
// Indice : serialiser les priorités en [String] JSON pour @AppStorage

struct ListePrioritésOrdrées: View {
    // @AppStorage pour sauvegarder l'ordre entre les lancements
    // Clé : "priorités_ordre"
    @State private var priorités = ["Urgent", "Important", "Normal", "Faible"]

    var body: some View {
        // TODO
        EmptyView()
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `List` fournit une liste iOS native avec swipe, sélection et sections — formatage automatique, apparence système. `ForEach` génère des vues dans n'importe quel container — `List`, `VStack`, `HStack`, `LazyVGrid`. `.swipeActions()` ajoute des actions glissées — `.leading` pour les actions positives, `.trailing` pour les destructives. `Section` organise la liste en groupes visuels avec en-têtes. `.onDelete` et `.onMove` activent la suppression et le réordonnement en mode édition. `LazyVStack` dans un `ScrollView` est plus performant que `VStack` pour les collections de 100+ éléments.

> Dans le module suivant, nous abordons le chargement de **données asynchrones** dans SwiftUI — `.task { }`, les états de chargement, la gestion d'erreurs et le pattern ViewModel async complet avec une API réelle.

<br>
