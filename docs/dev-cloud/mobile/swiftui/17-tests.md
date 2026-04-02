---
description: "SwiftUI tests : #Preview, PreviewProvider, tester les ViewModels avec XCTest et les bonnes pratiques de testabilité."
icon: lucide/book-open-check
tags: ["SWIFTUI", "TESTS", "XCTEST", "PREVIEW", "TESTABILITE"]
---

# Tests

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Filet de Sécurité du Funambule"
    Un funambule professionnel évolue sur son câble avec un filet de sécurité sous lui. Ce filet ne l'empêche pas de tomber — mais il limite les conséquences et lui permet de tenter des figures plus audacieuses. Les tests sont ce filet. Ils n'empêchent pas les bugs, mais ils les détectent avant que l'utilisateur final ne les rencontre, et ils vous donnent la confiance de refactoriser sans craindre de tout casser.

Une architecture MVVM (module 13) est la condition pour des tests efficaces en SwiftUI : les ViewModels sont testables sans interface, sans Simulateur, sans interactions manuelles.

<br>

---

## `#Preview` vs `PreviewProvider`

```swift title="Swift (SwiftUI) — #Preview (iOS 17) vs PreviewProvider (iOS 16)"
import SwiftUI

struct CartArticle: View {
    let titre: String
    let auteur: String
    let estNouveauté: Bool

    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(titre).font(.headline)
                Text(auteur).font(.caption).foregroundStyle(.secondary)
            }
            Spacer()
            if estNouveauté {
                Text("Nouveau")
                    .font(.caption2)
                    .padding(.horizontal, 8).padding(.vertical, 4)
                    .background(Color.orange.opacity(0.15))
                    .foregroundStyle(.orange)
                    .clipShape(Capsule())
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.06), radius: 6, x: 0, y: 3)
    }
}

// ═══════════════════════════════════════════
// iOS 17+ : macro #Preview — concise
// ═══════════════════════════════════════════

#Preview("Nouveauté") {
    CartArticle(titre: "Introduction à SwiftUI", auteur: "Alice", estNouveauté: true)
        .padding()
}

#Preview("Normal") {
    CartArticle(titre: "Async/Await", auteur: "Bob", estNouveauté: false)
        .padding()
}

#Preview("Dark Mode") {
    CartArticle(titre: "MVVM Pattern", auteur: "Alice", estNouveauté: true)
        .padding()
        .preferredColorScheme(.dark)
}

// ═══════════════════════════════════════════
// iOS 16 : PreviewProvider — plus verbeux
// ═══════════════════════════════════════════

struct CartArticle_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            CartArticle(titre: "Introduction à SwiftUI", auteur: "Alice", estNouveauté: true)
                .padding()
                .previewDisplayName("Nouveauté")

            CartArticle(titre: "Async/Await", auteur: "Bob", estNouveauté: false)
                .padding()
                .previewDisplayName("Normal")
                .preferredColorScheme(.dark)
                .previewDisplayName("Dark Mode")
        }
    }
}
```

*Les deux syntaxes sont compatibles en iOS 17+ — `PreviewProvider` n'est pas déprécié. La macro `#Preview` est plus concise et supporte les closures `async`.*

<br>

---

## `@Previewable` — État dans les Previews (iOS 17)

```swift title="Swift (SwiftUI) — @Previewable : @State dans les previews sans wrapper"
import SwiftUI

struct BoutonTogglePremium: View {
    @Binding var actif: Bool
    let label: String

    var body: some View {
        Button(action: { actif.toggle() }) {
            Label(label, systemImage: actif ? "checkmark.circle.fill" : "circle")
                .foregroundStyle(actif ? .indigo : .secondary)
        }
        .buttonStyle(.plain)
    }
}

// iOS 17+ : @Previewable permet d'avoir @State directement dans #Preview
// Sans avoir besoin d'une vue wrapper
#Preview {
    @Previewable @State var estActif = false

    VStack(spacing: 20) {
        BoutonTogglePremium(actif: $estActif, label: "Activer les notifications")
        Text("État : \(estActif ? "Actif" : "Inactif")")
    }
    .padding()
}

// iOS 16 : besoin d'une vue wrapper pour avoir @State dans les previews
struct BoutonTogglePremium_Wrapper: View {
    @State private var actif = false

    var body: some View {
        BoutonTogglePremium(actif: $actif, label: "Activer les notifications")
    }
}

struct BoutonTogglePremium_Previews: PreviewProvider {
    static var previews: some View {
        BoutonTogglePremium_Wrapper()
    }
}
```

