---
description: "Vapor Routing : paramètres de chemin, query parameters, groupes, RouteCollection et organisation des routes d'une API."
icon: lucide/book-open-check
tags: ["VAPOR", "ROUTING", "ROUTES", "CONTROLEUR", "ROUTECOLLECTION"]
---

# Routing

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Aiguilleur de Gare"
    Dans une grande gare, un aiguilleur oriente chaque train vers le bon quai selon sa destination et son type (TGV, régional, fret). Il ne s'occupe pas du contenu des wagons — seulement de l'orientation. Le routeur Vapor fait exactement cela : il examine chaque requête HTTP (méthode + chemin), l'oriente vers le bon handler, sans jamais traiter lui-même les données. Un routeur précis évite les confusions : GET `/articles` (lire tous) n'est pas la même chose que DELETE `/articles/42` (supprimer le numéro 42).

Le routing est le cœur de toute API. Il définit **quel code s'exécute** pour quelle combinaison méthode HTTP + chemin URL.

<br>

---

## Routes Basiques — Les Méthodes HTTP

```swift title="Swift (Vapor) — routes.swift : les méthodes HTTP fondamentales"
import Vapor

func routes(_ app: Application) throws {

    // ─── GET ───────────────────────────────────────────────────────
    // Lire des données — ne modifie rien
    app.get("articles") { req async throws -> [Article] in
        // Retourne tous les articles (voir Fluent en M05)
        []
    }

    // ─── POST ──────────────────────────────────────────────────────
    // Créer une ressource — corps JSON requis
    app.post("articles") { req async throws -> Article in
        let données = try req.content.decode(CréerArticleDTO.self)
        // Créer et sauvegarder (voir Fluent en M05)
        return Article(titre: données.titre)
    }

    // ─── PUT ───────────────────────────────────────────────────────
    // Remplacer complètement une ressource
    app.put("articles", ":id") { req async throws -> Article in
        guard let id = req.parameters.get("id") else {
            throw Abort(.badRequest, reason: "ID manquant")
        }
        let données = try req.content.decode(CréerArticleDTO.self)
        // Mettre à jour (voir Fluent)
        return Article(titre: données.titre)
    }

    // ─── PATCH ─────────────────────────────────────────────────────
    // Modifier partiellement une ressource
    app.patch("articles", ":id") { req async throws -> Article in
        // Modification partielle — seulement les champs fournis
        Article(titre: "Titre modifié")
    }

    // ─── DELETE ────────────────────────────────────────────────────
    // Supprimer une ressource — retourne 204 No Content
    app.delete("articles", ":id") { req async throws -> HTTPStatus in
        guard let id = req.parameters.get("id") else {
            throw Abort(.badRequest)
        }
        // Supprimer (voir Fluent)
        return .noContent   // 204 — succès sans corps de réponse
    }
}

// DTOs (Data Transfer Objects) — séparés des modèles de base de données
struct Article: Content {
    var id: UUID?
    let titre: String
}

struct CréerArticleDTO: Content {
    let titre: String
    let contenu: String
}
```

*La convention REST : `GET /ressources` (liste), `GET /ressources/:id` (un), `POST /ressources` (créer), `PUT /ressources/:id` (remplacer), `PATCH /ressources/:id` (modifier), `DELETE /ressources/:id` (supprimer).*

<br>

---

## Paramètres de Chemin

