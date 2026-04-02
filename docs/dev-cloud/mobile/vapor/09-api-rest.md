---
description: "Vapor API REST complète : DTOs, versioning, validation centralisée, pagination, gestion d'erreurs uniformes et structure en couches."
icon: lucide/book-open-check
tags: ["VAPOR", "API-REST", "DTO", "VERSIONING", "ARCHITECTURE", "PRODUCTION"]
---

# API REST Complète

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Manuel Technique d'un Avion"
    Un avion de ligne a des systèmes redondants, des procédures normalisées, des codes de panne standardisés. Les pilotes du monde entier utilisent les mêmes termes, les mêmes codes (`MAYDAY`, codes HTTP). Une API REST professionnelle suit des conventions similaires : codes HTTP sémantiques, réponses d'erreur structurées, nommage cohérent, versioning. Quand votre client iOS reçoit une réponse JSON, il sait exactement quoi en faire — parce que vous avez respecté les conventions. Une API incohérente, c'est un avion avec des instruments différents à chaque vol.

Ce module assemble tous les concepts précédents en une **architecture API complète**, prête pour la production.

<br>

---

## Structure d'un Projet Vapor en Production

```
Sources/App/
├── Controllers/
│   ├── Auth/
│   │   └── AuthController.swift        ← Inscription, connexion, refresh
│   └── API/
│       ├── ArticleController.swift     ← CRUD articles + pagination
│       └── UtilisateurController.swift ← Profil, préférences
│
├── Models/                             ← Modèles Fluent (ex: Article, Utilisateur)
│
├── DTOs/                               ← ⭐ Séparation modèles ↔ API
│   ├── Requests/                       ← Corps de requête (ce qu'on reçoit)
│   │   ├── CréerArticleRequest.swift
│   │   └── ModifierArticleRequest.swift
│   └── Responses/                      ← Corps de réponse (ce qu'on retourne)
│       ├── ArticleResponse.swift
│       └── PageResponse.swift
│
├── Middlewares/                        ← Middlewares personnalisés
│   ├── JWTMiddleware.swift
│   └── RateLimitMiddleware.swift
│
├── Services/                           ← ⭐ Logique métier hors des contrôleurs
│   └── ArticleService.swift
│
├── Migrations/                         ← Migrations Fluent
├── configure.swift
└── routes.swift
```

*Séparer les **DTOs** des **Modèles** est la règle fondamentale d'une API robuste : le modèle Fluent est la représentation en base de données, le DTO est le contrat avec le client. Ils changent indépendamment — le modèle peut évoluer sans casser le contrat API.*

<br>

---

## DTOs Complets : Request & Response

```swift title="Swift (Vapor) — DTOs : contrat explicite entre l'API et le client"
import Vapor

// ─── REQUEST DTOs (ce que le client envoie) ───────────────────────────────────

struct CréerArticleRequest: Content, Validatable {
    let titre: String
    let contenu: String
    let catégorie: String
    let publié: Bool?       // Optionnel — false par défaut
    let tagIds: [UUID]?     // Optionnel — tags à attacher

    static func validations(_ validations: inout Validations) {
        validations.add("titre",     as: String.self, is: !.empty && .count(3...200))
        validations.add("contenu",   as: String.self, is: !.empty && .count(10...))
        validations.add("catégorie", as: String.self, is: .in("swift", "swiftui", "vapor", "ios", "divers"))
    }
}

struct ModifierArticleRequest: Content, Validatable {
    let titre: String?              // Tous les champs optionnels (PATCH sémantique)
    let contenu: String?
    let catégorie: String?
    let publié: Bool?

    static func validations(_ validations: inout Validations) {
        // Valider uniquement si les champs sont présents
        validations.add("titre",   as: String.self, is: .count(3...200), required: false)
        validations.add("contenu", as: String.self, is: .count(10...),   required: false)
    }
}

// ─── RESPONSE DTOs (ce que l'API retourne) ────────────────────────────────────

struct ArticleBaseResponse: Content {
    let id: UUID
    let titre: String
    let catégorie: String
    let publié: Bool
    let créeA: Date
    let modifiéA: Date?
}

struct ArticleCompleteResponse: Content {
    let id: UUID
    let titre: String
    let contenu: String
    let catégorie: String
    let publié: Bool
    let créeA: Date
    let auteur: AuteurResponse
    let tags: [TagResponse]
}

struct AuteurResponse: Content {
    let id: UUID
    let prénom: String
    // Note : email et hash absents — principe du moindre privilège
}

struct TagResponse: Content {
    let id: UUID
    let nom: String
}

// Mapper un modèle Fluent vers un DTO de réponse
extension Article {
    func toBaseResponse() throws -> ArticleBaseResponse {
        guard let id = self.id else { throw Abort(.internalServerError) }
        return ArticleBaseResponse(
            id:        id,
            titre:     self.titre,
            catégorie: self.catégorie,
            publié:    self.publié,
            créeA:     self.créeA ?? Date(),
            modifiéA:  self.modifiéA
        )
    }
}
```

