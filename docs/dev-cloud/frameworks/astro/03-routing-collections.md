---
description: "Astro 03 — Routing & Collections : routing fichier, pages dynamiques, Content Collections API, Markdown et MDX."
icon: lucide/book-open-check
tags: ["ASTRO", "ROUTING", "CONTENT-COLLECTIONS", "MARKDOWN", "MDX", "DYNAMIC"]
---

# Routing & Collections

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Astro 4.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Bibliothèque Organisée"
    Dans une bibliothèque bien gérée, chaque livre a une cote (l'URL), chaque rayon correspond à un thème (le dossier dans `pages/`). Les **Content Collections** sont les catalogues de la bibliothèque : ils décrivent précisément ce que contient chaque rayon (le schéma), valident que les livres sont correctement étiquetés (validation TypeScript), et permettent de rechercher rapidement (API de requête).

<br>

---

## 1. Routing Basé sur les Fichiers

```
src/pages/
├── index.astro           → /
├── about.astro           → /about
├── contact.astro         → /contact
├── blog/
│   ├── index.astro       → /blog
│   └── [slug].astro      → /blog/:slug  (dynamique)
├── docs/
│   └── [...slug].astro   → /docs/:slug+ (catch-all)
└── api/
    └── posts.ts          → /api/posts   (API endpoint)
```

```astro title="Astro — Page statique simple"
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="À propos" description="Notre équipe et notre mission.">
    <main>
        <h1>À propos</h1>
        <p>Bienvenue sur notre site propulsé par Astro.</p>
    </main>
</BaseLayout>
```

<br>

---

## 2. Pages Dynamiques

```astro title="Astro — src/pages/blog/[slug].astro : page dynamique (SSG)"
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

// getStaticPaths() est OBLIGATOIRE pour les pages dynamiques en mode statique
// Elle retourne la liste de toutes les URL à générer au build
export async function getStaticPaths() {
    const articles = await getCollection('blog');

    return articles.map(article => ({
        params: { slug: article.slug },  // Valeur de [slug]
        props:  { article },             // Données passées à la page
    }));
}

// Props injectées par getStaticPaths
const { article } = Astro.props;
const { Content } = await article.render();  // Rendu Markdown → Composant
---

<BaseLayout title={article.data.title} description={article.data.description}>
    <article style="max-width: 750px; margin: 2rem auto; padding: 0 1rem;">
        <h1>{article.data.title}</h1>
        <p>Publié le {article.data.date.toLocaleDateString('fr-FR')}</p>

        <!-- Rendu du contenu Markdown -->
        <Content />
    </article>
</BaseLayout>
```

```typescript title="TypeScript — src/pages/api/posts.ts : API endpoint JSON"
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ url }) => {
    const articles = await getCollection('blog', (article) => {
        return !article.data.draft;  // Filtrer les brouillons
    });

    const data = articles.map(article => ({
        slug:        article.slug,
        title:       article.data.title,
        date:        article.data.date.toISOString(),
        description: article.data.description,
    }));

    return new Response(JSON.stringify(data), {
        status:  200,
        headers: { 'Content-Type': 'application/json' },
    });
};
```

<br>

---

## 3. Content Collections

```typescript title="TypeScript — src/content/config.ts : définir les schémas"
import { defineCollection, z } from 'astro:content';

// Collection "blog" : articles Markdown/MDX dans src/content/blog/
const blog = defineCollection({
    type: 'content',   // 'content' pour Markdown/MDX, 'data' pour JSON/YAML
    schema: z.object({
        title:       z.string().min(1).max(100),
        description: z.string().min(10).max(200),
        date:        z.date(),
        author:      z.string().default('Anonymous'),
        tags:        z.array(z.string()).default([]),
        image:       z.string().optional(),
        draft:       z.boolean().default(false),
    }),
});

// Collection "docs" : documentation technique
const docs = defineCollection({
    type: 'content',
    schema: z.object({
        title:   z.string(),
        order:   z.number().optional(),
        section: z.string().optional(),
    }),
});

// Exporter les collections (obligatoire)
export const collections = { blog, docs };
```

```markdown title="Markdown — src/content/blog/intro-astro.md : article de blog"
---
title:       "Introduction à Astro"
description: "Découvrez pourquoi Astro est le meilleur choix pour les sites de contenu."
date:        2024-03-15
author:      "Alice Dupont"
tags:        ["Astro", "SSG", "Performance"]
draft:       false
---

# Introduction à Astro

Astro est un framework web qui génère du HTML statique par défaut...

## Pourquoi Astro ?

- **Zéro JavaScript** par défaut
- **Architecture des Îles** pour l'interactivité
- **Content Collections** pour le contenu typé
```

```astro title="Astro — src/pages/blog/index.astro : liste des articles"
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

// Récupérer et trier les articles
const allArticles = await getCollection('blog', (article) => !article.data.draft);
const articles    = allArticles.sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
);
---

<BaseLayout title="Blog" description="Tous mes articles sur le développement web.">
    <main style="max-width: 900px; margin: 2rem auto; padding: 0 1rem;">
        <h1>Blog</h1>
        <p>{articles.length} articles publiés</p>

        <ul style="list-style: none; padding: 0;">
            {articles.map(article => (
                <li style="margin-bottom: 2rem;">
                    <a href={`/blog/${article.slug}`}>
                        <h2>{article.data.title}</h2>
                    </a>
                    <time>{article.data.date.toLocaleDateString('fr-FR')}</time>
                    <p>{article.data.description}</p>
                    <ul style="display: flex; gap: 0.5rem; list-style: none; padding: 0;">
                        {article.data.tags.map(tag => <li>#{tag}</li>)}
                    </ul>
                </li>
            ))}
        </ul>
    </main>
</BaseLayout>
```

<br>

---

## 4. MDX — Markdown avec Composants

```bash title="Bash — Ajouter le support MDX à Astro"
npx astro add mdx
```

```mdx title="MDX — src/content/blog/tutorial-avance.mdx : Markdown + Composants"
---
title: "Tutorial Astro Avancé"
description: "Exemple de MDX avec composants interactifs."
date: 2024-04-01
---

import Alert from '../../components/Alert.astro';
import Counter from '../../components/Counter.jsx';

# Tutorial Avancé

Le MDX permet d'utiliser des **composants dans le Markdown** :

<Alert type="warning" title="Attention">
    Assurez-vous d'avoir installé l'intégration MDX avec `npx astro add mdx`.
</Alert>

Voici un compteur interactif (composant React hydraté) :

<Counter client:visible />

Et voici du Markdown classique :

- Point 1
- Point 2
- **Point 3** avec mise en forme
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Le **routing Astro est basé sur les fichiers** : `src/pages/blog/[slug].astro` génère `/blog/:slug`. La fonction `getStaticPaths()` est obligatoire pour les routes dynamiques en mode statique — elle retourne toutes les URL à pré-générer. Les **Content Collections** définissent un schéma Zod pour valider le frontmatter Markdown et fournir une API TypeScript typée (`getCollection()`, `getEntry()`). **MDX** permet d'importer et d'utiliser des composants Astro/React/Vue directement dans du Markdown.

> Module suivant : [Déploiement →](./04-deploiement.md) — build statique, adapters SSR, Vercel/Netlify/Cloudflare.

<br>
