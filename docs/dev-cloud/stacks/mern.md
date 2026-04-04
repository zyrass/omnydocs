---
description: "MERN Stack — Architecture full-stack JavaScript : MongoDB, Express.js, React, Node.js. Setup, composants, state management, déploiement."
icon: lucide/layers-3
tags: ["MERN", "MONGODB", "EXPRESS", "REACT", "NODEJS", "FULLSTACK", "JAVASCRIPT"]
---

# MERN Stack

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2024"
  data-time="20-25 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Restaurant Libre-Service"
    Dans un restaurant classique (MEAN/Angular), le serveur vous apporte exactement ce que vous avez commandé sur la carte, dans l'ordre prévu. Dans un restaurant libre-service (MERN/React), vous prenez votre plateau et choisissez vous-même ce que vous mettez : entrée, plat, dessert, dans n'importe quel ordre. React n'impose pas de structure — vous assemblezez les bibliothèques selon votre besoin. Plus de liberté, plus de responsabilité.

La **MERN Stack** est la suite JavaScript la plus populaire en 2024 pour les applications web modernes :

| Lettre | Technologie | Rôle | Langage |
|---|---|---|---|
| **M** | MongoDB | Base de données document | JSON/BSON |
| **E** | Express.js | Serveur web / API REST | JavaScript/TypeScript |
| **R** | React | Framework frontend SPA | JavaScript/TypeScript |
| **N** | Node.js | Runtime JavaScript serveur | JavaScript/TypeScript |

> MERN est le choix le plus répandu pour les startups et les projets modernes. Sa flexibilité et l'immense écosystème React en font le point d'entrée privilégié du développement JS full-stack.

<br>

---

## 1. Architecture MERN

```mermaid
flowchart LR
    Client["🌐 Navigateur\nReact SPA (Vite)"] -->|HTTP / REST| API
    subgraph Node.js
        API["Express.js\nAPI REST (JSON)"] --> ODM
        ODM["Mongoose ODM"] --> DB
    end
    DB["MongoDB\nBase Document"]

    style Client fill:#61dafb,color:#000
    style API fill:#f0fdf4,stroke:#22c55e
    style DB fill:#f0f4ff,stroke:#4a6cf7
```

| Couche | Technologie | Port dev |
|---|---|---|
| Base de données | MongoDB (local ou Atlas) | 27017 |
| API Backend | Express.js | 5000 |
| Frontend | React + Vite | 5173 |

<br>

---

## 2. Setup MERN Stack

```bash title="Bash — Initialiser un projet MERN complet"
# ─── Structure projet ─────────────────────────────────────────────────────────
mkdir mern-app && cd mern-app

# ─── Backend ──────────────────────────────────────────────────────────────────
mkdir server && cd server
npm init -y
npm install express mongoose dotenv cors helmet morgan bcryptjs jsonwebtoken
npm install -D nodemon

# ─── Frontend (React + Vite) ──────────────────────────────────────────────────
cd ..
npm create vite@latest client -- --template react
cd client && npm install
npm install axios react-router-dom zustand @tanstack/react-query

# ─── Structure finale ─────────────────────────────────────────────────────────
# mern-app/
# ├── server/
# │   ├── models/
# │   ├── routes/
# │   ├── middleware/
# │   └── server.js
# └── client/
#     ├── src/
#     │   ├── components/
#     │   ├── pages/
#     │   ├── hooks/
#     │   └── services/
#     └── vite.config.js
```

```javascript title="JavaScript — server.js : serveur Express MERN"
// server/server.js
import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { articleRouter } from './routes/articles.js';
import { authRouter }    from './routes/auth.js';

dotenv.config();

const app = express();

// ─── Middleware ────────────────────────────────────────────────────────────────
app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:5173' }));
app.use(express.json());

// ─── Routes ───────────────────────────────────────────────────────────────────
app.use('/api/auth',     authRouter);
app.use('/api/articles', articleRouter);

// ─── Error Handler global ──────────────────────────────────────────────────────
app.use((err, _req, res, _next) => {
    const status = err.status || 500;
    res.status(status).json({
        message: err.message || 'Erreur interne',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
});

// ─── Connexion MongoDB + Start ─────────────────────────────────────────────────
mongoose.connect(process.env.MONGODB_URI)
    .then(() => {
        app.listen(process.env.PORT || 5000, () => {
            console.log(`🚀 API : http://localhost:${process.env.PORT || 5000}`);
        });
    })
    .catch(err => { console.error(err); process.exit(1); });