<br>

---

## Service Layer — Extraire la Logique Métier

```swift title="Swift (Vapor) — ArticleService : logique métier isolée et testable"
import Vapor
import Fluent

// Le service isole la logique métier — les contrôleurs ne font qu'orchestrer
// Avantage : testable indépendamment des routes HTTP
final class ArticleService {

    let db: Database

    init(db: Database) { self.db = db }

    // Créer un article
    func créer(_ dto: CréerArticleRequest, auteurId: UUID) async throws -> Article {
        let article = Article(
            titre:     dto.titre,
            contenu:   dto.contenu,
            catégorie: dto.catégorie,
            publié:    dto.publié ?? false,
            auteurId:  auteurId
        )
        try await article.save(on: db)

        // Attacher les tags si fournis
        if let tagIds = dto.tagIds, !tagIds.isEmpty {
            let tags = try await Tag.query(on: db).filter(\.$id ~~ tagIds).all()
            try await article.$tags.attach(tags, on: db)
        }

        return article
    }

    // Lister avec filtres et pagination
    func lister(
        catégorie: String?  = nil,
        publiéSeulement: Bool = true,
        page: Int = 1,
        par: Int = 20
    ) async throws -> (articles: [Article], total: Int) {

        var query = Article.query(on: db)
            .with(\.$auteur)
            .with(\.$tags)

        if publiéSeulement {
            query = query.filter(\.$publié == true)
        }

        if let cat = catégorie {
            query = query.filter(\.$catégorie == cat)
        }

        let total = try await query.count()
        let articles = try await query
            .sort(\.$créeA, .descending)
            .offset((page - 1) * par)
            .limit(par)
            .all()

        return (articles, total)
    }

    // Mettre à jour partiellement (PATCH)
    func modifier(_ article: Article, avec dto: ModifierArticleRequest) async throws -> Article {
        if let titre     = dto.titre     { article.titre     = titre }
        if let contenu   = dto.contenu   { article.contenu   = contenu }
        if let catégorie = dto.catégorie { article.catégorie = catégorie }
        if let publié    = dto.publié    { article.publié    = publié }

        try await article.save(on: db)
        return article
    }
}

// Extension Request pour accéder au service
extension Request {
    var articleService: ArticleService { ArticleService(db: self.db) }
}
```

<br>

---

## Contrôleur API v1 — Complet

```swift title="Swift (Vapor) — ArticleController v1 : CRUD + pagination + auth"
import Vapor
import Fluent

final class ArticleController: RouteCollection {

    func boot(routes: RoutesBuilder) throws {
        // Routes publiques : lire uniquement
        let public_ = routes.grouped("api", "v1", "articles")
        public_.get(use: lister)
        public_.get(":id", use: lire)

        // Routes authentifiées : écriture
        let protected_ = public_.grouped(JWTMiddleware())
        protected_.post(use: créer)
        protected_.patch(":id", use: modifier)
        protected_.delete(":id", use: supprimer)
    }

    // GET /api/v1/articles?page=1&par=20&catégorie=swift
    @Sendable
    func lister(req: Request) async throws -> PageResponse<ArticleBaseResponse> {
        struct Query: Content {
            var page:      Int?
            var par:       Int?
            var catégorie: String?
        }
        let q   = try req.query.decode(Query.self)
        let page = max(1, q.page ?? 1)
        let par  = min(50, max(1, q.par ?? 20))

        let (articles, total) = try await req.articleService.lister(
            catégorie:       q.catégorie,
            publiéSeulement: true,
            page:            page,
            par:             par
        )

        return PageResponse(
            données: try articles.map { try $0.toBaseResponse() },
            total:   total,
            page:    page,
            par:     par
        )
    }

    // GET /api/v1/articles/:id
    @Sendable
    func lire(req: Request) async throws -> ArticleCompleteResponse {
        let id = try req.parameters.require("id", as: UUID.self)

        guard let article = try await Article.query(on: req.db)
            .with(\.$auteur)
            .with(\.$tags)
            .filter(\.$id == id)
            .filter(\.$publié == true)
            .first() else {
            throw Abort(.notFound, reason: "Article introuvable")
        }

        return ArticleCompleteResponse(
            id:        article.id!,
            titre:     article.titre,
            contenu:   article.contenu,
            catégorie: article.catégorie,
            publié:    article.publié,
            créeA:     article.créeA!,
            auteur:    AuteurResponse(id: article.auteur.id!, prénom: article.auteur.prénom),
            tags:      article.tags.map { TagResponse(id: $0.id!, nom: $0.nom) }
        )
    }

    // POST /api/v1/articles
    @Sendable
    func créer(req: Request) async throws -> Response {
        let payload = try req.utilisateurJWTRequis()

        try CréerArticleRequest.validate(content: req)
        let dto = try req.content.decode(CréerArticleRequest.self)

        guard let auteurId = UUID(uuidString: payload.sub.value) else {
            throw Abort(.internalServerError)
        }

        let article = try await req.articleService.créer(dto, auteurId: auteurId)
        let réponse = try article.toBaseResponse()

        return try await réponse.encodeResponse(status: .created, for: req)
    }

    // PATCH /api/v1/articles/:id
    @Sendable
    func modifier(req: Request) async throws -> ArticleBaseResponse {
        let payload = try req.utilisateurJWTRequis()
        let id      = try req.parameters.require("id", as: UUID.self)

        guard let article = try await Article.find(id, on: req.db) else {
            throw Abort(.notFound)
        }

        // Seul l'auteur ou un admin peut modifier
        guard article.$auteur.id.uuidString == payload.sub.value || payload.rôle == "admin" else {
            throw Abort(.forbidden, reason: "Vous ne pouvez modifier que vos articles")
        }

        try ModifierArticleRequest.validate(content: req)
        let dto = try req.content.decode(ModifierArticleRequest.self)
        let articleModifié = try await req.articleService.modifier(article, avec: dto)
        return try articleModifié.toBaseResponse()
    }

    // DELETE /api/v1/articles/:id
    @Sendable
    func supprimer(req: Request) async throws -> HTTPStatus {
        let payload = try req.utilisateurJWTRequis()
        let id      = try req.parameters.require("id", as: UUID.self)

        guard let article = try await Article.find(id, on: req.db) else {
            throw Abort(.notFound)
        }

        guard article.$auteur.id.uuidString == payload.sub.value || payload.rôle == "admin" else {
            throw Abort(.forbidden)
        }

        try await article.delete(on: req.db)
        return .noContent
    }
}

// ─── PageResponse générique ───────────────────────────────────────────────────
struct PageResponse<T: Content>: Content {
    let données: [T]
    let total: Int
    let page: Int
    let par: Int
    var totalPages: Int { Int(ceil(Double(total) / Double(par))) }
}
```

