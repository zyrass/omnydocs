---
description: "SwiftUI accessibilité : VoiceOver, Dynamic Type, modificateurs d'accessibilité et internationalisation avec String(localized:)."
icon: lucide/book-open-check
tags: ["SWIFTUI", "ACCESSIBILITE", "VOICEOVER", "DYNAMICTYPE", "I18N"]
---

# Accessibilité & Internationalisation

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Construire pour Tous"
    Un bâtiment conforme aux normes d'accessibilité ne se contente pas de l'ascenseur — il prévoit des rampes, des bandes de sol podotactiles, des boutons en braille. Ces aménagements ne gênent pas les personnes valides ; ils rendent le bâtiment utilisable par tous. En développement mobile, l'accessibilité suit le même principe : elle ne retire rien aux utilisateurs "standard" mais permet à 15% de la population mondiale en situation de handicap d'utiliser votre application. Apple Review rejette les applications qui ne respectent pas les exigences minimales d'accessibilité.

SwiftUI fournit une **accessibilité gratuite** pour la plupart des vues natives (Text, Button, Toggle) — votre rôle est de compléter pour les cas personnalisés.

<br>

---

## Accessibilité "Gratuite" et Accessibilité à Compléter

```swift title="Swift (SwiftUI) — Ce qui est automatique vs ce qui demande du travail"
import SwiftUI

struct DémoAccessibilitéAutomatique: View {
    @State private var activé = false
    @State private var valeur: Double = 50

    var body: some View {
        VStack(spacing: 20) {

            // ✅ AUTOMATIQUE — VoiceOver lit "Bonjour, SwiftUI — Texte statique"
            Text("Bonjour, SwiftUI !")

            // ✅ AUTOMATIQUE — VoiceOver lit le label et l'état
            Toggle("Recevoir des notifications", isOn: $activé)

            // ✅ AUTOMATIQUE — VoiceOver lit "50 %, Curseur. Ajuster"
            Slider(value: $valeur, in: 0...100)

            // ✅ AUTOMATIQUE si Label, ❌ NÉCESSITE un accessibilityLabel si Image seule
            Button {
                // action
            } label: {
                Label("Partager", systemImage: "square.and.arrow.up")
                // VoiceOver lit "Partager, Bouton" ✅
            }

            // ❌ Problème : Image seule sans label — VoiceOver lit "square.and.arrow.up"
            Image(systemName: "square.and.arrow.up")
                .font(.title)
                // Solution : .accessibilityLabel pour les images décoratives ou significatives
                .accessibilityLabel("Partager")
        }
    }
}
```

<br>

---

## Modificateurs d'Accessibilité Essentiels

```swift title="Swift (SwiftUI) — Les modificateurs d'accessibilité à connaître"
import SwiftUI

struct DémoModificateursAccessibilité: View {
    @State private var progression: Double = 0.6
    @State private var estFavori = false

    var body: some View {
        VStack(spacing: 24) {

            // 1. accessibilityLabel : remplace le texte lu par VoiceOver
            Image(systemName: "heart.fill")
                .font(.largeTitle)
                .foregroundStyle(.red)
                // Sans ceci, VoiceOver lirait "heart.fill"
                .accessibilityLabel("Ajouter aux favoris")

            // 2. accessibilityHint : décrit l'action (lu après le label et le rôle)
            Button("Activer") { }
                .accessibilityHint("Active le mode de notification silencieux")

            // 3. accessibilityValue : valeur dynamique (lue après le label)
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Rectangle().fill(Color.gray.opacity(0.2))
                    Rectangle()
                        .fill(Color.indigo)
                        .frame(width: geo.size.width * progression)
                }
                .cornerRadius(4)
            }
            .frame(height: 12)
            .accessibilityLabel("Progression du module")
            // VoiceOver lit "Progression du module — 60 %"
            .accessibilityValue("\(Int(progression * 100)) pourcent")

            // 4. accessibilityAddTraits : ajouter des traits (rôles)
            HStack {
                Image(systemName: estFavori ? "star.fill" : "star")
                    .foregroundStyle(estFavori ? .yellow : .gray)
                Text(estFavori ? "Favori" : "Ajouter aux favoris")
            }
            .onTapGesture { estFavori.toggle() }
            // Déclarer que cet HStack se comporte comme un bouton
            .accessibilityAddTraits(.isButton)
            .accessibilityLabel(estFavori ? "Retirer des favoris" : "Ajouter aux favoris")

            // 5. accessibilityHidden : masquer un élément décoratif
            HStack {
                Image(systemName: "chevron.right")
                    // Élément décoratif — inutile à lire
                    .accessibilityHidden(true)
                Text("Module suivant")
            }

            // 6. Regrouper plusieurs vues en une seule entrée VoiceOver
            VStack(alignment: .leading) {
                Text("Alice Martin")
                    .font(.headline)
                Text("Développeuse iOS — Paris")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            // Regrouper les deux textes — VoiceOver les lit ensemble
            .accessibilityElement(children: .combine)
        }
        .padding()
    }
}
```

