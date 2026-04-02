---
description: "SwiftUI ViewModifier, @ViewBuilder et extension View : créer des modificateurs réutilisables et des composants de bibliothèque."
icon: lucide/book-open-check
tags: ["SWIFTUI", "VIEWMODIFIER", "VIEWBUILDER", "EXTENSION", "COMPOSANTS"]
---

# ViewModifier & Extensions

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Boîte à Outils du Designer"
    Un designer graphique professionnel ne recrée pas chaque fois un bouton depuis zéro. Il a une bibliothèque de composants — chaque type de bouton, chaque carte, chaque badge — définis une seule fois et réutilisés partout. Si la couleur de la marque change, il modifie un seul composant et tout le projet se met à jour. Les `ViewModifier` et les extensions `View` sont cette bibliothèque de composants pour SwiftUI. Définissez votre style une fois, appliquez-le à l'infini.

Ce module est le **quatrième pivot** SwiftUI. Sans `ViewModifier`, les styles sont dupliqués dans tout le projet. Avec eux, votre code est maintenable, cohérent et facilement refactorisable.

<br>

---

## Le Problème : Duplication de Styles

```swift title="Swift (SwiftUI) — Avant : styles dupliqués dans tout le projet"
import SwiftUI

// Sans ViewModifier : chaque bouton primaire répète le même code
struct VueAvecDuplication: View {
    var body: some View {
        VStack {
            // Bouton 1
            Button("Connexion") { }
                .font(.headline)
                .foregroundStyle(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 14)
                .background(Color.indigo)
                .clipShape(Capsule())
                .shadow(color: .indigo.opacity(0.4), radius: 8, x: 0, y: 4)

            // Bouton 2 — exactement le même code répété
            Button("Inscription") { }
                .font(.headline)
                .foregroundStyle(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 14)
                .background(Color.indigo)
                .clipShape(Capsule())
                .shadow(color: .indigo.opacity(0.4), radius: 8, x: 0, y: 4)

            // Si la couleur change → modifier TOUS les boutons manuellement
        }
    }
}
```

*Ce code contient 12 lignes de style répétées. Dans une vraie application avec 20 boutons, la maintenance devient un cauchemar.*

<br>

---

## `ViewModifier` — Créer un Modificateur Personnalisé

```swift title="Swift (SwiftUI) — ViewModifier : définir un style une seule fois"
import SwiftUI

// Modifier 1 : style de bouton primaire
struct StyleBoutonPrimaire: ViewModifier {

    var couleur: Color = .indigo
    var désactivé: Bool = false

    // func body(content:) — transforme la vue reçue
    // content : la vue à laquelle ce modifier est appliqué
    func body(content: Content) -> some View {
        content
            .font(.headline)
            .foregroundStyle(désactivé ? .secondary : .white)
            .padding(.horizontal, 24)
            .padding(.vertical, 14)
            .background(désactivé ? Color.gray.opacity(0.3) : couleur)
            .clipShape(Capsule())
            .shadow(color: désactivé ? .clear : couleur.opacity(0.4),
                    radius: 8, x: 0, y: 4)
    }
}

// Modifier 2 : carte avec ombre
struct StyleCarte: ViewModifier {
    var rayon: CGFloat = 16
    var ombre: CGFloat = 8

    func body(content: Content) -> some View {
        content
            .background(Color(.systemBackground))
            .clipShape(RoundedRectangle(cornerRadius: rayon))
            .shadow(color: .black.opacity(0.08), radius: ombre, x: 0, y: 4)
    }
}

// Modifier 3 : badge de statut
struct StyleBadge: ViewModifier {
    let couleur: Color

    func body(content: Content) -> some View {
        content
            .font(.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, 10)
            .padding(.vertical, 4)
            .background(couleur.opacity(0.15))
            .foregroundStyle(couleur)
            .clipShape(Capsule())
    }
}

// Usage avec .modifier() — syntaxe explicite
struct VueAvecModifiers: View {
    @State private var désactivé = false

    var body: some View {
        VStack(spacing: 20) {
            Button("Connexion") { }
                .modifier(StyleBoutonPrimaire(couleur: .indigo))

            Button("Inscription") { }
                .modifier(StyleBoutonPrimaire(couleur: .teal))

            Button("Désactivé") { }
                .modifier(StyleBoutonPrimaire(désactivé: désactivé))

            // Carte avec modifier
            VStack(alignment: .leading) {
                Text("Titre de la carte")
                    .font(.headline)
                Text("Contenu de la carte")
                    .foregroundStyle(.secondary)
            }
            .padding(20)
            .modifier(StyleCarte())

            // Badge
            Text("Nouveau")
                .modifier(StyleBadge(couleur: .orange))
        }
        .padding()
    }
}
```

<br>

---

## Extension `View` — Syntaxe `.monModifier()`

La syntaxe `.modifier(MonModifier())` est verbeux. Une extension sur `View` permet d'écrire `.boutonPrimaire()` — comme les modificateurs natifs SwiftUI.

