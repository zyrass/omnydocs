---
description: "SwiftUI animations : withAnimation, Animation, .transition(), matchedGeometryEffect et micro-animations pour des interfaces vivantes."
icon: lucide/book-open-check
tags: ["SWIFTUI", "ANIMATION", "TRANSITION", "SPRING", "MATCHEDGEOMETRYEFFECT"]
---

# Animations & Transitions

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chorégraphe et les Danseurs"
    Un chorégraphe ne décrit pas chaque mouvement de bras ou de jambe — il dit "rejoignez la formation B depuis la formation A en 2 secondes, avec une décélération à la fin". Les danseurs calculent comment y arriver. SwiftUI fonctionne de même : vous dites "passe de cet état à cet autre état", et SwiftUI calcule automatiquement l'interpolation entre les deux — taille, position, opacité, couleur. `withAnimation { }` est l'instruction du chorégraphe. `Animation` est la description du mouvement (vitesse, rebond, délai).

Une animation en SwiftUI est la **différence visuelle entre deux états**. Il n'y a pas de code d'animation explicite — seulement un changement d'état et une instruction d'animation.

<br>

---

## `withAnimation` — Animer un Changement d'État

```swift title="Swift (SwiftUI) — withAnimation : animer tout changement d'état"
import SwiftUI

struct DémoAnimationsBase: View {

    @State private var estAffichée = false
    @State private var taille: CGFloat = 80
    @State private var couleur: Color = .indigo
    @State private var rotation: Double = 0

    var body: some View {
        VStack(spacing: 30) {

            // 1. Apparition / Disparition animée
            if estAffichée {
                RoundedRectangle(cornerRadius: 16)
                    .fill(couleur)
                    .frame(height: 80)
                    .transition(.opacity)  // Fondu
            }

            Button("Afficher / Masquer") {
                withAnimation(.easeInOut(duration: 0.4)) {
                    estAffichée.toggle()
                }
            }
            .buttonStyle(.bordered)

            Divider()

            // 2. Modification de propriétés animée
            Circle()
                .fill(couleur)
                .frame(width: taille, height: taille)
                .rotationEffect(.degrees(rotation))

            HStack(spacing: 12) {
                Button("Grandir") {
                    withAnimation(.spring(duration: 0.5, bounce: 0.4)) {
                        taille = 140
                        couleur = .orange
                    }
                }
                .buttonStyle(.bordered)

                Button("Réinitialiser") {
                    withAnimation(.spring(duration: 0.3)) {
                        taille = 80
                        couleur = .indigo
                        rotation = 0
                    }
                }
                .buttonStyle(.bordered)

                Button("Tourner") {
                    withAnimation(.linear(duration: 1).repeatForever(autoreverses: false)) {
                        rotation = 360
                    }
                }
                .buttonStyle(.bordered)
            }
        }
        .padding()
    }
}
```

*`withAnimation { }` capture toutes les modifications d'état dans son bloc et les anime. Sans `withAnimation`, les changements sont instantanés. L'animation s'applique à toutes les propriétés qui changent.*

<br>

---

## Les Types d'Animation

