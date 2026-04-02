---
description: "Vapor Déploiement : Docker, Railway, Render, variables d'environnement, migrations en production, HTTPS et surveillance."
icon: lucide/book-open-check
tags: ["VAPOR", "DEPLOIEMENT", "DOCKER", "RAILWAY", "RENDER", "PRODUCTION", "HTTPS"]
---

# Déploiement

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="1.0"
  data-time="2-3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Atelier au Marché Public"
    Un artisan travaille dans son atelier privé (votre Mac en développement). Pour vendre, il dresse son stand au marché public (le serveur cloud) — même recettes, mêmes outils, mais un emplacement accessible à tous, ouvert 24h/24. Docker est la caisse de transport standardisée qui emballe l'atelier complet — recettes, outils, ingrédients — pour le déplacer fidèlement sur n'importe quelle surface de marché. Railway et Render sont les places de marché qui louent les emplacements et gèrent la logistique (HTTPS, scaling, monitoring).

Ce module couvre le chemin complet du développement local à un backend Vapor accessible depuis n'importe quel iPhone dans le monde.

<br>

---

## Architecture de Déploiement

```mermaid
flowchart TB
    Dev["💻 Développement\n(Mac + SQLite)"]

    subgraph Build["🔨 Build & CI"]
        direction LR
        GH["GitHub\n(commit)"]
        CI["GitHub Actions\n(test + build)"]
    end

    subgraph Deploy["☁️ Cloud"]
        direction TB
        Railway["Railway / Render\n(Container)"]
        PG[("PostgreSQL\n(Cloud DB)")]
    end

    iphone["📱 iPhone\nhttps://api.monapp.com"]

    Dev -->|"git push"| GH
    GH --> CI
    CI -->|"Docker image"| Railway
    Railway <--> PG
    iphone -->|"HTTPS"| Railway
```

<br>

---

## Dockerfile — Conteneuriser l'Application

```dockerfile title="Dockerfile — Conteneur multi-stage pour Vapor"
# ─── Étape 1 : Build ───────────────────────────────────────────────────────────
# Image Swift officielle — compiler l'application
FROM swift:6.0 AS builder

WORKDIR /build

# Copier les manifestes de dépendances en premier
# (meilleure utilisation du cache Docker — les deps changent rarement)
COPY Package.swift Package.resolved ./

# Télécharger et compiler les dépendances uniquement
RUN swift package resolve

# Copier le code source
COPY Sources ./Sources
COPY Tests ./Tests (optionnel si pas de tests en CI)

# Compiler en mode release (optimisations activées)
RUN swift build --configuration release

# ─── Étape 2 : Runtime ─────────────────────────────────────────────────────────
# Image Ubuntu minimale (pas de Swift complet — juste les libs runtime)
# Réduit la taille de l'image de ~2 Go à ~200 Mo
FROM ubuntu:22.04

# Installer les dépendances runtime de Swift
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier uniquement le binaire compilé depuis l'étape build
COPY --from=builder /build/.build/release/App ./App

# Copier les ressources publiques si nécessaire
# COPY --from=builder /build/Public ./Public

# Exposer le port 8080 (convention Vapor)
EXPOSE 8080

# Commande de démarrage
# --hostname 0.0.0.0 : écouter sur toutes les interfaces (requis en container)
# --port 8080 : port d'écoute
ENTRYPOINT ["./App", "serve", "--env", "production", "--hostname", "0.0.0.0", "--port", "8080"]
```

*Le build multi-stage est crucial : l'image finale ne contient pas le compilateur Swift (2 Go) — seulement le binaire compilé et ses dépendances runtime. L'image finale pèse ~150-200 Mo vs ~2 Go en image unique.*

<br>

---

## Variables d'Environnement

```swift title="Swift (Vapor) — configure.swift : configuration production via env vars"
import Fluent
import FluentPostgresDriver
import Vapor

public func configure(_ app: Application) async throws {

    // ─── Configuration selon l'environnement ───────────────────────
    if app.environment == .production {

        // Base de données PostgreSQL — URL depuis variable d'environnement
        guard let databaseURL = Environment.get("DATABASE_URL") else {
            throw Abort(.internalServerError, reason: "DATABASE_URL manquante")
        }
        try app.databases.use(.postgres(url: databaseURL), as: .psql)

        // Niveau de log : warning en production (pas de debug détaillé)
        app.logger.logLevel = .warning

    } else {
        // SQLite local pour dev et test
        app.databases.use(.sqlite(.file("dev.sqlite")), as: .sqlite)
        app.logger.logLevel = .debug
    }

    // ─── Clé JWT depuis env var en production ──────────────────────
    let jwtSecret = Environment.get("JWT_SECRET") ?? {
        if app.environment == .production {
            fatalError("JWT_SECRET manquante en production")
        }
        return "dev-secret-changez-moi-en-production-svp"
    }()

    await app.jwt.keys.add(hmac: .init(from: jwtSecret), digestAlgorithm: .sha256)

    // ─── CORS : origins autorisées en production ────────────────────
    let allowedOrigins: CORSMiddleware.AllowOriginSetting
    if app.environment == .production {
        allowedOrigins = .any(["https://app.omnyvia.com", "https://omnyvia.com"])
    } else {
        allowedOrigins = .all
    }

    app.middleware.use(CORSMiddleware(configuration: .init(
        allowedOrigin:  allowedOrigins,
        allowedMethods: [.GET, .POST, .PUT, .PATCH, .DELETE, .OPTIONS],
        allowedHeaders: [.accept, .authorization, .contentType, .origin]
    )))

    app.middleware.use(ErrorMiddleware.default(environment: app.environment))

    // ─── Migrations ────────────────────────────────────────────────
    app.migrations.add(CreateUtilisateur())
    app.migrations.add(CreateArticle())
    app.migrations.add(CreateRefreshToken())
    // autoMigrate : sûr en production (idempotent)
    try await app.autoMigrate()

    try routes(app)
}
```

