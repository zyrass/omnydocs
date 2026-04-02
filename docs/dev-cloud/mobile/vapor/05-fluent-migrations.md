---
description: "Vapor Fluent ORM : définir des modèles, créer des migrations versionnées, configurer SQLite et PostgreSQL."
icon: lucide/book-open-check
tags: ["VAPOR", "FLUENT", "ORM", "MIGRATIONS", "SQLITE", "POSTGRESQL"]
---

# Fluent & Migrations

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="3-4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Plans d'Architecte Versionnés"
    Un architecte ne remodèle pas un bâtiment en rasant tout. Il crée des plans modificatifs successifs : plan v1 (structure de base), plan v2 (ajout d'une mezzanine), plan v3 (cloison déplacée). Chaque plan est daté, numéroté, et ne peut être appliqué qu'après le précédent. Les **migrations Fluent** fonctionnent exactement ainsi : chaque migration décrit une transformation du schéma de base de données. Elles s'appliquent dans l'ordre, une seule fois, et sont traçables. Si l'équipe grandit, chacun peut rejoindre le projet et reconstruire la base complète en exécutant `autoMigrate()`.

Fluent est l'**ORM** (Object-Relational Mapper) de Vapor. Il permet de définir les tables de base de données en Swift, d'écrire des requêtes type-safe, et de faire évoluer le schéma via des migrations.

<br>

---

## Architecture Fluent

```mermaid
flowchart LR
    subgraph Swift["🔷 Code Swift"]
        Model["@Model\nArticle.swift"]
        Migration["Migration\nCreateArticle.swift"]
        Query["Article.query(on: db)\n.filter(...)"]
    end

    subgraph Fluent["⚙️ Fluent ORM"]
        Driver["Driver\n(SQLite ou PostgreSQL)"]
    end

    subgraph DB["🗄️ Base de données"]
        Table["TABLE articles\n(id, titre, contenu, créeA)"]
    end

    Migration -->|"CREATE TABLE"| Driver
    Query -->|"SELECT / INSERT / UPDATE"| Driver
    Driver --> DB
    Model -.->|"mappe les colonnes"| Table
```

<br>

---

## Premier Modèle Fluent

```swift title="Swift (Vapor) — Modèle Fluent : définir une table en Swift"
import Fluent
import Vapor

// final class Article : class (pas struct) — Fluent requiert des classes
// Model : protocol Fluent principal — définit la correspondance Swift ↔ Table SQL
final class Article: Model, Content, @unchecked Sendable {

    // schema : nom de la table SQL (convention : pluriel, minuscules, underscores)
    static let schema = "articles"

    // ─── Propriétés ───────────────────────────────────────────────

    // @ID : clé primaire — UUID est la valeur par défaut recommandée
    // .generateUUID : UUID généré automatiquement à la création
    @ID(key: .id)
    var id: UUID?

    // @Field : colonne SQL ordinaire
    // key: "titre" → nom de la colonne dans la base de données
    @Field(key: "titre")
    var titre: String

    @Field(key: "contenu")
    var contenu: String

    @Field(key: "auteur")
    var auteur: String

    // @OptionalField : colonne nullable (NULL autorisé dans SQL)
    @OptionalField(key: "résumé")
    var résumé: String?

    // @Timestamp : colonne de date gérée automatiquement par Fluent
    // .create : remplie au INSERT, jamais modifiée ensuite
    // .update : mise à jour à chaque UPDATE
    @Timestamp(key: "créé_à",    on: .create)
    var créeA: Date?

    @Timestamp(key: "modifié_à", on: .update)
    var modifiéA: Date?

    // Initialiser vide requis par Fluent pour le décodage depuis la DB
    init() { }

    // Initialiser avec valeurs — pour la création dans les handlers
    init(id: UUID? = nil, titre: String, contenu: String, auteur: String, résumé: String? = nil) {
        self.id      = id
        self.titre   = titre
        self.contenu = contenu
        self.auteur  = auteur
        self.résumé  = résumé
    }
}
```

*`@unchecked Sendable` est nécessaire sur les classes Fluent avec Swift 6 Strict Concurrency — Fluent gère lui-même la sécurité des threads via son propre système. Les `@Field` correspondent aux colonnes SQL — le `key:` est le nom exact de la colonne.*

<br>

---

## Migrations — Versionner le Schéma

```swift title="Swift (Vapor) — Migration : CreateArticle crée la table"
import Fluent

// CreateArticle : migration qui crée la table "articles"
// AsyncMigration : version async du protocol Migration
struct CreateArticle: AsyncMigration {

    // prepare : appliqué lors de l'exécution (création de table, ajout de colonne, etc.)
    func prepare(on database: any Database) async throws {
        try await database.schema("articles")
            // Colonnes de la table — correspondent aux @Field du modèle
            .id()                                       // Colonne "id" UUID PRIMARY KEY
            .field("titre",      .string, .required)    // VARCHAR NOT NULL
            .field("contenu",    .string, .required)    // TEXT NOT NULL
            .field("auteur",     .string, .required)    // VARCHAR NOT NULL
            .field("résumé",     .string)               // VARCHAR NULL (optionnel)
            .field("créé_à",     .datetime)             // DATETIME
            .field("modifié_à",  .datetime)             // DATETIME
            .create()                                   // Exécute CREATE TABLE
    }

    // revert : défait la migration (en cas de rollback)
    func revert(on database: any Database) async throws {
        try await database.schema("articles").delete()  // DROP TABLE
    }
}

// Migration d'évolution : ajouter une colonne "publié" à une table existante
struct AjouterPubliéÀArticle: AsyncMigration {

    func prepare(on database: any Database) async throws {
        try await database.schema("articles")
            .field("publié", .bool, .required, .sql(.default(false)))  // default false
            .update()   // ALTER TABLE (pas create)
    }

    func revert(on database: any Database) async throws {
        try await database.schema("articles")
            .deleteField("publié")
            .update()
    }
}
```

*Les migrations sont **idempotentes** — Fluent mémorise lesquelles ont déjà été exécutées dans une table `_fluent_migrations`. `autoMigrate()` dans `configure.swift` les applique automatiquement au démarrage, sans ré-exécuter celles déjà faites.*

<br>

---

## Enregistrer les Migrations dans `configure.swift`

```swift title="Swift (Vapor) — configure.swift : enregistrement des migrations"
import Fluent
import FluentSQLiteDriver
import Vapor

public func configure(_ app: Application) async throws {

    // ─── Base de données SQLite ─────────────────────────────────────
    app.databases.use(
        .sqlite(.file("data.sqlite")),  // Fichier persistant
        as: .sqlite
    )

    // ─── Migrations dans l'ordre chronologique ──────────────────────
    // L'ordre est CRITIQUE — une migration ne peut pas dépendre d'une table
    // qui n'a pas encore été créée par une migration précédente
    app.migrations.add(CreateArticle())              // Étape 1 : table articles
    app.migrations.add(CreateUtilisateur())          // Étape 2 : table utilisateurs
    app.migrations.add(AjouterPubliéÀArticle())      // Étape 3 : modifier articles

    // ─── Exécuter les migrations au démarrage ──────────────────────
    // Fluent compare les migrations enregistrées avec celles déjà exécutées
    // Seules les nouvelles sont appliquées
    try await app.autoMigrate()

    try routes(app)
}
```

<br>

---

## Passer à PostgreSQL

!!! tip "SQLite → PostgreSQL"
    Le code des modèles et migrations est **identique** entre SQLite et PostgreSQL. Seule la configuration du driver change dans `configure.swift`.

```swift title="Swift (Vapor) — Passer de SQLite à PostgreSQL"
// Package.swift : remplacer le driver SQLite
// .package(url: "https://github.com/vapor/fluent-sqlite-driver.git", ...),
// par :
// .package(url: "https://github.com/vapor/fluent-postgres-driver.git", from: "2.8.0"),

// configure.swift : remplacer la configuration de la base de données
import FluentPostgresDriver

public func configure(_ app: Application) async throws {

    // Option 1 : connexion via URL (recommandée pour production)
    let dbURL = Environment.get("DATABASE_URL") ?? "postgres://localhost/omnyapi"
    try app.databases.use(.postgres(url: dbURL), as: .psql)

    // Option 2 : connexion via paramètres individuels
    app.databases.use(.postgres(
        hostname: Environment.get("DB_HOST")     ?? "localhost",
        port:     Int(Environment.get("DB_PORT") ?? "5432") ?? 5432,
        username: Environment.get("DB_USER")     ?? "postgres",
        password: Environment.get("DB_PASSWORD") ?? "",
        database: Environment.get("DB_NAME")     ?? "omnyapi"
    ), as: .psql)

    // Les migrations restent IDENTIQUES — aucun changement
    app.migrations.add(CreateArticle())

    try await app.autoMigrate()
    try routes(app)
}
```

```bash title="Terminal — Lancer PostgreSQL avec Docker pour le développement"
# Démarrer PostgreSQL en conteneur Docker
docker run --name omnyapi-db \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=omnyapi \
    -p 5432:5432 \
    -d postgres:16

# Vérifier que le conteneur tourne
docker ps

# Dans votre terminal de développement :
DATABASE_URL=postgres://postgres:secret@localhost/omnyapi swift run
```

<br>

---

## Opérations CRUD de Base

```swift title="Swift (Vapor) — CRUD complet avec Fluent"
import Vapor
import Fluent

// Les opérations Fluent utilisent req.db : la connexion à la base de données
// req.db : Database ? résolu par le container de dépendances de Vapor

// ─── CREATE ───────────────────────────────────────────────────────────────

app.post("articles") { req async throws -> Article in
    let dto = try req.content.decode(CréerArticleDTO.self)

    // Créer l'objet Fluent
    let article = Article(titre: dto.titre, contenu: dto.contenu, auteur: dto.auteur)

    // .save(on: req.db) : INSERT INTO articles (...) VALUES (...)
    // Remplit article.id et article.créeA automatiquement
    try await article.save(on: req.db)

    return article  // Retourné avec son id UUID
}

// ─── READ ALL ─────────────────────────────────────────────────────────────

app.get("articles") { req async throws -> [Article] in
    // .query(on: req.db) : commence une requête Fluent
    // .all() : SELECT * FROM articles
    try await Article.query(on: req.db).all()
}

// ─── READ ONE ─────────────────────────────────────────────────────────────

app.get("articles", ":id") { req async throws -> Article in
    // .find(id, on: db) : SELECT * FROM articles WHERE id = ? LIMIT 1
    // Retourne Article? (nil si non trouvé)
    guard let article = try await Article.find(
        req.parameters.require("id", as: UUID.self),
        on: req.db
    ) else {
        throw Abort(.notFound, reason: "Article introuvable")
    }
    return article
}

// ─── UPDATE ───────────────────────────────────────────────────────────────

app.put("articles", ":id") { req async throws -> Article in
    guard let article = try await Article.find(
        req.parameters.require("id", as: UUID.self),
        on: req.db
    ) else {
        throw Abort(.notFound)
    }

    let dto = try req.content.decode(CréerArticleDTO.self)

    // Modifier les propriétés
    article.titre   = dto.titre
    article.contenu = dto.contenu

    // .save(on: req.db) : UPDATE articles SET ... WHERE id = ?
    try await article.save(on: req.db)

    return article
}

// ─── DELETE ───────────────────────────────────────────────────────────────

app.delete("articles", ":id") { req async throws -> HTTPStatus in
    guard let article = try await Article.find(
        req.parameters.require("id", as: UUID.self),
        on: req.db
    ) else {
        throw Abort(.notFound)
    }

    // .delete(on: req.db) : DELETE FROM articles WHERE id = ?
    try await article.delete(on: req.db)

    return .noContent  // 204
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Modèle et migration Catégorie**

```swift title="Swift (Vapor) — Exercice 1 : Modèle Catégorie"
// Créez un modèle Catégorie avec :
// - id: UUID (clé primaire)
// - nom: String (requis)
// - description: String? (optionnel)
// - couleurHex: String (requis, ex: "#FF5733")
// - créeA: Date (timestamp création)
//
// Créez la migration CreateCatégorie correspondante
// et enregistrez-la dans configure.swift avant CreateArticle

final class Catégorie: Model, Content, @unchecked Sendable {
    static let schema = "categories"
    // TODO : propriétés
    init() { }
}

struct CreateCatégorie: AsyncMigration {
    func prepare(on database: any Database) async throws {
        // TODO
    }
    func revert(on database: any Database) async throws {
        try await database.schema("categories").delete()
    }
}
```

**Exercice 2 — CRUD complet Catégorie**

```swift title="Swift (Vapor) — Exercice 2 : CatégorieController CRUD complet"
// Créez un CatégorieController (RouteCollection) avec :
// GET    /categories           → liste toutes les catégories
// GET    /categories/:id       → lire une catégorie
// POST   /categories           → créer (avec Validatable : nom non vide, couleur format #RRGGBB)
// PUT    /categories/:id       → modifier
// DELETE /categories/:id       → supprimer (204)
// Retourner 404 si non trouvé (pas de force unwrap)

final class CatégorieController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        // TODO
    }
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Fluent associe les classes Swift aux tables SQL via le protocol `Model` — `@Field(key: "col")` mappe chaque propriété à une colonne. Les migrations sont des transformations versionnées du schéma (`prepare` = appliquer, `revert` = défaire). L'ordre des migrations dans `configure.swift` est critique — une migration ne peut pas créer une clé étrangère vers une table qui n'existe pas encore. `autoMigrate()` applique automatiquement toutes les nouvelles migrations au démarrage — idempotent et sûr. Le passage SQLite → PostgreSQL se fait uniquement dans `configure.swift` — les modèles et migrations sont identiques. `.save()` fait INSERT ou UPDATE selon que `id` est nil ou non.

> Dans le module suivant, nous approfondissons les **Modèles et Relations** — `@Parent`, `@Children`, `@Siblings`, le chargement de relations avec eager loading et les patterns de modélisation avancés.

<br>
