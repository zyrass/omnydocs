---
description: "Vapor requêtes Fluent : filter, sort, paginate, count, agrégations, sous-requêtes et transactions."
icon: lucide/book-open-check
tags: ["VAPOR", "FLUENT", "REQUETES", "FILTER", "PAGINATE", "TRANSACTIONS"]
---

# Requêtes Fluent

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothécaire et le Catalogue"
    Une bibliothécaire accepte des demandes très précises : "Je veux tous les livres de Victor Hugo, publiés entre 1850 et 1870, triés par titre, page 2 de 10 résultats, avec uniquement le titre et l'année". Elle ne sort jamais toute la bibliothèque pour répondre — elle navigate directement dans le catalogue. Les requêtes Fluent fonctionnent de même : chaque critère (filter, sort, paginate, select) est traduit en SQL optimisé. Votre serveur charge uniquement les données nécessaires — pas de tri ni de filtrage en Swift après un `all()`.

Une bonne API n'expose jamais `SELECT * FROM table` sans filtre ni pagination — c'est une bombe à retardement de performance. Ce module couvre les outils Fluent pour des requêtes précises et efficaces.

<br>

---

## Filtres — `.filter()`

```swift title="Swift (Vapor) — Filtres Fluent : type-safe et expressifs"
import Vapor
import Fluent

// ─── Filtres basiques ─────────────────────────────────────────────────────────

// Égalité : WHERE publié = true
let articlesPubliés = try await Article.query(on: req.db)
    .filter(\.$publié == true)
    .all()

// Comparaison : WHERE vues > 100
let articlesPopulaires = try await Article.query(on: req.db)
    .filter(\.$vues > 100)
    .all()

// IN : WHERE catégorie IN ('swift', 'swiftui')
let articlesTech = try await Article.query(on: req.db)
    .filter(\.$catégorie ~~ ["swift", "swiftui"])
    .all()

// LIKE (contains) : WHERE titre LIKE '%vapor%'
let résultatsRecherche = try await Article.query(on: req.db)
    .filter(\.$titre, .custom("LIKE"), "%vapor%")
    .all()

// ─── Filtres combinés ─────────────────────────────────────────────────────────

// AND (chaîne de .filter) : WHERE publié = true AND vues > 50
let articlesFiltres = try await Article.query(on: req.db)
    .filter(\.$publié == true)
    .filter(\.$vues > 50)
    .all()

// OR : WHERE catégorie = 'swift' OR catégorie = 'swiftui'
let articlesSortis = try await Article.query(on: req.db)
    .group(.or) { group in
        group.filter(\.$catégorie == "swift")
        group.filter(\.$catégorie == "swiftui")
    }
    .all()

// NOT : WHERE NOT (catégorie = 'divers')
let articlesFiltrésSansDivers = try await Article.query(on: req.db)
    .filter(\.$catégorie != "divers")
    .all()

// ─── Filtrer sur une relation (@Parent) ───────────────────────────────────────
// WHERE auteur_id = ?
let articlesParAuteur = try await Article.query(on: req.db)
    .filter(\.$auteur.$id == auteurId)   // $auteur.$id : accès à l'ID de la relation @Parent
    .all()
```

*Les filtres Fluent utilisent des **KeyPaths** Swift (`\.$titre`) — si vous renommez une propriété en Swift, le compilateur vous avertit immédiatement. C'est l'avantage majeur sur les chaînes SQL brutes.*

<br>

---

## Tri et Limite

```swift title="Swift (Vapor) — .sort() et .limit() : ordonner et limiter"
import Fluent

// Tri ascendant : ORDER BY créé_à ASC
let articlesParDate = try await Article.query(on: req.db)
    .sort(\.$créeA, .ascending)
    .all()

// Tri descendant : ORDER BY vues DESC
let articlesLesPlusVus = try await Article.query(on: req.db)
    .sort(\.$vues, .descending)
    .all()

// Tri multiple : ORDER BY catégorie ASC, créé_à DESC
let articlesTitriés = try await Article.query(on: req.db)
    .sort(\.$catégorie, .ascending)
    .sort(\.$créeA, .descending)
    .all()

// .limit() et .offset() : LIMIT ? OFFSET ?
let cinqPremiersArticles = try await Article.query(on: req.db)
    .sort(\.$créeA, .descending)
    .limit(5)          // Les 5 premiers
    .all()

let pageDeuxArticles = try await Article.query(on: req.db)
    .sort(\.$créeA, .descending)
    .limit(10)         // 10 par page
    .offset(10)        // Sauter les 10 premiers (page 2)
    .all()

// Premier résultat uniquement : LIMIT 1
let premierArticle = try await Article.query(on: req.db)
    .sort(\.$créeA, .descending)
    .first()    // Article? (nil si absent)
```