```

<br>

---

## 3. Backend — Mongoose + Express

```javascript title="JavaScript — Mongoose : Modèle Article avec virtuals"
// server/models/Article.js
import mongoose from 'mongoose';

const articleSchema = new mongoose.Schema({
    title: {
        type: String,
        required: [true, 'Le titre est obligatoire'],
        trim: true,
        maxlength: [200, 'Titre trop long (max 200 caractères)'],
    },
    slug:      { type: String, required: true, unique: true, lowercase: true },
    content:   { type: String, required: true },
    excerpt:   { type: String, maxlength: 500 },
    author:    { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    tags:      [{ type: String, trim: true, lowercase: true }],
    published: { type: Boolean, default: false },
    views:     { type: Number, default: 0 },
}, {
    timestamps: true,
    toJSON:  { virtuals: true },  // Inclure les virtuals dans la sérialisation JSON
    toObject: { virtuals: true },
});

// Virtual : URL de l'article (pas stockée en DB)
articleSchema.virtual('url').get(function () {
    return `/articles/${this.slug}`;
});

// Index composites
articleSchema.index({ published: 1, createdAt: -1 });
articleSchema.index({ slug: 1 });
articleSchema.index({ tags: 1 });

export const Article = mongoose.model('Article', articleSchema);
```

```javascript title="JavaScript — API REST Articles complète"
// server/routes/articles.js
import { Router } from 'express';
import { Article } from '../models/Article.js';
import { auth } from '../middleware/auth.js';

const router = Router();

// GET /api/articles?page=1&limit=10&tag=react
router.get('/', async (req, res, next) => {
    try {
        const { page = 1, limit = 10, tag, search } = req.query;
        const filter = { published: true };

        if (tag)    filter.tags = tag;
        if (search) filter.$text = { $search: search };

        const skip = (page - 1) * limit;
        const [articles, total] = await Promise.all([
            Article.find(filter)
                   .populate('author', 'name avatar')
                   .sort({ createdAt: -1 })
                   .skip(skip)
                   .limit(Number(limit))
                   .lean(),          // .lean() retourne un objet JS pur (plus rapide)
            Article.countDocuments(filter),
        ]);

        res.json({
            articles,
            pagination: { page: +page, total, pages: Math.ceil(total / limit) }
        });
    } catch (err) { next(err); }
});

// POST /api/articles (authentifié)
router.post('/', auth, async (req, res, next) => {
    try {
        const article = await Article.create({
            ...req.body,
            author: req.userId,
        });
        res.status(201).json(article);
    } catch (err) { next(err); }
});

export { router as articleRouter };
```

<br>

---

## 4. Frontend — React

```jsx title="JSX — React + TanStack Query : fetching et cache"
// client/src/hooks/useArticles.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

// Hook personnalisé : liste les articles
export function useArticles(page = 1, tag = null) {
    return useQuery({
        queryKey: ['articles', page, tag],   // Cache unique par page + tag
        queryFn:  () => api.get('/articles', { params: { page, tag } }).then(r => r.data),
        staleTime: 5 * 60 * 1000,            // 5 minutes de cache
        keepPreviousData: true,              // UX fluide lors du changement de page
    });
}

// Hook : créer un article
export function useCreateArticle() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (data) => api.post('/articles', data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['articles'] });
        },
    });
}
```

```jsx title="JSX — React : Composants avec hooks"
// client/src/pages/ArticlesPage.jsx
import { useState } from 'react';
import { useArticles } from '../hooks/useArticles';
import { ArticleCard } from '../components/ArticleCard';

