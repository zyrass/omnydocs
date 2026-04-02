---
description: "Vapor — Introduction et Configuration : architecture SwiftNIO, lifecycle d'une requête, premier projet API, structure des fichiers."
icon: lucide/book-open-check
tags: ["VAPOR", "INTRODUCTION", "SWIFTNIO", "CONFIGURATION", "PREMIER-PROJET"]
---

# Introduction & Configuration

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Hôtel et sa Conciergerie"
    Un hôtel reçoit des clients (requêtes HTTP), les oriente vers le bon service (routage), traite leur demande (contrôleur), consulte les archives (base de données), et retourne une réponse (JSON, HTML). Vapor est l'infrastructure complète de cet hôtel — construite en Swift. SwiftNIO est le réseau téléphonique de l'hôtel : il traite des centaines d'appels simultanément sans jamais bloquer le standard. Chaque module de cette formation ajoute un service à l'hôtel : le routage, la réservation (base de données), la sécurité (authentification), etc.

Vapor est un **framework web backend** écrit en Swift. Il permet de créer des API REST, des serveurs web, des microservices — entièrement en Swift, avec les mêmes patterns `async/await` que vos applications SwiftUI.

<br>

---

## Architecture de Vapor

Vapor repose sur trois couches principales :

```mermaid
flowchart LR
    Client["📱 Client\n(iPhone / Browser)"]

    subgraph Vapor["⚙️ Vapor Framework"]
        direction TB
        NIO["SwiftNIO\n(Couche réseau)"]
        Router["Routeur\n(Routes / Contrôleurs)"]
        Middleware["Middlewares\n(Auth, CORS, Log)"]
        Services["Services\n(Fluent, JWT, Queue)"]
    end

    DB[("🗄️ Base de données\nSQLite / PostgreSQL")]

    Client -->|"HTTP Request"| NIO
    NIO --> Middleware
    Middleware --> Router
    Router --> Services
    Services --> DB
    DB --> Services
    Services --> Router
    Router --> Middleware
    Middleware --> NIO
    NIO -->|"HTTP Response"| Client
```

*Chaque requête HTTP traverse les middlewares (dans l'ordre d'ajout), atteint le routeur qui la dispatche vers le bon contrôleur, lequel interagit si besoin avec les services (base de données, JWT...) avant de renvoyer une réponse.*

<br>

---

## Installation et Premier Projet

### Prérequis

```bash title="Terminal — Prérequis et installation Vapor"
# 1. Vérifier Swift 6+
swift --version
# → swift-driver version: 1.x.x  Apple Swift version 6.0

# 2. Installer le Vapor Toolbox (macOS uniquement)
brew install vapor

# Vérifier
vapor --version
# → vapor/toolbox@18.x.x
```

### Créer un Projet

```bash title="Terminal — Créer et lancer un projet Vapor API"
# Créer un projet avec le template API (le plus courant)
vapor new OmnyAPI --template api
# → Sélectionner : Fluent (ORM) → yes
# → Sélectionner : SQLite → yes (le plus simple pour démarrer)

cd OmnyAPI

# Ouvrir dans Xcode
open Package.swift

# OU compiler et lancer depuis le terminal
swift run
# → Server starting on http://127.0.0.1:8080
```

*`vapor new --template api` génère un projet complet avec la structure de fichiers conventionnelle, Fluent ORM configuré, une route de test et un `Todo` modèle d'exemple.*

<br>

---

## Structure d'un Projet Vapor

```
OmnyAPI/
├── Sources/
│   └── App/
│       ├── Controllers/        ← Contrôleurs (logique métier par ressource)
│       │   └── TodoController.swift
│       ├── Models/             ← Modèles Fluent (correspond aux tables DB)
│       │   └── Todo.swift
│       ├── Migrations/         ← Migrations (versions du schéma DB)
│       │   └── CreateTodo.swift
│       ├── configure.swift     ← ⭐ Point de configuration de l'app
│       ├── entrypoint.swift    ← Point d'entrée (main)
│       └── routes.swift        ← ⭐ Déclaration de toutes les routes
├── Tests/
│   └── AppTests/               ← Tests XCTVapor
├── Package.swift               ← ⭐ Dépendances SPM (Swift Package Manager)
└── .env                        ← Variables d'environnement (secrets, DB URL)
```

Les trois fichiers clés au démarrage sont `Package.swift`, `configure.swift` et `routes.swift`.

<br>

---

## `Package.swift` — Dépendances SPM