```swift title="Swift (Vapor) — Paramètres de chemin avec req.parameters"
import Vapor

func routes(_ app: Application) throws {

    // Paramètre simple : :id
    // Chemin : /utilisateurs/42
    app.get("utilisateurs", ":id") { req async throws -> String in

        // req.parameters.get("id") → String? (le nom correspond au :id dans le chemin)
        guard let idStr = req.parameters.get("id") else {
            throw Abort(.badRequest, reason: "Paramètre 'id' manquant")
        }
        return "Utilisateur demandé : \(idStr)"
    }

    // Paramètre typé : Vapor convertit automatiquement String → type cible
    // Chemin : /articles/7
    app.get("articles", ":articleId") { req async throws -> String in

        // get("nom", as: Int.self) : conversion automatique + erreur 400 si invalide
        let articleId = try req.parameters.require("articleId", as: Int.self)
        return "Article numéro \(articleId)"
    }

    // Paramètre UUID : très courant avec Fluent (UUID = clé primaire)
    // Chemin : /notes/550e8400-e29b-41d4-a716-446655440000
    app.get("notes", ":noteId") { req async throws -> String in

        // UUID : Vapor valide le format — 400 si invalide
        let noteId = try req.parameters.require("noteId", as: UUID.self)
        return "Note UUID : \(noteId)"
    }

    // Chemin imbriqué : /auteurs/5/articles/12
    app.get("auteurs", ":auteurId", "articles", ":articleId") { req async throws -> String in
        let auteurId = try req.parameters.require("auteurId", as: Int.self)
        let articleId = try req.parameters.require("articleId", as: Int.self)
        return "Article \(articleId) de l'auteur \(auteurId)"
    }
}
```

*`req.parameters.require("nom", as: Type.self)` combine la récupération et la conversion — il lance automatiquement une `Abort(.badRequest)` si le paramètre est absent ou si la conversion échoue. À préférer à `req.parameters.get("nom")`.*

<br>

---

## Query Parameters

```swift title="Swift (Vapor) — Query parameters : filtres, pagination, tri"
import Vapor

// Requête : GET /articles?page=2&limit=10&titre=swift&tri=date
app.get("articles") { req async throws -> [Article] in

    // Lire un query parameter — nil si absent
    let page: Int = req.query["page"] ?? 1
    let limite: Int = req.query["limit"] ?? 20
    let tri: String = req.query["tri"] ?? "date"

    // Lire et valider avec un type — throws si invalide
    // (ex: ?limit=abc → erreur 400)

    // Décoder tous les query params en un struct Decodable
    struct FiltreArticles: Content {
        let page: Int?
        let limit: Int?
        let titre: String?    // Recherche textuelle
        let tri: String?
    }

    let filtre = try req.query.decode(FiltreArticles.self)

    // Utiliser les paramètres pour filtrer
    let pageUtilisée = filtre.page ?? 1
    let limiteUtilisée = min(filtre.limit ?? 20, 100)  // Maximum 100 par page

    return []  // Retour fictif — voir Fluent
}
```

*`req.query.decode(MonStruct.self)` est la pratique recommandée pour les APIs avec plusieurs paramètres optionnels — elle offre une validation et une documentation implicite des paramètres acceptés.*

<br>

---

## Groupes de Routes

Les groupes permettent de factoriser un préfixe de chemin commun ou un middleware.

```swift title="Swift (Vapor) — Groupes de routes : préfixes et middlewares"
import Vapor

func routes(_ app: Application) throws {

    // ─── Groupe par préfixe ─────────────────────────────────────────
    // Toutes les routes du groupe auront le préfixe /api/v1
    let apiV1 = app.grouped("api", "v1")

    apiV1.get("articles") { req async throws -> String in
        "GET /api/v1/articles"
    }

    apiV1.post("articles") { req async throws -> String in
        "POST /api/v1/articles"
    }

    // ─── Groupe imbriqué ────────────────────────────────────────────
    // /api/v1/utilisateurs
    let utilisateurs = apiV1.grouped("utilisateurs")
    utilisateurs.get { req async -> String in "GET /api/v1/utilisateurs" }
    utilisateurs.get(":id") { req async -> String in
        let id = req.parameters.get("id") ?? "?"
        return "GET /api/v1/utilisateurs/\(id)"
    }

    // ─── Groupe avec middleware ─────────────────────────────────────
    // Les routes de ce groupe nécessitent une authentification (voir M08)
    let protégé = apiV1.grouped(UserAuthMiddleware())

    protégé.get("profil") { req async throws -> String in
        "Profil de l'utilisateur authentifié"
    }

    protégé.delete("compte") { req async throws -> HTTPStatus in
        .noContent
    }

    // ─── Enregistrer les contrôleurs ───────────────────────────────
    try app.register(collection: ArticleController())
}

// Middleware factice pour l'exemple
struct UserAuthMiddleware: AsyncMiddleware {
    func respond(to request: Request, chainingTo next: AsyncResponder) async throws -> Response {
        // Vérification du token (voir Module 08)
        return try await next.respond(to: request)
    }
}
```

