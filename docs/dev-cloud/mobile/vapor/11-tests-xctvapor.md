---
description: "Vapor Tests XCTVapor : configurer un environnement de test, tester les routes HTTP, les middlewares et les contrôleurs avec XCTVapor."
icon: lucide/book-open-check
tags: ["VAPOR", "TESTS", "XCTVAPOR", "XCTEST", "TDD", "QUALITE"]
---

# Tests XCTVapor

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Double de Test en Crash Test"
    Avant de commercialiser une voiture, les ingénieurs la crashent contre un mur — pas la voiture de série, mais un double de test identique. Ils mesurent les déformations, vérifient les airbags, valident que la structure protège les occupants. XCTVapor est votre "double de test" : il lance votre application Vapor dans un mode de test avec une base de données SQLite en mémoire, exécute de vraies requêtes HTTP contre les vraies routes, et vous permet de mesurer exactement ce que votre API retourne. Pas de mocking de HTTP — de vraies requêtes contre votre vraie stack.

XCTVapor est le framework de test officiel de Vapor — il exécute votre application complète (routes, middlewares, DB) dans un contexte de test isolé.

<br>

---

## Configuration de l'Environnement de Test

```swift title="Swift (Vapor) — configure.swift : mode test avec SQLite in-memory"
import Fluent
import FluentSQLiteDriver
import Vapor

public func configure(_ app: Application) async throws {

    // ─── Base de données selon l'environnement ─────────────────────
    switch app.environment {
    case .testing:
        // In-memory : chaque test repart d'une base vide et propre
        // Aucun fichier créé — isolation parfaite entre les tests
        app.databases.use(.sqlite(.memory), as: .sqlite)

    case .development:
        app.databases.use(.sqlite(.file("dev.sqlite")), as: .sqlite)

    case .production:
        // PostgreSQL en production (voir Module 05)
        break

    default:
        app.databases.use(.sqlite(.memory), as: .sqlite)
    }

    // Migrations : identiques quel que soit l'environnement
    app.migrations.add(CreateUtilisateur())
    app.migrations.add(CreateArticle())
    app.migrations.add(CreateRefreshToken())

    try await app.autoMigrate()
    try routes(app)
}
```

<br>

---

## Structure d'un Test XCTVapor

```swift title="Swift (Vapor) — Structure de base d'un test XCTVapor"
import XCTest
import XCTVapor
@testable import App

// Classe de test — correspond à une ressource ou un contrôleur
final class ArticleControllerTests: XCTestCase {

    // app : l'application Vapor dans le mode test
    var app: Application!

    // setUp : appelé avant CHAQUE test — réinitialise l'app
    override func setUp() async throws {
        try await super.setUp()

        // Créer une nouvelle application en mode .testing
        app = try await Application.make(.testing)

        // Configurer l'app (routes, DB in-memory, migrations)
        try await configure(app)
    }

    // tearDown : appelé après CHAQUE test — libère les ressources
    override func tearDown() async throws {
        // Annuler les migrations (réinitialise la DB in-memory)
        try await app.autoRevert()

        // Arrêter l'application proprement
        try await app.asyncShutdown()
        try await super.tearDown()
    }
}
```

*`autoRevert()` dans `tearDown()` annule toutes les migrations — ainsi chaque test commence avec une base de données **vide et propre**. C'est l'isolation parfaite : un test ne peut pas influencer un autre.*

<br>

---

## Tester les Routes — `XCTVapor`