<br>
![Courbes de Temps d'Animation SwiftUI](/assets/images/swiftui/swiftui-animation-curves.png)
<br>

```swift title="Swift (SwiftUI) — Types d'animation et leur effet"
import SwiftUI

struct DémoTypesAnimation: View {

    @State private var décalage: CGFloat = 0

    var body: some View {
        VStack(spacing: 20) {

            // Ease In Out : lent au début et à la fin — usage général
            AnimationExemple(
                label: "easeInOut",
                décalage: $décalage
            ) {
                withAnimation(.easeInOut(duration: 0.6)) { décalage = 100 }
            }

            // Spring : rebond naturel — idéal pour les éléments interactifs
            AnimationExemple(
                label: "spring(bounce: 0.4)",
                décalage: $décalage
            ) {
                withAnimation(.spring(duration: 0.5, bounce: 0.4)) { décalage = 100 }
            }

            // Spring interpolating — courbe physique précise
            AnimationExemple(
                label: "spring bouncy",
                décalage: $décalage
            ) {
                withAnimation(.bouncy) { décalage = 100 }
            }

            // Linear : vitesse constante — pour les rotations continues
            AnimationExemple(
                label: "linear",
                décalage: $décalage
            ) {
                withAnimation(.linear(duration: 0.6)) { décalage = 100 }
            }

            Button("Réinitialiser tout") {
                withAnimation(.spring) { décalage = 0 }
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}

struct AnimationExemple: View {
    let label: String
    @Binding var décalage: CGFloat
    let action: () -> Void

    var body: some View {
        HStack {
            Text(label)
                .font(.caption)
                .frame(width: 150, alignment: .leading)
            Button("Lancer") { action() }
                .buttonStyle(.bordered)
                .font(.caption)
        }
    }
}
```

<br>

---

## `.animation(_:value:)` — Animation Implicite

Plutôt que `withAnimation`, vous pouvez attacher une animation directement à une vue.

```swift title="Swift (SwiftUI) — .animation(value:) : animation implicite sur la vue"
import SwiftUI

struct DémoAnimationImplicite: View {

    @State private var estActif = false
    @State private var nombreÉtoiles = 3

    var body: some View {
        VStack(spacing: 24) {

            // L'animation est attachée à la vue — se déclenche sur tout changement de estActif
            Circle()
                .fill(estActif ? Color.orange : Color.gray)
                .frame(width: estActif ? 120 : 60)
                .shadow(radius: estActif ? 12 : 0)
                // animation(_, value:) — s'anime quand estActif change
                .animation(.spring(duration: 0.5, bounce: 0.3), value: estActif)

            Button(estActif ? "Désactiver" : "Activer") {
                estActif.toggle()  // Pas de withAnimation nécessaire
            }
            .buttonStyle(.borderedProminent)

            Divider()

            // Affichage d'étoiles avec animation implicite
            HStack {
                ForEach(1...5, id: \.self) { index in
                    Image(systemName: index <= nombreÉtoiles ? "star.fill" : "star")
                        .foregroundStyle(index <= nombreÉtoiles ? .yellow : .gray)
                        .font(.title)
                        // Chaque étoile s'anime avec un délai croissant
                        .animation(
                            .spring(duration: 0.4).delay(Double(index) * 0.05),
                            value: nombreÉtoiles
                        )
                        .onTapGesture { nombreÉtoiles = index }
                }
            }
        }
        .padding()
    }
}
```

*`.animation(_:value:)` est préféré à `.animation(_:)` (déprécié iOS 15) car il spécifie précisément quelle valeur déclenche l'animation — évite les animations inattendues sur d'autres changements.*

<br>

---

## `.transition()` — Animations d'Apparition/Disparition

```swift title="Swift (SwiftUI) — .transition() pour les vues conditionnelles"
import SwiftUI

struct DémoTransitions: View {

    @State private var afficher = false

    var transitions: [(String, AnyTransition)] = [
        ("opacity",    .opacity),
        ("slide",      .slide),
        ("scale",      .scale),
        ("move top",   .move(edge: .top)),
        ("asymmetric", .asymmetric(insertion: .slide, removal: .opacity)),
    ]

    @State private var transitionSélectionnée: AnyTransition = .opacity
    @State private var nomTransition = "opacity"

    var body: some View {
        VStack(spacing: 20) {

            // Zone d'animation
            ZStack {
                Color.gray.opacity(0.1)
                    .cornerRadius(16)
                    .frame(height: 120)

                if afficher {
                    HStack(spacing: 12) {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundStyle(.green)
                            .font(.title)
                        Text("Transition : \(nomTransition)")
                            .font(.headline)
                    }
                    .transition(transitionSélectionnée)
                }
            }

            // Sélecteur
            ScrollView(.horizontal, showsIndicators: false) {
                HStack {
                    ForEach(transitions, id: \.0) { nom, transition in
                        Button(nom) {
                            afficher = false
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                                transitionSélectionnée = transition
                                nomTransition = nom
                                withAnimation(.spring(duration: 0.5)) {
                                    afficher = true
                                }
                            }
                        }
                        .buttonStyle(.bordered)
                        .font(.caption)
                    }
                }
                .padding(.horizontal)
            }

            Button("Basculer avec \(nomTransition)") {
                withAnimation(.spring(duration: 0.5)) {
                    afficher.toggle()
                }
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

*`.asymmetric(insertion:removal:)` permet d'avoir une animation différente à l'apparition et à la disparition — par exemple, glissant par le haut à l'entrée et disparaissant par fondu.*

<br>

---

## `matchedGeometryEffect` — Transitions de Héros

`matchedGeometryEffect` crée une animation "de héros" entre deux vues qui partagent le même identifiant — la vue semble se déplacer et transformer d'un état à l'autre.

```swift title="Swift (SwiftUI) — matchedGeometryEffect : animation de héros"
import SwiftUI

struct DémoHeroAnimation: View {

    @Namespace private var animation  // Espace de noms partagé
    @State private var élémentSélectionné: String? = nil

    let éléments = ["Swift", "SwiftUI", "Vapor", "Xcode"]

    var body: some View {
        VStack {
            if let sélection = élémentSélectionné {
                // Vue détail — grande
                VStack(spacing: 16) {
                    RoundedRectangle(cornerRadius: 20)
                        .fill(Color.indigo)
                        // matchedGeometryEffect : identifié par "rect-\(sélection)"
                        .matchedGeometryEffect(id: "rect-\(sélection)", in: animation)
                        .frame(height: 200)
                        .overlay {
                            Text(sélection)
                                .font(.largeTitle)
                                .bold()
                                .foregroundStyle(.white)
                                .matchedGeometryEffect(id: "text-\(sélection)", in: animation)
                        }

                    Button("Retour") {
                        withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
                            élémentSélectionné = nil
                        }
                    }
                    .buttonStyle(.bordered)
                }
                .frame(maxWidth: .infinity)
                .padding()

            } else {
                // Grille — petites vignettes
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())]) {
                    ForEach(éléments, id: \.self) { élément in
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.indigo.opacity(0.7))
                            .matchedGeometryEffect(id: "rect-\(élément)", in: animation)
                            .frame(height: 80)
                            .overlay {
                                Text(élément)
                                    .foregroundStyle(.white)
                                    .font(.headline)
                                    .matchedGeometryEffect(id: "text-\(élément)", in: animation)
                            }
                            .onTapGesture {
                                withAnimation(.spring(duration: 0.5, bounce: 0.3)) {
                                    élémentSélectionné = élément
                                }
                            }
                    }
                }
                .padding()
            }
        }
    }
}
```

*`@Namespace` crée un espace partagé pour les identifiants de `matchedGeometryEffect`. Les deux vues (source et destination) doivent partager **le même namespace** et **le même id** pour que l'animation fonctionne.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Bouton Like animé**

```swift title="Swift — Exercice 1 : bouton favori avec animation"
// Créez un BoutonFavori avec :
// - Un cœur vide → rempli au tap
// - Animation spring avec scale (grandit puis revient)
// - Particules ou burst simulé (cercle qui s'agrandit et disparaît)
// - Compteur de likes animé (update du nombre avec withAnimation)

