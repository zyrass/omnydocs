---
description: "Formation complète sur la technologie alpine.js"
icon: lucide/mountain
tags: ["ALPINE", "JAVASCRIPT", "REACTIVE", "FRONTEND", "CYBERSECURITY", "PENTEST"]
status: alpha
---

# Ateliers UI #3

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="3.13.3"
  data-time="15-16 heures">
</div>

## Todo list avancée (filtres + animation + recherche debounce)

## Objectif de l’atelier

Améliorer la Todo list “simple” pour en faire une version beaucoup plus réaliste, avec :

* filtres **All / Active / Done**
* recherche **debounce**
* animation ajout/suppression (via transitions)
* UX plus propre (état vide, compteur, actions rapides)
* structure maintenable (state clair + getters + méthodes)

On ne fait pas une “app parfaite”, on fait une app **solide et vendable** pédagogiquement.

---

## 1) Spécification fonctionnelle

### Fonctionnalités attendues

* ajouter une tâche
* cocher une tâche (done)
* supprimer une tâche
* filtrer :

  * All (tout)
  * Active (non terminées)
  * Done (terminées)
* rechercher une tâche (recherche live avec debounce)
* afficher des stats :

  * total
  * active
  * done

### UX attendue

* pas de tâche vide
* reset input après ajout
* état vide clair (“aucune tâche”)
* boutons filtres visuellement actifs
* suppression des terminées (clear done)

---

## 2) Livrable complet (Vanilla + CDN) — prêt à coller