```swift title="Swift (Vapor) — Tester des routes GET et POST avec XCTVapor"
import XCTest
import XCTVapor
@testable import App

final class ArticleControllerTests: XCTestCase {
    var app: Application!
    // setUp/tearDown comme ci-dessus

    // ─── Test GET /api/v1/articles ─────────────────────────────────
    func test_listerArticles_retourneListeVide() async throws {
        // When : requête GET sans données en DB
        try await app.test(.GET, "api/v1/articles") { response in

            // Then : 200 OK
            XCTAssertEqual(response.status, .ok)

            // Then : le JSON contient une liste vide
            let réponse = try response.content.decode(PageResponse<ArticleBaseResponse>.self)
            XCTAssertEqual(réponse.données.count, 0)
            XCTAssertEqual(réponse.total, 0)
        }
    }

    // ─── Test POST /api/v1/articles ────────────────────────────────
    func test_créerArticle_sansAuth_retourne401() async throws {
        let corps = CréerArticleRequest(
            titre:     "Titre test",
            contenu:   "Contenu de test suffisamment long",
            catégorie: "swift",
            publié:    false,
            tagIds:    nil
        )

        try await app.test(.POST, "api/v1/articles") { requête in
            // Encoder le corps JSON
            try requête.content.encode(corps)
        } afterResponse: { response in
            // Sans token → 401 Unauthorized
            XCTAssertEqual(response.status, .unauthorized)
        }
    }

    // ─── Test POST /api/v1/articles avec auth ─────────────────────
    func test_créerArticle_avecAuth_retourne201() async throws {
        // Given : créer un utilisateur + obtenir un token
        let token = try await créerUtilisateurEtObtenirToken()

        let corps = CréerArticleRequest(
            titre:     "Test Vapor Queues",
            contenu:   "Contenu détaillé de l'article de test pour Vapor",
            catégorie: "vapor",
            publié:    true,
            tagIds:    nil
        )

        try await app.test(.POST, "api/v1/articles") { requête in
            // Ajouter le header Authorization
            requête.headers.bearerAuthorization = .init(token: token)
            try requête.content.encode(corps)
        } afterResponse: { response in
            // 201 Created
            XCTAssertEqual(response.status, .created)

            let article = try response.content.decode(ArticleBaseResponse.self)
            XCTAssertEqual(article.titre, "Test Vapor Queues")
            XCTAssertEqual(article.catégorie, "vapor")
            XCTAssertTrue(article.publié)
            XCTAssertNotNil(article.id)
        }
    }

    // ─── Test GET /api/v1/articles/:id — non trouvé ────────────────
    func test_lireArticle_idInexistant_retourne404() async throws {
        let idInexistant = UUID()
        try await app.test(.GET, "api/v1/articles/\(idInexistant)") { response in
            XCTAssertEqual(response.status, .notFound)
        }
    }

    // ─── Test DELETE — ownership ────────────────────────────────────
    func test_supprimerArticle_autreUtilisateur_retourne403() async throws {
        // Given : Alice crée un article
        let tokenAlice = try await créerUtilisateurEtObtenirToken(email: "alice@test.com")
        let articleId   = try await créerArticle(token: tokenAlice)

        // Given : Bob se connecte
        let tokenBob = try await créerUtilisateurEtObtenirToken(email: "bob@test.com")

        // When : Bob essaie de supprimer l'article d'Alice
        try await app.test(.DELETE, "api/v1/articles/\(articleId)") { req in
            req.headers.bearerAuthorization = .init(token: tokenBob)
        } afterResponse: { response in
            // Then : 403 Forbidden
            XCTAssertEqual(response.status, .forbidden)
        }
    }
}
```

<br>

---

## Helpers de Test — Factoriser le Code Commun

```swift title="Swift (Vapor) — Helpers : éviter la duplication dans les tests"
import XCTest
import XCTVapor
@testable import App

// Extension pour les helpers communs à tous les tests
extension XCTestCase {

    // Créer un utilisateur et retourner son JWT
    func créerUtilisateurEtObtenirToken(
        email: String = "test@example.com",
        sur app: Application
    ) async throws -> String {

        // Inscription via l'API
        var accessToken = ""

        try await app.test(.POST, "auth/inscription") { req in
            try req.content.encode(InscriptionDTO(
                prénom:      "Test",
                email:       email,
                motDePasse:  "Test1234!"
            ))
        } afterResponse: { response in
            XCTAssertEqual(response.status, .created)
            let réponse = try response.content.decode(TokenRéponse.self)
            accessToken = réponse.accessToken
        }

        return accessToken
    }

    // Créer un article et retourner son UUID
    func créerArticle(
        token: String,
        titre: String = "Article de test",
        sur app: Application
    ) async throws -> UUID {

        var articleId = UUID()

        try await app.test(.POST, "api/v1/articles") { req in
            req.headers.bearerAuthorization = .init(token: token)
            try req.content.encode(CréerArticleRequest(
                titre:     titre,
                contenu:   "Contenu détaillé suffisamment long pour la validation",
                catégorie: "swift",
                publié:    true,
                tagIds:    nil
            ))
        } afterResponse: { response in
            XCTAssertEqual(response.status, .created)
            let article = try response.content.decode(ArticleBaseResponse.self)
            articleId = article.id!
        }

        return articleId
    }
}
```

<br>

---

## Tester les Middlewares et l'Authentification

