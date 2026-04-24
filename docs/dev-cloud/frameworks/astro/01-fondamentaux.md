---
description: "Astro 01 — Fondamentaux : installation, pages .astro, frontmatter, styles scoped, imports et intégrations."
icon: lucide/book-open-check
tags: ["ASTRO", "JAVASCRIPT", "SSG", "FRONTMATTER", "SCOPED-CSS", "VITE"]
---

# Fondamentaux

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Astro 4.x / Node.js 18+"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Chef Pizzaiolo"
    Un pizzaiolo prépare sa pâte (HTML), choisit ses ingrédients (données du frontmatter), les dispose sur la pizza (template Astro), et enfourne le tout (build). La pizza sort du four **cuite et prête** — c'est votre HTML statique. Contrairement à React qui prépare la pâte **à chaque commande** (côté client), Astro la prépare **en avance** (au build) pour servir instantanément.

Astro génère du **HTML pur** au moment du build. Il n'envoie aucun JavaScript au navigateur sauf si vous le demandez explicitement. Chaque fichier `.astro` est un **composant** avec deux zones :

```
---
// Zone frontmatter (JavaScript/TypeScript — exécuté au BUILD, côté serveur)
const titre = "Bonjour Astro";
---

<!-- Zone de template (HTML + expressions {}) -->
<h1>{titre}</h1>
```

<br>

---

## 1. Installation & Démarrage

```bash title="Bash — Créer un projet Astro avec le CLI officiel"
# Créer un nouveau projet (mode interactif)
npm create astro@latest mon-site

# Ou en mode non-interactif (template minimal)
npm create astro@latest mon-site -- --template minimal --no-install

# Installer les dépendances
cd mon-site && npm install

# Lancer le serveur de développement (hot reload)
npm run dev
# http://localhost:4321
```

```
Structure d'un projet Astro :
mon-site/
├── src/
│   ├── pages/           ← Routes automatiques (index.astro → /)
│   │   └── index.astro
│   ├── components/      ← Composants Astro réutilisables
│   ├── layouts/         ← Layouts (template parent)
│   └── content/         ← Content Collections (markdown/JSON)
├── public/              ← Assets statiques (images, fonts — copiés tels quels)
├── astro.config.mjs     ← Configuration Astro
└── package.json
```

```javascript title="JavaScript — astro.config.mjs : configuration de base"
import { defineConfig } from 'astro/config';

export default defineConfig({
    // Site URL (obligatoire pour le SEO et le sitemap)
    site: 'https://mon-site.com',

    // Répertoire de sortie du build
    outDir: './dist',

    // Intégrations (React, Tailwind, MDX, etc.)
    integrations: [],

    // Mode de rendu par défaut : 'static' ou 'server'
    output: 'static',
});
```

<br>

---

## 2. Syntaxe des Fichiers `.astro`

```astro title="Astro — src/pages/index.astro : page d'accueil complète"
---
// FRONTMATTER — JavaScript/TypeScript
// Exécuté au build (Node.js), jamais envoyé au navigateur

// Import de composants
import Header from '../components/Header.astro';
import Card from   '../components/Card.astro';

// Variables locales
const pageTitle  = "Mon Blog Astro";
const description = "Articles sur le développement web";

// Récupérer des données (fetch côté serveur au build)
const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=3');
const posts    = await response.json();

// TypeScript natif
interface Post {
    id:    number;
    title: string;
    body:  string;
}

const featured: Post[] = posts;
---

<!-- TEMPLATE — HTML avec expressions JavaScript entre {} -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="description" content={description}>
    <title>{pageTitle}</title>
</head>
<body>
    <Header title={pageTitle} />

    <main>
        <h1>{pageTitle}</h1>

        <!-- Rendu conditionnel -->
        {featured.length > 0
            ? <p>{featured.length} articles disponibles</p>
            : <p>Aucun article pour le moment.</p>
        }

        <!-- Boucle -->
        <section>
            {featured.map((post) => (
                <Card
                    title={post.title}
                    body={post.body}
                    url={`/articles/${post.id}`}
                />
            ))}
        </section>
    </main>
</body>
</html>

<!-- STYLES — scopés au composant (aucune fuite CSS) -->
<style>
    main {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }

    h1 {
        font-size: 2.5rem;
        color: hsl(250, 80%, 50%);
    }

    section {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }
</style>
```

_Les styles dans `<style>` sont **scopés** automatiquement — Astro ajoute un attribut CSS unique (`class="astro-XXXXX"`) pour éviter les conflits entre composants._

<br>

