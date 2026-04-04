---
description: "Architecture 02 — Clean Architecture : couches Domain/Application/Infrastructure, injection de dépendances et principes SOLID."
icon: lucide/book-open-check
tags: ["ARCHITECTURE", "CLEAN-ARCHITECTURE", "SOLID", "DDD", "INJECTION-DEPENDANCES"]
---

# Module 02 — Clean Architecture

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="2024"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Ville et ses Quartiers"
    Paris est structurée en quartiers distincts : les ministères (domaine métier) décident des lois, les services publics (application) les appliquent, et les entreprises privées (infrastructure) les exécutent. La règle d'or : les lois ne changent pas parce qu'un opérateur téléphonique change. Clean Architecture suit la même logique : le **domaine** (règles métier) ne dépend jamais de l'**infrastructure** (base de données, API externe).

<br>

---

## 1. Les Principes SOLID

```
S — Single Responsibility Principle
    Une classe = une seule responsabilité (une seule raison de changer)
    ❌ UserService gère les users ET envoie les emails ET fait des stats
    ✅ UserService : gestion des utilisateurs
       EmailService : envoi d'emails
       AnalyticsService : statistiques

O — Open/Closed Principle
    Ouvert à l'extension, fermé à la modification
    Ajouter des comportements via des interfaces, pas en modifiant le code existant

L — Liskov Substitution Principle
    Une sous-classe peut remplacer sa classe parente sans briser le comportement
    Si Dog extends Animal : partout où Animal est attendu, Dog doit fonctionner

I — Interface Segregation Principle
    Préférer plusieurs petites interfaces à une grande interface générale
    ❌ IAnimal { bark(); meow(); fly(); swim(); }  ← Tous les animaux implémentent tout
    ✅ IDog { bark(); }  ICat { meow(); }  IBird { fly(); }

D — Dependency Inversion Principle
    Dépendre des abstractions (interfaces), pas des implémentations concrètes
    ❌ UserService dépend de MySQLDatabase (concret)
    ✅ UserService dépend de IUserRepository (interface)
       MySQLUserRepository implémente IUserRepository
```

<br>

---

## 2. Structure des Couches

```
Clean Architecture — Les 4 couches (cercles concentriques) :

┌─────────────────────────────────────────────────┐
│  Infrastructure (couche externe)                │
│  ┌─────────────────────────────────────────┐    │
│  │  Application (Use Cases)                │    │
│  │  ┌───────────────────────────────────┐  │    │
│  │  │  Domain (cœur métier)             │  │    │
│  │  │  - Entities                       │  │    │
│  │  │  - Value Objects                  │  │    │
│  │  │  - Domain Events                  │  │    │
│  │  └───────────────────────────────────┘  │    │
│  │  - Use Cases (services applicatifs)     │    │
│  │  - Interfaces (ports)                   │    │
│  └─────────────────────────────────────────┘    │
│  - Repositories (BDD)                           │
│  - API Controllers (HTTP)                       │
│  - Email, File System, Cache                    │
└─────────────────────────────────────────────────┘

Règle fondamentale : les dépendances ne pointent QUE vers l'intérieur.
Domain ne connaît rien de la BDD. Application ne connaît pas Express.
```

```
Structure de dossiers recommandée :
src/
├── domain/                    ← Indépendant de tout framework
│   ├── entities/
│   │   └── Article.ts         ← Entité métier
│   ├── value-objects/
│   │   └── ArticleStatus.ts   ← Objet valeur (immuable)
│   ├── repositories/
│   │   └── IArticleRepository.ts  ← PORT (interface abstraite)
│   └── events/
│       └── ArticlePublished.ts
│
├── application/               ← Orchestration des cas d'usage
│   └── articles/
│       ├── CreateArticle.ts   ← Use Case
│       ├── PublishArticle.ts  ← Use Case
│       └── GetArticles.ts     ← Use Case (Query)
│
├── infrastructure/            ← Détails techniques (BDD, HTTP, Email)
│   ├── repositories/
│   │   └── PrismaArticleRepository.ts  ← ADAPTER (implémente le PORT)
│   ├── http/
│   │   └── ArticleController.ts        ← Couche HTTP (Express/Fastify)
│   └── email/
│       └── SendGridEmailService.ts
│
└── main.ts                    ← Composition Root (DI assembly)
```

<br>

---

## 3. Domain — Entités et Objets Valeur

```typescript title="TypeScript — Domain : Entity Article"
// src/domain/entities/Article.ts

export class Article {
    private constructor(
        public readonly id:        string,
        private          title:    string,
        private          content:  string,
        private          status:   ArticleStatus,
        public readonly  authorId: string,
        public readonly  createdAt: Date,
    ) {}

    // Factory method : logique de création dans l'entité
    static create(props: {
        title:    string;
        content:  string;
        authorId: string;
    }): Article {
        if (!props.title || props.title.trim().length < 3) {
            throw new Error("Le titre doit faire au moins 3 caractères");
        }
        if (!props.content || props.content.trim().length < 50) {
            throw new Error("Le contenu doit faire au moins 50 caractères");
        }

        return new Article(
            crypto.randomUUID(),
            props.title.trim(),
            props.content.trim(),
            ArticleStatus.DRAFT,
            props.authorId,
            new Date(),
        );
    }

    // Reconstruction depuis la persistance
    static reconstitute(data: ArticleData): Article {
        return new Article(
            data.id, data.title, data.content,
            data.status, data.authorId, data.createdAt
        );
    }

    // Méthodes métier (comportements de l'entité)
    publish(): void {
        if (this.status === ArticleStatus.PUBLISHED) {
            throw new Error("L'article est déjà publié");
        }
        this.status = ArticleStatus.PUBLISHED;
    }

    update(title: string, content: string): void {
        if (this.status === ArticleStatus.PUBLISHED) {
            throw new Error("Un article publié ne peut pas être modifié");
        }
        this.title   = title.trim();
        this.content = content.trim();
    }

    // Getters (lecture seule)
    get articleTitle():   string { return this.title; }
    get articleContent(): string { return this.content; }
    get articleStatus():  ArticleStatus { return this.status; }
    get isPublished():    boolean { return this.status === ArticleStatus.PUBLISHED; }
}
```

