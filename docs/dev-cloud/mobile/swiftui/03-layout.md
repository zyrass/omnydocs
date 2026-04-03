---
description: "SwiftUI Layout : VStack, HStack, ZStack, alignements, Spacer, LazyVGrid, LazyHGrid et GeometryReader pour les mises en page dynamiques."
icon: lucide/book-open-check
tags: ["SWIFTUI", "LAYOUT", "VSTACK", "HSTACK", "GRID", "GEOMETRYREADER"]
---

# Layout — Stack, Grid, GeometryReader

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chef d'Orchestre de la Scène"
    Un metteur en scène de théâtre ne place pas ses acteurs au hasard. Il décide qui est devant, qui est derrière, qui est à gauche, qui est à droite, et comment l'espace entre eux évolue quand la scène change de format. En SwiftUI, les containers de layout — `VStack`, `HStack`, `ZStack`, `Grid` — sont ce metteur en scène. Ils décident comment distribuer l'espace et positionner chaque vue, indépendamment de la taille de l'écran.

Le layout SwiftUI est déclaratif et adaptatif : vous décrivez la structure, le système calcule les dimensions. Sur iPhone SE, iPad, ou en mode paysage, la même description produit un rendu optimal — à condition de bien connaître les outils.

<br>

---

## `VStack`, `HStack`, `ZStack`

Les trois containers fondamentaux. Chacun empile ses enfants dans une direction.

```swift title="Swift (SwiftUI) — Les trois stacks fondamentaux"
import SwiftUI

struct DémoStacks: View {
    var body: some View {
        VStack(spacing: 30) {

            // VStack : empilage vertical (de haut en bas)
            VStack(alignment: .leading, spacing: 8) {
                Text("VStack").font(.headline)
                Text("Titre de la carte")
                    .font(.title2)
                    .bold()
                Text("Sous-titre descriptif")
                    .foregroundStyle(.secondary)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)

            // HStack : empilage horizontal (de gauche à droite)
            HStack(spacing: 16) {
                Image(systemName: "star.fill")
                    .foregroundStyle(.yellow)
                    .font(.title)
                VStack(alignment: .leading) {
                    Text("HStack").font(.headline)
                    Text("Icône + texte côte à côte")
                        .foregroundStyle(.secondary)
                }
                Spacer()         // Pousse le contenu à gauche
                Text("→")
                    .font(.title2)
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)

            // ZStack : superposition (arrière-plan vers avant-plan)
            ZStack {
                // Couche 1 : fond (arrière)
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.indigo.gradient)
                    .frame(height: 100)

                // Couche 2 : texte (avant)
                VStack {
                    Text("ZStack").font(.headline).foregroundStyle(.white)
                    Text("Superposition de vues")
                        .font(.caption)
                        .foregroundStyle(.white.opacity(0.8))
                }
            }
        }
        .padding()
    }
}
```

<br>
![Conteneurs de Layout VStack HStack ZStack](/assets/images/swiftui/swiftui-layout-containers.png)
<br>

*`Spacer()` dans un `HStack` crée un espace flexible qui pousse les éléments de chaque côté. Dans un `VStack`, il pousse vers le bas ou vers le haut.*

<br>

### Paramètres d'Alignement

```swift title="Swift (SwiftUI) — Alignements disponibles pour chaque stack"
import SwiftUI

struct DémoAlignement: View {
    var body: some View {
        HStack(alignment: .top, spacing: 20) {

            // VStack avec différentes hauteurs
            VStack(alignment: .center) {   // .leading / .center / .trailing
                Text("Centre")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Rectangle()
                    .fill(Color.blue)
                    .frame(width: 60, height: 80)
            }

            VStack(alignment: .leading) {
                Text("Gauche")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Rectangle()
                    .fill(Color.green)
                    .frame(width: 60, height: 120)
            }

            VStack(alignment: .trailing) {
                Text("Droite")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Rectangle()
                    .fill(Color.orange)
                    .frame(width: 60, height: 60)
            }
        }
        // HStack aligné en haut : toutes les vues commencent au même niveau en haut
        // Valeurs : .top / .center / .bottom / .firstTextBaseline / .lastTextBaseline
    }
}
```

*`firstTextBaseline` aligne les éléments sur la baseline du premier texte — utile pour mélanger des polices de tailles différentes dans un `HStack`.*

<br>

---

## `Spacer` et `Divider`