```swift title="Swift (Vapor) — Tests du flow d'authentification complet"
import XCTest
import XCTVapor
@testable import App

final class AuthControllerTests: XCTestCase {
    var app: Application!
    // setUp/tearDown...

    func test_inscription_avecEmailValide_retourne201() async throws {
        try await app.test(.POST, "auth/inscription") { req in
            try req.content.encode(InscriptionDTO(
                prénom:     "Alice",
                email:      "alice@test.com",
                motDePasse: "Pass1234!"
            ))
        } afterResponse: { response in
            XCTAssertEqual(response.status, .created)

            let réponse = try response.content.decode(TokenRéponse.self)
            XCTAssertFalse(réponse.accessToken.isEmpty)
            XCTAssertFalse(réponse.refreshToken.isEmpty)
            XCTAssertEqual(réponse.expireEn, 900)
        }
    }

    func test_inscription_avecEmailDéjàUtilisé_retourne409() async throws {
        // Given : un premier utilisateur créé
        _ = try await créerUtilisateurEtObtenirToken(email: "double@test.com", sur: app)

        // When : tenter de s'inscrire avec le même email
        try await app.test(.POST, "auth/inscription") { req in
            try req.content.encode(InscriptionDTO(
                prénom:     "Autre",
                email:      "double@test.com",
                motDePasse: "Pass1234!"
            ))
        } afterResponse: { response in
            // Then : 409 Conflict
            XCTAssertEqual(response.status, .conflict)
        }
    }

    func test_connexion_motDePasseErroné_retourne401() async throws {
        // Given : utilisateur créé
        _ = try await créerUtilisateurEtObtenirToken(email: "alice@test.com", sur: app)

        // When : connexion avec mauvais mot de passe
        try await app.test(.POST, "auth/connexion") { req in
            try req.content.encode(ConnexionDTO(email: "alice@test.com", motDePasse: "Wrong!"))
        } afterResponse: { response in
            // Then : 401 — même message que "email inexistant"
            XCTAssertEqual(response.status, .unauthorized)
        }
    }

    func test_refresh_avecTokenValide_retourneNouveauToken() async throws {
        // Given : inscription → refresh token
        var refreshToken = ""
        try await app.test(.POST, "auth/inscription") { req in
            try req.content.encode(InscriptionDTO(prénom: "Alice", email: "alice@test.com", motDePasse: "Pass1234!"))
        } afterResponse: { response in
            let réponse = try response.content.decode(TokenRéponse.self)
            refreshToken = réponse.refreshToken
        }

        // When : rafraîchir avec le refresh token
        try await app.test(.POST, "auth/refresh") { req in
            try req.content.encode(RefreshDTO(refreshToken: refreshToken))
        } afterResponse: { response in
            XCTAssertEqual(response.status, .ok)
            let réponse = try response.content.decode(TokenRéponse.self)
            XCTAssertFalse(réponse.accessToken.isEmpty)
        }
    }
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Suite de tests CRUD complète**

```swift title="Swift (Vapor) — Exercice 1 : tester le CRUD complet des articles"
// Écrivez les tests manquants pour ArticleController :
// - test_listerArticles_après3Créés_retourneTotal3
// - test_lireArticle_publiéExistant_retourneArticleComplet
// - test_lireArticle_nonPublié_retourne404 (les non-publiés ne sont pas accessibles publiquement)
// - test_modifierArticle_parSonAuteur_retourne200AvecModifs
// - test_modifierArticle_champInvalide_retourne400
// - test_supprimerArticle_parSonAuteur_retourne204
// - test_listerArticles_avecFiltreCategorie_retourneSeulementCetteCategorie

final class ArticleControllerTestsComplets: XCTestCase {
    var app: Application!
    // setUp/tearDown...

    func test_listerArticles_après3Créés_retourneTotal3() async throws {
        // TODO
    }

    // ... autres tests
}
```

**Exercice 2 — Test du middleware de rate limiting**

```swift title="Swift (Vapor) — Exercice 2 : tester le rate limiting"
// Testez RateLimitMiddleware :
// - Faites N requêtes successives sur la même IP
// - Vérifiez que la N+1ème retourne 429 Too Many Requests
// - Vérifiez que les headers X-RateLimit-Remaining décroissent correctement
// Note : configurez la limite à 5 pour les tests (limite de test)

final class RateLimitMiddlewareTests: XCTestCase {
    var app: Application!

    func test_rateLimiting_auDelàDeLaLimite_retourne429() async throws {
        // TODO : effectuer 6 requêtes, vérifier que la 6ème est 429
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    XCTVapor exécute votre **vraie application** en mode test — pas de mocking HTTP. `Application.make(.testing)` + `configure()` démarre l'app avec la DB en mémoire. `setUp` crée une app propre, `tearDown` + `autoRevert()` + `asyncShutdown()` la réinitialise complètement entre chaque test. `app.test(.METHODE, "chemin")` exécute une vraie requête HTTP — avec corps, headers, et vérifie la réponse. Les **helpers** (`créerUtilisateurEtObtenirToken`, `créerArticle`) évitent la duplication — factoriser dans `XCTestCase` extension. Suivre le pattern **Given / When / Then** pour des tests lisibles et maintenables.

> Dans le dernier module de cette formation, nous couvrons le **Déploiement** — Docker, Railway, Render, variables d'environnement, migrations en production et HTTPS.

<br>
