---
description: "Architecture 01 — API REST : principes REST, verbes HTTP, codes statuts, design des ressources, versionning et documentation OpenAPI."
icon: lucide/book-open-check
tags: ["ARCHITECTURE", "API-REST", "HTTP", "OPENAPI", "SWAGGER", "VERSIONING"]
---

# Module 01 — API REST

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Menu de Restaurant"
    Un restaurant propose un **menu** (la documentation API) avec des **plats** (les ressources) et des **modes de préparation** (GET, POST, PUT, DELETE). Le client (frontend) commande en suivant le menu ; le cuisinier (backend) prépare et sert. REST définit les règles du menu : chaque plat a un nom cohérent (`/articles`), les commandes se font en langage standard (verbes HTTP), et le cuisinier répond avec un code clair (200 OK, 404 Not Found).

**REST** (Representational State Transfer) est un style d'architecture pour les APIs web. Il ne définit pas un protocole strict, mais 6 contraintes qui guident la conception.

<br>

---

## 1. Les 6 Contraintes REST

```
1. Client-Server     : Séparation des responsabilités (UI ≠ logique métier)
2. Stateless         : Chaque requête est indépendante (pas de session côté serveur)
3. Cacheable         : Les réponses peuvent être mises en cache
4. Uniform Interface : Interface homogène (URLs, verbes, formats standardisés)
5. Layered System    : Client ne sait pas si il parle à un serveur direct ou un proxy
6. Code on Demand    : (Optionnel) Le serveur peut envoyer du code exécutable
```

!!! tip "REST ≠ HTTP"
    REST peut techniquement utiliser d'autres protocoles, mais en pratique REST = HTTP + JSON + conventions d'URLs.

<br>

---

## 2. Design des Ressources et URLs

```
Règles de nommage des URLs REST :
✅ Nom au pluriel pour les collections :   /articles       /users      /orders
✅ ID pour une ressource précise :          /articles/{id}  /users/{id}
✅ Relations imbriquées :                   /articles/{id}/comments
✅ Minuscules, séparés par des tirets :     /blog-posts     /user-profiles

❌ NE PAS utiliser de verbes dans les URLs :
   /getArticles        → GET /articles
   /createUser         → POST /users
   /deleteComment/42   → DELETE /comments/42
   /updateArticle/5    → PUT /articles/5
```

```
Mapping Ressources × Verbes HTTP :

Ressource               | GET              | POST         | PUT            | PATCH          | DELETE
------------------------|------------------|--------------|----------------|----------------|--------
/articles               | Lister tous      | Créer        | N/A            | N/A            | N/A
/articles/{id}          | Lire un seul     | N/A          | Remplacer      | Modifier       | Supprimer
/articles/{id}/comments | Lister comments  | Ajouter      | N/A            | N/A            | N/A
/articles/{id}/publish  | —                | Publier      | —              | —              | —
```

<br>

---

## 3. Verbes HTTP et leur Sémantique

```http title="HTTP — Exemples de requêtes REST"
# ─── GET : Lire une ou plusieurs ressources ──────────────────────────────────
GET /api/v1/articles HTTP/1.1
Accept: application/json

# Filtres, tri, pagination via Query String
GET /api/v1/articles?status=published&sort=-created_at&page=2&per_page=10

# ─── POST : Créer une nouvelle ressource ────────────────────────────────────
POST /api/v1/articles HTTP/1.1
Content-Type: application/json
Authorization: Bearer eyJhbGci...

{
    "title":   "Introduction à Astro",
    "content": "Astro est un framework web...",
    "tags":    ["astro", "javascript"]
}

# ─── PUT : Remplacer complètement une ressource ──────────────────────────────
PUT /api/v1/articles/42 HTTP/1.1
Content-Type: application/json

{
    "title":   "Introduction à Astro (v2)",
    "content": "Contenu complet mis à jour...",
    "tags":    ["astro"]
}

# ─── PATCH : Mise à jour partielle ──────────────────────────────────────────
PATCH /api/v1/articles/42 HTTP/1.1
Content-Type: application/json

{ "status": "published" }

# ─── DELETE : Supprimer une ressource ───────────────────────────────────────
DELETE /api/v1/articles/42 HTTP/1.1
Authorization: Bearer eyJhbGci...
```

<br>

---

## 4. Codes de Statut HTTP