```swift title="Swift (SwiftUI) — Extension View pour une syntaxe fluide"
import SwiftUI

// Extension sur View — active la syntaxe à points
extension View {

    // Bouton primaire
    func boutonPrimaire(couleur: Color = .indigo, désactivé: Bool = false) -> some View {
        modifier(StyleBoutonPrimaire(couleur: couleur, désactivé: désactivé))
    }

    // Carte
    func styleCarte(rayon: CGFloat = 16) -> some View {
        modifier(StyleCarte(rayon: rayon))
    }

    // Badge
    func badge(couleur: Color) -> some View {
        modifier(StyleBadge(couleur: couleur))
    }

    // Modificateur utilitaire : masquer conditionnellement
    @ViewBuilder
    func masqué(si condition: Bool) -> some View {
        if condition {
            self.hidden()
        } else {
            self
        }
    }

    // Modificateur utilitaire : fond de carte rapide
    func carteFond(padded: Bool = true) -> some View {
        self
            .if(padded) { $0.padding(16) }
            .styleCarte()
    }
}

// Extension conditionnelle sur View
extension View {
    // Applique une transformation si condition est vraie
    @ViewBuilder
    func `if`<Transform: View>(_ condition: Bool, transform: (Self) -> Transform) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}

// Résultat : syntaxe claire et lisible
struct VueAvecExtensions: View {
    @State private var afficherBadge = true

    var body: some View {
        VStack(spacing: 20) {
            // Syntaxe fluide — identique aux modificateurs SwiftUI natifs
            Button("Connexion") { }
                .boutonPrimaire()

            Button("Inscription") { }
                .boutonPrimaire(couleur: .teal)

            Button("Désactivé") { }
                .boutonPrimaire(désactivé: true)

            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("Documentation SwiftUI")
                        .font(.headline)
                    Spacer()
                    Text("Nouveau")
                        .badge(couleur: .orange)
                        .masqué(si: !afficherBadge)
                }
                Text("18 modules • 10 semaines")
                    .foregroundStyle(.secondary)
            }
            .carteFond()
        }
        .padding()
    }
}
```

<br>

---

## `@ViewBuilder` — Des Vues Conditionnelles dans les Fonctions

`@ViewBuilder` permet de retourner des vues différentes selon une condition — utilisé dans les paramètres et les fonctions qui produisent des vues.

```swift title="Swift (SwiftUI) — @ViewBuilder dans des composants flexibles"
import SwiftUI

// Composant de liste d'informations flexible
struct LigneInfoFlexible: View {
    let icône: String
    let titre: String
    let couleurIcône: Color

    // @ViewBuilder : peut retourner n'importe quelle vue selon la logique interne
    @ViewBuilder var valeursView: some View {
        // La logique peut retourner des types différents
        // @ViewBuilder handle la réconciliation de types automatiquement
        HStack {
            Text("Valeur")
                .fontWeight(.medium)
        }
    }

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icône)
                .foregroundStyle(couleurIcône)
                .frame(width: 30)
            Text(titre)
                .foregroundStyle(.secondary)
            Spacer()
            valeursView
        }
    }
}

// Composant bouton polyvalent avec @ViewBuilder
struct BoutonPolyvalent<Label: View>: View {
    let action: () -> Void
    let couleur: Color
    @ViewBuilder let label: () -> Label  // Closure @ViewBuilder : label générique

    init(couleur: Color = .indigo,
         action: @escaping () -> Void,
         @ViewBuilder label: @escaping () -> Label) {
        self.couleur = couleur
        self.action = action
        self.label = label
    }

    var body: some View {
        Button(action: action) {
            label()
                .font(.headline)
                .foregroundStyle(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 14)
                .background(couleur)
                .clipShape(Capsule())
        }
    }
}

struct DémoBoutonPolyvalent: View {
    var body: some View {
        VStack(spacing: 16) {

            // Utilisation avec Text simple
            BoutonPolyvalent(action: { }) {
                Text("Bouton texte")
            }

            // Utilisation avec Label (icône + texte)
            BoutonPolyvalent(couleur: .teal, action: { }) {
                Label("Télécharger", systemImage: "arrow.down.circle.fill")
            }

            // Utilisation avec HStack personnalisé
            BoutonPolyvalent(couleur: .orange, action: { }) {
                HStack {
                    Image(systemName: "star.fill")
                    Text("Ajouter aux favoris")
                    Image(systemName: "star.fill")
                }
            }
        }
        .padding()
    }
}
```

*`@ViewBuilder` est le mécanisme qui permet à `VStack`, `HStack`, et `body` d'accepter plusieurs vues en paramètre. En définissant vos propres closures `@ViewBuilder`, vous créez des composants aussi flexibles que les containers natifs SwiftUI.*

<br>

---

## Bibliothèque de Composants — Design System

Un design system complet combine ViewModifiers, extensions et composants.