```swift title="Swift (Vapor) — Package.swift : dépendances du projet"
// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "OmnyAPI",
    platforms: [
        // Vapor 4 requiert macOS 13+ pour Swift Concurrency complète
        .macOS(.v13)
    ],
    dependencies: [
        // Vapor : le framework principal
        .package(url: "https://github.com/vapor/vapor.git", from: "4.99.0"),
        // Fluent : l'ORM (Object-Relational Mapper)
        .package(url: "https://github.com/vapor/fluent.git", from: "4.9.0"),
        // Driver SQLite pour Fluent (à remplacer par fluent-postgres-driver en prod)
        .package(url: "https://github.com/vapor/fluent-sqlite-driver.git", from: "4.6.0"),
        // Leaf : moteur de templates HTML (optionnel — pour les API pures, pas nécessaire)
        // .package(url: "https://github.com/vapor/leaf.git", from: "4.3.0"),
    ],
    targets: [
        .executableTarget(
            name: "App",
            dependencies: [
                .product(name: "Vapor",          package: "vapor"),
                .product(name: "Fluent",          package: "fluent"),
                .product(name: "FluentSQLiteDriver", package: "fluent-sqlite-driver"),
            ]
        ),
        .testTarget(
            name: "AppTests",
            dependencies: [
                .target(name: "App"),
                .product(name: "XCTVapor", package: "vapor"),  // Framework de test Vapor
            ]
        )
    ]
)
```

*`Package.swift` est le manifeste du projet — l'équivalent de `composer.json` (PHP) ou `package.json` (Node). Swift Package Manager télécharge et compile les dépendances automatiquement lors de l'ouverture dans Xcode.*

<br>

---

## `configure.swift` — Configuration de l'Application

```swift title="Swift (Vapor) — configure.swift : initialisation des services"
import Fluent
import FluentSQLiteDriver
import Vapor

// configure(_ app: Application) est appelé au démarrage, AVANT les routes
// C'est ici qu'on initialise les services : base de données, middlewares, encodeurs
public func configure(_ app: Application) async throws {

    // ─── Base de données ───────────────────────────────────────────
    // SQLite en mode fichier (les données persistent entre les redémarrages)
    app.databases.use(
        .sqlite(.file("db.sqlite")),   // Fichier local : db.sqlite
        as: .sqlite
    )

    // SQLite en mémoire (pour les tests — données effacées à l'arrêt)
    // app.databases.use(.sqlite(.memory), as: .sqlite)

    // ─── Migrations ────────────────────────────────────────────────
    // Ajouter les migrations dans l'ordre (elles créent/modifient les tables)
    app.migrations.add(CreateTodo())    // Crée la table "todos"

    // Exécuter les migrations au démarrage (idempotent)
    try await app.autoMigrate()

    // ─── Encodeur JSON ─────────────────────────────────────────────
    // Configurer le format des dates en JSON (ISO8601 par défaut)
    let encoder = JSONEncoder()
    encoder.dateEncodingStrategy = .iso8601
    ContentConfiguration.global.use(encoder: encoder, for: .json)

    let decoder = JSONDecoder()
    decoder.dateDecodingStrategy = .iso8601
    ContentConfiguration.global.use(decoder: decoder, for: .json)

    // ─── Routes ────────────────────────────────────────────────────
    // Enregistrer toutes les routes définies dans routes.swift
    try routes(app)
}
```

<br>

---

## `routes.swift` — Premières Routes

```swift title="Swift (Vapor) — routes.swift : définir les premières routes"
import Vapor

// routes(_ app: Application) est appelé depuis configure()
// C'est ici qu'on déclare toutes les routes de l'application
func routes(_ app: Application) throws {

    // Route GET sur "/" — retourne un simple texte
    // app.get : méthode HTTP GET sur le chemin spécifié
    app.get { req async in
        "Bienvenue sur l'API OmnyDocs !"
    }

    // Route GET "/bonjour" — retourne un texte avec paramètre
    app.get("bonjour") { req async -> String in
        "Bonjour depuis Vapor !"
    }

    // Route GET "/version" — retourne un objet JSON
    // Response.Content : n'importe quel type Codable peut être retourné
    app.get("version") { req async -> APIVersion in
        APIVersion(version: "1.0.0", framework: "Vapor 4")
    }

    // Route POST "/echo" — retourne le corps reçu
    app.post("echo") { req async throws -> EchoResponse in
        // try req.content.decode() : décode le corps JSON en un type Codable
        let corps = try req.content.decode(EchoRequest.self)
        return EchoResponse(message: "Reçu : \(corps.texte)")
    }

    // Enregistrer les routes des contrôleurs (voir module 02)
    try app.register(collection: TodoController())
}

// ─── Types de réponse ──────────────────────────────────────────────────────

// Content : protocol qui rend un type encodable en réponse HTTP
struct APIVersion: Content {
    let version: String
    let framework: String
}

struct EchoRequest: Content {
    let texte: String
}

struct EchoResponse: Content {
    let message: String
}
```