<br>

---

## Dynamic Type — Polices Adaptatives

Dynamic Type permet à l'utilisateur de choisir la taille de texte dans ses Réglages. Votre interface doit s'adapter.

```swift title="Swift (SwiftUI) — Supporter Dynamic Type correctement"
import SwiftUI

struct DémoDynamicType: View {

    // Accès à la taille de police choisie par l'utilisateur
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {

                // ✅ Les polices système s'adaptent automatiquement
                Text("Titre principal")
                    .font(.title)      // S'agrandit avec les Réglages utilisateur

                Text("Corps de texte")
                    .font(.body)

                // ✅ Adapter le layout selon la taille Dynamic Type
                // Pour les grandes tailles, empiler verticalement plutôt qu'horizontalement
                LayoutAdaptif {
                    Image(systemName: "person.circle.fill")
                        .font(.system(size: 44))
                        .foregroundStyle(.indigo)

                    VStack(alignment: .leading) {
                        Text("Alice Martin").font(.headline)
                        Text("Développeuse iOS").font(.caption).foregroundStyle(.secondary)
                    }
                }

                // ❌ Éviter les polices de taille fixe pour du texte important
                Text("Texte à taille fixe")
                    .font(.system(size: 14))  // Ne s'adapte pas !
                    // Préférer : .font(.body) ou .font(.caption)

                // ✅ Limiter Dynamic Type si nécessaire (cas rares)
                Text("Texte limité")
                    .font(.body)
                    .dynamicTypeSize(.small ... .accessibility3)  // Plage autorisée
            }
            .padding()
        }
    }
}

// Composant adaptatif : horizontal en normal, vertical en grande taille
struct LayoutAdaptatif<Content: View>: View {
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize
    @ViewBuilder var content: () -> Content

    var body: some View {
        if dynamicTypeSize >= .accessibility1 {
            // Grande taille : empiler verticalement
            VStack(alignment: .leading, spacing: 8) { content() }
        } else {
            // Taille normale : affichage horizontal
            HStack(spacing: 12) { content() }
        }
    }
}
```

*`dynamicTypeSize >= .accessibility1` détecte les "Tailles d'accessibilité" (les 5 plus grandes tailles du sélecteur). C'est le meilleur seuil pour passer en layout vertical.*

<br>

---

## Internationalisation — `String(localized:)`

```swift title="Swift (SwiftUI) — Localisation avec String(localized:)"
import SwiftUI

struct VueLocalisée: View {

    @State private var compteur = 42
    let date = Date.now
    let prix = 29.99

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {

            // Dans SwiftUI : les littéraux String dans Text sont automatiquement localisés
            // SwiftUI cherche "Bonjour" dans Localizable.strings/xcstrings
            Text("Bienvenue sur OmnyDocs")  // Clé de localisation automatique

            // Interpolation localisée — n'utilisez pas \() directement
            // Utilisez LocalizedStringKey pour que l'interpolation soit localisée
            Text("Vous avez \(compteur) modules")

            // Date formatée selon la locale
            Text("Mise à jour : \(date, format: .dateTime.day().month().year())")
                .foregroundStyle(.secondary)

            // Prix formaté selon la locale (€ en FR, $ en US)
            Text("\(prix, format: .currency(code: "EUR"))")
                .font(.headline)

            Divider()

            // Pluriel localisé — utilisez String(localized:) pour le code non-Vue
            let message = String(
                localized: "\(compteur) article(s) disponible(s)",
                comment: "Nombre d'articles dans le catalogue"
            )
            Text(message)
        }
        .padding()
    }
}

// Configuration de la localisation dans un projet Xcode :
// 1. Project → Info → Localizations → Ajouter la ou les langues
// 2. Créer String Catalog (Localizable.xcstrings) — iOS 16+
//    OU Localizable.strings pour les projets existants
// 3. String Catalog : Xcode extrait automatiquement les clés du code
```

