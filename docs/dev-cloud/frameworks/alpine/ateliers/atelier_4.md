---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Ateliers UI #4

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Blog mock (Partie 1)

> Livrables : liste d’articles + recherche + catégories + favoris (local state)

### Objectif de l’atelier

Construire un mini “Blog UI” réaliste en Alpine, avec une structure maintenable :

* affichage d’une liste d’articles (objets)
* filtre par catégories
* recherche (debounce)
* favoris (toggle étoile) stockés **dans le state uniquement** (pas de persistance ici)
* UI claire : compteur, empty state, tri simple

On se place dans une logique “projet réel” : ton HTML reste lisible, ta logique est centralisée, et tes données ont une structure propre (id, title, excerpt, category, date, favorite).

---

## 1) Spécification fonctionnelle

### Fonctionnalités attendues

* Filtrer par catégorie : `all`, `frontend`, `backend`, `security`
* Rechercher sur le titre (et éventuellement l’extrait) avec debounce 300ms
* Trier (par date ou par titre)
* Mettre un article en favori
* Filtrer “favoris uniquement” (option pratique)
* Compteurs :

  * total
  * résultats affichés
  * nombre de favoris

### UX minimale

* Boutons filtres actifs visuellement
* Bouton reset
* Empty state clair
* Bouton “favori” accessible (aria-label)

---

## 2) Livrable complet (Vanilla + CDN) — prêt à coller