```swift title="Swift (SwiftUI) — Spacer et Divider : contrôle de l'espace"
import SwiftUI

struct DémoEspacements: View {
    var body: some View {
        VStack {

            // Spacer dans VStack : pousse vers le bas
            Text("Haut de page")
            Spacer()
            Text("Bas de page")
        }
        .frame(height: 200)
        .border(Color.gray.opacity(0.3))

        // Spacer dans HStack : distribue l'espace
        HStack {
            Text("Gauche")
            Spacer()
            Text("Centre")
            Spacer()
            Text("Droite")
        }
        .padding()

        // Spacer avec taille minimale
        HStack {
            Text("Min 20pt")
            Spacer(minLength: 20)   // Au moins 20pt d'espace garanti
            Text("Valeur")
        }
        .padding()

        // Divider
        VStack {
            Text("Section 1")
            Divider()               // Ligne horizontale grisée
            Text("Section 2")
            Divider()
                .background(Color.indigo)  // Couleur personnalisée
            Text("Section 3")
        }
        .padding()
    }
}
```

<br>

---

## `frame` — Contrôle de la Taille

```swift title="Swift (SwiftUI) — frame : toutes les variantes"
import SwiftUI

struct DémoFrame: View {
    var body: some View {
        VStack(spacing: 20) {

            // Taille fixe
            Text("200 × 50")
                .frame(width: 200, height: 50)
                .background(Color.yellow)

            // Largeur maximale — s'étire sur toute la largeur
            Text("Pleine largeur")
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.mint)

            // Hauteur maximale — s'étire verticalement
            Text("Hauteur max dans container limité")
                .frame(maxHeight: .infinity)
                .frame(height: 80)      // Le container parent limite à 80
                .background(Color.orange)

            // Alignement dans le frame
            Text("Aligné à gauche")
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Color.purple.opacity(0.2))

            // Taille minimale et maximale
            Text("Entre 100 et 300 de large")
                .frame(minWidth: 100, maxWidth: 300)
                .padding()
                .background(Color.teal.opacity(0.3))
        }
        .padding()
    }
}
```

*`frame(maxWidth: .infinity)` est le pattern le plus utilisé en SwiftUI pour qu'une vue occupe toute la largeur disponible — équivalent de `width: 100%` en CSS.*

<br>

---

## Grilles avec `LazyVGrid` et `LazyHGrid`

Les grilles `Lazy` ne créent leurs cellules que lorsqu'elles deviennent visibles — essentielles pour les longues listes.

```swift title="Swift (SwiftUI) — LazyVGrid : grille verticale"
import SwiftUI

struct DémoGrid: View {

    // Données
    let couleurs: [Color] = [.red, .orange, .yellow, .green, .teal, .blue,
                              .indigo, .purple, .pink, .mint, .cyan, .brown]

    // Configuration des colonnes
    let colonnesFlexibles = [
        GridItem(.flexible),    // Largeur flexible (1/n de l'espace)
        GridItem(.flexible),
        GridItem(.flexible)
    ]

    let colonnesAdaptatives = [
        // .adaptive : crée autant de colonnes que possible avec min 80pt
        GridItem(.adaptive(minimum: 80))
    ]

    let colonnesFixesEtFlexibles = [
        GridItem(.fixed(60)),   // Largeur fixe : toujours 60pt
        GridItem(.flexible),    // S'étire pour remplir le reste
        GridItem(.fixed(60))
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 30) {

                Text("3 colonnes flexibles")
                    .font(.headline)
                    .padding(.horizontal)

                // Grille verticale à 3 colonnes flexibles
                LazyVGrid(columns: colonnesFlexibles, spacing: 12) {
                    ForEach(Array(couleurs.enumerated()), id: \.offset) { index, couleur in
                        RoundedRectangle(cornerRadius: 8)
                            .fill(couleur)
                            .frame(height: 60)
                            .overlay {
                                Text("\(index + 1)")
                                    .foregroundStyle(.white)
                                    .bold()
                            }
                    }
                }
                .padding(.horizontal)

                Text("Colonnes adaptatives (min 80pt)")
                    .font(.headline)
                    .padding(.horizontal)

                // Les colonnes s'ajustent automatiquement selon la largeur
                LazyVGrid(columns: colonnesAdaptatives, spacing: 8) {
                    ForEach(couleurs, id: \.self) { couleur in
                        RoundedRectangle(cornerRadius: 8)
                            .fill(couleur)
                            .frame(height: 60)
                    }
                }
                .padding(.horizontal)
            }
        }
    }
}
```