struct BoutonFavori: View {
    @State private var aimé = false
    @State private var compteur = 42

    var body: some View {
        // TODO
        EmptyView()
    }
}
```

**Exercice 2 — Liste avec animation d'insertion**

```swift title="Swift — Exercice 2 : liste avec animations"
// Créez une liste de tâches où :
// - L'ajout d'une tâche glisse depuis le bas (.slide ou .move(edge: .bottom))
// - La suppression s'efface avec .opacity
// - La completion (✓) anime la couleur et le style barré

struct ListeAnimée: View {
    @State private var tâches: [String] = ["Tâche 1", "Tâche 2", "Tâche 3"]
    @State private var nouvelleTâche = ""

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
    Une animation SwiftUI est la **différence entre deux états** — vous changez l'état, SwiftUI interpole visuellement. `withAnimation { }` enveloppe le changement d'état pour l'animer. `.animation(_:value:)` attache l'animation à une vue spécifique et se déclenche sur une valeur précise. `.transition()` contrôle l'apparence et disparition des vues conditionnelles dans `if/else`. `.spring(bounce:)` produit les animations les plus naturelles pour les éléments interactifs. `matchedGeometryEffect` crée des animations de héros entre deux vues en les liant par un identifiant partagé. Pour les interfaces premium, préférez `.spring()` à `.easeInOut()` — les rebonds sont plus vivants et naturels.

> Dans le module suivant, nous abordons `ViewModifier` et les Extensions — comment créer vos propres modificateurs réutilisables, factoriser le code visuel et construire une bibliothèque de composants cohérents.

<br>