Copie-colle dans `blog-mock.html`.

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Atelier #4 — Blog mock (Alpine)</title>

    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      [x-cloak] { display: none !important; }

      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 16px;
        background: #fafafa;
      }

      .container {
        max-width: 920px;
        margin: 0 auto;
      }

      .card {
        background: #fff;
        border: 1px solid #eee;
        border-radius: 14px;
        padding: 16px;
      }

      .title {
        margin: 0;
        font-size: 20px;
      }

      .muted {
        color: #666;
        font-size: 14px;
        margin-top: 6px;
      }

      .row {
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
      }

      .controls {
        margin-top: 12px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }

      input[type="text"], select {
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: #fff;
      }

      input[type="text"] {
        flex: 1;
        min-width: 220px;
      }

      button {
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background: #111;
        color: #fff;
        cursor: pointer;
      }

      button.secondary {
        background: #fff;
        color: #111;
      }

      button:disabled {
        opacity: 0.55;
        cursor: not-allowed;
      }

      button:focus-visible, input:focus-visible, select:focus-visible {
        outline: 3px solid #111;
        outline-offset: 2px;
      }

      .filters {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      .filter-btn {
        background: #fff;
        color: #111;
      }

      .filter-btn.active {
        background: #111;
        color: #fff;
      }

      .badges {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 12px;
      }

      .badge {
        font-size: 12px;
        padding: 4px 8px;
        border: 1px solid #ddd;
        border-radius: 999px;
        background: #fff;
        color: #111;
      }

      .grid {
        margin-top: 12px;
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }

      @media (max-width: 820px) {
        .grid { grid-template-columns: 1fr; }
      }

      .post {
        border: 1px solid #eee;
        border-radius: 14px;
        padding: 14px;
        background: #fff;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .post-head {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: flex-start;
      }

      .post-title {
        margin: 0;
        font-size: 16px;
        line-height: 1.25;
      }

      .post-meta {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        color: #666;
        font-size: 12px;
      }

      .chip {
        font-size: 12px;
        border: 1px solid #ddd;
        border-radius: 999px;
        padding: 3px 8px;
        background: #fff;
        color: #111;
      }

      .excerpt {
        margin: 0;
        color: #333;
        font-size: 14px;
        line-height: 1.4;
      }

      .actions {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: center;
        margin-top: auto;
      }

      .fav-btn {
        background: #fff;
        color: #111;
      }

      .fav-btn.active {
        background: #111;
        color: #fff;
      }

      .empty {
        margin-top: 12px;
        color: #666;
      }
    </style>
  </head>

  <body>
    <div class="container" x-data="blogMock()">
      <div class="card">
        <h1 class="title">Blog mock — Partie 1</h1>
        <p class="muted">
          Liste + filtres + recherche debounce + favoris. Structure maintenable (data + getters + actions).
        </p>

        <!-- Controls -->
        <div class="controls">
          <!-- Recherche -->
          <input
            type="text"
            x-model="searchInput"
            placeholder="Rechercher un article..."
            aria-label="Rechercher"
            @input.debounce.300ms="applySearch()"
          />

          <!-- Tri -->
          <select x-model="sortBy" aria-label="Trier">
            <option value="date_desc">Date (récent → ancien)</option>
            <option value="date_asc">Date (ancien → récent)</option>
            <option value="title_asc">Titre (A → Z)</option>
            <option value="title_desc">Titre (Z → A)</option>
          </select>

          <!-- Favoris only -->
          <button
            type="button"
            class="secondary"
            :class="{ 'active': favoritesOnly }"
            @click="favoritesOnly = !favoritesOnly"
            :aria-pressed="favoritesOnly.toString()"
          >
            Favoris uniquement
          </button>

          <!-- Reset -->
          <button type="button" @click="reset()" class="secondary">
            Reset
          </button>
        </div>

        <!-- Catégories -->
        <div class="filters" style="margin-top: 12px;">
          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': category === 'all' }"
            @click="setCategory('all')"
          >
            All
          </button>

          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': category === 'frontend' }"
            @click="setCategory('frontend')"
          >
            Frontend
          </button>

          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': category === 'backend' }"
            @click="setCategory('backend')"
          >
            Backend
          </button>

          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': category === 'security' }"
            @click="setCategory('security')"
          >
            Security
          </button>
        </div>

        <!-- Badges -->
        <div class="badges">
          <span class="badge">
            Total : <strong x-text="totalCount"></strong>
          </span>

          <span class="badge">
            Résultats : <strong x-text="filteredPosts.length"></strong>
          </span>

          <span class="badge">
            Favoris : <strong x-text="favoritesCount"></strong>
          </span>
        </div>
      </div>

      <!-- Liste -->
      <div class="grid" style="margin-top: 12px;">
        <template x-for="post in filteredPosts" :key="post.id">
          <article class="post">
            <div class="post-head">
              <div style="min-width: 0;">
                <h2 class="post-title" x-text="post.title"></h2>

                <div class="post-meta" style="margin-top: 6px;">
                  <span class="chip" x-text="post.category"></span>
                  <span x-text="post.date"></span>
                </div>
              </div>

              <button
                type="button"
                class="fav-btn"
                :class="{ 'active': post.favorite }"
                @click="toggleFavorite(post.id)"
                :aria-label="post.favorite ? 'Retirer des favoris' : 'Ajouter aux favoris'"
              >
                <span x-show="!post.favorite">☆</span>
                <span x-show="post.favorite" x-cloak>★</span>
              </button>
            </div>

            <p class="excerpt" x-text="post.excerpt"></p>

            <div class="actions">
              <button type="button" class="secondary" @click="preview(post.id)">
                Lire (mock)
              </button>

              <span class="muted" style="margin:0;">
                id: <strong x-text="post.id"></strong>
              </span>
            </div>
          </article>
        </template>
      </div>

      <!-- Empty state -->
      <p class="empty" x-show="filteredPosts.length === 0" x-cloak>
        Aucun article ne correspond à ta recherche / tes filtres.
      </p>

      <script>
        function blogMock() {
          return {
            // Data (source of truth)
            posts: [
              {
                id: 1,
                title: "Alpine.js : x-data en pratique",
                excerpt: "Construire un state local propre, lisible et réutilisable.",
                category: "frontend",
                date: "2026-01-10",
                favorite: false,
              },
              {
                id: 2,
                title: "x-model : formulaires contrôlés",
                excerpt: "Structure pro : form, errors, touched, isSubmitting.",
                category: "frontend",
                date: "2026-01-11",
                favorite: true,
              },
              {
                id: 3,
                title: "XSS : pourquoi x-html est dangereux",
                excerpt: "Comprendre le risque, les attaques, et comment se protéger.",
                category: "security",
                date: "2026-01-12",
                favorite: false,
              },
              {
                id: 4,
                title: "Rendu dynamique : x-for + key",
                excerpt: "Éviter les bugs invisibles et structurer tes listes proprement.",
                category: "frontend",
                date: "2026-01-13",
                favorite: false,
              },
              {
                id: 5,
                title: "Backend mock : API et pagination (concept)",
                excerpt: "Comment on pense une liste côté API, même si on ne la code pas ici.",
                category: "backend",
                date: "2026-01-14",
                favorite: false,
              },
              {
                id: 6,
                title: "UX pro : outside, escape, debounce",
                excerpt: "Des interactions stables et prévisibles, comme un produit.",
                category: "frontend",
                date: "2026-01-15",
                favorite: true,
              },
            ],

            // Controls
            category: "all",
            sortBy: "date_desc",
            favoritesOnly: false,

            // Recherche debounce (pattern propre)
            searchInput: "",
            searchQuery: "",

            // Stats
            get totalCount() {
              return this.posts.length;
            },

            get favoritesCount() {
              return this.posts.filter((p) => p.favorite).length;
            },

            // Vue dérivée : filtre + recherche + tri
            get filteredPosts() {
              let list = [...this.posts];

              // 1) Catégorie
              if (this.category !== "all") {
                list = list.filter((p) => p.category === this.category);
              }

              // 2) Favoris only
              if (this.favoritesOnly) {
                list = list.filter((p) => p.favorite);
              }

              // 3) Recherche (titre + extrait)
              const q = this.searchQuery.trim().toLowerCase();
              if (q.length > 0) {
                list = list.filter((p) => {
                  return (
                    p.title.toLowerCase().includes(q) ||
                    p.excerpt.toLowerCase().includes(q)
                  );
                });
              }

              // 4) Tri
              if (this.sortBy === "date_desc") {
                list.sort((a, b) => b.date.localeCompare(a.date));
              }

              if (this.sortBy === "date_asc") {
                list.sort((a, b) => a.date.localeCompare(b.date));
              }

              if (this.sortBy === "title_asc") {
                list.sort((a, b) => a.title.localeCompare(b.title));
              }

              if (this.sortBy === "title_desc") {
                list.sort((a, b) => b.title.localeCompare(a.title));
              }

              return list;
            },

            // Actions
            setCategory(value) {
              this.category = value;
            },

            applySearch() {
              // debounce fait le job : on applique seulement après "pause"
              this.searchQuery = this.searchInput;
            },

            reset() {
              this.category = "all";
              this.sortBy = "date_desc";
              this.favoritesOnly = false;

              this.searchInput = "";
              this.searchQuery = "";
            },

            toggleFavorite(id) {
              const post = this.posts.find((p) => p.id === id);
              if (!post) return;

              post.favorite = !post.favorite;
            },

            preview(id) {
              // Mock : en atelier, on simule juste l’action
              const post = this.posts.find((p) => p.id === id);
              if (!post) return;

              console.log("Preview post:", post);
              alert(`Mock preview: ${post.title}`);
            },
          };
        }
      </script>
    </div>
  </body>
</html>
```

---

## 3) Explication formateur : pourquoi c’est structuré comme ça

### 1) `posts` = source of truth

Tu ne modifies pas “la liste affichée”.
Tu modifies uniquement `posts`, et l’UI se recalcule.

### 2) `filteredPosts` = vue dérivée

Tout est centralisé :

* catégorie
* favoris only
* recherche
* tri

Donc tu n’as pas de logique dispersée.

### 3) Favoris = un booléen dans l’objet

Pas besoin de persister ici, on reste sur du state local.
La persistance arrivera plus tard (Chapitre 10 + Persist).

### 4) Recherche debounce avec `searchInput` / `searchQuery`

Ça évite le spam de recalculs.
Et tu peux facilement changer le délai.

---

## 4) Pièges fréquents (à ne pas faire)

### Piège A — trier `this.posts` directement

`sort()` mute le tableau.
Donc on clone avant :

```js
let list = [...this.posts];
list.sort(...)
```

### Piège B — key non stable

Ici on fait :

```html
:Key="post.id"
```

Obligatoire pour un rendu stable.

### Piège C — logique “inline” dans le HTML

On évite les conditions illisibles dans le HTML.
Tout est dans le getter.

---

## 5) Exercices (obligatoires)

### Exercice 1 — Ajout d’un article (mock)

Ajoute un formulaire “Ajouter un post” :

* title
* excerpt
* category
* date
  À la soumission :
* push dans `posts`
* reset form

### Exercice 2 — Filtre “Favoris” en onglet

Au lieu d’un bouton toggle, fais un filtre supplémentaire :

* All / Favoris

### Exercice 3 — Badge dynamique de catégorie

Affiche une couleur de badge différente selon la catégorie
(même sans Tailwind, tu peux faire un `:class` simple).

---

## 6) Ce qu’on vient de valider (compétence réelle)

Tu sais :

* modéliser une liste d’objets
* afficher proprement avec `x-for` + `:key`
* construire un moteur filtre/recherche/tri
* gérer des interactions (favoris)
* produire une UI lisible et présentable

---

### Étape suivante logique

On enchaîne avec **Chapitre 6 — Réactivité & DOM control** :

* Leçon 1 : `x-effect` (réaction automatique)
* Leçon 2 : `$watch` (observer une variable)
* Leçon 3 : `x-ref` + `$refs` (contrôle du DOM : focus, scroll)
* Leçon 4 : `$nextTick` (attendre le DOM)
* Leçon 5 : `$el / $root / $data` (comprendre ce que tu manipules)

Quand tu dis “go”, je commence Chapitre 6, Leçon 1.
