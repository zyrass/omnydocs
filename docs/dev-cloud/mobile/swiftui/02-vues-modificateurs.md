---
description: "SwiftUI — Vues de base et chaîne de modificateurs : Text, Image, Button, Label, et les règles de composition."
icon: lucide/book-open-check
tags: ["SWIFTUI", "VIEWS", "MODIFICATEURS", "TEXT", "IMAGE", "BUTTON"]
---

# Vues et Modificateurs

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Toque du Chef"
    Un plat de restaurant n'est pas juste une recette — c'est une recette de base à laquelle le chef applique des transformations successives : assaisonner, dresser, décorer. Chaque étape transforme le plat précédent. Supprimer ou réordonner une étape change le résultat. En SwiftUI, les **vues** sont vos ingrédients de base (`Text`, `Image`, `Button`) et les **modificateurs** sont les transformations successives (`.font()`, `.padding()`, `.background()`). L'ordre compte — comme en cuisine.

Les vues SwiftUI sont des structures légères. Elles ne font que décrire l'interface — SwiftUI se charge du rendu. Les modificateurs ne modifient pas la vue originale : ils en créent une nouvelle, transformée. C'est ce qui rend la composition si puissante.

<br>

---

## Les Vues de Base

SwiftUI fournit un ensemble de vues primitives. Voici les plus utilisées.

<br>

### `Text` — Afficher du Texte

```swift title="Swift (SwiftUI) — Text : toutes les variantes essentielles"
import SwiftUI

struct DémoText: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {

            // Texte simple
            Text("Bonjour, OmnyDocs !")

            // Modificateurs de police
            Text("Titre principal")
                .font(.largeTitle)      // Police système selon la taille
                .bold()                 // Équivalent de .fontWeight(.bold)

            // Police personnalisée avec taille dynamique
            Text("Sous-titre")
                .font(.system(size: 20, weight: .semibold, design: .rounded))

            // Couleur et accessibilité
            Text("Texte coloré")
                .foregroundStyle(.blue)      // iOS 17 — remplace .foregroundColor()

            // Alignement multiligne (par défaut .center)
            Text("Un texte assez long qui peut s'étendre sur plusieurs lignes selon la largeur disponible.")
                .multilineTextAlignment(.leading)
                .lineLimit(3)           // Maximum 3 lignes — nil pour illimité

            // Texte barré et souligné
            Text("Prix original : 49 €")
                .strikethrough(true, color: .red)

            // Interpolation avec formatage
            let prix: Double = 29.99
            Text("Prix : \(prix, format: .currency(code: "EUR"))")
                .font(.headline)
        }
        .padding()
    }
}
```

*`foregroundStyle()` est préféré à `foregroundColor()` depuis iOS 17 car il supporte les gradients et les matériaux. Pour iOS 16, `foregroundColor()` est toujours valide.*

<br>

### `Image` — Afficher des Images

```swift title="Swift (SwiftUI) — Image : SF Symbols et images personnalisées"
import SwiftUI

struct DémoImage: View {
    var body: some View {
        VStack(spacing: 20) {

            // SF Symbol — bibliothèque de 5 000+ icônes Apple
            Image(systemName: "star.fill")
                .font(.system(size: 50))    // Taille via font pour les SF Symbols
                .foregroundStyle(.yellow)

            // SF Symbol avec rendu multicolore
            Image(systemName: "cloud.sun.rain.fill")
                .symbolRenderingMode(.multicolor)
                .font(.system(size: 50))

            // Image depuis les Assets (ajoutée dans Assets.xcassets)
            Image("maPhoto")
                .resizable()                    // Permet le redimensionnement
                .scaledToFit()                  // Conserve les proportions (fit)
                .frame(width: 200, height: 150) // Contrainte de taille
                .clipShape(RoundedRectangle(cornerRadius: 12))

            // Image avec accessibilité
            Image(systemName: "heart.fill")
                .accessibilityLabel("Favori")   // Texte lu par VoiceOver
                .font(.title)
                .foregroundStyle(.red)
        }
    }
}
```

*`resizable()` doit toujours précéder les modificateurs de taille — sans lui, l'image s'affiche à sa taille intrinsèque et ignore `.frame()`.*

<br>

### `Button` — Boutons Interactifs

