---
description: "MEAN Stack — Architecture full-stack JavaScript : MongoDB, Express.js, Angular, Node.js. Setup, structure, flux de données, déploiement."
tags: ["MEAN", "MONGODB", "EXPRESS", "ANGULAR", "NODEJS", "FULLSTACK", "TYPESCRIPT"]
---

# MEAN Stack

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2024"
  data-time="20-25 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Orchestra TypeScript"
    Dans un orchestre, chaque musicien joue un instrument différent mais tous lisent la même partition dans la même langue. La MEAN Stack est cet orchestre : **MongoDB** stocke les données en JSON, **Express** expose des APIs JSON, **Angular** consomme du JSON avec TypeScript, **Node.js** orchestre le tout. Un seul langage — JavaScript/TypeScript — du serveur au client. Pas de traduction entre les couches.

La **MEAN Stack** est une suite complète de technologies JavaScript/TypeScript pour construire des applications web from conception à production :

| Lettre | Technologie | Rôle | Langage |
|---|---|---|---|
| **M** | MongoDB | Base de données document | JSON/BSON |
| **E** | Express.js | Serveur web / API | JavaScript/TypeScript |
| **A** | Angular | Framework frontend SPA | TypeScript |
| **N** | Node.js | Runtime JavaScript serveur | JavaScript/TypeScript |

> MEAN est la variante **Angular** de l'écosystème Node+MongoDB. Sa force : TypeScript natif partout, parfait pour les équipes enterprise. À comparer avec [MERN (React) →](./mern.md).

<br>

---

## 1. Architecture MEAN

```mermaid
flowchart LR
    Client["🌐 Navigateur\nAngular SPA"] -->|HTTP/WebSocket| API
    subgraph Node.js
        API["Express.js\nAPI REST / GraphQL"] --> Models
        Models["Mongoose ODM"] --> DB
    end
    DB["MongoDB\nBase Document"]

    style Client fill:#dd0031,color:#fff
    style API fill:#f0fdf4,stroke:#22c55e
    style DB fill:#f0f4ff,stroke:#4a6cf7
```

**Flux d'une requête MEAN :**

```
1. Utilisateur clique sur "Charger les articles" (Angular Component)
2. Angular HttpClient: GET /api/articles
3. Express Route: router.get('/api/articles', ArticleController.index)
4. Mongoose: Article.find({ published: true }).sort('-createdAt')
5. MongoDB retourne les documents JSON
6. Express sérialise en JSON → Response 200
7. Angular reçoit le JSON → met à jour le component
8. Angular re-render la vue avec les données
```

<br>

---

## 2. Setup MEAN Stack

```bash title="Bash — Initialiser un projet MEAN complet"
# ─── Structure recommandée ────────────────────────────────────────────────────
mkdir mean-app
cd mean-app
mkdir backend frontend

# ─── Backend (Express + MongoDB) ─────────────────────────────────────────────
cd backend
npm init -y
npm install express mongoose dotenv cors helmet morgan
npm install -D typescript ts-node @types/node @types/express nodemon

# ─── Frontend (Angular) ───────────────────────────────────────────────────────
cd ../frontend
npm install -g @angular/cli
ng new client --routing --style=scss --standalone
```

<br>

---

## 3. Backend — Express + MongoDB

```typescript title="TypeScript — server.ts : serveur Express de base"
// backend/src/server.ts
import express, { Application, Request, Response } from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

import { articleRouter } from './routes/articles';

dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 3000;

// ─── Middleware globaux ────────────────────────────────────────────────────────
app.use(helmet());                       // Headers de sécurité
app.use(cors({ origin: process.env.CLIENT_URL }));
app.use(express.json());

// ─── Routes ───────────────────────────────────────────────────────────────────
app.use('/api/articles', articleRouter);

app.get('/api/health', (_req: Request, res: Response) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ─── Connexion MongoDB ────────────────────────────────────────────────────────
mongoose.connect(process.env.MONGODB_URI!)
    .then(() => {
        console.log('✅ MongoDB connecté');
        app.listen(PORT, () => console.log(`🚀 Serveur : http://localhost:${PORT}`));
    })
    .catch((err) => {
        console.error('❌ MongoDB erreur :', err.message);
        process.exit(1);
    });
