---
description: "Vapor Request & Response : décoder le corps JSON, Content protocol, headers, cookies, réponses personnalisées et streaming."
icon: lucide/book-open-check
tags: ["VAPOR", "REQUEST", "RESPONSE", "JSON", "CONTENT", "HEADERS"]
---

# Request & Response

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Lettre Recommandée"
    Envoyer une lettre recommandée, c'est plus qu'écrire un message. L'enveloppe (headers) indique l'expéditeur, le destinataire, le type de contenu. La lettre elle-même est le corps (body). L'accusé de réception est la réponse. En HTTP, c'est identique : chaque requête a une enveloppe (méthode, URL, headers) et optionnellement un corps (JSON, formulaire, fichier). Chaque réponse a un code de statut, des headers, et optionnellement un corps. Vapor vous donne accès à toutes ces couches via l'objet `Request`.

Maîtriser `Request` et `Response` est fondamental pour construire des APIs robustes — c'est le point de contact entre votre logique métier et le monde extérieur.

<br>

---

## L'Objet `Request` — Anatomie Complète

```swift title="Swift (Vapor) — Anatomie de la Request"
import Vapor

app.post("démonstration") { req async throws -> String in

    // ─── Méthode HTTP ─────────────────────────────────────────────
    let méthode = req.method  // .GET, .POST, .PUT, .DELETE, .PATCH

    // ─── URL et chemin ────────────────────────────────────────────
    let urlComplète = req.url.string          // "/démonstration?page=2"
    let chemin = req.url.path                 // "/démonstration"
    let queryString = req.url.query ?? ""     // "page=2"

    // ─── Headers ──────────────────────────────────────────────────
    // req.headers : HTTPHeaders — dictionnaire de headers HTTP
    let contentType = req.headers.contentType           // MediaType?
    let authorization = req.headers["Authorization"]   // [String]
    let accept = req.headers.first(name: "Accept") ?? "application/json"
    let userAgent = req.headers.first(name: "User-Agent") ?? "Inconnu"

    // ─── Corps (Body) ─────────────────────────────────────────────
    // req.body : l'accès bas niveau au corps de la requête (ByteBuffer)
    // req.content : l'accès haut niveau (décodage automatique)

    // ─── Logger ───────────────────────────────────────────────────
    // req.logger : instance de logger liée à la requête (traçabilité)
    req.logger.info("Requête reçue : \(méthode) \(chemin)")

    // ─── Informations réseau ──────────────────────────────────────
    let ipClient = req.remoteAddress?.description ?? "Inconnue"

    return "Requête de \(ipClient) — méthode : \(méthode) — chemin : \(chemin)"
}
```

<br>

---

## `Content` — Décoder le Corps JSON

Le protocol `Content` est l'interface de Vapor pour sérialiser/désérialiser le corps des requêtes et réponses.

```swift title="Swift (Vapor) — Décoder le corps JSON avec Content"
import Vapor

// ─── DTOs (Data Transfer Objects) ───────────────────────────────────────────
// Représentent exactement ce qu'on attend/retourne — différents des modèles DB

struct CréerUtilisateurDTO: Content {
    let prénom: String
    let nom: String
    let email: String
    let motDePasse: String        // Reçu en clair — hashé avant stockage
    let rôle: String?             // Optionnel : "admin" ou "user"
}

struct UtilisateurRéponse: Content {
    let id: UUID
    let prénom: String
    let nom: String
    let email: String
    let rôle: String
    let créeA: Date               // Date ISO8601
    // Note : motDePasse JAMAIS retourné
}

// Route POST qui crée un utilisateur
app.post("utilisateurs") { req async throws -> Response in

    // 1. Décoder le corps JSON en CréerUtilisateurDTO
    //    Throws 400 Bad Request si le JSON est invalide ou champs manquants
    let dto = try req.content.decode(CréerUtilisateurDTO.self)

    // 2. Utiliser les données décodées
    req.logger.info("Création : \(dto.email)")

    // 3. Construire la réponse
    let réponse = UtilisateurRéponse(
        id:      UUID(),
        prénom:  dto.prénom,
        nom:     dto.nom,
        email:   dto.email,
        rôle:    dto.rôle ?? "user",
        créeA:   Date()
    )

    // 4. Encoder en JSON avec le status 201 Created
    return try await réponse.encodeResponse(status: .created, for: req)
}
```