export function ArticlesPage() {
    const [page, setPage] = useState(1);
    const { data, isLoading, isError } = useArticles(page);

    if (isLoading) return <div className="loader">Chargement…</div>;
    if (isError)   return <div className="error">Erreur chargement.</div>;

    return (
        <main>
            <h1>Articles</h1>

            <div className="articles-grid">
                {data.articles.map(article => (
                    <ArticleCard key={article._id} article={article} />
                ))}
            </div>

            {/* Pagination */}
            <nav className="pagination">
                <button
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                >
                    ← Précédent
                </button>
                <span>Page {page} / {data.pagination.pages}</span>
                <button
                    onClick={() => setPage(p => p + 1)}
                    disabled={page >= data.pagination.pages}
                >
                    Suivant →
                </button>
            </nav>
        </main>
    );
}

// client/src/components/ArticleCard.jsx
export function ArticleCard({ article }) {
    return (
        <article className="card">
            <h2>
                <a href={`/articles/${article.slug}`}>{article.title}</a>
            </h2>
            <p className="excerpt">{article.excerpt}</p>
            <footer>
                <img src={article.author.avatar} alt={article.author.name} />
                <span>{article.author.name}</span>
                <time dateTime={article.createdAt}>
                    {new Date(article.createdAt).toLocaleDateString('fr-FR')}
                </time>
                <div className="tags">
                    {article.tags.map(tag => (
                        <span key={tag} className="tag">{tag}</span>
                    ))}
                </div>
            </footer>
        </article>
    );
}
```

```javascript title="JavaScript — Zustand : state management léger"
// client/src/stores/authStore.js
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
    persist(
        (set) => ({
            user:  null,
            token: null,

            login: (user, token) => set({ user, token }),
            logout: () => set({ user: null, token: null }),
            isAuthenticated: () => !!useAuthStore.getState().token,
        }),
        { name: 'auth-storage' }   // Persiste dans localStorage
    )
);
```

<br>

---

## 5. Configuration & Déploiement

```bash title="Bash — .env MERN Stack"
# server/.env
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/mern-app
JWT_SECRET=your-secret-min-32-chars
JWT_EXPIRES_IN=7d
CLIENT_URL=https://monapp.com
```

```javascript title="JavaScript — vite.config.js : proxy API dev"
// client/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/api': {                         // Proxy /api → Express
                target: 'http://localhost:5000',
                changeOrigin: true,
            }
        }
    }
});
```

<br>

---

## MERN vs MEAN — Guide de Choix

| Critère | MERN (React) | MEAN (Angular) |
|---|---|---|
| **Popularité** | ⭐⭐⭐⭐⭐ (dominant) | ⭐⭐⭐⭐ |
| **Flexibilité** | Très haute (bibliothèque) | Moyenne (framework opiniâtre) |
| **Structure** | À définir | Imposée par Angular CLI |
| **TypeScript** | Optionnel (recommandé) | Natif (obligatoire) |
| **Courbe** | Moyenne | Élevée |
| **Idéal pour** | Startups, prototypes, SPA | Enterprise, grande équipe |
| **Écosystème** | npm géant, React Native | Angular Material, NX |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La MERN Stack domine le développement full-stack JavaScript en 2024 grâce à la popularité de React. Sa flexibilité est une force (choisir ses libraries : Zustand, TanStack Query, React Router…) et une faiblesse (chaque projet ré-invente ses conventions). **TanStack Query** pour le fetching, **Zustand** pour le state global, **Vite** pour le build — c'est le trio combiné recommandé. Côté backend, Express reste minimaliste : anticipez la structure dès le départ (routes, models, middleware, services). Comparer la TALL Stack Laravel pour des projets PHP, ou Angular si votre équipe favorise la rigueur TypeScript imposée.

> Pour les projets OmnyDocs, la [TALL Stack →](../frameworks/index.md) reste la référence principale.

<br>