```typescript title="TypeScript — Domain : Port (interface de repository)"
// src/domain/repositories/IArticleRepository.ts

export interface IArticleRepository {
    findById(id: string):                     Promise<Article | null>;
    findAll(criteria?: ArticleCriteria):      Promise<Article[]>;
    save(article: Article):                   Promise<void>;
    delete(id: string):                       Promise<void>;
}

export interface ArticleCriteria {
    authorId?:  string;
    status?:    ArticleStatus;
    limit?:     number;
    offset?:    number;
}
```

<br>

---

## 4. Application — Use Cases

```typescript title="TypeScript — Application : Use Case CreateArticle"
// src/application/articles/CreateArticle.ts

// Interface du Use Case (port d'entrée)
export interface CreateArticleInput {
    title:    string;
    content:  string;
    authorId: string;
}

export interface CreateArticleOutput {
    id:     string;
    title:  string;
    status: string;
}

// Le Use Case dépend du PORT, pas de l'adaptateur
export class CreateArticleUseCase {
    constructor(
        private readonly articleRepo: IArticleRepository,   // Injection de l'interface
        private readonly eventBus?:  IEventBus,             // Optionnel
    ) {}

    async execute(input: CreateArticleInput): Promise<CreateArticleOutput> {
        // 1. Valider et créer via l'entité (logique métier dans le domaine)
        const article = Article.create({
            title:    input.title,
            content:  input.content,
            authorId: input.authorId,
        });

        // 2. Persister via le PORT (sans connaître MySQL/Prisma/etc)
        await this.articleRepo.save(article);

        // 3. Publier l'événement (optionnel)
        await this.eventBus?.publish(new ArticleCreatedEvent(article.id));

        // 4. Retourner le résultat (DTO)
        return {
            id:     article.id,
            title:  article.articleTitle,
            status: article.articleStatus,
        };
    }
}
```

<br>

---

## 5. Infrastructure — Adapters

```typescript title="TypeScript — Infrastructure : PrismaArticleRepository (Adapter)"
// src/infrastructure/repositories/PrismaArticleRepository.ts

import { PrismaClient } from '@prisma/client';

// L'ADAPTER implémente le PORT défini dans le domaine
export class PrismaArticleRepository implements IArticleRepository {
    constructor(private readonly prisma: PrismaClient) {}

    async findById(id: string): Promise<Article | null> {
        const data = await this.prisma.article.findUnique({ where: { id } });
        if (!data) return null;
        return Article.reconstitute(data);
    }

    async findAll(criteria?: ArticleCriteria): Promise<Article[]> {
        const rows = await this.prisma.article.findMany({
            where: {
                authorId: criteria?.authorId,
                status:   criteria?.status,
            },
            take: criteria?.limit  ?? 10,
            skip: criteria?.offset ?? 0,
        });
        return rows.map(Article.reconstitute);
    }

    async save(article: Article): Promise<void> {
        await this.prisma.article.upsert({
            where:  { id: article.id },
            create: this.toRecord(article),
            update: this.toRecord(article),
        });
    }

    async delete(id: string): Promise<void> {
        await this.prisma.article.delete({ where: { id } });
    }

    private toRecord(article: Article) {
        return {
            id:        article.id,
            title:     article.articleTitle,
            content:   article.articleContent,
            status:    article.articleStatus,
            authorId:  article.authorId,
            createdAt: article.createdAt,
        };
    }
}
```

```typescript title="TypeScript — Composition Root : assembler les dépendances"
// src/main.ts — Le seul endroit où les dépendances concrètes sont assemblées

import { PrismaClient } from '@prisma/client';
import express           from 'express';
import { PrismaArticleRepository } from './infrastructure/repositories/PrismaArticleRepository';
import { CreateArticleUseCase }     from './application/articles/CreateArticle';
import { ArticleController }        from './infrastructure/http/ArticleController';

async function bootstrap() {
    const prisma     = new PrismaClient();
    const articleRepo = new PrismaArticleRepository(prisma);           // Adapter

    const createArticle = new CreateArticleUseCase(articleRepo);       // Use Case

    const articleController = new ArticleController(createArticle);    // Controller

    const app = express();
    app.use(express.json());
    app.post('/api/articles', (req, res) => articleController.create(req, res));

    app.listen(3000, () => console.log('🚀 Serveur démarré sur :3000'));
}

bootstrap();
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Clean Architecture organise le code en **couches concentriques** : Domain (règles métier pures) → Application (use cases) → Infrastructure (BDD, HTTP, email). La règle fondamentale : **les dépendances ne pointent que vers l'intérieur**. Le Domain ne connaît ni Prisma ni Express. Le pattern **Port & Adapter** : le Domain définit l'interface (port), l'Infrastructure fournit l'implémentation (adapter). L'injection de dépendances via interfaces permet de **tester sans BDD** (en mockant le port). Le **Composition Root** (main.ts) est le seul endroit où tout est assemblé.

> Module suivant : [Patterns Pratiques →](./03-patterns-pratiques.md) — Repository, Service, Factory, Observer, CQRS.

<br>
