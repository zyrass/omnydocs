---
description: "Astro 02 — Composants & Layouts : composants .astro, props typées, slots nommés, layouts réutilisables et Head SEO."
icon: lucide/book-open-check
tags: ["ASTRO", "COMPOSANTS", "LAYOUTS", "SLOTS", "PROPS", "SEO"]
---

# Module 02 — Composants & Layouts

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Astro 4.x"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Les Pièces LEGO"
    Chaque composant Astro est une pièce LEGO : elle a une forme définie (les props), des emplacements pour d'autres pièces (les slots), et peut être assemblée de mille façons. Le Layout est la base LEGO — le plateau sur lequel vous construisez. Vous définissez les pièces une fois et les assemblez autant de fois que nécessaire, garantissant cohérence et maintenance facilitée.

<br>

---

## 1. Composants Astro

```astro title="Astro — src/components/Card.astro : composant avec props"
---
// Props typées avec TypeScript
interface Props {
    title:       string;
    description: string;
    url:         string;
    image?:      string;   // Optionnel
    tags?:       string[]; // Optionnel
}

// Déstructuration des props (avec valeur par défaut)
const {
    title,
    description,
    url,
    image       = '/images/default.webp',
    tags        = [],
} = Astro.props;
---

<article class="card">
    <img src={image} alt={title} loading="lazy" />

    <div class="card-body">
        <h2 class="card-title">
            <a href={url}>{title}</a>
        </h2>
        <p>{description}</p>

        {tags.length > 0 && (
            <ul class="tags">
                {tags.map(tag => <li class="tag">{tag}</li>)}
            </ul>
        )}
    </div>
</article>

<style>
    .card {
        border-radius: 0.75rem;
        overflow: hidden;
        box-shadow: 0 2px 12px hsl(0 0% 0% / 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px hsl(0 0% 0% / 0.15);
    }
    img { width: 100%; aspect-ratio: 16/9; object-fit: cover; }
    .card-body { padding: 1.25rem; }
    .card-title a { text-decoration: none; color: inherit; }
    .tags { display: flex; gap: 0.5rem; flex-wrap: wrap; list-style: none; padding: 0; margin-top: 0.75rem; }
    .tag { background: hsl(250 80% 95%); color: hsl(250 80% 40%); padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.8rem; }
</style>
```

```astro title="Astro — Utiliser le composant Card avec des props"
---
import Card from '../components/Card.astro';

const articles = [
    {
        title:       'Introduction à Astro',
        description: 'Découvrez le framework qui révolutionne le web statique.',
        url:         '/articles/intro-astro',
        tags:        ['Astro', 'SSG', 'Performance'],
    },
    {
        title:       'Architecture des Îles',
        description: 'Comprendre le concept central d\'Astro.',
        url:         '/articles/islands',
        tags:        ['Architecture', 'JavaScript'],
    },
];
---

<section class="grid">
    {articles.map(article => (
        <Card
            title={article.title}
            description={article.description}
            url={article.url}
            tags={article.tags}
        />
    ))}
</section>
```

<br>

---

## 2. Slots — Contenu Dynamique

```astro title="Astro — src/components/Alert.astro : composant avec slot"
---
interface Props {
    type?: 'info' | 'warning' | 'error' | 'success';
    title?: string;
}

const { type = 'info', title } = Astro.props;

const icons = {
    info:    'ℹ️',
    warning: '⚠️',
    error:   '❌',
    success: '✅',
};
---

<div class={`alert alert-${type}`}>
    {title && <strong class="alert-title">{icons[type]} {title}</strong>}
    <!-- slot : l'enfant injecté depuis le parent -->
    <slot />
</div>

<style>
    .alert { padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
    .alert-info    { background: hsl(210 100% 95%); border-left: 4px solid hsl(210 100% 50%); }
    .alert-warning { background: hsl(45 100% 93%);  border-left: 4px solid hsl(45 100% 45%); }
    .alert-error   { background: hsl(0 100% 95%);   border-left: 4px solid hsl(0 100% 60%); }
    .alert-success { background: hsl(145 80% 93%);  border-left: 4px solid hsl(145 80% 40%); }
    .alert-title   { display: block; margin-bottom: 0.5rem; }
</style>
```

```astro title="Astro — Slots nommés : plusieurs zones d'injection"
---
// src/components/TwoColumns.astro
---

<div class="two-columns">
    <aside class="sidebar">
        <!-- Slot nommé "sidebar" -->
        <slot name="sidebar" />
    </aside>
    <main class="content">
        <!-- Slot par défaut -->
        <slot />
    </main>
</div>

<style>
    .two-columns { display: grid; grid-template-columns: 250px 1fr; gap: 2rem; }
</style>
```