```swift title="Swift (SwiftUI) — Button : styles et configurations"
import SwiftUI

struct DémoButton: View {
    @State private var message = "Appuyez sur un bouton"

    var body: some View {
        VStack(spacing: 16) {

            Text(message)
                .font(.headline)

            // Bouton simple — label texte
            Button("Bouton simple") {
                message = "Bouton simple pressé"
            }

            // Style système — bordure proéminente (bouton principal)
            Button("Action principale") {
                message = "Action principale"
            }
            .buttonStyle(.borderedProminent)
            .tint(.indigo)          // Couleur de l'accentuation

            // Bouton avec icône via Label
            Button {
                message = "Téléchargement lancé"
            } label: {
                // Label combine texte et icône
                Label("Télécharger", systemImage: "arrow.down.circle.fill")
            }
            .buttonStyle(.bordered)

            // Bouton destructif (rouge)
            Button("Supprimer", role: .destructive) {
                message = "Suppression confirmée"
            }

            // Bouton désactivé conditionnellement
            Button("Envoi") {
                message = "Formulaire envoyé"
            }
            .buttonStyle(.borderedProminent)
            .disabled(message.isEmpty)  // Grisé si condition vraie
        }
        .padding()
    }
}
```

*`role: .destructive` applique automatiquement la couleur rouge système — cohérent avec les guidelines Human Interface Guidelines d'Apple.*

<br>

### Autres Vues Essentielles

```swift title="Swift (SwiftUI) — Divider, Spacer, Color, Rectangle"
import SwiftUI

struct DémoAutresVues: View {
    var body: some View {
        VStack {

            Text("Section A")
            Divider()           // Ligne de séparation horizontale
            Text("Section B")

            Spacer()            // Espace flexible qui pousse les éléments

            // Color est une vue — utilisable directement
            Color.blue
                .frame(height: 50)
                .cornerRadius(8)

            // Rectangle comme fond ou séparateur personnalisé
            Rectangle()
                .fill(Color.gray.opacity(0.2))
                .frame(height: 2)

            // Capsule — rectangle à coins parfaitement arrondis
            Capsule()
                .fill(Color.orange)
                .frame(width: 120, height: 40)
        }
        .padding()
    }
}
```

<br>

---

## La Chaîne de Modificateurs

Les modificateurs sont la signature de SwiftUI. Chaque `.modificateur()` retourne une nouvelle vue enveloppant la précédente — ils ne mutent rien.

```swift title="Swift (SwiftUI) — Visualiser la chaîne de modificateurs"
import SwiftUI

// Chaque modificateur crée une nouvelle couche autour de la vue précédente
// L'ordre EST significatif

struct DémoChaine: View {
    var body: some View {
        VStack(spacing: 40) {

            // Version A : padding AVANT background
            // Le fond couvre le texte + ses marges internes
            Text("Padding → Background")
                .padding(16)
                .background(Color.yellow)

            // Version B : background AVANT padding
            // Le fond ne couvre que le texte, pas les marges
            Text("Background → Padding")
                .background(Color.yellow)
                .padding(16)

            // Chaîne complète typique d'un composant
            Text("Composant complet")
                .font(.headline)
                .foregroundStyle(.white)
                .padding(.horizontal, 20)
                .padding(.vertical, 12)
                .background(Color.indigo)
                .clipShape(Capsule())
                .shadow(color: .black.opacity(0.2), radius: 4, x: 0, y: 2)
        }
    }
}
```

<br>
![Pipeline de Modificateurs SwiftUI](/assets/images/swiftui/swiftui-modificateurs-pipeline.png)
<br>

*L'ordre `padding` → `background` produit un fond qui englobe les marges. L'ordre inverse produit un fond collé au texte. SwiftUI applique les modificateurs de l'intérieur vers l'extérieur.*

<br>

### Les Modificateurs de Layout Essentiels

```swift title="Swift (SwiftUI) — Référence des modificateurs de mise en page"
import SwiftUI

struct DémoLayoutModificateurs: View {
    var body: some View {
        VStack(spacing: 30) {

            // frame : contraintes de taille et d'alignement
            Text("Texte centré")
                .frame(maxWidth: .infinity)     // S'étend sur toute la largeur
                .frame(height: 60)              // Hauteur fixe
                .background(Color.gray.opacity(0.1))

            // padding : espacement interne
            Text("Espacement asymétrique")
                .padding(.horizontal, 24)       // 24pt gauche et droite seulement
                .padding(.top, 12)              // 12pt en haut seulement
                .background(Color.mint.opacity(0.3))

            // overlay : superposer une vue par-dessus
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.indigo)
                .frame(height: 80)
                .overlay {
                    Text("Superposé")
                        .foregroundStyle(.white)
                        .bold()
                }

            // cornerRadius et shadow
            Text("Carte avec ombre")
                .padding(20)
                .background(Color.white)
                .cornerRadius(16)
                .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 4)
        }
        .padding()
    }
}
```