*`req.content.decode(MonDTO.self)` décode le corps selon le `Content-Type` de la requête — `application/json` par défaut. Vapor supporte aussi `application/x-www-form-urlencoded` et `multipart/form-data` avec le même pattern.*

<br>

---

## Validation avec `Validatable`

```swift title="Swift (Vapor) — Validation des données reçues avec Validatable"
import Vapor

// Validatable : ajoute la validation automatique avant décodage
struct InscriptionDTO: Content, Validatable {
    let prénom: String
    let email: String
    let motDePasse: String
    let âge: Int
    let siteWeb: String?

    // validations : déclare les règles — appelé par validate(content: req)
    static func validations(_ validations: inout Validations) {
        // Chaîne non vide ET entre 2 et 50 caractères
        validations.add("prénom",     as: String.self, is: !.empty && .count(2...50))

        // Format email valide
        validations.add("email",      as: String.self, is: .email)

        // Mot de passe : au moins 8 caractères
        validations.add("motDePasse", as: String.self, is: .count(8...))

        // Âge : entier entre 13 et 120
        validations.add("âge",        as: Int.self,    is: .range(13...120))

        // Site web : optionnel mais valide si présent
        validations.add("siteWeb",    as: String.self, is: .url, required: false)
    }
}

app.post("inscription") { req async throws -> UtilisateurRéponse in

    // validate(content: req) : valide AVANT de décoder
    // Si la validation échoue → 400 Bad Request avec détail des erreurs
    try InscriptionDTO.validate(content: req)
    let dto = try req.content.decode(InscriptionDTO.self)

    // Données validées — procéder à la création
    return UtilisateurRéponse(
        id:     UUID(),
        prénom: dto.prénom,
        nom:    "---",
        email:  dto.email,
        rôle:   "user",
        créeA:  Date()
    )
}
```

*La réponse d'erreur de validation est automatiquement structurée : `{"error": true, "reason": "prénom is less than minimum of 2 character(s)"}` — lisible par le client iOS pour afficher le bon message.*

<br>

---

## Construire des Réponses Personnalisées

```swift title="Swift (Vapor) — Construire des réponses HTTP personnalisées"
import Vapor

// 1. Retourner un type Content → status 200, headers standards
app.get("simple") { req async throws -> UtilisateurRéponse in
    UtilisateurRéponse(id: UUID(), prénom: "Alice", nom: "M",
                       email: "a@b.fr", rôle: "user", créeA: Date())
}

// 2. Retourner un HTTPStatus (sans corps)
app.delete("ressource", ":id") { req async throws -> HTTPStatus in
    .noContent   // 204
}

// 3. Réponse avec status personnalisé
app.post("ressource") { req async throws -> Response in
    let dto = try req.content.decode(CréerUtilisateurDTO.self)
    let réponse = UtilisateurRéponse(id: UUID(), prénom: dto.prénom, nom: dto.nom,
                                      email: dto.email, rôle: "user", créeA: Date())
    // 201 Created — convention pour les créations
    return try await réponse.encodeResponse(status: .created, for: req)
}

// 4. Réponse avec headers personnalisés
app.get("fichier-info") { req async throws -> Response in
    let info = ["taille": "1024", "type": "application/pdf"]
    var réponse = try await info.encodeResponse(for: req)

    // Ajouter des headers
    réponse.headers.add(name: "X-Fichier-Nom", value: "document.pdf")
    réponse.headers.add(name: "Cache-Control", value: "public, max-age=3600")

    return réponse
}

// 5. Redirection
app.get("ancienne-route") { req async -> Response in
    req.redirect(to: "/nouvelle-route", redirectType: .permanent)  // 301
}

// 6. Réponse vide ou erreur explicite
app.get("vide") { req async throws -> Response in
    Response(status: .ok, headers: HTTPHeaders(), body: .empty)
}
```

<br>

---

## Headers — Lire et Écrire