---

## 3. Expressions et Logique dans les Templates

```astro title="Astro — Expressions, conditions et boucles"
---
const user       = { name: 'Alice', isAdmin: true };
const fruits     = ['Pomme', 'Banane', 'Orange'];
const showBanner = true;
---

<!-- Interpolation simple -->
<p>Bonjour, {user.name} !</p>

<!-- Expression JavaScript -->
<p>Majuscules : {user.name.toUpperCase()}</p>

<!-- Condition ternaire (obligatoire dans le template) -->
{user.isAdmin
    ? <span class="badge">Administrateur</span>
    : <span class="badge">Utilisateur</span>
}

<!-- Rendu conditionnel avec &&  -->
{showBanner && <div class="banner">Nouvelle fonctionnalité disponible !</div>}

<!-- Boucle .map() -->
<ul>
    {fruits.map((fruit, index) => (
        <li key={index}>{fruit}</li>
    ))}
</ul>

<!-- Fragment (grouper sans élément parent) -->
<>
    <dt>Clé</dt>
    <dd>Valeur</dd>
</>

<!-- HTML brut (dangereux — seulement si contenu de confiance) -->
<div set:html="<strong>HTML injecté</strong>" />
```

<br>

---

## 4. Styles : Scoped, Global et Tailwind

```astro title="Astro — Styles scoped, global et variables CSS"
---
const color = 'blue';
---

<!-- Styles scoped (par défaut) -->
<style>
    h1 { color: var(--primary); }  /* Ne s'applique qu'à CE composant */
</style>

<!-- Styles globaux (affectent toute la page) -->
<style is:global>
    :root {
        --primary:    hsl(250, 80%, 55%);
        --text:       hsl(220, 15%, 15%);
        --background: hsl(220, 20%, 97%);
    }

    * { box-sizing: border-box; margin: 0; }
    body { font-family: system-ui, sans-serif; color: var(--text); }
</style>

<!-- Styles inline dynamiques (valeur depuis le frontmatter) -->
<p style={`color: ${color}`}>Texte coloré</p>
```

```bash title="Bash — Ajouter Tailwind CSS à Astro"
# Intégration officielle Astro × Tailwind
npx astro add tailwind

# Génère automatiquement tailwind.config.mjs et adapte astro.config.mjs
```

```javascript title="JavaScript — astro.config.mjs avec Tailwind"
import { defineConfig } from 'astro/config';
import tailwind from    '@astrojs/tailwind';

export default defineConfig({
    integrations: [tailwind()],
});
```

<br>

---

## 5. Imports et Assets

```astro title="Astro — Importer styles, images, JSON et modules"
---
// Importer CSS global
import '../styles/global.css';

// Importer JSON directement
import data from '../data/articles.json';

// Importer une image (Astro optimise automatiquement)
import heroImage from '../assets/hero.webp';

// Importer un composant React, Vue ou Svelte (avec intégration installée)
import Counter from '../components/Counter.jsx';
---

<!-- Image optimisée par Astro (composant natif) -->
<img src={heroImage.src} alt="Image héro" width={heroImage.width} height={heroImage.height} />

<!-- Ou avec le composant Image natif (optimisation avancée) -->
<!-- import { Image } from 'astro:assets'; -->
<!-- <Image src={heroImage} alt="..." /> -->

<!-- Composant React "hydraté" = interactif côté client -->
<!-- client:load = hydraté immédiatement au chargement de la page -->
<Counter client:load />

<!-- client:visible = hydraté quand le composant entre dans la viewport -->
<!-- <Counter client:visible /> -->

<!-- client:idle = hydraté quand le navigateur est inactif -->
<!-- <Counter client:idle /> -->
```

_Les **directives de client** (`client:load`, `client:visible`, `client:idle`) contrôlent **quand** un composant UI framework est hydraté — c'est le cœur de l'Architecture des Îles d'Astro._

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Un fichier `.astro` est divisé en deux zones : le **frontmatter** (JavaScript au build, `---`) et le **template** (HTML + expressions `{}`). Les **styles sont scopés par défaut** — aucune fuite entre composants. Astro génère du **HTML statique pur** au build : zéro JavaScript envoyé au navigateur sauf directive `client:*` explicite. Le `public/` est copié tel quel ; les assets dans `src/assets/` sont **optimisés** (images, compression). Astro supporte **React, Vue, Svelte** simultanément dans le même projet.

> Module suivant : [Composants & Layouts →](./02-composants-layouts.md) — créer des composants réutilisables, layouts avec slots, passage de props.

<br>