<br>

---

## Composition de Vues

La puissance de SwiftUI réside dans la **composition** — assembler des vues simples pour former des composants complexes, puis des composants pour former des écrans.

```swift title="Swift (SwiftUI) — Décomposer en sous-vues réutilisables"
import SwiftUI

// Composant atomique : un badge de statut
struct BadgeStatut: View {
    let label: String
    let couleur: Color

    var body: some View {
        Text(label)
            .font(.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, 10)
            .padding(.vertical, 4)
            .background(couleur.opacity(0.15))
            .foregroundStyle(couleur)
            .clipShape(Capsule())
    }
}

// Composant : une ligne d'information
struct LigneInfo: View {
    let icône: String
    let titre: String
    let valeur: String

    var body: some View {
        HStack {
            Label(titre, systemImage: icône)
                .foregroundStyle(.secondary)    // Couleur secondaire du système
            Spacer()
            Text(valeur)
                .fontWeight(.medium)
        }
    }
}

// Vue complète assemblée depuis les composants
struct FicheUtilisateur: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {

            // En-tête
            HStack(spacing: 16) {
                Image(systemName: "person.circle.fill")
                    .font(.system(size: 56))
                    .foregroundStyle(.indigo)

                VStack(alignment: .leading, spacing: 4) {
                    Text("Alice Martin")
                        .font(.title2)
                        .fontWeight(.bold)
                    BadgeStatut(label: "Développeuse iOS", couleur: .indigo)
                }
            }

            Divider()

            // Corps — utilise le composant LigneInfo
            LigneInfo(icône: "envelope", titre: "Email", valeur: "alice@omnyvia.fr")
            LigneInfo(icône: "location", titre: "Ville",  valeur: "Paris")
            LigneInfo(icône: "calendar", titre: "Depuis", valeur: "2022")
        }
        .padding(20)
        .background(Color(.systemBackground))  // Couleur de fond adaptée au mode (clair/sombre)
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .shadow(color: .black.opacity(0.08), radius: 12, x: 0, y: 4)
        .padding()
    }
}

#Preview {
    FicheUtilisateur()
}
```

*Extraire des sous-vues n'a aucun coût de performance en SwiftUI — le compilateur les aplatit. En revanche, les sous-vues améliorent la lisibilité et la réutilisabilité, et permettent à Xcode de limiter les re-rendus.*

<br>

---

## `Label` — Texte et Icône Combinés

```swift title="Swift (SwiftUI) — Label : le composant texte + icône standard"
import SwiftUI

struct DémoLabel: View {
    var body: some View {
        VStack(spacing: 16) {

            // Label standard — utilisé dans List, Menu, Button
            Label("Téléphone", systemImage: "phone.fill")

            Label("Localisation", systemImage: "location.fill")
                .foregroundStyle(.red)

            // Label avec image personnalisée
            Label {
                Text("Photo de profil")
                    .font(.headline)
            } icon: {
                Image(systemName: "person.crop.circle")
                    .foregroundStyle(.indigo)
            }

            // Style : icône seule (utile dans les barres d'outils)
            Label("Partager", systemImage: "square.and.arrow.up")
                .labelStyle(.iconOnly)

            // Style : texte seul
            Label("Partager", systemImage: "square.and.arrow.up")
                .labelStyle(.titleOnly)
        }
    }
}
```

*`Label` est le composant privilégié pour les combinaisons texte/icône — il s'adapte automatiquement au contexte (sidebar, bouton, liste) en choisissant le `labelStyle` approprié.*

<br>

---

## Modificateurs Adaptés au Mode Sombre

SwiftUI supporte nativement le mode sombre (Dark Mode). Les couleurs système s'adaptent automatiquement.