<br>

---

## `RouteCollection` — Contrôleurs Organisés

Pour les applications réelles, les routes sont groupées dans des **contrôleurs** qui implémentent `RouteCollection`.

```swift title="Swift (Vapor) — RouteCollection : contrôleur complet pour une ressource"
import Vapor

// ArticleController : gère toutes les routes liées aux articles
// RouteCollection : protocol qui oblige à implémenter boot(routes:)
final class ArticleController: RouteCollection {

    // boot(routes:) : appelé par app.register(collection:)
    // C'est ici qu'on déclare toutes les routes du contrôleur
    func boot(routes: RoutesBuilder) throws {

        // Groupe : toutes les routes de ce contrôleur auront le préfixe /articles
        let articles = routes.grouped("articles")

        // Enregistrer chaque handler
        articles.get(use: lister)          // GET  /articles
        articles.post(use: créer)          // POST /articles
        articles.get(":id", use: lire)     // GET  /articles/:id
        articles.put(":id", use: modifier) // PUT  /articles/:id
        articles.delete(":id", use: supprimer) // DELETE /articles/:id
    }

    // ─── Handlers ──────────────────────────────────────────────────

    // Lister tous les articles
    @Sendable
    func lister(req: Request) async throws -> [ArticleRéponse] {
        // En vrai : Article.query(on: req.db).all()
        [
            ArticleRéponse(id: UUID(), titre: "Introduction à Vapor", auteur: "Alice"),
            ArticleRéponse(id: UUID(), titre: "Fluent ORM",            auteur: "Bob"),
        ]
    }

    // Créer un article
    @Sendable
    func créer(req: Request) async throws -> ArticleRéponse {
        // Valider et décoder le corps de la requête
        try CréerArticleÉtenduDTO.validate(content: req)  // Validation des champs
        let dto = try req.content.decode(CréerArticleÉtenduDTO.self)

        // En vrai : créer le modèle + article.save(on: req.db)
        return ArticleRéponse(id: UUID(), titre: dto.titre, auteur: dto.auteur)
    }

    // Lire un article par ID
    @Sendable
    func lire(req: Request) async throws -> ArticleRéponse {
        guard let id = req.parameters.get("id", as: UUID.self) else {
            throw Abort(.badRequest, reason: "ID invalide")
        }
        // En vrai : Article.find(id, on: req.db)
        return ArticleRéponse(id: id, titre: "Article trouvé", auteur: "Alice")
    }

    // Modifier un article
    @Sendable
    func modifier(req: Request) async throws -> ArticleRéponse {
        guard let id = req.parameters.get("id", as: UUID.self) else {
            throw Abort(.badRequest)
        }
        let dto = try req.content.decode(CréerArticleÉtenduDTO.self)
        return ArticleRéponse(id: id, titre: dto.titre, auteur: dto.auteur)
    }

    // Supprimer un article
    @Sendable
    func supprimer(req: Request) async throws -> HTTPStatus {
        guard req.parameters.get("id", as: UUID.self) != nil else {
            throw Abort(.badRequest)
        }
        // En vrai : article.delete(on: req.db)
        return .noContent
    }
}

// ─── DTOs et types de réponse ─────────────────────────────────────────────

struct ArticleRéponse: Content {
    let id: UUID?
    let titre: String
    let auteur: String
}

struct CréerArticleÉtenduDTO: Content, Validatable {
    let titre: String
    let auteur: String
    let contenu: String

    // Validatable : déclare les règles de validation de Vapor
    static func validations(_ validations: inout Validations) {
        validations.add("titre",   as: String.self, is: !.empty && .count(3...200))
        validations.add("auteur",  as: String.self, is: !.empty)
        validations.add("contenu", as: String.self, is: !.empty)
    }
}
```