<br>

---

## Déploiement sur Railway

Railway est la plateforme cloud la plus simple pour Vapor — déploiement automatique depuis GitHub, PostgreSQL intégré.

```bash title="Terminal — Déploiement sur Railway"
# 1. Créer un compte et installer Railway CLI
npm install -g @railway/cli
railway login

# 2. Initialiser le projet Railway (dans le dossier du projet Vapor)
railway init
# → Sélectionner "Create new project"

# 3. Ajouter PostgreSQL
railway add --plugin postgresql
# → Railway crée une instance PostgreSQL et expose DATABASE_URL automatiquement

# 4. Configurer les variables d'environnement
railway variables set JWT_SECRET="votre-super-secret-production-minimum-32-chars"
railway variables set REDIS_URL="redis://..."    # Si vous utilisez les Queues

# 5. Déployer
railway up
# → Railway détecte le Dockerfile, build l'image, déploie

# 6. Obtenir l'URL publique
railway open
# → https://votre-app.railway.app

# Déploiement automatique : activer dans Railway Dashboard
# Chaque git push sur main → déploiement automatique
```

```
Variables d'environnement Railway (réglées automatiquement) :
├── DATABASE_URL : postgres://user:pass@host:5432/railway
└── PORT : 8080 (Railway expose ce port automatiquement)

Variables à configurer manuellement :
├── JWT_SECRET : chaîne aléatoire 64+ caractères
├── NODE_ENV : production
└── REDIS_URL : si vous utilisez les Queues
```

<br>

---

## Déploiement sur Render

```yaml title="YAML (Render) — render.yaml : configuration déclarative"
services:
  # Service API Vapor
  - type: web
    name: omny-api
    env: docker                    # Utilise le Dockerfile
    dockerfilePath: ./Dockerfile   # Chemin vers le Dockerfile

    # Région de déploiement
    region: oregon

    # Plan (gratuit disponible mais se met en veille)
    plan: starter

    # Commande de health check
    healthCheckPath: /statut

    # Variables d'environnement
    envVars:
      - key: JWT_SECRET
        generateValue: true        # Render génère une valeur aléatoire !
      - key: DATABASE_URL
        fromDatabase:
          name: omny-db
          property: connectionString

  # Base de données PostgreSQL
databases:
  - name: omny-db
    databaseName: omnyapi
    plan: starter

    # Rétention : 90 jours de sauvegardes
    ipAllowList: []  # Accessible uniquement depuis les services Render
```

<br>

---

## GitHub Actions — CI/CD Automatique

```yaml title="YAML (GitHub Actions) — .github/workflows/deploy.yml"
name: Test et Déploiement Vapor

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ─── Tests ──────────────────────────────────────────────────────────
  tests:
    name: Tests XCTVapor
    runs-on: ubuntu-latest

    container:
      image: swift:6.0

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Résoudre les dépendances
        run: swift package resolve

      - name: Compiler
        run: swift build --configuration debug

      - name: Exécuter les tests
        run: swift test --configuration debug
        env:
          # La DB de test est in-memory — pas besoin de PostgreSQL
          LOG_LEVEL: notice

  # ─── Déploiement (seulement sur main après succès des tests) ─────────
  deploy:
    name: Déploiement Railway
    runs-on: ubuntu-latest
    needs: tests              # Déploie seulement si les tests passent
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Installer Railway CLI
        run: npm install -g @railway/cli

      - name: Déployer sur Railway
        run: railway up --service omny-api
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

<br>

---

## Migrations en Production

```bash title="Terminal — Migrations en production : stratégies sûres"
# ─── Option A : autoMigrate() dans configure.swift ────────────────────────────
# Avantage   : simple, automatique au démarrage
# Inconvénient : en cas d'erreur de migration, le service ne démarre pas
# Recommandé pour : projets petits/moyens, Railway, Render

