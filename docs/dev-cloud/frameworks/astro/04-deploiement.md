---
description: "Astro 04 — Déploiement : build statique, adapters SSR, Vercel, Netlify, Cloudflare Pages et optimisations."
icon: lucide/book-open-check
tags: ["ASTRO", "DEPLOIEMENT", "VERCEL", "NETLIFY", "CLOUDFLARE", "SSR", "BUILD"]
---

# Module 04 — Déploiement

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Astro 4.x"
  data-time="2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Livre Imprimé vs Le Journal en Direct"
    Publier un site Astro en mode statique (SSG), c'est comme imprimer un livre : vous le préparez une fois (le build), puis vous en distribuez des copies identiques à tous les lecteurs — rapide, fiable, économique. Le mode serveur (SSR), c'est le journal en direct : chaque page est générée au moment où le lecteur la demande, permettant du contenu personnalisé. Astro excelle dans les deux modes.

<br>

---

## 1. Build Statique (Mode par Défaut)

```bash title="Bash — Construire et prévisualiser le site"
# Build de production (génère dist/)
npm run build

# Prévisualiser le build localement
npm run preview
# http://localhost:4321

# Contenu généré dans dist/
# dist/
# ├── index.html
# ├── blog/
# │   ├── index.html
# │   └── intro-astro/index.html
# ├── _astro/          ← Assets hachés (CSS, JS)
# └── favicon.svg
```

```javascript title="JavaScript — astro.config.mjs : configuration build"
import { defineConfig } from 'astro/config';

export default defineConfig({
    site:   'https://mon-site.com',     // Obligatoire pour les URLs absolues
    output: 'static',                   // Mode statique (défaut)

    build: {
        assets:   '_assets',            // Dossier pour les assets compilés
        inlineStylesheets: 'auto',      // Inline les petits CSS
    },

    // Compression des images
    image: {
        service: { entrypoint: 'astro/assets/services/sharp' },
    },
});
```

<br>

---

## 2. Déploiement Vercel

```bash title="Bash — Déployer sur Vercel"
# Installer l'adapter Vercel
npx astro add vercel

# Installer la CLI Vercel
npm install -g vercel

# Déploiement (suit les instructions interactives la première fois)
vercel

# Déploiement en production
vercel --prod
```

```javascript title="JavaScript — astro.config.mjs avec adapter Vercel"
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel/static';  // Mode statique
// import vercel from '@astrojs/vercel/serverless'; // Mode SSR

export default defineConfig({
    output:  'static',    // ou 'server' pour le SSR
    adapter: vercel(),
    site:    'https://mon-site.vercel.app',
});
```

```json title="JSON — vercel.json : configuration optionnelle Vercel"
{
    "buildCommand": "npm run build",
    "outputDirectory": "dist",
    "framework": "astro",
    "headers": [
        {
            "source": "/_astro/(.*)",
            "headers": [
                { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
            ]
        }
    ]
}
```

<br>

---

## 3. Déploiement Netlify

```bash title="Bash — Déployer sur Netlify"
# Installer l'adapter Netlify
npx astro add netlify

# Installer la CLI Netlify
npm install -g netlify-cli

# Connexion à votre compte
netlify login

# Déploiement depuis le dossier dist/
netlify deploy --dir=dist

# Déploiement en production
netlify deploy --dir=dist --prod
```

```toml title="TOML — netlify.toml : configuration Netlify"
[build]
  command     = "npm run build"
  publish     = "dist"

[[headers]]
  for = "/_astro/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
```

<br>

---

## 4. Déploiement Cloudflare Pages

```bash title="Bash — Déployer sur Cloudflare Pages"
# Installer l'adapter Cloudflare
npx astro add cloudflare

# Via la CLI Wrangler
npm install -g wrangler
wrangler pages deploy dist --project-name=mon-site
```

```javascript title="JavaScript — astro.config.mjs pour Cloudflare"
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
    output:  'server',          // SSR avec Cloudflare Workers
    adapter: cloudflare(),
    site:    'https://mon-site.pages.dev',
});
```

<br>

---

## 5. Mode SSR (Server-Side Rendering)

```javascript title="JavaScript — astro.config.mjs : activer le SSR"
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
    output:  'server',    // 'static' | 'server' | 'hybrid'
    adapter: node({
        mode: 'standalone',   // Génère un serveur Node.js autonome
    }),
});
```

```astro title="Astro — Page SSR dynamique avec accès aux cookies et headers"
---
// En mode SSR, cette page est générée à chaque requête

// Accès à la requête HTTP
const { cookies, request } = Astro;

// Récupérer un cookie
const token = cookies.get('auth-token')?.value;

// Rediriger si non authentifié
if (!token) {
    return Astro.redirect('/login');
}

// Données en temps réel (pas de build)
const response = await fetch('https://api.example.com/user', {
    headers: { Authorization: `Bearer ${token}` }
});
const user = await response.json();
---

<html>
<body>
    <h1>Bonjour, {user.name}</h1>
    <p>Heure du serveur : {new Date().toLocaleTimeString('fr-FR')}</p>
</body>
</html>
```

```astro title="Astro — Mode hybride : mix statique + SSR par page"
---
// Mode 'hybrid' dans astro.config : statique par défaut
// Ajouter export const prerender = false pour une page SSR spécifique
export const prerender = false;

// Cette page est maintenant SSR (générée à chaque requête)
const data = await fetch('https://api.example.com/live-data').then(r => r.json());
---

<h1>Données en temps réel : {data.value}</h1>
```

<br>

---

## 6. GitHub Actions — CI/CD

```yaml title="YAML — .github/workflows/deploy.yml : CI/CD GitHub → Vercel"
name: Deploy Astro to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Installer les dépendances
        run: npm ci

      - name: Build Astro
        run: npm run build
        env:
          PUBLIC_API_URL: ${{ secrets.API_URL }}

      - name: Déployer sur Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token:   ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id:  ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./dist
          vercel-args:    '--prod'
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Astro propose trois modes : **`static`** (tout pré-généré au build — performance maximale), **`server`** (tout SSR — contenu dynamique), **`hybrid`** (mix : statique par défaut, SSR au besoin avec `export const prerender = false`). Chaque plateforme de déploiement nécessite un **adapter** spécifique (`@astrojs/vercel`, `@astrojs/netlify`, `@astrojs/cloudflare`, `@astrojs/node`). Les assets dans `_astro/` sont **hachés et immuables** — mettre un cache d'un an pour les performances. La **CI/CD GitHub Actions** automatise build + déploiement à chaque push.

> **Formation Astro complète.** Retour à l'[index Frameworks →](../index.md) ou explorer [React →](#) / [Vue →](#).

<br>
