---
description: "Astro — Hub de navigation : fondamentaux, composants, layouts, routing, collections de contenu et déploiement."
tags: ["ASTRO", "JAVASCRIPT", "SSG", "SSR", "CONTENT", "FRAMEWORK"]
---

# Astro

<div
  class="omny-meta"
  data-level="🟢 Débutant → 🟡 Intermédiaire"
  data-version="Astro 4.x"
  data-time="Hub">
</div>

## Présentation

!!! quote "Analogie pédagogique — L'Architecture des Îles"
    Un journal papier n'a pas besoin d'électricité pour être lu — il est statique et rapide. Mais si vous ajoutez un QR code vers une vidéo, seul ce petit élément nécessite de l'interactivité. Astro fonctionne de la même façon : vos pages sont des journaux statiques (HTML pur, zéro JavaScript), et vos composants interactifs (formulaire de recherche, carrousel) sont des **îles** — des zones isolées qui s'hydratent uniquement quand nécessaire. Résultat : performance maximale, JavaScript minimal.

**Astro** est un framework web orienté contenu. Il adopte l'**Architecture des Îles** pour livrer des sites ultra-rapides avec zéro JavaScript par défaut.

| Caractéristique | Valeur |
|---|---|
| **Créé par** | Fred K. Schott & l'équipe Astro (2021) |
| **Philosophie** | Content-first, Zero JS by default |
| **Rendu** | SSG (statique) + SSR (serveur) |
| **Composants UI** | React, Vue, Svelte, Lit, SolidJS (optionnel) |
| **Cas d'usage** | Blogs, docs, landing pages, sites marketing |

<br>

---

## Modules de cette Formation

| Module | Contenu | Niveau |
|---|---|---|
| [01 — Fondamentaux](./01-fondamentaux.md) | Installation, pages, syntaxe `.astro`, styles, imports | 🟢 |
| [02 — Composants & Layouts](./02-composants-layouts.md) | Composants Astro, layouts, slots, props | 🟡 |
| [03 — Routing & Collections](./03-routing-collections.md) | Routing fichier, pages dynamiques, Content Collections | 🟡 |
| [04 — Déploiement](./04-deploiement.md) | Build statique, adapters SSR, Vercel/Netlify/Cloudflare | 🟡 |

<br>

---

## Prérequis

- Node.js 18+ (`node --version`)
- Bases HTML/CSS
- Bases JavaScript (ES6 : modules, destructuring, async/await)

<br>