```swift title="Swift (Vapor) — Manipulation des headers HTTP"
import Vapor

// Lire les headers de la requête
app.get("info-client") { req async -> String in

    // Content-Type
    let contentType = req.headers.contentType?.description ?? "non défini"

    // Authorization (Bearer token)
    let authHeader = req.headers.bearerAuthorization?.token ?? "aucun token"

    // Custom headers (ex: mobile app version)
    let appVersion = req.headers.first(name: "X-App-Version") ?? "inconnue"
    let plateforme = req.headers.first(name: "X-Plateforme") ?? "inconnue"

    // Accept-Language
    let langue = req.headers.first(name: "Accept-Language") ?? "fr"

    return """
    Content-Type: \(contentType)
    Token: \(authHeader.prefix(10))...
    App: iOS \(appVersion) — \(plateforme)
    Langue: \(langue)
    """
}

// Écrire des headers dans la réponse
app.get("avec-headers") { req async throws -> Response in
    var réponse = Response(status: .ok)
    réponse.headers.replaceOrAdd(name: "Content-Type", value: "application/json")
    réponse.headers.add(name: "X-Powered-By", value: "Vapor/OmnyDocs")
    réponse.headers.add(name: "X-Rate-Limit-Remaining", value: "99")
    réponse.body = .init(string: #"{"statut":"ok"}"#)
    return réponse
}
```

<br>

---

## Multipart & Upload de Fichiers

```swift title="Swift (Vapor) — Upload de fichiers avec multipart/form-data"
import Vapor

// Struct pour recevoir un upload
struct UploadFichier: Content {
    // File : type Vapor pour les fichiers uploadés
    let fichier: File
    let description: String?
}

app.on(.POST, "upload", body: .collect(maxSize: "10mb")) { req async throws -> String in

    // body: .collect(maxSize:) — collecte le corps en mémoire
    // Pour les fichiers volumineux, utiliser .stream à la place

    let upload = try req.content.decode(UploadFichier.self)

    // Informations sur le fichier
    let nom = upload.fichier.filename
    let taille = upload.fichier.data.readableBytes
    let contentType = upload.fichier.contentType?.description ?? "inconnu"

    // Sauvegarder sur disque
    let chemin = req.application.directory.publicDirectory + nom
    try await req.fileio.writeFile(upload.fichier.data, at: chemin)

    return "Fichier '\(nom)' (\(taille) octets, \(contentType)) sauvegardé"
}
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — API d'inscription complète**

```swift title="Swift (Vapor) — Exercice 1 : route POST /inscription avec validation"
// Créez une route POST /inscription avec :
// - DTO InscriptionComplèteDTO : nom, prénom, email, motDePasse, dateNaissance (String "YYYY-MM-DD")
// - Validation Validatable :
//   • email valide
//   • motDePasse : 8+ caractères
//   • nom/prénom : 2-50 caractères
// - Sur succès : retourne 201 avec { id, email, créeA }
// - Sur échec validation : 400 avec message d'erreur

struct InscriptionComplèteDTO: Content, Validatable {
    // TODO
    static func validations(_ validations: inout Validations) {
        // TODO
    }
}
```

**Exercice 2 — Inspecter une requête**

```swift title="Swift (Vapor) — Exercice 2 : route de diagnostic"
// Créez GET /diagnostic qui retourne un JSON complet décrivant la requête :
// {
//   "méthode": "GET",
//   "chemin": "/diagnostic",
//   "ip": "127.0.0.1",
//   "userAgent": "curl/7.x",
//   "contentType": "application/json",
//   "headersCount": 5
// }

struct DiagnosticRéponse: Content {
    // TODO
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    `req.content.decode(MonDTO.self)` décode automatiquement le corps JSON selon le `Content-Type` — throws `400` si le JSON est invalide. `Validatable` ajoute une couche de validation déclarative avant le décodage — les erreurs sont retournées en JSON structuré. Pour les réponses : retourner un type `Content` → `200 OK` automatique ; retourner `Response` → contrôle total sur le status, les headers et le corps. `req.headers` permet de lire les headers entrants (Authorization, Content-Type, headers custom). Les fichiers sont gérés avec `body: .collect(maxSize:)` et le type `File` — jamais de taille illimitée en production.

> Dans le module suivant, nous découvrons les **Middlewares** — comment intercepter chaque requête avant et après les handlers pour implémenter la journalisation, le CORS, le rate limiting et l'authentification de façon centralisée.

<br>