*`.adaptive(minimum:)` est idéal pour les galeries d'images — la grille adapte automatiquement le nombre de colonnes à la largeur disponible (différent entre iPhone et iPad).*

<br>

### `LazyVGrid` avec Données Réelles

```swift title="Swift (SwiftUI) — LazyVGrid avec modèle de données"
import SwiftUI

struct Photo: Identifiable {
    let id = UUID()
    let icône: String
    let titre: String
    let couleur: Color
}

struct GaleriePhotos: View {
    let photos: [Photo] = [
        Photo(icône: "mountain.2.fill",   titre: "Montagne", couleur: .teal),
        Photo(icône: "water.waves",        titre: "Mer",      couleur: .blue),
        Photo(icône: "sun.max.fill",       titre: "Soleil",   couleur: .orange),
        Photo(icône: "leaf.fill",          titre: "Forêt",    couleur: .green),
        Photo(icône: "snowflake",          titre: "Neige",    couleur: .cyan),
        Photo(icône: "flame.fill",         titre: "Désert",   couleur: .red),
    ]

    let colonnes = [GridItem(.adaptive(minimum: 150))]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: colonnes, spacing: 16) {
                ForEach(photos) { photo in
                    VStack(spacing: 8) {
                        Image(systemName: photo.icône)
                            .font(.system(size: 40))
                            .foregroundStyle(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 100)
                            .background(photo.couleur.gradient)
                            .cornerRadius(12)

                        Text(photo.titre)
                            .font(.caption)
                            .fontWeight(.medium)
                    }
                }
            }
            .padding()
        }
        .navigationTitle("Galerie")
    }
}
```

<br>

---

## `GeometryReader` — Dimensions Dynamiques

`GeometryReader` donne accès aux dimensions du conteneur parent. Utile pour les layouts qui dépendent de la taille de l'écran.

```swift title="Swift (SwiftUI) — GeometryReader pour les dimensions dynamiques"
import SwiftUI

struct DémoGeometryReader: View {
    var body: some View {
        VStack(spacing: 20) {

            // Barre de progression proportionnelle à la largeur disponible
            GeometryReader { geometry in
                // geometry.size.width : largeur disponible
                // geometry.size.height : hauteur disponible
                // geometry.frame(in: .global) : position dans l'écran complet

                ZStack(alignment: .leading) {
                    // Fond de la barre
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 20)

                    // Progression à 60%
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.indigo)
                        .frame(width: geometry.size.width * 0.6, height: 20)
                }
            }
            .frame(height: 20)  // Important : contraindre GeometryReader en hauteur

            Text("Barre à 60% de la largeur disponible")
                .font(.caption)
                .foregroundStyle(.secondary)

            // Disposition qui adapte le nombre de colonnes
            GeometryReader { geometry in
                let colonnes = geometry.size.width > 500 ? 3 : 2
                let item = GridItem(.flexible())
                let grille = Array(repeating: item, count: colonnes)

                LazyVGrid(columns: grille, spacing: 12) {
                    ForEach(0..<6, id: \.self) { index in
                        RoundedRectangle(cornerRadius: 8)
                            .fill(Color.indigo.opacity(0.7))
                            .frame(height: 80)
                            .overlay { Text("\(index + 1)").foregroundStyle(.white) }
                    }
                }
            }
            .frame(height: 200)
        }
        .padding()
    }
}
```

!!! warning "GeometryReader — Piège courant"
    `GeometryReader` consomme tout l'espace disponible (comme `Spacer()`). Contraignez-le toujours avec `.frame(height:)` ou placez-le dans un contexte où sa taille est déjà définie. Un `GeometryReader` non contraint dans un `VStack` peut faire exploser la mise en page.

<br>

---

## Layout Adaptatif — iPhone vs iPad