```

```typescript title="TypeScript — Mongoose : Modèle + Interface TypeScript"
// backend/src/models/Article.ts
import { Schema, model, Document } from 'mongoose';

// Interface TypeScript (contrat)
export interface IArticle extends Document {
    title:     string;
    content:   string;
    slug:      string;
    published: boolean;
    author:    Schema.Types.ObjectId;
    tags:      string[];
    createdAt: Date;
    updatedAt: Date;
}

// Schéma Mongoose
const ArticleSchema = new Schema<IArticle>({
    title:     { type: String, required: true, trim: true },
    content:   { type: String, required: true },
    slug:      { type: String, required: true, unique: true },
    published: { type: Boolean, default: false },
    author:    { type: Schema.Types.ObjectId, ref: 'User', required: true },
    tags:      [{ type: String, trim: true }],
}, {
    timestamps: true,              // Ajoute createdAt + updatedAt automatiquement
});

// Index pour les requêtes fréquentes
ArticleSchema.index({ slug: 1 });
ArticleSchema.index({ published: 1, createdAt: -1 });
ArticleSchema.index({ tags: 1 });

export const Article = model<IArticle>('Article', ArticleSchema);
```

```typescript title="TypeScript — Express Router + Controller"
// backend/src/routes/articles.ts
import { Router, Request, Response, NextFunction } from 'express';
import { Article } from '../models/Article';

export const articleRouter = Router();

// GET /api/articles — Lister les articles publiés
articleRouter.get('/', async (req: Request, res: Response, next: NextFunction) => {
    try {
        const { page = 1, limit = 10, tag } = req.query;

        const filter: Record<string, unknown> = { published: true };
        if (tag) filter.tags = tag;

        const [articles, total] = await Promise.all([
            Article.find(filter)
                .populate('author', 'name avatar')
                .sort({ createdAt: -1 })
                .skip((+page - 1) * +limit)
                .limit(+limit),
            Article.countDocuments(filter),
        ]);

        res.json({
            data: articles,
            pagination: { page: +page, limit: +limit, total, pages: Math.ceil(total / +limit) },
        });
    } catch (err) {
        next(err);
    }
});

// GET /api/articles/:slug
articleRouter.get('/:slug', async (req: Request, res: Response, next: NextFunction) => {
    try {
        const article = await Article.findOne({ slug: req.params.slug, published: true })
            .populate('author', 'name avatar bio');

        if (!article) return res.status(404).json({ message: 'Article non trouvé' });

        res.json(article);
    } catch (err) {
        next(err);
    }
});

// POST /api/articles
articleRouter.post('/', async (req: Request, res: Response, next: NextFunction) => {
    try {
        const article = await Article.create({
            ...req.body,
            author: req.user!._id,                  // Injecté par authMiddleware
        });
        res.status(201).json(article);
    } catch (err) {
        next(err);
    }
});
```

<br>

---

## 4. Frontend — Angular

```typescript title="TypeScript — Angular Service : HttpClient"
// frontend/src/app/services/article.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Article {
    _id:       string;
    title:     string;
    content:   string;
    slug:      string;
    published: boolean;
    author:    { name: string; avatar: string };
    tags:      string[];
    createdAt: string;
}

interface PaginatedResponse<T> {
    data:       T[];
    pagination: { page: number; limit: number; total: number; pages: number };
}

@Injectable({ providedIn: 'root' })
export class ArticleService {
    private readonly http = inject(HttpClient);
    private readonly apiUrl = '/api/articles';