<br>

### Fichier de Localisation (String Catalog)

```
// Localizable.xcstrings (iOS 16+ — format JSON)
// Le String Catalog remplace les anciens fichiers .strings — plus sûr, plus pratique

// Xcode extrait automatiquement les clés depuis le code et les affiche dans l'éditeur.
// Pour chaque langue ajoutée, vous renseignez la traduction dans l'éditeur visuel.

// Exemple de paires clé/traduction :
// "Bienvenue sur OmnyDocs" → [fr] "Bienvenue sur OmnyDocs"
//                           → [en] "Welcome to OmnyDocs"
//                           → [es] "Bienvenido a OmnyDocs"

// Variables de pluralisation :
// "%lld module(s)" → [fr] one: "%lld module" / other: "%lld modules"
//                  → [en] one: "%lld module" / other: "%lld modules"
```

*Le String Catalog (`.xcstrings`) d'iOS 16+ affiche toutes les chaînes à localiser dans un éditeur visuel Xcode. Il remplace les fichiers `.strings` fragmentés et offre la détection automatique des chaînes non traduites.*

<br>

---

## Test de l'Accessibilité et de la Localisation

```swift title="Swift (SwiftUI) — Previews pour accessibilité et localisation"
import SwiftUI

// Tester plusieurs configurations de Dynamic Type
#Preview("Dynamic Type — AX5") {
    VueLocalisée()
        .environment(\.dynamicTypeSize, .accessibility5)  // La plus grande
}

#Preview("Dark Mode + Large") {
    VueLocalisée()
        .preferredColorScheme(.dark)
        .environment(\.dynamicTypeSize, .xLarge)
}

// Tester en anglais
#Preview("English") {
    VueLocalisée()
        .environment(\.locale, .init(identifier: "en"))
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Audit d'accessibilité**

```swift title="Swift — Exercice 1 : corriger une vue non accessible"
// Cette vue a plusieurs problèmes d'accessibilité. Identifiez-les et corrigez-les.

struct VueNonAccessible: View {
    var body: some View {
        HStack {
            Image(systemName: "trash")          // Problème 1 : ?
                .foregroundStyle(.red)

            Text("Supprimer le fichier")
                .font(.system(size: 12))        // Problème 2 : ?

            Spacer()

            Circle()
                .fill(Color.green)
                .frame(width: 12, height: 12)    // Problème 3 : ? (indicateur de statut)
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .onTapGesture { }                        // Problème 4 : ?
    }
}
// TODO : corriger les 4 problèmes d'accessibilité identifiés
```

**Exercice 2 — Composant adaptatif Dynamic Type**

```swift title="Swift — Exercice 2 : carte adaptative"
// Créez une ProfilCard qui :
// - En taille normale : image à gauche, nom/rôle à droite (HStack)
// - En taille accessibility1+ : image en haut, nom/rôle en dessous (VStack)
// - Le nom utilise .font(.headline) — s'adapte automatiquement
// - Testez avec deux previews : dynamicTypeSize .medium et .accessibility3

struct ProfilCardAdaptative: View {
    let nom: String
    let rôle: String
    let icône: String

    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

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
    SwiftUI fournit l'accessibilité de base gratuitement pour `Text`, `Button`, `Toggle` et les contrôles natifs. Complétez avec `.accessibilityLabel()` (remplace le texte VoiceOver), `.accessibilityHint()` (décrit l'action), `.accessibilityValue()` (valeur dynamique), `.accessibilityHidden(true)` (éléments décoratifs), `.accessibilityAddTraits()` (déclarer le rôle) et `.accessibilityElement(children: .combine)` (regrouper). Dynamic Type est géré automatiquement par les polices système (`.font(.headline)`, etc.) — adaptez le layout avec `@Environment(\.dynamicTypeSize)` pour les grandes tailles. La localisation en SwiftUI repose sur le **String Catalog** (iOS 16+) — Xcode extrait les clés automatiquement depuis les littéraux `Text`.

> Dans le module suivant, nous abordons les **Tests** — `#Preview` (iOS 17), `PreviewProvider` (iOS 16), et comment structurer des ViewModèles testables avec XCTest.

<br>