```swift title="Swift (SwiftUI) — Adapter le layout à la taille de l'écran"
import SwiftUI

struct LayoutAdaptatif: View {

    // Environnement : taille de classe de l'écran
    @Environment(\.horizontalSizeClass) var sizeClass

    var body: some View {
        // compact : iPhone portrait
        // regular : iPhone paysage, iPad
        if sizeClass == .compact {
            // Layout une colonne pour iPhone portrait
            VStack(spacing: 16) {
                CarteInfoPrincipale()
                ListeDetails()
            }
        } else {
            // Layout deux colonnes pour iPad / iPhone paysage
            HStack(spacing: 24) {
                CarteInfoPrincipale()
                    .frame(width: 300)
                ListeDetails()
            }
        }
    }
}

// Vues fictives pour l'exemple
struct CarteInfoPrincipale: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(Color.indigo.opacity(0.2))
            .frame(height: 200)
            .overlay { Text("Carte principale") }
    }
}

struct ListeDetails: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 16)
            .fill(Color.gray.opacity(0.1))
            .frame(maxWidth: .infinity)
            .frame(height: 200)
            .overlay { Text("Liste de détails") }
    }
}
```

*`@Environment(\.horizontalSizeClass)` est la méthode SwiftUI pour détecter si l'interface est en mode "compact" (iPhone portrait) ou "regular" (iPad, iPhone paysage). Préférez cette approche aux vérifications de modèle d'appareil.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Reproduire un layout**

```swift title="Swift — Exercice 1 : layout de carte app"
// Reproduisez cette mise en page :
//
// ┌──────────────────────────────┐
// │  ★★★★☆                    │  ← HStack (étoiles + note)
// │  Titre de l'application      │  ← Text bold
// │  Développeur - Catégorie     │  ← HStack (texte · séparateur · texte)
// │  ──────────────────────────  │  ← Divider
// │  [OBTENIR]    [PARTAGER ↑]   │  ← HStack (2 boutons, Spacer entre)
// └──────────────────────────────┘

struct CarteApp: View {
    let titreApp: String
    let développeur: String
    let note: Int       // 0 à 5
    let catégorie: String

    var body: some View {
        // TODO : implémenter
    }
}

#Preview {
    CarteApp(titreApp: "OmnyDocs", développeur: "OmnyVia", note: 4, catégorie: "Éducation")
        .padding()
}
```

**Exercice 2 — Grille de couleurs**

```swift title="Swift — Exercice 2 : galerie de couleurs responsive"
// Créez une galerie de 12 couleurs en LazyVGrid
// La grille doit s'adapter : 2 colonnes sur iPhone, 4 sur iPad
// Utilisez @Environment(\.horizontalSizeClass) ou GeometryReader
// Chaque cellule : fond coloré + nom de la couleur en haut

let paletteNoms = ["Rouge", "Orange", "Jaune", "Vert", "Menthe", "Cyan",
                   "Bleu", "Indigo", "Violet", "Rose", "Brun", "Gris"]
```

**Exercice 3 — Barre de progression animée**

```swift title="Swift — Exercice 3 : barre de progression avec GeometryReader"
// Créez une BarreProgression avec :
// - Un paramètre progression (Double entre 0.0 et 1.0)
// - Un fond gris arrondi
// - Une barre colorée proportionnelle au pourcentage (GeometryReader)
// - Un texte "X %" centré sur la barre

struct BarreProgression: View {
    let progression: Double      // 0.0 → 1.0
    let couleur: Color

    var body: some View {
        // TODO : utiliser GeometryReader pour la largeur proportionnelle
    }
}

#Preview {
    VStack(spacing: 16) {
        BarreProgression(progression: 0.75, couleur: .indigo)
        BarreProgression(progression: 0.40, couleur: .orange)
        BarreProgression(progression: 0.90, couleur: .green)
    }
    .padding()
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `VStack`, `HStack` et `ZStack` sont les trois containers fondamentaux — vertical, horizontal et superposé. `Spacer()` crée un espace flexible qui distribue l'espace résiduel. `frame(maxWidth: .infinity)` est le pattern pour occuper toute la largeur. `LazyVGrid` avec `.adaptive(minimum:)` produit des grilles qui s'adaptent à la largeur disponible — parfait pour l'iPhone et l'iPad avec le même code. `GeometryReader` donne accès aux dimensions du conteneur parent, mais doit toujours être contraint en taille pour éviter les comportements inattendus. Pour les layouts adaptatifs, `@Environment(\.horizontalSizeClass)` détecte compact vs regular.

> Dans le module suivant, nous abordons le cœur de la réactivité SwiftUI : **`@State` et `@Binding`** — comment créer une source de vérité locale et comment partager un état mutable entre une vue parent et ses enfants.

<br>