```
2xx — Succès :
200 OK            : Succès general (GET, PUT, PATCH)
201 Created       : Ressource créée (POST) — inclure Location: /api/articles/42
204 No Content    : Succès sans corps de réponse (DELETE)

3xx — Redirection :
301 Moved Permanently : Redirection permanente
304 Not Modified      : Cache valide (pas besoin de renvoyer la ressource)

4xx — Erreurs Client :
400 Bad Request   : Données invalides ou malformées
401 Unauthorized  : Non authentifié (pas de token ou token invalide)
403 Forbidden     : Authentifié mais pas autorisé (droits insuffisants)
404 Not Found     : Ressource inexistante
409 Conflict      : Conflit (ex: email déjà utilisé)
422 Unprocessable : Validation échouée (données valides syntaxiquement mais invalides)
429 Too Many Req. : Rate limiting dépassé

5xx — Erreurs Serveur :
500 Internal      : Erreur serveur non gérée (à ne jamais exposer au client)
502 Bad Gateway   : Upstream server error (proxy, microservice down)
503 Unavailable   : Service temporairement indisponible
```

```json title="JSON — Format de réponse d'erreur standardisé"
{
    "error": {
        "code":    "VALIDATION_FAILED",
        "message": "Les données envoyées sont invalides.",
        "details": [
            { "field": "title",   "message": "Le titre est obligatoire." },
            { "field": "content", "message": "Le contenu doit faire au moins 50 caractères." }
        ]
    },
    "status":    422,
    "timestamp": "2024-03-15T10:30:00Z",
    "path":      "/api/v1/articles"
}
```

<br>

---

## 5. Format des Réponses

```json title="JSON — Réponse collection avec pagination"
{
    "data": [
        {
            "id":         1,
            "type":       "article",
            "attributes": {
                "title":      "Introduction à Astro",
                "status":     "published",
                "created_at": "2024-03-15T10:00:00Z"
            },
            "relationships": {
                "author": { "data": { "id": 5, "type": "user" } }
            },
            "links": {
                "self": "/api/v1/articles/1"
            }
        }
    ],
    "meta": {
        "total":    42,
        "page":     1,
        "per_page": 10,
        "pages":    5
    },
    "links": {
        "self":  "/api/v1/articles?page=1",
        "next":  "/api/v1/articles?page=2",
        "last":  "/api/v1/articles?page=5"
    }
}
```

<br>

---

## 6. Versionning d'API

```
Stratégies de versionning :

1. URL Path (recommandé)     : /api/v1/articles   /api/v2/articles
2. Query String              : /api/articles?version=1
3. Header personnalisé       : Accept-Version: v1
4. Content Negotiation       : Accept: application/vnd.api.v1+json

Règles d'évolution :
✅ Ajout de nouveaux champs        → Non-breaking, pas de nouvelle version
✅ Ajout de nouveaux endpoints     → Non-breaking, pas de nouvelle version
❌ Suppression de champs           → Breaking → incrémenter la version
❌ Renomm d'un champ existant      → Breaking → incrémenter la version
❌ Changement de type d'un champ   → Breaking → incrémenter la version
```

<br>

---

## 7. Documentation OpenAPI / Swagger

```yaml title="YAML — openapi.yaml : documentation API REST"
openapi: 3.1.0
info:
  title:       "Blog API"
  description: "API REST pour la gestion d'articles de blog"
  version:     "1.0.0"

servers:
  - url: "https://api.monblog.com/v1"
    description: "Production"
  - url: "http://localhost:3000/api/v1"
    description: "Développement"

paths:
  /articles:
    get:
      summary: "Lister les articles"
      tags: [Articles]
      parameters:
        - name: status
          in: query
          schema: { type: string, enum: [draft, published] }
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        "200":
          description: "Liste des articles"
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items: { $ref: "#/components/schemas/Article" }

    post:
      summary: "Créer un article"
      tags: [Articles]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: "#/components/schemas/CreateArticle" }
      responses:
        "201":
          description: "Article créé"
        "422":
          description: "Validation échouée"

components:
  schemas:
    Article:
      type: object
      properties:
        id:         { type: integer }
        title:      { type: string }
        status:     { type: string, enum: [draft, published] }
        created_at: { type: string, format: date-time }
    CreateArticle:
      type: object
      required: [title, content]
      properties:
        title:   { type: string, minLength: 1, maxLength: 200 }
        content: { type: string, minLength: 50 }
        tags:    { type: array, items: { type: string } }

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    REST définit **comment** concevoir une API HTTP cohérente. Les **URLs identifient des ressources** (noms au pluriel), les **verbes HTTP** définissent l'action (GET=lire, POST=créer, PUT=remplacer, PATCH=modifier, DELETE=supprimer). Les **codes HTTP** communiquent l'état de la réponse (2xx=succès, 4xx=erreur client, 5xx=erreur serveur). Documentez toujours votre API avec **OpenAPI/Swagger** — c'est le contrat entre le frontend et le backend. Versionnez par **URL path** (`/api/v1/`) pour une lisibilité maximale.

> Module suivant : [Clean Architecture →](./02-clean-architecture.md) — couches, injection de dépendances et principes SOLID.

<br>