```swift title="Swift (SwiftUI) — Couleurs adaptatives et mode sombre"
import SwiftUI

struct DémoModeSombre: View {
    var body: some View {
        VStack(spacing: 16) {

            // Couleurs système — s'adaptent automatiquement
            Text("Fond adaptatif")
                .padding()
                .background(Color(.systemGray6))    // Gris clair/foncé selon le mode

            Text("Couleur principale")
                .foregroundStyle(Color(.label))     // Noir/Blanc selon le mode

            // Matériaux — effet "verre dépoli" adaptatif
            RoundedRectangle(cornerRadius: 16)
                .fill(.ultraThinMaterial)           // Matériau translucide adaptatif
                .frame(height: 80)
                .overlay { Text("Matériau").foregroundStyle(.primary) }

            // Forcer un mode pour la preview
        }
        .padding()
    }
}

#Preview("Light") {
    DémoModeSombre()
}

#Preview("Dark") {
    DémoModeSombre()
        .preferredColorScheme(.dark)
}
```

*Utilisez `Color(.systemBackground)`, `Color(.label)`, `Color(.systemGray6)` plutôt que `.white`, `.black`, `.gray` — les premières s'adaptent automatiquement au mode sombre.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Carte de profil stylée**

```swift title="Swift — Exercice 1 : composition et modificateurs"
// Créez une vue ProfilCard qui affiche :
// - Un grand SF Symbol (personnage, avatar)
// - Un nom en titre
// - Un rôle en sous-titre (police secondaire, couleur grisée)
// - Un badge coloré avec le niveau ("Débutant", "Intermédiaire", "Avancé")
// - Un fond blanc avec coin arrondis et ombre légère
//
// Bonus : prévisualiser en mode sombre aussi

struct ProfilCard: View {
    let nom: String
    let rôle: String
    let niveau: String
    let couleurNiveau: Color

    var body: some View {
        // TODO : implémenter
    }
}

#Preview {
    VStack(spacing: 20) {
        ProfilCard(nom: "Alice", rôle: "Développeuse iOS", niveau: "Avancé", couleurNiveau: .indigo)
        ProfilCard(nom: "Bob",   rôle: "Designer UI",     niveau: "Débutant", couleurNiveau: .green)
    }
    .padding()
    .background(Color(.systemGroupedBackground))
}
```

**Exercice 2 — L'ordre des modificateurs**

```swift title="Swift — Exercice 2 : prédire le résultat"
// Pour chaque variante, prédisez l'apparence AVANT de tester
// Puis lancez le preview pour vérifier

struct ExerciceOrdre: View {
    var body: some View {
        VStack(spacing: 30) {
            // Variante A
            Text("A")
                .padding(20)
                .background(Color.yellow)
                .cornerRadius(12)

            // Variante B
            Text("B")
                .background(Color.yellow)
                .padding(20)
                .cornerRadius(12)

            // Variante C
            Text("C")
                .cornerRadius(12)       // Que se passe-t-il ici ?
                .padding(20)
                .background(Color.yellow)

            // Variante D : fond + frame
            Text("D")
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.yellow)
        }
    }
}
// Question : quelle variante a un fond sur toute la largeur ?
// Quelle variante a des coins arrondis visibles ?
```

**Exercice 3 — Composant bouton réutilisable**

```swift title="Swift — Exercice 3 : créer un BoutonPrimaire réutilisable"
// Créez un composant BoutonPrimaire avec :
// - Un titre (String)
// - Une icône optionnelle (String? — nom de SF Symbol)
// - Une action (closure)
// - Un style visuel cohérent (fond coloré, coins arrondis, ombre)

struct BoutonPrimaire: View {
    let titre: String
    let icône: String?
    let action: () -> Void

    var body: some View {
        // TODO : utiliser Label si icône != nil, Text sinon
    }
}

#Preview {
    VStack(spacing: 16) {
        BoutonPrimaire(titre: "Connexion", icône: "arrow.right", action: { })
        BoutonPrimaire(titre: "Continuer", icône: nil, action: { })
    }
    .padding()
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les vues SwiftUI (`Text`, `Image`, `Button`, `Label`) sont des structures légères qui décrivent l'interface. Les **modificateurs** transforment successivement chaque vue — ils ne la modifient pas, ils en créent une nouvelle enveloppante. **L'ordre des modificateurs est fondamental** : `.padding().background()` et `.background().padding()` produisent des résultats différents. La composition de petits composants réutilisables est la bonne pratique SwiftUI — sans coût de performance. Utilisez les couleurs système (`Color(.systemBackground)`) pour une adaptation automatique au mode sombre.

> Dans le module suivant, nous abordons le **Layout** — comment `VStack`, `HStack`, `ZStack`, `LazyVGrid` et `GeometryReader` organisent vos vues dans l'espace disponible, et comment `Spacer` et les alignements contrôlent la disposition.

<br>