# ─── Option B : commande migrate avant le démarrage ──────────────────────────
# Dans Docker (Railway / Render), exécuter les migrations AVANT le service
# Via un "Release Command" dans Railway ou Render :
swift run App migrate --yes

# ─── Règles de migration en production ───────────────────────────────────────
# ✅ Ajouter une colonne nullable
# ✅ Créer un nouvel index
# ✅ Ajouter une nouvelle table
# ✅ Renommer une table AVEC données (data migration)
# ❌ Supprimer une colonne (faire en 2 étapes : déprécier + supprimer)
# ❌ Renommer une colonne directement (perte de données)
# ❌ Changer le type d'une colonne (NULL → NOT NULL) sans valeur par défaut
```

<br>

---

## Checklist de Mise en Production

```
Checklist pré-déploiement Vapor :

─── SÉCURITÉ ───────────────────────────────────────────────────────────────
☐ JWT_SECRET : 64+ caractères aléatoires, stocké en variable d'environnement
☐ DATABASE_URL : jamais en dur dans le code
☐ Aucun secret dans git (vérifier avec git log)
☐ CORS configuré pour les origins de production uniquement
☐ Rate limiting activé sur toutes les routes publiques
☐ HTTPS obligatoire (Railway/Render le gèrent automatiquement)

─── PERFORMANCE ────────────────────────────────────────────────────────────
☐ Build en mode release (--configuration release)
☐ Log level à .warning en production (pas .debug)
☐ Pagination sur toutes les listes (pas de .all() sans limite)
☐ Indexes DB sur les colonnes filtrées fréquemment (email, auteur_id)

─── FIABILITÉ ──────────────────────────────────────────────────────────────
☐ Health check endpoint (/statut) retourne 200
☐ autoMigrate() configuré
☐ Sauvegardes DB automatiques activées
☐ Tests XCTVapor passent en CI avant déploiement

─── MONITORING ─────────────────────────────────────────────────────────────
☐ Logs accessibles dans le dashboard cloud
☐ Alertes configurées sur les erreurs 5xx
☐ Métriques de base : temps de réponse, taux d'erreur
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Dockerfile optimisé**

```bash title="Terminal — Exercice 1 : construire et tester le Dockerfile"
# 1. Créer le Dockerfile fourni dans ce module dans votre projet
# 2. Builder l'image :
docker build -t omny-api:latest .

# 3. Lancer en local avec les variables d'environnement :
docker run -p 8080:8080 \
    -e JWT_SECRET="dev-secret-32chars-minimum-longeur!" \
    omny-api:latest

# 4. Tester :
curl http://localhost:8080/statut
# → { "statut": "ok" }

# 5. Vérifier la taille de l'image :
docker images omny-api
# → La taille doit être < 300 Mo avec le multi-stage build

# 6. Inspecter les couches :
docker history omny-api:latest
```

**Exercice 2 — Health check enrichi**

```swift title="Swift (Vapor) — Exercice 2 : endpoint de santé complet"
// Créez GET /santé qui retourne :
// {
//   "statut": "ok" | "dégradé" | "hors-ligne",
//   "version": "1.0.0",
//   "db": true | false,     // Peut-on requêter la DB ?
//   "timestamp": "ISO8601",
//   "environnement": "production" | "development"
// }
// Si la DB ne répond pas → statut: "dégradé", db: false, HTTP 503

struct SantéRéponse: Content {
    let statut: String
    let version: String
    let db: Bool
    let timestamp: String
    let environnement: String
}

app.get("santé") { req async -> Response in
    // TODO : tester la connexion DB avec une requête simple (ex: count)
    // Retourner 200 si ok, 503 si db indisponible
}
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir de ce module"
    Le **Dockerfile multi-stage** est la bonne pratique — image de build (2 Go) séparée de l'image de runtime (~200 Mo). **Railway** et **Render** sont les plateformes cloud les plus simples pour Vapor — PostgreSQL intégré, HTTPS automatique, déploiement depuis GitHub. Toute la configuration sensible (JWT_SECRET, DATABASE_URL) doit passer par des **variables d'environnement** — jamais en dur dans le code ni dans git. **GitHub Actions** automatise les tests + le déploiement — déployer uniquement si les tests passent. En production : log level à `.warning`, CORS restrictif, rate limiting activé, health check endpoint disponible.

!!! quote "Félicitations — La Formation Vapor est Terminée"
    Vous maîtrisez maintenant le backend Swift de A à Z : routage, décodage JSON, middlewares, Fluent ORM (SQLite → PostgreSQL), relations, requêtes avancées, authentification JWT, queues, tests et déploiement. La prochaine étape est le **Projet Mobile Sécurisé** — une application iOS complète connectée à un backend Vapor avec JWT, RBAC et les meilleures protections contre les attaques.

**Prochaine étape : [Projet Mobile Sécurisé](../../projet-securise/index.md)**

<br>