<br>

---

## Pagination — `paginate()`

```swift title="Swift (Vapor) — Pagination avec Page de Fluent"
import Vapor
import Fluent

// ─── Pagination automatique via Fluent ────────────────────────────────────────
// Fluent lit automatiquement ?page=N&per=M depuis la Request

app.get("articles") { req async throws -> Page<Article> in
    // Page<Article> : struct Fluent avec { items, metadata }
    // metadata : { page, per, total }
    try await Article.query(on: req.db)
        .sort(\.$créeA, .descending)
        .paginate(for: req)   // Lit page= et per= depuis req.query
}

// Requête : GET /articles?page=2&per=10
// Réponse JSON :
// {
//   "items": [...],
//   "metadata": {
//     "page": 2,
//     "per": 10,
//     "total": 47
//   }
// }

// ─── Pagination personnalisée ─────────────────────────────────────────────────
// Quand on veut un DTO au lieu de retourner le modèle directement

struct PaginationQuery: Content {
    var page: Int?
    var par: Int?
}

app.get("articles", "filtrés") { req async throws -> PageDTO<ArticleDTO> in
    let query = try req.query.decode(PaginationQuery.self)
    let pageNum = max(1, query.page ?? 1)
    let par = min(50, max(1, query.par ?? 20))  // Entre 1 et 50

    let total = try await Article.query(on: req.db).count()

    let articles = try await Article.query(on: req.db)
        .with(\.$auteur)
        .sort(\.$créeA, .descending)
        .offset((pageNum - 1) * par)
        .limit(par)
        .all()

    let dtos = articles.map { ArticleDTO(id: $0.id, titre: $0.titre, auteurNom: $0.auteur.nom) }

    return PageDTO(
        éléments: dtos,
        page:     pageNum,
        par:      par,
        total:    total
    )
}

struct ArticleDTO: Content {
    let id: UUID?
    let titre: String
    let auteurNom: String
}

struct PageDTO<T: Content>: Content {
    let éléments: [T]
    let page: Int
    let par: Int
    let total: Int
}
```

<br>

---

## Agrégations — `count()`, `sum()`, `min()`, `max()`

```swift title="Swift (Vapor) — Agrégations Fluent : count, sum, min, max"
import Fluent

// count() : SELECT COUNT(*) FROM articles
let totalArticles = try await Article.query(on: req.db).count()

// count avec filtre
let totalPubliés = try await Article.query(on: req.db)
    .filter(\.$publié == true)
    .count()

// Agrégation sur un champ numérique
// sum \.$vues SELECT SUM(vues) FROM articles
let totalVues = try await Article.query(on: req.db)
    .sum(\.$vues)   // Int? (nil si table vide)

// max et min
let maxVues = try await Article.query(on: req.db).max(\.$vues)   // Int?
let minVues = try await Article.query(on: req.db).min(\.$vues)   // Int?

// Exemple : route de statistiques
app.get("articles", "statistiques") { req async throws -> StatistiquesRéponse in
    async let total    = Article.query(on: req.db).count()
    async let publiés  = Article.query(on: req.db).filter(\.$publié == true).count()
    async let totalVues = Article.query(on: req.db).sum(\.$vues)
    async let maxVues  = Article.query(on: req.db).max(\.$vues)

    // Les 4 requêtes s'exécutent en parallèle (async let)
    return try await StatistiquesRéponse(
        total:      total,
        publiés:    publiés,
        totalVues:  totalVues ?? 0,
        vuesRecord: maxVues   ?? 0
    )
}

struct StatistiquesRéponse: Content {
    let total: Int
    let publiés: Int
    let totalVues: Int
    let vuesRecord: Int
}
```

*`async let` en Swift 6 exécute plusieurs requêtes `async` en **parallèle** — les 4 requêtes de statistiques s'exécutent simultanément, réduisant le temps de réponse de 4× par rapport à 4 `await` séquentiels.*

<br>

---

## Transactions