*Tout type conforme à `Content` (lui-même conforme à `Codable`) peut être retourné directement depuis une route — Vapor se charge de la sérialisation JSON et des headers appropriés.*

<br>

---

## Tester les Routes avec cURL

```bash title="Terminal — Tester l'API avec cURL"
# Démarrer le serveur (dans un premier terminal)
swift run
# → Server starting on http://127.0.0.1:8080

# Dans un second terminal :

# GET simple
curl http://localhost:8080/
# → Bienvenue sur l'API OmnyDocs !

# GET JSON
curl http://localhost:8080/version
# → {"version":"1.0.0","framework":"Vapor 4"}

# POST avec corps JSON
curl -X POST http://localhost:8080/echo \
     -H "Content-Type: application/json" \
     -d '{"texte": "Bonjour Vapor"}'
# → {"message":"Reçu : Bonjour Vapor"}
```

<br>

---

## Variables d'Environnement

```swift title="Swift (Vapor) — Lire les variables d'environnement"
import Vapor

func configure(_ app: Application) async throws {

    // app.environment : l'environnement courant (development, testing, production)
    switch app.environment {
    case .development:
        app.logger.logLevel = .debug        // Logs verbeux en développement
        app.databases.use(.sqlite(.file("dev.sqlite")), as: .sqlite)

    case .production:
        app.logger.logLevel = .warning      // Logs réduits en production

        // Lire l'URL de DB depuis la variable d'environnement
        guard let dbURL = Environment.get("DATABASE_URL") else {
            throw Abort(.internalServerError, reason: "DATABASE_URL manquante")
        }
        // Configuration PostgreSQL en production (voir Module 05)
        // app.databases.use(.postgres(url: dbURL), as: .psql)

    default:
        break
    }

    try routes(app)
}
```

```bash title="Terminal — Lancer Vapor en différents modes"
# Mode développement (par défaut)
swift run

# Mode production
swift run --env production

# Avec variable d'environnement
DATABASE_URL=postgres://user:pass@localhost/mydb swift run --env production
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Exploration du projet généré**

```bash title="Terminal — Exercice 1 : créer et explorer le projet"
# 1. Créer un projet Vapor API
vapor new ExerciceVapor --template api

# 2. Lancer le serveur
swift run

# 3. Tester avec cURL :
#    - GET /todos        → liste vide
#    - POST /todos       → créer un todo {"title": "Mon premier todo"}
#    - GET /todos        → liste avec le todo créé
#    - DELETE /todos/:id → supprimer le todo

# 4. Ouvrir db.sqlite dans un viewer (DB Browser for SQLite)
#    et observer la structure de la table "todos"
```

**Exercice 2 — Nouvelles routes**

```swift title="Swift (Vapor) — Exercice 2 : ajouter des routes"
// Dans routes.swift, ajoutez :

// 1. GET /sante → retourne un objet { "statut": "ok", "timestamp": "..." }
struct RéponseStatut: Content {
    let statut: String
    let timestamp: String
}

// 2. GET /bonjour/:nom → retourne "Bonjour, Alice !" si :nom = "Alice"
// Indice : req.parameters.get("nom")

// 3. POST /calcul → reçoit { "a": 10, "b": 5, "opération": "addition" }
//    retourne { "résultat": 15 }
//    Supporte : addition, soustraction, multiplication
struct RequêteCalcul: Content {
    let a: Double
    let b: Double
    let opération: String
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Vapor est un framework backend Swift construit sur SwiftNIO — non bloquant, performant, et entièrement `async/await`. La structure d'un projet suit une convention claire : `configure.swift` (services), `routes.swift` (chemins), `Controllers/` (logique), `Models/` (données), `Migrations/` (schéma). Tout type conforme à `Content` (Codable) peut être retourné directement depuis une route — Vapor sérialise en JSON automatiquement. Les variables d'environnement (`Environment.get("CLE")`) sont la bonne pratique pour la configuration des secrets — jamais de valeurs sensibles en dur dans le code.

> Dans le module suivant, nous approfondissons le **Routing** — paramètres de chemin, groupes de routes, contrôleurs `RouteCollection` et l'organisation d'une API à plusieurs ressources.

<br>