<br>

---

## Tester les ViewModels avec XCTest

Les ViewModels MVVM (module 13) sont testables sans SwiftUI — pur Swift, pas de Simulateur requis.

```swift title="Swift — XCTest : tester un ViewModel sans SwiftUI"
import XCTest
@testable import OmnyDocs

// ─── ViewModel à tester ────────────────────────────

@MainActor
@Observable
final class ArticleViewModelTestable {
    var articles: [Article] = []
    var erreur: String? = nil
    var estEnChargement = false
    var filtreFavori = false

    private let service: ArticleServiceProtocol

    init(service: ArticleServiceProtocol) {
        self.service = service
    }

    var articlesFiltres: [Article] {
        filtreFavori ? articles.filter { $0.estFavori } : articles
    }

    func charger() async {
        estEnChargement = true
        do {
            articles = try await service.récupérerArticles()
        } catch {
            self.erreur = error.localizedDescription
        }
        estEnChargement = false
    }

    func basculerFavori(_ article: Article) {
        guard let index = articles.firstIndex(where: { $0.id == article.id }) else { return }
        articles[index].estFavori.toggle()
    }
}

// ─── Tests ─────────────────────────────────────────

class ArticleViewModelTests: XCTestCase {

    var viewModel: ArticleViewModelTestable!
    var serviceMock: ArticleServiceMock!

    @MainActor
    override func setUp() {
        super.setUp()
        serviceMock = ArticleServiceMock()
        viewModel = ArticleViewModelTestable(service: serviceMock)
    }

    // Test 1 : le chargement remplit les articles
    @MainActor
    func test_charger_remplitLesArticles() async {
        // Given : viewModel vide
        XCTAssertTrue(viewModel.articles.isEmpty)

        // When : charger
        await viewModel.charger()

        // Then : les articles sont présents
        XCTAssertFalse(viewModel.articles.isEmpty)
        XCTAssertEqual(viewModel.articles.count, Article.exemples.count)
    }

    // Test 2 : l'indicateur de chargement est actif pendant le chargement
    @MainActor
    func test_charger_indicateurActifPuisInactif() async {
        // Note : on ne peut pas vérifier l'état PENDANT le chargement
        // sans async streams — on vérifie avant et après
        XCTAssertFalse(viewModel.estEnChargement)
        await viewModel.charger()
        XCTAssertFalse(viewModel.estEnChargement)
    }

    // Test 3 : basculer favori fonctionne
    @MainActor
    func test_basculerFavori_changeLÉtat() async {
        await viewModel.charger()
        guard let premierArticle = viewModel.articles.first else {
            XCTFail("Aucun article chargé")
            return
        }

        let étaInitial = premierArticle.estFavori
        viewModel.basculerFavori(premierArticle)

        XCTAssertEqual(viewModel.articles.first?.estFavori, !étaInitial)
    }

    // Test 4 : le filtre favori retourne uniquement les favoris
    @MainActor
    func test_filtreFavori_retourneSeulementLesFavoris() async {
        await viewModel.charger()

        // Marquer le premier article comme favori
        if let premier = viewModel.articles.first {
            viewModel.basculerFavori(premier)
        }

        // Activer le filtre
        viewModel.filtreFavori = true

        // Vérifier que seuls les favoris sont retournés
        XCTAssertTrue(viewModel.articlesFiltres.allSatisfy { $0.estFavori })
        XCTAssertEqual(viewModel.articlesFiltres.count, 1)
    }

    // Test 5 : erreur réseau gérée
    @MainActor
    func test_charger_avecErreurRéseau_définitLErreur() async {
        // Utiliser un mock qui échoue
        viewModel = ArticleViewModelTestable(service: ArticleServiceEchecMock())
        await viewModel.charger()

        XCTAssertNotNil(viewModel.erreur)
        XCTAssertTrue(viewModel.articles.isEmpty)
    }
}
```