*`@Sendable` sur les handlers est nécessaire avec Swift 6 Strict Concurrency — il garantit que le handler est sûr à passer entre les threads de SwiftNIO.*

<br>

---

## Erreurs HTTP avec `Abort`

```swift title="Swift (Vapor) — Lancer des erreurs HTTP avec Abort"
import Vapor

app.get("articles", ":id") { req async throws -> ArticleRéponse in

    guard let id = req.parameters.get("id", as: UUID.self) else {
        // 400 Bad Request : paramètre malformé
        throw Abort(.badRequest, reason: "L'ID doit être un UUID valide")
    }

    // Simuler un article non trouvé
    let articleTrouvé = false

    guard articleTrouvé else {
        // 404 Not Found : ressource inexistante
        throw Abort(.notFound, reason: "Article \(id) introuvable")
    }

    // 403 Forbidden : accès refusé
    // throw Abort(.forbidden, reason: "Accès non autorisé")

    // 500 Internal Server Error : erreur inattendue
    // throw Abort(.internalServerError)

    return ArticleRéponse(id: id, titre: "Article", auteur: "Alice")
}
```

*Vapor transforme automatiquement les `Abort` en réponses JSON : `{"error": true, "reason": "Article introuvable"}` avec le code HTTP approprié. Votre client iOS recevra le bon status code et peut adapter son affichage.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — API de livres**

```swift title="Swift (Vapor) — Exercice 1 : RouteCollection pour une ressource Livre"
// Créez un LivreController avec RouteCollection :
// GET    /livres           → liste tous les livres (données statiques)
// GET    /livres/:id       → retourne un livre par UUID
// POST   /livres           → créer un livre (titre, auteur, isbn)
// DELETE /livres/:id       → supprimer (retourne 204)
//
// Ajoutez la validation Validatable sur le DTO de création :
// - titre : non vide, 2-200 caractères
// - isbn  : exactement 13 caractères

struct Livre: Content {
    var id: UUID?
    let titre: String
    let auteur: String
    let isbn: String
}

final class LivreController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        // TODO
    }
    // TODO : handlers
}
```

**Exercice 2 — Pagination et filtres**

```swift title="Swift (Vapor) — Exercice 2 : query parameters avec validation"
// Ajoutez à LivreController une route GET /livres/recherche avec :
// - ?q=swift              → filtre sur le titre (insensible à la casse)
// - ?auteur=alice         → filtre sur l'auteur
// - ?page=1&limit=5       → pagination (limit max : 50)
// - Retourne { "résultats": [...], "total": N, "page": N }

struct RésultatPaginé<T: Content>: Content {
    let résultats: [T]
    let total: Int
    let page: Int
    let parPage: Int
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Vapor route chaque requête selon la combinaison **méthode HTTP + chemin**. `req.parameters.require("nom", as: Type.self)` récupère et convertit les paramètres de chemin avec erreur automatique. `req.query.decode(MonStruct.self)` est le pattern recommandé pour les query parameters multiples. Les groupes (`app.grouped("préfixe")`) factorisent le chemin et les middlewares. `RouteCollection` organise les routes d'une ressource dans un contrôleur dédié — la convention de tout projet Vapor structuré. `Abort(.statusCode, reason: "...")` produit des réponses d'erreur JSON cohérentes.

> Dans le module suivant, nous approfondissons la **Request et la Response** — décoder le corps JSON, les Content types, les headers, les cookies et la construction de réponses personnalisées.

<br>