```swift title="Swift (SwiftUI) — Un design system minimal mais cohérent"
import SwiftUI

// ═══════════════════════════════════════════════
// DESIGN TOKENS — couleurs, tailles, rayons
// ═══════════════════════════════════════════════

enum DS {
    // Couleurs
    enum Couleurs {
        static let primaire = Color.indigo
        static let succès   = Color.green
        static let danger   = Color.red
        static let avertissement = Color.orange
    }

    // Rayons de coins
    enum Rayons {
        static let petit:    CGFloat = 8
        static let moyen:    CGFloat = 12
        static let grand:    CGFloat = 16
        static let capsule:  CGFloat = 100
    }

    // Espacement
    enum Espace {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }
}

// ═══════════════════════════════════════════════
// COMPOSANTS — construits sur les tokens
// ═══════════════════════════════════════════════

// Carte standard
struct DSCarte<Content: View>: View {
    @ViewBuilder var content: () -> Content

    var body: some View {
        VStack(alignment: .leading, spacing: DS.Espace.sm) {
            content()
        }
        .padding(DS.Espace.md)
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: DS.Rayons.grand))
        .shadow(color: .black.opacity(0.07), radius: 10, x: 0, y: 4)
    }
}

// Badge statut
struct DSBadge: View {
    enum Style { case info, succès, danger, avertissement }
    let texte: String
    let style: Style

    var couleur: Color {
        switch style {
        case .info:          return DS.Couleurs.primaire
        case .succès:        return DS.Couleurs.succès
        case .danger:        return DS.Couleurs.danger
        case .avertissement: return DS.Couleurs.avertissement
        }
    }

    var body: some View {
        Text(texte)
            .font(.caption2)
            .fontWeight(.bold)
            .padding(.horizontal, DS.Espace.sm)
            .padding(.vertical, DS.Espace.xs)
            .background(couleur.opacity(0.15))
            .foregroundStyle(couleur)
            .clipShape(Capsule())
    }
}

// Utilisation du design system
struct VueDesignSystem: View {
    var body: some View {
        ScrollView {
            VStack(spacing: DS.Espace.md) {

                DSCarte {
                    HStack {
                        Text("SwiftUI — Module 11")
                            .font(.headline)
                        Spacer()
                        DSBadge(texte: "Avancé", style: .avertissement)
                    }
                    Text("Animations et Transitions")
                        .foregroundStyle(.secondary)
                    HStack {
                        DSBadge(texte: "3h", style: .info)
                        DSBadge(texte: "Complété", style: .succès)
                    }
                }

                DSCarte {
                    HStack {
                        Text("Vapor — Module 08")
                            .font(.headline)
                        Spacer()
                        DSBadge(texte: "JWT", style: .danger)
                    }
                    Text("Authentification et JWT")
                        .foregroundStyle(.secondary)
                }
            }
            .padding(DS.Espace.md)
        }
    }
}

#Preview {
    VueDesignSystem()
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Créer 3 ViewModifiers**

```swift title="Swift — Exercice 1 : bibliothèque de modificateurs"
// Créez les trois modificateurs suivants + leurs extensions View :
//
// 1. styleEnTête : police titre, couleur primaire, padding bas
// 2. styleSectionTitre : police caption en majuscules, gris, padding
// 3. effetVerre : fond .ultraThinMaterial, cornedRadius 16, overlay border léger

// Vérification : utilisez-les dans une vue exemple sans aucun modificateur inline
struct VueSansModifiersInline: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Mon Application")
                .styleEnTête()

            Text("Section Récente")
                .styleSectionTitre()

            VStack {
                Text("Contenu avec effet verre")
            }
            .effetVerre()
        }
        .padding()
    }
}
```

**Exercice 2 — Composant Card générique**

```swift title="Swift — Exercice 2 : carte générique réutilisable (@ViewBuilder)"
// Créez un composant CartGénérique<Header: View, Content: View, Footer: View>
// avec trois zones séparées : header, content, footer
// Le footer est optionnel (default : EmptyView)
// Signature attendue :
//   CartGénérique {
//     Text("En-tête")  // header
//   } content: {
//     Text("Contenu")  // content
//   } footer: {
//     Button("Action") { }  // footer optionnel
//   }

struct CartGénérique<Header: View, Content: View, Footer: View>: View {
    @ViewBuilder var header: () -> Header
    @ViewBuilder var content: () -> Content
    @ViewBuilder var footer: () -> Footer

    // TODO : implémenter avec Dividers entre les zones
    var body: some View { EmptyView() }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `ViewModifier` est le pattern pour encapsuler un ensemble de modificateurs en un seul — défini une fois, réutilisé partout. La convention `extension View` avec des méthodes nommées `.monModifier()` active la syntaxe à points familière des modificateurs SwiftUI natifs. `@ViewBuilder` permet aux closures de fonctions et aux computed properties de contenir de la logique conditionnelle (if/else/switch) tout en retournant des vues — c'est le mécanisme derrière `body`, `VStack`, `HStack`. Un **design system** structuré avec des tokens (DS.Couleurs, DS.Rayons, DS.Espace) et des composants (DSCarte, DSBadge) garantit la cohérence visuelle et la maintenabilité à l'échelle d'une vraie application.

> Dans le module suivant, nous abordons l'architecture **MVVM** — comment organiser un projet SwiftUI en couches Modèle / ViewModel / Vue pour une scalabilité et une testabilité maximales.

<br>