    getAll(page = 1, tag?: string): Observable<PaginatedResponse<Article>> {
        let params = new HttpParams().set('page', page).set('limit', '10');
        if (tag) params = params.set('tag', tag);

        return this.http.get<PaginatedResponse<Article>>(this.apiUrl, { params });
    }

    getBySlug(slug: string): Observable<Article> {
        return this.http.get<Article>(`${this.apiUrl}/${slug}`);
    }

    create(data: Partial<Article>): Observable<Article> {
        return this.http.post<Article>(this.apiUrl, data);
    }
}
```

```typescript title="TypeScript — Angular Component (Standalone)"
// frontend/src/app/pages/articles/articles.component.ts
import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ArticleService, Article } from '../../services/article.service';

@Component({
    selector: 'app-articles',
    standalone: true,
    imports: [CommonModule, RouterLink],
    template: `
        <div class="articles-grid">
            @if (loading()) {
                <div class="loader">Chargement...</div>
            }
            @for (article of articles(); track article._id) {
                <article class="card">
                    <h2>
                        <a [routerLink]="['/articles', article.slug]">
                            {{ article.title }}
                        </a>
                    </h2>
                    <p class="meta">
                        Par {{ article.author.name }} —
                        {{ article.createdAt | date:'dd MMMM yyyy' }}
                    </p>
                    <div class="tags">
                        @for (tag of article.tags; track tag) {
                            <span class="tag">{{ tag }}</span>
                        }
                    </div>
                </article>
            }
            @if (!loading() && articles().length === 0) {
                <p>Aucun article disponible.</p>
            }
        </div>
    `,
})
export class ArticlesComponent implements OnInit {
    private readonly articleService = inject(ArticleService);

    articles = signal<Article[]>([]);
    loading  = signal(true);

    ngOnInit(): void {
        this.articleService.getAll().subscribe({
            next:     (res) => { this.articles.set(res.data); this.loading.set(false); },
            error:    () => this.loading.set(false),
            complete: () => this.loading.set(false),
        });
    }
}
```

<br>

---

## 5. `.env` et Déploiement

```bash title="Bash — .env backend MEAN Stack"
# Backend
NODE_ENV=production
PORT=3000
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/mean-app
JWT_SECRET=your-super-secret-key-min-32-chars
CLIENT_URL=https://monapp.com

# Frontend (environment.prod.ts)
# API_URL=https://api.monapp.com
```

```bash title="Bash — Scripts npm recommandés"
# backend/package.json scripts :
# "dev"   : "nodemon --exec ts-node src/server.ts"
# "build" : "tsc"
# "start" : "node dist/server.js"

# Lancement développement complet (racine du projet) :
# npm run dev:backend  → http://localhost:3000
# npm run dev:frontend → http://localhost:4200 (ng serve)
```

<br>

---

## Avantages & Limites MEAN

| ✅ Avantages | ❌ Limites |
|---|---|
| TypeScript natif partout | Courbe d'apprentissage Angular élevée |
| JSON bout en bout (pas de conversion) | MongoDB sans transactions ACID complexes |
| Scalabilité horizontale native | Boilerplate Angular plus verbeux que React/Vue |
| Angular CLI : structure enterprise | Moins populaire que MERN (React) |
| Modules DI natif Angular = testabilité | Node.js single-thread (CPU-intensive = problème) |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La MEAN Stack brille pour les applications **enterprise TypeScript** où la cohérence de typage end-to-end est prioritaire. Angular impose une structure stricte (modules, DI, decorators) qui convient aux grandes équipes avec des conventions fortes. MongoDB + Mongoose offre la flexibilité documentaire pour les schémas évolutifs. En 2024, **MERN (React)** domine en popularité, mais MEAN reste le choix références d'entreprises comme Google et diverses banques qui ont adopté Angular comme standard interne.

> Comparer avec [MERN Stack (React) →](./mern.md) pour choisir entre Angular et React.

<br>