```astro title="Astro — Utiliser les slots nommés"
---
import TwoColumns from '../components/TwoColumns.astro';
import Alert from '../components/Alert.astro';
---

<TwoColumns>
    <!-- Slot nommé : slot="sidebar" -->
    <nav slot="sidebar">
        <ul>
            <li><a href="#section1">Section 1</a></li>
            <li><a href="#section2">Section 2</a></li>
        </ul>
    </nav>

    <!-- Slot par défaut (pas d'attribut slot) -->
    <h1>Contenu principal</h1>
    <Alert type="success" title="Succès">
        L'opération s'est terminée correctement.
    </Alert>
    <p>Lorem ipsum dolor sit amet...</p>
</TwoColumns>
```

<br>

---

## 3. Layouts

```astro title="Astro — src/layouts/BaseLayout.astro : layout principal"
---
interface Props {
    title:        string;
    description?: string;
    image?:       string;
}

const {
    title,
    description = 'Mon site Astro',
    image       = '/og-default.png',
} = Astro.props;

const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO -->
    <title>{title}</title>
    <meta name="description" content={description}>
    <link rel="canonical" href={canonicalURL}>

    <!-- Open Graph -->
    <meta property="og:title"       content={title}>
    <meta property="og:description" content={description}>
    <meta property="og:image"       content={new URL(image, Astro.site)}>
    <meta property="og:type"        content="website">
    <meta property="og:url"         content={canonicalURL}>

    <!-- Twitter Card -->
    <meta name="twitter:card"        content="summary_large_image">
    <meta name="twitter:title"       content={title}>
    <meta name="twitter:description" content={description}>

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">

    <!-- Styles globaux -->
    <style is:global>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --color-primary:    hsl(250 80% 55%);
            --color-text:       hsl(220 15% 15%);
            --color-muted:      hsl(220 10% 60%);
            --color-background: hsl(220 20% 98%);
            --font-sans: system-ui, -apple-system, sans-serif;
        }
        body {
            font-family: var(--font-sans);
            color: var(--color-text);
            background: var(--color-background);
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <header class="site-header">
        <nav>
            <a href="/" class="logo">Mon Site</a>
            <ul>
                <li><a href="/blog">Blog</a></li>
                <li><a href="/about">À propos</a></li>
            </ul>
        </nav>
    </header>

    <!-- Contenu de la page -->
    <slot />

    <footer class="site-footer">
        <p>© {new Date().getFullYear()} Mon Site — Propulsé par Astro</p>
    </footer>
</body>
</html>

<style>
    .site-header { padding: 1rem 2rem; border-bottom: 1px solid hsl(0 0% 90%); }
    .site-header nav { display: flex; align-items: center; justify-content: space-between; max-width: 1200px; margin: auto; }
    .logo { font-size: 1.25rem; font-weight: 700; text-decoration: none; color: var(--color-primary); }
    nav ul { display: flex; gap: 1.5rem; list-style: none; }
    nav a { text-decoration: none; color: var(--color-text); }
    .site-footer { padding: 2rem; text-align: center; color: var(--color-muted); border-top: 1px solid hsl(0 0% 90%); margin-top: 4rem; }
</style>
```

```astro title="Astro — Utiliser un layout dans une page"
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
    title="À propos de nous"
    description="Découvrez notre équipe et notre mission."
>
    <main style="max-width: 800px; margin: 2rem auto; padding: 0 1rem;">
        <h1>À propos</h1>
        <p>Bienvenue sur notre site Astro...</p>
    </main>
</BaseLayout>
```

```astro title="Astro — Layout dédié pour les articles Markdown"
---
// src/layouts/ArticleLayout.astro
import BaseLayout from './BaseLayout.astro';

interface Props {
    frontmatter: {
        title:       string;
        description: string;
        date:        string;
        author?:     string;
        tags?:       string[];
    };
}

const { frontmatter } = Astro.props;
const date = new Date(frontmatter.date).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'long', year: 'numeric'
});
---

<BaseLayout title={frontmatter.title} description={frontmatter.description}>
    <article style="max-width: 750px; margin: 2rem auto; padding: 0 1rem;">
        <header>
            <h1>{frontmatter.title}</h1>
            <p class="meta">
                Publié le {date}
                {frontmatter.author && ` par ${frontmatter.author}`}
            </p>
        </header>

        <!-- slot : le contenu Markdown rendu en HTML -->
        <slot />
    </article>
</BaseLayout>
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Les **composants Astro** acceptent des **props typées TypeScript** via `Astro.props`. Les **slots** injectent du contenu enfant — `<slot />` (défaut) ou `<slot name="xxx" />` (nommé). Les **layouts** sont des composants spéciaux qui enveloppent le contenu des pages — ils centralisent le `<html>`, la navigation et le SEO. Le slot `<slot />` dans un layout reçoit tout le contenu `<BaseLayout> [ici] </BaseLayout>`. Pour les **articles Markdown**, le layout est déclaré dans le frontmatter via la clé `layout:`.

> Module suivant : [Routing & Collections →](./03-routing-collections.md) — routing fichier, pages dynamiques et Content Collections.

<br>