```swift title="Swift (Vapor) — Transactions : atomicité des opérations multiples"
import Vapor
import Fluent

// Une transaction garantit que TOUTES les opérations réussissent, ou AUCUNE
// Exemple : transférer un article d'un auteur à l'autre

app.post("articles", ":id", "transferer") { req async throws -> HTTPStatus in
    let articleId    = try req.parameters.require("id", as: UUID.self)
    let dto          = try req.content.decode(TransférerDTO.self)

    // req.db.transaction { db in } : toutes les opérations dans le bloc
    // si l'une échoue → ROLLBACK automatique de toutes
    try await req.db.transaction { db in

        // 1. Charger l'article
        guard let article = try await Article.find(articleId, on: db) else {
            throw Abort(.notFound, reason: "Article introuvable")
        }

        // 2. Vérifier que le nouvel auteur existe
        guard let nouvelAuteur = try await Utilisateur.find(dto.nouvelAuteurId, on: db) else {
            throw Abort(.badRequest, reason: "Auteur cible introuvable")
        }

        // 3. Modifier la relation
        article.$auteur.id = nouvelAuteur.id!

        // 4. Journaliser le transfert (opération liée)
        let journal = JournalTransfert(
            articleId:     article.id!,
            ancienAuteurId: article.$auteur.id,
            nouvelAuteurId: nouvelAuteur.id!
        )
        try await journal.save(on: db)

        // 5. Sauvegarder l'article modifié
        try await article.save(on: db)

        // Si n'importe laquelle de ces étapes échoue → tout est annulé (ROLLBACK)
    }

    return .ok
}

struct TransférerDTO: Content {
    let nouvelAuteurId: UUID
}

// Modèle journal fictif pour l'exemple
final class JournalTransfert: Model, @unchecked Sendable {
    static let schema = "journal_transferts"
    @ID(key: .id) var id: UUID?
    @Field(key: "article_id") var articleId: UUID
    @Field(key: "ancien_auteur_id") var ancienAuteurId: UUID
    @Field(key: "nouvel_auteur_id") var nouvelAuteurId: UUID
    init() {}
    init(articleId: UUID, ancienAuteurId: UUID, nouvelAuteurId: UUID) {
        self.articleId = articleId
        self.ancienAuteurId = ancienAuteurId
        self.nouvelAuteurId = nouvelAuteurId
    }
}
```

*`req.db.transaction { db in }` garantit l'**atomicité** — si l'une des opérations dans le bloc lance une erreur, la base de données revient à son état initial (ROLLBACK). Toujours utiliser `db` (le paramètre du bloc) et non `req.db` à l'intérieur d'une transaction.*

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Route de recherche avancée**

```swift title="Swift (Vapor) — Exercice 1 : recherche multi-critères paginée"
// Créez GET /articles/recherche avec :
// ?q=vapor       → filtre sur titre (contient, insensible à la casse)
// ?auteur=UUID   → filtre sur auteur_id
// ?publié=true   → filtre sur publié
// ?tri=date|vues → tri par date ou par vues (descendant)
// ?page=1&par=10 → pagination

struct FiltreRechercheQuery: Content {
    let q: String?
    let auteur: UUID?
    let publié: Bool?
    let tri: String?
    let page: Int?
    let par: Int?
}

app.get("articles", "recherche") { req async throws -> PageDTO<ArticleDTO> in
    let filtre = try req.query.decode(FiltreRechercheQuery.self)
    // TODO : construire la requête Fluent en fonction des filtres
    // (commencer par la query de base puis ajouter les filtres conditionnellement)
}
```

**Exercice 2 — Tableau de bord statistiques**

```swift title="Swift (Vapor) — Exercice 2 : statistiques parallèles"
// Créez GET /admin/statistiques qui retourne en parallèle (async let) :
// - totalArticles : count
// - totalUtilisateurs : count
// - articlesPubliésSemaineDernière : count + filter créé_à > (now - 7j)
// - auteurLePlusActif : auteur avec le plus d'articles (agrégation complexe)
// Note : auteurLePlusActif peut utiliser une requête SQL brute si Fluent ne le supporte pas

struct DashboardAdmin: Content {
    let totalArticles: Int
    let totalUtilisateurs: Int
    let articlesRécents: Int
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Les filtres Fluent avec KeyPaths (`\.$colonne`) sont **type-safe** — le compilateur détecte les erreurs. Enchaîner plusieurs `.filter()` produit un `AND` SQL. `.group(.or)` produit un `OR`. La pagination automatique `paginate(for: req)` lit `?page=` et `?per=` depuis la requête et retourne un `Page<T>` avec métadonnées. `async let` parallélise plusieurs requêtes `async` — divise le temps de réponse pour les tableaux de bord statistiques. Les transactions `req.db.transaction { db in }` garantissent l'atomicité — utiliser le `db` du bloc, jamais `req.db` à l'intérieur. Toujours paginer les listes — un `all()` sans limite peut retourner des millions de lignes en production.

> Dans le module suivant, nous implémentons l'**Authentification & JWT** — hachage de mots de passe avec BCrypt, génération et validation de tokens JWT, et les middlewares d'authentification Vapor.

<br>