<br>

---

## Stratégies de Testabilité SwiftUI

```swift title="Swift — Bonnes pratiques de testabilité SwiftUI"
import SwiftUI

// ═══════════════════════════════════════════
// 1. Extraire la logique dans des fonctions pures
// ═══════════════════════════════════════════

// ❌ Logique dans la Vue — non testable
struct VueNonTestable: View {
    var body: some View {
        let articles = ["A", "B", "C"]
        let filtrés = articles.filter { $0 != "B" }  // Logique impossible à tester
        Text("\(filtrés.count) articles")
    }
}

// ✅ Logique dans le ViewModel — testable
@Observable
final class VMTestable {
    var articles = ["A", "B", "C"]
    var articlesFiltres: [String] { articles.filter { $0 != "B" } }
}

struct VueTestable: View {
    @State private var vm = VMTestable()
    var body: some View {
        Text("\(vm.articlesFiltres.count) articles")
    }
}

// ═══════════════════════════════════════════
// 2. Préférer des previews par état
// ═══════════════════════════════════════════

// Créer des previews qui couvrent tous les états possibles
#Preview("Chargement") {
    VueStatut(état: .chargement)
}

#Preview("Succès — 0 articles") {
    VueStatut(état: .succès([]))
}

#Preview("Succès — plusieurs articles") {
    VueStatut(état: .succès(Article.exemples))
}

#Preview("Erreur") {
    VueStatut(état: .erreur("Connexion impossible"))
}

// Vue d'exemple pour les previews par état
struct VueStatut: View {
    let état: ÉtatChargement<[Article]>

    var body: some View {
        switch état {
        case .inactif:   Text("Inactif")
        case .chargement: ProgressView("Chargement...")
        case .succès(let articles): Text("\(articles.count) articles")
        case .erreur(let msg): Text("Erreur : \(msg)").foregroundStyle(.red)
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Previews exhaustifs**

```swift title="Swift — Exercice 1 : couvrir tous les états avec des previews"
// Pour votre VueListeArticles du module 13, créez des previews pour :
// 1. État de chargement (simuler avec Task.sleep + ProgressView)
// 2. Liste avec articles (mock avec données)
// 3. Liste vide (mock sans données)
// 4. Erreur de chargement (mock qui throws)
// 5. Mode sombre + Dynamic Type Large
// 6. Mode sombre + iPad (device: "iPad Pro 11-inch")

#Preview("...") {
    // TODO
}
```

**Exercice 2 — Tests du ViewModel**

```swift title="Swift — Exercice 2 : tests XCTest complets"
// Rédigez les tests seguants pour votre ViewModelTâches (exercice 1 du module 13) :
// 1. test_ajouterTâche_augmenteLaListe
// 2. test_supprimerTâche_réduitLaListe
// 3. test_tâchesFiltres_avecFiltrePrioriteHaute_retourneSeulementHaute
// 4. test_basculerFaite_inverseLÉtat
// 5. test_rechercheTexte_filtreParTitre
// Chaque test doit avoir : Given / When / Then clairement séparés

class TâcheViewModelTests: XCTestCase {
    // TODO
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    La macro `#Preview` (iOS 17) remplace `PreviewProvider` avec une syntaxe plus concise — supportant les closures async et `@Previewable @State`. Créez des previews pour **chaque état** de votre vue (chargement, vide, rempli, erreur, dark mode, accessibilité) — c'est votre filet de sécurité visuel. Les tests XCTest des ViewModels testent la **logique métier** sans SwiftUI, sans Simulateur, en millisecondes. L'architecture MVVM est la condition préalable : la Vue ne contient que de l'affichage, toute logique testable est dans le ViewModel. `@MainActor` sur le ViewModel est nécessaire avec `async/await` dans les tests — annotez vos méthodes de test ou la classe entière.

> Dans le module final, nous abordons la **Publication sur l'App Store** — Signing & Capabilities, Provisioning Profiles, Archive, TestFlight, App Review et la Privacy Nutrition Label.

<br>