Copie-colle dans `todo-advanced.html`.

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Atelier #3 — Todo avancée (Alpine)</title>

    <script defer src="https://unpkg.com/alpinejs"></script>

    <style>
      [x-cloak] {
        display: none !important;
      }

      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 16px;
        background: #fafafa;
      }

      .card {
        max-width: 720px;
        margin: 0 auto;
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
      }

      .row {
        display: flex;
        gap: 8px;
        align-items: center;
      }

      .stack {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 12px;
      }

      input[type="text"] {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
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
        opacity: 0.5;
        cursor: not-allowed;
      }

      button:focus-visible,
      input:focus-visible {
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

      .badge {
        font-size: 12px;
        padding: 4px 8px;
        border: 1px solid #ddd;
        border-radius: 999px;
        background: #fff;
        color: #111;
      }

      ul {
        list-style: none;
        padding: 0;
        margin: 0;
      }

      li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 10px 12px;
        border: 1px solid #eee;
        border-radius: 12px;
      }

      .todo-left {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
      }

      .todo-text {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 420px;
      }

      .done {
        text-decoration: line-through;
        opacity: 0.6;
      }

      /* Transitions Alpine */
      .fade-enter {
        opacity: 0;
        transform: translateY(-6px);
      }
      .fade-enter-active {
        transition: all 160ms ease;
      }
      .fade-enter-to {
        opacity: 1;
        transform: translateY(0);
      }

      .fade-leave {
        opacity: 1;
        transform: translateY(0);
      }
      .fade-leave-active {
        transition: all 160ms ease;
      }
      .fade-leave-to {
        opacity: 0;
        transform: translateY(-6px);
      }
    </style>
  </head>

  <body>
    <div class="card" x-data="todoAdvanced()">
      <h1 class="title">Todo list — version avancée</h1>
      <p class="muted">
        Filtres + recherche debounce + transitions. Structure pro (state + getters + méthodes).
      </p>

      <div class="stack">
        <!-- Ajout -->
        <form class="row" @submit.prevent="addTodo()">
          <input
            type="text"
            x-model="newTodo"
            placeholder="Ex: Réviser x-on + modificateurs"
            aria-label="Nouvelle tâche"
          />

          <button type="submit" :disabled="newTodo.trim().length === 0">
            Ajouter
          </button>
        </form>

        <!-- Recherche -->
        <div class="row">
          <input
            type="text"
            x-model="searchInput"
            placeholder="Rechercher une tâche..."
            aria-label="Rechercher"
            @input.debounce.300ms="applySearch()"
          />

          <button type="button" class="secondary" @click="resetSearch()" :disabled="searchInput.trim().length === 0">
            Reset recherche
          </button>
        </div>

        <!-- Filtres -->
        <div class="filters">
          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': filter === 'all' }"
            @click="setFilter('all')"
          >
            All
          </button>

          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': filter === 'active' }"
            @click="setFilter('active')"
          >
            Active
          </button>

          <button
            type="button"
            class="filter-btn"
            :class="{ 'active': filter === 'done' }"
            @click="setFilter('done')"
          >
            Done
          </button>
        </div>

        <!-- Stats + actions -->
        <div class="row" style="justify-content: space-between;">
          <div class="row">
            <span class="badge">
              Total : <strong x-text="totalCount"></strong>
            </span>

            <span class="badge">
              Active : <strong x-text="activeCount"></strong>
            </span>

            <span class="badge">
              Done : <strong x-text="doneCount"></strong>
            </span>
          </div>

          <div class="row">
            <button
              type="button"
              class="secondary"
              @click="markAllDone()"
              :disabled="activeCount === 0"
            >
              Tout cocher
            </button>

            <button
              type="button"
              class="secondary"
              @click="clearDone()"
              :disabled="doneCount === 0"
            >
              Supprimer done
            </button>
          </div>
        </div>

        <!-- Liste -->
        <ul class="stack" x-show="filteredTodos.length > 0" x-cloak>
          <template x-for="todo in filteredTodos" :key="todo.id">
            <li
              x-transition:enter="fade-enter"
              x-transition:enter-start="fade-enter"
              x-transition:enter-end="fade-enter-to"
              x-transition:leave="fade-leave"
              x-transition:leave-start="fade-leave"
              x-transition:leave-end="fade-leave-to"
            >
              <div class="todo-left">
                <input
                  type="checkbox"
                  x-model="todo.done"
                  :aria-label="`Marquer ${todo.label} comme terminée`"
                />

                <span
                  class="todo-text"
                  :class="{ 'done': todo.done }"
                  x-text="todo.label"
                ></span>
              </div>

              <button type="button" class="secondary" @click="removeTodo(todo.id)">
                Supprimer
              </button>
            </li>
          </template>
        </ul>

        <!-- Empty state -->
        <p x-show="filteredTodos.length === 0" x-cloak class="muted">
          Aucun résultat avec ce filtre / cette recherche.
        </p>
      </div>
    </div>

    <script>
      function todoAdvanced() {
        return {
          // Input ajout
          newTodo: "",

          // Recherche (input brut) + query appliquée
          searchInput: "",
          searchQuery: "",

          // Filtre
          filter: "all", // all | active | done

          // Data
          todos: [
            { id: 1, label: "Comprendre x-model", done: true },
            { id: 2, label: "Faire la Todo simple", done: true },
            { id: 3, label: "Apprendre @click.outside", done: false },
            { id: 4, label: "Maîtriser debounce / throttle", done: false },
          ],
          nextId: 5,

          // Stats (getters)
          get totalCount() {
            return this.todos.length;
          },

          get doneCount() {
            return this.todos.filter((t) => t.done).length;
          },

          get activeCount() {
            return this.todos.filter((t) => !t.done).length;
          },

          // Liste filtrée finale (filtre + recherche)
          get filteredTodos() {
            // 1) base selon filtre
            let list = [...this.todos];

            if (this.filter === "active") {
              list = list.filter((t) => !t.done);
            } else if (this.filter === "done") {
              list = list.filter((t) => t.done);
            }

            // 2) recherche
            const q = this.searchQuery.trim().toLowerCase();
            if (q.length > 0) {
              list = list.filter((t) => t.label.toLowerCase().includes(q));
            }

            return list;
          },

          // Actions
          addTodo() {
            const label = this.newTodo.trim();
            if (label.length === 0) return;

            // Anti-doublon simple (insensible à la casse)
            const exists = this.todos.some(
              (t) => t.label.toLowerCase() === label.toLowerCase()
            );
            if (exists) return;

            this.todos.push({
              id: this.nextId++,
              label,
              done: false,
            });

            this.newTodo = "";
          },

          removeTodo(id) {
            this.todos = this.todos.filter((t) => t.id !== id);
          },

          clearDone() {
            this.todos = this.todos.filter((t) => !t.done);
          },

          markAllDone() {
            this.todos = this.todos.map((t) => ({ ...t, done: true }));
          },

          setFilter(value) {
            this.filter = value;
          },

          applySearch() {
            // Ici le debounce fait le job.
            // On applique la query seulement après que l'utilisateur ait "terminé" de taper.
            this.searchQuery = this.searchInput;
          },

          resetSearch() {
            this.searchInput = "";
            this.searchQuery = "";
          },
        };
      }
    </script>
  </body>