<br>

---

## Versioning — Plusieurs Versions en Parallèle

```swift title="Swift (Vapor) — Versioning : /api/v1 et /api/v2 en parallèle"
import Vapor

func routes(_ app: Application) throws {

    // Les deux versions coexistent — v1 n'est pas supprimée
    let v1 = app.grouped("api", "v1")
    let v2 = app.grouped("api", "v2")

    // V1 : réponses minimalistes
    try v1.register(collection: ArticleController())

    // V2 : réponses enrichies (nouvelles fonctionnalités)
    // try v2.register(collection: ArticleControllerV2())

    // Route de découverte : l'API informe des versions disponibles
    app.get("api") { req async -> APIInfoResponse in
        APIInfoResponse(
            versions:    ["v1"],
            versionActuelle: "v1",
            documentation: "https://docs.omnyvia.com/api"
        )
    }
}

struct APIInfoResponse: Content {
    let versions: [String]
    let versionActuelle: String
    let documentation: String
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — TagController CRUD complet**

```swift title="Swift (Vapor) — Exercice 1 : TagController avec service layer"
// Créez TagController + TagService avec la structure en couches :
// GET    /api/v1/tags           → liste tous les tags (avec count d'articles pour chaque)
// GET    /api/v1/tags/:id/articles → articles associés à ce tag, paginés
// POST   /api/v1/tags           → créer (auth admin uniquement)
// DELETE /api/v1/tags/:id       → supprimer (admin + seulement si 0 articles associés)

struct TagAvecCompteResponse: Content {
    let id: UUID
    let nom: String
    let nbArticles: Int
}

final class TagService {
    let db: Database
    init(db: Database) { self.db = db }
    // TODO
}
```

**Exercice 2 — Erreurs uniformes**

```swift title="Swift (Vapor) — Exercice 2 : ErrorMiddleware personnalisé"
// Créez un ErrorMiddlewarePersonnalisé qui intercèpte toutes les erreurs
// et retourne TOUJOURS un JSON structuré :
// {
//   "erreur": true,
//   "code": "RESSOURCE_INTROUVABLE",
//   "message": "Article introuvable",
//   "statusHTTP": 404,
//   "timestamp": "2026-04-03T..."
// }

struct ErreurAPIResponse: Content {
    let erreur: Bool
    let code: String
    let message: String
    let statusHTTP: UInt
    let timestamp: String
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Séparer **DTOs** (contrat API) et **Modèles** (base de données) est la règle numéro un d'une API robuste — ils évoluent indépendamment. Le **Service Layer** extrait la logique métier des contrôleurs — les contrôleurs orchestrent, les services implémentent. Le versioning `/api/v1` est à mettre en place dès le début — le refaire après coup coûte cher. Les `PageResponse<T>` génériques évitent de dupliquer le code de pagination pour chaque ressource. La vérification de **propriété** (l'auteur peut modifier son article, l'admin peut tout modifier) doit se faire dans le Contrôleur ou le Service — jamais en base de données uniquement.

> Dans le module suivant, nous abordons les **Queues & Jobs** — exécuter des tâches en arrière-plan (emails, rapport PDF, nettoyage) sans bloquer les réponses HTTP.

<br>