</html>
```

---

## 3) Explication formateur (pour comprendre le design)

### Pourquoi on a `searchInput` ET `searchQuery` ?

Parce que c’est un pattern très propre :

* `searchInput` = ce que l’utilisateur tape instantanément
* `searchQuery` = la valeur “validée” après debounce

Donc tu peux :

* taper librement
* et le filtrage ne se déclenche qu’après 300ms

C’est exactement l’idée de debounce.

---

## 4) Pourquoi on filtre dans un getter `filteredTodos` ?

Parce que ça centralise la logique.

Tu ne veux pas :

* filtrer dans le HTML
* filtrer dans 3 endroits différents

Le getter `filteredTodos` fait :

1. filtre (All/Active/Done)
2. recherche

Et l’UI affiche simplement le résultat.

---

## 5) Transitions : comment ça marche ici ?

On utilise `x-transition` sur chaque `<li>`.

Quand un élément apparaît/disparaît, Alpine applique les classes.

Tu as :

* enter-start → invisible + léger déplacement
* enter-end → visible
* leave-start → visible
* leave-end → invisible

Résultat : animation propre sans framework lourd.

---

## 6) Pièges fréquents dans cet atelier

### Piège A — oublier `:key`

Sans clé stable, tu peux avoir :

* checkbox qui se mélange
* animations qui glitch

Ici on a `:key="todo.id"` donc c’est clean.

### Piège B — recherche trop agressive

Sans debounce, tu recalcules tout à chaque frappe.

Sur 2000 items, tu peux sentir le lag.

### Piège C — doublons

Une todo list qui accepte 15 fois “Acheter du lait” devient inutile.

Ici on empêche les doublons (simple mais efficace).

---

## 7) Exercices (obligatoires)

### Exercice 1 — Ajoute un bouton “Tout décocher”

* désactive si `doneCount === 0`

### Exercice 2 — Ajoute un compteur “Résultats affichés”

Tu veux afficher :

* “Résultats : X”

Indice : `filteredTodos.length`

### Exercice 3 — Ajoute une priorité (facile)

Chaque todo a une priorité :

* low / medium / high

Tu ajoutes un select à l’ajout :

* la todo stocke `priority`
* tu affiches un badge

---

## 8) Ce qu’on vient de valider (niveau compétence)

À ce stade tu sais :

* gérer une vraie UI réactive
* filtrer proprement une liste
* faire une recherche performante
* ajouter une animation simple
* structurer ton code de façon maintenable

Tu es prêt pour le **Bloc 2** (x-if, x-for, key, etc.) et surtout pour construire des UI plus “app”.

---

### Étape suivante logique

On passe au **Chapitre 5 — Rendu dynamique (conditions & listes)**

* Leçon 1 : `x-if` vs `x-show` (choix stratégique DOM/perf/UX)
* Leçon 2 : `x-for` propre (listes)
* Leçon 3 : `:key` obligatoire
* Leçon 4 : tri / filtre / recherche (patterns)

Quand tu me dis “go”, j’attaque Chapitre 5, Leçon 1.
